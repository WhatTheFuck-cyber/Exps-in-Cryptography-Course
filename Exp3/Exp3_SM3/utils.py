

def rotl(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

def modified_message(m, len_bit_stream):
    """
    将输入转换为指定长度的二进制比特流字符串
    
    参数:
    m: 可以是整数、列表、二进制/十六进制/十进制字符串
    len_bit_stream: 期望的比特流长度
    
    返回:
    二进制字符串，长度为len_bit_stream
    """
    if isinstance(m, str):
        # 处理二进制字符串
        if all(c in {'0', '1'} for c in m):
            bit_str = m
        # 处理带0b前缀的二进制字符串
        elif m[:2] == '0b':
            bit_str = m[2:]
            if not all(c in {'0', '1'} for c in bit_str):
                raise ValueError("二进制字符串包含非法字符")
        # 处理十六进制字符串
        elif m[:2] == '0x':
            try:
                num = int(m, 16)
                bit_str = bin(num)[2:]
            except ValueError:
                raise ValueError("无效的十六进制字符串")
        elif any(c in {'a', 'b', 'c', 'd', 'e', 'f', 'A', 'B', 'C', 'D', 'E', 'F'} for c in m):
            try:
                num = int('0x' + m, 16)
                bit_str = bin(num)[2:]
            except ValueError:
                raise ValueError("无效的十六进制字符串")
        # 处理十进制字符串
        elif m[:2] == '0d':
            try:
                num = int(m[2:], 10)
                bit_str = bin(num)[2:]
            except ValueError:
                raise ValueError("无效的十进制字符串")
        else:
            try:
                num = int(m, 10)
                bit_str = bin(num)[2:]
            except ValueError:
                raise ValueError("只支持十六进制、十进制、二进制的字符串输入")
    # 处理整数
    elif isinstance(m, int):
        bit_str = bin(m)[2:]
    # 处理二进制列表
    elif isinstance(m, list):
        if not all(isinstance(x, int) and x in {0, 1} for x in m):
            raise ValueError("列表元素必须是0或1")
        bit_str = ''.join(map(str, m))
    else:
        raise ValueError("只支持整数，列表，二进制、十六进制、十进制字符串输入。其他请自行转换成二进制字符串或整数输入")
    
    # 确保比特流长度正确
    if len(bit_str) > len_bit_stream:
        bit_str = bit_str[-len_bit_stream:]  # 截断高位
    else:
        bit_str = bit_str.zfill(len_bit_stream)  # 左侧补零
    
    return bit_str