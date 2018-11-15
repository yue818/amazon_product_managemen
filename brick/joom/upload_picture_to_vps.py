# coding=utf-8

from ftplib import FTP
import sys
import socket
import os
import urllib2
from PIL import Image
from random import choice as randomChoice
import string
from brick.function.get_ip_proxy import get_ip_proxy
from joom_app.table.t_config_online_ftp import t_config_online_ftp

reload(sys)
sys.setdefaultencoding('utf-8')


# ShopInfo = {
#     'joom2': {
#         'host': '119.23.144.25', 'port': '21', 'username': 'administrator', 'passwd': 'nhkilHbrOq4', 'pic_path': '/image/', 'code_length': 11
#     },
#     'joom3': {
#         'host': '114.115.161.21', 'port': '21', 'username': 'administrator', 'passwd': 'zyzztYY3', 'pic_path': '/jpg/', 'code_length': 20
#     },
#     'joom4': {
#         'host': '121.43.198.134', 'port': '21', 'username': 'administrator', 'passwd': 'jKTzM0rYRhJK', 'pic_path': '/pic/', 'code_length': 16
#     },
#     'joom5': {
#         'host': '120.26.7.212', 'port': '21', 'username': 'administrator', 'passwd': '123', 'pic_path': '/picture/', 'code_length': 7
#     },
#     'joom8': {
#         'host': '120.76.118.141', 'port': '21', 'username': 'administrator', 'passwd': 'tKkILzI8Idbi', 'pic_path': '/img/', 'code_length': 18
#     },

#     'Mall-0001-Fanqube/HF': {
#         'host': '115.29.213.208', 'port': '212', 'username': 'administrator', 'passwd': '5uDtssp7ID', 'pic_path': '/mymallpic/', 'code_length': 12
#     },
#     'Mall-0002-wangyue/HF': {
#         'host': '101.200.73.161', 'port': '212', 'username': 'administrator', 'passwd': 'zyzz321tYY3', 'pic_path': '/mymallimage/', 'code_length': 16
#     },
#     'Mall-0003-SaiYou/HF': {
#         'host': '101.200.86.1', 'port': '212', 'username': 'administrator', 'passwd': 'zyzztYY693', 'pic_path': '/mallpic/', 'code_length': 18
#     },
#     'Mall-0004-Hequ/HF': {
#         'host': '120.55.125.236', 'port': '212', 'username': 'administrator', 'passwd': 'EqTphOc02IiE', 'pic_path': '/mallimg/', 'code_length': 20
#     },
#     'Mall-0005-Yilalei/HF': {
#         'host': '123.57.83.18', 'port': '212', 'username': 'administrator', 'passwd': 'ugbQMA8D4', 'pic_path': '/imageofmall/', 'code_length': 10
#     },
#     'Mall-0006-Jingj/HF': {
#         'host': '139.196.44.136', 'port': '212', 'username': 'administrator', 'passwd': 'uQjxmJzaVc7', 'pic_path': '/mymallimg/', 'code_length': 8
#     },
#     'Mall-0007-Dingyou/HF': {
#         'host': '101.200.212.146', 'port': '212', 'username': 'administrator', 'passwd': '123', 'pic_path': '/picofmall/', 'code_length': 14
#     },
# }


# def get_shop_info():
#     shops_ftp_info = t_config_online_ftp.objects.all()
#     ftp_info = dict()
#     for i in shops_ftp_info:
#         ftp_info[i.ShopName] = dict()
#         ftp_info[i.ShopName]['host'] = str(i.Host)
#         ftp_info[i.ShopName]['port'] = str(i.Port)
#         ftp_info[i.ShopName]['username'] = str(i.UserName)
#         ftp_info[i.ShopName]['passwd'] = str(i.PassWord)
#         ftp_info[i.ShopName]['pic_path'] = str(i.PicPath)
#         ftp_info[i.ShopName]['code_length'] = int(i.CodeLength)
#
#     return ftp_info
#
#
# ShopInfo = get_shop_info()


def get_shop_info(shop_name):
    shops_ftp_info = t_config_online_ftp.objects.filter(ShopName=shop_name)
    shop_info = dict()
    for i in shops_ftp_info:
        shop_info['host'] = str(i.Host)
        shop_info['port'] = str(i.Port)
        shop_info['username'] = str(i.UserName)
        shop_info['passwd'] = str(i.PassWord)
        shop_info['pic_path'] = str(i.PicPath)
        shop_info['code_length'] = int(i.CodeLength)
    return shop_info


def uploadPic(ftp, picPath):
    fp = open(picPath, 'rb')

    picname = os.path.basename(picPath)
    filesize = os.path.getsize(picPath)
    try:
        ftp.storbinary('STOR %s' % picname, fp, filesize)
        fp.close()
        return 0
    except Exception, e:
        print e
        fp.close()
        return 3


def ftp_Login(host, username, password, port):
    ftp = FTP()
    # ftp.set_pasv(False)
    try:
        ftp.connect(host, port)
    except (socket.error, socket.gaierror):
        return 1
    try:
        ftp.login(username, password)
    except:
        ftp.quit()
        return 2

    # print ftp.getwelcome()
    return ftp


