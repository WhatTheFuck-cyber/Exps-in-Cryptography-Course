from ..ZUC import GenKeys
from ..Main.utils import*
from ..Main.data import *

if __name__ == '__main__':

    # 第一个样例
    count1 = [0x66, 0x03, 0x54, 0x92]
    bearer1 = 0x0f
    direction1 = 0
    length1 = 0xc1
    key1_ = [0x17, 0x3d, 0x14, 0xba, 0x50, 0x03, 0x73, 0x1d, 0x7a, 0x60, 0x04, 0x94, 0x70, 0xf0, 0x0a, 0x29]

    keys1 = GenKeys.gen_keys(count1, bearer1, direction1, length1, key1_)
    GenKeys.clear_cache_all()
    
    IBS_1 = IBS1_
    OBS_1 = encrypt(IBS_1, length1, keys1)

    show_result(IBS_1, OBS_1, keys1)
    save_encryption_result(IBS_1, OBS_1, keys1)


    # 第二个样例
    count2 = [0x00, 0x05, 0x68, 0x23]
    bearer2 = 0x18
    direction2 = 1
    length2 = 0x320
    key2_ = [0xe5, 0xbd, 0x3e, 0xa0, 0xeb, 0x55, 0xad, 0xe8, 0x66, 0xc6, 0xac, 0x58, 0xbd, 0x54, 0x30, 0x2a]

    keys2 = GenKeys.gen_keys(count2, bearer2, direction2, length2, key2_)
    GenKeys.clear_cache_all()

    IBS_2 = IBS2_
    OBS_2 = encrypt(IBS_2, length2, keys2)

    show_result(IBS_2, OBS_2, keys2)
    save_encryption_result(IBS_2, OBS_2, keys2)


    # 第三个样例
    count3 = [0x27, 0x38, 0xcd, 0xaa]
    bearer3 = 0x1a
    direction3 = 0
    length3 = 0xfb3
    key3_ = [0xe1, 0x3f, 0xed, 0x21, 0xb4, 0x6e, 0x4e, 0x7e, 0xc3, 0x12, 0x53, 0xb2, 0xbb, 0x17, 0xb3, 0xe0]

    keys3 = GenKeys.gen_keys(count3, bearer3, direction3, length3, key3_)
    GenKeys.clear_cache_all()
    
    IBS_3 = IBS3_
    OBS_3 = encrypt(IBS_3, length3, keys3)

    show_result(IBS_3, OBS_3, keys3)
    save_encryption_result(IBS_3, OBS_3, keys3)

# cd "../Exp2_ZUC"

# python -m Task3.Main.main_str