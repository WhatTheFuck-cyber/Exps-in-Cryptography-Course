import json
from TDES import *
from TDES import _b2i, _i2b, _xor
from data_process import json_data_process
import os

def validate_blocks_CBC(blocks, input_data, output_data, key1, key2, key3, iv, is_encrypt=True, log_file=None):
    """验证CBC模式下的每个数据块（加密/解密），支持日志输出"""
    prev_cipher = iv.to_bytes(8, 'big')
    block_size = 8
    for idx, block_info in enumerate(blocks, 1):
        log_line = f"\nBlock {idx}:\n"
        start = idx * block_size - block_size
        input_block_data = input_data[start:start+block_size]
        output_block_data = output_data[start:start+block_size]
        if is_encrypt:
            expected_cipher_block_hex = block_info['Ciphertext'].upper()
            input_xor_bytes = _xor(input_block_data, prev_cipher)
            input_xor_int = _b2i(input_xor_bytes)
            cipher_block_int = tdes_encrypt_block(input_xor_int, key1, key2, key3)
            log_line += (
                f"要加密的明文块: {input_block_data.hex().upper()}\n"
                f"块输入: {input_xor_int:016X}\n"
                f"块输出: {cipher_block_int:016X}\n"
                f"预期加密结果: {expected_cipher_block_hex}\n"
                f"实际加密结果: {output_block_data.hex().upper()}\n"
            )
            block_pass = (
                input_xor_int == int(block_info['InputBlock'], 16) and
                cipher_block_int == int(block_info['OutputBlock'], 16) and
                output_block_data.hex().upper() == expected_cipher_block_hex
            )
            prev_cipher = output_block_data
        else:
            cipher_block_int = _b2i(input_block_data)
            expected_plain_block_hex = block_info['Plaintext'].upper()
            decrypted_intermediate_int = tdes_decrypt_block(cipher_block_int, key1, key2, key3)
            decrypted_intermediate_bytes = _i2b(decrypted_intermediate_int)
            plain_block_bytes = _xor(decrypted_intermediate_bytes, prev_cipher)
            log_line += (
                f"要解密的密文块: {input_block_data.hex().upper()}\n"
                f"块输入: {cipher_block_int:016X}\n"
                f"块输出: {decrypted_intermediate_int:016X}\n"
                f"预期解密结果: {expected_plain_block_hex}\n"
                f"实际解密结果: {plain_block_bytes.hex().upper()}\n"
            )
            block_pass = (
                cipher_block_int == int(block_info['InputBlock'], 16) and
                decrypted_intermediate_int == int(block_info['OutputBlock'], 16) and
                plain_block_bytes.hex().upper() == expected_plain_block_hex
            )
            prev_cipher = input_block_data
        log_line += f"块验证结果: {'通过' if block_pass else '失败'}\n"
        print(log_line.strip())
        if log_file:
            log_file.write(log_line)

def run_test_cases_CBC(test_cases, log_file=None):
    """运行CBC模式的所有测试用例，支持日志输出"""
    for case in test_cases:
        case_log = f"\n##---------- 测试用例: {case['场景']} ----------##\n"
        print(case_log.strip())
        if log_file:
            log_file.write(case_log)  
        key1 = int(case['Key1'], 16)
        key2 = int(case['Key2'], 16)
        key3 = int(case['Key3'], 16)
        iv = int(case['IV'], 16)
        if "Encryption" in case['场景']:
            plaintext = bytes.fromhex(case['Plaintext'])
            expected_ciphertext = bytes.fromhex(case['Ciphertext'])
            ciphertext = tdes_cbc_encrypt(plaintext, key1, key2, key3, iv) 
            encrypt_log = (
                f"明文: {plaintext.hex().upper()}\n"
                f"预期密文: {case['Ciphertext'].upper()}\n"
                f"实际密文: {ciphertext.hex().upper()}\n"
                f"整体验证: {'通过' if ciphertext == expected_ciphertext else '失败'}\n"
            )
            print(encrypt_log.strip())
            if log_file:
                log_file.write(encrypt_log)
            validate_blocks_CBC(
                case['Blocks'], plaintext, ciphertext, key1, key2, key3, iv,
                is_encrypt=True, log_file=log_file
            )
        elif "Decryption" in case['场景']:
            ciphertext = bytes.fromhex(case['Ciphertext'])
            expected_plaintext = bytes.fromhex(case['Plaintext'])
            plaintext = tdes_cbc_decrypt(ciphertext, key1, key2, key3, iv)
            decrypt_log = (
                f"密文: {ciphertext.hex().upper()}\n"
                f"预期明文: {case['Plaintext'].upper()}\n"
                f"实际明文: {plaintext.hex().upper()}\n"
                f"整体验证: {'通过' if plaintext == expected_plaintext else '失败'}\n"
            )
            print(decrypt_log.strip())
            if log_file:
                log_file.write(decrypt_log)
            validate_blocks_CBC(
                case['Blocks'], ciphertext, plaintext, key1, key2, key3, iv,
                is_encrypt=False, log_file=log_file
            )
        else:
            skip_log = f"跳过未知场景: {case['场景']}\n"
            print(skip_log.strip())
            if log_file:
                log_file.write(skip_log)

if __name__ == "__main__":
    log_dir = "Log"
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "Test_CBC.txt")
    with open('../data_task2/_TDES_CBC.json', 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
        std_data = json_data_process(raw_data) 
    with open(log_path, 'w', encoding='utf-8') as log_file:
        run_test_cases_CBC(std_data, log_file=log_file) 
    print(f"测试结果已保存至：{log_path}")