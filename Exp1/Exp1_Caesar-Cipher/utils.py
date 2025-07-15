

def caesar_encrypt(text, shift):
    result = ""
    for ch in text:
        if ch.isalpha():
            if ch.isupper():
                base = ord('A')
                result += chr((ord(ch) - base + shift) % 26 + base)
            else:
                base = ord('a')
                result += chr((ord(ch) - base + shift) % 26 + base)
        else:
            result += ch
    return result

def caesar_decrypt(text, shift):
    result = ""
    for ch in text:
        if ch.isalpha():
            if ch.isupper():
                base = ord('A')
                result += chr((ord(ch) - base - shift) % 26 + base)
            else:
                base = ord('a')
                result += chr((ord(ch) - base - shift) % 26 + base)
        else:
            result += ch
    return result
'''实际上，caesar_decrypt函数可以复用caesar_encrypt函数
    def caesar_decrypt(text, shift):
        return caesar_encrypt(text, -shift)
'''