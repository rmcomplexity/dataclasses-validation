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
