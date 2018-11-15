# coding=utf-8

import MySQLdb,sys,urllib,shutil
import time
import os
import oss2
import xlrd
from datetime import datetime
import traceback
reload(sys)
sys.setdefaultencoding('utf8')

def daemonize(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    # 重定向标准文件描述符（默认情况下定向到/dev/null）
    try:
        pid = os.fork()
        # 父进程(会话组头领进程)退出，这意味着一个非会话组头领进程永远不能重新获得控制终端。
        if pid > 0:
            sys.exit(0)  # 父进程退出
    except OSError, e:
        sys.stderr.write("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)

        # 从母体环境脱离
    os.chdir("/")  # chdir确认进程不保持任何目录于使用状态，否则不能umount一个文件系统。也可以改变到对于守护程序运行重要的文件所在目录
    os.umask(0)  # 调用umask(0)以便拥有对于写的任何东西的完全控制，因为有时不知道继承了什么样的umask。
    os.setsid()  # setsid调用成功后，进程成为新的会话组长和新的进程组长，并与原来的登录会话和进程组脱离。

    # 执行第二次fork
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)  # 第二个父进程退出
    except OSError, e:
        sys.stderr.write("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)

        # 进程已经是守护进程了，重定向标准文件描述符

    for f in sys.stdout, sys.stderr: f.flush()
    si = open(stdin, 'r')
    so = open(stdout, 'a+')
    se = open(stderr, 'a+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())  # dup2函数原子化关闭和复制文件描述符
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

PREFIX = 'http://'
ACCESS_KEY_ID = 'LTAIH6IHuMj6Fq2h'
ACCESS_KEY_SECRET = 'N5eWsbw8qBkMfPREkgF2JnTsDASelM'
# ENDPOINT = 'vpc100-oss-cn-shanghai.aliyuncs.com'
ENDPOINT_OUT = 'oss-cn-shanghai.aliyuncs.com'
BUCKETNAME_pic = 'fancyqube-all-mainsku-pic'
BUCKETNAME_xls = 'fancyqube-upload-xls'


def connnect2Mysql():
    """连接MySQL数据库"""
    HOST = 'hequskuapp.mysql.rds.aliyuncs.com'
    PORT = 3306
    USER = 'by15161458383'
    PASSWORD = 'K120Esc1'
    DB = 'hq_db_test2'
    # HOST = '192.168.105.111'
    # PORT = 3306
    # USER = 'root'
    # # by15161458383
    # PASSWORD = 'root123'
    # DB = 'hq'
    CHARSET = 'utf8'
    try:
        mysqlClient = MySQLdb.connect(host=HOST, port=PORT, user=USER, passwd=PASSWORD, db=DB, charset=CHARSET)
    except MySQLdb.Error, e:
        print 'MySQL Error:%s，30秒后重新连接……' % str(e)
        time.sleep(30)
        connnect2Mysql()
    return mysqlClient


from brick.ebay.ebay_column import insertdictk
from brick.function.get_time_stamp import get_time_stamp as get_time
from brick.ebay.read_excel import read_excel
from brick.ebay.get_pic import get_pic




def selectFromMySQL(client):
    """从数据库查询待入库的zip文件地址"""
    cur = client.cursor()
    sql = ' select ExcelFile, CreateTime, CreateStaff, UpdateStaff, OssUrl, id from t_templet_ebay_collection_box WHERE Status="OPEN" '
    cur.execute(sql)
    info = cur.fetchall()
    cur.close()
    return info

def downloadXls2Local(url, bucket_xls):
    """下载xls文件到本地"""
    filePath = '/tmp/xlseBay'
    xlsPath = filePath + '/xlsTemp.xls'
    # xlsPath = 'C:/Users/Administrator/Desktop/temp/xlsTmp/xlsTemp.xls'

    if os.path.exists(xlsPath):
        os.remove(xlsPath)
    if not os.path.exists(filePath):
        # os.mkdir(file_path)
        os.makedirs(filePath)

    bucket_xls.get_object_to_file(url, xlsPath)
    return xlsPath






def upload_img(bucket_pic, img_urls, userName, img_names):
    for i in range(len(img_urls)):
        try:
            print '***************************************%s*******************************************************'%i
            print img_urls[i]
            fileDir = userName + img_urls[i].replace('/tmp/piceBay', '')
            print fileDir
            print img_names[i]
            bucket_pic.put_object(u'%s' % (fileDir), open(img_urls[i]))
        except:
            picUrl = 'https://i.ebayimg.com' + img_urls[i].replace('/tmp/piceBay', '')
            get_pic(picUrl)
            bucket_pic.put_object(u'%s' % (fileDir), open(img_urls[i]))
            traceback.print_exc()

def main(client, bucket_xls, bucket_pic):
    info = selectFromMySQL(client)
    print info
    for each in info:
        url = each[4]
        userName = url.split('/')[0]
        filePath = downloadXls2Local(url, bucket_xls)
        img_urls, img_names = read_excel(each, filePath, client)
        upload_img(bucket_pic, img_urls, userName, img_names)


daemonize('/dev/null','/tmp/ebay_open_print.log','/tmp/ebay_open_error.log')
if __name__ == "__main__":
    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
    bucket_xls = oss2.Bucket(auth, ENDPOINT_OUT, BUCKETNAME_xls)
    # print bucket_xls
    bucket_pic = oss2.Bucket(auth, ENDPOINT_OUT, BUCKETNAME_pic)
    while True:
        try:
            client = connnect2Mysql()
            main(client, bucket_xls, bucket_pic)
        except Exception, e:
            print '%s' % get_time(), e
            traceback.print_exc()

        client.close()
        print '%s' % get_time(), 'The next plan will be executed in 60 seconds ......'
        time.sleep(60)