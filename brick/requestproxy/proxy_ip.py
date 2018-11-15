# coding=utf-8

import time
import requests
from random import choice, randint


# user-agent
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


def get_ip_proxy():
    """获取代理"""
    # proxyAPI = r'http://dynamic.goubanjia.com/dynamic/get/0f43af0bb144af370b5c1df840c7df35.html'
    proxyAPI = r'http://tvp.daxiangdaili.com/ip/?tid=558968873047809&num=1&protocol=https&category=2'

    proxy = {}
    while not proxy:
        try:
            response = requests.get(proxyAPI)
            context = response.content
            if 'IP' in context:
                proxy = {}
                time.sleep(1)
            else:
                proxy = {'http': context.strip()}
        except Exception, e:
            print e
    return proxy


def get_headers():
    """生成headers"""
    ali_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': choice(USER_AGENT),
        'Connection': 'close'
    }
    return ali_headers


def get_random_code():
    """生成随机码 (生成规则：‘unix 13位时间戳字符串’.‘五位随机数字符串，不足前面补零’.‘五位随机数字符串，不足前面补零’)"""
    unix_time = str(int(time.time() * 1000))
    first_random = str(randint(0, 99999)).zfill(5)
    second_random = str(randint(0, 99999)).zfill(5)
    random_code = '.'.join([unix_time, first_random, second_random])
    return random_code


def ip_verification():
    """验证代理IP可用性"""
    usability_flag = False
    while not usability_flag:
        http_proxy = get_ip_proxy()
        # print 'http_proxy: %s' % http_proxy
        headers = get_headers()
        random_code = get_random_code()
        verification_url = 'http://47.100.6.69:32578/ip?randomCode=%s' % random_code
        # verification_url = 'https://www.baidu.com/'
        try:
            response = requests.get(verification_url, proxies=http_proxy, headers=headers)
            if response.status_code == 200:
                usability_flag = True
                http_proxy = {'http': http_proxy['http']}
                print 'http_proxy: %s' % http_proxy
                return http_proxy, headers, random_code
            else:
                print response.status_code
        except Exception,e:
            print(e.message)

#测试函数可用性
if __name__ == '__main__':
    for n in range(100):
        http_proxy, headers, random_code = ip_verification()
        print(http_proxy["http"])
        time.sleep(1)
