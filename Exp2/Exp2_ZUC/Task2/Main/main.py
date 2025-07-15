from ..Functions_ZUC.process import *    

Invalid_Flag = 0

S = [0] * 16    # 线性循环位移寄存器，每个长度为31bit
X = [0] * 4     # 比特重组寄存器，每个长度为32bit
keys = []       # 密钥流
R1,R2 =0, 0,     # 线性反馈移位寄存器（LFSR）中的两个寄存器

def clear_cache():
    global S, X, keys, R1, R2
    S = [0] * 16
    X = [0] * 4
    keys = []
    R1, R2 = 0, 0,

if __name__ == "__main__":

    key_length = 2  # 密钥流长度，单个密钥长为32bit

    ## 前两个样例是测试代码的正确性，后两个样例是使用代码得出ZUC的密钥流
    key1 = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    iv1 = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    S, X, keys, R1, R2 = initialize_lfsr(key1, iv1, S, X, keys, R1, R2)
    S, X, keys, R1, R2 = generate_key(key_length, S, X, keys, R1, R2)
    print("-----------------------------------------------------")
    display_key(key_length, keys)
    save_key(key_length, keys, 1, Invalid_Flag)
    clear_cache()
    print("保存后清空之前的缓存。")
    print("-----------------------------------------------------")

    key2 = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff]
    iv2 = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff]
    S, X, keys, R1, R2 = initialize_lfsr(key2, iv2, S, X, keys, R1, R2)
    S, X, keys, R1, R2 = generate_key(key_length, S, X, keys, R1, R2)
    print("-----------------------------------------------------")
    display_key(key_length, keys)
    save_key(key_length, keys, 2, Invalid_Flag)
    clear_cache()
    print("保存后清空之前的缓存。")
    print("-----------------------------------------------------")
    
    key3 = [0x3d, 0x4c, 0x4b, 0xe9, 0x6a, 0x82, 0xfd, 0xae, 0xb5, 0x8f, 0x64, 0x1d, 0xb1, 0x7b, 0x45, 0x5b]
    iv3 = [0x84, 0x31, 0x9a, 0xa8, 0xde, 0x69, 0x15, 0xca, 0x1f, 0x6b, 0xda, 0x6b, 0xfb, 0xd8, 0xc7, 0x66]
    S, X, keys, R1, R2 = initialize_lfsr(key3, iv3, S, X, keys, R1, R2)
    S, X, keys, R1, R2 = generate_key(key_length, S, X, keys, R1, R2)
    print("-----------------------------------------------------")
    display_key(key_length, keys)
    save_key(key_length, keys, Invalid_Flag, 1)
    clear_cache()
    print("保存后清空之前的缓存。")
    print("-----------------------------------------------------")

    key4 = [0x3d, 0x4c, 0x4b, 0xe9, 0x6a, 0x82, 0xfd, 0xae, 0xb5, 0x8f, 0x64, 0x1d, 0xb1, 0x7b, 0x45, 0x5c]
    iv4 = [0x84, 0x31, 0x9a, 0xa8, 0xde, 0x69, 0x15, 0xca, 0x1f, 0x6b, 0xda, 0x6b, 0xfb, 0xd8, 0xc7, 0x66]
    S, X, keys, R1, R2 = initialize_lfsr(key4, iv4, S, X, keys, R1, R2)
    S, X, keys, R1, R2 = generate_key(key_length, S, X, keys, R1, R2)
    print("-----------------------------------------------------")
    display_key(key_length, keys)
    save_key(key_length, keys, Invalid_Flag, 2)
    clear_cache()
    print("保存后清空之前的缓存。")
    print("-----------------------------------------------------")

'''
result_log_path = ../ZUC/Task2/Log/key.json
'''
# cd "....../Exp2_ZUC"
# python -m Task2.Main.main