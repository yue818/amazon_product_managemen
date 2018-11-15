# coding=utf-8

"""
下载图片
"""

import os, time, urllib2
from get_ip_proxy import get_ip_proxy


def download_image(url, main_sku):
    """下载图片，文件夹名为MainSKU，文件名为webimage/后面的字符串"""
    # picture_path = r'C:/Users/Administrator/Desktop/picture'
    time_stamp = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + '_'
    picture_path = '/home/picture'
    opener = get_ip_proxy()
    small_url = url.replace('original', "small")
    try:
        os.makedirs(r'%s/%s' % (picture_path, main_sku))
    except:
        pass
    if 'webimage/' in url:
        fileName = time_stamp + small_url.split('webimage/')[-1].split('?')[0]
    else:
        fileName = time_stamp + small_url.split('wxalbum/')[-1].replace('/', '_')
    print 'url---%s' % small_url
    try:
        request = urllib2.Request(small_url)
        resp = opener.open(request, timeout=30)
        image_path = r'%s/%s/%s' % (picture_path, main_sku, fileName)
        with open(image_path, 'ab') as f:
            f.write(resp.read())
        return image_path
    except Exception, e:
        print e
        return None