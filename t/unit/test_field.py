from dataclasses import dataclass, fields, field
import pytest
from typing import Optional, cast, List
from inspect import signature
from dcv.fields import Field
import types

class MyField(Field):
    """Custom field."""
    TYPES = (str, )

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
        last_name: str = field(default=MyField(), init=False)

    @dataclass
    class OT:
        name: str = field(default=MyField())

    t = T(name="x")
    t.last_name = "x"
    assert t.name == "x", "Custom field does not accept a valid string."
    assert t.last_name == "x"

    ot = OT(name="x")
    assert ot.name == "x", "Custom field does not accept a valid string."

    with pytest.raises(AssertionError):
        t = T(name="invalid string")

    with pytest.raises(AssertionError):
        ot = T(name="invalid string")

    with pytest.raises(AssertionError):
        t.last_name = "asdf"


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


def test_field_use_private_attr():
    """Base field.

    GIVEN a custom field with a `default` value and `optional` set to False.
    WHEN a dataclass uses it
    THEN it should correctly initialize class.
    """
    @dataclass
    class T:
        name: str = MyField(use_private_attr=True)

    @dataclass
    class OT:
        name: str = MyField(use_private_attr=True)

    t = T(name="x")
    assert t.name == "x"
    assert t.__dict__["_name"] == "x"
    assert ("name" in t.__dict__) == False

    ot = OT(name="x")
    assert ot.name == "x"
    assert ot.__dict__["_name"] == "x"
    assert ("name" in ot.__dict__) == False


def test_field_with_wrong_typehint():
    """Base field.

    GIVEN a custom field with a defined tuple of supported types
    WHEN a dataclass uses it in a field with the wrong typehint
    THEN it should raise a TypeError
    """
    with pytest.raises(RuntimeError):
        @dataclass
        class T:
            name: int = MyField()

    with pytest.raises(RuntimeError):
        @dataclass
        class T:
            name: Optional[int] = MyField()

    with pytest.raises(RuntimeError):
        @dataclass
        class T:
            name: List[str] = MyField()

    class S(str):
        pass

    @dataclass
    class T:
        name: S = MyField()

    assert isinstance(vars(T)['name'], MyField)
