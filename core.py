from .algorithms import *
from .utils import *
import dis
import types

class iu_lambda:
    def __init__(self, key=None, *, formula=None, index_path=None, variables=None, total_vars_loaded=None):
        if key is not None:
            formula, index_path, variables, total_vars_loaded = iu_lambda.from_lambda(key)
        elif any(arg is None for arg in (formula, index_path, variables, total_vars_loaded)):
            raise ValueError("Invalid arguments for custom iu_lambda")
        self.for_eval = f"lambda {','.join(variables)}: {formula}"
        self.formula = formula
        self.index_path = tuple(index_path)
        self.variables = variables
        self.total_vars_loaded = total_vars_loaded
        self.key = key
        
    def __repr__(self):
        return f"iu_lambda(key={self.for_eval})"

    def __str__(self):
        return f"<class iu_lambda({self.for_eval}) at {hex(id(self))}>"

    def __call__(self, *args, **kwargs):
        return self.key(*args, **kwargs)

    def from_lambda(key):
        instructions = list(dis.get_instructions(key))
        print([instr.opname for instr in instructions])
        RETURN = instructions[-1].opname
        if RETURN.endswith("CONST"):
            return str(RETURN.argval)
        elif RETURN.endswith("VALUE"):
            print("Start loop!!")
            i=0
            QUEUE = []
            LOADED_GLOBALS_QUEUE = []
            index_path = []
            TOTAL_VARS_LOADED = 0
            VAR_NAMES = set()
            for instr in instructions:
                print(f"\nInstruction {i}: {instr.opname}"); i+= 1
                
                match instr.opname:
                    case "RESUME":
                        continue
                    case "LOAD_CONST":
                        QUEUE.append(str(instr.argval))
                        print(f"Loaded {instr.argval} to QUEUE")
                    case "LOAD_FAST":
                        QUEUE.append(str(instr.argval))
                        VAR_NAMES.add(str(instr.argval))
                        TOTAL_VARS_LOADED += 1
                        print(f"Loaded {instr.argval} to QUEUE")
                    case "UNARY_INVERT":
                        QUEUE[-1] = "~"+QUEUE[-1]
                    case "BINARY_SUBSCR":
                        QUEUE[-2] = f"{QUEUE[-2]}[{QUEUE[-1]}]"
                        index_path.append(QUEUE[-1])
                        QUEUE.pop(-1)
                    case "LOAD_GLOBAL":
                        LOADED_GLOBALS_QUEUE.append(instr.argval)
                        print(f"loaded global variable '{str(instr.argval)}'")
                    case "CALL":
                        last_global = LOADED_GLOBALS_QUEUE.pop(-1)
                        QUEUE[-1] = f"{last_global}({QUEUE[1]})"
                        print(f"retrieved last loaded global '{last_global}'")
                    case "CALL_FUNCTION":
                        last_global = LOADED_GLOBALS_QUEUE.pop(-1)
                        QUEUE[-1] = f"{last_global}({QUEUE[-1]})"
                        print(f"retrieved last loaded global '{last_global}'")
                    case "LOAD_ATTR":
                        QUEUE[-1] += "." + str(instr.argval)
                    case "RETURN_VALUE":
                        return ("".join(QUEUE), index_path, VAR_NAMES, TOTAL_VARS_LOADED)
                    case _:
                        if instr.opname.startswith("BINARY_"):
                            #strip off "BINARY_"
                            opname = instr.opname[7:]
                            symbol_code = instr.argval
                            # if older command, find matching symbol for name
                            if opname != "OP":
                                opnames = ("ADD", "AND", "FLOOR_DIVIDE", "LSHIFT", "MATRIX_MULTIPLY", "MULTIPLY", "MODULO", "OR", "POWER", "RSHIFT", "SUBTRACT", "TRUE_DIVIDE", "XOR")
                                try:
                                    symbol_code = opnames.index(opname)
                                except ValueError:
                                    raise ValueError(f"Unable to find binary operation {instr.opname}")
                            # now find the correct symbol
                            operators = ('+', '&', '//', '<<', '@', '*', '%', '|', '**', '>>', '-', '/', '^')
                        
                            if operators[symbol_code] is not None:
                                QUEUE[-2] += operators[symbol_code]+QUEUE[-1]
                                print(f"Operation completed: {QUEUE[-2]}{operators[symbol_code]}{QUEUE[-1]}")
                                QUEUE.pop(-1)
                            else: 
                                raise ValueError(f"Unexpected operator argval {instr.argval}") 
                        
                        else:
                            print(f"ERROR!! unexpected opname '{instr.opname}'")

                print(" ".join(QUEUE))
        else:
            raise ValueError(f"ERROR!! Unexpected return code '{instr.opname}'")
    def lambda_analyse(key):
        """Deconstruct a lambda into its main components and print a chronological table"""
        instructions = list(dis.get_instructions(key))
        for instr in instructions:
            print(f"{(instr.opname+'  ('+str(instr.opcode)+')'):30}| arg={str(instr.arg):7} argval={instr.argval}\n")


