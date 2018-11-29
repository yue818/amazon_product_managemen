# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: 20181129.py
 @time: 2018/11/29 16:54
"""
import logging.handlers
from mws import Reports, Products, Finances, MWSError
import time
import datetime
import pymysql
import traceback
from bs4 import BeautifulSoup
import requests
import logging
import logging.handlers
import platform
import os
import sys
import win32api
import oss2
import chardet
from requests.exceptions import ConnectionError

log_day = datetime.datetime.now().strftime("%Y%m%d")
log_file_name = 'fba_refresh_' + log_day + '.log'
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [%(filename)s %(funcName)s:%(lineno)d] %(thread)d %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=log_file_name,
                    filemode='a')

logging.handlers.RotatingFileHandler(log_file_name,
                                     maxBytes=20 * 1024 * 1024,
                                     backupCount=10)

DATABASE = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'hq_db',
    'HOST': 'rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com',
    'PORT': '3306',
    'USER': 'by15161458383',
    'PASSWORD': 'K120Esc1'
}


class GetLocalIPAndAuthInfo:
    """
    获取当前vps服务器IP；从数据库获取MQ信息
    """

    def __init__(self):
        self.db_conn = pymysql.connect(DATABASE['HOST'],
                                       DATABASE['USER'],
                                       DATABASE['PASSWORD'],
                                       DATABASE['NAME'])

    def close_db_conn(self):
        try:
            if self.db_conn:
                self.db_conn.close()
        except Exception as ex:
            print ex
            logging.error('class  GetLocalIPAndAuthInfo close db connection failed!')
            logging.error('traceback.format_exc():\n%s' % traceback.format_exc())

    @staticmethod
    def get_real_url(url=r'http://www.ip138.com/'):
        r = requests.get(url)
        txt = r.text
        soup = BeautifulSoup(txt, "html.parser").iframe
        return soup["src"]

    @staticmethod
    def get_out_ip(url):
        r = requests.get(url)
        txt = r.text
        ip = txt[txt.find("[") + 1: txt.find("]")]
        print('ip:' + ip)
        return ip

    def get_mq_info(self):
        cursor = self.db_conn.cursor()
        try:
            rabbit_mq = {}
            sql = "select ip, k, v from t_config_mq_info where name = 'Amazon-RabbitMQ-Server'"
            cursor.execute(sql)
            mq_config_info = cursor.fetchall()
            cursor.close()
            for mq_config_info_obj in mq_config_info:
                rabbit_mq['hostname'] = mq_config_info_obj[0]
                k = mq_config_info_obj[1]
                v = mq_config_info_obj[2]
                rabbit_mq[k] = v
            return rabbit_mq
        except Exception as e:
            cursor.close()
            print e
            return None

    def get_auth_info_by_ip(self, ip):
        cursor = self.db_conn.cursor()
        sql = "select IP,Name,K,V, site from t_config_online_amazon  where IP= '%s'" % ip
        print sql
        cursor.execute(sql)
        t_config_online_amazon_objs = cursor.fetchall()
        print t_config_online_amazon_objs
        cursor.close()
        auth_info_all = dict()
        for t_config_obj in t_config_online_amazon_objs:
            if t_config_obj[1] in auth_info_all:
                auth_info_all[t_config_obj[1]]['ShopIP'] = ip
                auth_info_all[t_config_obj[1]]['update_type'] = 'refresh_ad_data'
                auth_info_all[t_config_obj[1]]['table_name'] = 't_online_info_amazon'
                auth_info_all[t_config_obj[1]]['ShopName'] = t_config_obj[1]
                auth_info_all[t_config_obj[1]]['ShopSite'] = t_config_obj[4]
                auth_info_all[t_config_obj[1]][t_config_obj[2]] = t_config_obj[3]
            else:
                auth_info_all[t_config_obj[1]] = dict()
                auth_info_all[t_config_obj[1]][t_config_obj[2]] = t_config_obj[3]
        return auth_info_all


class FinancesGroupPublic:
    def __init__(self, auth_info_public, data_base=None):
        self.auth_info = auth_info_public
        self.finance_public = Finances(self.auth_info['AWSAccessKeyId'],
                                       self.auth_info['SecretKey'],
                                       self.auth_info['SellerId'],
                                       self.auth_info['ShopSite'])
        self.db_conn = pymysql.connect(data_base['HOST'],
                                       data_base['USER'],
                                       data_base['PASSWORD'],
                                       data_base['NAME'],
                                       charset='utf8')

    def close_db_conn(self):
        try:
            if self.db_conn:
                self.db_conn.close()
        except Exception as ex:
            print ex
            logging.error('class  FinancesPublic close db connection failed!')
            logging.error('traceback.format_exc():\n%s' % traceback.format_exc())

    def update_shop_status_finance(self, auth_info_public, begin_time, end_time, status, remark):
        cursor = self.db_conn.cursor()
        sql_record_exists = "select  name from t_perf_amazon_refresh_status where name = '%s'" % auth_info_public['ShopName']
        cursor.execute(sql_record_exists)
        shop_exists_obj = cursor.fetchone()
        if shop_exists_obj is None or shop_exists_obj[0] is None:
            sql_insert = '''
                insert into t_perf_amazon_refresh_status
                  (name,
                   shop_name,
                   shop_site,
                   IP,
                   finance_refresh_begin_time,
                   finance_refresh_end_time,
                   finance_refresh_status,
                   finance_refresh_remark)
                values
                  ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')
                ''' % (auth_info_public['ShopName'],
                       auth_info_public['ShopName'][0:8],
                       auth_info_public['ShopSite'],
                       auth_info_public['ShopIP'],
                       begin_time,
                       end_time,
                       status,
                       remark)
            logging.debug(sql_insert)
            cursor.execute(sql_insert)
            cursor.execute('commit;')
        else:
            sql_update = '''
            update t_perf_amazon_refresh_status
               set finance_refresh_begin_time = '%s',
                   finance_refresh_end_time   = '%s',
                   finance_refresh_status     = '%s',
                   finance_refresh_remark     = '%s'
             where name = '%s'
            ''' % (begin_time,
                   end_time,
                   status,
                   remark,
                   auth_info_public['ShopName'])
            logging.debug(sql_update)
            cursor.execute(sql_update)
            cursor.execute('commit;')
        cursor.close()

    def get_finance_group_report(self, begin_time=None, end_time=None, next_token=None):
        finance_report = self.finance_public.list_financial_event_groups(created_after=begin_time, created_before=end_time, next_token=next_token)
        finance_report_dict = finance_report._response_dict
        logging.debug('get data raw:%s' % finance_report_dict)
        return finance_report_dict

    def finance_flow(self, begin_time, end_time=None):
        try:
            begin_time_status = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logging.debug('begin flow, begin_time: %s, end_time:%s' % (begin_time, end_time))
            finance_report_raw = self.get_finance_group_report(begin_time=begin_time, end_time=end_time)
            logging.debug('get data')

            # 报告是否分页返回
            next_token = None
            next_token_dict = finance_report_raw.get('ListFinancialEventGroupsResult').get('NextToken')
            if next_token_dict:
                next_token = next_token_dict.get('value')

            group_report = finance_report_raw.get('ListFinancialEventGroupsResult').get('FinancialEventGroupList').get('FinancialEventGroup')

            result_all = list()
            for report in group_report:
                result_each = dict()
                for key, val in report.items():
                    if isinstance(val, dict):
                        for val_key, val_val in val.items():
                            if val_key == 'value' and len(val) == 1:
                                result_each[key] = val_val
                            else:
                                if val_key != 'value':
                                    result_each[key + '_' + val_key] = val_val.get('value')
                result_each['shop_name'] = self.auth_info['ShopName']
                result_all.append(result_each)

            with self.db_conn.cursor() as cursor:
                sql_delete = 'delete from t_amazon_finance_group_record where shop_name ="%s" ' % self.auth_info['ShopName']
                cursor.execute(sql_delete)
                for each in result_all:
                    placeholders = ', '.join(['%s'] * len(each))
                    columns = ', '.join(each.keys())
                    insert_sql = "INSERT INTO t_amazon_finance_group_record (%s) VALUES (%s)" % (columns, placeholders)
                    cursor.execute(insert_sql, each.values())
            self.db_conn.commit()

            # while next_token:
            #     finance_report_raw = self.get_finance_report(next_token=next_token)
            #     next_token = None
            #     next_token_dict = finance_report_raw.get('ListFinancialEventsByNextTokenResult').get('NextToken')
            #     if next_token_dict:
            #         next_token = next_token_dict.get('value')
        except (MWSError, ConnectionError):  # 因MWS错误 或 链接错误 且重试次数不超过5次，重试；否则退出
            logging.error('traceback.format_exc():\n%s' % traceback.format_exc())
        except:
            logging.error('traceback.format_exc():\n%s' % traceback.format_exc())


if __name__ == '__main__':
    # 基础信息获取
    get_info_obj = GetLocalIPAndAuthInfo()
    # 获取VPS外网IP
    while True:
        try:
            try:
                local_ip = get_info_obj.get_out_ip(get_info_obj.get_real_url())
            except Exception as ex:
                from json import load
                from urllib2 import urlopen
                local_ip = load(urlopen('https://api.ipify.org/?format=json'))['ip']

            # 印度站160和201单独申请了后台调用API
            if local_ip is not None:
                if local_ip == '47.254.83.145':
                    local_ip = '210.16.103.56'  # 160
                elif local_ip == '47.251.3.95':
                    local_ip = '103.95.13.105'  # 201
                else:
                    pass
                print 'local ip is: %s' % local_ip
                logging.debug('local ip is: %s' % local_ip)
                break
        except Exception as e:
            print e
            local_ip = None

    # 获取该VPS上的店铺token信息，并做遍历
    auth_info_all = get_info_obj.get_auth_info_by_ip(local_ip)
    get_info_obj.close_db_conn()
    logging.debug('auth_info_all is: %s' % str(auth_info_all))
    for key, val in auth_info_all.items():
        auth_info = val
        logging.debug('auth_info now is: %s ' % str(auth_info))
        finace_obj = FinancesGroupPublic(auth_info, DATABASE)
        finace_obj.finance_flow(begin_time='2017-01-01')
