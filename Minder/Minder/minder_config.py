# -*- coding: utf-8 -*-
__author__ = 'harlanaubuchon'

import ConfigParser
import os
import json
from sys import platform
import minder_defaults as md

## Change USER_DIRECTORY to '~' for *nix and M$ or 
## overwrite function with '/sdcard' for Android
## Change SYSTEM to sys.platform for *nix and M$ or 'ANDROID' for Android

CURRENT_DIRECTORY = os.getcwd()
USER_DIRECTORY = os.path.expanduser('~')
parser = ConfigParser.ConfigParser()
SYSTEM = platform
MINDER_CONFIG_FILE = 'minder_config.ini'
MINDER_HOME = os.path.join(USER_DIRECTORY, '.Minder')
M_PATH = os.path.join(MINDER_HOME, MINDER_CONFIG_FILE)
M_CONFIG = {}


def minderconfig(minder_config=None, update=False):
    """ 
    Minder Config returns the Minder config file parsed as a dictionary.  If 
    the initial read fails minderConfig assumes this is a new install or 
    something has deleted the config file in the .Minder home directory.  In 
    this case it writes a new 'Default' Config file.
    
    """

    try:
        if update is True and minder_config is not None:
            _write_minder_config(minder_config)

        else:
            _read_minder_config()
            print 'Reading Minder Config'

    except OSError:
        if os.path.isdir(MINDER_HOME) is False:
            print 'New Minder install...  Creating Minder Home.'
            os.makedirs(MINDER_HOME)
        _write_minder_config(md.DEFAULT_CONFIG)
        print 'Created Minder Home at %s' % M_PATH

    minder_config = _read_minder_config()

    return minder_config


def read_minder_settings(as_json=False):
    m_config = minderconfig()
    config_uom = md.CONFIG_UOM
    json_dict= {'sections': []}

    for section in m_config:
        config_items = {
                    "name": section,
                    "items": [],
                    }
        for k, v in m_config[section].iteritems():
            split_label = k.split('_')
            label = k.split('_')
            if split_label[-1] in config_uom:
                config_item =  {
                        "key": k,
                        "value": str(v),
                        "type": config_uom[split_label[-1]]['type'],
                        "label": (' ').join(split_label[:-1]).capitalize(),
                        "uom": config_uom[split_label[-1]]['uom']
                        }
            else:
                 config_item =  {
                        "key": k,
                        "value": str(v),
                        "type": config_uom['text']['type'],
                        "label": (' ').join(label).capitalize(),
                        "uom": config_uom[['text']]['uom']
                        }
            config_items['items'].append(config_item)

        json_dict['sections'].append(config_items)

    if as_json is True:
        je = json.JSONEncoder(indent=4, sort_keys=True, encoding="utf-8")
        json_config = je.encode(json_dict)

    else:
        json_config = json_dict

    return json_config


def _read_minder_config():
    if os.path.isfile(M_PATH):
        parser.read(M_PATH)
        section_list = parser.sections()

        for section in section_list:
            M_CONFIG[section] = {}
            for key, value in parser.items(section):
                M_CONFIG[section][key] = value

    else:
        raise OSError

    return M_CONFIG


def _write_minder_config(minder_config):
    section_list = minder_config.keys()
    try:
        if os.path.isfile(M_PATH) is False:
            for section in section_list:
                parser.add_section(section)
                for key in minder_config[section].keys():
                    parser.set(section, key, minder_config[section][key])
        else:
            for section in section_list:
                for key in minder_config[section].keys():
                    parser.set(section, key, minder_config[section][key])

        with open(M_PATH, 'w') as file_handle:
            parser.write(file_handle)
            print 'Writing Minder Config'

    except:
        raise


if __name__ == "__main__":
    config = minderconfig()
    for item in config.keys():
        print item, config[item]

