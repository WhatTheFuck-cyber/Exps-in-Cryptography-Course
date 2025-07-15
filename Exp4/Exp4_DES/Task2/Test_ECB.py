import json
from TDES import *
from data_process import json_data_process
import os  

def validate_blocks_ECB(blocks, input_data, output_data, key1, key2, key3, is_encrypt=True, log_file=None):
    """验证ECB模式下的每个数据块（加密/解密），支持日志输出"""
    block_size = 8  
    for idx, block_info in enumerate(blocks, 1):
        log_line = f"\nBlock {idx}:\n" 
        start = idx * block_size - block_size
        input_block_data = input_data[start:start+block_size]
        if is_encrypt:
            plain_block_int = int.from_bytes(input_block_data, 'big')
            expected_cipher_block_int = int(block_info['Blockout'], 16)
            cipher_block_int = tdes_encrypt_block(plain_block_int, key1, key2, key3)
            log_line += (
                f"要加密的明文块: {input_block_data.hex().upper()}\n"
                f"经过加密的结果: {cipher_block_int:016X}\n"
                f"预期加密结果: {expected_cipher_block_int:016X}\n"
            )
            block_pass = (cipher_block_int == expected_cipher_block_int)
        else:
            cipher_block_int = int.from_bytes(input_block_data, 'big')
            expected_plain_block_int = int(block_info['Blockout'], 16)
            plain_block_int = tdes_decrypt_block(cipher_block_int, key1, key2, key3)
            log_line += (
                f"要解密的密文块: {input_block_data.hex().upper()}\n"
                f"经过解密的结果: {plain_block_int:016X}\n"
                f"预期解密结果: {expected_plain_block_int:016X}\n"
            )
            block_pass = (plain_block_int == expected_plain_block_int)
        log_line += f"块验证结果: {'通过' if block_pass else '失败'}\n"
        print(log_line.strip())  
        if log_file:
            log_file.write(log_line)

def run_test_cases_ECB(test_cases, log_file=None):
    """运行ECB模式的所有测试用例，支持日志输出"""
    for case in test_cases:
        case_log = f"\n##---------- 测试用例: {case['场景']} ----------##\n"
        print(case_log.strip()) 
        if log_file:
            log_file.write(case_log)
        key1 = int(case['Key1'], 16)
        key2 = int(case['Key2'], 16)
        key3 = int(case['Key3'], 16)
        if "Encryption" in case['场景']:
            plaintext = bytes.fromhex(case['Plaintext'])
            expected_ciphertext = bytes.fromhex(case['Ciphertext'])
            ciphertext = tdes_ecb_encrypt(plaintext, key1, key2, key3)
            
            encrypt_log = (
                f"明文: {plaintext.hex().upper()}\n"
                f"预期密文: {case['Ciphertext'].upper()}\n"
                f"实际密文: {ciphertext.hex().upper()}\n"
                f"整体验证: {'通过' if ciphertext == expected_ciphertext else '失败'}\n"
            )
            print(encrypt_log.strip())  
            if log_file:
                log_file.write(encrypt_log)
            
            validate_blocks_ECB(
                case['Blocks'], plaintext, ciphertext, key1, key2, key3,
                is_encrypt=True, log_file=log_file
            )
        elif "Decryption" in case['场景']:
            ciphertext = bytes.fromhex(case['Ciphertext'])
            expected_plaintext = bytes.fromhex(case['Plaintext'])
            plaintext = tdes_ecb_decrypt(ciphertext, key1, key2, key3)
            
            decrypt_log = (
                f"密文: {ciphertext.hex().upper()}\n"
                f"预期明文: {case['Plaintext'].upper()}\n"
                f"实际明文: {plaintext.hex().upper()}\n"
                f"整体验证: {'通过' if plaintext == expected_plaintext else '失败'}\n"
            )
            print(decrypt_log.strip())  
            if log_file:
                log_file.write(decrypt_log)

            validate_blocks_ECB(
                case['Blocks'], ciphertext, plaintext, key1, key2, key3,
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
    log_path = os.path.join(log_dir, "Test_ECB.txt")
    with open('../data_task2/_TDES_ECB.json', 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
        std_data = json_data_process(raw_data)
    with open(log_path, 'w', encoding='utf-8') as log_file:
        run_test_cases_ECB(std_data, log_file=log_file)
    print(f"测试结果已保存至：{log_path}")