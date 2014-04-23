# -*- coding: utf-8 -*-
__author__ = 'harlanaubuchon'

import ConfigParser
import os
from sys import platform

## Change USER_DIRECTORY to '~' for *nix and M$ or 
## overwrite function with '/sdcard' for Android
## Change SYSTEM to sys.platform for *nix and M$ or 'ANDROID' for Android

CURRENT_DIRECTORY = os.getcwd()
USER_DIRECTORY = os.path.expanduser('~')
parser = ConfigParser.ConfigParser()
SYSTEM = platform
MINDER_CONFIG_FILE = 'minder_config.ini'
MINDER_HOME = USER_DIRECTORY + '/.Minder/'
M_PATH = MINDER_HOME + MINDER_CONFIG_FILE

# I know this isn't a constant
M_CONFIG = {}

# I might move this to a "defaults" module
DEFAULT_CONFIG = {
                     "defaults": {
                         "space_remaining_threshold_bytes": 2048,
                         "text_difference_threshold_percentage": 99,
                         },
                     "minds": {}
                     }


def minderconfig():
    """ 
    Minder Config returns the Minder config file parsed as a dictionary.  If 
    the initial read fails minderConfig assumes this is a new install or 
    something has deleted the config file in the .Minder home directory.  In 
    this case it writes a new 'Default' Config file.
    
    """

    try:
        _read_minder_config()
        print 'Reading Minder Config'

    except OSError:
        print 'New Minder install...  Creating Minder Home.'
        os.makedirs(MINDER_HOME)
        _write_minder_config(DEFAULT_CONFIG)
        print 'Created Minder Home at %s' % M_PATH

    minder_config = _read_minder_config()

    return minder_config


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

    for section in section_list:
        parser.add_section(section)
        for key in minder_config[section].keys():
            parser.set(section, key, minder_config[section][key])

    with open(M_PATH, 'w') as file_handle:
        parser.write(file_handle)
        print 'Writing Minder Config'

if __name__ == "__main__":
    config = minderconfig()
    for item in config.keys():
        print item, config[item]

