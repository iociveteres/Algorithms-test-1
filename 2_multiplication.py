import sys
import math
import re

def split_a(n: int, s: int) -> tuple[int, int]:
    power = 10 ** (s)
    quotient, remainder = divmod(n, power)
    return quotient, remainder

def calc_b_(b: int) -> int:
    return 10 - b if b in {1, 9} else b

def digitize(n):
    return [int(i) for i in str(n)]

def dedigitize(numList):
    s = ''.join(map(str, numList))
    return int(s)

def fourier(a, b): 
    a_r = digitize(a)[::-1] # reversed upper number
    b_ = digitize(b) # bottom number
    b_r = b_[::-1] # reversed bottom number, needed for simplier indexing
    result = []
    upper_padding = len(b_) - 1
    overflow = 0 # flag to show if got "digit" greater than 10

    for i in range(len(a_r) + len(b_) - 1):
        print(f'Step {i}')
        print(f'{dedigitize(a_r):{len(a_r) + upper_padding}}')
        print(' '*i + f'{b}')

        l_u = i if i < (len(a_r) - 1) else (len(a_r) - 1) # leftest digit of upper number
        if overflow == 0: 
            result.append(0)
        else:
            overflow -= 1 
        for j in range(0, len(b_)):
            l_d = j if i < (len(a_r)) else (i - len(a_r) + 1 + j) # leftest digit of bottom number under rightest digit
            if (len(b_) - l_d) <= 0: # no digits in the lower to multiply
                break
            result[i] += a_r[l_u - j] * b_r[l_d]                
            if (l_u - l_d) <= 0: # no digits in the upper to multiply
                break
        # deal with overflow
        k = i
        while (result[k] >= 10): 
            quotient, remainder = divmod(result[k], 10)
            result[k] = remainder
            if len(result) - 1 < k + 1: # if needed add digit
                result.append(quotient)
                overflow += 1
            else:
                result[k + 1] += quotient 
            k += 1
        print(' '*(i + upper_padding - 1*overflow) + f'{dedigitize(result[::-1])}')
        print()
    return dedigitize(result[::-1])

def shortened(a, b):
    # Make vectors
    to_sum = []
    a_ = digitize(a)
    b_ = digitize(b)
    for i in range(0, len(a_) - len(b_)):
        b_.insert(0, 0)

    print(' ' * (len(a_) // 2) + ''.join(map(str, a_)))
    print(' ' * (len(b_) // 2) + ''.join(map(str, b_)))
    print('-' * (2 * len(a_)))

    for iteration, _ in enumerate(b_):
        temp = []
        x_wideness = iteration
        if x_wideness == 0: # easier to do it differently for 0 and everything else
            for i in range(len(b_)):
                r = a_[i] * b_[i]
                r = digitize(r)
                if len(r) == 1: # len(r) can't be gt 2
                    r.insert(0, 0)
                temp += r 
            to_sum.append(temp)
        else:
            for i in range(len(b_) - x_wideness):
                r = a_[i] * b_[i + x_wideness] + b_[i] * a_[i + x_wideness]
                r = digitize(r)
                if len(r) == 1: 
                    r.insert(0, 0)
                if len(r) == 3: # max is 9*9 + 9*9 = 162, three digits, so one digit overflow
                    temp[-1] += r.pop(0)
                temp += r 
            to_sum.append(temp)
        
        print(' ' * x_wideness, end = '')
        print(''.join(map(str, to_sum[-1])), end = '')
        print(' ' * x_wideness, end = '')
        print()
    # Fill shorter from boths sides
    for index, row in enumerate(to_sum):
        for i in range(index):
            row.insert(0, 0)
            row.append(0)
    # Sum
    summed = [sum(i) for i in zip(*to_sum)]
    # Deal with overflow
    # in fourier number was reversed, so overflow there is reversed, relative to it
    # because of direct order have to think about secondary overflow
    # doing it in reverse order is much wiser
    i = 0
    while i < len(summed):
        if (summed[i] >= 10):
            quotient, remainder = divmod(summed[i], 10)
            summed[i] = remainder
            if len(summed) - 1 < i + 1: # if needed add digit
                summed.insert(0, quotient)
            else:
                summed[i - 1] += quotient 
                i -= 2
        i += 1
    print('-' * (2 * len(a_)))
    print(''.join(map(str, summed)))
    result = dedigitize(summed)
    return result

def russian(a, b):
    to_mul = []
    to_mul.append(a)
    to_divide = []
    to_divide.append(b)

    while True:
        print(f'{to_divide[-1]:6} | ', end = '')
        print(f'{to_mul[-1]:10}', end = '')
        if to_divide[-1] % 2 == 0:
            print('-')
        else:
            print()
        if to_divide[-1] == 1:
            break
        to_divide.append(to_divide[-1] // 2)
        to_mul.append(to_mul[-1] * 2)
       
    sum = 0
    for (d, m) in zip(to_divide, to_mul):
        if d % 2 != 0:
            sum += m

    print('-'*20)
    print(' '*6 + f' | {sum:10}')
    return sum
        
def karatsuba(a, b):
    print('Use this:  https://tinsed.github.io/pages/karatsuba.html')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Error: provide two arguments")
        sys.exit(1)
    try:
        a = int(sys.argv[1])
        b = int(sys.argv[2])
    except ValueError:
        print("Error: arguments must be as")
        sys.exit(1)

    print(f'a = {a}, b = {b}')
    print('\nfourier')
    fourier(a, b)
    print('\nshortened')
    shortened(a, b)
    print('\nrussian')
    russian(a, b)
    print('\nkaratsuba')
    karatsuba(a, b)


