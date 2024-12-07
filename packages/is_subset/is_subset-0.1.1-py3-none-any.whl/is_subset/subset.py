import typing
from .helper import matches_str, matches_number, matches_bool


"""
This code defines a function is_subset that checks if a dictionary dict2 is a subset of another dictionary dict1. 
It returns True if dict2 is a subset of dict1 and False otherwise.

The function first checks if both dictionaries are not None and are indeed dictionaries. 
It then checks if the length of dict1 is greater than the length of dict2, in which case it immediately returns False.

The function then iterates over the keys in dict2 and checks if the corresponding values in dict1 match the values in dict2. 
The matching is done using helper functions matches_str, matches_number, and matches_bool for string, number, and boolean values, respectively. 
For nested dictionaries, the function calls itself recursively.

If any of the checks fail, the function returns False. If all checks pass, the function returns True.
"""
def is_subset(
    dict1: typing.Dict[typing.Any, typing.Any],
    dict2: typing.Dict[typing.Any, typing.Any],
) -> bool:
    """
    Determines if `dict2` is a subset of `dict1`.

    Args:
        dict1 (Dict[Any, Any]): The dictionary to be checked against.
        dict2 (Dict[Any, Any]): The dictionary to check as a subset.

    Returns:
        bool: True if `dict2` is a subset of `dict1`, False otherwise.

    Raises:
        ValueError: If either `dict1` or `dict2` is None or not a dictionary.

    Notes:
        - The function supports matching of string, number (int or float), 
          boolean, and nested dictionary values using helper functions.
        - The function currently does not support list values.
    """
    if dict1 is None:
        raise ValueError("dict1 cannot be None")

    if dict2 is None:
        raise ValueError("dict2 cannot be None")
    
    # type checking
    if not isinstance(dict1, dict):
        raise ValueError("dict1 must be a dictionary")

    if not isinstance(dict2, dict):
        raise ValueError("dict2 must be a dictionary")

    # This means dict2 can be a subset of dict1
    if len(dict2) > len(dict1):
        return False
    
    for key in dict2:
        dict2_value = dict2[key]
        if key not in dict1:
            return False
        
        dict1_value = dict1[key]
        if dict1_value is None and dict2_value is None:
            continue

        if isinstance(dict1_value, str):
            sub_is_match = matches_str(dict1_value, dict2_value)
            if not sub_is_match:
                return False
            
        if isinstance(dict1_value, (int, float)):
            sub_is_match = matches_number(dict1_value, dict2_value)
            if not sub_is_match:
                return False
        
        if isinstance(dict1_value, bool):
            sub_is_match = matches_bool(dict1_value, dict2_value)
            if not sub_is_match:
                return False
        
        if isinstance(dict1_value, dict):
            if not isinstance(dict2_value, dict):
                return False
            sub_is_match = is_subset(dict1_value, dict2_value)
            if not sub_is_match:
                return False

        # TODO: create subset matcher for list    
    return True