from ..ZUC import params
from ..ZUC.ZUC_constant import *

def LFSRWithInitialisationMode(u):

    v = (2**15 * params.S[15] + 2**17 * params.S[13] + 2**21 * params.S[10] + 2**20 * params.S[4] + (2**8 + 1) * params.S[0]) % (2**31 - 1)
    S_16 = (v + u) % (2**31 - 1)
    if S_16 == 0:
        S_16 = 2**31 - 1
    params.S[:] = params.S[1:] + [S_16]

def LFSRWithWorkMode():

    v = (2**15 * params.S[15] + 2**17 * params.S[13] + 2**21 * params.S[10] + 2**20 * params.S[4] + (2**8 + 1) * params.S[0]) % (2**31 - 1)
    S_16 = v
    if S_16 == 0:
        S_16 = 2**31 - 1
    params.S[:] = params.S[1:] + [S_16]

def BitReconstruction():

    params.X[0] = ((params.S[15] >> 15) << 16) | (params.S[14] & 0xffff)
    params.X[1] = ((params.S[11] & 0xffff) << 16) | (params.S[9] >> 15)
    params.X[2] = ((params.S[7] & 0xffff) << 16) | (params.S[5] >> 15)
    params.X[3] = ((params.S[2] & 0xffff) << 16) | (params.S[0] >> 15)

def F(): 

    W = add_mod((params.X[0] ^ params.R1), params.R2) 
    W_1 = add_mod(params.R1, params.X[1])
    W_2 = params.R2 ^ params.X[2]

    temp_1 = ((W_1 & 0xffff) << 16) | ((W_2 >> 16)) 
    temp_2 = ((W_2 & 0xffff) << 16) | ((W_1 >> 16))
    params.R1 = S_box(Liner_1(temp_1))
    params.R2 = S_box(Liner_2(temp_2))

    return W