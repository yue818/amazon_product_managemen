#-*-coding:utf-8-*-

u"""
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: wish_store.py
 @time: 2018-05-07 8:51
"""
import sys
import os,sys
sys.path.append('/data/djangostack-1.9.7/apps/django/django_projects/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE','Project.settings')

import logging,json

# 这个用的是 Django 语法，如果别处调用，请修改下    to_wait_publish
from skuapp.table.t_online_info import t_online_info as product_infos   #从这里取值
from wishpubapp.table.t_templet_wish_publish_draft import t_templet_wish_publish_draft  # 到这里存放

from django.db import connection
from django_redis import get_redis_connection
redis_coon = get_redis_connection(alias='product')
from datetime import datetime as syntime

from brick.wish.api.wishapi import cwishapi
from brick.table.t_online_info import t_online_info
from brick.wish.wishlisting import refreshwishlisting
from brick.classredis.classshopsku import classshopsku
from brick.classredis.classlisting import classlisting
from brick.table.t_online_api_return_code_business_language_comparison import t_online_api_return_code_business_language_comparison
from brick.table.t_online_info_wish import t_online_info_wish

from brick.table.t_store_configuration_file import t_store_configuration_file

from brick.table.t_wish_store_oplogs import t_wish_store_oplogs

from brick.wish.wish_api_before.token_verification import verb_token

import xlwt
from Project.settings import MEDIA_ROOT, BUCKETNAME_XLS
from brick.public.create_dir import mkdir_p
from brick.public.generate_excel import generate_excel
from brick.public.upload_to_oss import upload_to_oss
from brick.wish.wish_pub.wish_image_upload import wish_image_upload
from brick.table.t_wish_shopcode_warehouse import t_wish_shopcode_warehouse

import traceback
logger = logging.getLogger('sourceDns.webdns.views')


def CreateParam(shopname,productid,parentsku):
    auth_info = verb_token(shopname, connection)
    assert auth_info['errorcode'] == 1, auth_info['errortext']

    params = {
        'access_token': auth_info['access_token'],
        'ProductID': productid,
        'ParentSKU':''
    }  # api参数
    if parentsku:
        params['ParentSKU'] = parentsku
    return params


def business_Terms(_content):
    comparison_obj = t_online_api_return_code_business_language_comparison(connection)
    bt = comparison_obj.get_bl_by_code(_content.get('code'))
    if bt is None:
        comparison_obj.insert_code_message(
            _content.get('code'), _content.get('message')
        )
        bt = _content.get('message')
    if _content.get('code') is None:
        bt = '%s' % _content
    return bt


def ToCalculateADS(productid,shopname,dbconn):
    try:
        t_online_info_obj = t_online_info(shopname,dbconn)
        rResult = t_online_info_obj.getonlinestatusbyproductid(productid)
        assert rResult['errorcode'] == 0,rResult['errortext']
        if rResult['Status'] == 'Enabled' and rResult['ReviewState'] == 'approved':
            return '1'
        else:
            return '0'
    except Exception,e:
        rResult = {'errorcode': -1, 'errortext': '%s:%s' % (Exception, e)}
    return rResult


