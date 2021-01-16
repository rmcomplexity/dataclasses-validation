from dataclasses import dataclass
import pytest
from dcv.fields import text

def test_str():
    """Str and text fields.

    GIVEN a dataclass with an `str` field and a text validator
    WHEN a valid value is given
    THEN it should validate the input on instantiation
    """
    @dataclass
    class T:
        name: str = text()

    t = T(name="valid string")
    assert t.name == "valid string", "Validation does not accept a valid string."

    with pytest.raises(AttributeError):
        t = T(name=123)
