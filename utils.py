def clamp(iterable, index):
    """clamps an input index between 0 and len(iterable)-1"""
    if type(index) is not int:
        raise ValueError(f"Invalid type for index: expected <int>, got {type(index)}.")
    return min(max(0,index), len(iterable)-1)