def Wish_Data_Syn(list,synname=''):
    sresult = {'Code':0,'messages':''}
    try :
        shopname  = list[0]
        productid = list[1]
        parentsku = list[2]

        upstatus = 'over'  # 日志 状态 更新
        uptext = None

        t_store_configuration_file_obj = t_store_configuration_file(connection)
        t_wish_store_oplogs_obj = t_wish_store_oplogs(connection)
        t_online_info_wish_obj = t_online_info_wish(connection)

        store_status = t_store_configuration_file_obj.getshopStatusbyshopcode(shopname)  # 获取店铺状态
        assert store_status['errorcode'] == 0, store_status['errortext']

        if store_status['status'] == '0':  # 店铺状态正常的
            snstatus = '0'   # listing 店铺状态标记
            cwishapi_obj = cwishapi()
            classlisting_obj = classlisting(db_conn=connection, redis_conn=redis_coon)
            t_online_info_obj = t_online_info(shopname, connection, redis_coon)

            params = CreateParam(shopname, productid, parentsku)

            result = cwishapi_obj.update_wish_goods_data(param=params,timeout=30)
            _content = eval(result._content)

            if result.status_code == 200 and _content['code'] == 0:  # api 调用成功
                t_online_info_obj.insertWishV2([_content.get('data', [])])  # 更新到t_online_info

                toResult = ToCalculateADS(productid, shopname, connection)
                assert toResult in ['0', '1'], toResult['errortext']  # 获取该product的在线不在线的状态

                sresult['messages'] = u'%s:同步成功'%(productid,)
            else:  # 调用失败
                if _content.get('code') in [1000, 1028, 1006, 1031]:  #
                    toResult = ToCalculateADS(productid, shopname, connection)
                    assert toResult in ['0', '1'], toResult['errortext']  # 获取该product的在线不在线的状态
                else:
                    toResult = '-1'

                upstatus = 'error'
                uptext = business_Terms(_content)

                # 更新下 redis中shopskulist
                classlisting_db = classlisting(db_conn=connection)
                all_shopsku = classlisting_db.getShopSKUList(productid)
                classlisting_obj.setShopSKUList(productid, '|'.join(all_shopsku))
                sresult['messages'] = u'%s:%s' % (productid, business_Terms(_content))

            refreshwishlisting.run({'ShopName': shopname, 'dbcnxn': connection, 'ProductID': productid})  # Wish数据更新操作

            adResult = t_online_info_wish_obj.UpdateWishStatusAD(productid, toResult)  # listing
            assert adResult['errorcode'] == 1, adResult['errortext']
        else:
            upstatus = 'error'
            snstatus = '-1'  # listing 店铺状态标记
            uptext = u'店铺状态被标记为异常'
            sresult['messages'] = u'%s:%s' % (productid, uptext)

        SNResult = t_online_info_wish_obj.UpdateWishSNameByShopName(shopname, snstatus)  # listing
        assert SNResult['errorcode'] == 1, SNResult['errortext']

        uResult = t_wish_store_oplogs_obj.updateStatusP(synname, productid, upstatus, uptext)  # 更新日志表状态
        assert uResult['errorcode'] == 0, uResult['errortext']

        sresult['Code'] = 1
    except Exception, e:
        sresult['Code'] = -1
        sresult['messages'] = '%s:%s;%s' % (Exception, e, traceback.format_exc())
    return sresult


