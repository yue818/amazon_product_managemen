# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: test1.py
 @time: 2018-05-11 13:19
"""
import traceback
import pymysql as MySQLdb
# Image XML
IMAGE_HEAD_XML = '''<?xml version="1.0" encoding="utf-8" ?>
<AmazonEnvelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="amznenvelope.xsd">
    <Header>
        <DocumentVersion>1.01</DocumentVersion>
        <MerchantIdentifier>SELLERID</MerchantIdentifier>
    </Header>
    <MessageType>ProductImage</MessageType>'''
IMAGE_BODY_XML = '''
    <Message>
        <MessageID>MESSAGENUM</MessageID>
        <OperationType>Update</OperationType>
        <ProductImage>
            <SKU>PRODUCTSKU</SKU>
            <ImageType>CHANGE_IMAGE_TYPE</ImageType>
            <ImageLocation>IMAGELOCALTIONURL</ImageLocation>
        </ProductImage>
    </Message>'''
IMAGE_FEET_XML = '''
</AmazonEnvelope>'''


DATABASES = {
    'NAME': 'hq_db',
    'HOST': 'rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com',
    'PORT': '3306',
    'USER': 'by15161458383',
    'PASSWORD': 'K120Esc1'
}

def get_images_new(db_connect, upload_id):
    """
    从t_templet_amazon_wait_upload表取主sku图片信息
    从t_templet_amazon_published_variation取变体sku图片信息
    若有变体则只上传变体图片，若无则上传主体图片
    返回sku图片字典，格式如下
    {'seller_sku':{'main_url':main_image_url, 'other_url1':other_url1,'other_url12:other_url2,……}}

    """
    cursor = db_connect.cursor()
    try:
        # 主体图片信息
        sql_main = "SELECT id, prodcut_variation_id, item_sku, productSKU, main_image_url, other_image_url1, other_image_url2, other_image_url3, other_image_url4, other_image_url5, other_image_url6, other_image_url7, other_image_url8, item_package_quantity,ShopSets FROM 	t_templet_amazon_wait_upload a WHERE 	id = %s" % upload_id
        cursor.execute(sql_main)
        main_image_info = cursor.fetchone()


        sql_variation = "SELECT 	id, prodcut_variation_id, child_sku, productSKU, main_image_url, other_image_url1, other_image_url2, other_image_url3, other_image_url4, other_image_url5, other_image_url6, other_image_url7, other_image_url8,item_quantity FROM 	t_templet_amazon_published_variation a WHERE prodcut_variation_id = %s" % \
                        main_image_info[1]
        cursor.execute(sql_variation)
        variation_image_info = cursor.fetchall()

        image_all_dic = {}
        if variation_image_info:  # 有变体则只上传变体图片
            for variation_image in variation_image_info:
                image_each_dic = {}
                for i in range(4, 13):
                    if variation_image[i]:
                        image_url_local = variation_image[i]
                        if i == 4:
                            image_each_dic['main_url'] = image_url_local
                        else:
                            image_each_dic['other_url' + str(i - 4)] = image_url_local
                if variation_image[13] is not None and variation_image[13] != '1':
                    image_all_dic[variation_image[2] + '*' + variation_image[13]] = image_each_dic
                else:
                    image_all_dic[variation_image[2]] = image_each_dic
        else:  # 无变体上传主体的图片
            image_each_dic = {}
            for i in range(4, 13):
                if main_image_info[i]:
                    image_url_local = main_image_info[i]
                    if i == 4:
                        image_each_dic['main_url'] = image_url_local
                    else:
                        image_each_dic['other_url' + str(i - 4)] = image_url_local
            if main_image_info[13] is not None and main_image_info[13] != '1':
                image_all_dic[main_image_info[2] + '*' + main_image_info[13]] = image_each_dic
            else:
                image_all_dic[main_image_info[2]] = image_each_dic

        return image_all_dic
    except Exception as e:
        print e
        traceback.print_exc()
        return None
    finally:
        cursor.close()


def get_image_xml_new(image_info, seller_id):
    try:
        num = 1
        image_xml = {}
        for key, value in image_info.items():
            for key_child in sorted(value.keys()):
                if key_child == 'main_url':
                    image_type = 'Main'
                else:
                    image_type = 'PT' + key_child[-1]
                image_url = value[key_child]
                image_xml[num] = IMAGE_BODY_XML
                image_xml[num] = image_xml[num].replace('MESSAGENUM', str(num))
                image_xml[num] = image_xml[num].replace('PRODUCTSKU', key)
                image_xml[num] = image_xml[num].replace('CHANGE_IMAGE_TYPE', image_type)
                image_xml[num] = image_xml[num].replace('IMAGELOCALTIONURL', image_url)
                num += 1

        image_complete_xml = ''
        image_complete_xml += IMAGE_HEAD_XML
        image_complete_xml = image_complete_xml.replace('SELLERID', seller_id)
        for i in image_xml:
            image_complete_xml += image_xml[i]
        image_complete_xml += IMAGE_FEET_XML
        return image_complete_xml
    except Exception as e:
        traceback.print_exc()

db_conn = MySQLdb.connect(DATABASES['HOST'], DATABASES['USER'], DATABASES['PASSWORD'], DATABASES['NAME'])
images = get_images_new(db_conn, 3817)
image_xml = get_image_xml_new(images, 'A1R7WBALNH6GA0')
print image_xml
db_conn.close()