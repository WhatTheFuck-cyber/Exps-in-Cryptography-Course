from Constants import *

def rotl(a, k):
    k = k % 32
    return ((a << k) | (a >> (32 - k))) & 0xffffffff

def F(X, rk):
    return X[0] ^ T(X[1] ^ X[2] ^ X[3] ^ rk)

def T(x):
    B = S(x)
    return B ^ rotl(B, 2) ^ rotl(B, 10) ^ rotl(B, 18) ^ rotl(B, 24)

def T_pie(x):
    B = S(x)
    return B ^ rotl(B, 13) ^ rotl(B, 23)

def S(x):
    re = 0x0
    for i in range(4):
        y = (x >> (24 - i * 8)) & 0xff
        row = y >> 4
        col = y & 0x0f 
        re += S_BOX[row * 16 + col] << (24 - i * 8) # int
    return re


def rkey(MK):
    K = [FK[i] ^ MK[i] for i in range(4)]
    rk = []
    for i in range(32):
        K.append(K[i] ^ T_pie(K[i+1] ^ K[i+2] ^ K[i+3] ^ CK[i]))
        # print(hex(K[4]))
        rk.append(K[i+4])
    return rk

def enc(X, rk):
    for i in range(32):
        X.append(F(X[i:i+4], rk[i]))
    Y = [X[35], X[34], X[33], X[32]]
    return Y

def dec(Y, rk):
    for i in range(32):
        Y.append(F(Y[i:i+4], rk[31 - i]))
    re = [Y[35], Y[34], Y[33], Y[32]]
    return re