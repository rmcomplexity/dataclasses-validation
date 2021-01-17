from abc import ABC, abstractmethod
from typing import Any

class Field(ABC):
    """Abstract Field class.

    Every field should inherit this class, even user defined fields.
    """

    # Type to verify value set.
    TYPE = None

    def __init__(self, default: Any=None, optional: bool=False) -> None:
        self.default = default
        self.optional = optional

    def __set_name__(self, owner: Any, name: str) -> None:
        self.public_attr_name = name
        self.private_attr_name = f"_{name}"

    def __get__(self, obj: Any, objtype: Any=None) -> Any:
        return getattr(obj, self.private_attr_name)

    def __set__(self, obj: Any, value: Any) -> Any:
        """Set value to private attribute.

        Validation and transformation happen here.
        A `validate` method will be called on the value.
        After validation a `transform` method will be called on the validate value.

        Custom fields MUST implement `validate` but `transform` is optional.
        """
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

    def _validate_optional(self, value:Any) -> None:
        if not self.optional and value is None:
            raise AttributeError(f"{self.public_attr_name} cannot be 'None'.")
