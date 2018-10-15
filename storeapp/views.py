# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import logging
import re
import oss2
from Project.settings import *
from urllib import urlencode
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from Project.settings import *
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction

from skuapp.table.t_online_info import t_online_info
from storeapp.models import t_add_variant_information
from storeapp.models import t_online_info_wish_store, t_wish_product_api_log
from brick.wish.wish_api_before.token_verification import verb_token
from brick.table.t_platform_color_select_table import t_platform_color_select_table
from brick.table.t_online_api_return_code_business_language_comparison import t_online_api_return_code_business_language_comparison

from brick.pydata.py_redis.py_SynRedis_tables import py_SynRedis_tables

from brick.table.t_country_code_name_table import t_country_code_name_table

from brick.wish.api.wishapi import cwishapi
from brick.classredis.classshopname import classshopname
from brick.classredis.classlisting import classlisting
from brick.classredis.classshopsku import classshopsku
from brick.classredis.classmainsku import classmainsku

from app_djcelery.tasks import syndata_by_wish_api
from app_djcelery.tasks import syndata_by_wish_api_shopname
from app_djcelery.tasks import update_status_by_shopsku_func
from app_djcelery.tasks import update_goods_information_by_wish_api
from app_djcelery.tasks import wish_change_shipping_to_country
from brick.classredis.classsku import classsku
from django.db.models import F

from brick.table.t_wish_store_oplogs import t_wish_store_oplogs
from brick.wish.wish_store import business_Terms
from brick.table.t_store_configuration_file import t_store_configuration_file
from brick.table.t_online_info_wish import t_online_info_wish
from brick.table.t_wish_shopcode_warehouse import t_wish_shopcode_warehouse

from brick.wish.wish_store import ToCalculateADS

from datetime import datetime as mydatetime

from django.db import connection
from django_redis import get_redis_connection
from brick.table.t_operation_log_online_syn_py import t_operation_log_online_syn_py

from skuapp.table.t_store_configuration_file import t_store_configuration_file as store_config
from pyapp.models import b_goods as py_b_goods,B_Supplier as py_b_Supplier, xxxb_packinfo as py_b_packinfo

from brick.wish.wish_pub.wish_pub_start import wish_image_upload

from brick.wish.wish_store import Wish_Data_Syn

from skuapp.table.t_product_enter_ed import t_product_enter_ed
from skuapp.table.t_product_mainsku_sku import t_product_mainsku_sku
from brick.shopee.t_shopee_oplogs import t_shopee_oplogs

# from Project.settings import connRedis
redis_coon = get_redis_connection(alias='product')
# redis_conn = connRedis
logger = logging.getLogger('sourceDns.webdns.views')

def syndata(request):
    '''
    Wish店铺管理--同步listID、list上架、list下架
    :param request:
    :return:
    '''
    sResult = {}
    try:
        t_wish_store_oplogs_obj = t_wish_store_oplogs(connection)
        productid = None
        fe = None
        for flag in ['syn','enable','disable']:
            if request.GET.get(flag):
                fe = flag
                productid = request.GET.get(flag)
                break
        opnum = fe+'_%s_%s' % (mydatetime.now().strftime('%Y%m%d%H%M%S'), request.user.username)

        param = {}  # 操作日志的参数
        param['OpNum'] = opnum
        param['OpKey'] = [productid]
        param['OpType'] = fe + 'id'
        param['Status'] = 'runing'
        param['ErrorInfo'] = ''
        param['OpPerson'] = request.user.first_name
        param['OpTime'] = mydatetime.now()
        param['OpStartTime'] = mydatetime.now()
        param['OpEndTime'] = None
        param['aNum'] = 1
        param['rNum'] = 0
        param['eNum'] = 0

        iResult = t_wish_store_oplogs_obj.createLog(param)
        assert iResult['errorcode'] == 0, fe + " insert log error."

        storeobj = t_online_info_wish_store.objects.get(ProductID=productid)
        storeResult = syndata_by_wish_api([storeobj.ShopName, storeobj.ProductID, storeobj.ParentSKU],fe,opnum)
        sResult['resultCode'] = storeResult['Code']
        sResult['messages'] = storeResult['messages']
    except Exception,e:
        sResult['resultCode'] = -1
        sResult['messages'] = '%s:%s' % (Exception,e)
    return JsonResponse(sResult)

def syndata_shopname(request):
    '''
    flag:判断是否全量或者增量刷新店铺数据
    bar：判断是否用来查询刷新进度的
    :param request:
    :return:
    '''
    shopname = request.GET.get('shopname','')
    flag = request.GET.get('flag','')
    bar = request.GET.get('bar','')
    classshopname_obj = classshopname(redis_cnxn=redis_coon)
    sResult = {}
    try:
        if bar == '0':  # 用来刷新该店铺同步进程
            shopstatus = classshopname_obj.get_api_status_by_shopname(shopname)
            if shopstatus is None or shopstatus == '':
                sResult['messages'] = 'Over' # 已经刷新完成
            else:
                sResult['messages'] = shopstatus
            sResult['resultCode'] = '3'
        else:
            if shopname != ''and flag != '':
                shopstatus = classshopname_obj.get_api_status_by_shopname(shopname)
                if shopstatus is None or shopstatus == '':
                    classshopname_obj.set_api_status_by_shopname(shopname,u'开始刷新店铺数据')
                    syndata_by_wish_api_shopname.delay(shopname,int(flag))
                    # messages.success(request, '正在同步 %s，请稍后刷新页面。。。' % shopname)
                    sResult['messages'] = u'开始刷新店铺数据'
                    sResult['resultCode'] = '0'
                else:
                    # messages.error(request, '%s,该店铺正在刷新，请稍后再试。。' % shopname)
                    sResult['messages'] = u'该店铺正在刷新'
                    sResult['resultCode'] = '3'
            else:
                sResult['resultCode'] = '2'
    except:
        sResult['resultCode'] = '1'
    return JsonResponse(sResult)

