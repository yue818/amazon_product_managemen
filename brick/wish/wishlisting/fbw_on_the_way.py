#-*-coding:utf-8-*-
u"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: fbw_on_the_way.py
 @time: 2018/9/4 14:44
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fbw_on_the_way(transport_id):
    url = "http://139.224.60.129:8321/track_query.aspx?track_number=" + transport_id
    print url
    res = requests.get(url, timeout=1).content
    soup = BeautifulSoup(res, "lxml")
    SignTmp = soup.html.find_all("span", string = u'签收人')
    if not SignTmp:
        SignTmp = soup.html.find_all("span", string = u'Sign for people')
    if SignTmp:
        print SignTmp[0].string


if __name__ == '__main__':
    a = datetime.now()
    fbw_on_the_way('08090013')
    # fbw_on_the_way('08090009')
    b = datetime.now()

    print a
    print b
    print b-a