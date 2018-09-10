#-*-coding:utf-8-*-

"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: proxy.py
 @time: 2018-03-28 14:13

 代理IP获取
"""
import urllib2

class proxy():
    @staticmethod
    def get_proxy():
        """IP代理池"""
        proxyAPI = r'http://dynamic.goubanjia.com/dynamic/get/0f43af0bb144af370b5c1df840c7df35.html'
        proxy = {}

        try:
            proxyIP = urllib2.urlopen(proxyAPI).read().strip("\n")
            proxy = {'http': proxyIP}
        except:
            pass

        httpproxy_handler = urllib2.ProxyHandler(proxy)
        opener = urllib2.build_opener(httpproxy_handler)

        return opener