# Python Dataclasses Validation

### Validation for dataclasses. No dependencies. Field-specific configuration.

Dataclasses are powerful, but we still need to validate incoming data.
Validation libraries make you either subclass a 3rd party class or use a schema class.
**Now, you can easily validate fields in dataclasses by using field-specific validation**.

## ![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+) This is a work in progress. The only field implemented right now is [`TextField`](https://github.com/rmcomplexity/dataclasses-validation/blob/main/dcv/fields/text.py)

## Example:

```python
import logging
from dataclasses import dataclass, field, asdict
from typing import Optional
from dcv.fields import TextField


logging.basicConfig(level=logging.INFO)


@dataclass
class User:
    # trailing/leading blank spaces will be removed
    name: str = TextField(min_length=1, trim=" ")

    # 'last_name' can be None or an empty string.
    last_name: Optional[str] = TextField(min_length=1, trim=" ", optional=True, blank=True)

    # 'opt_out' has a default value of "Yes", uses a regex
    # and it's not used in __init__
    opt_out: str = field(default=TextField(default="Yes", regex="(Yes|No)"), init=False)

# Insantiation without any issues
>>> user = User(name="Josué", last_name="Balandrano")
>>> logging.info(user)
... INFO:root:User(name="Josué", last_name="Balandrano", opt_out="Yes")

# We get a ValueError if we try to set an invalid value on a non-init attr.
>>> user.opt_out = "Maybe"
... ValueError: 'opt_out' does not match regex: (Yes|No) .

# We automatically have serialization with dataclasses
>>> asdict(user)
... {'name': 'Josué', 'last_name': 'Balandrano', 'opt_out': 'Yes'}

# We get a ValueError if an invalid value is used on init
>>> User(name = "", last_name="Balandrano")
... ValueError: 'name' cannot be blank.
```

## Reasoning

Current validation libraries (like [pydantic](https://pydantic-docs.helpmanual.io/))
modify classes to be aware of the data that is being stored on each instance.
Some other libraries(like [marshmallow](https://marshmallow.readthedocs.io/en/stable/))
makes you use a schema for validation.

[Python descriptors](https://docs.python.org/3/howto/descriptor.html)
give us the power to specify how data is looked up, stored and deleted.
And this is seameless to the main class. 
[Python dataclasses](https://docs.python.org/3/library/dataclasses.html)
are powerfull classes tailored to hold data.
`dcv` implementation leverages descriptors and dataclasses
to implement a less obtrusive validation and to be able to specify
which fields will be validated instead of having a one-or-nothing solution.

## Benefits of `dcv`

- Use dataclasses to handle your data.
- Validation is implemented in descriptors and not in the class.
- Validation happens on instantiation automatically.
- Easily nest objects simply by using more dataclasses.
- No need to sublcass anything.
- No need to create another class to define the schema.
- Shallow run-time type checking.

### Shallow run-time type checking

`dcv` does a type check for built-int types. `dcv` **does not** check type hints.
Checking type hints at run-time is diffcult and probably not worth it.

There are plans to see how can `dcv` improve run-time type checking.

## Future Work

Check the [project board]() for in-flight and future work.

If you have a specific question or request, please create a github issue.
