from AES_and_workmode import *
from HMAC_SHA2_256 import *
import os
# 使用cryptography、hashlib、hmac库进行标准测试
import hashlib
import hmac
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class EtM:
    def __init__(self, work_mode : str, IV : str, encryption_key : str, mac_key : str):
        self.work_mode = work_mode
        self.IV = IV
        self.encryption_key = encryption_key
        self.mac_key = mac_key

    def catch_lenght(self) -> int:
        if "128" in self.work_mode:
            return 128
        elif "192" in self.work_mode:
            return 192
        elif "256" in self.work_mode:
            return 256
        else:
            raise Exception("Illegal work mode length in self.work_mode")
        
    def get_encrpytion_bytes(self) -> bytes:
        if "CTR" in self.work_mode.upper():
            return hex_to_bytes(self.encryption_key)
        else:
            return hex_to_bytes(self.encryption_key)[:self.catch_lenght()//4]

    def etm_encrypt_and_mac(self, plaintext : str):
        plaintext_bytes = hex_to_bytes(plaintext)
        iv_bytes = hex_to_bytes(self.IV)
        encryption_key_bytes = self.get_encrpytion_bytes()

        if len(plaintext_bytes) % 16 == 0:
            print("注意: 想要加密的明文长度是块大小的整数倍，不进行填充")

        if self.work_mode == "" :
            print("Please input self.work_mode, must include work mode and block lenght.\nFor example: CBC-128")
            return 
        elif "CBC" in self.work_mode.upper():
            encryption_text = cbc_encrypt(plaintext_bytes, encryption_key_bytes, iv_bytes, use_padding=False).hex()
        elif "CTR" in self.work_mode.upper():
            encryption_text = ctr_encrypt(plaintext_bytes, encryption_key_bytes, iv_bytes).hex()
        else:
            raise Exception("Unsupportted work mode")
        
        mac_OB = SHA2_256_HMAC()
        mac_str = mac_OB.hmac_sha256(self.mac_key, encryption_text)

        return encryption_text, mac_str
    
    def etm_decrypt_and_mac(self, ciphertext : str, mac_str : str):
        mac_OB = SHA2_256_HMAC()
        verify = mac_OB.verify_hmac(self.mac_key, ciphertext, mac_str)
        if verify:
            print("MAC验证成功")
        else:
            print("MAC验证失败，退出解密程序！")
            return

        ciphertext_bytes = hex_to_bytes(ciphertext)
        iv_bytes = hex_to_bytes(self.IV)
        decryption_key_bytes = self.get_encrpytion_bytes()

        if self.work_mode == "" :
            print("Please input self.work_mode, must include work mode and block lenght.\nFor example: CBC-128")
            return None
        elif "CBC" in self.work_mode.upper():
            decryption_text = cbc_decrypt(ciphertext_bytes, decryption_key_bytes, iv_bytes, use_padding=False).hex()
        elif "CTR" in self.work_mode.upper():
            decryption_text = ctr_decrypt(ciphertext_bytes, decryption_key_bytes, iv_bytes).hex()
        else:
            raise Exception("Unsupportted work mode")
        
        return decryption_text
    
def radom_test(count : int = 10):
    for mode in range(3):
        if mode == 0:
            lenght = 16
        elif mode == 1:
            lenght = 24
        elif mode == 2:
            lenght = 32
        print(f"##########################密钥长度为{lenght}字节的测试开始##########################")
        for i in range(count):
            print("第{}次测试".format(i+1))
            plaintext = os.urandom(16).hex()
            print("欲加密的明文: {}".format(plaintext))
            IV = os.urandom(16).hex()
            encryption_key = os.urandom(lenght).hex()
            mac_key = os.urandom(16).hex()
            # --------------------------------------------------------------------------------------------------------- #
            
            if mode == 0:
                if i % 2 == 0:
                    work_mode = "CBC-128"
                else:
                    work_mode = "CTR-128"
            elif mode == 1:
                if i % 2 == 0:
                    work_mode = "CBC-192"
                else:
                    work_mode = "CTR-192"
            elif mode == 2:
                if i % 2 == 0:
                    work_mode = "CBC-256"
                else:
                    work_mode = "CTR-256"

            print("# --------自定义 EtM 测试-------- #")
            etm = EtM(work_mode, IV, encryption_key, mac_key)
            ciphertext, mac_str = etm.etm_encrypt_and_mac(plaintext)
            print(f"使用{work_mode}加密后的密文: {ciphertext}")
            print("密文的MAC值: {}".format(mac_str))
            decryption_text = etm.etm_decrypt_and_mac(ciphertext, mac_str)
            print("解密后的明文: {}".format(decryption_text))
            if plaintext == decryption_text:
                print("解密成功！")
                print("# --------自定义 EtM 测试通过！-------- #")
            else:
                print("解密失败！")
                print("# --------自定义 EtM 测试失败！-------- #")
            print()
            # --------------------------------------------------------------------------------------------------------- #
            print("# --------标准库 EtM 测试-------- #") 
            if i % 2 == 0:
                work_mode_ = "CBC"
                encryption_key_bytes = bytes.fromhex(encryption_key)
                iv_bytes = bytes.fromhex(IV)
                plaintext_bytes = bytes.fromhex(plaintext)
                cipher = Cipher(algorithms.AES(encryption_key_bytes), modes.CBC(iv_bytes), backend=default_backend())
                encryptor = cipher.encryptor()
                ciphertext_ = encryptor.update(plaintext_bytes) + encryptor.finalize()
                mac_val = hmac.new(bytes.fromhex(mac_key), ciphertext_, hashlib.sha256).hexdigest().upper()
                decipher = Cipher(algorithms.AES(encryption_key_bytes), modes.CBC(iv_bytes), backend=default_backend())
                decryptor = decipher.decryptor()
                decryption_text_ = decryptor.update(ciphertext_) + decryptor.finalize()
                decryption_text_hex = decryption_text_.hex()
                print(f"使用{work_mode_}加密后的密文: {ciphertext_.hex()}")
                print("密文的MAC值: {}".format(mac_val))
                print("解密后的明文: {}".format(decryption_text_hex))
                if plaintext == decryption_text_hex:
                    print("解密成功！")
                    print("# --------标准库 EtM 测试通过！-------- #")
                else:
                    print("解密失败！")
                    print("# --------标准库 EtM 测试失败！-------- #")
            else:
                work_mode_ = "CTR"
                encryption_key_bytes = bytes.fromhex(encryption_key)
                iv_bytes = bytes.fromhex(IV)
                plaintext_bytes = bytes.fromhex(plaintext)
                cipher = Cipher(algorithms.AES(encryption_key_bytes), modes.CTR(iv_bytes), backend=default_backend())
                encryptor = cipher.encryptor()
                ciphertext_ = encryptor.update(plaintext_bytes) + encryptor.finalize()
                mac_val = hmac.new(bytes.fromhex(mac_key), ciphertext_, hashlib.sha256).hexdigest().upper()
                decipher = Cipher(algorithms.AES(encryption_key_bytes), modes.CTR(iv_bytes), backend=default_backend())
                decryptor = decipher.decryptor()
                decryption_text_ = decryptor.update(ciphertext_) + decryptor.finalize()
                decryption_text_hex = decryption_text_.hex()
                print(f"使用{work_mode_}加密后的密文: {ciphertext_.hex()}")
                print("密文的MAC值: {}".format(mac_val))
                print("解密后的明文: {}".format(decryption_text_hex))
                if plaintext == decryption_text_hex:
                    print("解密成功！")
                    print("# --------标准库 EtM 测试通过！-------- #")
                else:
                    print("解密失败！")
                    print("# --------标准库 EtM 测试失败！-------- #")
            print() 
            # --------------------------------------------------------------------------------------------------------- #
            print("自定义与标准库比较结果：")
            if decryption_text == decryption_text_hex and mac_val == mac_str:
                print("自定义的方法与标准库结果一样")
            else:
                print("自定义的方法与标准库结果不一样")
                raise Exception("Method Error")
            print("##########################第{}次测试结束##########################".format(i+1))
        print(f"##########################密钥长度为{lenght}字节的测试结束##########################")
        print("\n\n\n")

if __name__ == "__main__":
    radom_test(100)