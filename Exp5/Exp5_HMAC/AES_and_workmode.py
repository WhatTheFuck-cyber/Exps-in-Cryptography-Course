import galois
def SBOX(a: int) -> int:
    """S盒变换"""
    GF = galois.GF(2**8, irreducible_poly=0x11B)
    b = int(GF(a) ** (-1)) if a != 0 else 0
    return b ^ ((b << 1) & 0xff | (b >> 7)) ^ ((b << 2) & 0xff | (b >> 6)) ^ ((b << 3) & 0xff | (b >> 5)) ^ ((b << 4) & 0xff | (b >> 4)) ^ 0x63

def INVSBOX(c : int) -> int:
    """S盒的逆变换"""
    b = ((c << 1) & 0xff | (c >> 7)) ^ ((c << 3) & 0xff | (c >> 5)) ^ ((c << 6) & 0xff | (c >> 2)) ^ 0x05
    # 在GF(2^8)上求逆
    GF = galois.GF(2**8, irreducible_poly=0x11B)
    return int(GF(b) ** (-1)) if b != 0 else 0

# 实际上，可以不使用galois库：
'''
def SBOX(a:int) -> int:
    """S盒变换"""
    if a == 0:
        return 0x63  
    u, v = a, 0x11B  
    x1, x2 = 1, 0
    while u != 1:
        j = len(bin(u)) - len(bin(v))
        if j < 0:
            u, v = v, u
            x1, x2 = x2, x1
            continue
        u ^= (v << j)
        x1 ^= (x2 << j)
    b = x1
    c = b
    for i in range(4):  
        b = ((b << 1) | (b >> 7)) & 0xFF
        c ^= b
    return c ^ 0x63

def INVSBOX(c:int) -> int:
    """S盒的逆变换"""
    b = 0
    for i in range(8):
        bit1 = (c >> ((i + 7) % 8)) & 1  
        bit3 = (c >> ((i + 5) % 8)) & 1  
        bit6 = (c >> ((i + 2) % 8)) & 1  
        new_bit = (bit1 ^ bit3 ^ bit6 ^ ((0x05 >> i) & 1))
        b |= (new_bit << i)
    if b == 0:
        return 0
    poly = 0x11B 
    u, v = b, poly
    x1, x2 = 1, 0
    while u != 1:
        j = u.bit_length() - v.bit_length()
        if j < 0:
            u, v = v, u
            x1, x2 = x2, x1
            j = -j
        u ^= (v << j)
        x1 ^= (x2 << j)
    a = x1
    return a
'''

# ----------------------------------------------------------------------------------------------------------------------------------------------------------- #

Rcon = [0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]

