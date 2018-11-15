# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from Project.settings import *
from urllib import urlencode
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from Project.settings import *
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from aliapp.models import *
from datetime import datetime as mydatetime
from app_djcelery.tasks import refresh_online_info_by_ali_api,enable_products_by_ali_api,disable_products_by_ali_api,syn_products_by_ali_api
from app_djcelery.tasks import edit_productSKU_stock_by_ali_api,edit_productSKU_price_by_ali_api,edit_product_by_ali_api,upload_product_by_ali_api
import json, copy, urllib2, time
from brick.classredis.classlisting import classlisting
from brick.classredis.classshopsku import classshopsku
from django.db import connection
from django_redis import get_redis_connection
from brick.classredis.classsku import classsku

from brick.pydata.py_redis.py_redis_ali_sku import py_redis_ali_sku

from brick.pydata.py_redis.py_SynRedis_tables import py_SynRedis_tables
from brick.pricelist.calculate_price import calculate_price
from brick.classredis.classshopsku import classshopsku
# from Project.settings import connRedis
redis_conn = get_redis_connection(alias='product')
classshopskuobjs = classshopsku(connection, redis_conn)
py_SynRedis_tables_obj = py_SynRedis_tables()
# redis_conn = connRedis
logger = logging.getLogger('sourceDns.webdns.views')
api_url = 'http://47.100.224.71'


def insert_into_action_temp(action_temp):
    t_erp_aliexpress_action_temp_obj = t_erp_aliexpress_action_temp()
    t_erp_aliexpress_action_temp_obj.shopName = action_temp.get('shopName','')
    t_erp_aliexpress_action_temp_obj.accountName = action_temp.get('accountName','')
    t_erp_aliexpress_action_temp_obj.action_type = action_temp.get('action_type','')
    t_erp_aliexpress_action_temp_obj.action_param = action_temp.get('action_param','')
    t_erp_aliexpress_action_temp_obj.action_result = action_temp.get('action_result','')
    t_erp_aliexpress_action_temp_obj.action_time = action_temp.get('action_time','')
    t_erp_aliexpress_action_temp_obj.action_user = action_temp.get('action_user','')
    t_erp_aliexpress_action_temp_obj.table_name = action_temp.get('table_name','')
    t_erp_aliexpress_action_temp_obj.field_name = action_temp.get('field_name','')
    t_erp_aliexpress_action_temp_obj.old_value = action_temp.get('old_value','')
    t_erp_aliexpress_action_temp_obj.action_id = action_temp.get('action_id','')
    t_erp_aliexpress_action_temp_obj.save()
    id = t_erp_aliexpress_action_temp_obj.id
    return id


# 刷新店铺在线商品信息
# request 请求
# 返回sResult刷新进度结果
def refresh_ali_online_info_by_shopname(request):
    shopname = request.GET.get('shopname', '')
    flag = request.GET.get('flag','')
    bar = request.GET.get('bar','')
    sResult = {}
    if shopname:
        if bar == '0':  # 用来刷新该店铺同步进程
            log_id = request.GET.get('log_id', '')
            api_url = 'http://47.100.224.71/api/product_progress_bar/'
            api_url += str(log_id) + '/'
            req = urllib2.Request(api_url)
            res_data = urllib2.urlopen(req)
            res = json.loads(res_data.read())
            if res:
                rate = res['rate']
                sResult['resultCode'] = '3'
                sResult['success_percent'] = rate
                if rate == '100%':
                    sResult['messages'] = 'Over'  # 已经刷新完成
        else:
            if shopname != '' and flag != '':
                t_erp_aliexpress_shop_info_objs = t_erp_aliexpress_shop_info.objects.filter(shopName__exact=shopname)
                if t_erp_aliexpress_shop_info_objs.exists():
                    account_name = t_erp_aliexpress_shop_info_objs[0].accountName
                    id = insert_into_action_temp({'shopName': '', 'accountName': account_name, 'action_type': 'synall','action_param': '',
                                                  'action_result': '','action_time': mydatetime.now(),'action_user': request.user.first_name,
                                                  'table_name': 't_erp_aliexpress_online_info','field_name': '','old_value': '','action_id': 0})
                    refresh_online_info_by_ali_api.delay(id)
                    sResult['log_id'] = id
                    sResult['messages'] = u'开始刷新店铺数据'
                    sResult['resultCode'] = '0'
                else:
                    sResult['resultCode'] = '-1'
            else:
                sResult['resultCode'] = '2'
    return JsonResponse(sResult)

