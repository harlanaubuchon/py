# -*- coding: utf-8 -*-
__author__ = 'harlanaubuchon'

import os
from datetime import datetime
import time
import hashlib
import json
from functools import reduce


MIND_DIR = '/.mind'
MIND = '/mind_palace.json'
MIND_FILE = MIND_DIR + MIND


def mind(mind_path, refresh=False):
    """ 
    Minds returns a JSON Data object representing the file structure and some 
    useful meta-data about the files for the path given.  An optional argument
    refresh=True can be used to re-save the mind_palace.json file to the .mind 
    directory.
    """

    file_path = mind_path + MIND_FILE  # Replace this with Class attribute
    mind_time = datetime.fromtimestamp(time.time()).isoformat()[:23] + 'Z'
    mind_dir = {mind_path: {"minded_datetime": mind_time}}

    if os.path.isfile(file_path):
        if refresh is True:
            mind_palace = interrogate(mind_path, mind_dir)
        else:
            mind_palace = _read_mind_palace(mind_path)
    else:
        if os.path.isdir(mind_path + MIND_DIR) is False:
            os.makedirs(mind_path + MIND_DIR)
        mind_palace = interrogate(mind_path, mind_dir)
        _write_mind_palace(mind_path, mind_palace)

    return mind_palace


def interrogate(mind_path, mind_dir):
    """
    Adapted from:
    code.activestate.com/recipes/577879-create-a-nested-dictionary-from-oswalk
    Created by Andrew Clark on Mon, 26 Sep 2011 (MIT)
    Creates a nested dictionary that represents the folder structure of mind_path
    """
    file_dir = {}
    mind_path = mind_path.rstrip(os.sep)
    start = mind_path.rfind(os.sep) + 1
    for path, dirs, files in os.walk(mind_path):
        folders = path[start:].split(os.sep)
        subdir = dict.fromkeys(files)
        if len(files) > 0:
            for file_name in files:
                with open(path + '/' + file_name) as file_handle:
                    file_data = file_handle.read()
                    checksum = hashlib.md5(file_data).hexdigest()
                    subdir[file_name] = {"md5_sum": checksum, "mime_type": None}
        parent = reduce(dict.get, folders[:-1], file_dir)
        parent[folders[-1]] = subdir

    dir_key = file_dir.keys()[0]
    mind_dir[mind_path][dir_key] = file_dir[dir_key]

    return mind_dir


def _write_mind_palace(mind_path, mind_palace):
    je = json.JSONEncoder(indent=4, sort_keys=True, encoding="utf-8")
    file_path = mind_path + MIND_FILE  # Replace this with Class attribute
    with open(file_path, 'w') as write_handle:
        json_dir = je.encode(mind_palace)
        write_handle.write(json_dir)


def _read_mind_palace(mind_path):
    jd = json.JSONDecoder(encoding="utf-8")
    file_path = mind_path + MIND_FILE  # Replace this with Class attribute
    with open(file_path) as read_handle:
        json_string = read_handle.read()
        json_dir = jd.decode(json_string)

    return json_dir