from random import randint
from .core import iu_list

def main():
    random_list = [randint(-99,100) for _ in range(10)]
    list_2d = [[randint(1,20),randint(50,100)] for _ in range(10)]
    many_duplicates = [randint(0,3) for _ in range(20)]
    ulist = iu_list(many_duplicates)
    
    print(ulist)
    ulist.merge_sort(key=lambda x: x)
    print(ulist)

    print(ulist.binary_search(2))

    ulist.reverse()
    print("Reversed! ==================================================")
    print(ulist)
    print(ulist.binary_search(2))

if __name__ == "__main__":
    main()