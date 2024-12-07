# is_subset

[![GPLv2 License](https://img.shields.io/badge/License-GPL%20v2-blue.svg)](https://opensource.org/licenses/) ![PyPI](https://img.shields.io/pypi/v/is_subset) [![Actions Status](https://github.com/WajahatAliAbid/is-subset/workflows/Build/badge.svg)](https://github.com/WajahatAliAbid/is-subset/actions)


**`is_subset`** is a Python utility for checking if a given dictionary (`dict2`) is a subset of another dictionary (`dict1`). It supports advanced matching features such as nested dictionaries, regular expressions, and conditional operators.



## Installation

Install my-project with pip

```bash
pip install is_subset
```
    
## Features

- Check if one dictionary (`dict2`) is a subset of another dictionary (`dict1`).
- Supports:
  - Exact matches
  - Nested dictionaries
  - Conditional checks like `__is`, `__not`, `__in`, `__not_in`, `__matches`, and `__not_matches`.
- Works seamlessly with Python primitives like strings, numbers, booleans, and collections.


## Usage

You can check if a dictionary is subset of another using

### Basic Examples
```python
from is_subset import is_subset

# Simple matching
dict1 = {"age": 30, "name": "John"}

dict2 = {"age": 30}
print(is_subset(dict1, dict2))  # Output: True

dict2 = {"age": 25}
print(is_subset(dict1, dict2))  # Output: False
```

### Advanced Examples
Nested Dictionary Matching
```python
dict1 = {
    "user": {
        "name": "John",
        "details": {
            "age": 30,
            "city": "Metropolis"
        }
    }
}

dict2 = {"user": {"details": {"city": "Metropolis"}}}
print(is_subset(dict1, dict2))  # Output: True
```

Conditional Matching (__is, __not, __in, __not_in)
```python
# Conditional matching for exact values
dict2 = {"user": {"details": {"city": {"__is": "Metropolis"}}}}
print(is_subset(dict1, dict2))  # Output: True

# Conditional matching for exclusion
dict2 = {"user": {"details": {"city": {"__not": "Gotham"}}}}
print(is_subset(dict1, dict2))  # Output: True

# Conditional matching for inclusion in a list
dict2 = {"user": {"details": {"age": {"__in": [25, 30]}}}}
print(is_subset(dict1, dict2))  # Output: True

# Conditional matching for exclusion in list

dict2 = {"user": {"details": {"age": {"__not_in": [20, 23]}}}}
print(is_subset(dict1, dict2))  # Output: True
```

Regular Expression Matching (__matches, __not_matches)
```python
dict1 = {"email": "john.doe@example.com"}

# Regex matching
dict2 = {"email": {"__matches": r".*@example\.com"}}
print(is_subset(dict1, dict2))  # Output: True

# Negative regex matching
dict2 = {"email": {"__not_matches": r".*@gmail\.com"}}
print(is_subset(dict1, dict2))  # Output: True
```


## API Reference
`is_subset(dict1: dict, dict2: dict) -> bool`

**Parameters**:
- `dict1` (`dict`): The main dictionary to check against.
- `dict2` (`dict`): A dictionary specifying the conditions to check.

**Returns**:
- `bool`: `True` if all conditions in `dict2` match the `dict1`, otherwise `False`.

**Supported Condition Operators**:
- `__is`: Matches if the value is equal.
- `__not`: Matches if the value is not equal.
- `__in`: Matches if the value is in a list or collection.
- `__not_in`: Matches if the value is not in a list or collection.
- `__matches`: Matches if the value satisfies the given regex.
- `__not_matches`: Matches if the value does not satisfy the given regex.

## Contributing

Contributions are always welcome! In case you have any request or encounter a bug, please create an issue on the repo.

## Authors

- [@WajahatAliAbid](https://www.github.com/WajahatAliAbid)

