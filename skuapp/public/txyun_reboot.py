#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
#=============================================================================
#
#     FileName: QcloudSign.py
#         Desc: 腾讯云 api 联调工具
#
#       Author: gavinyao
#        Email: gavinyao@tencent.com
#
#      Created: 2014-08-19 15:40:02
#      Version: 0.0.1
#      History:
#               0.0.1 | gavinyao | 2014-08-19 15:40:02 | initialization
#
#=============================================================================*/
'''
import sys  
  
reload(sys)  
sys.setdefaultencoding('utf8')

import urllib
import urllib2
import httplib
import binascii
import hashlib
import hmac
import time
import random
import sys
import json
import MySQLdb
##
# @brief 拼出签名字符串原文
# @author gavinyao@tencent.com
# @date 2014-08-20 12:25:14
#
# @param requestMethod
# @param requestHost
# @param requestPath
# @param params
#
# @return
def makePlainText(requestMethod, requestHost, requestPath, params):
    str_params = "&".join(k + "=" + str(params[k]) for k in sorted(params.keys()))

    source = '%s%s%s?%s' % (
            requestMethod.upper(),
            requestHost,
            requestPath,
            str_params
            )
    return source

##
# @brief 签名
# @author gavinyao@tencent.com
# @date 2014-08-20 12:24:53
#
# @param requestMethod 请求方法 POST/GET
# @param requestHost 请求主机
# @param requestPath 请求路径
# @param params 请求参数
# @param secretKey
#
# @return

def sign(requestMethod, requestHost, requestPath, params, secretKey):
    source = makePlainText(requestMethod, requestHost, requestPath, params)
    hashed = hmac.new(secretKey, source, hashlib.sha1)
    return binascii.b2a_base64(hashed.digest())[:-1]


def main(YOUR_SECRET_KEY,YOUR_PARAMS):
    # secretId 和 secretKey
    #secretId = YOUR_SECRET_ID
    secretKey = YOUR_SECRET_KEY

    requestMethod = 'POST'
    requestHost = 'cvm.api.qcloud.com'
    requestPath = '/v2/index.php'

    # 请求参数

    params=YOUR_PARAMS
    plainText = makePlainText(requestMethod, requestHost, requestPath, params)
    signText = sign(requestMethod, requestHost, requestPath, params, secretKey)
    #print "原文:%s" % plainText
    #print "签名:%s" % signText

    params['Signature'] = signText

    headers = {"Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/plain"}

    # 发送请求
    httpsConn = None
    try:
        httpsConn = httplib.HTTPSConnection(host = requestHost, port = 443)
        if requestMethod == "GET":
            params['Signature'] = urllib.quote(signText)

            str_params = "&".join(k + "=" + str(params[k]) for k in sorted(params.keys()))
            url =  'https://%s%s?%s' % (requestHost, requestPath, str_params)
            httpsConn.request("GET", url)
        elif requestMethod == "POST":
            params = urllib.urlencode(params)
            httpsConn.request("POST", requestPath, params, headers)

        response = httpsConn.getresponse()
        data = response.read()
        # print data
        jsonRet = json.loads(data)
        #print json.dumps(jsonRet, indent = 4, ensure_ascii=False)
        return json.dumps(jsonRet, indent = 4, ensure_ascii=False)

    except Exception, e:
        print e
    finally:
        if httpsConn:
            httpsConn.close()

if __name__ == '__main__':
    SecretId='AKIDJWaWGsByFRVN3Wo7NX9apskRXYROoSXY'
    regions=['ap-guangzhou','ap-shenzhen-fsi','ap-shanghai','ap-shanghai-fsi','ap-beijing',]
    #regions=['ap-shanghai',]
    for region in regions:
        YOUR_PARAMS = {
                'SecretId': SecretId,
                'Timestamp': int(time.time()),
                'Nonce': random.randint(1, sys.maxint),
                'Region': region,
                'Action': 'DescribeInstances',
                'Limit':100,
                'Version':'2017-03-12'
                }
        #main('c7eBvePFzjVKA4naOC0kWJ6seQBriaTE',YOUR_PARAMS)
        content=main('c7eBvePFzjVKA4naOC0kWJ6seQBriaTE',YOUR_PARAMS)
        #print content

        if content is not None:
            null=''
            false=''
            content=eval(content)
            
            if content["Response"].has_key("InstanceSet"):
                for lis in content["Response"]['InstanceSet']:
                    regionId=lis['Placement']['Zone']
                    instanceId=lis['InstanceId']
                    ipAddress=lis['PublicIpAddresses'][0]
                    cnxn = MySQLdb.connect('hequskuapp.mysql.rds.aliyuncs.com','by15161458383','K120Esc1','hq_db' )
                    cursor =cnxn.cursor();
                    sql = "update t_config_mstsc set  RegionId='%s',InstanceId='%s',CloudName='tengxunyun' where ip='%s'"%(region,instanceId,ipAddress)
                    #sql = "update t_config_mstsc set  RegionId='%s',InstanceId='%s' where ip='%s'"%(regionId,instanceId,ipAddress[0])
                    #sql='update t_config_mstsc set  RegionId="cn-qingdao",InstanceId="i-m5eijiwzg03cxwhz3lti" where ip="10.29.168.221"'
                    cursor.execute(sql)
                    cursor.execute('commit')
            #lis['wanIpSet'] lis['instanceId'] lis['Region']
            
    #content=main('AKIDJWaWGsByFRVN3Wo7NX9apskRXYROoSXY','c7eBvePFzjVKA4naOC0kWJ6seQBriaTE')
'''
if __name__ == '__main__':
    SecretId='AKIDJWaWGsByFRVN3Wo7NX9apskRXYROoSXY'
    #regions=['ap-guangzhou','ap-shenzhen-fsi','ap-shanghai','ap-shanghai-fsi','ap-beijing',]
    regions=['ap-beijing',]
    for region in regions:
        YOUR_PARAMS = {
                'SecretId': SecretId,
                'Timestamp': int(time.time()),
                'Nonce': random.randint(1, sys.maxint),
                'Region': region,
                'Action': 'DescribeInstancesStatus',
                'Limit':100,
                'InstanceIds.0':'ins-jn6dgo7d',
                'Version':'2017-03-12'
                }
        #main('c7eBvePFzjVKA4naOC0kWJ6seQBriaTE',YOUR_PARAMS)
        content=main('c7eBvePFzjVKA4naOC0kWJ6seQBriaTE',YOUR_PARAMS)
        print content
        content['Response']['InstanceSet'][0]['InstanceState']
        #content['Response']['InstanceSet'][0]['CreatedTime']
        #content['Response']['InstanceSet'][0]['ExpiredTime']
            
    #content=main('AKIDJWaWGsByFRVN3Wo7NX9apskRXYROoSXY','c7eBvePFzjVKA4naOC0kWJ6seQBriaTE')
'''