def key_expansion(key_bytes, key_size_in_bits):
    Nk = key_size_in_bits // 32
    if Nk == 4: Nr = 10
    elif Nk == 6: Nr = 12
    elif Nk == 8: Nr = 14
    Nb = 4
    w = [[0]*4 for _ in range(Nb * (Nr + 1))]
    for i in range(Nk):
        w[i] = list(key_bytes[4*i : 4*(i+1)])
    for i in range(Nk, Nb * (Nr + 1)):
        temp = list(w[i-1])
        if i % Nk == 0:
            temp = temp[1:] + temp[:1]
            temp = [SBOX(b) for b in temp]
            temp[0] = temp[0] ^ Rcon[i // Nk]
        elif Nk > 6 and i % Nk == 4:
            temp = [SBOX(b) for b in temp]
        w[i] = [w[i-Nk][j] ^ temp[j] for j in range(4)]
    round_keys_matrices = []
    for round_num in range(Nr + 1):
        round_key_matrix = [[0]*4 for _ in range(4)]
        for c in range(4):
            word_from_w = w[round_num * Nb + c]
            for r in range(4):
                round_key_matrix[r][c] = word_from_w[r]
        round_keys_matrices.append(round_key_matrix)
    return round_keys_matrices

# ----------------------------------------------------------------------------------------------------------------------------------------------------------- #

def hex_to_bytes(hex_str):
    return bytes.fromhex(hex_str)

def bytes_to_hex(bytes_data):
    if isinstance(bytes_data, list):
        bytes_data = bytes(bytes_data)
    return bytes_data.hex().upper()

def bytes_to_state(bytes_data):
    state = [[0]*4 for _ in range(4)]
    for i in range(16):
        state[i % 4][i // 4] = bytes_data[i]
    return state

def state_to_bytes(state):
    bytes_data = []
    for i in range(4):
        for j in range(4):
            bytes_data.append(state[j][i])
    return bytes_data

def add_round_key(state, round_key):
    for i in range(4):
        for j in range(4):
            state[i][j] ^= round_key[i][j]
    return state

def sub_bytes(state):
    for i in range(4):
        for j in range(4):
            state[i][j] = SBOX(state[i][j])
    return state

def shift_rows(state):
    state[1] = state[1][1:] + state[1][:1]
    state[2] = state[2][2:] + state[2][:2]
    state[3] = state[3][3:] + state[3][:3]
    return state

def mix_columns(state):
    for i in range(4):
        a0 = state[0][i]
        a1 = state[1][i]
        a2 = state[2][i]
        a3 = state[3][i]
        
        state[0][i] = gf_mul(0x02, a0) ^ gf_mul(0x03, a1) ^ a2 ^ a3
        state[1][i] = a0 ^ gf_mul(0x02, a1) ^ gf_mul(0x03, a2) ^ a3
        state[2][i] = a0 ^ a1 ^ gf_mul(0x02, a2) ^ gf_mul(0x03, a3)
        state[3][i] = gf_mul(0x03, a0) ^ a1 ^ a2 ^ gf_mul(0x02, a3)
    return state

def gf_mul(a, b):
    p = 0
    for i in range(8):
        if b & 1:
            p ^= a
        high_bit_set = a & 0x80
        a <<= 1
        if high_bit_set:
            a ^= 0x1B  # x^8 + x^4 + x^3 + x + 1
        b >>= 1
    return p & 0xFF

def inv_sub_bytes(state):
    for i in range(4):
        for j in range(4):
            state[i][j] = INVSBOX(state[i][j])
    return state

def inv_shift_rows(state):
    state[1] = state[1][-1:] + state[1][:-1]
    state[2] = state[2][-2:] + state[2][:-2]
    state[3] = state[3][-3:] + state[3][:-3]
    return state

def inv_mix_columns(state):
    for i in range(4):
        a0 = state[0][i]
        a1 = state[1][i]
        a2 = state[2][i]
        a3 = state[3][i]
        
        state[0][i] = gf_mul(0x0E, a0) ^ gf_mul(0x0B, a1) ^ gf_mul(0x0D, a2) ^ gf_mul(0x09, a3)
        state[1][i] = gf_mul(0x09, a0) ^ gf_mul(0x0E, a1) ^ gf_mul(0x0B, a2) ^ gf_mul(0x0D, a3)
        state[2][i] = gf_mul(0x0D, a0) ^ gf_mul(0x09, a1) ^ gf_mul(0x0E, a2) ^ gf_mul(0x0B, a3)
        state[3][i] = gf_mul(0x0B, a0) ^ gf_mul(0x0D, a1) ^ gf_mul(0x09, a2) ^ gf_mul(0x0E, a3)
    return state

def aes_encrypt_block(plaintext_block, key_bytes, key_size_in_bits):
    round_keys = key_expansion(key_bytes, key_size_in_bits)
    state = bytes_to_state(plaintext_block)
    state = add_round_key(state, round_keys[0])
    
    Nk = key_size_in_bits // 32
    if Nk == 4: Nr = 10
    elif Nk == 6: Nr = 12
    elif Nk == 8: Nr = 14
    
    for round_num in range(1, Nr):
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, round_keys[round_num])
    
    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, round_keys[Nr])
    
    return state_to_bytes(state)

def aes_decrypt_block(ciphertext_block, key_bytes, key_size_in_bits):
    round_keys = key_expansion(key_bytes, key_size_in_bits)
    state = bytes_to_state(ciphertext_block)
    state = add_round_key(state, round_keys[-1])
    
    Nk = key_size_in_bits // 32
    if Nk == 4: Nr = 10
    elif Nk == 6: Nr = 12
    elif Nk == 8: Nr = 14
    
    for round_num in range(Nr-1, 0, -1):
        state = inv_shift_rows(state)
        state = inv_sub_bytes(state)
        state = add_round_key(state, round_keys[round_num])
        state = inv_mix_columns(state)
    
    state = inv_shift_rows(state)
    state = inv_sub_bytes(state)
    state = add_round_key(state, round_keys[0])
    
    return state_to_bytes(state)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------- #

