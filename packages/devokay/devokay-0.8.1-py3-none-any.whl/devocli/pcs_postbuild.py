# -*- coding: UTF-8 -*-
# python3

# PC SDK build tool

from devolib import DynamicObject
from devolib.util_log import LOG_D, LOG_E, LOG_W, LOG_I
from devolib.util_os import get_env_var, current_dir
from devolib.util_str import ends_with, str_to_bytes, bytes_to_str
from devolib.util_argparse import typeparse_list
from devolib.util_httpc import POST_JSON, GET_JSON
from devolib.util_crypt import sim_cipher_decrypt, aes_encrypt_without_b64, aes_decrypt_without_b64
from devolib.util_fs import path_join_one, write_bytes_to_file, path_exists, read_bytes_of_file
from devolib.util_json import json_to_str

# MARK: Consts

SVC_HOST = "PCS_POSTBUILD_HOST"
SVC_HOST_2 = "PCS_POSTBUILD_HOST_2"
SVC_TOKEN = "PCS_POSTBUILD_TOKEN"

CIPHER_FOR_CIPHER_BYTES = [0xc7, 0xc4, 0xc5, 0xda, 0xcb, 0xcf, 0xcc, 0xcd, 0xc2, 0xc3, 0xc0, 0xc4, 0xc5, 0xda, 0xdb, 0xd8]
CIPHER_FOR_CIPHER_SALT = 0xAA
CIPHER_FOR_CIPHER_IV = [0x9b, 0x98, 0xcb, 0xcb, 0xec, 0xee, 0xf9, 0xeb, 0xc1, 0xcb, 0xc7, 0xcc, 0xce, 0xd9, 0xcb, 0x9b]

# MARK: Utils


# MARK: Conf retrieve

def get_conf_data(host, info):
    if len(host) > 0 and info != None:
        param_arr = info.split("-") # official-pc-10001
        res_json = GET_JSON(
            host=f'https://{host}', 
            path='/pconf/pack', 
            query=f"app_id={param_arr[2]}&store_type={param_arr[0]}&platform={param_arr[1]}",
            headers={
                'Authorization': get_env_var(SVC_TOKEN)
            })
        
        if res_json is None:
            raise Exception(f'get conf data failed.')

        code = res_json['code']
        if code != 200:
            raise Exception(f'get conf data failed, code: {code}')

        return res_json
    else:
        LOG_E('host empty')

        return None

# MARK: Build Stages

def stage_get_conf(params):
    conf_json = get_conf_data(get_env_var(SVC_HOST), params)
    if conf_json is None:
        conf_json = get_conf_data(get_env_var(SVC_HOST_2), params)

    LOG_W(f"[STAGE] conf json: {conf_json}")

    return conf_json

def stage_parse_conf(conf_json):
    pass

def stage_handle_files(origin_dir, target_dir):
    pass

def stage_save_conf(conf_json, target_dir): # 加密配置数据，保存在指定目录
    global CIPHER_FOR_CIPHER_BYTES, CIPHER_FOR_CIPHER_SALT

    # conf_data_encrypt
    # sim_cipher_encrypt
    LOG_D(f"target_dir: {target_dir}")

    conf_file_path = path_join_one(target_dir, "pcsdk.json")

    LOG_D(f"conf_file_path: {conf_file_path}")

    cipher_decrypted = sim_cipher_decrypt(cipher_bytes=CIPHER_FOR_CIPHER_BYTES, salt=CIPHER_FOR_CIPHER_SALT)
    iv_decrypted = sim_cipher_decrypt(cipher_bytes=CIPHER_FOR_CIPHER_IV, salt=CIPHER_FOR_CIPHER_SALT)

    conf_json_str = json_to_str(conf_json)

    LOG_D(f"conf_json_str: {conf_json_str}")

    conf_str_encrypted = aes_encrypt_without_b64(conf_json_str, cipher_decrypted, iv_decrypted)

    write_bytes_to_file(conf_file_path, conf_str_encrypted)

    if path_exists(conf_file_path):
        LOG_I(f"conf path exists: {conf_file_path}")
    else:
        LOG_E(f"conf path not exists")

# MARK: Command Handle

def cmd_handle_build_store(args):
    LOG_D(f'params: {args.params}')
    LOG_D(f'origin: {args.origin}')
    LOG_D(f'target: {args.target}')

    conf_data = stage_get_conf(args.params)

    stage_parse_conf(conf_data)

    if args.origin != None and len(args.origin) != 0:
        stage_handle_files(args.origin, args.target)

    if args.target == None or len(args.target) == 0:
        args.target = current_dir()

    stage_save_conf(conf_data, args.target)

def cmd_handle_tools_decrypt(args):
    if args.path is not None:
        file_path = args.path
        decrypted_file_path = f"{file_path}.decrypted"

        LOG_D(f"file_path: {file_path}")
        LOG_D(f"decrypted_file_path: {decrypted_file_path}")

        cipher_decrypted = sim_cipher_decrypt(cipher_bytes=CIPHER_FOR_CIPHER_BYTES, salt=CIPHER_FOR_CIPHER_SALT)
        iv_decrypted = sim_cipher_decrypt(cipher_bytes=CIPHER_FOR_CIPHER_IV, salt=CIPHER_FOR_CIPHER_SALT)

        encrypted_bytes = read_bytes_of_file(file_path)
        decrypted_bytes = aes_decrypt_without_b64(encrypted_bytes, cipher_decrypted, iv_decrypted)
        write_bytes_to_file(decrypted_file_path, decrypted_bytes)
    else:
        LOG_E(f"none file is processed.")

# MARK: Command Regist

def cmd_regist(subparsers):
    parser = subparsers.add_parser('pcs.build.store', help='pc sdk build tool for game build in postprocess.')
    # parser.add_argument('-h', '--hosts', type=typeparse_list, default=None, help="hosts, E.g: ['wwww.baidu.com', 'www.baidu2.com']")
    parser.add_argument('-p', '--params', type=str, default=None, help='store params, E.g: offcial-pc-10000')
    parser.add_argument('-o', '--origin', type=str, default=None, help='origin full path, E.g:')
    parser.add_argument('-t', '--target', type=str, default=None, help='target full path, E.g:')
    parser.set_defaults(handle=cmd_handle_build_store)

    parser = subparsers.add_parser('pcs.tools.decrypt', help='pc sdk tools for file decryption.')
    parser.add_argument('-p', '--path', type=str, default=None, help='encrypted file path, default search current dir for `pcsdk.json` file.')
    parser.set_defaults(handle=cmd_handle_tools_decrypt)

# python src/devocli/pcs_postbuild.py
if __name__ == '__main__':
    # args = DynamicObject(params='official-pc-10001', origin='', target='/Users/fallenink/Desktop/Developer/devokay-py/tmp')
    # cmd_handle_build_store(args)

    args = DynamicObject(path="/Users/fallenink/Desktop/Developer/devokay-py/tmp/pcsdk.json")
    cmd_handle_tools_decrypt(args)