@csrf_exempt
def ShopSKU_edit(request):
    '''
    店铺SKU信息展示及信息修改
    :param request:
    :return:
    '''
    classlisting_obj = classlisting(db_conn=connection,redis_conn=redis_coon)
    ProductID = request.GET.get('abc')
    activeflag = request.GET.get('express', 'STANDARD')
    readonly = request.GET.get('readonly', '')

    if request.method == 'POST':
        alldata = request.POST.get('alldata','{}')
        sResult = Update_Variant_detail_info(alldata, ProductID, request, activeflag)
        return HttpResponse(json.dumps(sResult))
    else:
        mylist = []
        classsku_obj = classsku()
        shopname = classlisting_obj.getShopName(ProductID)
        classshopsku_obj = classshopsku(db_conn=connection, redis_conn=redis_coon, shopname=shopname)
        for shopsku in classlisting_obj.getShopSKUList(ProductID):
            mylist.append(Get_All_ShopSKU_INfo(shopsku,classsku_obj,classshopsku_obj,shopname,ProductID, activeflag))

        warehouse_obj = t_wish_shopcode_warehouse(connection)
        wResult = warehouse_obj.get_warehouse(shopname)
        # assert wResult['errorcode'] == 1, wResult['errortext']

        whlist = [key for key in wResult['warehouse']]

        t_platform_color_select_table_obj = t_platform_color_select_table(connection)
        colorlist = t_platform_color_select_table_obj.get_wish_color()

        return render(request, 'edit_update_goods_infor_by_shopsku.html',
                      {'mylist': mylist, 'ProductID': ProductID, 'colorlist': json.dumps(colorlist),
                       'activeflag': activeflag, 'warehouse': whlist, 'readonly': readonly})

def Get_All_ShopSKU_INfo(shopsku,classsku_obj,classshopsku_obj,shopname,ProductID, activeflag):
    '''
    :param shopsku: 店铺SKU
    :param py_SynRedis_pub_obj: 商品SKU信息获取接口
    :param classshopsku_obj: 店铺SKU信息获取接口
    :return:该店铺SKU对应的商品SKU，所有的信息
    '''
    rowdict = {}
    rowdict['SKU'] = classshopsku_obj.getSKU(shopsku)
    rowdict['ShopSKU'] = shopsku
    rowdict['Price'] = classshopsku_obj.getPrice(shopsku)

    if activeflag in ['DE', 'GB', 'US']:
        acs = getattr(classshopsku_obj, 'getWish%sShipping' % activeflag)
        rowdict['Shipping'] = acs(shopsku)

        aci = getattr(classshopsku_obj, 'getWish%sQuantity' % activeflag)
        rowdict['Quantity'] = aci(shopsku)
    else:
        rowdict['Quantity'] = classshopsku_obj.getQuantity(shopsku)
        rowdict['Shipping'] = classshopsku_obj.getShipping(shopsku)

    rowdict['Status'] = classshopsku_obj.getStatus(shopsku)
    rowdict['ShopName'] = shopname

    rowdict['ShopSKUImage'] = classshopsku_obj.getImage(shopsku)

    rowdict['ProductID'] = ProductID
    rowdict['Color'] = classshopsku_obj.getColor(shopsku)
    rowdict['Size'] = classshopsku_obj.getSize(shopsku)
    rowdict['msrp'] = classshopsku_obj.getmsrp(shopsku)
    rowdict['ShippingTime'] = classshopsku_obj.getshippingtime(shopsku)

    tmpsku = ('{}'.format(rowdict['SKU'])).split('*')[0]
    rowdict['nn'] = classsku_obj.get_uninstore_by_sku(tmpsku)
    goodsstatus = classsku_obj.get_goodsstatus_by_sku(tmpsku)
    if goodsstatus == '1':
        goodsstatus = u'正常'
    if goodsstatus == '2':
        goodsstatus = u'售完下架'
    if goodsstatus == '3':
        goodsstatus = u'临时下架'
    if goodsstatus == '4':
        goodsstatus = u'停售'

    rowdict['goodsstatus'] = goodsstatus

    inventory = classsku_obj.get_number_by_sku(tmpsku)
    if inventory is None or inventory == -1:
        inventory = 0
    else:
        inventory = str(inventory).split('.')[0]
        if inventory == '':
            inventory = '0'
    occupyNum = classsku_obj.get_reservationnum_by_sku(tmpsku)
    if occupyNum is None or occupyNum == -1:
        occupyNum = 0
    else:
        occupyNum = str(occupyNum).split('.')[0]
        if occupyNum == '':
            occupyNum = '0'

    rowdict['inventory'] = inventory
    rowdict['occupyNum'] = occupyNum
    rowdict['canuse'] = int(inventory) - int(occupyNum)
    rowdict['CanSaleDay'] = classsku_obj.get_cansaleday_by_sku(tmpsku)
    return rowdict

