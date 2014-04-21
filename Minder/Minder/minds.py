__author__ = 'harlanaubuchon'

import os
from datetime import datetime
import time
import hashlib
import pprint
import json
from collections import namedtuple

MIND_DIR = '/.mind'
MIND = '/mind_palace'
MIND_FILE = MIND_DIR + MIND
#null = None


def mind(mind_path):
    file_path = mind_path + MIND_FILE  # Replace this with Class attribute
    mind_time = datetime.fromtimestamp(time.time()).isoformat()[:23] + 'Z'
    mind_dir = {mind_path: {"minded_datetime": mind_time}}

    if os.path.isfile(file_path):
        mind_palace = _read_mind_palace(mind_path)
    else:
        if os.path.isdir(mind_path + MIND_DIR) is False:
            os.makedirs(mind_path + MIND_DIR)
        mind_palace = interrogate(mind_path, mind_dir)
        _write_mind_palace(mind_path, mind_palace)

    return mind_palace


def interrogate(mind_path, mind_dir):
    """
    Creates a nested dictionary within mind_dir that represents the folder structure of
    mind_path.
    """
    start = mind_path.rfind(os.sep) + 1

    for dir_name, dirs, files in os.walk(mind_path):
        folders = dir_name[start:].split(os.sep)
        sub_dir = dict.fromkeys(files)

        parent = reduce(dict.get, folders[:-1], mind_dir[mind_path])
        parent[folders[-1]] = sub_dir

    """
    for (dir_name, dirs, files) in os.walk(path):
        for dirs_name in dirs:
            counter = 0
            if dirs_name.startswith('.'):
                print 'found a . in %s - removing from list' %dirs_name
                dirs.pop(counter)
            counter += 1

        for file_name in files:
            if filename[0] != '.':
                thefile = os.path.join(dir_name,file_name)
                file_handle = open(thefile,'r')
                file_data = file_handle.read()
                file_handle.close()
                checksum = hashlib.md5(file_data).hexdigest()
                file_dict[checksum] = thefile
                print os.path.getsize(thefile), thefile, checksum
    """
    return mind_dir


def _write_mind_palace(mind_path, mind_palace):
    je = json.JSONEncoder(indent=4, sort_keys=True)
    file_path = mind_path + MIND_FILE  # Replace this with Class attribute
    with open(file_path, 'w') as write_handle:
        json_dir = je.encode(mind_palace)
        write_handle.write(json_dir)
        print 'Writing Mind'


def _read_mind_palace(mind_path):
    jd = json.JSONDecoder()
    file_path = mind_path + MIND_FILE  # Replace this with Class attribute
    with open(file_path) as read_handle:
        json_string = read_handle.read()
        json_dir = jd.decode(json_string)
        print 'Reading Mind'

    return json_dir