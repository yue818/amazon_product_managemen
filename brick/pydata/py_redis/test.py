from py_SynRedis_pub import py_SynRedis_pub
from py_redis_log import py_redis_log
from redis import Redis
import time

'''
from django_redis import get_redis_connection
import os
import sys

sys.path.append('/data/djangostack-1.9.7/apps/django/django_projects/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
connRedis = get_redis_connection(alias='py_add1')
'''

connRedis = Redis(host='192.168.105.223', port=6379,db=0)

if __name__ == "__main__":
    pLog = py_redis_log()

    nMax = 1000000
    nWriteTime = 0.0
    nReadTime = 0.0
    nDelTime = 0.0
    strStartTime = pLog.get_time_stamp()
    print  strStartTime
    for i in range(0, nMax):
        connRedis.hset('testRedis', '01', 'wangzhiyang')
    strEndTime = pLog.get_time_stamp()
    print strEndTime

    strStartTime = pLog.get_time_stamp()
    print strStartTime
    for i in range(0, nMax):
        connRedis.hget('testRedis', '01')
    strEndTime = pLog.get_time_stamp()
    print strEndTime