def Update_Variant_detail_info(infoData, ProductID, request, activeflag):
    '''
    更新该店铺SKU的信息，状态
    :param infoData:
    :param ProductID:
    :return:
    '''
    try:
        t_online_info_wish_obj = t_online_info_wish(connection)
        classlisting_obj = classlisting(db_conn=connection, redis_conn=redis_coon)
        shopname = classlisting_obj.getShopName(ProductID)

        t_wish_store_oplogs_obj    = t_wish_store_oplogs(connection)
        Type = 'Edit_ShopSKU'
        flagname = Type + '_%s_%s' % (mydatetime.now().strftime('%Y%m%d%H%M%S'), request.user.username)

        param = {}  # 操作日志的参数
        param['OpNum'] = flagname
        param['OpKey'] = [k for k, v in eval(infoData).items()]
        param['OpType'] = Type
        param['Status'] = 'runing'
        param['ErrorInfo'] = ''
        param['OpPerson'] = request.user.first_name
        param['OpTime'] = mydatetime.now()
        param['OpStartTime'] = mydatetime.now()
        param['OpEndTime'] = None
        param['aNum'] = len(eval(infoData).items())
        param['rNum'] = 0
        param['eNum'] = 0

        iResult = t_wish_store_oplogs_obj.createLog(param)
        assert iResult['errorcode'] == 0, "insert log error."

        v_result = ''

        t_store_configuration_file_obj = t_store_configuration_file(connection)
        store_status = t_store_configuration_file_obj.getshopStatusbyshopcode(shopname)  # 获取店铺状态
        assert store_status['errorcode'] == 0, store_status['errortext']

        if store_status['status'] == '0':  # 店铺状态正常的
            snstatus = '0'  # listing 店铺状态标记
            for k, v in eval(infoData).items():
                v_dict = eval(v)

                v_info = ''
                code = 0
                _content = ''
                if v_dict.has_key('edcheck'):  # 店铺SKU 上下架
                    if v_dict['edcheck'] == 'Enabled':
                        flag = 0
                    else:  # if v_dict['edcheck'] == 'Disabled'
                        flag = 1
                    StatusResult = Variant_ShopSKU_Status_Update(k, shopname, flag, '') # 不修改log
                    assert StatusResult['Code'] == 1, StatusResult['messages']
                    code = StatusResult['Code']
                    v_info = '%s' % StatusResult['messages']
                    _content = StatusResult['_content']
                    # 删除 店铺SKU的信息
                    v_dict.pop('edcheck')
                if v_dict:  # 修改店铺SKU的属性信息
                    inresult = updateShopSKUInfo(v_dict, k, ProductID, shopname, activeflag)
                    assert inresult['code'] in [1, 2], inresult['errorinfo']
                    code = inresult['code']
                    _content = inresult['_content']
                    v_info = '%s%s' % (inresult['info'], v_info)
                if code == 1:   # 修改成功
                    uPResult = t_wish_store_oplogs_obj.updateStatusP(flagname, k, 'over', '')
                else:  # 修改失败
                    uPResult = t_wish_store_oplogs_obj.updateStatusP(flagname, k, 'error', '%s,%s' % (business_Terms(_content), v_info))
                assert uPResult['errorcode'] == 0, uPResult['errortext']
                v_result = '%s%s\n' % (v_result, v_info)
        else:
            snstatus = '-1'  # listing 店铺状态标记
            uptext = u'店铺状态被标记为异常 %s' % store_status
            v_result = u'%s %s' % (uptext, shopname)

            uPResult = t_wish_store_oplogs_obj.update_error(flagname, uptext)
            assert uPResult['errorcode'] == 0, uPResult['errortext']

        SNResult = t_online_info_wish_obj.UpdateWishSNameByShopName(shopname, snstatus)  # shopname
        assert SNResult['errorcode'] == 1, SNResult['errortext']

        result = {'resultCode': 1, 'info': v_result}
    except Exception, e:
        result = {'resultCode': -1, 'errorinfo': '%s:%s' % (Exception, e)}
    return result



def updateShopSKUInfo(v_dict, k, ProductID, shopname, activeflag):
    t_store_configuration_file_obj = t_store_configuration_file(connection)
    cwishapi_obj = cwishapi()
    t_online_info_wish_obj = t_online_info_wish(connection)
    warehouse_obj = t_wish_shopcode_warehouse(connection)

    try:
        auth_info = verb_token(shopname, connection)
        assert auth_info['errorcode'] == 1, auth_info['errortext']

        wResult = warehouse_obj.get_warehouse(shopname)
        assert wResult['errorcode'] == 1, wResult['errortext']
        # warehouse = wResult['warehouse']
        if not wResult['warehouse'].has_key(activeflag):
            raise Exception(u'该店铺没有相应的仓库:%s,店铺所有仓库:%s' % (activeflag, wResult['warehouse']))
        # 对除店铺SKU状态以外的其余信息做修改
        datadict = v_dict
        datadict['sku'] = k
        datadict['format'] = 'json'
        datadict['access_token'] = auth_info['access_token']
        datadict['warehouse_name'] = wResult['warehouse'][activeflag]

        if datadict.get('main_image'):  # 如果需要更新变体的图片，就必须 有下面的设置 不能修改主产品的图片
            main_image = datadict['main_image'].keys()[0]
            if datadict['main_image'][main_image] == '1':  # 本地上传图片
                vResult = wish_image_upload(main_image, auth_info)
                assert vResult['errorcode'] == 1, vResult['errortext']
                datadict['main_image'] = vResult['image_url']
            else:
                datadict['main_image'] = main_image
            datadict['update_product_image'] = "False"

        rt = cwishapi_obj.update_shopsku_info_by_wish_api(datadict, timeout=30)
        _content = eval(rt._content)

        if rt.status_code == 200 and _content['code'] == 0:
            uResult = Update_ShopSKU_info_To_Redis(v_dict, ProductID, k, activeflag, shopname)
            assert uResult['errorcode'] == 0, uResult['errortext']

            toResult = ToCalculateADS(ProductID, shopname, connection)
            assert toResult in ['0', '1'], toResult['errortext']  # 获取该product的在线不在线的状态

            info = u'%s:信息修改成功' % (k,)
            result = {'code': 1, 'info': info,'_content':_content}
        else:
            if _content.get('code') in [1000, 1028, 1006, 1031]:  #
                toResult = ToCalculateADS(ProductID, shopname, connection)
                assert toResult in ['0', '1'], toResult['errortext']  # 获取该product的在线不在线的状态
            else:
                toResult = '-1'

            info = u'%s:信息修改失败,%s' % (k, business_Terms(_content))
            result = {'code': 2, 'info': info,'_content':_content}

        adResult = t_online_info_wish_obj.UpdateWishStatusAD(ProductID, toResult)
        assert adResult['errorcode'] == 1, adResult['errortext']

    except Exception, e:
        result = {'code': -1, 'errorinfo': '%s:%s' % (Exception, e)}
    return result


