from ..ZUC.GEN_func import *

def __init__(count, bearer, direction, length, key_):
    params.__init__(count, bearer, direction, length, key_)

def show_params():
    params.show_params()

def gen_keys(count, bearer, direction, length, key_):
    __init__(count, bearer, direction, length, key_)
    params.gen_iv()
    initialize_lfsr()
    generate_key()
    # display_key()
    return params.keys

def clear_cache_all():
    params.clear_cache()