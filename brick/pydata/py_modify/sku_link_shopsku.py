# coding=utf-8

from datetime import datetime
from brick.pydata.py_syn.public import public
from brick.table.t_operation_log_online_syn_py import t_operation_log_online_syn_py
from brick.pydata.py_syn.py_conn import py_conn
from pyapp.models import b_goodsskulinkshop, t_log_sku_shopsku_change
from brick.classredis.classshopsku import classshopsku
from django.db import connection
from django_redis import get_redis_connection
redis_coon = get_redis_connection(alias='product')




def get_param(sku_link_data, opflag):
    """获取SKU绑定参数"""
    sku = sku_link_data['sku']
    shop_sku = sku_link_data['shop_sku']
    memo = sku_link_data['memo']
    person_code = sku_link_data['person_code']
    shop_name = sku_link_data['shop_name']

    b_goodsskulinkshop_data_list = []
    if shop_sku is not None and shop_sku.strip() != '':
        for shoptmp in shop_sku.split('+'):
            shopsku = shoptmp.split('\\\\')[0].split('*')[0]
            temp_dict = {
                'SKU': sku, 'ShopSKU': shopsku, 'Memo': deal_illegal_char(memo),
                'PersonCode': deal_illegal_char(person_code),
                'opflag': opflag, 'ShopName': deal_illegal_char(shop_name)
            }
            b_goodsskulinkshop_data_list.append(temp_dict)
    return b_goodsskulinkshop_data_list


def deal_illegal_char(illegal_char):
    try:
        normal_char = illegal_char.replace('\u0000', '').replace('\x00', '')
    except:
        normal_char = illegal_char
    return normal_char


def online_sku_binding_add_puyuan(sku_link_data_list, opnum):
    """新增普源SKU绑定信息"""
    operation_log_obj = t_operation_log_online_syn_py(DBConn=connection)
    start_time = end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    aNum = len(sku_link_data_list)
    rNum = 0
    eNum = 0
    operation_log_obj.update_banding_schedue(opnum, start_time, end_time, aNum, rNum, eNum)

    public_obj = public()
    pyconn_obj = py_conn()
    conn_result = pyconn_obj.py_conn_database()
    sqlserver_cursor = conn_result['py_cursor']
    success_add_id_list = []
    i = 0
    for sku_link_data in sku_link_data_list:
        if sqlserver_cursor:
            b_goodsskulinkshop_data_list = get_param(sku_link_data=sku_link_data, opflag='add')
            result = public_obj.goodsskulinkshop_info_to_pydb(
                b_goodsskulinkshop_data_list=b_goodsskulinkshop_data_list, sqlserverInfo=conn_result
            )
            if result['errorcode'] == 0:
                success_add_id_list.append(sku_link_data['id'])
                rNum += 1
            else:
                eNum += 1
        else:
            eNum += 1
        operation_log_obj.update_banding_schedue(opnum, start_time, end_time, aNum, rNum, eNum)
        i += 1
        if i == 100:
            b_goodsskulinkshop.objects.filter(NID__in=success_add_id_list).update(Falg=1)
            i = 0
            success_add_id_list = []
    b_goodsskulinkshop.objects.filter(NID__in=success_add_id_list).update(Falg=1)
    pyconn_obj.py_close_conn_database()

    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    endFlag = 1
    operation_log_obj.update_banding_schedue(opnum, start_time, end_time, aNum, rNum, eNum, endFlag)

# def online_sku_binding_add_puyuan(sku_link_data_list, opnum):
#     """新增普源SKU绑定信息"""
#     public_obj = public()
#     operation_log_obj = t_operation_log_online_syn_py(DBConn=connection)
#     pyconn_obj = py_conn()
#     conn_result = pyconn_obj.py_conn_database()
#     sqlserver_cursor = conn_result['py_cursor']
#     success_add_id_list = []
#     i = 0
#     for sku_link_data in sku_link_data_list:
#         shop_sku = sku_link_data['shop_sku']
#         if sqlserver_cursor:
#             b_goodsskulinkshop_data_list = get_param(sku_link_data=sku_link_data, opflag='add')
#             result = public_obj.goodsskulinkshop_info_to_pydb(
#                 b_goodsskulinkshop_data_list=b_goodsskulinkshop_data_list, sqlserverInfo=conn_result
#             )
#             if result['errorcode'] == 0:
#                 status = 'over'
#                 error_info = str(b_goodsskulinkshop_data_list)
#                 success_add_id_list.append(sku_link_data['id'])
#             else:
#                 status = 'error'
#                 error_info = result['errortext']
#         else:
#             status = 'error'
#             error_info = u'普源数据库连接失败'
#         ooResult = operation_log_obj.updateStatusP(opnum=opnum, opkey=shop_sku, status=status, elogs=error_info)
#         assert ooResult['errorcode'] == 0, ooResult['errortext']
#         i += 1
#         if i == 100:
#             b_goodsskulinkshop.objects.filter(NID__in=success_add_id_list).update(Falg=1)
#             i = 0
#             success_add_id_list = []
#     b_goodsskulinkshop.objects.filter(NID__in=success_add_id_list).update(Falg=1)
#     pyconn_obj.py_close_conn_database()