def Update_ShopSKU_info_To_Redis(v_dict, ProductID, k, activeflag, shopname):
    '''
    修改该店铺SKU的redis信息
    :param v_dict:
    :return:
    '''
    # tmplist = ['main_image','color','size','msrp','price','inventory','shipping','shipping_time']
    # 颜色例外
    try:
        classshopsku_obj = classshopsku(db_conn=connection, redis_conn=redis_coon, shopname=shopname)
        online_pbjs = t_online_info.objects.filter(ProductID=ProductID, ShopSKU=k)
        for vk, vv in v_dict.items():
            if vk == 'main_image':
                online_pbjs.update(ShopSKUImage=vv)
                classshopsku_obj.setImage(k, vv)
            if vk == 'color':
                online_pbjs.update(Color=vv)
                classshopsku_obj.setColor(k, vv)
            elif vk == 'size':
                online_pbjs.update(Size=vv)
                classshopsku_obj.setSize(k, vv)
            elif vk == 'msrp':
                online_pbjs.update(msrp=vv)
                classshopsku_obj.setmsrp(k, vv)
            elif vk == 'price':
                online_pbjs.update(Price=vv)
                classshopsku_obj.setPrice(k, vv)
            elif vk == 'inventory':
                if vv == '':
                    vv = None
                invdict = {}
                if activeflag == 'STANDARD':
                    invdict['Quantity'] = vv
                    f = getattr(classshopsku_obj, 'setQuantity')
                else:
                    invdict['%sExpressInventory' % activeflag] = vv
                    f = getattr(classshopsku_obj, 'setWish%sQuantity' % activeflag)
                online_pbjs.update(**invdict)
                f(k, vv)

            elif vk == 'shipping':
                if vv == '':
                    vv = None
                shidict = {}
                if activeflag == 'STANDARD':
                    shidict['Shipping'] = vv
                    f = getattr(classshopsku_obj, 'setShipping')
                else:
                    shidict['%sExpressShipping' % activeflag] = vv
                    f = getattr(classshopsku_obj, 'setWish%sShipping' % activeflag)
                online_pbjs.update(**shidict)
                f(k, vv)

            elif vk == 'shipping_time':
                online_pbjs.update(ShippingTime=vv)
                classshopsku_obj.setshippingtime(k, vv)
        return {'errorcode': 0, 'errortext': ''}
    except Exception, e:
        return {'errorcode': -1, 'errortext': '%s:%s'%(Exception, e)}


def Variant_ShopSKU_Status_Update(shopsku, shopname,StatusFlag,flagname):
    '''
    :param StatusFlag: 0-下架；1-上架
    :return: {'code': 0, 'content': ''}
    '''
    try:
        sflag = ''
        if StatusFlag == 0:
            sflag = 'disshopsku'
        elif StatusFlag == 1:
            sflag = 'enshopsku'

        sresult = update_status_by_shopsku_func(shopsku, shopname, sflag, flagname)
    except Exception, e:
        sresult = {'Code': -1, 'messages': '%s:%s' % (shopsku, e)}

    return sresult

def dis_enable_by_shopsku(request):
    sResult = {}
    flag = request.GET.get('flag')
    Infos = request.POST.get('alldata','[]')
    try:
        t_wish_store_oplogs_obj = t_wish_store_oplogs(connection)
        if int(flag) == 0:
            Type = 'Dis_ShopSKU'
        else:
            Type = 'En_ShopSKU'
        flagname = Type + '_%s_%s' % (mydatetime.now().strftime('%Y%m%d%H%M%S'),request.user.username)

        param = {}  # 操作日志的参数
        param['OpNum'] = flagname
        param['OpKey'] = [fo[1] for fo in eval(Infos)]
        param['OpType'] = Type
        param['Status'] = 'runing'
        param['ErrorInfo'] = ''
        param['OpPerson'] = request.user.first_name
        param['OpTime'] = mydatetime.now()
        param['OpStartTime'] = mydatetime.now()
        param['OpEndTime'] = None
        param['aNum'] = len(eval(Infos))
        param['rNum'] = 0
        param['eNum'] = 0

        iResult = t_wish_store_oplogs_obj.createLog(param)
        assert iResult['errorcode'] == 0, "insert log error."

        v_result = ''
        for info in eval(Infos):
            Result = Variant_ShopSKU_Status_Update(info[1], info[0], int(flag),flagname)
            v_result = '%s%s\n'%(v_result,Result['messages'])

        sResult['code'] = 0
        sResult['content'] = v_result
    except Exception, e:
        sResult['code'] = -1
        sResult['messages'] = '%s:%s' % (Exception, e)
    return JsonResponse(sResult)


@csrf_exempt
def wish_edit_update(request):
    '''
    更新该productid的平台在线信息
    :param request:
    :return:
    '''
    productid = request.GET.get('productid','')
    shopname = request.GET.get('shopname','')
    readonly = request.GET.get('readonly', '')

    if request.method == 'POST' and productid != '':
        try:
            t_wish_store_oplogs_obj = t_wish_store_oplogs(connection)
            Type = 'UpdataID'
            flagname = Type + '_%s_%s' % (mydatetime.now().strftime('%Y%m%d%H%M%S'), request.user.username)

            param = {}  # 操作日志的参数
            param['OpNum'] = flagname
            param['OpKey'] = [productid]
            param['OpType'] = Type
            param['Status'] = 'runing'
            param['ErrorInfo'] = ''
            param['OpPerson'] = request.user.first_name
            param['OpTime'] = mydatetime.now()
            param['OpStartTime'] = mydatetime.now()
            param['OpEndTime'] = None
            param['aNum'] = 1
            param['rNum'] = 0
            param['eNum'] = 0

            iResult = t_wish_store_oplogs_obj.createLog(param)
            assert iResult['errorcode'] == 0, "insert log error."
            uResult = to_updateInfors_byID(shopname,productid,request,flagname)
        except Exception, e:
            uResult = {'Code':-1,'messages':'%s:%s' % (Exception, e)}
        return HttpResponse(json.dumps(uResult))

    # 信息展示
    if productid != '':
        showDatas = show_infos_byID(productid,shopname)
        showDatas['readonly'] = readonly
        return render(request, 'wish_edit_update_store_product.html',showDatas)


def to_updateInfors_byID(shopname,productid,request,flagname):
    try:
        formdata = request.POST.get('formdata', '{}')
        formdata = eval(formdata)
        # logger.info('formdata1===============%s' % formdata)
        formdata['id'] = productid
        # logger.info('formdata2===============%s' % formdata)
        uResult = update_goods_information_by_wish_api(formdata, shopname, flagname)
    except Exception, e:
        uResult = {'Code':-1,'messages':'%s:%s' % (Exception, e)}
    return uResult


