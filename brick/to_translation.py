#-*-coding:utf-8-*-

"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: to_translation.py
 @time: 2018-05-11 15:30
"""
import urllib, urllib2, sys
import MySQLdb
import os,errno
import oss2
import csv
from xlwt import *
import time
from io import StringIO
from datetime import datetime
import traceback


def to_translate (FromLanguage,Translated,ToLanguage):
    result = ''
    try:
        host = 'http://jisuzxfy.market.alicloudapi.com'
        path = '/translate/translate'
        method = 'GET'
        appcode = "2cd4ea81891e4118bee6ecfae5d0f2f1"
        querys = "from=" + FromLanguage + "&" + "%s"%(urllib.urlencode({"text":Translated})) + "&to=" + ToLanguage + "&type=google"
                #'from=    en              &     %s                                                     &to=     es           &type=google'
        bodys = {}
        url = host + path + "?" + querys

        # print '---------%s'%url
        request = urllib2.Request(url)
        request.add_header('Authorization', 'APPCODE ' + appcode)
        request.add_header('Content-Type','application/json; charset=utf-8')
        response = urllib2.urlopen(request)
        # {"status":"0","msg":"ok","result":{"type":"google","from":"en","to":"es","text":"This is the test","result":"Esta es la prueba"}}
        _content = eval(response.read())
        if _content['status'] == '0' and _content['msg'] == 'ok':
            result = _content['result'].get('result','')
        # print 'to_translate--result---%s'%_content
    except Exception,ex:
        print '%s_%s:%s'%(traceback.print_exc(),Exception,ex)
    return result

def main():
    FromLanguage = sys.argv[1]
    ToLanguage   = sys.argv[2]
    Translated   = sys.argv[3]

    result = to_translate(FromLanguage, Translated, ToLanguage)
    print result


if __name__ == "__main__":
    main()