# 修改店铺在线商品信息
# request 请求
# 返回sResult刷新进度结果
#edit_product_by_ali_api
def edit_update_by_ali_api_listid(request):
    productid = request.GET.get('productid', '')
    shopname = request.GET.get('shopname', '')

    if request.method == 'POST' and productid != '' and shopname != '':
        t_erp_aliexpress_authorize_info_objs = t_erp_aliexpress_authorize_info.objects.filter(
            user_nick=shopname).values('access_token')
        token_info = ''
        for t_erp_aliexpress_authorize_info_obj in t_erp_aliexpress_authorize_info_objs:
            if t_erp_aliexpress_authorize_info_obj:
                token_info = t_erp_aliexpress_authorize_info_obj['access_token']

# AliExpress店铺在线管理 --同步listID、list上架、list下架
# request 请求
# 返回sResult刷新进度结果
def syndata_by_ali_api(request):
    sResult = {}
    taskid_list=[]
    try:
        productid = 0
        product_id = request.GET.get('product_id', '')
        fe = None
        for flag in ['syn', 'enable', 'disable', 'delete']:
            if request.GET.get(flag):
                fe = flag
                productid = request.GET.get(flag)
                break
        shopname = request.GET.get('shopname', '')
        accountName = request.GET.get('accountName', '')
        if fe == 'delete':
            t_erp_aliexpress_online_info.objects.filter(id=productid).update(product_status_type='Delete')
            t_erp_aliexpress_online_info_delete_obj = t_erp_aliexpress_online_info_delete()
            t_erp_aliexpress_online_info_delete_obj.__dict__ = t_erp_aliexpress_online_info.objects.filter(id=productid)[0].__dict__
            t_erp_aliexpress_online_info_delete_obj.updatetime = None
            t_erp_aliexpress_online_info_delete_obj.updateUser = request.user.first_name
            t_erp_aliexpress_online_info_delete_obj.createUser = request.user.first_name
            t_erp_aliexpress_online_info_delete_obj.createTime = mydatetime.now()
            t_erp_aliexpress_online_info_delete_obj.remark = ''
            t_erp_aliexpress_online_info_delete_obj.save()
            sResult['resultCode'] = '1'
            sResult['messages'] = u'标记删除中...'
        else:
            id = insert_into_action_temp({'shopName': shopname, 'accountName': accountName, 'action_type': fe,'action_param': json.dumps({'product_id': str(product_id)}),
                                                  'action_result': '','action_time': mydatetime.now(),'action_user': request.user.first_name,
                                                  'table_name': 't_erp_aliexpress_online_info','field_name': '','old_value': '','action_id': productid})
            taskid_list.append(id)
            online_status = fe + '_ing'
            if fe == 'syn':
                t_erp_aliexpress_online_info.objects.filter(id=productid).update(is_syn=1)
                syn_products_by_ali_api.delay(id)
                sResult['test'] = id
            else:
                t_erp_aliexpress_online_info.objects.filter(id=productid).update(online_status=online_status)
                if fe == 'enable':
                    enable_products_by_ali_api.delay(id)
                else:
                    disable_products_by_ali_api.delay(id)

            # storeResult = ''
            sResult['resultCode'] = '1'
            sResult['messages'] = u'努力同步中...'
        sResult['taskid'] = taskid_list
    except Exception, e:
        sResult['resultCode'] = -1
        sResult['messages'] = '%s:%s' % (Exception, e)
    return JsonResponse(sResult)

