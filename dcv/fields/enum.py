from dcv.fields import Field, MISSING
from typing import Optional, Union, cast
from enum import Enum

class EnumField(Field):
    """Field validation for enum values."""

    ERROR_MSGS = {
        "parse": "'{attr_name}' value '{value}' cannot be parsed as '{enum_cls}'"
    }
    TYPES = (Enum, )

    def __init__(
        self,
        default: Optional[Enum] = cast(Enum, MISSING),
        optional: bool=False,
        use_private_attr: bool=False
    ):
        super().__init__(
            default=default,
            optional=optional,
            use_private_attr=use_private_attr
        )

    def validate(self, value: Enum) -> None:
        self._validate_optional(value)

        self._check_type(value)
