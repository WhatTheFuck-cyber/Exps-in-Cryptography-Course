'''
本模块用于初始化ZUC算法的参数
'''

import math

COUNT = [0] * 4  #32位
iv = [0] * 16 #128位
BEARER = 0 #5位
DIRECTION = 0 #1位
LENGTH = 0

L = 0 #4字节

S = [0] * 16 
X = [0] * 4
key = [0] * 16 #128位
keys = [] 
key_length = 0
R1 = 0
R2 = 0

def __init__(count, bearer, direction, length, key_):
    global COUNT, BEARER, DIRECTION, LENGTH, L, key, key_length

    COUNT = count
    BEARER = bearer
    DIRECTION = direction
    LENGTH = length

    key = key_

    L = math.ceil(LENGTH / 32)
    key_length = math.ceil(LENGTH / 32)


def show_params():
    print(f"COUNT: {COUNT}")
    print(f"iv: {iv}")
    print(f"BEARER: {BEARER}")
    print(f"DIRECTION: {DIRECTION}")
    print(f"LENGTH: {LENGTH}")
    print(f"L: {L}")
    print(f"S: {S}")
    print(f"X: {X}")
    print(f"key: {key}")
    print(f"keys: {keys}")
    print(f"key_length: {key_length}")
    print(f"R1: {R1}")
    print(f"R2: {R2}")

def gen_iv():
    global iv

    iv[0] = COUNT[0]
    iv[1] = COUNT[1]
    iv[2] = COUNT[2]
    iv[3] = COUNT[3]
    iv[4] = (BEARER << 3) | (DIRECTION << 2) | 0b00 
    iv[5] = iv[6] = iv[7] = 0
    iv[8] = iv[0]
    iv[9] = iv[1]
    iv[10] = iv[2]
    iv[11] = iv[3]
    iv[12] = iv[4]
    iv[13] = iv[5]
    iv[14] = iv[6]
    iv[15] = iv[7]

def clear_cache():
    global COUNT, iv, BEARER, DIRECTION, LENGTH, L, S, X, key, keys, key_length, R1, R2

    COUNT = [0] * 4  #32位
    iv = [0] * 16 #128位
    BEARER = 0 #5位
    DIRECTION = 0 #1位
    LENGTH = 0

    L = 0 #4字节

    S = [0] * 16 
    X = [0] * 4
    key = [0] * 16 #128位
    keys = [] 
    key_length = 0
    R1 = 0
    R2 = 0