def cbc_encrypt(plaintext, key_bytes, iv_bytes, use_padding=True):
    block_size = 16
    if use_padding:
        # 填充明文到块大小的整数倍 (PKCS#7 填充)
        padding_length = block_size - (len(plaintext) % block_size)
        padded_plaintext = plaintext + bytes([padding_length]) * padding_length
    else:
        if len(plaintext) % block_size != 0:
            raise ValueError("明文长度必须是块大小的整数倍，或者启用填充")
        padded_plaintext = plaintext
    
    ciphertext = bytearray()
    previous_block = iv_bytes
    
    for i in range(0, len(padded_plaintext), block_size):
        block = padded_plaintext[i:i+block_size]
        # 异或上一个密文块 (或 IV)
        xored_block = bytes(a ^ b for a, b in zip(block, previous_block))
        encrypted_block = aes_encrypt_block(xored_block, key_bytes, len(key_bytes) * 8)
        ciphertext.extend(encrypted_block)
        previous_block = encrypted_block
    
    return bytes(ciphertext)

def cbc_decrypt(ciphertext, key_bytes, iv_bytes, use_padding=True):
    block_size = 16
    if len(ciphertext) % block_size != 0:
        raise ValueError("密文长度必须是块大小的整数倍")
    
    plaintext = bytearray()
    previous_block = iv_bytes
    
    for i in range(0, len(ciphertext), block_size):
        block = ciphertext[i:i+block_size]
        decrypted_block = aes_decrypt_block(block, key_bytes, len(key_bytes) * 8)
        # 异或上一个密文块 (或 IV)
        plaintext_block = bytes(a ^ b for a, b in zip(decrypted_block, previous_block))
        plaintext.extend(plaintext_block)
        previous_block = block
    
    # 移除填充 (PKCS#7)
    if use_padding and plaintext:
        padding_length = plaintext[-1]
        if padding_length < 1 or padding_length > block_size:
            raise ValueError("无效的填充长度")
        if plaintext[-padding_length:] != bytes([padding_length]) * padding_length:
            raise ValueError("无效的填充")
        return bytes(plaintext[:-padding_length])
    return plaintext

def increment_counter(counter_bytes):
    """递增CTR模式的计数器值（大端序）"""
    counter = int.from_bytes(counter_bytes, 'big')
    counter += 1
    return counter.to_bytes(16, 'big')

def ctr_encrypt(plaintext, key_bytes, init_counter_bytes):
    """CTR模式加密（与解密逻辑相同）"""
    block_size = 16
    ciphertext = bytearray()
    counter = init_counter_bytes
    
    for i in range(0, len(plaintext), block_size):
        block = plaintext[i:i+block_size]
        
        # 加密当前计数器值
        keystream_block = aes_encrypt_block(counter, key_bytes, len(key_bytes) * 8)
        
        # 与明文块异或（处理最后一个可能不足块大小的块）
        xored_block = bytes(a ^ b for a, b in zip(block, keystream_block[:len(block)]))
        ciphertext.extend(xored_block)
        
        # 递增计数器
        counter = increment_counter(counter)
    
    return bytes(ciphertext)

def ctr_decrypt(ciphertext, key_bytes, init_counter_bytes):
    return ctr_encrypt(ciphertext, key_bytes, init_counter_bytes)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------- #

if __name__ == "__main__":
    print("This is a module for AES encryption and decryption with modes CBC and CTR (also ECB, but named as aes). Please import it in your code.")
    print("if you want to know more about this module, please open and read the code.")
"""
对外接口：
- AES加密：`aes_encrypt_block(plaintext_block, key_bytes, key_size_in_bits)`
- AES解密：`aes_decrypt_block(ciphertext_block, key_bytes, key_size_in_bits)`
- CBC加密：`cbc_encrypt(plaintext, key_bytes, iv_bytes, use_padding=True)`
- CBC解密：`cbc_decrypt(ciphertext, key_bytes, iv_bytes, use_padding=True)`
- CTR加密：`ctr_encrypt(plaintext, key_bytes, init_counter_bytes)`
- CTR解密：`ctr_decrypt(ciphertext, key_bytes, init_counter_bytes)`

- S盒变换：`SBOX(a: int) -> int`
- 逆S盒变换：`inv_SBOX(a: int) -> int`

注意：
- 本文件没有测试用例，请自行编写测试用例。
- 参考测试见Task1/AES--CBC_CTR.ipynb文件
"""