# coding=utf-8

"""
导入表格的形式批量修改供应商及商品信息对应的采购员和责任归属人二
"""


import xlrd
import sys
from django.db.models import Q
from datetime import datetime
from pyapp.models import B_Supplier, b_goods, B_Person
from pyapp.table.b_supplier_purchaser_relationship import b_supplier_purchaser_relationship
# from sqlapp.models import b_person as B_Person
from brick.pydata.py_syn.public import public
from django_redis import get_redis_connection
r = get_redis_connection(alias='schedule')


def update_redis_schedule(param):
    r.hset(param['schedule_name'], 'StartTime', param['start_time'])
    r.hset(param['schedule_name'], 'EndTime', param['end_time'])
    r.hset(param['schedule_name'], 'ImportTime', param['import_time'])
    r.hset(param['schedule_name'], 'aNum', param['all_num'])
    r.hset(param['schedule_name'], 'sNum', param['success_num'])
    r.hset(param['schedule_name'], 'eNum', param['error_num'])
    r.hset(param['schedule_name'], 'etype', 'modify_purchaser')
    r.hset(param['schedule_name'], 'ErrorInfo', param['error_info'])
    r.hset(param['schedule_name'], 'endFlag', param['end_flag'])
    r.hset(param['schedule_name'], 'AllInfo', param['all_info'])
    r.hset(param['schedule_name'], 'FileError', param['file_error'])

def get_redis_schedule(schedule_name):
    result = {
        'schedule_name': schedule_name,
        'start_time': r.hget(schedule_name, 'StartTime'),
        'import_time': r.hget(schedule_name, 'ImportTime'),
        'all_num': r.hget(schedule_name, 'aNum'),
        'success_num': r.hget(schedule_name, 'sNum'),
        'error_num': r.hget(schedule_name, 'eNum'),
        'end_flag': r.hget(schedule_name, 'endFlag'),
        'all_info': r.hget(schedule_name, 'AllInfo'),
        'end_time': r.hget(schedule_name, 'EndTime'),
        'error_info': r.hget(schedule_name, 'ErrorInfo'),
        'file_error': r.hget(schedule_name, 'FileError')
    }
    return result

def read_purchaser_excel(modify_file):
    """读取修改采购员的excel"""
    error_num = 0
    try:
        file_name = modify_file.name
        if file_name.endswith('.xls') or file_name.endswith('xlsx'):
            data = xlrd.open_workbook(filename=None, file_contents=modify_file.read())
            table = data.sheets()[0]
            nrows = table.nrows
            modify_list = []
            category_blank_list = []
            for rownum in range(1, nrows):
                row = table.row_values(rownum)
                if row:
                    supplier = str(row[0]).strip()
                    purchaser = str(row[1]).strip()
                    category = str(row[2]).strip()
                    if category and judge_decimal(category) and int(float(category)) in [0, 1]:
                        modify_list.append(
                            {
                                'supplier': supplier, 'purchaser': purchaser, 'category': int(float(category))
                            }
                        )
                    else:
                        category_blank_list.append(supplier)
                        error_num += 1
            return {'error_code': 0, 'modify_list': modify_list, 'category_blank_list': category_blank_list, 'error_num': error_num}
        else:
            return {'error_code': -1, 'error_info': u'文件: "%s" 格式错误, 请使用 ".xls" 或 ".xlsx" 格式文件' % file_name}
    except Exception, e:
        error_info = 'error: 文件内容错误  ex=%s;  __LINE__=%s' % (e, sys._getframe().f_lineno)
        return {'error_code': -1, 'error_info': error_info}

def judge_decimal(str):
    try:
        float(str)
        return True
    except:
        return False

