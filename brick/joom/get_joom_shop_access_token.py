# coding: utf-8
"""
@author: wangzy, sunjian
@contact: 15205512335
@site:
@software: PyCharm
@说明: 将joom申请api涉及信息导入表中
@time: 2018-01-23 15:21
"""

# Get Authorize Code
# https://merchant.joom.com/oauth/authorize?oauth_client_id=an_example_client_id

# Test Authentication
# https://api-merchant.joom.com/api/v2/auth_test?access_token=an_example_access_token

import MySQLdb
import ConfigParser
from bs4 import BeautifulSoup
import requests

DATABASES = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'hq_db',
    'HOST': 'rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com',
    'PORT': '3306',
    'USER': 'by15161458383',
    'PASSWORD': 'K120Esc1'
}

db_conn = MySQLdb.Connect(DATABASES['HOST'], DATABASES['USER'], DATABASES['PASSWORD'], DATABASES['NAME'], charset='utf8')
sqlcursor = db_conn.cursor()


def closeSql():
    '''
    说明：如果本地数据库连接，需要关闭数据库
    '''
    sqlcursor.close()
    db_conn.close()


def Insert_T_Config_Online_Joom(id, ip, shopname, client_secret, client_id, access_token, refresh_token):
    select_info = "SELECT id FROM t_config_online_joom WHERE ShopName='%s'" % shopname
    res = sqlcursor.execute(select_info)
    if res:
        return
    strInsertSql = "INSERT INTO t_config_online_joom  VALUES(NULL,'" + ip + "','" + shopname + "','PlatformName','Joom'" + ")"
    strInsertSql_1 = "INSERT INTO t_config_online_joom  VALUES(NULL,'" + ip + "','" + shopname + "','client_secret','" + client_secret + "')"
    strInsertSql_2 = "INSERT INTO t_config_online_joom  VALUES(NULL,'" + ip + "','" + shopname + "','client_id','" + client_id + "')"
    strInsertSql_3 = "INSERT INTO t_config_online_joom  VALUES(NULL,'" + ip + "','" + shopname + "','access_token','" + access_token + "')"
    strInsertSql_4 = "INSERT INTO t_config_online_joom  VALUES(NULL,'" + ip + "','" + shopname + "','refresh_token','" + refresh_token + "')"
    sqlcursor.execute(strInsertSql)  # 执行sql语句
    sqlcursor.execute(strInsertSql_1)  # 执行sql语句
    sqlcursor.execute(strInsertSql_2)  # 执行sql语句
    sqlcursor.execute(strInsertSql_3)  # 执行sql语句
    sqlcursor.execute(strInsertSql_4)  # 执行sql语句
    db_conn.commit()


def execute_db(sql):
    sqlcursor.execute(sql)
    columns = sqlcursor.description
    result = []
    for value in sqlcursor.fetchall():
        tmp = {}
        for (index, column) in enumerate(value):
            tmp[columns[index][0]] = column
        result.append(tmp)

    return result


def get_shopnames():
    shopnames_sql = "SELECT ShopName FROM t_store_configuration_file WHERE ShopName LIKE 'JOOM-%';"
    res = execute_db(shopnames_sql)
    shopnames = list()
    for i in res:
        shopnames.append(i['ShopName'])
    return shopnames


def get_out_ip(url):
    r = requests.get(url)
    txt = r.text
    ip = txt[txt.find("[") + 1: txt.find("]")]
    print('ip:' + ip)
    return ip


def get_real_url(url=r'http://www.ip138.com/'):
    r = requests.get(url)
    txt = r.text
    soup = BeautifulSoup(txt, "html.parser").iframe
    return soup["src"]


