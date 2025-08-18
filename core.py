from .algorithms import merge_sort, binary_search, is_sorted

class iu_list(list):
    def __init__(self, iterable):
        super().__init__(iterable)
        self.sorted = False
        self.track_sorted = True
        self.is_reversed = False
        self.track_reverse = True
        self.sorting_key = lambda x:x

    def reverse(self):
        super().reverse()
        self.is_reversed = not self.is_reversed

    def __setitem__(self,index,value):
        super().__setitem__(index,value)
        if self.track_sorted and self.sorted:
            self.sorted = self.is_sorted(index)

    def append(self,x):
        super().append(x)
        self.sorted = self.is_sorted(-1)

    def extend(self, iterable):
        pre_extend_length = len(self)
        super().extend(iterable)
        for i in range(len(iterable)):
            if not self.is_sorted(pre_extend_length + i):
                self.sorted = False
                break
        

    def insert(self, index, x):
        super().insert(index, x)
        self.sorted = self.is_sorted(index)

    def sort(self, *, key=None, reverse=False):
        if not callable(key):
            key = self.sorting_key
        super().sort(key=key, reverse=reverse)
        self.sorted = True

    @property
    def len(self):
        return super().__len__()

    def is_sorted(self, i=..., *, reverse=None, key=None):
        return is_sorted(self, i, reverse=reverse, key=key)

    def merge_sort(self, input_iterable=None, *, reverse=None, key=None, visual=True):
        return merge_sort(self, input_iterable, reverse=reverse, key=key, visual=visual)

    def binary_search(self, target, *, reverse=None, key=None, override_sorted=False):
        return binary_search(self, target, reverse=reverse, key=key, override_sorted=override_sorted)
