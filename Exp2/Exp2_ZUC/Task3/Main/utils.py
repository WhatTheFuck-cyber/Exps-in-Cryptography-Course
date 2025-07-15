import math
import json
import os


'''-----------------------------------------------------------------------------------------------'''
def group_bit(hex_str, bit_length = 32):

    if (type(hex_str) != str) and (type(hex_str) != list):
        raise TypeError("hex_str must be a string or list")
    
    if type(hex_str) == list:
        return hex_str

    char_length = bit_length // 4
    result = []
    for i in range(0, len(hex_str), char_length):
        group = hex_str[i:i + char_length]
        result.append(int(group, 16))
    return result

def standardize(unstd_IBS, unstd_bit, std_bit = 32):
    # 将unstd_IBS中的元素转换为二进制字符串，并拼接成一个大的二进制字符串
    bin_str = ''.join(format(x, f'0{unstd_bit}b') for x in unstd_IBS)
    # 计算需要补零的数量
    padding = (std_bit - (len(bin_str) % std_bit)) % std_bit
    # 补零
    bin_str += '0' * padding
    # 按照std_bit进行分组
    std_IBS = [int(bin_str[i:i+std_bit], 2) for i in range(0, len(bin_str), std_bit)]
    return std_IBS

def encrypt(IBS, length, keys):

    L = math.ceil(length / 32)
    
    if (L < len(IBS)) and (type(IBS) == list) :
        IBS = standardize(IBS, 8)

    plaintext = group_bit(IBS)

    ciphertext = []

    for i in range(L):
        # 计算当前块的bit位置范围
        block_start_bit = i * 32
        block_end_bit = (i + 1) * 32
    
        # 判断当前块是否包含填充位
        if block_start_bit >= length:
            # 整个块都是填充
            ciphertext.append(0)
        elif block_end_bit > length:
            # 块的一部分是填充
            padding_in_block = block_end_bit - length
            data_bits = 32 - padding_in_block
        
            # 保留数据部分，填充部分设为0
            mask = (0xFFFFFFFF >> padding_in_block) << padding_in_block
            data_part = plaintext[i] & mask
        
            # 只加密数据部分
            encrypted_data = data_part ^ (keys[i] & mask)
            ciphertext.append(encrypted_data)
        else:
            # 块中没有填充，正常加密
            ciphertext.append(plaintext[i] ^ keys[i])

    OBS = ''.join([f"{c:08x}" for c in ciphertext])

    return OBS
'''以上是加密接口'''



'''-----------------------------------------------------------------------------------------------'''
def split_string(s):
        return ' '.join(s[i:i + 8] for i in range(0, len(s), 8))

def show_result(IBS, OBS, keys):
    
    print(f"IBS: {split_string(str(IBS))}")
    print(f"OBS: {split_string(str(OBS))}")
    print(f"keys: {split_string(str(keys))}")
'''以上是将加密结果打印出来的接口'''



'''-----------------------------------------------------------------------------------------------'''
def to_string(keys):
    return ''.join(str(key) for key in keys)

def save_encryption_result(IBS, OBS, keys):
    flag = False
    keys = to_string(keys)
    if type(IBS) != str:
        IBS = to_string(IBS)
        flag = True

    current_dir = os.getcwd()
    log_path = os.path.join(current_dir, 'Task3', 'log')
    result_file_path = os.path.join(log_path, 'encryption_result.json')

    if not os.path.exists(log_path):
        os.makedirs(log_path)

    # 读取现有的 JSON 文件内容
    existing_data = []
    if os.path.exists(result_file_path):
        try:
            with open(result_file_path, 'r') as f:
                existing_data = json.load(f)
        except json.JSONDecodeError:
            # 如果文件为空或格式错误，使用空列表
            existing_data = []

    # 生成新的数据
    if flag:
        new_data = {
            "main file": "main_list",
            "IBS": IBS,
            "OBS": OBS,
            "keys": keys
        }
    else:
        new_data = {
            "main file": "main_str",
            "IBS": IBS,
            "OBS": OBS,
            "keys": keys
        } 

    # 将新的数据追加到现有内容中
    existing_data.append(new_data)

    # 将更新后的内容写回到 JSON 文件中
    with open(result_file_path, 'w') as f:
        json.dump(existing_data, f, indent=4)
    print(f"加密结果已保存到 {result_file_path} 文件中。")
'''以上是将加密结果保存起来的接口'''