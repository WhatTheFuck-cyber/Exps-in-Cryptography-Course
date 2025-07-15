import json
import os
from TDES import *
from TDES import _b2i, _i2b
from data_process import json_data_process

def validate_blocks_OFB(blocks, key1, key2, key3, iv, is_encrypt=True, log_file=None):
    """验证OFB模式下的每个数据块（加密/解密），支持日志输出"""
    block_size = 8
    feedback = iv.to_bytes(8, 'big')
    
    for idx, block_info in enumerate(blocks, 1):
        log_line = f"\nBlock {idx}:\n"
        
        input_block_hex = block_info['InputBlock'].replace(" ", "")
        output_block_hex = block_info['OutputBlock'].replace(" ", "")
        text_in_hex = block_info['Text-In'].replace(" ", "")
        text_out_hex = block_info['Text-Out'].replace(" ", "")
        
        feedback_int = int(input_block_hex, 16)
        output_block_int = int(output_block_hex, 16)
        text_in_bytes = bytes.fromhex(text_in_hex)
        text_out_bytes = bytes.fromhex(text_out_hex)
        
        key_stream_int = tdes_encrypt_block(feedback_int, key1, key2, key3)
        key_stream_bytes = key_stream_int.to_bytes(block_size, 'big')
        
        process_block = text_in_bytes
        xor_result_bytes = bytes(a ^ b for a, b in zip(key_stream_bytes, process_block))
        
        log_line += (
            f"{'要加密的明文' if is_encrypt else '要解密的密文'}块: {text_in_hex.upper()}\n"
            f"块输入: {feedback_int:016X}\n"
            f"块输出: {key_stream_int:016X}\n"
            f"预期{'加密' if is_encrypt else '解密'}结果: {text_out_hex.upper()}\n"
            f"实际{'加密' if is_encrypt else '解密'}结果: {xor_result_bytes.hex().upper()}\n"
        )
        
        key_stream_pass = (key_stream_int == output_block_int)
        xor_pass = (xor_result_bytes == text_out_bytes)
        block_pass = key_stream_pass and xor_pass
        
        log_line += f"块验证结果: {'通过' if block_pass else '失败'}\n"
        
        print(log_line.strip())
        if log_file:
            log_file.write(log_line)
        
        feedback = key_stream_bytes

def run_test_cases_OFB(test_cases, log_file=None):
    """运行OFB模式的所有测试用例，支持日志输出"""
    for case in test_cases:
        case_log = f"\n##---------- 测试用例: {case['场景']} ----------##\n"
        print(case_log.strip())
        if log_file:
            log_file.write(case_log)
            
        key1 = int(case['Key1'].replace(" ", ""), 16)
        key2 = int(case['Key2'].replace(" ", ""), 16)
        key3 = int(case['Key3'].replace(" ", ""), 16)
        iv = int(case['IV'].replace(" ", ""), 16)

        if "Encryption" in case['场景']:
            plaintext = bytes.fromhex(case['Plaintext'].replace(" ", ""))
            expected_ciphertext = bytes.fromhex(case['Ciphertext'].replace(" ", ""))
            
            ciphertext = tdes_ofb_process(plaintext, key1, key2, key3, iv)
            
            encrypt_log = (
                f"明文: {plaintext.hex().upper()}\n"
                f"预期密文: {case['Ciphertext'].upper()}\n"
                f"实际密文: {ciphertext.hex().upper()}\n"
                f"整体验证: {'通过' if ciphertext == expected_ciphertext else '失败'}\n"
            )
            print(encrypt_log.strip())
            if log_file:
                log_file.write(encrypt_log)
            
            validate_blocks_OFB(
                case['Blocks'], key1, key2, key3, iv,
                is_encrypt=True, log_file=log_file
            )
            
        elif "Decryption" in case['场景']:
            ciphertext = bytes.fromhex(case['Ciphertext'].replace(" ", ""))
            expected_plaintext = bytes.fromhex(case['Plaintext'].replace(" ", ""))
            
            plaintext = tdes_ofb_process(ciphertext, key1, key2, key3, iv)
            
            decrypt_log = (
                f"密文: {ciphertext.hex().upper()}\n"
                f"预期明文: {case['Plaintext'].upper()}\n"
                f"实际明文: {plaintext.hex().upper()}\n"
                f"整体验证: {'通过' if plaintext == expected_plaintext else '失败'}\n"
            )
            print(decrypt_log.strip())
            if log_file:
                log_file.write(decrypt_log)

            validate_blocks_OFB(
                case['Blocks'], key1, key2, key3, iv,
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
    log_path = os.path.join(log_dir, "Test_OFB.txt")
    
    with open('../data_task2/_TDES_OFB.json', 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
        std_data = json_data_process(raw_data)
        
    with open(log_path, 'w', encoding='utf-8') as log_file:
        run_test_cases_OFB(std_data, log_file=log_file)
        
    print(f"测试结果已保存至：{log_path}")