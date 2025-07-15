'''
包含process.py中所有函数的实现
'''

from ..Constants_ZUC.D_VECTOR import *  
from ..Constants_ZUC.S_BOX import *
# from sys_import import * 
from .utils import *


def LFSRWithInitialisationMode(u, S):    # 初始化阶段中的LFSR工作流程
    v = (2**15 * S[15] + 2**17 * S[13] + 2**21 * S[10] + 2**20 * S[4] + (2**8 + 1) * S[0]) % (2**31 - 1)
    S_16 = (v + u) % (2**31 - 1)
    if S_16 == 0:
        S_16 = 2**31 - 1
    S[:] = S[1:] + [S_16]
    return S

def LFSRWithWorkMode(S):    # 工作阶段中的LFSR工作流程
    v = (2**15 * S[15] + 2**17 * S[13] + 2**21 * S[10] + 2**20 * S[4] + (2**8 + 1) * S[0]) % (2**31 - 1)
    S_16 = v
    if S_16 == 0:
        S_16 = 2**31 - 1
    S[:] = S[1:] + [S_16]
    return S

def BitReconstruction(S, X):    # 比特重组

    '''
    X[0] = ((S[15] & 0x7FFF8000) << 1) | (S[14] & 0x0000FFFF) 
    X[1] = ((S[11] & 0x0000FFFF) << 16) | ((S[9] & 0x7FFF8000) >> 15) 
    X[2] = ((S[7] & 0x0000FFFF) << 16) | ((S[5] & 0x7FFF8000) >> 15) 
    X[3] = ((S[2] & 0x0000FFFF) << 16) | ((S[0] & 0x7FFF8000) >> 15)
    '''

    X[0] = (((S[15] >> 15) << 16) | (S[14] & 0xffff))
    X[1] = (((S[11] & 0xffff) << 16) | (S[9] >> 15))
    X[2] = (((S[7] & 0xffff) << 16) | (S[5] >> 15))
    X[3] = (((S[2] & 0xffff) << 16) | (S[0] >> 15))
    return X

def F(X, R1, R2):    # 线性变换函数
    '''
    global R1, R2, X

    W = ((X[0] ^ R1) + R2) & 0xFFFFFFFF  
    
    W1 = (R1 + X[1]) & 0xFFFFFFFF   
    W2 = (R2 ^ X[2]) & 0xFFFFFFFF 
    
    W1L, W1H = (W1 & 0xFFFF), (W1 >> 16)  
    W2L, W2H = (W2 & 0xFFFF), (W2 >> 16)
    
    input_R1 = (W1L << 16) | W2H   
    input_R2 = (W2L << 16) | W1H   
    
    R1 = S_box(Liner_1(input_R1))     
    R2 = S_box(Liner_2(input_R2))      

    return W
    '''
    
    W = add_mod((X[0] ^ R1), R2) 
    W_1 = add_mod(R1, X[1])
    W_2 = R2 ^ X[2]

    temp_1 = ((W_1 & 0xffff) << 16) | ((W_2 >> 16)) 
    temp_2 = ((W_2 & 0xffff) << 16) | ((W_1 >> 16))
    R1 = S_box_operation(Liner_1(temp_1))
    R2 = S_box_operation(Liner_2(temp_2))

    return W, R1, R2