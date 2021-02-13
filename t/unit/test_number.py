from dataclasses import dataclass, field
from decimal import Decimal
from typing import Union
import pytest
from dcv.fields import NumberField, ComplexField

def test_numbers():
    """Test all number types.

    GIVEN a dataclass with a `Union[int, float, complex, Decimal]` field
    WHEN a valid value is given
    THEN it should validate the input on init.
    """
    @dataclass
    class T:
        co_num: complex = ComplexField()
        num: Union[int, float, complex, Decimal] = NumberField()
        second_co_num: complex = field(default=ComplexField())
        second_num: Union[int, float, complex, Decimal] = field(default=NumberField())

    t = T(num=1, second_num=1, co_num=1+2j, second_co_num=1+2j)
    assert t.num == 1
    assert t.second_num == 1
    assert t.co_num == 1+2j
    assert t.second_co_num == 1+2j

    t = T(num=1.0, second_num=1.0, co_num=1+2j, second_co_num=1+2j)
    assert t.num == 1.0
    assert t.second_num == 1.0

    t = T(num=complex("1+2j"), second_num=1+2j, co_num=1+2j, second_co_num=1+2j)
    assert t.num == 1+2j
    assert t.second_num == 1+2j

    t = T(num=Decimal("1.0"), second_num=Decimal(1.0), co_num=1+2j, second_co_num=1+2j)
    assert t.num == Decimal("1.0")
    assert t.second_num == Decimal("1.0")

    with pytest.raises(TypeError):
        T(num="asdf")

    with pytest.raises(TypeError):
        T(second_num={})

    with pytest.raises(TypeError):
        T(num=[])


def test_lt():
    """Test less than.

    GIVEN a dataclass with a `Union[int, float, complex, Decimal]` field and a
        validator with a lt
    WHEN a valid value is given
    THEN it should validate the input on init.
    """
    @dataclass
    class TInt:
        num: Union[int, float, complex, Decimal] = NumberField(lt=3)
        second_num: Union[int, float, complex, Decimal] = field(default=NumberField(lt=3))

    @dataclass
    class TFloat:
        num: Union[int, float, complex, Decimal] = NumberField(lt=3)
        second_num: Union[int, float, complex, Decimal] = field(default=NumberField(lt=3))

    @dataclass
    class TDecimal:
        num: Union[int, float, complex, Decimal] = NumberField(lt=Decimal(3.0))
        second_num: Union[int, float, complex, Decimal] = field(default=NumberField(lt=3))

    t_int = TInt(num=1, second_num=1)
    assert t_int.num == 1
    assert t_int.second_num == 1

    t_float = TFloat(num=1.0, second_num=1.0)
    assert t_float.num == 1.0
    assert t_float.second_num == 1.0

    t_dec = TDecimal(num=Decimal(1.0), second_num=Decimal(1.0))
    assert t_dec.num == 1
    assert t_dec.second_num == 1

    with pytest.raises(ValueError):
        TInt(num=4)

    with pytest.raises(ValueError):
        TFloat(second_num=3.1, num=3.1)

    with pytest.raises(ValueError):
        TDecimal(second_num=Decimal(3.1), num=3.1)


