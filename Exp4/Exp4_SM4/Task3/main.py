from utils import *

if __name__ == '__main__':
    X = [0x01234567, 0x89ABCDEF, 0xFEDCBA98, 0x76543210]
    MK = [0x01234567, 0x89ABCDEF, 0xFEDCBA98, 0x76543210]
    rk = rkey(MK)
    C = X
    for i in range(10):
        C = enc(C, rk)
    for x in C:
        print('{0:08x}'.format(x), end=' ')
        re = C
    for i in range(10):
        re = dec(re, rk)
    print()
    for x in re:
        print('{0:08x}'.format(x), end=' ')