from dcv.fields import Field, MISSING
from typing import Optional, Union, cast


class BoolField(Field):
    """Field validation for bool values."""

    ERROR_MSGS = {}
    TYPES = (bool, )

    def __init__(
        self,
        default: Optional[bool] = cast(bool, MISSING),
        optional: bool=False,
        use_private_attr: bool=False
    ):
        super().__init__(
            default=default,
            optional=optional,
            use_private_attr=use_private_attr
        )

    def validate(self, value: bool) -> None:
        self._validate_optional(value)

        self._check_type(value)
