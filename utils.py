import dis
from collections.abc import Iterable

def clamp(iterable, index):
    """clamps an input index between 0 and len(iterable)-1"""
    if type(index) is not int:
        raise ValueError(f"Invalid type for index: expected <int>, got {type(index)}.")
    return min(max(0,index), len(iterable)-1)


def is_iterable(obj, exclude_string=False):
    reject_is_string = isinstance(obj, (str, bytes, bytearray)) and exclude_string
    return (isinstance(obj, Iterable) and not reject_is_string)

def deep_max(iterable, index=0):
    left = iterable[index]
    if is_iterable(left, exclude_string=True):
        left = deep_max(left)
    if index == len(iterable) - 1:
        return left
    right = deep_max(iterable, index+1)
    print(f"Comparing {left} and {right}")
    return max(left, right)

def deep_max(iterable, index=0):
    left = iterable[index]
    if is_iterable(left, exclude_string=True):
        left = deep_max(left)
    if index == len(iterable) - 1:
        return left
    right = deep_max(iterable, index+1)
    print(f"Comparing {left} and {right}")
    return max(left, right)

def recursive_replace(iterable, target_type):
    if isinstance(iterable, dict):
        iterable = iterable.items()
    iterable = list(iterable)
    for index, item in enumerate(iterable):
        if is_iterable(item, exclude_string=True):
            iterable[index] = recursive_replace(item, target_type)
    return target_type(iterable)

