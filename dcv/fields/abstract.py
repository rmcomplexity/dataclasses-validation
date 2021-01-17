from abc import ABC, abstractmethod
from typing import Any

class Field(ABC):
    """Abstract Field class.

    Every field should inherit this class, even user defined fields.
    """
    def __set_name__(self, owner: Any, name: str) -> None:
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
        self._validate(value)
        try:
            transform_fn = self.transform
        except AttributeError:
            transform_fn = lambda x: x

        setattr(obj, self.private_attr_name, transform_fn(value))

    @abstractmethod
    def validate(self, value: Any) -> None:
        """Every field should implement this method."""
        raise NotImplemented
