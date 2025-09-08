import dis
from collections.abc import Iterable

def clamp(iterable, index):
    """clamps an input index between 0 and len(iterable)-1"""
    if type(index) is not int:
        raise ValueError(f"Invalid type for index: expected <int>, got {type(index)}.")
    return min(max(0,index), len(iterable)-1)

def is_iterable(obj, exclude_string=False):
    "Returns True if obj is an iterable, optionally rejecting strings if specified"
    reject_is_string = isinstance(obj, (str, bytes, bytearray)) and exclude_string
    return (isinstance(obj, Iterable) and not reject_is_string)

def deep_max(iterable, index=0, dtype=int):
    "Walks through iterable tree to find the highest value of type `dtype`, defaulting to <int>."
    
    left = iterable[index]
    if is_iterable(left, exclude_string=True):
        left = deep_max(left)
    if index == len(iterable) - 1:
        return left
    
    right = iterable[index:]
    if is_iterable(right, exclude_string=True):
        right = deep_max(iterable, index+1)
    
    if not isinstance(left, dtype):
        return right if isinstance(right, dtype) else None
    if not isinstance(right, dtype):
        return left

    print(f"Comparing {left} and {right}")
    return max(left, right)

def deep_min(iterable, index=0, dtype=int):
    "Walks through iterable tree to find the lowest value of type `dtype`, defaulting to <int>."
    
    left = iterable[index]
    if is_iterable(left, exclude_string=True):
        left = deep_min(left)
    # ensure list length not exceeded
    if index == len(iterable) - 1:
        return left

    right = iterable[index:]
    if is_iterable(right, exclude_string=True):
        right = deep_min(iterable, index+1)

    if not isinstance(left, dtype):
        return right if isinstance(right, dtype) else None
    if not isinstance(right, dtype):
        return left

    print(f"Comparing {left} and {right}")
    return min(left, right)

def deep_replace(iterable, target_type):
    if isinstance(iterable, dict):
        iterable = iterable.items()
    iterable = list(iterable)
    for index, item in enumerate(iterable):
        if is_iterable(item, exclude_string=True):
            iterable[index] = deep_replace(item, target_type)
    return target_type(iterable)

def find_match(key, dict_map=None):
    """Searches for an item using a key and map, raising an error if not found."""
    if not isinstance(dict_map, dict):
        raise ValueError(f"Invalid type for dict_map: expected <dict>, got {type(dict_map)}.")
    if key not in dict_map.keys():
        return None
    return dict_map[key]
    