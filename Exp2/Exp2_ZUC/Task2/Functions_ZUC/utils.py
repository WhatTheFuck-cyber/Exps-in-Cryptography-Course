'''
包含process_func.py中所有函数的实现
'''

from ..Constants_ZUC.D_VECTOR import *  
from ..Constants_ZUC.S_BOX import *
# from sys_import import *

def add_mod(a, b):  # 
    return (a + b) % (2 ** 32)

def circular_shift(x, n): 
    return ((x << n) | (x >> (32 - n))) & 0xffffffff

def Liner_1(x): 
    return x ^ circular_shift(x, 2) ^ circular_shift(x, 10) ^ circular_shift(x, 18) ^ circular_shift(x, 24)


def Liner_2(x): 
    return x ^ circular_shift(x, 8) ^ circular_shift(x, 14) ^ circular_shift(x, 22) ^ circular_shift(x, 30)

def S_box_operation(x): 

    x0 = (x >> 24) & 0xff
    x1 = (x >> 16) & 0xff
    x2 = (x >> 8) & 0xff
    x3 = x & 0xff
    y0 = S0[x0 >> 4][x0 & 0xf]
    y1 = S1[x1 >> 4][x1 & 0xf] 
    y2 = S0[x2 >> 4][x2 & 0xf] 
    y3 = S1[x3 >> 4][x3 & 0xf] 
    return (y0 << 24) | (y1 << 16) | (y2 << 8) | y3