def show_infos_byID(productid,shopname):
    name = ''
    obj = t_online_info_wish_store.objects.filter(ProductID=productid)
    if obj.exists():
        name = obj[0].Title
    descri = ''
    tags = ''
    MainImage = ''
    all_extra_images = ''
    t_online_info_obj = t_online_info.objects.filter(ProductID=productid)
    if t_online_info_obj.exists():
        all_extra_images = t_online_info_obj[0].ExtraImages
        descri = t_online_info_obj[0].Description
        tags = t_online_info_obj[0].Tags
        MainImage = t_online_info_obj[0].Image

    vpic_list = []
    for online_obj in t_online_info_obj:
        if online_obj.ShopSKUImage:
            vpic_list.append(online_obj.ShopSKUImage)

    # 附图展示需要 排除 变体图 这里还没改
    extra_image_list = []
    if all_extra_images != '':
        for e_obj in all_extra_images.split('|'):
            if e_obj not in vpic_list:
                extra_image_list.append(e_obj)

    for i in range(0, 20 - len(extra_image_list)):
        extra_image_list.append('')

    return {
        'productid': productid,'extra_image_list':extra_image_list,
        'name':name,'descri':descri,'tags':tags,'shopname':shopname,'MainImage':MainImage
    }


def change_image(request):
    '''
    弹出图片修改的第二层
    :param request:
    :return:
    '''
    return render(request, 'change_image.html',{})

def refresh_sku_info(request):
    '''
    刷新商品SKU信息 商品状态和库存等
    :param request:
    :return:
    '''
    sResult = {}
    try:
        productid = request.GET.get('productid', '')

        classlisting_obj = classlisting(db_conn=connection,redis_conn=redis_coon)
        shopname = classlisting_obj.getShopName(productid)

        classshopsku_obj = classshopsku(db_conn=connection,redis_conn=redis_coon,shopname=shopname)
        py_SynRedis_tables_obj = py_SynRedis_tables()

        skulist = []
        for shopsku in classlisting_obj.getShopSKUList(productid):
            sku= classshopsku_obj.getSKU(shopsku)
            if sku is not None:
                skulist.append(sku)

        if skulist:
            py_SynRedis_tables_obj.UpdateSkuInfo(skulist)
        sResult['resultCode'] = '1'
        sResult['messages'] = u'同步SKU信息成功'
    except Exception as error:
        sResult['resultCode'] = '-1'
        sResult['messages'] = u'{}'.format(error)
    return JsonResponse(sResult)

def w_remark(request):
    productid = request.GET.get('productid','')
    readonly = request.GET.get('readonly','')
    id = request.GET.get('id','')
    if productid != '':
        if request.method == 'POST':
            sResult = {}
            remark = request.POST.get('alldata','')
            t_online_info_wish_store.objects.filter(ProductID=productid).update(Remarks=remark)
            sResult = {'code':0,'remark':remark}
            return HttpResponse(json.dumps(sResult))
        else:
            t_online_info_wish_store_obj = t_online_info_wish_store.objects.filter(ProductID=productid)
            remark = t_online_info_wish_store_obj[0].Remarks
            if id == '':
                id = t_online_info_wish_store_obj[0].id
            return render(request, 'change_remarks.html',
                          {'remark':remark,'productid':productid,'id':id, 'readonly': readonly})


def wish_store_update_title(request):
    protmp = request.GET.get('productid')
    if request.method == 'POST':
        try:
            t_wish_store_oplogs_obj = t_wish_store_oplogs(connection)
            ProObjs = t_online_info_wish_store.objects.filter(ProductID__in=protmp.split('|'))

            Type = 'UpdataIDTitle'
            flagname = Type + '_%s_%s' % (mydatetime.now().strftime('%Y%m%d%H%M%S'), request.user.username)

            param = {}  # 操作日志的参数
            param['OpNum'] = flagname
            param['OpKey'] = ProObjs.values_list('ProductID',flat=True)
            param['OpType'] = Type
            param['Status'] = 'runing'
            param['ErrorInfo'] = ''
            param['OpPerson'] = request.user.first_name
            param['OpTime'] = mydatetime.now()
            param['OpStartTime'] = mydatetime.now()
            param['OpEndTime'] = None
            param['aNum'] = len(ProObjs)
            param['rNum'] = 0
            param['eNum'] = 0

            iResult = t_wish_store_oplogs_obj.createLog(param)
            assert iResult['errorcode'] == 0, "insert log error."

            oldkeywords = request.POST.get('oldkeywords')
            newkeywords = request.POST.get('newkeywords')

            for Proobj in ProObjs:
                if Proobj.Title.lower().find(oldkeywords.lower()) == -1:
                    uResult = t_wish_store_oplogs_obj.updateStatusP(flagname,Proobj.ProductID,'error',u'该ProduceID没有发现需要修改的关键词')
                    assert uResult['errorcode'] == 0, uResult['errortext']
                    continue

                reg = re.compile(re.escape(oldkeywords), re.IGNORECASE)
                data = {
                    'id':Proobj.ProductID,
                    'name':reg.sub(newkeywords, Proobj.Title)
                }
                update_goods_information_by_wish_api.delay(data,Proobj.ShopName,flagname)
            sResult = {'Code':1,'messages':'','flagname':flagname}
        except Exception, e:
            sResult = {'Code': -1, 'messages': '%s:%s' % (Exception, e)}
        return HttpResponse(json.dumps(sResult))

    return render(request, 'wish_replace_title.html', {'protmp':protmp})


def wish_store_change_shipping(request):

    if request.method == 'POST':
        all_productid = request.POST.get('ProductID','')
        all_country = request.POST.getlist('Country',[])
        # IdList = []
        countrys_mo = ['FR', 'DE', 'JP', 'HU', 'ZA', 'US', 'FI', 'DK', 'PR', 'NL', 'NO', 'NZ', 'PL', 'CH', 'IT', 'CZ', 'AU', 'AT', 'IE', 'ES', 'SE', 'GB']
        for product in all_productid.split(','):
            insertobj = t_add_variant_information()
            insertobj.ProductID = product
            insertobj.Information   = json.dumps({'country':all_country,'country_mo':countrys_mo})
            insertobj.save()
            # IdList.append(insertobj.id)
            wish_change_shipping_to_country.delay([insertobj.id])

    # # 分页显示调价数据
    # contact_list = t_add_variant_information.objects.all()
    # paginator = Paginator(contact_list, 25)  # Show 25 contacts per page
    #
    # page = request.GET.get('page')
    # try:
    #     contacts = paginator.page(page)
    # except PageNotAnInteger:
    #     # If page is not an integer, deliver first page.
    #     contacts = paginator.page(1)
    # except EmptyPage:
    #     # If page is out of range (e.g. 9999), deliver last page of results.
    #     contacts = paginator.page(paginator.num_pages)
    #
    # return render(request, 'wish_store_change_shipping.html', {'contacts': contacts})
    return HttpResponseRedirect("/Project/admin/storeapp/t_add_variant_information/")


def refresh_process(request):
    name = request.GET.get('key')

    puyuan_log_opnum = ['add_sku', 'modify_sku', 'modify_binding', 'add_binding', 'delete_binding', 'sku_tort']
    puyuan_flag = 0
    for opnum in puyuan_log_opnum:
        if name.startswith(opnum):
            puyuan_flag = 1
            break
    if puyuan_flag == 1:
        operation_log = t_operation_log_online_syn_py
    else:
        operation_log = t_wish_store_oplogs

    sResult = {}
    sResult['resultCode'] = 0 # 初始状态
    try:
        operation_log_obj = operation_log(connection)

        # 同步店铺SKU绑定信息到普源，使用redis查询进程
        if name.startswith('add_binding'):
            sResult['resultCode'] = 1
            sResult['eSynLog'] = []
            objs = operation_log_obj.search_banding_schedule(opnum=name)
            if objs['endFlag'] == '1':
                sResult['resultCode'] = 2
            sResult['StartTime'] = objs['StartTime']
            sResult['EndTime'] = objs['EndTime']
            sResult['aNum'] = objs['aNum']
            sResult['rNum'] = objs['rNum']
            sResult['eNum'] = objs['eNum']
            sResult['etype'] = objs['etype']
            sResult['downinfo'] = objs['downinfo']
        elif name.split('_')[0] == 'Shopee':
            # Shopee店铺日志和进度条
            shopee_log_obj = t_shopee_oplogs(connection)
            sResult['resultCode'] = 1 # 正在进行操作
            p_count = shopee_log_obj.DoneOrNot(name)
            assert p_count['errorcode'] == 0, u"完成状态查询失败"
            if p_count['count'] == 0:
                sResult['resultCode'] = 2  # 所有操作已经完成
            log_shopee = shopee_log_obj.selectLogs(name)
            assert log_shopee['errorcode'] == 0,u"操作日志查询错误"
            sLogsList = []
            for logobj in log_shopee['OpLogs']:
                sResult['StartTime'] = logobj[7]
                sResult['EndTime'] = logobj[8]
                sResult['aNum'] = logobj[9]
                sResult['rNum'] = logobj[10]
                sResult['eNum'] = logobj[11]
                sResult['etype'] = logobj[1]
                sResult['downinfo'] = logobj[4]
                if logobj[3] == 'error':
                    sLogsList.append({'key':logobj[2],'mag':logobj[4]})
            sResult['eSynLog']   = sLogsList
        else:
            sResult['resultCode'] = 1  # 正在进行操作
            countObjs = operation_log_obj.DoneOrNot(name)
            assert countObjs['errorcode'] == 0, u"完成状态查询失败"
            if countObjs['count'] == 0:
                sResult['resultCode'] = 2  # 所有操作已经完成

            logobjs = operation_log_obj.selectLogs(name)
            assert logobjs['errorcode'] == 0,u"操作日志查询错误"
            sLogsList = []
            for logobj in logobjs['OpLogs']:
                sResult['StartTime'] = logobj[7]
                sResult['EndTime'] = logobj[8]
                sResult['aNum'] = logobj[9]
                sResult['rNum'] = logobj[10]
                sResult['eNum'] = logobj[11]
                sResult['etype'] = logobj[1]
                sResult['downinfo'] = logobj[4]

                if logobj[3] == 'error':
                    sLogsList.append({'key':logobj[2],'mag':logobj[4]})

            sResult['eSynLog']   = sLogsList
        
    except Exception,e:
        sResult['resultCode'] = -1
        sResult['errorText'] = '%s:%s'%(Exception,e)

    return JsonResponse(sResult)



def change_wish_express_type(request):
    sResult = {}
    sResult['resultCode'] = 0  # 初始状态
    try:
        id = request.GET.get('id')
        type_value = request.GET.get('value')

        t_online_info_wish_store.objects.filter(ProductID=id).update(WishExpressType=type_value)
        sResult['resultCode'] = 1
    except Exception, e:
        sResult['resultCode'] = -1
        sResult['errorText'] = '%s:%s' % (Exception, e)

    return JsonResponse(sResult)


def update_store_status(request):
    try:
        transaction.set_autocommit(False)
        t_online_info_wish_obj = t_online_info_wish(connection)

        id = request.GET.get('id')
        value = request.GET.get('value')

        config_objs = store_config.objects.filter(id=id)
        assert config_objs.exists(), u'id 未查到相关记录 id: %s' % id

        if config_objs[0].PlatformID == 'Wish':
            cResult = t_online_info_wish_obj.UpdateWishSNameByShopName(config_objs[0].ShopName_temp,value,f=1)
            assert cResult['errorcode'] == 1, cResult['errortext']

        config_objs.update(Status=value)

        transaction.commit()
        sResult = {'errorcode': 1, 'id': id, 'value': value}
    except Exception as e:
        transaction.rollback()
        sResult = {'errorcode': -1, 'errorText': u'%s' % e}

    return JsonResponse(sResult)



def seach_sku_infor(request):
    try:
        product_mainsku = request.GET.get('product_mainsku')
        classmainsku_obj = classmainsku(db_cnxn=connection)
        product_sku_list = classmainsku_obj.get_sku_by_mainsku(product_mainsku)
        product_sku_list = product_sku_list if product_sku_list else [product_mainsku,]

        enter_ed_objs = t_product_enter_ed.objects.filter(MainSKU=classsku(connection).get_bemainsku_by_sku(product_mainsku))
        ReverseLink = ''
        SupplierPUrl1 = ''
        for enter_ed_obj in enter_ed_objs:
            ReverseLink = enter_ed_obj.SourceURL
            SupplierPUrl1 = enter_ed_obj.SupplierPUrl1

        py_b_goods_objs = py_b_goods.objects.filter(SKU__in=product_sku_list)
        datalist = []
        for py_b_goods_obj in py_b_goods_objs:
            Image = u'http://fancyqube.net:89/ShopElf/images/%s.jpg' % py_b_goods_obj.SKU.replace('OAS-','').replace('FBA-', '')
            Name = py_b_goods_obj.GoodsName
            Weight = py_b_goods_obj.Weight
            Price = py_b_goods_obj.CostPrice

            if py_b_goods_obj.SalerName:
                SalerName = py_b_goods_obj.SalerName
            else:
                SalerName = py_b_goods_obj.SalerName2
            DevDate = py_b_goods_obj.DevDate
            Supplier = ''
            py_b_Supplier_objs = py_b_Supplier.objects.filter(NID=py_b_goods_obj.SupplierID)
            if py_b_Supplier_objs.exists():
                Supplier = py_b_Supplier_objs[0].SupplierName

            pack_Weight = 0
            py_b_packinfo_objs = py_b_packinfo.objects.filter(PackName=py_b_goods_obj.PackName)
            if py_b_packinfo_objs.exists():
                pack_Weight = py_b_packinfo_objs[0].Weight

            SupplierLink = SupplierPUrl1
            mainsku_sku_objs = t_product_mainsku_sku.objects.filter(SKU=py_b_goods_obj.SKU,)
            if mainsku_sku_objs.exists() and mainsku_sku_objs[0].SupplierLink:
                SupplierLink = mainsku_sku_objs[0].SupplierLink

            if not SupplierLink:
                SupplierLink = py_b_goods_obj.LinkUrl.split(';')[0]

            e_sku_infor = {
                'Image': Image,'Name': Name, 'Weight': Weight,'Price':Price,'Supplier':Supplier,
                'product_sku': py_b_goods_obj.SKU, 'pack_Weight': pack_Weight,'SalerName': SalerName,
                'DevDate':DevDate.strftime('%Y-%m-%dT%H:%M:%S'),'ReverseLink':ReverseLink, 'SupplierLink':SupplierLink,
                'SalerName2':py_b_goods_obj.SalerName2
            }
            datalist.append(e_sku_infor)

        if datalist:
            sResult = {'errorcode': 1, 'datalist': datalist}
        else:
            sResult = {'errorcode': 0, 'errorText': u'sku:%s,没有同步！' % product_mainsku}
    except Exception as e:
        sResult = {'errorcode': -1, 'errorText': u'%s' % e}
    return JsonResponse(sResult)


@csrf_exempt
def store_upload_image(request):
    try:
        PicFile = request.FILES.get('image')
        if PicFile:
            filename = 'wish_store/upload_pic_%s/%s.jpg' % (request.user.username, mydatetime.now().strftime('%Y%m%d%H%M%S'))
            auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
            bucket = oss2.Bucket(auth, ENDPOINT, BUCKETNAME_PIC)
            presult = bucket.put_object(filename, PicFile)
            _content = presult.__dict__
            PicPath = PREFIX + BUCKETNAME_PIC + '.' + ENDPOINT_OUT + '/' + filename
            if _content['status'] == 200:
                sResult = {'Code': '1', 'PicPath': PicPath, 'presult': _content['status']}
            else:
                sResult = {'Code': '0', 'PicPath': PicPath, 'presult': _content['status']}
        else:
            sResult = {'Code': '-1'}
    except Exception,e:
        sResult = {'Code': '-2', 'messages': '%s:%s' % (Exception, e)}
    return HttpResponse(json.dumps(sResult))


def upload_variant(variantData, shopname, request, synlist):
    t_wish_store_oplogs_obj = t_wish_store_oplogs(connection)
    Type = 'AddVariant'
    flagname = Type + '_%s_%s' % (mydatetime.now().strftime('%Y%m%d%H%M%S'), request.user.username)
    param = {}  # 操作日志的参数
    param['OpNum'] = flagname
    param['OpKey'] = [variantData['sku']]
    param['OpType'] = Type
    param['Status'] = 'runing'
    param['ErrorInfo'] = ''
    param['OpPerson'] = request.user.first_name
    param['OpTime'] = mydatetime.now()
    param['OpStartTime'] = mydatetime.now()
    param['OpEndTime'] = None
    param['aNum'] = 1
    param['rNum'] = 0
    param['eNum'] = 0
    try:
        iResult = t_wish_store_oplogs_obj.createLog(param)
        assert iResult['errorcode'] == 0, "insert log error."

        t_store_configuration_file_obj = t_store_configuration_file(connection)
        store_status = t_store_configuration_file_obj.getshopStatusbyshopcode(shopname)
        assert store_status['errorcode'] == 0, store_status['errortext']
        if store_status['status'] == '0':
            cwishapi_obj = cwishapi()

            auth_info = verb_token(shopname, connection)
            assert auth_info['errorcode'] == 1, auth_info['errortext']

            variantData['format'] = 'json'
            variantData['access_token'] = auth_info['access_token']

            if variantData.get('main_image'):  #
                main_image = variantData['main_image'].keys()[0]
                if variantData['main_image'][main_image] == '1':  # 本地上传图片
                    vResult = wish_image_upload(main_image, auth_info)
                    assert vResult['errorcode'] == 1, vResult['errortext']
                    variantData['main_image'] = vResult['image_url']
                else:
                    variantData['main_image'] = main_image

            vResult = cwishapi_obj.wish_variant_goods_add_api(variantData)
            assert vResult['errorcode'] == 1, vResult['errortext']

            wsResult = Wish_Data_Syn(synlist)
            assert wsResult['Code'] == 1, wsResult['messages']

            messages = u'变体增加成功！变体sku: %s' % variantData['sku']
        else:
            messages = u'该店铺: %s 状态已被标记为异常' % shopname

        uPResult = t_wish_store_oplogs_obj.updateStatusP(flagname, variantData['sku'], 'over', '')
        assert uPResult['errorcode'] == 0, uPResult['errortext']

        sResult = {'errorcode': 1, 'messages': messages}
    except Exception as e:
        sResult = {'errorcode': -1, 'errortext': u'%s' % e}
        t_wish_store_oplogs_obj.update_error(flagname, sResult['errortext'])
    return sResult

