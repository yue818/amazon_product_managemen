# -*- coding: utf-8 -*-


# import time
import MySQLdb
import sys
import traceback

DATABASES = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'hq_db',
    'HOST': 'rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com',
    'PORT': '3306',
    'USER': 'by15161458383',
    'PASSWORD': 'K120Esc1',
    'CHARSET': 'utf8'
}


# -*- coding: utf-8 -*-
# params  是一个字典
# result 也是一个字典
def run(params):
    print 'dbconnect::run in params=%s' % params
    result = {}

    try:
        db_conn = MySQLdb.connect(DATABASES['HOST'], DATABASES['USER'], DATABASES['PASSWORD'], DATABASES['NAME'], charset=DATABASES['CHARSET'])
        result['db_conn'] = db_conn
        result['errorcode'] = 0
        print 'dbconnect::run out params' % params
        return result
    except MySQLdb.Error, e:
        result['errorcode'] = -1
        result['errortext'] = "MySQL Error:%s" % str(e)
        # time.sleep(2)
    except Exception, ex:
        result['errorcode'] = -1
        result['errortext'] = '%s:Exception = %s ex=%s  __LINE__=%s' % (traceback.print_exc(), Exception, ex, sys._getframe().f_lineno)
        # time.sleep(2)
    print 'dbconnect::run out params' % params
    return result


DATABASES2 = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'hq_db_test2',
    'HOST': 'rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com',
    'PORT': '3306',
    'USER': 'by15161458383',
    'PASSWORD': 'K120Esc1',
    'CHARSET': 'utf8'
}


# -*- coding: utf-8 -*-
# params  是一个字典
# result 也是一个字典
def run2(params):
    print 'dbconnect::run in params=%s' % params
    result = {}

    try:
        db_conn = MySQLdb.connect(DATABASES2['HOST'], DATABASES2['USER'], DATABASES2['PASSWORD'], DATABASES2['NAME'], charset=DATABASES2['CHARSET'])
        result['db_conn'] = db_conn
        result['errorcode'] = 0
        print 'dbconnect::run out params' % params
        return result
    except MySQLdb.Error, e:
        result['errorcode'] = -1
        result['errortext'] = "MySQL Error:%s" % str(e)
        # time.sleep(2)
    except Exception, ex:
        result['errorcode'] = -1
        result['errortext'] = '%s:Exception = %s ex=%s  __LINE__=%s' % (traceback.print_exc(), Exception, ex, sys._getframe().f_lineno)
        # time.sleep(2)
    print 'dbconnect::run out params' % params
    return result


# Execute sql
def execute_db(sql, db_conn, option, params=None):
    cursor = db_conn.cursor()
    if option == 'select':
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        columns = cursor.description
        result = []
        for value in cursor.fetchall():
            tmp = {}
            for (index, column) in enumerate(value):
                tmp[columns[index][0]] = column
            result.append(tmp)
    elif option == 'update' or option == 'insert' or option == 'delete':
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        cursor.execute("commit;")
        result = {'code': 0, 'message': ''}
    else:
        result = {'code': 1, 'message': 'Please choose an option from select or insert or udpate or delete.'}
    cursor.close()
    return result
