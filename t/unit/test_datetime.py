from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, date, time
from typing import Union
import pytest
from dcv.fields import (
    DateTimeField, TimeDeltaField,
    TimeField, DateField
)


def test_base_datetime():
    """Test DateTimeBaseField

    GIVEN a dataclass with a `Union[datetime, timedelta, date, time]` field
    WHEN a valid value is given
    THEN it should validate the input on init.
    """
    @dataclass
    class T:
        date_time: datetime = DateTimeField()
        time_delta: timedelta = TimeDeltaField()
        date_val: date = DateField()
        time_val: time = TimeField()

    date_time: datetime = datetime(2021, 1, 1, 1, 1, 1)
    time_delta: timedelta = timedelta(days=1)
    date_val: date = date(2021,1,1)
    time_val: time = time(2)
    t = T(
        date_time=date_time,
        time_delta=time_delta,
        date_val=date_val,
        time_val=time_val
    )
    assert t.date_time == date_time
    assert t.time_delta == time_delta
    assert t.date_val == date_val
    assert t.time_val == time_val

    with pytest.raises(TypeError):
        t = T(date_time='asdf',
              time_delta=time_delta,
              date_val=date_val,
              time_val=time_val
        )

    with pytest.raises(TypeError):
        t = T(date_time=date_time,
              time_delta='asdf',
              date_val=date_val,
              time_val=time_val
        )

    with pytest.raises(TypeError):
        t = T(date_time=date_time,
              time_delta=time_delta,
              date_val='asdf',
              time_val=time_val
        )

    with pytest.raises(TypeError):
        t = T(date_time=date_time,
              time_delta=time_delta,
              date_val=date_val,
              time_val='asdf'
        )

def test_datetime_gt():
    """Test datetime fields gt

    GTIVEN a dataclass with a date time field
    WHEN a `gt` limit is set
    THEN any value that's set should be validated correctly
    """
    @dataclass
    class T:
        date_time: datetime = DateTimeField(gt=datetime(2021,1,1))
        time_delta: timedelta = TimeDeltaField(gt=timedelta(hours=1))
        date_val: date = DateField(gt=date(2021,1,1))
        time_val: time = TimeField(gt=time(hour=1))

    valid_dt: datetime = datetime(2021, 2, 2)
    invalid_dt: datetime = datetime(2020, 1, 1)
    valid_td: timedelta = timedelta(hours=2)
    invalid_td: timedelta = timedelta(minutes=50)
    valid_da: date = date(2021,2,2)
    invalid_da: date = date(2020,1,1)
    valid_ti: time = time(hour=2)
    invalid_ti: time = time(hour=0,minute=50)

    t = T(
        date_time=valid_dt,
        time_delta=valid_td,
        date_val=valid_da,
        time_val=valid_ti
    )
    
    assert t.date_time == valid_dt
    assert t.time_delta == valid_td
    assert t.date_val == valid_da
    assert t.time_val == valid_ti

    with pytest.raises(ValueError):
        t = T(
            date_time=invalid_dt,
            time_delta=valid_td,
            date_val=valid_da,
            time_val=valid_ti
        )


    with pytest.raises(ValueError):
        t = T(
            date_time=valid_dt,
            time_delta=invalid_td,
            date_val=valid_da,
            time_val=valid_ti
        )

    with pytest.raises(ValueError):
        t = T(
            date_time=valid_dt,
            time_delta=valid_td,
            date_val=invalid_da,
            time_val=valid_ti
        )

    with pytest.raises(ValueError):
        t = T(
            date_time=valid_dt,
            time_delta=valid_td,
            date_val=valid_da,
            time_val=invalid_ti
        )


def test_datetime_lt():
    """Test datetime fields lt

    GTIVEN a dataclass with a date time field
    WHEN a `lt` limit is set
    THEN any value that's set should be validated correctly
    """
    @dataclass
    class T:
        date_time: datetime = DateTimeField(lt=datetime(2021,1,1))
        time_delta: timedelta = TimeDeltaField(lt=timedelta(hours=1))
        date_val: date = DateField(lt=date(2021,1,1))
        time_val: time = TimeField(lt=time(hour=1))

    valid_dt: datetime = datetime(2020, 2, 2)
    invalid_dt: datetime = datetime(2021, 1, 2)
    valid_td: timedelta = timedelta(minutes=50)
    invalid_td: timedelta = timedelta(hours=2)
    valid_da: date = date(2020,2,2)
    invalid_da: date = date(2021,1,1)
    valid_ti: time = time(hour=0, minute=50)
    invalid_ti: time = time(hour=2)

    t = T(
        date_time=valid_dt,
        time_delta=valid_td,
        date_val=valid_da,
        time_val=valid_ti
    )
    
    assert t.date_time == valid_dt
    assert t.time_delta == valid_td
    assert t.date_val == valid_da
    assert t.time_val == valid_ti

    with pytest.raises(ValueError):
        t = T(
            date_time=invalid_dt,
            time_delta=valid_td,
            date_val=valid_da,
            time_val=valid_ti
        )


    with pytest.raises(ValueError):
        t = T(
            date_time=valid_dt,
            time_delta=invalid_td,
            date_val=valid_da,
            time_val=valid_ti
        )

    with pytest.raises(ValueError):
        t = T(
            date_time=valid_dt,
            time_delta=valid_td,
            date_val=invalid_da,
            time_val=valid_ti
        )

    with pytest.raises(ValueError):
        t = T(
            date_time=valid_dt,
            time_delta=valid_td,
            date_val=valid_da,
            time_val=invalid_ti
        )