def switch_online_info_json(request, old_online_info):
    params_list = ["product_id","category_id","product_price","subject","detail",
                   "owner_member_id","owner_member_seq","package_width","package_height","package_length",
                   "is_pack_sell","product_status_type","lot_num","group_id","group_ids","product_unit",
                   "promise_template_id","ws_display","ws_valid_num","ws_offline_date","is_image_dynamic",
                   "delivery_time","gross_weight","freight_template_id","package_type","reduce_strategy",
                   "currency_code","add_unit","add_weight",
                   "base_unit","bulk_discount","bulk_order","coupon_end_date","coupon_start_date","keyword",
                   "product_more_keywords1","product_more_keywords2","mobile_detail","sizechart_id","summary"]
    new_online_info = {}
    change_params = {"multimedia":"aeop_a_e_multimedia","product_properties":"aeop_ae_product_propertys",
                    "product_skus":"aeop_ae_product_s_k_us","image_urls":"image_u_r_ls",
                    "data_src":"src","national_quote_configuration":"aeop_national_quote_configuration"}
    for param_each in params_list:
        # messages.error(request, 'param_each: %s' %param_each)
        # messages.error(request, 'param_each_value: %s' % old_online_info[param_each])
        if old_online_info[param_each] and old_online_info[param_each] != 'None'\
                and old_online_info[param_each] != 'False' and old_online_info[param_each] is not None:
            if isinstance(old_online_info[param_each], str) and old_online_info[param_each].strip != '':
                new_online_info[param_each] = old_online_info[param_each]
                if param_each == 'group_ids' or param_each == "mobile_detail":
                    new_online_info[param_each] = json.loads(old_online_info[param_each])
            else:
                new_online_info[param_each] = old_online_info[param_each]
                if param_each == 'group_ids' or param_each == "mobile_detail":
                    new_online_info[param_each] = json.loads(old_online_info[param_each])
    for change_param,change_value in change_params.items():
        # messages.error(request, 'change_param: %s' % change_param)
        if old_online_info[change_param] and old_online_info[change_param] != 'None' and old_online_info[change_param] != 'False' \
                and old_online_info[change_param] is not None and old_online_info[change_param] is not None:
            if change_param == "image_urls" or change_param == "data_src":
                new_online_info[change_value] = old_online_info[change_param]
            else:
                new_online_info[change_value] = json.loads(old_online_info[change_param])
    return new_online_info

