import logging
from abc import ABC, abstractmethod
from typing import Any

LOG = logging.getLogger(__name__)

class _MISSING_TYPE:
    pass

MISSING = _MISSING_TYPE()

class Field(ABC):
    """Abstract Field class.

    Every field should inherit this class, even user defined fields.
    """

    # Type to verify value set.
    TYPE: Any = None

    def __init__(
        self,
        default: Any=MISSING,
        optional: bool=False,
        use_private_attr: bool=False
    ) -> None:
        """Init base field.

        By default every field can have a default and an optional flag.
        
        If `optional` is set to true and no default value is given,
        `default` is set to `None`.

        If `default` is set but `optional` is automatically set to `True`.
        """
        self.optional = optional
        self.use_private_attr = use_private_attr
        if optional and default is MISSING:
           default = None

        if not optional and default is not MISSING:
            self.optional = True

        self.default = default

    def __set_name__(self, owner: Any, name: str) -> None:
        self.public_attr_name = name
        self.private_attr_name = f"_{name}"

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
        A `validate` method will be called on the value.
        After validation a `transform` method will be called on the validate value.

        Custom fields MUST implement `validate` but `transform` is optional.

        If a field is marked as optional and it has a value of None, no validation is run.
        """
        value = self._compute_default_value(value)

        if not self._check_value_is_optional_none(value):
            self.validate(value)

        value = self.transform(value)

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
        if not isinstance(value, self.TYPE):
            raise TypeError(
                f"Value ({value}) set to field {self.public_attr_name} "
                f"must be of type {self.TYPE} and not {type(value)}"
            )

    def _validate_optional(self, value:Any) -> None:
        if not self.optional and value is None:
            raise AttributeError(f"{self.public_attr_name} cannot be 'None'.")

    def _check_value_is_optional_none(self, value:Any) -> bool:
        """Check if value of attribute is 'None' and CAN be none."""
        if self.optional and value is None:
            return True

        return False

    def _check_value_has_been_set_or_optional(self, value: Any) -> None:
        """Check if value has been set and there is not a default value we can use.

        An `AttributeError` will be raised if the value has not been set and
        we cannot use a `default` value.
        """
        if not self.optional and value is MISSING and self.default is MISSING:
            raise AttributeError(
                f"Attribute f{self.public_attr_name} on object f{type(self).__name__} "
                "has not been set."
            )

    def _compute_default_value(self, value: Any) -> Any:
        """Check if we have to return a default value."""
        if self.default is not MISSING and (value is MISSING or value is None):
            value = self.default

        if self.optional and self.default is MISSING:
            value = None

        return value
