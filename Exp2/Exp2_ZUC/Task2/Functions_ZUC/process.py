from .process_func import *
import os
import json

def generate_key(key_length, S, X, keys, R1, R2):    # 工作（生成密钥流）阶段
    X = BitReconstruction(S, X)
    W, R1, R2 = F(X, R1, R2)
    S = LFSRWithWorkMode(S)
    for _ in range(key_length):
        X = BitReconstruction(S, X)
        W, R1, R2 = F(X, R1, R2)
        keys.append(W ^ X[3])
        S = LFSRWithWorkMode(S)
    return S, X, keys, R1, R2


def initialize_lfsr(key, iv, S, X, keys, R1, R2):    # 初始化阶段
    W = 0
    for i in range(16):
        S[i] = (key[i] << 23) | (D[i] << 8) | iv[i]
    for i in range(32):
        X = BitReconstruction(S, X)
        W, R1, R2 = F(X, R1, R2) 
        S = LFSRWithInitialisationMode(W >> 1, S)
    return S, X, keys, R1, R2

def display_key(key_length, keys):
    for i in range(key_length):
        print(f"z{i+1}: {keys[i]:08x}")

def save_key(key_length, keys, test_number, generation_number):
    current_dir = os.getcwd()
    log_dir = os.path.join(current_dir, 'Task2', 'log')
    key_file_path = os.path.join(log_dir, 'key.json')

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 读取现有的 key.json 文件内容
    existing_data = []
    if os.path.exists(key_file_path):
        try:
            with open(key_file_path, 'r') as f:
                existing_data = json.load(f)
        except json.JSONDecodeError:
            # 如果文件为空或格式错误，使用空列表
            existing_data = []

    # 生成新的数据
    new_data = {
        "label" : "test_number or generation_number is invalid if less than 1",
        "test_number": test_number,
        "generation_number": generation_number
    }
    for i in range(key_length):
        new_data[f"z{i + 1}"] = f"{keys[i]:08x}"

    # 将新的数据追加到现有内容中
    existing_data.append(new_data)

    # 将更新后的内容写回到 key.json 文件中
    with open(key_file_path, 'w') as f:
        json.dump(existing_data, f, indent=4)
    print("密钥流已保存到 key.json 文件中。")