def uploadVps(picName, shopname, shop_info):
    host = shop_info['host']
    username = shop_info['username']
    port = shop_info['port']
    passwd = shop_info['passwd']
    file = shop_info['pic_path']

    ftp = ftp_Login(host, username, passwd, port)
    if (ftp == 1):
        # print 'ERROR:cannot reach " %s"' % host
        return 1
    elif (ftp == 2):
        # print 'ERROR: cannot login anonymously'
        return 2
    else:
        picIndex = uploadPic(ftp, picName)
        if (picIndex == 0):
            ftp.quit()
            return 'http://' + host + file + picName
        else:
            ftp.quit()
            return -1


def astrcmp(str1, str2):
    return str1.lower() == str2.lower()


def Cut_image(img_path):
    try:
        mPath, ext = os.path.splitext(img_path)
        if (astrcmp(ext, ".png") or astrcmp(ext, ".jpg")):
            img = Image.open(img_path)
            out = img.resize((800, 800), Image.ANTIALIAS)
            new_file_name = '%s%s' % (mPath, ext)
            out.save(new_file_name)
            print 'Resize Image Success'
        else:
            print "ERROR: Wrong Image Type"
    except Exception, e:
        print e


def getNewName(length):
    picList = []
    choiceData = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'
    ]

    count = 0
    while count != length:
        picList.append(randomChoice(choiceData))
        count += 1
    picNewName = string.join(picList).replace(" ", "")

    return picNewName


def resize_image(url, shopname, index, shop_info):
    global mainPic
    # ip代理池
    opener = get_ip_proxy()
    length = shop_info['code_length']

    if index == 0:
        mainPic = None
        picName = getNewName(length)
        mainPic = picName
    else:
        picName = mainPic + '-' + str(index)
    pic_path = picName + '.jpg'

    try:
        request = urllib2.Request(url)
        response = opener.open(request, timeout=20).read()
    except:
        return -1

    with open(pic_path, 'wb') as f:
        f.write(response)
    try:
        Cut_image(pic_path)
        result = uploadVps(pic_path, shopname, shop_info)
        os.remove(pic_path)

        if (result == -1):
            print 'Upload To VPS Failed'
            return -1
        else:
            return result
    except:
        print "Unexpected error:", sys.exc_info()
        return -1

def upload_picture_to_vps(image):
    i = 0
    result = {}
    shopname = image.get('shopname', '')
    main_image = image.get('main_image', '')

    shop_info = get_shop_info(shopname)

    # 主图处理
    main_img = resize_image(main_image, shopname, 0, shop_info)
    j = 0
    while j < 3:
        j += 1
        if main_img == -1 or main_img == 1:
            main_img = resize_image(main_image, shopname, 0, shop_info)
        else:
            break
    result['main_image'] = main_img

    # 变种图处理
    variation_image_list = image.get('variation_image_list', [])
    result_variation_image_list = []
    for variation_image in variation_image_list:
        i += 1
        j = 0

        variation_img = resize_image(variation_image, shopname, i, shop_info)
        # 如果
        while j < 3:
            if variation_img == -1 or variation_img == 1:
                variation_img = resize_image(variation_image, shopname, i, shop_info)
            else:
                break
            j += 1

        result_variation_image_list.append(variation_img)
    result['variation_image_list'] = result_variation_image_list

    # 副图处理
    extra_image_list = image.get('extra_image_list', [])
    result_extra_image_list = []
    for extra_image in extra_image_list:
        i += 1
        j = 0
        extra_img = resize_image(extra_image, shopname, i, shop_info)
        while j < 3:
            if extra_img == -1 or extra_img == 1:
                extra_img = resize_image(extra_image, shopname, i, shop_info)
            else:
                break
            j += 1

        result_extra_image_list.append(extra_img)
    result['extra_image_list'] = result_extra_image_list
    print result
    return result


def upload_pic_to_vps_by_file(file_obj, flag, shopname):
    sRes = {'code': 0, 'data': None, 'message': ''}
    shop_info = get_shop_info(shopname)
    host = shop_info['host']
    port = shop_info['port']
    username = shop_info['username']
    passwd = shop_info['passwd']
    file_path = shop_info['pic_path']

    ftp = ftp_Login(host, username, passwd, port)
    if (ftp == 1):
        message = 'ERROR:cannot reach " %s"' % host
        sRes['code'] = 1
        sRes['message'] = message
        return sRes
    elif (ftp == 2):
        message = 'ERROR: cannot login anonymously'
        sRes['code'] = 2
        sRes['message'] = message
        return sRes
    else:
        length = shop_info['code_length']
        picName = getNewName(length)
        pic_path = picName + '.jpg'
        file_obj._set_name(pic_path)

        try:
            ftp.storbinary('STOR %s' % pic_path, file_obj, file_obj.size)
            url = 'http://' + host + file_path + pic_path
            sRes['data'] = {'url': url}
            return sRes
        except Exception, e:
            message = str(e)
            sRes['code'] = 3
            sRes['message'] = message
            return sRes
