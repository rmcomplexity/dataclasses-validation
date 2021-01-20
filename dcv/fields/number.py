from typing import Optional, Union, cast
from decimal import Decimal
from dcv.fields import Field, MISSING

class NumberField(Field):
    """Field validation for number values."""
    ERROR_MSGS = {
        "nan": "'{attr_name}' value '{value}' is not a number.",
        "gt": "'{attr_name}' value '{value}' must be greater than {limit}.",
        "lt": "'{attr_name}' value '{value}' must be less than {limit}.",
        "ge": "'{attr_name}' value '{value}' must be greater than or equals to {limit}.",
        "le": "'{attr_name}' value '{value}' must be less than or equals to {limit}.",
    }
    TYPE = (int, float, complex, Decimal)

    def __init__(
        self,
        default: Union[int, float, complex, Decimal, None] = cast(int, MISSING),
        optional: bool=False,
        use_private_attr: bool=False,
        gt: Union[int, float, complex, Decimal, None] = None,
        lt: Union[int, float, complex, Decimal, None] = None,
        ge: Union[int, float, complex, Decimal, None] = None,
        le: Union[int, float, complex, Decimal, None] = None
    ):
        super().__init__(
            default=default,
            optional=optional,
            use_private_attr=use_private_attr
        )
        self.gt = gt
        self.lt = lt
        self.ge = ge
        self.le = le

    def validate(self, value: Union[int, float, complex, Decimal, None]) -> None:
        self._validate_optional(value)

        self._check_type(value)

        if self.gt is not None:
            self._validate_gt(value, self.gt)

        if self.lt is not None:
            self._validate_lt(value, self.lt)

        if self.ge is not None:
            self._validate_ge(value, self.ge)

        if self.le is not None:
            self._validate_le(value, self.le)

    def _validate_gt(
        self,
        value: Union[int, float, complex, Decimal],
        limit: Union[int, float, complex, Decimal]
    ):
        if not value > limit:
            raise ValueError(
                self.ERROR_MSGS["gt"].format(
                    attr_name=self.public_attr_name,
                    value=value,
                    limit=limit
                )
            )

    def _validate_lt(
        self,
        value: Union[int, float, complex, Decimal],
        limit: Union[int, float, complex, Decimal]
    ):
        if not value < limit:
            raise ValueError(
                self.ERROR_MSGS["lt"].format(
                    attr_name=self.public_attr_name,
                    value=value,
                    limit=limit
                )
            )

    def _validate_ge(
        self,
        value: Union[int, float, complex, Decimal],
        limit: Union[int, float, complex, Decimal]
    ):
        if not value >= limit:
            raise ValueError(
                self.ERROR_MSGS["ge"].format(
                    attr_name=self.public_attr_name,
                    value=value,
                    limit=limit
                )
            )

    def _validate_le(
        self,
        value: Union[int, float, complex, Decimal],
        limit: Union[int, float, complex, Decimal]
    ):
        if not value <= limit:
            raise ValueError(
                self.ERROR_MSGS["le"].format(
                    attr_name=self.public_attr_name,
                    value=value,
                    limit=limit
                )
            )


class IntField(NumberField):
    TYPE = int


class FloatField(NumberField):
    TYPE = float


class DecimalField(NumberField):
    TYPE = Decimal


class ComplexField(NumberField):
    """Complex numbers cannot be compared."""

    TYPE = complex

    def __init__(
        self,
        default: Optional[complex] = cast(complex, MISSING),
        optional: bool=False,
        use_private_attr: bool=False
    ):
        super().__init__(
            default=default,
            optional=optional,
            use_private_attr=use_private_attr
        )
