import sys
import math
import re
import numpy as np

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
    j_tr =  j + j_m
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
# not generalised properly
def strassen(A, B):
    sub_A = []
    sub_B = []
    # no 0's fill for matrixes with odd row/count count 
    for i in range(0, len(A), 2):
        sub_A.append([])
        for j in range(0, len(A), 2):
            sub_A[-1].append(np.array(sub2x2(A, i, j))) # use that initial matrixes are 4x4
            print(f'A{i // 2 + 1}{j // 2 + 1}')
            print(sub_A[-1][-1])

    print()
    for i in range(0, len(B), 2):
        sub_B.append([])
        for j in range(0, len(B), 2):
            sub_B[-1].append(np.array(sub2x2(B, i, j)))
            print(f'B{i // 2 + 1}{j // 2 + 1}')
            print(sub_B[-1][-1])
    print()
    A = sub_A
    B = sub_B
    D0 = (A[0][0] + A[1][1]) @ (B[0][0] + B[1][1])
    print('D0')
    print(D0)

    D1 = (A[0][1] - A[1][1]) @ (B[1][0] + B[1][1])
    print('D1')
    print(D1)

    D2 = (A[1][0] - A[0][0]) @ (B[0][0] + B[0][1])
    print('D2')
    print(D2)

    D3 = (A[0][0] + A[0][1]) @ B[1][1] 
    print('D3')
    print(D3)

    D4 = A[0][0] @ (B[0][1] - B[1][1])
    print('D4')
    print(D4)

    D5 = A[1][1] @ (B[1][0] - B[0][0])
    print('D5')
    print(D5)

    D6 = (A[1][0] + A[1][1]) @ B[0][0]
    print('D6')
    print(D6)

    a = D0 + D1 - D3 + D5
    b = D3 + D4
    c = D5 + D6
    d = D0 + D2 + D4 - D6
    r = np.vstack([np.hstack([a, b]), np.hstack([c, d])])   
    print('Result')
    print(r)


if __name__ == "__main__":
    with open('matrix_4A.txt', 'r') as f:
        lines = f.readlines()

    A = []
    for line in lines:
        values = line.strip().split()
        A.append([int(v) for v in values])
    print('A')
    print_matrix(A)
    print()

    with open('matrix_4B.txt', 'r') as f:
        lines = f.readlines()

    B = []
    for line in lines:
        values = line.strip().split()
        B.append([int(v) for v in values])
    print('B')
    print_matrix(B)

    print('\nstrassen')
    strassen(A, B)


