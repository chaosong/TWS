#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2016年09月16日
@author: gongqingyi
@email:  gongqingyi@qq.com
"""

import time
import datetime  # datetime, date, time, timedelta, tzinfo

import os
import re
import imp
import platform
import shutil
import zipfile
import functools
import threading
import subprocess


def get_datetime_string(seconds=0, fmt='%Y-%m-%d %H:%M:%S'):
    if seconds == 0:
        seconds = time.time()
    return time.strftime(fmt, time.localtime(seconds))


def get_seconds(dt=None, fmt='%Y-%m-%d %H:%M:%S'):
    if dt is None:
        return int(time.time())
    return int(time.mktime(time.strptime(dt, fmt)))


def get_microsecond():
    now = datetime.datetime.now()
    return int(1000000 * (time.mktime(now.timetuple())) + now.microsecond)


def get_today(fmt='%Y-%m-%d'):
    return datetime.datetime.now().strftime(fmt)


def get_date(offset=0, base=None, fmt='%Y%m%d'):
    s = get_seconds() + offset * 3600 * 24
    if base is not None:
        s += (get_seconds(base, '%Y%m%d') - get_seconds())
    return get_datetime_string(s, fmt)


def get_weekday():
    return datetime.date.fromtimestamp(time.time()).isoweekday()


def load_module(module_path, module_name):
        a = imp.find_module(module_name, [module_path])
        return imp.load_module(module_name, a[0], a[1], a[2])


def time_cost(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = get_microsecond()
        func(*args, **kwargs)
        end = get_microsecond()
        cost = (end - start)/1000000.0
        print("%s cost %s seconds" % (func.__name__, cost))
    return wrapper


def async(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        threading.Thread(target=func, args=args, kwargs=kwargs).start()
    return wrapper


def is_empty(s):
    return s is None or s.strip() == ''


def get_platform():
    arr = platform.platform().split('-')
    return arr[0].lower(), arr[1]


def get_files(path):
    files = []
    for parent, dir_names, filenames in os.walk(path):
        for filename in filenames:
            files.append(os.path.join(parent, filename))
    return files


def get_size(path):
    size = 0
    for f in get_files(path):
        if is_file(f):
            size += os.path.getsize(f)
    return size


def is_file(filename):
    return os.path.isfile(filename)


def is_dictionary(path):
    return os.path.isdir(path)


def file_replace(filename, old, new):
    f_new = filename + '.' + str(get_microsecond())
    with open(filename, 'r') as f1:
        content, cnt = re.subn(old, new, f1.read())
        with open(f_new, 'w') as f2:
            f2.write(content)
    shutil.move(f_new, filename)


def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()


def write_file(filename, content):
    mkdir(os.sep.join(filename.split(os.sep)[:-1]))
    with open(filename, 'w') as f:
        f.write(content)


def mkdir(path):
    path = path.strip().rstrip(os.sep)
    if not os.path.exists(path):
        os.makedirs(path)


def copy(src, dst):
    if not is_dictionary(src) and not is_file(src):
        return
    if is_dictionary(dst):
        shutil.rmtree(dst)
    if is_file(dst):
        os.remove(dst)
    if not is_dictionary(src):
        shutil.copyfile(src, dst)
    if is_dictionary(src):
        shutil.copytree(src, dst)


def rm(path):
    if not is_dictionary(path) and not is_file(path):
        return
    if is_dictionary(path):
        shutil.rmtree(path)
    if is_file(path):
        os.remove(path)


def zip_dir(dir_name, zip_filename):
    filelist = []
    if os.path.isfile(dir_name):
        filelist.append(dir_name)
    else:
        for root, dirs, files in os.walk(dir_name):
            for name in files:
                filelist.append(os.path.join(root, name))
    zf = zipfile.ZipFile(zip_filename, 'w', zipfile.zlib.DEFLATED)
    for f in filelist:
        arcname = f[len(dir_name):]
        zf.write(f, arcname)
    zf.close()


def unzip_file(zip_filename, unzip_to_dir):
    if not os.path.exists(unzip_to_dir):
        os.makedirs(unzip_to_dir, 755)
    zf_obj = zipfile.ZipFile(zip_filename)
    for name in zf_obj.namelist():
        if name.endswith(os.sep):
            os.makedirs(os.path.join(unzip_to_dir, name))
        else:
            ext_filename = os.path.join(unzip_to_dir, name)
            ext_dir = os.path.dirname(ext_filename)
            if not os.path.exists(ext_dir):
                os.makedirs(ext_dir, 755)
            outfile = open(ext_filename, 'wb')
            outfile.write(zf_obj.read(name))
            outfile.close()


def shell_cmd(cmd):
    f = re.subn(' +', ' ', cmd)[0].split(';')[-1].split(' ')[0]  # export k=v; f.sh v1 v2 v3
    if is_file(f):
        process = subprocess.Popen('chmod +x ' + f, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        process.wait()
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while process.poll() is None:
        ret = process.stdout.readline()
        if len(ret.strip()) == 0:
            continue
        if ret.lower().find('error') >= 0 or ret.lower().find('fail') >= 0:
            return 1
    return process.returncode



if __name__ == "__main__":
    print(get_datetime_string())
    print(get_datetime_string(1332888820, '%Y-%m-%d %H:%M:%S'))

    print(get_seconds())
    print(get_seconds('2013-10-25 13:25:40'))

    print(get_microsecond())
    print(get_today('%Y%m%d'))
    print(get_weekday())
