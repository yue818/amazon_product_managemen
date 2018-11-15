# coding=utf-8

import urllib2
from brick.function.get_ip_proxy import get_ip_proxy


def get_pic_1(img_url):
    """
    下载图片内容
    :param img_url: 图片的url
    :return: 图片二进制内容
    """
    opener = get_ip_proxy()

    try:
        request = urllib2.Request(img_url.replace('\\', ''))
        resp = opener.open(request, timeout=30)
        if resp.code == 200:
            result = resp.read()
    except Exception, e:
        print 'get_ip----------------------------', e
        result = 'ERROR'

    return result


def get_pic(img_url):
    result = get_pic_1(img_url)

    i = 0
    while i < 3:
        if result == 'ERROR':
            result = get_pic_1(img_url)
        else:
            break
        i += 1

    return result