def test_datetime_ge():
    """Test datetime fields ge

    GTIVEN a dataclass with a date time field
    WHEN a `ge` limit is set
    THEN any value that's set should be validated correctly
    """
    @dataclass
    class T:
        date_time: datetime = DateTimeField(ge=datetime(2021,1,1))
        time_delta: timedelta = TimeDeltaField(ge=timedelta(hours=1))
        date_val: date = DateField(ge=date(2021,1,1))
        time_val: time = TimeField(ge=time(hour=1))

    valid_dt: datetime = datetime(2021, 1, 1)
    invalid_dt: datetime = datetime(2020, 1, 1)
    valid_td: timedelta = timedelta(hours=1)
    invalid_td: timedelta = timedelta(minutes=50)
    valid_da: date = date(2021,1,1)
    invalid_da: date = date(2020,1,1)
    valid_ti: time = time(hour=1)
    invalid_ti: time = time(hour=0,minute=50)

    t = T(
        date_time=valid_dt,
        time_delta=valid_td,
        date_val=valid_da,
        time_val=valid_ti
    )
    
    assert t.date_time == valid_dt
    assert t.time_delta == valid_td
    assert t.date_val == valid_da
    assert t.time_val == valid_ti

    with pytest.raises(ValueError):
        t = T(
            date_time=invalid_dt,
            time_delta=valid_td,
            date_val=valid_da,
            time_val=valid_ti
        )


    with pytest.raises(ValueError):
        t = T(
            date_time=valid_dt,
            time_delta=invalid_td,
            date_val=valid_da,
            time_val=valid_ti
        )

    with pytest.raises(ValueError):
        t = T(
            date_time=valid_dt,
            time_delta=valid_td,
            date_val=invalid_da,
            time_val=valid_ti
        )

    with pytest.raises(ValueError):
        t = T(
            date_time=valid_dt,
            time_delta=valid_td,
            date_val=valid_da,
            time_val=invalid_ti
        )


def test_datetime_le():
    """Test datetime fields le

    GTIVEN a dataclass with a date time field
    WHEN a `le` limit is set
    THEN any value that's set should be validated correctly
    """
    @dataclass
    class T:
        date_time: datetime = DateTimeField(le=datetime(2021,1,1))
        time_delta: timedelta = TimeDeltaField(le=timedelta(hours=1))
        date_val: date = DateField(le=date(2021,1,1))
        time_val: time = TimeField(le=time(hour=1))

    valid_dt: datetime = datetime(2020, 1, 1)
    invalid_dt: datetime = datetime(2021, 1, 2)
    valid_td: timedelta = timedelta(hours=1)
    invalid_td: timedelta = timedelta(hours=2)
    valid_da: date = date(2020,1,1)
    invalid_da: date = date(2021,1,2)
    valid_ti: time = time(hour=1)
    invalid_ti: time = time(hour=2)

    t = T(
        date_time=valid_dt,
        time_delta=valid_td,
        date_val=valid_da,
        time_val=valid_ti
    )
    
    assert t.date_time == valid_dt
    assert t.time_delta == valid_td
    assert t.date_val == valid_da
    assert t.time_val == valid_ti

    with pytest.raises(ValueError):
        t = T(
            date_time=invalid_dt,
            time_delta=valid_td,
            date_val=valid_da,
            time_val=valid_ti
        )


    with pytest.raises(ValueError):
        t = T(
            date_time=valid_dt,
            time_delta=invalid_td,
            date_val=valid_da,
            time_val=valid_ti
        )

    with pytest.raises(ValueError):
        t = T(
            date_time=valid_dt,
            time_delta=valid_td,
            date_val=invalid_da,
            time_val=valid_ti
        )

    with pytest.raises(ValueError):
        t = T(
            date_time=valid_dt,
            time_delta=valid_td,
            date_val=valid_da,
            time_val=invalid_ti
        )
