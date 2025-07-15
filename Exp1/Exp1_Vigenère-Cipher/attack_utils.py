import json
import os
import time

# 计算文本的重合指数（IC）
def calculate_index_of_coincidence(text):
    IC = 0
    result = {}
    total = len(text)
    if total < 2:
        return 0
    for char in text:
        result[char] = result.get(char, 0) + 1

    for char in result:
        IC += (result[char] / total) * ((result[char] - 1) / (total - 1))

    return IC

# 计算给定密钥长度n时，文本的重合指数与标准重合指数（0.065）的差值。
def calculate_ic_difference(text, n):
    total = len(text)
    substrings = []
    IC_values = []

    for i in range(n):
        substring = ""
        for j in range(total):
            if j % n == i:
                substring += text[j]
        substrings.append(substring)
        # print(f"密钥长度为 {n} 时，第 {i} 个子字符串: {substring}")
        ic_value = calculate_index_of_coincidence(substring)
        IC_values.append(ic_value)
    total_ic = sum(IC_values)
    avg_Ic = total_ic / n
    difference = abs(avg_Ic - 0.065)

    # print("当密钥长度为", n, "时，子字符串的IC值为：", IC_values, "平均Ic值为：", avg_Ic)
    return difference

# 简化密钥。如果密钥是由重复的较短的模式组成的，则返回该模式。（后面没用到）
def simplify_key(key):
    length = len(key)
    for i in range(1, length // 2 + 1):
        if length % i == 0:
            pattern = key[:i]
            if pattern * (length // i) == key:
                return pattern
    return key

# 将密文按照给定的密钥长度分组，以便后续分析。
def divide_list_into_groups(key_len, num_groups, cipher_text):
    group_list = []
    for i in range(key_len):
        group = []
        for j in range(num_groups):
            index = i + j * key_len
            if index < len(cipher_text):
                group.append(cipher_text[index])
        group_list.extend(group)
    return group_list

# 计算特定字符在组中的频率。
def count_frequency(unicode_j, group):
    count = 0
    for char in group:
        if ord(char) == unicode_j:
            count += 1
    return count

# 根据密钥长度和密文，尝试找出密钥。
def know_key_len_to_get_key(key_len, cipher_text):
    num_groups = int((len(cipher_text) - len(cipher_text) % key_len) / key_len)
    group_list = divide_list_into_groups(key_len, num_groups, cipher_text)
    usual_frequencies = [0.082, 0.015, 0.028, 0.043, 0.127, 0.022, 0.020, 0.061, 0.070, 0.002, 0.008, 0.040, 0.024, 0.067, 0.075, 0.019, 0.001, 0.060, 0.063, 0.091, 0.028, 0.010, 0.023, 0.001, 0.020, 0.001]

    secret_key = []

    for i in range(key_len):
        frequencies = []

        for j in range(26):
            unicode_j = ord('A') + j
            frequencies.append(count_frequency(unicode_j, group_list[i * num_groups:(i * num_groups + num_groups)]))

        for g in range(26):
            sum_frequencies = 0
            for p in range(26):
                sum_frequencies += usual_frequencies[p] * frequencies[(p + g) % 26]
            M = abs((sum_frequencies / num_groups) - 0.065)
            if g == 0:
                t = M
                secret = 0
            elif g != 0:
                if M <= t:
                    t = M
                    secret = g
        secret_key.append(secret)

    key_str = ""

    for i in range(key_len):
        key_str += chr(ord('A') + secret_key[i])
    return key_str

# 破解Vigenère密码。
# 首先通过重合指数推测密钥长度，然后通过频率分析推测密钥，最后使用推测的密钥解密密文。
def attack_and_get_plain_text(cipher_text):
    min_difference = float('inf')
    best_key_length = 1
    
    for n in range(1, len(cipher_text)):
        difference = calculate_ic_difference(cipher_text, n)
        if difference < min_difference:
            min_difference = difference
            best_key_length = n
        if difference < 0.001:
            break

    print("推测的密钥长度为:", best_key_length)
    key = know_key_len_to_get_key(best_key_length, cipher_text)
    print("推测的密钥为:", key)

    plain_text = ""
    key_index = 0
    for char in cipher_text:
        key_char = key[key_index % len(key)]
        shift = ord(key_char) - ord('A')
        new_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
        plain_text += new_char
        key_index += 1

    parent_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(parent_dir, 'Log')

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    timestamp = int(time.time())
    filename = os.path.join(log_dir, f'{timestamp}.json')

    data = {
        'key': key,
        'key_length': len(key),
        'cipher_text': cipher_text,
        'plain_text': plain_text
    }

    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

    return plain_text
