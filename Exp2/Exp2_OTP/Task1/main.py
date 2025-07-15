import os
from binascii import hexlify

def generate_key(length):
    """
    生成length字节的随机密钥(一次性)
    """
    return os.urandom(length)

def otp_encrypt(plaintext_bytes, key_bytes):
    """
    加密
    """
    ciphertext = bytes([a^b for a, b in zip(plaintext_bytes, key_bytes)]) 
    return ciphertext

def otp_decrypt(ciphertext_bytes, key_bytes):
    """
    解密
    """
    recovered = bytes([a^b for a, b in zip(ciphertext_bytes, key_bytes)])
    return recovered 

if __name__ == '__main__':
    # 1.准备明文(这里用UTF-8编码的字符串)
    plaintext = '密码学真好玩'.encode('utf-8')
    print("原始明文： ", plaintext)

    # 2.生成一次性密钥
    key = generate_key(len(plaintext))
    print('一次性密钥： ', hexlify(key))

    # 3.加密
    ciphertext = otp_encrypt(plaintext, key)
    print('得到密文： ', hexlify(ciphertext))

    # 4.解密
    recovered = otp_decrypt(ciphertext, key)
    print('解密结果： ', recovered.decode('utf-8'))