# coding=utf-8


from skuapp.table.t_tort_info_sync import t_tort_info_sync
from skuapp.public.const import tort
from brick.pydata.py_syn.public import public
from django.db import connection
from brick.table.t_operation_log_online_syn_py import t_operation_log_online_syn_py as operation_log
from brick.pydata.py_syn.py_conn import py_conn
pyconn_obj = py_conn()
public_obj = public()
operation_log_obj = operation_log(DBConn=connection)


def online_tort_syn_puyuan(tort_data_list, opnum, now_time, user_name):
    try:
        conn_result = pyconn_obj.py_conn_database()
        sqlserver_cursor = conn_result['py_cursor']
        id_list = []
        id_list_com = []
        for tort_data in tort_data_list:
            main_sku = tort_data['main_sku']
            single_data_list = tort_data['single_data_list']
            id_1 = tort_data['id_1']
            id_2 = tort_data['id_2']
            if single_data_list:
                if sqlserver_cursor:
                    result = public_obj.b_goods_modify_to_pydb(
                        b_goods_data_list=single_data_list, sqlserverInfo=conn_result, pydb_connect=connection
                    )

                    if result['errorcode'] == 0:
                        if id_1:
                            id_list.append(id_1)
                        else:
                            id_list_com.append(id_2)
                        status = 'over'
                        error_info = str(single_data_list)
                    else:
                        status = 'error'
                        error_info = result['errortext']
                else:
                    status = 'error'
                    error_info = u'普源数据库连接失败'
            else:
                status = 'error'
                error_info = u'未查到主SKU：%s' % main_sku
            ooResult = operation_log_obj.updateStatusP(opnum=opnum, opkey=main_sku, status=status, elogs=error_info)
            assert ooResult['errorcode'] == 0, ooResult['errortext']
        t_tort_info_sync.objects.filter(ID__in=id_list).update(Step=tort.SYNC, SyncStaffID=user_name, SyncTime=now_time)
        t_tort_info_sync.objects.filter(ID__in=id_list_com).update(Step=tort.SYNC_COM, SyncStaffID=user_name, SyncTime=now_time)
        pyconn_obj.py_close_conn_database()
    except Exception, e:
        print '1111111111--------%s' % e