def OnTheShelf_OR_LowerFrame(list,flag,synname):
    sresult = {'Code': 0, 'messages': ''}
    try:
        shopname = list[0]
        productid = list[1]
        parentsku = list[2]

        upstatus = 'over'  # 日志
        uptext = None

        t_store_configuration_file_obj = t_store_configuration_file(connection)
        t_wish_store_oplogs_obj = t_wish_store_oplogs(connection)
        t_online_info_wish_obj = t_online_info_wish(connection)

        store_status = t_store_configuration_file_obj.getshopStatusbyshopcode(shopname)  # 获取店铺状态
        assert store_status['errorcode'] == 0, store_status['errortext']

        if store_status['status'] == '0':  # 店铺状态正常的
            snstatus = '0'  # listing 店铺状态标记

            classlisting_obj = classlisting(db_conn=connection, redis_conn=redis_coon)
            cwishapi_obj = cwishapi()
            classshopsku_obj = classshopsku(redis_conn=redis_coon,shopname=shopname)

            t_online_info_obj = t_online_info(shopname, connection, redis_coon)

            params = CreateParam(shopname, productid, parentsku)

            if flag == 'enable':
                Status = 'Enabled'
                result = cwishapi_obj.enable_by_wish_api(params,timeout=30)
            else:
                Status = 'Disabled'
                result = cwishapi_obj.disable_by_wish_api(params,timeout=30)

            _content = eval(result._content)

            if result.status_code == 200 and _content['code'] == 0:
                aResult = t_online_info_wish_obj.UpdateWishStatus(productid, Status)
                assert aResult['errorcode'] == 1, aResult['errortext']

                iResult = t_online_info_obj.update_status_by_productid(Status, productid)
                assert iResult['errorcode'] == 0, "SynSuccess:%s" % iResult['errortext']

                shopskulist = classlisting_obj.getShopSKUList(productid)
                if shopskulist is None:
                    shopskulist = []
                for shopsku in shopskulist:
                    classshopsku_obj.setStatus(shopsku, Status)

                toResult = ToCalculateADS(productid, shopname, connection)
                assert toResult in ['0', '1'], toResult['errortext']  # 获取该product的在线不在线的状态

                if flag == 'enable':
                    sresult['messages'] = u'%s:上架成功' % (productid,)
                else:
                    sresult['messages'] = u'%s:下架成功' % (productid,)
            else:
                if _content.get('code') in [1000, 1028, 1006, 1031]:  # 平台禁止修改加钻产品标题
                    toResult = ToCalculateADS(productid, shopname, connection)
                    assert toResult in ['0', '1'], toResult['errortext']  # 获取该product的在线不在线的状态

                else:
                    toResult = '-1'  # 单链接操作状态

                upstatus = 'error'
                uptext = business_Terms(_content)
                sresult['messages'] = u'%s:%s' % (productid, business_Terms(_content))

            refreshwishlisting.run({'ShopName': shopname, 'dbcnxn': connection, 'ProductID': productid})  # Wish数据更新操作

            adResult = t_online_info_wish_obj.UpdateWishStatusAD(productid, toResult)
            assert adResult['errorcode'] == 1, adResult['errortext']
        else:
            upstatus = 'error'
            snstatus = '-1'  # listing 店铺状态标记
            uptext = u'店铺状态被标记为异常'
            sresult['messages'] = u'%s:%s' % (productid, uptext)

        uResult = t_wish_store_oplogs_obj.updateStatusP(synname, productid, upstatus, uptext)
        assert uResult['errorcode'] == 0, uResult['errortext']

        SNResult = t_online_info_wish_obj.UpdateWishSNameByShopName(shopname, snstatus)  # listing
        assert SNResult['errorcode'] == 1, SNResult['errortext']

        sresult['Code'] = 1
    except Exception, e:
        sresult['Code'] = -1
        sresult['messages'] = '%s:%s' % (Exception,e)
    return sresult


