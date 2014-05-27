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
import logging

WAIT_TIME = eval(mc.minderconfig()['Settings']['mind_time_minutes'])
LOG_HOME = os.path.join(mc.MINDER_HOME, 'logs')
M_CONFIG = mc.minderconfig()

#TODO Add a file size check and zip/tar.gz archiver
if os.path.isdir(LOG_HOME):
    os.chdir(LOG_HOME)
else:
    os.mkdir(LOG_HOME)
    os.chdir(LOG_HOME)

logging.basicConfig(filename='daemon.log',level=logging.DEBUG)


def mind_daemon():

    mind_time = datetime.fromtimestamp(time.time()).isoformat()[:23] + 'Z'
    log_event = '%s-MINDER DAEMON - Looking for work.' % mind_time
    logging.info(log_event)
    minds_config = minds.recollect()


    if len(minds_config.keys()) > 0:
        for key in minds_config:
            file_list = []
            ext_list = minds_config[key]['file_extensions_list'].replace(' ', '').split(',')
            search_folder = key.split('@')[1]
            dest_folder = minds_config[key]['destination']

            for file_ext in ext_list:
                l = [files for files in os.listdir(search_folder) if files.endswith(file_ext)]
                for i in l:
                    file_list.append(os.path.join(search_folder, i))
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
                        log_event0 = '%s-MINDER DAEMON moved - %s to - %s' % (mind_time, target, dest_folder)
                        logging.info(log_event0)

                    else:
                        with open(potential_file) as file_handle:
                            file_data = file_handle.read()
                            potential_md5 = hashlib.md5(file_data).hexdigest()

                        if potential_md5 == target_md5:
                            log_event1 = '%s-MINDER DAEMON found identical file %s in %s' % (mind_time, potential_file, dest_folder)
                            logging.info(log_event1)
                            os.remove(target)
                            log_event2 = '%s-MINDER DAEMON Deleted duplicate file %s' % (mind_time, target)
                            logging.info(log_event2)

                        else:
                            file_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S-%f')
                            rename_file = '%s_%s' % (file_timestamp, target_name)
                            shutil.move(target, os.path.join(dest_folder, rename_file))
                            log_event3 = '%s-MINDER DAEMON Renamed duplicate file name %s to %s' % (mind_time, target, rename_file)
                            logging.info(log_event3)

            except:
                raise

    else:
        log_event4 = '%s-MINDER DAEMON - Nothing to do here. Sleeping for %s minutes' % (mind_time, WAIT_TIME)
        logging.info(log_event4)

    log_event9 = '%s-MINDER DAEMON - Nothing left to do. Going back to sleep for %s minutes' % (mind_time, WAIT_TIME)
    logging.info(log_event9)

    return 0


def daemon_runner():
    while True:
        time.sleep(WAIT_TIME * 60)
        runner_time = datetime.fromtimestamp(time.time()).isoformat()[:23] + 'Z'
        log_start = '%s-MINDER DAEMON - Runner waking up deamon' % runner_time
        logging.info(log_start)
        mind_daemon()


if __name__ == "__main__":
    daemon_runner()