@csrf_exempt
def add_variant(request):
    product_id = request.GET.get('product_id')
    store_objs = t_online_info_wish_store.objects.get(ProductID=product_id)
    parent_sku = store_objs.ParentSKU
    if request.method == 'POST':
        shopname = store_objs.ShopName
        synlist = [shopname, product_id, parent_sku]
        variantData_str = request.POST.get('formData', '{}')
        variantData = eval(variantData_str)
        variantData['parent_sku'] = parent_sku
        sResult = upload_variant(variantData, shopname, request, synlist)
        return HttpResponse(json.dumps(sResult))
    try:
        t_platform_color_select_table_obj = t_platform_color_select_table(connection)
        colorlist = t_platform_color_select_table_obj.get_wish_color()
    except:
        colorlist = []
    return render(request, 'wish_store_add_variant.html',
        {'parent_sku': parent_sku,'colorlist': json.dumps(colorlist),'product_id':product_id}
    )


@csrf_exempt
def edit_shipping(request):
    product_id = request.GET.get('product_id')
    shopname   = request.GET.get('shopname')
    readonly   = request.GET.get('readonly', '')
    warehouse  = request.GET.get('warehouse', 'STANDARD')
    if request.method == 'POST':
        shipping_data_str = request.POST.get('post_data','[]')
        shipping_data_dict = eval(shipping_data_str)
        sResult = ergodic_shipping_setting(request, shipping_data_dict)
        return HttpResponse(json.dumps(sResult))
    else:
        try:
            auth_info = verb_token(shopname, connection)
            if auth_info['errorcode'] != 1:
                raise Exception(auth_info['errortext'])

            access_token = auth_info['access_token']

            rsplist = []
            if warehouse == 'STANDARD':
                rsp = cwishapi().Get_All_Shipping_Prices_of_a_Product({'access_token': access_token, 'product_id': product_id})
                if rsp['errorcode'] == 1:
                    for detail_shipping in rsp['shiping_infors']['ProductCountryAllShipping']['shipping_prices']:
                        rsplist.append(detail_shipping['ProductCountryShipping'])
                else:
                    raise Exception(rsp['errortext'])
            elif warehouse == 'FBW':
                raise Exception(u'<div style="margin:0 auto; width:320px; height:100px; text-align: center;line-height: 50px;color: red">{}</div>'.format('FBW的运费修改权限,暂未开通'))
            else:
                rsp = cwishapi().Get_Shipping_Prices_of_a_Product({'access_token': access_token, 'product_id': product_id, 'country': warehouse})
                if rsp['errorcode'] == 1:
                    rsplist.append(rsp['shiping_infors']['ProductCountryShipping'])
                else:
                    raise Exception(rsp['errortext'])

            countrys_code = t_country_code_name_table(connection).GetAllCountryCode()
            if countrys_code['errorcode'] != 1:
                raise Exception(countrys_code['errortext'])

            return render(request, 'edit_shipping_other_country.html',
                {'errorcode': 1,'product_id': product_id, 'shopname': shopname, 'readonly': readonly,
                'rsplist':sorted(rsplist, key=lambda x: x['country_code']),'countrys_code': countrys_code['data'],
                 'warehouse': warehouse}
            )
        except Exception as error:
            return render(request, 'edit_shipping_other_country.html',
                {'errorcode': -1, 'errortext': u'{}'.format(error),
                 'product_id': product_id, 'shopname': shopname, 'readonly': readonly, 'warehouse': warehouse}
            )


def ergodic_shipping_setting(request, shippingDataList):
    product_id = request.GET.get('product_id')
    shopname = request.GET.get('shopname')
    warehouse = request.GET.get('warehouse', 'STANDARD')

    try:
        t_wish_store_oplogs_obj = t_wish_store_oplogs(connection)
        Type = 'Edit_Shipping_Price'
        flagname = Type + '_%s_%s' % (mydatetime.now().strftime('%Y%m%d%H%M%S'), request.user.username)

        param = {}  # 操作日志的参数
        param['OpNum'] = flagname
        param['OpKey'] = ['{}_{}'.format(product_id, tmp['country'])  for tmp in shippingDataList]
        param['OpType'] = Type
        param['Status'] = 'runing'
        param['ErrorInfo'] = ''
        param['OpPerson'] = request.user.first_name
        param['OpTime'] = mydatetime.now()
        param['OpStartTime'] = mydatetime.now()
        param['OpEndTime'] = None
        param['aNum'] = len(shippingDataList)
        param['rNum'] = 0
        param['eNum'] = 0

        iResult = t_wish_store_oplogs_obj.createLog(param)
        assert iResult['errorcode'] == 0, "insert log error."

        auth_info = verb_token(shopname=shopname, conn=connection)
        assert auth_info['errorcode'] == 1, auth_info['errortext']

        warehouse_obj = t_wish_shopcode_warehouse(connection)
        wResult = warehouse_obj.get_warehouse(shopname)
        assert wResult['errorcode'] == 1, wResult['errortext']
        if not wResult['warehouse'].has_key(warehouse):
            raise Exception(u'该店铺没有相应的仓库:%s,店铺所有仓库:%s' % (warehouse, wResult['warehouse']))

        cwishapi_obj = cwishapi()

        show_log_text = u'{}, 运费修改日志：\n'.format(product_id)
        for shippingData in shippingDataList:
            shippingData['id'] = product_id
            shippingData['format']         = 'json'
            shippingData['access_token']   = auth_info['access_token']
            shippingData['warehouse_name'] = wResult['warehouse'][warehouse]
            # if not shippingData.get('wish_express'):

            edit_result = cwishapi_obj.edit_shipping_price_of_a_product(shippingData)
            # edit_result = {'errorcode': -1, 'errortext': u'测试测试测试测试'}
            if edit_result['errorcode'] == 1:
                uPResult = t_wish_store_oplogs_obj.updateStatusP(flagname, '{}_{}'.format(product_id, shippingData['country']), 'over', '')
                utext = uPResult['errortext'] if uPResult['errorcode'] == -1 else ''
                show_log_text += u'国家: {}; 修改成功！{}\n'.format(shippingData['country'], utext)
            else:
                uPResult = t_wish_store_oplogs_obj.updateStatusP(flagname,'{}_{}'.format(product_id, shippingData['country']),'error', edit_result['errortext'])
                utext = uPResult['errortext'] if uPResult['errorcode'] == -1 else ''
                show_log_text += u'国家: {}; 修改失败！错误原因: {}, {} \n'.format(shippingData['country'], edit_result['errortext'], utext)

        return {'errorcode': 1, 'logs': show_log_text}
    except Exception as error:
        return {'errorcode': -1, 'errortext': u'{}'.format(error)}



# def batch_update_shipping(request):


















