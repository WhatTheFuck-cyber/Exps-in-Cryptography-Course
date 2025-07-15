# Task2 项目说明

## 1. 项目简介

本项目为 ZUC 算法应用实现，包含以下模块：

- `ZUC`: 定义了 ZUC 算法的密钥生成
- `Main`: 复现标准文档里的加密方案
- `log`: 日志文件，记录了每次运行项目生成的密钥流以及明、密文
- `assets`: 存放作者的运行结果截图与标准文档中`IBS`与`OBS`数据的`.txt`文件
- `README.md`: 项目说明文件

## 2. 使用说明

```bash
cd "....../Exp2_ZUC"
python -m Task3.Main.main_type      
```

`type metioned above must be list or str`

## 3.`answer_version1.py`

- 这是一个只能测试一个样例的文件，要求将`IBS`转成无空格字符串作为输入