def purchaser_modify(supplier_id, new_purchaser_id, category, modify_name, new_purchaser=None, supplier_name=None):
    """批量修改采购员"""
    clothing = ['0|1|', '0|2|', '0|170|', '0|174|', '0|174|175|', '0|176|', '0|176|177|', '0|176|178|', '0|176|180|', '0|176|183|']
    if not new_purchaser:
        new_purchaser = B_Person.objects.filter(NID=new_purchaser_id).values_list('PersonName', flat=True)[0]
    if not supplier_name:
        supplier_name = B_Supplier.objects.filter(NID=supplier_id).values_list('SupplierName', flat=True)[0]

    # 修改一：将b_goods表对应供应商、对应类别(服装、非服装)下的采购更新成新的采购
    if category == 0:
        # objs = b_goods.objects.filter(CategoryCode__in=clothing, SupplierID=supplier_id).exclude(GoodsStatus='停售').update(Purchaser=new_purchaser)
        objs = b_goods.objects.filter(CategoryCode__in=clothing, SupplierID=supplier_id).exclude(GoodsStatus='停售')
        c = u'服装'
    else:
        # b_goods.objects.filter(~Q(CategoryCode__in=clothing), SupplierID=supplier_id).exclude(GoodsStatus='停售').update(Purchaser=new_purchaser)
        objs = b_goods.objects.filter(~Q(CategoryCode__in=clothing), SupplierID=supplier_id).exclude(GoodsStatus='停售')
        c = u'非服装'
    if objs.exists():
        objs.update(Purchaser=new_purchaser)

        # 修改二：查询更新后的b_goods表对应供应商下的所有非停售SKU下的采购员，拼接成字符串后更新到b_supplier表
        b_goods_objs = b_goods.objects.filter(SupplierID=supplier_id).exclude(GoodsStatus='停售').values_list('Purchaser', flat=True)
        purchaser_list = []
        for each in b_goods_objs:
            if each:
                if each.strip() and each.strip() != 'None':
                    purchaser_list.append(each.strip())
        purchaser_str = '/'.join(list(set(purchaser_list)))
        B_Supplier.objects.filter(NID=supplier_id).update(SupPurchaser=purchaser_str, Modifier=modify_name, ModifyDate=datetime.now())

        # 修改三：将b_supplier_purchaser_relationship表对应供应商、对应类别(服装、非服装)下的采购员标记为失效状态，并将采购员更新进来
        modify_time = datetime.now()
        b_supplier_purchaser_relationship.objects.filter(SupplierID=supplier_id, Category=category).update(
            InvalidTime=modify_time, ModifyName=modify_name, ModifyTime=modify_time)

        b_supplier_purchaser_relationship.objects.create(
            SupplierID=supplier_id, PurchaserID=new_purchaser_id, EffectiveTime=modify_time, Category=category,
            ModifyName=modify_name, ModifyTime=modify_time)
        return {'error_code': 0}
    else:
        return {'error_code': -1, 'error_info': u'"%s"无非停售状态、%s类别的SKU可修改采购员' % (supplier_name, c)}

