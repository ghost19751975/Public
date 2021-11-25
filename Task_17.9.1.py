def sort_insert(array):
    for i in range(1, len(array)):
        x = array[i]
        idx = i
        while idx > 0 and array[idx-1] > x:
            array[idx] = array[idx-1]
            idx -= 1
        array[idx] = x


def bin_search(arr_in, elem_in, left, right):
    if left > right:
        return None
    middle = (right + left) // 2
    if arr_in[middle] == elem_in:
        return middle
    elif elem_in < arr_in[middle]:
        return bin_search(arr_in, elem_in, left, middle - 1)
    else:
        return bin_search(arr_in, elem_in, middle + 1, right)


def int_verify(str_in):
    try:
        str_int = int(str_in)
        return str_int
    except ValueError:
        print(f"Значение '{str_in}' невозможно преобразовать в целое число")
        return None


str_ = input("Введите целые неповторяющиеся числа через пробел: ").split()
num_ = list(map(int_verify, str_))

if not num_ or None in num_:
    print("Числа введены неверно!")
    exit()

set_ = list(set(num_))
if len(num_) != len(set_):
    print("Имеются повторяющиеся числа!")
    exit()

sort_insert(num_)

str_ = input("Введите целое число: ")
cfr_ = int_verify(str_)
if not cfr_:
    print("Число введено неверно!")
    exit()

# Поиск требуемой позиции
if num_[0] >= cfr_ or num_[-1] < cfr_:
    print("Элемент не найден!")
else:
    for i in range(cfr_ - 1, num_[0] - 1, -1):
        idx = bin_search(num_, i, 0, len(num_))
        if idx != None and :
            print(f"Номер позиции равен {idx} (элемент {i})")
            break

            
