# coding=utf-8

"""
WISH主图更新数据库操作类
"""


from datetime import datetime


def connect_mysql():
    """
        连接MySQL数据库
        返回值：MySQL连接
    """
    import MySQLdb
    HOST = 'rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com'
    PORT = 3306
    USER = 'by15161458383'
    PASSWORD = 'K120Esc1'
    DB = 'hq_db'
    CHARSET = 'utf8'
    mysqlClient = MySQLdb.connect(host=HOST, port=PORT, user=USER, passwd=PASSWORD, db=DB, charset=CHARSET)
    return mysqlClient


class DbOperation(object):

    def __init__(self, cur):
        self.cursor = cur


    def get_updated_listing_pic(self):
        """
        获取最新更新的在线listing的图片链接，包括主图和副图
        返回值格式[[MainSKU, Image, ExtraImage1, ExtraImage2……]……]
        """
        sql_1 = 'select ProductID, MainSKU, Image from t_online_info_wish where DateUploaded >= DATE_ADD(UTC_DATE(), INTERVAL - 1 DAY) ' \
                'and MainSKU is not NULL and MainSKU != "" and MainSKU not like "%%,%%" AND MainSKU != "None" AND DataSources="NORMAL" ORDER BY DateUploaded DESC;'
        self.cursor.execute(sql_1)
        online_info_wish_objs = self.cursor.fetchall()
        all_sku_pic_list = []
        for obj in online_info_wish_objs:
            product_id = str(obj[0])
            main_sku = str(obj[1])
            main_image = str(obj[2])
            extra_image_list = []
            sql_2 = 'select ExtraImages from t_online_info WHERE ProductID=\"%s\"' % product_id
            self.cursor.execute(sql_2)
            online_info_obj = self.cursor.fetchone()
            if online_info_obj:
                extra_image_list = str(online_info_obj[0]).split('|')
            extra_image_list.insert(0, main_image)
            extra_image_list.insert(0, main_sku)
            all_sku_pic_list.append(extra_image_list)
        return all_sku_pic_list


    def get_exists_hashstr(self, main_sku):
        """根据mainSKU获取已经在图片库里的图片hash串"""
        hash_str_list = []
        sql = 'select HashStr from t_product_mainsku_pic where MainSKU=%s'
        self.cursor.execute(sql, (main_sku, ))
        hash_str_infos = self.cursor.fetchall()
        if hash_str_infos:
            for hash_str_info in hash_str_infos:
                hash_str_list.append(hash_str_info[0])
        return hash_str_list


    def insert_new_url(self, main_sku, wish_url, current_hash_str):
        """将不重复图片插入到图片库"""
        update_time = str(datetime.now())[:19]
        sql = 'insert into t_product_mainsku_pic(MainSKU, wishPic, UpdateTime ,HashStr) VALUES (%s, %s, %s, %s)'
        self.cursor.execute(sql, (main_sku, wish_url, update_time, current_hash_str))
        self.cursor.execute('commit; ')


    def sign_modify_update_flag(self, main_sku):
        """标志图片修改存在图片更新"""
        sql = 'update t_product_image_modify set UpdateFlag=1 WHERE MainSKU=%s;'
        self.cursor.execute(sql, (main_sku, ))
        self.cursor.execute('commit; ')


    def insert_image_modify(self, main_sku):
        """在图片维护表中新增一条记录"""
        try:
            sql = 'insert into t_product_image_modify(MainSKU, UpdateFlag) VALUES (%s, %s)'
            self.cursor.execute(sql, (main_sku, 1))
        except:
            sql = 'update t_product_image_modify set UpdateFlag=1 WHERE MainSKU=%s;'
            self.cursor.execute(sql, (main_sku, ))
        self.cursor.execute('commit; ')

