#-*-coding:utf-8-*-

"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: HTTP301_302_303_307_ERROR.py
 @time: 2018-03-29 11:18
 url重定向问题解决
"""
import urllib2

class MyHTTPRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        print "Cookie Manip Right Here"
        return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)

    http_error_301 = http_error_303 = http_error_307 = http_error_302

cookieprocessor = urllib2.HTTPCookieProcessor()

urlopener = urllib2.build_opener(MyHTTPRedirectHandler, cookieprocessor)


# 用法如下
# urllib2.install_opener(urlopener)
# req = urllib2.Request(www1688urls)
# response = urllib2.urlopen(req, timeout = 30).read().decode('gbk')
# print response
#
# print cookieprocessor.cookiejar