def test_gt():
    """Test gt.

    GIVEN a dataclass with a `Union[int, float, complex, Decimal]` field and a
        validator with a max limit
    WHEN a valid value is given
    THEN it should validate the input on init.
    """
    @dataclass
    class TInt:
        num: Union[int, float, complex, Decimal] = NumberField(gt=3)
        second_num: Union[int, float, complex, Decimal] = field(default=NumberField(gt=3))

    @dataclass
    class TFloat:
        num: Union[int, float, complex, Decimal] = NumberField(gt=3)
        second_num: Union[int, float, complex, Decimal] = field(default=NumberField(gt=3))

    @dataclass
    class TDecimal:
        num: Union[int, float, complex, Decimal] = NumberField(gt=Decimal(3.0))
        second_num: Union[int, float, complex, Decimal] = field(default=NumberField(gt=3))

    t_int = TInt(num=4, second_num=4)
    assert t_int.num == 4 
    assert t_int.second_num == 4

    t_float = TFloat(num=3.1, second_num=3.1)
    assert t_float.num == 3.1
    assert t_float.second_num == 3.1

    t_dec = TDecimal(num=Decimal(3.1), second_num=Decimal(3.1))
    assert t_dec.num == 3.1
    assert t_dec.second_num == 3.1

    with pytest.raises(ValueError):
        TInt(num=3)

    with pytest.raises(ValueError):
        TFloat(second_num=3.0, num=3.0)

    with pytest.raises(ValueError):
        TDecimal(second_num=Decimal(3.0), num=3.0)


def test_le():
    """Test less than or equal.

    GIVEN a dataclass with a `Union[int, float, complex, Decimal]` field and a
        validator with le
    WHEN a valid value is given
    THEN it should validate the input on init.
    """
    @dataclass
    class TInt:
        num: Union[int, float, complex, Decimal] = NumberField(le=3)
        second_num: Union[int, float, complex, Decimal] = field(default=NumberField(le=3))

    @dataclass
    class TFloat:
        num: Union[int, float, complex, Decimal] = NumberField(le=3)
        second_num: Union[int, float, complex, Decimal] = field(default=NumberField(le=3))

    @dataclass
    class TDecimal:
        num: Union[int, float, complex, Decimal] = NumberField(le=Decimal(3.0))
        second_num: Union[int, float, complex, Decimal] = field(default=NumberField(le=3))

    t_int = TInt(num=3, second_num=2)
    assert t_int.num == 3 
    assert t_int.second_num == 2

    t_float = TFloat(num=2.9, second_num=3.0)
    assert t_float.num == 2.9
    assert t_float.second_num == 3.0

    t_dec = TDecimal(num=Decimal(2.9), second_num=Decimal(3.0))
    assert t_dec.num == 2.9
    assert t_dec.second_num == 3.0

    with pytest.raises(ValueError):
        TInt(num=4)

    with pytest.raises(ValueError):
        TFloat(second_num=3.1, num=3.0)

    with pytest.raises(ValueError):
        TDecimal(second_num=Decimal(3.0), num=3.1)


def test_le():
    """Test less than or equal.

    GIVEN a dataclass with a `Union[int, float, complex, Decimal]` field and a
        validator with le
    WHEN a valid value is given
    THEN it should validate the input on init.
    """
    @dataclass
    class TInt:
        num: Union[int, float, complex, Decimal] = NumberField(le=3)
        second_num: Union[int, float, complex, Decimal] = field(default=NumberField(le=3))

    @dataclass
    class TFloat:
        num: Union[int, float, complex, Decimal] = NumberField(le=3)
        second_num: Union[int, float, complex, Decimal] = field(default=NumberField(le=3))

    @dataclass
    class TDecimal:
        num: Union[int, float, complex, Decimal] = NumberField(le=Decimal(3.0))
        second_num: Union[int, float, complex, Decimal] = field(default=NumberField(le=3))

    t_int = TInt(num=3, second_num=2)
    assert t_int.num == 3 
    assert t_int.second_num == 2

    t_float = TFloat(num=2.9, second_num=3.0)
    assert t_float.num == 2.9
    assert t_float.second_num == 3.0

    t_dec = TDecimal(num=Decimal(2.9), second_num=Decimal(3.0))
    assert t_dec.num == 2.9
    assert t_dec.second_num == 3.0

    with pytest.raises(ValueError):
        TInt(num=4)

    with pytest.raises(ValueError):
        TFloat(second_num=3.1, num=3.0)

    with pytest.raises(ValueError):
        TDecimal(second_num=Decimal(3.0), num=3.1)
