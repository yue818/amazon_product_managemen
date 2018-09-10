# coding=utf-8

"""
类 ShopskuApply：申请和绑定店铺SKU
类 SKUProcess：处理sku信息，并判断sku合法性
"""


from django.db import connection
import time, sys
from random import randint
from datetime import datetime
from brick.public.create_shop_table import create_shop_table
from brick.classredis.classshopsku import classshopsku
from brick.public.combination_sku import G_ZHSKU
from django_redis import get_redis_connection
redis_coon = get_redis_connection(alias='product')
classshopsku_obj = classshopsku(db_conn=None, redis_conn=redis_coon)



class ShopskuApply(object):

    def __init__(self, cur, shop_name, staff_name, apply_type):
        self.cur = cur
        self.shop_name = u'%s' % shop_name.strip()
        self.shop_name_original = u'%s' % shop_name.strip()
        self.staff_name = staff_name
        self.apply_type = apply_type
        self.classshopsku_obj = classshopsku(db_conn=None, redis_conn=redis_coon)


    def get_shop_name_temp(self):
        """
        根据店铺名全称在配置文件内查找简称
        """
        try:
            shop_name_index_dict = {'Ali': 8, 'AMZ': 8, 'CDIS': 9, 'eBay': 9, 'JOOM': 12, 'Jumia': 10, 'LZD': 8,
                                    'Mall': 9, 'SHP': 7, 'Tanga': 10, 'Top': 8, 'UMKA': 9, 'Vova':9, 'Wish': 9
                                    }
            for key, val in shop_name_index_dict.items():
                if self.shop_name.startswith(key):
                    shop_name_temp = self.shop_name[: val]
                    self.shop_name = shop_name_temp
            return {'error_code': 0, 'shop_name_temp': shop_name_temp}
        except Exception, e:
            error_info = '[get_shop_name_temp] ex=%s LINE=%s' % (e, sys._getframe().f_lineno)
            return {'error_code': 10000, 'error_info': error_info}

    def get_shop_code(self):
        """
        根据店铺获取店铺的特征码,并盘算seq数据库中是否有该店铺的表
        """
        try:
            select_table_exists_sql = 'select `table_name` from `information_schema`.`tables` where `table_schema`="seq" and `table_name`=%s'
            self.cur.execute(select_table_exists_sql, ('seq_' + self.shop_name.replace('-', '_').lower(), ))
            table_exists_info = self.cur.fetchone()

            select_shop_code_sql = 'select code from t_all_plateform_code_shopname WHERE ShopName=%s; '
            self.cur.execute(select_shop_code_sql, (self.shop_name, ))
            shop_code_info = self.cur.fetchone()

            # 店铺seq表存在，能查询到店铺特征码
            if shop_code_info and table_exists_info:
                shop_code = shop_code_info[0]
                return {'error_code': 0, 'shop_code': shop_code}
            # 店铺seq表不存在，能查询到店铺特征码
            elif shop_code_info and (not table_exists_info):
                shop_code = shop_code_info[0]
                return {'error_code': 30000, 'shop_code': shop_code}
            else:
                return {'error_code': 10000, 'error_info': u'未查询到店铺：%s 的配置文件' % self.shop_name}
        except Exception, e:
            error_info = '[get_shop_code] ex=%s LINE=%s' % (e, sys._getframe().f_lineno)
            return {'error_code': 20000, 'error_info': error_info}

    def get_random_code(self):
        """
        生成随机码，用于特异性标识每条插入信息
        :return: 随机码（生成规则：‘unix 13位时间戳字符串’.‘五位随机数字符串，不足前面补零’.‘五位随机数字符串，不足前面补零’）
        """
        try:
            unix_time = str(int(time.time() * 1000))
            first_random = str(randint(0, 99999)).zfill(5)
            second_random = str(randint(0, 99999)).zfill(5)
            random_code = '.'.join([unix_time, first_random, second_random])
            return {'error_code': 0, 'random_code': random_code}
        except Exception, e:
            error_info = '[get_random_code] ex=%s  __LINE__=%s' % (e, sys._getframe().f_lineno)
            return {'error_code': 99999, 'error_info': error_info}

    def insert_seq(self, random_code, sku):
        """
        将生成的随机码以及绑定信息插入到对应店铺的seq表中
        :param random_code: 随机码
        :param sku: 商品SKU
        """
        try:
            table_name = 'seq_' + self.shop_name.replace('-', '_').lower()
            insert_seq_sql = 'insert into seq.%s(RandomCode, ShopName, SKU, StaffName) ' \
                             'VALUES (\"%s\", \"%s\", \"%s\", \"%s\")' % \
                             (table_name,  random_code, self.shop_name, sku, self.staff_name)
            self.cur.execute(insert_seq_sql)
            insert_id = int(self.cur.lastrowid)
            self.cur.execute('commit;')
            return {'error_code': 0, 'insert_id': insert_id}
        except Exception, e:
            error_info = '[insert_seq] ex=%s LINE=%s' % (e, sys._getframe().f_lineno)
            return {'error_code': 20000, 'error_info': error_info}

    def insert_log(self, sku, status, random_code=None, shop_sku=None, error_info=None):
        """
        将申请信息插入到log表
        :param sku: 商品SKU
        :param status: 申请结果
        :param random_code: 随机码
        :param shop_sku: 店铺sku
        :param error_info: 错误信息
        """
        try:
            apply_time = datetime.now()
            insert_log_sql = 'insert into py_db.t_log_sku_shopsku(RandomCode, ShopName, SKU, ShopSKU, StaffName, ' \
                             'ApplyTime, Status, ErrorInfo, ApplyType) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
            self.cur.execute(insert_log_sql, (random_code, self.shop_name_original, sku, shop_sku, self.staff_name, apply_time,
                                              status, error_info, self.apply_type))
            self.cur.execute('commit; ')
            return {'error_code': 0}
        except Exception, e:
            error_info = '[insert_log] ex=%s LINE=%s' % (e, sys._getframe().f_lineno)
            return {'error_code': 20000, 'error_info': error_info}

    def insert_link(self, sku, shop_sku, flag=0):
        try:
            insert_link_sql = 'insert into py_db.b_goodsskulinkshop(SKU, ShopSKU, Memo, PersonCode, Falg) ' \
                              'VALUES (%s, %s, %s, %s, %s)'
            self.cur.execute(insert_link_sql, (sku, shop_sku, self.shop_name_original, self.staff_name, flag))
            self.cur.execute('commit; ')
            return {'error_code': 0}
        except Exception, e:
            error_info = '[insert_link] ex=%s LINE=%s' % (e, sys._getframe().f_lineno)
            return {'error_code': 20000, 'error_info': error_info}



