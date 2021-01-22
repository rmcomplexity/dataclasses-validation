from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Any
import pytest
from dcv.fields.enum import EnumField

class Size(Enum):
    XS = 'x-small'
    S = 'small'
    M = 'medium'
    L = 'large'
    XL = 'x-large'

def test_enums():
    """Test enum field.

    GIVEN a dataclass with a `Enum` field
    WHEN a valid enum value is given
    THEN it should validate input on init.
    """
    class NotASize(Enum):
        XS = 'xs'

    @dataclass
    class T:
        enumeration: Enum = EnumField()
        size: Size = EnumField()
        optional_size: Optional[Size] = EnumField()
        enumeration_field: Enum = field(default=EnumField())
        size_field: Size = field(default=EnumField())

    t = T(
        enumeration=Size.XS,
        enumeration_field=Size.S,
        size=Size.L,
        size_field=Size.XL,
        optional_size=Size.M,
    )

    assert t.enumeration == Size.XS
    assert t.enumeration_field == Size.S
    assert t.size == Size.L
    assert t.size_field == Size.XL

    with pytest.raises(TypeError):
        t = T(
            enumeration="small",
            enumeration_field="x-small",
            size="large",
            size_field="x-large"
        )

    with pytest.raises(TypeError):
        t = T(
            enumeration=Size.XS,
            enumeration_field=Size.S,
            size=Size.L,
            size_field=Size.XL,
            optional_size=NotASize.XS,
        )
