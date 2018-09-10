# coding=utf-8

"""
创建以shop_name命名的数据库表，并初始化该店铺的特征码和初始值
"""

import sys
import random

Letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
Numbers = ['0','1','2','3','4','5','6','7','8','9']
Characters = ['#','$','!','@',':','_','(',')','{','}']


class CreateShopTable(object):

    def __init__(self, cur, shop_name):
        self.cur = cur
        self.shop_name = shop_name

    def get_shop_exists(self):
        """
        判断待创建的shop_name是否已经在平台配置表内
        """
        try:
            sql = 'select id,  CurrentNum from t_all_plateform_code_shopname WHERE ShopName=%s'
            self.cur.execute(sql, (self.shop_name, ))
            shop_info = self.cur.fetchone()
            if shop_info:
                return {'error_code': 0, 'exists': True, 'current_num': shop_info[1]}
            else:
                return {'error_code': 0, 'exists': False}
        except Exception, e:
            error_info = '[get_shop_code] ex=%s LINE=%s' % (e, sys._getframe().f_lineno)
            return {'error_code': 20000, 'error_info': error_info}

    def get_max_type(self):
        """
        获取当前表格里最大的类型
        """
        try:
            sql = 'select TypeNum from t_all_plateform_code_shopname order by id desc limit 1'
            self.cur.execute(sql)
            info = self.cur.fetchone()
            if info:
                return {'error_code': 0, 'max_type': info[0]}
            else:
                return {'error_code': 0, 'max_type': 1}
        except Exception, e:
            error_info = '[get_max_type] ex=%s LINE=%s' % (e, sys._getframe().f_lineno)
            return {'error_code': -1, 'error_info': error_info}

    def generate_code(self, max_type):
        """
        生成新的特征码和初始值
        """
        try:
            if (max_type + 1) % 6 == 0:
                current_type = 6
            else:
                current_type = (max_type + 1) % 6
            if self.shop_name.split('-')[0] == 'ALI':
                current_type = random.sample([1, 4], 1)[0]
            length = random.randint(5, 10)
            initial_num = random.randint(100, 10000)
            code = self.random_code(current_type, length)
            return {'error_code': 0, 'initial_num': initial_num, 'code': code, 'current_type': current_type, 'length': length}
        except Exception, e:
            error_info = '[generate_code] ex=%s LINE=%s' % (e, sys._getframe().f_lineno)
            return {'error_code': -1, 'error_info': error_info}

    def random_code(self, type, length):
        """随机生成特征码"""
        resultList = []

        # 字母
        if type == 1:
            tempList = Letters
        # 特殊字符
        elif type == 2:
            tempList = Characters
        # 字母+特殊字符
        elif type == 3:
            tempList = Letters + Characters
        # 字母+数字
        elif type == 4:
            tempList = Letters + Numbers
        # 数字+特殊字符
        elif type == 5:
            tempList = Numbers + Characters
        # 字母+数字+特殊字符
        elif type == 6:
            tempList = Letters + Numbers + Characters

        for i in range(length):
            resultList.append(random.choice(tempList))
        result = ''.join(resultList)
        return result

    def create_table(self, initial_num):
        """
        创建shop_name对应的数据库表,并设置id从initial_num开始自增长
        KEY `idx_seq_wish_0001_1` (`RandomCode`) USING BTREE
        """
        try:
            table_name = 'seq_' + self.shop_name.replace('-', '_').lower()
            sql = 'CREATE TABLE seq.`%s` (' \
                  '`id` int(11) NOT NULL AUTO_INCREMENT,' \
                  '`RandomCode` varchar(64) NOT NULL,' \
                  '`ShopName` varchar(16) NOT NULL,`SKU` varchar(16) NOT NULL,' \
                  '`ShopSKU` varchar(32) NOT NULL DEFAULT "",' \
                  '`StaffName` varchar(16) NOT NULL,' \
                  '`InsertTime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,' \
                  'PRIMARY KEY (`id`)) ' \
                  'ENGINE=InnoDB AUTO_INCREMENT=%s DEFAULT CHARSET=utf8' % (table_name, initial_num)
            self.cur.execute(sql)
            self.cur.execute('commit; ')
            return {'error_code': 0}
        except Exception, e:
            error_info = '[create_table] ex=%s LINE=%s' % (e, sys._getframe().f_lineno)
            return {'error_code': -1, 'error_info': error_info}

    def insert_plateform_code(self, current_type, length, code, initial_num):
        """插入到店铺SKU特征编码表"""
        try:
            sql = 'insert into t_all_plateform_code_shopname(TypeNum, `Length`, ShopName, Code, InitialNum, CurrentNum) ' \
                  'VALUES (%s,%s,%s,%s,%s,%s)'
            params = (current_type, length, self.shop_name, code, initial_num, initial_num)
            self.cur.execute(sql, params)
            self.cur.execute("commit;")
            return {'error_code': 0}
        except Exception, e:
            error_info = '[insert_plateform_code] ex=%s LINE=%s' % (e, sys._getframe().f_lineno)
            return {'error_code': -1, 'error_info': error_info}


def create_shop_table(cur, shop_name):
    CreateShopTable_obj = CreateShopTable(cur=cur, shop_name=shop_name)
    get_shop_exists_info = CreateShopTable_obj.get_shop_exists()
    if get_shop_exists_info['error_code'] == 0 and get_shop_exists_info['exists'] == False:
        get_max_type_info = CreateShopTable_obj.get_max_type()
        if get_max_type_info['error_code'] == 0:
            max_type = get_max_type_info['max_type']
            generate_code_info = CreateShopTable_obj.generate_code(max_type=max_type)
            if generate_code_info['error_code'] == 0:
                initial_num, code = generate_code_info['initial_num'], generate_code_info['code']
                current_type, length = generate_code_info['current_type'], generate_code_info['length']
                create_table_info = CreateShopTable_obj.create_table(initial_num=initial_num)
                if create_table_info['error_code'] == 0:
                    insert_plateform_code_info = CreateShopTable_obj.insert_plateform_code(current_type=current_type, length=length, code=code, initial_num=initial_num)
                    if insert_plateform_code_info['error_code'] == 0:
                        return {'error_code': 0, 'shop_code': code}
                    else:
                        return insert_plateform_code_info
                else:
                    return create_table_info
            else:
                return generate_code_info
        else:
            return get_max_type_info
    elif get_shop_exists_info['error_code'] == 0 and get_shop_exists_info['exists'] == True:
        current_num = get_shop_exists_info['current_num']
        create_table_info = CreateShopTable_obj.create_table(current_num)
        return create_table_info
    else:
        return get_shop_exists_info
