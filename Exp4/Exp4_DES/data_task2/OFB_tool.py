import re
import json
from typing import Dict, List

def parse_ofb_encryption_section(section_text: str) -> Dict:
    """解析OFB-TDES加密场景"""
    result = {
        "场景": "",
        "Key1": "", "Key2": "", "Key3": "",
        "IV": "",
        "Plaintext": "", "Ciphertext": "",
        "Blocks": []
    }

    result["场景"] = re.search(r'^(\d+\.\d+\s+OFB-TDES\s*\(Encryption\))', section_text, re.M).group(1)
    result["Key1"] = re.search(r'Key1:\s*([\s\S]*?)Key2:', section_text, re.DOTALL).group(1).strip()
    result["Key2"] = re.search(r'Key2:\s*([\s\S]*?)Key3:', section_text, re.DOTALL).group(1).strip()
    result["Key3"] = re.search(r'Key3:\s*([\s\S]*?)IV:', section_text, re.DOTALL).group(1).strip()
    result["IV"] = re.search(r'IV:\s*([\s\S]*?)Plaintext:', section_text, re.DOTALL).group(1).strip()
    result["Plaintext"] = re.search(r'Plaintext:\s*([\s\S]*?)(Block 1:)', section_text, re.DOTALL).group(1).strip()

    block_pattern = r'Block (\d+):\s*' \
                   r'InputBlock:\s*([^\n]+)\s*' \
                   r'OutputBlock:\s*([^\n]+)\s*' \
                   r'Text-In:\s*([^\n]+)\s*' \
                   r'Text-Out:\s*([^\n]+)'
    
    for match in re.finditer(block_pattern, section_text, re.IGNORECASE):
        block_data = {
            "编号": int(match.group(1)),
            "InputBlock": match.group(2).strip(),
            "OutputBlock": match.group(3).strip(),
            "Text-In": match.group(4).strip(),
            "Text-Out": match.group(5).strip()
        }
        result["Blocks"].append(block_data)

    result["Ciphertext"] = re.search(r'Ciphertext:\s*([\s\S]*?)(?:\*{10,}|$)', section_text, re.DOTALL).group(1).strip()

    return result

def parse_ofb_decryption_section(section_text: str) -> Dict:
    """解析OFB-TDES解密场景"""
    result = {
        "场景": "",
        "Key1": "", "Key2": "", "Key3": "",
        "IV": "",
        "Ciphertext": "", "Plaintext": "",
        "Blocks": []
    }

    result["场景"] = re.search(r'^(\d+\.\d+\s+OFB-TDES\s*\(Decryption\))', section_text, re.M).group(1)
    result["Key1"] = re.search(r'Key1:\s*([\s\S]*?)Key2:', section_text, re.DOTALL).group(1).strip()
    result["Key2"] = re.search(r'Key2:\s*([\s\S]*?)Key3:', section_text, re.DOTALL).group(1).strip()
    result["Key3"] = re.search(r'Key3:\s*([\s\S]*?)IV:', section_text, re.DOTALL).group(1).strip()
    result["IV"] = re.search(r'IV:\s*([\s\S]*?)Ciphertext:', section_text, re.DOTALL).group(1).strip()
    result["Ciphertext"] = re.search(r'Ciphertext:\s*([\s\S]*?)(Block 1:)', section_text, re.DOTALL).group(1).strip()

    block_pattern = r'Block (\d+):\s*' \
                   r'InputBlock:\s*([^\n]+)\s*' \
                   r'OutputBlock:\s*([^\n]+)\s*' \
                   r'Text-In:\s*([^\n]+)\s*' \
                   r'Text-Out:\s*([^\n]+)'
    
    for match in re.finditer(block_pattern, section_text, re.IGNORECASE):
        block_data = {
            "编号": int(match.group(1)),
            "InputBlock": match.group(2).strip(),
            "OutputBlock": match.group(3).strip(),
            "Text-In": match.group(4).strip(),
            "Text-Out": match.group(5).strip()
        }
        result["Blocks"].append(block_data)

    result["Plaintext"] = re.search(r'Plaintext:\s*([\s\S]*?)(?:\*{10,}|$)', section_text, re.DOTALL).group(1).strip()

    return result

def main():
    """主函数：解析文件并生成JSON"""
    try:
        with open('TDES_OFB.txt', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("错误：文件未找到")
        return
    
    sections_with_separators = re.split(r'(\*{10,})', content)
    sections: List[str] = []
    current_section = ""
    
    for item in sections_with_separators:
        item = item.strip()
        if not item:
            continue
            
        if re.fullmatch(r'\*{10,}', item):
            if current_section:
                sections.append(f"{current_section}\n{item}")
                current_section = ""
            else:
                sections.append(item)
        else:
            if current_section:
                current_section += "\n" + item
            else:
                current_section = item
    
    if current_section:
        sections.append(current_section)

    json_data = []
    
    for section in sections:
        if 'OFB-TDES' in section:
            if 'Encryption' in section:
                parsed = parse_ofb_encryption_section(section)
            elif 'Decryption' in section:
                parsed = parse_ofb_decryption_section(section)
            else:
                continue
                
            json_data.append(parsed)
    
    with open('_TDES_OFB.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    print(f"成功生成JSON文件，包含{len(json_data)}个场景")

if __name__ == "__main__":
    main()