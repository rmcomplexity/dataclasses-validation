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
    TYPE = None

    def __init__(self, default: Any=MISSING, optional: bool=False) -> None:
        """Init base field.

        By default every field can have a default and an optional flag.
        
        If `optional` is set to true and no default value is given,
        `default` is set to `None`.

        If `default` is set but `optional` is automatically set to `True`.
        """
        self.optional = optional
        if optional and default is MISSING:
            self.default = None

        if not optional and default is not MISSING:
            self.optional = True

        self.default = default

    def __set_name__(self, owner: Any, name: str) -> None:
        self.public_attr_name = name
        self.private_attr_name = f"_{name}"

    def __get__(self, obj: Any, objtype: Any=None) -> Any:
        """Get value.

        `MISSING` is used as a sentinel to identify when no `default` value has been set.
        """
        val: Any = getattr(obj, self.private_attr_name, MISSING)

        if val is MISSING and self.default is MISSING:
            raise AttributeError(
                f"Attribute f{self.public_attr_name} on object f{type(self).__name__} "
                "has not been set."
            )

        if val is MISSING and self.default is not MISSING:
            setattr(obj, self.private_attr_name, self.default)
            val = getattr(obj, self.private_attr_name)

        return val

    def __set__(self, obj: Any, value: Any) -> Any:
        """Set value to private attribute.

        Validation and transformation happen here.
        A `validate` method will be called on the value.
        After validation a `transform` method will be called on the validate value.

        Custom fields MUST implement `validate` but `transform` is optional.

        If a field is marked as optional and it has a value of None, no validation is run.
        """
        if self.default is not MISSING and value is None:
            value = self.default

        if not self._check_value_is_optional(value):
            self.validate(value)
        try:
            transform_fn = self.transform
        except AttributeError:
            transform_fn = lambda x: x

        setattr(obj, self.private_attr_name, transform_fn(value))

    def _check_type(self, value: Any) -> None:
        if not isinstance(value, self.TYPE):
            raise TypeError(
                f"Value ({value}) set to field {self.public_attr_name} "
                f"must be of type {self.TYPE} and not {type(value)}"
            )

    @abstractmethod
    def validate(self, value: Any) -> None:
        """Every field should implement this method."""
        raise NotImplemented

    def transform(self, value: Any) -> Any:
        """Implement if you want to transform value after validation."""
        return value

    def _validate_optional(self, value:Any) -> bool:
        if not self.optional and value is None:
            raise AttributeError(f"{self.public_attr_name} cannot be 'None'.")

    def _check_value_is_optional(self, value:Any) -> bool:
        """Check if value of attribute is 'None' and CAN be none."""
        if self.optional and value is None:
            return True

        return False
