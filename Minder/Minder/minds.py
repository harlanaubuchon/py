# -*- coding: utf-8 -*-
__author__ = 'harlanaubuchon'

import os
from datetime import datetime
import time
import hashlib
import json
import mimetypes
from functools import reduce
import minder_config as mc


MIND_DIR = '.mind'
MIND = 'mind_palace.json'
MIND_FILE = os.path.join(MIND_DIR, MIND)
USER_DIR = os.path.expanduser('~')
M_CONFIG = mc.minderconfig()


def _init_mindtypes():
    mind_types = {}
    for i in mimetypes.types_map.keys():
        k = mimetypes.types_map[i].split('/')[0]
        mind_types.setdefault(k, {})
        mind_types[k][i] = mimetypes.types_map[i]
    return mind_types


mindtypes = _init_mindtypes()


def mind(mind_path, refresh=False):
    """ 
    Minds returns a JSON Data object representing the file structure and some 
    useful meta-data about the files for the path given.  An optional argument
    refresh=True can be used to re-save the mind_palace.json file to the .mind 
    directory.
    """

    file_path = os.path.join(mind_path, MIND_FILE)
    mind_time = datetime.fromtimestamp(time.time()).isoformat()[:23] + 'Z'
    mind_dir = {mind_path: {"minded_datetime": mind_time}}

    if os.path.isfile(file_path):
        if refresh is True:
            mind_palace = interrogate(mind_path, mind_dir)
            _write_mind_palace(mind_path, mind_palace)
        else:
            mind_palace = _read_mind_palace(mind_path)
    else:
        if os.path.isdir(os.path.join(mind_path, MIND_DIR)) is False:
            os.makedirs(os.path.join(mind_path, MIND_DIR))
        mind_palace = interrogate(mind_path, mind_dir)
        _write_mind_palace(mind_path, mind_palace)

    return mind_palace


def _file_obj(path, hidden_files=False):
    size_limit = int(M_CONFIG['defaults']['file_size_limit_in_kilobytes'])
    file_name = os.path.split(path)[-1]
    file_size = int(os.path.getsize(path))

    checksum = None

    if hidden_files is True:
        if file_size < size_limit:
            with open(path) as file_handle:
                file_data = file_handle.read()
                checksum = hashlib.md5(file_data).hexdigest()

    guess_mime = mimetypes.guess_type(file_name)
    if guess_mime[0] is not None:
        mime_type = guess_mime[0].split('/')

    else:
        mime_type = ['None', 'Unknown']

    mind_file = {
        "name": os.path.split(path)[-1],
        "mime_type": '/'.join(mime_type),
        "size": file_size,
        "checksum": checksum
    }

    return mind_file


def interrogate(mind_path, mind_dir=None, hidden_files=False):
    """
    Creates a nested dictionary that represents the folder structure of mind_path
    """
    print hidden_files
    folder_list = []
    file_list = []

    for node in os.listdir(mind_path):
        node_path = os.path.join(mind_path, node)

        if os.path.isfile(node_path) is True:
            if hidden_files is False and node.startswith('.') is False:
                file_list.append(node)

            if hidden_files is True:
                file_list.append(node)

        if os.path.isdir(node_path) is True:
            if hidden_files is False and node.startswith('.') is False:
                folder_list.append(node)

            if hidden_files is True:
                folder_list.append(node)

    folder_list.sort()
    file_list.sort()

    file_dict_list = []
    folder_dict_list = []

    for file_name in file_list:
        file_path = os.path.join(mind_path, file_name)
        file_dict_list.append(_file_obj(file_path, hidden_files))

    for folder_name in folder_list:
        file_path = os.path.join(mind_path, folder_name)
        folder_dict_list.append(interrogate(file_path, hidden_files))

    mind_dir = {
        "root": os.path.split(mind_path)[0],
        "name": os.path.split(mind_path)[-1],
        "files": file_dict_list,
        "folders": folder_dict_list
    }
    #ji = json.dumps(mind_dir, indent=4, sort_keys=True)
    #result = json.loads(ji)
    return mind_dir


def _write_mind_palace(mind_path, mind_palace):
    je = json.JSONEncoder(indent=4, sort_keys=True, encoding="utf-8")
    file_path = os.path.join(mind_path, MIND_FILE)
    with open(file_path, 'w') as write_handle:
        json_dir = je.encode(mind_palace)
        write_handle.write(json_dir)


def _read_mind_palace(mind_path):
    jd = json.JSONDecoder(encoding="utf-8")
    file_path = os.path.join(mind_path, MIND_FILE)
    with open(file_path) as read_handle:
        json_string = read_handle.read()
        json_dir = jd.decode(json_string)

    return json_dir


if __name__ == "__main__":
    m = mind(USER_DIR, refresh=True)
    print m
