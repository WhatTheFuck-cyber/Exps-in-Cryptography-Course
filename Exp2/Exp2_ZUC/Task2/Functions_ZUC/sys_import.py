'''
在运行时把目标文件夹路径添加到 Python 的模块搜索路径里

这个文件不是必须的，但是为了方便管理，我们可以把所有的包都放在一个文件夹里，然后在运行时把那个文件夹的路径添加到 Python 的模块搜索路径里，这样就可以直接 import 那个文件夹里的包了。

本项目包很少，可以直接使用相对路径来导入包，但是如果项目变大了，包的数量增多了，就需要使用这个文件了。
'''

import sys
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def add_import_path():
    try:
        # 获取当前脚本所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 获取需要导入的包的绝对路径
        import_bag_path = os.path.abspath(os.path.join(current_dir, '../Constants_sys'))
        # 检查路径是否存在
        if not os.path.exists(import_bag_path):
            logging.error(f"指定的包路径 {import_bag_path} 不存在。")
            return False
        # 检查路径是否已经在sys.path中
        if import_bag_path not in sys.path:
            # 将import_bag_path的路径添加到sys.path
            sys.path.append(import_bag_path)
            logging.info(f"成功将路径 {import_bag_path} 添加到sys.path。")
        else:
            logging.info(f"路径 {import_bag_path} 已经存在于sys.path中。")
        return True
    except Exception as e:
        logging.error(f"在添加导入路径时发生错误: {e}")
        return False
    
def add_import_path_and_save_log():
    # 配置日志记录
    # 创建一个日志记录器
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    '''
    如果希望保存到绝对路径，可以添加下面的代码：
    log_dir = 'your_log_directory' 
    
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file_path = os.path.join(log_dir, 'import_path.log')
    '''

    # 创建一个文件处理器
    file_handler = logging.FileHandler('import_path.log')   # 在当前工作终端保存.log文件
    file_handler.setLevel(logging.INFO)

    # 创建一个格式化器并添加到文件处理器
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # 将文件处理器添加到日志记录器
    logger.addHandler(file_handler)

    # 创建一个流处理器（用于在终端输出）
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    try:
        # 获取当前脚本所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 获取需要导入的包的绝对路径
        import_bag_path = os.path.abspath(os.path.join(current_dir, '../Constants_sys'))
        # 检查路径是否存在
        if not os.path.exists(import_bag_path):
            logger.error(f"指定的包路径 {import_bag_path} 不存在。")
            return False
        # 检查路径是否已经在sys.path中
        if import_bag_path not in sys.path:
            # 将import_bag_path的路径添加到sys.path
            sys.path.append(import_bag_path)
            logger.info(f"成功将路径 {import_bag_path} 添加到sys.path。")
        else:
            logger.info(f"路径 {import_bag_path} 已经存在于sys.path中。")
        return True
    except Exception as e:
        logger.error(f"在添加导入路径时发生错误: {e}")
        return False