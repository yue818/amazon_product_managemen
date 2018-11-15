# -*- coding:utf-8 -*-

"""
 @desc:
 @author: wuchongxiang
 @site:
 @software: PyCharm
 @file: 20181112a.py
 @time: 2018/11/12 19:02
"""
import urllib2
from bs4 import BeautifulSoup
import traceback
import re
import datetime


def format_urls(url):
    WISH_URL = 'wish.'
    AMAZON_URL = 'amazon.'
    WWW1688_URL = '1688.'
    EBAY_URL = 'ebay.'
    ALIEXPRESS_URL = 'aliexpress.'

    if url is None or url.strip() == '':
        return ''

    return_url = url
    # wish
    if url.find(WISH_URL) >= 0:
        if url.find('=') >= 0:
            PlatformPIDs = url.split(r'=')
            if len(PlatformPIDs) > 1:
                return_url = PlatformPIDs[-1]
                return_url = 'wish.com/c/%s' % (return_url)
        return_url = return_url.replace('http://', '').replace('https://', '').replace('www.', '').replace(' ', '')
        return_url = 'https://www.%s' % (return_url)

    if url.find(AMAZON_URL) >= 0:
        if url.find('?') >= 0:
            return_url = url.split(r'?')[0]
        return_url = return_url.replace('http://', '').replace('https://', '').replace('www.', '').replace(' ', '')
        return_url = 'https://www.%s' % (return_url)
        return return_url

    if url.find(EBAY_URL) >= 0:
        if url.find('?') >= 0:
            return_url = url.split(r'?')[0]
        return_url = return_url.replace('http://', '').replace('https://', '').replace('www.', '').replace(' ', '')
        return_url = 'https://www.%s' % (return_url)
        return return_url

    if url.find(ALIEXPRESS_URL) >= 0:
        if url.find('?') >= 0:
            return_url = url.split(r'?')[0]
        return_url = return_url.replace('http://', '').replace('https://', '').replace('www.', '').replace(' ', '')
        return_url = 'https://www.%s' % (return_url)
        return return_url

    if url.find(WWW1688_URL) >= 0:
        if url.find('?') >= 0:
            return_url = url.split(r'?')[0]
        if url.find('#') >= 0:
            return_url = url.split(r'#')[0]
        return_url = return_url.replace('http://', '').replace('https://', '').replace('www.', '').replace(' ', '')
        return_url = 'https://%s' % (return_url)
        return return_url
    print 'format_url is: %s' % return_url
    return return_url


def has_child_tag(tag):
    return tag.children is not None


def has_child_p(tag):
    result = False
    if tag.name == 'div' and tag.descendants is not None:
        for child in tag.descendants:
            if child.name == 'p':
                result = True
                break
    return result


def has_child_li_or_tr(tag):
    result = False
    if tag.name == 'div' and tag.descendants is not None:
        for child in tag.descendants:
            if child.name in  ('li', 'tr'):
                result = True
                break
    return result


def read_amazon(pri_key_id, source_url):
    if source_url is not None and source_url.strip() != '':
        if source_url.find('www.') < 0:
            url_mid = ' https://www.amazon.com/dp/' + source_url
        else:
            url_mid = source_url
        new_source_url = format_urls(url_mid)
    else:
        return
    print 'new_source_url is: %s' % new_source_url
    # url，query_user，query_time，img_url，title，second_category，price
    try:
        head = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10'}
        req = urllib2.Request(new_source_url, headers=head)
        data_bytes = urllib2.urlopen(req, timeout=30).read()
        print 'get data_bytes success'

        if data_bytes is not None:
            soup = BeautifulSoup(data_bytes, "lxml")

            [style.extract() for style in soup.find_all('style')]
            [script.extract() for script in soup.find_all('script')]

            print datetime.datetime.now()

            # 图片
            image_dic = dict(soup.find("div", id="imgTagWrapperId").find("img").attrs)
            images = []
            if image_dic['src'].endswith(('.jpg',)):
                images.append(image_dic['src'])
            if image_dic['data-old-hires'].endswith(('.jpg',)):
                images.append(image_dic['data-old-hires'])
            image_match = re.findall('"(https?://.*?.jpg)"', image_dic['data-a-dynamic-image'])
            for ima in image_match:
                images.append(ima)
            print 'Image_url: %s' % images[0]

            # 店铺信息
            shop_info = soup.find("a", id=["bylineInfo", "brand"]).get_text().strip().replace("'", '`')
            pattern = '\\b' + shop_info + '\\b'
            # 商品标题
            title = soup.find("span", id="productTitle").get_text().strip().replace("'", '`')
            title = re.sub(pattern, '', title)
            print 'Title: %s' % title

            # 二级类目
            item_all_html = soup.find("div", id=["wayfinding-breadcrumbs_container"]).find_all('span', "a-list-item")
            item_all = ''
            second_category = ''
            for idx, item in enumerate(item_all_html):
                item_all += item.get_text().strip().replace("'", '`')
                if idx == 2:
                    second_category = item.get_text().strip().replace("'", '`')
            print 'item_all: %s' % item_all
            print 'second_category: %s' % second_category

            # 价格
            price = soup.find("span", id=["priceblock_ourprice"]).get_text().strip()
            price = filter(lambda ch: ch in '0123456789.', str(price))
            print 'price: %s' % price

        else:
            print 'Warn: feed back is null'
    except Exception as e:
            print e
            print 'Error: %s' % traceback.print_exc()


read_amazon(1, 'https://www.amazon.com/dp/B07J5L9J7Z')