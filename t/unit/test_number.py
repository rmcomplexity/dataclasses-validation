from dataclasses import dataclass, field
from decimal import Decimal
from typing import Union
import pytest
from dcv.fields.number import NumberField

def test_numbers():
    """Test all number types.

    GIVEN a dataclass with a `Union[int, float, complex, Decimal]` field
    WHEN a valid value is given
    THEN it should validate the input on init.
    """
    @dataclass
    class T:
        num: Union[int, float, complex, Decimal] = NumberField()
        second_num: Union[int, float, complex, Decimal] = field(default=NumberField())

    t = T(num=1, second_num=1)
    assert t.num == 1
    assert t.second_num == 1

    t = T(num=1.0, second_num=1.0)
    assert t.num == 1.0
    assert t.second_num == 1.0

    t = T(num=complex("1+2j"), second_num=1+2j)
    assert t.num == 1+2j
    assert t.second_num == 1+2j

    t = T(num=Decimal("1.0"), second_num=Decimal(1.0))
    assert t.num == Decimal("1.0")
    assert t.second_num == Decimal("1.0")

    with pytest.raises(TypeError):
        T(num="asdf")

    with pytest.raises(TypeError):
        T(second_num={})

    with pytest.raises(TypeError):
        T(num=[])