def OnTheShelf_OR_LowerFrame_BY_ShopSKU(shopsku,shopname,flag,flagname=''):
    myresult = {'Code': 0, 'messages': ''}
    try:
        upstatus = 'over'  # 日志
        uptext = None

        t_wish_store_oplogs_obj = t_wish_store_oplogs(connection)
        t_store_configuration_file_obj = t_store_configuration_file(connection)
        t_online_info_wish_obj = t_online_info_wish(connection)

        store_status = t_store_configuration_file_obj.getshopStatusbyshopcode(shopname)  # 获取店铺状态
        assert store_status['errorcode'] == 0, store_status['errortext']

        if store_status['status'] == '0':  # 店铺状态正常的
            snstatus = '0'  # 店铺状态
            classshopsku_obj = classshopsku(redis_conn=redis_coon, shopname=shopname)
            cwishapi_obj = cwishapi()
            t_online_info_obj = t_online_info(shopname, connection)

            auth_info = verb_token(shopname, connection)
            assert auth_info['errorcode'] == 1, auth_info['errortext']

            data = {}
            data['access_token'] = auth_info.get('access_token', '')
            data['ShopSKU'] = shopsku

            proinfo = t_online_info_obj.get_listingid_by_shopname_shopsku(shopsku)
            assert proinfo['errorcode'] == 0, 'EDGetProductIDSuccess:%s' % proinfo['errortext']

            if flag == 'enshopsku':  # ShopSKU上架
                sstatus = 'Enabled'
                result = cwishapi_obj.update_to_enable(data,timeout=30)
            else:
                sstatus = 'Disabled'
                result = cwishapi_obj.update_to_disable(data,timeout=30)

            _content = eval(result._content)

            if result.status_code == 200 and _content['code'] == 0:
                uResult = t_online_info_obj.update_status_by_shopsku(sstatus, shopsku)  # 更新shopsku状态数据
                assert uResult['errorcode'] == 0,'EDSuccess:%s' % uResult['errortext']

                classshopsku_obj.setStatus(shopsku, sstatus)  # 修改redis数据

                toResult = ToCalculateADS(proinfo['productid'], shopname, connection)
                assert toResult in ['0', '1'], toResult['errortext']  # 获取该product的在线不在线的状态

                if flag == 'enshopsku':  # ShopSKU上架
                    myresult['messages'] = u'%s:上架成功' % (shopsku,)
                else:
                    myresult['messages'] = u'%s:下架成功' % (shopsku,)
            else:
                if _content.get('code') in [1000, 1028, 1006, 1031]:  # 平台禁止修改加钻产品标题
                    toResult = ToCalculateADS(proinfo['productid'], shopname, connection)
                    assert toResult in ['0', '1'], toResult['errortext']  # 获取该product的在线不在线的状态
                else:
                    toResult = '-1'

                upstatus = 'error'  # 日志
                uptext = business_Terms(_content)
                myresult['messages'] = u'%s:上下架操作失败!%s' % (shopsku, business_Terms(_content))

            refreshwishlisting.run({'ShopName': shopname, 'dbcnxn': connection, 'ProductID': proinfo['productid']})  # Wish数据更新操作

            adResult = t_online_info_wish_obj.UpdateWishStatusAD(proinfo['productid'], toResult)
            assert adResult['errorcode'] == 1, adResult['errortext']

            myresult['_content'] = _content
        else:
            upstatus = 'error'
            snstatus = '-1'  # listing 店铺状态标记
            uptext = u'店铺状态被标记为异常'
            myresult['_content'] = uptext
            myresult['messages'] = u'%s:上下架操作失败!%s' % (shopsku, uptext)

        uPResult = t_wish_store_oplogs_obj.updateStatusP(flagname, shopsku, upstatus, uptext)
        assert uPResult['errorcode'] == 0, uPResult['errortext']

        SNResult = t_online_info_wish_obj.UpdateWishSNameByShopName(shopname, snstatus)  # shopname
        assert SNResult['errorcode'] == 1, SNResult['errortext']

        myresult['Code'] = 1
    except Exception, e:
        myresult['Code'] = -1
        myresult['messages'] = '%s:%s:%s' % (shopsku,Exception, e)
    return myresult



