# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: reverse_collection.py
 @time: 2018-03-07 9:49
"""

import urllib2
from bs4 import BeautifulSoup
import traceback
import re
import datetime


class GetProductInfoByUrl:
    def __init__(self, db_connection):
        self.db_conn = db_connection

    def execute_sql(self, sql):
        cursor = self.db_conn.cursor()
        try:
            cursor.execute(sql)
            cursor.execute('commit;')
            cursor.close()
        except Exception as e:
            cursor.close()
            print e

    def format_urls(self, url):
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

    def read_amazon(self, pri_key_id, source_url):
        if source_url is not None and source_url.strip() != '':
            if source_url.find('www.') < 0:
                url_mid = ' https://www.amazon.com/dp/' + source_url
            else:
                url_mid = source_url
            new_source_url = self.format_urls(url_mid)
        else:
            return
        print 'new_source_url is: %s' % new_source_url

        try:
            head = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10'}
            req = urllib2.Request(new_source_url, headers=head)
            data_bytes = urllib2.urlopen(req, timeout=30).read()
            print 'get data_bytes success'

            if data_bytes is not None:
                soup = BeautifulSoup(data_bytes, "lxml")

                [style.extract() for style in soup.find_all('style')]
                [script.extract() for script in soup.find_all('script')]

                # 店铺信息
                shop_info = soup.find("a", id=["bylineInfo","brand"]).get_text().strip().replace("'", '`')
                pattern = '\\b' + shop_info + '\\b'


                # 商品标题
                title = soup.find("span", id="productTitle").get_text().strip().replace("'", '`')
                title = re.sub(pattern, '', title)
                print '\nTitle:'
                print '  ' + title
                sql_title = "update t_templet_amazon_collection_box set item_name ='%s' where id = %d" %(title, pri_key_id)
                print sql_title
                self.execute_sql(sql_title)

                # 商品描述
                key_words = soup.find("div", id="featurebullets_feature_div").find_all("span", "a-list-item")
                i = 0
                print '\nKey_words:'
                for key in key_words:
                    if not key.find_all(self.has_child_tag):
                        key_word = key.get_text().strip().replace('\n', ' ').replace("'", '`')
                        key_word = re.sub(pattern, '', key_word)
                        i += 1
                        if i <= 5:
                            sql_keyword = "update t_templet_amazon_collection_box set bullet_point%d ='%s' where id = %d" % (i, key_word, pri_key_id)
                            print sql_keyword
                            self.execute_sql(sql_keyword)
                        print '  key word %d is:  %s' % (i, key_word)

                # 商品图片
                # link_jpg = dict(soup.find("div", id="imgTagWrapperId").find("img").attrs)['src']
                # if not link_jpg.endswith(('.jpg',)):
                #     link_jpg = dict(soup.find("div", id="imgTagWrapperId").find("img").attrs)['data-old-hires']
                # if not link_jpg.endswith(('.jpg',)):
                #     link_jpg = dict(soup.find("div", id="imgTagWrapperId").find("img").attrs)['data-a-dynamic-image']
                # print '\nImage url:'
                # print '  ' + str(link_jpg)
                # sql_image = "update t_templet_amazon_collection_box set main_image_url ='%s' where id = %d" % (str(link_jpg), pri_key_id)
                # print sql_image
                # self.execute_sql(sql_image)

                image_dic = dict(soup.find("div", id="imgTagWrapperId").find("img").attrs)
                images = []
                if image_dic['src'].endswith(('.jpg',)):
                    images.append(image_dic['src'])
                if image_dic['data-old-hires'].endswith(('.jpg',)):
                    images.append(image_dic['data-old-hires'])
                image_match = re.findall('"(https?://.*?.jpg)"', image_dic['data-a-dynamic-image'])
                for ima in image_match:
                    images.append(ima)
                print images

                link_jpg = images[0]
                sql_image = "update t_templet_amazon_collection_box set main_image_url ='%s' where id = %d" % (str(link_jpg), pri_key_id)
                print sql_image
                self.execute_sql(sql_image)
                print "images len is "
                print len(images)
                if len(images) >= 2:
                    n = 0
                    for image in images:
                        n += 1
                        if n <= 8:
                            sql_image_other = "update t_templet_amazon_collection_box set other_image_url%d ='%s' where id = %d" % (n, str(image), pri_key_id)
                            print sql_image_other
                            self.execute_sql(sql_image_other)

                # 产品描述
                product_des_1 = ''
                descriptions = soup.find(self.has_child_p, id=re.compile("product.*description.*", re.IGNORECASE))
                print '\nProduct_description'
                if descriptions:
                    des = descriptions.find_all('p')
                    for des_ in des:
                        product_description = des_.get_text().strip().replace("'", '`')
                        if product_description == '':
                            continue
                        product_des_1 += product_description + '\n'
                    print 'product_des_1'
                    print product_des_1

                product_desc2 = ''
                details = soup.html.find(self.has_child_li_or_tr, id=re.compile("detail.*(bullets|feature).*", re.IGNORECASE))  # id=['detail_bullets_id', 'productDetails_feature_div', 'detail-bullets_feature_div']
                print '\nProduct_details:'
                #detail_descs = details.find_all(text=re.compile("sellers.*rank", re.IGNORECASE))
                detail_descs = details.find_all("li")
                if not detail_descs:
                    detail_descs = details.find_all("tr")
                for detai_des in detail_descs:
                    detail_each = detai_des.get_text().strip().replace('\n', ' ').replace("'", '`')
                    match_ = re.match('.*sellers.*rank.*', detail_each, re.IGNORECASE)
                    if match_:
                        product_desc2 += detail_each + '\n'
                        print detail_each
                print 'product_desc2'
                print product_desc2
                product_desc = product_des_1 + product_desc2
                product_desc = re.sub(' +', ' ', product_desc)
                product_desc = re.sub(pattern, '', product_desc)


                sql_product_desc = "update t_templet_amazon_collection_box set product_description ='%s' where id = %d" % (product_desc, pri_key_id)
                print sql_product_desc
                self.execute_sql(sql_product_desc)

                sql_status = "update t_templet_amazon_collection_box set collect_state ='1' where id = %d" % pri_key_id
                self.execute_sql(sql_status)
            else:
                sql_no_result = "update t_templet_amazon_collection_box set collect_state ='-1', collect_result ='feed back is null' where id = %d" % (pri_key_id)
                self.execute_sql(sql_no_result)
        except Exception as e:
            sql_except = "update t_templet_amazon_collection_box set collect_state ='-1', collect_result ='%s' where id = %d" % (str(e).replace("'", '`'), pri_key_id)
            print 'sql_except: %s' % sql_except
            self.execute_sql(sql_except)
            print e
            traceback.print_exc()

    def get_amazon_reverse_info(self, url, query_user, flag=1):
        if url is not None and url.strip() != '':
            if url.find('www.') < 0:
                url_mid = ' https://www.amazon.com/dp/' + url
            else:
                url_mid = url
            new_source_url = self.format_urls(url_mid)
        else:
            return
        print 'new_source_url is: %s' % new_source_url

        try:
            sql_insert = 'insert into t_templet_amazon_follow (url, query_user, query_time, img_url, title, second_category, price, crawl_result) value (%s, %s, %s, %s, %s, %s, %s,%s)'
            head = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10'}
            req = urllib2.Request(new_source_url, headers=head)
            data_bytes = urllib2.urlopen(req, timeout=30).read()
            print 'get data_bytes success'
            print data_bytes
            crawl_result = 'OK'

            if data_bytes is not None:
                soup = BeautifulSoup(data_bytes, "lxml")

                [style.extract() for style in soup.find_all('style')]
                [script.extract() for script in soup.find_all('script')]
                print datetime.datetime.now()

                # 图片
                try:
                    image_dic = dict(soup.find("div", id="imgTagWrapperId").find("img").attrs)
                    images = []
                    if image_dic['src'].endswith(('.jpg',)):
                        images.append(image_dic['src'])
                    if image_dic['data-old-hires'].endswith(('.jpg',)):
                        images.append(image_dic['data-old-hires'])
                    image_match = re.findall('"(https?://.*?.jpg)"', image_dic['data-a-dynamic-image'])
                    for ima in image_match:
                        images.append(ima)
                    image_url = images[0]
                    print 'Image_url: %s' % images[0]

                except Exception as pic_ex:
                    image_url = ''
                    crawl_result = 'Warn: failed to get image due to %s;' % pic_ex

                try:
                    # 店铺信息
                    shop_info = soup.find("a", id=["bylineInfo", "brand"]).get_text().strip().replace("'", '`')
                    pattern = '\\b' + shop_info + '\\b'
                    # 商品标题
                    title = soup.find("span", id="productTitle").get_text().strip().replace("'", '`')
                    title = re.sub(pattern, '', title)
                    print 'Title: %s' % title
                except Exception as title_ex:
                    title = ''
                    if crawl_result == 'OK':
                        crawl_result = 'Warn: failed to get title due to %s;' % title_ex
                    else:
                        crawl_result += 'failed to get title due to %s;' % title_ex

                # 二级类目
                try:
                    item_all_html = soup.find("div", id=["wayfinding-breadcrumbs_container"]).find_all('span', "a-list-item")
                    item_all = ''
                    second_category = ''
                    for idx, item in enumerate(item_all_html):
                        item_all += item.get_text().strip().replace("'", '`')
                        if idx == 2:
                            second_category = item.get_text().strip().replace("'", '`')
                    print 'item_all: %s' % item_all
                    print 'second_category: %s' % second_category
                except Exception as second_category_ex:
                    second_category = ''
                    if crawl_result == 'OK':
                        crawl_result = 'Warn: failed to get second_category due to %s;' % second_category_ex
                    else:
                        crawl_result += 'failed to get second_category due to %s;' % second_category_ex

                # 价格
                try:
                    price = soup.find("span", id=["priceblock_ourprice", "priceblock_saleprice"])
                    if not price:
                        price = soup.find("div", id=["buyNew_noncbb"])
                    price = price.get_text()
                    price = filter(lambda ch: ch in '0123456789.', str(price))
                    print 'price: %s' % price
                except Exception as price_ex:
                    price = ''
                    if crawl_result == 'OK':
                        crawl_result = 'Warn: failed to get price due to %s;' % price_ex
                    else:
                        crawl_result += 'failed to get price due to %s;' % price_ex
                data_tuple = (url, query_user, datetime.datetime.now(), image_url, title, second_category, price, crawl_result)

            else:
                print 'Warn: feed back is null'
                data_tuple = (url, query_user, datetime.datetime.now(), '', '', '', '', 'Warn: feed back is null')
        except Exception as ex:
            print traceback.print_exc()
            error_msg = 'Error: %s' % ex
            data_tuple = (url, query_user, datetime.datetime.now(), '', '', '', '', error_msg)
        print sql_insert
        with self.db_conn.cursor() as cursor:
            cursor.execute(sql_insert, data_tuple)
            self.db_conn.commit()

    def has_child_tag(self, tag):
        return tag.children is not None

    def has_child_p(self, tag):
        result = False
        if tag.name == 'div' and tag.descendants is not None:
            for child in tag.descendants:
                if child.name == 'p':
                    result = True
                    break
        return result

    def has_child_li_or_tr(self, tag):
        result = False
        if tag.name == 'div' and tag.descendants is not None:
            for child in tag.descendants:
                if child.name in  ('li', 'tr'):
                    result = True
                    break
        return result
