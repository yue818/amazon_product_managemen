# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: test-1008.py
 @time: 2018/10/8 13:34
"""
import requests
from bs4 import BeautifulSoup
from json import load
from urllib2 import urlopen

def get_out_ip(url):
    try:
        r = requests.get(url)
        txt = r.text
        ip = txt[txt.find("[") + 1: txt.find("]")]
    except Exception as ex:
        print ex
        ip = load(urlopen('https://api.ipify.org/?format=json'))['ip']
    print('ip:' + ip)
    return ip


def get_real_url(url=r'http://www.ip138.com/'):
    r = requests.get(url)
    txt = r.text
    soup = BeautifulSoup(txt, "html.parser").iframe
    print soup
    return soup["src"]


print get_out_ip(get_real_url())






from urllib2 import urlopen

my_ip = urlopen('http://ip.42.pl/raw').read()
print 'ip.42.pl', my_ip

from json import load
from urllib2 import urlopen

my_ip = load(urlopen('http://jsonip.com'))['ip']
print 'jsonip.com', my_ip

from json import load
from urllib2 import urlopen

my_ip = load(urlopen('http://httpbin.org/ip'))['origin']
print 'httpbin.org', my_ip

from json import load
from urllib2 import urlopen

my_ip = load(urlopen('https://api.ipify.org/?format=json'))['ip']
print 'api.ipify.org', my_ip
