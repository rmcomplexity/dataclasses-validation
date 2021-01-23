from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import pytest
from dcv.fields import BoolField

def test_bool():
    """Test bool field.

    GIVEN a dataclass with a `bool` field
    WHEN a valid bool value is given
    THEN it should validate input on assign.
    """
    @dataclass
    class T:
        flag: bool = BoolField()
        flag_op: Optional[bool] = BoolField(optional=True)
        flag_f: bool = field(default=BoolField())

    t = T(flag=True, flag_f=False)

    assert t.flag
    assert not t.flag_f
    assert t.flag_op is None

    t = T(flag=True, flag_op=False, flag_f=False)

    assert t.flag
    assert not t.flag_op
    assert not t.flag_f

    with pytest.raises(TypeError):
        T(flag="false", flag_=False)

    with pytest.raises(TypeError):
        T(flag=False, flag_="False")

    with pytest.raises(TypeError):
        T(flag=False, flag_=False).flag_op = "false"
