from collections import Counter
import json
import os
import datetime

def count_and_sort_letters(text):
    text
    filtered_text = "".join(ch for ch in text.lower() if ch.isalpha())
    letter_counts = Counter(filtered_text)
    sorted_letters = sorted(letter_counts.items(), key = lambda item: item[1], reverse=True)
    return sorted_letters

def decrypt_by_frequency(cipher_text, sorted_letters, std_sorted_letters):
    cipher_chars = [char for char, _ in sorted_letters]
    std_chars = list(std_sorted_letters)
    
    mapping = {cipher: std for cipher, std in zip(cipher_chars, std_chars)}
    
    decrypted = []
    for ch in cipher_text:
        if ch.isalpha():
            lower_ch = ch.lower()
            std_char = mapping.get(lower_ch, lower_ch)
            decrypted.append(std_char)
        else:
            decrypted.append(ch)
    
    return ''.join(decrypted)
    
def save_as_json(crypted_text, try_to_decrypt_text, std_sorted_letters="etaoinshrdlcumwfgypbvkjxqz"):
    current_file_path = os.path.abspath(__file__)
    parent_dir = os.path.dirname(current_file_path)
    log_dir = os.path.join(parent_dir, "Log")
    os.makedirs(log_dir, exist_ok=True)
    file_path = os.path.join(log_dir, "try_decrypted_result.json")
    
    new_entry = {
        "encrypted_text": crypted_text,
        "decrypted_text": try_to_decrypt_text,
        "std_sorted_letters": std_sorted_letters,
        "cipher_text_length": len(crypted_text),
        "decryption_method": "Frequency Analysis for Monoalphabetic Substitution Cipher",
        "timestamp": datetime.datetime.now().isoformat()
    }
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
            if not isinstance(existing_data, list):
                existing_data = []
    except FileNotFoundError:
        existing_data = []

    existing_data.append(new_entry)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)
    
    print(f"解密结果已追加到：{file_path}，当前记录数：{len(existing_data)}")