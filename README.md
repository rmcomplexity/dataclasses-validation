# Python Dataclasses Validation

### Validation for dataclasses. No dependencies. Field-specific configuration.

Dataclasses are powerful, but we still need to validate incoming data.
Validation libraries make you either subclass a 3rd party class or use a schema class.
**Now, you can easily validate fields in dataclasses by using field-specific validation**.

## ![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+) This is a work in progress.
Please check the [project board](https://github.com/rmcomplexity/dataclasses-validation/projects/1) to see pendining tasks in case there isn't a proper release yet.

- [Example](#example)
- [Rationale](#rationale)
- [Runtime Type Hint Checking](#runtime-type-hint-checking)
- [Available Fields](#available-fields)
- [Custom Fields](#custom-fields)
- [Future Work](#future-work)

## Example:

```python
import logging
from dataclasses import dataclass, field, asdict
from typing import Optional
from enum import Enum
from dcv.fields import TextField, IntField


logging.basicConfig(level=logging.INFO)


@dataclass
class User:
    # trailing/leading blank spaces will be removed
    name: str = TextField(min_length=1, trim=" ")

    # 'last_name' can be None or an empty string.
    # Optional fields have a default value of None.
    last_name: Optional[str] = TextField(min_length=1, trim=" ", optional=True, blank=True)

    # A user cannot be born before 1800. Time travelers are not considered here :(.
    year_of_birth: Optional[int] = IntField(gt=1800, optional=True)

    # 'opt_out' has a default value of "Yes", uses a regex
    # and it's not used in __init__
    opt_out: str = field(default=TextField(default="Yes", regex="(Yes|No)"), init=False)

# Insantiation without any issues
>>> user = User(name="Josué", last_name="Balandrano", year_of_birth=1985)
>>> logging.info(user)
... INFO:root:User(name="Josué", last_name="Balandrano", opt_out="Yes")

# We get a ValueError if we try to set an invalid value on a non-init attr.
>>> user.opt_out = "Maybe"
... ValueError: 'opt_out' does not match regex: (Yes|No) .

# We automatically have serialization with dataclasses
>>> asdict(user)
... {'name': 'Josué', 'last_name': 'Balandrano', 'opt_out': 'Yes'}

# We get a ValueError if an invalid value is used on init
>>> User(name = "", last_name="Balandrano", year_of_birth=1755)
... ValueError: 'name' cannot be blank.
>>> User(name = "Josué", last_name="Balandrano", year_of_birth=1775)
... ValueError: 'year_of_birth' value '1775' must be greater than 1800.
```

## Features of `dcv`

- Works with dataclasses out of the box.
- Validation is implemented in descriptors and not in the class.
- Validation happens when a value is assigned to an attribute, could be on `__init__` or afterwards.
- Easily nest objects simply by using more dataclasses.
- No need to sublcass anything.
- No need to create another class to define the schema.
- Basic [runtime type hint checking](#runtime-type-hint-checking).

## Rationale

Current validation libraries (like [pydantic](https://pydantic-docs.helpmanual.io/))
modify classes to be aware of the data that is being stored on each instance.
Some other libraries(like [marshmallow](https://marshmallow.readthedocs.io/en/stable/))
makes you use a schema (specialized class) for validation and data storage.

[Python descriptors](https://docs.python.org/3/howto/descriptor.html)
give us the power to specify how data is looked up, stored and deleted.
And this is seameless to the main class. 
[Python dataclasses](https://docs.python.org/3/library/dataclasses.html)
are powerfull classes tailored to hold data.
`dcv` implementation leverages descriptors and dataclasses
to implement a less obtrusive validation and to be able to specify
which fields will be validated instead of having a one-or-nothing solution.

### Runtime type hint checking

`dcv` checks typehints in two instances.

First, when a field is instantiated and assigned to a dataclass field.
The type hint used in the dataclass field will be used to make sure it matches
the `dcv` field supported `TYPES`.

Second, when a value is assigned to a dataclass attribute managed by a `dcv` field.
This could happen on `__init__` or afterwards.

A type hint matches a `dcv` field if the
origin of the type hint is present in the `Field.TYPES` class variable or
if the origin is a subclass of an object present in the `Field.TYPES` class variable.
The origin is retrieved by using [`typing.get_origin`](https://docs.python.org/3/library/typing.html#typing.get_origin)

If the origin cannot be retrieved then it means the type hint is a `Generic` container
e.g. `Optional`, `Union`, etc. In this case the arguments of the type hint are
checked against the objects in the `Field.TYPES` tuple.

#### Examples

- `field_name: str` - Will check if any object in `Field.TYPES` is `str` or a subclass of `str`.
- `field_name: Optional[str]` - `Optional` will be discarded and `str` will be used to check values.
- `field_name: List[str]` - `list` will be used to check values.
- `field_name: Optional[List[int]] - `list` will be used to check values.

## Available Fields

---------------------------------------------------------------------------------------
| Name          | Types Supported                        | Implemented | Parent Field | 
---------------------------------------------------------------------------------------
| `TextField`   | `str`, `bytes`                         | (/) Yes     | `Field`      |
| `NumberField` | `int`, `float`, `complex`, `Decimal`   | (/) Yes     | `Field`      |
| `IntField`    | `int`                                  | (/) Yes     | `NumberField`|
| `FloatField`  | `float`                                | (/) Yes     | `NumberField`|
| `ComplexField`| `complex`                              | (/) Yes     | `NumberField`|
| `DecimalField`| `Decimal`                              | (/) Yes     | `NumberField`|
| `EnumField`   | `Enum`                                 | (/) Yes     | `Field`      |
| `BooleanField`| `bool`                                 | (x) No      |  ---         |
| `ListField`   | `list`, `tuple`                        | (x) No      |  ---         |
| `SetField`    | `set`                                  | (x) No      |  ---         |
| `DictField`   | `dict`                                 | (x) No      |  ---         |

## Future Work

Check the [project board](https://github.com/rmcomplexity/dataclasses-validation/projects/1) for in-flight and future work.

If you have a specific question or request, please create a github issue.
