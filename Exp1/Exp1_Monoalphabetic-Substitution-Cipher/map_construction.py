import json
import os
import string

plain_text = "the emblem of sun yatsen university is circular in shape the upper part features the full official chinese name of the university arranged from left to right along the edge and the lower part features the full official english name also arranged from left to right the center displays a crab apple shaped lattice window pattern this pattern takes the iconic building grand bell tower of the former national guangdong university as the main design element combining the artistic conception of chinese gardens with modern design techniques the emblem uses the crab apple shaped lattice window and the tower is appearance to form the characters for suny at the trees on both sides of the window decrease in size from front to back creating a sense of depth and spatial layering the curved shape in the middle cleverly forms a red kapok flower symbolizing the university is location in the lingnan region a central avenue formed by the founding year embodies the profound academic foundation and glorious history of sun yatsen university the emblem is usually rendered in standard green representing life growth and eternity symbolizing the vitality and vigor of the university"

cipher_text = "ZITTDWSTDGYLXFNQZLTFXFOCTKLOZNOLEOKEXSQKOFLIQHTZITXHHTKHQKZYTQZXKTLZITYXSSGYYOEOQSEIOFTLTFQDTGYZITXFOCTKLOZNQKKQFUTRYKGDSTYZZGKOUIZQSGFUZITTRUTQFRZITSGVTKHQKZYTQZXKTLZITYXSSGYYOEOQSTFUSOLIFQDTQSLGQKKQFUTRYKGDSTYZZGKOUIZZITETFZTKROLHSQNLQEKQWQHHSTLIQHTRSQZZOETVOFRGVHQZZTKFZIOLHQZZTKFZQATLZITOEGFOEWXOSROFUUKQFRWTSSZGVTKGYZITYGKDTKFQZOGFQSUXQFURGFUXFOCTKLOZNQLZITDQOFRTLOUFTSTDTFZEGDWOFOFUZITQKZOLZOEEGFETHZOGFGYEIOFTLTUQKRTFLVOZIDGRTKFRTLOUFZTEIFOJXTLZITTDWSTDXLTLZITEKQWQHHSTLIQHTRSQZZOETVOFRGVQFRZITZGVTKOLQHHTQKQFETZGYGKDZITEIQKQEZTKLYGKLXFNQZZITZKTTLGFWGZILORTLGYZITVOFRGVRTEKTQLTOFLOMTYKGDYKGFZZGWQEAEKTQZOFUQLTFLTGYRTHZIQFRLHQZOQSSQNTKOFUZITEXKCTRLIQHTOFZITDORRSTESTCTKSNYGKDLQKTRAQHGAYSGVTKLNDWGSOMOFUZITXFOCTKLOZNOLSGEQZOGFOFZITSOFUFQFKTUOGFQETFZKQSQCTFXTYGKDTRWNZITYGXFROFUNTQKTDWGROTLZITHKGYGXFRQEQRTDOEYGXFRQZOGFQFRUSGKOGXLIOLZGKNGYLXFNQZLTFXFOCTKLOZNZITTDWSTDOLXLXQSSNKTFRTKTROFLZQFRQKRUKTTFKTHKTLTFZOFUSOYTUKGVZIQFRTZTKFOZNLNDWGSOMOFUZITCOZQSOZNQFRCOUGKGYZITXFOCTKLOZN"

def create_mapping(plain_text, cipher_text):
    plain_no_space = plain_text.replace(" ", "")
    if len(plain_no_space) != len(cipher_text):
        raise ValueError("明文与密文长度不一致，无法建立单表置换映射")
    
    mapping = {}
    plain_chars = set()
    for p_char, c_char in zip(plain_no_space, cipher_text):
        if p_char in mapping:
            if mapping[p_char] != c_char:
                raise ValueError(f"明文字符 {p_char} 映射冲突：已有 {mapping[p_char]}，当前为 {c_char}")
        mapping[p_char] = c_char
        plain_chars.add(p_char)
    
    return mapping, plain_chars

def save_mapping_to_json(mapping, plain_letters):
    current_file_path = os.path.abspath(__file__)
    parent_dir = os.path.dirname(current_file_path)
    log_dir = os.path.join(parent_dir, "Log")
    os.makedirs(log_dir, exist_ok=True)
    
    file_path = os.path.join(log_dir, "substitution_mapping.json")
    
    all_letters = set(string.ascii_lowercase)
    plain_letters = {letter.lower() for letter in plain_letters}
    unused_letters = sorted(list(all_letters - plain_letters))
    
    data = {
        "mapping form": "plain_text ：cipher_text",
        "mapping": mapping,
        "unused_letters": unused_letters,
        "说明": "unused_letters 表示在明文中未出现的字母（不区分大小写）"
    }
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"映射表已保存到：{file_path}")
    print(f"明文中未出现的字母（共 {len(unused_letters)} 个）已在substitution_mapping.json中说明")

if __name__ == "__main__":
    mapping, plain_chars = create_mapping(plain_text, cipher_text)
    
    print("----------单表置换密码映射表----------")
    print("明文字符 → 密文字符 映射：")
    for p_char, c_char in mapping.items():
        print(f"  {p_char} → {c_char}")
    
    print("\n----------保存映射表及未出现字符----------")
    save_mapping_to_json(mapping, plain_chars)

'''
可使用在线单表置换破解软件，url为
    https://www.quipqiup.com/
注意，小体量的密文，在线破解软件能够简单破解，但大体量的密文很难破解
'''