def online_sku_binding_delete_puyuan(sku_link_data_list, opnum):
    """删除普源SKU绑定信息"""
    public_obj = public()
    operation_log_obj = t_operation_log_online_syn_py(DBConn=connection)
    pyconn_obj = py_conn()
    conn_result = pyconn_obj.py_conn_database()
    sqlserver_cursor = conn_result['py_cursor']

    success_delete_id_list = []
    success_delete_nid_list = []
    for sku_link_data in sku_link_data_list:
        shop_sku = sku_link_data['shop_sku']
        if sqlserver_cursor:
            b_goodsskulinkshop_data_list = get_param(sku_link_data=sku_link_data, opflag='delete')
            result = public_obj.goodsskulinkshop_info_to_pydb(
                b_goodsskulinkshop_data_list=b_goodsskulinkshop_data_list, sqlserverInfo=conn_result
            )
            if result['errorcode'] == 0:
                status = 'over'
                error_info = str(b_goodsskulinkshop_data_list)
                success_delete_id_list.append(sku_link_data['id'])
                success_delete_nid_list.append(sku_link_data['link_id'])
            else:
                status = 'error'
                error_info = result['errortext']
        else:
            status = 'error'
            error_info = u'普源数据库连接失败'
        ooResult = operation_log_obj.updateStatusP(opnum=opnum, opkey=shop_sku, status=status, elogs=error_info)
        assert ooResult['errorcode'] == 0, ooResult['errortext']
    t_log_sku_shopsku_change.objects.filter(id__in=success_delete_id_list).update(Status='DELETED')
    b_goodsskulinkshop.objects.filter(NID__in=success_delete_nid_list).delete()
    pyconn_obj.py_close_conn_database()


def online_sku_binding_modify_puyuan(sku_link_data_list, opnum):
    """修改普源SKU绑定信息"""
    public_obj = public()
    operation_log_obj = t_operation_log_online_syn_py(DBConn=connection)
    pyconn_obj = py_conn()
    conn_result = pyconn_obj.py_conn_database()
    sqlserver_cursor = conn_result['py_cursor']

    for sku_link_data in sku_link_data_list:
        old_sku = sku_link_data['old_sku']
        new_sku = sku_link_data['new_sku']
        shop_sku = sku_link_data['shop_sku']
        person_code = sku_link_data['person_code']
        memo = sku_link_data['memo']
        shop_name = sku_link_data['shop_name']
        if sqlserver_cursor:
            delete_data_dict = {'sku': old_sku, 'shop_sku': shop_sku, 'person_code': person_code, 'memo': memo, 'shop_name': shop_name}
            add_data_dict = {'sku': new_sku, 'shop_sku': shop_sku, 'person_code': person_code, 'memo': memo, 'shop_name': shop_name}
            b_goodsskulinkshop_data_delete_list = get_param(sku_link_data=delete_data_dict, opflag='delete')
            b_goodsskulinkshop_data_add_list = get_param(sku_link_data=add_data_dict, opflag='add')

            delete_result = public_obj.goodsskulinkshop_info_to_pydb(
                b_goodsskulinkshop_data_list=b_goodsskulinkshop_data_delete_list, sqlserverInfo=conn_result
            )
            if delete_result['errorcode'] == 0:
                add_result = public_obj.goodsskulinkshop_info_to_pydb(
                    b_goodsskulinkshop_data_list=b_goodsskulinkshop_data_add_list, sqlserverInfo=conn_result
                )
                if add_result['errorcode'] == 0:
                    status = 'over'
                    error_info = str(delete_data_dict) + str(add_data_dict)
                    link_id = sku_link_data['id']
                    b_goodsskulinkshop.objects.filter(NID=link_id).update(Falg=3, SKU=new_sku)

                    shop_code_list = (u'{}'.format(delete_data_dict['memo'])).split('-')
                    if len(shop_code_list) >= 2:
                        shopname = u'{}-{}'.format(shop_code_list[0], shop_code_list[1])
                    else:
                        shopname = delete_data_dict['memo']
                    classshopsku_obj = classshopsku(db_conn=None, redis_conn=redis_coon, shopname=shopname)
                    classshopsku_obj.setSKU(shopsku=shop_sku, sku=new_sku)
                else:
                    status = 'error'
                    error_info = add_result['errortext']
            else:
                status = 'error'
                error_info = delete_result['errortext']
        else:
            status = 'error'
            error_info = u'普源数据库连接失败'
        ooResult = operation_log_obj.updateStatusP(opnum=opnum, opkey=shop_sku, status=status, elogs=error_info)
        assert ooResult['errorcode'] == 0, ooResult['errortext']
    pyconn_obj.py_close_conn_database()


