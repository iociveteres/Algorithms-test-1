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

def print_matrix(A):
    for row in A:
        for col in row:
            print(f'{col:6g}', end = '')
        print()

def sub2x2(A, i, j):
    a = []
    a.append([A[i][j], A[i][j + 1]])
    a.append([A[i + 1][j], A[i + 1][j + 1]])
    return a

def chio_sub2x2(A, i, j):
    a = []
    a.append([A[0][0], A[0][j + 1]])
    a.append([A[i + 1][0], A[i + 1][j + 1]])
    return a

def chio_gen_sub2x2(A, i, j, i_m, j_m): # only for k = 1
    a = []
    # find coordinates for
    i_tr = i_m # top left el
    j_tr = j + j_m
    if j >= 0:
        j_tr += 1

    i_bl = i + i_m # bot left el
    if i >= 0:
        i_bl += 1
    j_bl = j_m

    i_br = i + i_m # bot right el
    if i >= 0:
        i_br += 1
    j_br = j + j_m
    if j >= 0:
        j_br += 1
    if i_m < i_bl: # change order if lower row is higher
        if j_m < j_tr: # or lefter col is righter
            a.append([A[i_m][j_m], A[i_tr][j_tr]]) # don't like how it is looking
            a.append([A[i_bl][j_bl], A[i_br][j_br]])
        else:
            a.append([A[i_m][j_m], A[i_tr][j_tr]][::-1])
            a.append([A[i_bl][j_bl], A[i_br][j_br]][::-1])
    else: 
        if j_m < j_tr:
            a.append([A[i_bl][j_bl], A[i_br][j_br]])
            a.append([A[i_m][j_m], A[i_tr][j_tr]])
        else:
            a.append([A[i_bl][j_bl], A[i_br][j_br]][::-1])
            a.append([A[i_m][j_m], A[i_tr][j_tr]][::-1])
    return a

def det2x2(a, printing = False):
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    if (printing):
        print(f'|A| = ad - bc = {a[0][0]} * {a[1][1]} - {a[0][1]} * {a[1][0]} = {det}')
    return det

def find_minor(A):
    i = 1
    while True:
        for i_row, row in enumerate(A):
            for i_col, col in enumerate(row):
                if col == i:
                    return i_row, i_col
                elif col == -i:
                    return i_row, i_col
        i += 1

def chio_condensation(A):
    new_A = []
    prev_A = []
    cur_A = A
    coef = 1

    for k in range(len(A) - 1):
        dim = len(cur_A) - 1
        try:
            coef *= 1/(cur_A[0][0] **(dim - 1))
        except ZeroDivisionError:
            print("Error: arguments must be numbers")
            return None
        print(f'coef = {coef:g} (*= 1/{cur_A[0][0]} ^ {dim - 1})')
        for i in range(dim):
            row = []
            for j in range(dim):
                det = det2x2(chio_sub2x2(cur_A, i, j))
                
                row.append(det)
            new_A.append(row)

        print_matrix(new_A)
        print()

        prev_A = cur_A
        cur_A = new_A
        new_A = []

    a = cur_A[0][0]
    a *= coef
    print(f'\ndet = {coef} * {cur_A[0][0]} = {a}')
    return a
# for k = 1
# generalising k would took more time
def generalised_chio_condensation(A, k = 1):
    new_A = []
    prev_A = []
    cur_A = A
    coef = 1
    print(f'k = {k}')
    for p in range(len(A) - 1):
        dim = len(cur_A) - 1

        i_m, j_m = find_minor(cur_A)
        minor = cur_A[i_m][j_m]
        print(f'minor is {minor} at {i_m}, {j_m}')

        coef *= 1/(minor**(dim - 1))
        print(f'coef = {coef:g} (*= 1/{minor} ^ {dim - 1})')
        for i in range(-i_m, dim - i_m):
            row = []
            for j in range(-j_m, dim - j_m):
                t = chio_gen_sub2x2(cur_A, i, j, i_m, j_m)
                det = det2x2(t)
                
                row.append(det)
            new_A.append(row)

        print_matrix(new_A)
        print()

        prev_A = cur_A
        cur_A = new_A
        new_A = []

    a = cur_A[0][0]
    a *= coef
    print(f'\ndet = {coef} * {cur_A[0][0]} = {a}')
    return a

def dodgson_condensation(A):
    new_A = []
    prev_A = []
    cur_A = A

    print_matrix(A)
    print()
    for k in range(len(A) - 1):
        dim = len(cur_A) - 1
        for i in range(dim):
            row = []
            for j in range(dim):
                det = det2x2(sub2x2(cur_A, i, j))
                if k != 0: 
                    try:
                        coef = 1/prev_A[i + 1][j + 1]
                        det *= coef
                    except ZeroDivisionError:
                        print(f'In prev matrix element at {i + 1}, {j + 1} is 0')
                        print(f'Try another linear combination of rows')
                        return None
                    #print(f'{coef:g}')
                    
                row.append(det)
            new_A.append(row)

        print_matrix(new_A)
        print()

        prev_A = cur_A
        cur_A = new_A
        new_A = []

    return cur_A[0]

if __name__ == "__main__":
    with open('matrix_3.txt', 'r') as f:
        lines = f.readlines()

    A = []
    for line in lines:
        values = line.strip().split()
        A.append([int(v) for v in values])
    print_matrix(A)

    print('\nchio_condenastion')
    chio_condensation(A)
    print('\ngeneralised_chio_condensation')
    generalised_chio_condensation(A)
    print('\ndodgson_condensation')
    dodgson_condensation(A)

