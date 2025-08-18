from .utils import clamp
from copy import deepcopy

class SearchObject:
    def __init__(self, target=None, found=None, occurences=0, floor=None, ceil=None, sorted=None, reverse=None):
        self.target = target
        self.found = found
        self.occurences = occurences
        self.floor = floor
        self.ceil = ceil
        self.sorted = sorted
        self.reverse = reverse
    def __repr__(self):
        return f"SearchObject(target={self.target}, found={self.found}, occurences={self.occurences}, floor={self.floor}, ceil={self.ceil}, sorted={self.sorted}, reverse={self.reverse})"


def is_sorted(self,i=..., *, reverse=None, key=None):
    if not callable(key):
        key = self.sorting_key
    # check surrounding the modified index (i) to ensure they are still sorted
    if reverse is not None:
        self.is_reversed = reverse
    reverse = -1 if self.is_reversed else 1
    if i is not ...:
        if type(i) is not int:
            raise ValueError(f"Error: argument `i`: expected <int>, got {type(i)}")
        if i < 0:
            if -i > len(self):
                raise ValueError(f"Error: cannot accept negative index {i} exceeding list length {len(self)}")
            i = len(self) + i
        # key(...)*reverse first applies the key to retrieve the desired item, then flips the equality (or not) based on `reverse`` (-1 or 1)
        return key(self[clamp(self,i-reverse)]) <= key(self[i]) <= key(self[clamp(self,i+reverse)])
    else:
        for index in range(len(self)-1):
            if key(self[index])*reverse > key(self[index])*reverse:
                return False
        return True

def merge_sort(self, input_iterable=None, *, reverse=None, key=None, visual=True):
    if not callable(key):
        key = self.sorting_key
    else:
        self.sorting_key = key
    iterable = self if input_iterable is None else input_iterable
    #if visual:
    #    print(iterable, end="\n",flush=True)
    #    sleep(1/len(self))
    if not callable(key):
        key = self.sorting_key
    # base reverse off of tracked value if track_reverse is enabled. Otherwise use reverse
    if reverse is not None:
        self.is_reversed = reverse
    reverse = -1 if self.is_reversed else 1
        
    size = len(iterable)
    if size == 1:
        return iterable
    left = self.merge_sort(iterable[:size//2], key=key, visual=visual)
    right= self.merge_sort(iterable[size//2:], key=key, visual=visual)
    left_ptr = right_ptr = 0
    for i in range(size):
        if right_ptr == (size - size//2) or (left_ptr != size//2 and key(left[left_ptr])*reverse < key(right[right_ptr])*reverse):
            iterable[i] = left[left_ptr]
            left_ptr += 1
        else:
            iterable[i] = right[right_ptr]
            right_ptr += 1
    if input_iterable is None:
        iterable = deepcopy(iterable)
        self.clear()
        self.extend(iterable)
        self.sorted = True
    #if visual:
    #    print(iterable, end="\n",flush=True)
    #    sleep(1/len(self))
    return iterable

def binary_search(self, target, *, reverse=None, key=None, override_sorted=False):
    """
    Searches for a specific item in a sorted list, returning first & last occurence indexes
    OUTPUTS:
    SearchObject -- successful search lead to either a match or a range of indexes
    -1 -- ERROR: list is not sorted. Can be overriden with `override_sorted=True`
    """
    found = False
    occurences = 0

    # check whether the list is sorted in reverse or not
    if reverse is not None:
        self.is_reversed = reverse
    rev = -1 if self.is_reversed else 1

    # retrieve the sorting key
    if not callable(key):
        key = self.sorting_key

    # return error if list is not sorted
    if not ((self.track_sorted and self.sorted) or override_sorted==True):
        return -1

    lwr_bound = 0
    upr_bound = len(self)-1
    target *= rev
    while upr_bound - lwr_bound > 1:
        ptr = (lwr_bound + upr_bound) // 2
        val = key(self[ptr])
        val *= rev
        if val < target:
            lwr_bound = ptr
        elif val > target:
            upr_bound = ptr
        else:
            # find the lowest occurrence
            while ptr - rev >= 0 and self[ptr-1] == self[ptr]:
                ptr -= 1
            lwr_bound = ptr

            # find the highest occurrence
            while ptr + rev < len(self) and self[ptr+1] == self[ptr]:
                ptr += 1
            upr_bound = ptr

            found = True
            occurences = upr_bound - lwr_bound + 1
            break

    return SearchObject(target=target*rev, found=found, occurences=occurences, floor=lwr_bound, ceil=upr_bound, sorted=not override_sorted, reverse=self.is_reversed)