def edit_GoodsInformation_by_ID(datadict,ShopName,flagname):
    myresult = {'Code':0,'messages':''}
    try:
        uptext = None
        upstatus = 'over'  # 日志

        t_wish_store_oplogs_obj        = t_wish_store_oplogs(connection)
        t_store_configuration_file_obj = t_store_configuration_file(connection)
        t_online_info_wish_obj = t_online_info_wish(connection)

        store_status = t_store_configuration_file_obj.getshopStatusbyshopcode(ShopName)  # 获取店铺状态
        assert store_status['errorcode'] == 0, store_status['errortext']

        if store_status['status'] == '0':  # 店铺状态正常的
            snstatus = '0'

            cwishapi_obj = cwishapi()

            auth_info = verb_token(ShopName, connection)
            assert auth_info['errorcode'] == 1, auth_info['errortext']

            datadict['access_token'] = auth_info.get('access_token','')
            datadict['format'] = 'json'

            if datadict.get('main_image'):  # 主图发生改变
                mainimage = datadict['main_image'].keys()[0]
                if datadict['main_image'][mainimage] == '1':  # 本地上传图片
                    mResult = wish_image_upload(mainimage, auth_info)
                    assert mResult['errorcode'] == 1, mResult['errortext']
                    datadict['main_image'] = mResult['image_url']
                else:
                    datadict['main_image'] = mainimage.replace('-medium.','-original.')

            eImage_list = []
            for eImage in datadict.get('extra_images', []):
                e_pic = eImage.keys()[0]
                if eImage[e_pic] == '1':
                    evResult = wish_image_upload(e_pic, auth_info)
                    assert evResult['errorcode'] == 1, evResult['errortext']
                    eImage_list.append(evResult['image_url'])
                else:
                    eImage_list.append(e_pic.replace('-medium.','-original.'))

            if eImage_list:
                datadict['extra_images'] = '|'.join(eImage_list)

            logger.info('datadict===============%s' % datadict)
            rtresult = cwishapi_obj.update_goods_info_by_wish_api(datadict,timeout=30)
            _content = eval(rtresult._content)

            if rtresult.status_code ==200 and _content['code'] == 0:

                toResult = ToCalculateADS(datadict['id'], ShopName, connection)
                assert toResult in ['0', '1'], toResult['errortext']  # 获取该product的在线不在线的状态

                myresult['messages'] = u'%s:链接信息修改成功'%(datadict['id'],)
            else:
                if _content.get('code') in [1000, 1028, 1006, 1031]:  # 平台禁止修改加钻产品标题
                    toResult = ToCalculateADS(datadict['id'], ShopName, connection)
                    assert toResult in ['0', '1'], toResult['errortext']  # 获取该product的在线不在线的状态

                else:
                    toResult = '-1'
                upstatus = 'error'  # 日志
                uptext = business_Terms(_content)

                myresult['messages'] = u'%s:链接信息修改失败，%s' % (datadict['id'],uptext)

            dResult = Wish_Data_Syn([ShopName, datadict['id'], ''], 'syn')
            assert dResult['Code'] == 1, dResult['messages']

            adResult = t_online_info_wish_obj.UpdateWishStatusAD(datadict['id'], toResult)
            assert adResult['errorcode'] == 1, adResult['errortext']

            myresult['_content'] = _content
        else:
            upstatus = 'error'
            snstatus = '-1'  # listing 店铺状态标记
            uptext = u'店铺状态被标记为异常'
            myresult['_content'] = uptext
            myresult['messages'] = u'%s:链接信息修改失败，%s' % (datadict['id'], uptext)

        uResult = t_wish_store_oplogs_obj.updateStatusP(flagname, datadict['id'], upstatus, uptext)
        assert uResult['errorcode'] == 0, uResult['errortext']

        SNResult = t_online_info_wish_obj.UpdateWishSNameByShopName(ShopName, snstatus)  # shopname
        assert SNResult['errorcode'] == 1, SNResult['errortext']

        myresult['Code'] = 1
    except Exception, e:
        myresult['Code'] = -1
        myresult['messages'] = '%s:%s:%s' % (datadict['id'],Exception, e)
    return myresult



def download_excel_by_porductid(list, opname='', warehouse='STANDARD'):
    myresult = {}
    try:
        classlisting_obj = classlisting(connection, redis_coon)

        t_wish_store_oplogs_obj = t_wish_store_oplogs(connection)

        username = opname.split('-')[-1]
        path = MEDIA_ROOT + 'download_xls/' + username
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))

        mkdir_p(path)
        os.popen('chmod 777 %s' % (path, ))

        datalist = []
        datalist.append(['shopname', 'productid', 'sku', 'shopsku', 'Inventory'])

        num = len(list)
        for i, elist in enumerate(list):
            shopname = elist[0]
            productid = elist[1]
            parentsku = elist[2]

            classshopsku_obj = classshopsku(connection, redis_coon,shopname=shopname)

            shopskulist = classlisting_obj.getJoomShopSKUList(productid)
            for shopsku in shopskulist:
                sku = classshopsku_obj.getSKU(shopsku)

                if warehouse == 'STANDARD':
                    inventory = classshopsku_obj.getQuantity(shopsku)
                else:
                    q = getattr(classshopsku_obj, 'getWish%sQuantity' % warehouse)
                    inventory = q(shopsku)
                datalist.append([shopname, productid, sku, shopsku, inventory])

            if i < num - 1:
                uResult = t_wish_store_oplogs_obj.updateStatusP(opname, opname, 'runing', '')
                assert uResult['errorcode'] == 0, uResult['errortext']

        filename = username + '_' + syntime.now().strftime('%Y%m%d%H%M%S') + '.xls'

        eResult = generate_excel(datalist, path + '/' + filename)
        assert eResult['code'] == 0, eResult['error']

        os.popen(r'chmod 777 %s' % (path + '/' + filename))

        upload_to_oss_obj = upload_to_oss(BUCKETNAME_XLS)
        upResult = upload_to_oss_obj.upload_to_oss({
            'path': username,
            'name': filename,
            'byte': open(path + '/' + filename),
            'del': 0
        })
        assert upResult['errorcode'] == 0, upResult['errortext']

        filepath = upResult['result']

        uResult = t_wish_store_oplogs_obj.updateStatusP(opname, opname, 'over', filepath)
        assert uResult['errorcode'] == 0, uResult['errortext']

        myresult['Code'] = 1
        myresult['messages'] = u'文件生成成功! \n 下载链接：%s' % (filepath,)
    except Exception, e:
        myresult['Code'] = -1
        myresult['messages'] = '%s:%s:%s' % (opname, Exception, e)
    return myresult


