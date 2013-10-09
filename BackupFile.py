import profile
import unittest

__author__ = 'song'

import tarfile
import os.path


class BackupFile(object):
    def __init__(self, fileName):
        self.__filename = fileName

    def add_files(self, file_list):
        backup_file = tarfile.open(self.__filename, 'w')
        try:
            for fl in file_list:
                tarinfo = backup_file.gettarinfo(fl, os.path.basename(fl))
                backup_file.addfile(tarinfo, open(fl, 'rb'))
        finally:
            backup_file.close()

    def extract(self, data_dir, log_dir):
        backup_file = tarfile.open(self.__filename, 'r')
        try:
            for info in backup_file.getmembers():
                if os.path.splitext(info.name)[0][-3:] == 'log':
                    backup_file.extract(info, log_dir)
                else:
                    backup_file.extract(info, data_dir)
        finally:
            backup_file.close()


class IsOddTests(unittest.TestCase):
    def testOne(self):
        backup = BackupFile("song.test.tar")
        backup.add_files(file_list=["C:\\baidu player\\style.css", "C:\\Sites\\a.txt"])
        self.assertEqual(1, 1)


