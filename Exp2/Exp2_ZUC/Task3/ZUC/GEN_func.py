from ..ZUC.utils import *

def initialize_lfsr(): # OK
    W = 0
    for i in range(16):
        params.S[i] = (params.key[i] << 23) | (D[i] << 8) | params.iv[i]
    for i in range(32):
        BitReconstruction()
        W = F() # 这里需要传入X0, X1, X2
        LFSRWithInitialisationMode(W >> 1)

def generate_key(): # OK
    BitReconstruction()
    F()
    LFSRWithWorkMode()
    for _ in range(params.key_length):
        BitReconstruction()
        W = F()
        params.keys.append(W ^ params.X[3])
        LFSRWithWorkMode()

def display_key(): # OK
    for i in range(params.key_length):
        print(f"z{i+1}: {params.keys[i]:08x}")