def modify_purchaser_batch(modify_file, modify_name, modify_time, schedule_name):
    """批量修改采购员入口"""
    public_obj = public()
    import_time = modify_time.strftime('%Y-%m-%d %H:%M:%S')
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    read_excel_result = read_purchaser_excel(modify_file)
    param = {
        'schedule_name': schedule_name, 'start_time': start_time, 'import_time': import_time, 'all_num': 0,
        'success_num': 0, 'error_num': 0,  'end_flag': 0, 'all_info': '', 'end_time': '', 'error_info': [],
        'file_error': ''
    }
    if read_excel_result['error_code'] == 0:
        modify_list = read_excel_result['modify_list']
        error_num = read_excel_result['error_num']
        category_blank_list = read_excel_result['category_blank_list']
        for category_blank in category_blank_list:
            param['error_info'].append(u'修改供应商: "%s", 列 "是否服装" 未指定或指定错误' % category_blank)
        param['all_num'] = len(modify_list) + error_num
        param['error_num'] = error_num
        update_redis_schedule(param)

        for modify in modify_list:
            supplier = modify['supplier']
            purchaser = modify['purchaser']
            category = modify['category']
            try:
                B_Supplier_obj = B_Supplier.objects.filter(SupplierName=supplier)
                if not B_Supplier_obj.exists():
                    param['error_info'].append(u'供应商: "%s" 未查到' % supplier)
                    param['error_num'] += 1
                else:
                    supplier_id = B_Supplier_obj[0].NID
                    B_Person_obj = B_Person.objects.filter(PersonName=purchaser)
                    if not B_Person_obj.exists():
                        param['error_info'].append(u'采购员: "%s" 未查到' % purchaser)
                        param['error_num'] += 1
                    else:
                        purchaser_id = B_Person_obj[0].NID
                        modify_py_result = public_obj.modify_py_purchaser(
                            supplier_id=supplier_id, new_purchaser_id=purchaser_id, category=category,
                            modify_name=modify_name, new_purchaser=purchaser)
                        if modify_py_result['error_code'] == 0:
                            modify_online_result = purchaser_modify(
                                supplier_id=supplier_id, new_purchaser_id=purchaser_id, category=category,
                                modify_name=modify_name, new_purchaser=purchaser, supplier_name=supplier)
                            if modify_online_result['error_code'] == 0:
                                param['success_num'] += 1
                            else:
                                param['error_info'].append(modify_online_result['error_info'])
                                param['error_num'] += 1
                        else:
                            param['error_info'].append(modify_py_result['error_info'])
                            param['error_num'] += 1
            except Exception, e:
                error = u'供应商: "%s" ex=%s;  __LINE__=%s' % (supplier, e, sys._getframe().f_lineno)
                param['error_info'].append(error)
                param['error_num'] += 1
            update_redis_schedule(param)
    else:
        param['file_error'] = read_excel_result['error_info']
        update_redis_schedule(param)

    param['end_flag'] = 1
    param['end_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    update_redis_schedule(param)



def read_possessman2_excel(modify_file):
    """读取修改责任归属人二的excel"""
    try:
        file_name = modify_file.name
        if file_name.endswith('.xls') or file_name.endswith('xlsx'):
            data = xlrd.open_workbook(filename=None, file_contents=modify_file.read())
            table = data.sheets()[0]
            nrows = table.nrows
            modify_list = []
            for rownum in range(1, nrows):
                row = table.row_values(rownum)
                if row:
                    supplier = str(row[0]).strip()
                    possessman2 = str(row[1]).strip()
                    modify_list.append(
                        {'supplier': supplier, 'possessman2': possessman2}
                    )
            return {'error_code': 0, 'modify_list': modify_list}
        else:
            return {'error_code': -1, 'error_info': u'文件: "%s" 格式错误, 请使用 ".xls" 或 ".xlsx" 格式文件' % file_name}
    except Exception, e:
        error_info = 'error: 文件内容错误  ex=%s;  __LINE__=%s' % (e, sys._getframe().f_lineno)
        return {'error_code': -1, 'error_info': error_info}

def possessman2_modify(possessman2_info):
    """批量修改责任归属人二"""
    B_Supplier.objects.filter(NID=possessman2_info['nid']).update(PossessMan2=possessman2_info['PossessMan2'])
    b_goods.objects.filter(SupplierID=possessman2_info['nid']).update(possessMan2=possessman2_info['PossessMan2'])
    return {'error_code': 0}

def modify_possessman2_batch(modify_file, modify_name, modify_time, schedule_name):
    """批量修改责任归属人二入口"""
    public_obj = public()
    import_time = modify_time.strftime('%Y-%m-%d %H:%M:%S')
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    read_excel_result = read_possessman2_excel(modify_file)
    param = {
        'schedule_name': schedule_name, 'start_time': start_time, 'import_time': import_time, 'all_num': 0,
        'success_num': 0, 'error_num': 0, 'end_flag': 0, 'all_info': '', 'end_time': '', 'error_info': [],
        'file_error': ''
    }
    if read_excel_result['error_code'] == 0:
        modify_list = read_excel_result['modify_list']
        param['all_num'] = len(modify_list)
        update_redis_schedule(param)

        for modify in modify_list:
            supplier = modify['supplier']
            possessman2 = modify['possessman2']
            try:
                B_Supplier_obj = B_Supplier.objects.filter(SupplierName=supplier)
                if not B_Supplier_obj.exists():
                    param['error_info'].append(u'供应商: "%s" 未查到' % supplier)
                    param['error_num'] += 1
                else:
                    supplier_id = B_Supplier_obj[0].NID
                    possessman2_info = {'nid': supplier_id, 'PossessMan2': u'%s' % possessman2}
                    modify_py_result = public_obj.modify_py_possessman2(possessman2_info)
                    if modify_py_result['error_code'] == 0:
                        modify_online_result = possessman2_modify(possessman2_info)
                        if modify_online_result['error_code'] == 0:
                            param['success_num'] += 1
                        else:
                            param['error_info'].append(modify_online_result['error_info'])
                            param['error_num'] += 1
                    else:
                        param['error_info'].append(modify_py_result['error_info'])
                        param['error_num'] += 1
            except Exception, e:
                error = u'供应商: "%s" ex=%s;  __LINE__=%s' % (supplier, e, sys._getframe().f_lineno)
                param['error_info'].append(error)
                param['error_num'] += 1
            update_redis_schedule(param)
    else:
        param['file_error'] = read_excel_result['error_info']
        update_redis_schedule(param)

    param['end_flag'] = 1
    param['end_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    update_redis_schedule(param)