from dataclasses import dataclass, field
import pytest
from dcv.fields import TextField

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
    """Max length.

    GIVEN a dataclass with an `str` field and a text validator with max_length
    WHEN a valid value is given
    THEN it should validate the input on instantiation
    """
    @dataclass
    class T:
        name: str = TextField(max_length=5)

    t = T(name="names")
    assert t.name == "names"

    with pytest.raises(ValueError):
        t = T(name="invalid string")


def test_str_min_length():
    """Min length.

    GIVEN a dataclass with an `str` field and a text validator with min_length
    WHEN a valid value is given
    THEN it should validate the input on instantiation
    """
    @dataclass
    class T:
        name: str = TextField(min_length=3)

    t = T(name="name")
    assert t.name == "name"

    with pytest.raises(ValueError):
        t = T(name="x")


def test_str_max_min_length():
    """Max and min.

    GIVEN a dataclass with an `str` field and a text validator with min and max length
    WHEN a valid value is given
    THEN it should validate the input on instantiation
    """
    @dataclass
    class T:
        name: str = TextField(min_length=3, max_length=5)

    t = T(name="names")
    assert t.name == "names"
    
    with pytest.raises(ValueError):
        t = T(name="x")

    with pytest.raises(ValueError):
        t = T(name="invalid string")

def test_str_blank():
    """blank paremeter

    GIVEN a dataclass with an `str` field and a text validator with blank=True
    WHEN a valid value is given
    THEN it should validate the input on instantiation
    """
    @dataclass
    class T:
        name: str = TextField(blank=True)

    t = T(name="")
    assert t.name == ""

    with pytest.raises(ValueError):
        t = T(name=None)

def test_str_trim():
    """trim paremeter

    GIVEN a dataclass with an `str` field and a text validator with trim
    WHEN a valid value is given
    THEN it should transform the value
    """
    @dataclass
    class T:
        name: str = TextField(trim=" ")

    t = T(name="    A    ")
    assert t.name == "A"

def test_str_regex():
    """regex parameter

    GIVEN a dataclass with an `str` field and a text validator with trim
    WHEN a valid value is given
    THEN it should transform the value
    """
    @dataclass
    class T:
        name: str = TextField(regex="^[aA]")

    t = T(name="arturo")
    assert t.name == "arturo"
    t1 = T(name="Arturo")
    assert t1.name == "Arturo"
    with pytest.raises(ValueError):
        t2 = T(name="Pedro")
