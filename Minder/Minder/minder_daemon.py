#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Harlan AuBuchon'

import os
import shutil
import minder_config as mc
import minds
from datetime import datetime
import time
import hashlib
import collections
import logging

WAIT_TIME = eval(mc.minderconfig()['Settings']['mind_time_minutes'])
DIR_DEPTH = eval(mc.minderconfig()['System']['directory_listing_depth_number'])
LOG_HOME = os.path.join(mc.MINDER_HOME, 'logs', 'minder.log')
M_CONFIG = mc.minderconfig()

#TODO Add a file size check and zip/tar.gz archiver for logfiles
if os.path.isdir(os.path.join(mc.MINDER_HOME, 'logs')) is False:
    os.mkdir(os.path.join(mc.MINDER_HOME, 'logs'))

logging.basicConfig(filename=LOG_HOME, level=logging.DEBUG)


def mind_daemon():
    # TODO Use minds.mind to setup json file for use here once Git binary compile issues are sorted
    mind_time = datetime.fromtimestamp(time.time()).isoformat()[:23] + 'Z'
    logging.info('%s-MINDER DAEMON - Looking for work.' % mind_time)
    minds_config = minds.recollect()

    if minds_config:
        for key in minds_config:
            file_list = []
            ext_list = minds_config[key]['file_extensions_list'].replace(' ', '').split(',')
            search_folder = key.split('@')[1]
            dest_folder = minds_config[key]['destination']
            f_cnt = collections.Counter()
            minds.mind(dest_folder)
            logging.info('%s-MINDER DAEMON - Setting up Destination Directory %s.' % (mind_time, dest_folder))

            if os.path.isdir(search_folder):
                m = minds.mind(search_folder)
                logging.info('%s-MINDER DAEMON - Analyzing Directory %s.' % (mind_time, search_folder))
                for file_ext in ext_list:
                    l = [files for files in os.listdir(search_folder) if files.endswith(file_ext)]
                    for i in l:
                        file_list.append(os.path.join(search_folder, i))

                    for i in m['files']:
                        f_cnt[i['name'].split('.')[-1]] += 1

                try:
                    for target in file_list:
                        target_md5 = 0
                        potential_md5 = 1
                        target_name = target.split(os.path.sep)[-1]
                        potential_file = os.path.join(dest_folder, target_name)

                        with open(target) as file_handle:
                            file_data = file_handle.read()
                            target_md5 = hashlib.md5(file_data).hexdigest()

                        if os.path.isfile(potential_file) is False:
                            shutil.move(target, dest_folder)
                            logging.info('%s-MINDER DAEMON - Moved - %s to - %s' % (mind_time, target, dest_folder))

                        else:
                            with open(potential_file) as file_handle:
                                file_data = file_handle.read()
                                potential_md5 = hashlib.md5(file_data).hexdigest()

                            if potential_md5 == target_md5:
                                logging.info('%s-MINDER DAEMON - Found identical file %s in %s' % (
                                    mind_time, potential_file, dest_folder
                                ))
                                os.remove(target)
                                logging.info('%s-MINDER DAEMON - Deleted duplicate file %s' % (mind_time, target))

                            else:
                                #file_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S-%f')
                                rename_file = '%s_%s' % (potential_md5, target_name)
                                if os.path.isfile(os.path.join(dest_folder, rename_file)):
                                    os.remove(target)
                                    logging.info('%s-MINDER DAEMON - Duplicate file name %s found again. Deleting %s' % (
                                        mind_time, rename_file, target
                                    ))
                                else:
                                    shutil.move(target, os.path.join(dest_folder, rename_file))
                                    logging.info('%s-MINDER DAEMON - Renamed duplicate file name %s to %s' % (
                                        mind_time, target, rename_file
                                    ))

                except Exception, e:
                    logging.exception(e)

            else:
                logging.info('%s-MINDER DAEMON - No Directory %s, this is a trick...' % (mind_time, search_folder))

    else:
        logging.info('%s-MINDER DAEMON - Nothing to do here. Sleeping for %s minutes' % (mind_time, WAIT_TIME))

    logging.info('%s-MINDER DAEMON - Nothing left to do. Going back to sleep for %s minutes' % (mind_time, WAIT_TIME))

    return 0


def daemon_runner():
    while True:
        try:
            time.sleep(WAIT_TIME * 60)
            runner_time = datetime.fromtimestamp(time.time()).isoformat()[:23] + 'Z'
            logging.info('%s-MINDER DAEMON - Runner waking up daemon' % runner_time)
            mind_daemon()

        except KeyboardInterrupt:
            runner_time = datetime.fromtimestamp(time.time()).isoformat()[:23] + 'Z'
            logging.info('%s-MINDER DAEMON - Shutting down' % runner_time)
            exit(0)

if __name__ == "__main__":
    daemon_runner()

