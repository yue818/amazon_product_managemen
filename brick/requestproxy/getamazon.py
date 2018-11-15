# -*- coding: utf-8 -*-
"""  
 @desc: 抓取亚马逊信息，从restAPI下载
 @author: fangyu  
 @site: 
 @software: PyCharm
 @file: getamazon.py
 @time: 2018-05-25 17:05
"""

import binascii
import urllib2
import base64

def getProxyHost():
    return "http://139.196.120.231:7789"

def getProxyURI():
    return "/amazon/proxy"

def getProxyedURL(url):
    urlBase64 = base64.urlsafe_b64encode(url)
    proxyURL = getProxyHost() + getProxyURI() + "?url=" + urlBase64
    print(proxyURL)
    return proxyURL

def getAmazonConentFromURL(url):
    import requests
    from proxy_ip import get_headers
    proxyURL = getProxyedURL(url)
    try:
        headers = get_headers()
        resp = requests.get(proxyURL, headers=headers, timeout=30)
        respBody = resp.content
        resp.close()
    except urllib2.HTTPError, e:
        print("===============================")
        print(e.code)
        return e.reason,""
    except urllib2.URLError, e:
        print("===============================")
        print(e.reason)
        return e.reason,""
    except Exception,e:
        print("===============================")
        print(e.message)
        return e.message,""
    return None,respBody

def getTitleImageurl(url):
    import json,requests
    from formatUrl import format_urls
    try:
        platform,ASIN = format_urls(url)
        if platform != "amazon":
            return "此url当前不支持", {}
    except Exception,e:
        return "url不支持",{}
    resp = requests.get("http://139.196.120.231:7789/amazon/get?ASIN=%s"%ASIN, timeout=30)
    respDict = json.loads(resp.content)
    resp.close()
    return None,respDict