def deal_with_sku(request, product_dict, fe):
    try:
        taskid_list = []
        for each_product_id, shopSKUs in product_dict.items():
            t_erp_aliexpress_online_info_obj = t_erp_aliexpress_online_info.objects.filter(id=each_product_id)
            if t_erp_aliexpress_online_info_obj.exists():
                old_online_info_obj = switch_online_info_json(request, t_erp_aliexpress_online_info_obj[0].__dict__)
                new_online_info_obj = copy.deepcopy(old_online_info_obj)
                accountName = new_online_info_obj['owner_member_id']
                sku_info_list = new_online_info_obj['aeop_ae_product_s_k_us'].get('aeop_ae_product_sku', '')
                new_param_info = {'product_id': new_online_info_obj['product_id'], 'sku_stocks': {}}
                ipm_sku_stock = {}
                product_disable = 1 #该商品链接的所有SKU库存都为0的标志位
                product_enable = 1  # 该商品链接的所有SKU库存都不为0的标志位

                for sku_info in sku_info_list:
                    if sku_info:
                        shopsku = sku_info.get('sku_code', '')
                        if shopsku in shopSKUs:
                            if fe == 'disableSKU':
                                sku_info['ipm_sku_stock'] = 0
                                ipm_sku_stock[sku_info['id']] = 0
                            elif fe == 'enableSKU':
                                sku_info['ipm_sku_stock'] = 999
                                ipm_sku_stock[sku_info['id']] = 999
                        if sku_info['ipm_sku_stock'] != 0:
                            product_disable = 0
                        if sku_info['ipm_sku_stock'] == 0:
                            product_enable = 0
                new_param_info['sku_stocks'] = ipm_sku_stock
                if new_online_info_obj['product_status_type'] == 'offline':
                    if fe == 'disableSKU':
                        messages.error(request, u'%s 该商品已下架，请勿重复操作'%(new_online_info_obj['product_id']))
                        continue
                    else:
                        product_enable = 1
                # if new_online_info_obj['product_status_type'] == 'onSelling':
                #     if product_enable == 1:
                #         messages.error(request, u'%s 该商品已上架，请勿重复操作'%(new_online_info_obj['product_id']))
                #         continue
                if product_disable == 1: #该商品链接的所有SKU库存都为0时，下架该商品链接，反之，下架单个SKU
                    fw = fe.replace('SKU', '')
                    id = insert_into_action_temp({'shopName': '', 'accountName': accountName, 'action_type': fw,'action_param': json.dumps({'product_id': str(new_online_info_obj['product_id'])}),
                                                  'action_result': '', 'action_time': mydatetime.now(),'action_user': request.user.first_name,
                                                  'table_name': 't_erp_aliexpress_online_info', 'field_name': '','old_value': '', 'action_id': each_product_id})
                    taskid_list.append(id)
                    online_status = fe + '_ing'
                    t_erp_aliexpress_online_info.objects.filter(id=each_product_id).update(online_status=online_status)
                    disable_products_by_ali_api.delay(id)
                elif product_enable == 1: #该商品链接的所有SKU库存都不为0时，上架该商品链接，反之，上架单个SKU
                    fw = fe.replace('SKU', '')
                    id = insert_into_action_temp({'shopName': '', 'accountName': accountName, 'action_type': fw,'action_param': json.dumps({'product_id': str(new_online_info_obj['product_id'])}),
                                                  'action_result': '', 'action_time': mydatetime.now(),'action_user': request.user.first_name,
                                                  'table_name': 't_erp_aliexpress_online_info', 'field_name': '','old_value': '', 'action_id': each_product_id})
                    taskid_list.append(id)
                    online_status = fe + '_ing'
                    t_erp_aliexpress_online_info.objects.filter(id=each_product_id).update(online_status=online_status)
                    enable_products_by_ali_api.delay(id)
                id = insert_into_action_temp({'shopName': '', 'accountName': accountName, 'action_type': fe,'action_param': json.dumps(new_param_info),
                                              'action_result': '', 'action_time': mydatetime.now(),'action_user': request.user.first_name,
                                              'table_name': 't_erp_aliexpress_online_info', 'field_name': 'product_skus','old_value': '', 'action_id': each_product_id})
                taskid_list.append(id)
                online_status = fe + '_ing'
                t_erp_aliexpress_online_info.objects.filter(id=each_product_id).update(online_status=online_status)
                edit_productSKU_stock_by_ali_api.delay(id)
        return taskid_list
    except Exception, e:
        messages.error(request, u'商品状态修改失败，系统异常')


