## ���������������ɣ����ն����� `bash.sh` �ļ�

- ����������<span style='color:red'>����ˮƽ���ޣ�������ʽд�Ŀ��ܿ��ǵĲ����ܵ�������ֻ��Ա�Ŀ¼�µ����txt�ļ�����������Ч���ݣ����������һ�������䡣��л���</span>

- ���䣺���߱�д����ʱ�˽⵽һЩϸ�ڣ�

    - ���з�֮ǰ�Լ�֮������ֿհ׷�����Ҫ����
    - ���з����ܲ�ֹһ������Ҫ����
    - ����ĳЩ���ݵ��Ų�˳�򲢲���һֱ����һ�£���Ҫʹ������Ԥ�鼼����

```python
# ������OFB_tool�У�segment��ƥ���������д��
segment_pattern = r'Segment (\d+):\s*(?=(?:(?!Segment \d+).)*?Plaintext:\s*([^\n]+))' \
                     r'(?=(?:(?!Segment \d+).)*?InputBlock:\s*([^\n]+))' \
                     r'(?=(?:(?!Segment \d+).)*?OutputBlock:\s*([^\n]+))' \
                     r'(?=(?:(?!Segment \d+).)*?Ciphertext:\s*([^\n]+))'
# ԭ����д����
segment_pattern = r'Segment (\d+):\s*' \
                     r'InputBlock:\s*([^\n]+)\s*' \
                     r'OutputBlock:\s*([^\n]+)\s*' \
                     r'Ciphertext:\s*([^\n]+)\s*' \
                     r'Plaintext:\s*([^\n]+)'
```


**����Ԥ��ʹ�� (?=pattern) �﷨������ pattern ������Ҫ�������ݡ�**���磺

```python
foo(?=bar)
```

���ģʽ��ƥ�� "foo"����ǰ��������������� "bar"��ע�⣬ƥ��ɹ���������ʽ��ָ�벻���ƶ��� "bar" ֮����Ȼͣ���� "foo" ������λ�á�

    - ��ʹʹ��������Ԥ�鼼����ҲҪ�����ֶα�ǣ�����д�����ݣ�

```python
# һ�ֿ��ܵķ�����
def parse_decryption_section(section_text: str) -> Dict:
    """����CFB-TDES���ܳ���"""
    result = {
        "����": "",
        "Key1": "", "Key2": "", "Key3": "", "IV": "",
        "Ciphertext": "", "Plaintext": "",
        "SegmentLength": "",
        "Segments": []
    }
    
    result["����"] = re.search(r'^(\d+\.\d+\s+CFB-TDES\s*\(Decryption\))', section_text, re.M).group(1)
    result["Key1"] = re.search(r'Key1:\s*([\s\S]*?)Key2:', section_text, re.DOTALL).group(1).strip()
    result["Key2"] = re.search(r'Key2:\s*([\s\S]*?)Key3:', section_text, re.DOTALL).group(1).strip()
    result["Key3"] = re.search(r'Key3:\s*([\s\S]*?)IV:', section_text, re.DOTALL).group(1).strip()
    result["IV"] = re.search(r'IV:\s*([\s\S]*?)Ciphertext:', section_text, re.DOTALL).group(1).strip()
    result["Ciphertext"] = re.search(r'Ciphertext:\s*([\s\S]*?)Segment Length =', section_text, re.DOTALL).group(1).strip()
    result["SegmentLength"] = re.search(r'Segment Length = (\d+)', section_text).group(1)
    
    # ƥ�䵥��Segment�Ŀ�ʼ���
    segment_start_pattern = r'Segment (\d+):'
    
    # ƥ��Segment�е������ֶ�
    field_pattern = r'(Plaintext|InputBlock|OutputBlock|Ciphertext):\s*([^\n]+)'
    
    # ��������Segment�Ŀ�ʼλ��
    segment_starts = list(re.finditer(segment_start_pattern, section_text))
    
    # ����ÿ��Segment
    for i in range(len(segment_starts)):
        current_start = segment_starts[i]
        next_start = segment_starts[i+1] if i+1 < len(segment_starts) else None
        
        # ȷ����ǰSegment���ı���Χ
        if next_start:
            segment_text = section_text[current_start.end():next_start.start()]
        else:
            # ���һ��Segment��ֱ���ĵ�������ָ���
            end_pos = section_text.find('**********', current_start.end())
            if end_pos == -1:
                end_pos = len(section_text)
            segment_text = section_text[current_start.end():end_pos]
        
        # ��ʼ��Segment����
        segment_data = {
            "���": int(current_start.group(1)),
            "InputBlock": "",
            "OutputBlock": "",
            "Plaintext": "",
            "Ciphertext": ""
        }
        
        # ��ȡSegment�е������ֶ�
        for field_match in re.finditer(field_pattern, segment_text, re.IGNORECASE):
            field_name = field_match.group(1).strip()
            field_value = field_match.group(2).strip()
            
            # ���ֶ�ֵ������ȷ������
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