# 将现有的链接转到  待刊登
def to_wait_publish(datalist, opname, opPerson):
    t_wish_store_oplogs_obj = t_wish_store_oplogs(connection)
    product_id = datalist[1]
    try:
        product_objs = product_infos.objects.filter(ProductID=product_id)

        title, descri, tags, extraimages, mainimage = '', '', '', '', ''
        if len(product_objs) > 0:
            title        = product_objs[0].Title
            descri       = product_objs[0].Description
            tags         = product_objs[0].Tags
            extraimages  = product_objs[0].ExtraImages
            mainimage    = product_objs[0].Image

        maindict = {}
        maindict['MSRP'] = ''
        maindict['Price'] = ''
        maindict['Shipping'] = ''
        maindict['ShippingTime'] = ''
        maindict['KC'] = ''
        maindict['ParentSKU'] = ''
        maindict['MainProfitRate'] = ''

        maininfo = json.dumps(maindict)

        vList, vImage_list, mainsku_list = [], [], []
        for product_obj in product_objs:
            vDict = {}
            vDict['vPic']         = product_obj.ShopSKUImage
            if product_obj.ShopSKUImage:
                vImage_list.append(product_obj.ShopSKUImage.strip())

            vDict['SKU']          = product_obj.SKU
            vDict['ShopSKU']      = ''
            vDict['Color']        = product_obj.Color
            vDict['Size']         = product_obj.Size
            vDict['Msrp']         = str(product_obj.msrp)
            vDict['Price']        = str(product_obj.Price)
            vDict['ProfitRate']   = ''
            vDict['Kc']           = str(product_obj.Quantity)
            vDict['Shipping']     = str(product_obj.Shipping)
            vDict['Shippingtime'] = product_obj.ShippingTime

            if product_obj.MainSKU:
                mainsku_list.append(product_obj.MainSKU)

            vList.append(vDict)

        variants = json.dumps(vList)

        mainsku = ' '.join(set(mainsku_list))

        A_extraList = [eImage.strip() for eImage in extraimages.split('|') if eImage.strip()]  # 所有附图 包括 变体图
        extraimages_list = list(set(A_extraList) ^ set(vImage_list))  # 求 附图和变体图的差集

        extraimages = '|'.join(extraimages_list)

        publish_draft = t_templet_wish_publish_draft(
            Title = title, Description = descri, Tags = tags, MainSKU = mainsku, MainInfo = maininfo,
            MainImage = mainimage, ExtraImages = extraimages, Variants = variants, Status = 'notyet',
            CreateStaff = opPerson, CreateTime = syntime.now(), ShopName = None
        )
        publish_draft.save()

        uResult = t_wish_store_oplogs_obj.updateStatusP(opname, product_id, 'over', '')
        assert uResult['errorcode'] == 0, uResult['errortext']

        return {'Code': 1, 'messages': ''}
    except Exception as e:
        errortext = u'%s' % e
        t_wish_store_oplogs_obj.updateStatusP(opname, product_id, 'error', errortext)
        return {'Code': -1, 'messages': errortext}