# AliExpress店铺在线管理 --SKU上架、SKU下架
# request 请求
# 返回sResult刷新进度结果
def syndata_sku_status_by_ali_api(request):
    sResult = {}
    update_datas = request.POST.get('alldata', '')
    update_datas = eval(update_datas)
    product_dict = {}
    try:
        for update_data in update_datas:
            if update_data and '_' in update_data:
                update_data_list = update_data.split('_ywp_')
                t_erp_aliexpress_online_info_obj = t_erp_aliexpress_online_info.objects.filter(id=update_data_list[0])
                if t_erp_aliexpress_online_info_obj.exists():
                    online_status = t_erp_aliexpress_online_info_obj[0].online_status
                    if online_status:
                        operation_type = online_status.split('_')[1]
                        if operation_type == 'ing':
                            messages.error(request, u'%s API调用中，请稍后' % t_erp_aliexpress_online_info_obj[0].product_id)
                            continue
                if product_dict.has_key(update_data_list[0]):
                    product_dict_value = product_dict.get(update_data_list[0])
                    product_dict_value.append(update_data_list[1])
                    product_dict[update_data_list[0]] = product_dict_value
                else:
                    product_dict[update_data_list[0]] = [update_data_list[1],]
            else:
                messages.error(request, u'未选中需要上下架的子商品')
        # messages.error(request, u'product_dict: %s'%product_dict)
        flag = request.GET.get('flag', '')
        # messages.error(request, u'flag: %s' % flag)
        taskid_list=deal_with_sku(request, product_dict, flag)
        sResult['taskid']=taskid_list
        sResult['code'] = 0
        sResult['content'] = u'努力同步中...'

    except Exception, e:
        sResult['code'] = -1
        sResult['messages'] = '%s:%s' % (Exception, e)
    return JsonResponse(sResult)

def get_sku_info_list(sku_info_list):
    py_redis_ali_sku_obj = py_redis_ali_sku()
    infor = []
    shopsku_info_db = {}
    for sku_info in sku_info_list:
        if sku_info:
            shopsku = sku_info.get('sku_code', '')
            shopsku_info_db[shopsku] = {'sku_price': sku_info.get('sku_price', ''), 'id': sku_info.get('id', ''),
                                        'ipm_sku_stock': sku_info.get('ipm_sku_stock', '')}
            eachinfor = {}
            eachinfor['SKU'] = classshopskuobjs.getSKU(shopsku)
            eachinfor['SKUKEY'] = ['NotInStore', 'GoodsStatus', 'Number', 'ReservationNum', 'CanSaleDay']
            eachinfor['ShopSKU'] = shopsku
            eachinfor['ShopSKUKEY'] = ['Quantity', 'Price', 'Shipping', 'Status']
            infor.append(eachinfor)
    # 这里调取redis数据
    sInfors = py_SynRedis_tables_obj.BatchReadRedis(infor)
    num = 0
    all_sku_info = []
    all_shopSKU_list = '['
    all_shopSKU_id_list = '['
    for a, sinfor in enumerate(sInfors):
        shopSKU_info = {}
        try:
            shop_sku = sinfor['ShopSKU'].replace('<', '&lt;').replace('>', '&gt;')
            shopsku_info = py_redis_ali_sku_obj.hgetall_data(shop_sku)
            if len(shopsku_info) == 0:
                shopsku_info = shopsku_info_db[shop_sku]
            sellingPrice = float(shopsku_info['sku_price'])
            calculate_price_obj = calculate_price(str(sinfor['SKU']))
            profitrate_info = calculate_price_obj.calculate_profitRate(sellingPrice, platformCountryCode='ALIEXPRESS-RUS',
                                                                           DestinationCountryCode='US',category='non_ornament')
            profitrate = profitrate_info['profitRate']
        except:
            profitrate = ' '
        num += 1
        inventory = sinfor['SKUKEY'][2]
        if inventory is None or inventory == -1:
            inventory = 0
        else:
            inventory = str(inventory).split('.')[0]
            if inventory == '':
                inventory = '0'
        occupyNum = sinfor['SKUKEY'][3]
        if occupyNum is None or occupyNum == -1:
            occupyNum = 0
        else:
            occupyNum = str(occupyNum).split('.')[0]
            if occupyNum == '':
                occupyNum = '0'

        goodsstatus = sinfor['SKUKEY'][1]
        if sinfor['SKUKEY'][1] == '1':
            goodsstatus = u'正常'
        if sinfor['SKUKEY'][1] == '2':
            goodsstatus = u'售完下架'
        if sinfor['SKUKEY'][1] == '3':
            goodsstatus = u'临时下架'
        if sinfor['SKUKEY'][1] == '4':
            goodsstatus = u'停售'

        sku_status = 'Out of stock'
        if shopsku_info['ipm_sku_stock'] > 0:
            sku_status = 'On Sale'
        shopSKU_info['SKU'] = sinfor['SKU']
        shopSKU_info['CGWRK'] = sinfor['SKUKEY'][0]
        shopSKU_info['goods_status'] = goodsstatus
        shopSKU_info['KC'] = inventory
        shopSKU_info['ZY'] = occupyNum
        shopSKU_info['can_use_num'] = int(inventory) - int(occupyNum)
        shopSKU_info['can_selling_day'] = sinfor['SKUKEY'][-1]
        shopSKU_info['shopSKU'] = sinfor['ShopSKU'].replace('<', '&lt;').replace('>', '&gt;')
        shopSKU_info['sku_stocks'] = shopsku_info['ipm_sku_stock']
        shopSKU_info['sku_price'] = shopsku_info['sku_price']
        shopSKU_info['profitrate'] = profitrate
        shopSKU_info['sku_status'] = sku_status
        shopSKU_info['skuid'] = shopsku_info['id']
        all_sku_info.append(shopSKU_info)
        all_shopSKU_list += '"' + shopSKU_info['shopSKU'] + '",'
        all_shopSKU_id_list += '"' + shopSKU_info['skuid'] + '",'
    all_shopSKU_list = all_shopSKU_list[:-1] + ']'
    all_shopSKU_id_list = all_shopSKU_id_list[:-1] + ']'
    return all_sku_info, all_shopSKU_list, all_shopSKU_id_list

