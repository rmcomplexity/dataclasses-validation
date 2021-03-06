from dcv.fields import Field, MISSING
from typing import Optional, Union, cast
import re

class TextField(Field):
    """Field validation for string values."""
    __slots__ = ('max_length', 'min_length', 'blank', 'trim', 'regex', 'compiled')

    ERROR_MSGS = {
        "max_length": "'{attr_name}' length cannot be more than {length}.",
        "min_length": "'{attr_name}' length cannot be less than {length}.",
        "blank": "'{attr_name}' cannot be blank.",
        "regex": "'{attr_name}' does not match regex: {regex} .",
    }
    TYPES = (str, bytes)

    def __init__(
        self,
        default: Optional[str] = cast(str, MISSING),
        optional: bool=False,
        use_private_attr: bool=False,
        max_length: Optional[int]=None,
        min_length: Optional[int]=None, *,
        blank: bool=False,
        regex: Optional[str]=None,
        trim: Union[str, bool]=False
    ):
        super().__init__(
            default=default,
            optional=optional,
            use_private_attr=use_private_attr
        )
        self.max_length = max_length
        self.min_length = min_length
        self.blank = blank
        self.trim = trim
        self.regex = None
        if regex:
            self.regex = regex
            self.compiled: re.Pattern = re.compile(regex)

    def validate(self, value: str) -> None:
        self._validate_optional(value)

        self._check_type(value)

        self._validate_blank(value)

        if self.max_length is not None:
            self._validate_max_length(value, self.max_length)

        if self.min_length is not None:
            self._validate_min_length(value, self.min_length)

        if self.regex is not None:
            self._validate_regex(value)

    def transform(self, value: str) -> str:
        if self.trim is True:
            return value.strip()
        elif isinstance(self.trim, str):
            return value.strip(self.trim)

        return value

    def _validate_max_length(self, value: str, max_length: int) -> None:
        if len(value) > max_length:
            raise ValueError(
                self.ERROR_MSGS["max_length"].format(
                    attr_name=self.public_attr_name,
                    length=self.max_length
                )
            )

    def _validate_min_length(self, value: str, min_length: int) -> None:
        if len(value) < min_length:
            raise ValueError(
                self.ERROR_MSGS["min_length"].format(
                    attr_name=self.public_attr_name,
                    length=self.min_length
                )
            )
    def _validate_blank(self, value: str) -> None:
        if not self.blank and not len(value):
            raise ValueError(self.ERROR_MSGS["blank"].format(attr_name=self.public_attr_name))

    def _validate_regex(self, value: str) -> None:
        if self.regex and not self.compiled.match(value):
            raise ValueError(
                self.ERROR_MSGS["regex"].format(
                    attr_name=self.public_attr_name,
                    regex=self.regex
               )
            )

