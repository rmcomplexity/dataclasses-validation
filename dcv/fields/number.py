from typing import Optional, Union, cast
from decimal import Decimal
from dcv.fields import Field, MISSING

class NumberField(Field):
    """Field validation for number values."""
    ERROR_MSGS = {
        "nan": "'{attr_name}' value '{value}' is not a number.",
        "min": "'{attr_name}' value '{value}' cannot be less than {min}.",
        "max": "'{attr_name}' value '{value}' cannot be more than {max}.",
    }
    TYPE = (int, float, complex, Decimal)

    def __init__(
        self,
        default: Union[int, float, complex, Decimal, None] = cast(int, MISSING),
        optional: bool=False,
        use_private_attr: bool=False,
        max_limit: Union[int, float, complex, Decimal, None] = None,
        min_limit: Union[int, float, complex, Decimal, None] = None
    ):
        super().__init__(
            default=default,
            optional=optional,
            use_private_attr=use_private_attr
        )
        self.max_limit = max_limit
        self.min_limit = min_limit

    def validate(self, value: Union[int, float, complex, Decimal, None]) -> None:
        self._validate_optional(value)

        self._check_type(value)
