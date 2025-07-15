

def vigenere_encrypt(plain_text, key):
    result = ""
    key_len = len(key)
    key_idx = 0
    for ch in plain_text:
        if ch.isalpha():
            key_ch = key[key_idx % key_len]

            if key_ch.isupper():
                shift = ord(key_ch) - ord('A')
            else:
                shift = ord(key_ch) - ord('a')
        
            if ch.isupper():
                base = ord('A')
                new_ch = chr((ord(ch) - base + shift) % 26 + base)
            else:
                base = ord('a')
                new_ch = chr((ord(ch) - base + shift) % 26 + base)

            result += new_ch
            key_idx += 1
        else:
            result += ch
    return result

def vigenere_decrypt(cipher_text, key):
    result = ""
    key_len = len(key)
    key_idx = 0
    for ch in cipher_text:
        if ch.isalpha():
            key_ch = key[key_idx % key_len]

            if key_ch.isupper():
                shift = ord(key_ch) - ord('A')
            else:
                shift = ord(key_ch) - ord('a')
        
            if ch.isupper():
                base = ord('A')
                new_ch = chr((ord(ch) - base - shift) % 26 + base)
            else:
                base = ord('a')
                new_ch = chr((ord(ch) - base - shift) % 26 + base)

            result += new_ch
            key_idx += 1
        else:
            result += ch
    return result

'''下面是经过改进的函数：（仅供参考）

def vigenere_encrypt(plain_text, key):
    """
    维吉尼亚密码加密函数（明文→密文）
    :param plain_text: 明文字符串（包含字母及非字母字符）
    :param key: 密钥（建议全大写，自动统一转为大写处理）
    :return: 加密后的密文字符串
    """
    result = ""
    key = key.upper()  # 统一密钥为大写，避免大小写混淆
    key_len = len(key)
    
    for i, ch in enumerate(plain_text):
        if ch.isalpha():
            key_ch = key[i % key_len]  # 循环使用密钥（索引i而非单独的key_idx）
            shift = ord(key_ch) - ord('A')  # 统一基于大写计算移位（0-25）
            
            if ch.isupper():
                base = ord('A')
            else:
                base = ord('a')
            
            new_ch = chr((ord(ch) - base + shift) % 26 + base)
            result += new_ch
        else:
            result += ch  # 保留非字母字符
    return result

def vigenere_decrypt(cipher_text, key):
    """
    维吉尼亚密码解密函数（密文→明文）
    :param cipher_text: 密文字符串（包含字母及非字母字符）
    :param key: 密钥（建议全大写，自动统一转为大写处理）
    :return: 解密后的明文字符串
    """
    result = ""
    key = key.upper()  # 统一密钥为大写，避免大小写混淆
    key_len = len(key)
    
    for i, ch in enumerate(cipher_text):
        if ch.isalpha():
            key_ch = key[i % key_len]
            shift = ord(key_ch) - ord('A')  # 统一基于大写计算移位（0-25）
            
            if ch.isupper():
                base = ord('A')
            else:
                base = ord('a')
            
            # 解密公式：(密文字符 - 密钥移位) mod 26，处理负数情况
            new_ch = chr((ord(ch) - base - shift + 26) % 26 + base)
            result += new_ch
        else:
            result += ch  # 保留非字母字符
    return result
'''