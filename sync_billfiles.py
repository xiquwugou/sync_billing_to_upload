__author__ = 'song'

from datetime import date, datetime, timedelta
from time import clock as now
import commands
import decimal
import urllib2
import json
import datetime
import time
import logging
import logging.config


def get_billing_filename(logger, api):
    try:
        opener = urllib2.urlopen(api, timeout=30)
        datas = []
        for recorder in json.loads(opener.read()):   # By default, it returns one row. It may return fewer rows than you asked for, but never more. If you set maxrows=0, it returns all rows of the result set
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


def send_billing_files(logger, path, remote_address):
    try:
        command = "rsync -av " + path + remote_address
	print  command
        a, b = commands.getstatusoutput(command)
	
        retry = 0
        if a != 0:
            time.sleep(3)
            print 'Exception occur! sleep 3 s, retry......'
            logger.error('Exception occur! sleep 3 s, retry......')
            return send_billing_files(logger, path, remote_address)
    except Exception, e:
        print e
        logger.error(e)
        return send_billing_files(logger, path, remote_address)


def copy_files_to_temp(logger, path, remote_address):
    try:
        command = "cp  " + path + "  /Application/billing/billingSync/temp/"
        a, b = commands.getstatusoutput(command)
        retry = 0
        if a != 0:
            time.sleep(3)
            logger.error(command)
    except Exception, e:
        print e
        logger.error(e)

def tar_files_to_temp():
    try:
        command = "sh /Application/billing/billingSync/tar.sh"
        a, b = commands.getstatusoutput(command)
    except Exception, e:
        print e
        logger.error(e)

if __name__ == '__main__':
    try:
        logging.config.fileConfig("logging.conf")
        logger = logging.getLogger("sync_billing_log")
#        api = 'http://monitor.chinacache.net/billing/get_diff_data/?role=1'
        api = 'http://monitor.chinacache.net/billing/get_diff_data_bydate/?role=1&start_time=201310081900&end_time=201310082335'
#        remote_ip = ''
#        remote_device_alias_name = ''
	remote_ip = '192.168.131.198'
	
	remote_device_alias_name = 'CcSnp'
        filenames = get_billing_filename(logger, api)
        prefix_dir = '/Data/billing/upload_normandy/history'
        remote_address = " fromcf@" + remote_ip + "::" + remote_device_alias_name
	print remote_address
	print len(filenames)
        for f in filenames:
            path = prefix_dir + "/" + f["day"] + "/" + f["dev_name"] + "/" + f["filename"]
            #send_billing_files(logger, path, remote_address)
            copy_files_to_temp(logger, path, remote_address)
            logger.info(path)
	tar_files_to_temp()
	send_billing_files(logger,"/Application/billing/billingSync/tgz/*.tgz",remote_address)
        a, b = commands.getstatusoutput("rm -f /Application/billing/billingSync/tgz/*.tgz")
    except Exception, e:
        print e
    finally:
        print 'finshed'




