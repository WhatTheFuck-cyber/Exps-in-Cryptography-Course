from Constants import *

def message_padding(m: str) -> list[int]:  # `二进制字符串` 输入， `字节列表` 输出

    if not isinstance(m, str) or not all(c in {'0', '1'} for c in m):
        raise ValueError("输入必须是二进制字符串")
    
    l = len(m)
    padded_bits = m + '1'
    k = (448 - (l + 1)) % 512
    padded_bits += '0' * k
    
    length_bin = bin(l)[2:].zfill(64)  # 转为64位二进制字符串
    padded_bits += length_bin
    
    byte_list = []
    for i in range(0, len(padded_bits), 8):
        byte_str = padded_bits[i:i+8]
        byte_value = int(byte_str, 2)
        byte_list.append(byte_value)
    
    return byte_list

def message_grouping(m):  # m是一个 `字节列表``
    return [m[i:i+64] for i in range(0, len(m), 64)]  # 返回一个 `单元素64字节的列表`

def message_expansion(G):  # G是一个64字节的列表
    # 第一步：将64字节块划分为16个32位字
    W = [0] * 68
    W_ = [0] * 64
    
    # 注意：G的元素是字节，W的元素是字
    for i in range(16):
        word_bytes = G[i*4 : (i+1)*4]
        W[i] = ((word_bytes[0] << 24) | (word_bytes[1] << 16) | (word_bytes[2] << 8) | word_bytes[3]) & 0xffffffff
    
    for i in range(16, 68):
        W[i] = P1(W[i-16] ^ W[i-9] ^ rotl(W[i-3], 15)) ^ rotl(W[i-13], 7) ^ W[i-6]
        W[i] &= 0xFFFFFFFF  # 确保结果是32位整数
    
    for i in range(64):
        W_[i] = (W[i] ^ W[i+4]) & 0xFFFFFFFF  
    
    return W, W_  # W: 68个字，W_: 64个字

def CF(V, G, W, W_):
    # 初始化寄存器
    A, B, C, D, E, F, G, H = V
    
    # 循环64轮
    for i in range(64):
        # 计算SS1
        SS1 = rotl(((rotl(A, 12) + E + rotl(T[i], i % 32)) & 0xFFFFFFFF), 7)
        SS2 = SS1 ^ rotl(A, 12)
        TT1 = (FF(A, B, C, i) + D + SS2 + W_[i]) & 0xFFFFFFFF
        TT2 = (GG(E, F, G, i) + H + SS1 + W[i]) & 0xFFFFFFFF
        
        # 更新寄存器
        D = C
        C = rotl(B, 9)
        B = A
        A = TT1
        H = G
        G = rotl(F, 19)
        F = E
        E = P0(TT2)
    
    # 返回新的中间哈希值
    return [
        (V[0] ^ A) & 0xFFFFFFFF, (V[1] ^ B) & 0xFFFFFFFF, (V[2] ^ C) & 0xFFFFFFFF, (V[3] ^ D) & 0xFFFFFFFF,
        (V[4] ^ E) & 0xFFFFFFFF, (V[5] ^ F) & 0xFFFFFFFF, (V[6] ^ G) & 0xFFFFFFFF, (V[7] ^ H) & 0xFFFFFFFF]

def SM3(m_, len_bit_stream):
    
    m_ = modified_message(m_, len_bit_stream)  # 标准化消息

    m = message_padding(m_)  # 填充消息
    G = message_grouping(m)  # 分组消息
    V = IV  # 初始化中间哈希值

    for G_i in G:
        W, W_ = message_expansion(G_i)
        V = CF(V, G_i, W, W_)
    
    # 返回最终的哈希值
    return V