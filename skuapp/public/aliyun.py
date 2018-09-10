# coding=utf-8
"""
__created__ =  2017/6/9 17:33
__author__ = 'baishaohua'
# @Site    : https://github.com/bashhu
"""


import os, sys
import hashlib
import hmac
import base64
import urllib
import time
import uuid
import requests
import MySQLdb

def get_iso8601_time():
    '''返回iso8601格式的时间'''
    TIME_ZONE = "GMT"
    FORMAT_ISO8601 = "%Y-%m-%dT%H:%M:%SZ"
    return time.strftime(FORMAT_ISO8601, time.gmtime())


def get_uuid():
    '''返回uuid'''
    return str(uuid.uuid4())


def get_parameters(user_param, Action, AccessKeyId, Version):
    '''
    拼接参数字典
    user_param: {"RegionId":"cn-beijing", "LoadBalancerName":"test-node1", "AddressType":"intranet", "VSwitchId":"vsw-2zevjlczuvp2mkhhch12x"}
    Action操作例如:CreateLoadBalancer
    AccessKeyId：access key ID
    Version: 接口的版本
    '''
    parameters = {}
    parameters['HTTPMethod'] = 'GET'
    parameters['AccessKeyId'] = AccessKeyId
    parameters['Format'] = 'json'
    parameters['Version'] = Version
    parameters['SignatureMethod'] = 'HMAC-SHA1'
    parameters['Timestamp'] = get_iso8601_time()
    parameters['SignatureVersion'] = '1.0'
    parameters['SignatureNonce'] = get_uuid()
    parameters['Action'] = Action
    for (k, v) in sorted(user_param.items()):
        parameters[k] = v
    return parameters


def get_param(parameters):
    '''把公共参数拼接成字符串'''
    param_str = ''
    for (k, v) in sorted(parameters.items()):
        param_str += "&" + urllib.quote(k, safe='') + "=" + urllib.quote(v, safe='')
    param_str = param_str[1:]
    return param_str


def get_StringToSign(parameters, param_str):
    '''拼接生成签名的字符串'''
    StringToSign = parameters['HTTPMethod'] + "&%2F&" + urllib.quote(param_str, safe='')
    return StringToSign


def get_signature(StringToSign, AccessKeySecret):
    '''构建签名'''
    h = hmac.new(AccessKeySecret, StringToSign, hashlib.sha1)
    signature = base64.encodestring(h.digest()).strip()
    return signature


def build_request(server_url, param_str, signature, AccessKeySecret):
    '''拼接url并进行请求'''
    Signature = "Signature=" + urllib.quote(signature)
    param = param_str + "&" + Signature
    request_url = server_url + param
    s = requests.get(request_url)
    #print s.content
    return s.content
    
    
def get_regions(server_url, Action, user_param, AccessKeySecret, AccessKeyId, Version):
    '''对请求进行模块
    server_url： slb.aliyun.com
    Action = 'DescribeRegions'
    AccessKeySecret, AccessKeyId:也就是ak
    user_param = {'LoadBalancerId': 'lb-2zekxu2elibyexxoo9hlw'}
    Version:例如slb的版本是2014-05-15,每个服务都不相同
    '''
    server_url = 'https://' + server_url + '/?'
    AccessKeySecret = AccessKeySecret
    AccessKeyId = AccessKeyId
    parameters = get_parameters(user_param, Action, AccessKeyId, Version)
    param_str = get_param(parameters)
    StringToSign = get_StringToSign(parameters, param_str)
    signature = get_signature(StringToSign, AccessKeySecret + '&')
    return build_request(server_url, param_str, signature, AccessKeySecret)
#if __name__ == '__main__':
    #get_regions("ecs.aliyuncs.com","RebootInstance",{"InstanceId":'i-bp1j7ffkk3uzdj8btpv4',},"wjEIGuPnRjSURzUDYUmBXrFv3ijk8f","FP60l5Rd7FBHDNAZ","2014-05-26") 

'''
批量导入把instanceId和regionId导入数据库
'''
if __name__ == '__main__':
    areas=['cn-qingdao','cn-beijing','cn-zhangjiakou','cn-hangzhou','cn-shanghai','cn-shenzhen']
    for area in areas:
        #print ("%s \n ")%area
        for i in range(1,5):
            content = get_regions("ecs.aliyuncs.com","DescribeInstances",{"RegionId":area,"PageSize":"100","PageNumber":str(i)},"wjEIGuPnRjSURzUDYUmBXrFv3ijk8f","FP60l5Rd7FBHDNAZ","2014-05-26")
            true=''
            false=''
            content =eval(content)
            contentList=content["Instances"]["Instance"]
            for lis in contentList:
                ipAddress=lis["PublicIpAddress"]["IpAddress"]
                regionId=lis['RegionId']
                instanceId=lis['InstanceId']
                print ("%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(ipAddress,ipAddress[0],type(ipAddress[0]),regionId,type(regionId),instanceId,type(instanceId)))
                cnxn = MySQLdb.connect('hequskuapp.mysql.rds.aliyuncs.com','by15161458383','K120Esc1','hq_db' )
                cursor =cnxn.cursor();
                sql = "update t_config_mstsc set  RegionId='%s',InstanceId='%s' where ip='%s'"%(regionId,instanceId,ipAddress[0])
                #sql='update t_config_mstsc set  RegionId="cn-qingdao",InstanceId="i-m5eijiwzg03cxwhz3lti" where ip="10.29.168.221"'
                cursor.execute(sql)
                cursor.execute('commit')

