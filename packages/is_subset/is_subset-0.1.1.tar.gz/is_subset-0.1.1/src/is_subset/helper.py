import re
import typing


def matches_str(
    input: str,
    matcher: str | typing.Dict[str, typing.Any],
) -> bool:
    if isinstance(matcher, str):
        return input == matcher
    
    if not isinstance(matcher, dict):
        return False

    if len(matcher) != 1:
        return False
    first_key = list(matcher.keys())[0]
    if first_key not in [
        '__is', 
        '__not', 
        '__in', 
        '__not_in', 
        '__matches', 
        '__not_matches'
    ]:
        print("We are here")
        return False
    
    if first_key == '__is':
        return input == matcher[first_key]
    if first_key == '__not':
        return input != matcher[first_key]
    if first_key == '__in':
        return input in matcher[first_key]
    if first_key == '__not_in':
        return input not in matcher[first_key]
    if first_key == '__matches':
        return re.match(matcher[first_key], input) is not None
    if first_key == '__not_matches':
        return re.match(matcher[first_key], input) is None

    return False

def matches_number(
    input: int | float,
    matcher: int | float | typing.Dict[str, typing.Any],
) -> bool:
    if isinstance(matcher, (int, float)):
        return input == matcher
    
    if not isinstance(matcher, dict):
        return False

    if len(matcher) != 1:
        return False
    first_key = list(matcher.keys())[0]
    if first_key not in [
        '__is', 
        '__not', 
        '__in', 
        '__not_in'
    ]:
        return False
    
    if first_key == '__is':
        return input == matcher[first_key]
    if first_key == '__not':
        return input != matcher[first_key]
    if first_key == '__in':
        return input in matcher[first_key]
    if first_key == '__not_in':
        return input not in matcher[first_key]
    
    return False

def matches_bool(
    input: bool,
    matcher: bool | typing.Dict[str, typing.Any],
) -> bool:
    if isinstance(matcher, bool   ):
        return input == matcher
    
    if not isinstance(matcher, dict):
        return False

    if len(matcher) != 1:
        return False
    first_key = list(matcher.keys())[0]
    if first_key not in [
        '__is', 
        '__not'
    ]:
        return False
    
    if first_key == '__is':
        return input == matcher[first_key]
    if first_key == '__not':
        return input != matcher[first_key]
    
    return False