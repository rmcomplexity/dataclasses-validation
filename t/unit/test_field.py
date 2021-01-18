from dataclasses import dataclass, fields, field
import pytest
from typing import Optional, cast
from inspect import signature
from dcv.fields import Field
import types

class MyField(Field):
    """Custom field."""

    def validate(self, value):
        assert value == "x" or value is None


def test_field():
    """Base field.

    GIVEN a custom field
    WHEN a dataclass uses it
    THEN it should run validate method.
    """
    @dataclass
    class T:
        name: str = MyField()

    @dataclass
    class OT:
        name: str = field(default=MyField())

    t = T(name="x")
    assert t.name == "x", "Custom field does not accept a valid string."

    ot = OT(name="x")
    assert ot.name == "x", "Custom field does not accept a valid string."

    with pytest.raises(AssertionError):
        t = T(name="invalid string")

    with pytest.raises(AssertionError):
        ot = T(name="invalid string")


def test_field_optional_with_default():
    """Base field.

    GIVEN a custom field with optional set to `True` and a default value
    WHEN a dataclass uses it
    THEN it should validate correctly.
    """
    @dataclass
    class T:
        name: Optional[str] = MyField(optional=True, default="x")

    t = T()
    assert t.name == "x"

def test_field_optional_no_default():
    """Base field.

    GIVEN a custom field with with optional set to `True` and no default value
    WHEN a dataclass uses it
    THEN it should use `None` as `default`.
    """
    @dataclass
    class T:
        name: Optional[str] = MyField(optional=True)

    @dataclass
    class OT:
        name: Optional[str] = MyField(optional=True)

    t = T()
    assert t.name is None

    ot = OT()
    assert ot.name is None

def test_field_default_and_optional_False():
    """Base field.

    GIVEN a custom field with a `default` value and `optional` set to False.
    WHEN a dataclass uses it
    THEN it should correctly initialize class.
    """
    @dataclass
    class T:
        name: Optional[str] = MyField(default="x")

    @dataclass
    class OT:
        name: Optional[str] = MyField(default="x")

    t = T()
    assert t.name == "x"

    ot = OT()
    assert ot.name == "x"
