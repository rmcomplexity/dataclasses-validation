from dcv.fields import Field, MISSING
from typing import Optional, Union, cast
from datetime import datetime, timedelta, date, time

class DateTimeBaseField(Field):
    """Datetime field validation."""
    __slots__ = ('gt', 'lt', 'ge', 'le')

    ERROR_MSGS = {
        "gt": "'{attr_name}' value '{value}' must be greater than {limit}.",
        "lt": "'{attr_name}' value '{value}' must be less than {limit}.",
        "ge": "'{attr_name}' value '{value}' must be greater than or equals to {limit}.",
        "le": "'{attr_name}' value '{value}' must be less than or equals to {limit}.",
    }
    TYPES = (datetime, timedelta, date, time)

    def __init__(
        self,
        default: Optional[datetime] = cast(datetime, MISSING),
        optional: bool=False,
        use_private_attr: bool=False,
        gt: Union[datetime, timedelta, date, time, None]=None,
        lt: Union[datetime, timedelta, date, time, None]=None,
        ge: Union[datetime, timedelta, date, time, None]=None,
        le: Union[datetime, timedelta, date, time, None]=None
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

    def validate(self, value: Union[datetime, timedelta, date, time, None]) -> None:
        self._validate_optional(value)

        self._check_type(value)

        if self.gt is not None:
            self._validate_gt(value, self.gt)

        if self.lt is not None:
            self._validate_ge(value, self.lt)

        if self.ge is not None:
            self._validate_ge(value, self.ge)

        if self.le is not None:
            self._validate_le(value, self.le)

    def _validate_gt(
        self,
        value: Union[datetime, timedelta, date, time],
        limit: Union[datetime, timedelta, date, time]
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
        value: Union[datetime, timedelta, date, time],
        limit: Union[datetime, timedelta, date, time]
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
        value: Union[datetime, timedelta, date, time],
        limit: Union[datetime, timedelta, date, time]
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
        value: Union[datetime, timedelta, date, time],
        limit: Union[datetime, timedelta, date, time]
    ):
        if not value <= limit:
            raise ValueError(
                self.ERROR_MSGS["le"].format(
                    attr_name=self.public_attr_name,
                    value=value,
                    limit=limit
                )
            )

    def _check_limits_type(self):
        """Verify the values given as limits match the field type."""
        for limit_attr_name in ["gt", "lt", "ge", "le"]:
            self._check_type(getattr(self, limit_attr_name))


class DateTimeField(DateTimeBaseField):
    TYPES = (datetime,)


class TimeDeltaField(DateTimeBaseField):
    TYPES = (timedelta,)


class DateField(DateTimeBaseField):
    TYPES = (date,)


class TimeField(DateTimeBaseField):
    TYPES = (time,)
