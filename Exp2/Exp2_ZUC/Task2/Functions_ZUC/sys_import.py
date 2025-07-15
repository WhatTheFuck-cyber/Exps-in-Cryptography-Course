'''
������ʱ��Ŀ���ļ���·����ӵ� Python ��ģ������·����

����ļ����Ǳ���ģ�����Ϊ�˷���������ǿ��԰����еİ�������һ���ļ����Ȼ��������ʱ���Ǹ��ļ��е�·����ӵ� Python ��ģ������·��������Ϳ���ֱ�� import �Ǹ��ļ�����İ��ˡ�

����Ŀ�����٣�����ֱ��ʹ�����·��������������������Ŀ����ˣ��������������ˣ�����Ҫʹ������ļ��ˡ�
'''

import sys
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def add_import_path():
    try:
        # ��ȡ��ǰ�ű�����Ŀ¼
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # ��ȡ��Ҫ����İ��ľ���·��
        import_bag_path = os.path.abspath(os.path.join(current_dir, '../Constants_sys'))
        # ���·���Ƿ����
        if not os.path.exists(import_bag_path):
            logging.error(f"ָ���İ�·�� {import_bag_path} �����ڡ�")
            return False
        # ���·���Ƿ��Ѿ���sys.path��
        if import_bag_path not in sys.path:
            # ��import_bag_path��·����ӵ�sys.path
            sys.path.append(import_bag_path)
            logging.info(f"�ɹ���·�� {import_bag_path} ��ӵ�sys.path��")
        else:
            logging.info(f"·�� {import_bag_path} �Ѿ�������sys.path�С�")
        return True
    except Exception as e:
        logging.error(f"����ӵ���·��ʱ��������: {e}")
        return False
    
def add_import_path_and_save_log():
    # ������־��¼
    # ����һ����־��¼��
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    '''
    ���ϣ�����浽����·���������������Ĵ��룺
    log_dir = 'your_log_directory' 
    
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file_path = os.path.join(log_dir, 'import_path.log')
    '''

    # ����һ���ļ�������
    file_handler = logging.FileHandler('import_path.log')   # �ڵ�ǰ�����ն˱���.log�ļ�
    file_handler.setLevel(logging.INFO)

    # ����һ����ʽ��������ӵ��ļ�������
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # ���ļ���������ӵ���־��¼��
    logger.addHandler(file_handler)

    # ����һ�������������������ն������
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    try:
        # ��ȡ��ǰ�ű�����Ŀ¼
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # ��ȡ��Ҫ����İ��ľ���·��
        import_bag_path = os.path.abspath(os.path.join(current_dir, '../Constants_sys'))
        # ���·���Ƿ����
        if not os.path.exists(import_bag_path):
            logger.error(f"ָ���İ�·�� {import_bag_path} �����ڡ�")
            return False
        # ���·���Ƿ��Ѿ���sys.path��
        if import_bag_path not in sys.path:
            # ��import_bag_path��·����ӵ�sys.path
            sys.path.append(import_bag_path)
            logger.info(f"�ɹ���·�� {import_bag_path} ��ӵ�sys.path��")
        else:
            logger.info(f"·�� {import_bag_path} �Ѿ�������sys.path�С�")
        return True
    except Exception as e:
        logger.error(f"����ӵ���·��ʱ��������: {e}")
        return False