@csrf_exempt
def show_ali_child_sku_info(request):
    '''
    店铺SKU信息展示及信息修改
    :param request:
    :return:
    '''
    product_id = request.GET.get('product_id', '')
    if request.method == 'POST':
        accountName = request.GET.get('accountName', '')
        pid = request.GET.get('id', '')
        #{"QSSHSR2648":"{\"sku_stocks\":\"991\",\"sku_price\":\"3.372\"},\"skuid\":\"<none>\"}"}
        alldata = request.POST.get('alldata','')
        if alldata != '':
            sku_stocks_dict = {'product_id': product_id, 'sku_stocks': {}}
            sku_price_dict = {str(product_id): {}}
            for k,v in eval(alldata).items():
                edit_params = eval(v)
                #修改库存 edit_productSKU_stock_by_ali_api
                if edit_params.has_key('sku_stocks'):
                    skuid = edit_params['skuid']
                    sku_stocks_dict['sku_stocks'][skuid] = edit_params['sku_stocks']
                # 修改价格 edit_productSKU_price_by_ali_api
                if edit_params.has_key('sku_price'):
                    skuid = edit_params['skuid']
                    sku_price_dict[str(product_id)][str(skuid)] = str(edit_params['sku_price'])
            if sku_stocks_dict['sku_stocks']:
                id = insert_into_action_temp({'shopName': '', 'accountName': accountName, 'action_type': 'editStock',
                                              'action_param': json.dumps(sku_stocks_dict),
                                              'action_result': '', 'action_time': mydatetime.now(),
                                              'action_user': request.user.first_name,
                                              'table_name': 't_erp_aliexpress_online_info', 'field_name': '',
                                              'old_value': '', 'action_id': pid})
                online_status = 'editStock_ing'
                t_erp_aliexpress_online_info.objects.filter(id=pid).update(online_status=online_status)
                edit_productSKU_stock_by_ali_api.delay(id)
            if sku_stocks_dict['sku_stocks'] and sku_price_dict[str(product_id)]:
                time.sleep(2)
            if sku_price_dict[str(product_id)]:
                id = insert_into_action_temp({'shopName': '', 'accountName': accountName, 'action_type': 'editPrice',
                                              'action_param': json.dumps(sku_price_dict),
                                              'action_result': '', 'action_time': mydatetime.now(),
                                              'action_user': request.user.first_name,
                                              'table_name': 't_erp_aliexpress_online_info', 'field_name': '',
                                              'old_value': '', 'action_id': pid})
                online_status = 'editPrice_ing'
                t_erp_aliexpress_online_info.objects.filter(id=pid).update(online_status=online_status)
                edit_productSKU_price_by_ali_api.delay(id)
            result = {'resultCode': 1, 'info': u'正在修改中'}
        else:
            result = {'resultCode': -1, 'errorinfo': u'未选中需要修改的数据'}
        return HttpResponse(json.dumps(result))
    else:
        t_erp_aliexpress_online_info_obj = t_erp_aliexpress_online_info.objects.filter(product_id=product_id)
        if t_erp_aliexpress_online_info_obj.exists():
            sku_infos = json.loads(t_erp_aliexpress_online_info_obj[0].product_skus)
            accountName = t_erp_aliexpress_online_info_obj[0].owner_member_id
            id = t_erp_aliexpress_online_info_obj[0].id
            sku_info_list = sku_infos.get('aeop_ae_product_sku', '')
            all_sku_info, all_shopSKU_list, all_shopSKU_id_list = get_sku_info_list(sku_info_list)

        return render(request, 'ali_sku_info_edit.html',
                      {'all_sku_info': all_sku_info,'ProductID':product_id, 'all_shopSKU_id_list': all_shopSKU_id_list, 'id': id,
                       'sku_size': len(all_sku_info), 'all_shopSKU_list': all_shopSKU_list, 'accountName': accountName})
