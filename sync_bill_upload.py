#-*-encoding:utf-8-*-
import commands
import hashlib
import json
import logging
import logging.config
from os import rename

import pprint
import unittest
import time
import urllib2
import sys
from BackupFile import BackupFile

__author__ = 'song'

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("sync")


def get_billing_filename(api):
    try:
        opener = urllib2.urlopen(api, timeout=30)
        datas = []
        for recorder in json.loads(
                opener.read()):
            billing_filename = {
                "filename": recorder["filename"],
                "dev_name": recorder["dev_name"],
                "day": recorder["day"]
            }
            datas.append(billing_filename)
        return datas
    except Exception, e:
        print e
        logger.error(e)


def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def split_list(file_names=["song", 'xiao', "feng", "desk", "book", "cook"]):
    return list(chunks(file_names, 100))


def get_file_name():
    prefix = 'StatisticData_'
    return prefix + time.strftime('%Y%m%d%H%M%S') + "_"


def md5sum(filename):
    md5 = hashlib.md5()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(128 * md5.block_size), b''):
            md5.update(chunk)
    return md5.hexdigest()


def create_tar_file(file_list):
    backup = BackupFile("tmp")
    backup.add_files(file_list)


def append_md5(filename):
    _md5 = md5sum(filename)
    _file_name = get_file_name()
    rename(filename, _file_name + _md5 + ".tgz")


def create_api():
    if len(sys.argv) < 3:
        print 'error, please input start and end time!'
        return ''
    start = sys.argv[1]
    end = sys.argv[2]
    url = 'http://monitor.chinacache.net/billing/get_diff_data_bydate/?role=1'
    return url + "&start_time=" + start + '&end_time=' + end


def get_history_dir_file_path(f):
    prefix_dir = '/Data/billing/upload_normandy/history'
    path = prefix_dir + "/" + f["day"] + "/" + f["dev_name"] + "/" + f["filename"]
    return path


def append_path_to_fragment(f):
    paths = []
    for p in f:
        path = get_history_dir_file_path(p)
        paths.append(path)
    return paths


def create_send_billing_files_command(path, remote_address):
    return "rsync -av " + path + remote_address


def create_rm_command(path):
    return "rm -f " + path



def execute_linux_command(_command):
    try:
        a, b = commands.getstatusoutput(_command)
    except Exception, e:
        logger.error(e)


def send_file():
    remote_ip = '192.168.131.198'
    remote_device_alias_name = 'CcSnp'
    remote_address = " fromcf@" + remote_ip + "::" + remote_device_alias_name
    path = "/Application/billing/billingSync/tgz/*.tgz"
    send_command = create_send_billing_files_command(path, remote_address)
    _create_rm_command = create_rm_command(path)
    logger.info(send_command)
    logger.info(_create_rm_command)
    # execute_linux_command(send_command)
    # execute_linux_command(_create_rm_command)

if __name__ == '__main__':
    url = create_api()
    print url
    data = get_billing_filename(url)
    logger.info('read file size is [ ' + str(len(data)) + ' ]')
    fragments = split_list(data)
    for f in fragments:
        f = append_path_to_fragment(f)
        create_tar_file(f)
        append_md5("tmp")
    send_file()


class MyTests(unittest.TestCase):
    def test_split_list(self):
        fragment = split_list(file_names=["song", 'xiao', "feng", "desk", "book", "cook"])
        d = get_file_name()
        logger.info(d)
        md5name = md5sum("test.log")
        # self.assertEqual("null", md5name)
        # self.assertEqual("null", d)
        self.assertEqual(3, len(fragment))

    def test_create_tar_file(self):
        create_tar_file(file_list=["C:\\Sites\\a.txt"])
        append_md5("tmp")
        self.assertEqual(1, 1)





