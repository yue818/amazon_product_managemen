# coding=utf-8

from brick.pydata.py_syn.public import public
import pymssql
from django.db import connection
from skuapp.table.t_product_information_modify import t_product_information_modify
from datetime import datetime
from brick.table.t_operation_log_online_syn_py import t_operation_log_online_syn_py as operation_log
from brick.pydata.py_syn.py_conn import py_conn
pyconn_obj = py_conn()
public_obj = public()
operation_log_obj = operation_log(DBConn=connection)


GOODSSTATUS_DICT = {
    u'清仓下架(需审核)': u'清仓',
    u'售完下架(需审核)': u'售完下架',
    u'处理库尾(需审核)': u'处理库尾',
    u'清仓（合并）': u'清仓（合并）',
    u'停售': u'停售',
    u'清仓（合并）(需审核)': u'清仓（合并）',
    u'停售(需审核)': u'停售',
    u'临时下架': u'临时下架',
    u'重新上架': u'正常',
    u'清仓下架(无需审核)': u'清仓',
    u'停售(无需审核)': u'停售',
    u'清仓': u'清仓',
    u'售完下架': u'售完下架'
}


def merge_sku(details, apply_name, conn_result, modify_id, first_name):
    delete_list = []
    update_sku_link_shop_list = []
    for detail in details:
        delete_sku = detail['delete_sku']
        retain_sku = detail['retain_sku']
        describe = detail['describe']

        single_delete_temp_dict = {
            'SKU': delete_sku, 'columnname': 'GoodsStatus', 'columnvalue': u'清仓（合并）',
            'describe': describe,'apply_name': apply_name
        }
        delete_list.append(single_delete_temp_dict)
        single_update_temp_dict = {
            'delete_sku': delete_sku, 'retain_sku': retain_sku, 'opflag': 'update'
        }
        update_sku_link_shop_list.append(single_update_temp_dict)

    # 待合并SKU修改为清仓（合并）状态
    modify_result = public_obj.b_goods_modify_to_pydb(b_goods_data_list=delete_list, sqlserverInfo=conn_result, pydb_connect=connection)
    if modify_result['errorcode'] == 0:
        # 修改绑定关系
        goodsskulinkshop_result = public_obj.goodsskulinkshop_info_to_pydb(b_goodsskulinkshop_data_list=update_sku_link_shop_list, sqlserverInfo=conn_result)
        if goodsskulinkshop_result['errorcode'] == 0:
            t_product_information_modify.objects.filter(id=modify_id).update(Mstatus="WCXG", XGTime=datetime.now(), XGStaffName=first_name)
            status = 'over'
            error_info = str(details)
        else:
            status = 'error'
            error_info = goodsskulinkshop_result['errortext']
    else:
        status = 'error'
        error_info = modify_result['errortext']
    return status, error_info


def online_modify_puyuan(modify_data_list, first_name, opnum):
    import time
    time.sleep(1)
    try:
        conn_result = pyconn_obj.py_conn_database()
        sqlserver_cursor = conn_result['py_cursor']

        for modify_data in modify_data_list:
            modify_status = modify_data['modify_status']
            modify_id = modify_data['modify_id']
            details = modify_data['details']
            main_sku = modify_data['main_sku']
            apply_name = modify_data['apply_name']
            select = modify_data.get('select', '')

            if sqlserver_cursor:
                single_data_list = []
                if modify_status == "DXG":
                    if details:
                        if select == '7':
                            status, error_info = merge_sku(details, apply_name, conn_result, modify_id, first_name)
                        else:
                            for k1, v1 in details.items():
                                for k2, v2 in v1.items():
                                    if k2 == 'BmpUrl':
                                        continue
                                    if k2 == 'GoodsStatus':
                                        column_value = GOODSSTATUS_DICT[v2[2]]
                                    else:
                                        column_value = v2[2].strip() if v2[2] else ''
                                    product_modify_dict = {
                                        'SKU': k1, 'columnname': k2, 'columnvalue': column_value, 'describe': v2[3],
                                        'apply_name': apply_name
                                    }
                                    single_data_list.append(product_modify_dict)

                            result = public_obj.b_goods_modify_to_pydb(b_goods_data_list=single_data_list, sqlserverInfo=conn_result, pydb_connect=connection)
                            if result['errorcode'] == 0:
                                t_product_information_modify.objects.filter(id=modify_id).update(Mstatus="WCXG", XGTime=datetime.now(),XGStaffName=first_name)
                                status = 'over'
                                error_info = str(single_data_list)
                            else:
                                status = 'error'
                                error_info = result['errortext']
                    else:
                        status = 'error'
                        error_info = 'id: %s的修改信息为空!!!' % modify_id
                else:
                    status = 'error'
                    error_info = '主SKU:%s非待修改状态，不可同步普源' % main_sku
            else:
                status = 'error'
                error_info = u'普源数据库连接失败'
            ooResult = operation_log_obj.updateStatusP(opnum=opnum, opkey=main_sku, status=status, elogs=error_info)
            assert ooResult['errorcode'] == 0, ooResult['errortext']
        pyconn_obj.py_close_conn_database()
    except Exception, e:
        print '1111111111--------%s' % e