def all_shipping_list(paramlsit):
    classshopsku_obj = classshopsku(db_conn=connection, redis_conn=redis_coon, shopname=paramlsit[0])
    classlisting_obj = classlisting(db_conn=connection, redis_conn=redis_coon)
    shopskulist = classlisting_obj.getShopSKUList(paramlsit[1])
    shippinglist = []
    for shopsku in shopskulist:
        shipping = classshopsku_obj.getShipping(shopsku)
        shippinglist.append(float(shipping))
    return shippinglist


def MainBatchUpdateShipping(paramlsit, synname, warehouse):
    try:
        shippingDataList = eval(paramlsit[2])

        auth_info = verb_token(shopname=paramlsit[0], conn=connection)
        assert auth_info['errorcode'] == 1, auth_info['errortext']

        warehouse_obj = t_wish_shopcode_warehouse(connection)
        wResult = warehouse_obj.get_warehouse(paramlsit[0])
        assert wResult['errorcode'] == 1, wResult['errortext']
        if not wResult['warehouse'].has_key(warehouse):
            raise Exception(u'该店铺没有相应的仓库:%s,店铺所有仓库:%s' % (warehouse, wResult['warehouse']))

        cwishapi_obj = cwishapi()
        t_wish_store_oplogs_obj = t_wish_store_oplogs(connection)

        show_log_text = ''
        for shippingData in shippingDataList:
            shippingData['id'] = paramlsit[1]
            shippingData['format'] = 'json'
            shippingData['access_token'] = auth_info['access_token']
            shippingData['warehouse_name'] = wResult['warehouse'][warehouse]

            if shippingData.get('_add') and int(shippingData.get('_add').strip()) != 0:# 原有基础上增加 运费
                rsp = cwishapi().Get_Shipping_Prices_of_a_Product(
                    {'access_token': auth_info['access_token'], 'product_id': paramlsit[1], 'country': shippingData['country']}
                )
                _add = shippingData.pop('_add')
                if rsp['errorcode'] == 1:
                    if rsp['shiping_infors']['ProductCountryShipping']['use_product_shipping'] == 'True':
                        shippinglist = all_shipping_list(paramlsit)
                        shippingData['price'] = str(max(shippinglist) + float(_add))
                    else:
                        shippingData['price'] = str(float(rsp['shiping_infors']['ProductCountryShipping']['shipping_price']) + float(_add))
                else:
                    raise Exception(rsp['errortext'])

            elif shippingData.get('_add') and int(shippingData.get('_add').strip()) == 0:
                shippinglist = all_shipping_list(paramlsit)
                shippingData['price'] = str(max(shippinglist))

            edit_result = cwishapi_obj.edit_shipping_price_of_a_product(shippingData)
            # edit_result = {'errorcode': -1, 'errortext': json.dumps(shippingData)}
            keyone = '{}_{}'.format(paramlsit[1], shippingData['country'])
            if edit_result['errorcode'] == 1:
                uPResult = t_wish_store_oplogs_obj.updateStatusP(synname, keyone, 'over', '')
                utext = uPResult['errortext'] if uPResult['errorcode'] == -1 else ''
                show_log_text += u'ProductID: {},国家: {}; 修改成功！{}\n'.format(paramlsit[1],shippingData['country'], utext)
            else:
                uPResult = t_wish_store_oplogs_obj.updateStatusP(synname, keyone,'error', edit_result['errortext'])
                utext = uPResult['errortext'] if uPResult['errorcode'] == -1 else ''
                show_log_text += u'ProductID: {},国家: {}; 修改失败！错误原因: {}, {} \n'.format(paramlsit[1],shippingData['country'], edit_result['errortext'], utext)
        return {'Code': 1, 'messages': ''}
    except Exception as error:
        return {'Code': -1, 'messages': '%s:%s' % (synname, error)}























