from utils import *

if __name__ == "__main__":
    message = "Hello, SageMath!"
    shift = 3
    encrypted_text = caesar_encrypt(message, shift)
    decrypted_text = caesar_decrypt(encrypted_text, shift)

    print("原文：", message)
    print("加密成的密文：", encrypted_text)
    print("解密后的明文：", decrypted_text)

    tag = True
    if message != decrypted_text:
        tag = False
    print("校验：", tag)
'''
    # 测试加密
    assert caesar_encrypt("ABC", 1) == "BCD"
    assert caesar_encrypt("XYZ", 3) == "ABC"  # 循环移位
    assert caesar_encrypt("aBc12!", 25) == "zAb12!"  # 大小写混合+非字母

    # 测试解密（加密后解密应还原）
    text = "Hello, World!"
    shift = 5
    encrypted = caesar_encrypt(text, shift)
    decrypted = caesar_decrypt(encrypted, shift)
    assert decrypted == text
'''