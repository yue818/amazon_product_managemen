#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: wish_rating.py
 @time: 2018/7/4 13:39
"""
import json
import re
import requests
from random import choice



USER_AGENT = [
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
    'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Mozilla/5.0 (Windows NT 6.1; rv,2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
]

def http_headers():
    """生成headers"""
    ali_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': choice(USER_AGENT),
        'Connection': 'close'
    }
    return ali_headers

def ip_proxy():
    """获取代理"""
    proxyAPI = r'http://dynamic.goubanjia.com/dynamic/get/995d33fcec25d7040a8e584463124997.html'
    proxy = {}
    while not proxy.get('http', ''):
        try:
            response = requests.get(proxyAPI)
            context = response.content
            current_ip = context.strip()
            proxy = {'http': current_ip}
        except Exception, e:
            print e
    return proxy


def product_rating(product_id):

    url = 'https://www.wish.com/c/%s' % product_id
    code = 0
    errof_info = ''
    rating = None
    status_code = 200
    time_out = 0
    if product_id:
        headers = http_headers()
        for i in range(3):
            try:
                proxy = ip_proxy()
                response = requests.get(url, headers=headers, proxies=proxy, timeout=30, verify=False)
                status_code = response.status_code
                page_source = response.text

                # 评论数为零，评分直接为零
                count = 0
                try:
                    pattern_count = r'"rating_count": (.+?), "rating_class'
                    count_list = re.findall(pattern_count, page_source)
                    count = float(count_list[0])
                except Exception, e:
                    print e
                if count == 0:
                    rating = 0
                    break
                else:
                    pattern_rating = r'product_rating": {"rating": (.+?), "rating_count'
                    rating_list = re.findall(pattern_rating, page_source)
                    if rating_list:
                        rating = round(float(rating_list[0]), 1)
                        break
            except requests.exceptions.Timeout:
                time_out = 1
            except Exception, e:
                print e
        if rating is None:
            if status_code == 404:
                code = 2
                errof_info = 'The only parameter "productID" is wrong'
            elif time_out:
                code = 3
                errof_info = 'Request Wish page timeout'
            else:
                code = 4
                errof_info = 'Undefined errors'
    else:
        code = 1
        errof_info = 'The only parameter "productID" is empty'

    result = {'code': code, 'error_info': errof_info, 'rating': rating}
    return json.dumps(result)


