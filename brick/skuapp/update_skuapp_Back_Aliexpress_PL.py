# -*- coding: utf-8 -*-

import urllib
import time
import datetime
import json
from bs4 import BeautifulSoup
import MySQLdb
import sys
sys.path.append('../../')
from Project.settings import DATABASES
  

def get_data():
    start_time = datetime.datetime.now()
    print 'start time: %s' % start_time
    host = DATABASES['default']['HOST']
    user = DATABASES['default']['USER']
    passwd = DATABASES['default']['PASSWORD']
    db = DATABASES['default']['NAME']
    port = DATABASES['default']['PORT']
    conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, port=3306, charset='utf8')
    cur = conn.cursor()
    sql = "select id, SourceURL, SourceURL2 from t_product_enter_ed where SourceURL like '%aliexpress%' or SourceURL2 like '%aliexpress%';"
    cur.execute(sql)
    data = cur.fetchall()
    sql2 = "select * from t_aliexpress_categories_LargeClass;"
    cur.execute(sql2)
    class_data = cur.fetchall()
    c_data = {}
    for c_d in class_data:
        c_data[c_d[2]] = c_d[1]
    for d in data:
        url = ''
        if d[1] and 'aliexpress' in d[1]:
            url = d[1]
        if d[2] and  'aliexpress' in d[2]:
            url = d[2]
        if url:
            try:
                page = urllib.urlopen(url)
            except:
                time.sleep(5)
                page = urllib.urlopen(url)
            htmlcode = page.read()
            soup = BeautifulSoup(htmlcode, 'html.parser')
            try:
                data_url = soup.select('.ui-breadcrumb')[0]
            except:
                data_url = ''
            if data_url:
                Back_Aliexpress_PL = ''
                try:
                    if data_url.findAll('a')[0].get_text() == 'Home' and data_url.findAll('a')[1].get_text() == 'All Categories':
                        english_name = data_url.findAll('a')[2].get_text()
                        english_name2 = data_url.findAll('a')[3].get_text()
                        if english_name2 == 'Electronic Cigarettes':
                            if english_name == 'Consumer Electronics':
                                Back_Aliexpress_PL = c_data[english_name2]
                            else:
                                Back_Aliexpress_PL = c_data[english_name]
                        elif english_name:
                            Back_Aliexpress_PL = c_data[english_name]
                        if Back_Aliexpress_PL:
                            sql3 = 'update t_product_enter_ed set Back_Aliexpress_PL="%s" where id=%s' % (Back_Aliexpress_PL, d[0])
                            try:
                                print url
                                cur.execute(sql3)
                                conn.commit()
                            except Exception as e:
                                print repr(e)
                                conn.rollback()
                except Exception as e:
                    print url
                    print repr(e)
                    continue
    conn.close()
    end_time = datetime.datetime.now()
    print 'end time: %s' % end_time
    handle_time = (end_time - start_time).total_seconds()
    print 'handle time: %s' % handle_time


if __name__ == "__main__":
    get_data()