import requests
@csrf_exempt
def aliexpress_online_sku_off(request):
    event=t_erp_aliexpress_action_temp.objects.filter(action_type='disable_all_stopsales_SKU')
    if request.user.first_name not in ('段小迪','李嫦','刘翠仙'):
        return JsonResponse({'msg': '执行该功能请联系 段小迪,李嫦,刘翠仙'})
    if event.exists():
       return JsonResponse({'msg':'任务正在进行，请勿重复提交'})
    event_id=insert_into_action_temp(
        {'action_type': 'disable_all_stopsales_SKU',
         'action_result': '', 'action_time': mydatetime.now(), 'action_user': request.user.first_name,
         'table_name': 't_erp_aliexpress_online_info', 'field_name': 'product_skus', 'old_value': '',
         'action_id': 0})
    product_ids=t_erp_aliexpress_online_info.objects.filter(StopSalesFlag__range=[1,99],skustock_isempty=0).values('product_id','owner_member_id')
    for p in product_ids:
        product_id=p.get('product_id')
        accountName=p.get('owner_member_id')
        skuinfo=t_erp_aliexpress_product_sku.objects.filter(product_id=product_id,GoodsStatus=4).values('shopsku_id')
        sku_stocks={}
        for shopsku_id in skuinfo:
            sku_stocks[shopsku_id.get('shopsku_id')]=0
        id = insert_into_action_temp(
            {'shopName': '', 'accountName': accountName, 'action_type': 'disableSKU', 'action_param': json.dumps({'product_id': product_id, 'sku_stocks': sku_stocks}),
             'action_result': '', 'action_time': mydatetime.now(), 'action_user': request.user.first_name,
             'table_name': 't_erp_aliexpress_online_info', 'field_name': 'product_skus', 'old_value': '','remark':'disableSKU',
             'action_id': 0})
        online_status = 'disableSKU' + '_ing'
        t_erp_aliexpress_online_info.objects.filter(id=product_id).update(online_status=online_status)
        #edit_productSKU_stock_by_ali_api.delay(id)
    try:
        requests.get('http://106.14.157.218/api/disable_all_stopssales_sku/{}/'.format(event_id))
    except Exception:
        pass
    # event_obj=t_erp_aliexpress_action_temp.objects.filter(id=event_id).first()
    # t_erp_aliexpress_action_log(action_type=event_obj.action_type,action_time=event_obj.action_time,action_user=event_obj.action_user).save()
    # event_obj.delete()
