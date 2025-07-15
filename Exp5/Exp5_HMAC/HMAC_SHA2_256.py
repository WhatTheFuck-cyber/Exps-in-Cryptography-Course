import random
import os 
import hashlib  # 仅做校验 SHA2-256 的正确性
import hmac  # 仅做校验 HMAC-SHA2-256 的正确性

class SHA2_256_HMAC:
    
    @staticmethod
    def _rightrotate(x, n):
        """向右循环移位"""
        return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF

    def sha256(self, message: str) -> str:
        """实现 SHA2-256 哈希算法"""
        message = bytes.fromhex(message)

        h0 = 0x6a09e667
        h1 = 0xbb67ae85
        h2 = 0x3c6ef372
        h3 = 0xa54ff53a
        h4 = 0x510e527f
        h5 = 0x9b05688c
        h6 = 0x1f83d9ab
        h7 = 0x5be0cd19

        K = [
            0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
            0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
            0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
            0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
            0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
            0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
            0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
            0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
        ]

        original_bit_len = len(message) * 8
        message += b'\x80'
        while (len(message) * 8) % 512 != 448:
            message += b'\x00'
        message += original_bit_len.to_bytes(8, 'big')
        for i in range(0, len(message), 64):
            chunk = message[i:i+64]
            w = [int.from_bytes(chunk[j:j+4], 'big') for j in range(0, 64, 4)]
            for j in range(16, 64):
                s0 = (self._rightrotate(w[j-15], 7)) ^ (self._rightrotate(w[j-15], 18)) ^ (w[j-15] >> 3)
                s1 = (self._rightrotate(w[j-2], 17)) ^ (self._rightrotate(w[j-2], 19)) ^ (w[j-2] >> 10)
                w.append((w[j-16] + s0 + w[j-7] + s1) & 0xFFFFFFFF)
            a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7
            for j in range(64):
                S1 = (self._rightrotate(e, 6)) ^ (self._rightrotate(e, 11)) ^ (self._rightrotate(e, 25))
                ch = (e & f) ^ ((~e) & g)
                temp1 = (h + S1 + ch + K[j] + w[j]) & 0xFFFFFFFF
                S0 = (self._rightrotate(a, 2)) ^ (self._rightrotate(a, 13)) ^ (self._rightrotate(a, 22))
                maj = (a & b) ^ (a & c) ^ (b & c)
                temp2 = (S0 + maj) & 0xFFFFFFFF
                h = g
                g = f
                f = e
                e = (d + temp1) & 0xFFFFFFFF
                d = c
                c = b
                b = a
                a = (temp1 + temp2) & 0xFFFFFFFF

            h0 = (h0 + a) & 0xFFFFFFFF
            h1 = (h1 + b) & 0xFFFFFFFF
            h2 = (h2 + c) & 0xFFFFFFFF
            h3 = (h3 + d) & 0xFFFFFFFF
            h4 = (h4 + e) & 0xFFFFFFFF
            h5 = (h5 + f) & 0xFFFFFFFF
            h6 = (h6 + g) & 0xFFFFFFFF
            h7 = (h7 + h) & 0xFFFFFFFF

        hash_value_int = (h0 << 224) | (h1 << 192) | (h2 << 160) | (h3 << 128) | (h4 << 96) | (h5 << 64) | (h6 << 32) | h7
        return '{:064x}'.format(hash_value_int)
    
    def test_sha256(self, bit_length_start : int = 100, bit_length_end : int = 200, is_show = False):
        """测试 SHA2-256 哈希算法的正确性"""
        print("--------测试 SHA2-256 哈希算法的正确性--------")
        length = random.randint(bit_length_start // 2, bit_length_end // 2) * 2
        random_bytes = os.urandom(length // 2)
        test_str = random_bytes.hex()

        self_hash = self.sha256(test_str)
        message_bytes = bytes.fromhex(test_str)
        hashlib_hash = hashlib.sha256(message_bytes).hexdigest()

        if self_hash == hashlib_hash:
            print("SHA2-256 随机校验通过")
        else:
            print("SHA2-256 随机校验失败")
        
        if is_show:
            print("测试字符串: ", test_str)
            print("计算得到的哈希值: ", self_hash)
            print("标准哈希值: ", hashlib_hash)
        print("--------测试结束--------\n")

    @staticmethod
    def _expand_key(key_hex: str) -> str:
        """扩展密钥到64字节的整数倍"""
        key_bytes = bytes.fromhex(key_hex)
        if len(key_bytes) > 64:
            key_bytes = bytes.fromhex(hashlib.sha256(key_bytes).hexdigest())
        target_length = ((len(key_bytes) - 1) // 64 + 1) * 64
        expanded_bytes = key_bytes.ljust(target_length, b'\x00')
        return expanded_bytes.hex()

    @staticmethod
    def _xor_with_ipad(expanded_key_hex: str) -> str:
        """与ipad (0x36) 进行异或操作"""
        expanded_key_bytes = bytes.fromhex(expanded_key_hex)
        ipad_bytes = bytes([0x36] * len(expanded_key_bytes))
        xor_result = bytes(a ^ b for a, b in zip(expanded_key_bytes, ipad_bytes))
        return xor_result.hex()

    @staticmethod
    def _xor_with_opad(expanded_key_hex: str) -> str:
        """与opad (0x5C) 进行异或操作"""
        expanded_key_bytes = bytes.fromhex(expanded_key_hex)
        opad_bytes = bytes([0x5C] * len(expanded_key_bytes))
        xor_result = bytes(a ^ b for a, b in zip(expanded_key_bytes, opad_bytes))
        return xor_result.hex()
    
    def hmac_sha256(self, key_hex: str, message_hex: str) -> str:
        """使用SHA2-256计算HMAC"""
        expanded_key = self._expand_key(key_hex)
        # print(f"Expanded Key: {expanded_key}")
        k0_xor_ipad = self._xor_with_ipad(expanded_key)
        # print(f"K0^ipad: {k0_xor_ipad}")
        inner_data = k0_xor_ipad + message_hex
        inner_hash = self.sha256(inner_data)
        # print(f"Inner Hash: {inner_hash}")
        k0_xor_opad = self._xor_with_opad(expanded_key)
        # print(f"K0^opad: {k0_xor_opad}")
        outer_data = k0_xor_opad + inner_hash
        mac = self.sha256(outer_data)
        return mac.upper()
    
    def verify_hmac(self, key_hex: str, message_hex: str, expected_mac: str) -> bool:
        """验证HMAC值是否正确，使用时间恒定比较防止时序攻击"""
        computed_mac = self.hmac_sha256(key_hex, message_hex).upper()
        if len(computed_mac) != len(expected_mac):
            return False
        result = 0
        for x, y in zip(computed_mac, expected_mac):
            result |= ord(x) ^ ord(y)
        return result == 0
    
    @staticmethod
    def hmac_sha256_std(key_hex: str, message_hex: str) -> str:
        """使用Python内置的hmac库计算HMAC-SHA256"""
        key_bytes = bytes.fromhex(key_hex)
        message_bytes = bytes.fromhex(message_hex)
        hmac_result = hmac.new(key_bytes, message_bytes, hashlib.sha256).hexdigest().upper()
        return hmac_result

    def test_hmac_sha256(self, key="", message="", is_show = False):
        """测试 HMAC-SHA2-256 的正确性"""
        print("--------测试 HMAC-SHA2-256 的正确性，与测试期望进行比较--------")
        if key == "" or message == "":
            print("key和message至少有一个是空，抛弃原来的输入，采用随机生成进行校验")
            key = os.urandom(16).hex()
            message = os.urandom(16).hex()
            hmac_sha256_result = self.hmac_sha256(key, message).upper()
            expected_mac = self.hmac_sha256_std(key, message).upper()
        else:
            hmac_sha256_result = self.hmac_sha256(key, message).upper()
            expected_mac = self.hmac_sha256_std(key, message).upper()

        if hmac_sha256_result == expected_mac:
            print("HMAC-SHA256 计算正确")
            if self.verify_hmac(key, message, expected_mac):
                print("MAC值校验通过")
            else:
                print("MAC值校验失败")
                return 
        else:
            print("HMAC-SHA256 计算错误")

        if is_show:
            print("Key: ", key)
            print("Message: ", message)
            print("HMAC-SHA256 Result: ", hmac_sha256_result)
            print("Expected MAC: ", expected_mac)
        print("--------测试结束--------\n")

if __name__ == "__main__":
    #"""
    # 以下是校验代码（使用Python标准库进行校验）：
    # --------测试 SHA2-256 哈希算法的正确性，与标准库计算的结果进行比较。-------- #
    sha2_256 = SHA2_256_HMAC()
    for i in range(10):
        sha2_256.test_sha256(is_show=True)
    # --------测试 HMAC-SHA2-256 的正确性，与测试期望进行比较-------- #
    sha2_256 = SHA2_256_HMAC()
    for i in range(10):
        sha2_256.test_hmac_sha256(is_show=True)
    print("this is a module for HMAC with SHA2-256. Please import it in your code.")
    print("if you want to know more about this module, please open and read the code.")
    # """
# python HMAC_SHA2_256.py