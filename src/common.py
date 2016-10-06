#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2016年10月02日
@author: gongqingyi
@email:  gongqingyi@qq.com
"""

import os
import shutil
import logging
import logging.config
import configparser
import utility


def get_root():
    return os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../')


def get_logger():
    root = get_root()
    f1 = root + os.sep + 'conf' + os.sep + 'logger.conf'
    f2 = f1 + '.' + str(utility.get_microsecond())
    shutil.copyfile(f1, f2)
    utility.file_replace(f2, '\$\{app_home\}', root)
    logging.config.fileConfig(f2)
    logger = logging.getLogger('root')   #其他模块直接 get
    os.remove(f2)
    return logger


def get_system_conf():
    root = get_root()
    conf_file = root + os.sep + 'conf' + os.sep + 'system.conf'
    config = configparser.ConfigParser()
    config.read(conf_file)
    for k, v in config.items():
        for _k, _v in v.items():
            v[_k] = _v.replace(' ', '')
    return config

log = get_logger()


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton
