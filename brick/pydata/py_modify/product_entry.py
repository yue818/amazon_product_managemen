# coding=utf-8

"""
产品开发
信息录入同步写入普源数据库
"""

import math
from datetime import datetime
import pymssql
from skuapp.table.t_product_mainsku_sku import t_product_mainsku_sku
from skuapp.table.B_PackInfo import B_PackInfo
from skuapp.table.t_product_oplog import t_product_oplog
from skuapp.table.t_product_enter_ed import t_product_enter_ed
from skuapp.table.t_product_pic_completion import t_product_pic_completion
from skuapp.table.public import getChoices, ChoiceCategory2
from skuapp.table.t_base import getChoicesuser
from Project.settings import SBBL
from skuapp.views import end_t_product_oplog
from brick.pydata.py_syn.public import public
from brick.table.t_operation_log_online_syn_py import t_operation_log_online_syn_py as operation_log
from django.db import connection
from skuapp.table.t_product_enter_ing import t_product_enter_ing
from skuapp.table.t_sku_weight_examine import t_sku_weight_examine
from brick.pydata.py_syn.py_conn import py_conn
pyconn_obj = py_conn()


Category2 = getChoices(ChoiceCategory2)


def get_mainsku_sku(qs_id, main_sku):
    """获取mainsku_sku表信息"""
    mainsku_sku_infos = []
    objs = t_product_mainsku_sku.objects.filter(pid=qs_id, MainSKU=main_sku)
    if objs.exists():
        for obj in objs:
            temp_dict = {
                'product_sku': obj.ProductSKU.strip(), 'sku_attrs': obj.SKUATTRS, 'min_pack_num': obj.MinPackNum,
                'weight': obj.Weight, 'pack_nid': obj.PackNID, 'unit_price': obj.UnitPrice,
                'dress_info': obj.DressInfo,'SupplierLink': obj.SupplierLink, 'SupplierNum': obj.SupplierNum
            }
            mainsku_sku_infos.append(temp_dict)
    return mainsku_sku_infos

def get_small_category(qs_SmallCategory):
    """小类名称"""
    small_category = None
    for cate in Category2:
        if cate[0] == qs_SmallCategory:
            small_category = cate[1]
            break
    if small_category is None:
        small_category = qs_SmallCategory
    return small_category

def get_product_name(qs_ContrabandAttribute, qs_SmallCategory, qs_PrepackMark, qs_Name2, SKUATTRS):
    """获取商品名称"""
    wjp = ''
    if qs_ContrabandAttribute and qs_ContrabandAttribute != u'普货':
        if qs_SmallCategory != u'手表':  # 手表特殊
            wjp = u'-违禁品'
    PrepackMark = qs_PrepackMark
    if qs_PrepackMark is None:
        PrepackMark = ''
    product_name = u'%s%s-%s%s' % (PrepackMark, qs_Name2, SKUATTRS, wjp)
    return product_name

def get_weight_packName_packCost(qs_Weight, qs_PackNID, sku_Weight, sku_pack_nid):
    """获取商品重量、包装规格"""
    weight = 0
    pack_name = ''
    pack_cost = 0
    if qs_Weight is not None and qs_Weight > 0:
        weight = qs_Weight
    if sku_Weight is not None and sku_Weight > 0:
        weight = sku_Weight
    PackNID = sku_pack_nid if sku_pack_nid > 0 else qs_PackNID
    B_PackInfo_obj = B_PackInfo.objects.filter(id__exact=PackNID)

    pack_weight = 0
    if B_PackInfo_obj.exists():
        pack_weight = int(B_PackInfo_obj[0].Weight)
        weight = weight + pack_weight
        pack_name = B_PackInfo_obj[0].PackName
        pack_cost = B_PackInfo_obj[0].CostPrice
    return weight, pack_name, pack_cost, pack_weight

def get_yjgs_name2(qs_id, qs_YJGS2StaffName):
    """获取业绩归属人二"""
    yjgs_name2 = ''
    t_product_oplog_obj2 = t_product_oplog.objects.filter(pid=qs_id, StepID='JZL')
    if qs_YJGS2StaffName:
        yjgs_name2 = getChoicesuser(qs_YJGS2StaffName)
    elif t_product_oplog_obj2.exists():
        yjgs_name2 = t_product_oplog_obj2[0].OpName
    return yjgs_name2

def get_lwh(lwh):
    l = None
    w = None
    h = None
    c = ''
    try:
        if lwh:
            if lwh.find('cloth') >= 0:
                ll = lwh.split(';')
                if ll[0] == 'cloth':
                    c = ll[1]
                elif ll[0] == 'nocloth':
                    r = ll[1].replace('cm', '').split('*')
                    l, w, h = r[0], r[1], r[2]
            else:
                c = lwh
    except:
        pass
    return l, w, h, c

def write_py(data_list, sqlserverInfo, main_sku):
    error_code = 0
    error_info = ''
    public_obj = public()
    result = public_obj.sku_info_to_pydb(b_goods_data_list=data_list, sqlserverInfo=sqlserverInfo, mainsku=main_sku, pydb_connect=connection)
    if result['errorcode'] != 0:
        error_code = 1
        error_info = result['errortext']
    return {'error_code': error_code, 'error_info': error_info}

def to_enter_ed_enter_ing(qs, first_name, user_name, data_list):
    """录入完成"""
    obj = t_product_enter_ed()
    obj.__dict__ = qs.__dict__
    obj.id = qs.id
    obj.CreateTime = datetime.now()
    obj.CreateStaffName = first_name
    obj.StaffID = user_name
    obj.LRTime = datetime.now()
    obj.LRStaffName = first_name
    try:
        del obj.auditnote
    except Exception:
        pass
    piccomplete = t_product_pic_completion.objects.filter(MainSKU=qs.MainSKU, pid=qs.id)
    if piccomplete:
        # 2完成实拍 3完成制作
        if piccomplete[0].YNphoto == u'0':
            obj.MGProcess = 2
        elif piccomplete[0].YNphoto == u'1':
            obj.MGProcess = 3
        obj.MGStaffName = piccomplete[0].MGStaffName
        obj.MGTime = piccomplete[0].MGTime
        obj.PZStaffName = piccomplete[0].PZStaffName
        obj.PZTime = piccomplete[0].PZTime
    obj.onebuOperation = '0'
    obj.twobuOperation = '0'
    obj.threebuOperation = '0'
    obj.fourbuOperation = '0'
    obj.fivebuOperation = '0'
    obj.sixbuOperation = '0'
    obj.sevenbuOperation = '0'
    obj.eightbuOperation = '0'
    obj.ninebuOperation = '0'
    obj.tenbuOperation = '0'
    obj.elevenbuOperation = '0'
    obj.twelvebuOperation = '0'
    obj.thirteenbuOperation = '0'
    obj.save()
    
    # 将精准调研的记录放入 克重审核模块 等待审核
    for info in data_list:
        if info.get('AI_FLAG') == '1':
            sku_examine_objs = t_sku_weight_examine(
                product_image=qs.SourcePicPath2,  # 供应商图
                product_name = info['GoodsName'],   # 商品名称  中文
                product_mainsku = qs.MainSKU,
                product_sku = info['SKU'],
                create_person = qs.JZLStaffName,
                create_time = datetime.now(),
                survey_weight = info['Weight'],
                packinfo_weight = info['pack_weight'],
                examine_weight = None,
                examine_status = '0',   # 默认 未审核
                auditor = None,
                examine_time = None,
                supplier_name = info['SupplierName'],
                product_price = info['CostPrice'],
                product_lcate = qs.LargeCategory,  # 大类名称
                product_scate = qs.SmallCategory,   # 小类编号
                canuse_num = 0   # 可用数量默认为  0
            )
            sku_examine_objs.save()
        
        
    end_t_product_oplog(first_name, user_name,  qs.MainSKU, 'LR', qs.Name2, qs.id)
    qs.delete()


def end_t_product_oplog(first_name, user_name, mainsku, tempstepid, tempname, temppid):
    tempstepname = u'其他'
    if tempstepid == 'DY' :
        tempstepname = u'调研'
    if tempstepid == 'DYSH' :
        tempstepname = u'调研审核'
    if tempstepid == 'PC' :
        tempstepname = u'排重'
    if tempstepid == 'KF' :
        tempstepname = u'开发'
    if tempstepid == 'XJ' :
        tempstepname = u'询价'
    if tempstepid == 'JZL' :
        tempstepname = u'建资料'
    if tempstepid == 'PZ':
        tempstepname = u'拍照'
    if tempstepid == 'MG' :
        tempstepname = u'美工'
    if tempstepid == 'LR' :
        tempstepname = u'录入'
    if tempstepid == 'BMLY' :
        tempstepname = u'部门领用'
    if tempstepid == 'DEL' :
        tempstepname = u'删除'

    t_product_oplog_objs = t_product_oplog.objects.filter(StepID=tempstepid,pid = temppid)
    if t_product_oplog_objs is  None or t_product_oplog_objs.count() ==0:
        t_product_oplog_obj = t_product_oplog(MainSKU= mainsku,Name2=tempname,OpID=user_name,OpName=first_name,StepID=tempstepid,StepName=tempstepname,BeginTime=datetime.now(),EndTime=datetime.now(), pid=temppid)
        t_product_oplog_obj.save()
    else:
        for t_product_oplog_obj in t_product_oplog_objs :
            t_product_oplog_obj.MainSKU = mainsku
            t_product_oplog_obj.Name2 = tempname
            t_product_oplog_obj.OpID=user_name
            t_product_oplog_obj.OpName=first_name
            t_product_oplog_obj.StepName =tempstepname
            t_product_oplog_obj.EndTime=datetime.now()
            t_product_oplog_obj.save()


def handle_param(qs):
    data_list = []
    sku_list = []
    main_sku = ''

    if not qs:
        return data_list, sku_list, main_sku

    main_sku = qs.MainSKU
    mainsku_sku_infos = get_mainsku_sku(qs_id=qs.id, main_sku=main_sku)
    store_house = qs.Storehouse         # 发货仓库
    large_category = qs.LargeCategory   # 大类名称
    material = qs.Material              # 材质
    status = u'正常'                    # 商品状态
    multi_style = u'否'                 # 是否多款式
    has_sample = u'否'                  # 是否有样品
    # model = qs.SupplierArtNO            # 型号
    brand = u'fancyqube'                # 品牌
    unit = qs.Unit                      # 单位
    small_category = get_small_category(qs.SmallCategory)     # 小类名称
    supplier_name =  qs.SupplierID      # 供应商名称
    report_name = qs.ReportName         # 英文申报名
    report_name2 = qs.ReportName2       # 中文申报名
    original_country_code = 'CN'        # 原产国代码
    original_country_name = 'China'     # 原产国
    yjgs_name1 = qs.DYStaffName         # 业绩归属人一
    yjgs_name2 = get_yjgs_name2(qs.id, qs.YJGS2StaffName)         # 业绩归属人二
    create_date = qs.UpdateTime.strftime('%Y-%m-%d')              # 开发日期
    purchaser = qs.Buyer                    # 采购员
    purchase_arrive_days = qs.OrderDays     # 采购到货天数
    stock_alarm_days = qs.StockAlarmDays    # 库存预警销售周期
    min_order = qs.MinOrder                 # 采购最小订货量
    possess_man2 = qs.possessMan2           # 责任归属人2
    product_attr = u'%s' % qs.ContrabandAttribute   # 商品属性
    AI_FLAG = u'%s' % qs.__dict__.get('AI_FLAG')   # 精准调研

    for info in mainsku_sku_infos:
        product_code = info['product_sku']      # 商品编码
        product_sku = info['product_sku']       # 商品SKU
        min_pack_num = info['min_pack_num']     # 最小包装数

        model = info['SupplierNum'] if info['SupplierNum'] else qs.SupplierArtNO # 型号

        # 商品名称
        product_name = get_product_name(qs.ContrabandAttribute, qs.SmallCategory, qs.PrepackMark, qs.Name2, info['sku_attrs'])
        # 重量、包装规格、内包装成本, 包装重量
        weight, pack_name, pack_cost, pack_weight = get_weight_packName_packCost(qs.Weight, qs.PackNID, info['weight'], info['pack_nid'])
        # 成本单价(元)
        unit_price = info['unit_price'] if info['unit_price'] and info['unit_price'] > 0 else qs.UnitPrice
        # 备注(不要链接)
        # remark = u'%s\n%s\n%s\n%s\n%s' % (info['dress_info'], qs.Remark, qs.LWH, qs.SupplierPUrl1, qs.SupplierPUrl2)
        l, w, h, c = get_lwh(qs.LWH)
        remark = u'【%s】\n%s\n%s' % (c, qs.Remark, info['dress_info'])
        # 申报价值(美元)
        report_price = int(math.ceil(float(unit_price if unit_price else 0) / SBBL))

        if info.get('SupplierLink') and info.get('SupplierLink').strip() != qs.SupplierPUrl1:
            url1 = u'%s;' % info.get('SupplierLink')
            url4 = u'%s; %s; %s;' % (info.get('SupplierLink'), qs.SupplierPUrl1, qs.SupplierPUrl2)
        else:
            url1 = u'%s;' % qs.SupplierPUrl1
            url4 = u'%s; %s;' % (qs.SupplierPUrl1, qs.SupplierPUrl2)

        url2 = u'%s; %s; %s;' % (info['dress_info'], qs.Remark, qs.LWH)

        b_goods_data = {
            'GoodsCategoryID': '', 'CategoryCode': '',  'GoodsCode': product_code, 'GoodsName': product_name,
            'ShopTitle': '', 'SKU': product_sku, 'BarCode': '', 'FitCode': '', 'MultiStyle': u'否',
            'Material': material, 'Class': info['sku_attrs'], 'Model': model, 'Unit': unit, 'Style': '', 'Brand': brand,
            'LocationID': '', 'Quantity': '', 'SalePrice': '', 'CostPrice': unit_price, 'AliasCnName': report_name2,
            'AliasEnName': report_name, 'Weight': weight, 'DeclaredValue': report_price,
            'OriginCountry':original_country_name, 'OriginCountryCode': original_country_code, 'ExpressID': '',
            'Used': '', 'BmpFileName': '', 'BmpUrl': '', 'MaxNum': '', 'MinNum': '', 'GoodsCount': '', 'SupplierID': '',
            'Notes': remark, 'SampleFlag': u'否', 'SampleCount': '', 'SampleMemo': '', 'CreateDate': create_date,
            'GroupFlag': '', 'SalerName': yjgs_name1, 'SellCount': '', 'SellDays': stock_alarm_days,
            'PackFee': pack_cost, 'PackName': pack_name, 'GoodsStatus': u'正常', 'DevDate': '', 'SalerName2': yjgs_name2,
            'BatchPrice': '', 'MaxSalePrice': '', 'RetailPrice': '', 'MarketPrice': '', 'PackageCount': min_pack_num,
            'ChangeStatusTime': '', 'StockDays': purchase_arrive_days, 'StoreID': '', 'Purchaser': purchaser,
            'LinkUrl': url1, 'LinkUrl2': '', 'LinkUrl3': '', 'StockMinAmount': min_order, 'MinPrice': '',
            'HSCODE': '', 'ViewUser': '', 'InLong': l, 'InWide': w, 'InHigh': h, 'InGrossweight': '',
            'InNetweight': '', 'OutLong': '', 'OutWide': '', 'OutHigh': '',  'OutGrossweight': '', 'OutNetweight': '',
            'ShopCarryCost': '', 'ExchangeRate': '','WebCost': '', 'PackWeight': '', 'LogisticsCost': '',
            'GrossRate': '', 'CalSalePrice': '', 'CalYunFei': '', 'CalSaleAllPrice': '', 'PackMsg': '', 'ItemUrl': '',
            'IsCharged': '', 'DelInFile': '', 'Season': '', 'IsPowder': '', 'IsLiquid': '', 'possessMan1': '',
            'possessMan2': possess_man2, 'LinkUrl4': url4, 'LinkUrl5': '', 'LinkUrl6': '', 'isMagnetism': '',
            'NoSalesDate': '', 'NotUsedReason': '', 'PackingRatio': '', 'shippingType': '', 'FreightRate': '',
            'USEDueDate': '', 'SupplierName': supplier_name, 'LargeCategoryName': large_category,
            'SmallCategoryName': small_category, 'Storehouse': store_house, 'ProductAttr': product_attr,
            'AI_FLAG': AI_FLAG, 'pack_weight': pack_weight
        }
        data_list.append(b_goods_data)
        sku_list.append(product_sku)
    return data_list, sku_list, main_sku


def get_qs(enter_id):
    t_product_enter_ing_obj = t_product_enter_ing.objects.filter(id=enter_id)
    if t_product_enter_ing_obj.exists():
        qs = t_product_enter_ing_obj[0]
    else:
        qs = None
    return qs


def online_syn_to_puyuan(enter_id_list, opnum, first_name, user_name):
    operation_log_obj = operation_log(DBConn=connection)
    conn_result = pyconn_obj.py_conn_database()
    sqlserver_cursor = conn_result['py_cursor']

    for enter_id in enter_id_list:
        try:
            qs = get_qs(enter_id=enter_id)
            data_list, sku_list, main_sku = handle_param(qs)
            if sqlserver_cursor:
                write_result = write_py(data_list=data_list, sqlserverInfo=conn_result, main_sku=main_sku)
                sku = ','.join(sku_list)
                oResult = operation_log_obj.update_sku(opnum=opnum, sku=sku, main_sku=main_sku)
                assert oResult['errorcode'] == 0, oResult['errortext']

                if write_result['error_code'] == 0:
                    to_enter_ed_enter_ing(qs=qs, first_name=first_name, user_name=user_name, data_list=data_list)
                    status = 'over'
                    error_info = str(data_list)
                else:
                    status = 'error'
                    error_info = write_result['error_info']
            else:
                status = 'error'
                error_info = u'普源数据库连接失败'
        except Exception, e:
            status = 'error'
            error_info = u'error: %s' % e
        ooResult = operation_log_obj.updateStatusP(opnum=opnum, opkey=main_sku, status=status, elogs=error_info)
        assert ooResult['errorcode'] == 0, ooResult['errortext']
    pyconn_obj.py_close_conn_database()