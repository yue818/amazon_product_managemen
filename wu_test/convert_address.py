# -*- coding:utf-8 -*-

"""
 @desc:
 @author: wuchongxiang
 @site:
 @software: PyCharm
 @file: convert_address.py
 @time: 2018/12/7 15:05
"""
import traceback
import xlrd
import xlwt
import urllib2
from json import load
import random
import oss2


def convert_url():
    w = xlwt.Workbook()
    sheet_convert = w.add_sheet('convert_url')
    work_book = xlrd.open_workbook(r'C:\inetpub\wwwroot\1.xlsx')
    print work_book.sheet_names()
    sheet_name = work_book.sheet_names()[0]
    print sheet_name
    sheet = work_book.sheet_by_name('Sheet1')
    print sheet.name, sheet.nrows, sheet.ncols
    for row_num in range(76, 101):
        print '-'*100
        print row_num
        for col_num in (0, 10, 11, 12, 13, 14, 15, 16):
            if 10 <= col_num < 17 and row_num >= 1:
                url = sheet.row(row_num)[col_num].value.encode('utf-8')
                url_new = get_image(url)
                print url
                print url_new
                sheet_convert.write(row_num, col_num, url_new.encode('utf-8'))
            else:
                print sheet.row(row_num)[col_num].value.encode('utf-8')
                sheet_convert.write(row_num, col_num, sheet.row(row_num)[col_num].value.encode('utf-8'))
        try:
            w.save(r'C:\inetpub\wwwroot\4.xls')
        except:
            continue


def random_code():
    # Random Code Info
    Upper = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    Lower = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    Number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    code = []

    for i in range(2):
        code.append(random.choice(Number))

    letter = Upper + Lower

    for i in range(9):
        code.append(random.choice(letter))

    result = ''.join(code)

    return result


def get_image(url):
    ACCESS_KEY_ID = 'LTAIH6IHuMj6Fq2h'
    ACCESS_KEY_SECRET = 'N5eWsbw8qBkMfPREkgF2JnTsDASelM'
    ENDPOINT_OUT = 'oss-cn-shanghai.aliyuncs.com'
    BUCKETNAME_APIVERSION = 'fancyqube-all-mainsku-pic'

    # Path for Download Images
    LOCAL_PATH = 'C:\inetpub\wwwroot\\'

    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, ENDPOINT_OUT, BUCKETNAME_APIVERSION)

    image_url = url.split('/', 3)[-1]
    code = random_code()
    image_url_local = code + '.' + url.split('.')[-1]
    bucket.get_object_to_file(image_url, LOCAL_PATH + image_url_local)

    local_ip = load(urllib2.urlopen('https://api.ipify.org/?format=json'))['ip']

    return 'http://' + local_ip + '/' + image_url_local


convert_url()










