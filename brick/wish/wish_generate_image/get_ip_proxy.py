# coding=utf-8


"""
获取ip代理
"""
import urllib2


def get_ip_proxy():
    """
    IP代理池
    返回值：拥有ip代理的opener
    """
    proxyAPI = r'http://dynamic.goubanjia.com/dynamic/get/0f43af0bb144af370b5c1df840c7df35.html'
    proxy = {}
    try:
        response = urllib2.urlopen(proxyAPI).read()
        if len(response)>20:
            proxy = {}
        else:
            proxyIP = urllib2.urlopen(proxyAPI).read().strip("\n")
            proxy = {'http': proxyIP}
            print proxy
    except:
        pass
    httpproxy_handler = urllib2.ProxyHandler(proxy)
    opener = urllib2.build_opener(httpproxy_handler)
    return opener
