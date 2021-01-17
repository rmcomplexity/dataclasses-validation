from dataclasses import dataclass
import pytest
from dcv.fields.text import TextField

def test_str():
    """Str and text fields.

    GIVEN a dataclass with an `str` field and a text validator
    WHEN a valid value is given
    THEN it should validate the input on instantiation
    """
    @dataclass
    class T:
        name: str = TextField()

    t = T(name="valid string")
    assert t.name == "valid string", "Validation does not accept a valid string."

    with pytest.raises(TypeError):
        t = T(name=123)


def test_str_max_length():
    """Str and text fields.

    GIVEN a dataclass with an `str` field and a text validator
    WHEN a valid value is given
    THEN it should validate the input on instantiation
    """
    @dataclass
    class T:
        name: str = TextField(max_length=5)

    t = T(name="names")
    assert t.name == "names"

    with pytest.raises(AttributeError):
        t = T(name="invalid string")


def test_str_min_length():
    """Str and text fields.

    GIVEN a dataclass with an `str` field and a text validator
    WHEN a valid value is given
    THEN it should validate the input on instantiation
    """
    @dataclass
    class T:
        name: str = TextField(min_length=3)

    t = T(name="name")
    assert t.name == "name"

    with pytest.raises(AttributeError):
        t = T(name="x")


def test_str_max_min_length():
    """Str and text fields.

    GIVEN a dataclass with an `str` field and a text validator
    WHEN a valid value is given
    THEN it should validate the input on instantiation
    """
    @dataclass
    class T:
        name: str = TextField(min_length=3, max_length=5)

    t = T(name="names")
    assert t.name == "names"

    with pytest.raises(AttributeError):
        t = T(name="x")

    with pytest.raises(AttributeError):
        t = T(name="invalid string")
