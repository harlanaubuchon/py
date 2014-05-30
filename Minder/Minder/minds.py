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
from urllib import quote


MIND_DIR = '.mind'
MIND = 'mind_palace.json'
MINDS = 'minds.json'
MINDS_FILE = os.path.join(mc.MINDER_HOME, MINDS)
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
    hidden_files = eval(mc.minderconfig()['System']['show_hidden_files_boolean'])
    dirs_depth = eval(mc.minderconfig()['System']['directory_listing_depth_number'])
    file_path = os.path.join(mind_path, MIND_FILE)
    mind_time = datetime.fromtimestamp(time.time()).isoformat()[:23] + 'Z'
    minded_time = ["minded_datetime", mind_time]
    deep = True

    if os.path.isfile(file_path):
        if refresh is True:
            mind_palace = interrogate(mind_path, hidden_files, deep, minded_time)
            _write_mind_palace(file_path, mind_palace)
        else:
            mind_palace = _read_mind_palace(file_path)
    else:
        if os.path.isdir(os.path.join(mind_path, MIND_DIR)) is False:
            os.makedirs(os.path.join(mind_path, MIND_DIR))
        mind_palace = interrogate(mind_path, hidden_files, deep, minded_time)
        _write_mind_palace(file_path, mind_palace)

    return mind_palace


def recollect(minds_dict=None):
    minds_section_dict = None
    minds_json = None
    if os.path.isfile(MINDS_FILE):
        minds_section_dict = _read_mind_palace(MINDS_FILE)
    else:
        minds_section_dict = {}

    if isinstance(minds_dict, dict):
        print 'minds.MINDS DICT - %s' % minds_dict
        if minds_dict.has_key('delete'):
            deleted_mind = minds_section_dict.pop(minds_dict['delete'])
            print 'Delete Mind - %s' % deleted_mind

        if minds_dict.has_key('new_mind'):
            new_mind = minds_dict['new_mind']
            minds_name = '%s@%s' % (new_mind['name_of_mind'], new_mind['origin'])
            minds_section_dict[minds_name] = {
                "destination": new_mind['destination'],
                "file_extensions_list": new_mind['file_extensions_list']
                }

        if minds_dict.has_key('delete') is False and minds_dict.has_key('new_mind') is False:
            minds_section_dict[minds_dict.keys()[0]] = minds_dict.values()[0]

        minds_json = _write_mind_palace(MINDS_FILE, minds_section_dict)

    else:
        minds_json = minds_section_dict

    return minds_json


def _file_obj(file_path, deep=None):
    if deep is None:
        deep = False

    size_limit = int(M_CONFIG['Settings']['file_size_limit_kilobytes'])
    file_name = os.path.split(file_path)[-1]
    file_size = int(os.path.getsize(file_path))
    file_modified_time = os.path.getmtime(file_path)
    modified_timestamp = datetime.fromtimestamp(file_modified_time).isoformat()[:23] + 'Z'

    checksum = None

    if deep is True:
        if file_size < size_limit:
            with open(file_path) as file_handle:
                file_data = file_handle.read()
                checksum = hashlib.md5(file_data).hexdigest()

    guess_mime = mimetypes.guess_type(file_name)
    if guess_mime[0] is not None:
        mime_type = guess_mime[0].split('/')

    else:
        mime_type = ['None', 'Unknown']

    mind_file = {
        "name": os.path.split(file_path)[-1],
        "mime_type": '/'.join(mime_type),
        "size": file_size,
        "checksum": checksum,
        "modified_timestamp": modified_timestamp
    }

    return mind_file


def interrogate(mind_path, hidden_files=None, deep=None, minded_time=None):
    """
    minds.interrogate(mind_path=File path, hidden_file=Look for '.name' files, deep=Perform md5 checksum)
    Creates a nested dictionary that represents the folder structure of mind_path
    """
    #mind_path = qp['root']
    print 'MIND PATH = %s' % mind_path
    if hidden_files is None:
        hidden_files = eval(mc.minderconfig()['System']['show_hidden_files_boolean'])
    if deep is None:
        deep = False
    ignore_list = M_CONFIG['System']['ignored_directories_list']
    folder_list = []
    file_list = []
    # I know, let's wrap this thing in a ridiculous try/except block
    # to deal with M$ Windows and all the moronic symlinked directories sprinkled
    # all over the "User" directory! Mr. Balmer, you owe me 5 hours for this crap.
    try:
        directory_list = os.listdir(mind_path)
        
        for node in directory_list:
            node_path = os.path.join(mind_path, node)

            if os.path.isfile(node_path) is True:
                if hidden_files is False and node.startswith('.') is False and node not in ignore_list:
                    file_list.append(node)

                if hidden_files is True:
                    file_list.append(node)

            if os.path.isdir(node_path) is True:
                if hidden_files is False and node.startswith('.') is False and node not in ignore_list:
                    folder_list.append(node)

                if hidden_files is True:
                    folder_list.append(node)
    
          
    except:
        if mc.SYSTEM.startswith('win'):
            print "Microsoft, in their infinite wisdom, has forbidden you from looking at %s" % mind_path
        else:
            print "IOError - Check permissions for folders - %s" % mind_path


    folder_list.sort()
    file_list.sort()

    file_dict_list = []
    folder_dict_list = []

    for file_name in file_list:
        file_path = os.path.join(mind_path, file_name)
        file_dict_list.append(_file_obj(file_path, deep))

    for folder_name in folder_list:
        file_path = os.path.join(mind_path, folder_name)
        folder_dict_list.append(interrogate(file_path, hidden_files, deep))

    mind_dir = {
        "root": os.path.split(mind_path)[0],
        "url": quote(mind_path),
        "name": os.path.split(mind_path)[-1],
        "files": file_dict_list,
        "folders": folder_dict_list
    }

    if minded_time is not None:
        mind_dir[minded_time[0]] = minded_time[1]

    return mind_dir


def _write_mind_palace(mind_path, mind_palace):
    je = json.JSONEncoder(indent=4, sort_keys=True)

    try:
        with open(mind_path, 'w') as write_handle:
            json_dir = je.encode(mind_palace)
            write_handle.write(json_dir)
    except:
        raise

    return mind_palace


def _read_mind_palace(mind_path):
    jd = json.JSONDecoder()

    try:
        with open(mind_path) as read_handle:
            json_string = read_handle.read()
            json_dir = jd.decode(json_string)
    except:
        raise

    return json_dir


if __name__ == "__main__":
    m = mind(USER_DIR, refresh=True)
    print m
