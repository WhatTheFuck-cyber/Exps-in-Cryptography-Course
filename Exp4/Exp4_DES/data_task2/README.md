## 快速启动数据生成：在终端运行 `bash.sh` 文件

- 作者声明：<span style='color:red'>作者水平有限，正则表达式写的可能考虑的不够周到，仅仅只针对本目录下的五个txt文件可以生成有效数据，其他情况不一定能适配。感谢理解</span>

- 补充：作者编写代码时了解到一些细节：

    - 换行符之前以及之后可能又空白符，需要处理
    - 换行符可能不止一个，需要处理
    - 由于某些数据的排布顺序并不是一直保持一致，需要使用正向预查技术：

```python
# 比如在OFB_tool中，segment的匹配可以这样写：
segment_pattern = r'Segment (\d+):\s*(?=(?:(?!Segment \d+).)*?Plaintext:\s*([^\n]+))' \
                     r'(?=(?:(?!Segment \d+).)*?InputBlock:\s*([^\n]+))' \
                     r'(?=(?:(?!Segment \d+).)*?OutputBlock:\s*([^\n]+))' \
                     r'(?=(?:(?!Segment \d+).)*?Ciphertext:\s*([^\n]+))'
# 原本的写法：
segment_pattern = r'Segment (\d+):\s*' \
                     r'InputBlock:\s*([^\n]+)\s*' \
                     r'OutputBlock:\s*([^\n]+)\s*' \
                     r'Ciphertext:\s*([^\n]+)\s*' \
                     r'Plaintext:\s*([^\n]+)'
```


**正向预查使用 (?=pattern) 语法，其中 pattern 是你想要检查的内容。**例如：

```python
foo(?=bar)
```

这个模式会匹配 "foo"，但前提是它后面紧跟着 "bar"。注意，匹配成功后，正则表达式的指针不会移动到 "bar" 之后，仍然停留在 "foo" 结束的位置。

    - 即使使用了正向预查技术，也要做好字段标记，方便写入数据：

```python
# 一种可能的方法：
def parse_decryption_section(section_text: str) -> Dict:
    """解析CFB-TDES解密场景"""
    result = {
        "场景": "",
        "Key1": "", "Key2": "", "Key3": "", "IV": "",
        "Ciphertext": "", "Plaintext": "",
        "SegmentLength": "",
        "Segments": []
    }
    
    result["场景"] = re.search(r'^(\d+\.\d+\s+CFB-TDES\s*\(Decryption\))', section_text, re.M).group(1)
    result["Key1"] = re.search(r'Key1:\s*([\s\S]*?)Key2:', section_text, re.DOTALL).group(1).strip()
    result["Key2"] = re.search(r'Key2:\s*([\s\S]*?)Key3:', section_text, re.DOTALL).group(1).strip()
    result["Key3"] = re.search(r'Key3:\s*([\s\S]*?)IV:', section_text, re.DOTALL).group(1).strip()
    result["IV"] = re.search(r'IV:\s*([\s\S]*?)Ciphertext:', section_text, re.DOTALL).group(1).strip()
    result["Ciphertext"] = re.search(r'Ciphertext:\s*([\s\S]*?)Segment Length =', section_text, re.DOTALL).group(1).strip()
    result["SegmentLength"] = re.search(r'Segment Length = (\d+)', section_text).group(1)
    
    # 匹配单个Segment的开始标记
    segment_start_pattern = r'Segment (\d+):'
    
    # 匹配Segment中的任意字段
    field_pattern = r'(Plaintext|InputBlock|OutputBlock|Ciphertext):\s*([^\n]+)'
    
    # 查找所有Segment的开始位置
    segment_starts = list(re.finditer(segment_start_pattern, section_text))
    
    # 遍历每个Segment
    for i in range(len(segment_starts)):
        current_start = segment_starts[i]
        next_start = segment_starts[i+1] if i+1 < len(segment_starts) else None
        
        # 确定当前Segment的文本范围
        if next_start:
            segment_text = section_text[current_start.end():next_start.start()]
        else:
            # 最后一个Segment，直到文档结束或分隔符
            end_pos = section_text.find('**********', current_start.end())
            if end_pos == -1:
                end_pos = len(section_text)
            segment_text = section_text[current_start.end():end_pos]
        
        # 初始化Segment数据
        segment_data = {
            "编号": int(current_start.group(1)),
            "InputBlock": "",
            "OutputBlock": "",
            "Plaintext": "",
            "Ciphertext": ""
        }
        
        # 提取Segment中的所有字段
        for field_match in re.finditer(field_pattern, segment_text, re.IGNORECASE):
            field_name = field_match.group(1).strip()
            field_value = field_match.group(2).strip()
            
            # 将字段值存入正确的属性
            if field_name == "Plaintext":
                segment_data["Plaintext"] = field_value
            elif field_name == "InputBlock":
                segment_data["InputBlock"] = field_value
            elif field_name == "OutputBlock":
                segment_data["OutputBlock"] = field_value
            elif field_name == "Ciphertext":
                segment_data["Ciphertext"] = field_value
        
        result["Segments"].append(segment_data)

    result["Plaintext"] = re.search(r'Plaintext:\s*([\s\S]*?)(?:\*{10,}|$)', section_text, re.DOTALL).group(1).strip()

    return result
```