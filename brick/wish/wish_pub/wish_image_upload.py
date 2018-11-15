#-*-coding:utf-8-*-
u"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: wish_image_upload.py
 @time: 2018/10/22 13:56
"""
import urllib2, base64
from retrying import retry

from brick.wish.api.wishapi import cwishapi

@retry(stop_max_attempt_number=3,wait_exponential_multiplier=500,wait_exponential_max=3000)
def upload_img_retry(data):
    uresult = cwishapi().upload_image_wish(data)
    if uresult['errorcode'] == 1:
        return uresult
    else:
        raise Exception(u'An error occurred while uploading the image. Upload failed! Please try again later. errortext: %s' % uresult['errortext'])


def wish_image_upload(imgurl,auth_info):
    try:
        if imgurl.find('.wish.com/') != -1:  # 如果使用的是Wish的图片，则直接返回，不用再次下载上传
            return {'errorcode': 1, 'errortext': '', 'image_url': imgurl}

        req = urllib2.Request(imgurl)
        image_bytes = urllib2.urlopen(req, timeout=30).read()

        img = base64.b64encode(image_bytes)

        data = {
            'access_token': auth_info['access_token'],
            'format': 'json',
            'image': img,
        }

        uresult = upload_img_retry(data)

    except Exception, e:
        uresult = {'errorcode': -1, 'errortext': '%s:%s' % (Exception, e)}

    return uresult
