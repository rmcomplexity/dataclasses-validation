import logging
from abc import ABC, abstractmethod, ABCMeta
from typing import Any, get_origin, get_args, get_type_hints

LOG = logging.getLogger(__name__)

class _MISSING_TYPE:
    pass

MISSING = _MISSING_TYPE()

class Field(ABC):
    """Abstract Field class.

    Every field should inherit this class, even user defined fields.

    By default every field can have a default and an optional flag.
    
    If `optional` is set to true and no default value is given,
    `default` is set to `None`.

    If `default` is set, `optional` is automatically set to `True`.
    """
    __slots__ = (
        'optional', 'use_private_attr', 'default',
        'public_attr_name', 'private_attr_name', '_stored_value',
        '_annotation'
    )

    # Type to verify value set.
    TYPES: tuple = (None, )

    def __init__(
        self,
        default: Any=MISSING,
        optional: bool=False,
        use_private_attr: bool=False
    ) -> None:
        self.optional = optional
        self.use_private_attr = use_private_attr
        if optional and default is MISSING:
           default = None

        if not optional and default is not MISSING:
            self.optional = True

        self.default = default
        self._stored_value = None
        self._annotation = None

    def __set_name__(self, owner: Any, name: str) -> None:
        """Store necessary values."""
        self.public_attr_name = name
        self.private_attr_name = f"_{name}"
        self._annotation = get_type_hints(owner).get(name, None)
        self._get_annotation_valid_classes()

    def __get__(self, obj: Any, objtype: Any=None) -> Any:
        """Get value.

        `MISSING` is used as a sentinel to identify when a value has not been set.
        """
        value: Any = self._get_value(obj)

        self._check_value_has_been_set_or_optional(value)

        value = self._compute_default_value(value)

        return value

    def __set__(self, obj: Any, value: Any) -> None:
        """Set value to private attribute.

        Validation and transformation happen here.
        A `transform` method will be called on the value.
        After `transform` a `validate` method will be called on the transformed value.

        Custom fields MUST implement `validate` but `transform` is optional.

        If a field is marked as optional and it has a value of None, no validation is run.
        """
        value = self._compute_default_value(value)

        if not self._check_value_is_optional_none(value):
            value = self.transform(value)
            self.validate(value)

        self._set_value(obj, value)

    @abstractmethod
    def validate(self, value: Any) -> None:
        """Every field should implement this method."""
        raise NotImplemented

    def transform(self, value: Any) -> Any:
        """Implement if you want to transform value after validation."""
        return value

    def _get_value(self, obj: Any) -> Any:
        """Retrieve value from object.

        If `use_private_attr` the value will be read from `_{public_attr_name}`.
        Else the value will be read from `{public_attr_name}`.
        """
        if self.use_private_attr:
            return getattr(obj, self.private_attr_name, MISSING)

        if hasattr(obj, "__dict__"):
            return obj.__dict__.get(self.public_attr_name, MISSING)

        return MISSING

    def _set_value(self, obj: Any, value: Any) -> Any:
        """Set value to attribute in object.

        If `use_private_attr` the value will be set to `_{public_attr_name}`.
        Else the value will be set to `{public_attr_name}`.
        """
        if self.use_private_attr:
            setattr(obj, self.private_attr_name, value)
        else:
            obj.__dict__[self.public_attr_name] = value

    def _check_type(self, value: Any) -> None:
        types = self._get_annotation_valid_classes()
        if not isinstance(value, types):
            raise TypeError(
                f"Value ({value}) set to field {self.public_attr_name} "
                f"must be of type {types} and not {type(value)}."
            )

    def _validate_optional(self, value:Any) -> None:
        if not self.optional and value is None:
            raise ValueError(f"{self.public_attr_name} cannot be 'None'.")

    def _check_value_is_optional_none(self, value:Any) -> bool:
        """Check if value of attribute is 'None' and CAN be none."""
        if self.optional and value is None:
            return True

        return False

    def _check_value_has_been_set_or_optional(self, value: Any) -> None:
        """Check if value has been set and there is not a default value we can use.

        An `ValueError` will be raised if the value has not been set and
        we cannot use a `default` value.
        """
        if not self.optional and value is MISSING and self.default is MISSING:
            raise AttributeError(
                f"Attribute {self.public_attr_name} on object {type(self).__name__} "
                "has not been set."
            )

    def _compute_default_value(self, value: Any) -> Any:
        """Check if we have to return a default value."""
        if self.default is not MISSING and (value is MISSING or value is None):
            value = self.default

        if self.optional and self.default is MISSING:
            value = None

        return value

    def _check_typehint_match_field_types(self, valid_type: Any, hint_arguments: tuple) -> bool:
        """Check if typehint arguments are valid field types.

        A field `TYPES` can appear directly in a typehint argument tuple or
        a typehint argument could be a subclass of a valid field typehint.
        """
        for argument in hint_arguments:
            try:
                type_cls = self._get_annotation_valid_classes(argument)
                if issubclass(type_cls, valid_type):
                    return True
            except TypeError:
                continue
        
        if valid_type in hint_arguments:
            return True

        return False

    def _get_annotation_valid_classes(self, type_hint: Any=MISSING):
        """Get origin class or type for field type hint.

        If the type hint has arguments then we want to focus on those because
        that is waht we can use to check for an obj type unless
        the type hint origin is already a built-in type.

        If `get_origin` returns `None` it means we could have a built-in type already.
        """
        if type_hint is MISSING:
            type_hint = self._annotation

        origin = get_origin(type_hint)
        hint_arguments = get_args(type_hint)

        if (origin is None and
            (type_hint in self.TYPES or
             any([issubclass(type_hint, valid_type) for valid_type in self.TYPES]))):
            return type_hint

        elif origin is not None and origin in self.TYPES:
            return origin

        elif type(origin) is not type and any(
            [
                self._check_typehint_match_field_types(valid_type, hint_arguments)
                for valid_type in self.TYPES
            ]
        ):
            return hint_arguments

        raise TypeError(
            f"Attribute '{self.public_attr_name}' has an invalid type hint of '{self._annotation}' ."
            f"Type hint should be '{self.TYPES}' or a subclass."
        )


    def __str__(self):
        ret = f"{self.__class__.__name__}("
        attrs = []
        for attribute_name in self.__slots__:
            val = getattr(self, attribute_name, MISSING)
            if val is MISSING:
                continue
            attrs.append(f"{attribute_name}={val}")

        return f"{self.__class__.__name__}({', '.join(attrs)})"

    def __repr__(self):
        return self.__str__()
