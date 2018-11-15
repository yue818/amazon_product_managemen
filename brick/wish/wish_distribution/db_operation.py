# coding=utf-8

"""
WISH铺货用到的数据库操作
"""

import sys
from datetime import datetime




class DbOperation(object):

    def __init__(self, cur):
        self.cur = cur

    def get_wait_open(self, id_tuple):
        """获取待展开的信息"""
        wait_open_list = []
        if len(id_tuple) > 1:
            sql = 'select id, MainSKU, Title, Description, Tags, ExtraImages, Variants, ShopSets, TimePlan, CoreWords, ' \
                  'CreateStaff, PostTime, MainImage from t_templet_wish_wait_upload where id in %s ' % str(id_tuple)
        else:
            sql = 'select id, MainSKU, Title, Description, Tags, ExtraImages, Variants, ShopSets, TimePlan, CoreWords, ' \
                  'CreateStaff, PostTime, MainImage from t_templet_wish_wait_upload where id=%s' % id_tuple[0]
        self.cur.execute(sql)
        infos = self.cur.fetchall()
        for info in infos:
            temp_dict = {
                'id': info[0], 'main_sku': info[1], 'title': info[2], 'description': info[3], 'tags': info[4],
                'extra_images': info[5], 'variants': info[6], 'shop_sets': info[7], 'time_plan': info[8],
                'core_words': info[9], 'create_staff': info[10], 'post_time': info[11], 'main_image': info[12]
            }
            wait_open_list.append(temp_dict)
        return {'error_code': 0, 'wait_open_list': wait_open_list}

    def get_core_list(self):
        """核心关键词库"""
        core_words_list = []
        sql = 'select CoreWords from t_product_corewords'
        self.cur.execute(sql)
        for each in self.cur.fetchall():
            core_words_list.append(each[0])
        return {'error_code': 0, 'core_words_list': core_words_list}

    def get_main_image(self, main_sku):
        """获取可作为主图的图片的列表"""
        main_image_list = []
        sql = 'select WishPic from t_product_mainsku_pic where MainSKU=\"%s\" AND Flag=1' % main_sku
        self.cur.execute(sql)
        image_infos = self.cur.fetchall()
        for image_info in image_infos:
            main_image_list.append(image_info[0])
        return {'error_code': 0, 'main_image_list': main_image_list}

    def insert_into_distribution_review(self, review_param):
        """将展开的铺货信息插入到铺货审核"""
        sql = 'insert into t_templet_wish_upload_review(MainSKU, ParentSKU, Title, Description, Tags, MainImage, ' \
              'ExtraImages, Variants, ShopName, Schedule, CoreWords, CreateStaff, CreateTime, PostStatus, ReviewStatus) ' \
              'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        self.cur.execute(sql, review_param)
        self.cur.execute('commit')
        return {'error_code': 0}

    def update_wait_upload(self, open_id):
        """更新待铺货的展开状态"""
        sql = 'update t_templet_wish_wait_upload set `Status`="YES" WHERE id=%s ' % open_id
        self.cur.execute(sql)
        self.cur.execute('commit')

    def get_distribution_info(self, id_tuple):
        wait_distribution_list = []
        if len(id_tuple) > 1:
            sql = 'select id, MainSKU, Title, Description, Tags, ExtraImages, Variants, ShopName, Schedule, ParentSKU, CreateStaff, PostTime, MainImage ' \
                  'from t_templet_wish_upload_review where id in %s ' % str(id_tuple)
        else:
            sql = 'select id, MainSKU, Title, Description, Tags, ExtraImages, Variants, ShopName, Schedule, ParentSKU, CreateStaff, PostTime, MainImage ' \
                  'from t_templet_wish_upload_review where id=%s' % id_tuple[0]
        self.cur.execute(sql)
        infos = self.cur.fetchall()
        for info in infos:
            temp_dict = {
                'id': info[0], 'main_sku': info[1], 'title': info[2], 'description': info[3], 'tags': info[4],
                'extra_images': info[5], 'variants': info[6], 'shop_name': info[7], 'schedule': info[8],
                'parent_sku': info[9], 'create_staff': info[10], 'post_time': info[11], 'main_image': info[12]
            }
            wait_distribution_list.append(temp_dict)
        return {'error_code': 0, 'wait_distribution_list': wait_distribution_list}

    def goods_exits_in_shop(self, main_sku, shop_name):
        """判断店铺是否已经上架该商品"""
        sql = 'select id from t_online_info_wish where ShopName=%s AND MainSKU=%s AND `Status`="Enabled"; '
        self.cur.execute(sql, (shop_name, main_sku))
        info = self.cur.fetchone()
        if info == None:
            return {'error_code': 0}
        else:
            return {'error_code': 10000, 'error_info': 'REPETITION'}

    def judge_exists_result(self, main_sku, shop_name):
        """判断待铺货的记录是否已经在铺货结果"""
        sql_1 = 'select id from t_templet_wish_upload_result where MainSKU=%s AND ShopName=%s AND Status="DEFEAT"; '
        sql_2 = 'select id from t_templet_wish_upload_result where MainSKU=%s AND ShopName=%s; '
        self.cur.execute(sql_1, (main_sku, shop_name))
        info_1 = self.cur.fetchall()
        self.cur.execute(sql_2, (main_sku, shop_name))
        info_2 = self.cur.fetchall()
        if (len(info_1) != 0) or (len(info_2) == 0):
            return True
        else:
            return False

    def insert_into_result(self, main_sku, pid, shopName, result_status, user, time, ScheduleTime=None, params=None, Parent_SKU=None, image=None):
        """插入到结果表"""
        sql = 'insert into t_templet_wish_upload_result(PID, MainSKU, ShopName, Submitter, InsertTime, MainImage, Status, Variants, ParentSKU, Schedule ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        if params != None:
            param = (pid, main_sku, shopName, user, time, image, result_status, str(params), Parent_SKU, ScheduleTime)
        else:
            param = (pid, main_sku, shopName, user, time, image, result_status, params, Parent_SKU, ScheduleTime)
        self.cur.execute(sql, param)
        id = int(self.cur.lastrowid)
        self.cur.execute('commit; ')
        return {'error_code': 0, 'result_id': id}

    def insert_into_schedule(self, shop_name, schedule_time, params, result_id):
        """插入到指令表"""
        time = datetime.now()
        sql = 'insert into t_api_schedule_ing_wish_upload(ShopName, PlatformName, CMDID, WishResultID, ScheduleTime,' \
              'InsertTime, Params, Processed, Successful, WithError, WithWarning, Status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        param = (shop_name, 'Wish', 'UPLOAD', result_id, schedule_time, time, str(params), 0, 0, 0, 0, 0)
        self.cur.execute(sql, param)
        self.cur.execute('commit')


