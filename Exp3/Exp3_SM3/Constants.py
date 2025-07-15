from utils import *

IV = [0x7380166f, 0x4914b2b9, 0x172442d7, 0xda8a0600, 0xa96f30bc, 0x163138aa, 0xe38dee4d, 0xb0fb0e4e]

T = [0x79cc4519] * 16 + [0x7a879d8a] * 48

def FF(x, y, z, j):
    return x ^ y ^ z if j < 16 else (x & y) | (x & z) | (y & z)

def GG(x, y, z, j):
    return x ^ y ^ z if j < 16 else (x & y) | (~x & z)

def P0(x):
    return x ^ rotl(x, 9) ^ rotl(x, 17)

def P1(x):
    return x ^ rotl(x, 15) ^ rotl(x, 23)