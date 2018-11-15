# -*-coding:utf-8-*-
"""
 @desc:
 @author: yewangping
 @site:
 @software: PyCharm
 @file: t_config_mq_info.py
 @time: 2018/2/9 9:11
"""
from brick.db.dbconnect import execute_db


class t_config_mq_info():
    def __init__(self, db_cnxn=None):
        self.cnxn = db_cnxn

    def get_mq_info(self, ip=None, platformName=None):
        cursor = self.cnxn.cursor()
        sql = "select IP,Name,K,V from t_config_online_amazon  where IP= %s AND PlatformName=%s"
        print sql
        cursor.execute(sql, (ip.strip(), platformName))
        t_config_mq_info_objs = cursor.fetchall()
        print t_config_mq_info_objs
        cursor.close()

        MQ_dict = {}
        MQ_dict['IP'] = ip.strip()
        for t_config_mq_info_obj in t_config_mq_info_objs:
            MQ_dict[t_config_mq_info_obj.K] = t_config_mq_info_obj.V

        return MQ_dict

    def get_rabbitmq_info_by_name_platform(self, Name, PlatformName):
        sql = "SELECT IP, K, V FROM t_config_mq_info WHERE Name='%s' AND PlatformName='%s';" % (Name, PlatformName)
        res = execute_db(sql, self.cnxn, 'select')
        RABBITMQ = dict()
        for i in res:
            if i.get('K') == 'MQPort':
                RABBITMQ['port'] = i.get('V')
            elif i.get('K') == 'MQUser':
                RABBITMQ['username'] = i.get('V')
            elif i.get('K') == 'MQPassword':
                RABBITMQ['password'] = i.get('V')
            else:
                pass
            RABBITMQ['hostname'] = i.get('IP')
        return RABBITMQ
