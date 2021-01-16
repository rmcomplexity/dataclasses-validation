from dataclasses import dataclass
import pytest
import typing
from dcv.fields import Field

class MyField(Field):
    """Custom field."""

    def validate(self, value):
        assert value == "x"


def test_field():
    """Base field.

    GIVEN a custom field
    WHEN a dataclass uses it
    THEN it should run validate method.
    """
    @dataclass
    class T:
        name: str = typing.cast(str, MyField())

    t = T(name="x")
    assert t.name == "x", "Custom field does not accept a valid string."

    with pytest.raises(AssertionError):
        t = T(name="invalid string")
