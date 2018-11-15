#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Time    : 2018-08-20 10:45
@Author  : chenchen
@Site    : lazada
@File    : get_token_info.py
@Software: PyCharm
'''

import lazop
import MySQLdb

class get_token_info():
    def __init__(self,ip,appkey,appSecret):
        self.url = 'http://%s:9193/fancyqube/auth.lazada.com/rest'%ip
        self.appkey = appkey
        self.appSecret = appSecret

    def get_access_token(self, code):
        client = lazop.LazopClient(self.url, self.appkey, self.appSecret)
        request = lazop.LazopRequest('/auth/token/create')
        request.add_api_param('code', '%s'%code)
        response = client.execute(request)
        token_info = {}
        print response.body
        if response.code == '0':
            token_info['access_token'] = response.body['access_token']
            token_info['refresh_token'] = response.body['refresh_token']
        return token_info
        #{'access_token': u'50000402033YH7q5K0wiJDKIamtzBk4GOshvvaquQz1iP1b43f1b8CNFTUk5kr', 'refresh_token': u'50001401c33bXLdYBjs9ORuEKmMnxly0jg3kvTbSSzvPN11b7c02dW2jcCIPVu'} 7天

    def get_refresh_token(self, refresh_token):
        client = lazop.LazopClient(self.url, self.appkey, self.appSecret)
        request = lazop.LazopRequest('/auth/token/refresh')
        request.add_api_param('refresh_token', refresh_token)
        response = client.execute(request)
        print response.body
        token_info = {}
        if response.code == '0':
            token_info['access_token'] = response.body['access_token']
            token_info['refresh_token'] = response.body['refresh_token']
        print 'token信息已刷新'
        return token_info
        #{'access_token': u'50000400b34fWdiBN4pvD8zHYlkwbzwk6fhRAPs2GjjxHW192d2237kVgkelyp', 'refresh_token': u'50001400a34MJN7jjwysT9ZaK2forhzwCaiCwil0XglHuH1a5da3e82IeTBRm9'} 13.9天

if __name__ == '__main__':
    conn = MySQLdb.connect(host='rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com', user='by15161458383', passwd='K120Esc1',
                           db='hq_db', port=3306,
                           charset='utf8')
    cur = conn.cursor()
    cur2 = conn.cursor()

    # cur.execute('SELECT ip,appkey,appsecret,code,site FROM t_config_online_lazada WHERE access_token is NULL ')
    # print ('阿里数据库连接成功！')
    # rows = cur.fetchall()
    # for row in rows:
    #     token_info = get_token_info(str(row[0]),str(row[1]),str(row[2])).get_access_token(str(row[3]))
    #     print row[0],row[1],row[2],row[3],row[4]
    #     sql = 'update t_config_online_lazada set access_token = "%s",refresh_token = "%s" WHERE ip = "%s" AND site = "%s" '%(token_info['access_token'],token_info['refresh_token'],str(row[0]),str(row[4]))
    #     cur2.execute(sql)
    #     cur2.execute('commit;')
    #     print 'success'

    cur.execute('SELECT ip,appkey,appsecret,refresh_token,site FROM t_config_online_lazada WHERE access_token is NOT NULL')
    print ('阿里数据库连接成功！')
    rows = cur.fetchall()
    count = 1
    for row in rows:
        token_info = get_token_info(str(row[0].strip()),str(row[1].strip()),str(row[2].strip())).get_refresh_token(str(row[3].strip()))
        sql = 'update t_config_online_lazada set access_token = "%s",refresh_token = "%s" WHERE ip = "%s" AND site = "%s" ' % (token_info['access_token'], token_info['refresh_token'], str(row[0]), str(row[4]))
        cur2.execute(sql)
        cur2.execute('commit;')
        count += 1
        print 'ip:%s----%s'%(row[0],count)
    print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>全部完成刷新token信息！'

    cur.close()
    cur2.close()
    conn.close()

    # client = lazop.LazopClient('http://139.196.37.211:9193/fancyqube/auth.lazada.com/rest','105915','YAj2ZoCon0h412jXD4pLBTlzsfwQMV6k')
    # request = lazop.LazopRequest('/auth/token/create')
    # request.add_api_param('code', '0_105915_y1AE6OVoMJwI82Tjb8IslxLi3881')
    # response = client.execute(request)
    # print response.body