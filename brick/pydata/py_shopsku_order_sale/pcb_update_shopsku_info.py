# coding=utf-8

# import csv
# import time
# import codecs
# import pymssql

import MySQLdb
import commands
import datetime
import subprocess

DATABASES = {
    'mysql': {
        'PORT': 3306,
        'NAME': 'py_db',
        'HOST': 'hequskuapp.mysql.rds.aliyuncs.com',
        'USER': 'by15161458383',
        'PASSWORD': 'K120Esc1',
    },
    'sqlserver': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ShopElf',
        'HOST': '122.226.216.10',
        'PORT': '18793',
        'USER': 'fancyqube',
        'PASSWORD': 'K120Esc1'
    },
}


class syn_bcp_method():
    def __init__(self):
        self.db_conn = MySQLdb.connect(
            user=DATABASES['mysql']['USER'],
            passwd=DATABASES['mysql']['PASSWORD'],
            host=DATABASES['mysql']['HOST'],
            db=DATABASES['mysql']['NAME'],
            port=DATABASES['mysql']['PORT'],
            charset='utf8'
        )

    def close_mysql(self):
        self.db_conn.close()

    def load_data_to_mysql(self, table, pysql):
        try:
            beginTime = datetime.datetime.now()
            print "Begin Time:", beginTime

            cur = self.db_conn.cursor()
            BCPout = "/opt/mssql-tools/bin/bcp '%s' queryout /bcpOnline/createfile/%s.csv -w -t '{<}' -r '{>}' -U %s -P %s -S %s,%s -k" \
                % (pysql, table, DATABASES['sqlserver']['USER'], DATABASES['sqlserver']['PASSWORD'], DATABASES['sqlserver']['HOST'], DATABASES['sqlserver']['PORT'])

            result_code = subprocess.call(BCPout, shell=True)
            print(result_code)

            commands.getoutput(('iconv -f UTF-16 -t UTF-8 /bcpOnline/createfile/%s.csv > /bcpOnline/createfile/%s_utf8.csv' % (table, table)))
            commands.getoutput(("sed -i 's/\\\\/\\\\\\\\/g' /bcpOnline/createfile/%s_utf8.csv" % table))

            onlinesql = 'truncate table %s' % table
            cur.execute(onlinesql)
            cur.execute('commit')

            loadsql = 'LOAD DATA LOCAL INFILE "/bcpOnline/createfile/%s_utf8.csv" INTO TABLE %s fields terminated by "{<}" lines terminated by "{>}"' % (table, table)
            cur.execute(loadsql)
            cur.execute('commit')
            cur.close()

            endTime = datetime.datetime.now()
            print "End Time:", endTime
            print 'cost time: %f s' % (endTime - beginTime).seconds
        except Exception, e:
            print repr(e)

if __name__ == '__main__':
    py_bcp = syn_bcp_method()

    tablem = 'py_shopsku_info'

    sqlm = "SELECT row_number () OVER (ORDER BY a.sku ASC) AS id, CONVERT(VARCHAR(10), b.ordertime, 120) AS orderday, b.suffix, " \
        "a.ebaysku AS shopsku, a.sku, COUNT(b.nid) AS ordernum, SUM(a.l_qty) AS skusales, CONVERT(varchar,GETDATE(),20) AS NowDate " \
        "FROM ShopElf.dbo.P_TradeDt a INNER JOIN ShopElf.dbo.P_Trade b ON b.nid = a.tradenid GROUP BY CONVERT(varchar(10), b.ordertime, 120), " \
        "b.suffix, a.ebaysku, a.sku;"

    py_bcp.load_data_to_mysql(tablem, sqlm)

    py_bcp.close_mysql()