################################################################################################################################


class iu_list(list):
    def __init__(self, iterable, replace_all=False):
        self.apply_key = False
        super().__init__(iterable)
        self.track_sorted = True
        self.is_reversed = False
        self.track_reverse = True
        self._key = iu_lambda(lambda x:x)
        self.sorted = self.is_sorted()
        self.hash_history = set()
        self.current_hash = self.last_saved_hash = None
        if replace_all:
            for index, item in enumerate(self):
                if is_iterable(item, exclude_string=True):
                    self[index] = iu_list(item)


    def __setitem__(self,index,value):
        self.current_hash = None
        if self.apply_key:
            pass
        super().__setitem__(index,value)
        if self.track_sorted and self.sorted:
            self.sorted = self.is_sorted(index)

    def __getitem__(self, index):
        item = super().__getitem__(index)
        if self.apply_key is True:
            item = self._key.key(item)
        return item

    def Type(self):
        return type(self)

    def reverse(self):
        self.current_hash = None
        super().reverse()
        self.is_reversed = not self.is_reversed

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
        if self.sorted and iu_lambda(key).formula==self._key.formula:
            if reverse:
                self.reverse()
                self.current_hash = None
            print("bypassed!!")
            return self
        self.current_hash = None
        if not callable(key):
            key = self._key.key
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
        if self.sorted and iu_lambda(key).formula==self._key.formula:
            if reverse:
                self.reverse()
                self.current_hash = None
            print("bypassed!!")
            return self

        if not callable(key):
            key = self._key.key
        else:
            self._key.key = key

        if reverse is not None:
            self.is_reversed = reverse
        reverse = -1 if self.is_reversed else 1
        
        iterable = merge_sort(self, reverse=reverse, key=key, visual=visual)
        self.sorted = True
        return self

    def binary_search(self, target, *, reverse=None, key=None, override_sorted=False):
        return binary_search(self, target, reverse=reverse, key=key, override_sorted=override_sorted)

    def __hash__(self): 
        self.current_hash = hash(tuple(self))
        return self.current_hash
    
    def clear_hashes(self):
        self.hash_history.clear()

    def save_current_hash(self):
        if self.current_hash is None:
            hash(self)
        self.last_saved_hash = self.current_hash
        self.hash_history.add(current_hash)

    def set_key(self, key):
        self._key.key = iu_key(key)

    def activate_key(self):
        self.apply_key = True
    
    def deactivate_key(self):
        self.apply_key = False

    @property
    def with_key_applied(self):
        return iu_list([self._key.key(item) for item in self])

    def deep_max(self, *, iterable=None, index=0):
        if iterable is None:
            iterable = self
        left = iterable[index]
        if is_iterable(left, exclude_string=True):
            left = deep_max(left)
        if index == len(iterable) - 1:
            return left
        right = deep_max(iterable, index+1)
        return max(left, right)

    def deep_min(self, *, iterable=None, index=0):
        if iterable is None:
            iterable = self
        left = iterable[index]
        if is_iterable(left, exclude_string=True):
            left = deep_min(left)
        if index == len(iterable) - 1:
            return left
        right = deep_min(iterable, index+1)
        return min(left, right)