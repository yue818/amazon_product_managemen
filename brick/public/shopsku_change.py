# coding=utf-8

import xlrd
import sys
from datetime import datetime
from django.db import connection
from pyapp.models import b_goodsskulinkshop



class ShopskuChange(object):
    def __init__(self, cur, staff_name, file_obj=None):
        self.cur = cur
        self.staff_name = staff_name
        self.file_obj = file_obj
        self.file_name = file_obj.name if file_obj else ''
        self.apply_type = 'CHANGE'

    def read_excel(self):
        if self.file_obj:
            try:
                data = xlrd.open_workbook(filename=None, file_contents=self.file_obj.read())
                table = data.sheets()[0]
                nrows = table.nrows
                sku_info_list = []
                for rownum in range(1, nrows):
                    row = table.row_values(rownum)
                    if row:
                        shop_name = str(row[0]).strip()[0:9]
                        unbind_sku = str(row[1]).strip()
                        shop_sku = str(row[2]).strip()
                        bind_sku = str(row[3]).strip()
                        sku_info_list.append([shop_name, unbind_sku, shop_sku, bind_sku])
                return {'error_code': 0, 'sku_info_list': sku_info_list}
            except Exception, e:
                error_info = '[read_excel] ex=%s LINE=%s' % (e, sys._getframe().f_lineno)
                return {'error_code': -1, 'error_info': error_info}
        else:
            return {'error_code': 10000, 'error_info': u'无效的导入文件'}


    def rebind_shopsku(self, unbind_sku, shop_sku, bind_sku):
        """
        修改绑定SKU信息，包括redis、绑定表、wish  online在线信息
        :param sku: 商品SKU
        :param shop_sku: 店铺sku
        :param shop_name: 店铺名
        """
        b_goodsskulinkshop_objs = b_goodsskulinkshop.objects.filter(SKU=unbind_sku, ShopSKU=shop_sku)
        if b_goodsskulinkshop_objs.exists():
            try:
                link_id = b_goodsskulinkshop_objs[0].NID
                current_flag = b_goodsskulinkshop_objs[0].Falg
                if (current_flag == 1) or (current_flag == 3) or (current_flag is None):
                    pass
                else:
                    return {'error_code': 10000, 'error_info': u'商品SKU：%s和店铺SKU：%s绑定关系处于尚未完成状态' % (unbind_sku, shop_sku)}
                # 修改linkshop表状态
                b_goodsskulinkshop_objs.update(Falg=2, SKU=bind_sku)
                return {'error_code': 0, 'link_id': link_id}
            except Exception, e:
                error_info = '[unbind_shopsku] ex=%s LINE=%s' % (e, sys._getframe().f_lineno)
                return {'error_code': -1, 'error_info': error_info}
        else:
            return {'error_code': 10000, 'error_info': u'未查到商品SKU：%s和店铺SKU：%s 绑定关系' % (unbind_sku, shop_sku)}


    def insert_log(self, shop_name, unbind_sku, shop_sku,  bind_sku, status, link_id=None, error_info=None, confirm_change=None):
        """
        将申请信息插入到log表
        :param sku: 商品SKU
        :param status: 申请结果
        :param shop_name: 店铺名
        :param shop_sku: 店铺sku
        :param error_info: 错误信息
        """
        try:
            apply_time = datetime.now()
            insert_log_sql = 'insert into py_db.t_log_sku_shopsku(ShopName, SKU, ShopSKU, StaffName, ApplyTime, Status, ' \
                             'ErrorInfo, ApplyType, UnbindFile, UnbindSku, linkId, ConfirmChange) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            self.cur.execute(insert_log_sql, (shop_name, bind_sku, shop_sku, self.staff_name, apply_time, status,
                                              error_info, self.apply_type, self.file_name, unbind_sku, link_id, confirm_change))
            self.cur.execute('commit; ')
            return {'error_code': 0}
        except Exception, e:
            error_info = '[insert_log] ex=%s LINE=%s' % (e, sys._getframe().f_lineno)
            return {'error_code': 20000, 'error_info': error_info}


def shopsku_change(staff_name, file_obj=None):
    """
    sku解绑
    :param staff_name: 解绑人
    :param staff_name: 待解绑的信息（如果是空列表，则为导入文件解绑）
    :param file_obj: 文件流
    """
    defeat_sku_list = []
    success_sku_list = []
    change_result = {'result': '', 'defeat_sku': '', 'success_sku': '', 'error_code': '', 'error_info': ''}

    cur = connection.cursor()
    ShopskuChange_obj = ShopskuChange(cur=cur, staff_name=staff_name, file_obj=file_obj)

    read_excel_info = ShopskuChange_obj.read_excel()
    if read_excel_info['error_code'] == 0:
        sku_info_list = read_excel_info['sku_info_list']
    else:
        change_result['result'] = 'DEFEAT'
        change_result['error_code'] = read_excel_info['error_code']
        change_result['error_info'] = read_excel_info['error_info']
        return change_result

    for sku_info in sku_info_list:
        shop_name = sku_info[0]
        unbind_sku = sku_info[1]
        shop_sku = sku_info[2]
        bind_sku = sku_info[3]

        rebind_shopsku_info = ShopskuChange_obj.rebind_shopsku(unbind_sku=unbind_sku, shop_sku=shop_sku, bind_sku=bind_sku)
        if rebind_shopsku_info['error_code'] == 0:
            success_sku_list.append([shop_name, unbind_sku, shop_sku, bind_sku])
            link_id = rebind_shopsku_info['link_id']
            ShopskuChange_obj.insert_log(shop_name=shop_name, unbind_sku=unbind_sku, shop_sku=shop_sku, bind_sku=bind_sku, status='CHANGESUCCESS', link_id=link_id, confirm_change=0)
        else:
            defeat_sku_list.append([shop_name, unbind_sku, shop_sku, bind_sku])
            error_info = rebind_shopsku_info['error_info']
            ShopskuChange_obj.insert_log(shop_name=shop_name, unbind_sku=unbind_sku, shop_sku=shop_sku, bind_sku=bind_sku, status='CHANGEDEFEAT', error_info=error_info)
    change_result['result'] = 'SUCCESS'
    change_result['defeat_sku'] = defeat_sku_list
    change_result['success_sku'] = success_sku_list
    return change_result