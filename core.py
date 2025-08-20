from .algorithms import merge_sort, binary_search, is_sorted
from .utils import clamp

class iu_list(list):
    def __init__(self, iterable):
        super().__init__(iterable)
        self.track_sorted = True
        self.is_reversed = False
        self.track_reverse = True
        self.sorting_key = lambda x:x
        self.sorted = self.is_sorted()
        self.hash_history = set()
        self.last_hash = None

    def reverse(self):
        self.current_hash = None
        super().reverse()
        self.is_reversed = not self.is_reversed

    def __setitem__(self,index,value):
        self.current_hash = None
        super().__setitem__(index,value)
        if self.track_sorted and self.sorted:
            self.sorted = self.is_sorted(index)

    def append(self,x):
        self.current_hash = None
        super().append(x)
        self.sorted = self.is_sorted(-1)

    def extend(self, iterable):
        self.current_hash = None
        pre_extend_length = len(self)
        super().extend(iterable)
        for i in range(len(iterable)):
            if not self.is_sorted(pre_extend_length + i):
                self.sorted = False
                break
        
    def insert(self, index, x):
        self.current_hash = None
        super().insert(index, x)
        self.sorted = self.is_sorted(index)

    def sort(self, *, reverse=None, key=None):
        if self.sorted and key.__code__.co_code==self.sorting_key.__code__.co_code:
            if reverse:
                self.reverse()
                self.current_hash = None
            print("bypassed!!")
            return self
        self.current_hash = None
        if not callable(key):
            key = self.sorting_key
        if reverse is not None:
            self.is_reversed = reverse
        super().sort(key=key, reverse=self.is_reversed)
        self.sorted = True
        return self

    @property
    def len(self):
        return super().__len__()

    def clamped(self, index):
        return self[clamp(self,index)]

    def is_sorted(self, i=..., *, reverse=None, key=None):
        return is_sorted(self, i, reverse=reverse, key=key)

    def merge_sort(self, *, reverse=False, key=lambda x:x, visual=True):
        # check bytecode of keys to check for similarity & bypass
        if self.sorted and key.__code__.co_code==self.sorting_key.__code__.co_code:
            if reverse:
                self.reverse()
                self.current_hash = None
            print("bypassed!!")
            return self

        if not callable(key):
            key = self.sorting_key
        else:
            self.sorting_key = key

        if reverse is not None:
            self.is_reversed = reverse
        reverse = -1 if self.is_reversed else 1
        
        iterable = merge_sort(self, reverse=reverse, key=key, visual=visual)
        self.sorted = True
        return self

    def binary_search(self, target, *, reverse=None, key=None, override_sorted=False):
        return binary_search(self, target, reverse=reverse, key=key, override_sorted=override_sorted)

    def __hash__(self): 
        self.last_hash = self.current_hash = hash(tuple(self))
        return self.current_hash
    
    def clear_hashes(self):
        self.hash_history.clear()

    def save_current_hash(self):
        self.hash_history.add(current_hash)