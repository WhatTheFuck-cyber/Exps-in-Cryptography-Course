import re

# 这只是简单的处理，有时可能无法满足需求，请按需求自行修改
def remove_whitespace(value):
    """递归去除字符串中的所有空白符号，其他类型值保持不变"""
    if isinstance(value, str):
        # 使用正则表达式移除所有空白字符（包括空格、制表符、换行符等）
        return re.sub(r'\s+', '', value)
    elif isinstance(value, list):
        # 递归处理列表中的每个元素
        return [remove_whitespace(item) for item in value]
    elif isinstance(value, dict):
        # 递归处理字典中的每个值
        return {key: remove_whitespace(val) for key, val in value.items()}
    else:
        # 非字符串、列表、字典类型保持不变
        return value


def json_data_process(json_data):
    """
    清理JSON对象中的所有空白符号
    
    参数:
        json_data: 要处理的JSON对象（字典或列表）
    
    返回:
        处理后的JSON对象
    """
    return remove_whitespace(json_data)  