if __name__ == "__main__":
    # sArrayJoom = [
    #     'JOOM-0002-01-HedongCloth/YW', 'JOOM-0002-02-bl/YW', 'JOOM-0002-03-Gadget/YW', 'JOOM-0002-04-BabyToy/YW',
    #     'JOOM-0002-05-WomenBeauty/YW', 'JOOM-0002-06-CoolBag/YW', 'JOOM-0002-07-BDDecor/YW', 'JOOM-0002-08-Shine/YW', 'JOOM-0002-09-Memo/YW',
    #     'JOOM-0002-10-Liberty/YW', 'JOOM-0002-11-Thunder/YW', 'JOOM-0002-12-Fire/YW', 'JOOM-0002-14-Grace/YW', 'JOOM-0002-15-Cheirsh/YW',
    #     'JOOM-0002-13-Destiny/YW', 'JOOM-0002-16-Cosy/YW', 'JOOM-0002-17-Diana/YW', 'JOOM-0002-18-Pretty/YW', 'JOOM-0002-19-NiceMelody/YW',
    #     'JOOM-0002-20-NiceGirl/YW', 'JOOM-0002-21-Believe/YW', 'JOOM-0002-22-Sweetness/YW', 'JOOM-0002-23-ThisGirl/YW',
    #     'JOOM-0002-24-ThatGirl/YW', 'JOOM-0002-25-Teenager/YW', 'JOOM-0002-26-GaGa/YW', 'JOOM-0002-27-NeverMore/YW',
    #     'JOOM-0002-28-RealLove/YW', 'JOOM-0002-29-Kaer/YW', 'JOOM-0002-30-Slark/YW', 'JOOM-0002-31-Whites/YW', 'JOOM-0002-32-Halo/YW',
    #     'JOOM-0002-33-Cherry/YW', 'JOOM-0002-34-Kindy/YW', 'JOOM-0002-35-Parrot/YW', 'JOOM-0003-01-BeautyMakeup/YW',
    #     'JOOM-0003-02-HealthandBeauty/YW', 'JOOM-0003-03-nicewatch/YW', 'JOOM-0003-04-wallart/YW', 'JOOM-0003-05-beautifuljewellery/YW',
    #     'JOOM-0003-06-fineaccessories/YW', 'JOOM-0003-07-niceornaments/YW', 'JOOM-0003-08-Fashionhomedecoration/YW',
    #     'JOOM-0003-09-SpecialClothes/YW', 'JOOM-0003-10-trendaccessories/YW', 'JOOM-0003-11-noveltyproduct/YW',
    #     'JOOM-0003-12-womenbeautifulclothes/YW', 'JOOM-0003-13-funtoys/YW', 'JOOM-0003-14-trendbags/YW', 'JOOM-0003-15-babyappliance/YW',
    #     'JOOM-0003-16-Electronicgoods/YW', 'JOOM-0003-17-specialphoneaccessories/YW', 'JOOM-0003-18-carsupplies/YW', 'JOOM-0003-19-homedesign/YW',
    #     'JOOM-0003-20-adornmentaccessories/YW', 'JOOM-0003-21-officenecessities/YW', 'JOOM-0003-22-sportsupplies/YW',
    #     'JOOM-0003-23-specialornament/YW', 'JOOM-0003-24-housedecoration/YW', 'JOOM-0003-25-colorfulwearing/YW', 'JOOM-0003-26-fashionclothing/YW',
    #     'JOOM-0003-27-varietygoods/YW', 'JOOM-0003-28-nicewomenclothes/YW', 'JOOM-0003-29-specialtoys/YW', 'JOOM-0003-30-homecreative/YW',
    #     'JOOM-0003-31-womenmakeup/YW', 'JOOM-0003-32-mentrend/YW', 'JOOM-0003-33-ladyornament/YW', 'JOOM-0003-34-sportsandfitness/YW',
    #     'JOOM-0003-35-Battle/YW', 'JOOM-0003-36-Grocery/YW']

    realIP = get_out_ip(get_real_url())

    sArrayJoom = get_shopnames()

    cf = ConfigParser.ConfigParser()
    cf.read("joom_shopnames.conf")

    sUrl = ""
    sClientID = ""
    sClientSCR = ""
    sCode = ""
    sAccess_Token = ""
    sRefresh_Token = ""
    shopName = ""
    for sRow in sArrayJoom:
        if sRow.startswith('JOOM-0002'):
            shop_ip = '119.23.144.25'
            if realIP != shop_ip:
                continue
            print 'sRow: ', sRow
        elif sRow.startswith('JOOM-0003'):
            shop_ip = '114.115.161.21'
            if realIP != shop_ip:
                continue
            print 'sRow: ', sRow
        elif sRow.startswith('JOOM-0004'):
            shop_ip = '121.43.198.134'
            if realIP != shop_ip:
                continue
            print 'sRow: ', sRow
        elif sRow.startswith('JOOM-0005'):
            shop_ip = '120.26.7.212'
            if realIP != shop_ip:
                continue
            print 'sRow: ', sRow
        elif sRow.startswith('JOOM-0006'):
            shop_ip = '115.29.213.208'
            if realIP != shop_ip:
                continue
            print 'sRow: ', sRow
        elif sRow.startswith('JOOM-0007'):
            shop_ip = '120.76.171.177'
            if realIP != shop_ip:
                continue
            print 'sRow: ', sRow
        elif sRow.startswith('JOOM-0008'):
            shop_ip = '120.76.118.141'
            if realIP != shop_ip:
                continue
            print 'sRow: ', sRow
        elif sRow.startswith('JOOM-0009'):
            shop_ip = '121.41.52.241'
            if realIP != shop_ip:
                continue
            print 'sRow: ', sRow
        elif sRow.startswith('JOOM-0001'):
            shop_ip = 'joom_1_local_ip'
            print 'sRow: ', sRow
        else:
            continue
        strJoomNameSql = "SELECT ShopName FROM t_store_configuration_file WHERE ShopName='" + sRow + "';"
        n = sqlcursor.execute(strJoomNameSql)
        sArray = sqlcursor.fetchall()
        if len(sArray) == 0:
            print("t_store_configuration_file 表里不存在：{}".format(sRow))
        else:
            shopName = sArray[0][0]
        if cf.has_section(sRow):
            sUrl = cf.get(sRow, "url")
            print 'sUrl', sUrl
            sClientID = cf.get(sRow, "clientID")
            print 'sClientID', sClientID
            sClientSCR = cf.get(sRow, "clientSCR")
            print 'sClientSCR', sClientSCR
            sCode = cf.get(sRow, "code")
            print 'sCode', sCode
        else:
            print 'This config file has no %s section' % sRow
            continue

        url = 'https://api-merchant.joom.com/api/v2/oauth/access_token'
        params = {
            'client_id': sClientID,
            'client_secret': sClientSCR,
            'code': sCode,
            'redirect_uri': 'https://merchant.joom.it',
            'grant_type': 'authorization_code',
        }
        ret_token = requests.post(url, params=params, timeout=60)
        result_code = eval(ret_token._content.replace(':null,', ':0,'))
        print 'ret_token', ret_token
        print 'result_code', result_code
        print ("sUrl={},sClientID={},sClientSCR={},sCode={},sAccess_Token={},sRefresh_Token={}".format(sUrl, sClientID, sClientSCR, sCode, result_code.get('data').get('access_token'), result_code.get('data').get('refresh_token')))
        Insert_T_Config_Online_Joom(0, shop_ip, sRow, sClientSCR, sClientID, result_code.get('data').get('access_token'), result_code.get('data').get('refresh_token'))
    closeSql()
