# Task2 项目说明

## 1. 项目简介

本项目为 ZUC 算法实现，包含以下模块：

- `Constants_ZUC`: 定义了 ZUC 算法所需的常量（两个S盒和一个常向量D）
- `Functions_ZUC`: 定义了 ZUC 算法所需的函数（`process.py`是大体过程，`process_func.py`是大体过程里的函数，`utils.py`是为了减少代码量封装的函数）
- `Main`: 主程序，包含输入输出和调用函数
- `log`: 日志文件，记录了每次运行项目生成的密钥流
- `assets`: 存放作者的运行结果截图
- `README.md`: 项目说明文件

## 2. 使用说明

```bash
cd "....../Exp2_ZUC"
python -m Task2.Main.main
```

## 3.`answer_version1.py`

- 这是只包含两个需要求密钥的样例的文件，不包括两个测试样例