import sys
import math
import re

def split_number(n: int, s: int) -> tuple[int, int]:
    power = 10 ** (s)
    quotient, remainder = divmod(n, power)
    return quotient, remainder

def calc_b_(b: int) -> int:
    return 10 - b if b in {1, 9} else b

def digitize(n):
    return [int(i) for i in str(n)]

def rachinsky_1(n, p, s, first_time = False):
    a, b = split_number(p, s)
    m, k = split_number(n, s)
    temp = m * b - k * a

    if first_time:
        print(f'a = {a}, b = {b}')
    else:
          print()
    print(f'm = {m}, k = {k}')
    print(f'mb - ka = {m} * {b} + {k} * {a} = {temp}')
    if temp > p:
        rachinsky_1(temp, p, s)
    elif temp == p or temp == 0:
        print(f'Number is divisible by {p}\n')
    else:
        print(f'Number is indivisible by {p}\n')

def rachinsky_2(n, p, first_time = False):
    a, b = split_number(p, 1)
    b_ = calc_b_(b)
    q = int((p * b_ + 1) / 10) 
    m, k = split_number(n, 1)
    temp = m + k * q

    if first_time:
        print(f'a = {a}, b = {b}, q = (pb* + 1)/10 = ({p} * {b_} + 1) / 10 = {q}')
    else:
        print()
    print(f'm = {m}, k = {k}')
    print(f'm + kq = {m} + {k} * {q} = {temp}')
    if temp >= n:
        print('Temp result isn\'t decreasing, try another\n')
    elif temp == p or temp == 0:
        print(f'Number is divisible by {p}\n')
    elif temp > p:
        rachinsky_2(temp, p)
    else:
        print(f'Number is indivisible by {p}\n')

def rachinsky_3(n, p, first_time = False):
    a, b = split_number(p, 1)
    b_ = calc_b_(b)
    q = int((p * b_ + 1) / 10)
    q_ = abs(p - q)
    m, k = split_number(n, 1)
    temp = m - k * q_

    if first_time:
        print(f'a = {a}, b = {b},')
        print(f'q = (pb* + 1)/10 = ({p} * {b_} + 1) / 10 = {q},')
        print(f'q* = |p - q| = |{p} - {q}| = {q_}')
    else:
        print()
    print(f'm = {m}, k = {k}')
    print(f'm - kq* = {m} - {k} * {q_} = {temp}')
    if temp >= n:
        print('Temp result isn\'t decreasing, try another\n')
    elif temp == p or temp == 0:
        print(f'Number is divisible by {p}\n')
    elif temp > p:
        rachinsky_3(temp, p)
    else:
        print(f'Number is indivisible by {p}\n')

def pascal(n, p):
    r = n
    r_prev = 0
    prev_counter = 0
    r_digits = digitize(r)
    starting_n_len = len(r_digits)
    modules = []
    for i in range(len(r_digits)):
        modules.append(pow(10, i, p))
    strings = []
    for i, module in enumerate(modules):
        strings.append(f'r{i} = {module}')
    print(', '.join(strings))
   
    while r > p and prev_counter < 2:
        r_digits = digitize(r)
        r = 0
        print(f'r = ', end = '')
        # fill in with spaces if new r is shorter
        i = 0
        while i + len(r_digits) < starting_n_len:
             print(' ' * 9, end = '')
             i += 1
        # new r
        for i, digit in enumerate(r_digits):
            module = pow(10, len(r_digits) - (i + 1), p)
            r += digit * module
            print(f'+ {digit} * {module:2} ', end = '')
        print(f'= {r}')
       
        if r_prev == r:
            prev_counter += 1
        r_prev = r

    if r == p or r == 0:
        print(f'Number is divisible by {p}\n')
    else:
        print(f'Number is indivisible by {p}\n')

    
def lucas(n, p):
    cur = n
    cur_prev = 0
    prev_counter = 0
    while cur > p and cur_prev < 2:
        # search for better split s  
        splits = dict()
        cur_len = len(str(cur))
        for s in range(1, cur_len):
            a, b = split_number(cur, s)
            rn = pow(10, s, p)
            temp = rn * a + b
            splits[s] = temp
        # take minimal that divides by p, could take any shorter really
        min_s = min(splits, key = splits.get)

        a, b = split_number(cur, min_s)
        cur = splits[min_s]
        print(f'a = {a}, b = {b}, r{min_s} = {pow(10, min_s, p)}')
        print(f'r{min_s} * a + b = {pow(10, min_s, p)} * {a} + {b} = {cur}')
        if cur > p:
            print()
        if cur_prev == cur:
            prev_counter += 1
        cur_prev = cur
        
    if cur == p or cur == 0:
        print(f'Number is divisible by {p}\n')
    else:
        print(f'Number is indivisible by {p}\n')

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Error: provide three arguments")
        sys.exit(1)
    try:
        number = int(sys.argv[1])
        divisible_by = int(sys.argv[2])
        s = int(sys.argv[3])
    except ValueError:
        print("Error: arguments must be numbers")
        sys.exit(1)

    print(f'n = {number}, divisible by = {divisible_by}')
    print('\nrachinsky_1')
    rachinsky_1(number, divisible_by, s, True)
    print('\nrachinsky_2')
    rachinsky_2(number, divisible_by, True)
    print('\nrachinsky_3')
    rachinsky_3(number, divisible_by, True)
    print('\npascal')
    pascal(number, divisible_by)
    print('\nlucas')
    lucas(number, divisible_by)

