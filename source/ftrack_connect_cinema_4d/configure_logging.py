# :coding: utf-8
# :copyright: Copyright (c) 2015 ftrack
import logging
import os
import os.path
import errno

import appdirs


def get_log_directory():
    '''Get log directory.

    Will create the directory (recursively) if it does not exist.

    Raise if the directory can not be created.
    '''
    user_data_dir = appdirs.user_data_dir('ftrack-connect', 'ftrack')
    log_directory = os.path.join(user_data_dir, 'log')
    try:
        os.makedirs(log_directory)
    except OSError as error:
        if error.errno == errno.EEXIST and os.path.isdir(log_directory):
            pass
        else:
            raise

    return log_directory


def configure_logging(loggerName, level=None, format=None):
    '''Configure `loggerName` loggers with file handler.

    Optionally specify log *level* (default logging.DEBUG)

    Optionally set *format*, default:
    `%(asctime)s - %(name)s - %(levelname)s - %(message)s`.
    '''
    if level is None:
        level = logging.DEBUG

    if format is None:
        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    log_directory = get_log_directory()
    log_file_path = os.path.join(log_directory, '{0}.log'.format(loggerName))
    handler = logging.FileHandler(log_file_path)
    handler.setFormatter(logging.Formatter(format))
    handler.setLevel(level)

    logging.getLogger(loggerName).addHandler(handler)
