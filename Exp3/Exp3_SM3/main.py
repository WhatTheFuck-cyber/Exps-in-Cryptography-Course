from SM3 import *

if __name__ == "__main__":
    m1 = 0x616263  # 输入消息
    res1 = SM3(m1, 24)  # 期望答案：66c7f0f4 62eeedd9 d1f2d46b dc10e4e2 4167c487 5cf2f7a2 297da02b 8f4ba8e0
    print('res1: ', end = '')
    for num in res1:
        print(f"{num:08x}", end = ' ')  
    print('\n', end = '')

    m2 = 0x61626364616263646162636461626364616263646162636461626364616263646162636461626364616263646162636461626364616263646162636461626364
    res2 = SM3(bin(m2)[2 : ].zfill(4 * 128), 4 * 128)  # 期望答案：debe9ff9 2275b8a1 38604889 c18e5a4d 6fdb70e5 387e5765 293dcba3 9c0c5732
    print('res2: ', end = '')
    for num in res2:
        print(f"{num:08x}", end = ' ')

'''
本项目支持整数、整数列表、字符串三种输入方式
'''