# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: amazon_image_modify.py
 @time: 2018-03-14 14:47
"""  
import oss2
from Project.settings import ACCESS_KEY_ID,ACCESS_KEY_SECRET,PREFIX,ENDPOINT,ENDPOINT_OUT,BUCKETNAME_ALL_MAINSKU_PIC


class ModifyImageBeforeUpload:
    def __init__(self):
        self.bucket_name = BUCKETNAME_ALL_MAINSKU_PIC
        self.auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        self.bucket = oss2.Bucket(self.auth, ENDPOINT, BUCKETNAME_ALL_MAINSKU_PIC)

    def upload_image_to_oss(self, shop_set, image_source, variation_type, image_type, parent_sku, child_sku, image_cnt):
        """
        :param image_source: 待上传的图片源
        :param variation_type: 主变体信息，parent表示主体，child表示变体
        :param image_type: main表示主图，other表示附图
        :param parent_sku: 主体sku
        :param child_sku: 变体sku
        :param image_cnt: 图片编号
        :return: oss图片链接
        """
        shopnames = shop_set.split('-')
        last_filename = shopnames[0] + '-' + shopnames[1] + '-' + shopnames[-1].split('/')[0]
        image_path = parent_sku + '/Amazon' + '/' + last_filename

        if image_type == 'main':
            if image_cnt == 0:
                image_index = ''
        else:
            image_index = '_' + str(image_cnt + 1)

        if variation_type == 'parent':
            image_name = parent_sku + image_index + '.jpg'
        else:
            image_name = parent_sku + '_' + child_sku + image_index + '.jpg'

        self.bucket.put_object(u'%s/%s' % (image_path, image_name), image_source)

        return PREFIX + self.bucket_name + '.' + ENDPOINT_OUT + '/' + image_path + '/' + image_name

