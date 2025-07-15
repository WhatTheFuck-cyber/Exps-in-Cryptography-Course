import json
import os
from TDES import *
from TDES import _b2i, _i2b
from data_process import json_data_process

def validate_blocks_CFB(blocks, key1, key2, key3, iv, segment_bits=1, is_encrypt=True, log_file=None):
    """验证CFB模式下的每个数据块（加密/解密），支持日志输出"""
    if segment_bits == 1:
        reg = iv
        bit_results = []
        
        if is_encrypt:
            for block in blocks:
                ks = (tdes_encrypt_block(reg, key1, key2, key3) >> 63) & 1
                mbit = int(block['Plaintext'].replace(' ', ''), 16)
                cbit = mbit ^ ks
                bit_results.append({
                    'input_block': reg,
                    'output_block': tdes_encrypt_block(reg, key1, key2, key3),
                    'plain_bit': mbit,
                    'cipher_bit': cbit
                })
                reg = ((reg << 1) & ((1 << 64) - 1)) | cbit
        else:
            for block in blocks:
                ks = (tdes_encrypt_block(reg, key1, key2, key3) >> 63) & 1
                cbit = int(block['Ciphertext'].replace(' ', ''), 16)
                mbit = cbit ^ ks
                bit_results.append({
                    'input_block': reg,
                    'output_block': tdes_encrypt_block(reg, key1, key2, key3),
                    'plain_bit': mbit,
                    'cipher_bit': cbit
                })
                reg = ((reg << 1) & ((1 << 64) - 1)) | cbit
        
        for i, (result, block_info) in enumerate(zip(bit_results, blocks)):
            log_line = f"\nSegment {i+1}:\n"
            log_line += (
                f"实际的InputBlock:  {result['input_block']:016X}\n"
                f"实际的OutputBlock: {result['output_block']:016X}\n"
                f"实际的Plaintext:   {result['plain_bit']:0X}\n"
                f"实际的Ciphertext:  {result['cipher_bit']:0X}\n"
            )
            
            input_pass = (result['input_block'] == int(block_info['InputBlock'].replace(' ', ''), 16))
            output_pass = (result['output_block'] == int(block_info['OutputBlock'].replace(' ', ''), 16))
            plain_bit_pass = (result['plain_bit'] == int(block_info['Plaintext'].replace(' ', ''), 16))
            cipher_bit_pass = (result['cipher_bit'] == int(block_info['Ciphertext'].replace(' ', ''), 16))
            block_pass = input_pass and output_pass and plain_bit_pass and cipher_bit_pass
            
            log_line += f"块验证结果: {'通过' if block_pass else '失败'}\n"
            
            print(log_line.strip())
            if log_file:
                log_file.write(log_line)
    else:
        reg_bytes = iv.to_bytes(8, 'big')
        segment_bytes = segment_bits // 8
        
        for i, block_info in enumerate(blocks):
            log_line = f"\nSegment {i+1}:\n"
            
            ks_full = tdes_encrypt_block(int.from_bytes(reg_bytes, 'big'), key1, key2, key3)
            ks_bytes = ks_full.to_bytes(8, 'big')
            ks = ks_bytes[:segment_bytes]
            
            if is_encrypt:
                p_byte = bytes.fromhex(block_info['Plaintext'].replace(' ', ''))
                c_byte = bytes(a ^ b for a, b in zip(p_byte, ks))
            else:
                c_byte = bytes.fromhex(block_info['Ciphertext'].replace(' ', ''))
                p_byte = bytes(a ^ b for a, b in zip(c_byte, ks))
            
            log_line += (
                f"实际的InputBlock:  {int.from_bytes(reg_bytes, 'big'):016X}\n"
                f"实际的OutputBlock: {ks_full:016X}\n"
                f"实际的Plaintext:   {p_byte.hex().upper()}\n"
                f"实际的Ciphertext:  {c_byte.hex().upper()}\n"
            )
            
            input_pass = (f"{int.from_bytes(reg_bytes, 'big'):016X}" == block_info['InputBlock'].replace(' ', ''))
            output_pass = (f"{ks_full:016X}" == block_info['OutputBlock'].replace(' ', ''))
            plain_byte_pass = (p_byte.hex().upper() == block_info['Plaintext'].replace(' ', ''))
            cipher_byte_pass = (c_byte.hex().upper() == block_info['Ciphertext'].replace(' ', ''))
            block_pass = input_pass and output_pass and plain_byte_pass and cipher_byte_pass
            
            log_line += f"块验证结果: {'通过' if block_pass else '失败'}\n"
            
            print(log_line.strip())
            if log_file:
                log_file.write(log_line)
            
            reg_bytes = reg_bytes[segment_bytes:] + c_byte

def run_test_cases_CFB(test_cases, log_file=None):
    """运行CFB模式的所有测试用例，支持日志输出"""
    for case in test_cases:
        case_log = f"\n##---------- 测试用例: {case['场景']} ----------##\n"
        print(case_log.strip())
        if log_file:
            log_file.write(case_log)
            
        key1 = int(case['Key1'].replace(" ", ""), 16)
        key2 = int(case['Key2'].replace(" ", ""), 16)
        key3 = int(case['Key3'].replace(" ", ""), 16)
        iv = int(case['IV'].replace(" ", ""), 16)
        segmentlength = int(case['SegmentLength'].replace(" ", ""))
        segments = case['Segments']

        if "Encryption" in case['场景']:
            plaintext = bytes.fromhex(case['Plaintext'].replace(" ", ""))
            expected_ciphertext = bytes.fromhex(case['Ciphertext'].replace(" ", ""))
            
            ciphertext = tdes_cfb_encrypt(plaintext, key1, key2, key3, iv, segmentlength)
            
            encrypt_log = (
                f"场景: {case['场景']}\n"
                f"明文: {plaintext.hex().upper()}\n"
                f"加密得到的密文: {ciphertext.hex().upper()}\n"
                f"预期密文: {expected_ciphertext.hex().upper()}\n"
                f"整体验证: {'通过' if ciphertext == expected_ciphertext else '失败'}\n"
            )
            print(encrypt_log.strip())
            if log_file:
                log_file.write(encrypt_log)
            
            validate_blocks_CFB(
                segments, key1, key2, key3, iv, 
                segment_bits=segmentlength, is_encrypt=True, log_file=log_file
            )
        else:
            ciphertext = bytes.fromhex(case['Ciphertext'].replace(" ", ""))
            expected_plaintext = bytes.fromhex(case['Plaintext'].replace(" ", ""))
            
            plaintext = tdes_cfb_decrypt(ciphertext, key1, key2, key3, iv, segmentlength)
            
            decrypt_log = (
                f"场景: {case['场景']}\n"
                f"密文: {ciphertext.hex().upper()}\n"
                f"解密得到的明文: {plaintext.hex().upper()}\n"
                f"预期明文: {expected_plaintext.hex().upper()}\n"
                f"整体验证: {'通过' if plaintext == expected_plaintext else '失败'}\n"
            )
            print(decrypt_log.strip())
            if log_file:
                log_file.write(decrypt_log)
            
            validate_blocks_CFB(
                segments, key1, key2, key3, iv, 
                segment_bits=segmentlength, is_encrypt=False, log_file=log_file
            )

if __name__ == "__main__":
    log_dir = "Log"
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "Test_CFB.txt")
    
    with open('../data_task2/_TDES_CFB.json', 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
        std_data = json_data_process(raw_data)
        
    with open(log_path, 'w', encoding='utf-8') as log_file:
        run_test_cases_CFB(std_data, log_file=log_file)
        
    print(f"测试结果已保存至：{log_path}")