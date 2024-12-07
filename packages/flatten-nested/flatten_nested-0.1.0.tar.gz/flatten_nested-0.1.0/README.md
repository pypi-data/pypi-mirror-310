# Flatten Nested

A Python package for flattening nested data structures including lists, tuples, dictionaries, and sets.

## Installation

```bash
pip install flatten-nested
```

## Usage

```python
from flatten_nested import flatten

# Flatten a nested list
nested_list = [1, [2, 3, [4, 5]], 6]
flattened = flatten(nested_list)
print(flattened)  # [1, 2, 3, 4, 5, 6]

# Flatten a nested dictionary
nested_dict = {'a': 1, 'b': {'c': 2, 'd': {'e': 3}}}
flattened = flatten(nested_dict)
print(flattened)  # [('a', 1), ('b.c', 2), ('b.d.e', 3)]

# Flatten with depth limit
nested = [1, [2, [3, [4]]]]
flattened = flatten(nested, depth=1)
print(flattened)  # [1, 2, [3, [4]]]
```

## Features

- Supports lists, tuples, dictionaries, and sets
- Optional depth limit for partial flattening
- Customizable dictionary key handling
- Configurable separator for nested dictionary keys
- Type hints for better IDE support
- Comprehensive test suite
- Exception handling for unsupported types

## License

This project is licensed under the MIT License.