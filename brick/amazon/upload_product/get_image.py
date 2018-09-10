# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: get_image.py
 @time: 2018-05-04 16:55
"""
import tracebac

def get_images_new(self, db_connect, upload_id):
    """
    从t_templet_amazon_wait_upload表取主sku图片信息
    从t_templet_amazon_published_variation取变体sku图片信息
    若有变体则只上传变体图片，若无则上传主体图片
    返回sku图片字典，格式如下
    {'seller_sku':{'main_url':main_image_url, 'other_url1':other_url1,'other_url12:other_url2,……}}

    """
    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, ENDPOINT_OUT, BUCKETNAME_APIVERSION)
    cursor = db_connect.cursor()
    try:
        # 主体图片信息
        sql_main = "SELECT id, prodcut_variation_id, item_sku, productSKU, main_image_url, other_image_url1, other_image_url2, other_image_url3, other_image_url4, other_image_url5, other_image_url6, other_image_url7, other_image_url8, item_package_quantity,ShopSets FROM 	t_templet_amazon_wait_upload a WHERE 	id = %s" % upload_id
        cursor.execute(sql_main)
        main_image_info = cursor.fetchone()

        image_path = LOCAL_PATH  # 本地图片根目录
        # is_path_exist = os.path.exists(image_path)
        # if not is_path_exist:
        #     os.makedirs(image_path)
        # 变体图片信息
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
                        image_url = variation_image[i].split('/', 3)[-1]
                        code = self.random_code()
                        image_url_local = code + '.' + variation_image[i].split('.')[-1]
                        bucket.get_object_to_file(image_url, image_path + image_url_local)
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
                    image_url = main_image_info[i].split('/', 3)[-1]
                    code = self.random_code()
                    image_url_local = code + '.' + main_image_info[i].split('.')[-1]
                    bucket.get_object_to_file(image_url, image_path + image_url_local)
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
        logger.error('get_image_new: traceback.format_exc():\n%s' % traceback.format_exc())
        return None
    finally:
        cursor.close()

images = get_images_new(db_conn, amazon_upload_id)
image_xml = get_image_xml_new(images, auth_info['SellerId'])