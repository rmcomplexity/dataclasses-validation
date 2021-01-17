from dcv.fields import Field
from typing import Optional
import re

class TextField(Field):
    """Field validation for string values."""
    ERROR_MSGS = {
        "max_length": "{attr_name} length cannot be more than {length}.",
        "min_length": "{attr_name} length cannot be less than {length}.",
        "optional": "{attr_name} must contain a value.",
        "blank": "{attr_name} cannot be blank.",
        "regex": "{attr_name} does not match regex: {regex} .",
    }

    def __init__(
        self,
        default: Optional[str]=None,
        max_length: Optional[int]=None,
        min_length: Optional[int]=None, *,
        optional: bool=False,
        blank: bool=False,
        regex: str=None,
        trim: str=None
    ):
        super().__init__(default, optional)
        self.max_length = max_length
        self.min_length = min_length
        self.optional = optional
        self.blank = blank
        self.trim = trim
        self.regex = None
        if regex:
            self.compiled: re.Pattern = re.compile(regex)

    def validate(self, value: str) -> None:
        self._validate_optional(value)

        self._validate_blank(value)

        if self.max_length is not None:
            self._validate_max_length(value, self.max_length)

        if self.min_length is not None:
            self._validate_min_length(value, self.min_length)

        if self.regex is not None:
            self._validate_regex(value)

    def _validate_max_length(self, value: str, max_length: int) -> None:
        if len(value) > max_length:
            raise AttributeError(
                self.ERROR_MSGS["max_length"].format(
                    attr_name=self.private_attr_name,
                    length=self.max_length
                )
            )

    def _validate_min_length(self, value: str, min_length: int) -> None:
        if len(value) > min_length:
            raise AttributeError(
                self.ERROR_MSGS["min_length"].format(
                    attr_name=self.private_attr_name,
                    length=self.max_length
                )
            )
    def _validate_blank(self, value: str) -> None:
        if not self.blank and not len(value):
            raise AttributeError(self.ERROR_MSGS["blank"].format(attr_name=self.private_attr_name))

    def _validate_regex(self, value: str) -> None:
        if self.regex and not self.compiled.match(value):
            raise AttributeError(
                self.ERROR_MSGS["regex"].format(
                    attr_name=self.private_attr_name,
                    regex=self.regex
               )
            )
