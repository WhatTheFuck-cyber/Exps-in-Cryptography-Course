# --------------------------------------- DES 工具函数 --------------------------------------- #
# —— 置换与常量表 —— #
IP  = [58,50,42,34,26,18,10,2, 60,52,44,36,28,20,12,4,
       62,54,46,38,30,22,14,6, 64,56,48,40,32,24,16,8,
       57,49,41,33,25,17,9,1,  59,51,43,35,27,19,11,3,
       61,53,45,37,29,21,13,5, 63,55,47,39,31,23,15,7]

FP  = [40,8,48,16,56,24,64,32, 39,7,47,15,55,23,63,31,
       38,6,46,14,54,22,62,30, 37,5,45,13,53,21,61,29,
       36,4,44,12,52,20,60,28, 35,3,43,11,51,19,59,27,
       34,2,42,10,50,18,58,26, 33,1,41,9,49,17,57,25]

E   = [32,1,2,3,4,5, 4,5,6,7,8,9, 8,9,10,11,12,13,
       12,13,14,15,16,17, 16,17,18,19,20,21,
       20,21,22,23,24,25, 24,25,26,27,28,29,
       28,29,30,31,32,1]

P   = [16,7,20,21,29,12,28,17,
       1,15,23,26,5,18,31,10,
       2,8,24,14,32,27,3,9,
       19,13,30,6,22,11,4,25]

PC1 = [57,49,41,33,25,17,9,
       1,58,50,42,34,26,18,
       10,2,59,51,43,35,27,
       19,11,3,60,52,44,36,
       63,55,47,39,31,23,15,
       7,62,54,46,38,30,22,
       14,6,61,53,45,37,29,
       21,13,5,28,20,12,4]

PC2 = [14,17,11,24,1,5,3,28,
       15,6,21,10,23,19,12,4,
       26,8,16,7,27,20,13,2,
       41,52,31,37,47,55,30,40,
       51,45,33,48,44,49,39,56,
       34,53,46,42,50,36,29,32]