class SKUProcess(object):

    def __init__(self, cur, input_sku, file_type, first_name):
        self.cur = cur
        self.input_sku = input_sku
        self.file_type = file_type
        self.defeat_sku_info = {}
        self.first_name = first_name

    def sku_process(self):
        """
        读取excel中的sku信息
        :return:
        """
        try:
            codetype = ['|', '，', ',']
            coty = ','
            for code in codetype:
                if self.input_sku.find(code) != -1:
                    coty = code
            templist = self.input_sku.replace('\n', '').replace('\r', '').replace('\r\n', '').replace(' ', '').split(coty)
            templist = [temp.strip() for temp in templist if temp.strip()]
        except Exception, e:
            error_info = '[sku_process] ex=%s LINE=%s' % (e, sys._getframe().f_lineno)
            return {'error_code': -1, 'error_info': error_info}

        all_sku_list = []
        if self.file_type == 'SONSKUAPPLY':
            for son_sku in templist:
                judge_sku_exists_info = self.judge_sku_exists(sku=son_sku)
                if judge_sku_exists_info['error_code'] == 0:
                    all_sku_list.append(son_sku)
        elif self.file_type == 'MAINSKUAPPLY':
            for main_sku in templist:
                son_sku_info = self.get_son_sku(main_sku=main_sku)
                if son_sku_info['error_code'] == 0:
                    all_sku_list += son_sku_info['sku_list']
        elif self.file_type == 'GROUPSKUAPPLY':
            for cskuset in templist:
                if cskuset.find('+') == -1 and cskuset.startswith('ZH'):
                    all_sku_list.append(cskuset)
                else:
                    ZHSKU_dict = G_ZHSKU(cskuset, connection, self.first_name, '', datetime.now())
                    ZHSKU = ZHSKU_dict.get('ZHSKU', '')
                    all_sku_list.append(ZHSKU)
        return {'error_code': 0, 'all_sku_list': all_sku_list}

    def judge_sku_exists(self, sku):
        """
        判断sku是否在普源信息里能查到，即该SKU存不存在
        :param sku: 子SKU
        """
        try:
            sql = 'select nid from py_db.b_goods WHERE SKU=%s; '
            self.cur.execute(sql, (sku, ))
            sku_info = self.cur.fetchone()
            if sku_info:
                return {'error_code': 0}
            else:
                self.defeat_sku_info[sku] = u'未查到商品SKU：%s' % sku
                return {'error_code': 10000}
        except Exception, e:
            error_info = '[judge_son_sku_exists] ex=%s LINE=%s' % (e, sys._getframe().f_lineno)
            self.defeat_sku_info[sku] = error_info
            return {'error_code': 20000, 'error_info': error_info}

    def get_son_sku(self, main_sku):
        """
        根据主SKU到普源查询子SKU信息
        :param main_sku: 主SKU
        """
        try:
            sql = 'select SKU from py_db.b_goods WHERE SKU like \"%s%%\"; ' % main_sku
            self.cur.execute(sql)
            sku_infos = self.cur.fetchall()
            sku_list = []
            if sku_infos:
                for sku_info in sku_infos:
                    sku_list.append(sku_info[0])
            if sku_list:
                return {'error_code': 0, 'sku_list': sku_list}
            else:
                self.defeat_sku_info[main_sku] = u'未查到主SKU：%s' % main_sku
                return {'error_code': 10000, 'error_info': u'未查到主SKU：%s' % main_sku}
        except Exception, e:
            error_info = '[get_son_sku] ex=%s LINE=%s' % (e, sys._getframe().f_lineno)
            self.defeat_sku_info[main_sku] = error_info
            return {'error_code': 20000, 'error_info': error_info}


