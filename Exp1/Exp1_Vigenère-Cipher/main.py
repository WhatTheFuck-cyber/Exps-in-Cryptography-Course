from utils import *

key = "sysu"

if __name__ == "__main__":
    plain_text = "Hello, world!"
    cipher_text = vigenere_encrypt(plain_text, key)

    decrypt_text = vigenere_decrypt(cipher_text, key)

    print("原文：", plain_text)
    print("加密后的密文：", cipher_text)
    print("解密后的明文：", decrypt_text)

    tag = True
    if plain_text != decrypt_text:
        tag = False

    print("校验：", tag)