SBOX = [
[[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
 [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
 [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
 [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]],

[[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
 [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
 [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
 [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]],

[[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
 [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
 [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
 [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]],

[[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
 [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
 [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
 [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]],

[[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
 [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
 [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
 [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]],

[[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
 [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
 [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
 [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]],

[[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
 [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
 [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
 [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]],

[[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
 [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
 [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
 [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]]
]

SHIFT = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1] # 每轮左移位数

BLOCK = 8 # 块大小（位）

# —— 工具函数 —— #
def _permute(val, table, bits_in):
    """按给定置换表重新排列位。"""
    out = 0
    for pos in table:
        out = (out << 1) | ((val >> (bits_in - pos)) & 1)
    return out

def _rotl(val, k, width=28):
    """循环左移 k 位（width-bit 宽度）。"""
    return ((val << k) & ((1 << width) - 1)) | (val >> (width - k))

# —— 密钥调度 —— #
def _subkeys(key64):
    """生成 16 个 48-bit 子密钥。"""
    key56 = _permute(key64, PC1, 64)
    C, D = key56 >> 28, key56 & ((1 << 28) - 1)
    K = []
    for s in SHIFT:
        C, D = _rotl(C, s), _rotl(D, s)
        K.append(_permute((C << 28) | D, PC2, 56))
    return K

# —— Feistel F 函数 —— #
def _F(R, Ki):
    Rex = _permute(R, E, 32)
    Rxor = Rex ^ Ki
    S_output = 0
    for i in range(8):
        group = (Rxor >> (6 * (7 - i))) & 0x3F
        row = ((group >> 5) << 1) | (group & 1)  
        col = (group >> 1) & 0x0F
        sbox = SBOX[i]
        value = sbox[row][col]
        S_output = (S_output << 4) | value
    return _permute(S_output, P, 32)

# ------------------------------------- DES 单块加/解密 ------------------------------------- #
def _rounds(block, subkeys):
    L, R = block >> 32, block & 0xFFFFFFFF
    for K in subkeys:              
        L, R = R, L ^ _F(R, K)
    return (R << 32) | L             

def des_encrypt_block(plain64, key64):
    """ECB 单块加密"""
    klist = _subkeys(key64)
    pre   = _permute(plain64, IP, 64)
    post  = _rounds(pre, klist)
    return _permute(post, FP, 64)

def des_decrypt_block(cipher64, key64):
    """ECB 单块解密"""
    klist = _subkeys(key64)
    pre = _permute(cipher64, IP, 64)
    # 逆序使用子密钥
    post = _rounds(pre, reversed(klist))
    return _permute(post, FP, 64)

# ------------------------------------------ 3DES ------------------------------------------ #

def _b2i(b: bytes) -> int:
    return int.from_bytes(b, 'big')

def _i2b(i: int) -> bytes:
    return int(i).to_bytes(BLOCK, 'big')

def _xor(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

def tdes_encrypt_block(plain64: int, k1: int, k2: int, k3: int) -> int:
    """EDE 加密"""
    x1 = des_encrypt_block(plain64, k1)
    x2 = des_decrypt_block(x1,     k2)
    x3 = des_encrypt_block(x2,     k3)
    return x3

def tdes_decrypt_block(cipher64: int, k1: int, k2: int, k3: int) -> int:
    """EDE 解密"""
    x1 = des_decrypt_block(cipher64, k3)
    x2 = des_encrypt_block(x1,       k2)
    x3 = des_decrypt_block(x2,       k1)
    return x3

def _process_blocks(data: bytes, f) -> bytes:
    assert len(data) % BLOCK == 0
    out = bytearray()
    for i in range(0, len(data), BLOCK):
        out.extend(_i2b(f(_b2i(data[i:i+BLOCK]))))
    return bytes(out)



# --------------------------------- 3DES 加密/解密 工作模式 --------------------------------- #
# ECB模式
def tdes_ecb_encrypt(data: bytes, k1: int, k2: int, k3: int) -> bytes:
    return _process_blocks(data, lambda x: tdes_encrypt_block(x, k1, k2, k3))

def tdes_ecb_decrypt(data: bytes, k1: int, k2: int, k3: int) -> bytes:
    return _process_blocks(data, lambda x: tdes_decrypt_block(x, k1, k2, k3))

# CBC模式
def tdes_cbc_encrypt(data: bytes, k1: int, k2: int, k3: int, iv: int) -> bytes:
    prev = _i2b(iv)
    out  = bytearray()
    for i in range(0, len(data), BLOCK):
        blk    = _xor(data[i:i+BLOCK], prev)
        cipher = _i2b(tdes_encrypt_block(_b2i(blk), k1, k2, k3))
        out.extend(cipher)
        prev   = cipher
    return bytes(out)

def tdes_cbc_decrypt(ciphertext: bytes, k1: int, k2: int, k3: int, iv: int) -> bytes:
    prev_cipher = _i2b(iv)  
    out = bytearray()
    for i in range(0, len(ciphertext), BLOCK):
        cipher_block = ciphertext[i:i+BLOCK]
        decrypted_block_int = tdes_decrypt_block(_b2i(cipher_block), k1, k2, k3)
        decrypted_block = _i2b(decrypted_block_int)
        plain_block = _xor(decrypted_block, prev_cipher)
        out.extend(plain_block)
        prev_cipher = cipher_block
    return bytes(out)

# CFB模式
def tdes_cfb_encrypt(data: bytes, k1: int, k2: int, k3: int, iv: int, segment_bits: int = 1) -> bytes:
    assert 1 <= segment_bits <= 64 and 64 % segment_bits == 0
    # ---------- CFB-1：逐 bit ----------
    if segment_bits == 1:
        reg = iv & ((1 << 64) - 1)      
        out = bytearray()
        for byte in data:                   
            new_byte = 0
            for b in range(7, -1, -1):      
                ks = (tdes_encrypt_block(reg, k1, k2, k3) >> 63) & 1
                mbit = (byte >> b) & 1
                cbit = mbit ^ ks
                new_byte |= (cbit << b)
                reg = ((reg << 1) & ((1 << 64) - 1)) | cbit
            out.append(new_byte)
        return bytes(out)
    # -------------- CFB-s --------------
    assert segment_bits % 8 == 0
    s_bytes = segment_bits // 8             
    reg = int(iv).to_bytes(8, 'big')        
    out = bytearray()
    for off in range(0, len(data), s_bytes):
        ks_full = int(tdes_encrypt_block(int.from_bytes(reg, 'big'),
                                         k1, k2, k3)).to_bytes(8, 'big')
        ks = ks_full[:s_bytes]
        p_seg = data[off:off + s_bytes]
        c_seg = bytes(a ^ b for a, b in zip(p_seg, ks))
        out.extend(c_seg)
        reg = reg[s_bytes:] + c_seg
    return bytes(out)

def tdes_cfb_decrypt(data: bytes, k1: int, k2: int, k3: int, iv: int, segment_bits: int = 64) -> bytes:
    assert 1 <= segment_bits <= 64 and 64 % segment_bits == 0
    if segment_bits == 1:
        # ---------- CFB-1：逐 bit ----------
        reg = iv & ((1 << 64) - 1)
        out = bytearray()
        for byte in data:
            new_byte = 0
            for b in range(7, -1, -1):
                ks = (tdes_encrypt_block(reg, k1, k2, k3) >> 63) & 1
                cbit = (byte >> b) & 1
                mbit = cbit ^ ks
                new_byte |= (mbit << b)
                reg = ((reg << 1) & ((1 << 64) - 1)) | cbit # 关键差异：加密时用cbit更新寄存器，解密时也用cbit（因为寄存器需要密文）
            out.append(new_byte)
        return bytes(out)
    # -------------- CFB-s --------------
    assert segment_bits % 8 == 0
    s_bytes = segment_bits // 8
    reg = int(iv).to_bytes(8, 'big')
    out = bytearray()
    for i in range(0, len(data), s_bytes):
        ks_full = int(tdes_encrypt_block(int.from_bytes(reg, 'big'), k1, k2, k3)).to_bytes(8, 'big')
        ks = ks_full[:s_bytes]
        c_seg = data[i:i + s_bytes]
        p_seg = bytes(a ^ b for a, b in zip(c_seg, ks))
        out.extend(p_seg)
        reg = reg[s_bytes:] + c_seg
    return bytes(out)
    
# OFB模式
def tdes_ofb_process(data: bytes, k1: int, k2: int, k3: int, iv: int) -> bytes:
    feedback = _i2b(iv)
    out      = bytearray()
    for i in range(0, len(data), BLOCK):
        feedback = _i2b(tdes_encrypt_block(_b2i(feedback), k1, k2, k3))
        out.extend(_xor(data[i:i+BLOCK], feedback))
    return bytes(out)

# CTR模式
def tdes_ctr_process(data: bytes, k1: int, k2: int, k3: int,
                     counter0: int) -> bytes:
    out      = bytearray()
    counter  = counter0 & 0xFFFFFFFFFFFFFFFF         
    for i in range(0, len(data), BLOCK):
        stream = _i2b(tdes_encrypt_block(counter, k1, k2, k3))
        out.extend(_xor(data[i:i+BLOCK], stream[:len(data[i:i+BLOCK])]))
        counter = (counter + 1) & 0xFFFFFFFFFFFFFFFF
    return bytes(out)