def change_global_result(result_info=None, result='DEFEAT', defeat_sku=None, success_sku=None):
    """
    改变全局变量 店铺SKU申请结果
    """
    shopsku_apply_result = {'result': '', 'defeat_sku': '', 'success_sku': '', 'error_code': '', 'error_info': ''}

    if result == 'DEFEAT':
        shopsku_apply_result['result'] = result
        shopsku_apply_result['error_code'] = result_info['error_code']
        shopsku_apply_result['error_info'] = result_info['error_info']
    else:
        shopsku_apply_result['result'] = result
        shopsku_apply_result['defeat_sku'] = defeat_sku
        shopsku_apply_result['success_sku'] = success_sku
    return shopsku_apply_result


def shopsku_apply(input_sku, shop_name, apply_type="SONSKUAPPLY", first_name="UPLOAD"):
    cur = connection.cursor()
    defeat_sku_info = {}
    success_sku_info = {}
    shopsku_apply_result = {'result': '', 'defeat_sku': '', 'success_sku': '', 'error_code': '', 'error_info': ''}
    ShopskuApply_obj = ShopskuApply(cur=cur, shop_name=shop_name, staff_name=first_name, apply_type=apply_type)
    shop_name_temp_info = ShopskuApply_obj.get_shop_name_temp()     # 查询店铺名简写
    if shop_name_temp_info['error_code'] == 0:
        shop_name_temp = shop_name_temp_info['shop_name_temp']
        shop_code_info = ShopskuApply_obj.get_shop_code()   # 获取该店铺的特征码
        shop_code = ''
        table_exists = False
        # 存在店铺特征码、店铺seq表
        if shop_code_info['error_code'] == 0:
            shop_code = shop_code_info['shop_code']
            table_exists = True
        # 存在店铺特征码，不存在店铺seq表
        elif shop_code_info['error_code'] == 30000:
            shop_code = shop_code_info['shop_code']
            create_shop_table_info = create_shop_table(cur=cur, shop_name=shop_name_temp)
            if create_shop_table_info['error_code'] == 0:
                table_exists = True
            else:
                shopsku_apply_result = change_global_result(result_info=create_shop_table_info, result='DEFEAT')
        # 不存在店铺特征码、店铺seq表
        elif shop_code_info['error_code'] == 10000:
            create_shop_table_info = create_shop_table(cur=cur, shop_name=shop_name_temp)
            if create_shop_table_info['error_code'] == 0:
                shop_code = create_shop_table_info['shop_code']
                table_exists = True
            else:
                shopsku_apply_result = change_global_result(result_info=create_shop_table_info, result='DEFEAT')
        else:
            shopsku_apply_result = change_global_result(result_info=shop_code_info, result='DEFEAT')
        if shop_code and table_exists:           # 如果查询到店铺特征码，并且店铺seq表存在，则进行处理SKU文件
            SKUProcess_obj = SKUProcess(cur=cur, input_sku=input_sku, file_type=apply_type, first_name=first_name)
            sku_process_info = SKUProcess_obj.sku_process()
            defeat_sku_info = SKUProcess_obj.defeat_sku_info
            if sku_process_info['error_code'] == 0:
                all_sku_list = sku_process_info['all_sku_list']
                for sku in all_sku_list:
                    get_random_code_info = ShopskuApply_obj.get_random_code()
                    if get_random_code_info['error_code'] == 0:
                        random_code = get_random_code_info['random_code']
                        insert_seq_info = ShopskuApply_obj.insert_seq(random_code=random_code, sku=sku)
                        if insert_seq_info['error_code'] == 0:
                            insert_id = insert_seq_info['insert_id']
                            shop_sku = shop_code + str(insert_id)
                            ShopskuApply_obj.insert_log(sku=sku, status='APPLYSUCCESS', random_code=random_code, shop_sku=shop_sku)
                            insert_link_info = ShopskuApply_obj.insert_link(sku=sku, shop_sku=shop_sku)
                            if insert_link_info['error_code'] == 0:
                                success_sku_info[shop_sku] = sku
                                # 写入redis
                                classshopsku_obj.setSKU(shopsku=shop_sku, sku=sku)
                            else:
                                defeat_sku_info[sku] = insert_link_info['error_info']
                        else:
                            defeat_sku_info[sku] = insert_seq_info['error_info']
                    else:
                        defeat_sku_info[sku] = get_random_code_info['error_info']
                shopsku_apply_result = change_global_result(result='SUCCESS', defeat_sku=defeat_sku_info, success_sku=success_sku_info)
            else:
                shopsku_apply_result = change_global_result(result_info=sku_process_info, result='DEFEAT')
    else:
        shopsku_apply_result = change_global_result(result_info=shop_name_temp_info, result='DEFEAT')
    for k, v in defeat_sku_info.items():
        ShopskuApply_obj.insert_log(sku=k, status='APPLYDEFEAT', error_info=v)  # 将错误的sku信息插入到log表
    cur.close()
    return shopsku_apply_result


"""
参数:
input_sku: 英文逗号拼接的商品SKU字符串;
shop_name: 店铺名;
apply_type: 申请类型(非必须, 默认SONSKUAPPLY,可选值:MAINSKUAPPLY: 主SKU申请, SONSKUAPPLY: 子SKU申请, GROUPSKUAPPLY: 组合SKU申请);
first_name: 铺货人(非必须, 默认UPLOAD)

返回值:
shopsku_apply_result格式：字典
shopsku_apply_result = {
    'result': SUCCESS或者DEFEAT,
    'defeat_sku': {
                    参数SKU: 失败原因
                    ……
                    },
    'success_sku': {
                    生成的ShopSKU: 参数SKU
                    ……
                    },
    'error_code': 错误返回码,
    'error_info': 错误信息
}
"""

