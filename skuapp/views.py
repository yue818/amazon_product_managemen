# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.shortcuts import render,render_to_response
from pyapp.models import b_goods as py_b_goods
from pyapp.models import B_Supplier as sku_b_supplier
# Create your views here.
#导入模块
from django.db.models import F
import logging
import django.utils.log
import logging.handlers
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
import random
from brick.function.StockData import StockData
from brick.function.upload_kc_to_oss import upload_kc_to_oss
from Project.settings import *
from django.contrib import messages

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import time
from django.contrib.auth.models import *
from skuapp.table import *
from skuapp.table.t_config_mstsc_log import t_config_mstsc_log 
import re
import oss2
from django.views.decorators.csrf import requires_csrf_token  ,csrf_exempt
from datetime import datetime
from django.db import transaction,connection
from skuapp.table.t_report_orders1days import t_report_orders1days
from skuapp.table.t_store_marketplan_execution import t_store_marketplan_execution 
from skuapp.table.t_online_info import *
from skuapp.table.t_product_price_check import *
from skuapp.table.t_report_ebay_orders1days import t_report_ebay_orders1days
from skuapp.table.t_online_info_ebay import t_online_info_ebay
from skuapp.table.t_online_info_ebay_subsku import t_online_info_ebay_subsku
from skuapp.table.t_config_paypal_account import *
from skuapp.table.t_shop_amazon_india import *
from skuapp.table.t_product_up_down import *
from skuapp.table.t_order_item_amazon_india import *
from skuapp.table.t_online_info_wish import *
from skuapp.table.t_online_info_publish_joom import *
from skuapp.table.t_api_schedule_ing import *
from skuapp.table.t_amazon_schedule_ing import *
from skuapp.table.t_order_track_info_amazon_india import *
#from skuapp.table.t_online_info_wait_publish import *
from skuapp.table.t_distribution_product_to_store_temp import t_distribution_product_to_store_temp as store_temp
from skuapp.table.t_distribution_product_to_store import t_distribution_product_to_store
from skuapp.table.t_config_user_buyer import *
from pyapp.models import b_goods
from django.shortcuts import render
import math
from skuapp.table.t_templet_wish_collection_box import *
from skuapp.table.t_templet_amazon_wait_published import *
from skuapp.table.t_templet_public_wish import *
from skuapp.table.t_templet_wish_wait_upload import *
from skuapp.table.t_upload_shopname import *
from skuapp.table.t_templet_wish_upload_result import *
from skuapp.table.t_templet_amazon_collection_box import *
from skuapp.table.t_templet_amazon_published_variation import *
from skuapp.table.t_templet_amazon_wait_upload import *
from skuapp.table.t_config_shop_alias import *
import urllib2
from skuapp.table.t_templet_aliexpress_collection_box import *
import httplib
from skuapp.public.url_Stitching import *

from skuapp.table.t_templet_ebay_collection_box import *
from skuapp.table.t_templet_ebay_pic_set import *
from skuapp.table.t_templet_ebay_wait_upload import *
from skuapp.table.t_templet_public_ebay import *
from skuapp.table.t_config_apiurl_amazon import *
from skuapp.table.t_templet_config_amazon_published import *
from skuapp.table.t_template_product_config_amazon import *
from skuapp.table.t_supply_chain_production_basic import t_supply_chain_production_basic

from skuapp.table.t_templet_joom_collection_box import *
from skuapp.table.t_templet_public_joom import *
from skuapp.table.t_templet_joom_wait_upload import *
from django.db.models import Q
from skuapp.table.t_aliexpress_compare_price import t_aliexpress_compare_price
from skuapp.table.t_tort_info import *
from skuapp.table.t_wish_pb_campaignproductstats import t_wish_pb_campaignproductstats as t_wish_pb
from brick.function.encryption import encrypt_password
from brick.aliexpress.get_info_from_url import *
from brick.aliexpress.get_info_from_puyuan import *
from brick.wish.WishPbAPI import getKeyWords, StopCampaign, CancelCampaign
from brick.classredis.classmainsku import classmainsku
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import os
import uuid
import json
import datetime as dt

@csrf_exempt
def upload_image(request, dir_name):
    ##################
    #  kindeditor图片上传返回数据格式说明：
    # {"error": 1, "message": "出错信息"}
    # {"error": 0, "url": "图片地址"}
    ##################
    result = {"error": 1, "message": "上传出错"}
    files = request.FILES.get("imgFile", None)
    if files:
        result = image_upload(files, dir_name)
    return HttpResponse(json.dumps(result), content_type="application/json")
@csrf_exempt
def prompt_develop(request):
    from skuapp.table.t_product_survey_history import *
    supplierURL_objs = t_product_survey_history.objects.values_list('SupplierPUrl1',flat=True)
    
    message=1
    if request.is_ajax() and request.method=="GET":       
        SupplierPUrl=request.GET.get('a')
        if SupplierPUrl in supplierURL_objs:
            if len(SupplierPUrl) != 0:                  
                message=0

    #messages.error(request,"--------%s"%message)
    return HttpResponse(message)
    
@csrf_exempt
def aliexpress_refund_info(request):
    import pyodbc, MySQLdb,pymssql
    ShopOrderNumber=request.POST.get('ShopOrderNumber')
    conn = pymssql.connect(host='122.226.216.10', user='fancyqube', password='K120Esc1',
                                             database='ShopElf',
                                             port='18793')
    cursor = conn.cursor()
    sql = '''SELECT
    ptd.sku,
    ptd.[L_AMT],
    c.countryznname,
    m.CLOSINGDATE,
    m.SUFFIX
FROM
    P_Trade (nolock) m
LEFT JOIN B_Country (nolock) c ON c.CountryCode = m.SHIPTOCOUNTRYCODE
LEFT JOIN P_TradeDt (nolock) ptd ON m.nid = ptd.tradenid

WHERE
    ordertime >= '2017-03-08 16:00:00'
AND ordertime <= GETDATE()
AND m.ACK ='%s'
UNION
    SELECT
        ptd.sku,
        ptd.[L_AMT],
        c.countryznname,
        m.CLOSINGDATE,
        m.SUFFIX
    FROM
        P_Trade (nolock) m
    INNER JOIN S_UserSuffix (nolock) Us ON us.suffix = m.suffix
    AND us.userid = 58
    LEFT JOIN B_Country (nolock) c ON c.CountryCode = m.SHIPTOCOUNTRYCODE
    LEFT JOIN P_TradeDt (nolock) ptd ON m.nid = ptd.tradenid
    WHERE
        ordertime >= '2017-03-08 16:00:00'
    AND ordertime <= GETDATE()
    AND EXISTS (
        SELECT
            TOP 1 Z.MergeBillID
        FROM
            P_trade_b (nolock) Z
        WHERE
            m.NID = MergeBillID
        AND z.ACK ='%s')
UNION
    SELECT
        ptd.sku,
        ptd.[L_AMT],
        c.countryznname,
        m.CLOSINGDATE,
        m.SUFFIX
    FROM
        P_Trade_His (nolock) m
    INNER JOIN S_UserSuffix (nolock) Us ON us.suffix = m.suffix
    AND us.userid = 58
    LEFT JOIN B_Country (nolock) c ON c.CountryCode = m.SHIPTOCOUNTRYCODE
    LEFT JOIN P_TradeDt_His (nolock) ptd ON m.nid = ptd.tradenid
    WHERE
        ordertime >= '2017-03-08 16:00:00'
    AND ordertime <= GETDATE()
    AND m.ACK ='%s'
UNION
    SELECT
        ptd.sku,
        ptd.[L_AMT],
        c.countryznname,
        m.CLOSINGDATE,
        m.SUFFIX
    FROM
        P_Trade_His (nolock) m
    INNER JOIN S_UserSuffix (nolock) Us ON us.suffix = m.suffix
    AND us.userid = 58
    LEFT JOIN B_Country (nolock) c ON c.CountryCode = m.SHIPTOCOUNTRYCODE
    LEFT JOIN P_TradeDt_His (nolock) ptd ON m.nid = ptd.tradenid
    WHERE
        ordertime >= '2017-03-08 16:00:00'
    AND ordertime <= GETDATE()
    AND EXISTS (
        SELECT
            TOP 1 Z.MergeBillID
        FROM
            P_trade_b (nolock) Z
        WHERE
            m.NID = MergeBillID
        AND z.ACK ='%s')
UNION
    SELECT
        ptd.sku,
        ptd.[L_AMT],
        c.countryznname,
        m.CLOSINGDATE,
        m.SUFFIX
    FROM
        P_TradeUn_His (nolock) m
    INNER JOIN S_UserSuffix (nolock) Us ON us.suffix = m.suffix
    AND us.userid = 58
    LEFT JOIN B_Country (nolock) c ON c.CountryCode = m.SHIPTOCOUNTRYCODE
    LEFT JOIN P_TradeDtUn_His (nolock) ptd ON m.nid = ptd.tradenid
    WHERE
        ordertime >= '2017-03-08 16:00:00'
    AND ordertime <= GETDATE()
    AND m.ACK ='%s'
UNION
    SELECT
        ptd.sku,
        ptd.[L_AMT],
        c.countryznname,
        m.CLOSINGDATE,
        m.SUFFIX
    FROM
        P_TradeUn_His (nolock) m
    INNER JOIN S_UserSuffix (nolock) Us ON us.suffix = m.suffix
    AND us.userid = 58
    LEFT JOIN B_Country (nolock) c ON c.CountryCode = m.SHIPTOCOUNTRYCODE
    LEFT JOIN P_TradeDtUn_His (nolock) ptd ON m.nid = ptd.tradenid
    WHERE
        ordertime >= '2017-03-08 16:00:00'
    AND ordertime <= GETDATE()
    AND EXISTS (
        SELECT
            TOP 1 Z.MergeBillID
        FROM
            P_trade_b (nolock) Z
        WHERE
            m.NID = MergeBillID
        AND z.ACK ='%s')
UNION
    SELECT
        ptd.sku,
        ptd.[L_AMT],
        c.countryznname,
        m.CLOSINGDATE,
        m.SUFFIX
    FROM
        P_TradeUn (nolock) m
    INNER JOIN S_UserSuffix (nolock) Us ON us.suffix = m.suffix
    AND us.userid = 58
    LEFT JOIN B_Country (nolock) c ON c.CountryCode = m.SHIPTOCOUNTRYCODE
    LEFT JOIN P_TradeDtUn (nolock) ptd ON m.nid = ptd.tradenid
    WHERE
        ordertime >= '2017-03-08 16:00:00'
    AND ordertime <= GETDATE()
    AND m.ACK ='%s'
UNION
    SELECT
        ptd.sku,
        ptd.[L_AMT],
        c.countryznname,
        m.CLOSINGDATE,
        m.SUFFIX
    FROM
        P_TradeUn (nolock) m
    INNER JOIN S_UserSuffix (nolock) Us ON us.suffix = m.suffix
    AND us.userid = 58
    LEFT JOIN B_Country (nolock) c ON c.CountryCode = m.SHIPTOCOUNTRYCODE
    LEFT JOIN P_TradeDtUn (nolock) ptd ON m.nid = ptd.tradenid
    WHERE
        ordertime >= '2017-03-08 16:00:00'
    AND ordertime <= GETDATE()
    AND EXISTS (
        SELECT
            TOP 1 Z.MergeBillID
        FROM
            P_trade_b (nolock) Z
        WHERE
            m.NID = MergeBillID
        AND z.ACK ='%s');

 '''%(ShopOrderNumber,ShopOrderNumber,ShopOrderNumber,ShopOrderNumber,ShopOrderNumber,ShopOrderNumber,ShopOrderNumber,ShopOrderNumber)
    print sql
    #param = (ShopOrderNumber,ShopOrderNumber,ShopOrderNumber,ShopOrderNumber,ShopOrderNumber,ShopOrderNumber,ShopOrderNumber,ShopOrderNumber)
    cursor.execute(sql)
    objs = cursor.fetchall()
    return_value = {}
    list1 = []
    list2 = []
    #list3 = []
    list4 = []
    list5 = []                                                                                                                                                                                                                                                              
    if request.is_ajax() and request.method=="POST": 
        for obj in objs:
            list1.append(str(obj[0]))
            list2.append(str(obj[1]))
            #list3.append(obj[2])
            list4.append(str(obj[3]))
            list5.append(str(obj[4]))
            return_value['Country'] = obj[2]
        return_value['ProductSKU']  = str(list1).replace('[','').replace(']','').replace("'","")
        return_value['Sale_price']  = str(list2).replace('[','').replace(']','').replace("'","")
        #return_value['Country']     = str(list3).replace('[','').replace(']','').replace("'","")
        return_value['ClosingDate'] = str(list4).replace('[','').replace(']','').replace("'","")
        return_value['ShopName']    = str(list5).replace('[','').replace(']','').replace("'","")
    cursor.close()
    conn.close()
    return HttpResponse(json.dumps(return_value), content_type="application/json")
    #return HttpResponseRedirect('/Project/admin/skuapp/t_aliexpress_refund_info')  

# 目录创建
def upload_generation_dir(dir_name):
    today = dt.datetime.today()
    url_part = dir_name + '/%d/%d/' % (today.year, today.month)
    dir_name = os.path.join(dir_name, str(today.year), str(today.month))
    print("*********", os.path.join(settings.MEDIA_ROOT, dir_name))
    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, dir_name)):
        os.makedirs(os.path.join(settings.MEDIA_ROOT, dir_name))
    return dir_name,url_part


# 图片上传
def image_upload(files, dir_name):
    # 允许上传文件类型
    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_TORT)
    allow_suffix = ['jpg', 'png', 'jpeg', 'gif', 'bmp', 'xls', 'xlsx']
    file_suffix = files.name.split(".")[-1]
    if file_suffix not in allow_suffix:
        return {"error": 1, "message": "格式不正确"}
    relative_path_file, url_part = upload_generation_dir(dir_name)
    path = os.path.join(settings.MEDIA_ROOT, relative_path_file)
    print("&&&&path", path)
    if not os.path.exists(path):  # 如果目录不存在创建目录
        os.makedirs(path)
    file_name = str(uuid.uuid1()) + "." + file_suffix
    path_file = os.path.join(path, file_name)
    file_url =settings.MEDIA_URL + url_part +file_name
    open(path_file, 'wb').write(files.file.read())
    return {"error": 0, "url": file_url}

def show_tree(request):
    return render(request, 't_product_up_downPlugin.html')
#basepath=os.getcwd()+'\\dockerApp\\app\\templates\\';
def homepage(request):
    #response=render_to_response(basepath+"index.html");
    return HttpResponseRedirect("/Project/admin/skuapp/t_task_trunk?status=mytask&Flow_Status=TC,SH,CL,NYZ,YZ")

def page_not_found(request):
    return render(request, '404.html')
def page_error1(request):
    return render(request, '500.htm')
def page_error2(request):
    return render(request, '502.htm')
def page_error3(request):
    return render(request, '504.htm')
    
def begin_oplog(request,obj,objAdmin):
    t_product_oplog_objs = t_product_oplog.objects.filter(StepID=objAdmin.StepID,pid=obj.id)
    if t_product_oplog_objs is  None or t_product_oplog_objs.count() ==0:
        t_product_oplog_obj = t_product_oplog(MainSKU= obj.MainSKU,Name2=obj.Name2,OpID=request.user.username,OpName=request.user.first_name,StepID=objAdmin.StepID,StepName=objAdmin.StepName,BeginTime=datetime.now(),pid=obj.id)
        t_product_oplog_obj.save()
def end_oplog(request,obj,objAdmin):
    t_product_oplog_objs = t_product_oplog.objects.filter(StepID=objAdmin.StepID,pid = obj.id)
    if t_product_oplog_objs is  None or t_product_oplog_objs.count() ==0:
        t_product_oplog_obj = t_product_oplog(MainSKU= obj.MainSKU,Name2=obj.Name2,OpID=request.user.username,OpName=request.user.first_name,StepID=objAdmin.StepID,StepName=objAdmin.StepName,BeginTime=datetime.now(),EndTime=datetime.now(), pid=obj.id)
        t_product_oplog_obj.save()
    else:
        for t_product_oplog_obj in t_product_oplog_objs :
            t_product_oplog_obj.MainSKU = obj.MainSKU
            t_product_oplog_obj.Name2 = obj.Name2
            t_product_oplog_obj.OpID=request.user.username
            t_product_oplog_obj.OpName=request.user.first_name
            t_product_oplog_obj.StepName =objAdmin.StepName
            t_product_oplog_obj.EndTime=datetime.now()
            t_product_oplog_obj.save()
#记录操作历史
def begin_t_product_oplog(request,mainsku,tempstepid,tempname ,temppid):
    from datetime import datetime
    t_product_oplog_objs = t_product_oplog.objects.filter(StepID=tempstepid,pid=temppid,MainSKU=mainsku)
    if t_product_oplog_objs is  None or t_product_oplog_objs.count() ==0:
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
        if tempstepid == 'PZ' :
            tempstepname = u'拍照'
        if tempstepid == 'MG' :
            tempstepname = u'美工'
        if tempstepid == 'LR' :
            tempstepname = u'录入'
        if tempstepid == 'SH' :
            tempstepname = u'审核'
        if tempstepid == 'BMLY' :
            tempstepname = u'部门领用'
        if tempstepid == 'DEL' :
            tempstepname = u'删除'
        t_product_oplog_obj = t_product_oplog(MainSKU= mainsku,Name2=tempname,OpID=request.user.username,OpName=request.user.first_name,StepID=tempstepid,StepName=tempstepname,BeginTime=datetime.now(),pid=temppid)
        t_product_oplog_obj.save()


def end_t_product_oplog(request,mainsku,tempstepid,tempname,temppid):
    from datetime import datetime
    tempstepname = u'其他'
    if tempstepid == 'DY' :
        tempstepname = u'调研'
    if tempstepid == 'DYSH' :
        tempstepname = u'调研审核'
    if tempstepid == 'PC' :
        tempstepname = u'排重'
    if tempstepid == 'KF' :
        tempstepname = u'开发'
    if tempstepid == 'PASS' :
        tempstepname = u'审核'
    if tempstepid == 'BACK' :
        tempstepname = u'驳回'
    if tempstepid == 'NOKF' :
        tempstepname = u'不开发'
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
    if tempstepid == 'SH' :
            tempstepname = u'审核'

    t_product_oplog_objs = t_product_oplog.objects.filter(StepID=tempstepid,pid = temppid ,MainSKU=mainsku)
    if t_product_oplog_objs is  None or t_product_oplog_objs.count() ==0:
        t_product_oplog_obj = t_product_oplog(MainSKU= mainsku,Name2=tempname,OpID=request.user.username,OpName=request.user.first_name,StepID=tempstepid,StepName=tempstepname,BeginTime=datetime.now(),EndTime=datetime.now(), pid=temppid)
        t_product_oplog_obj.save()
    else:
        for t_product_oplog_obj in t_product_oplog_objs :
            t_product_oplog_obj.MainSKU = mainsku
            t_product_oplog_obj.Name2 = tempname 
            t_product_oplog_obj.OpID=request.user.username
            t_product_oplog_obj.OpName=request.user.first_name
            t_product_oplog_obj.StepName =tempstepname
            t_product_oplog_obj.EndTime=datetime.now()
            t_product_oplog_obj.save()

@receiver(post_save, sender=t_product_survey_ing)
def save_t_product_survey_ing_callback(sender,created, instance, **kwargs):
    logger = logging.getLogger('sourceDns.webdns.views')    #刚才在setting.py中配置的logger
    logger.error("cccccczzzzzzzzzzzzzzzzcccccccccccccccccc111111")
    logger.error(sender)
    logger.error("1")
    logger.error(created)
    logger.error("2")
    logger.error(instance)
    logger.error("3")
    logger.error(kwargs)
    logger.error("cccccczzzzzzzzzzzzzzzzcccccccccccccccccc222222")

#post_save.connect(save_t_product_survey_ing_callback,dispatch_uid="my_unique_identifier")
# xxoo指上述导入的内容


def contact(request):
    logger = logging.getLogger('sourceDns.webdns.views')    #刚才在setting.py中配置的logger
    logger.error("zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz")
    errors = []
    errors.append('Enter11begin.')

    logger.error(request.FILES)
    if request.method == 'POST':
        files = request.FILES.getlist('myfiles')
        for f in files :
            logger.error(f.name)
            destination = open(MEDIA_ROOT + 'upload_imgs/' +  f.name,'wb+')
            for chunk in f.chunks():
              destination.write(chunk)
            destination.close()





    messages.warning(request, 'FBI ssssssssssssssssss.')
    messages.error(request, 'You shall not sssssssssssssssssss!')

    #return HttpResponseRedirect('/contact/thanks/')
    #return render_to_response('change_form.html', {'errors': errors,},context_instance=RequestContext(request))
    #return render_to_response('change_form.html', {'errors': errors,},)
    #return HttpResponseRedirect("/admin/")
    t_product_survey_ing.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    returnHttpResponsessssss("upload over!")

def showpic(request):
    import datetime
    now = datetime.datetime.now()
    #return render_to_response('/admin/skuapp/t_product_survey_ing/change_form.html', {'current_date': now})
    return render_to_response('admin/skuapp/t_product_survey_ing/showpic.html', {'current_date': now,},)
    #return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def addsurvey(request):
        t_product_survey_ing_obj= t_product_survey_ing(StaffID=request.user.username)
        t_product_survey_ing_obj.save()
        begin_t_product_oplog(request,t_product_survey_ing_obj.MainSKU,'DY',t_product_survey_ing_obj.Name2,t_product_survey_ing_obj.id)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def adddeveloping(request):
        t_product_develop_ing_obj= t_product_develop_ing(StaffID=request.user.username)
        t_product_develop_ing_obj.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def addmainsku_sku(request):
    #messages.error(request,u'ERROR:请先填写正确的MainSKU,并保存!!!')
    #logger = logging.getLogger('sourceDns.webdns.views')
    #logger.error("request====%s"%(request))
    object_id = ''
    mainsku_sku_num = 0
    if request.method == 'POST':
        object_id = request.POST.get('object_id','')
        if object_id is None or object_id.strip()=='':
            pass
            #return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        mainsku_sku_num = request.POST.get('mainsku_sku_num',0)
        if mainsku_sku_num is None or mainsku_sku_num <=0 or mainsku_sku_num =='0':
            pass

    obj = t_product_build_ing.objects.get(id__exact=object_id)
    if obj.MainSKU is None:
        messages.error(request,u'ERROR:请先填写正确的MainSKU,并保存!!!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    for index in range(0, int(mainsku_sku_num)):
        if obj.SupplierPColor is None or obj.SupplierPColor == 'None'  or obj.SupplierPColor == '':
            obj.SupplierPColor = ''
        if obj.UnitPrice is None or obj.UnitPrice == 'None'  or obj.UnitPrice == '':
            obj.UnitPrice = 0
        if obj.Weight is None or obj.Weight == 'None'  or obj.Weight == '':
            obj.Weight = 0

        t_product_mainsku_sku_obj = t_product_mainsku_sku(
            MainSKU='',SKU='',SKUATTRS= obj.SupplierPColor,UnitPrice=obj.UnitPrice,Weight= obj.Weight,
            PackNID=obj.PackNID,MinPackNum=obj.MinPackNum,pid = obj.id,DressInfo='',SupplierLink=obj.SupplierPUrl1
        )
        t_product_mainsku_sku_obj.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
def addlog(request):
    import datetime
    if request.method == 'POST':
        BA = request.POST.get('name_BuyerAccount','')
        procount = request.POST.get('procount',)
        if procount is None or procount == '':
            procount = 3
        else:
            procount = procount
        procount = int(procount)
        #Price_1 = request.POST.get('Price_1','')
    #messages.error(request,'BABABA=====%s'%BA)
    #Price_1 = '123123'
    #t_store_marketplan_execution_objs = t_store_marketplan_execution_log
    
    num = 0
    for index in range(0, 100):
        t_store_marketplan_execution_log_objs = t_store_marketplan_execution_log.objects.filter(Status='EXEING',StaffId=request.user.username).values_list("ShopName")
        #t_store_marketplan_execution_log_pros = t_store_marketplan_execution_log.objects.filter(Exetime__gte=(datetime.datetime.now()+(datetime.timedelta(days=-1))).strftime('%Y-%m-%d %H:%M:%S'),Result != '成功').values_list("ProductID")
        
        t_store_marketplan_execution_objs = t_store_marketplan_execution.objects.exclude(ShopName__in = t_store_marketplan_execution_log_objs).filter(Demand__gt=F('Quantity'),CreateTime__lte=(datetime.datetime.now()+(datetime.timedelta(days=-1))).strftime('%Y-%m-%d %H:%M:%S'))
        if t_store_marketplan_execution_objs.exists():
            t_store_marketplan_execution_objs_l = random.sample(list(t_store_marketplan_execution_objs),1)
            
        
            for t_store_marketplan_execution_obj in t_store_marketplan_execution_objs_l:
                try: 
                    pic = t_online_info.objects.filter(ProductID=t_store_marketplan_execution_obj.ProductID).values_list("Image")[0][0]
                except:
                    pic=''
                    
                if t_store_marketplan_execution_obj.Demand <=5:
                    bb = math.ceil(t_store_marketplan_execution_obj.Demand/2)    
                    t_store_marketplan_execution_log_objs_count = t_store_marketplan_execution_log.objects.filter(Exetime__gte=(datetime.datetime.now()+(datetime.timedelta(days=-1))).strftime('%Y-%m-%d %H:%M:%S'),Pid=t_store_marketplan_execution_obj.id).count()
                    if t_store_marketplan_execution_log_objs_count>bb:
                        continue
                    else:
                        t_store_marketplan_execution_log_obj = t_store_marketplan_execution_log(PicURL=pic,Pid=t_store_marketplan_execution_obj.id,ShopName=t_store_marketplan_execution_obj.ShopName,ShopSKU=t_store_marketplan_execution_obj.ParentSKU,BuyerAccount=BA,ProductID=t_store_marketplan_execution_obj.ProductID,Status='EXEING',StaffId=request.user.username,Price=t_store_marketplan_execution_obj.Price)
                    
                        #t_store_marketplan_execution_log_objs = t_store_marketplan_execution_log.objects.all()
                        countall = t_store_marketplan_execution_obj.Demand
                        count1 = t_store_marketplan_execution_log_objs.filter(Pid=t_store_marketplan_execution_obj.id).count()
                        #messages.error(request,'Demand=====%s'%countall)
                        #messages.error(request,'count1=====%s'%count1)
                        if count1 < countall:
                            num = num+1
                            if num >procount:
                                break
                            t_store_marketplan_execution_log_obj.save()
                            
                            
                elif t_store_marketplan_execution_obj.Demand >5 and t_store_marketplan_execution_obj.Demand <10:
                    aa = math.ceil(t_store_marketplan_execution_obj.Demand/3)
                    t_store_marketplan_execution_log_objs_count = t_store_marketplan_execution_log.objects.filter(Exetime__gte=(datetime.datetime.now()+(datetime.timedelta(days=-1))).strftime('%Y-%m-%d %H:%M:%S'),Pid=t_store_marketplan_execution_obj.id).count()
                    if t_store_marketplan_execution_log_objs_count>aa:
                        continue
                    else:
                        t_store_marketplan_execution_log_obj = t_store_marketplan_execution_log(PicURL=pic,Pid=t_store_marketplan_execution_obj.id,ShopName=t_store_marketplan_execution_obj.ShopName,ShopSKU=t_store_marketplan_execution_obj.ParentSKU,BuyerAccount=BA,ProductID=t_store_marketplan_execution_obj.ProductID,Status='EXEING',StaffId=request.user.username,Price=t_store_marketplan_execution_obj.Price)
                    
                        #t_store_marketplan_execution_log_objs = t_store_marketplan_execution_log.objects.all()
                        countall = t_store_marketplan_execution_obj.Demand
                        count1 = t_store_marketplan_execution_log_objs.filter(Pid=t_store_marketplan_execution_obj.id).count()
                        #messages.error(request,'Demand=====%s'%countall)
                        #messages.error(request,'count1=====%s'%count1)
                        if count1 < countall:
                            num = num+1
                            if num >procount:
                                break
                            t_store_marketplan_execution_log_obj.save()
                            
                else:
                    cc = math.ceil(t_store_marketplan_execution_obj.Demand/5)
                    t_store_marketplan_execution_log_objs_count = t_store_marketplan_execution_log.objects.filter(Exetime__gte=(datetime.datetime.now()+(datetime.timedelta(days=-1))).strftime('%Y-%m-%d %H:%M:%S'),Pid=t_store_marketplan_execution_obj.id).count()
                    if t_store_marketplan_execution_log_objs_count>cc:
                        continue
                    else:
                        t_store_marketplan_execution_log_obj = t_store_marketplan_execution_log(PicURL=pic,Pid=t_store_marketplan_execution_obj.id,ShopName=t_store_marketplan_execution_obj.ShopName,ShopSKU=t_store_marketplan_execution_obj.ParentSKU,BuyerAccount=BA,ProductID=t_store_marketplan_execution_obj.ProductID,Status='EXEING',StaffId=request.user.username,Price=t_store_marketplan_execution_obj.Price)
                    
                        #t_store_marketplan_execution_log_objs = t_store_marketplan_execution_log.objects.all()
                        countall = t_store_marketplan_execution_obj.Demand
                        count1 = t_store_marketplan_execution_log_objs.filter(Pid=t_store_marketplan_execution_obj.id).count()
                        #messages.error(request,'Demand=====%s'%countall)
                        #messages.error(request,'count1=====%s'%count1)
                        if count1 < countall:
                            num = num+1
                            if num >procount:
                                break
                            t_store_marketplan_execution_log_obj.save()
                            
                
            
        else:
            pass
   
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
#@csrf_exempt

def saveform(request):
    import time,datetime     
    #messages.error(request,'username===%s'%(request.user.username))
        
    t_store_marketplan_execution_log_objs = t_store_marketplan_execution_log.objects.filter(Status='EXEING',StaffId = request.user.username )
    #messages.error(request,'t_store_marketplan_execution_log_objs===%s'%t_store_marketplan_execution_log_objs)
    count = t_store_marketplan_execution_log_objs.count()
    #messages.error(request,'count===%s'%count)
    for i in range(0,count) : #for t_store_marketplan_execution_log_obj in t_store_marketplan_execution_log_objs:
        Remark = request.POST.get('Remark_%d'%i,'')
            
        if Remark is None or Remark =='' or Remark=='None' or Remark ==0 or Remark.strip() =='':
            pass
                
        xid = request.POST.get('id_%d'%i,''  )
            
        Remark = request.POST.get('Remark_%d'%i,'')
            
        Price = request.POST.get('Price_%d'%i,'')
            
        if Price is None or Price =='' or Price=='None' or Price ==0 or Price.strip() =='':
            pass
            
        Price2 = request.POST.get('Price2_%d'%i,'')
            

                
        xid = request.POST.get('id_%d'%i,''  )
            
        Price = request.POST.get('Price_%d'%i,'')
            
        Result = request.POST.get('Result_%d'%i,'')
        
            
        if Result is None or Result =='' or Result=='None' or Result ==0 or Result.strip() =='':
            pass
                
        xid = request.POST.get('id_%d'%i,''  )
            
        Result = request.POST.get('Result_%d'%i,'')   
        
        if Result == '成功':
            if Price2 is None or Price2 =='' or Price2=='None' or Price2 ==0 or Price2.strip() =='':
                messages.error(request,u'刷单金额不能为空！！！')
                continue
        else:
            Price2 = 0            
        #Status = request.POST.get('Status_%d'%i,'')  
                
            
        #messages.error(request,'%s===%s'%(Remark,id))
        Pid = request.POST.get('Pid_%d'%i,'' )
        ct = t_store_marketplan_execution.objects.filter(id=Pid)[0].CreateTime
        
        t_store_marketplan_execution.objects.filter(id=Pid).update(Quantity=F('Quantity')+1,CreateTime=ct)
        #Demand_obj = t_store_marketplan_execution.objects.get(id=Pid).Demand
        #if(t_store_marketplan_execution.objects.get(id=Pid).Quantity==Demand_obj):
            #messages.error(request,'亲~该产品刷单任务完成！')
        
        BuyerAccount1 = request.POST.get('BuyerAccount_%d'%i,'')
        t_store_marketplan_execution_log.objects.filter(id = xid).update(BuyerAccount=BuyerAccount1,Result=Result,Price2=Price2,Remark = Remark,Status='FINISHED')
        
        if Result == '成功':
            t_config_user_buyer.objects.filter(BuyerAccount=BuyerAccount1).update(Balance=F('Balance')-Price2)
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
def saleseveryday(request):
    import datetime
    SKU = request.GET['SKU']
    today = datetime.date.today()
    salesdate = [(today - datetime.timedelta(days=d)).strftime("%Y-%m-%d") for d in range(29, -1, -1)]
    salesnum = [0]*30

    sql = '''select OrderDay,SalesVolume from hq_db.t_report_sales_daily_bysku where OrderDay>=date_sub(sysdate(),INTERVAL 30 day) and SKU=%s ORDER BY 1'''
    cursor = connection.cursor()
    cursor.execute(sql, (SKU, ))
    data = cursor.fetchall()
    cursor.close()

    for od, sv in data:
        i = salesdate.index(od.strftime('%Y-%m-%d'))
        salesnum[i] = int(sv)

    return render(request, 'saleseveryday.html', {'SKU': SKU, 'salesdate': json.dumps(salesdate), 'salesnum': salesnum})
def jump_kc_Status(request):
    from pyapp.table.kc_currentstock_cg_purchaser import kc_currentstock_cg_purchaser
    import datetime
    
    PODate_ago = (datetime.datetime.now()-datetime.timedelta(days=7)).strftime('%Y-%m-%d')
    
    gdStatus = ''
    gdStatus = request.GET['purchaseStatus']
    
    purchaserIndex0 = kc_currentstock_cg_purchaser.objects.filter(Purchasersite=0).values_list('Purchaser',flat=True)

    purchaserIndex1 = kc_currentstock_cg_purchaser.objects.filter(Purchasersite=1).values_list('Purchaser',flat=True)
    purchaserIndex0_0 = ""
    purchaserIndex1_1 = ""
    for pur in purchaserIndex0:
        purchaserIndex0_0 = purchaserIndex0_0 + pur + ','
    for pur in purchaserIndex1:
        purchaserIndex1_1 = purchaserIndex1_1 + pur + ','
      
    url = "/Project/admin/pyapp/kc_currentstock_sku_log_abnormal/?SystemConfirm=N1&StatusUpTimeStart=" + PODate_ago + "&Purchaser="  
    if gdStatus == '0':
        url = url + purchaserIndex0_0
    elif gdStatus == '1':
        url = url + purchaserIndex1_1
    else:
        if request.user.first_name in kc_currentstock_cg_purchaser.objects.filter(permission=0).values_list('Purchaser',flat=True):
            url = "/Project/admin/pyapp/kc_currentstock_sku_log_abnormal/?SystemConfirm=N1&StatusUpTimeStart=" + PODate_ago + "&Purchaser=" + request.user.first_name
        else:
            url = "/Project/admin/pyapp/kc_currentstock_sku_log_abnormal/?SystemConfirm=N1&StatusUpTimeStart=" + PODate_ago
        
    return HttpResponseRedirect(url)
def search_Purchaser(request):  
    cgname = ''
    cgname = request.GET['purchaser']
    url = '/Project/admin/pyapp/kc_currentstock_sku/?storeID=1&GoodsStatus=temporary,over,normal&Purchaser=' + cgname
    return HttpResponseRedirect(url)
@csrf_exempt
def update_cg_status(request):
    import datetime
    from pyapp.table.kc_currentstock_sku_log import *
    id = request.GET.get('id')
    PODate_now = datetime.datetime.now().strftime('%Y-%m-%d')
    value_index = request.GET.get('index')#判断按钮是否被选中,选中为1表示忽略,否则没选中将其状态撤回
    if value_index == '1':
        RemarkContent = kc_currentstock_sku_log.objects.filter(id=id).values('Remark')
        DataFlag = kc_currentstock_sku_log.objects.filter(id=id).values('DataFlag')

        if RemarkContent[0]['Remark'] == '' or RemarkContent[0]['Remark'] is None and DataFlag[0]['DataFlag'] != 2:           
            return HttpResponse(2)
        else:
            kc_currentstock_sku_log.objects.filter(id=id).update(PurchaseStatus='H')
            kc_currentstock_sku_log.objects.filter(id=id).update(PurchaseNum=0)
            kc_currentstock_sku_log.objects.filter(id=id).update(StatusUpTime=datetime.datetime.now())
            kc_currentstock_sku_log.objects.filter(id=id).update(Processor=request.user.first_name)
            return HttpResponse(1)
    else:       
        kc_currentstock_sku_log.objects.filter(id=id).update(PurchaseStatus='W')
        kc_currentstock_sku_log.objects.filter(id=id).update(PurchaseNum=0)

        return HttpResponse(0)

@csrf_exempt
def update_purchaserData(request):
    import datetime
    from pyapp.table.kc_currentstock_sku_log import *
    from pyapp.table.kc_currentstock_sku_log_realtime import *
    from django.db import connection, transaction
    import pyodbc, MySQLdb,pymssql
    from brick.function.update_purchaser import update_purchaser
    import datetime
    from app_djcelery.tasks import exec_purchaser
    timeval = 3*60*60
    if request.is_ajax() and request.method=="GET":
        cgname = request.GET.get('a')
        try: 
            today = datetime.date.today()
            yyyymm08=datetime.datetime(year=today.year, month=today.month, day=today.day, hour=8)
            LastRefreshTime = yyyymm08
            PODate_now = datetime.datetime.now().strftime('%Y-%m-%d')
            refresh_time_objs = kc_currentstock_sku_log_realtime.objects.filter(Purchaser=request.user.first_name,PODate=PODate_now).values('RefreshTime')
            if refresh_time_objs is not None  and len(refresh_time_objs) > 0:
                LastRefreshTime = refresh_time_objs[0]['RefreshTime']       
            off_time = ( datetime.datetime.now() - LastRefreshTime).seconds
            if off_time <= timeval:                                          
                return HttpResponse((timeval - off_time)/60 )
            else:
                update_purchaser_obj = update_purchaser()
                checkifrunRsp= update_purchaser_obj.checkifrun(cgname)
                if checkifrunRsp == 1:                     
                    return HttpResponse(-1)  # 任务正在执行,手贱
            exec_purchaser.delay(cgname)            
            return HttpResponse(0)  #任务请求发送成功，任务正在执行
        except Exception,e:
            messages.error(request,'error----------%s'%e)
            return HttpResponse(-2) #出现exception

@csrf_exempt
def kc_currentstock_Plugin(request):
    import datetime
    from pyapp.table.kc_currentstock_sku import *
    from django.db import connection, transaction
    import pyodbc, MySQLdb,pymssql
    
    if request.is_ajax() and request.method=="GET":
        cgname = request.GET.get('a')

        kc_currentstock_sku_objs = kc_currentstock_sku.objects.filter(Purchaser=cgname).values()
        if cgname == '':
            return HttpResponse(1)
    
        mysqlDBConn = MySQLdb.connect(host=DATABASES['default']['HOST'], user=DATABASES['default']['USER'], passwd=DATABASES['default']['PASSWORD'], db="py_db", charset='utf8')
        mysqlCursor= mysqlDBConn.cursor()
    
        sql1 = "select username from hq_db.auth_user where first_name = '%s'" % cgname
        mysqlCursor.execute(sql1)
        Purchaser = mysqlCursor.fetchone()
    
        mysqlCursor.close()
        mysqlDBConn.close()
        s = datetime.datetime.now()
        try:
            rep = StockData()
        
            rep.getdata(cgname)
            rep.closeconn()
            s1 = datetime.datetime.now()
            #messages.error(request,"----------exec time_sql = %s"%(s1-s))
        except:
            messages.error(request,"----------")
            return HttpResponse(1)
        try:
            upload = upload_kc_to_oss()
            filename = upload.write_excel(cgname,Purchaser[0],kc_currentstock_sku_objs)
            upload.uploadOss(Purchaser[0],filename)
            s2 = datetime.datetime.now()
            #messages.error(request,"----------exec time_upload = %s"%(s2-s1))
            return HttpResponse(0)
        except:
            return HttpResponse(1)
    else:
        return HttpResponse(1)

def kc_currentstock_Plugin_1(request):
    import datetime
    import time
    from pyapp.table.kc_currentstock_sku import *
    from django.db import connection, transaction
    import pyodbc, MySQLdb,pymssql
    cgname = ''
    cgname = request.GET['abc']
    #messages.error(request,"cgname------%s"%cgname)
    s = time.clock()
    mysqlDBConn = MySQLdb.connect(host=DATABASES['default']['HOST'], user=DATABASES['default']['USER'], passwd=DATABASES['default']['PASSWORD'], db="py_db", charset='utf8')
    mysqlCursor= mysqlDBConn.cursor()
    
    sql1 = "select username from hq_db.auth_user where first_name = '%s'" % cgname
    mysqlCursor.execute(sql1)
    Purchaser = mysqlCursor.fetchone()
    #messages.error(request,"Purchaser------%s"%Purchaser)
    
    #sql2 = "SELECT DISTINCT(Purchaser) FROM py_db.b_goods"
    #mysqlCursor.execute(sql2)
    #Purchasers = mysqlCursor.fetchall()

    mysqlCursor.close()
    mysqlDBConn.close()
    
    s = datetime.datetime.now()
    #s = time.clock()
    try:
        rep = StockData()
        rep.getdata(cgname)
        rep.closeconn()
    except:
        messages.error(request,"----------")
    #messages.error(request,"----------exec time = %s"%(time.clock()-s))
    
    upload = upload_kc_to_oss()
    filename = upload.write_excel(cgname,Purchaser[0])
    upload.uploadOss(Purchaser[0],filename)
    messages.error(request,"----------exec time = %s"%(datetime.datetime.now()-s))
    url = '/Project/admin/pyapp/kc_currentstock_sku/?storeID=1&Purchaser=' + cgname
    return HttpResponseRedirect(url)

@csrf_exempt    
def search_SupplierName(request):
    import datetime
    from reportapp.models import t_report_supplier_sku_m
    from pyapp.table.t_product_b_goods import t_product_b_goods
    from pyapp.models import B_Supplier
    from django.db.models import Q
    from  pyapp.models import b_supplier_money
    
    if request.is_ajax() and request.method=="GET":
        try:
            SupplierName_param = request.GET.get('SupplierName')
            return_param = {}
            return_param['supplierSkuCount'] = 0
            return_param['cgSkuCount'] = 0
            return_param['CGALLmoney'] = 0
            lastMonth = datetime.datetime.now().strftime('%Y%m')

            if lastMonth[-2:] == '01':
                lastMonth = str((int(lastMonth[:4]) - 1)) + '12'
            else:
                lastMonth = str(int(lastMonth) - 1)

            SupplierName_num_objs = b_supplier_money.objects.filter(SupplierName=SupplierName_param).values('CGSKUcount','CGALLmoney')
            if SupplierName_num_objs:
                return_param['cgSkuCount'] = SupplierName_num_objs[0]['CGSKUcount']
                return_param['CGALLmoney'] = str(SupplierName_num_objs[0]['CGALLmoney'])

            SupplierID_param = B_Supplier.objects.filter(SupplierName=SupplierName_param).values('NID')
            if SupplierID_param:
                return_param['supplierSkuCount'] = t_product_b_goods.objects.filter(Q(GoodsStatus='正常')|Q(GoodsStatus='临时下架')|Q(GoodsStatus='在售'),SupplierID=SupplierID_param[0]['NID'],Used=0).count()        
            return HttpResponse(json.dumps(return_param),content_type="application/json") 
        except Exception,ex:
            #messages.error(request,'%s_%s:%s'%(traceback.print_exc(),Exception,ex))
            return HttpResponse(-1)
    else:
        return HttpResponse(-1)
def black_list_Plugin(request):
     #连接 sqlserver数据库
    import datetime 
    from skuapp.table.p_trade_blacklist_zip import *
    from django.db import connection, transaction
    import pyodbc, MySQLdb,pymssql
    conn = pymssql.connect(host='122.226.216.10', user='fancyqube', password='K120Esc1',
                                             database='ShopElf',
                                             port='18793')
    cursor = conn.cursor()
    count1 = p_trade_blacklist_zip.objects.all().count()
    try:
        max_nid1 = p_trade_blacklist_zip.objects.filter(From_type='p_trade').latest('NID').NID
        max_nid2 = p_trade_blacklist_zip.objects.filter(From_type='p_tradeun').latest('NID').NID
    except:
        max_nid1 = 0
        max_nid2 = 0
        
    sql1= "SELECT NID,RECEIVERBUSINESS,RECEIVERID,EMAIL,PAYERID,PAYERSTATUS,COUNTRYCODE,SUFFIX,ADDRESSOWNER,ORDERTIME,AllGoodsDetail,SHIPTOZIP,SHIPTOSTREET,SHIPTOSTREET2 FROM p_trade where NID > %d AND shiptozip in ('60604','60601','10028','60604-1406') and (SHIPTOCOUNTRYCODE  ='US' OR COUNTRYCODE  ='US') order by NID"%(max_nid1)
    sql2= "SELECT NID,RECEIVERBUSINESS,RECEIVERID,EMAIL,PAYERID,PAYERSTATUS,COUNTRYCODE,SUFFIX,ADDRESSOWNER,ORDERTIME,AllGoodsDetail,SHIPTOZIP,SHIPTOSTREET,SHIPTOSTREET2 FROM P_TradeUn where NID > %d AND shiptozip in ('60604','60601','10028','60604-1406') and (SHIPTOCOUNTRYCODE  ='US' OR COUNTRYCODE  ='US') order by NID"%(max_nid2)
    
    cursor.execute(sql1)
    objs = cursor.fetchall()
    mysqlDBConn = MySQLdb.connect(host=DATABASES['default']['HOST'], user=DATABASES['default']['USER'], passwd=DATABASES['default']['PASSWORD'], db=DATABASES['default']['NAME'], charset='utf8')
    mysqlCursor= mysqlDBConn.cursor()
    for obj in objs:
        insert_sql = "insert into hq_db.p_trade_blacklist_zip(NID,RECEIVERBUSINESS,RECEIVERID,EMAIL,PAYERID,PAYERSTATUS,COUNTRYCODE,SUFFIX,ADDRESSOWNER,ORDERTIME,AllGoodsDetail,SHIPTOZIP,SHIPTOSTREET,SHIPTOSTREET2,TbTime,From_type) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        #messages.error(request,'insert_sql === %s'%insert_sql)
        #mysqlCursor.execute(insert_sql, (obj.NID,obj.RECEIVERBUSINESS,obj.RECEIVERID,obj.EMAIL,obj.PAYERID,obj.PAYERSTATUS,obj.COUNTRYCODE,obj.SUFFIX,obj.ADDRESSOWNER,obj.ORDERTIME,obj.AllGoodsDetail,obj.SHIPTOZIP,obj.SHIPTOSTREET,obj.SHIPTOSTREET2,datetime.datetime.now(),'p_trade'))
        mysqlCursor.execute(insert_sql, (obj[0],obj[1],obj[2],obj[3],obj[4],obj[5],obj[6],obj[7],obj[8],obj[9],obj[10],obj[11],obj[12],obj[13],datetime.datetime.now(),'p_trade'))
 
    cursor.execute(sql2)
    objs2 = cursor.fetchall()
    for obj in objs2:
        insert_sql = "insert into hq_db.p_trade_blacklist_zip(NID,RECEIVERBUSINESS,RECEIVERID,EMAIL,PAYERID,PAYERSTATUS,COUNTRYCODE,SUFFIX,ADDRESSOWNER,ORDERTIME,AllGoodsDetail,SHIPTOZIP,SHIPTOSTREET,SHIPTOSTREET2,TbTime,From_type) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        #messages.error(request,'insert_sql === %s'%insert_sql)
        #mysqlCursor.execute(insert_sql, (obj.NID,obj.RECEIVERBUSINESS,obj.RECEIVERID,obj.EMAIL,obj.PAYERID,obj.PAYERSTATUS,obj.COUNTRYCODE,obj.SUFFIX,obj.ADDRESSOWNER,obj.ORDERTIME,obj.AllGoodsDetail,obj.SHIPTOZIP,obj.SHIPTOSTREET,obj.SHIPTOSTREET2,datetime.datetime.now(),'p_tradeun'))
        mysqlCursor.execute(insert_sql, (obj[0],obj[1],obj[2],obj[3],obj[4],obj[5],obj[6],obj[7],obj[8],obj[9],obj[10],obj[11],obj[12],obj[13],datetime.datetime.now(),'p_tradeun'))

    
    sql_update1 = "UPDATE p_trade_blacklist_zip SET AllGoodsDetail = getMainSKU(AllGoodsDetail)"
    sql_update2 = "UPDATE t_product_mainsku_pic a,p_trade_blacklist_zip b SET b.pic = a.pic where a.MainSKU = b.AllGoodsDetail"
    mysqlCursor.execute(sql_update1) 
    mysqlCursor.execute(sql_update2)    
    mysqlDBConn.commit()

    mysqlCursor.close()
    mysqlDBConn.close()

    cursor.close()
    #关闭数据库连接
    conn.close()
    count2 = p_trade_blacklist_zip.objects.all().count()
    if count1 == count2:
        messages.error(request,'亲，最近一次更新已经是最新的数据了！')
    return HttpResponseRedirect('/Project/admin/skuapp/p_trade_blacklist_zip/')




    


from brick.wish.cexport_refund_to_oss import *
from brick.db import dbconnect
from django.template import context
from app_djcelery.tasks import CexportRefundCSVTask
import datetime
from django.db import connection

def cexport_refund_to_oss_Plugin(request):
    import datetime
    StrTime = ''
    EndTime = ''
    if request.method == 'POST':
        StrTime = request.POST.get('StrTime','')
        EndTime = request.POST.get('EndTime','')
    if request.method == 'GET':
        StrTime = request.GET.get('StrTime', '')
        EndTime = request.GET.get('EndTime', '')

    if not StrTime or not EndTime:
        messages.error(request, '请正确输入查询时间区间！')
        return HttpResponseRedirect('/Project/admin/skuapp/t_order_refunded/')

    st = datetime.datetime.strptime(StrTime, "%Y-%m-%d")
    ed = datetime.datetime.strptime(EndTime, "%Y-%m-%d")
    daycount = (ed - st).days

    if daycount < 0 :
        messages.error(request, '请正确输入查询时间区间！')
        return HttpResponseRedirect('/Project/admin/skuapp/t_order_refunded')

    if daycount > 60:
        messages.error(request, '请输入两月内查询时间区间！')
        return HttpResponseRedirect('/Project/admin/skuapp/t_order_refunded')

    #username = request.user.username
    # db_conn = dbconnect.run({})['db_conn']
    #params = {'db_conn':connection, 'StrTime': StrTime, 'EndTime': EndTime, 'UserName': username}
    #cexport_refund_to_oss_obj = cexport_refund_to_oss()
    #cexport_refund_to_oss_obj.fexport_refund_to_oss(params)
    # params = {'StrTime': StrTime, 'EndTime': EndTime,'UserName'}
    
    username = request.user.username
    params = {'StrTime': StrTime, 'EndTime': EndTime, 'UserName': username}
    CexportRefundCSVTask.delay(params)
    return HttpResponseRedirect('/Project/admin/skuapp/t_order_refunded/')
    
    
    
def t_product_up_downPlugin(request):
    #from brick.pydata.py_redis.py_SynRedis_pub import py_SynRedis_pub
    from brick.classredis.classsku import classsku
    SKU = request.POST.get('SKU1','')
    if SKU=='':
        messages.error(request,'SKU不能为空!!')
        return HttpResponseRedirect('/Project/admin/skuapp/t_product_up_down/add/')
    else:
         Goods_objs = py_b_goods.objects.filter(SKU__contains=SKU)  #.exclude(GoodsStatus='临时下架')
         SKU_objs = Goods_objs.values('NID','SKU')
         #py_SynRedis_pub=py_SynRedis_pub()
         classsku_obj=classsku()
         for SKU_obj in SKU_objs:
            #allkc = float(py_SynRedis_pub.getFromHashRedis('',SKU_obj['SKU'],'Number'))
            allkc = classsku_obj.get_number_by_sku(SKU_obj['SKU'])
            if allkc is None:
                allkc = 0.0
            #messages.error(request,'1---%s'%allkc)
            #zykc = float(py_SynRedis_pub.getFromHashRedis('',SKU_obj['SKU'],'ReservationNum'))
            zykc = classsku_obj.get_reservationnum_by_sku(SKU_obj['SKU'])
            if zykc is None:
                zykc = 0.0
            #messages.error(request,'2---%s'%zykc)
            kykc = float(allkc)-float(zykc)
            #messages.error(request,'3---%s'%kykc)
            #messages.error(request,'cccccccc---xx%s'%kykc)
            kc = str(kykc)
            #messages.error(request,'cccccccc---ss%s'%kc)
            if kc == '-1':             
                kc = '未查询到'
            py_b_goods.objects.filter(NID=SKU_obj['NID']).update(kykc=kc)
            #messages.error(request,'%s---%s'%(type(kykc),kykc))
         #time = Goods_objs[0].CreateDate
         #messages.error(request,Goods_objs)
    return render(request, 't_product_up_downPlugin.html',{'Goods_objs':Goods_objs,'page_status':1})
    
def save_up_down(request):
    from skuapp.table.t_product_information_modify import *
    from skuapp.table.t_product_up_down import t_product_up_down
    import datetime
    from brick.classredis.classsku import classsku
    from django_redis import get_redis_connection
    redis_coon = get_redis_connection(alias='product')
    classsku_obj = classsku(db_cnxn=connection, redis_cnxn=redis_coon)

    post = request.POST
    SKUList = post.getlist('SKU')
    GoodsNameList = post.getlist('GoodsName')
    GoodsStatusList = post.getlist('GoodsStatus')
    PurchaserList = post.getlist('Purchaser')
    SalerName2List = post.getlist('SalerName2')
    SupplierIDList = post.getlist('SupplierID')
    Supplier_urlList = post.getlist('Supplier_url')
    CreateDateList = post.getlist('CreateDate')
    Add_DayList = post.getlist('AddDay')
    RemarkList = post.getlist('Remark')
    #messages.info(request, 'sku-----------%s' % Add_DayList)
    #messages.info(request, 'time-----------%s' % Add_TimeList)
    #messages.info(request, 'Supplier_urlList-----------%s' % Supplier_urlList)        
    #messages.info(request, 'len(SKUList)-----------%s' % len(SKUList)) 

    Request_man_obj = request.user.first_name
    Request_date_obj = datetime.datetime.now()
    
    if len(SKUList)>1:
        for i in range(len(SKUList)):
            try:
                SupplierID=SupplierIDList[i]
                SupplierName=sku_b_supplier.objects.filter(NID=SupplierID).SupplierName
            except:
                SupplierName=''
            #messages.info(request, 'Supplier_urlList[i]-----------%s' % Supplier_urlList[i])

            try:
                if Add_DayList[0] != '' or Add_DayList[0] is not None:
                    try:
                        t_product_up_down.objects.filter(SKU=SKUList[i]).update(sum=F('sum')+1)
                        sum_obj = t_product_up_down.objects.filter(SKU=SKUList[i]).latest('id').sum
                        t_product_up_down.objects.filter(SKU=SKUList[i]).delete()
                    except:
                        sum_obj = 1
                    date_obj = datetime.datetime.now() + datetime.timedelta(days = int(Add_DayList[i]))
                    t_product_up_down.objects.create(SKU=SKUList[i], Goods_Name=GoodsNameList[i], Goods_Status='0',
                                                 Purchase_man=PurchaserList[i],Producer=SalerName2List[i],SupplierID=SupplierIDList[i],
                                                 Supplier_url=Supplier_urlList[i],Goodsbirth=CreateDateList[i],Supplier=SupplierName,
                                                 Add_Date=date_obj,Request_man=Request_man_obj,Request_date=Request_date_obj,Remark=RemarkList[i],day_obj=int(Add_DayList[i]),sum=sum_obj)
            except:
                #messages.error(request,'天数必须是数字!')
                pass

    else:
        try:
            SupplierID=SupplierIDList[0]
            SupplierName=sku_b_supplier.objects.filter(NID=SupplierID).SupplierName
        except:
            SupplierName=''
        #messages.info(request, 'Supplier_urlList[i]-----------%s' % Supplier_urlList[i])
        if Add_DayList[0] != '' or Add_DayList[0] is not None:
            #try:
            try:
                t_product_up_down.objects.filter(SKU=SKUList[0]).update(sum=F('sum')+1)         
                sum_obj = t_product_up_down.objects.filter(SKU=SKUList[0]).latest('id').sum
                t_product_up_down.objects.filter(SKU=SKUList[0]).delete()
            except:
                sum_obj = 1
            date_obj = datetime.datetime.now() + datetime.timedelta(days = int(Add_DayList[0]))
            #except:
                #messages.error(request,'天数必须是数字!')
            SupplierID = SupplierIDList[0]
            if SupplierIDList[0] == '':
                SupplierID = None
            t_product_up_down.objects.create(SKU=SKUList[0], Goods_Name=GoodsNameList[0], Goods_Status='0',
                             Purchase_man=PurchaserList[0],Producer=SalerName2List[0],SupplierID=SupplierID,
                             Supplier_url=Supplier_urlList[0],Goodsbirth=CreateDateList[0],Supplier=SupplierName,
                             Add_Date=date_obj,Request_man=Request_man_obj,Request_date=Request_date_obj,Remark=RemarkList[0],day_obj=int(Add_DayList[0]),sum=sum_obj)
        else:
            pass
    try:
        t_obj = py_b_goods.objects.filter(SKU=SKUList[0]).values('GoodsName', 'CreateDate')
        pic = u'http://fancyqube.net:89/ShopElf/images/%s.jpg' % SKUList[0].replace('OAS-', '').replace('FBA-', '')
        goods_name = ''
        dev_date = None
        if t_obj.exists():
            goods_name = t_obj[0]['GoodsName']
            dev_date = t_obj[0]['CreateDate']
        main_sku = classsku_obj.get_bemainsku_by_sku(sku=SKUList[0])
        details = {}
        for i in range(len(SKUList)):
            sku = SKUList[i]
            remark = RemarkList[i]
            add_day = int(Add_DayList[i])
            date_obj = (datetime.datetime.now() + datetime.timedelta(days=add_day)).strftime('%Y年%m月%d日')
            xgms = '备注：%s;%s天后%s重新上架' % (remark, add_day, date_obj)
            current_status = classsku_obj.get_goodsstatus_by_sku(sku=sku)
            details[sku] = {'GoodsStatus': [u'当前状态', current_status, u'临时下架', xgms, u'临时下架']}
        t_product_information_modify.objects.create(
            Mstatus='DLQ', SQTimeing=Request_date_obj, SKU=sku, Name2=goods_name,
            SourcePicPath2=pic, InputBox=','.join(SKUList), DevDate=dev_date, Select='2',
            SQStaffNameing=Request_man_obj, Details=details, MainSKU=main_sku, XGcontext=''
        )
    except Exception, e:
        print e

    return HttpResponseRedirect('/Project/admin/skuapp/t_product_up_down/')




def t_online_info_logisticPlugin(request):
    return HttpResponseRedirect('/Project/admin/skuapp/t_online_info_logistic/')












def aaa(request):
        if request.method == 'POST':
            object_id = request.POST.get('object_id','')
            if object_id is None or object_id.strip()=='':
                return
        obj  = t_product_survey_ing.objects.get(id__exact=object_id)
        if request.method == 'POST':
            files = request.FILES.getlist('file_%s'%object_id)
            for f in files :
                logger = logging.getLogger('sourceDns.webdns.views')    #刚才在setting.py中配置的logger
                logger.error("zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz%s"%f.name)
                auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
                bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_SV)


                bucket.put_object(u'%s/%s.jpg'%(obj.id,obj.id),f)
                #保存图片
                obj.SourcePicPath =  u'%s%s.%s/%s/%s.jpg'%(PREFIX,BUCKETNAME_SV,ENDPOINT_OUT,obj.id,obj.id)
                obj.save()
        #obj.savexxx()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
def applymainsku(request):
    Category2New = request.POST.get('Category2','')
    object_id = request.POST.get('object_id','')

    t_product_develop_ing_obj  = t_product_develop_ing.objects.get(id__exact=object_id)
    #判断是否已经分配mainsku

    if t_product_develop_ing_obj.MainSKU is not None and t_product_develop_ing_obj.MainSKU.strip()!='' :
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    Category2_seq = t_sys_sku_seq.objects.filter(CategoryName=Category2New);
    if Category2_seq.count() <=0 :
        t_sys_sku_seq_obj = t_sys_sku_seq(CategoryName=Category2New,CategoryDesc=Category2New,CategoryPrefix='A',CurValue=1000)

        t_product_develop_ing_obj.MainSKU = '%s%s%s'%(Category2New , t_sys_sku_seq_obj.CategoryPrefix, t_sys_sku_seq_obj.CurValue)
        t_product_develop_ing_obj.SKU = t_product_develop_ing_obj.MainSKU
        t_product_develop_ing_obj.Category2 = Category2New

        t_sys_sku_seq_obj.CurValue = t_sys_sku_seq_obj.CurValue + 1

        t_sys_sku_seq_obj.save()
        t_product_develop_ing_obj.save()
    else:
        t_product_develop_ing_obj.MainSKU = '%s%s%s'%(Category2New,Category2_seq[0].CategoryPrefix ,Category2_seq[0].CurValue)
        t_product_develop_ing_obj.SKU = t_product_develop_ing_obj.MainSKU
        t_product_develop_ing_obj.Category2 = Category2New

        Category2_seq.update(CurValue = Category2_seq[0].CurValue + 1)
        t_product_develop_ing_obj.save()

    #插入表头数据 name
    t_product_mainsku_arrt_name_obj= t_product_mainsku_arrt_name(MainSKU=t_product_develop_ing_obj.MainSKU ,Attrid=0,AttrName='子SKU名称', pid=object_id)
    t_product_mainsku_arrt_name_obj.save()


    #插入主SKU和子SKU对应关系
    t_product_mainsku_sku_obj = t_product_mainsku_sku(MainSKU=t_product_develop_ing_obj.MainSKU ,SKU = t_product_develop_ing_obj.SKU , pid=object_id)
    t_product_mainsku_sku_obj.save()

    #插入属性数据 name
    t_product_sku_attr_value_obj= t_product_sku_attr_value(MainSKU=t_product_develop_ing_obj.MainSKU,SKU=t_product_develop_ing_obj.MainSKU,Attrid=0,AttrValue=t_product_develop_ing_obj.Name)
    t_product_sku_attr_value_obj.save()

    #尝试去创建 bucket,失败没事
    path_az = re.sub('[^a-zA-Z]','',t_product_develop_ing_obj.MainSKU) #去掉字母
    bucket_name = 'fancyqube-%s'%(path_az.lower())
    oss2auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(oss2auth, ENDPOINT,bucket_name)
    bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
def mstsc2(request):
    #logger.error("-------------------requestrequestrequestrequest22222,request.websocket=%s"%request.websocket)
    #id = request.GET['id']
    #logger.error("aaa=%s"%aaa)
    xid = request.GET['id']
    t_config_mstsc_log.objects.filter(id=xid).delete()
def mstsc3(request):
    xid = request.GET['id']
    t=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    t_config_mstsc_log.objects.filter(id=xid).update(LoginOutTime=t,QuitReason="OUT")
def mstsc4(request):
    xid = request.GET['id']
    t=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    logger = logging.getLogger('sourceDns.webdns.views')
    logger.error("id =%s tttttttttttttttttttttttttttttt=%s "%(id,t))
    t_config_mstsc_log.objects.filter(id=xid).update(LastAnswerTime=t)
            

def mstsc(request):
    #logger = logging.getLogger('sourceDns.webdns.views')
    
    t=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    mstscid = request.GET['id']
    staffID=''
    CloudName=''
    kvmName=''
    try:
        #根据传过来的username查找auth_user表格中的firstname
        staffID=request.GET['staffID']
        CloudName=request.GET['CloudName']
        kvmName=request.GET['kvmName']
    except:
        pass
    #sql1='select first_name from auth_user where username=\'%s\' '%staffID
    #cursor.execute(sql1)
    #auth_user_obj = cursor.fetchone()
    try:
        auth_user_obj = User.objects.get(username=staffID)
        if auth_user_obj is not None:
             first_name= auth_user_obj.first_name
    except:
        #用户名不唯一
        pass
    
    
    
    
    
    #sql2 = 'select IP,UserName,Password,ShopName from t_config_mstsc where id=\'%s\' '%id
    #cursor.execute(sql2)
    #t_config_mstsc_obj = cursor.fetchone()
    #cursor.close()
    try:
        t_config_mstsc_obj = t_config_mstscfinance.objects.get(id=mstscid)
        if t_config_mstsc_obj is not None:
            ip = t_config_mstsc_obj.IP
            userName = t_config_mstsc_obj.UserName
            password = t_config_mstsc_obj.Password
            ShopName=t_config_mstsc_obj.ShopName
            hostip = t_config_mstsc_obj.hostip
    except:
        #店铺ID不唯一
        pass

    t_config_mstsc_log_obj = t_config_mstsc_log(ShopName=ShopName,UserName=userName,FirstName=first_name,LoginInTime=t,LastAnswerTime=t,QuitReason="IN")
    t_config_mstsc_log_obj.save()
    id=t_config_mstsc_log_obj.id

    # Encrypt password
    password = encrypt_password(password)

    data={'ip':ip,'userName':userName,'password':password,'ShopName':ShopName,'staffID':staffID,'first_name':first_name,'time':t,'id':id,'kvmName':kvmName,'hostip':hostip}
    return render(request,"mstsc.html",data)

    #return render(request,"mstsc.html",data)
def mstschequyun(request):
    #logger = logging.getLogger('sourceDns.webdns.views')
    
    t=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    mstscid = request.GET['id']
    
    #根据传过来的username查找auth_user表格中的firstname
    staffID=request.GET['staffID']
    CloudNamehequyun=request.GET['CloudName']
    ShopNamehequyun=request.GET['ShopName']
    #sql1='select first_name from auth_user where username=\'%s\' '%staffID
    #cursor.execute(sql1)
    #auth_user_obj = cursor.fetchone()
    try:
        auth_user_obj = User.objects.get(username=staffID)
        if auth_user_obj is not None:
             first_name= auth_user_obj.first_name
    except:
        #用户名不唯一
        pass
    #调用函数获取登陆的ip 用户名 密码
    ################################ 
    
    #获取拨vpn需要的参数
    try:
        t_config_mstsc_obj = t_config_mstscfinance.objects.get(ShopName=ShopNamehequyun,IP_isnull=False)
        if t_config_mstsc_obj is not None:
            Shopip = t_config_mstsc_obj.IP
            ShopuserName = t_config_mstsc_obj.UserName
            Shoppassword = t_config_mstsc_obj.Password
            ShopName=t_config_mstsc_obj.ShopName
    except:
        #店铺ID不唯一
        pass
    t_config_mstsc_log_obj = t_config_mstsc_log(ShopName=ShopName,UserName=userName,FirstName=first_name,LoginInTime=t,LastAnswerTime=t,QuitReason="IN")
    t_config_mstsc_log_obj.save()
    id=t_config_mstsc_log_obj.id
    data={'ip':ip,'userName':userName,'password':password,'ShopName':ShopName,'staffID':staffID,'first_name':first_name,'time':t,'id':id}
    return render(request,"mstsc.html",data)
    

from skuapp.public.aliyun_reboot import *
from skuapp.public.txyun_reboot import *
def mstscReboot(request):
    logger = logging.getLogger('sourceDns.webdns.views')
    t=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    mstscid = request.GET['id']
    staffID=request.GET['staffID']
    try:
        auth_user_obj = User.objects.get(username=staffID)
        if auth_user_obj is not None:
             first_name= auth_user_obj.first_name
    except:
        pass
    try:
        t_config_mstsc_obj = t_config_mstscfinance.objects.get(id=mstscid)
        if t_config_mstsc_obj is not None:
            ip = t_config_mstsc_obj.IP
            userName = t_config_mstsc_obj.UserName
            password = t_config_mstsc_obj.Password
            ShopName=t_config_mstsc_obj.ShopName
            InstanceId=t_config_mstsc_obj.InstanceId
            RegionId=t_config_mstsc_obj.RegionId
    except:
        pass
    if t_config_mstsc_obj is not None:
        if t_config_mstsc_obj.CloudName=='aliyun':
            instanceId = r'%s'%InstanceId
            get_regions("ecs.aliyuncs.com","RebootInstance",{"InstanceId":instanceId,},str("wjEIGuPnRjSURzUDYUmBXrFv3ijk8f"),"FP60l5Rd7FBHDNAZ","2014-05-26")
            
        if t_config_mstsc_obj.CloudName=='tengxunyun':
            SecretId='AKIDJWaWGsByFRVN3Wo7NX9apskRXYROoSXY'
            #regions=['ap-guangzhou','ap-shenzhen-fsi','ap-shanghai','ap-shanghai-fsi','ap-beijing',]
            #regions=['ap-beijing',]
            #for region in regions:
            YOUR_PARAMS = {
                    'SecretId': SecretId,
                    'Timestamp': int(time.time()),
                    'Nonce': random.randint(1, sys.maxint),
                    'Region':r'%s'%RegionId,
                    'Action': 'RebootInstances',
                    'InstanceIds.0':r'%s'%InstanceId,
                    'ForceReboot':True,
                    'Version':'2017-03-12'
                    }
            #main('c7eBvePFzjVKA4naOC0kWJ6seQBriaTE',YOUR_PARAMS)
            content=main(str('c7eBvePFzjVKA4naOC0kWJ6seQBriaTE'),YOUR_PARAMS)
        t_config_mstsc_log_obj = t_config_mstsc_log(ShopName=ShopName,UserName=userName,FirstName=first_name,LoginInTime=t,LoginOutTime=t,QuitReason="Reboot")
        t_config_mstsc_log_obj.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



def order1day(request):
    import datetime as datime
    from django.db.models import Max
    from skuapp.table.t_wish_pb_productdailystats import t_wish_pb_productdailystats

    ProductID = request.GET['aID']
    mdate = '0'
    pbobjs = t_wish_pb_productdailystats.objects.filter(product_id=ProductID)
    if pbobjs.exists():
        dateobjs = pbobjs.aggregate(mdate=Max('p_date'))
        mdate = dateobjs['mdate'].strftime('%Y%m%d')
    mdate = int(mdate)

    categories = []
    series = []
    rt = ''
    newcategories = []
    t_report_orders1days_objs = t_report_orders1days.objects.filter(ProductID=ProductID)
    if t_report_orders1days_objs.exists():
        for t_report_orders1days_obj in t_report_orders1days_objs:
            categories.append(int(t_report_orders1days_obj.YYYYMMDD))
            series.append(t_report_orders1days_obj.OrdersLast1Days)
    categ = (datime.datetime.now()++ datime.timedelta(days=-1)).strftime('%Y%m%d')
    # if len(categories) >= 1:
    #     categ = str(categories[0])
    for i in range(0,60):
        tmpcategories = int((datime.datetime.strptime(categ, '%Y%m%d') + datime.timedelta(days=-i)).strftime('%Y%m%d'))
        if tmpcategories not in categories:
            series.insert(i,0)
        newcategories.append(tmpcategories)
    if len(series) > 60:
        series = series[0:60]
    newcategories.reverse()
    series.reverse()

    try:
        idx = newcategories.index(mdate)
    except :
        idx = -1

    return render(request, 'order1day.html',{'rt':rt,'categories':newcategories,'series':series, 'idx': idx, 'mdate': mdate})



def ebay_order1day(request):
    itemid = request.GET['ID']
    categories = []
    series = []
    rt = ''
    t_report_ebay_orders1days_objs = t_report_ebay_orders1days.objects.filter(itemid=itemid)
    if t_report_ebay_orders1days_objs.exists():
        for t_report_ebay_orders1days_obj in t_report_ebay_orders1days_objs:
            categories.append(int(t_report_ebay_orders1days_obj.YYYYMMDD))
            series.append(t_report_ebay_orders1days_obj.OrdersLast1Days)
        categories.reverse()
        series.reverse()
    else:
        rt = '<span>抱歉！没有该itemid的日销量记录！</span>'
    return render(request, 'order1day.html',{'rt':rt,'categories':categories,'series':series})

def SKU(request):
    ProductID = request.GET['abc']
    rt='<table   style="text-align:center;" border="1" cellpadding="3" cellspacing="1" bgcolor="#c1c1c1"><tr bgcolor="#C00"><th style="text-align:center">子SKU</th><th style="text-align:center">店铺SKU</th><th style="text-align:center">库存量</th><th style="text-align:center">价格</th><th style="text-align:center">运费</th><th style="text-align:center">状态</th></tr>'
    t_online_info_wish_objs = t_online_info.objects.values('SKU','ShopSKU','Quantity','Price','Status','Shipping').filter(ProductID=ProductID)
    for t_online_info_wish_obj in t_online_info_wish_objs:
        rt = '%s <tr bgcolor="#FFFFFF"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr> '%(rt,t_online_info_wish_obj['SKU'],t_online_info_wish_obj['ShopSKU'],t_online_info_wish_obj['Quantity'],t_online_info_wish_obj['Price'],t_online_info_wish_obj['Shipping'],t_online_info_wish_obj['Status'])
    rt = "%s</table>"%rt

    return render(request, 'SKU.html', {'rt':rt})

def trunk_bhtc(request):
    from datetime import datetime
    from skuapp.table.t_task_trunk import *
    from skuapp.table.t_task_operation_log import *
    Task_id = request.GET.get('ts_id')
    #messages.error(request,'----%s'%Task_id)
    Task_info = request.GET.get('Task_info')
    Task_handler = request.GET.get('Task_handler')
    Create_man = request.GET.get('Create_man')
    t_task_operation_log.objects.create(Original_number=Task_id,Flow_way_status='处理==>提出',Flow_handle_result='驳回问题提出处',Flow_handle_remark=Task_info,Flow_handle_man=Task_handler,Flow_handle_time=datetime.now())
    t_task_trunk.objects.filter(Original_number=Task_id).update(Current_chargeman=Create_man,Flow_Status='TC',Check_result=None,Check_info=None,Check_time=None,Ask_time=None,Task_status=None,Task_info=None,Task_handler=None,Task_handler_time=None)
    return HttpResponseRedirect('/Project/admin/skuapp/t_task_trunk?status=mytask&Flow_Status=TC,SH,CL,NYZ,YZ')


def trunk_wtqx(request):
    from datetime import datetime
    from skuapp.table.t_task_trunk import *
    from skuapp.table.t_task_operation_log import *
    Task_id = request.GET.get('ts_id')
    Create_man = request.GET.get('Create_man')
    if Create_man is None or Create_man == '':
        pass
    else:
        #messages.error(request,'----%s'%Task_id)
        t_task_operation_log.objects.create(Original_number=Task_id,Flow_way_status='提出==>取消',Flow_handle_result='问题单取消',Flow_handle_remark="/",Flow_handle_man=request.user.first_name,Flow_handle_time=datetime.now())
        t_task_trunk.objects.filter(Original_number=Task_id).update(Current_chargeman=Create_man,Flow_Status='QX')
    return HttpResponseRedirect('/Project/admin/skuapp/t_task_trunk?status=mytask&Flow_Status=TC,SH,CL,NYZ,YZ') 

    
def t_task_trunk_rwtj(request):
    from datetime import datetime
    from skuapp.table.t_task_trunk import t_task_trunk
    from django.db.models import Q
    from django.db.models import Count
    import MySQLdb
    #trunk_objs = t_task_trunk.objects.exclude(Q(Flow_Status='GB')|Q(Flow_Status='QX')).values('Current_chargeman').annotate(count=Count('Current_chargeman')).values('Current_chargeman', 'count')
    #上述这个条件为什么不行?by chenchen
    conn = MySQLdb.connect(host=DATABASES['default']['HOST'], user=DATABASES['default']['USER'], passwd=DATABASES['default']['PASSWORD'], db=DATABASES['default']['NAME'], charset='utf8')
    sql = "SELECT Current_chargeman,COUNT(Current_chargeman) FROM t_task_trunk where flow_status !='GB' AND flow_status !='QX' GROUP BY Current_chargeman"
    cursor = conn.cursor()
    cursor.execute(sql)
    trunk_objs = cursor.fetchall()
    flag = True
    list_obj = []
    big_list = []
    for trunk_obj in trunk_objs:
        dic = {}
        dic['first_name'] = ''
        objs = User.objects.filter(username=trunk_obj[0]).values('first_name')
        xg_objs = t_task_trunk.objects.filter(Current_chargeman=trunk_obj[0]).values('Create_man','Check_man','Task_handler','Identifier')
        xg_list = []
        for xg_obj in xg_objs:
            try:
                name_create = User.objects.filter(username=xg_obj['Create_man']).values_list('first_name',flat=True)[0]
            except:
                name_create = ''
            try:
                name_check = User.objects.filter(username=xg_obj['Check_man']).values_list('first_name',flat=True)[0]
            except:
                name_check = ''
            try:
                name_handler = User.objects.filter(username=xg_obj['Task_handler']).values_list('first_name',flat=True)[0]
            except:
                name_handler = ''
            try:
                name_Identifier = User.objects.filter(username=xg_obj['Identifier']).values_list('first_name',flat=True)[0]
            except:
                name_Identifier = ''
            xg_list.append(name_create)
            xg_list.append(name_check)
            xg_list.append(name_handler)
            xg_list.append(name_Identifier)
            big_list.append(name_create)
            big_list.append(name_check)
            big_list.append(name_handler)
            big_list.append(name_Identifier)        
        sorted(set(big_list))
        dic['xgr'] = ' '.join(sorted(set(xg_list)))
        if objs.exists():
            dic['first_name'] = objs[0]['first_name']
        dic['username'] = trunk_obj[0]
        dic['count'] = trunk_obj[1]
        list_obj.append(dic)
    big_list = list(sorted(set(big_list)))
    usingname = request.user.first_name
    return render(request,'t_task_trunkPlugin.html',{'flag':flag,'trunk_objs':trunk_objs,'list_obj':list_obj,'big_list':big_list,'usingname':usingname})


def t_task_trunk(request):
    import json
    Task_id = request.GET['cc']
    cl_man = request.GET['dd']
    hadler_objs = User.objects.all()
    list_objs = User.objects.values('username','first_name')
    list_list = []
    for list_obj in list_objs:
        list_list.append(list_obj['username']+'/'+list_obj['first_name'])
    return render(request, 'task_details.html', {'objs':hadler_objs,'Task_id':Task_id,'cl_man':cl_man,'list_list':json.dumps(list_list)})
    
def task_trunk(request):
    from datetime import datetime
    from skuapp.table.t_task_trunk import *
    from skuapp.table.t_task_operation_log import *
    Task_id = request.GET.get("Task_id")
    Task_handler = request.GET.get("Task_handler")
    #messages.error(request,"--------%s"%Task_handler)
    Task_handler = Task_handler.split("/")[0]
    cl_man = request.GET.get("cl_man")
    try:
        cl_man = User.objects.filter(username=cl_man).values_list('first_name',flat=True)[0]
    except:
        cl_man = u'找不到对应的中文用户名！'
    t_task_operation_log.objects.create(Original_number=Task_id,Flow_way_status='转发',Flow_handle_result='通过',Flow_handle_remark='/',Flow_handle_man=cl_man,Flow_handle_time=datetime.now())
    t_task_trunk.objects.filter(Original_number=Task_id).update(Task_handler=Task_handler,Current_chargeman=Task_handler)
    return render(request, 'task_details.html') 
    
def trunk_form(request):
    from datetime import datetime
    from skuapp.table.t_task_trunk import * 
    ts_id=request.GET.get("ts_id")
    fs_obj=request.GET.get("fs_obj") 
    #messages.error(request,u'xxxxxx--cc%s'%ts_id)
    try:
        ts_id = int(ts_id)
    except:
        ts_id = -1
    Flow_type=request.GET.get("Flow_type")
    Demand_name=request.GET.get("Demand_name")
    Demand_description=request.GET.get("Demand_description")
    Check_man=request.GET.get("Check_man")
    Pre_Identifier=request.GET.get("Pre_Identifier")
    Hope_time=request.GET.get("Hope_time")
    Create_man = request.user.username
    Create_time = datetime.now()
    
    Check_result=request.GET.get("Check_result")
    Check_info=request.GET.get("Check_info")
    Task_handler=request.GET.get("Task_handler")
    Ask_time=request.GET.get("Ask_time")
    #messages.error(request,u'xxxxxx--cc%s'%Ask_time)
    
    Task_status=request.GET.get("Task_status")
    Task_info=request.GET.get("Task_info")
    Identifier=request.GET.get("Identifier")
    
    Identifier_result=request.GET.get("Identifier_result")
    Identifier_info=request.GET.get("Identifier_info")
    #messages.error(request,'------%s'%ts_id)
    if ts_id == -1:
        t_task_trunk.objects.create(Flow_type=Flow_type,Demand_name=Demand_name,Demand_description=Demand_description,Check_man=Check_man,Pre_Identifier=Pre_Identifier,Create_man=Create_man,Create_time=Create_time,Current_chargeman=Create_man,Flow_Status='TC')
    else:
        if fs_obj == 'TC' or fs_obj == '':
            t_task_trunk.objects.filter(Original_number=ts_id).update(Flow_type=Flow_type,Demand_name=Demand_name,Demand_description=Demand_description,Check_man=Check_man,Pre_Identifier=Pre_Identifier,Hope_time=Hope_time,Create_man=Create_man,Create_time=Create_time)
        elif fs_obj == 'SH':
            t_task_trunk.objects.filter(Original_number=ts_id).update(Check_result=Check_result,Check_info=Check_info,Task_handler=Task_handler,Ask_time=Ask_time)
        elif fs_obj == 'CL':
            t_task_trunk.objects.filter(Original_number=ts_id).update(Task_status=Task_status,Task_info=Task_info,Identifier=Identifier)
        elif fs_obj == 'YZ':
            t_task_trunk.objects.filter(Original_number=ts_id).update(Identifier_result=Identifier_result,Identifier_info=Identifier_info)
        else:
            pass
    return HttpResponseRedirect('/Project/admin/skuapp/t_task_trunk?status=mytask&Flow_Status=TC,SH,CL,NYZ,YZ')
    
def t_task_details(request):
    Task_name_current = request.GET['cur_name']
    Task_name_original = request.GET['orgi_name']
    Current_number = request.GET['cur_num']
    Original_number = request.GET['orgi_num']
    rt='<form action="/task/sub"><table   style="text-align:center;" border="1" cellpadding="3" cellspacing="1" bgcolor="#c1c1c1"><tr><td>父任务名</td><td><input name="parent_name" readonly="readonly" value="%s" /></td></tr>\
    <tr><td>原始任务名</td><td><input readonly="readonly" name="original_name" value="%s" /></td></tr> <tr><td>当前任务名</td><td><input name="current_name" value="" /></td></tr> <tr><td>当前责任人</td><td><input name="current_man" value="" /></td></tr>\
    '%(Task_name_current,Task_name_original)
    rt = '%s</table><br><input type="hidden" name="parent_num" value="%s"><input type="hidden" name="original_num" value="%s"><input id="sub" type="submit" value="提交" /> </form>'%(rt,Current_number,Original_number,)
    

    return render(request, 'task_details.html', {'rt':rt})
    
def task_sub(request):
    from skuapp.table.t_task_details import *
    current_name = request.GET.get("current_name")
    current_man = request.GET.get("current_man")
    
    Task_name_original = request.GET.get("original_name")
    Original_number = request.GET.get("original_num")
    Task_name_current = request.GET.get("parent_name")
    Current_number = request.GET.get("parent_num")  
    t_task_details.objects.create(Task_name_current=current_name,Task_name_original=Task_name_original,Original_number=Original_number,Task_name_parent=Task_name_current,
                                    Parent_number=Current_number,Create_man=request.user.first_name,Task_status='create',Current_chargeman=current_man)
    return render(request, 'task_details.html')
    
def t_task_son(request):
    from skuapp.table.t_task_details import *
    original_num = request.GET['original_num']
    Task_name_original = request.GET['original_name']
    t_task_details.objects.create(Original_number=original_num,Parent_number=original_num,Task_name_parent='顶级任务',Task_status='create',Task_name_original=Task_name_original,Create_man=request.user.first_name)
    Current_number = t_task_details.objects.filter(Original_number=original_num).latest('Current_number').Current_number
    Current_number = int(Current_number)
    return HttpResponseRedirect('/Project/admin/skuapp/t_task_details/%s/update/'%Current_number)
    #messages.error(request,Current_number)
    #return HttpResponseRedirect('/Project/admin/skuapp/t_task_trunk')

    


def storage(request):
    from decimal import *
    from skuapp.table.t_set_warehouse_storage_situation_list import t_set_warehouse_storage_situation_list
    from skuapp.table.t_shipping_management import t_shipping_management
    storage_list = request.GET.get("request_data")
    try:
        # messages.error(request,'----%s'%storage_list)
        objs = t_set_warehouse_storage_situation_list.objects.filter(AccountNum=storage_list,
                                                                     Destination_warehouse__icontains='FBW',
                                                                     Arrival_status='already', Storage_status='already')
        if objs:
            The_lot_number = 'SHIP' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '-' + str(objs[0].id)
            myplan = []
            myproductinfo = []
            warehouselist = []
            Cargo_infor = []
            for obj in objs:
                if obj.Arrival_status == 'already' and obj.Storage_status == 'already' and obj.Delivery_status == 'notyet':
                    myplan.append(obj.Stocking_plan_number)
                    myproductinfo.append(obj.ProductSKU + '*' + str(obj.The_arrival_of_the_number))
                    warehouselist.append(obj.Destination_warehouse)
                    productinfo = [obj.ProductSKU, obj.Stocking_quantity, obj.The_arrival_of_the_number, '', obj.ProductName,
                                   '']
                    Cargo_infor.append(productinfo)

            if len(set(warehouselist)) > 1:
                messages.error(request, u'同一批次必须是同一目的地仓库！！！')
            elif len(set(warehouselist)) == 1:
                from brick.public.generate_excel import generate_excel
                from brick.public.create_dir import mkdir_p
                from Project.settings import BUCKETNAME_overseas_warehouse_cargo_infor_xls, MEDIA_ROOT
                import os, oss2
                from brick.public.upload_to_oss import upload_to_oss

                Cargo_infor.insert(0, ['SKU', u'计划发货数量', u'实际发货数量', u'备注', u'产品名称', u'仓位'])

                path = MEDIA_ROOT + 'download_xls/' + request.user.username
                # if not os.path.exists(path):
                mkdir_p(MEDIA_ROOT + 'download_xls')
                os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))

                mkdir_p(path)
                os.popen('chmod 777 %s' % (path))

                filename = request.user.username + '_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.xls'
                exresult = generate_excel(Cargo_infor, path + '/' + filename)
                if exresult['code'] == 0:
                    os.popen(r'chmod 777 %s' % (path + '/' + filename))
                    upload_to_oss_obj = upload_to_oss(BUCKETNAME_overseas_warehouse_cargo_infor_xls)
                    uploadresult = upload_to_oss_obj.upload_to_oss(
                        {'path': request.user.username, 'name': filename, 'byte': open(path + '/' + filename), 'del': 1})

                    if uploadresult['result'] != '':
                        objs.update(Delivery_lot_number=The_lot_number, Delivery_status='already',genBatchMan=request.user.first_name,genBatchTime=datetime.datetime.now())

                        t_shipping_management.objects.create(Stocking_plan_number='|'.join(myplan),
                                                             Cargo_infor=uploadresult['result'],
                                                             Delivery_lot_number=The_lot_number,
                                                             Destination_warehouse=warehouselist[0],OplogTime=datetime.datetime.now(),
                                                             Status='notyet', All_ProductSKU_Num=';'.join(myproductinfo))
                    else:
                        messages.error(request, u'导出失败！请稍后 重试。。。')
                else:
                    messages.error(request, u'导出失败！请稍后 重试。。。%s' % exresult['error'])
    except Exception as e:
        messages.error(request, '针对FBW生成批次报错:%s，请联系IT查看原因。'%(str(e)))

    return HttpResponseRedirect('/Project/admin/skuapp/t_set_warehouse_storage_situation_list')

def t_product_up_down_delay(request):
    idx = request.GET['id']
    add_date = request.GET['add_date']
    SKU = request.GET['SKU']
    rt = u'<form action="/delay/day">延期天数(必须为整数)：<input name="day_obj" type="text" value=""></input><input type="hidden" name="add_date" value="%s"></input><input type="hidden" name="idx" value="%s" /><input type="hidden" name="SKU" value="%s" />&nbsp;<input type="button" id="tt" value="提交" /><script> var idx=parent.layer.getFrameIndex(window.name);document.getElementById("tt").setAttribute("type", "submit"); function sub_sub(){document.getElementById("sub_form").submit();parent.layer.close(idx);} </script> </form>'%(add_date,idx,SKU)
    return render(request, 'SKU.html', {'rt': rt})
    
def delay_day(request):
    import datetime
    from brick.classredis.classsku import classsku
    from django_redis import get_redis_connection
    redis_coon = get_redis_connection(alias='product')
    classsku_obj = classsku(db_cnxn=connection, redis_cnxn=redis_coon)

    id = request.GET.get("idx")
    day_obj = request.GET.get("day_obj")
    add_date = request.GET.get("add_date")
    SKU = request.GET.get("SKU")
    add_date = datetime.datetime.strptime(add_date,'%Y-%m-%d %H:%M:%S')
    #messages.error(request,'111---%s'%add_date)
    try:
        add_date = add_date + datetime.timedelta(days = int(day_obj))
    except:
        messages.error(request,'延期天数非空,并且为整数！')
    #messages.error(request,'yyyyyy---%s'%day_obj)
    #messages.error(request,'xxxxxx---%s'%add_date)
    xgmss = u'延期%s天,预计%s重新上架'%(day_obj,add_date)
    current_status = classsku_obj.get_goodsstatus_by_sku(sku=SKU)
    xgms = {SKU: {'GoodsStatus': [u'当前状态', current_status, u'临时下架', xgmss, u'临时下架']}}
    id_max = int(t_product_information_modify.objects.filter(InputBox__contains=SKU).latest('id').id)
    m_obj = t_product_information_modify.objects.filter(id=id_max).values('InputBox','MainSKU','SQStaffNameing','SKU','Name2','DevDate','SourcePicPath2')
    t_product_information_modify.objects.create(Mstatus='DLQ',SQTimeing=datetime.datetime.now(),MainSKU=m_obj[0]['MainSKU'],InputBox=m_obj[0]['InputBox'],SKU=m_obj[0]['SKU'],Select='2',SQStaffNameing=m_obj[0]['SQStaffNameing'],Name2=m_obj[0]['Name2'],DevDate=m_obj[0]['DevDate'],SourcePicPath2=m_obj[0]['SourcePicPath2'],Details=xgms,XGcontext='')
    t_product_up_down.objects.filter(id=id).update(Add_Date = add_date,sum=F('sum')+1)
    return render(request, 'SKU.html')
    
def PB(request):
    from skuapp.table.t_wish_pb import *
    ProductID = request.GET['pb']
    rt='<table   style="text-align:center;" border="1" cellpadding="3" cellspacing="1" bgcolor="#c1c1c1"><th style="text-align:center"><p align="center">时间/费用/销售额</p></th>'
    pb_objs = t_wish_pb.objects.filter(ProductID = ProductID).values_list('Duration','PbFee','PbCount')
    for pb_obj in pb_objs:
        rt = u'%s<tr><td nowrap><font color="red">%s/%s/%s</font></td></tr>'%(rt,pb_obj[0][6:10]+'-'+pb_obj[0][0:5].replace('/','-'),pb_obj[1],pb_obj[2])
    rt = "%s</table>"%rt

    return render(request, 'PB.html', {'rt':rt})
def SKUB(request):
    from skuapp.table.t_product_b_goods_all_productsku import *
    MainSKU_tmp = request.GET['abc']
    rt = '<table  style="text-align:center" border="1" cellpadding="1" cellspacing="1" bgcolor="#FFFAF0">' \
         '<tr bgcolor="#C00"><th style="text-align:center" width=100px>&nbsp&nbspSKU&nbsp&nbsp</th><th style="text-align:center" width=100px>' \
         '属性</th><th style="text-align:center">单价</th>' \
         '<th style="text-align:center" width=250px>包装规格</th>' \
         '<th style="text-align:center">内包装成本</th><th style="text-align:center">最小包装数</th>' \
         '<th style="text-align:center">服装类信息</th><th style="text-align:center">商品状态</th></tr>'
    t_product_b_goods_all_productsku_objs = t_product_b_goods_all_productsku.objects.filter(MainSKU=MainSKU_tmp)
    for t_product_b_goods_all_productsku_obj in t_product_b_goods_all_productsku_objs:
        rt = '%s <tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr> ' \
             % (rt, t_product_b_goods_all_productsku_obj.SKU, t_product_b_goods_all_productsku_obj.GoodsName,
                t_product_b_goods_all_productsku_obj.RetailPrice,
                t_product_b_goods_all_productsku_obj.PackName, t_product_b_goods_all_productsku_obj.PackFee,
                t_product_b_goods_all_productsku_obj.PackageCount, t_product_b_goods_all_productsku_obj.Style,
                t_product_b_goods_all_productsku_obj.GoodsStatus)

    rt = '%s</table>' % rt
    return render(request, 'SKU.html', {'rt': rt})
    

def ebay_result_SKU(request):
    from skuapp.table.t_templet_ebay_upload_result import t_templet_ebay_upload_result
    
    id = request.GET['abc']
    rt='<table   style="text-align:center;" border="1" cellpadding="3" cellspacing="1" bgcolor="#c1c1c1"><tr bgcolor="#C00"><th style="text-align:center">商品SKU</th><th style="text-align:center">店铺SKU</th></tr>'
    t_templet_ebay_upload_result_objs = t_templet_ebay_upload_result.objects.values('product_sku','shopsku').filter(id=id).distinct()
    #messages.error(request,'*&*&*&$#@@@##%s'%t_templet_ebay_upload_result_objs)
    new_sku = t_templet_ebay_upload_result_objs[0]
    sku = ""
    shop_sku = ""
    try:
        sku = eval(str(new_sku['product_sku']).replace("`","'"))
        #messages.error(request,'#$#$%s'%sku)
        shop_sku = eval(str(new_sku['shopsku']).replace("`","'"))
        #messages.error(request, '#$#$%s' % shop_sku)
    except:
        messages.error(request,u'----------=-=-=出错了！')
        pass
        
    for i in range(len(sku)):
        rt = '%s <tr bgcolor="#FFFFFF"><td>%s</td><td>%s</td></tr> '%(rt,sku[i],shop_sku[i])
    rt = "%s</table>"%rt
    return render(request, 'SKU.html', {'rt':rt})
    
    
    
    
    
    
    

def shopSKU(request):
    MainSKU_tmp = request.GET['aID']
    SKU_tmp = []
    db_conn = MySQLdb.Connect(DATABASES['syn']['HOST'], DATABASES['syn']['USER'],
                              DATABASES['syn']['PASSWORD'], DATABASES['syn']['NAME'])
    if db_conn:
        cursor = db_conn.cursor()
        from skuapp.table.t_product_mainsku_sku import *
        t_product_mainsku_sku_objs = t_product_mainsku_sku.objects.filter(MainSKU=MainSKU_tmp)
        for t_product_mainsku_sku_obj in t_product_mainsku_sku_objs:
            SKU_tmp.append(t_product_mainsku_sku_obj.ProductSKU)
        rt = '<table style="text-align:center" border="1" cellpadding="3" cellspacing="1" bgcolor="#FFFAF0">' \
             '<tr bgcolor="#C00"><th style="text-align:center">店铺SKU</th><th style="text-align:center">' \
             '备注</th><th style="text-align:center">销售员</th></tr>'
        for sku_obj in SKU_tmp:
            sql = "select ShopSKU,Memo,PersonCode from b_goodsskulinkshop WHERE SKU = '%s'" % sku_obj
            cursor.execute(sql)
            ShopSKUTmp = cursor.fetchall()
            for ShopSKUTmp_obj in ShopSKUTmp:
                rt = '%s <tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (rt, ShopSKUTmp_obj[0], ShopSKUTmp_obj[1], ShopSKUTmp_obj[2])
        rt = '%s</table>' % rt
        if cursor:
            cursor.close()
        db_conn.close()

    return render(request, 'SKU.html', {'rt':rt})

def ebay_SKU(request):
    itemid = request.GET['abc']
    rt='<table   style="text-align:center;" border="1" cellpadding="3" cellspacing="1" bgcolor="#c1c1c1"><tr bgcolor="#C00"><th style="text-align:center">子SKU</th><th style="text-align:center">价格</th></tr>'
    t_online_info_ebay_subsku_objs = t_online_info_ebay_subsku.objects.filter(itemid=itemid)
    for t_online_info_ebay_subsku_obj in t_online_info_ebay_subsku_objs:
        rt = '%s <tr bgcolor="#FFFFFF"><td>%s</td><td>%s</td></tr> '%(rt,t_online_info_ebay_subsku_obj.subSKU,t_online_info_ebay_subsku_obj.startprice)
    rt = "%s</table>"%rt

    return render(request, 'ebay_SKU.html', {'rt':rt})
    
def aliexpress_info(request):
    MainSKU = request.GET['SKU']
    rt='<table   style="text-align:center;" border="1" cellpadding="3" cellspacing="1" bgcolor="#c1c1c1"><tr bgcolor="#C00"><th style="text-align:center">店铺名称</th><th style="text-align:center">产品ID</th></tr>'
    t_online_info_objs = t_online_info.objects.filter(MainSKU=MainSKU).distinct()
    for t_online_info_obj in t_online_info_objs:
        rt = '%s <tr bgcolor="#FFFFFF"><td>%s</td><td>%s</td></tr> '%(rt,t_online_info_obj.ShopName,t_online_info_obj.ProductID)
    rt = "%s</table>"%rt

    return render(request, 'aliexpress_info.html', {'rt':rt})
    
def Z_KC(request):
    #from pyapp.models import b_goods as py_b_goods
    from pyapp.models import kc_currentstock
    
    InputBox = request.GET['KID']
    InputBox_list = InputBox.split(',')
    #messages.error(request,"InputBox_list==%s"%InputBox_list)
    rt = '<table style="text-align:center"><tr><th style="text-align:center">商品编码</th><th style="text-align:center">月销售量-</th><th style="text-align:center">可用库存量</th></tr>'
    for InputBox_l in InputBox_list:
        b_goods_objs = py_b_goods.objects.filter(SKU=InputBox_l)
        if b_goods_objs.exists() :
            #for b_goods_obj in b_goods_objs:
            kc_currentstock_objs = kc_currentstock.objects.filter(GoodsID = b_goods_objs[0].NID)
            if kc_currentstock_objs.exists() :
                for kc_currentstock_obj in kc_currentstock_objs:
                    rt = '%s <tr><td>%s</td><td>%s</td><td>%s</td></tr> '%(rt,InputBox_l,kc_currentstock_obj.SellCount3,kc_currentstock_obj.Number-kc_currentstock_obj.ReservationNum)
    
    rt = '%s</table>'%rt
       
    return render(request, 'SKU.html', {'rt':rt})
    
def show_rank(request):
    from skuapp.table.t_config_apiurl_asin_rank_history import t_config_apiurl_asin_rank_history
    ASIN =  request.GET['ASIN']
    categories = []
    series = []
    rt=''
    t_config_apiurl_asin_rank_history_objs = t_config_apiurl_asin_rank_history.objects.filter(ASIN=ASIN)
    if t_config_apiurl_asin_rank_history_objs.exists():
        for t_config_apiurl_asin_rank_history_obj in t_config_apiurl_asin_rank_history_objs:
            RefreshTime = u'%s'%t_config_apiurl_asin_rank_history_obj.RefreshTime.strftime('%Y%m%d')
            categories.append(int(RefreshTime))
            series.append(int(t_config_apiurl_asin_rank_history_obj.Rank))
        categories.reverse()
        series.reverse()
    else:
        rt = '<span>抱歉！没有该ASIN的历史记录！</span>'
        
    return render(request, 'show_rank.html', {'rt':rt,'categories':categories,'series':series})
    
def wish_calculate(request):
    from skuapp.table.B_PackInfo   import B_PackInfo as skuapp_B_PackInfo
    from skuapp.table.t_sys_param import t_sys_param as t_sys_param1
    
    PackNID = request.GET['PackNID']
    ID      = request.GET['ID']
    Weight = 0
    Cost = 0
    
    t_product_mainsku_sku_objs = t_product_mainsku_sku.objects.filter(id = ID,PackNID=PackNID)
    if t_product_mainsku_sku_objs.exists():
        Weight = t_product_mainsku_sku_objs[0].Weight
        Cost = t_product_mainsku_sku_objs[0].UnitPrice
    B_packinfo_objs = skuapp_B_PackInfo.objects.filter(id=PackNID)
    
    AllWeight=0
    AllCost=0
    if B_packinfo_objs.exists():
        AllCost=float(B_packinfo_objs[0].CostPrice)+float(Cost)
        AllWeight=float(B_packinfo_objs[0].Weight)+float(Weight)
    else:
        AllWeight=Weight
        AllCost=Cost
    
     
    ExchangeRate=0
    ExchangeRate_obj=t_sys_param.objects.values('V','VDesc').filter(Type=40).order_by('Seq')
    if ExchangeRate_obj.exists():
        for ExRate_obj in ExchangeRate_obj:
            if ExRate_obj['VDesc']==u'wish平台默认美元汇率':
                ExchangeRate=ExRate_obj['V']
                
    ProfitRate=0
    ProfitRate_obj=t_sys_param.objects.values('V','VDesc').filter(Type=39).order_by('Seq')
    if ProfitRate_obj.exists():
        for PfitRate_obj in ProfitRate_obj:
            if PfitRate_obj['VDesc']==u'wish平台默认利润率':
                ProfitRate=PfitRate_obj['V']
                
        Dollar = 0.0
        if 0<AllWeight and AllWeight<300:
            Dollar=(float(AllWeight)*0.1*0.85+float(AllCost))*100/float(ExchangeRate)/(1-float(ProfitRate)/100-0.06-0.1)
        elif AllWeight is not None:
            Dollar=((float(AllWeight)*0.1+8)*0.8+float(AllCost))*100/float(ExchangeRate)/(1-float(ProfitRate)/100-0.06-0.1)
        
        product_cost = Cost 
        product_weight=Weight            
        product_Dollar = 0.0
        if 0<product_weight and product_weight<300:
            product_Dollar=(float(product_weight)*0.1*0.85+float(product_cost))*100/float(ExchangeRate)/(1-float(ProfitRate)/100-0.06-0.1)
        elif product_weight is not None:
            product_Dollar=((float(product_weight)*0.1+8)*0.8+float(product_cost))*100/float(ExchangeRate)/(1-float(ProfitRate)/100-0.06-0.1)
                
    return render(request,'t_wish_calculate.html',{'AllWeight':AllWeight,'AllCost':AllCost,'ProductWeight':Weight,'ProductCost':Cost,'ExchangeRate':ExchangeRate,'ProfitRate':ProfitRate,'Dollar':Dollar,'product_Dollar':product_Dollar})


def search_sku_Plugin(request):
    try:
        from datetime import datetime
        MainSKU = request.POST.get('MainSKU','')
        SalerName2 = request.user.first_name
        CreateDate = datetime.now()
        if MainSKU == '':
            messages.error(request,'商品编码不能为空')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            listProducts = []
            from skuapp.table.t_product_mainsku_sku import t_product_mainsku_sku
            objProducts = t_product_mainsku_sku.objects.filter(MainSKU=MainSKU).values_list('ProductSKU')
            listProducts = [obj[0] for obj in objProducts]
            if len(listProducts) == 0 and MainSKU != '':
                listProducts.append(MainSKU)
            if len(listProducts) > 0:
                objs = py_b_goods.objects.filter(SKU__in = listProducts)
                number = len(objs)
                temp = []
                for i in range(number):
                    name = 'a' + str(i)
                    temp.append(name)

                tempList = []
                for j in range(number):
                    temp[j] = {}
                    temp[j]['MainSKU'] = objs[j].SKU
                    temp[j]['price'] = objs[j].CostPrice
                    tempList.append(temp[j])
                    SalerName2 = objs[0].SalerName2
                    CreateDate = objs[0].CreateDate
            else:
                messages.error(request, '主SKU=%s在t_product_mainsku_sku表未查到到对应的商品SKU。'%(MainSKU))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    except Exception as e:
        messages.error(request,u'通过主SKU查找商品SKU失败,error=%s'%(str(e)))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return render(request,'search_sku_Plugin.html',{'objs':tempList,'num':1,'SalerName2':SalerName2,'CreateDate':CreateDate})
    
    
def search_sku_save(request):
    from datetime import datetime
    from pyapp.models import b_goodscats as py_b_goodscats

    if request.method == 'POST':
        MainSKUList = request.POST.getlist('MainSKU')
        allGoodsSKU = ','.join(MainSKUList)
       
        XGcontext =  request.POST.get('XGcontext','')
        SalerName2 =  request.POST.get('SalerName2','')
        CreateDate =  request.POST.get('CreateDate','')
        Select = request.POST.get('Select','')
    
        UnitPriceList =  request.POST.getlist('UnitPrice')
        NowPriceList =  request.POST.getlist('NowPrice')


        oldprice = ','.join(UnitPriceList)
        newprice = ','.join(NowPriceList)

        if Select.strip() != '':
            b_goods_objs = py_b_goods.objects.filter(SKU__in=MainSKUList)
          
            if b_goods_objs.exists() :
                obj = t_product_information_modify()
                obj.SKU = b_goods_objs[0].SKU #子SKU
                obj.Name2     = b_goods_objs[0].GoodsName #商品名称
                obj.Keywords  = b_goods_objs[0].AliasEnName #英文关键词
                obj.Keywords2 = b_goods_objs[0].AliasCnName #中文关键词
                obj.SourcePicPath2  = u'http://fancyqube.net:89/ShopElf/images/%s.jpg'%b_goods_objs[0].SKU.replace('OAS-','').replace('FBA-','')
                obj.Material  = b_goods_objs[0].Material #材质
                obj.DevDate  = b_goods_objs[0].DevDate
                obj.XGcontext  = XGcontext
                obj.InputBox  = allGoodsSKU

                goodscat = b_goods_objs[0].CategoryCode.split('|')  # 类别code

                obj.LargeCategory = None
                obj.SmallCategory = None
                if len(goodscat) >= 3:
                    py_b_goodscats_objs = py_b_goodscats.objects.filter(CategoryCode='|'.join(goodscat))
                    if py_b_goodscats_objs.exists():
                        if goodscat[2].strip() != '':
                            obj.LargeCategory = py_b_goodscats_objs[0].CategoryParentName
                            obj.SmallCategory = py_b_goodscats_objs[0].CategoryName
                        else:
                            obj.LargeCategory = py_b_goodscats_objs[0].CategoryName

                obj.SQTimeing      =  datetime.now()
                obj.SQStaffNameing =  request.user.first_name
                obj.Source         =  u'普源信息'
                if Select in ['4',]:
                    obj.oldvalue      = oldprice
                    obj.newvalue       = newprice
                
                if Select in ['1',]:

                    obj.Mstatus = 'DHT' #待换图
                    from skuapp.modelsadminx.t_product_Admin import t_product_Admin
                    t_product_Admin_obj = t_product_Admin()
                    
                    # 插入 领取美工 步骤
                    t_product_develop_ed_obj = t_product_develop_ed.objects.create(id=t_product_Admin_obj.get_id(),MGProcess  = '5',MainSKU = obj.InputBox,SKU = b_goods_objs[0].SKU,
                                                        Name2 = b_goods_objs[0].GoodsName,Keywords = b_goods_objs[0].AliasEnName,
                                                        Keywords2 = b_goods_objs[0].AliasCnName,
                                                        SourcePicPath2 = u'http://fancyqube.net:89/ShopElf/images/%s.jpg'%b_goods_objs[0].SKU.replace('OAS-','').replace('FBA-',''),
                                                        UnitPrice = b_goods_objs[0].CostPrice,Material = b_goods_objs[0].Material,
                                                        PictureRequest = XGcontext,JZLStaffName = SalerName2,JZLTime=CreateDate)
                    
                    t_product_oplog.objects.create(pid=t_product_develop_ed_obj.id,MainSKU=obj.InputBox,Name = b_goods_objs[0].GoodsName,
                                                   Name2 = b_goods_objs[0].GoodsName,OpID=request.user.username,OpName=request.user.first_name,
                                                   StepID=u'DHT',StepName='去换图',BeginTime=datetime.now())

                if Select in ['2','3','8','11','12','17']:
                    obj.Mstatus = 'DLQ'  #待领取
                

                if Select in ['4','5','6','7','9','10','13', '14', '15', '16', '18']:
                    obj.Mstatus = 'DSH' #待审核
                
                obj.Select = Select
                obj.save()
                if len(MainSKUList) >= 1:
                    mainsku_objs = t_product_mainsku_sku.objects.filter(ProductSKU=MainSKUList[0]).values_list('MainSKU')
                    if mainsku_objs.exists():
                        obj.MainSKU = mainsku_objs[0][0]
                        obj.save()
        
        else:
            messages.error(request,u'出错了')

        return HttpResponseRedirect('/Project/admin/skuapp/t_product_information_modify/')


        
    
    
def button_Plugin(request):
    sku = request.POST.get('GoodsSKU','')
    if sku=='':
        messages.error(request,'SKU不能为空')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        objs = py_b_goods.objects.filter(SKU__contains=sku)
        number = len(objs)
        temp = []
        for i in range(number):
            name = 'a' + str(i)
            temp.append(name)
        # 动态创建字典名称，并将全部字典添加到同一个列表中，列表返回到指定的HTML页面
        tempList = []
        for j in range(number):
            temp[j] = {}
            temp[j]['SKU'] = objs[j].SKU
            temp[j]['price'] = objs[j].CostPrice
            temp[j]['weight'] = objs[j].Weight

            ID = objs[j].SupplierID
            b_supplier_objs = sku_b_supplier.objects.filter(NID=ID)
            if b_supplier_objs.exists():
                temp[j]['supplier'] = b_supplier_objs[0].SupplierName
            else:
                temp[j]['supplier'] = '不存在'
            # if objs[j].Notes == 1:
            #     temp[j]['URL'] = '不存在'
            # else:
                # url = re.findall(r'[a-zA-Z0-9//-?!.+]',objs[j].Notes.split('https')[-1])
                # temp[j]['URL'] = 'https' + ''.join(url)
            temp[j]['URL'] = objs[j].Notes
            tempList.append(temp[j])
    return render(request, 'button_Plugin.html', {'objs': tempList,'num':1})

def button_save(request):
    from datetime import datetime
    post = request.POST
    SKUList = post.getlist('SKU')
    oldpriceList = post.getlist('oldprice')
    nowpriceList = post.getlist('nowprice')
    oldsupplierList = post.getlist('oldsupplier')
    newsupplierList = post.getlist('newsupplier')
    oldsupplierURLList = post.getlist('oldsupplierURL')
    newsupplierURLList = post.getlist('newsupplierURL')
    remarkList = post.getlist('remark')
    oldweightList = post.getlist('oldweight')
    nowweightList = post.getlist('nowweight')


    userName = request.user.first_name
    time = datetime.now()
    for i in range(len(SKUList)):
        notes = py_b_goods.objects.filter(SKU=SKUList[i])[0].Notes
        content = notes + '\n\t' + newsupplierURLList[i]
        try:
            oldprice = float(oldpriceList[i])
        except Exception:
            oldprice = None
        try:
            nowprice= float(nowpriceList[i])
        except Exception:
            nowprice = oldprice

        check_obj = t_product_price_check.objects.filter(GoodsSKU=SKUList[i])

        if (nowprice != oldprice) or (nowweightList[i] != ''):
            # 判断是否重复（两个标准，确定现价和克重均不重复才可以插入）
            if check_obj.exists():
                for each in check_obj:
                    try:
                        if nowprice == float(each.NowPrice) and nowweightList[i] == each.NowWeight and each.Mstatus in (u'在修改', u'待修改'):
                            flag = 0
                            break
                        else:
                            flag = 1
                    except:
                        flag = 1
            else:
                flag = 1

            if flag == 1:
                if nowprice == None:
                    nowprice = oldprice
                percent = '%.2f%%' % ((nowprice - oldprice) / oldprice * 100)
                t_product_price_check.objects.create(GoodsSKU=SKUList[i], GoodsCode=SKUList[i], SQStaffName=userName,
                                                     SQTime=time,
                                                     Mstatus='待修改', OldPrice=oldprice, PricePercent=percent,
                                                     NowPrice=nowprice, NowWeight=nowweightList[i],
                                                     OldWeight=oldweightList[i],
                                                     OldSupplier=oldsupplierList[i],
                                                     OldSupplierURL=oldsupplierURLList[i],
                                                     NewSupplier=newsupplierList[i],
                                                     NewSupplierURL=newsupplierURLList[i],
                                                     XGcontext=content, remarks2=remarkList[i])
    return HttpResponseRedirect('/Project/admin/skuapp/t_product_price_check/')

def paypalSave(request):
    post = request.POST
    Account = post.get('select-payout', '')
    Payout_Account = post.get('select-paypal', '')
    t_paypal_account = t_config_paypal_account.objects.filter(Paypal_Account=Payout_Account)
    if (len(t_paypal_account) > 0) and (t_paypal_account[0] != ''):
        receipt_accounts = str(request.POST).split(':')[-1][1:-3].split(',')
        if len(receipt_accounts) > 0 and receipt_accounts[0] != '':
            for receipt_account in receipt_accounts:
                receipt = receipt_account[3:-1]
                if len(receipt) > 0:
                    params = {'Paypal_Account': Payout_Account, 'Buyer_Id': receipt, 'Payout_Account': str(Account)}
                    t_api_schedule_ing_obj = t_api_schedule_ing()
                    t_api_schedule_ing_obj.ShopName = 'ShopName'
                    t_api_schedule_ing_obj.PlatformName = 'Paypal'
                    t_api_schedule_ing_obj.CMDID = 'payout'
                    t_api_schedule_ing_obj.ScheduleTime = datetime.now()
                    t_api_schedule_ing_obj.Status = '0'
                    t_api_schedule_ing_obj.InsertTime = datetime.now()
                    t_api_schedule_ing_obj.UpdateTime = datetime.now()
                    t_api_schedule_ing_obj.Timedelta = 30
                    t_api_schedule_ing_obj.RetryCount = 0
                    t_api_schedule_ing_obj.Processed = 0
                    t_api_schedule_ing_obj.Successful = 0
                    t_api_schedule_ing_obj.WithError = 0
                    t_api_schedule_ing_obj.WithWarning = 0
                    t_api_schedule_ing_obj.Params = params
                    t_api_schedule_ing_obj.save()

                else:
                    messages.error(request, 'there is not any buyer account selected!')
        else:
            messages.error(request, 'there is not any buyer account selected!')
    else:
        messages.error(request, 'the paypal account should be selected!')
    return HttpResponseRedirect('/Project/admin/skuapp/t_paypal_payout_log/')


def add_Secondary_research(request):
    from skuapp.table.t_product_depart_get import t_product_depart_get
    #logger = logging.getLogger('sourceDns.webdns.views')#'{'Wish':'http:','Wish':'http:','Wish':'http:','Wish':'http:',}'
    sites = t_sys_param.objects.filter(Type=302).order_by('Seq')
    newSites = {}
    for site in sites:
        newSites[site.V] = ''
    #URLwish
    id = request.GET.get('id','')
    t_product_depart_get_objs = t_product_depart_get.objects.filter(id = id)
    if t_product_depart_get_objs.exists():
        Secondary_research = t_product_depart_get_objs[0].URLwish
        if Secondary_research is not None and Secondary_research.strip() != '':
            URLwish_json = eval(Secondary_research)
            if isinstance(URLwish_json,dict):
                for k,v in URLwish_json.items():
                    newSites[k] = v
                return render(request, 'Secondary_research.html', {'sites': newSites,'id':id})
            else:
                return render(request, 'Secondary_research.html', {'sites': newSites,'id':id})
        else:
            return render(request, 'Secondary_research.html', {'sites': newSites,'id':id})
    
def add_Secondary_research_result(request):
    from skuapp.table.t_product_depart_get import t_product_depart_get
    logger = logging.getLogger('sourceDns.webdns.views')
    if request.method == 'POST':
        sites = t_sys_param.objects.filter(Type=302).order_by('Seq')
        params = {}
        for site in sites:
            name = request.POST.get(site.V + '_URL_value','')
            if name is not None and name.strip() != '':
                siteKey = site.V
                params[siteKey] = name
        id = request.POST.get('id','')
        logger.error("--------------ddd==%s"%(params))
        t_product_depart_get.objects.filter(id = id).update(URLwish = params)
        rt = u'修改成功!'
    return render(request, 'result.html', {'rt': rt})
    
def add_Remarks(request):
    from skuapp.table.t_config_apiurl_asin_xprx import t_config_apiurl_asin_xprx
    #logger = logging.getLogger('sourceDns.webdns.views')#'{'Wish':'http:','Wish':'http:','Wish':'http:','Wish':'http:',}'

    #URLwish
    id = request.GET.get('id','')
    t_config_apiurl_asin_xprx_objs = t_config_apiurl_asin_xprx.objects.filter(id = id)
    if t_config_apiurl_asin_xprx_objs.exists():
        Remarks = t_config_apiurl_asin_xprx_objs[0].Remarks
        if Remarks is not None and Remarks.strip() != '':
            return render(request, 'Remarks.html', {'id':id})
        else:
            return render(request, 'Remarks.html', {'id':id})
    
def add_Remarks_result(request):
    from datetime import datetime 
    from django.db.models import F
    from skuapp.table.t_config_apiurl_asin_xprx import t_config_apiurl_asin_xprx
    from skuapp.table.t_config_apiurl_asin_operation import t_config_apiurl_asin_operation
    if request.method == 'POST':
        name = request.POST.get('_URL_value','')
        if name is not None and name.strip() != '':
            Remarks = name
            dealname =request.user.first_name
            dealtime = datetime.now()
            dealstatus ='alreadyprocessed'
        id = request.POST.get('id','')
        t_config_apiurl_asin_xprx_objs = t_config_apiurl_asin_xprx.objects.filter(id = id)
        if t_config_apiurl_asin_xprx_objs[0].DealName is not None and t_config_apiurl_asin_xprx_objs[0].DealName !=request.user.first_name :
            messages.error(request, '该产品已经被人处理了！请换另一个产品处理')
            rt =u'添加失败!'
        else:
            t_config_apiurl_asin_xprx.objects.filter(id = id).update(Remarks = Remarks)
            t_config_apiurl_asin_xprx.objects.filter(id = id).update(DealName = dealname)
            t_config_apiurl_asin_xprx.objects.filter(id = id).update(DealTime = dealtime)
            t_config_apiurl_asin_xprx.objects.filter(id = id).update(dealStatus = dealstatus)
            rt = u'添加成功!'
            b = t_config_apiurl_asin_operation.objects.filter(OperationMan=request.user.first_name,OperationWeek=datetime.now().strftime('%Y%W'))
            if b.exists() :
                t_config_apiurl_asin_operation.objects.filter(OperationMan=request.user.first_name,OperationWeek=datetime.now().strftime('%Y%W')).update(Handled=F('Handled')+1)                
            else :
                t_config_apiurl_asin_operation.objects.filter().create(Developed=0,Repeation=0,Handled=1,OperationMan=request.user.first_name,OperationWeek=datetime.now().strftime('%Y%W'))

    return render(request, 'result.html', {'rt': rt})
    
def wish_change(request):

    wishID = request.GET['abc']
    store_temp_obj = store_temp.objects.filter(NID=wishID)

    # 取出所有副图
    store_obj = t_distribution_product_to_store.objects.filter(id=wishID)
    if store_obj.exists():
        extarImage = store_obj[0].ExtraImages
        if extarImage == None:
            imageList = []
        else:
            imageList = extarImage.split('|')
    else:
        imageList = []

    if store_temp_obj.exists():
        shopName = store_temp_obj[0].ShopName
        result = store_temp.objects.filter(NID=wishID,ShopName=shopName).order_by('oldPrice','Quantity')
        reList = []
        for each in result:
            reDict = {}
            reDict['SKU'] = each.SKU
            reDict['ShopSKU'] = each.ShopSKU
            number = 1
            if each.ShopSKU.find('*') != -1:
                number = each.ShopSKU.split('*')[-1]
            reDict['number'] = number
            reDict['Quantity'] = each.Quantity
            reDict['Price'] = each.Price
            reDict['Status'] = each.Status
            reDict['msrp'] = each.msrp
            reDict['ShippingTime'] = each.ShippingTime
            reDict['Shipping'] = each.Shipping
            reDict['oldPrice'] = each.oldPrice
            reDict['color'] = each.Color
            reDict['size'] = each.Size
            VariationImage = each.VariationImage
            if VariationImage == None:
                VariationImage = ''
            reDict['VariationImage'] = VariationImage

            # SKU在普源售卖状态
            st = py_b_goods.objects.filter(SKU=each.SKU)
            if st.exists():
                st = st[0].GoodsStatus
            else:
                st = u'未知'
            reDict['sonStatus'] = st
            reList.append(reDict)
    else:
        reList = []

    return render(request, 'wish_change.html',{'result':reList,'nid':wishID,'imageList':imageList})

def get_shopName(shopname):
    shopcode = re.findall(r'[0-9]',shopname)
    code = ''.join(shopcode)
    new_shopname = 'Wish-%s'%(code.zfill(4))
    return new_shopname
    
def get_parent_SKU(ShopName):
    from skuapp.table.t_ShopName_ParentSKU import t_ShopName_ParentSKU
    t_ShopName_ParentSKU_ParentSKU_objs = t_ShopName_ParentSKU.objects.values('ParentSKU').filter(ShopName=ShopName)
    if t_ShopName_ParentSKU_ParentSKU_objs.exists():
        Parent_SKU_list = re.split(r'(\d+)', t_ShopName_ParentSKU_ParentSKU_objs[0]['ParentSKU'])
        Parent_SKU = u'%s%s' % (
            Parent_SKU_list[0], str(int(Parent_SKU_list[1]) + 1).zfill(len(Parent_SKU_list[1])))

        t_ShopName_ParentSKU.objects.filter(ShopName=ShopName).update(ParentSKU=Parent_SKU)

    elif not t_ShopName_ParentSKU_ParentSKU_objs.exists():
        t_online_info_ParentSKUs = t_online_info.objects.values('ParentSKU').filter(ShopName=ShopName[0:9])
        if t_online_info_ParentSKUs.exists():
            ParentSKU_head = []
            ParentSKU_list = []
            for t_online_info_ParentSKU in t_online_info_ParentSKUs:
                ParentSKU_l = re.split(r'(\d+)', t_online_info_ParentSKU['ParentSKU'])
                if len(ParentSKU_l) >= 2:
                    ParentSKU_head.append(ParentSKU_l[0])
                    ParentSKU_list.append(int(str(int(ParentSKU_l[1]) + 1).zfill(len(ParentSKU_l[1]))))
                else:
                    ParentSKU_head.append(t_online_info_ParentSKU['ParentSKU'])
                    ParentSKU_list.append('00001')
            Parent_SKU = u'%s%s%s' % (random.sample(set(ParentSKU_head), 1)[0], 'A', max(ParentSKU_list))

        elif not t_online_info_ParentSKUs.exists():

            # Parent_SKU = u'%sA0001' % ShopName[10:14].upper()
            randChar = ''
            for i in range(4):
                randChar += random.choice(string.ascii_uppercase)
            randNum = str(random.randint(100000, 999999))
            Parent_SKU = u'%s%s' % (randChar, randNum)

        t_ShopName_ParentSKU_objs = t_ShopName_ParentSKU()
        t_ShopName_ParentSKU_objs.ShopName = ShopName
        t_ShopName_ParentSKU_objs.ParentSKU = Parent_SKU
        t_ShopName_ParentSKU_objs.save()
    return Parent_SKU
    
def get_shopSKU(Parent_SKU, SKU, number, num):
    ShopSKU = u'%s%d' % (Parent_SKU, number)
    t_online_info_ShopSKU_list_f = re.split(r'(\d+)', SKU)
    for i in range(2, len(t_online_info_ShopSKU_list_f)):
        ShopSKU = u'%s%s' % (ShopSKU, t_online_info_ShopSKU_list_f[i])
    logger.error("ShopSKU===================%s" % (ShopSKU))
    if int(num) > 1:
        ShopSKU = ShopSKU + '*' + num
    return ShopSKU
    
def wish_save(request):
    post = request.POST
    NID = post.get('nid')
    to_store_obj = t_distribution_product_to_store.objects.filter(id=NID)
    if to_store_obj.exists():
        type = to_store_obj[0].Type
        if type == None:
            rt = u'请先选择铺货类型再提交，或点击"关闭页面"退出！'
        else:
            sonsku = post.getlist('sonsku')
            quantity = post.getlist('quantity')
            price = post.getlist('price')
            status = post.getlist('status')
            msrp = post.getlist('msrp')
            time = post.getlist('time')
            shipping = post.getlist('shipping')
            oldprice = post.getlist('oldprice')
            imgURL = post.getlist('imgURL')
            color = post.getlist('color')
            size = post.getlist('size')
            sonST = post.getlist('sonST')
            shopsku = post.getlist('shopsku')
            number = post.getlist('number')

            store_temp_objs =  store_temp.objects.filter(NID=NID)

            productID = store_temp_objs[0].ProductID # 可能没用
            shopNameList = []
            info = {}
            for each in store_temp_objs:
                if each.ShopName not in shopNameList:
                    shopNameList.append(each.ShopName)
                    info[each.ShopName] = each.ParentSKU
                # each.DeleteFlag = '1'
                # each.save()
            store_temp_objs.exclude(SKU__in=sonsku).delete()
            for eachName in shopNameList:
                parentSKU = get_parent_SKU(eachName)
                for i in range(0,len(sonsku)):
                    if price[i] == '':
                        Price = 1
                    else:
                        Price = price[i]

                    if msrp[i] == '':
                        Msrp = 1
                    else:
                        Msrp = msrp[i]

                    if shipping[i] == '':
                        Shipping = 1
                    else:
                        Shipping = shipping[i]

                    if oldprice[i] == '':
                        Oldprice = 1
                    else:
                        Oldprice = oldprice[i]

                    if quantity[i] == '':
                        Quantity = 9999
                    else:
                        Quantity = quantity[i]

                    if time[i] == '':
                        shippingtime = '7-21'
                    else:
                        shippingtime = time[i]
                    
                    ShopSKU = get_shopSKU(parentSKU,sonsku[i],i,number[i])
                    
                    # store_temp.objects.create(NID=NID,ShopName=eachName,ShopSKU=shopsku[i],Price=Price,
                                              # msrp=Msrp, Status=status[i],VariationImage=imgURL[i],
                                              # Quantity=Quantity, ShippingTime=shippingtime, Shipping=Shipping,
                                              # oldPrice=Oldprice,Size=size[i], Color=color[i],
                                              # ProductID=productID,SKU=sonsku[i],ParentSKU=parentSKU)

                    update_date={'ShopSKU':ShopSKU,'Price':Price,'msrp':Msrp,'Status':status[i],'VariationImage':imgURL[i],
                                'Quantity':Quantity,'ShippingTime':shippingtime,'Shipping':Shipping,
                                'oldPrice':Oldprice,'Size':size[i], 'Color':color[i],'NID':NID,'ShopName':eachName,
                                'ProductID':productID,'SKU':sonsku[i],'ParentSKU':parentSKU}
                    
                    store_temp_objs.update_or_create(SKU = sonsku[i],ShopName=eachName,Color=color[i],Size=size[i],
                                            defaults= update_date
                                            )

            rt = u'修改成功！'
    return render(request, 'SKU.html', {'rt':rt})
'''    
def import_joom(request):
    number = int(request.GET['num'])
    logger = logging.getLogger('sourceDns.webdns.views')
    
    mainSKU_list = []
    t_online_info_wait_publish_objs = t_online_info_wait_publish.objects.all()
    #logger.error("t_online_info_wait_publish_objs ============%s"%(t_online_info_wait_publish_objs))
    for t_online_info_wait_publish_obj in t_online_info_wait_publish_objs:
        mainSKU_list.append(t_online_info_wait_publish_obj.MainSKU)
    #logger.error("mainSKU_list ============%s"%(mainSKU_list))
    nub = t_online_info_wish.objects.exclude(MainSKU__in=mainSKU_list)
    if nub.count() >= number:
        objs = nub[0:number]
        #logger.error("objs ============%s"%(len(objs)))
            
    else:
        objs = nub
    #logger.error("nub.count() ============%s"%(nub.count()))
    insertinto = []
    ProductID_list_obls=[]
    mainSKU_list_obls = []
    
    for i in range(0,number):
        if objs[i].MainSKU not in mainSKU_list_obls and objs[i].MainSKU is not None and objs[i].MainSKU.strip() != '' and objs[i].SKU is not None:
            skuStatus = ''
            for SKU_l in objs[i].SKU.split(','):
                if SKU_l.strip() != '':
                    b_goods_objs = py_b_goods.objects.filter(SKU=SKU_l)
                    if b_goods_objs.exists():
                        goodsStatus = b_goods_objs[0].GoodsStatus
                        if (goodsStatus == u'正常') or (goodsStatus == u'在售'):
                            skuStatus = u'正常'
                            
            if skuStatus == u'正常':
                #logger.error("i---------------------%s"%i)
                #logger.error("objs[i]---------------------%s"%objs[i])
                mainSKU_list_obls.append(objs[i].MainSKU)
                ProductID_list_obls.append(objs[i].ProductID)
                insertinto.append(t_online_info_wait_publish(
                    PlatformName   =  objs[i].PlatformName,
                    ProductID      =  objs[i].ProductID,
                    ShopIP         =  objs[i].ShopIP,
                    ShopName       =  objs[i].ShopName,
                    Title          =  objs[i].Title,
                    SKU            =  objs[i].SKU,
                    ShopSKU        =  objs[i].ShopSKU,
                    Price          =  objs[i].Price,
                    Quantity       =  objs[i].Quantity,
                    Orders7Days    =  objs[i].Orders7Days,
                    SoldYesterday  =  objs[i].SoldYesterday,
                    SoldTheDay     =  objs[i].SoldTheDay,
                    SoldXXX        =  objs[i].SoldXXX,
                    DateOfOrder    =  objs[i].DateOfOrder,
                    Remarks        =  objs[i].Remarks,
                    RefreshTime    =  objs[i].RefreshTime,
                    Image          =  objs[i].Image,
                    Status         =  objs[i].Status,
                    ReviewState    =  objs[i].ReviewState,
                    DateUploaded   =  objs[i].DateUploaded,
                    LastUpdated    =  objs[i].LastUpdated,
                    OfSales        =  objs[i].OfSales,
                    ParentSKU      =  objs[i].ParentSKU,
                    Seller         =  objs[i].Seller,
                    ispublished    =  u'未刊登',
                    MainSKU        =  objs[i].MainSKU
                    ))
        else:
            continue
            
    t_online_info_wait_publish.objects.bulk_create(insertinto)
    #logger.error("insertinto============%s"%(insertinto))
    #logger.error("mainSKU_list_obls============%s"%(mainSKU_list_obls))
    t_online_info_objs = t_online_info.objects.filter(ProductID__in=ProductID_list_obls)
    for t_online_info_obj in t_online_info_objs:
        t_online_info_publish_joom_obj = t_online_info_publish_joom()
        t_online_info_publish_joom_obj.__dict__ = t_online_info_obj.__dict__
        t_online_info_publish_joom_obj.save()

    return HttpResponseRedirect('/Project/admin/skuapp/t_online_info_wait_publish/')
'''    
logger = logging.getLogger('sourceDns.webdns.views')    #刚才在setting.py中配置的logger
def get_Price(Price):
    new_Price = 0.00
    if Price is not None and Price.strip() != '':
        Price_list = re.findall('[0-9.]',Price)
        new_Price_tmp = ''
        for Price_l in Price_list:
            new_Price_tmp = '%s%s'%(new_Price_tmp,Price_l)
        new_Price = float(new_Price_tmp)
    
    return new_Price

def to_wish_store(request):
    from skuapp.table.t_distribution_product_to_store import t_distribution_product_to_store
    from skuapp.table.t_distribution_product_to_store_temp import t_distribution_product_to_store_temp
    if request.method == 'POST':
        id = request.POST.get('id','')
        shopname = request.POST.get('shopname','')
        ProductID = request.POST.get('ProductID','')
        #插入temp
        objs = t_online_info.objects.filter(ProductID=ProductID)
        new_shopname_list = []
        new_shopname_str = ''
        if shopname.strip() != '':
            for shopcode in shopname.split(','):
                new_shopname = u'Wish-%s'%(shopcode.zfill(4))
                if shopcode in new_shopname_list:
                    continue
                else:
                    #new_shopname_str = u'%s%s,'%(new_shopname_str,shopcode)
                    new_shopname_list.append(shopcode)
                    logger.error("-------------shopName:%s"%new_shopname)
                    nub = t_distribution_product_to_store_temp.objects.filter(NID=id,ShopName=new_shopname).count()
                    if nub<=0:
                        insert_into_temp = []
                        for obj in objs:
                            Price = get_Price(obj.Price)
                            Shipping = get_Price(obj.Shipping)
                            msrp = get_Price(obj.msrp)
                            if msrp == 0.00:
                                msrp = (Price + Shipping) * 3
                            logger.error("-------------Price:%s-------------Shipping:%s-------------msrp:%s"%(Price,Shipping,msrp))
                            insert_into_temp.append(t_distribution_product_to_store_temp(
                                NID=id,ProductID=ProductID,SKU=obj.SKU,ShopSKU=obj.ShopSKU,
                                Status=obj.Status,Price=Price,Quantity=obj.Quantity,
                                ParentSKU=obj.ParentSKU,msrp=msrp,oldPrice=Price,
                                Color=obj.Color,Size=obj.Size,Shipping=Shipping,
                                ShippingTime=obj.ShippingTime,ShopName=new_shopname
                            ))
                        t_distribution_product_to_store_temp.objects.bulk_create(insert_into_temp)
            t_distribution_product_to_store.objects.filter(id = id).update(csvShop1= ",".join(new_shopname_list)) #修改铺货目标店铺
            rt = u'修改成功!'
        else:   
            rt = u'铺货目标店铺,不可为空。请重新填写!'
        return render(request, 'result.html', {'rt': rt})
    else:
        id = request.GET.get('id','')
        ShopName_all = ''
        ProductID = ''
        t_distribution_product_to_store_objs = t_distribution_product_to_store.objects.filter(id = id)
        if t_distribution_product_to_store_objs.exists():
            ShopName_all = t_distribution_product_to_store_objs[0].csvShop1
            ProductID = t_distribution_product_to_store_objs[0].ProductID
        return render(request, 'update_upload_product_to_wish_shopname.html', {'ShopName_all':ShopName_all,'id':id,'ProductID':ProductID})
    
    
def shelves_search(request):
    from urllib import urlencode
    #urlencode({'_p_group1__exact':obj.group1,'_p_group2__exact':obj.group2})
    parem = {}
    rt = '?'
    url = ''
    if request.method == 'POST':
    
        shopname = request.POST.get('ShopName','')
        if shopname.strip() != '':
            shopname_list = re.findall(r'[0-9]', shopname)
            shopcode = ''.join(shopname_list)
            new_shopname = 'Wish-%s'%(shopcode.zfill(4))
            parem['_p_ShopName__exact'] = new_shopname.strip()

        productsku = request.POST.get('SKU','')
        if productsku.strip() != '':
            parem['_p_SKU__exact'] = productsku.strip()
            
        MainSKU = request.POST.get('MainSKU','')
        if MainSKU.strip() != '':
            parem['_p_MainSKU__exact'] = MainSKU.strip()
            
        GoodsStatus = request.POST.get('GoodsStatus','')
        if GoodsStatus.strip() != '' and GoodsStatus != 'all':
            parem['_p_GoodsStatus'] = GoodsStatus.strip()
            
        APIState = request.POST.get('APIState','') 
        if APIState and APIState != 'all':
            parem['_p_APIState__exact'] = APIState.strip()
            
        Orders7Days_Start = request.POST.get('Orders7Days_gte','')
        if Orders7Days_Start.strip() != '':
            parem['_p_Orders7Days__gte'] = Orders7Days_Start.strip()

        Orders7Days_End = request.POST.get('Orders7Days_lt','')
        if Orders7Days_End.strip() != '':
            parem['_p_Orders7Days__lt'] = Orders7Days_End.strip()
            
        OfSales_Start = request.POST.get('OfSales_gte','')
        if OfSales_Start.strip() != '':
            parem['_p_OfSales__gte'] = OfSales_Start.strip()

        OfSales_End = request.POST.get('OfSales_lt','')
        if OfSales_End.strip() != '':
            parem['_p_OfSales__lt'] = OfSales_End.strip()
            
        url = request.POST.get('url','')
            
    if not parem:
        rt = ''
    rt = u'%s%s%s'%(url,rt,urlencode(parem))
    return HttpResponseRedirect(rt)

    
def get_api_ing_objs_by_ID(obj):
    from skuapp.table.t_api_schedule_ing import t_api_schedule_ing
    api_objs = []
    apiingid = obj['apiingid']
    if apiingid is not None and apiingid.strip() != '':
        for apiid in apiingid.split(','):
            id_list = apiid.split('-')
            resultid=''
            api_ing_objs = t_api_schedule_ing.objects.filter(id=id_list[0]).values('id','ShopName','ScheduleTime')
            if len(id_list)>1 :
                resultid = id_list[1]
            ing_objs = {}
            if api_ing_objs.exists():
                ing_objs['id']           = api_ing_objs[0]['id']
                ing_objs['ShopName']     = api_ing_objs[0]['ShopName']
                ing_objs['ScheduleTime'] = api_ing_objs[0]['ScheduleTime']
                ing_objs['resultid']     = resultid
            if ing_objs and ing_objs not in api_objs:
                api_objs.append(ing_objs)
    return api_objs
    
def upload_Implementation_plan(request):
    import datetime as datime
    api_objs = []
    id = request.GET.get('getapiingid','')
    objs = t_distribution_product_to_store.objects.filter(id = id).values('apiingid')
    if objs.exists():
        api_objs = get_api_ing_objs_by_ID(objs[0])
    if request.method == 'POST':
        APID = request.POST.getlist('smell_ID')
        logger.error('................%s'%(api_objs))
        for api_obj in api_objs:
            logger.error('%s.................%s'%(api_obj['id'],APID))
            if str(api_obj['id']) in APID: # param['product'].pop('productSKU')
                # logger.error('%s'%(api_obj['id']))
                t_distribution_product_to_store_result.objects.filter(id=api_obj['resultid']).update(Status='cancel')
                t_api_schedule_ing.objects.filter(id=api_obj['id']).delete()
                api_objs.remove(api_obj)

    api_ing_objs = api_objs

    return render(request, 'api_instruction_execution_plan.html', {'objs':api_ing_objs,'id':id})

import hashlib
def calcsign(request_data,appKey):
    keyset = sorted(request_data.keys())
    signdata = ''
    for i in range(0, len(keyset)):
        signdata = signdata + keyset[i] + '=' + str(request_data[keyset[i]])
    signdata += 'Key=' + appKey
    m = hashlib.md5()
    m.update(signdata)
    psw = m.hexdigest()
    signature = psw.upper()
    return signature

import decimal
def applyPostTrackInfo(t_order_amazon_india_obje,t_shop_amazon_india_obj,t_order_item_amazon_india_objs,dealData):
    url = 'http://120.78.88.110:9090/service/parser'
    timeStamp = int(time.time() * 1000)
    appKey = '6dd8a3d04db5430c9ab1eebe6373b82d'
    appId = '07AADCF1662M1ZH'
    t_order_amazon_india_obj = t_order_amazon_india_obje[0]
    allDV = 0
    goodsToStr = ''
    pweight = 0
    trasationUSD = decimal.Decimal("%.2f" % float(6.6))
    decimal.getcontext().prec = 2
    for t_order_item_amazon_india_obj in t_order_item_amazon_india_objs:
        aliasCnName = t_order_item_amazon_india_obj.AliasCnName
        aliasEnName = t_order_item_amazon_india_obj.AliasEnName
        cargoClass = 1
        if t_order_item_amazon_india_obj.IsCharged == '1':
            cargoClass = 3
        if t_order_item_amazon_india_obj.IsPowder == '1':
            cargoClass = 10
        if t_order_item_amazon_india_obj.IsLiquid == '1':
            cargoClass = 9
        if t_order_item_amazon_india_obj.isMagnetism == '1':
            cargoClass = 5
        for k in dealData['aliasCnNames']:
            if k==str(t_order_item_amazon_india_obj.id):
                aliasCnName = dealData['aliasCnNames'][k]
                aliasEnName = dealData['aliasEnNames'][k]
        dv = t_order_item_amazon_india_obj.CostPrice/trasationUSD
        allDV += dv
        goodsCount = 1
        SellerSKUList = [t_order_item_amazon_india_obj.SellerSKU,]
        if '+' in t_order_item_amazon_india_obj.SellerSKU:
            SellerSKUList = t_order_item_amazon_india_obj.SellerSKU.split('+')
        for sellerSKU in SellerSKUList:
            if t_order_item_amazon_india_obj.ShopSKU in sellerSKU:
                if '*' in sellerSKU:
                    goodsCount = int(sellerSKU.split('*')[1])

        # if '*' in t_order_item_amazon_india_obj.SellerSKU:
        #     goodsCount = int(t_order_item_amazon_india_obj.SellerSKU.split('*')[1])
        # elif '+' in t_order_item_amazon_india_obj.SellerSKU:
        #     goodsCount = len(t_order_item_amazon_india_obj.SellerSKU.split('+'))
        pweight += t_order_item_amazon_india_obj.PackWeight+(t_order_item_amazon_india_obj.Weight * goodsCount)
        goodsToStr += '{"CnName":"'+aliasCnName + '","EnName":"' + aliasEnName + '","Description":"","Unit":'+ \
                '"PCS","Sku":"' + t_order_item_amazon_india_obj.SKU + '","Quantity":'+str(t_order_item_amazon_india_obj.QuantityOrdered)+\
                ',"DeclaredValue":"'+str(dv)+'","DeclareCurrency":"USD","Origin":"CN","CargoClass":'+str(cargoClass)+',"HsCode":""},'
    shipAddressLine2 = ''
    if t_order_amazon_india_obj.shipAddressLine2 is not None:
        shipAddressLine2 = t_order_amazon_india_obj.shipAddressLine2
    pweight = pweight/1000
    pweight = decimal.Decimal("%.2f" % pweight)

    CustomerRef = t_order_amazon_india_obj.AmazonOrderId
    if dealData['trackTime'] != 'first':
        CustomerRef += '_2'

    toMD5Data1 = '{"CustomerRef":"'+CustomerRef+'","ServiceCode":"'+dealData['track_server']+'","ConType":2,"ReturnWay":1,"TradeTerms":"FOB",' \
                 '"CustomerOrderID":"","CodAmount":"0","DomesticExp":"","ReturnLabelData":0,"TrackNumber":"","DepotCode":"SZX","ImportGateway":"","Notes":"'
    toMD5Data2 = '","DeclaredValue":"'+str(allDV)+'","DeclareCurrency":"USD","HsCode":"","InsuranceVal":"0","InsuranceCur":"","LabelType":"URL","ShipFrom":' \
                 '{"Name":"'+t_shop_amazon_india_obj.ShopUserName+'","PostCode":"'+t_shop_amazon_india_obj.PostCode+'","Phone":{"Tel":"'+t_shop_amazon_india_obj.UserPhoneTel+ \
                '"},"Mobile":"'+t_shop_amazon_india_obj.Mobile+'","Email":"'+t_shop_amazon_india_obj.Email+'","CountryCode":"'+t_shop_amazon_india_obj.CountryCode+ \
                '","Company":"'+t_shop_amazon_india_obj.Company+'","Address":"'+t_shop_amazon_india_obj.UserAdress+'","Province":"'+t_shop_amazon_india_obj.Province+ \
                '","City":"'+t_shop_amazon_india_obj.City+'"},"ShipTo":{"Name":"'+t_order_amazon_india_obj.shipName+ \
                '","PostCode":"'+t_order_amazon_india_obj.shipPostalCode+'","Phone":{"Tel":""},"Mobile":"'+t_order_amazon_india_obj.shipPhone+ \
                '","Email":"'+t_order_amazon_india_obj.BuyerEmail+'","CountryCode":"'+t_order_amazon_india_obj.shipCountryCode+'","Company":"'+t_order_amazon_india_obj.shipName+'",'+ \
                '"Address":"'+t_order_amazon_india_obj.shipAddressLine1+', '+shipAddressLine2+'","Province":"'+t_order_amazon_india_obj.shipStateOrRegion+'",'+ \
                '"City":"'+t_order_amazon_india_obj.shipCity+'"},"Goods":['+goodsToStr[:-1]+'],"Packages":[{"CustomerPkgRef":"","PackingType":"2","Weight":"'+str(pweight)+'","Quantity":'
    toMD5Data3 = ',"Dimension":{"L":"0.000","W":"0.000","H":"0.000","U":"M"}}]}'

    request_data = {"AppId": appId, "TimeStamp": timeStamp, "RequestName": "submitShipment",
                   "Content":toMD5Data1+dealData['order_notes']+toMD5Data2+dealData['pQuantity']+toMD5Data3}
    tosignature = {"AppId": appId, "TimeStamp": timeStamp}
    signature = calcsign(tosignature, appKey)
    request_data['Sign'] = signature
    request_str = '{"AppId":"'+request_data['AppId']+'","TimeStamp":"'+str(request_data['TimeStamp'])+'","RequestName":"submitShipment","Content":'+request_data['Content']+\
                    ',"Sign":"'+signature+'"}||'+url

    t_order_amazon_india_obje.update(DeclaredValue=allDV, DeclareCurrency='USD')

    return request_str


def applyTrack(request):
    post = request.GET
    order_id = post.get('order_id', '')
    shopName = post.get('shopname','')
    trackTime = post.get('trackTime','')
    t_order_amazon_india_obj = t_order_amazon_india.objects.filter(id=order_id)[0]
    t_shop_amazon_india_obj = t_shop_amazon_india.objects.filter(ShopName=shopName)[0]
    AmazonOrderId = t_order_amazon_india_obj.AmazonOrderId
    t_order_item_amazon_india_objs = t_order_item_amazon_india.objects.filter(AmazonOrderId=AmazonOrderId)
    toiaios=[]
    tsFlag = '0'
    num = 0
    for t_order_item_amazon_india_obj in t_order_item_amazon_india_objs:
        toiaio = {}
        num += 1
        goods_amount = t_order_item_amazon_india_obj.ItemPrice + t_order_item_amazon_india_obj.ItemTax
        goods_amount = decimal.Decimal("%.2f" % goods_amount)
        IsCharged='未绑定SKU'
        if t_order_item_amazon_india_obj.IsCharged == '1':
            tsFlag = '1'
            IsCharged = '是'
        elif t_order_item_amazon_india_obj.IsCharged == '0':
            IsCharged = '否'

        toiaio['goods_amount'] = str(goods_amount) + t_order_item_amazon_india_obj.CurrencyCode
        toiaio['IsCharged'] = IsCharged
        toiaio['SKU'] = t_order_item_amazon_india_obj.SKU
        toiaio['QuantityOrdered'] = t_order_item_amazon_india_obj.QuantityOrdered
        toiaio['id'] = t_order_item_amazon_india_obj.id
        toiaio['AliasCnName'] = t_order_item_amazon_india_obj.AliasCnName
        toiaio['AliasEnName'] = t_order_item_amazon_india_obj.AliasEnName
        toiaio['InvoiceRequirement'] = t_order_item_amazon_india_obj.InvoiceRequirement
        toiaios.append(toiaio)

    # track_server = ''
    if tsFlag == '1':
        track_server = 'INWPX-BAT'
    else:
        track_server = 'INWPX'

    canTrack = '0'
    for toiaio in toiaios:
        if toiaio['IsCharged'] == '未绑定SKU':
            canTrack = '1'

    # toPostdict = applyPostTrackInfo(t_order_amazon_india_obj,t_shop_amazon_india_obj,t_order_item_amazon_india_objs,track_server)

    #t_order_amazon_india_obj.s()
    turl = '/Project/admin/skuapp/t_order_amazon_india/apply_track_comfir/?_p_ShopName__exact='+shopName
    return render(request, 't_order_amazon_indiaPlugin.html', {'t_order_amazon_india_obj': t_order_amazon_india_obj,
                                                              't_shop_amazon_india_obj': t_shop_amazon_india_obj,'trackTime':trackTime,
                                                               'toiaios': toiaios, 'canTrack': canTrack, 'num': num,
                                                               'id': order_id, 'turl': turl, 'track_server': track_server})

def applyTrackComfir(request):
    from app_djcelery.tasks import get_trackno_amazon_india
    post = request.GET
    order_id = post.get('order_id','')
    shopName = post.get('shopname','')
    track_server = post.get('track_server','')
    order_notes = post.get('order_notes','')
    pQuantity = post.get('pQuantity', '')
    aliasCnNames = post.get('aliasCnNames', '')
    aliasEnNames = post.get('aliasEnNames', '')
    trackTime = post.get('trackTime','')
    dealData = {"track_server":track_server,"order_notes":order_notes,"pQuantity":pQuantity,
                "aliasCnNames": eval(aliasCnNames),"aliasEnNames":eval(aliasEnNames),"trackTime":trackTime}
    t_order_amazon_india_obj = t_order_amazon_india.objects.filter(id=order_id)
    t_shop_amazon_india_obj = t_shop_amazon_india.objects.filter(ShopName=shopName)[0]
    AmazonOrderId = t_order_amazon_india_obj[0].AmazonOrderId
    t_order_item_amazon_india_objs = t_order_item_amazon_india.objects.filter(AmazonOrderId=AmazonOrderId)
    request_str = applyPostTrackInfo(t_order_amazon_india_obj, t_shop_amazon_india_obj, t_order_item_amazon_india_objs,
                                     dealData)

    request_str += '||'+order_id

    # t_amazon_schedule_ing_obj = t_amazon_schedule_ing()
    # t_amazon_schedule_ing_obj.ShopName = shopName
    # t_amazon_schedule_ing_obj.PlatformName = 'Amazon'
    # t_amazon_schedule_ing_obj.CMDID = 'apply_track_number'
    # t_amazon_schedule_ing_obj.ScheduleTime = datetime.now()
    # t_amazon_schedule_ing_obj.Status = '0'
    # t_amazon_schedule_ing_obj.InsertTime = datetime.now()
    # t_amazon_schedule_ing_obj.UpdateTime = datetime.now()
    # t_amazon_schedule_ing_obj.Timedelta = 90
    # t_amazon_schedule_ing_obj.RetryCount = 0
    # t_amazon_schedule_ing_obj.Processed = 0
    # t_amazon_schedule_ing_obj.Successful = 0
    # t_amazon_schedule_ing_obj.WithError = 0
    # t_amazon_schedule_ing_obj.WithWarning = 0
    # t_amazon_schedule_ing_obj.Params = request_str
    # t_amazon_schedule_ing_obj.save()
    # get_trackno_amazon_india.delay(connection, request_str)

    t_order_amazon_india_obj.update(applyTracking='1',dealTime=datetime.datetime.now(),dealUser=request.user.username,dealAction='apply track number',applyTrackNoTime=datetime.datetime.now())

    result_code = {}
    if request_str:
        result_code = get_trackno_amazon_india.delay([request_str])
    print result_code

    toiaios = []
    for t_order_item_amazon_india_obj in t_order_item_amazon_india_objs:
        toiaio = {}
        goods_amount = t_order_item_amazon_india_obj.ItemPrice + t_order_item_amazon_india_obj.ItemTax
        goods_amount = decimal.Decimal("%.2f" % goods_amount)
        IsCharged = '未绑定SKU'
        if t_order_item_amazon_india_obj.IsCharged == '1':
            IsCharged = '是'
        elif t_order_item_amazon_india_obj.IsCharged == '0':
            IsCharged = '否'

        toiaio['goods_amount'] = str(goods_amount) + t_order_item_amazon_india_obj.CurrencyCode
        toiaio['IsCharged'] = IsCharged
        toiaio['SKU'] = t_order_item_amazon_india_obj.SKU
        toiaio['QuantityOrdered'] = t_order_item_amazon_india_obj.QuantityOrdered
        toiaio['InvoiceRequirement'] = t_order_item_amazon_india_obj.InvoiceRequirement
        toiaios.append(toiaio)
    turl = '/Project/admin/skuapp/t_order_amazon_india/?_p_ShopName__exact=' + shopName
    return render(request, 't_order_amazon_india_track.html', {'t_order_amazon_india_obj': t_order_amazon_india_obj[0],
                                                               'toiaios': toiaios, 'turl': turl,'toPostdict':request_str})

def trackInfo(request):
    from datetime import datetime 
    post = request.GET
    order_id = post.get('order_id', '')
    shopName = post.get('shopname', '')
    t_order_track_info_amazon_india_obj = t_order_track_info_amazon_india.objects.filter(id=order_id)[0]
    track_info = t_order_track_info_amazon_india_obj.track_info
    new_track_info = []
    if track_info:
        deal_track_infos = track_info[1:-1].replace('},','}||').split('||')
        for deal_track_info in deal_track_infos:
            if deal_track_info:
                deal_track_info = eval(deal_track_info)
            else:
                deal_track_info = {}
                deal_track_info['DateTime'] = datetime.now()
                deal_track_info['Place'] = u'暂无物流信息'
                deal_track_info['Info'] = u'未发货'
            new_track_info.append(deal_track_info)
    else:
        deal_track_info = {}
        deal_track_info['DateTime'] = datetime.now()
        deal_track_info['Place'] = u'暂无物流信息'
        deal_track_info['Info'] = u'未发货'
        new_track_info.append(deal_track_info)
    # t_order_amazon_india_obj.s()

    turl = '/Project/admin/skuapp/t_order_amazon_india/?_p_ShopName__exact=' + shopName
    return render(request, 't_order_amazon_india_trackInfo.html', {'t_order_track_info_amazon_india_obj': t_order_track_info_amazon_india_obj,
                                                                   'track_info': new_track_info, 'turl': turl})

def local2utc(local_st):
    import datetime
    """本地时间转UTC时间（-8:00）"""
    time_struct = time.mktime(local_st.timetuple())
    utc_st = datetime.datetime.utcfromtimestamp(time_struct)
    return utc_st

def feedAmazon(request):
    import datetime
    post = request.GET
    order_id = post.get('order_id', '')
    shopName = post.get('shopname', '')
    trackId = post.get('trackId', '')
    t_order_amazon_india_obj = t_order_amazon_india.objects.filter(id=order_id)
    t_order_track_info_amazon_india_obj = t_order_track_info_amazon_india.objects.filter(id=trackId)[0]
    track_info = t_order_track_info_amazon_india_obj.track_info
    textStr = 'Check In Scan'
    deal_track_infos = eval(track_info)
    track_date = ''
    for deal_track_info in deal_track_infos:
        if deal_track_info:
            if textStr in deal_track_info['Info']:
                track_date = deal_track_info['DateTime']+":00"
                date_time = datetime.datetime.strptime(track_date, '%Y-%m-%d %H:%M:%S')
                # date_time = date_time + datetime.timedelta(days=-1)
                utc_tran = local2utc(date_time).strftime("%Y-%m-%dT%H:%M:%SZ")
                track_date = str(utc_tran)
    if track_date == '':
        lastShipDate = t_order_amazon_india_obj[0].LatestShipDate
        if lastShipDate:
            date_time = datetime.datetime.strptime(lastShipDate, '%Y-%m-%dT%H:%M:%SZ')
            date_time = date_time + datetime.timedelta(hours=-6)
            utc_tran = local2utc(date_time).strftime("%Y-%m-%dT%H:%M:%SZ")
            track_date = str(utc_tran)
    trackNo = t_order_track_info_amazon_india_obj.trackNumber
    track_company = "Delhivery"
    if trackNo.find('EQ9') == 0:
        track_company = "India Post"
    if trackNo.find('22') == 0 and len(trackNo) == 9:
        track_company = "ECOM EXPRESS"
    request_str = '{"track_date": "%s", "track_company": "%s", "track_num": "%s", "AmazonOrderId": "%s", "shopName": "%s"}'%(track_date, track_company, trackNo, t_order_amazon_india_obj[0].AmazonOrderId, shopName)

    t_amazon_schedule_ing_obj = t_amazon_schedule_ing()
    t_amazon_schedule_ing_obj.ShopName = shopName
    t_amazon_schedule_ing_obj.PlatformName = 'Amazon'
    t_amazon_schedule_ing_obj.CMDID = 'amazon_feed_track'
    t_amazon_schedule_ing_obj.ScheduleTime = datetime.datetime.now()
    t_amazon_schedule_ing_obj.Status = '0'
    t_amazon_schedule_ing_obj.InsertTime = datetime.datetime.now()
    t_amazon_schedule_ing_obj.UpdateTime = datetime.datetime.now()
    t_amazon_schedule_ing_obj.Timedelta = 5
    t_amazon_schedule_ing_obj.RetryCount = 0
    t_amazon_schedule_ing_obj.Processed = 0
    t_amazon_schedule_ing_obj.Successful = 0
    t_amazon_schedule_ing_obj.WithError = 0
    t_amazon_schedule_ing_obj.WithWarning = 0
    t_amazon_schedule_ing_obj.Params = request_str
    t_amazon_schedule_ing_obj.save()

    t_order_amazon_india_obj.update(is_sure_feed=1,dealTime=datetime.datetime.now(),dealUser=request.user.username,dealAction='feed amazon')
    delParams = ['order_id','trackId', 'shopname']
    url_Stitching_obj = url_Stitching(request)
    postStr = url_Stitching_obj.reStitching_url(delParams,{},{})
    turl = '/Project/admin/skuapp/t_order_amazon_india/'+postStr.replace('/','%2F')
    return HttpResponseRedirect(turl)
    
def feedTrack(request):
    post = request.GET
    order_id = post.get('order_id', '')
    shopName = post.get('shopname', '')
    t_order_amazon_india_obj = t_order_amazon_india.objects.filter(id=order_id)
    AmazonOrderId = t_order_amazon_india_obj[0].AmazonOrderId
    turl = '/Project/admin/skuapp/t_order_amazon_india/feed_track_comfir/?_p_ShopName__exact=' + shopName
    return render(request, 't_order_feed_track_amazon_india.html', {'AmazonOrderId': AmazonOrderId,
                                                               'order_id': order_id, 'turl': turl})
    
def feedTrackComfir(request):
    from datetime import datetime
    post = request.GET
    order_id = post.get('order_id', '')
    AmazonOrderId = post.get('AmazonOrderId', '')
    trackNumber = post.get('trackNumber', '')
    track_service = post.get('track_service', '')
    t_order_amazon_india_obj = t_order_amazon_india.objects.filter(id=order_id)
    t_order_track_info_amazon_india_obj = t_order_track_info_amazon_india()
    t_order_track_info_amazon_india_obj.AmazonOrderId = AmazonOrderId
    t_order_track_info_amazon_india_obj.trackNumber = trackNumber
    t_order_track_info_amazon_india_obj.track_service = track_service
    t_order_track_info_amazon_india_obj.track_company = 'gati'
    t_order_track_info_amazon_india_obj.UpdateTime = datetime.now()
    t_order_track_info_amazon_india_obj.save()

    t_order_amazon_india_obj.update(applyTracking='1',dealTime=datetime.now(),dealUser=request.user.username,dealAction='apply track number',dealResult='Success')
    return render(request, 't_order_feed_track_comfir_amazon_india.html', {'AmazonOrderId': AmazonOrderId,
                                                                    'trackNumber': trackNumber, 'track_service': track_service})
def char_process(param):
    if param == None:
        result = ''
    else:
        result = param.replace('"', '`').replace("'", '`')

    result = result.replace("&#39;", "'").replace("&amp;", "&").replace("\\/", '/').replace("&quot;", '`')
    return result


def create_wish_collection_box(request):
    """生成WISH采集箱"""
    # from pyapp.models import b_goodsskulinkshop
    # from table.t_product_mainsku_sku import t_product_mainsku_sku
    from skuapp.table.t_online_info import t_online_info
    from skuapp.table.t_online_info_wish import t_online_info_wish
    from datetime import datetime
    from brick.classredis.classsku import classsku
    classsku_obj = classsku()

    productID = request.GET.get('productID', '')
    MainSKU = request.GET.get('mainsku', '')
    plate = request.GET.get('plate', '')

    if MainSKU == 'None':
        messages.info(request, '--------------------商品SKU未绑定！！！')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    elif ',' in MainSKU:
        messages.info(request, '--------------------组合链接不支持铺货！！！')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    if plate == '':
        collection_box_objs = t_templet_wish_collection_box.objects.filter(MainSKU=MainSKU)
    else:
        collection_box_objs = t_templet_joom_collection_box.objects.filter(MainSKU=MainSKU)

    if collection_box_objs.exists():
        messages.error(request, '请勿重复采集MainSKU:%s' % MainSKU)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    online_info_objs = t_online_info.objects.filter(ProductID=productID).extra(select={'price':'Price+0'}).order_by('price')
    if online_info_objs.exists():
        Title = char_process(online_info_objs[0].Title)
        Description = char_process(online_info_objs[0].Description)
        Tags = char_process(online_info_objs[0].Tags)
        MainImage = online_info_objs[0].Image
        ExtraImages = online_info_objs[0].ExtraImages
        SrcProductID = online_info_objs[0].ProductID

        # 变体信息
        Variants = []
        # 普源SKU对应商品状态
        sku_state = {}
        # 克重、成本价, 数据格式是[{sku:{'cost_price':CostPrice, 'weight':Weight}}, ……]
        b_cost_weight = []

        for obj in online_info_objs:
            Variant = {}
            VariantDict = {}

            sku = obj.SKU
            st = classsku_obj.get_goodsstatus_by_sku(sku=sku)
            sku_state[sku] = st
            if plate == 'joom':
                cost_weight = {'cost_price': str(classsku_obj.get_price_by_sku(sku=sku)),
                               'weight': str(classsku_obj.get_weight_by_sku(sku=sku))
                               }
                sku_cost_weight = {sku: cost_weight}
                b_cost_weight.append(sku_cost_weight)

            VariantDict['sku'] = obj.ShopSKU
            VariantDict['productSKU'] = obj.SKU
            if obj.ShopSKUImage is None:
                VariantDict['main_image'] = ''
            else:
                VariantDict['main_image'] = obj.ShopSKUImage.replace('\\', '')
            VariantDict['color'] = char_process(obj.Color)
            VariantDict['size'] = char_process(obj.Size)
            VariantDict['price'] = float(obj.Price)
            VariantDict['shipping'] = float(obj.Shipping)
            VariantDict['inventory'] = '9999'
            VariantDict['msrp'] = obj.msrp
            VariantDict['shipping_time'] = '7-25'
            VariantDict['format'] = 'json'
            VariantDict['parent_sku'] = ''
            # if (obj.Status == 'Enabled') and st in ('正常', '在售'):
            if obj.Status == 'Enabled':
                enabled = True
            else:
                enabled = False
            VariantDict['enabled'] = enabled

            Variant['Variant'] = VariantDict
            Variants.append(Variant)
        time = datetime.now()
        user = request.user.first_name

        if plate == '':
            t_templet_wish_collection_box.objects.create(MainSKU=MainSKU, Title=Title, Description=Description,
                                                 Tags=Tags, MainImage=MainImage, ExtraImages=ExtraImages,
                                                 Variants=Variants, CreateTime=time, CreateStaff=user, Status='0',
                                                 UpdateTime=time, UpdateStaff=user, SrcProductID=SrcProductID,
                                                         SkuState=sku_state)
        else:
            t_templet_joom_collection_box.objects.create(MainSKU=MainSKU, Title=Title, Description=Description,
                                                 Tags=Tags, MainImage=MainImage, ExtraImages=ExtraImages, B_cost_weight=b_cost_weight,
                                                 Variants=Variants, CreateTime=time, CreateStaff=user, Status='0', Source='COLLECT',
                                                 UpdateTime=time, UpdateStaff=user, SrcProductID=SrcProductID, SkuState=sku_state)
        messages.info(request, 'MainSKU: %s采集成功' % MainSKU)
    else:
        messages.info(request, '--------------------未选择商品！')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def show_wish_variant(request):
    """展示采集箱变种信息"""
    from skuapp.table.t_templet_wish_collection_box import t_templet_wish_collection_box
    from skuapp.table.t_templet_public_wish_review import t_templet_public_wish_review
    from skuapp.table.t_templet_public_wish import t_templet_public_wish
    from skuapp.table.t_templet_wish_wait_upload import t_templet_wish_wait_upload
    from skuapp.table.t_templet_wish_upload_review import t_templet_wish_upload_review
    from skuapp.table.t_templet_joom_collection_box import t_templet_joom_collection_box
    from skuapp.table.t_templet_public_joom import t_templet_public_joom
    from skuapp.table.t_templet_joom_wait_upload import t_templet_joom_wait_upload
    from base64 import urlsafe_b64encode
    from django.db import connection
    from django_redis import get_redis_connection
    redis_coon = get_redis_connection(alias='product')
    from brick.classredis.classsku import classsku
    classsku_obj = classsku(connection, redis_coon)

    id = request.GET.get('id', '')
    page = request.GET.get('page', '')
    plateform = request.GET.get('plateform', '')

    platefrom_page_table_dict = {
        'wish': {
            'box': t_templet_wish_collection_box,
            'public_review': t_templet_public_wish_review,
            'public': t_templet_public_wish,
            'wait_upload': t_templet_wish_wait_upload,
            'upload_review': t_templet_wish_upload_review
        },
        'joom':{
            'box': t_templet_joom_collection_box,
            'public': t_templet_public_joom,
            'wait_upload': t_templet_joom_wait_upload
        }
    }
    change_dict = {'box': 1, 'public_review': 1, 'public': 1, 'wait_upload': 0, 'upload_review': 0}

    mysql_table = platefrom_page_table_dict[plateform][page]
    table_objs = mysql_table.objects.filter(id=int(id))

    if table_objs.exists():
        extraImages = table_objs[0].ExtraImages
        imageList = []
        if extraImages != None:
            imageList = extraImages.split('|')
        imageDict = {}
        for image in imageList:
            p_encode = urlsafe_b64encode(image)
            imageDict[p_encode] = image.replace('original', 'medium')
        variantsList = eval(table_objs[0].Variants)
        for variant in variantsList:
            productSKU = variant['Variant']['productSKU']
            goodsStatus = classsku_obj.get_goodsstatus_by_sku(productSKU)
            variant['Variant']['py_state'] = goodsStatus

    return render(request, 'show_wish_variant.html',
                  {'variants':variantsList,'page': page, 'id': id, 'plateform':plateform,'images':imageDict, 'change': change_dict[page]})

def save_wish_variant(request):
    """修改采集箱变种信息"""
    from datetime import datetime
    from skuapp.table.t_templet_wish_collection_box import t_templet_wish_collection_box
    from skuapp.table.t_templet_public_wish_review import t_templet_public_wish_review
    from skuapp.table.t_templet_public_wish import t_templet_public_wish
    from skuapp.table.t_templet_wish_wait_upload import t_templet_wish_wait_upload
    from skuapp.table.t_templet_wish_upload_review import t_templet_wish_upload_review
    from skuapp.table.t_templet_joom_collection_box import t_templet_joom_collection_box
    from skuapp.table.t_templet_public_joom import t_templet_public_joom
    from skuapp.table.t_templet_joom_wait_upload import t_templet_joom_wait_upload

    platefrom_page_table_dict = {
        'wish': {
            'box': t_templet_wish_collection_box,
            'public_review': t_templet_public_wish_review,
            'public': t_templet_public_wish,
            'wait_upload': t_templet_wish_wait_upload,
            'upload_review': t_templet_wish_upload_review
        },
        'joom': {
            'box': t_templet_joom_collection_box,
            'public': t_templet_public_joom,
            'wait_upload': t_templet_joom_wait_upload
        }
    }

    post = request.POST
    user = request.user.first_name
    time = datetime.now()
    plateform = post.get('plateform', '')
    page = post.get('page', '')
    id = int(post.get('id', ''))
    main_image = post.getlist('imgURL')
    productSKU = post.getlist('sonsku')
    color = post.getlist('color')
    size = post.getlist('size')
    sku = post.getlist('shopsku')
    inventory = post.getlist('quantity')
    price = post.getlist('price')
    msrp = post.getlist('msrp')
    shipping = post.getlist('shipping')
    shipping_time = post.getlist('time')
    enabled = post.getlist('status')

    mysql_table = platefrom_page_table_dict[plateform][page]
    Variants = []
    for i in range(len(sku)):
        Variant = {}
        VariantDict = {}
        VariantDict['sku'] = sku[i]
        VariantDict['productSKU'] = productSKU[i]
        VariantDict['main_image'] = main_image[i]
        VariantDict['color'] = color[i]
        VariantDict['price'] = price[i]
        VariantDict['shipping'] = shipping[i]
        VariantDict['inventory'] = inventory[i]
        VariantDict['msrp'] = msrp[i]
        VariantDict['shipping_time'] = shipping_time[i]
        VariantDict['format'] = 'json'
        VariantDict['parent_sku'] = ''
        VariantDict['size'] = size[i]
        VariantDict['enabled'] = eval(enabled[i])

        Variant['Variant'] = VariantDict
        Variants.append(Variant)
    mysql_table.objects.filter(id=id).update(Variants=Variants, UpdateStaff=user, UpdateTime=time)
    rt = u'修改成功！'
    return render(request, 'SKU.html', {'rt': rt})

def show_wish_schedule(request):
    """展示WISH铺货定时计划"""
    myId = eval(request.GET.get('myId', ''))
    url = request.get_full_path()
    params = ''
    if 'param' in url:
        params = url.split('param=')[-1]


    if isinstance(myId, int):
        wish_wait_upload_objs = t_templet_wish_wait_upload.objects.filter(id=myId)
        if wish_wait_upload_objs.exists():
            obj = wish_wait_upload_objs[0]
            schedule = {}

            if obj.ShopSets == None:
                shops = ''
            else:
                shops = obj.ShopSets

            if obj.TimePlan == None:
                start = ''
                interval = ''
            else:
                schedule = eval(obj.TimePlan)
                start = schedule['start']
                interval = schedule['interval']

            schedule['shops'] = shops
            schedule['start'] = start
            schedule['interval'] = interval
        flag = 1
        id_flag = 1

    else:
        schedule = {'shops':'', 'start':'已自动分配', 'interval':''}
        myId = ','.join(myId)
        flag = 2
        id_flag = 2
    return render(request, 'show_wish_schedule.html', {'schedule':schedule, 'myId':myId, 'flag':flag,
                                                       'id_flag':id_flag, 'param':params})

def save_wish_schedule(request):
    from datetime import datetime
    post = request.POST
    user = request.user.first_name
    time = datetime.now()
    number = post.get('number', '')
    shops = post.get('shops', '')
    start = post.get('start', '')
    interval = post.get('interval', '')
    param = post.get('param', '')

    myId = eval(post.get('myId', ''))

    if (start == '') or (interval == ''):
        rt = u'铺货开始时间和时间间隔都不能为空!'
        return render(request, 'SKU.html', {'rt': rt})

    elif (number == '') and (shops == ''):
        rt = u'铺货数量和铺货店铺不能都为空!'
        return render(request, 'SKU.html', {'rt': rt})

    else:

        # 所有店铺名的列表
        ShopName_list = []
        t_upload_shopname_objs = t_upload_shopname.objects.values('ShopName')
        for t_upload_shopname_obj in t_upload_shopname_objs:
            ShopName_list.append(t_upload_shopname_obj['ShopName'][-4:])

        if number == '':
            shops = shops
            if isinstance(myId, int):
                schedule = {}
                schedule['start'] = start
                schedule['interval'] = interval
                t_templet_wish_wait_upload.objects.filter(id=int(myId)).update(ShopSets=shops, TimePlan=schedule,
                                                                               UpdateStaff=user, UpdateTime=time)
                rt = u'修改成功！'
                return render(request, 'SKU.html', {'rt': rt})

            else:
                for each in myId:
                    obj = t_templet_wish_wait_upload.objects.filter(id=int(each))
                    schedule = eval(obj[0].TimePlan)
                    schedule['interval'] = interval
                    obj.update(ShopSets=shops, TimePlan=schedule, UpdateStaff=user, UpdateTime=time)
                return HttpResponseRedirect('%s' % param)
        else:
            num_int = int(number)
            if num_int > 50:
                num_int = 50

            # 修改单个记录
            if isinstance(myId, int):
                Shop_list = random.sample(ShopName_list, num_int)
                shops = ','.join(Shop_list)
                schedule = {}
                schedule['start'] = start
                schedule['interval'] = interval
                t_templet_wish_wait_upload.objects.filter(id=int(myId)).update(ShopSets=shops, TimePlan=schedule,
                                                                               UpdateStaff=user, UpdateTime=time)
                rt = u'修改成功！'
                return render(request, 'SKU.html', {'rt': rt})

            else:
                for each in myId:
                    Shop_list = random.sample(ShopName_list, num_int)
                    shops = ','.join(Shop_list)
                    obj = t_templet_wish_wait_upload.objects.filter(id=int(each))
                    schedule = eval(obj[0].TimePlan)
                    schedule['interval'] = interval
                    obj.update(ShopSets=shops, TimePlan=schedule, UpdateStaff=user, UpdateTime=time)
                return HttpResponseRedirect('%s' % param)

def show_wish_result(request):
    myId = request.GET.get('myId', '')
    rt = '<table   style="text-align:center;" border="1" cellpadding="3" cellspacing="1" bgcolor="#c1c1c1">' \
         '<tr bgcolor="#C00"><th style="text-align:center">店铺SKU</th>' \
         '<th style="text-align:center">商品SKU</th></tr>'

    tempList1 = []
    tempList2 = []
    Variants = eval(t_templet_wish_upload_result.objects.filter(id=myId)[0].Variants)
    tempList1 = [Variants['first']['product']['sku'], Variants['first']['product']['productSKU']]
    tempList2.append(tempList1)
    for product in Variants['second']['product']:
        tempList1 = [product['sku'], product['productSKU']]
        tempList2.append(tempList1)
    for each in tempList2:
        rt = '%s <tr bgcolor="#FFFFFF"><td>%s</td><td>%s</td></tr> ' % (rt, each[0], each[1])
    rt = "%s</table>" % rt
    return render(request, 'SKU.html', {'rt': rt})
    
    
    
def get_pic_list(MainSKU):
    from skuapp.table.t_product_mainsku_pic import t_product_mainsku_pic
    ImageTemp = t_product_mainsku_pic.objects.filter(MainSKU = MainSKU)
    main_pic_list = []
    other_pic_list = []
    for temp in ImageTemp:
        pic = temp.WishPic.replace('original', 'small')
        if temp.Flag == 0:
            other_pic_list.append({'id': temp.id, 'pic': pic, 'new': temp.NewFlag})
        else:
            main_pic_list.append({'id': temp.id, 'pic': pic, 'new': temp.NewFlag})
    return main_pic_list, other_pic_list
    
def oss2_image(MainSKU,name,imgs,url):
    from datetime import datetime as inserttime
    from skuapp.table.t_product_mainsku_pic import t_product_mainsku_pic
    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, ENDPOINT_OUT,BUCKETNAME_PIC)
    bucket.put_object('%s/%s'%(MainSKU,name),imgs)
    pic_url = PREFIX + BUCKETNAME_PIC + '.' + ENDPOINT_OUT + '/' + '%s/%s'%(MainSKU,name)
    t_product_mainsku_pic.objects.get_or_create(MainSKU=MainSKU,pic=pic_url,WishPic=url,UpdateTime=inserttime.now(),Flag=1)

def all_image_modify(request):
    from skuapp.table.t_product_image_modify import t_product_image_modify
    from datetime import datetime
    MainSKU = request.GET.get('code','')
    t_product_image_modify.objects.filter(MainSKU=MainSKU).update(UpdateFlag=0)
    if request.method == "POST":
        image_local = request.FILES.get('image_local', '')
        image_web = request.POST.get('image_web', '')
        if image_local:
            name = request.FILES.get('image_local').name
            oss2_image(MainSKU,name,image_local,None)
        if image_web.strip() != '':
            image_bytes = None
            try:
                req = urllib2.Request(image_web)
                image_bytes = urllib2.urlopen(req,timeout = 30).read()
            except :
                pass
            if image_bytes is not None:
                name = '%s.jpg'%datetime.now().strftime('%Y%m%d%H%M%S')
                oss2_image(MainSKU,name,image_bytes,image_web)
    main_pic_list, other_pic_list = get_pic_list(MainSKU)
    return render(request, 'all_image.html', {'main_pic_list':main_pic_list, 'other_pic_list': other_pic_list, 'MainSKU':MainSKU})
    
    
def all_image_modify_del(request):
    from skuapp.table.t_product_mainsku_pic import t_product_mainsku_pic
    id = request.GET.get('id','')
    MainSKU = request.GET.get('code','')
    source = request.GET.get('source','')
    if id is not None and id.strip() != '':
        if source == 'remove':
            t_product_mainsku_pic.objects.filter(id=id).update(Flag=0)
        else:
            t_product_mainsku_pic.objects.filter(id=id).update(Flag=1)
    main_pic_list, other_pic_list = get_pic_list(MainSKU)
    return render(request, 'all_image.html', {'main_pic_list':main_pic_list, 'other_pic_list': other_pic_list, 'MainSKU':MainSKU})
    
    
def show_aliexpress_warning(request):
    warning_id = request.GET.get('warning_id', '')
    objs = t_templet_aliexpress_collection_box.objects.filter(id=warning_id)

    result = []
    oss_url = 'http://fancyqube-alipic.oss-cn-shanghai.aliyuncs.com/'

    if objs.exists():
        skuArray = objs[0].PriceInfo
        productID = objs[0].ProductID
        skuList = eval(skuArray)['skuArray']
        for sku in skuList:
            temp = {}
            propertiesDict = sku[u'属性']
            for k, v in propertiesDict.items():
                if '#' in v:
                    temp['sku'] = v.split('#')[-1]

            image = ''
            pa = r'.*?\.jpg'
            for each in re.findall(pa, str(sku)):
                try:
                    image = oss_url + productID + '/img/' + each[-40:]
                except Exception, e:
                    print e
            temp['image'] = image
            result.append(temp)
    return render(request, 'aliexpress_warning.html', {'result': result, 'warning_id':warning_id})

def save_aliexpress_warning(request):
    warning_id = request.POST.get('warning_id', '')
    propertyList = request.POST.getlist('property', '')

    objs = t_templet_aliexpress_collection_box.objects.filter(id=warning_id)
    if objs.exists():
        info = objs[0].PriceInfo

        # 判断更改后的信息是否仍存在预警
        flag = 1
        for each_property in propertyList:
            numList = re.findall(r'\d+', each_property)
            for num in numList:
                if len(num) >= 3:
                    flag = 100
                    break
            if flag == 100:
                break

        # 如果更改后的信息不存在预警
        if flag == 1:
            # 找到原有的属性，放在列表中
            skuList = eval(info)['skuArray']
            old_property_list = []
            for sku in skuList:
                propertiesDict = sku['属性']
                for k, v in propertiesDict.items():
                    if '#' in v:
                        old_property_list.append(v)

            # 将更改的信息逐个替换原始信息
            for i in range(len(propertyList)):
                info = info.replace(old_property_list[i], propertyList[i])

            objs.update(PriceInfo=info, Flag=flag)
            rt = u'修改成功'
        else:
            rt = u'修改不成功，仍有自定义属性错误，请认真核对再修改！！！'

    return render(request, 'SKU.html', {'rt': rt})

def save_aliexpress_image(request):
    """保存速卖通主图"""
    myId = request.POST.get('image_id', '')
    image = request.POST.getlist('imageName', '')
    state = request.POST.getlist('status', '')

    MainImage = ''
    OtherImage = ''

    for i in range(len(image)):
        if state[i] == '1':
            if MainImage == '':
                MainImage = image[i]
            else:
                MainImage = MainImage + ',' + image[i]
        else:
            if OtherImage == '':
                OtherImage = image[i]
            else:
                OtherImage = OtherImage + ',' + image[i]

    if OtherImage == '':
        images = MainImage
    else:
        images = MainImage + "|" + OtherImage

    t_templet_aliexpress_collection_box.objects.filter(id=int(myId)).update(Images=images )
    return HttpResponseRedirect('/Project/admin/skuapp/t_templet_aliexpress_collection_box/')

def show_aliexpress_image(request):
    """展示速卖通主图"""
    myId = request.GET.get('myId', '')
    str = 'http://fancyqube-alipic.oss-cn-shanghai.aliyuncs.com/'
    imageList = t_templet_aliexpress_collection_box.objects.filter(id=int(myId))[0].Images.split('|')

    MainImageList = imageList[0].split(',')
    OtherImageList = []
    try:
        OtherImageList = imageList[1].split(',')
    except:
        pass

    MainUrlDict = {}
    OtherUrlDict = {}

    # 主图列表
    if len(MainImageList) != 0:
        for MainImage in MainImageList:
            MainUrl = str + MainImage
            MainUrlDict[MainImage] = MainUrl

    # 非主图列表
    if len(OtherImageList) != 0:
        for OtherImage in OtherImageList:
            OtherUrl = str + OtherImage
            OtherUrlDict[OtherImage] = OtherUrl

    return render(request, 'aliexpress_image.html', {'MainImage':MainUrlDict, 'OtherImage':OtherUrlDict, 'image_id':myId})


def make_shopname(request):
    from skuapp.table.t_aliexpress_categories_code import t_aliexpress_categories_code
    from skuapp.table.t_templet_aliexpress_wait_upload import t_templet_aliexpress_wait_upload
    from skuapp.table.t_aliexpress_distribution_shop import t_aliexpress_distribution_shop
    from skuapp.table.t_templet_aliexpress_wait_upload_temp import t_templet_aliexpress_wait_upload_temp
    myid = request.GET.get('myId', '')
    mycate = request.GET.get('cate', '')
    Ali=["Ali-0013","Ali-0037","Ali-0123","Ali-0124","Ali-0126","Ali-0136","Ali-0140","Ali-0156","Ali-0166","Ali-0186","Ali-0194","Ali-0202","Ali-0216","Ali-0222","Ali-0243","Ali-0263","Ali-0270","Ali-0274","Ali-0279","Ali-0280","Ali-0294","Ali-0300","Ali-0302","Ali-0306","Ali-0310","Ali-0311","Ali-0320"]
    ali=0
    if request.method == "POST":
        shopcodelist = [x.split('/')[0] for x in request.POST.getlist('shopname')]
        mycodelist = []
        for code in shopcodelist:
            mycodelist.append(code.split('-')[1])
        t_templet_aliexpress_wait_upload.objects.filter(id__in=myid.split('|')).update(ShopName=','.join(mycodelist))
        messages.success(request, u'ID:%s,已经将铺货目标店铺修改为:%s...' % (myid, shopcodelist,))
        return HttpResponseRedirect('/Project/admin/skuapp/t_templet_aliexpress_wait_upload/')
    else:
        mylist = []
        

        if myid is not None and myid.strip() != '' and mycate is not None and mycate.strip() != '':
            objs = t_aliexpress_categories_code.objects.filter(Classification=mycate).values('ShopName').order_by('ShopName')
            for obj in objs:
                tmp = {}
                tmp['ShopName'] = obj['ShopName']
                tmp['UpdateTime'] = ''
                tmp['AccountGroup'] = ''
                oj1 = t_templet_aliexpress_wait_upload_temp.objects.filter(ShopName__contains=obj['ShopName'][-3:],Status='OK').order_by('-UpdateTime')[:1]
                if oj1:
                    tmp['UpdateTime'] = oj1[0].UpdateTime
                oj2 = t_aliexpress_distribution_shop.objects.filter(ShopCode=obj['ShopName'])
                if oj2:
                    tmp['AccountGroup']=oj2[0].AccountGroup
                if obj['ShopName'] in Ali:
                    tmp['is_cloth']='服装'
                    mylist.insert(0,tmp)
                else:
                    tmp['is_cloth']='非服装'
                    mylist.append(tmp)        
        return render(request, 'to_change_ali_upload_shopname.html',
                      {'objs': mylist, 'myid': myid, 'mycate': mycate })


def importfile_paypal_tort(request):
    from app_djcelery.tasks import import_excel_file_paypal_tort
    if request.FILES.get('myfile') is not None:
        user_name = request.user.username
        file_obj = request.FILES['myfile']
        import_excel_file_paypal_tort(file_obj)
        messages.success(request,u'导入成功，请稍后。。。')
    return HttpResponseRedirect('/Project/admin/skuapp/paypal_tort/')
    

def importfile_aliexpress_refund(request):
    from app_djcelery.tasks import import_excel_file_aliexpress
    if request.FILES.get('myfile') is not None:
        user_name = request.user.username
        file_obj = request.FILES['myfile']
        result = import_excel_file_aliexpress(file_obj, user_name)
        if result["errorcode"] == 1:
            messages.success(request, u'导入成功，请稍后刷新。。。')
        else:
            messages.success(request, u'导入失败，失败原因%s,请联系开发人员查看'%(result["errortext"]))
    return HttpResponseRedirect('/Project/admin/skuapp/t_aliexpress_refund/')
    
def importfile_stocking_demand(request):
    from app_djcelery.tasks import import_excel_file
    if request.FILES.get('myfile') is not None:
        user_name = request.user.first_name
        file_obj = request.FILES['myfile']
        result = import_excel_file(file_obj,user_name)
        if result['errorcode'] == 0:
            messages.success(request,result['errortext'])
        else:
            messages.success(request, result['errortext'])
    return HttpResponseRedirect('/Project/admin/skuapp/t_stocking_demand_list/')

def upload_to_oss2(data,name):
    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, ENDPOINT_OUT,BUCKETNAME_DOWNLOAD)
    bucket.put_object('%s'%name,data)
    myurl = PREFIX + BUCKETNAME_DOWNLOAD + '.' + ENDPOINT_OUT + '/' + '%s'%name
    return myurl

def importfile_Invoice_BoxPaste(request):
    from skuapp.table.t_shipping_management import t_shipping_management
    id = request.GET.get('myid')
    batchnum = request.GET.get('batchnum')
    if request.method == "POST":
        invoice = request.FILES.get('invoice')
        boxpaste = request.FILES.get('boxpaste')
        if invoice is not None:
            invoice_path = upload_to_oss2(invoice, 'invoice/%s_%s'%(batchnum,invoice.name))
            t_shipping_management.objects.filter(id=id).update(Invoice=invoice_path)
        if boxpaste is not None:
            boxpaste_path = upload_to_oss2(boxpaste, 'boxpaste/%s_%s' % (batchnum, boxpaste.name))
            t_shipping_management.objects.filter(id=id).update(BoxPaste=boxpaste_path)
        rt = u'修改成功。。。'
        return render(request, 'result.html', {'rt': rt})
    else:
        return render(request, 'importfile_invoice_boxpaste.html', {'id': id,'batchnum':batchnum})
    
    
    
def show_ebay_image(request):
    """展示ebay主图"""
    myId = request.GET.get('myId', '')
    collection_box_obj = t_templet_ebay_collection_box.objects.filter(id=int(myId))[0]
    MainImageList = collection_box_obj.Images.split(',')
    imageDict = {}
    for i in range(len(MainImageList)):
        imageDict[i] = MainImageList[i]#.replace('https://i.ebayimg.com','http://fancyqube-ebaypic.oss-cn-shanghai.aliyuncs.com')
    return render(request, 'ebay_image.html', {'imageDict':imageDict, 'image_id':myId})

def ebay_oss_image(name, img_byte, user, sku):
    from skuapp.table.t_templet_ebay_collection_box import *
    BUCKETNAME_PIC = 'fancyqube-ebaypic'
    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, ENDPOINT_OUT, BUCKETNAME_PIC)
    bucket.put_object('%s/%s/%s' % (user, sku, name), img_byte)
    pic_url = PREFIX + BUCKETNAME_PIC + '.' + ENDPOINT_OUT + '/' + '%s/%s/%s' % (user, sku, name)
    return pic_url

def save_ebay_image(request):
    """保存ebay主图"""
    from datetime import datetime
    myId = request.GET.get('myId', '')
    collection_box_obj = t_templet_ebay_collection_box.objects.filter(id=int(myId))[0]
    Images = collection_box_obj.Images
    sku = collection_box_obj.sku
    MainImageList = Images.split(',')

    imageDict = {}

    # 上传图片
    if request.method == "POST":
        user = request.user.username
        image_local = request.FILES.get('image_local')
        image_url = request.POST.get('image_url','')

        # 上传本地照片
        if image_local is not None:
            pic_name = request.FILES.get('image_local').name
            pic_url = ebay_oss_image(pic_name ,image_local, user, sku)
            MainImageList.append(pic_url)

        # 上传图片链接
        if image_url.strip() != '':
            image_bytes = None
            try:
                req = urllib2.Request(image_url)
                image_bytes = urllib2.urlopen(req,timeout = 30).read()
            except :
                pass
            if image_bytes is not None:
                pic_name = '%s.jpg' % datetime.now().strftime('%Y%m%d%H%M%S')
                pic_url = ebay_oss_image(pic_name, image_bytes, user, sku)
                MainImageList.append(pic_url)

    else:
        imageId = int(request.GET.get('id', ''))
        # 删除图片
        del MainImageList[imageId]

    mainImage = ','.join(MainImageList)
    for i in range(len(MainImageList)):
        imageDict[i] = MainImageList[i]

    t_templet_ebay_collection_box.objects.filter(id=int(myId)).update(Images=mainImage)

    return render(request, 'ebay_image.html', {'imageDict': imageDict, 'image_id': myId})
    
def modify_ebay_schedule(request):
    """展示eBay铺货定时计划"""
    from datetime import datetime
    from skuapp.table.t_config_store_ebay import t_config_store_ebay

    myId = request.GET.get('myId', '')

    if request.method == 'POST':
        user = request.user.first_name
        post = request.POST
        time = datetime.now()
        shops = post.get('shops', '')
        #shops = post.getlist('shops')
        #messages.error(request,'&*&*&*&*&*&%s'%shops)
        start = post.get('start', '')
        interval = post.get('interval', '')

        if start.strip() != '' and interval.strip() != '' and shops.strip() != '':
        #if start.strip() != '' and interval.strip() != '' and len(shops)>0:
            shops_list =[]
            for i in shops:
                shops_list.append(shops)
            Shops = shops_list[0].split(',')
            #messages.error(request,'&*&*&*&*&*&%s'%Shops)
                
            Site = t_templet_ebay_wait_upload.objects.filter(id=myId).values('Site')
            if int(Site[0]['Site']) == 2:      #加拿大账号与美国一样
                Site = t_templet_ebay_wait_upload.objects.filter(Site=0)[:1].values('Site')
            #messages.error(request,'********%s'%Site)
            site_name = t_config_store_ebay.objects.filter(siteID=Site).values('storeName')
            #messages.error(request,'********%s'%site_name)
        #for k, v in range(0, len(site_name)):
            site_storename = []
            for i in site_name:
                if isinstance(i,dict):
                    for k,v in i.items():
                        if v:
                            site_storename.append(v)

            if Shops and set(Shops).issubset(site_storename):
                # 铺货店铺和站点对应
                repeate_Shop = [val for val in list(set(Shops)) if Shops.count(val) > 1]
                if repeate_Shop:
                    rt = '请勿重复填写铺货店铺: %s' % ",".join(repeate_Shop)
                else:
                    schedule = {}
                    schedule['start'] = start
                    schedule['interval'] = interval
                    t_templet_ebay_wait_upload.objects.filter(id=myId).update(ShopSets=shops, TimePlan=schedule,UpdateStaff=user, UpdateTime=time, Status='NO')
                    rt = u'修改成功！'
            elif Shops and not set(Shops).issubset(site_storename):
                rt = ''
                for each in Shops:
                    if each not in site_storename:
                        rt += str(each) + ','
                rt = '您填写的铺货店铺:' + rt[0:-1] + '与站点不对应!'
            else:
                rt = '系统异常，请重试！' # 异常
        # else:
        #     rt = '未完全填写数据!'
        return render(request, 'SKU.html', {'rt': rt})
    else:
        ebay_wait_upload_objs = t_templet_ebay_wait_upload.objects.filter(id=myId)
        if ebay_wait_upload_objs.exists():
            obj = ebay_wait_upload_objs[0]
            schedule = {}
            if obj.ShopSets == None:
                shops = ''
            else:
                shops = obj.ShopSets
            if obj.TimePlan == None:
                start = ''
                interval = ''
            else:
                schedule = eval(obj.TimePlan)
                start = schedule['start']
                interval = schedule['interval']
            schedule['shops'] = shops
            schedule['start'] = start
            schedule['interval'] = interval

        return render(request, 'show_ebay_schedule.html', {'schedule':schedule, 'myId':myId})

def show_ebay_variation(request):
    """展示采集箱变种信息"""
    box_id = request.GET.get('box', '')
    public_id = request.GET.get('public', '')
    upload_id = request.GET.get('upload', '')

    title = {}

    if box_id != '':
        MySQL_table = t_templet_ebay_collection_box
        templet_id = box_id
        title['box_id'] = templet_id
    elif public_id != '':
        MySQL_table = t_templet_public_ebay
        templet_id = public_id
        title['public_id'] = templet_id
    else:
        MySQL_table = t_templet_ebay_wait_upload
        templet_id = upload_id
        title['upload_id'] = templet_id

    tables_objs = MySQL_table.objects.filter(id=int(templet_id))
    if tables_objs.exists():
        obj = tables_objs[0]
        if (obj.Variation.strip() != '') and (obj.Variation is not None):
            variation_list = eval(obj.Variation).get("Variation", '')
            result = []
            if variation_list != '':
                for variation in variation_list:
                    sku = variation.get('SKU', '')
                    price = variation.get('StartPrice', '')
                    quantity = variation.get('Quantity', '')

                    color = ''
                    size = ''
                    VariationSpecifics = variation.get('VariationSpecifics', '')
                    if VariationSpecifics != '':
                        NameValueList = VariationSpecifics.get('NameValueList', '')
                        if NameValueList != '':
                            for each in NameValueList:
                                if 'Color' in each.values():
                                    color = each.get('Value', '')
                                if 'Size' in each.values():
                                    size = each.get('Value', '')

                    result_dict = {'sku':sku, 'price':price, 'quantity':quantity, 'color':color, 'size':size}
                    result.append(result_dict)

    return render(request, 'show_ebay_variation.html', {'result': result, 'ebay_title': title})

def save_ebay_variation(request):
    """修改采集箱变体信息"""
    post = request.POST
    box_id = post.get('box_id', '')

    sku = post.getlist('sku')
    price = post.getlist('price')
    quantity = post.getlist('quantity')
    color = post.getlist('color')
    size = post.getlist('size')

    collection_box_obj = t_templet_ebay_collection_box.objects.filter(id=int(box_id))
    Variation = eval(collection_box_obj[0].Variation)
    variation_list = Variation.get('Variation', '')
    length = len(variation_list)
    for i in range(length):
        variation_list[i]['SKU'] = sku[i]
        variation_list[i]['StartPrice'] = price[i]
        variation_list[i]['Quantity'] = quantity[i]

        NameValueList = variation_list[i]['VariationSpecifics']['NameValueList']
        for each in NameValueList:
            if 'Color' in each.values():
                each['Value'] = color[i]
            if 'Size' in each.values():
                each['Value'] = size[i]
    collection_box_obj.update(Variation = str(Variation))

    rt = u'修改成功！'
    return render(request, 'SKU.html', {'rt': rt})
    
    
from django.db import connection
#from brick.db.ebay_api import *
from brick.ebay.ebay_api import *
from brick.table.t_developer_info_ebay import *

def t_config_store_ebay_regetpes_torken(request):
    from brick.table.t_config_store_ebay import *
    id = request.GET.get('id', '')
    appID = request.GET.get('appID', '')
    sessionid = request.GET.get('sessionid', '')
    if not sessionid:
        messages.error(request, '重新授权失败，请重试！id --> %s' % id)
        return HttpResponseRedirect('/Project/admin/skuapp/t_config_store_ebay/')

    t_developer_info_ebay_obj = t_developer_info_ebay(connection)
    developerdata = t_developer_info_ebay_obj.queryDeveloperEbay(appID)
    if developerdata['errorcode']  <> 0:
        messages.error(request, '重新授权失败，请重试！id --> %s' % id)
        return HttpResponseRedirect('/Project/admin/skuapp/t_config_store_ebay/')

    appinfo = {
        'appid': appID,
        'devid': developerdata['datasrcset'][0],
        'certid': developerdata['datasrcset'][1],
        'runame': developerdata['datasrcset'][2],
    }

    ebayapi_obj = EBayAPI(appinfo)
    r_torken = ebayapi_obj.fetchToken(sessionid=sessionid)
    if not r_torken:
        messages.error(request, '重新授权失败，请重试！id --> %s'% id)
        return HttpResponseRedirect('/Project/admin/skuapp/t_config_store_ebay/')

    tokenExpireTime = datetime.datetime.strptime(r_torken[1][:19], "%Y-%m-%dT%H:%M:%S")
    params = {'token':r_torken[0],'tokenExpireTime':tokenExpireTime,'id':id}
    t_config_store_ebay_obj = t_config_store_ebay(connection)
    resultcode = t_config_store_ebay_obj.update_token(params=params)
    if resultcode['errorcode'] <> 0:
        messages.error(request, '重新授权失败，请重试！id --> %s'% id)
    elif resultcode['errorcode'] == 0:
        messages.success(request,'重新授权完成: id --> %s'% id)
    return HttpResponseRedirect('/Project/admin/skuapp/t_config_store_ebay/')

def t_config_store_ebay_regetpes_oauth(request):
    from brick.table.t_config_store_ebay import *
    import urllib
    import urlparse
    import base64
    import urllib2
    import datetime as hdltime
    import json
    if request.method == 'GET':
        try:
            code_mess = request.GET.get('code_mess', '')
            appID = request.GET.get('appID', '')
            regType = request.GET.get('regType', '')
            id = request.GET.get('id', '')
            de_url = urllib.unquote(code_mess)
            # query = urlparse.urlparse(de_url).query
            # de_url_dict =  dict([(k, v[0]) for k, v in urlparse.parse_qs(query).items()])
            # code = de_url_dict['code']
            code = de_url.split('=')[3]

            t_developer_info_ebay_obj = t_developer_info_ebay(connection)
            developerdata = t_developer_info_ebay_obj.queryDeveloperEbay(appID)
            if developerdata['errorcode'] <> 0:
                return HttpResponse('one======数据获取失败请重试!!!')
            appinfo = {
                'appid': appID,
                'devid': developerdata['datasrcset'][0],
                'certid': developerdata['datasrcset'][1],
                'runame': developerdata['datasrcset'][2],
            }
            ClientSecretId = str(appinfo['appid'])+':'+str(appinfo['certid'])
            base64_ClientSecretId = base64.encodestring(ClientSecretId)
            headers = {'Content-Type': 'application/x-www-form-urlencoded','Authorization': 'Basic '+str(base64_ClientSecretId).replace("\n","")}
            # return HttpResponse(str(headers))
            body = 'grant_type=authorization_code&code='+str(code)+'&redirect_uri='+str(appinfo['runame'])
            get_OAuth_request_url = 'https://api.ebay.com/identity/v1/oauth2/token'
            # return HttpResponse(str(headers) + str(body))
            req = urllib2.Request(url=get_OAuth_request_url, data=body, headers=headers)
            res = urllib2.urlopen(req, timeout=30).read()
            # texst = str(res)
            """
                {"access_token":"v^1.1#i^1#f^0#r^0#p^3#I^3#t^H4sIAAAAAAAAAN1XfWwTZRjfbd10MkSjGYQQrAdEBa9973rtfUgrZetkwrayGxOHZNzHe+256129u24UMTYzAfkw0SgalD8gRAWDCRgEFEREEpPFaBSJaGSif/hFNMYvIMPoe906uhkHYSQ2tr0097zPPe/v93uee9/3Abmq6tlrFqw5OxG7pnxrDuTKMYycAKqrKudcX1E+tbIMFDlgW3Mzc57eiu/m2mJKT/Ot0E6bhg29K1O6YfN5YxjPWAZvirZm84aYgjbvyLwQbVrEUz7Apy3TMWVTx72N9WFcUgAriwqQVRmSMqUgq1GI2WaG8aCsAIUFChcKSXSA5NC4bWdgo2E7ouGEcQqQLAHQj2kDLA8AT9M+hgt04N52aNmaaSAXH8Ajebh8/lmrCOvYUEXbhpaDguCRxmiD0BJtrI81t831F8WKDOkgOKKTsUfe1ZkK9LaLegaOPY2d9+aFjCxD28b9kcEZRgblowUwVwA/L7UKSDkohmg5wDAUK7NXRcoG00qJztg4XIumEGrelYeGoznZSymK1JAehLIzdNeMQjTWe92/xRlR11QNWmE8Nj96/xIh1op7hXjcMrs1BSouU5pFDDkWkHiEY7qGog+GGNJ2VPg601A0Vynb22w68yGCCkcKwvDBIkGQU4vRYkVVx4VR5EeCgnBssMPN5GDqMk7ScJMJU4i9N397adkLdXAx81erEmiKI4MiICmRVBVKBWNVgvuuX241RNyERONxv4sFSmKWSIlWF3TSuihDQkbyZlLQ0hQ+EFSpAKtCQglxKkFzqkpIQSVEkCqEAEJJkjn2f18UjmNpUsaBw4UxeiDPLIy7QvKaqPKO2QWNtmwa4qM984vMUDWstMN40nHSvN/f09Pj6wn4TCvhpwAg/UubFglyEqZEfNhXu7QzoeXrQoboKVvjHQQgjK9EZYcmNxJ4pDXW0BoTFnS2tSyMNRdKdgSyyGjrvzAVZDMN46auydnSohiwlLhoOVkB6joyjIuk7ZIsLXpGRtdd9O67fsW8oul0o1JavO6FhpHtSGYIgYi31hN0UGFEEAAMWnZAiOQUdlyJVGC3JsNOrcRIF5J5xbzqYXepJVKhFFWCYoAQWQ4SNIl2E46VQwQL0NGRZVT0DY6Lc1Oi1NJI0myAoZkgHQCAGhe3Ol1Dm8vofcPTi/X/9ywXmLYDlfHRQyeb0kqdu9YUlhqaClAER0JA0JQiERytAoKU4GWvPKMMRWeFf5wN/SM7skhZ/kP2Yq+DXmwPauqAH8wiZ4BbqyqWeCpqptqaA33oXOGztYSBGg0L+rpgNi1qVnkVtmza7p2dRT3g1uVgynAXWF1BTihqCcG0iyOV5KTJE0kWsIBBF6DpDjDj4qiHrPXcvHfLz0umJKvfFu4Ms4naTJ8HrOsHE4edMKyyDBVn2T7wfefxF1Z/9lP7E8EzuVdrz52M/pjw/Fl34Gzk2DP9B76+e9cE/eNPy59dN+nLxw/WJWvwzY/8sHDjJ01RaeCcvuqbXQvfOPHKB9Spfrga+/2pe/YnZtVseJlcsyO7fvIfd21bPuXw6lMnJ18IPjT9pTnNd0STN3bP3bHxORZfW3PoxDvbmr79cOayv/pu2nLM+/5XmyPXKu8xJ4+e2X4kt/+WFb/MnreBnhbjDj2Nvbu872h5ZRW5mDgovXVbU93S6+7bDt/cfaFjT8/0eb8+tna3UB8Dy/ZiD3tyx4+HVjUcbn9SOf/o3o9Cfb+tGGjed5rc9HntwOmegdfOP5Ckzjx/+4ovXuzY1HdDTfbcrCM7B9P3NypJXl+dDwAA",
                "expires_in":7200,
                "refresh_token":"v^1.1#i^1#r^1#p^3#I^3#f^0#t^Ul4xMF8xOjFFNEQ1OEQ1MDA3QUZCNjM0ODc2Qjk5NUQ1NTU3RTk4XzJfMSNFXjI2MA==",
                "refresh_token_expires_in":47304000,
                "token_type":"User Access Token"}

            """
            d_res = json.loads(res)
            if isinstance(d_res, dict):
                messages.success(request,d_res['refresh_token'])

            if isinstance(d_res,dict):
                params = {}
                if d_res.has_key('refresh_token'):
                    params['refresh_token'] = d_res['refresh_token']
                    params['refresh_token_expires_in'] = d_res['refresh_token_expires_in']
                    params['id'] = id
                    params['refresh__time'] = hdltime.datetime.now()
                    t_config_store_ebay_obj = t_config_store_ebay(connection)
                    resultcode = t_config_store_ebay_obj.update_refresh_token(params=params)
                    if resultcode['errorcode'] ==  0:
                        return HttpResponse('刷新token成功')
                    else:
                        return HttpResponse('two=====刷新失败')
                else:
                    return HttpResponse('three===刷新失败')
            else:
                return HttpResponse('four ====刷新失败')
        except Exception,ex:
            return HttpResponse(str(repr(ex)))
    else:
        return HttpResponse('POST ......')
    return HttpResponseRedirect('/Project/admin/skuapp/t_config_store_ebay/')



def t_config_store_ebay_regetpes_plugin(request):
    appID = request.GET.get('appID', '')
    id = request.GET.get('id', '')
    accountID = request.GET.get('accountID', '')
    regType = request.GET.get('regType', '')
    return HttpResponseRedirect('/Project/admin/skuapp/t_config_store_ebay/?testparam=markparameters&appID=%s&id=%s&accountID=%s&regType=%s'%(appID,id,accountID,regType))




def t_config_wishapi_product_analyse_info_start(request):
    jsonurl = request.GET.get('jsonurl', '')
    return render(request, 't_config_wishapi_product_analyse_info.html', {'jsonurl':jsonurl})


def update_order_count(request):
    from datetime import datetime as my_time
    data = ''
    num = ''
    time = ''
    time1 = ''
    time2 = ''
    if request.method == 'POST':
        num = request.POST['num']
        if num.isdigit():
            time = str(my_time.now())[:10]
            import pymssql
            sqlserver_conn = pymssql.connect(host='122.226.216.10', user='sa', password='$%^AcB2@9!@#',
                                             database='ShopElf',
                                             port='18793')
            sqlcursor = sqlserver_conn.cursor()
            time1 = my_time.now()
            sql1 = "truncate table p_tradebig_tmp"
            sql2 = "truncate table p_tradebig_tmp_top3"
            sql3 = "insert into p_tradebig_tmp select a.SKU as SKU,sum(a.L_QTY) as tradenum from P_TradeDt(nolock) a " \
                   "INNER JOIN P_Trade(nolock) b on a.TradeNID = b.NID AND ordertime>= (GETDATE()-{})" \
                   "GROUP BY a.SKU,a.TradeNID UNION ALL select a.SKU as SKU,sum(a.L_QTY) as tradenum from P_TradedtUn(nolock) " \
                   "a INNER JOIN P_TradeUn(nolock) b on a.TradeNID = b.NID AND ordertime>= (GETDATE()-{}) " \
                   "GROUP BY a.SKU,a.TradeNID".format(num,num)
            sql4 = "insert into p_tradebig_tmp_top3 select a.sku,a.tradenum from p_tradebig_tmp(nolock) a  where checksum(*) in (select top 3 checksum(*) from p_tradebig_tmp(nolock) c where a.sku=c.sku order by c.tradenum desc)"
            sql5 = "update  B_Goods set LinkUrl5 = c.values2 + '| {}' from B_Goods f, (select tb.sku, " \
                   "stuff((select '|'+REPLACE([tradenum],' ','') from p_tradebig_tmp_top3(nolock) t  where SKU=tb.SKU order by " \
                   "tradenum desc for xml path('')), 1, 1, '') as values2  from p_tradebig_tmp_top3(nolock) tb group by tb.sku ) " \
                   "c where f.SKU = c.sku".format(time)
            try:
                sqlcursor.execute(sql1)
                sqlcursor.execute(sql2)
                sqlcursor.execute(sql3)
                sqlcursor.execute(sql4)
                sqlcursor.execute(sql5)
                sqlserver_conn.commit()
            except pymssql.Error, e:
                logger.error("pymssql Error %d: %s" % (e.args[0], e.args[1]))
                sqlserver_conn.rollback()
                data = "操作失败"
            else:
                time2 = my_time.now()
                data = "操作成功,本次消耗时长{}".format(time2-time1)
            finally:
                if sqlcursor:
                    sqlcursor.close()
                sqlserver_conn.close()
        else:
            data = "请输入有效值!"
    return render(request,'update_order_count.html',{'data':data})
    
    
    
def change_col(request):
    from django.db import connection
    """
    用于记录‘显示列’点击保存后的url列
    """
    mymodel = ['/']
    param = ''
    url = request.GET.get('_cols', '')
    if request.method == "POST":
        param = request.POST.get('param','')
        model = request.POST.get('model','')

        if model != '':
            mymodel = model.split('/')
            mymodel.remove(mymodel[-2])

        if url != '':
            cursor = connection.cursor()
            cursor.execute("insert into mm_bookmarks SET userid=%s,username=%s,url=%s,model=%s "
                           "on duplicate KEY update url=%s;",
                           (request.user.id,request.user.first_name,'?_cols='+url,mymodel[-2],'?_cols='+url))
            cursor.execute('commit;')
            cursor.close()

        if param != '':
            param = param + '&'

    return HttpResponseRedirect('/'.join(mymodel) + '?' + param + '_cols=' + url)
    
    
    
    
def update_status_by_sku(request):
    from django.db import connection
    from django_redis import get_redis_connection
    from datetime import datetime as logtime
    redis_conn = get_redis_connection(alias='product')
    redis_conn = None
    from brick.classredis.classsku import classsku
    from brick.classredis.classshopsku import classshopsku
    from app_djcelery.tasks import update_status_by_shopsku_func
    from brick.table.t_wish_product_sku_upload_or_not_log import t_wish_product_sku_upload_or_not_log

    sku = request.GET.get('disshopsku','')
    flag = 'disshopsku'
    if sku == '':
        sku = request.GET.get('enshopsku','')
        flag = 'enshopsku'

    classsku_obj = classsku(connection,redis_conn)
    shopskulist = classsku_obj.get_shopsku_by_sku(sku)

    if shopskulist is not None:
        classshopsku_obj = classshopsku(connection,redis_conn)
        t_wish_product_sku_upload_or_not_log_obj = t_wish_product_sku_upload_or_not_log(connection)
        for shopsku in shopskulist:
            shopname = classshopsku_obj.get_shopname_by_shopsku(shopsku)
            logdata = {'SKU':sku,'ShopSKU':shopsku,'Type':flag,'Person':request.user.first_name,
                       'Time':logtime.now(),'Status':''}
            t_wish_product_sku_upload_or_not_log_obj.insert_data(logdata)
            update_status_by_shopsku_func.delay(shopsku,shopname,flag)
            messages.success(request, u'%s,%s,disshopsku'%(shopsku,shopname))
        messages.success(request, u'下架操作正在执行，请稍等片刻。。。')
    else:
        messages.error(request,u'没有找到绑定的商品编码。。。')

    return HttpResponseRedirect('/Project/admin/skuapp/t_product_b_goods_all_productsku/')



# 通过商品SKU来上下架其绑定的所有的ShopSKU（目前没有用到）
def update_status_by_sku(request):
    from django.db import connection
    from django_redis import get_redis_connection
    from datetime import datetime as logtime
    redis_conn = get_redis_connection(alias='product')
    redis_conn = None
    from brick.classredis.classsku import classsku
    from brick.classredis.classshopsku import classshopsku
    from app_djcelery.tasks import update_status_by_shopsku_func
    from brick.table.t_wish_product_sku_upload_or_not_log import t_wish_product_sku_upload_or_not_log

    sku = request.GET.get('disshopsku','')
    flag = 'disshopsku'
    if sku == '':
        sku = request.GET.get('enshopsku','')
        flag = 'enshopsku'

    classsku_obj = classsku(connection,redis_conn)
    shopskulist = classsku_obj.get_shopsku_by_sku(sku)

    if shopskulist is not None:
        classshopsku_obj = classshopsku(connection,redis_conn)
        t_wish_product_sku_upload_or_not_log_obj = t_wish_product_sku_upload_or_not_log(connection)
        for shopsku in shopskulist:
            shopname = classshopsku_obj.get_shopname_by_shopsku(shopsku)
            logdata = {'SKU':sku,'ShopSKU':shopsku,'Type':flag,'Person':request.user.first_name,
                       'Time':logtime.now(),'Status':''}
            t_wish_product_sku_upload_or_not_log_obj.insert_data(logdata)
            update_status_by_shopsku_func.delay(shopsku,shopname,flag)
            messages.success(request, u'%s,%s,disshopsku'%(shopsku,shopname))
        messages.success(request, u'下架操作正在执行，请稍等片刻。。。')
    else:
        messages.error(request,u'没有找到绑定的商品编码。。。')

    return HttpResponseRedirect('/Project/admin/skuapp/t_product_b_goods_all_productsku/')



def TestAjax(request):
    msg = []
    if request.is_ajax():
        supplier = request.POST.get("supplier")
        if supplier:
            from pyapp.models import B_Supplier
            B_Supplier_objs = B_Supplier.objects.filter(SupplierName__contains=supplier)
            for B_Supplier_obj in B_Supplier_objs:
                msg.append(B_Supplier_obj.SupplierName)
        ret = {"msg":msg}
        return HttpResponse(json.dumps(ret))
    else:
        return render(request, 'TestAjax.html')


from django.shortcuts import render, HttpResponse
# 根据店铺同步
def t_online_info_amazon_listing_syn_shopname(request):
    import traceback
    try:
        import uuid
        from brick.amazon.product_refresh.get_auth_info import GetAuthInfo
        from brick.amazon.product_refresh.put_refresh_message_to_rabbitmq import MessageToRabbitMq
        from brick.table.t_config_amazon_progress_bar import t_config_amazon_progress_bar
        from brick.table.t_config_amazon_shop_status import t_config_amazon_shop_status
        from django.db import connection
        if request.method == 'GET':
            ShopName = request.GET.get('ShopName','')
            # if ShopName:
            #     searchSite = ShopName.split('-')[-1].split('/')[0]
            # else:
            #     searchSite = ''
            synType = request.GET.get('synType')
            UUID = uuid.uuid4()
            get_auth_info_ins = GetAuthInfo(connection)
            # name = get_auth_info_ins.get_name_by_shop_and_site(ShopName, searchSite)# 'AMZ-0052-Bohonan-US/PJ'
            auth_info = get_auth_info_ins.get_auth_info_by_shop_name(ShopName)
            auth_info['table_name'] = 't_online_info_amazon'
            auth_info['update_type'] = 'refresh_shop_' + synType
            auth_info['uuid'] = str(UUID)
            message_to_mq_ins = MessageToRabbitMq(auth_info, connection)
            message_to_mq_ins.put_message(str(auth_info))
            t_config_amazon_progress_bar_obj = t_config_amazon_progress_bar(db_conn=connection)
            t_config_amazon_progress_bar_obj.insert_into_Progress(auth_info, 'submit')
            t_config_amazon_shop_status_obj = t_config_amazon_shop_status(db_conn=connection)
            t_config_amazon_shop_status_obj.update_shop_status(auth_info, ShopName, 'process')
            return HttpResponse(UUID)

            # if synType == 'all':
            #     # 执行同步任务  全量同步
            #     UUID = uuid.uuid4()
            #     t_config_amazon_progress_bar_obj = t_config_amazon_progress_bar(db_conn=connection)
            #     t_config_amazon_progress_bar_obj.insert_into_Progress(UUID, 'accomplish')
            #     return HttpResponse(UUID)
            # elif synType == 'increment':
            #     # 执行同步任务  增量同步
            #     UUID = uuid.uuid4()
            #     t_config_amazon_progress_bar_obj = t_config_amazon_progress_bar(db_conn=connection)
            #     t_config_amazon_progress_bar_obj.insert_into_Progress(UUID, 'accomplish')
            #     return HttpResponse(UUID)
    except Exception, ex:
        traceback.print_exc(file=open('/tmp/view.log', 'a'))
    return render(request, 't_online_info_amazon_listing_plugin.html')


# 询问是否执行完毕
def t_online_info_amazon_listing_complete_shopname(request):
    from brick.table.t_config_amazon_progress_bar import t_config_amazon_progress_bar
    if request.method == 'GET':
        #ShopName = request.GET.get('ShopName')
        #searchSite = request.GET.get('searchSite')
        # 查询 同步是否完成
        uuid=request.GET.get('uuid')
        t_config_amazon_progress_bar_obj = t_config_amazon_progress_bar(db_conn=connection)
        p_result = t_config_amazon_progress_bar_obj.getProgress(uuid)
        p_flag = ''
        if p_result['code'] == 0:
            p_flag = p_result['data'][0]
        # return HttpResponse('标志同步完成的值')
        return HttpResponse(p_flag)
    return render(request, 't_online_info_amazon_listing_plugin.html')



# Amazon店铺管理--同步listID、list上架、list下架
def syndata_by_amazon_api(request):
    import traceback
    # logging.basicConfig(level=logging.DEBUG,
    #                     format='%(asctime)s [%(filename)s %(funcName)s:%(lineno)d] %(thread)d %(levelname)s %(message)s',
    #                     datefmt='%Y-%m-%d %H:%M:%S',
    #                     filename='/home/wcx/Project/view.log',
    #                     filemode='a')
    #
    # logging.handlers.RotatingFileHandler('/home/wcx/Project/view.log',
    #                                      maxBytes=5 * 1024 * 1024,
    #                                      backupCount=10)
    try:
        # logging.debug('11111111')
        from skuapp.table.t_online_info_amazon_listing import *
        shopName = request.GET.get('shopName')
        seller_sku = request.GET.get('seller_sku')
        operation_type = request.GET.get('operation_type')
        pri_id =  request.GET.get('pri_id')
        # logging.debug('shopname: %s' % shopName)
        # logging.debug('seller_sku: %s' % seller_sku)
        # logging.debug('pri_id: %s' % pri_id)
        product_list_obj = t_online_info_amazon_listing.objects.filter(id=int(pri_id))[0]

        if operation_type == 'sync':
            messages.success(request, u'正在同步，请稍后刷新页面。。。')
            return HttpResponseRedirect('/Project/admin/skuapp/t_online_info_amazon_listing/?seller_sku=%s&ShopName=%s' % (seller_sku,shopName))
        elif operation_type == 'upload':
            messages.success(request, u'正在执行上架操作，请稍后刷新页面。。。')
            return HttpResponseRedirect('/Project/admin/skuapp/t_online_info_amazon_listing/?seller_sku=%s&ShopName=%s' % (seller_sku,shopName))
        elif operation_type == 'download':
            messages.success(request, u'正在执行下架操作，请稍后刷新页面。。。')
            return HttpResponseRedirect('/Project/admin/skuapp/t_online_info_amazon_listing/?seller_sku=%s&ShopName=%s' % (seller_sku,shopName))
        elif operation_type == 'change':
            if product_list_obj.sale_from_date:
                sale_from_date_0 = str(product_list_obj.sale_from_date)[0:10]
                sale_from_date_1 = str(product_list_obj.sale_from_date)[11:16]
            else:
                sale_from_date_0 = ''
                sale_from_date_1 = ''

            if product_list_obj.sale_end_date:
                sale_end_date_0 = str(product_list_obj.sale_end_date)[0:10]
                sale_end_date_1 = str(product_list_obj.sale_end_date)[11:16]
            else:
                sale_end_date_0 = ''
                sale_end_date_1 = ''

            parent_asin1 = product_list_obj.Parent_asin
            parent_sku = ''
            if parent_asin1 is not None:
                parent_sku_obj = t_online_info_amazon_listing.objects.filter(asin1=parent_asin1)
                if parent_sku_obj:
                    parent_sku = parent_sku_obj[0].seller_sku

            return render(request, 'product_info_modify_amazon.html', {'product_list_obj': product_list_obj, 'sale_from_date_0':sale_from_date_0, 'sale_from_date_1':sale_from_date_1, 'sale_end_date_0':sale_end_date_0, 'sale_end_date_1':sale_end_date_1, 'parent_sku':parent_sku})
        else:
            pass
    except Exception as e:
        print e
        # traceback.print_exc(file=open('/home/wcx/Project/view.log', 'a'))


def product_info_modify_amazon(request):
    from django.db import connection
    from django.contrib import messages
    from skuapp.table.t_online_info_amazon_listing import *
    from brick.amazon.product_refresh.get_auth_info import GetAuthInfo
    from brick.amazon.product_refresh.generate_feed_xml import GenerateFeedXml
    # from brick.amazon.product_refresh.put_refresh_message_to_rabbitmq import MessageToRabbitMq
    from brick.amazon.upload_product.message_to_rabbitmq import MessageToRabbitMq
    import json
    from brick.amazon.product_refresh.modify_image_before_upload import *
    import datetime

    modify_type = request.POST.get('modify_type')
    pri_id = request.POST.get('pri_id')
    amazon_list_ins = t_online_info_amazon_listing.objects.filter(id=int(pri_id))
    amazon_list_obj = t_online_info_amazon_listing.objects.filter(id=int(pri_id))[0]
    seller_sku = amazon_list_obj.seller_sku
    if modify_type == 'product_info_modify':
        get_auth_info_ins = GetAuthInfo(connection)
        auth_info_product = get_auth_info_ins.get_auth_info_by_shop_name(str(amazon_list_obj.ShopName))
        auth_info_product['IP'] = auth_info_product['ShopIP']
        auth_info_product['table_name'] = 't_online_info_amazon'
        auth_info_product['update_type'] = 'product_info_modify'

        product_info_dic = {}
        item_name = request.POST.get('item_name')
        bullet_point1 = request.POST.get('bullet_point1')
        bullet_point2 = request.POST.get('bullet_point2')
        bullet_point3 = request.POST.get('bullet_point3')
        bullet_point4 = request.POST.get('bullet_point4')
        bullet_point5 = request.POST.get('bullet_point5')
        product_description = request.POST.get('product_description')
        generic_keywords1 = request.POST.get('generic_keywords1')
        generic_keywords2 = request.POST.get('generic_keywords2')
        generic_keywords3 = request.POST.get('generic_keywords3')
        generic_keywords4 = request.POST.get('generic_keywords4')
        generic_keywords5 = request.POST.get('generic_keywords5')
        product_info_dic['seller_sku'] = amazon_list_obj.seller_sku
        product_info_dic['item_name'] = item_name
        product_info_dic['product_description'] = product_description
        product_info_dic['bullet_point1'] = bullet_point1
        product_info_dic['bullet_point2'] = bullet_point2
        product_info_dic['bullet_point3'] = bullet_point3
        product_info_dic['bullet_point4'] = bullet_point4
        product_info_dic['bullet_point5'] = bullet_point5
        product_info_dic['generic_keywords1'] = generic_keywords1
        product_info_dic['generic_keywords2'] = generic_keywords2
        product_info_dic['generic_keywords3'] = generic_keywords3
        product_info_dic['generic_keywords4'] = generic_keywords4
        product_info_dic['generic_keywords5'] = generic_keywords5

        feed_xml_ins = GenerateFeedXml(auth_info_product)
        feed_xml = feed_xml_ins.get_product_xml(product_info_dic)
        auth_info_product['feed_xml'] = feed_xml
        auth_info_product['product_info_dic'] = product_info_dic

        message_to_rabbit_obj = MessageToRabbitMq(auth_info_product, connection)
        auth_info_product = json.dumps(auth_info_product)
        message_to_rabbit_obj.put_message(auth_info_product)
        # put_message_ins = MessageToRabbitMq(auth_info_product, connection)
        # put_message_ins.put_message(str(auth_info_product))
        amazon_list_ins.update(deal_action='product_info_modify',
                                        deal_result=None,
                                        deal_result_info=None,
                                        UpdateTime=datetime.datetime.now())
    elif modify_type == 'product_price_modify':
        price = request.POST.get('standard_price')
        sale_price = request.POST.get('sale_price')
        sale_from_date_0 = request.POST.get('sale_from_date_0')
        sale_from_date_1 = request.POST.get('sale_from_date_1')
        sale_end_date_0 = request.POST.get('sale_end_date_0')
        sale_end_date_1 = request.POST.get('sale_end_date_1')

        if sale_from_date_0 != '' and sale_from_date_1 != '':
            start_date_str = sale_from_date_0 + ' ' + sale_from_date_1
            start_date_time = datetime.datetime.strptime(start_date_str.replace('/', '-'), '%Y-%m-%d %H:%M')
            start_date = (start_date_time + datetime.timedelta(hours=-8)).strftime('%Y-%m-%dT%H:%M:%S')
        else:
            start_date = ''

        if sale_end_date_0 != '' and sale_end_date_1 != '':
            end_date_str = sale_end_date_0 + ' ' + sale_end_date_1
            end_date_time = datetime.datetime.strptime(end_date_str.replace('/', '-'), '%Y-%m-%d %H:%M')
            end_date = (end_date_time + datetime.timedelta(hours=-8)).strftime('%Y-%m-%dT%H:%M:%S')
        else:
            end_date = ''
        get_auth_info_ins = GetAuthInfo(connection)
        auth_info_price = get_auth_info_ins.get_auth_info_by_shop_name(str(amazon_list_obj.ShopName))
        auth_info_price['IP'] = auth_info_price['ShopIP']
        auth_info_price['table_name'] = 't_online_info_amazon'
        auth_info_price['update_type'] = 'product_price_modify'
        auth_info_price['seller_sku'] = str(amazon_list_obj.seller_sku)
        price_info_dic = {}
        price_info_dic['standard_price'] = price
        price_info_dic['sale_price'] = sale_price
        price_info_dic['start_date'] = start_date
        price_info_dic['end_date'] = end_date

        sale_sites = {'US': 'USD', 'DE': 'EUR', 'FR': 'EUR', 'UK': 'GBP', 'AU': 'AUD', 'IN': 'INR'}
        shop_site = amazon_list_obj.ShopSite
        if shop_site in sale_sites.keys():
            currency_type = sale_sites[shop_site]
        else:
            currency_type = 'USD'

        feed_xml_price_obj = GenerateFeedXml(auth_info_price)
        feed_xml_price = feed_xml_price_obj.get_price_xml(auth_info_price['seller_sku'], price, currency_type, start_date,  end_date, sale_price)
        auth_info_price['feed_xml'] = feed_xml_price
        auth_info_price['price_info_dic'] = price_info_dic

        message_to_rabbit_obj = MessageToRabbitMq(auth_info_price, connection)
        auth_info_price = json.dumps(auth_info_price)
        message_to_rabbit_obj.put_message(auth_info_price)

        # put_message_price = MessageToRabbitMq(auth_info_price, connection)
        # put_message_price.put_message(str(auth_info_price))
        amazon_list_ins.update(deal_action='product_price_modify',
                               deal_result=None,
                               deal_result_info=None,
                               UpdateTime=datetime.datetime.now())
    elif modify_type == 'product_image_modify':
        pic_url = None
        shop_name = request.POST.get('shop_name', '')
        parent_sku = request.POST.get('parent_sku', '')
        seller_sku = amazon_list_obj.seller_sku


        if parent_sku is None or parent_sku.strip() == '':
            variation_type = 'parent'
            parent_sku = seller_sku
            child_sku = ''
        else:
            variation_type = 'child'
            child_sku = seller_sku


        # 上传图片
        image_local = request.FILES.get('image_local')
        image_url = request.POST.get('image_url', '')

        # 上传本地照片
        if image_local is not None:
            modify_image_obj = ModifyImageBeforeUpload()
            pic_url = modify_image_obj.upload_image_to_oss(shop_name, image_local, variation_type, 'main', parent_sku, child_sku, 0)

        # 上传图片链接
        if image_url.strip() != '':
            image_bytes = None
            try:
                req = urllib2.Request(image_url)
                image_bytes = urllib2.urlopen(req, timeout=30).read()
            except:
                pass
            if image_bytes is not None:
                modify_image_obj = ModifyImageBeforeUpload()
                pic_url = modify_image_obj.upload_image_to_oss(shop_name, image_bytes, variation_type, 'main', parent_sku, child_sku, 0)
        if pic_url is not None:
            get_auth_info_ins = GetAuthInfo(connection)
            auth_info_image = get_auth_info_ins.get_auth_info_by_shop_name(str(amazon_list_obj.ShopName))
            auth_info_image['IP'] = auth_info_image['ShopIP']
            auth_info_image['table_name'] = 't_online_info_amazon'
            auth_info_image['update_type'] = 'product_image_modify'
            auth_info_image['seller_sku'] = str(amazon_list_obj.seller_sku)
            auth_info_image['pri_id'] = pri_id
            image_info_dic = {}
            image_info_dic['pic_url'] = pic_url

            feed_xml_image_obj = GenerateFeedXml(auth_info_image)
            feed_xml_image = feed_xml_image_obj.get_image_xml(image_info_dic)
            auth_info_image['feed_xml'] = feed_xml_image
            auth_info_image['image_info_dic'] = image_info_dic

            message_to_rabbit_obj = MessageToRabbitMq(auth_info_image, connection)
            auth_info_image = json.dumps(auth_info_image)
            message_to_rabbit_obj.put_message(auth_info_image)

            # put_message_price = MessageToRabbitMq(auth_info_image, connection)
            #             # put_message_price.put_message(str(auth_info_image))
            amazon_list_ins.update(deal_action='product_image_modify',
                                   deal_result=None,
                                   deal_result_info=None,
                                   UpdateTime=datetime.datetime.now())
        else:
            messages.error(request, '图片上传失败')

    # t_online_info_amazon_listing.objects.filter(id=int(pri_id)).update(item_name=item_name,
    #                                                                    bullet_point1=bullet_point1,
    #                                                                    bullet_point2=bullet_point2,
    #                                                                    bullet_point3=bullet_point3,
    #                                                                    bullet_point4=bullet_point4,
    #                                                                    bullet_point5=bullet_point5,
    #                                                                    product_description=product_description,
    #                                                                    price=price,
    #                                                                    sale_price=sale_price,
    #                                                                    generic_keywords1=generic_keywords1,
    #                                                                    generic_keywords2=generic_keywords2,
    #                                                                    generic_keywords3=generic_keywords3,
    #                                                                    generic_keywords4=generic_keywords4,
    #                                                                    generic_keywords5=generic_keywords5
    #                                                                    )


    return HttpResponseRedirect('/Project/admin/skuapp/t_online_info_amazon_listing/?SKU=%s' % seller_sku)




def add_amazon_images(request):
    productSKU = request.GET.get('productSKU', '')
    productItemSku = request.GET.get('productItemSku', '')
    shop_site = 'ShopName=' + request.GET.get('ShopName', '') + '&searchSite=' + request.GET.get('searchSite', '')
    return render(request, 'add_amazon_images.html', {'productSKU':productSKU, 'productItemSku':productItemSku,'shop_site': shop_site})

from brick.public.upload_to_oss import *
from Project.settings import BUCKETNAME_ALL_MAINSKU_PIC
def deal_image(params):
    upload_to_oss_obj = upload_to_oss(BUCKETNAME_ALL_MAINSKU_PIC)
    result = upload_to_oss_obj.upload_to_oss(params=params)
    image_urls = {'image_url': '', 'errorInfo': ''}
    if result['errorcode'] == 0:
        image_urls['image_url'] = result['result']
    else:
        image_urls['errorInfo'] = result['errortext']
    return image_urls

def save_amazon_images(request):
    postImage = request.FILES
    mainImage = postImage.get('main_image_url', '')
    other_image_url1 = postImage.get('other_image_url1', '')
    other_image_url2 = postImage.get('other_image_url2', '')
    other_image_url3 = postImage.get('other_image_url3', '')
    other_image_url4 = postImage.get('other_image_url4', '')
    other_image_url5 = postImage.get('other_image_url5', '')
    other_image_url6 = postImage.get('other_image_url6', '')
    other_image_url7 = postImage.get('other_image_url7', '')
    other_image_url8 = postImage.get('other_image_url8', '')
    productSKU = request.POST.get('productSKU', '').strip()
    productItemSku = request.POST.get('productItemSku', '')
    shop_site = request.POST.get('ShopSets', '') + '-' + request.GET.get('searchSite', '')
    imagePath = productSKU + '/Amazon/' + shop_site
    imageFileFirstName = productSKU
    if productItemSku:
        imageFileFirstName += '_' + productItemSku.strip()
    imageFileEndName = '.jpg'
    main_image_url_name = imageFileFirstName + imageFileEndName
    image_urls = deal_image({'path': imagePath,'name': main_image_url_name, 'byte': mainImage, 'del': 1})
    main_image_url = image_urls['image_url']
    if main_image_url == '':
        messages.error(request,
                       'upload image(main_image_url) to oss failed, the reason is "%s"' % image_urls['errorInfo'])

    other_image_url_list = {'other_image_url1': other_image_url1, 'other_image_url2': other_image_url2,
                            'other_image_url3': other_image_url3, 'other_image_url4': other_image_url4,
                            'other_image_url5': other_image_url5, 'other_image_url6': other_image_url6,
                            'other_image_url7': other_image_url7, 'other_image_url8': other_image_url8, }
    num_count = 1
    for k, v in other_image_url_list.items():
        if v:
            main_image_url_name = imageFileFirstName + '_' + str(num_count) + imageFileEndName
            image_urls = deal_image({'path': imagePath,'name': main_image_url_name, 'byte': v, 'del': 1})
            other_image_url_list[k] = image_urls['image_url']
            num_count += 1
            if v == '':
                messages.error(request,
                               'upload image('+ k +') to oss failed, the reason is "%s"' % image_urls[
                                   'errorInfo'])

    other_image_url_list['main_image_url'] = main_image_url
    image_ur_str = str(other_image_url_list)
    return render(request, 'save_amazon_images.html', {'other_image_url_list': other_image_url_list, 'image_ur_str': image_ur_str})

def show_amazon_schedule(request):
    """展示Amazon刊登计划"""
    myId = eval(request.GET.get('myId', ''))
    url = request.get_full_path()
    params = ''
    if 'param' in url:
        params = url.split('param=')[-1]


    if isinstance(myId, int):
        amazon_wait_upload_objs = t_templet_amazon_wait_upload.objects.filter(id=myId)
        if amazon_wait_upload_objs.exists():
            obj = amazon_wait_upload_objs[0]
            schedule = {}

            if obj.ShopSets == None:
                shops = ''
            else:
                shops = obj.ShopSets

            schedule['shops'] = shops
        flag = 1
        id_flag = 1

    else:
        schedule = {'shops':'', 'start':'已自动分配'}
        myId = ','.join(myId)
        flag = 2
        id_flag = 2
    return render(request, 'show_amazon_schedule.html', {'schedule':schedule, 'myId':myId, 'flag':flag,
                                                       'id_flag':id_flag, 'param':params})

def save_amazon_schedule(request):
    from datetime import datetime
    post = request.POST
    user = request.user.first_name
    time = datetime.now()
    shops = post.get('shops', '')
    param = post.get('param', '')

    myId = eval(post.get('myId', ''))

    if shops == '':
        rt = u'铺货数量和铺货店铺不能都为空!'
        return render(request, 'SKU.html', {'rt': rt})

    else:

        # 所有店铺名的列表
        ShopName_list = []
        t_upload_shopname_objs = t_upload_shopname.objects.values('ShopName')
        for t_upload_shopname_obj in t_upload_shopname_objs:
            ShopName_list.append(t_upload_shopname_obj['ShopName'][-4:])

        shops = shops
        if isinstance(myId, int):
            shopAlias = t_config_shop_alias.objects.filter(ShopName=shops)[0].ShopAlias
            item_name = shopAlias + ' ' + t_templet_amazon_wait_upload.objects.filter(id=int(myId))[0].item_name

            update_sites = {'US': 'Update', 'DE': 'Aktualisierung', 'FR': 'Actualisation', 'UK': 'Update'}
            shipping_group_sites = {'US': 'Migrated Template', 'DE': u'默认模板', 'FR': 'Modèle par défaut Amazon',
                                    'UK': 'Migrated Template'}
            site = shops.split('-')[-1].split('/')[0]
            t_templet_amazon_wait_upload.objects.filter(id=int(myId)).update(ShopSets=shops,manufacturer=shopAlias,brand_name=shopAlias,item_name=item_name,
                                                                             updateUser=user, updateTime=time,update_delete=update_sites[site],
                                                                             merchant_shipping_group_name=shipping_group_sites[site])
            rt = u'修改成功！'
            return render(request, 'SKU.html', {'rt': rt})

        else:
            for each in myId:
                obj = t_templet_amazon_wait_upload.objects.filter(id=int(each))
                obj.update(ShopSets=shops, updateUser=user, updateTime=time)
            return HttpResponseRedirect('%s' % param)

def select_amazon_menu_bak(request):
    groupRoot = request.GET.get('groupRoot', '').replace('RBNAND', '&')
    group2 = request.GET.get('group2', '').replace('RBNAND', '&')
    group3 = request.GET.get('group3', '').replace('RBNAND', '&')
    group4 = request.GET.get('group4', '').replace('RBNAND', '&')
    group5 = request.GET.get('group5', '').replace('RBNAND', '&')
    group6 = request.GET.get('group6', '').replace('RBNAND', '&')
    group7 = request.GET.get('group7', '').replace('RBNAND', '&')
    group8 = request.GET.get('group8', '').replace('RBNAND', '&')
    searchSite = request.GET.get('searchSite', '')
    itemType = request.GET.get('itemType', '')
    uploadProductType = request.GET.get('uploadProductType', '')
    url = request.path + '?'
    if searchSite is None or searchSite.strip() == '':
        searchSite = 'US'
    if itemType:
        url += 'itemType=' + itemType + '&'
    if uploadProductType:
        url += 'uploadProductType=' + uploadProductType + '&'
    t_config_apiurl_amazon_objs = t_config_apiurl_amazon.objects.filter(site=searchSite)
    if itemType:
        t_config_apiurl_amazon_objs = t_config_apiurl_amazon_objs.filter(item_type__icontains=itemType)
    t_config_apiurl_amazon_objs_1 = t_config_apiurl_amazon_objs.values("groupRoot").distinct()
    groupRoots = []
    for t_config_apiurl_amazon_obj_1 in t_config_apiurl_amazon_objs_1:
        if t_config_apiurl_amazon_obj_1 and t_config_apiurl_amazon_obj_1['groupRoot'] not in groupRoots:
            groupRoots.append(t_config_apiurl_amazon_obj_1['groupRoot'])
    recommended_browse_nodes_str = ''
    last_group = '0'
    group2s = []
    if groupRoot:
        recommended_browse_nodes_str += groupRoot
        url += 'groupRoot=' + groupRoot.replace('&', 'RBNAND')
        t_config_apiurl_amazon_objs = t_config_apiurl_amazon_objs.filter(groupRoot__exact=groupRoot)\
            .values('group2','RootID','item_type').distinct()
        for t_config_apiurl_amazon_obj in t_config_apiurl_amazon_objs:
            if t_config_apiurl_amazon_obj['group2'] not in group2s and t_config_apiurl_amazon_obj['group2']:
                group2s.append(t_config_apiurl_amazon_obj['group2'])
        if len(group2s) == 0:
            last_group = '1'
    group3s = []
    if group2:
        recommended_browse_nodes_str += '>' + group2
        url += '&group2=' + group2.replace('&', 'RBNAND')
        t_config_apiurl_amazon_objs = t_config_apiurl_amazon_objs.filter(group2__exact=group2)\
            .values('group3', 'groupRoot','RootID','item_type').distinct()
        for t_config_apiurl_amazon_obj in t_config_apiurl_amazon_objs:
            if t_config_apiurl_amazon_obj['group3'] not in group3s and t_config_apiurl_amazon_obj['group3']:
                group3s.append(t_config_apiurl_amazon_obj['group3'])
        if len(group3s) == 0:
            last_group = '1'
    group4s = []
    if group3:
        recommended_browse_nodes_str += '>' + group3
        url += '&group3=' + group3.replace('&', 'RBNAND')
        t_config_apiurl_amazon_objs = t_config_apiurl_amazon_objs.filter(group3__exact=group3)\
            .values('group4','RootID','item_type').distinct()
        for t_config_apiurl_amazon_obj in t_config_apiurl_amazon_objs:
            if t_config_apiurl_amazon_obj['group4'] not in group4s and t_config_apiurl_amazon_obj['group4']:
                group4s.append(t_config_apiurl_amazon_obj['group4'])
        if len(group4s) == 0:
            last_group = '1'
    group5s = []
    if group4:
        recommended_browse_nodes_str += '>' + group4
        url += '&group4=' + group4.replace('&', 'RBNAND')
        t_config_apiurl_amazon_objs = t_config_apiurl_amazon_objs.filter(group4__exact=group4)\
            .values('group5','RootID','item_type').distinct()
        for t_config_apiurl_amazon_obj in t_config_apiurl_amazon_objs:
            if t_config_apiurl_amazon_obj['group5'] not in group5s  and t_config_apiurl_amazon_obj['group5']:
                group5s.append(t_config_apiurl_amazon_obj['group5'])
        if len(group5s) == 0:
            last_group = '1'
    group6s = []
    if group5:
        recommended_browse_nodes_str += '>' + group5
        url += '&group5=' + group5.replace('&', 'RBNAND')
        t_config_apiurl_amazon_objs = t_config_apiurl_amazon_objs.filter(group5__exact=group5)\
            .values('group6','RootID','item_type').distinct()
        for t_config_apiurl_amazon_obj in t_config_apiurl_amazon_objs:
            if t_config_apiurl_amazon_obj['group6'] not in group6s and t_config_apiurl_amazon_obj['group6']:
                group6s.append(t_config_apiurl_amazon_obj['group6'])
        if len(group6s) == 0:
            last_group = '1'
    group7s = []
    if group6:
        recommended_browse_nodes_str += '>' + group6
        url += '&group6=' + group6.replace('&', 'RBNAND')
        t_config_apiurl_amazon_objs = t_config_apiurl_amazon_objs.filter(group6__exact=group6)\
            .values('group7','RootID','item_type').distinct()
        for t_config_apiurl_amazon_obj in t_config_apiurl_amazon_objs:
            if t_config_apiurl_amazon_obj['group7'] not in group7s and t_config_apiurl_amazon_obj['group7']:
                group7s.append(t_config_apiurl_amazon_obj['group7'])
        if len(group7s) == 0:
            last_group = '1'
    group8s = []
    if group7:
        recommended_browse_nodes_str += '>' + group7
        url += '&group7=' + group7.replace('&', 'RBNAND')
        t_config_apiurl_amazon_objs = t_config_apiurl_amazon_objs.filter(group7__exact=group7)\
            .values('group8','RootID','item_type').distinct()
        for t_config_apiurl_amazon_obj in t_config_apiurl_amazon_objs:
            if t_config_apiurl_amazon_obj['group8'] not in group8s and t_config_apiurl_amazon_obj['group8']:
                group8s.append(t_config_apiurl_amazon_obj['group8'])
        if len(group8s) == 0:
            last_group = '1'
    if group8:
        recommended_browse_nodes_str += '>' + group8
        t_config_apiurl_amazon_objs = t_config_apiurl_amazon_objs.filter(group8__exact=group8).values('RootID')
    tid = 0
    if len(t_config_apiurl_amazon_objs) == 1:
        tid = t_config_apiurl_amazon_objs[0]['RootID']
        itemType = t_config_apiurl_amazon_objs[0]['item_type']
    product_types = t_template_product_config_amazon.objects.values('product_type')
    # messages.error(request,product_types)
    all_product_type = []
    need_not_done = ['CameraPhoto', 'EntertainmentCollectibles', 'Tools', 'FoodAndBeverages', 'Gourmet',
                     'Computers', 'TiresAndWheels', 'Music', 'Video', 'LargeAppliances', 'LabSupplies',
                     'Industrial', 'MaterialHandling', 'WineAndAlcohol', 'CE', 'SWVG']
    for product_type in product_types:
        if product_type['product_type'] not in need_not_done:
            all_product_type.append(product_type['product_type'])
    recommended_browse_nodes_str = recommended_browse_nodes_str.replace('&', 'RBNAND')

    return render(request, 'select_menu_amazon.html', {'groupRoot':groupRoot, 'group2': group2, 'group3': group3, 'group4': group4,
                                                       'group5': group5, 'group6': group6, 'group7': group7, 'group8': group8,
                                                       'groupRoots':groupRoots, 'group2s': group2s, 'group3s': group3s, 'group4s': group4s,
                                                       'group5s': group5s, 'group6s': group6s, 'group7s': group7s, 'group8s': group8s,
                                                      'url': url,'t_config_apiurl_amazon_objs':t_config_apiurl_amazon_objs, 'tid': tid,
                                                       'recommended_browse_nodes_str': recommended_browse_nodes_str,'itemType': itemType,
                                                       'all_product_type': all_product_type, 'uploadProductType': uploadProductType,
                                                       'searchSite': searchSite, 'last_group': last_group})

def select_amazon_menu(request):
    from skuapp.table.t_sys_param import t_sys_param
    from skuapp.table.t_config_apiurl_amazon_new import *
    item_key_word = request.GET.get('item_key_word', '')
    groupRoot = request.GET.get('groupRoot', '').replace('RBNAND', '&')
    group_selected = request.GET.get('group_selected', '').replace('RBNAND', '&')
    product_type_select = request.GET.get('product_type_select', '')
    searchSite = request.GET.get('searchSite', '')
    itemType = request.GET.get('itemType', '')
    root_id = request.GET.get('root_id', '')
    uploadProductType = request.GET.get('uploadProductType', '')
    url = request.path + '?'

    product_types = t_template_product_config_amazon.objects.values('product_type')
    all_product_type = []
    need_not_done = ['CameraPhoto', 'EntertainmentCollectibles', 'Tools', 'FoodAndBeverages', 'Gourmet',
                     'Computers', 'TiresAndWheels', 'Music', 'Video', 'LargeAppliances', 'LabSupplies',
                     'Industrial', 'MaterialHandling', 'WineAndAlcohol', 'CE', 'SWVG']
    for product_type in product_types:
        if product_type['product_type'] not in need_not_done:
            all_product_type.append(product_type['product_type'])

    product_sites = t_sys_param.objects.filter(Type=350).exclude(Seq=0).values_list('V', 'VDesc').order_by('Seq')
    all_product_site =[]
    for product_site in product_sites:
        all_product_site.append([product_site[0], product_site[1]])

    group_all = []
    if searchSite is None or searchSite.strip() == '' or item_key_word is None or item_key_word.strip() == '':
        pass
    else:
        t_config_apiurl_amazon_new_objs = t_config_apiurl_amazon_new.objects.filter(site=searchSite)
        # if itemType:
        #     t_config_apiurl_amazon_new_objs = t_config_apiurl_amazon_new_objs.filter(item_type__icontains=itemType)
        # t_config_apiurl_amazon_new_objs_all = t_config_apiurl_amazon_new_objs.filter(group_all__icontains=item_key_word).values("group_all")
        t_config_apiurl_amazon_new_objs_all = t_config_apiurl_amazon_new_objs.filter(category__icontains=item_key_word).values_list("RootID","group_all","item_type")
        for t_config_apiurl_amazon_new_each in t_config_apiurl_amazon_new_objs_all:
            # group_all.append(t_config_apiurl_amazon_new_each['group_all'])
            group_all.append([t_config_apiurl_amazon_new_each[0], t_config_apiurl_amazon_new_each[1], t_config_apiurl_amazon_new_each[2]])
    return render(request, 'select_menu_amazon.html', {'url':url, 'groupRoot':groupRoot, 'itemType': itemType, 'root_id':root_id,'uploadProductType': uploadProductType,'searchSite': searchSite, 'all_product_site':all_product_site,'all_product_type': all_product_type, 'group_all':group_all,'item_key_word':item_key_word, 'group_selected':group_selected, 'product_type_select':product_type_select})


def validation_amazon_product_data(obj):
    is_all_data_done = 1
    department_name_list = ['ClothingAccessories', 'ProductClothing', 'Jewelry']
    product_subtype_list = ['ClothingAccessories', 'ProductClothing', 'AutoAccessory', 'MechanicalFasteners']
    clothing_list = ['ClothingAccessories', 'ProductClothing']
    unit_count_list = ['Health', 'Beauty', 'LuxuryBeauty','Baby']
    upload_product_type = obj.upload_product_type
    prodcut_variation_id = obj.prodcut_variation_id
    main_image_url = obj.main_image_url
    deal_result = u'待完善字段：'
    if obj.recommended_browse_nodes is None or obj.recommended_browse_nodes.strip() == '':
        is_all_data_done = -1
        deal_result += u'商品类型,'
    if obj.ShopSets is None or obj.ShopSets.strip() == '':
        is_all_data_done = -1
        deal_result += u'待刊登店铺,'
    if '---' in obj.ShopSets:
        is_all_data_done = -1
        deal_result += u'待刊登店铺,'
    if obj.merchant_shipping_group_name is None or obj.merchant_shipping_group_name.strip() == '':
        is_all_data_done = -1
        deal_result += u'运输模板,'
    if obj.item_name is None or obj.item_name.strip() == '':
        is_all_data_done = -1
        deal_result += u'产品标题,'
    if obj.productSKU is None or obj.productSKU.strip() == '':
        is_all_data_done = -1
        deal_result += u'商品SKU,'
    if obj.quantity is None or str(obj.quantity).strip() == '':
        is_all_data_done = -1
        deal_result += u'产品数量,'
    if obj.item_package_quantity is None or str(obj.item_package_quantity).strip() == '':
        is_all_data_done = -1
        deal_result += u'包装数,'
    if obj.external_product_id_type is None or obj.external_product_id_type.strip() == '':
        is_all_data_done = -1
        deal_result += u'产品ID类型,'
    if obj.condition_type is None or obj.condition_type.strip() == '':
        is_all_data_done = -1
        deal_result += u'产品新旧,'
    if obj.bullet_point1 is None or obj.bullet_point1.strip() == '':
        is_all_data_done = -1
        deal_result += u'产品描述1,'
    if obj.bullet_point2 is None or obj.bullet_point2.strip() == '':
        is_all_data_done = -1
        deal_result += u'产品描述2,'
    if obj.bullet_point3 is None or obj.bullet_point3.strip() == '':
        is_all_data_done = -1
        deal_result += u'产品描述3,'
    if obj.bullet_point4 is None or obj.bullet_point4.strip() == '':
        is_all_data_done = -1
        deal_result += u'产品描述4,'
    if obj.bullet_point5 is None or obj.bullet_point5.strip() == '':
        is_all_data_done = -1
        deal_result += u'产品描述5,'
    if obj.product_description is None or obj.product_description.strip() == '':
        is_all_data_done = -1
        deal_result += u'产品描述,'
    if obj.standard_price is None or str(obj.standard_price).strip() == '':
        is_all_data_done = -1
        deal_result += u'商品价格,'
    if obj.mfg_minimum is None or str(obj.mfg_minimum).strip() == '':
        is_all_data_done = -1
        deal_result += u'最小使用年龄,'
    if obj.mfg_minimum_unit_of_measure is None or obj.mfg_minimum_unit_of_measure.strip() == '':
        is_all_data_done = -1
        deal_result += u'年龄单位,'
    if obj.generic_keywords1 is None or obj.generic_keywords1.strip() == '':
        is_all_data_done = -1
        deal_result += u'关键词1,'
    # if obj.generic_keywords2 is None or obj.generic_keywords2.strip() == '':
    #     is_all_data_done = -1
    #     deal_result += u'关键词2,'
    # if obj.generic_keywords3 is None or obj.generic_keywords3.strip() == '':
    #     is_all_data_done = -1
    #     deal_result += u'关键词3,'
    # if obj.generic_keywords4 is None or obj.generic_keywords4.strip() == '':
    #     is_all_data_done = -1
    #     deal_result += u'关键词4,'
    # if obj.generic_keywords5 is None or obj.generic_keywords5.strip() == '':
    #     is_all_data_done = -1
    #     deal_result += u'关键词5,'
    if (obj.feed_product_type is None or obj.feed_product_type.strip() == '') and obj.upload_product_type not in ('ProductClothing', 'ClothingAccessories'):
        is_all_data_done = -1
        deal_result += u'商品种类,'
    if obj.upload_product_type is None or obj.upload_product_type.strip() == '':
        is_all_data_done = -1
        deal_result += u'刊登种类,'
    if 'IN' in obj.ShopSets.split('-')[-1]:
        if obj.mrp is None or str(obj.mrp).strip() == '':
            is_all_data_done = -1
            deal_result += u'最大销售价格(MRP),'
        if obj.fulfillment_latency is None or str(obj.fulfillment_latency).strip() == '':
            is_all_data_done = -1
            deal_result += u'产品处理时间,'
        if upload_product_type == 'Home':
            if obj.homes_size is None or str(obj.homes_size).strip() == '':
                is_all_data_done = -1
                deal_result += u'家居品尺寸(IN),'
            if obj.homes_color is None or str(obj.homes_color).strip() == '':
                is_all_data_done = -1
                deal_result += u'家居品颜色(IN),'
        if upload_product_type == 'Sports':
            if obj.item_type_name is None or str(obj.item_type_name).strip() == '':
                is_all_data_done = -1
                deal_result += u'产品类型,'
        if upload_product_type == 'ProductClothing':
            if obj.clothing_size is None or str(obj.clothing_size).strip() == '':
                is_all_data_done = -1
                deal_result += u'服装尺寸,'
            if obj.clothing_color is None or str(obj.clothing_color).strip() == '':
                is_all_data_done = -1
                deal_result += u'服装颜色,'
            if obj.fit_type is None or str(obj.fit_type).strip() == '':
                is_all_data_done = -1
                deal_result += u'服装适合类型(IN),'
            if obj.material_type is None or str(obj.material_type).strip() == '':
                is_all_data_done = -1
                deal_result += u'材料种类,'
            if obj.sleeve_type is None or str(obj.sleeve_type).strip() == '':
                is_all_data_done = -1
                deal_result += u'服装袖筒类型(IN),'
        if upload_product_type == 'Office':
            if obj.item_type_name is None or str(obj.item_type_name).strip() == '':
                is_all_data_done = -1
                deal_result += u'产品类型,'
            if obj.warranty_description is None or str(obj.warranty_description).strip() == '':
                is_all_data_done = -1
                deal_result += u'制造商保修说明,'
        if upload_product_type == 'Toys' or upload_product_type == 'ToysBaby':
            if obj.toy_color is None or str(obj.toy_color).strip() == '':
                is_all_data_done = -1
                deal_result += u'玩具颜色(IN),'
    if 'DE' in obj.ShopSets.split('-')[-1]:
        if upload_product_type == 'ProductClothing':
            if obj.season is None or str(obj.season).strip() == '':
                is_all_data_done = -1
                deal_result += u'季节(德法),'
            if obj.material_composition is None or str(obj.material_composition).strip() == '':
                is_all_data_done = -1
                deal_result += u'材料成分(德法),'
    else:
        if upload_product_type in department_name_list:
            department_name1 = obj.department_name1
            if department_name1 is None or department_name1.strip() == '':
                is_all_data_done = -1
                deal_result += u'适用性别1,'
        if upload_product_type in product_subtype_list:
            product_subtype = obj.product_subtype
            if product_subtype is None or product_subtype.strip() == '':
                is_all_data_done = -1
                deal_result += u'服装类型,'
        if upload_product_type in clothing_list:
            clothing_size = obj.clothing_size
            clothing_color = obj.clothing_color
            if clothing_size is None or clothing_size.strip() == '':
                is_all_data_done = -1
                deal_result += u'服装尺寸,'
            if clothing_color is None or clothing_color.strip() == '':
                is_all_data_done = -1
                deal_result += u'服装颜色,'
        if upload_product_type in unit_count_list:
            unit_count = obj.unit_count
            unit_count_type = obj.unit_count_type
            if unit_count is None or unit_count.strip() == '':
                is_all_data_done = -1
                deal_result += u'单位数量,'
            if unit_count_type is None or unit_count_type.strip() == '':
                is_all_data_done = -1
                deal_result += u'单位名称,'
        if upload_product_type == 'Home' or upload_product_type == 'Jewelry':
            material = obj.material_type
            if material is None or material.strip() == '':
                is_all_data_done = -1
                deal_result += u'材料种类,'
        if upload_product_type == 'Jewelry':
            metal = obj.metal_type
            item_shape = obj.item_shape
            if metal is None or metal.strip() == '':
                is_all_data_done = -1
                deal_result += u'金属类型,'
        if upload_product_type == 'Luggage':
            item_weight = str(obj.item_weight)
            item_weight_unit  = obj.item_weight_unit
            color_name_public = obj.color_name_public
            if item_weight is None or item_weight.strip() == '':
                is_all_data_done = -1
                deal_result += u'重量,'
            if item_weight_unit is None or item_weight_unit.strip() == '':
                is_all_data_done = -1
                deal_result += u'重量单位,'
            if color_name_public is None or color_name_public.strip() == '':
                is_all_data_done = -1
                deal_result += u'颜色,'
        # if item_shape is None or item_shape.strip() == '':
        #     is_all_data_done = -1
    variation_objs = t_templet_amazon_published_variation.objects.filter(
        prodcut_variation_id=prodcut_variation_id)
    if variation_objs.exists():
        count = 1
        for variation_obj in variation_objs:
            if variation_obj.main_image_url is None or str(variation_obj.main_image_url).strip()=='':
                is_all_data_done = -1
                deal_result += u'变体%s主图,'%count
            if variation_obj.item_quantity is None or str(variation_obj.item_quantity).strip()=='' or str(variation_obj.item_quantity) == '0':
                is_all_data_done = -1
                deal_result += u'变体%s包装数,'%count
            if variation_obj.productSKU is None or str(variation_obj.productSKU).strip() == '':
                is_all_data_done = -1
                deal_result += u'变体%s商品SKU,'%count
            if variation_obj.price is None or str(variation_obj.price).strip() == '' or str(variation_obj.price) == '0.00':
                is_all_data_done = -1
                deal_result += u'变体%s价格,'%count
            if 'Color' in variation_obj.variation_theme:
                if variation_obj.color_name is None or str(variation_obj.color_name).strip() == '' or \
                   variation_obj.color_map is None or str(variation_obj.color_map).strip() == '':
                    is_all_data_done = -1
                    deal_result += u'变体%s颜色名称,'%count
            if 'Size' in variation_obj.variation_theme:
                if variation_obj.size_name is None or str(variation_obj.size_name).strip() == '' or \
                   variation_obj.size_map is None or str(variation_obj.size_map).strip() == '':
                    is_all_data_done = -1
                    deal_result += u'变体%s尺寸名称,'%count
                if upload_product_type == 'Luggage' and (variation_obj.color_name is None or str(variation_obj.color_name).strip() == '' or variation_obj.color_map is None or str(variation_obj.color_map).strip() == ''):
                    is_all_data_done = -1
                    deal_result += u'变体%s颜色名称,'%count
            if 'MetalType' in variation_obj.variation_theme:
                if variation_obj.MetalType is None or str(variation_obj.MetalType).strip() == '':
                    is_all_data_done = -1
                    deal_result += u'变体%s材质,'%count
            count += 1
    else:
        if main_image_url is None or str(main_image_url).strip() == '':
            is_all_data_done = -1
            deal_result += u'主图,'
    if deal_result:
        deal_result = deal_result[:-1]
    return is_all_data_done, deal_result

def validation_UPC(upc):
    is_repeat = 0
    t_templet_amazon_wait_upload_objs = t_templet_amazon_wait_upload.objects.filter(external_product_id=upc)
    t_templet_amazon_published_variation_objs = t_templet_amazon_published_variation.objects.filter(external_product_id=upc)
    if t_templet_amazon_published_variation_objs:
        is_repeat = 1
    if t_templet_amazon_wait_upload_objs:
        is_repeat = 1
    return is_repeat

def edit_amazon_variation(request):
    prodcut_variation_id = request.GET.get('prodcut_variation_id', '')
    productSKU = request.GET.get('productSKU', '')
    sizeCount = request.GET.get('sizeCount','')
    update_view = 0
    t_templet_amazon_wait_upload_obj = t_templet_amazon_collection_box.objects.filter(prodcut_variation_id=prodcut_variation_id)[0]
    t_templet_amazon_wait_upload_objs = t_templet_amazon_wait_upload.objects.filter(prodcut_variation_id=prodcut_variation_id)
    if t_templet_amazon_wait_upload_objs.exists():
        t_templet_amazon_wait_upload_obj = t_templet_amazon_wait_upload_objs[0]
    feedPtype = t_templet_amazon_wait_upload_obj.feed_product_type
    if sizeCount:
        t_templet_amazon_published_variation_objs = t_templet_amazon_published_variation.objects.filter(
            prodcut_variation_id=prodcut_variation_id)
        old_variation_ids = []
        for t_templet_amazon_published_variation_obj in t_templet_amazon_published_variation_objs:
            old_variation_ids.append(str(int(t_templet_amazon_published_variation_obj.id)))
        variation_ids = request.POST.getlist('variation_id', '')
        del_variation_ids = list(set(old_variation_ids).difference(set(variation_ids)))
        variation_themes = request.POST.getlist('variation_theme', '')
        productSKUs = request.POST.getlist('product_SKU', '')
        color_names = request.POST.getlist('color_name', '')
        size_names = request.POST.getlist('size_name', '')
        MetalTypes = request.POST.getlist('MetalType', '')
        item_quantitys = request.POST.getlist('item_quantity', '')
        prices = request.POST.getlist('price', '')
        for i in range(0,len(variation_ids)):
            if variation_ids[i] == 'new_add':
                t_templet_amazon_published_variation_obj = t_templet_amazon_published_variation()
                t_templet_amazon_published_variation_obj.relationship_type = 'variation'
                t_templet_amazon_published_variation_obj.item_quantity = item_quantitys[i]
                t_templet_amazon_published_variation_obj.variation_theme = variation_themes[i]
                t_templet_amazon_published_variation_obj.parent_child = 'child'
                t_templet_amazon_published_variation_obj.parent_item_sku = productSKU
                t_templet_amazon_published_variation_obj.productSKU = productSKUs[i]
                t_templet_amazon_published_variation_obj.color_name = color_names[i]
                t_templet_amazon_published_variation_obj.size_name = size_names[i]
                t_templet_amazon_published_variation_obj.color_map = color_names[i]
                t_templet_amazon_published_variation_obj.MetalType = MetalTypes[i]
                t_templet_amazon_published_variation_obj.size_map = size_names[i]
                t_templet_amazon_published_variation_obj.price = prices[i]
                t_templet_amazon_published_variation_obj.prodcut_variation_id = prodcut_variation_id
                t_templet_amazon_published_variation_obj.save()
            else:
                t_templet_amazon_published_variation_obj = t_templet_amazon_published_variation.objects.filter(id=variation_ids[i])[0]
                t_templet_amazon_published_variation_obj.variation_theme = variation_themes[i]
                t_templet_amazon_published_variation_obj.productSKU = productSKUs[i]
                t_templet_amazon_published_variation_obj.color_name = color_names[i]
                t_templet_amazon_published_variation_obj.size_name = size_names[i]
                t_templet_amazon_published_variation_obj.color_map = color_names[i]
                t_templet_amazon_published_variation_obj.size_map = size_names[i]
                t_templet_amazon_published_variation_obj.MetalType = MetalTypes[i]
                t_templet_amazon_published_variation_obj.price = prices[i]
                t_templet_amazon_published_variation_obj.item_quantity = item_quantitys[i]
                t_templet_amazon_published_variation_obj.save()
        # t_templet_amazon_published_variation.s()
        if del_variation_ids:
            for del_variation_id in del_variation_ids:
                t_templet_amazon_published_variation.objects.filter(id=del_variation_id).delete()
        t_templet_amazon_published_variation_objs = t_templet_amazon_published_variation.objects.filter(
            prodcut_variation_id=prodcut_variation_id)
        update_view = 1
        is_all_data_done, deal_result = validation_amazon_product_data(t_templet_amazon_wait_upload_obj)
        if is_all_data_done == 1:
            t_templet_amazon_wait_upload_obj.can_upload = '0'
            deal_result = ''
        else:
            t_templet_amazon_wait_upload_obj.can_upload = '-1'
        t_templet_amazon_wait_upload_obj.remark = deal_result
        t_templet_amazon_wait_upload_obj.save()
    else:
        if prodcut_variation_id:
            t_templet_amazon_published_variation_objs = t_templet_amazon_published_variation.objects.filter(prodcut_variation_id=prodcut_variation_id)

    size_color_list = ["Hardware", "Tools", "MajorHomeAppliances", "OrganizersAndStorage"]
    color_list = ["LightsAndFixtures", "OfficePhone", "OfficePrinter", "OfficeScanner", "VoiceRecorder",
                  "PowersportsVehicle",
                  "Autooil", "CleaningOrRepairKit", "Autobattery", "WirelessAccessories",
                  "BrassAndWoodwindInstruments", "Guitars", "KeyboardInstruments",
                  "MiscWorldInstruments", "SoundAndRecordingEquipment"]
    color_metalType_list = ["FineOther", "FineEarring", "FineNecklaceBraceletAnklet", "FashionOther",
                            "FashionEarring", "FashionNecklaceBraceletAnklet"]
    jewelry_list = []
    size_metalType_list = ["FineRing", "FashionRing"]
    select_type = 0
    if feedPtype:
        if feedPtype in size_color_list:
            select_type = 1
        if feedPtype in color_list:
            select_type = 2
        if feedPtype in color_metalType_list:
            select_type = 3
        if feedPtype in jewelry_list:
            select_type = 4
        if feedPtype in size_metalType_list:
            select_type = 5
    sizeCount = len(t_templet_amazon_published_variation_objs)
    return render(request, 'edit_amazon_variation.html', {'objs': t_templet_amazon_published_variation_objs, 'sizeCount': sizeCount,
                                                          'prodcut_variation_id': prodcut_variation_id, 'select_type': select_type,
                                                          'update_view': update_view, 'productSKU': productSKU})






def chioce_large_small(request):
    from skuapp.table.t_Large_Small_Corresponding_Cate import t_Large_Small_Corresponding_Cate
    objs = t_Large_Small_Corresponding_Cate.objects.values_list('LCode','LargeClass').distinct().order_by('LargeClass')
    largecate_dict = {}
    large_list = []
    for obj in objs:
        if obj[1] is not None:
            large_list.append(obj[1])
            largecate_dict[obj[1]] = obj[0]
    return render(request, 'Large_Small_To_Chioce.html',{'largecate': largecate_dict,'large_list':large_list})
    
def select_smallcate_by_large(request):
    from django.http import JsonResponse
    from skuapp.table.t_Large_Small_Corresponding_Cate import t_Large_Small_Corresponding_Cate

    largecate = request.GET.get('largecate','')
    sResult = {}
    try:
        objs = t_Large_Small_Corresponding_Cate.objects.filter(LCode = largecate).values_list('SCode','SmallClass')
        smallcate = []
        for obj in objs:
            smallcate.append({'SCode':obj[0],'SmallClass':obj[1]})
        # WXL   无小类
        smallcate.append({'SCode':'WXL','SmallClass':'无小类'})
        sResult['resultCode'] = '0'
        sResult['smallcate'] = smallcate
    except:
        sResult['resultCode'] = '-1'
    return JsonResponse(sResult)

def chioce_three_cate_of_clothing(request):
    from skuapp.table.t_Three_Grade_Classification_Of_Clothing import t_Three_Grade_Classification_Of_Clothing
    first_objs = t_Three_Grade_Classification_Of_Clothing.objects.values_list('CateOne').order_by('id')
    first_list = []
    first_dict = {}
    for first_obj in first_objs:
        if first_obj[0] not in first_list:
            first_list.append(first_obj[0])
            first_dict[first_obj[0]] = first_obj[0]
    return render(request, 'Three_Grade_Classification_Of_Clothing_Chioce.html', {'first_list': first_list, 'first_dict': first_dict})
    
def select_next_cate(request):
    from skuapp.table.t_Three_Grade_Classification_Of_Clothing import t_Three_Grade_Classification_Of_Clothing
    sResult = {}
    try:
        objs = None
        CateOne = request.GET.get('CateOne', '')
        if CateOne != '':
            objs = t_Three_Grade_Classification_Of_Clothing.objects.filter(CateOne=CateOne).values_list('CateTwo').order_by('id')
        CateTwo = request.GET.get('CateTwo', '')
        if CateTwo != '':
            objs = t_Three_Grade_Classification_Of_Clothing.objects.filter(CateTwo=CateTwo).values_list('CateThree').order_by('id')
        if objs is not None:
            nextcate = []
            for obj in objs:
                eachdict = {'Code': obj[0], 'Look': obj[0]}
                if eachdict not in nextcate:
                    nextcate.append(eachdict)
            sResult['nextcate'] = nextcate
        sResult['resultCode'] = '0'
    except:
        sResult['resultCode'] = '-1'
    return JsonResponse(sResult)
    
    
    
def show_feedback_step(request):
    from skuapp.table.t_product_quality_feedback_submit import t_product_quality_feedback_submit as feedback_submit
    from skuapp.table.t_product_quality_feedback_cpzy import t_product_quality_feedback_cpzy as feedback_cpzy
    from skuapp.table.t_product_quality_feedback_cgy import t_product_quality_feedback_cgy as feedback_cgy

    page_contrast_dict = {'submit': feedback_submit, 'cpzy': feedback_cpzy, 'cgy': feedback_cgy}

    search_id = request.GET.get('id', '')
    page = request.GET.get('page', '')

    original_table_obj = page_contrast_dict[page].objects.filter(id=search_id)
    steps = eval(original_table_obj[0].Step)

    return render(request, 'feedback_quality_step.html', {'results': steps})


def show_feedback_picture(request):
    """
    显示质量反馈提交人图片
    """
    from skuapp.table.t_product_quality_feedback_submit import t_product_quality_feedback_submit as feedback_submit
    from skuapp.table.t_product_quality_feedback_zjy import t_product_quality_feedback_zjy as feedback_zjy
    from skuapp.table.t_product_quality_feedback_cpzy import t_product_quality_feedback_cpzy as feedback_cpzy
    from skuapp.table.t_product_quality_feedback_cgy import t_product_quality_feedback_cgy as feedback_cgy
    from skuapp.table.t_product_quality_feedback_ck import t_product_quality_feedback_ck as feedback_ck
    from skuapp.table.t_product_quality_feedback_final_sh import  t_product_quality_feedback_final_sh as feedback_final_sh
    from skuapp.table.t_product_quality_feedback_final_result import t_product_quality_feedback_final_result as feedback_final_result

    table_contrast_dict = {'submit': feedback_submit, 'zjy': feedback_zjy, 'cpzy': feedback_cpzy, 'cgy': feedback_cgy,
                           'ck': feedback_ck, 'final_sh': feedback_final_sh, 'final_result': feedback_final_result}

    search_id = request.GET.get('id', '')
    page = request.GET.get('page', '')

    table = table_contrast_dict[page]
    table_obj = table.objects.filter(id=search_id)
    pic_list = []

    if table_obj[0].Picture_1:
        pic_list.append(table_obj[0].Picture_1)
    if table_obj[0].Picture_2:
        pic_list.append(table_obj[0].Picture_2)
    if table_obj[0].Picture_3:
        pic_list.append(table_obj[0].Picture_3)
    if table_obj[0].Picture_4:
        pic_list.append(table_obj[0].Picture_4)
    if table_obj[0].Picture_5:
        pic_list.append(table_obj[0].Picture_5)
    return render(request, 'feedback_submit_picture.html', {'pic_list': pic_list, 'page': page, 'now_id': search_id})




# amazon 产品刷新
def refresh_product_amzon(request):
    from skuapp.table.t_online_info_amazon import t_online_info_amazon
    from app_djcelery.tasks import amazon_product_refresh
    import datetime
    if request.method == 'GET':
        ids = request.GET.get('id').split(',')
        shop_sku = {}
        for record in ids:
            t_online_info_amazon_ins = t_online_info_amazon.objects.filter(id=record)
            for obj in t_online_info_amazon_ins:
                seller_sku = obj.seller_sku
                shop_name = obj.ShopName
                if not shop_sku.has_key(shop_name):
                    shop_sku[shop_name] = [seller_sku]
                else:
                    shop_sku[shop_name].append(seller_sku)
                t_online_info_amazon_ins.update(deal_action='refresh_product',
                                            deal_result=None,
                                            deal_result_info=None,
                                            UpdateTime=datetime.datetime.now())
        amazon_product_refresh.delay(shop_sku, 'refresh_product')
        messages.success(request, '商品刷新中' % ids)
        return  HttpResponse('ffff')
    return render(request, 't_online_info_amazon_listing_plugin.html')


# amazon 产品上下架
def load_amazon_products(request):
    from django.db import connection
    from brick.amazon.product_refresh.get_auth_info import GetAuthInfo
    from brick.amazon.product_refresh.generate_feed_xml import GenerateFeedXml
    from brick.amazon.upload_product.message_to_rabbitmq import MessageToRabbitMq
    import json
    from skuapp.table.t_online_info_amazon import t_online_info_amazon
    import datetime
    import urllib
    from django.http import HttpResponseRedirect

    if request.method == 'GET':
        ids = request.GET.get('id').split(',')
        synType = request.GET.get('synType')
        shop_sku = {}
        sku_str = ''
        if synType == 'load':  # 产品上架
            refresh_type = 'load_product'
            for record in ids:
                t_online_info_amazon_ins = t_online_info_amazon.objects.filter(id=record)
                for obj in t_online_info_amazon_ins:
                    seller_sku = obj.seller_sku
                    sku_str = sku_str + seller_sku + ','
                    shop_name = obj.ShopName
                    if not shop_sku.has_key(shop_name):
                        shop_sku[shop_name] = [seller_sku]
                    else:
                        shop_sku[shop_name].append(seller_sku)
                    t_online_info_amazon_ins.update(deal_action='load_product',
                                                    deal_result=None,
                                                    deal_result_info=None,
                                                    UpdateTime=datetime.datetime.now())
        elif synType == 'unload':  # 产品下架
            refresh_type = 'unload_product'
            for record in ids:
                t_online_info_amazon_ins = t_online_info_amazon.objects.filter(id=record)
                for obj in t_online_info_amazon_ins:
                    seller_sku = obj.seller_sku
                    sku_str = sku_str + seller_sku + ','
                    shop_name = obj.ShopName
                    if not shop_sku.has_key(shop_name):
                        shop_sku[shop_name] = [seller_sku]
                    else:
                        shop_sku[shop_name].append(seller_sku)
                    t_online_info_amazon_ins.update(deal_action='unload_product',
                                                    deal_result=None,
                                                    deal_result_info=None,
                                                    UpdateTime=datetime.datetime.now())

        for key, value in shop_sku.items():
            get_auth_info_ins = GetAuthInfo(connection)
            auth_info = get_auth_info_ins.get_auth_info_by_shop_name(str(key))
            auth_info['IP'] = auth_info['ShopIP']
            auth_info['table_name'] = 't_online_info_amazon'
            auth_info['update_type'] = refresh_type
            auth_info['product_list'] = value

            if refresh_type == 'load_product':
                feed_xml_ins = GenerateFeedXml(auth_info)
                feed_xml = feed_xml_ins.get_inventory_xml(value, 999)
            elif refresh_type == 'unload_product':
                feed_xml_ins = GenerateFeedXml(auth_info)
                feed_xml = feed_xml_ins.get_inventory_xml(value, 0)
            else:
                feed_xml = None

            auth_info['feed_xml'] = feed_xml

            message_to_rabbit_obj = MessageToRabbitMq(auth_info, connection)
            auth_info = json.dumps(auth_info)
            message_to_rabbit_obj.put_message(auth_info)

        if refresh_type == 'load_product':
            messages.success(request, '商品上架中')
        elif refresh_type == 'unload_product':
            messages.success(request, '商品下架中')
        else:
            pass

        if sku_str == '':
            sku_str = ' '
        else:
            sku_str = sku_str[:-1]

        sku_str = urllib.quote(sku_str.decode('gbk', 'replace').encode('utf-8', 'replace'))
        # messages.success(request, 'sku_str is %s' % sku_str)
        # return HttpResponse('SKU=%s' % sku_str)
        return HttpResponseRedirect('/Project/admin/skuapp/t_online_info_amazon_listing/?SKU=%s' % sku_str)



def change_joom_picture(request):
    table_dict = {'box': t_templet_joom_collection_box, 'public': t_templet_public_joom, 'upload': t_templet_joom_wait_upload}

    now_id = request.GET.get('now_id', '')
    page = request.GET.get('page', '')
    pic_index = request.GET.get('pic', '')

    objs = table_dict[page].objects.filter(id=now_id)
    pic_list = objs[0].ExtraImages.split('|')
    for pic in pic_list:
        if pic_index in pic:
            pic_list.remove(pic)
    objs.update(ExtraImages='|'.join(pic_list))
    myResult = {'resultCode': 0}
    return JsonResponse(myResult)




import re
import xlrd
import datetime
from django.db.models import Q
from table.t_aliexpress_service_division_standard import t_aliexpress_service_division_standard
from table.t_aliexpress_service_division_analysis import t_aliexpress_service_division_analysis

score_pattern = re.compile(r'\d+(\.\d+)?\((?P<score>\d+(\.\d+)?)\)')  # 25.68(4.88)
rate_pattern = re.compile(r'\d+(\.\d+)?\((?P<rate>\d+(\.\d+)?)%\)')  # 15(0.04%)



def aliexpress_service_divsion_analysis(request):
    start=datetime.datetime.now()
    last_category_set = set()  # 存放标准分表中最后一级category
    unknow_category_set = set()  #存放未知category
    Primary_category_set = set()
    category_obj={}             #存放category和standard表中记录的映射
    already_iter = set()
    query_list = []
    insert_status = True


    Disputes_rate_col = ''
    DSR_description_col = ''
    sellername_col = ''
    productid_col = ''
    category_col = ''
    map_checklevel={
        1:'Primary_category',
        2:'Second_category',
        3:'Third_category',
        4:'Fourth_category'
    }

    if request.FILES.get('myfile') is not None:
        file_obj = request.FILES['myfile']
        user_name = request.user.first_name
        try:
            workbook = xlrd.open_workbook(filename=None, file_contents=file_obj.read())
            sheet = workbook.sheet_by_index(0)
        except Exception :
            messages.error(request, u'文件解析失败，请上传xls,xlsx格式文件')
            return HttpResponseRedirect('/Project/admin/skuapp/t_aliexpress_service_division_analysis/')

        _col = 0
        try:
            len(sheet.row_values(0))
        except IndexError:
            messages.error(request, u'文件解析为空，请上传xls,xlsx格式,sheet1非空文件')
            return HttpResponseRedirect('/Project/admin/skuapp/t_aliexpress_service_division_analysis/')
        for _ in sheet.row_values(0):

            matcher1 = re.match('SNAD Mediation Rate', _)  # 确定货不对版纠纷提起率列
            if matcher1:
                Disputes_rate_col = _col
                _col += 1
                continue

            matcher2 = re.match('Product Description Rating', _)  # DSR商品描述
            if matcher2:
                DSR_description_col = _col
                _col += 1
                continue
            matcher3 = re.match('Seller Name', _)  # 卖家列
            if matcher3:
                sellername_col = _col
                _col += 1
                continue

            matcher4 = re.match('Product Id', _)  # 产品ID
            if matcher4:
                productid_col = _col
                _col += 1
                continue

            matcher5 = re.match('Category', _)  # 最后一级类目
            if matcher5:
                category_col = _col

            _col += 1

        if not (isinstance(Disputes_rate_col,int) and isinstance(DSR_description_col,int) and isinstance(productid_col,int)
                and isinstance(category_col,int) and isinstance(sellername_col,int)):

            messages.error(request, '导入数据格式错误：必须含有"SNAD Mediation Rate", "Product Description Rating",\n' +
                           '"Seller Name","Product Id","Category"列')
            return HttpResponseRedirect('/Project/admin/skuapp/t_aliexpress_service_division_analysis/')

        category_cols = set(sheet.col_values(category_col))  # 获取所有导入category


        objs = t_aliexpress_service_division_standard.objects \
                                   .filter(Q(Fourth_category__in=category_cols) | Q(Third_category__in=category_cols) |
                                           Q(Second_category__in=category_cols)| Q(Primary_category__in=category_cols))\
        .values('Primary_category','Second_category', 'Third_category', 'Fourth_category', 'Disputes_rate', 'DSR_description',
                            'Dis_decrease','DSR_increase','Check_level')

        for obj in objs:
            Last_category=obj.get(map_checklevel.get(obj.get('Check_level')))
            if Last_category:
                last_category_set.add(Last_category)
                category_obj[Last_category]=obj

        unknow_category_set=category_cols-last_category_set

        try:
            unknow_category_set.remove('Category')
        except Exception :
            pass

        if unknow_category_set:
            err_msg=','.join([str(msg) for msg in unknow_category_set])
            messages.error(request, u'Category类目:{} 不存在，请前往"速卖通服务分标准"添加该类目标准!'.format(err_msg))
            return HttpResponseRedirect('/Project/admin/skuapp/t_aliexpress_service_division_analysis/')

        if not last_category_set:
            messages.error(request, u'文件解析为空，请上传xls,xlsx格式非空文件')
            return HttpResponseRedirect('/Project/admin/skuapp/t_aliexpress_service_division_analysis/')

        for i in range(1, sheet.nrows):
            if i in already_iter:
                continue
            already_iter.add(i)
            try:
                Disputes_rate = re.match(rate_pattern, sheet.cell_value(i, Disputes_rate_col))
                DSR_description = re.match(score_pattern, sheet.cell_value(i, DSR_description_col))
                if Disputes_rate !=None and DSR_description != None:
                    Disputes_rate = float(Disputes_rate.groupdict().get('rate', ''))  # DSR商品描述
                    DSR_description = float(DSR_description.groupdict().get('score', ''))  # 货不对版纠纷提起率
                    productid = str(sheet.cell_value(i, productid_col)).strip()  # 产品ID
                    category = str(sheet.cell_value(i, category_col)).strip()  # 类目
                    sellername = str(sheet.cell_value(i, sellername_col)).strip() if isinstance(sellername_col,int) else ''

                    obj=category_obj[category]
                    if obj:
                        Disputes_rate_standard=obj.get('Disputes_rate') - obj.get('Dis_decrease')
                        DSR_description_standard=obj.get('DSR_description') + obj.get('DSR_increase')
                        if Disputes_rate < Disputes_rate_standard and DSR_description >= DSR_description_standard:
                            continue
                        else:
                            status = False  # 向数据库添加状态异常信息
                            insert_row = t_aliexpress_service_division_analysis(Disputes_rate=Disputes_rate,
                                                                                DSR_description=DSR_description,
                                                                                Productid=productid,
                                                                                Category=category,
                                                                                Inputdatetime=datetime.datetime.now()
                                                                                , Status=status,
                                                                                Importuser=user_name,
                                                                                Seller_Name=sellername,
                                                                                Disputes_rate_standard=Disputes_rate_standard,
                                                                                DSR_description_standard=DSR_description_standard)
                            query_list.append(insert_row)
            except Exception as e:
                messages.error(request,u'数据错误：请联系IT.出错信息{}'.format(e))
                return HttpResponseRedirect('/Project/admin/skuapp/t_aliexpress_service_division_analysis/')

        try:
            t_aliexpress_service_division_analysis.objects.bulk_create(query_list)
            insert_status=True
        except Exception as e:
            messages.error(request,u'数据提交失败：请联系IT.出错信息{}'.format(e))
            return HttpResponseRedirect(
                '/Project/admin/skuapp/t_aliexpress_service_division_analysis/')

        messages.success(request, u'导入成功!') if insert_status else messages.error(request, u'导入失败,请稍后重试')
    return HttpResponseRedirect('/Project/admin/skuapp/t_aliexpress_service_division_analysis/')

def reverse_collection(request):
    return render(request, 'reverse_collection_url.html')


def get_reverse_info(request):
    from django.db import connection
    from app_djcelery.tasks import amazon_reverse_collection
    import datetime
    import time
    cursor = connection.cursor()
    try:
        url = request.GET.get('Reverse_url')
        site = request.GET.get('site')
        user_name = request.user.username
        prodcut_variation_id = str(int(time.time() * 1000))
        shop_set = '---' + str(site) + '/PJ'
        sql_insert = "insert into t_templet_amazon_collection_box(dataFromUrl,createUser,createTime, prodcut_variation_id,ShopSets) values ('%s', '%s', '%s', '%s', '%s')" % (url, user_name, datetime.datetime.now(), prodcut_variation_id,shop_set)
        cursor.execute(sql_insert)
        cursor.execute('commit;')
        sql_max_id = "select max(id) id from t_templet_amazon_collection_box where dataFromUrl = '%s'" % url
        cursor.execute(sql_max_id)
        this_id_obj = cursor.fetchone()
        cursor.close()
        id = None
        if this_id_obj is not None and this_id_obj[0] is not None:
            id = this_id_obj[0]
        if id is not None:
            amazon_reverse_collection.delay([[id, url]])
    except Exception as e:
        cursor.close()
        print e
    return HttpResponseRedirect('/Project/admin/skuapp/t_templet_amazon_collection_box/')


def show_amazon_pictures(request):
    from skuapp.table.t_templet_amazon_collection_box import *
    from skuapp.table.t_templet_amazon_wait_upload import *
    from skuapp.table.t_templet_amazon_published_variation import *
    prodcut_variation_id = request.GET.get('prodcut_variation_id', '')
    collectiton_objs = t_templet_amazon_collection_box.objects.filter(prodcut_variation_id=int(prodcut_variation_id))
    wait_upload_objs = t_templet_amazon_wait_upload.objects.filter(prodcut_variation_id=int(prodcut_variation_id))
    if wait_upload_objs is not None and wait_upload_objs.count() != 0:
        # wait_upload_obj = wait_upload_objs[0]
        wait_upload_obj = collectiton_objs[0]
        main_table_type = 'wait_upload'
    else:
        wait_upload_obj = collectiton_objs[0]
        main_table_type = 'collection_box'
    published_variation_obj = t_templet_amazon_published_variation.objects.filter(prodcut_variation_id=int(prodcut_variation_id))
    return render(request, 'edit_amazon_image.html', {'main_obj': wait_upload_obj,'main_table_type':main_table_type, 'variation_obj':published_variation_obj, 'prodcut_variation_id': prodcut_variation_id})


def change_amazon_image(request):
    from skuapp.table.t_templet_amazon_collection_box import *
    from skuapp.table.t_templet_amazon_wait_upload import *
    from skuapp.table.t_templet_amazon_published_variation import *
    main_table_type = request.GET.get('main_table_type', '')
    shop_set = request.GET.get('shop_set', '')
    pri_id = request.GET.get('pri_id', '')
    variation_type = request.GET.get('variation_type', '')
    image_type = request.GET.get('image_type', '')
    prodcut_variation_id = request.GET.get('prodcut_variation_id', '')
    image_list = []
    if main_table_type == 'collection_box':
        wait_upload_obj = t_templet_amazon_collection_box.objects.filter(prodcut_variation_id=int(prodcut_variation_id))[0]
    else:
        wait_upload_obj = t_templet_amazon_wait_upload.objects.filter(prodcut_variation_id=int(prodcut_variation_id))[0]
    parent_sku = wait_upload_obj.productSKU
    child_sku = None
    if variation_type == 'parent':
        if main_table_type == 'collection_box':
            get_data_obj = t_templet_amazon_collection_box.objects.filter(id=int(pri_id))[0]
        else:
            get_data_obj = t_templet_amazon_wait_upload.objects.filter(id=int(pri_id))[0]
    else:
        get_data_obj = t_templet_amazon_published_variation.objects.filter(id=int(pri_id))[0]
        child_sku = get_data_obj.productSKU

    if image_type == 'main':
        image_list.append(get_data_obj.main_image_url)
    else:
        image_list.append(get_data_obj.other_image_url1)
        image_list.append(get_data_obj.other_image_url2)
        image_list.append(get_data_obj.other_image_url3)
        image_list.append(get_data_obj.other_image_url4)
        image_list.append(get_data_obj.other_image_url5)
        image_list.append(get_data_obj.other_image_url6)
        image_list.append(get_data_obj.other_image_url7)
        image_list.append(get_data_obj.other_image_url8)

    image_dic = {}
    for i in range(len(image_list)):
        image_dic[i] = image_list[i]
    image_dic = {k:v for k, v in image_dic.items() if v}
    return render(request, 'change_amazon_image.html', {'main_table_type':main_table_type, 'imageDict':image_dic, 'variation_type':variation_type,'image_type':image_type, 'prodcut_variation_id':prodcut_variation_id, 'pri_id':pri_id, 'parent_sku':parent_sku, 'child_sku':child_sku, 'shop_set':shop_set})


def save_amazon_image_change(request):
    from skuapp.table.t_templet_amazon_collection_box import *
    from skuapp.table.t_templet_amazon_wait_upload import *
    from skuapp.table.t_templet_amazon_published_variation import *
    from brick.amazon.product_refresh.modify_image_before_upload import *
    main_table_type = request.GET.get('main_table_type', '')
    shop_set = request.GET.get('shop_set', '')
    pri_id = request.GET.get('pri_id', '')
    variation_type = request.GET.get('variation_type', '')
    image_type = request.GET.get('image_type', '')
    prodcut_variation_id = request.GET.get('prodcut_variation_id', '')
    parent_sku = request.GET.get('parent_sku', '')
    child_sku = request.GET.get('child_sku', '')

    if variation_type == 'parent':
        if main_table_type == 'collection_box':
            get_data_obj = t_templet_amazon_collection_box.objects.filter(id=int(pri_id))[0]
        else:
            get_data_obj = t_templet_amazon_wait_upload.objects.filter(id=int(pri_id))[0]
    else:
        get_data_obj = t_templet_amazon_published_variation.objects.filter(id=int(pri_id))[0]

    image_list = []
    image_max_cnt = None
    if image_type == 'main':
        image_max_cnt = 1
        if get_data_obj.main_image_url:
            image_list.append(get_data_obj.main_image_url)
    else:
        image_max_cnt = 8
        if get_data_obj.other_image_url1:
            image_list.append(get_data_obj.other_image_url1)
        if get_data_obj.other_image_url2:
            image_list.append(get_data_obj.other_image_url2)
        if get_data_obj.other_image_url3:
            image_list.append(get_data_obj.other_image_url3)
        if get_data_obj.other_image_url4:
            image_list.append(get_data_obj.other_image_url4)
        if get_data_obj.other_image_url5:
            image_list.append(get_data_obj.other_image_url5)
        if get_data_obj.other_image_url6:
            image_list.append(get_data_obj.other_image_url6)
        if get_data_obj.other_image_url7:
            image_list.append(get_data_obj.other_image_url7)
        if get_data_obj.other_image_url8:
            image_list.append(get_data_obj.other_image_url8)

    # 采集回来的图片上传到oss
    try:
        for k in range(len(image_list)):
            if 'fancyqube' not in str(image_list[k]):
                image_bytes = None
                try:
                    req = urllib2.Request(str(image_list[k]))
                    image_bytes = urllib2.urlopen(req, timeout=30).read()
                except Exception as e:
                    pass
                if image_bytes is not None:
                    modify_image_obj = ModifyImageBeforeUpload()
                    pic_url = modify_image_obj.upload_image_to_oss(shop_set,image_bytes, variation_type, image_type, parent_sku, child_sku, k)
                    image_list[k] = pic_url
    except Exception as e:
        print e

    image_cnt = len(image_list)

    # 上传图片
    if request.method == "POST":
        if image_cnt >= image_max_cnt:
            pass
        else:
            user = request.user.username
            image_local = request.FILES.get('image_local')
            image_url = request.POST.get('image_url', '')

            # 上传本地照片
            if image_local is not None:
                modify_image_obj = ModifyImageBeforeUpload()
                pic_url = modify_image_obj.upload_image_to_oss(shop_set,image_local,variation_type, image_type, parent_sku, child_sku, image_cnt)
                image_list.append(pic_url)

            # 上传图片链接
            if image_url.strip() != '':
                image_bytes = None
                try:
                    req = urllib2.Request(image_url)
                    image_bytes = urllib2.urlopen(req, timeout=30).read()
                except:
                    pass
                if image_bytes is not None:
                    modify_image_obj = ModifyImageBeforeUpload()
                    pic_url = modify_image_obj.upload_image_to_oss(shop_set,image_bytes, variation_type, image_type, parent_sku, child_sku, image_cnt)
                    image_list.append(pic_url)
    else:
        image_index_id = int(request.GET.get('id', ''))
        # 删除图片
        del image_list[image_index_id]

    image_dic = {}
    for i in range(len(image_list)):
        image_dic[i] = image_list[i]

    if len(image_list) < image_max_cnt:
        for k in range(image_max_cnt - len(image_list)):
            image_list.append(None)

    if variation_type == 'parent':
        if image_type == 'main':
            t_templet_amazon_collection_box.objects.filter(id=int(pri_id)).update(main_image_url=image_list[0])
        else:
            t_templet_amazon_collection_box.objects.filter(id=int(pri_id)).update(other_image_url1=image_list[0], other_image_url2=image_list[1], other_image_url3=image_list[2],
                                                                                  other_image_url4=image_list[3], other_image_url5=image_list[4], other_image_url6=image_list[5],
                                                                                  other_image_url7=image_list[6], other_image_url8=image_list[7])
        is_all_data_done, deal_result = validation_amazon_product_data(t_templet_amazon_collection_box.objects.filter(id=int(pri_id))[0])
        if is_all_data_done == 1:
            t_templet_amazon_collection_box.objects.filter(id=int(pri_id)).update(can_upload='0',remark = '')
            deal_result = ''
        else:
            t_templet_amazon_collection_box.objects.filter(id=int(pri_id)).update(can_upload='-1', remark = deal_result)

        # if main_table_type == 'collection_box':
        #     if image_type == 'main':
        #         t_templet_amazon_collection_box.objects.filter(id=int(pri_id)).update(main_image_url=image_list[0])
        #     else:
        #         t_templet_amazon_collection_box.objects.filter(id=int(pri_id)).update(other_image_url1=image_list[0], other_image_url2=image_list[1], other_image_url3=image_list[2], other_image_url4=image_list[3], other_image_url5=image_list[4], other_image_url6=image_list[5], other_image_url7=image_list[6], other_image_url8=image_list[7])
        #
        #     if validation_amazon_product_data(t_templet_amazon_collection_box.objects.filter(id=int(pri_id))[0]) == 1:
        #         t_templet_amazon_collection_box.objects.filter(id=int(pri_id)).update(can_upload='0')
        #     else:
        #         t_templet_amazon_collection_box.objects.filter(id=int(pri_id)).update(can_upload='-1')
        # else:
        #     if image_type == 'main':
        #         t_templet_amazon_wait_upload.objects.filter(id=int(pri_id)).update(main_image_url=image_list[0])
        #     else:
        #         t_templet_amazon_wait_upload.objects.filter(id=int(pri_id)).update(other_image_url1=image_list[0], other_image_url2=image_list[1], other_image_url3=image_list[2], other_image_url4=image_list[3], other_image_url5=image_list[4], other_image_url6=image_list[5], other_image_url7=image_list[6], other_image_url8=image_list[7])
        #     if validation_amazon_product_data(t_templet_amazon_wait_upload.objects.filter(id=int(pri_id))[0]) == 1:
        #         t_templet_amazon_wait_upload.objects.filter(id=int(pri_id)).update(can_upload='0')
        #     else:
        #         t_templet_amazon_wait_upload.objects.filter(id=int(pri_id)).update(can_upload='-1')
    else:
        if image_type == 'main':
            t_templet_amazon_published_variation.objects.filter(id=int(pri_id)).update(main_image_url=image_list[0])
        else:
            t_templet_amazon_published_variation.objects.filter(id=int(pri_id)).update(other_image_url1=image_list[0], other_image_url2=image_list[1], other_image_url3=image_list[2], other_image_url4=image_list[3], other_image_url5=image_list[4], other_image_url6=image_list[5], other_image_url7=image_list[6], other_image_url8=image_list[7])

        prodcut_variation_id = t_templet_amazon_published_variation.objects.filter(id=int(pri_id)).values('prodcut_variation_id')[0]['prodcut_variation_id']
        is_all_data_done, deal_result = validation_amazon_product_data(
            t_templet_amazon_collection_box.objects.filter(prodcut_variation_id=prodcut_variation_id)[0])
        if is_all_data_done == 1:
            t_templet_amazon_collection_box.objects.filter(prodcut_variation_id=prodcut_variation_id).update(can_upload='0', remark='')
        else:
            t_templet_amazon_collection_box.objects.filter(prodcut_variation_id=prodcut_variation_id).update(can_upload='-1', remark=deal_result)
            
    return render(request, 'change_amazon_image.html', {'main_table_type':main_table_type, 'imageDict': image_dic, 'pri_id': pri_id, 'prodcut_variation_id':prodcut_variation_id, 'variation_type':variation_type, 'image_type':image_type, 'parent_sku':parent_sku, 'child_sku':child_sku, 'shop_set':shop_set})


def feedback_zjy_picture(request):
    """
    显示质量反馈质检员图片
    """
    from skuapp.table.t_product_quality_feedback_zjy import t_product_quality_feedback_zjy as feedback_zjy
    from skuapp.table.t_product_quality_feedback_ck import t_product_quality_feedback_ck as feedback_ck
    from skuapp.table.t_product_quality_feedback_final_result import t_product_quality_feedback_final_result as feedback_final_result
    from skuapp.table.t_product_quality_feedback_cpzy import t_product_quality_feedback_cpzy as feedback_cpzy
    from skuapp.table.t_product_quality_feedback_cgy import t_product_quality_feedback_cgy as feedback_cgy
    from skuapp.table.t_product_quality_feedback_final_sh import  t_product_quality_feedback_final_sh as feedback_final_sh


    table_contrast_dict = {'zjy': feedback_zjy, 'cpzy': feedback_cpzy, 'cgy': feedback_cgy, 'ck': feedback_ck,
                           'final_sh': feedback_final_sh, 'final_result': feedback_final_result}

    now_id = request.GET.get('id', '')
    page = request.GET.get('page', '')

    table = table_contrast_dict[page]
    table_obj = table.objects.filter(id=now_id)
    pic_list = []
    if table_obj.exists():
        zjy_pic = table_obj[0].ZJY_Pic
        pic_list = zjy_pic.split('|') if zjy_pic else []
    return render(request, 'feedback_zjy_picture.html', {'pic_list': pic_list, 'page': page, 'now_id': now_id})

def feedback_oss_image(name, img_byte, user):
    BUCKETNAME_PIC = 'fancyqube-product-quality'
    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, ENDPOINT_OUT, BUCKETNAME_PIC)
    bucket.put_object('%s/%s' % (user, name), img_byte)
    pic_url = PREFIX + BUCKETNAME_PIC + '.' + ENDPOINT_OUT + '/' + '%s/%s' % (user, name)
    return pic_url

def save_feedback_zjy_picture(request):
    """
    保存质量反馈质检员提交的图片
    """
    from skuapp.table.t_product_quality_feedback_zjy import t_product_quality_feedback_zjy as feedback_zjy
    from datetime import datetime
    now_id = request.GET.get('now_id', '')
    feedback_zjy_obj = feedback_zjy.objects.filter(id=int(now_id))[0]
    Images = feedback_zjy_obj.ZJY_Pic
    pic_list = []
    if Images:
        pic_list = Images.split(',')
    time_now = datetime.now()

    if request.method == "POST":
        user = request.user.username
        image_local = request.FILES.get('image_local')
        pic_name = user + '-' + time_now.strftime('%Y%m%d%H%M%S') + '.jpg'
        pic_url = feedback_oss_image(pic_name ,image_local, user)
        pic_list.append(pic_url)

    ZJY_Pic = '|'.join(pic_list)

    feedback_zjy.objects.filter(id=int(now_id)).update(ZJY_Pic=ZJY_Pic)

    return render(request, 'feedback_zjy_picture.html', {'pic_list': pic_list, 'page': 'zjy', 'now_id': now_id})


def del_feedback_pic(request):
    """
    删除质量反馈的图片（包括提交人图片和质检员图片）
    """
    from skuapp.table.t_product_quality_feedback_submit import t_product_quality_feedback_submit as feedback_submit
    from skuapp.table.t_product_quality_feedback_zjy import t_product_quality_feedback_zjy as feedback_zjy

    source = request.GET.get('source')
    index = int(request.GET.get('index'))
    del_id = request.GET.get('del_id')

    if source == 'submit':
        table_obj = feedback_submit.objects.filter(id=del_id)
        if index == 0:
            table_obj.update(Picture_1='')
        if index == 1:
            table_obj.update(Picture_2='')
        if index == 2:
            table_obj.update(Picture_3='')
        if index == 3:
            table_obj.update(Picture_4='')
        if index == 4:
            table_obj.update(Picture_5='')
        pic_list = []
        if table_obj[0].Picture_1:
            pic_list.append(table_obj[0].Picture_1)
        if table_obj[0].Picture_2:
            pic_list.append(table_obj[0].Picture_2)
        if table_obj[0].Picture_3:
            pic_list.append(table_obj[0].Picture_3)
        if table_obj[0].Picture_4:
            pic_list.append(table_obj[0].Picture_4)
        if table_obj[0].Picture_5:
            pic_list.append(table_obj[0].Picture_5)
        return render(request, 'feedback_submit_picture.html', {'pic_list': pic_list, 'page': source, 'now_id': del_id})

    else:
        feedback_zjy_objs = feedback_zjy.objects.filter(id=del_id)
        pic_list = []
        if feedback_zjy_objs.exists():
            zjy_pic_list = feedback_zjy_objs[0].ZJY_Pic.split('|')
            del zjy_pic_list[index]
            feedback_zjy_objs.update(ZJY_Pic='|'.join(zjy_pic_list))
            pic_list = zjy_pic_list
        return render(request, 'feedback_zjy_picture.html', {'pic_list': pic_list, 'page': source, 'now_id': del_id})
        
        
def update_applyInfo(request):
    from datetime import datetime
    sku = request.GET.get('sku', '')

    from skuapp.table.t_cloth_factory_dispatch_audit import t_cloth_factory_dispatch_audit
    from django.db.models import Q
    t_cloth_factory_dispatch_other_objs = t_cloth_factory_dispatch_audit.objects.filter(SKU=sku).filter(
        Q(currentState='1') | Q(currentState='3') | Q(currentState='4') | Q(currentState='5'))
    hiddenSkuValue = request.POST.get('sku_hidden', '')
    hiddenNoValue = request.POST.get('no_hidden', '')
    if t_cloth_factory_dispatch_other_objs.count() != 0 and hiddenSkuValue == "":
        return render(request, 't_cloth_factory_tip.html',
                      {'sku': sku})
    elif hiddenNoValue == "yes":
        request.method = "GET"
        sku = hiddenSkuValue

    if request.method == "POST":
        sku = request.POST.get('girard_hidden', '')
        girard = request.POST.get('girard', '')
        buyer = request.POST.get('buyer', '')
        colour = request.POST.get('colour', '')
        size = request.POST.get('check_hidden', '')
        productNumbers = ""
        if request.POST.get('productNumbersXS', '') != "" and request.POST.get('productNumbersXS', '') !="0":
            productNumbersXS = request.POST.get('productNumbersXS', '')
            productNumbers = productNumbers + productNumbersXS + ";"
        if request.POST.get('productNumbersS', '') != "" and request.POST.get('productNumbersS', '') !="0":
            productNumbersS = request.POST.get('productNumbersS', '')
            productNumbers = productNumbers + productNumbersS + ";"
        if request.POST.get('productNumbersM', '') != "" and request.POST.get('productNumbersM', '') !="0":
            productNumbersM = request.POST.get('productNumbersM', '')
            productNumbers = productNumbers + productNumbersM +";"
        if request.POST.get('productNumbersL', '') != "" and request.POST.get('productNumbersL', '') !="0":
            productNumbersL = request.POST.get('productNumbersL', '')
            productNumbers = productNumbers + productNumbersL +";"
        if request.POST.get('productNumbersXL', '') != "" and request.POST.get('productNumbersXL', '') !="0":
            productNumbersXL = request.POST.get('productNumbersXL', '')
            productNumbers = productNumbers + productNumbersXL +";"
        if request.POST.get('productNumbers2XL', '') != "" and request.POST.get('productNumbers2XL', '') !="0":
            productNumbers2XL = request.POST.get('productNumbers2XL', '')
            productNumbers = productNumbers + productNumbers2XL +";"
        if request.POST.get('productNumbers3XL', '') != "" and request.POST.get('productNumbers3XL', '') !="0":
            productNumbers3XL = request.POST.get('productNumbers3XL', '')
            productNumbers = productNumbers + productNumbers3XL +";"
        if request.POST.get('productNumbers4XL', '') != "" and request.POST.get('productNumbers4XL', '') !="0":
            productNumbers4XL = request.POST.get('productNumbers4XL', '')
            productNumbers = productNumbers + productNumbers4XL
        if productNumbers[-1] == ";":
            productNumbers = productNumbers[0:-1]
        loanMoney = 0
        if request.POST.get('loanMoney', '') != "":
            loanMoney = request.POST.get('loanMoney', '')
        actualMoney = 0
        if request.POST.get('actualMoney', '') != "":
            actualMoney = request.POST.get('actualMoney', '')
        outFactory = request.POST.get('outFactory', '')
        from skuapp.table.t_cloth_factory import t_cloth_factory
        t_cloth_factory_obj = t_cloth_factory.objects.filter(value=outFactory)
        if t_cloth_factory_obj is None or t_cloth_factory_obj.count() == 0:
            t_cloth_factory_obj1 = t_cloth_factory(name=outFactory, value=outFactory)
            t_cloth_factory_obj1.save()
        rawNumbers = 0
        if request.POST.get('rawNumbers', '') != "":
            rawNumbers = request.POST.get('rawNumbers', '')
        unit = 1
        strUnit = u"条"
        if request.POST.get('branches', '') != "":
            unit = request.POST.get('branches', '')
        
        if int(unit) == 1:
            strUnit = u"条"
        else:
            strUnit = u"米"
        
        remarkApply = request.POST.get('remarkApply', '')
        from skuapp.table.t_cloth_factory_dispatch_audit import t_cloth_factory_dispatch_audit
        t_cloth_factory_dispatch_audit_objs = t_cloth_factory_dispatch_audit.objects.filter(SKU=sku,currentState=None)
        if t_cloth_factory_dispatch_audit_objs is None or t_cloth_factory_dispatch_audit_objs.count() == 0:
            t_cloth_factory_dispatch_audit_obj1 = t_cloth_factory_dispatch_audit(SKU=sku,girard=girard,buyer=buyer,colour=colour,size=size,productNumbers=productNumbers,
                                                                                 loanMoney=loanMoney,actualMoney=actualMoney,outFactory=outFactory,rawNumbers=rawNumbers,unit=strUnit,remarkApply=remarkApply,
                                                                                createDate = datetime.now(),applyMan = request.user.first_name,applyDate = datetime.now(),currentState = '2')
            t_cloth_factory_dispatch_audit_obj1.save()
        else:
            i = 0
            for t_cloth_factory_dispatch_audit_obj in t_cloth_factory_dispatch_audit_objs:
                i += 1
                if i > 1:
                    t_cloth_factory_dispatch_audit_obj.delete()
                t_cloth_factory_dispatch_audit_obj.girard = girard
                t_cloth_factory_dispatch_audit_obj.buyer = buyer
                t_cloth_factory_dispatch_audit_obj.colour = colour
                t_cloth_factory_dispatch_audit_obj.size = size
                t_cloth_factory_dispatch_audit_obj.productNumbers = productNumbers
                t_cloth_factory_dispatch_audit_obj.loanMoney = loanMoney
                t_cloth_factory_dispatch_audit_obj.actualMoney = actualMoney
                t_cloth_factory_dispatch_audit_obj.outFactory = outFactory
                t_cloth_factory_dispatch_audit_obj.rawNumbers = rawNumbers
                t_cloth_factory_dispatch_audit_obj.unit = strUnit
                t_cloth_factory_dispatch_audit_obj.remarkApply = remarkApply
                t_cloth_factory_dispatch_audit_obj.createDate = datetime.now()
                t_cloth_factory_dispatch_audit_obj.applyMan = request.user.first_name
                t_cloth_factory_dispatch_audit_obj.applyDate = datetime.now()
                t_cloth_factory_dispatch_audit_obj.currentState = '2'
                t_cloth_factory_dispatch_audit_obj.save()
            messages.info(request, 'sku=%s申请信息已提交审核阶段。。。'%(sku))
        #跟新表操作
        rt = u'派单新增成功'
        return render(request, 'result.html', {'rt': rt})

    from skuapp.table.t_cloth_factory import t_cloth_factory
    t_cloth_factory_list = t_cloth_factory.objects.values_list('name','value')
    allFactoryList = []
    for sRow in t_cloth_factory_list:
        allFactoryList.append(sRow[0])
    return render(request, 't_cloth_factory_dispatch.html', {'sku': sku,'t_cloth_factory_list':set(allFactoryList)})

def ali_compare_price(request):
    df = request.GET.get('df')
    wf = request.GET.get('wf')
    dfid = int(get_id_from_url(df))

    showprice,orders = get_price_sum(dfid)
    week_sum = get_OneWeek_Sum(dfid)

    wfid = get_id_from_url(wf)
    from brick.aliexpress.get_info_from_puyuan import get_sqleifo_from_db
    from datetime import datetime as fydate
    print('++++++++++++++++++++++++++++++++++++对方id：')
    print(wfid)
    sku, shopsku, salesCount, weekCount, price = get_sqleifo_from_db(wfid)
    t_aliexpress_compare_price_obj = t_aliexpress_compare_price(OurProductID = wfid,
                                                                OurMainSKU = sku,
                                                                OurSales = salesCount,
                                                                OurWeekSales = weekCount,
                                                                OurPrice = price,
                                                                OppositeProductID = dfid,
                                                                OppositeSales = orders,
                                                                OppositeWeekSales = week_sum,
                                                                OppositePrice = showprice,
                                                                QueryTime = fydate.now())
    t_aliexpress_compare_price_obj.save()
    return HttpResponseRedirect('/Project/admin/skuapp/t_aliexpress_compare_price/')    

@csrf_exempt
def t_product_build_FBA(request):
    import pyodbc, MySQLdb,pymssql
    from datetime import datetime as fbadate
    OldSKU=request.POST.get('OldSKU')
    FBA_OldSKU = "FBA-" + OldSKU
    conn = pymssql.connect(host='122.226.216.10', user='fancyqube', password='K120Esc1',
                                             database='ShopElf',
                                             port='18794')
    cursor = conn.cursor()
    return_value = {}
    str_b_goods = "select count(1) as nCount from b_goods where sku='%s'"%(FBA_OldSKU)
    cursor.execute(str_b_goods)
    objCount = cursor.fetchall()
    if request.is_ajax() and request.method=="POST":
        for obj in objCount:
            if obj[0] > 0:
                return_value["SKUFBA"] = "FBA"
            else:
                sql = '''select  bg.goodscode as '商品编码0',bg.sku as 'SKU1',convert(nvarchar(20), bgc.CategoryParentName) as '大类名称2',convert(nvarchar(20), bgc.categoryname) as '小类名称3',convert(nvarchar(64), bg.GoodsName) as '商品名称4',
                convert(nvarchar(20), bg.GoodsStatus) as '当前状态5',convert(nvarchar(20), bg.Material) as '材质6',convert(nvarchar(20), bg.Model) as '型号7',convert(nvarchar(20), bg.Brand) as '品牌8',bg.Unit as '单位9',bg.PackageCount as '最小包装数10',bg.Weight as '重量11',
                bs.SupplierName as '供应商名称12' ,bg.CostPrice as '成本单价(元)13',bg.Notes as '备注14',convert(nvarchar(32), bg.AliasCnName) as '中文申报名15',bg.AliasEnName as '英文申报名16',bg.DeclaredValue as '申报价值(美元)17',
                bg.OriginCountryCode as '原产国代码18',convert(nvarchar(20), bg.OriginCountry) as '原产国19',bg.MaxNum as '库存上限20',bg.MinNum as '库存下限21',convert(nvarchar(20), bg.SalerName) as '业绩归属人122',convert(nvarchar(20), bg.SalerName2) as '业绩归属人223',
                bg.PackName as '包装规格24',bg.DevDate as '开发日期25',convert(nvarchar(20), bg.Purchaser) as '采购员26',bg.StockDays as '采购到货天数27',bg.CostPrice as '内包装成本28',
                bg.LinkUrl as '网页URL29',bg.LinkUrl2 as '网页URL230',bg.SellDays as '库存预警销售周期31',bg.StockMinAmount as '采购最小订货量32',bg.IsCharged as '是否带电33',
                bg.IsPowder as '是否粉末34',bg.IsLiquid as '是否液体35',bg.possessMan1 as '责任归属人136',bg.possessMan2 as '责任归属人237',
                '普货' as '商品属性38','' as '包装难度系数39','' as '店铺名称40',bg.LinkUrl4 as '网页URL441',bg.LinkUrl5 as '网页URL542',bg.LinkUrl6 as '网页URL643',bg.ShopCarryCost as '店铺运费44',
                '' as '包装材料重量45','' as '汇率46','' as '物流公司价格47','' as '交易费48','' as '毛利率49','' as '计算售价50' 
                from b_goods(nolock) bg left JOIN b_supplier(nolock) bs on bg.SupplierID = bs.nid
                            left join B_GoodsCats(nolock) bgc on bg.GoodsCategoryID = bgc.NID and bg.CategoryCode = bgc.CategoryCode
                where bg.sku='%s'
                 '''%(OldSKU)

                #print("sql={}".format(sql))
                cursor.execute(sql)
                objs = cursor.fetchall()

                import sys
                reload(sys)
                sys.setdefaultencoding('utf8')
                if request.is_ajax() and request.method=="POST":
                    for obj in objs:
                        if str(obj[1]).find('FBA-') == -1:
                            return_value["SKU"] = "FBA-" + str(obj[1])
                            return_value["Name2"] = str(obj[4])
                            return_value["ReportName"] = str(obj[16])
                            return_value["ReportName2"] = str(obj[15])
                            return_value["GoodsStatus"] = str(obj[5])
                            return_value["Purchaser"] = str(obj[26])
                            return_value["CostPrice"] = str(obj[13])
                            return_value["Weight"] = str(obj[11])
                            return_value["SalerName"] = str(obj[22])
                            return_value["Storehouse"] = u'亚马逊仓库'
                            return_value["MainSKU"] = str(obj[0])
                            return_value["LargeCategory"] = str(obj[2])
                            return_value["SmallCategory"] = str(obj[3])
                            return_value["Material"] = str(obj[6])
                            return_value["Model"] = str(obj[7])
                            return_value["Brand"] = str(obj[8])
                            return_value["Unit"] = str(obj[9])
                            return_value["MinPackNum"] = str(obj[10])
                            return_value["SupplierName"] = str(obj[12])
                            return_value["Remark"] = str(obj[14])
                            return_value["DeclaredValue"] = str(obj[17])
                            return_value["OriginCountryCode"] = str(obj[18])
                            return_value["OriginCountry"] = str(obj[19])
                            return_value["MaxNum"] = str(obj[20])
                            return_value["MinNum"] = str(obj[21])
                            return_value["SalerName2"] = str(obj[23])
                            return_value["PackingID"] = str(obj[24])
                            return_value["DevDate"] = str(fbadate.now())
                            return_value["Purchaser"] = str(obj[26])
                            return_value["StockDays"] = str(obj[27])
                            return_value["InnerPrice"] = str(obj[28])
                            return_value["LinkUrl"] = str(obj[29])
                            return_value["LinkUrl2"] = str(obj[30])
                            return_value["SellDays"] = str(obj[31])
                            return_value["StockMinAmount"] = str(obj[32])
                            return_value["Electrification"] = str(obj[33])
                            return_value["Powder"] = str(obj[34])
                            return_value["Liquid"] = str(obj[35])
                            return_value["possessMan1"] = str(obj[36])
                            return_value["possessMan2"] = str(obj[37])
                            return_value["ContrabandAttribute"] = str(obj[38])
                            return_value["DegreeOfDifficulty"] = str(obj[39])
                            return_value["ShopName"] = str(obj[40])
                            return_value["LinkUrl4"] = str(obj[41])
                            return_value["LinkUrl5"] = str(obj[42])
                            return_value["LinkUrl6"] = str(obj[43])
                            return_value["ShopFreight"] = str(obj[44])
                            return_value["PackWeight"] = str(obj[45])
                            return_value["ExchangeRate"] = str(obj[46])
                            return_value["LogisticsPrice"] = str(obj[47])
                            return_value["TransactionFee"] = str(obj[48])
                            return_value["ProfitRate"] = str(obj[49])
                            return_value["SellingPrice"] = str(obj[50])
                        else:
                            return_value["SKUFBA"] = "FBA"

    cursor.close()
    conn.close()
    return HttpResponse(json.dumps(return_value), content_type="application/json")
    
    
    


def edit_show_SalesAttr(request):
    import json
    from skuapp.table.t_product_depart_get import t_product_depart_get

    id = request.GET.get('id')
    obj = t_product_depart_get.objects.filter(id=id)
    salesname = obj[0].SalesAttr
    if request.method == "POST":
        sResult = {}
        salesname = request.POST.get('salesattr')
        try:
            obj.update(SalesAttr=salesname)
            sResult['code'] = 0
        except:
            sResult['code'] = -1
        return HttpResponse(json.dumps(sResult))
    return render(request, 'edit_salesattr.html', {'id': id, 'salesname': salesname})

@csrf_exempt
def t_cloth_factory_dealdata(request):
    try:
        from skuapp.table.t_cloth_factory_dispatch_plan import t_cloth_factory_dispatch_plan
        get_sku = request.GET.get('SKU')
        get_id = request.GET.get('id')
        productNumbers_Num = request.GET.get('productNumbers_Num')
        rawNum_Num = request.GET.get('rawNum_Num')
        selData = request.GET.get('selData')
        remarkAudit = request.GET.get('remarkAudit')
        if selData == "kong":
            selData = ''
        remarkApply = request.GET.get('remarkApply')
        completeNumber = request.GET.get('completeNumber')
        if int(productNumbers_Num) == 0 or float(productNumbers_Num) == 0.0 or float(completeNumber) == 0.0:
            return JsonResponse({'result': 'NG'})
        if completeNumber == "111229999":
            t_cloth_factory_dispatch_plan.objects.filter(id=get_id).update(productNumbers=productNumbers_Num,rawNumbers=rawNum_Num,unit=selData,remarkApply=remarkApply,remarkAudit=remarkAudit)
        else:
            if productNumbers_Num is None or productNumbers_Num == "":
                productNumbers_Num = "0"
            #productNumbers_Num = float(productNumbers_Num) * 1.3
            if float(productNumbers_Num) < float(completeNumber):
                return JsonResponse({'result': 'RP'})
            else:
                t_cloth_factory_dispatch_plan.objects.filter(id=get_id).update(completeNumbers=completeNumber)
        return JsonResponse({'result': 'OK'})
    except Exception as e:
        messages.info(request, u'id=%s,SKU=%s,productNumbers=%s,rawNum=%s,selData=%s,remarkApply=%s,remarkAudit=%s,error:%s,录入数据存在问题，请修正后重新保存。'
                      % (get_id,obj.SKU,productNumbers_Num,rawNum_Num,selData,remarkApply,remarkAudit,str(e)))
        return JsonResponse({'result': 'NG'})


def category_info(request):
    from skuapp.table.t_cfg_category_info import *
    
    sResult = {}
    CategoryId = request.GET.get('CategoryId')
    try:
        t_cfg_category_info_objs = t_cfg_category_info.objects.filter(CategoryId=CategoryId).values('id','CategoryName')
        lis = []
        for t_cfg_category_info_obj in t_cfg_category_info_objs:
            lis.append({'id':t_cfg_category_info_obj['id'],'CategoryName':t_cfg_category_info_obj['CategoryName']})
        sResult['PL'] = lis
        sResult['resultCode'] = '200'
    except:
        sResult['resultCode'] = '500'
        
    return JsonResponse(sResult)
    
def category_info_add(request):
    from skuapp.table.t_cfg_category_info import *
    id = request.GET.get("id")
    t_cfg_category_info.objects.get_or_create(CategoryId=id,CategoryName=None)
    rea_id = t_cfg_category_info.objects.latest("id").id
    return HttpResponseRedirect('/Project/admin/skuapp/t_cfg_category_info/%s/update/'%rea_id)  
    
def addseats(request):
    from skuapp.table.t_store_marketplan_execution_aliexpress import t_store_marketplan_execution_aliexpress
    type_num = request.GET.get("type_num")
    new_obj = t_store_marketplan_execution_aliexpress()
    new_obj.type_num = type_num
    new_obj.save()
    id = t_store_marketplan_execution_aliexpress.objects.latest("id").id
    return HttpResponseRedirect('/Project/admin/skuapp/t_store_marketplan_execution_aliexpress/%s/update/'%id)  

def joom_refund(request):
    import csv  
    from itertools import islice
    from django.db import connection
    cursor = connection.cursor()
    
    import pyodbc, MySQLdb,pymssql
    ShopOrderNumber=request.POST.get('ShopOrderNumber')
    conn = pymssql.connect(host='122.226.216.10', user='fancyqube', password='K120Esc1',
                                             database='ShopElf',
                                             port='18793')
    cursor2 = conn.cursor()
        
    username = request.user.username
    if request.FILES.get('joom_file') is not None:
        joom_file = request.FILES['joom_file']
        for row in islice(csv.reader(joom_file),1,None):
            try:
                sql2 = "select TOP 1 a.nid,b.sku from P_Trade a,p_tradedt b where a.nid = b.tradenid AND a.ack = '%s'"%row[0]
                cursor2.execute(sql2)
                obj = cursor2.fetchone()
                nid = obj[0]
                SKU = obj[1]
                    
            except:
                try:
                    sql3 = "select TOP 1 a.nid,b.sku from P_Trade_His a,P_TradeDt_His b where a.nid = b.tradenid AND a.ack = '%s'"%row[0]
                    cursor2.execute(sql3)
                    obj = cursor2.fetchone()
                    nid = obj[0]
                    SKU = obj[1]
                except:
                    nid = ''
                    SKU = ''
            sql = "INSERT INTO t_joom_refund(ShopNum,RefundPrice,RefundReason,UploadMan,nid,SKU,UploadTime,UpdateTime) VALUES('%s',%s,'%s','%s','%s','%s',now(),now())"%(row[0],row[1],row[2].decode('GBK'),request.user.first_name,nid,SKU)
            cursor.execute(sql)
            cursor.execute('commit;')
    cursor.close()            
    cursor2.close()                      
    return HttpResponseRedirect('/Project/admin/skuapp/t_joom_refund/') 
    
def price_list(request):
    from skuapp.table.t_cfg_platform_country import *
    from skuapp.table.t_cfg_b_country import *
    from skuapp.table.t_cfg_b_emsfare2 import *
    from skuapp.table.t_cfg_standard_large import *
    SKU = request.GET.get('SKU')
    platformCountryCode = request.GET.get("platformCountryCode")
    DestinationCountryCode = request.GET.get("DestinationCountryCode")
    category = request.GET.get('category', '')
    try:
        country_name = t_cfg_b_country.objects.get(country_code=DestinationCountryCode).country
    except:
        country_name = ''
    SellingPrice = request.GET.get('sellingPrice')
    if SKU != '' or SKU is not None:
        SKU_info = SKU
        SellingPrice_info = SellingPrice
        platformCountryCode_info = platformCountryCode
        DestinationCountryCode_info = DestinationCountryCode
    t_cfg_platform_country_objs = t_cfg_platform_country.objects.values('platform_country_code','platform_country_name').order_by('platform_country_code')
    t_cfg_b_country_objs = t_cfg_b_country.objects.values('country_code','country').order_by('country_code')
    t_cfg_b_emsfare2_objs = t_cfg_b_emsfare2.objects.values('platform_country_code','countrycode').distinct()
    t_cfg_standard_large_objs = t_cfg_standard_large.objects.filter(standard_id=1).values('standard_large_code','standard_large_name').order_by('-standard_large_code')
    
    username = request.GET.get("username")
    from django.db import connection
    cursor = connection.cursor()
    sql = "SELECT platform,country FROM t_cfg_b_login_info WHERE username = '%s'"%username
    cursor.execute(sql)
    row = cursor.fetchone()
    try:
        platform_his = str(row[0])
        country_his = str(row[1])
    except:
        platform_his = ''
        country_his = ''

    return render(request, 'price_list.html',{'t_cfg_platform_country_objs':t_cfg_platform_country_objs,'t_cfg_b_emsfare2_objs':t_cfg_b_emsfare2_objs,'t_cfg_b_country_objs':t_cfg_b_country_objs,'SKU_info':SKU_info,'SellingPrice_info':SellingPrice_info,'platformCountryCode_info':platformCountryCode,'DestinationCountryCode_info':DestinationCountryCode,'t_cfg_standard_large_objs':t_cfg_standard_large_objs,'country_name':country_name,
                                               'category': category,'platform_his':platform_his,'country_his':country_his,'username':username})
    
def price_list2(request):
    from skuapp.table.t_cfg_platform_country import *
    from skuapp.table.t_cfg_b_country import *
    from skuapp.table.t_cfg_b_emsfare2 import *
    from skuapp.table.t_cfg_category import *

    sResult = {}
    Platform = request.GET.get('Platform')
    Country = request.GET.get('Country')
    try:
        t_cfg_b_emsfare2_objs = t_cfg_b_emsfare2.objects.filter(platform_country_code=Platform).values_list('countrycode').distinct()
        lis = []
        lis2 = []
        for t_cfg_b_emsfare2_obj in t_cfg_b_emsfare2_objs:
            country = t_cfg_b_country.objects.filter(country_code=t_cfg_b_emsfare2_obj[0]).values_list('country', flat=True)[0]
            lis.append({'countrycode': t_cfg_b_emsfare2_obj[0], 'countryname': country})
        sResult['s_country'] = lis
        sResult['resultCode'] = '200'
    except:
        sResult['resultCode'] = '500'
    if Country is None or Country.strip() == '':
        c_country = t_cfg_b_emsfare2_objs[:1][0][0]
    else:
        c_country = Country
    cc = int(t_cfg_b_emsfare2.objects.get(platform_country_code=Platform, countrycode=c_country).category_id)
    t_cfg_category_objs = t_cfg_category.objects.filter(category_id=cc).values_list('category_code', 'category_name')
    for t_cfg_category_obj in t_cfg_category_objs:
        lis2.append({'category_code': t_cfg_category_obj[0], 'category_name': t_cfg_category_obj[1]})
    sResult['PL'] = lis2
    
    from django.db import connection
    cursor = connection.cursor()
    sql1 = "INSERT INTO t_cfg_b_login_info(username,platform) VALUES ('%s','%s') ON DUPLICATE KEY UPDATE platform=VALUES(platform);"%(request.user.username,Platform)
    sql2 = "INSERT INTO t_cfg_b_login_info(username,country) VALUES ('%s','%s') ON DUPLICATE KEY UPDATE country=VALUES(country);"%(request.user.username,c_country)
    cursor.execute(sql1)
    cursor.execute(sql2)
    cursor.execute("commit;")
    
    CURRENCYCODE = str(t_cfg_b_country.objects.get(country_code=c_country).CURRENCYCODE)
    sql3 = '''select currencycode,
       currencyname,
       max(case
             when rank = 2 then
              exchangerate
           end) ex1,
       max(case
             when rank = 2 then
              updatetime
           end) t1,
       max(case
             when rank = 1 then
              exchangerate
           end) ex2,
       max(case
             when rank = 1 then
              updatetime
           end) t2
      from (select currencycode, currencyname, exchangerate, updatetime, rank
              from (select log_order.currencycode,
                           log_order.updatetime,
                           log_order.exchangerate,
                           log_order.currencyname,
                           @rownum := @rownum + 1,
                           if(@pdept = log_order.currencycode,
                              @rank := @rank + 1,
                              @rank := 1) as rank,
                           @pdept := log_order.currencycode
                      from (select currencycode,
                                   currencyname,
                                   exchangerate,
                                   updatetime,
                                   id
                              from t_cfg_b_currencycode_log
                             order by currencycode, id desc) log_order,
                           (select @rownum := 0, @pdept := null, @rank := 0) a) a
             where rank <= 2) aa
     group by aa.currencycode, aa.currencyname HAVING aa.currencycode = '%s' AND ex1 is NOT NULL;
    '''%CURRENCYCODE
    cursor.execute(sql3)
    row = cursor.fetchone()
    try:
        ex1 = float(row[2])
        ex2 = float(row[4])
        t1 = str(row[3])
        t2 = str(row[5])
    except:
        ex1 = 0
        ex2 = 0
        t1 = ''
        t2 = ''
    sResult['ex1'] = ex1
    sResult['ex2'] = ex2
    sResult['t1'] = t1
    sResult['t2'] = t2
    
    if cc == 0:
        sResult['PL_flag'] = 0
    else:
        sResult['PL_flag'] = 1

    return JsonResponse(sResult)

    
def price_list3(request):
    from skuapp.table.t_cfg_b_emsfare2 import t_cfg_b_emsfare2
    from skuapp.table.t_cfg_standard_small import *
    from skuapp.table.t_cfg_standard_large_small import *
    
    sResult = {}
    bigflag = request.GET.get('bigflag')
    Country = request.GET.get('Country')
    if Country:
        t_cfg_b_emsfare2_obj = t_cfg_b_emsfare2.objects.get(platform_country_code='AMAZON-FBA', countrycode=Country)
        standard_id = int(t_cfg_b_emsfare2_obj.standard_id)
    else:
        standard_id = 1
    try:
        t_cfg_standard_large_small_objs = t_cfg_standard_large_small.objects.filter(standard_id=standard_id,standard_large_code=bigflag).values_list('standard_small_code')
        lis = []
        for t_cfg_standard_large_small_obj in t_cfg_standard_large_small_objs:
            smallname = t_cfg_standard_small.objects.filter(standard_id=standard_id,standard_small_code=t_cfg_standard_large_small_obj[0]).values_list('standard_small_name',flat=True)[0]
            lis.append({'smallcode':t_cfg_standard_large_small_obj[0],'smallname':smallname})
        sResult['guige'] = lis
        sResult['resultCode'] = '200'
    except:
        sResult['resultCode'] = '500'
        
    return JsonResponse(sResult)
    
def price_list4(request):
    from skuapp.table.t_cfg_b_emsfare2 import t_cfg_b_emsfare2
    from skuapp.table.t_cfg_standard_large import t_cfg_standard_large
    from skuapp.table.t_cfg_standard_small import t_cfg_standard_small
    from skuapp.table.t_cfg_standard_large_small import t_cfg_standard_large_small
    
    sResult = {}
    Platform = request.GET.get('Platform')
    Country = request.GET.get('Country')
    #try:
    lis = []
    lis2 = []
    t_cfg_b_emsfare2_obj = t_cfg_b_emsfare2.objects.get(platform_country_code=Platform, countrycode=Country)
    standard_id = int(t_cfg_b_emsfare2_obj.standard_id)
    t_cfg_standard_large_objs = t_cfg_standard_large.objects.filter(standard_id=standard_id).values_list('standard_large_code','standard_large_name')
    for t_cfg_standard_large_obj in t_cfg_standard_large_objs:
        lis.append({'large_code':t_cfg_standard_large_obj[0],'large_name':t_cfg_standard_large_obj[1]})
        
    standard_large_code = t_cfg_standard_large_small.objects.filter(standard_id=standard_id).values_list('standard_large_code')[:1][0][0] 
    standard_small_code_objs = t_cfg_standard_large_small.objects.filter(standard_large_code=standard_large_code).values_list('standard_small_code')
    for standard_small_code_obj in standard_small_code_objs:
        standard_small_name = t_cfg_standard_small.objects.get(standard_id=standard_id,standard_small_code=standard_small_code_obj[0]).standard_small_name
        lis2.append({'small_code':standard_small_code_obj[0],'small_name':standard_small_name})
    sResult['big'] = lis
    sResult['small'] = lis2
    sResult['resultCode'] = '200'
    #except:
        #sResult['resultCode'] = '500'
        
    return JsonResponse(sResult)
    
def price_list_tab(request):
    return render(request, 'price_list_tab.html')
    
def show_1688pic(request):
    conn = MySQLdb.connect(host='rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com', user='by15161458383', passwd='K120Esc1',
                       db='hq_db_test2', port=3306,
                       charset='utf8')
    cur = conn.cursor()
    sql = 'SELECT pic,datacreate,url FROM temp_1688_xp order by datacreate Desc'
    cur.execute(sql)
    rows = cur.fetchall()
    return render(request, 'show_1688pic.html',{'rows':rows})
    
def price_list_file(request):
    ACCESS_KEY_ID = 'LTAIH6IHuMj6Fq2h'
    ACCESS_KEY_SECRET = 'N5eWsbw8qBkMfPREkgF2JnTsDASelM'
    ENDPOINT_OUT = 'oss-cn-shanghai.aliyuncs.com'
    BUCKETNAME_APIVERSION = 'fancyqube-download'
    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, ENDPOINT_OUT, BUCKETNAME_APIVERSION)
    lis = []
    for obj in oss2.ObjectIterator(bucket,prefix='pricelist/'): 
        file_name =  (obj.key).split("/")[1].decode("utf8")
        lis.append(file_name)
    lis.remove(lis[0])
    return render(request, 'price_list_file.html',{'lis':lis})
    
def price_list_rz(request):
    return render(request, 'price_list_rz.html')
def batch_suanjia(request):  
    import csv  
    from itertools import islice
    from brick.pricelist.calculate_price import *
    
    from datetime import datetime
    ACCESS_KEY_ID = 'LTAIH6IHuMj6Fq2h'
    ACCESS_KEY_SECRET = 'N5eWsbw8qBkMfPREkgF2JnTsDASelM'
    ENDPOINT_OUT = 'oss-cn-shanghai.aliyuncs.com'
    BUCKETNAME_APIVERSION = 'fancyqube-download'
    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, ENDPOINT_OUT, BUCKETNAME_APIVERSION)

    Platform = request.POST.get('Platform')
    Country = request.POST.get('Country')
    category = request.POST.get('category')
    
    
    username = request.user.username
    if request.FILES.get('batch_suanjia') is not None:
        batch_file = request.FILES['batch_suanjia']
        csv_name = '%s.csv'%username
        with open(csv_name,"w") as csvfile: 
            writer = csv.writer(csvfile)  
            writer.writerow(['SKU',u'克重',u'成本价(￥)',u'利润率(%)',u'售价($)',u'售价(目的地国家币种)']) 
            for row in islice(csv.reader(batch_file),1,None):
                if row[4] is None or row[4] == '':
                    calculate_price_obj = calculate_price(row[0],Money=row[2],Weight=row[1])
                    try:
                        calculate_price_obj = calculate_price_obj.calculate_selling_price(row[3],platformCountryCode=Platform, DestinationCountryCode=Country,category=category)
                        sellingPrice_us = calculate_price_obj['sellingPrice_us']
                        sellingPrice_des = calculate_price_obj['sellingPrice_destination']
                    except:
                        sellingPrice_us = ''
                    new_row = [row[0],row[1],row[2],row[3],sellingPrice_us,sellingPrice_des]                                     
                    writer.writerow(new_row)
                else:
                    calculate_price_obj = calculate_price(row[0],Money=row[2],Weight=row[1])
                    try:
                        calculate_price_obj.calculate_profitRate(row[4],platformCountryCode=Platform, DestinationCountryCode=Country,category=category)
                        profitRate = calculate_price_obj['profitRate']
                    except:
                        profitRate = ''
                    new_row = [row[0],row[1],row[2],profitRate,row[4]]
                    writer.writerow(new_row)
        csvfile.close()
        des_path = 'suanjia/%s.csv'%username
        bucket.put_object_from_file(des_path,csv_name)

    return HttpResponseRedirect('/price_list/?username=%s'%username)  
def aliexpress_exe(request):
    from skuapp.table.t_store_marketplan_execution_aliexpress import t_store_marketplan_execution_aliexpress
    from skuapp.table.t_store_execution_aliexpress import t_store_execution_aliexpress
    from django.db.models import F
    import datetime
    t_store_marketplan_execution_aliexpress_objs = t_store_marketplan_execution_aliexpress.objects.filter(exe_sum__gte=0,exe_sum__gt=F('run_sum')).values_list('shopname','type_num').distinct()
    new_list = []
    today=datetime.date.today()
    log_list = t_store_execution_aliexpress.objects.filter(sd_time=today).values_list('shopname',flat=True)

    for t_store_marketplan_execution_aliexpress_obj in t_store_marketplan_execution_aliexpress_objs:
        try:
            if t_store_marketplan_execution_aliexpress_obj[0] not in log_list:
                new_list.append(int(t_store_marketplan_execution_aliexpress_obj[1]))
                if len(new_list) >=3:
                    break
        except:
            break
    sd_objs = t_store_marketplan_execution_aliexpress.objects.filter(type_num__in=new_list)

    return render(request, 'aliexpress_exe.html',{'new_list':new_list,'log_list':log_list,'sd_objs':sd_objs})
@csrf_exempt    
def aliexpress_cc(request):
    from skuapp.table.t_store_marketplan_execution_aliexpress import t_store_marketplan_execution_aliexpress
    from skuapp.table.t_store_execution_aliexpress import t_store_execution_aliexpress
    from django.db.models import F
    import datetime
    type_num_list = request.POST.getlist('type_num')
    createtime_list = request.POST.getlist('createtime')
    shopname_list = request.POST.getlist('shopname') 
    createman_list = request.POST.getlist('createman') 
    MainSKU_list = request.POST.getlist('MainSKU') 
    productid_list = request.POST.getlist('productid') 
    money_list = request.POST.getlist('money') 
    count_list=request.POST.getlist('count') 
    reason_list=request.POST.getlist('reason') 
    remark_list=request.POST.getlist('remark') 
    ordernum_list=request.POST.getlist('ordernum') 
    tracenum_list=request.POST.getlist('tracenum') 
    sd_man_list=request.POST.getlist('sd_man')
    sd_time_list=request.POST.getlist('sd_time') 
    jd_man_list=request.POST.getlist('jd_man') 
    yx_fee_list=request.POST.getlist('yx_fee') 
    route_name_list=request.POST.getlist('route_name')  
    ip_list=request.POST.getlist('ip') 
    buyer_account_list=request.POST.getlist('buyer_account') 
    pay_account_list=request.POST.getlist('pay_account') 
    pj_time_man_list=request.POST.getlist('pj_time_man')
    
    for i in range(0,len(shopname_list)):
        new_obj = t_store_execution_aliexpress()
        new_obj.type_num = type_num_list[i]
        new_obj.createtime = datetime.datetime.strptime(createtime_list[i],'%Y年%m月%d日 %H:%M')
        new_obj.shopname = shopname_list[i]
        new_obj.createman = createman_list[i]
        new_obj.MainSKU = MainSKU_list[i]
        new_obj.productid = productid_list[i]
        new_obj.money=money_list[i]
        new_obj.count=count_list[i]
        new_obj.reason=reason_list[i]
        new_obj.remark=remark_list[i]
        new_obj.ordernum=ordernum_list[i]
        new_obj.tracenum=tracenum_list[i]
        new_obj.sd_man=sd_man_list[i]
        try:
            new_obj.sd_time=datetime.datetime.strptime(sd_time_list[i],'%Y-%m-%d')
        except:
            new_obj.sd_time=None
        new_obj.jd_man=jd_man_list[i]

        if yx_fee_list[i] =='':
            new_obj.yx_fee = None
        else:
            new_obj.yx_fee = yx_fee_list[i]
        
        new_obj.route_name=route_name_list[i]
        new_obj.ip=ip_list[i]
        new_obj.buyer_account=buyer_account_list[i]
        new_obj.pay_account=pay_account_list[i]
        new_obj.pj_time_man=pj_time_man_list[i]
        new_obj.save()
    t_store_marketplan_execution_aliexpress.objects.filter(type_num__in=type_num_list).update(run_sum=F('run_sum')+1)
    return HttpResponseRedirect("/Project/admin/skuapp/t_store_execution_aliexpress/")
   
@csrf_exempt    
def suanjia1(request):
    from brick.pricelist.calculate_price import *
    return_value = {}
    if request.is_ajax() and request.method=="POST":
        SKU = request.POST.get("SKU")
        calculate_price = calculate_price(SKU)
        platformCountryCode = request.POST.get("platformCountryCode")
        DestinationCountryCode = request.POST.get("DestinationCountryCode")
        profitRate = request.POST.get("profitRate")
        LargeCode = request.POST.get("LargeCode")
        SmallCode = request.POST.get("SmallCode")
        PackWeight = request.POST.get("PackWeight")
        kb = request.POST.get("kb")
        category = request.POST.get("category")
        sb_discount = request.POST.get("sb_discount")
        bcd_rate = request.POST.get("bcd_rate")
        yj_rate = request.POST.get("yj_rate")
        xss_rate = request.POST.get("xss_rate")


        if PackWeight is None or PackWeight.strip() == '' or PackWeight == 'None':
            PackWeight = 20
        if SKU is None or SKU == '':
            w = request.POST.get("Weight")
            cp = request.POST.get("CostPrice")
        else:
            try:
                count = 1.0
                if SKU.find('*') >=0:
                    try:
                        count = float(SKU.replace(' ','').split('*')[1])
                    except:
                        count = 1.0
                    SKU = SKU.split('*')[0]                 
                b_goods_obj = py_b_goods.objects.get(SKU=SKU)
                cp = float(b_goods_obj.CostPrice) * count
                w = float(b_goods_obj.Weight) * count
            except:
                cp = None
                w = None
        return_value ={}
        return_value['CostPrice']=str(cp)
        return_value['Weight']=str(w)       
        calculate_price_obj = calculate_price.calculate_selling_price(profitRate,platformCountryCode=platformCountryCode, DestinationCountryCode=DestinationCountryCode,PackWeight=PackWeight,LargeCode=LargeCode,SmallCode=SmallCode,kb=kb,category=category,sb_discount=sb_discount,bcd_rate=bcd_rate,yj_rate=yj_rate,xss_rate=xss_rate,Money=cp,Weight=w)
        return_value['sellingPrice_destination'] = str(calculate_price_obj['sellingPrice_destination'])
        return_value['sellingPrice_china'] = str(calculate_price_obj['sellingPrice_china'])
        return_value['sellingPrice_us'] = str(calculate_price_obj['sellingPrice_us'])
        return_value['logisticName'] = calculate_price_obj['logisticName']
        return_value['kickback'] = str(calculate_price_obj['kickback'])
        return_value['ExchangeRate'] = str(calculate_price_obj['ExchangeRate'])
        return_value['Discount'] = str(calculate_price_obj['Discount'])
        return_value['CURRENCYCODE'] = str(calculate_price_obj['CURRENCYCODE'])
        return_value['sb_discount'] = str(calculate_price_obj['sb_discount'])
        return_value['bcd_rate'] = str(calculate_price_obj['bcd_rate'])
        return_value['yj_rate'] = str(calculate_price_obj['yj_rate'])
        return_value['xss_rate'] = str(calculate_price_obj['xss_rate'])
        flag = calculate_price_obj['params_flow']['flag']
        new_params_obj = calculate_price_obj['params_flow']
        try:
            return_value['price_yf'] = str(new_params_obj['price_yf'])
        except:
            return_value['price_yf'] = u'FBA暂不支持'
        try:
            return_value['fd_money'] = str(new_params_obj['fd_money'])
        except:
            return_value['fd_money'] = u'FBA暂不支持'
        try:
            return_value['zyf'] = str((new_params_obj['price_yf']+new_params_obj['fd_money'])*new_params_obj['Discount']/100)
        except:
            return_value['zyf'] = u'FBA暂不支持'
        return_value['logisticwaycode_desc'] = str(new_params_obj['logisticwaycode_desc'])
        if flag == 01:
            html_info = "<center>一次算价: 美元售价%s$=((物流基本费用%s￥+物流分档费用%s￥)*物流折扣%s%%+成本价%s￥+平台扣除的费用%s￥)/汇率%s/(1-利润率%s%%-平台折扣%s%%)</center>"%(return_value['sellingPrice_us'],new_params_obj['price_yf'],new_params_obj['fd_money'],new_params_obj['Discount'],new_params_obj['Money'],new_params_obj['basefee'],new_params_obj['ExchangeRate_USD'],new_params_obj['profitRate'],new_params_obj['kickback'])
            html_info = "%s<br><center><font color='red'>物流规则简单描述:%s</font></center>"%(html_info,new_params_obj['logisticwaycode_desc'])
            html_info = "%s<br><center><font color='red'>费用规则简单描述:%s</font></center>"%(html_info,new_params_obj['getprice_desc'])
        elif flag == 02:
            new_params_obj1 = calculate_price_obj['params_flow1']
            html_info = "<center>一次算价: 美元售价%s$=((物流基本费用%s￥+物流分档费用%s￥)*物流折扣%s%%+成本价%s￥+平台扣除的费用%s￥)/汇率%s/(1-利润率%s%%-平台折扣%s%%)</center>"%(new_params_obj1['sellingPrice1'],new_params_obj1['price_yf'],new_params_obj1['fd_money'],new_params_obj1['Discount'],new_params_obj1['Money'],new_params_obj1['basefee'],new_params_obj1['ExchangeRate_USD'],new_params_obj1['profitRate'],new_params_obj1['kickback'])
            html_info = "%s<br><center>二次算价: 美元售价%s$=((物流基本费用%s￥+物流分档费用%s￥)*物流折扣%s%%+成本价%s￥+平台扣除的费用%s￥)/汇率%s/(1-利润率%s%%-平台折扣%s%%)</center>"%(html_info,return_value['sellingPrice_us'],new_params_obj['price_yf'],new_params_obj['fd_money'],new_params_obj['Discount'],new_params_obj['Money'],new_params_obj['basefee'],new_params_obj['ExchangeRate_USD'],new_params_obj['profitRate'],new_params_obj['kickback'])
            html_info = "%s<br><center><font color='red'>物流规则简单描述:%s</font></center>"%(html_info,new_params_obj['logisticwaycode_desc'])
            html_info = "%s<br><center><font color='red'>费用规则简单描述:%s</font></center>"%(html_info,new_params_obj['getprice_desc'])
        elif flag == 03:
            html_info = "<center>美元售价%s$=(物流头程尾程总费用%s￥*物流折扣%s%%+成本价%s￥+平台扣除的费用%s￥)/汇率%s/(1-利润率%s%%-平台折扣%s%%)</center>"%(return_value['sellingPrice_us'],new_params_obj['sum_price_tw'],new_params_obj['Discount'],new_params_obj['Money'],new_params_obj['basefee'],new_params_obj['ExchangeRate_USD'],new_params_obj['profitRate'],new_params_obj['kickback'])
            html_info = "%s<br><center><font color='red'>物流规则简单描述:%s;尾程费用(%s)</font></center>"%(html_info,new_params_obj['logisticwaycode_desc'],new_params_obj['getprice_standard_desc'])
            html_info = "%s<br><center><font color='red'>费用规则简单描述:%s</font></center>"%(html_info,new_params_obj['getprice_desc'])
            html_info = "%s<br><center>%s</center><br><center>%s</center>"%(html_info,new_params_obj['standard_large_desc'],new_params_obj['standard_small_desc'])
        return_value['html_info'] = html_info

    return HttpResponse(json.dumps(return_value), content_type="application/json")
    
@csrf_exempt    
def suanjia2(request):
    from brick.pricelist.calculate_price import *
    if request.is_ajax() and request.method=="POST":
        SKU = request.POST.get("SKU")
        calculate_price = calculate_price(SKU)
        platformCountryCode = request.POST.get("platformCountryCode")
        DestinationCountryCode = request.POST.get("DestinationCountryCode")
        sellingPrice = request.POST.get("SellPrice")
        kb = request.POST.get("kb")
        price_des = request.POST.get("price_des")
        currencycode = request.POST.get("currencycode")
        category = request.POST.get("category")
        sb_discount = request.POST.get("sb_discount")
        bcd_rate = request.POST.get("bcd_rate")
        yj_rate = request.POST.get("yj_rate")
        xss_rate = request.POST.get("xss_rate")
        if SKU is None or SKU == '':
            w = request.POST.get("Weight")
            cp = request.POST.get("CostPrice")
        else:
            try:
                count = 1.0
                if SKU.find('*') >=0:
                    try:
                        count = float(SKU.replace(' ','').split('*')[1])
                    except:
                        count = 1.0
                    SKU = SKU.split('*')[0]                 
                b_goods_obj = py_b_goods.objects.get(SKU=SKU)
                cp = float(b_goods_obj.CostPrice) * count
                w = float(b_goods_obj.Weight) * count
            except:
                cp = None
                w = None
        return_value = {}
        return_value['CostPrice'] = str(cp)
        return_value['Weight'] = str(w)
        calculate_price_obj = calculate_price.calculate_profitRate(sellingPrice,platformCountryCode=platformCountryCode, DestinationCountryCode=DestinationCountryCode,kb=kb,price_des=price_des,currencycode=currencycode,category=category,sb_discount=sb_discount,bcd_rate=bcd_rate,yj_rate=yj_rate,xss_rate=xss_rate,Money=cp,Weight=w)
        return_value['sellingPrice_destination'] = str(calculate_price_obj['sellingPrice_destination'])
        return_value['sellingPrice_china'] = str(calculate_price_obj['sellingPrice_china'])
        return_value['sellingPrice'] = str(calculate_price_obj['sellingPrice'])
        return_value['profitRate'] = str(calculate_price_obj['profitRate'])
        return_value['logisticName'] = calculate_price_obj['logisticName']
        return_value['kickback'] = str(calculate_price_obj['kickback'])
        return_value['price_yf'] = str(calculate_price_obj['price_yf'])
        return_value['fd_money'] = str(calculate_price_obj['fd_money'])
        return_value['zyf'] = str((calculate_price_obj['price_yf']+calculate_price_obj['fd_money'])*calculate_price_obj['Discount']/100)
        return_value['logisticwaycode_desc'] = str(calculate_price_obj['logisticwaycode_desc']) 
        return_value['ExchangeRate'] = str(calculate_price_obj['ExchangeRate'])
        return_value['Discount'] = str(calculate_price_obj['Discount'])
        return_value['CURRENCYCODE'] = str(calculate_price_obj['CURRENCYCODE'])
        return_value['sb_discount'] = str(calculate_price_obj['sb_discount'])
        return_value['bcd_rate'] = str(calculate_price_obj['bcd_rate'])
        return_value['yj_rate'] = str(calculate_price_obj['yj_rate'])
        return_value['xss_rate'] = str(calculate_price_obj['xss_rate'])
        html_info = '<center>费用总和%s￥=(物流基本费用%s￥+物流分档费用%s￥)*物流折扣%s%%+成本价%s￥+平台扣除费用%s￥</center>'%(calculate_price_obj['sum_money'],calculate_price_obj['price_yf'],calculate_price_obj['fd_money'],calculate_price_obj['Discount'],calculate_price_obj['Money'],calculate_price_obj['basefee'])
        html_info = '%s<br><center>利润率%s%% = (1-平台扣点%s%%-费用总和%s/美元汇率%s/售价%s)*100</center>'%(html_info,calculate_price_obj['profitRate'],calculate_price_obj['kickback'],calculate_price_obj['sum_money'],calculate_price_obj['ExchangeRate_USD'],calculate_price_obj['sellingPrice'])
        return_value['html_info'] = html_info
    return HttpResponse(json.dumps(return_value), content_type="application/json")
    
def suanjia_test(request):
    from brick.pricelist.calculate_price_common import *
    from django.db import connection as conn
    SKU = request.GET.get("SKU")
    calculate_price = calculate_price(SKU,conn)
    sellingPrice = request.GET.get("SellPrice")
    return_value = {}
    calculate_price_obj = calculate_price.calculate_profitRate(sellingPrice)
    return_value['sellingPrice_destination'] = str(calculate_price_obj['sellingPrice_destination'])
    return_value['sellingPrice_china'] = str(calculate_price_obj['sellingPrice_china'])
    return_value['sellingPrice'] = str(calculate_price_obj['sellingPrice'])
    return_value['profitRate'] = str(calculate_price_obj['profitRate'])
    return_value['logisticName'] = calculate_price_obj['logisticName']
    return_value['kickback'] = str(calculate_price_obj['kickback'])
    return_value['ExchangeRate'] = str(calculate_price_obj['ExchangeRate'])
    return_value['Discount'] = str(calculate_price_obj['Discount'])
    return_value['CURRENCYCODE'] = str(calculate_price_obj['CURRENCYCODE'])
    return HttpResponse(json.dumps(return_value), content_type="application/json")


# 插件的处理方法，解决重复sku输入，给予提示
#author:wxb
@csrf_exempt
def repeat_sku(request):
    from skuapp.table.t_product_saler_requirement_photograph import *
    from skuapp.table.t_product_photograph import *
    if request.is_ajax() and request.method=="POST":
        url_location=request.POST.get('url_location').strip()
        SKU=request.POST.get('id_MainSKU').strip()
        if url_location=="t_product_saler_requirement_photograph":
            obj=t_product_saler_requirement_photograph.objects.filter(MainSKU=str(SKU))
        elif url_location=="t_product_photograph":
            obj=t_product_photograph.objects.filter(MainSKU=str(SKU),SampleState='notyet')
        elif url_location=="t_product_photo_alreadly":
            obj=t_product_photograph.objects.filter(MainSKU=str(SKU),SampleState='alreadly')
        else:
            return_value['exception']='exception'
        if len(obj)==0 or len(SKU)==0:
                    Bool="repeat_not"
        else:
                    Bool="repeat_yes"
        return_value= {}
        return_value['SKU']=str(Bool)
    return HttpResponse(json.dumps(return_value),content_type="application/json")
    
#处理搜索运营人员显示相应的店铺的函数
#author wxb
def t_config_searchplugin(request):
    # from skuapp.table.t_config_mstsc import *
    # from skuapp.table.t_store_configuration_file import *
    opeartor=request.GET.get('_ShopName_opeartor_')
    # shopname_list=[]
    # if  len(opeartor)!=0:
    #     shopname_objs=t_store_configuration_file.objects.filter(Operators=opeartor).values_list('ShopName',flat=True)
    #     if len(shopname_objs)!=0: 
    #         for shopname in shopname_objs:
    #             t_config_mstsc_objs=t_config_mstsc.objects.filter(ShopName__icontains=shopname[:shopname.rfind('-')]).values_list('ShopName',flat=True)
    #             shopname_list.extend(t_config_mstsc_objs)
    #         for i in range(len(shopname_list)):
    #             shopname_list[i]=shopname_list[i]+','
    #             shopname_str="".join(list(shopname_list))
    url='/Project/admin/skuapp/t_config_mstsc/?ShopName_opeartor_=%s'%opeartor


    # else:
    #     url='/Project/admin/skuapp/t_config_mstsc/'




    #return render(request,'test2.html',{'shopname':shopname_objs,'shopname2':shopname_list,'shopname_str':shopname_str})
    return HttpResponseRedirect(url)

# 插件的方法：查询主sku个数
#author：wxb
@csrf_exempt
def sku_countplugin(request):
    from skuapp.table.t_product_photo_ing import t_product_photo_ing
    from skuapp.table.t_product_photo_alreadly import t_product_photo_alreadly
    from skuapp.table.t_product_develop_ed import t_product_develop_ed
    from skuapp.table.t_product_art_ing import t_product_art_ing
    from skuapp.table.t_product_photograph import t_product_photograph
    from skuapp.table.t_product_mainsku_sku import t_product_mainsku_sku 
    if request.is_ajax() and request.method=="POST":
        is_checked=request.POST.get('is_checked').strip()
        is_cloth=request.POST.get('is_cloth').strip()
        url_location=request.POST.get('url_location').strip()
        check_obj=request.POST.get('check_val').strip()
        list_check=check_obj.split(',')
        return_value={}
        Main_sku_all=[]
        Main_sku=[]
        SKU_COUNT=[]
        SKU_COUNT_ALL=[] 
        catelist = [u'001.时尚女装', u'002.时尚男装', u'021.泳装', u'024.童装', u'025.内衣']
        if "t_product_photo_alreadly"==url_location:
            if is_checked=='not_checked':
                if is_cloth=='is_cloth':
                    Main_sku_all.extend(t_product_photo_alreadly.objects.filter(SampleState = 'alreadly',LargeCategory__in=catelist).values_list('MainSKU',flat=True).distinct())
                elif is_cloth=='not_cloth':
                    Main_sku_all.extend(t_product_photo_alreadly.objects.filter(SampleState = 'alreadly').exclude(LargeCategory__in=catelist).values_list('MainSKU',flat=True).distinct())
                else:
                    Main_sku_all.extend(t_product_photo_alreadly.objects.filter(SampleState = 'alreadly').values_list('MainSKU',flat=True).distinct())
                for i in range(len(Main_sku_all)):
                    if len(t_product_mainsku_sku.objects.filter(MainSKU=Main_sku_all[i]).values_list('ProductSKU',flat=True).distinct())!=0:
                        SKU_COUNT_ALL.extend(t_product_mainsku_sku.objects.filter(MainSKU=Main_sku_all[i]).values_list('ProductSKU',flat=True).distinct())
                    elif len(py_b_goods.objects.filter(SKU=Main_sku_all[i]).values_list('SKU',flat=True).distinct())!=0:
                        SKU_COUNT_ALL.extend(py_b_goods.objects.filter(SKU=Main_sku_all[i]).values_list('SKU',flat=True).distinct())
                    else:
                        SKU_COUNT_ALL.extend(t_product_photo_alreadly.objects.filter(MainSKU=Main_sku_all[i]).values_list('SKU',flat=True).distinct())
                SKU_COUNT_ALL=list(set(SKU_COUNT_ALL))
                return_value['check_val_all']=len(SKU_COUNT_ALL)

            if len(check_obj)!=0:
                for i in range(len(list_check)):
                    Main_sku.extend(t_product_photo_alreadly.objects.filter(id=list_check[i]).values_list('MainSKU',flat=True).distinct())
                for i in range(len(Main_sku)):
                    if len(t_product_mainsku_sku.objects.filter(MainSKU=Main_sku[i]).values_list('ProductSKU',flat=True).distinct())!=0:
                        SKU_COUNT.extend(t_product_mainsku_sku.objects.filter(MainSKU=Main_sku[i]).values_list('ProductSKU',flat=True).distinct())
                    elif len(py_b_goods.objects.filter(SKU=Main_sku[i]).values_list('SKU',flat=True).distinct())!=0:
                        SKU_COUNT.extend(py_b_goods.objects.filter(SKU=Main_sku[i]).values_list('SKU',flat=True).distinct())
                    else:
                        SKU_COUNT.extend(t_product_photo_alreadly.objects.filter(MainSKU=Main_sku[i]).values_list('SKU',flat=True).distinct())
                SKU_COUNT=list(set(SKU_COUNT))
                return_value['check_val']=len(SKU_COUNT)
            else:
                return_value['check_val']='unchecked'
           
                
        elif 't_product_photo_ing'==url_location:
            if is_checked=='not_checked':        
                if is_cloth=='is_cloth':
                    Main_sku_all.extend(t_product_photo_ing.objects.filter(LargeCategory__in=catelist).values_list('MainSKU',flat=True).distinct())
                elif is_cloth=='not_cloth':
                    Main_sku_all.extend(t_product_photo_ing.objects.exclude(LargeCategory__in=catelist).values_list('MainSKU',flat=True).distinct())
                else:
                    Main_sku_all.extend(t_product_photo_ing.objects.values_list('MainSKU',flat=True).distinct())
                for i in range(len(Main_sku_all)):
                    if len(t_product_mainsku_sku.objects.filter(MainSKU=Main_sku_all[i]).values_list('ProductSKU',flat=True).distinct())!=0:
                        SKU_COUNT_ALL.extend(t_product_mainsku_sku.objects.filter(MainSKU=Main_sku_all[i]).values_list('ProductSKU',flat=True).distinct())
                    elif len(py_b_goods.objects.filter(SKU=Main_sku_all[i]).values_list('SKU',flat=True).distinct())!=0:
                        SKU_COUNT_ALL.extend(py_b_goods.objects.filter(SKU=Main_sku_all[i]).values_list('SKU',flat=True).distinct())
                    else:
                        SKU_COUNT_ALL.extend(t_product_photo_ing.objects.filter(MainSKU=Main_sku_all[i]).values_list('SKU',flat=True).distinct())
                SKU_COUNT_ALL=list(set(SKU_COUNT_ALL))
                return_value['check_val_all']=len(SKU_COUNT_ALL)

            if len(check_obj)!=0:
                for i in range(len(list_check)):
                    Main_sku.extend(t_product_photo_ing.objects.filter(id=list_check[i]).values_list('MainSKU',flat=True).distinct())
                for i in range(len(Main_sku)):
                    if len(t_product_mainsku_sku.objects.filter(MainSKU=Main_sku[i]).values_list('ProductSKU',flat=True).distinct())!=0:
                        SKU_COUNT.extend(t_product_mainsku_sku.objects.filter(MainSKU=Main_sku[i]).values_list('ProductSKU',flat=True).distinct())
                    elif len(py_b_goods.objects.filter(SKU=Main_sku[i]).values_list('SKU',flat=True).distinct())!=0:
                        SKU_COUNT.extend(py_b_goods.objects.filter(SKU=Main_sku[i]).values_list('SKU',flat=True).distinct())
                    else:
                        SKU_COUNT.extend(t_product_photo_ing.objects.filter(MainSKU=Main_sku[i]).values_list('SKU',flat=True).distinct())
                SKU_COUNT=list(set(SKU_COUNT))
                return_value['check_val']=len(SKU_COUNT)
            else:
                return_value['check_val']='unchecked'
                   
        elif 't_product_develop_ed'==url_location:
            if is_checked=='not_checked':
                if is_cloth=='is_cloth':
                    Main_sku_all.extend(t_product_develop_ed.objects.filter(LargeCategory__in=catelist).values_list('MainSKU',flat=True).distinct())
                elif is_cloth=='not_cloth':
                    Main_sku_all.extend(t_product_develop_ed.objects.exclude(LargeCategory__in=catelist).values_list('MainSKU',flat=True).distinct())
                else:
                    Main_sku_all.extend(t_product_develop_ed.objects.values_list('MainSKU',flat=True).distinct())        
                for i in range(len(Main_sku_all)):
                    if len(t_product_mainsku_sku.objects.filter(MainSKU=Main_sku_all[i]).values_list('ProductSKU',flat=True).distinct())!=0:
                        SKU_COUNT_ALL.extend(t_product_mainsku_sku.objects.filter(MainSKU=Main_sku_all[i]).values_list('ProductSKU',flat=True).distinct())
                    elif len(py_b_goods.objects.filter(SKU=Main_sku_all[i]).values_list('SKU',flat=True).distinct())!=0:
                        SKU_COUNT_ALL.extend(py_b_goods.objects.filter(SKU=Main_sku_all[i]).values_list('SKU',flat=True).distinct())
                    else:
                        SKU_COUNT_ALL.extend(t_product_develop_ed.objects.filter(MainSKU=Main_sku_all[i]).values_list('SKU',flat=True).distinct())
                SKU_COUNT_ALL=list(set(SKU_COUNT_ALL))
                return_value['check_val_all']=len(SKU_COUNT_ALL)

            if len(check_obj)!=0:
                for i in range(len(list_check)):
                    Main_sku.extend(t_product_develop_ed.objects.filter(id=list_check[i]).values_list('MainSKU',flat=True).distinct())
                for i in range(len(Main_sku)):
                    if len(t_product_mainsku_sku.objects.filter(MainSKU=Main_sku[i]).values_list('ProductSKU',flat=True).distinct())!=0:
                        SKU_COUNT.extend(t_product_mainsku_sku.objects.filter(MainSKU=Main_sku[i]).values_list('ProductSKU',flat=True).distinct())
                    elif len(py_b_goods.objects.filter(SKU=Main_sku[i]).values_list('SKU',flat=True).distinct())!=0:
                        SKU_COUNT.extend(py_b_goods.objects.filter(SKU=Main_sku[i]).values_list('SKU',flat=True).distinct())
                    else:
                        SKU_COUNT.extend(t_product_develop_ed.objects.filter(MainSKU=Main_sku[i]).values_list('SKU',flat=True).distinct())
                SKU_COUNT=list(set(SKU_COUNT))
                return_value['check_val']=len(SKU_COUNT)
            else:
                return_value['check_val']='unchecked'

        elif 't_product_art_ing'==url_location:
            if is_checked=='not_checked':
                if is_cloth=='is_cloth':
                    Main_sku_all.extend(t_product_art_ing.objects.filter(LargeCategory__in=catelist).values_list('MainSKU',flat=True).distinct())
                elif is_cloth=='not_cloth':
                    Main_sku_all.extend(t_product_art_ing.objects.exclude(LargeCategory__in=catelist).values_list('MainSKU',flat=True).distinct())
                else:
                    Main_sku_all.extend(t_product_art_ing.objects.values_list('MainSKU',flat=True).distinct())         
                for i in range(len(Main_sku_all)):
                    if len(t_product_mainsku_sku.objects.filter(MainSKU=Main_sku_all[i]).values_list('ProductSKU',flat=True).distinct())!=0:
                        SKU_COUNT_ALL.extend(t_product_mainsku_sku.objects.filter(MainSKU=Main_sku_all[i]).values_list('ProductSKU',flat=True).distinct())
                    elif len(py_b_goods.objects.filter(SKU=Main_sku_all[i]).values_list('SKU',flat=True).distinct())!=0:
                        SKU_COUNT_ALL.extend(py_b_goods.objects.filter(SKU=Main_sku_all[i]).values_list('SKU',flat=True).distinct())
                    else:
                        SKU_COUNT_ALL.extend(t_product_art_ing.objects.filter(MainSKU=Main_sku_all[i]).values_list('SKU',flat=True).distinct())
                SKU_COUNT_ALL=list(set(SKU_COUNT_ALL))
                return_value['check_val_all']=len(SKU_COUNT_ALL)

            if len(check_obj)!=0:
                for i in range(len(list_check)):
                    Main_sku.extend(t_product_art_ing.objects.filter(id=list_check[i]).values_list('MainSKU',flat=True).distinct())
                for i in range(len(Main_sku)):
                    if len(t_product_mainsku_sku.objects.filter(MainSKU=Main_sku[i]).values_list('ProductSKU',flat=True).distinct())!=0:
                        SKU_COUNT.extend(t_product_mainsku_sku.objects.filter(MainSKU=Main_sku[i]).values_list('ProductSKU',flat=True).distinct())
                    elif len(py_b_goods.objects.filter(SKU=Main_sku[i]).values_list('SKU',flat=True).distinct())!=0:
                        SKU_COUNT.extend(py_b_goods.objects.filter(SKU=Main_sku[i]).values_list('SKU',flat=True).distinct())
                    else:
                        SKU_COUNT.extend(t_product_art_ing.objects.filter(MainSKU=Main_sku[i]).values_list('SKU',flat=True).distinct())
                SKU_COUNT=list(set(SKU_COUNT))
                return_value['check_val']=len(SKU_COUNT)
            else:
                return_value['check_val']='unchecked'


        

    return HttpResponse(json.dumps(return_value),content_type="application/json")







def amazon_prodcut_variation(request):
    from skuapp.table.t_templet_amazon_published_variation import t_templet_amazon_published_variation

    prodcut_variation_id = request.GET.get('pvi')
    t_templet_amazon_published_variation_objs = t_templet_amazon_published_variation.objects.filter(prodcut_variation_id=prodcut_variation_id)
    prodcut_variation_list = []
    if t_templet_amazon_published_variation_objs:
        for t_templet_amazon_published_variation_obj in t_templet_amazon_published_variation_objs:
            variation_value = ''
            if t_templet_amazon_published_variation_obj.variation_theme == 'Color':
                variation_value = t_templet_amazon_published_variation_obj.color_name
            if t_templet_amazon_published_variation_obj.variation_theme == 'Size':
                variation_value = t_templet_amazon_published_variation_obj.size_name
            if t_templet_amazon_published_variation_obj.variation_theme == 'Size-Color':
                variation_value = t_templet_amazon_published_variation_obj.size_name + '--' + \
                                  t_templet_amazon_published_variation_obj.color_name
            if t_templet_amazon_published_variation_obj.variation_theme == 'MetalType':
                variation_value = t_templet_amazon_published_variation_obj.MetalType
            if t_templet_amazon_published_variation_obj.variation_theme == 'MetalType-Size':
                variation_value = t_templet_amazon_published_variation_obj.MetalType + '--' + \
                                  t_templet_amazon_published_variation_obj.size_name
            prodcut_variation_list.append({'variation_theme':t_templet_amazon_published_variation_obj.variation_theme,
                                           'variation_value':variation_value,
                                           'child_sku':t_templet_amazon_published_variation_obj.child_sku,
                                           'item_quantity':t_templet_amazon_published_variation_obj.item_quantity,
                                           })
    return render(request, 't_templet_amazon_upload.html', {'prodcut_variation_list': prodcut_variation_list,})

    
    
def remove_wish_pic_update_flag(request):
    """
    去掉主图维护里的图片存在更新的标志和图片右上方new的标志
    """
    from skuapp.table.t_product_image_modify import t_product_image_modify
    from skuapp.table.t_product_mainsku_pic import t_product_mainsku_pic
    main_sku = request.GET.get('main_sku', '')
    t_product_mainsku_pic.objects.filter(MainSKU=main_sku).update(NewFlag=1)
    t_product_image_modify.objects.filter(MainSKU=main_sku).update(UpdateFlag=0)
    myResult = {'resultCode': 0}
    return JsonResponse(myResult)

@csrf_exempt
def t_tort_info_audit_ipfp(request):

    ipfvalue = request.GET.get('ipfvalue', '')
    idvalue = request.GET.get('ID', '')
    try:
        t_tort_info.objects.filter(ID=idvalue).update(IPForbiddenSite=ipfvalue)
        return JsonResponse({'result': 'OK'})
    except:
        return JsonResponse({'result': 'NG'})


def t_tort_info_image_info(request):
    idvalue = request.GET.get('ID', '')

    rt='<table  style="text-align:center;" border="1" cellpadding="3" cellspacing="1" bgcolor="#c1c1c1"><tr bgcolor="#7FFFAA"><th style="text-align:center">流水号</th><th style="text-align:center">店铺账号</th><th style="text-align:center">账号所有人</th><th style="text-align:center">主SKU</th><th style="text-align:center">侵权站点</th><th style="text-align:center">侵权类型</th><th style="text-align:center">IP范围</th><th style="text-align:center">IP禁用平台</th><th style="text-align:center">源头网站</th></tr>'
    objs = t_tort_info.objects.values('ID','Account','AccountStaffID','MainSKU','Site','Intellectual','IPRange','IPForbiddenSite','SourceUrl').filter(ID=idvalue)
    for obj in objs:
        rt = '%s <tr bgcolor="#FFFFFF"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr> '%(rt,obj['ID'],obj['Account'],obj['AccountStaffID'],obj['MainSKU'],obj['Site'],obj['Intellectual'],obj['IPRange'],obj['IPForbiddenSite'],obj['SourceUrl'])
    rt = "%s</table>"%rt

    return render(request, 'SKU.html', {'rt': rt})
    
def t_config_mstsc_user_per(request):
    from brick.table.t_config_mstsc_user import t_config_mstsc_user
    username = request.user
    t_config_mstsc_user_objs = t_config_mstsc_user(connection)
    t_config_mstsc_user_obj = t_config_mstsc_user_objs.getdata(username)
    if t_config_mstsc_user_obj:
        return HttpResponseRedirect("/Project/admin/skuapp/t_config_mstscfinance/")
    else:
        return HttpResponseRedirect("/Project/admin/skuapp/t_config_mstscfinance_user/")

    
@csrf_exempt
def op_t_wish_pb(request):
    from datetime import datetime

    url = request.path
    param = {}
    pbid = request.POST.get('pbid', '')  # 流水号
    x = request.POST.get('access_token', '')
    if x != '':
        param[str('access_token')] = str(x)
    x = request.POST.get('id', '')
    if x != '':
        param[str('id')] = str(x)

    if 'keywords' in url:
        _prarm = {}
        _prarm['access_token'] = param['access_token']
        _prarm['keyword'] = param['id']
        _prarm['exclude_keywords'] = []
        _prarm['limit'] = 10
        try:
            x = getKeyWords(_prarm)
            if x['retcode'] == 0:
                KWs = []
                data = x['data']['data']
                for v in sorted(data, key=lambda x: x['Keyword']['hotness']):
                    keyword = v['Keyword']
                    KWs.append(keyword)

                return JsonResponse({'result': 'OK', 'data': KWs})

            else:
                return JsonResponse({'result': 'NG', 'data': x['data']})
        except Exception, ex:
            return JsonResponse({'result':'NG', 'data': repr(ex)})
    elif 'stop' in url:
        try:
            x = StopCampaign(param)
            if x['retcode'] == 0:
                t_wish_pb.objects.filter(id=pbid).update(campaign_state='STOPPED',
                                                         updatetime=datetime.now(),
                                                         StaffID=request.user.username)

                # 联动取消新广告20180625
                objs = t_wish_pb.objects.filter(id=pbid).values('product_id')

                productid = objs[0]['product_id']
                t_wish_pb.objects.filter(product_id=productid, campaign_state='NEW').update(campaign_state='CANCELLED',
                                                                                     updatetime=datetime.now(),
                                                                                     StaffID=request.user.username)

                messages.success(request, u'已计划停止成功 %s ....' % param['id'])

                return JsonResponse({'result': 'OK'})
            else:
                if 'already' in x['data']:
                    # 后台广告已是停止的
                    t_wish_pb.objects.filter(id=pbid).update(campaign_state='STOPPED',
                                                             updatetime=datetime.now(),
                                                             StaffID=request.user.username)

                    messages.success(request, u'后台广告已停止 %s ....' % param['id'])

                    return JsonResponse({'result': 'OK'})
                else:
                    return JsonResponse({'result': x['data']})
        except Exception, ex:
            return JsonResponse({'result': repr(ex)})

    elif 'cancel' in url:
        try:
            x = CancelCampaign(param)
            if x['retcode'] == 0:
                t_wish_pb.objects.filter(id=pbid).update(campaign_state='CANCELLED',
                                                         updatetime=datetime.now(),
                                                         StaffID=request.user.username)

                messages.success(request, u'已取消成功 %s ....' % param['id'])

                return JsonResponse({'result': 'OK'})
            else:
                if 'already' in x['data']:
                    # 后台广告已是停止的
                    t_wish_pb.objects.filter(id=pbid).update(campaign_state='CANCELLED',
                                                             updatetime=datetime.now(),
                                                             StaffID=request.user.username)

                    messages.success(request, u'后台广告已取消 %s ....' % param['id'])

                    return JsonResponse({'result': 'OK'})
                else:
                    return JsonResponse({'result': x['data']})
        except Exception, ex:
            return JsonResponse({'result': repr(ex)})
    else:
        return JsonResponse({'result': 'invalid url:%s'%url})



def update_info(request):
    sResult = {}
    try:
        import datetime
        from skuapp.table.t_work_flow_of_plate_house import t_work_flow_of_plate_house
        from skuapp.table.t_work_battledore import t_work_battledore
        from skuapp.table.t_stocking_purchase_order import t_stocking_purchase_order
        from skuapp.table.t_product_suvering import t_product_suvering
        from skuapp.table.t_supply_chain_production_basic_permission import t_supply_chain_production_basic_permission
        from pyapp.table.kc_unsalable_dispose import kc_unsalable_dispose
        from skuapp.table.t_sku_weight_examine import t_sku_weight_examine
        from skuapp.table.t_progress_tracking_of_product_customization_table import t_progress_tracking_of_product_customization_table

        udata = {}
        id = request.GET.get('id')
        key = request.GET.get('key')
        value = request.GET.get('value')
        type = request.GET.get('type')
        workobjs = None
        supply_chain_flag=False
        supply_chain_update_flag=False
        if type == '0':
            workobjs = t_work_flow_of_plate_house.objects.filter(id=id)
        elif type == '1':
            workobjs = t_work_battledore.objects.filter(id=id)
        elif type == 't_stocking_purchase_order':
            workobjs = t_stocking_purchase_order.objects.filter(id=id)
            if key == "Single_number" and len(value) > 0:
                t_stocking_purchase_order.objects.filter(id=id).update(Status='purchasing')
        elif type == 't_supply_chain_production_basic':
            if key:
                workobjs=t_supply_chain_production_basic.objects.filter(id=id)
                _workobjs=workobjs.first()
                EditFlag=json.loads(_workobjs.EditFlag) if _workobjs.EditFlag else {}
                _permission = t_supply_chain_production_basic_permission.objects.filter(
                    username=request.user.username).values_list('username')
                permission = [x[0] for x in _permission]
                if request.user.is_superuser or permission or _workobjs.Lock==0:
                    pass
                elif not EditFlag.get(key):
                    EditFlag[key]=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    supply_chain_update_flag=True

                elif EditFlag.get(key):
                    supply_chain_flag=True
        elif type == 't_product_suvering':
            workobjs = t_product_suvering.objects.filter(id=id)
        elif type == 'kc_unsalable_H':
            workobjs = kc_unsalable_dispose.objects.filter(id=id)
            data = value.split(':')
            value = data[1]
            udata['DataFlag'] = data[0]
            if data[0] in ('3', '4', '5', '6', '7'):
                if workobjs[0].Remark1 is None or workobjs[0].Remark1.strip() == '':
                    if data[0] in ('3', '6'):
                        errmsg = u'请备注相关打折退信息！'
                    elif data[0] in ('4', '5'):
                        errmsg = u'请备注相关部分退的信息！'
                    else:
                        errmsg = u'请备注无法退货的原因！'
                    sResult['Code'] = -1
                    sResult['messages'] = errmsg
                    return JsonResponse(sResult)

            if data[0] in ('3', '6'):
                udata['AuditResults'] = u'未审核'  # 打折退需要审核

            udata['HandleTime'] = datetime.datetime.now()
            udata['HandleMan'] = request.user.first_name
        elif type == 'kc_unsalable_A':
            workobjs = kc_unsalable_dispose.objects.filter(id=id)
            udata['HandleTime'] = datetime.datetime.now()
            udata['AuditMan'] = request.user.first_name

        elif type == 't_sku_weight_examine':
            workobjs = t_sku_weight_examine.objects.filter(id=id)
        elif type == 't_progress_tracking_of_product_customization_table':
            workobjs = t_progress_tracking_of_product_customization_table.objects.filter(id=id)
        else:
            raise Exception(u'没有对应的type值：{s}'.format(s=type))
        if supply_chain_flag:
            sResult['Code'] = -2
            sResult['messages'] = '权限不足,只能修改一次!请联系超级权限用户'
            return JsonResponse(sResult)

        if key:
            udata[key] = value

        if workobjs and udata:
            workobjs.update(**udata)
        if supply_chain_update_flag:
            workobjs.update(EditFlag=json.dumps(EditFlag))

        sResult['Code'] = 1
        sResult['udata'] = udata
    except Exception, e:
        sResult['Code'] = -1
        sResult['messages'] = '%s:%s' % (Exception, e)
    return JsonResponse(sResult)

















#获取4种不同平台商品详情页信息ajax
@csrf_exempt
def get_survey_results_info(request):
    WISH_URL = 'wish.'
    AMAZON_URL = 'amazon.'
    WWW1688_URL = '1688.'
    EBAY_URL = 'ebay.'
    ALIEXPRESS_URL = 'aliexpress.'
    import json
    # from brick.spider.get_web_survey_results_info import get_info_by_url
    from brick.spider.get import readWish,readAmazon,readeBay,readAliexpress
    # from storeapp.models import t_online_info_wish_store
    from skuapp.table.t_online_info import t_online_info

    err, fifteenOrders, priceRange, enTitle, cnTitle, imageUrl = None,"","","","",""
    message = {"error":1}
    # if request.is_ajax() and request.method == "GET":
    url = request.GET.get('url')
    flag = request.GET.get('flag')
    print(url)
    try:
        if url.find(WISH_URL) >= 0:  # wish的数据采集
            if flag == '1':
                productid = url.split('/')[-1]
                imageUrl = u'https://contestimg.wish.com/api/webimage/%s-medium.jpg' % productid

                # 是不是wish？？？
                pricelist = t_online_info.objects.filter(ProductID=productid,Size='L').values_list('Price', 'Shipping')
                if pricelist.exists():
                    priceRange = float(pricelist[0][0]) + float(pricelist[0][1]) # 直接在online表格中查询 价格

            if not priceRange:
                err, fifteenOrders, priceRange, enTitle, cnTitle, imageUrl = readWish(url)

        if url.find(AMAZON_URL) >= 0:  # amazon的数据采集
            err, fifteenOrders, priceRange, enTitle, cnTitle, imageUrl = readAmazon(url)
            # err = "amazon not support"
        if url.find(EBAY_URL) >= 0:  # EBAY的数据采集
            err, fifteenOrders, priceRange, enTitle, cnTitle, imageUrl = readeBay(url)
        if url.find(ALIEXPRESS_URL) >= 0:  # aliexpress的数据采集
            err, enTitle, imageUrl, priceRange, fifteenOrders = readAliexpress(url)
            if flag == '1':
                priceRange = eval(priceRange)[0]
        if err is None:
            message = {"error":0,'errmsg':err,'fifteenOrders':fifteenOrders,'priceRange':priceRange,'enTitle':enTitle,
                       'cnTitle':cnTitle,'imageUrl':imageUrl}
        else:
            message = {"error": 1, 'errmsg': err}
            # messages.error(request,"--------%s"%message)
    except Exception,e:
        message = {"error": 1, 'errmsg': "%s:%s" % (Exception,e)}
    return HttpResponse(json.dumps(message))












#获取1688商品页相关信息ajax API
@csrf_exempt
def get_ali1688_page_info(request):
    import json
    import datetime
    from reportapp.models import t_report_supplier_sku_m
    from pyapp.table.t_product_b_goods import t_product_b_goods
    from pyapp.models import B_Supplier
    from django.db.models import Q
    from  pyapp.models import b_supplier_money
    # from brick.spider.get_ali1688_page_info import get_info_by_url
    from brick.spider.get import read1688
    err, suppliertitle, suppliername, supplierimgurl, priceRange = None,"","","",""
    message = {"error":1}
    # if request.is_ajax() and request.method == "GET":
    url = request.GET.get('url')
    print(url)
    try:
        err,suppliername,suppliertitle,supplierimgurl, priceRange = read1688(url)
        print("+++++++++++++++++++++++++get over")
        print(err,suppliertitle,suppliername,supplierimgurl, priceRange)
    except:
        err = "request err"
    
    if err is None:
        message = {"error":0,'errmsg': err,'suppliertitle':suppliertitle,'suppliername':suppliername,
                   'supplierimgurl':supplierimgurl,'priceRange':priceRange,'supplierSkuCount':0,
                   'cgSkuCount':0,'CGALLmoney':0,'query_code':0}
        try:
            lastMonth = datetime.datetime.now().strftime('%Y%m')

            if lastMonth[-2:] == '01':
                lastMonth = str((int(lastMonth[:4]) - 1)) + '12'
            else:
                lastMonth = str(int(lastMonth) - 1)

            SupplierName_num_objs = b_supplier_money.objects.filter(SupplierName=suppliername).values('CGSKUcount','CGALLmoney')
            if SupplierName_num_objs:
                message['cgSkuCount'] = SupplierName_num_objs[0]['CGSKUcount']
                message['CGALLmoney'] = str(SupplierName_num_objs[0]['CGALLmoney'])

            SupplierID_param = B_Supplier.objects.filter(SupplierName=suppliername).values('NID')
            if SupplierID_param:
                message['supplierSkuCount'] = t_product_b_goods.objects.filter(Q(GoodsStatus='正常')|Q(GoodsStatus='临时下架')|Q(GoodsStatus='在售'),SupplierID=SupplierID_param[0]['NID'],Used=0).count()        
        except Exception,ex:
            #messages.error(request,'%s_%s:%s'%(traceback.print_exc(),Exception,ex))
            message['query_code'] = 1
    else:
        message = {"error": 1, 'errmsg': err ,'query_code':1}
        
    # messages.error(request,"--------%s"%message)
    return HttpResponse(json.dumps(message))
    
@csrf_exempt
def sales_trend(request):
    try:
        import uuid, time, datetime
        returndata = {}
        SKU = request.GET.get('SKU', '')
        ProductID = request.GET.get('ProductID', '')
        SKUType = request.GET.get('SKUType', '')
        MarketingTime = request.GET.get('MarketingTime', '')
        ReviewTime = request.GET.get('ReviewTime', '')
        if SKU is None:
            SKU = 'TestDemo'
            ProductID = '1510822698731674141-209-1-709-3816824524'
        title = u'SKU:%s 商品日订单量' % (SKU)
        #messages.info(request, '001:%s'%(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        #messages.info(request,'%s,%s,%s,%s'%(SKU,ProductID,MarketingTime,ReviewTime))
        if SKUType == "productsku":
            sql = '''select OrderDay,sum(SalesVolume),count(1) from t_report_sales_daily WHERE SKU='%s' and ProductID='%s' group by OrderDay order by OrderDay ASC ''' % (SKU,ProductID,)
        else:
            sql = '''select OrderDay,sum(SalesVolume),count(1) from t_report_sales_daily WHERE MainSKU='%s' and ProductID='%s' group by OrderDay order by OrderDay ASC ''' % (
            SKU, ProductID,)
        with connection.cursor() as cursor:
            cursor.execute(sql)
            objs = cursor.fetchall()
        #messages.info(request, 'MarketingTime=%s,ReviewTime=%s'%(MarketingTime,ReviewTime))
        daylist = []
        saleslist = []
        salesCountlist = []
        MarketingList = []
        ReviewList = []
        index1 = 0
        index2 = 0
        #将未录入的日期生成
        allDaySalers = []
        currentDate = time.strftime('%Y%m%d', time.localtime(time.time()))
        strMinTime = currentDate
        strMaxTime = currentDate
        for row in objs:
            if cmp(row[0].strftime('%Y%m%d'), strMinTime) < 0:
                strMinTime = row[0].strftime('%Y%m%d')
            if cmp(row[0].strftime('%Y%m%d'), strMaxTime) > 0:
                strMaxTime = row[0].strftime('%Y%m%d')
        if MarketingTime is not None and MarketingTime != '' and MarketingTime != 'None' and cmp(MarketingTime, strMinTime) < 0:
            strMinTime = MarketingTime
        if MarketingTime is not None and MarketingTime != '' and MarketingTime != 'None' and cmp(MarketingTime, strMaxTime) > 0:
            strMaxTime = MarketingTime
        if ReviewTime is not None and ReviewTime != '' and ReviewTime != 'None' and cmp(ReviewTime, strMinTime) < 0:
            strMinTime = ReviewTime
        if ReviewTime is not None and ReviewTime != '' and ReviewTime != 'None' and cmp(ReviewTime, strMaxTime) > 0:
            strMaxTime = ReviewTime
        for row1 in objs:
            while True:
                flag = 0
                listTemp = []
                if cmp(row1[0].strftime('%Y%m%d'), strMinTime) > 0:
                    listTemp.append(strMinTime)
                    listTemp.append(0)
                    listTemp.append(0)
                if cmp(row1[0].strftime('%Y%m%d'), strMinTime) == 0:
                    listTemp.append(strMinTime)
                    listTemp.append(int(row1[1]))
                    listTemp.append(int(row1[2]))
                    flag = 1
                allDaySalers.append(listTemp)
                tmpDate = datetime.datetime.strptime(strMinTime,'%Y%m%d')
                addDate = tmpDate + datetime.timedelta(days=1)
                strMinTime = addDate.strftime('%Y%m%d')
                if flag == 1:
                    break
        while True:
            listTemp = []
            if cmp(strMaxTime, strMinTime) > 0:
                listTemp.append(strMinTime)
                listTemp.append(0)
                listTemp.append(0)
                allDaySalers.append(listTemp)
            if cmp(strMaxTime, strMinTime) == 0:
                listTemp.append(strMinTime)
                listTemp.append(0)
                listTemp.append(0)
                allDaySalers.append(listTemp)
                break
            tmpDate = datetime.datetime.strptime(strMinTime, '%Y%m%d')
            addDate = tmpDate + datetime.timedelta(days=1)
            strMinTime = addDate.strftime('%Y%m%d')
        for obj in allDaySalers:
            if cmp(obj[0], MarketingTime) == 0 and index1 == 0 and MarketingTime is not None and MarketingTime != '' and MarketingTime != 'None':
                index1 = len(daylist) + 1
            elif cmp(obj[0], MarketingTime) > 0 and index1 == 0 and MarketingTime is not None and MarketingTime != '' and MarketingTime != 'None':
                index1 = len(daylist) + 1
                daylist.append(MarketingTime)
                saleslist.append(0)
                salesCountlist.append(0)
            if cmp(obj[0], ReviewTime) == 0 and index2 == 0 and ReviewTime is not None and ReviewTime != '' and ReviewTime != 'None':
                index2 = len(daylist) + 1
            elif cmp(obj[0], ReviewTime) > 0 and index2 == 0 and ReviewTime is not None and ReviewTime != '' and ReviewTime != 'None':
                index2 = len(daylist) + 1
                daylist.append(ReviewTime)
                saleslist.append(0)
                salesCountlist.append(0)
            daylist.append('%s' % obj[0])
            saleslist.append(int(obj[1]))
            salesCountlist.append(int(obj[2]))
        if index1 == 0 and len(objs) > 0 and MarketingTime is not None and MarketingTime != '' and MarketingTime != 'None':
            index1 = len(daylist) + 1
            daylist.append(MarketingTime)
            saleslist.append(0)
            salesCountlist.append(0)
        if index2 == 0 and len(objs) > 0 and ReviewTime is not None and ReviewTime != '' and ReviewTime != 'None':
            index2 = len(daylist) + 1
            daylist.append(ReviewTime)
            saleslist.append(0)
            salesCountlist.append(0)

        if MarketingTime is None:
            index1 = len(saleslist) + 100
        if ReviewTime is None:
            index2 = len(saleslist) + 100

        returndata = {'title': title,
                      'daylist': json.dumps(daylist),
                      'saleslist': json.dumps(saleslist),
                      'MarketingTime':MarketingTime,
                      'ReviewTime':ReviewTime,
                      'index1': index1,
                      'index2': index2,
                      'MarketingList':json.dumps(MarketingList),
                      'ReviewList':json.dumps(ReviewList),
                      'salesCountlist':json.dumps(salesCountlist)}
    except Exception as e:
        messages.info(request,u'商品(%s)日销量取数据错误，请联系开发人员查看原因。'%(SKU))
    return render(request, 'sales_trend.html', returndata)

@csrf_exempt
def importfile_marketing(request):
    try:
        downloadmodel = request.POST.get('downloadmodel')
        if downloadmodel == "downloadmodel0001":
            # 写execl
            from Project.settings import *
            import oss2
            from xlwt import *
            from skuapp.modelsadminx.t_product_Admin import mkdir_p
            path = MEDIA_ROOT + 'download_xls/' + request.user.username
            mkdir_p(MEDIA_ROOT + 'download_xls')
            os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))
            mkdir_p(path)
            os.popen('chmod 777 %s' % (path))
            w = Workbook()
            sheet = w.add_sheet('sheet1')
            XLS_FIELDS = (u'SKU类型(productsku-商品SKU mainsku-主SKU)', u'商品SKU或主SKU', u'产品ID', u'普源店铺名称', u'调研日期', u'刊登日期',
            u'英文关键词', u'初步定价',u'初步定价最大值', u'反向链接', u'营销时间', u'留评时间')
            for index, item in enumerate(XLS_FIELDS):
                sheet.write(0, index, item)
            filename = request.user.username + '_downloadmodel' + '.xls'
            w.save(path + '/' + filename)
            os.popen(r'chmod 777 %s' % (path + '/' + filename))
            # 上传oss对象
            auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
            bucket = oss2.Bucket(auth, ENDPOINT, BUCKETNAME_XLS)
            bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)
            # 删除现有的
            for object_info in oss2.ObjectIterator(bucket,prefix='%s/%s_' % (request.user.username, request.user.username)):
                bucket.delete_object(object_info.key)
            bucket.put_object(u'%s/%s' % (request.user.username, filename), open(path + '/' + filename))
            messages.error(request, u'%s%s.%s/%s/%s' % (PREFIX, BUCKETNAME_XLS, ENDPOINT_OUT, request.user.username,filename) + u':成功导出模版,可点击Download下载到本地............................。')
            return HttpResponseRedirect('/Project/admin/skuapp/t_marketing_review_trace/')
        else:
            if request.FILES.get('myfile') is not None:
                user_name = request.user.first_name
                file_obj = request.FILES['myfile']

                import xlrd
                from xlrd import xldate_as_tuple
                from skuapp.table.t_marketing_review_trace import t_marketing_review_trace
                from datetime import datetime as YXDate
                from skuapp.table.public import *
                from brick.pricelist.calculate_price import calculate_price as joom_calculate_price
                # SKUtype类型 sku  ProductID  ShopName店铺名 调研时间  刊登日期  英文关键字   初步定价    反向链接    营销时间   留言时间
                insertinto = []
                wb = xlrd.open_workbook(filename=None, file_contents=file_obj.read())  # 关键点在于这里
                table = wb.sheets()[0]
                row = table.nrows
                for i in xrange(1, row):
                    col = table.row_values(i)
                    SKUType = col[0].strip()
                    strSKU = col[1].strip()
                    strProductID = str(col[2]).strip()
                    strShopName = col[3].strip()
                    if str(col[4]).strip().find('-') > 0:
                        DYDate = str(col[4]).strip()
                    else:
                        DYDate = str(YXDate(*xldate_as_tuple(col[4],0)))[:10]
                    if str(col[5]).strip().find('-') > 0:
                        PublishDate = str(col[5]).strip()
                    else:
                        PublishDate = str(YXDate(*xldate_as_tuple(col[5],0)))[:10]
                    #messages.info(request, 'test00003  %s,%s' % (PublishDate, DYDate))
                    #PublishDate = str(col[5]).strip()
                    EnKeys = str(col[6]).strip()
                    prePrice = str(col[7])
                    prePriceMax = str(col[8])
                    ReverseLink = col[9].strip()
                    if col[10] is not None and str(col[10]).strip() != '':
                        if str(col[10]).strip().find('-') > 0:
                            MarketingTime = str(col[10]).strip()
                        else:
                            MarketingTime = str(YXDate(*xldate_as_tuple(col[10],0)))[:10]
                    else:
                        MarketingTime = None
                    if col[11] is not None and str(col[11]).strip() != '':
                        if str(col[11]).strip().find('-') > 0:
                            ReviewTime = str(col[11]).strip()
                        else:
                            ReviewTime = str(YXDate(*xldate_as_tuple(col[11],0)))[:10]
                    else:
                        ReviewTime = None

                    from joom_app.table.t_online_info_joom import t_online_info_joom
                    from joom_app.table.t_joom_price_parity_log import t_joom_price_parity_log
                    from joom_app.table.t_joom_competitor_product_info import t_joom_competitor_product_info
                    # 通过ProductID获取对手价格、对手利润率、对手上架时间（页面抓取不到）
                    # JOOM 取7天销量最好的商品（如果有多个店铺销售同一个商品，取一个7天销量最好的主SKU）
                    if strProductID.strip() == '':
                        messages.info(request, u'productID 不能为空值')
                        return HttpResponseRedirect('/Project/admin/skuapp/t_marketing_review_trace/')

                    strOpPrice = "0-0"
                    strOpProfitRate = "0.0%-0.0%"
                    CurrentPrice = prePrice
                    list_t_online_info_objs = t_online_info_joom.objects.filter(
                        ProductID=strProductID.strip()).values_list('MainSKU', flat=True)
                    if len(list_t_online_info_objs) != 0:
                        mainSKU = list_t_online_info_objs[0]
                        list_t_online_info_objs1 = t_online_info_joom.objects.filter(MainSKU=mainSKU).filter(~Q(competitor_ProductID=None)).order_by('-Orders7Days').values_list('competitor_ProductID', flat=True)
                        if len(list_t_online_info_objs1) != 0:
                            list_t_joom_competitor_product_info_objs = t_joom_competitor_product_info.objects.filter(ProductID=list_t_online_info_objs1[0].strip())
                            if len(list_t_joom_competitor_product_info_objs) != 0:
                                strOpPrice = str(list_t_joom_competitor_product_info_objs[0].minPrice) + "-" + str(list_t_joom_competitor_product_info_objs[0].maxPrice)
                                strOpProfitRate = str(list_t_joom_competitor_product_info_objs[0].minProfitRate) + "%-" + str(list_t_joom_competitor_product_info_objs[0].maxProfitRate) + "%"
                    list_t_joom_price_parity_log_objs = t_joom_price_parity_log.objects.filter(ProductID=strProductID.strip()).order_by('-ChangePriceDatetime')
                    if len(list_t_joom_price_parity_log_objs) != 0:
                        CurrentPrice = list_t_joom_price_parity_log_objs[0].NewPrice

                    zeroSellingPrice = 0.0
                    profitRate = '0.0%-0.0%'
                    if SKUType == "productsku":
                        try:
                            # 通过SKU获取零利润价格、利润率
                            calculate_price_obj = joom_calculate_price(strSKU)
                            sellingPrice_info = calculate_price_obj.calculate_selling_price(0)
                            zeroSellingPrice = float(sellingPrice_info['sellingPrice_us'])
                            profitRateMin_info = calculate_price_obj.calculate_profitRate(prePrice)
                            profitRateMax_info = calculate_price_obj.calculate_profitRate(prePriceMax)
                            profitRate = str(float(profitRateMin_info['profitRate'])) + '%-' + str(
                                float(profitRateMax_info['profitRate'])) + '%'
                        except Exception as e:
                            messages.info(request, u'productsku=%s,获取零利润价格存有问题(%s)，请联系开发人员。' % (strSKU, str(e)))
                            return HttpResponseRedirect('/Project/admin/skuapp/t_marketing_review_trace/')

                        insertinto.append(t_marketing_review_trace(
                            SKU=strSKU, ProductID=strProductID,
                            ShopName=strShopName,DYDate=DYDate,
                            PublishDate=PublishDate, EnKeys=EnKeys, ZeroProfitPrice=zeroSellingPrice,
                            PrePrice=prePrice,MaxPrePrice=prePriceMax, CurrentPrice=CurrentPrice,ProfitPrice=profitRate,
                            ReverseLink=ReverseLink,OpPrice=strOpPrice,OpProfitPrice=strOpProfitRate,
                            MarketingTime=MarketingTime, ReviewTime=ReviewTime,
                            LRStaff=user_name,LRTime=YXDate.now(),SKUType=SKUType
                        ))
                    else:
                        # 主SKU类型，需要关联
                        from skuapp.table.t_product_mainsku_sku import t_product_mainsku_sku
                        listSKU = t_product_mainsku_sku.objects.filter(MainSKU=strSKU).values_list('ProductSKU', flat=True)
                        if len(listSKU) == 0:
                            messages.info(request, u'主SKU(%s)未查找到对应商品SKU.' % (strSKU))
                            return HttpResponseRedirect('/Project/admin/skuapp/t_marketing_review_trace/')
                        for subSKU in listSKU:
                            try:
                                # 通过SKU获取零利润价格、利润率
                                calculate_price_obj = joom_calculate_price(str(subSKU))
                                sellingPrice_info = calculate_price_obj.calculate_selling_price(0)
                                zeroSellingPrice = sellingPrice_info['sellingPrice_us']
                                profitRateMin_info = calculate_price_obj.calculate_profitRate(prePrice)
                                profitRateMax_info = calculate_price_obj.calculate_profitRate(prePriceMax)
                                profitRate = str(float(profitRateMin_info['profitRate'])) + '%-' + str(
                                    float(profitRateMax_info['profitRate'])) + '%'
                            except Exception as e:
                                messages.info(request,u'sku=%s,获取零利润价格存有问题(%s)，请联系开发人员。' % (subSKU, str(e)))
                                return HttpResponseRedirect('/Project/admin/skuapp/t_marketing_review_trace/')

                        insertinto.append(t_marketing_review_trace(
                            SKU=strSKU, ProductID=strProductID,
                            ShopName=strShopName, DYDate=DYDate,
                            PublishDate=PublishDate, EnKeys=EnKeys, ZeroProfitPrice=zeroSellingPrice,
                            PrePrice=prePrice,MaxPrePrice=prePriceMax, CurrentPrice=CurrentPrice, ProfitPrice=profitRate,
                            ReverseLink=ReverseLink, OpPrice=strOpPrice, OpProfitPrice=strOpProfitRate,
                            MarketingTime=MarketingTime, ReviewTime=ReviewTime,
                            LRStaff=user_name, LRTime=YXDate.now(), SKUType=SKUType
                        ))
                t_marketing_review_trace.objects.bulk_create(insertinto)
                messages.success(request,u'导入成功。')
    except Exception as e:
        messages.info(request,u'导入失败，请检查导入文档格式,error=%s'%(str(e)))
    return HttpResponseRedirect('/Project/admin/skuapp/t_marketing_review_trace/')  
    
def more_product_informations(request):
    obj_id = request.GET.get('flag_obj','')
    flag = request.GET.get('flag','')
    #try:
    if flag == 't_product_building':
        from skuapp.table.t_product_build_ing import t_product_build_ing
        t_product_build_ing_objs = t_product_build_ing.objects.filter(id=obj_id)
        for t_product_build_ing_obj in t_product_build_ing_objs:
            KFStaffName = t_product_build_ing_obj.KFStaffName
            KFTime = t_product_build_ing_obj.KFTime
            XJStaffName = t_product_build_ing_obj.XJStaffName
            XJTime = t_product_build_ing_obj.XJTime
            Name2 = t_product_build_ing_obj.Name2
            Keywords = t_product_build_ing_obj.Keywords
            SupplierPDes = t_product_build_ing_obj.SupplierPDes
            Pricerange  = t_product_build_ing_obj.Pricerange
            information_title = [u'开发',u'时间',u'询价',u'时间',u'商品名称(中文)',u'英文标题',u'供货商商品标题',u'价格区间']
            information_dec = [KFStaffName,KFTime,XJStaffName,XJTime,Name2,Keywords,SupplierPDes,Pricerange]
            information = {'information_title':information_title,'information_dec':information_dec}
    if flag == 't_product_enter_ed':
        from skuapp.table.t_product_enter_ed import t_product_enter_ed
        t_product_enter_ed_objs = t_product_enter_ed.objects.filter(id=obj_id)
        for t_product_enter_ed_obj in t_product_enter_ed_objs:
            KFStaffName = t_product_enter_ed_obj.KFStaffName
            KFTime = t_product_enter_ed_obj.KFTime
            JZLTime = t_product_enter_ed_obj.JZLTime
            JZLStaffName = t_product_enter_ed_obj.JZLStaffName
            Name2 = t_product_enter_ed_obj.Name2
            Keywords = t_product_enter_ed_obj.Keywords
            Pricerange = t_product_enter_ed_obj.Pricerange
            information_title = [u'开发', u'时间', u'建资料', u'时间', u'商品名称(中文)', u'英文标题', u'价格区间']
            information_dec = [KFStaffName, KFTime, JZLStaffName, JZLTime, Name2, Keywords, Pricerange]
            information = {'information_title': information_title, 'information_dec': information_dec}
    if flag == 'v_product_allsku':
        from skuapp.table.v_product_allsku import v_product_allsku
        v_product_allsku_objs = v_product_allsku.objects.filter(id=obj_id)
        for v_product_allsku_obj in v_product_allsku_objs:
            DYTime = v_product_allsku_obj.DYTime
            DYStaffName = v_product_allsku_obj.DYStaffName
            KFStaffName = v_product_allsku_obj.KFStaffName
            KFTime = v_product_allsku_obj.KFTime
            JZLTime = v_product_allsku_obj.JZLTime
            JZLStaffName = v_product_allsku_obj.JZLStaffName
            Name2 = v_product_allsku_obj.Name2
            Keywords = v_product_allsku_obj.Keywords
            Pricerange = v_product_allsku_obj.Pricerange
            information_title = [u'调研',u'时间',u'开发', u'时间', u'建资料', u'时间', u'商品名称(中文)', u'英文标题', u'价格区间']
            information_dec = [DYStaffName,DYTime,KFStaffName, KFTime, JZLStaffName, JZLTime, Name2, Keywords, Pricerange]
            information = {'information_title': information_title, 'information_dec': information_dec}
    if flag == 't_product_depart_get':
        from skuapp.table.t_product_depart_get import t_product_depart_get
        t_product_depart_get_objs = t_product_depart_get.objects.filter(id=obj_id)
        for t_product_depart_get_obj in t_product_depart_get_objs:
            DYTime = t_product_depart_get_obj.DYTime
            DYStaffName = t_product_depart_get_obj.DYStaffName
            KFStaffName = t_product_depart_get_obj.KFStaffName
            KFTime = t_product_depart_get_obj.KFTime
            JZLTime = t_product_depart_get_obj.JZLTime
            JZLStaffName = t_product_depart_get_obj.JZLStaffName
            Name2 = t_product_depart_get_obj.Name2
            Keywords = t_product_depart_get_obj.Keywords
            Pricerange = t_product_depart_get_obj.Pricerange
            ShelveDay = t_product_depart_get_obj.ShelveDay
            OrdersLast7Days = t_product_depart_get_obj.OrdersLast7Days
            information_title = [u'调研', u'时间', u'开发', u'时间', u'建资料', u'时间', u'商品名称(中文)', u'英文标题', u'价格区间',u'上架时间',u'15天order']
            information_dec = [DYStaffName, DYTime, KFStaffName, KFTime, JZLStaffName, JZLTime, Name2, Keywords, Pricerange,ShelveDay,OrdersLast7Days]
            information = {'information_title': information_title, 'information_dec': information_dec}
    if flag == 't_product_information_modify':
        from skuapp.table.t_product_information_modify import t_product_information_modify
        t_product_information_modify_objs = t_product_information_modify.objects.filter(id=obj_id)
        for t_product_information_modify_obj in t_product_information_modify_objs:
            Name2 = t_product_information_modify_obj.Name2
            Keywords = t_product_information_modify_obj.Keywords
            SQStaffNameing = t_product_information_modify_obj.SQStaffNameing
            SQTimeing = t_product_information_modify_obj.SQTimeing
            XGStaffName = t_product_information_modify_obj.XGStaffName
            XGTime = t_product_information_modify_obj.XGTime
            SHStaffName = t_product_information_modify_obj.SHStaffName
            SHTime = t_product_information_modify_obj.SHTime
            LQStaffName = t_product_information_modify_obj.LQStaffName
            LQTime = t_product_information_modify_obj.LQTime
            XGcontext = t_product_information_modify_obj.XGcontext    
            information_title = [u'申请人', u'申请时间', u'商品名称(中文)', u'英文标题',u'修改描述', u'修改',u'时间', u'审核', u'时间', u'领取',u'时间', ]
            information_dec = [SQStaffNameing, SQTimeing, Name2, Keywords, XGcontext, XGStaffName, XGTime, SHStaffName, SHTime, LQStaffName, LQTime]
            information = {'information_title': information_title, 'information_dec': information_dec}
    if flag == 't_product_modify_ed':
        from skuapp.table.t_product_modify_ed import t_product_modify_ed
        t_product_modify_ed_objs = t_product_modify_ed.objects.filter(id=obj_id)
        for t_product_modify_ed_obj in t_product_modify_ed_objs:
            Name2 = t_product_modify_ed_obj.Name2
            Keywords = t_product_modify_ed_obj.Keywords
            SQStaffNameing = t_product_modify_ed_obj.SQStaffNameing
            SQTimeing = t_product_modify_ed_obj.SQTimeing
            XGStaffName = t_product_modify_ed_obj.XGStaffName
            XGTime = t_product_modify_ed_obj.XGTime
            SHStaffName = t_product_modify_ed_obj.SHStaffName
            SHTime = t_product_modify_ed_obj.SHTime
            LQStaffName = t_product_modify_ed_obj.LQStaffName
            LQTime = t_product_modify_ed_obj.LQTime
            XGcontext = t_product_modify_ed_obj.XGcontext
           
            information_title = [u'申请人', u'申请时间', u'商品名称(中文)', u'英文标题', u'修改描述', u'修改', u'时间', u'审核', u'时间', u'领取',u'时间', ]
            information_dec = [SQStaffNameing, SQTimeing, Name2, Keywords, XGcontext, XGStaffName, XGTime, SHStaffName,SHTime, LQStaffName, LQTime]
            information = {'information_title': information_title, 'information_dec': information_dec}
        
    #except Exception:
    #    information = {'information_title':[],'information_dec':[]}
    return render(request, 'more_product_informations.html', information)

def wish_processed_order_syn(request):
    type = request.GET.get('type', '')
    shopname = request.GET.get('shopname', '')
    code = -1
    userName = request.user.username
    # errorShopName = 0
    if type == 'one':
        from skuapp.public.wish_processed_order_syn import wish_processed_order
        wish_processed_order_obj = wish_processed_order()
        from django_redis import get_redis_connection
        r = get_redis_connection(alias='product')
        errorShopName1 = r.get('{}_errorShopName_1'.format(userName))
        errorShopName2 = r.get('{}_errorShopName_2'.format(userName))
        errorShopName3 = r.get('{}_errorShopName_3'.format(userName))
        # if errorShopName1.find(shopname[5:]) != -1:
        #     errorShopName = 1
        # if errorShopName2.find(shopname[5:]) != -1:
        #     errorShopName = 2
        # if errorShopName3.find(shopname[5:]) != -1:
        #     errorShopName = 3
        try:
            code = wish_processed_order_obj.insertDB(shopname)
            if code == 0:
                if errorShopName1.find(shopname[5:] + ',') != -1:
                    errorShopName1 = errorShopName1.replace('{},'.format(shopname[5:]), '')
                    r.set('{}_errorShopName_1'.format(userName), errorShopName1)
                elif errorShopName2.find(shopname[5:] + ',') != -1:
                    errorShopName2 = errorShopName2.replace('{},'.format(shopname[5:]), '')
                    r.set('{}_errorShopName_2'.format(userName), errorShopName2)
                elif errorShopName3.find(shopname[5:] + ',') != -1:
                    errorShopName3 = errorShopName3.replace('{},'.format(shopname[5:]), '')
                    r.set('{}_errorShopName_3'.format(userName), errorShopName3)
            elif code == 1:
                # 没有token
                r.append('{}_errorShopName_1'.format(userName), shopname[5:] + ',')
            elif code == 2:
                # 错误的token
                r.append('{}_errorShopName_2'.format(userName), shopname[5:] + ',')
            elif code == 3:
                # 数据同步错误
                r.append('{}_errorShopName_3'.format(userName), shopname[5:] + ',')
        except Exception, e:
            logger.error(e)
        finally:
            wish_processed_order_obj.closeDB()
            return HttpResponseRedirect(
                '/Project/admin/skuapp/wish_processed_order/?shopname={}&code={}'.format(shopname, code))


def wish_processed_order_show_customer(request):
    id = request.GET.get('id', '')
    rt = ''
    if id:
        from skuapp.table.wish_processed_order import wish_processed_order
        objs = wish_processed_order.objects.filter(id=id)
        obj = objs[0]
        rt = "<table border='1'><tr><td>姓名</td><td>{}</td></tr>".format(obj.user_name)
        rt = "{}<tr><td>街道地址1</td><td>{}</td></tr>".format(rt, obj.street_address1)
        rt = "{}<tr><td>街道地址2</td><td>{}</td></tr>".format(rt,
                                                           obj.street_address2) if obj.street_address2 else '{}'.format(
            rt)
        rt = "{}<tr><td>城市</td><td>{}</td></tr>".format(rt, obj.city)
        rt = "{}<tr><td>状态</td><td>{}</td></tr>".format(rt, obj.state)
        rt = "{}<tr><td>邮编</td><td>{}</td></tr>".format(rt, obj.zipcode)
        rt = "{}<tr><td>国家</td><td>{}</td></tr>".format(rt, obj.country)
        rt = "{}<tr><td>电话</td><td>{}</td></tr>".format(rt, obj.phone_number)
    return render(request, 'ebay_SKU.html', {'rt': rt})


from threading import Thread


def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper


@async
def wish_foo(user, userName, r):
    try:
        from concurrent import futures
        # import redis  # 导入redis模块，通过python操作redis 也可以直接在redis主机的服务端操作缓存数据库
        # r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        objs_tmps = []
        try:
            if user.is_superuser:
                objs_tmp = t_store_configuration_file.objects.filter(ShopName__startswith='Wish-').values(
                    'ShopName_temp')
            else:
                objs_tmp = t_store_configuration_file.objects.filter(Operators=user.first_name).values('ShopName_temp')
        except Exception, e:
            logger.error(e)
        # objs_tmp = objs_tmp[:20]
        for obj_tmp in objs_tmp:
            objs_tmps.append(obj_tmp['ShopName_temp'])
        objs = objs_tmps
        r.hset('wish_processed_order_{}'.format(userName), 'shopname', len(objs))
        r.hset('wish_processed_order_{}'.format(userName), 'isend', 0)
        # progress = 0
        # error = 0
        # errorShopName = []
        objs.sort()
        workers = 5
        with futures.ThreadPoolExecutor(workers) as executor:
            futs = {executor.submit(sync_way, obj, r, userName) for obj in objs}
        # for obj in objs:
        #     try:
        #         code = wish_processed_order_obj.insertDB(obj)
        #     except Exception, e:
        #         logger.error(e)
        #         code = -1
        #     if code == 0:
        #         progress += 1
        #         r.hset('wish_processed_order_{}'.format(userName), 'progress', progress)
        #     else:
        #         error += 1
        #         r.hset('wish_processed_order_{}'.format(userName), 'error', error)
        #         errorShopName.append(obj)
        #         r.hset('wish_processed_order_{}'.format(userName), 'errorShopName', errorShopName)
        # r.hset('wish_processed_order_{}'.format(userName), 'isend', 1)
    except Exception, e:
        logger.error(e)
    finally:
        # wish_processed_order_obj.closeDB()
        r.hset('wish_processed_order_{}'.format(userName), 'isend', 1)


def sync_way(obj, r, userName):
    '''
    多线程获取wishApi和写入数据库
    :param objs:
    :return:
    '''
    from skuapp.public.wish_processed_order_syn import wish_processed_order
    wish_processed_order_obj = wish_processed_order()
    try:
        code = wish_processed_order_obj.insertDB(obj)
    except Exception, e:
        logger.error(e)
        code = -1
    if code == 0:
        r.hincrby('wish_processed_order_{}'.format(userName), 'progress', amount=1)
    elif code == 1:
        errorShopName = obj.replace('Wish-', '') + ','
        r.hincrby('wish_processed_order_{}'.format(userName), 'error', amount=1)
        # 没有token
        r.append('{}_errorShopName_1'.format(userName), errorShopName)
        wish_processed_order_obj.closeDB()
    elif code == 2:
        errorShopName = obj.replace('Wish-', '') + ','
        r.hincrby('wish_processed_order_{}'.format(userName), 'error', amount=1)
        # 错误的token
        r.append('{}_errorShopName_2'.format(userName), errorShopName)
        wish_processed_order_obj.closeDB()
    elif code == 3:
        errorShopName = obj.replace('Wish-', '') + ','
        r.hincrby('wish_processed_order_{}'.format(userName), 'error', amount=1)
        # 数据同步错误
        r.append('{}_errorShopName_3'.format(userName), errorShopName)
        wish_processed_order_obj.closeDB()


def wish_processed_order_ajax(request):
    if request.is_ajax() and request.method == "POST":
        userName = request.user.username
        sResult = {'sMsg': ''}
        msg = request.POST.get('msg')
        if msg == 'all':
            try:
                from django_redis import get_redis_connection
                r = get_redis_connection(alias='product')
                if r.hget('wish_processed_order_{}'.format(userName), 'isend') == '0':
                    pass
                else:
                    r.delete('wish_processed_order_{}'.format(userName))
                    r.delete('{}_errorShopName_1'.format(userName))
                    r.delete('{}_errorShopName_2'.format(userName))
                    r.delete('{}_errorShopName_3'.format(userName))
                    wish_foo(request.user, userName, r)
            except:
                sResult['sMsg'] = -1
            else:
                sResult['sMsg'] = 0
        else:
            sResult['sMsg'] = -1
        return HttpResponse(json.dumps(sResult), content_type="application/json")


def wish_processed_order_status(request):
    if request.is_ajax():
        userName = request.user.username
        from django_redis import get_redis_connection
        status = 0
        process = '0'
        shopname = '0'
        error = '0'
        # errorShopName = ''
        try:
            r = get_redis_connection(alias='product')
            result = r.hmget('wish_processed_order_{}'.format(userName), 'progress', 'shopname', 'isend', 'error')
            # errorShopName = r.get('{}_errorShopName'.format(userName))
            # if not errorShopName:
            #     errorShopName = ''
            process = result[0] if result[0] else 0
            shopname = result[1]
            status = int(str(float(result[0]) / float(result[1]) * 100).split('.')[0])
            sStatus = str(float(result[0]) / float(result[1]) * 100).split('.')[0] + '%'
            if result[2] == '1':
                sStatus = '100%'
                status = 100
            if result[3]:
                error = result[3]
            else:
                error = '0'
        except Exception, e:
            logger.error(e)
            sStatus = '0%'
        sResult = {}
        sResult['x'] = status if status else 0
        sResult['status'] = sStatus if sStatus else '0'
        sResult['process'] = process if process else '0'
        sResult['shopname'] = shopname if shopname else '0'
        sResult['error'] = error if error else '0'
        # sResult['errorShopName'] = errorShopName.replace('[', '').replace(']', '').replace('u', '').replace("'",
        #                                                                                                     "") if errorShopName else ''
        return HttpResponse(json.dumps(sResult), content_type="application/json")


def syn_amazon_cpc_ad(request):
    # site = request.GET.get('searchSite','')
    # return HttpResponse(site)
    import traceback
    try:
        import uuid
        from brick.amazon.product_refresh.get_auth_info import GetAuthInfo
        from brick.amazon.product_refresh.put_refresh_message_to_rabbitmq import MessageToRabbitMq
        from brick.table.t_config_amazon_progress_bar import t_config_amazon_progress_bar
        # from brick.table.t_config_amazon_ad_shop_status import t_config_amazon_ad_shop_status
        from django.db import connection
        if request.method == 'GET':
            ShopName = request.GET.get('ShopName')
            searchSite = request.GET.get('searchSite')
            UUID = uuid.uuid4()
            get_auth_info_ins = GetAuthInfo(connection)
            name = get_auth_info_ins.get_name_by_shop_and_site(ShopName, searchSite)  # 'AMZ-0052-Bohonan-US/PJ'
            auth_info = get_auth_info_ins.get_auth_info_by_shop_name(name)
            auth_info['update_type'] = 'refresh_ad_data'
            auth_info['table_name'] = 't_online_info_amazon'
            auth_info['uuid'] = str(UUID)
            message_to_mq_ins = MessageToRabbitMq(auth_info, connection)
            message_to_mq_ins.put_message(str(auth_info))
            t_config_amazon_progress_bar_obj = t_config_amazon_progress_bar(db_conn=connection)
            t_config_amazon_progress_bar_obj.insert_into_Progress(auth_info, 'submit')
            # t_config_amazon_shop_status_obj = t_config_amazon_shop_status(db_conn=connection)
            # t_config_amazon_shop_status_obj.update_shop_status(auth_info, ShopName, 'process')
            return HttpResponse(UUID)
    except Exception, ex:
        traceback.print_exc(file=open('/tmp/view.log', 'a'))

def syn_amazon_cpc_ad_progress(request):
    from brick.table.t_config_amazon_progress_bar import t_config_amazon_progress_bar
    if request.method == 'GET':
        #ShopName = request.GET.get('ShopName')
        #searchSite = request.GET.get('searchSite')
        # 查询 同步是否完成
        uuid = request.GET.get('uuid')
        t_config_amazon_progress_bar_obj = t_config_amazon_progress_bar(db_conn=connection)
        p_result = t_config_amazon_progress_bar_obj.getProgress(uuid)
        p_flag = ''
        if p_result['code'] == 0:
            p_flag = p_result['data'][0]
        # return HttpResponse('标志同步完成的值')
        return HttpResponse(p_flag)


def show_inventory_detail(request):
    from skuapp.table.t_online_amazon_fba_inventory import t_online_amazon_fba_inventory
    seller_sku = request.GET.get('seller_sku', '')
    shopname = request.GET.get('shopname', '')
    inventory_objs = t_online_amazon_fba_inventory.objects.filter(sku=seller_sku,ShopName=shopname)
    if inventory_objs:
        inventory_obj = inventory_objs[0]
    else:
        inventory_obj = None
    return render(request, 'show_inventory_detail.html', {'inventory_obj': inventory_obj})

def show_orders_detail(request):
    from skuapp.table.t_amazon_all_orders_data import t_amazon_all_orders_data
    # from pyapp.table.t_report_trades_daily import t_report_trades_daily
    import datetime
    seller_sku = request.GET.get('seller_sku', '')
    shop_name = request.GET.get('shopname', '')
    asin = request.GET.get('asin', '')
    # orders_objs = t_report_trades_daily.objects.filter(ShopSKU=seller_sku, ShopName=shop_name).order_by('OrderDay')
    orders_objs = t_amazon_all_orders_data.objects.filter(sku=seller_sku, shop_name=shop_name).order_by('purchase_date')
    order_dic = dict()
    if orders_objs:
        for orders_obj in orders_objs:
            order_day = orders_obj.purchase_date.strftime("%Y-%m-%d")
            if order_day in order_dic:
                order_dic[order_day] += 1
            else:
                order_dic[order_day] = 1

    sale_date = list()
    sale_num = list()

    if order_dic:

        for key, val in sorted(order_dic.items(), key=lambda x:x[0]):
            sale_date.append(key)
            sale_num.append(val)


    # if orders_objs:
    #     # orders_obj = orders_objs
    #     for orders_obj in orders_objs:
    #         sale_date.append(orders_obj.OrderDay.strftime("%Y-%m-%d"))
    #         sale_num.append(int(orders_obj.SalesVolume))
    # else:
    #     orders_obj = None

    return render(request, 'show_orders_detail.html', {'SKU': asin, 'salesdate': json.dumps(sale_date), 'salesnum': sale_num})
    # return render(request, 'show_orders_detail.html', {'orders_obj': orders_obj})

def show_ads_detail(request):
    return render(request, 'show_ads_detail.html')
    
    
    
def wish_processed_order_syn(request):
    type = request.GET.get('type', '')
    shopname = request.GET.get('shopname', '')
    code = -1
    userName = request.user.username
    # errorShopName = 0
    if type == 'one':
        from skuapp.public.wish_processed_order_syn import wish_processed_order
        wish_processed_order_obj = wish_processed_order()
        from django_redis import get_redis_connection
        r = get_redis_connection(alias='product')
        errorShopName1 = r.get('{}_errorShopName_1'.format(userName))
        errorShopName2 = r.get('{}_errorShopName_2'.format(userName))
        errorShopName3 = r.get('{}_errorShopName_3'.format(userName))
        try:
            code = wish_processed_order_obj.insertDB(shopname)
            if code == 0:
                if errorShopName1.find(shopname[5:] + ',') != -1:
                    errorShopName1 = errorShopName1.replace('{},'.format(shopname[5:]), '')
                    r.set('{}_errorShopName_1'.format(userName), errorShopName1)
                elif errorShopName2.find(shopname[5:] + ',') != -1:
                    errorShopName2 = errorShopName2.replace('{},'.format(shopname[5:]), '')
                    r.set('{}_errorShopName_2'.format(userName), errorShopName2)
                elif errorShopName3.find(shopname[5:] + ',') != -1:
                    errorShopName3 = errorShopName3.replace('{},'.format(shopname[5:]), '')
                    r.set('{}_errorShopName_3'.format(userName), errorShopName3)
            elif code == 1:
                # 没有token
                r.append('{}_errorShopName_1'.format(userName), shopname[5:] + ',')
            elif code == 2:
                # 错误的token
                r.append('{}_errorShopName_2'.format(userName), shopname[5:] + ',')
            elif code == 3:
                # 数据同步错误
                r.append('{}_errorShopName_3'.format(userName), shopname[5:] + ',')
        except Exception, e:
            logger.error(e)
        finally:
            # wish_processed_order_obj.closeDB()
            return HttpResponseRedirect(
                '/Project/admin/skuapp/wish_processed_order/?shopname={}&code={}'.format(shopname, code))


def wish_notification_syn(request):
    type = request.GET.get('type', '')
    shopname = request.GET.get('shopname', '')
    code = -1
    userName = request.user.username
    # errorShopName = 0
    if type == 'one':
        from skuapp.public.wish_notification_syn import wish_notification_syn
        wish_notification_syn_obj = wish_notification_syn()
        from django_redis import get_redis_connection
        r = get_redis_connection(alias='product')
        errorShopName1 = r.get('{}_errorShopName_noti1'.format(userName))
        errorShopName2 = r.get('{}_errorShopName_noti2'.format(userName))
        errorShopName3 = r.get('{}_errorShopName_noti3'.format(userName))
        try:
            code = wish_notification_syn_obj.insertDB(shopname)
            if code == 0:
                if errorShopName1.find(shopname[5:] + ',') != -1:
                    errorShopName1 = errorShopName1.replace('{},'.format(shopname[5:]), '')
                    r.set('{}_errorShopName_noti1'.format(userName), errorShopName1)
                elif errorShopName2.find(shopname[5:] + ',') != -1:
                    errorShopName2 = errorShopName2.replace('{},'.format(shopname[5:]), '')
                    r.set('{}_errorShopName_noti2'.format(userName), errorShopName2)
                elif errorShopName3.find(shopname[5:] + ',') != -1:
                    errorShopName3 = errorShopName3.replace('{},'.format(shopname[5:]), '')
                    r.set('{}_errorShopName_noti3'.format(userName), errorShopName3)
            elif code == 1:
                # 没有token
                r.append('{}_errorShopName_noti1'.format(userName), shopname[5:] + ',')
            elif code == 2:
                # 错误的token
                r.append('{}_errorShopName_noti2'.format(userName), shopname[5:] + ',')
            elif code == 3:
                # 数据同步错误
                r.append('{}_errorShopName_noti3'.format(userName), shopname[5:] + ',')
        except Exception, e:
            logger.error(e)
        finally:
            # wish_notification_syn_obj.closeDB()
            return HttpResponseRedirect(
                '/Project/admin/skuapp/wish_notification/?shopname={}&code={}'.format(shopname, code))

def wish_ticket_syn(request):
    type = request.GET.get('type', '')
    shopname = request.GET.get('shopname', '')
    code = -1
    userName = request.user.username
    # errorShopName = 0
    if type == 'one':
        from skuapp.public.wish_ticket_syn import wish_ticket_syn
        wish_ticket_syn_obj = wish_ticket_syn()
        from django_redis import get_redis_connection
        r = get_redis_connection(alias='product')
        errorShopName1 = r.get('{}_errorShopName_ti1'.format(userName))
        errorShopName2 = r.get('{}_errorShopName_ti2'.format(userName))
        errorShopName3 = r.get('{}_errorShopName_ti3'.format(userName))
        try:
            code = wish_ticket_syn_obj.insertDB(shopname)
            if code == 0:
                if errorShopName1.find(shopname[5:] + ',') != -1:
                    errorShopName1 = errorShopName1.replace('{},'.format(shopname[5:]), '')
                    r.set('{}_errorShopName_ti1'.format(userName), errorShopName1)
                elif errorShopName2.find(shopname[5:] + ',') != -1:
                    errorShopName2 = errorShopName2.replace('{},'.format(shopname[5:]), '')
                    r.set('{}_errorShopName_ti2'.format(userName), errorShopName2)
                elif errorShopName3.find(shopname[5:] + ',') != -1:
                    errorShopName3 = errorShopName3.replace('{},'.format(shopname[5:]), '')
                    r.set('{}_errorShopName_ti3'.format(userName), errorShopName3)
            elif code == 1:
                # 没有token
                r.append('{}_errorShopName_ti1'.format(userName), shopname[5:] + ',')
            elif code == 2:
                # 错误的token
                r.append('{}_errorShopName_ti2'.format(userName), shopname[5:] + ',')
            elif code == 3:
                # 数据同步错误
                r.append('{}_errorShopName_ti3'.format(userName), shopname[5:] + ',')
        except Exception, e:
            logger.error(e)
        finally:
            # wish_notification_syn_obj.closeDB()
            return HttpResponseRedirect(
                '/Project/admin/skuapp/wish_ticket/?shopname={}&code={}'.format(shopname, code))

def wish_in_syn(request):
    type = request.GET.get('type', '')
    shopname = request.GET.get('shopname', '')
    code = -1
    userName = request.user.username
    # errorShopName = 0
    if type == 'one':
        from skuapp.public.wish_infractions_syn import wish_infractions_syn
        wish_infractions_syn_obj = wish_infractions_syn()
        from django_redis import get_redis_connection
        r = get_redis_connection(alias='product')
        errorShopName1 = r.get('{}_errorShopName_in1'.format(userName))
        errorShopName2 = r.get('{}_errorShopName_in2'.format(userName))
        errorShopName3 = r.get('{}_errorShopName_in3'.format(userName))
        try:
            code = wish_infractions_syn_obj.insertDB(shopname)
            if code == 0:
                if errorShopName1.find(shopname[5:] + ',') != -1:
                    errorShopName1 = errorShopName1.replace('{},'.format(shopname[5:]), '')
                    r.set('{}_errorShopName_in1'.format(userName), errorShopName1)
                elif errorShopName2.find(shopname[5:] + ',') != -1:
                    errorShopName2 = errorShopName2.replace('{},'.format(shopname[5:]), '')
                    r.set('{}_errorShopName_in2'.format(userName), errorShopName2)
                elif errorShopName3.find(shopname[5:] + ',') != -1:
                    errorShopName3 = errorShopName3.replace('{},'.format(shopname[5:]), '')
                    r.set('{}_errorShopName_in3'.format(userName), errorShopName3)
            elif code == 1:
                # 没有token
                r.append('{}_errorShopName_in1'.format(userName), shopname[5:] + ',')
            elif code == 2:
                # 错误的token
                r.append('{}_errorShopName_in2'.format(userName), shopname[5:] + ',')
            elif code == 3:
                # 数据同步错误
                r.append('{}_errorShopName_in3'.format(userName), shopname[5:] + ',')
        except Exception, e:
            logger.error(e)
        finally:
            # wish_notification_syn_obj.closeDB()
            return HttpResponseRedirect(
                '/Project/admin/skuapp/wish_infractions/?shopname={}&code={}'.format(shopname, code))

def wish_processed_order_show_customer(request):
    id = request.GET.get('id', '')
    rt = ''
    if id:
        from skuapp.table.wish_processed_order import wish_processed_order
        objs = wish_processed_order.objects.filter(id=id)
        obj = objs[0]
        rt = "<table border='1'><tr><td>姓名</td><td>{}</td></tr>".format(obj.user_name)
        rt = "{}<tr><td>街道地址1</td><td>{}</td></tr>".format(rt, obj.street_address1)
        rt = "{}<tr><td>街道地址2</td><td>{}</td></tr>".format(rt,
                                                           obj.street_address2) if obj.street_address2 else '{}'.format(
            rt)
        rt = "{}<tr><td>城市</td><td>{}</td></tr>".format(rt, obj.city)
        rt = "{}<tr><td>状态</td><td>{}</td></tr>".format(rt, obj.state)
        rt = "{}<tr><td>邮编</td><td>{}</td></tr>".format(rt, obj.zipcode)
        rt = "{}<tr><td>国家</td><td>{}</td></tr>".format(rt, obj.country)
        rt = "{}<tr><td>电话</td><td>{}</td></tr>".format(rt, obj.phone_number)
    return render(request, 'ebay_SKU.html', {'rt': rt})


from threading import Thread


def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper


@async
def wish_foo(user, userName, r):
    try:
        from concurrent import futures
        objs_tmps = []
        try:
            if user.is_superuser or userName == 'jinyuling' or userName == 'meidandan':
                objs_tmp = t_store_configuration_file.objects.filter(ShopName__startswith='Wish-').values(
                    'ShopName_temp')
            else:
                objs_tmp = t_store_configuration_file.objects.filter(Operators=user.first_name).values('ShopName_temp')
        except Exception, e:
            logger.error(e)
        for obj_tmp in objs_tmp:
            objs_tmps.append(obj_tmp['ShopName_temp'])
        objs = objs_tmps
        r.hset('wish_processed_order_{}'.format(userName), 'shopname', len(objs))
        r.hset('wish_processed_order_{}'.format(userName), 'isend', 0)
        objs.sort()
        workers = 5
        with futures.ThreadPoolExecutor(workers) as executor:
            futs = {executor.submit(sync_way, obj, r, userName) for obj in objs}
    except Exception, e:
        logger.error(e)
    finally:
        r.hset('wish_processed_order_{}'.format(userName), 'isend', 1)

@async
def wish_foo_noti(user, userName, r):
    try:
        from concurrent import futures
        objs_tmps = []
        try:
            if user.is_superuser or userName == 'jinyuling' or userName == 'meidandan':
                objs_tmp = t_store_configuration_file.objects.filter(ShopName__startswith='Wish-').values(
                    'ShopName_temp')
            else:
                objs_tmp = t_store_configuration_file.objects.filter(Operators=user.first_name).values('ShopName_temp')
        except Exception, e:
            logger.error(e)
        for obj_tmp in objs_tmp:
            objs_tmps.append(obj_tmp['ShopName_temp'])
        objs = objs_tmps
        r.hset('wish_notification_{}'.format(userName), 'shopname', len(objs))
        r.hset('wish_notification_{}'.format(userName), 'isend', 0)
        objs.sort()
        workers = 5
        with futures.ThreadPoolExecutor(workers) as executor:
            futs = {executor.submit(sync_way_noti, obj, r, userName) for obj in objs}
    except Exception, e:
        logger.error(e)
    finally:
        r.hset('wish_notification_{}'.format(userName), 'isend', 1)

@async
def wish_foo_ti(user, userName, r):
    try:
        from concurrent import futures
        objs_tmps = []
        try:
            if user.is_superuser or userName == 'jinyuling' or userName == 'meidandan':
                objs_tmp = t_store_configuration_file.objects.filter(ShopName__startswith='Wish-').values(
                    'ShopName_temp')
            else:
                objs_tmp = t_store_configuration_file.objects.filter(Operators=user.first_name).values('ShopName_temp')
        except Exception, e:
            logger.error(e)
        for obj_tmp in objs_tmp:
            objs_tmps.append(obj_tmp['ShopName_temp'])
        objs = objs_tmps
        r.hset('wish_ticket_{}'.format(userName), 'shopname', len(objs))
        r.hset('wish_ticket_{}'.format(userName), 'isend', 0)
        objs.sort()
        # 多线程貌似在django中使用还不如不用
        workers = 5
        with futures.ThreadPoolExecutor(workers) as executor:
            futs = {executor.submit(sync_way_ti, obj, r, userName) for obj in objs}
        # for obj in objs:
        #     sync_way_ti(obj, r, userName)
    except Exception, e:
        logger.error(e)
    finally:
        r.hset('wish_ticket_{}'.format(userName), 'isend', 1)

@async
def wish_foo_in(user, userName, r):
    try:
        from concurrent import futures
        objs_tmps = []
        try:
            if user.is_superuser or userName == 'jinyuling' or userName == 'meidandan':
                objs_tmp = t_store_configuration_file.objects.filter(ShopName__startswith='Wish-').values(
                    'ShopName_temp')
            else:
                objs_tmp = t_store_configuration_file.objects.filter(Operators=user.first_name).values('ShopName_temp')
        except Exception, e:
            logger.error(e)
        for obj_tmp in objs_tmp:
            objs_tmps.append(obj_tmp['ShopName_temp'])
        objs = objs_tmps
        r.hset('wish_in_{}'.format(userName), 'shopname', len(objs))
        r.hset('wish_in_{}'.format(userName), 'isend', 0)
        objs.sort()
        # 多线程貌似在django中使用还不如不用
        workers = 5
        with futures.ThreadPoolExecutor(workers) as executor:
            futs = {executor.submit(sync_way_in, obj, r, userName) for obj in objs}
        # for obj in objs:
        #     sync_way_ti(obj, r, userName)
    except Exception, e:
        logger.error(e)
    finally:
        r.hset('wish_in_{}'.format(userName), 'isend', 1)



def sync_way(obj, r, userName):
    '''
    多线程获取wishApi和写入数据库
    :param objs:
    :return:
    '''
    from skuapp.public.wish_processed_order_syn import wish_processed_order
    wish_processed_order_obj = wish_processed_order()
    try:
        code = wish_processed_order_obj.insertDB(obj)
    except Exception, e:
        logger.error(e)
        code = -1
    if code == 0:
        r.hincrby('wish_processed_order_{}'.format(userName), 'progress', amount=1)
    elif code == 1:
        errorShopName = obj.replace('Wish-', '') + ','
        r.hincrby('wish_processed_order_{}'.format(userName), 'error', amount=1)
        # 没有token
        r.append('{}_errorShopName_1'.format(userName), errorShopName)
        # wish_processed_order_obj.closeDB()
    elif code == 2:
        errorShopName = obj.replace('Wish-', '') + ','
        r.hincrby('wish_processed_order_{}'.format(userName), 'error', amount=1)
        # 错误的token
        r.append('{}_errorShopName_2'.format(userName), errorShopName)
        # wish_processed_order_obj.closeDB()
    elif code == 3:
        errorShopName = obj.replace('Wish-', '') + ','
        r.hincrby('wish_processed_order_{}'.format(userName), 'error', amount=1)
        # 数据同步错误
        r.append('{}_errorShopName_3'.format(userName), errorShopName)
        # wish_processed_order_obj.closeDB()

def sync_way_noti(obj, r, userName):
    '''
    多线程获取wishApi和写入数据库
    :param objs:
    :return:
    '''
    from skuapp.public.wish_notification_syn import wish_notification_syn
    wish_notification_syn_obj = wish_notification_syn()
    try:
        code = wish_notification_syn_obj.insertDB(obj)
    except Exception, e:
        logger.error(e)
        code = -1
    if code == 0:
        r.hincrby('wish_notification_{}'.format(userName), 'progress', amount=1)
    elif code == 1:
        errorShopName = obj.replace('Wish-', '') + ','
        r.hincrby('wish_notification_{}'.format(userName), 'error', amount=1)
        # 没有token
        r.append('{}_errorShopName_noti1'.format(userName), errorShopName)
        # wish_notification_syn_obj.closeDB()
    elif code == 2:
        errorShopName = obj.replace('Wish-', '') + ','
        r.hincrby('wish_notification_{}'.format(userName), 'error', amount=1)
        # 错误的token
        r.append('{}_errorShopName_noti2'.format(userName), errorShopName)
        # wish_notification_syn_obj.closeDB()
    elif code == 3:
        errorShopName = obj.replace('Wish-', '') + ','
        r.hincrby('wish_notification_{}'.format(userName), 'error', amount=1)
        # 数据同步错误
        r.append('{}_errorShopName_noti3'.format(userName), errorShopName)
        # wish_notification_syn_obj.closeDB()

def sync_way_ti(obj, r, userName):
    '''
    多线程获取wishApi和写入数据库
    :param objs:
    :return:
    '''
    from skuapp.public.wish_ticket_syn import wish_ticket_syn
    wish_ticket_syn_obj = wish_ticket_syn()
    try:
        code = wish_ticket_syn_obj.insertDB(obj)
    except Exception, e:
        logger.error(e)
        code = -1
    if code == 0:
        r.hincrby('wish_ticket_{}'.format(userName), 'progress', amount=1)
    elif code == 1:
        errorShopName = obj.replace('Wish-', '') + ','
        r.hincrby('wish_ticket_{}'.format(userName), 'error', amount=1)
        # 没有token
        r.append('{}_errorShopName_ti1'.format(userName), errorShopName)
        # wish_notification_syn_obj.closeDB()
    elif code == 2:
        errorShopName = obj.replace('Wish-', '') + ','
        r.hincrby('wish_ticket_{}'.format(userName), 'error', amount=1)
        # 错误的token
        r.append('{}_errorShopName_ti2'.format(userName), errorShopName)
        # wish_notification_syn_obj.closeDB()
    elif code == 3:
        errorShopName = obj.replace('Wish-', '') + ','
        r.hincrby('wish_ticket_{}'.format(userName), 'error', amount=1)
        # 数据同步错误
        r.append('{}_errorShopName_ti3'.format(userName), errorShopName)
        # wish_notification_syn_obj.closeDB()

def sync_way_in(obj, r, userName):
    '''
    多线程获取wishApi和写入数据库
    :param objs:
    :return:
    '''
    from skuapp.public.wish_infractions_syn import wish_infractions_syn
    wish_infractions_syn_obj = wish_infractions_syn()
    try:
        code = wish_infractions_syn_obj.insertDB(obj)
    except Exception, e:
        logger.error(e)
        code = -1
    if code == 0:
        r.hincrby('wish_in_{}'.format(userName), 'progress', amount=1)
    elif code == 1:
        errorShopName = obj.replace('Wish-', '') + ','
        r.hincrby('wish_in_{}'.format(userName), 'error', amount=1)
        # 没有token
        r.append('{}_errorShopName_in1'.format(userName), errorShopName)
    elif code == 2:
        errorShopName = obj.replace('Wish-', '') + ','
        r.hincrby('wish_in_{}'.format(userName), 'error', amount=1)
        # 错误的token
        r.append('{}_errorShopName_in2'.format(userName), errorShopName)
    elif code == 3:
        errorShopName = obj.replace('Wish-', '') + ','
        r.hincrby('wish_in_{}'.format(userName), 'error', amount=1)
        # 数据同步错误
        r.append('{}_errorShopName_in3'.format(userName), errorShopName)

def wish_processed_order_ajax(request):
    if request.is_ajax() and request.method == "POST":
        userName = request.user.username
        sResult = {'sMsg': ''}
        msg = request.POST.get('msg')
        if msg == 'all':
            try:
                from django_redis import get_redis_connection
                r = get_redis_connection(alias='product')
                if r.hget('wish_processed_order_{}'.format(userName), 'isend') == '0':
                    pass
                else:
                    r.delete('wish_processed_order_{}'.format(userName))
                    r.delete('{}_errorShopName_1'.format(userName))
                    r.delete('{}_errorShopName_2'.format(userName))
                    r.delete('{}_errorShopName_3'.format(userName))
                    wish_foo(request.user, userName, r)
            except:
                sResult['sMsg'] = -1
            else:
                sResult['sMsg'] = 0
        else:
            sResult['sMsg'] = -1
        return HttpResponse(json.dumps(sResult), content_type="application/json")

def wish_notification_ajax(request):
    if request.is_ajax() and request.method == "POST":
        userName = request.user.username
        sResult = {'sMsg': ''}
        msg = request.POST.get('msg')
        if msg == 'all':
            try:
                from django_redis import get_redis_connection
                r = get_redis_connection(alias='product')
                if r.hget('wish_notification_{}'.format(userName), 'isend') == '0':
                    pass
                else:
                    r.delete('wish_notification_{}'.format(userName))
                    r.delete('{}_errorShopName_noti1'.format(userName))
                    r.delete('{}_errorShopName_noti2'.format(userName))
                    r.delete('{}_errorShopName_noti3'.format(userName))
                    wish_foo_noti(request.user, userName, r)
            except:
                sResult['sMsg'] = -1
            else:
                sResult['sMsg'] = 0
        else:
            sResult['sMsg'] = -1
        return HttpResponse(json.dumps(sResult), content_type="application/json")

def wish_ticket_ajax(request):
    if request.is_ajax() and request.method == "POST":
        userName = request.user.username
        sResult = {'sMsg': ''}
        msg = request.POST.get('msg')
        if msg == 'all':
            try:
                from django_redis import get_redis_connection
                r = get_redis_connection(alias='product')
                if r.hget('wish_ticket_{}'.format(userName), 'isend') == '0':
                    pass
                else:
                    r.delete('wish_ticket_{}'.format(userName))
                    r.delete('{}_errorShopName_ti1'.format(userName))
                    r.delete('{}_errorShopName_ti2'.format(userName))
                    r.delete('{}_errorShopName_ti3'.format(userName))
                    wish_foo_ti(request.user, userName, r)
            except:
                sResult['sMsg'] = -1
            else:
                sResult['sMsg'] = 0
        else:
            sResult['sMsg'] = -1
        return HttpResponse(json.dumps(sResult), content_type="application/json")

def wish_in_ajax(request):
    if request.is_ajax() and request.method == "POST":
        userName = request.user.username
        sResult = {'sMsg': ''}
        msg = request.POST.get('msg')
        if msg == 'all':
            try:
                from django_redis import get_redis_connection
                r = get_redis_connection(alias='product')
                if r.hget('wish_in_{}'.format(userName), 'isend') == '0':
                    pass
                else:
                    r.delete('wish_in_{}'.format(userName))
                    r.delete('{}_errorShopName_in1'.format(userName))
                    r.delete('{}_errorShopName_in2'.format(userName))
                    r.delete('{}_errorShopName_in3'.format(userName))
                    wish_foo_in(request.user, userName, r)
            except:
                sResult['sMsg'] = -1
            else:
                sResult['sMsg'] = 0
        else:
            sResult['sMsg'] = -1
        return HttpResponse(json.dumps(sResult), content_type="application/json")

def wish_processed_order_status(request):
    if request.is_ajax():
        userName = request.user.username
        from django_redis import get_redis_connection  # 导入redis模块，通过python操作redis 也可以直接在redis主机的服务端操作缓存数据库
        status = 0
        process = '0'
        shopname = '0'
        error = '0'
        isend = ''
        # errorShopName = ''
        try:
            r = get_redis_connection(alias='product')   
            result = r.hmget('wish_processed_order_{}'.format(userName), 'progress', 'shopname', 'isend', 'error')
            # errorShopName = r.get('{}_errorShopName'.format(userName))
            # if not errorShopName:
            #     errorShopName = ''
            process = result[0] if result[0] else 0
            shopname = result[1]
            if result[3]:
                error = result[3]
            status = int(str((float(result[0]) + float(error)) / float(result[1]) * 100).split('.')[0])
            sStatus = str((float(result[0]) + float(error)) / float(result[1]) * 100).split('.')[0] + '%'
            if result[2] == '1':
                isend = '1'
                sStatus = '100%'
                status = 100
        except Exception, e:
            # logger.error(e)
            sStatus = '0%'
            if isend == '1':
                sStatus = '100%'
                status = 100
        sResult = {}
        sResult['x'] = status if status else 0
        sResult['status'] = sStatus if sStatus else '0'
        sResult['process'] = process if process else '0'
        sResult['shopname'] = shopname if shopname else '0'
        sResult['error'] = error if error else '0'
        # sResult['errorShopName'] = errorShopName.replace('[', '').replace(']', '').replace('u', '').replace("'",
        #                                                                                                     "") if errorShopName else ''
        return HttpResponse(json.dumps(sResult), content_type="application/json")

def wish_notification_status(request):
    if request.is_ajax():
        userName = request.user.username
        from django_redis import get_redis_connection # 导入redis模块，通过python操作redis 也可以直接在redis主机的服务端操作缓存数据库
        status = 0
        process = '0'
        shopname = '0'
        error = '0'
        isend = ''
        try:
            r = get_redis_connection(alias='product')
            result = r.hmget('wish_notification_{}'.format(userName), 'progress', 'shopname', 'isend', 'error')
            process = result[0] if result[0] else 0
            shopname = result[1]
            if result[3]:
                error = result[3]
            status = int(str((float(result[0]) + float(error)) / float(result[1]) * 100).split('.')[0])
            sStatus = str((float(result[0]) + float(error)) / float(result[1]) * 100).split('.')[0] + '%'
            if result[2] == '1':
                isend = '1'
                sStatus = '100%'
                status = 100
        except Exception, e:
            # logger.error(e)
            sStatus = '0%'
            if isend == '1':
                sStatus = '100%'
                status = 100
        sResult = {}
        sResult['x'] = status if status else 0
        sResult['status'] = sStatus if sStatus else '0'
        sResult['process'] = process if process else '0'
        sResult['shopname'] = shopname if shopname else '0'
        sResult['error'] = error if error else '0'
        return HttpResponse(json.dumps(sResult), content_type="application/json")

def wish_ticket_status(request):
    if request.is_ajax():
        userName = request.user.username
        from django_redis import get_redis_connection
        status = 0
        process = '0'
        shopname = '0'
        error = '0'
        isend = ''
        try:
            r = get_redis_connection(alias='product')
            result = r.hmget('wish_ticket_{}'.format(userName), 'progress', 'shopname', 'isend', 'error')
            process = result[0] if result[0] else 0
            shopname = result[1]
            if result[3]:
                error = result[3]
            status = int(str((float(result[0]) + float(error)) / float(result[1]) * 100).split('.')[0])
            sStatus = str((float(result[0]) + float(error)) / float(result[1]) * 100).split('.')[0] + '%'
            if result[2] == '1':
                isend = '1'
                sStatus = '100%'
                status = 100
        except Exception, e:
            # logger.error(e)
            sStatus = '0%'
            if isend == '1':
                sStatus = '100%'
                status = 100
        sResult = {}
        sResult['x'] = status if status else 0
        sResult['status'] = sStatus if sStatus else '0'
        sResult['process'] = process if process else '0'
        sResult['shopname'] = shopname if shopname else '0'
        sResult['error'] = error if error else '0'
        return HttpResponse(json.dumps(sResult), content_type="application/json")

def wish_in_status(request):
    if request.is_ajax():
        userName = request.user.username
        from django_redis import get_redis_connection
        status = 0
        process = '0'
        shopname = '0'
        error = '0'
        isend = ''
        try:
            r = get_redis_connection(alias='product')
            result = r.hmget('wish_in_{}'.format(userName), 'progress', 'shopname', 'isend', 'error')
            process = result[0] if result[0] else 0
            shopname = result[1]
            if result[3]:
                error = result[3]

            status = int(str((float(result[0]) + float(error)) / float(result[1]) * 100).split('.')[0])
            sStatus = str((float(result[0]) + float(error)) / float(result[1]) * 100).split('.')[0] + '%'
            if result[2] == '1':
                isend = '1'
                sStatus = '100%'
                status = 100

        except Exception, e:
            # logger.error(e)
            sStatus = '0%'
            if isend == '1':
                sStatus = '100%'
                status = 100
        sResult = {}
        sResult['x'] = status if status else 0
        sResult['status'] = sStatus if sStatus else '0'
        sResult['process'] = process if process else '0'
        sResult['shopname'] = shopname if shopname else '0'
        sResult['error'] = error if error else '0'
        return HttpResponse(json.dumps(sResult), content_type="application/json")
        
#7天回评详情
def t_product_suring_ratingdetails(obj):
    import simplejson as json
    import re
    num = 0
    match_condition_day = 'about a day ago,about 2 days ago,about 3 days ago,about 4 days ago,about 5 days ago,about 6 days ago,about 7 days ago'
    match_condition_hour = 'hour'
    match_condition_minute = 'minute'
    try:
        params = {}
        params = json.loads(obj)
        if len(params['data']) == 0:
            return num
        for sRow in list(params['data']):
            if len(sRow) == 0:
                continue
            if re.search(match_condition_minute,str(sRow['day'])) is not None:
                num = num + 1
                continue
            if re.search(match_condition_hour,str(sRow['day'])) is not None:
                num = num + 1
                continue
            if re.search(str(sRow['day']), match_condition_day) is not None:
                num = num + 1
                continue
    except:
        num = -1
    return num

#通过cid获取类目名称
def get_cid_name(cursor,cids):
    try:
        sql = "select categoryname from t_product_category_dict where category = '%s'" %cids
        cursor.execute(sql)
        objs = cursor.fetchone()
        if objs:
            result = objs[0]
        else:
            result = 'has no categoryname'
    except:
        result = 'Get categoryname from t_product_category_dict fail'
    return result

# wish 调研
def t_product_suringPlugin(request):
    from skuapp.table.t_product_suvering import t_product_suvering
    import requests
    import json
    from django.db import connection
    from datetime import datetime as tttime
    cursor = connection.cursor()
    if request.method == 'GET':
        try:
            pid = request.GET.get('_pid_').strip()
            url = 'https://1039393360449722.cn-shanghai.fc.aliyuncs.com/2016-08-15/proxy/Stock/Simplefunction2/?pid=%s' % pid
            re = requests.get(url)
            obj = json.loads(re.text)
            if obj['errcode'] == 0 or obj['errcode'] == -2:
                try:
                    picpath = 'https://contestimg.wish.com/api/webimage/' + pid + '-small.jpg'
                    fxprice = obj['o_price'] + "+" + obj['price']
                    obj['title'] = obj['title'].replace('\'', '\'\'')
                    obj['cids'] = obj['cids'].replace('\'', '')
                    cids = obj['cids'].split(',')
                    user_name = request.user.username
                    categorynames = ''
                    for cid in cids:
                        categoryname = get_cid_name(cursor, cid)
                        categorynames = categorynames + ' CATEGORY:' + categoryname
                    if len(categorynames) == 0:
                        categorynames = 'can not get category'
                    obj['rating_detail'] = obj['rating_detail'].replace('\'', '\'\'')
                    rating_num = t_product_suring_ratingdetails(obj['rating_detail'])
                    if rating_num == -1:
                        messages.info(request, '7天回评数据异常,计算数量失败,:%s' % rating_num)
                    else:
                        messages.info(request, '7天回评数:%s' % rating_num)
                    params = {}
                    params = json.loads(obj['rating_detail'])
                    if params['avg_star'] == '':
                        params['avg_star'] = 0
                    if params['rating_count'] == '':
                        params['rating_count'] = 0
                    if params['rating_count'] == 0:
                        params['avg_star'] = 0
                    boughtthis = params['num_bought'].replace('+ bought this', '').replace(' bought this', '')
                    if boughtthis == '':
                        boughtthis = 0
                    if obj['errcode'] == 0:
                        getinfostatus = 'SUCCESS'
                        status = 1
                    else:
                        getinfostatus = 'Get data from haiying api is None or out of stock'
                        status = 0
                    sql = "insert into t_product_suvering (suvering_time,sourcepic_path,product_id,title,category,price,sale_time,sale_number,comment_number,point," \
                          "little_flames,rating_details,PB,saler,getinfo_time,getinfo_status,sevenratingnum,status)  " \
                          "values ('%s','%s','%s','%s','%s','%s','%s',%s,%s,%s,%s,'%s',%s,'%s','%s','%s',%s,%s) on  DUPLICATE key update sourcepic_path='%s',category='%s',price='%s',sale_number=%s,comment_number=%s,point=%s,little_flames=%s,rating_details='%s',getinfo_time='%s',getinfo_status='%s',sevenratingnum=%s,status=%s ;" \
                          % (tttime.now(), picpath, pid, obj['title'], str(categorynames), fxprice, obj['gen_time'],
                             boughtthis, params['rating_count'], params['avg_star'], obj['aver'], obj['rating_detail'],
                             obj['is_pb'],user_name, tttime.now(), getinfostatus, rating_num, status, picpath, str(categorynames),
                             fxprice, boughtthis,
                             params['rating_count'], params['avg_star'], obj['aver'], obj['rating_detail'],
                             tttime.now(), getinfostatus, rating_num, status)
                    sql_1 = "update t_product_suvering set rating_details = REPLACE(REPLACE(rating_details, CHAR(10), ''), CHAR(13), '') where product_id = '%s'" % pid
                    cursor.execute(sql)
                    cursor.execute(sql_1)
                    cursor.execute('commit;')
                except Exception as e:
                    getinfostatus = '异常数据,请联系IT人员查看'
            else:
                try:
                    if obj['errcode'] == -1:
                        getinfostatus = 'Get data from wish api fail'
                    if obj['errcode'] == -3:
                        getinfostatus = 'Get data from haiying api fail'
                    if obj['errcode'] == -4:
                        getinfostatus = 'wish api requests fail'
                    sql = "insert into t_product_suvering (suvering_time,product_id,getinfo_time,getinfo_status,status) values ('%s','%s','%s','%s',%s) on  DUPLICATE key update product_id ='%s',getinfo_time='%s',getinfo_status='%s',status=%s" % (
                    tttime.now(), pid, tttime.now(), getinfostatus, 0, pid, tttime.now(), getinfostatus, 0)
                    cursor.execute(sql)
                    cursor.execute('commit;')
                except:
                    getinfostatus = '异常数据,请联系IT人员查看'
        except Exception as e:
            getinfostatus = 'wish商品pid: %s,云函数请求失败,请联系IT人员' % pid
    cursor.close()
    messages.info(request, '%s' % getinfostatus)
    return HttpResponseRedirect('/Project/admin/skuapp/t_product_suvering/')

# wish 竞品调研评论展示
def show_wish_variant_jp(request):
    import simplejson as json
    idvalue = request.GET.get('product_id', '')

    rt = '<table  style="text-align:center;" border="1" cellpadding="3" cellspacing="1" bgcolor="#c1c1c1"><tr bgcolor="#7FFFAA"><th style="text-align:center">星级数</th><th>评论内容</th><th style="text-align:center">评论时间</th></tr>'
    from skuapp.table.t_product_suvering import t_product_suvering
    t_product_suvering_objs = t_product_suvering.objects.filter(product_id=idvalue).values_list('rating_details',flat=True)
    try:
        for objRow in t_product_suvering_objs:
            if objRow is None or str(objRow) == '':
                #messages.info(request, 'wish商品pid: %s,评论详情为空' % idvalue)
                rt = '%s <tr bgcolor="#FFFFFF"><td>%s</td><td>%s</td><td>%s</td></tr> ' % (rt, '', '评论详情为空', '')
                continue
            params = {}
            params = json.loads(objRow)
            if len(params['data']) == 0:
                rt = '%s <tr bgcolor="#FFFFFF"><td>%s</td><td>%s</td><td>%s</td></tr> ' % (rt, '', '评论详情为空', '')
            else:
                for sRow in list(params['data']):
                    if len(sRow) == 0:
                        rt = '%s <tr bgcolor="#FFFFFF"><td>%s</td><td>%s</td><td>%s</td></tr> ' % (rt, '', '评论详情为空', '')
                    else:
                        rt = '%s <tr bgcolor="#FFFFFF"><td>%s</td><td>%s</td><td>%s</td></tr> ' % (rt, sRow['star'], sRow['com'], sRow['day'])
        rt = "%s</table>" % rt
    except:
        rt = '%s <tr bgcolor="#FFFFFF"><td>%s</td><td>%s</td><td>%s</td></tr> ' % (rt, '', '评论数据异常,请联系IT人员', '')

    return render(request, 'rating.html', {'rt': rt})

def show_wish_refresh(request):
    idvalue = request.GET.get('product_id', '')
    from skuapp.table.t_product_suvering import t_product_suvering
    import requests
    import json
    from django.db import connection
    from datetime import datetime as tttime
    cursor = connection.cursor()
    try:
        pid = idvalue
        url = 'https://1039393360449722.cn-shanghai.fc.aliyuncs.com/2016-08-15/proxy/Stock/Simplefunction2/?pid=%s' % pid
        re = requests.get(url)
        obj = json.loads(re.text)
        if obj['errcode'] == 0 or obj['errcode'] == -2:
            try:
                picpath = 'https://contestimg.wish.com/api/webimage/' + pid + '-small.jpg'
                fxprice = obj['o_price'] + "+" + obj['price']
                obj['title'] = obj['title'].replace('\'', '\'\'')
                obj['cids'] = obj['cids'].replace('\'', '')
                cids = obj['cids'].split(',')
                categorynames = ''
                for cid in cids:
                    categoryname = get_cid_name(cursor, cid)
                    categorynames = categorynames + ' CATEGORY:' + categoryname
                if len(categorynames) == 0:
                    categorynames = 'can not get category'
                obj['rating_detail'] = obj['rating_detail'].replace('\'', '\'\'')
                rating_num = t_product_suring_ratingdetails(obj['rating_detail'])
                if rating_num == -1:
                    messages.info(request, '7天回评数据异常,计算数量失败,:%s' % rating_num)
                else:
                    messages.info(request, '7天回评数:%s' % rating_num)
                params = {}
                params = json.loads(obj['rating_detail'])
                if params['avg_star'] == '':
                    params['avg_star'] = 0
                if params['rating_count'] == '':
                    params['rating_count'] = 0
                if params['rating_count'] == 0:
                    params['avg_star'] = 0
                boughtthis = params['num_bought'].replace('+ bought this', '').replace(' bought this', '')
                if boughtthis == '':
                    boughtthis = 0
                if obj['errcode'] == 0:
                    getinfostatus = 'Refresh SUCCESS'
                    status = 1
                else:
                    getinfostatus = 'Get data from haiying api is None or out of stock'
                    status = 0
                sql = "insert into t_product_suvering (suvering_time,sourcepic_path,product_id,title,category,price,sale_time,sale_number,comment_number,point," \
                      "little_flames,rating_details,PB,getinfo_time,getinfo_status,sevenratingnum,status)  " \
                      "values ('%s','%s','%s','%s','%s','%s','%s',%s,%s,%s,%s,'%s',%s,'%s','%s',%s,%s) on  DUPLICATE key update sourcepic_path='%s',category='%s',price='%s',sale_number=%s,comment_number=%s,point=%s,little_flames=%s,rating_details='%s',getinfo_time='%s',getinfo_status='%s',sevenratingnum=%s,status=%s ;" \
                      % (tttime.now(), picpath, pid, obj['title'], str(categorynames), fxprice, obj['gen_time'],
                         boughtthis, params['rating_count'], params['avg_star'], obj['aver'], obj['rating_detail'],
                         obj['is_pb'], tttime.now(), getinfostatus, rating_num, status, picpath, str(categorynames),
                         fxprice, boughtthis,
                         params['rating_count'], params['avg_star'], obj['aver'], obj['rating_detail'],
                         tttime.now(), getinfostatus, rating_num, status)
                sql_1 = "update t_product_suvering set rating_details = REPLACE(REPLACE(rating_details, CHAR(10), ''), CHAR(13), '') where product_id = '%s'" % pid
                cursor.execute(sql)
                cursor.execute(sql_1)
                cursor.execute('commit;')
            except Exception as e:
                getinfostatus = '异常数据,请联系IT人员查看'
        else:
            try:
                if obj['errcode'] == -1:
                    getinfostatus = 'Get data from wish api fail'
                if obj['errcode'] == -3:
                    getinfostatus = 'Get data from haiying api fail'
                if obj['errcode'] == -4:
                    getinfostatus = 'wish api requests fail'
                sql = "insert into t_product_suvering (suvering_time,product_id,getinfo_time,getinfo_status,status) values ('%s','%s','%s','%s',%s) on  DUPLICATE key update product_id ='%s',getinfo_time='%s',getinfo_status='%s',status=%s" % (
                    tttime.now(), pid, tttime.now(), getinfostatus, 0, pid, tttime.now(), getinfostatus, 0)
                cursor.execute(sql)
                cursor.execute('commit;')
            except Exception as e:
                getinfostatus = '异常数据,请联系IT人员查看'
    except Exception as e:
        getinfostatus = 'wish商品pid: %s,云函数请求失败,请联系IT人员' % pid
    cursor.close()
    return render(request, 'result.html', {'rt': getinfostatus})


def show_data_by_user(request,cur_model):
    from django.db import connection
    cursor = connection.cursor()
    try:
        user_name = request.user.username
        #超级管理员直接查看所有数据
        sql = "select 1 from auth_user where username = '%s' and is_superuser = 1" %user_name
        cursor.execute(sql)
        results = cursor.fetchall()
        for result in results:
            if result:
                cursor.close()
                return 1
        #非超级管理员,查看配置的角色权限
        flag = 0
        sql = "select role from  auth_view_permissions where model= '%s' and user='%s' and role = 1" % (cur_model,user_name)
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) > 0:
            flag = 1
    except Exception as e:
        flag = 0
    cursor.close()
    return flag

@csrf_exempt
def show_edit_jp_info_tile(request):
    from skuapp.table.t_product_suvering import t_product_suvering
    try:
        idvalue = request.GET.get('id')
        newtitle = request.GET.get('title')
        newtitle = newtitle.replace('\'', '\'\'')
        t_product_suvering.objects.filter(id=idvalue).update(title=newtitle)
    except Exception as e:
        messages.info(request, 'title 编辑失败:%s' % newtitle)
    return HttpResponse(1)

@csrf_exempt
def show_edit_jp_info_pb(request):
    from skuapp.table.t_product_suvering import t_product_suvering
    try:
        idvalue = request.GET.get('id')
        newpb = request.GET.get('pb')
        if newpb == '1' or newpb == '0' or newpb == '-1':
            t_product_suvering.objects.filter(id=idvalue).update(PB=newpb)
        else:
            messages.info(request, '广告内容输入错误只能输入1或0或-1,实际输入:%s' % newpb)
    except Exception as e:
        messages.info(request, 'PB 编辑失败:%s' % newpb)
    return HttpResponse(1)

def t_cloth_factory_remark(request):
    from skuapp.table.t_cloth_factory_dispatch_needpurchase import t_cloth_factory_dispatch_needpurchase
    remarkValue = request.GET.get('remarkInfo', '')
    inputInfo = request.GET.get('inputInfo', '')
    remark = remarkValue + ',' + inputInfo
    idValue = request.GET.get('id', '')
    try:
        t_cloth_factory_dispatch_needpurchase.objects.filter(id=idValue).update(remarkGenPurchase=remark)
        return JsonResponse({'result': 'OK'})
    except:
        return JsonResponse({'result': 'NG'})
        
def generate_fba_price_pdf(request):
    from app_djcelery.tasks import generate_amazon_india_fba_pdf
    timestamp = int(time.time())
    fba_sku = request.GET.get('fba_sku', '')
    shopname = request.GET.get('_p_ShopName__exact', '')
    if shopname:
        shopname = shopname.replace('%2F', '/')
    #调用task任务
    upload_path = 'Amazon_IN/FBA_price/' + request.user.username
    generate_amazon_india_fba_pdf(fba_sku, shopname, upload_path, str(timestamp))
    url_path = request.get_full_path()
    if '' in url_path:
        url_path = url_path.replace('generate_fba_price_pdf/', '')
    url_start = url_path.split('?')[0]
    params = url_path.split('?')[-1].split('&')
    for param in params:
        if 'fba_sku=' in param:
            pass
        else:
            url_start += '&' + param
    url_path = url_start.replace('/&', '/?')
    messages.info(request, u'FBA面单压缩包FBA_Price_%s.zip正在生成中...请稍后前往下载中心下载'%str(timestamp))
    return HttpResponseRedirect('%s' % url_path)    
    
@csrf_exempt
def BeyondNum(request):
    from skuapp.table.t_cloth_factory_dispatch_needpurchase import t_cloth_factory_dispatch_needpurchase
    from brick.pydata.py_syn.py_conn import py_conn
    result = {'errorcode': -1, 'errortext': '','count':''}
    productSKU = request.GET.get('SKU', '')
    OrderNum = request.GET.get('OrderNum', '')
    #BeyondNum = request.GET.get('BeyondNum', '')
    OtherInfo = request.GET.get('OtherInfo', '')
    remark = OrderNum + '#@#' + '' + '#@#' + OtherInfo
    idValue = request.GET.get('id', '')
    try:
        if OrderNum != "":
            OrderNum = "'" + OrderNum.replace(',','\',\'').replace(' ','') + "'"
            pyconn = py_conn()
            sqlserverInfo = pyconn.py_conn_database()
            if sqlserverInfo['errorcode'] == 0:
                str_py_selectSql = "select cast(sum(Amount) as decimal(18,0)),cast(sum(InAmount) as decimal(18,0)),GoodsID from CG_StockOrderD(nolock) d where d.StockOrderNID in " \
                                   "(select  nid from CG_StockOrderM(nolock) m where m.BillNumber in(%s) ) " \
                                   "and d.GoodsID = (select top 1 nid from B_Goods where SKU='%s') group by GoodsID; ; " % (OrderNum, productSKU)
                sqlserverInfo['py_cursor'].execute(str_py_selectSql)
                tupple_py_unpurchase = sqlserverInfo['py_cursor'].fetchone()
                InAmount = '0'
                if tupple_py_unpurchase:
                    InAmount = tupple_py_unpurchase[0]
                t_cloth_factory_dispatch_needpurchase.objects.filter(id=idValue).update(remarkDisPatch=remark,completeNumbers=InAmount)
                result['errorcode'] = 0
                result['errortext'] = "OK"
                result['count'] = InAmount
            else:
                result['errorcode'] = -1
                result['errortext'] = u"链接普元数据库失败"
            pyconn.py_close_conn_database()
            return JsonResponse(result)
        else:
            t_cloth_factory_dispatch_needpurchase.objects.filter(id=idValue).update(remarkDisPatch='',
                                                                                    completeNumbers='0')
            result['errorcode'] = 0
            result['errortext'] = "OK"
            result['count'] = 0
            return JsonResponse(result)
    except:
        return JsonResponse(result)
        
        
def remove_wish_pic_update_flag(request):
    """
    去掉主图维护里的图片存在更新的标志和图片右上方new的标志
    """
    from skuapp.table.t_product_image_modify import t_product_image_modify
    from skuapp.table.t_product_mainsku_pic import t_product_mainsku_pic
    main_sku = request.GET.get('main_sku', '')
    t_product_mainsku_pic.objects.filter(MainSKU=main_sku).update(NewFlag=1)
    t_product_image_modify.objects.filter(MainSKU=main_sku).update(UpdateFlag=0)
    myResult = {'resultCode': 0}
    return JsonResponse(myResult)


def t_supply_chain_production_subsku(request):

    mainsku=request.GET.get('mainsku')
    objid=request.GET.get('objid')
    info = ''
    conn=classmainsku(connection)
    if mainsku:
        # _subskus = b_goods.objects.filter(SKU__startswith=mainsku).values_list('SKU')
        # subskus = [x[0] for x in _subskus]
        subskus=conn.get_sku_by_mainsku(mainsku)
        for subsku in subskus:
            info=info+str(int(objid))+","+'http://122.226.216.10:89/ShopElf/images/{}.jpg'.format(subsku)+","+subsku+' (split) '

    return JsonResponse({'info':info})


def t_supply_chain_production_mainpic(request):
    from skuapp.table.t_supply_chain_production_basic_permission import t_supply_chain_production_basic_permission
    _permission = t_supply_chain_production_basic_permission.objects.filter(username=request.user.username).values_list(
        'username')
    permission = [x[0] for x in _permission]

    read = 'readonly'
    if request.user.is_superuser or permission :
        errmsg=''
        from skuapp.table.t_supply_chain_production_basic import t_supply_chain_production_basic
        objid=request.GET.get('objid')
        subsku=request.GET.get('subsku')
        MainPic='http://122.226.216.10:89/ShopElf/images/{}.jpg'.format(subsku)
        if objid and MainPic:
            row=t_supply_chain_production_basic.objects.filter(id=objid).update(Main_Pic=MainPic)
            if row==1:
                errmsg=''
            else:
                errmsg='修改失败，请联系IT'
        elif not objid:
            errmsg='该数据不存在！'
        elif not MainPic:
            errmsg='主图URL不存在！'
    else:
        errmsg='抱歉，您的权限不足！'
    return JsonResponse({'errmsg':errmsg})
    
    
    
def delete_wish_joom_extraimage(request):
    """删除WISH、JOOM铺货副图"""
    from skuapp.table.t_templet_wish_collection_box import t_templet_wish_collection_box
    from skuapp.table.t_templet_public_wish_review import t_templet_public_wish_review
    from skuapp.table.t_templet_public_wish import t_templet_public_wish
    from skuapp.table.t_templet_wish_wait_upload import t_templet_wish_wait_upload
    from skuapp.table.t_templet_wish_upload_review import t_templet_wish_upload_review
    from skuapp.table.t_templet_joom_collection_box import t_templet_joom_collection_box
    from skuapp.table.t_templet_public_joom import t_templet_public_joom
    from skuapp.table.t_templet_joom_wait_upload import t_templet_joom_wait_upload
    from base64 import urlsafe_b64encode
    platefrom_page_table_dict = {
        'wish': {
            'box': t_templet_wish_collection_box,
            'public_review': t_templet_public_wish_review,
            'public': t_templet_public_wish,
            'wait_upload': t_templet_wish_wait_upload,
            'upload_review': t_templet_wish_upload_review
        },
        'joom': {
            'box': t_templet_joom_collection_box,
            'public': t_templet_public_joom,
            'wait_upload': t_templet_joom_wait_upload
        }
    }

    plateform = request.GET.get('plateform', '')
    page = request.GET.get('page', '')
    id = int(request.GET.get('now_id', ''))
    p_encode = request.GET.get('p_encode', '')
    table_obj = platefrom_page_table_dict[plateform][page].objects.filter(id=id)
    if table_obj.exists():
        extra_images = table_obj[0].ExtraImages
        extra_image_list = extra_images.split('|') if extra_images else []
        for i in range(len(extra_image_list)):
            extra_image = extra_image_list[i]
            if urlsafe_b64encode(extra_image) == p_encode:
                del extra_image_list[i]
                break
        extra_images = '|'.join(extra_image_list)
        table_obj.update(ExtraImages=extra_images)
    myResult = {'resultCode': 0}
    return JsonResponse(myResult)
    
def deal_with_fba_sku_to_list(mrp_sku):
    skus = mrp_sku.split(',')
    all_sku_list = []
    for sku in skus:
        print sku
        each_sku_dict = {}
        sku_dict = {}
        if ' ' in sku:
            all_skus = sku.split(' ')
            for each_sku in all_skus:
                count = 1
                final_sku = each_sku
                if '*' in each_sku:
                    final_sku = each_sku.split('*')[0]
                    count = each_sku.split('*')[1]
                sku_dict[final_sku] = count
        else:
            count = 1
            final_sku = sku
            if '*' in sku:
                final_sku = sku.split('*')[0]
                count = sku.split('*')[1]
            sku_dict[final_sku] = count
        each_sku_dict[sku] = sku_dict
        all_sku_list.append(each_sku_dict)
    return all_sku_list

def get_shop_price_config(shopname):
    from brick.table.amzon_india_price_config import amzon_india_price_config
    try:
        params = {}
        amzon_india_price_config_obj = amzon_india_price_config(connection)
        price_config = amzon_india_price_config_obj.getAmazonPriceCofig(ShopName=shopname)
        if price_config['code'] <> 0:
            raise Exception(u'无店铺价格配置')
        params['EXCHANGE_RATE'] = float(price_config['data']['EXCHANGE_RATE'])
        params['PROFIT_RATE'] = float(price_config['data']['PROFIT_RATE'])
        params['TRACK_PRICE_ELEC'] = float(price_config['data']['TRACK_PRICE_ELEC'])
        params['TRACK_PRICE_UNELEC'] = float(price_config['data']['TRACK_PRICE_UNELEC'])
        params['TRACK_DEAL_WEIGHT'] = decimal.Decimal("%.2f" % float(price_config['data']['TRACK_DEAL_WEIGHT']))
        params['TRACK_DEAL_PRICE'] = float(price_config['data']['TRACK_DEAL_PRICE'])
        params['MARKETED'] = price_config['data']['MARKETED']
        params['MANUFACTURED'] = price_config['data']['MANUFACTURED']
        params['MRP_START'] = price_config['data']['MRP_START']
        params['MRP_END'] = price_config['data']['MRP_END']
        params['CUSTOMER_PHONE'] = price_config['data']['CUSTOMER_PHONE']
        params['END_MESSAGE'] = price_config['data']['END_MESSAGE']
        params['TABLE_WIDTH'] = price_config['data']['TABLE_WIDTH']
    except Exception as e:
        params = u'%s'%e
    return params

def get_mrp_price_xls_result(all_sku_list, params):
    from brick.classredis.classsku import classsku
    from brick.amazon.generate_price_order import *
    generate_price_order_obj = generate_price_order()
    final_price_list = []
    all_sku_info_list = []
    for all_skus in all_sku_list:
        sku_dict = {}
        for sku,sku_values in all_skus.items():
            result_sku_info = generate_price_order_obj.get_price_and_weight_color_by_sku(sku_values, params)
            for sku1, sku_values1 in sku_values.items():
                each_packinfo = classsku(db_cnxn=connection).get_packinfo_by_sku(sku1)
                each_goodsName = classsku(db_cnxn=connection).get_goodsName_by_sku(sku1)
                each_price = classsku(db_cnxn=connection).get_price_by_sku(sku1)
                cost_price = each_price
                if each_price:
                    cost_price = decimal.Decimal("%.2f" % float(each_price)) * int(sku_values1)
                sku1_dict = {'packinfo': each_packinfo, 'goodsName': each_goodsName, 'costPrice': cost_price}
                sku_dict[sku1] = sku1_dict
            sku_dict['sku'] = sku
            sku_dict['mrp_price'] = result_sku_info['price']
            final_price_list.append(result_sku_info['price'])
        all_sku_info_list.append(sku_dict)
    return final_price_list, all_sku_info_list

def generate_mrp_price_xls(all_sku_info_list, filename, user_name):
    import xlwt
    from brick.public.create_dir import mkdir_p
    from brick.public.clear_dir import clear_p
    path = MEDIA_ROOT + 'download_xlsx/' + user_name
    mkdir_p(MEDIA_ROOT + 'download_xlsx')
    os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xlsx'))
    clear_p(path)
    mkdir_p(path)
    os.popen('chmod 777 %s' % (path))
    try:
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet('Sheet1', cell_overwrite_ok=True)
        style = xlwt.XFStyle()
        # 字体 宋体
        fnt = xlwt.Font()
        fnt.name = u'SimSun'
        style.font = fnt
        # 位置：居中
        alignment = xlwt.Alignment()  # Create Alignment
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        alignment.vert = xlwt.Alignment.VERT_CENTER
        style.alignment = alignment
        # 边框：实线
        borders = xlwt.Borders()
        borders.left = xlwt.Borders.THIN
        borders.right = xlwt.Borders.THIN
        borders.top = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN
        style.borders = borders

        row = 0
        col = 1
        worksheet.write_merge(row, row + 0, col, col + 4, u'SHIPPER(发件人信息）', style)
        row = 1
        col = 0
        worksheet.write_merge(row, row + 0, col, col + 0, u'标签序号', style)
        col = 1
        worksheet.write_merge(row, row + 0, col, col + 0, u'FBA_SKU', style)
        col = 2
        worksheet.write_merge(row, row + 0, col, col + 0, u'商品名称', style)
        col = 3
        worksheet.write_merge(row, row + 0, col, col + 0, u'商品包装', style)
        col = 4
        worksheet.write_merge(row, row + 0, col, col + 0, u'成本价', style)
        col = 5
        worksheet.write_merge(row, row + 0, col, col + 0, u'MRP价格', style)

        params_count = 1
        for params in all_sku_info_list:
            if params:
                all_count = len(params)
                idx_count = all_count - 3
                row += 1
                last_row = row
                col = 0
                worksheet.write_merge(row, row + idx_count, col, col + 0, params_count, style)
                sku_list = str(params['sku'])
                if ' ' in params['sku']:
                    sku_list = params['sku'].split(' ')
                for k, v in params.items():
                    if k == 'sku' or k == 'mrp_price':
                        pass
                    else:
                        col = 1
                        sku_param = k
                        # print '---------------%s===================%s'%(type(sku_list), sku_list)
                        if isinstance(sku_list, str):
                            sku_param = sku_list
                        else:
                            for sku_each in sku_list:
                                if k in sku_each:
                                    sku_param = sku_each
                        worksheet.write_merge(row, row + 0, col, col + 0, sku_param, style)
                        col = 2
                        worksheet.write_merge(row, row + 0, col, col + 0, v['goodsName'], style)
                        col = 3
                        worksheet.write_merge(row, row + 0, col, col + 0, v['packinfo'], style)
                        col = 4
                        worksheet.write_merge(row, row + 0, col, col + 0, v['costPrice'], style)
                        if idx_count != 0:
                            row += 1
                if idx_count != 0:
                    row = row - 1
                col = 5
                worksheet.write_merge(last_row, last_row + idx_count, col, col + 0, params['mrp_price'], style)
            params_count += 1

        workbook.save(path + '/' + filename)
        upload_to_oss_obj = upload_to_oss(BUCKETNAME_XLS)
        myresult = upload_to_oss_obj.upload_to_oss({'path': user_name+'/Amazon_IN/MRP', 'name': filename, 'byte': open(path + '/' + filename), 'del': 0})
        if myresult['result'] != '':
            sResult = {'code': 1, 'data': u'%s%s.%s/%s/%s' % (PREFIX, BUCKETNAME_XLS, ENDPOINT_OUT, user_name+'/Amazon_IN/MRP', filename)}
        else:
            sResult = {'code': -1, 'errortext': u'上传文件失败'}
    except Exception,e:
        sResult = {'code': -1, 'errortext': u'%s' % e}
    return sResult

def generate_mrp_price_india(request):
    from datetime import datetime as dtywp
    from brick.table.amzon_india_price_config import amzon_india_price_config
    try:
        mrp_sku = request.GET.get('mrp_sku', '')
        shopname = request.GET.get('_p_ShopName__exact', '')
        action_type = request.GET.get('action_type', '')
        all_sku_list = deal_with_fba_sku_to_list(mrp_sku)
        params = get_shop_price_config(shopname)
        final_price_list, all_sku_info_list = get_mrp_price_xls_result(all_sku_list, params)
        sResult = {'code': 1, 'data': final_price_list, 'data2': all_sku_info_list, 'data3': all_sku_list}
        if action_type == 'mrp_xls':
            filename = request.user.username + '_MRP_XLSX_' + dtywp.now().strftime('%Y%m%d%H%M%S') + '.xlsx'
            result = generate_mrp_price_xls(all_sku_info_list, filename, request.user.username)
            if result['code'] == 1:
                sResult = {'code': 1, 'data': result['data'], 'data2': all_sku_info_list, 'data3': all_sku_list}
            else:
                sResult = {'code': -1, 'errortext': result['errortext']}
    except Exception as e:
        traceback.print_exc()
        sResult = {'code': -1, 'errortext': u'%s' % e}
    return JsonResponse(sResult)

def validation_SKU_tortinfo(productSku):
    from brick.classredis.classmainsku import classmainsku
    from brick.classredis.classsku import classsku
    productSKUlist = [productSku, ]
    newProductSKUlist = []
    if 'and' in productSku:
        productSKUlist = productSku.split('and')
    for productSKU in productSKUlist:
        productSKUtemp = productSKU
        if '*' in productSKU:
            productSKUtemp = productSKU.split('*')[0]
        newProductSKUlist.append(productSKUtemp)
    isTort = 0
    tort_list = []
    for newProductSKU in newProductSKUlist:
        classsku_obj = classsku(connection)
        mainSKU = classsku_obj.get_bemainsku_by_sku(newProductSKU)
        classmainsku_obj = classmainsku(connection)
        tortInfo = classmainsku_obj.get_tort_by_mainsku(mainSKU)
        if tortInfo:
            for tortinfo in tortInfo:
                if 'Amazon' in tortinfo:
                    isTort = -1
                    tort_list.append(newProductSKU)
    return isTort, tort_list

def get_childSKU_by_mainSKU(request):
    from brick.classredis.classmainsku import classmainsku
    try:
        main_SKU = request.GET.get('productSKU', '')
        is_Tort, tort_lsit = validation_SKU_tortinfo(main_SKU)
        if is_Tort == 0:
            # messages.info(request, main_SKU)
            child_SKUs = classmainsku(db_cnxn=connection).get_sku_by_mainsku(main_SKU)
            child_SKU_list = []
            for childSKU in child_SKUs:
                child_SKU_dict = {}
                if '-' in childSKU:
                    child_SKU_dict['productSKU'] = childSKU
                    child_SKU_dict['productSize'] = childSKU.split('-')[1]
                else:
                    child_SKU_dict['productSKU'] = childSKU
                    child_SKU_dict['productSize'] = ''
                child_SKU_list.append(child_SKU_dict)
            # messages.info(request, child_SKUs)
            sResult = {'code': 1, 'data': child_SKU_list}
        else:
            sResult = {'code': 0, 'data': tort_lsit}
    except Exception,e:
        sResult = {'code': -1, 'errortext': u'%s'%e}

    return JsonResponse(sResult)
    
    
def add_information_modify(request):
    """增加商品信息修改"""
    source = request.GET.get('source', '')
    if source == 'add_modify':
        return render(request, 't_product_information_modify.html', {'sku': '', 'exists': 'no'})
    elif source == 'search_modify':
        sku = request.GET.get('search_sku', '').strip()
        search_modify_result = search_modify(sku)
        return render(request, 't_product_information_modify.html', search_modify_result)
    else:
        save_modify(request)
        return render(request, 'SKU.html', {'rt': u'提交成功,关闭后刷新!!!'})


def search_modify(sku):
    """根据SKU查询普源信息"""
    import json
    from Project.settings import ITEM_DICT, ITEM_ORDER_LIST
    from pyapp.models import b_goods
    from pyapp.models import ChoicesUnit
    from pyapp.models import B_Supplier
    from skuapp.table.t_product_mainsku_sku import t_product_mainsku_sku
    from pyapp.table.kc_currentstock_sku import kc_currentstock_sku
    from brick.classredis.classsku import classsku
    from django_redis import get_redis_connection
    redis_coon = get_redis_connection(alias='product')
    classsku_obj = classsku(db_cnxn=connection, redis_cnxn=redis_coon)

    if sku.strip() == '':
        return {'sku': sku, 'exists': 'no', 'error_info': u'SKU不能为空'}
    else:
        unit_dict = {}
        for each in ChoicesUnit:
            try:
                unit_dict[each[0]] = each[1]
            except:
                pass

        # 判断传入的是主SKU还是子SKU
        # 主SKU情况：先到t_product_mainsku_sku表找到所有子SKU，再到b_goods表查询商品属性
        # 子SKU情况：直接到b_goods表查询商品属性
        temp_sku_list = []
        t_product_mainsku_sku_objs = t_product_mainsku_sku.objects.filter(MainSKU=sku).values_list('ProductSKU', flat=True)
        if t_product_mainsku_sku_objs.exists():
            for t_product_mainsku_sku_obj in t_product_mainsku_sku_objs:
                temp_sku_list.append(t_product_mainsku_sku_obj)
        if temp_sku_list:
            b_goods_objs = b_goods.objects.filter(SKU__in=temp_sku_list)
            main_sku = sku
        else:
            b_goods_objs = b_goods.objects.filter(SKU=sku)
            main_sku = classsku_obj.get_bemainsku_by_sku(sku=sku)

        if b_goods_objs.exists():
            modify_dict = {}
            sku_list = []
            for obj in b_goods_objs:
                supplier_name = ''
                B_Supplier_obj = B_Supplier.objects.filter(NID=obj.SupplierID)
                if B_Supplier_obj.exists():
                    supplier_name = B_Supplier_obj[0].SupplierName
                warning_obj = kc_currentstock_sku.objects.filter(SKU=sku).values_list('CgCategory')
                if warning_obj.exists():
                    WarningCats = WARNING_DICT.get(warning_obj[0][0], '')
                else:
                    WarningCats = ''
                modify_dict[obj.SKU] = {
                    'GoodsName': str(obj.GoodsName), 'GoodsStatus': str(obj.GoodsStatus), 'Material': str(obj.Material),
                    'Class': str(obj.Class), 'Model': str(obj.Model), 'Style': str(obj.Style), 'Brand': str(obj.Brand),
                    'Unit': str(obj.Unit), 'PackageCount': str(obj.PackageCount), 'Weight': str(obj.Weight),
                    'BarCode': str(obj.BarCode), 'SupplierName': supplier_name, 'CostPrice': str(obj.CostPrice),
                    'BatchPrice': str(obj.BatchPrice), 'RetailPrice': str(obj.RetailPrice),
                    'SalePrice': str(obj.SalePrice), 'MaxSalePrice': str(obj.MaxSalePrice),
                    'MarketPrice': str(obj.MarketPrice), 'Notes': str(obj.Notes), 'AliasCnName': str(obj.AliasCnName),
                    'AliasEnName': str(obj.AliasEnName), 'DeclaredValue': str(obj.DeclaredValue),
                    'OriginCountryCode': str(obj.OriginCountryCode), 'OriginCountry': str(obj.OriginCountry),
                    'MaxNum': str(obj.MaxNum), 'MinNum': str(obj.MinNum), 'SalerName': str(obj.SalerName),
                    'SalerName2': str(obj.SalerName2), 'PackName': str(obj.PackName), 'DevDate': str(obj.DevDate),
                    'BmpUrl': str(obj.BmpUrl), 'Purchaser': str(obj.Purchaser), 'StoreID': str(obj.StoreID),
                    'StockDays': str(obj.StockDays), 'LinkUrl': str(obj.LinkUrl), 'LinkUrl2': str(obj.LinkUrl2),
                    'LinkUrl3': str(obj.LinkUrl3), 'MinPrice': str(obj.MinPrice), 'HSCODE': str(obj.HSCODE),
                    'SellDays': str(obj.SellDays), 'StockMinAmount': str(obj.StockMinAmount), 'InLong': str(obj.InLong),
                    'InWide': str(obj.InWide), 'InHigh': str(obj.InHigh), 'InGrossweight': str(obj.InGrossweight),
                    'InNetweight': str(obj.InNetweight), 'OutLong': str(obj.OutLong), 'OutWide': str(obj.OutWide),
                    'OutHigh': str(obj.OutHigh), 'OutGrossweight': str(obj.OutGrossweight),
                    'OutNetweight': str(obj.OutNetweight), 'ItemUrl': str(obj.ItemUrl), 'PackMsg': str(obj.PackMsg),
                    'IsCharged': str(obj.IsCharged), 'Season': str(obj.Season), 'IsPowder': str(obj.IsPowder),
                    'IsLiquid': str(obj.IsLiquid), 'possessMan1': str(obj.possessMan1),
                    'possessMan2': str(obj.possessMan2), 'ShopTitle': str(obj.ShopTitle), 'LinkUrl4': str(obj.LinkUrl4),
                    'LinkUrl5': str(obj.LinkUrl5), 'LinkUrl6': str(obj.LinkUrl6),
                    'ShopCarryCost': str(obj.ShopCarryCost), 'PackWeight': str(obj.PackWeight),
                    'ExchangeRate': str(obj.ExchangeRate), 'LogisticsCost': str(obj.LogisticsCost),
                    'GrossRate': str(obj.GrossRate), 'CalSalePrice': str(obj.CalSalePrice), 'PackFee': str(obj.PackFee),
                    'AttributeName': str(obj.AttributeName)
                }
                sku_list.append(obj.SKU)
            modify_dict['public'] = modify_dict[sku_list[0]]
            pack_data_list = get_pack_info()
            return {
                'sku': sku, 'exists': 'yes', 'sku_list': sku_list, 'modify_dict': json.dumps(modify_dict),
                'item_dict': json.dumps(ITEM_DICT), 'item_order_list': ITEM_ORDER_LIST, 'item_dict_1': ITEM_DICT,
                'unit_dict': json.dumps(unit_dict), 'mainsku': main_sku, 'pack_data': json.dumps(pack_data_list)
            }
        else:
           return {'sku': sku, 'exists': 'no', 'error_info': sku + u' 不存在'}


def get_pack_info():
    from skuapp.table.B_PackInfo import B_PackInfo
    packname_cost_list = B_PackInfo.objects.filter().values_list('PackName', 'CostPrice')
    data_list = []
    for packname_cost in packname_cost_list:
        try:
            packname = packname_cost[0].strip()
            cost = float(packname_cost[1])
            if packname and cost:
                temp_dict = {
                    'title': packname, 'result': {'cost': cost}
                }
                data_list.append(temp_dict)
        except:
            pass
    return data_list


def save_modify(request):
    """保存提交的商品信息修改"""
    from datetime import datetime
    from pyapp.models import b_goodscats as py_b_goodscats
    from skuapp.modelsadminx.t_product_Admin import t_product_Admin
    import json
    import copy
    from Project.settings import ITEM_DICT

    son_sku_list = request.POST.getlist('son_sku', '')
    main_sku = request.POST.get('mainsku', '')
    modify_dict = request.POST.get('modify_dict', '')
    modify_dict = json.loads(modify_dict)
    sys_param_dict = get_information_modify_param()

    select_list = []
    sh_flag = 0  # 待审核标记
    lq_flag = 0  # 待领去标记
    ht_flag = 0  # 待换图标记
    picture_note_list = []
    is_request_picture_list = []

    obj = t_product_information_modify()

    b_goods_objs = py_b_goods.objects.filter(SKU__startswith=main_sku)
    value_dict = {}
    all_cost_reduction_dict = {}
    if son_sku_list:
        for son_sku in son_sku_list:
            son_sku_dict = {}
            for k, v in ITEM_DICT.items():
                if son_sku == 'public':
                    public_property = request.POST.getlist(k + '_' + 'all', '')  # 公共属性
                    if public_property:
                        change_list, ht_flag, sh_flag, lq_flag, select_list, picture_note_list, is_request_picture, single_cost_reduction_dict = \
                            information_modify_detail_process(public_property, select_list, picture_note_list, k, v, sys_param_dict, ht_flag, sh_flag, lq_flag)
                        if len(change_list) == 3:
                            continue
                        for x_sku in son_sku_list:
                            if x_sku != 'public':
                                temp = copy.deepcopy(change_list)
                                temp[1] = modify_dict[x_sku][k]
                                son_sku_dict[k] = temp
                                if is_request_picture:
                                    is_request_picture_list.append(x_sku)
                                if value_dict.get(x_sku, ''):
                                    value_dict[x_sku] = dict(copy.deepcopy(son_sku_dict), **value_dict[x_sku])
                                else:
                                    value_dict[x_sku] = copy.deepcopy(son_sku_dict)

                                if single_cost_reduction_dict:
                                    single_cost_reduction_dict['old_price'] = modify_dict[x_sku]['CostPrice']
                                    all_cost_reduction_dict[x_sku] = single_cost_reduction_dict
                else:
                    sku_property = request.POST.getlist(k + '_' + son_sku, '')  # 子SKU属性
                    if sku_property:
                        change_list, ht_flag, sh_flag, lq_flag, select_list, picture_note_list, is_request_picture, single_cost_reduction_dict = \
                            information_modify_detail_process(sku_property, select_list, picture_note_list, k, v, sys_param_dict, ht_flag, sh_flag, lq_flag)
                        if len(change_list) == 3:
                            continue
                        if is_request_picture:
                            is_request_picture_list.append(son_sku)
                        son_sku_dict[k] = change_list
                        if value_dict.get(son_sku, ''):
                            value_dict[son_sku] = dict(son_sku_dict, **value_dict[son_sku])
                        else:
                            value_dict[son_sku] = son_sku_dict

                        if single_cost_reduction_dict:
                            single_cost_reduction_dict['old_price'] = modify_dict[son_sku]['CostPrice']
                            all_cost_reduction_dict[son_sku] = single_cost_reduction_dict

    obj.MainSKU = main_sku
    obj.Details = value_dict
    obj.SKU = b_goods_objs[0].SKU  # 子SKU
    obj.Name2 = b_goods_objs[0].GoodsName  # 商品名称
    obj.Keywords = b_goods_objs[0].AliasEnName  # 英文关键词
    obj.Keywords2 = b_goods_objs[0].AliasCnName  # 中文关键词
    obj.SourcePicPath2 = u'http://fancyqube.net:89/ShopElf/images/%s.jpg' % b_goods_objs[0].SKU.replace('OAS-','').replace('FBA-', '')
    obj.Material = b_goods_objs[0].Material  # 材质
    obj.DevDate = b_goods_objs[0].DevDate
    obj.XGcontext = ''
    obj.InputBox = ','.join(son_sku_list).replace('public,', '')

    goodscat = b_goods_objs[0].CategoryCode.split('|')  # 类别code
    obj.LargeCategory = None
    obj.SmallCategory = None
    if len(goodscat) >= 3:
        py_b_goodscats_objs = py_b_goodscats.objects.filter(CategoryCode='|'.join(goodscat))
        if py_b_goodscats_objs.exists():
            if goodscat[2].strip() != '':
                obj.LargeCategory = py_b_goodscats_objs[0].CategoryParentName
                obj.SmallCategory = py_b_goodscats_objs[0].CategoryName
            else:
                obj.LargeCategory = py_b_goodscats_objs[0].CategoryName

    obj.SQTimeing = datetime.now()
    obj.SQStaffNameing = request.user.first_name
    obj.Source = u'普源信息'
    obj.CostReduction = all_cost_reduction_dict if all_cost_reduction_dict else None

    if ht_flag == 1:
        obj.Mstatus = 'DHT'  # 待换图
        t_product_Admin_obj = t_product_Admin()
        # 插入 领取美工 步骤
        main_sku_str = ','.join(list(set(is_request_picture_list)))
        ed_obj = t_product_develop_ed.objects.create(
            id=t_product_Admin_obj.get_id(), MGProcess='5', MainSKU=main_sku_str, SKU=b_goods_objs[0].SKU,
            Name2=b_goods_objs[0].GoodsName, Keywords=b_goods_objs[0].AliasEnName, Keywords2=b_goods_objs[0].AliasCnName,
            SourcePicPath2=u'http://fancyqube.net:89/ShopElf/images/%s.jpg' % b_goods_objs[0].SKU.replace('OAS-', '').replace('FBA-', ''),
            UnitPrice=b_goods_objs[0].CostPrice, Material=b_goods_objs[0].Material,
            PictureRequest=';'.join(list(set(picture_note_list))), JZLStaffName='', JZLTime=None
        )
        t_product_oplog.objects.create(
            pid=ed_obj.id, MainSKU=main_sku, Name=b_goods_objs[0].GoodsName, Name2=b_goods_objs[0].GoodsName,
            OpID=request.user.username, OpName=request.user.first_name, StepID=u'DHT', StepName='去换图',
            BeginTime=datetime.now()
        )
    if lq_flag == 1:
        obj.Mstatus = 'DLQ'  # 待领取
    if sh_flag == 1:
        obj.Mstatus = 'DSH'  # 待审核
    select = list(set(select_list))
    if len(select) == 1:
        obj.Select = select[0]
    else:
        obj.Select = 100
    obj.save()


def get_information_modify_param():
    """获取t_sys_param配置的修改类型"""
    from skuapp.table.t_sys_param import t_sys_param
    t_sys_param_objs = t_sys_param.objects.filter(Type=3)
    sys_param_dict = {}
    for t_sys_param_obj in t_sys_param_objs:
        sys_param_dict[t_sys_param_obj.VDesc] = t_sys_param_obj.V
    return sys_param_dict


def information_modify_detail_process(change_list, select_list, picture_note_list, k, v, sys_param_dict, ht_flag, sh_flag, lq_flag):
    """保存商品信息修改细节处理过程"""
    sh_item = ['SalerName2', 'WarningCats']
    sh_goodsstatus = [u'清仓下架(需审核)', u'售完下架(需审核)', u'处理库尾(需审核)', u'停售(需审核)', u'清仓（合并）(需审核)']
    is_request_picture = 0
    single_cost_reduction_dict = {}

    if (change_list[1].strip() == '') and (k != 'BmpUrl'):
        pass
    else:
        change_list.insert(0, v)
        if k == 'BmpUrl':
            ht_flag = 1
        elif k in sh_item:
            sh_flag = 1
        else:
            lq_flag = 1

        if k == 'GoodsStatus':
            new_status = change_list[2]
            select_list.append(sys_param_dict[new_status])
            change_list.append(new_status)
            if new_status in sh_goodsstatus:
                sh_flag = 1
        elif k == 'WarningCats':
            select_list.append(19)
            change_list.append(u'库存预警(需审核)')
        elif k == 'CostPrice':
            try:
                old_price = float(str(change_list[1]))
                new_price = float(str(change_list[2]))
            except Exception, e:
                old_price, new_price = 0, 0

            if old_price < new_price:
                select_list.append(4)
                change_list.append(u'涨价(需审核)')
                sh_flag = 1
            else:
                select_list.append(11)
                change_list.append(u'降价')
                single_cost_reduction_dict['old_price'] = old_price
                single_cost_reduction_dict['new_price'] = new_price
        elif k == 'SalerName2':
            select_list.append(6)
            change_list.append(u'变更业绩归属人2(需审核)')
        elif k == 'BmpUrl':
            select_list.append(1)
            picture_note_list.append(change_list[3])
            change_list.append(u'换图片')
            is_request_picture = 1
        else:
            select_list.append(3)
            change_list.append(u'更改商品信息')
    return change_list, ht_flag, sh_flag, lq_flag, select_list, picture_note_list, is_request_picture, single_cost_reduction_dict


def show_modify_detail(request):
    """显示商品信息修改详情"""
    from Project.settings import WARNING_DICT
    from pyapp.models import ChoicesUnit
    modify_id = request.GET.get('modify_id', '')
    page = request.GET.get('page', '')
    from skuapp.table.t_product_information_modify import t_product_information_modify as information_modify
    all_result_list = []
    infomation_modify_obj = information_modify.objects.filter(id=modify_id)
    if infomation_modify_obj.exists():
        details = eval(infomation_modify_obj[0].Details) if infomation_modify_obj[0].Details else ''
        if infomation_modify_obj[0].Select == '7':
            all_result_list = details
            flag = 'merge_sku'
        else:
            flag = 'modify_all'
            for k1, v1 in details.items():
                sku = k1
                for k2, v2 in v1.items():
                    name = v2[0]
                    if k2 == 'WarningCats':
                        old_val = WARNING_DICT.get(v2[1], '') if v2[1] else ''
                        new_val = WARNING_DICT.get(v2[2], '') if v2[2] else ''
                    else:
                        old_val = v2[1]
                        new_val = v2[2]
                    describe = v2[3]
                    modify_type = v2[4]
                    single_result_list = [sku, name, old_val, new_val, describe, modify_type]
                    all_result_list.append(single_result_list)
    unit_dict = {}
    for each in ChoicesUnit:
        try:
            unit_dict[each[0]] = each[1]
        except:
            pass
    return render(request, 'show_modify_detail.html',
                  {'all_result_list': all_result_list, 'flag': flag, 'details': details, 'unit': unit_dict,
                   'modify_id': modify_id, 'WARNING_DICT': WARNING_DICT, 'page': page})

def save_modify_second(request):
    from Project.settings import ITEM_ORDER_LIST
    from skuapp.table.t_product_information_modify import t_product_information_modify
    from copy import deepcopy

    flag = request.POST.get('flag', '')
    modify_id = request.POST.get('modify_id', '')
    sku_list = request.POST.getlist('son_sku', '')
    all_sku_dict = {}
    all_sku_list = []
    if sku_list:
        sku_list = list(set(sku_list))
        if flag == 'modify_all':
            for sku in sku_list:
                single_sku_dict = {}
                for item in ITEM_ORDER_LIST:
                    name = item + '_' + sku
                    post_value = request.POST.getlist(name, '')
                    if post_value:
                        if item == 'GoodsStatus':
                            post_value[-1] = post_value[2]
                        single_sku_dict[item] = deepcopy(post_value)
                all_sku_dict[sku] = single_sku_dict
            t_product_information_modify.objects.filter(id=modify_id).update(Details=str(all_sku_dict))
        else:
            for sku in sku_list:
                post_value = request.POST.getlist(sku, '')
                if post_value:
                    single_sku_dict = {'delete_sku': sku, 'retain_sku': post_value[0], 'describe': post_value[1]}
                    all_sku_list.append(single_sku_dict)
            t_product_information_modify.objects.filter(id=modify_id).update(Details=str(all_sku_list))
        rr = u'修改成功,关闭后刷新'
    else:
        rr = u'没有要保存的数据，此次不保存您的修改'
    return render(request, 'SKU.html', {'rt': rr})


def add_warning_modify(request):
    source = request.GET.get('source', '')
    if source == 'add_warning':
        return render(request, 't_product_warning_modify.html', {'sku': '', 'exists': 'no'})
    elif source == 'search_warning':
        main_sku = request.GET.get('main_sku', '').strip()
        son_sku = request.GET.get('son_sku', '').strip()
        search_result = search_warning(main_sku_str=main_sku, son_sku_str=son_sku)
        error_info = search_result.get('errortext', '')
        if error_info == '':
            return render(request, 't_product_warning_modify.html', search_result)
        else:
            return render(request, 't_product_warning_modify.html', {'exists': 'no', 'error_info': error_info})
    else:
        save_warning(request)
        return render(request, 'SKU.html', {'rt': u'提交成功,关闭后刷新!!!'})

def search_warning(main_sku_str, son_sku_str):
    try:
        from pyapp.models import b_goods
        from pyapp.table.kc_currentstock_sku import kc_currentstock_sku
        from Project.settings import WARNING_DICT
        from brick.classredis.classsku import classsku
        from skuapp.table.t_product_mainsku_sku import t_product_mainsku_sku
        from django_redis import get_redis_connection
        redis_coon = get_redis_connection(alias='product')
        classsku_obj = classsku(db_cnxn=connection, redis_cnxn=redis_coon)

        error_main_sku_list = []
        error_son_sku_list = []
        sku_list = []
        sku_warning_list = []
        real_main_sku_list = []
        main_sku_list = main_sku_str.split(',')
        son_sku_list = son_sku_str.split(',')

        if main_sku_str:
            for main_sku in main_sku_list:
                objs = t_product_mainsku_sku.objects.filter(MainSKU=main_sku).values_list('ProductSKU', flat=True)
                if objs.exists():
                    for obj in objs:
                        son_sku_list.append(obj)
                else:
                    error_main_sku_list.append(main_sku)

        for son_sku in son_sku_list:
            son_sku_obj = b_goods.objects.filter(SKU=son_sku).values_list('SKU')
            if son_sku_obj.exists():
                sku_list.append(son_sku)
            else:
                error_son_sku_list.append(son_sku)

        if len(sku_list) > 200:
            return {'errortext': u'商品SKU个数已经超出200个,请分批提交'}

        for sku in sku_list:
            real_main_sku = classsku_obj.get_bemainsku_by_sku(sku=sku)
            real_main_sku_list.append(real_main_sku)
            temp_dict = {'SKU': sku}
            warning_obj = kc_currentstock_sku.objects.filter(SKU=sku).values_list('CgCategory')
            if warning_obj.exists():
                temp_dict['Warning'] = WARNING_DICT.get(warning_obj[0][0], '')
            else:
                temp_dict['Warning'] = ''
            sku_warning_list.append(temp_dict)

        error_main_sku_str = ','.join(error_main_sku_list)
        error_son_sku_str = ','.join(error_son_sku_list)
        return {
            'main_sku': main_sku_str, 'son_sku': son_sku_str, 'error_main_sku_str': error_main_sku_str,
            'error_son_sku_str': error_son_sku_str, 'sku_warning_list': sku_warning_list, 'exists': 'yes',
            'real_main_sku': real_main_sku_list[0] if real_main_sku_list else ''
        }
    except Exception, e:
        result = {'errortext': 'Exception=%s ex=%s;__LINE__=%s' % (Exception, e, sys._getframe().f_lineno), 'error_code': 1}
        return result


def save_warning(request):
    try:
        from pyapp.models import b_goodscats as py_b_goodscats
        from datetime import datetime
        main_sku = request.POST.get('real_main_sku', '')
        sku_list = request.POST.getlist('sku', '')
        old_warning_list = request.POST.getlist('old_warning', '')
        new_warning_list = request.POST.getlist('new_warning', '')
        describe_list = request.POST.getlist('describe', '')

        obj = t_product_information_modify()
        for sku in sku_list:
            b_goods_objs = b_goods.objects.filter(SKU=sku)
            if b_goods_objs.exists():
                break
            else:
                pass

        input_sku = ','.join(sku_list)
        details = {}
        for i in range(len(sku_list)):
            temp_dict = {'WarningCats': [u'库存预警', old_warning_list[i], new_warning_list[i], describe_list[i], u'库存预警(需审核)']}
            details[sku_list[i]] = temp_dict

        obj.MainSKU = main_sku
        obj.Details = details
        obj.SKU = sku_list[0]  # 子SKU
        obj.Name2 = b_goods_objs[0].GoodsName  # 商品名称
        obj.Keywords = b_goods_objs[0].AliasEnName  # 英文关键词
        obj.Keywords2 = b_goods_objs[0].AliasCnName  # 中文关键词
        obj.SourcePicPath2 = u'http://fancyqube.net:89/ShopElf/images/%s.jpg' % b_goods_objs[0].SKU.replace('OAS-',
                                                                                                            '').replace(
            'FBA-', '')
        obj.Material = b_goods_objs[0].Material  # 材质
        obj.DevDate = b_goods_objs[0].DevDate
        obj.XGcontext = ''
        obj.InputBox = input_sku

        goodscat = b_goods_objs[0].CategoryCode.split('|')  # 类别code
        obj.LargeCategory = None
        obj.SmallCategory = None
        if len(goodscat) >= 3:
            py_b_goodscats_objs = py_b_goodscats.objects.filter(CategoryCode='|'.join(goodscat))
            if py_b_goodscats_objs.exists():
                if goodscat[2].strip() != '':
                    obj.LargeCategory = py_b_goodscats_objs[0].CategoryParentName
                    obj.SmallCategory = py_b_goodscats_objs[0].CategoryName
                else:
                    obj.LargeCategory = py_b_goodscats_objs[0].CategoryName

        obj.SQTimeing = datetime.now()
        obj.SQStaffNameing = request.user.first_name
        obj.Source = u'普源信息'
        obj.Mstatus = 'DSH'
        obj.Select = 19
        obj.save()
        return {'error_code': 0}
    except Exception, e:
        result = {'errortext': 'Exception=%s ex=%s;__LINE__=%s' % (Exception, e, sys._getframe().f_lineno), 'error_code': 1}
        return result


def add_merge_sku(request):
    source = request.GET.get('source', '')
    if source == 'add_merge':
        return render(request, 't_product_merge_sku.html', {'sku': '', 'exists': 'no'})
    elif source == 'search_merge':
        search_sku = request.GET.get('search_sku', '').strip()
        search_result = search_merge(search_sku=search_sku)
        error_info = search_result.get('error_info', '')
        if error_info == '':
            return render(request, 't_product_merge_sku.html', search_result)
        else:
            return render(request, 't_product_merge_sku.html', {'exists': 'no', 'error_info': error_info, 'sku': search_sku})
    else:
        save_result = save_merge(request)
        if save_result['error_code'] == 0:
            rt = u'提交成功,关闭后刷新!!!'
        else:
            rt = u'%s' % save_result['error_info']
        return render(request, 'SKU.html', {'rt': rt})


def search_merge(search_sku):
    from pyapp.models import b_goods
    from skuapp.table.t_product_mainsku_sku import t_product_mainsku_sku
    from brick.classredis.classsku import classsku
    from django_redis import get_redis_connection
    redis_coon = get_redis_connection(alias='product')
    classsku_obj = classsku(db_cnxn=connection, redis_cnxn=redis_coon)

    sku_list = []
    main_sku = ''
    if search_sku:
        objs = t_product_mainsku_sku.objects.filter(MainSKU=search_sku).values_list('ProductSKU', flat=True)
        if objs.exists():
            main_sku = search_sku
            for obj in objs:
                sku_list.append(obj)
        else:
            b_goods_objs = b_goods.objects.filter(SKU=search_sku).values_list('SKU', flat=True)
            if b_goods_objs.exists():
                main_sku = classsku_obj.get_bemainsku_by_sku(sku=search_sku)
                for b_goods_obj in b_goods_objs:
                    sku_list.append(b_goods_obj)
        if sku_list:
            return {'sku_list': sku_list, 'sku': search_sku, 'main_sku': main_sku}
        else:
            return {'error_info': '未查询到您输入的SKU：%s' % search_sku}
    else:
        return {'error_info': '搜索内容不能为空'}


def verify_merge_sku(request):
    from pyapp.models import b_goods
    from django.http import HttpResponse

    sku_str = request.POST.get('sku_str', '')
    sku_list = sku_str.split(',')
    non_existent_sku = []
    for sku in sku_list:
        if sku:
            obj = b_goods.objects.filter(SKU=sku)
            if not obj.exists():
                non_existent_sku.append(sku)
    if non_existent_sku:
        error_sku = ','.join(non_existent_sku)
        error_info = u'下列SKU："%s" 未查询到，请检查后提交！！！' % error_sku
        sResult = {'sMsg': '-1', 'sError': error_info}
    else:
        sResult = {'sMsg': '0'}
    return HttpResponse(json.dumps(sResult))


def save_merge(request):
    from pyapp.models import b_goods
    from pyapp.models import b_goodscats as py_b_goodscats
    from datetime import datetime

    main_sku = request.POST.get('main_sku', '')
    delete_sku_list = request.POST.getlist('delete_sku', '')
    retain_sku_list = request.POST.getlist('retain_sku', '')
    describe_list = request.POST.getlist('describe', '')
    try:
        obj = t_product_information_modify()
        b_goods_objs = b_goods.objects.filter(SKU=delete_sku_list[0])
        input_sku = ','.join(delete_sku_list)
        details = []
        for i in range(len(delete_sku_list)):
            temp_dict = {
                'delete_sku': delete_sku_list[i], 'retain_sku': retain_sku_list[i], 'describe': describe_list[i]
            }
            details.append(temp_dict)

        obj.MainSKU = main_sku
        obj.Details = details
        obj.SKU = delete_sku_list[0]  # 子SKU
        obj.Name2 = b_goods_objs[0].GoodsName  # 商品名称
        obj.Keywords = b_goods_objs[0].AliasEnName  # 英文关键词
        obj.Keywords2 = b_goods_objs[0].AliasCnName  # 中文关键词
        obj.SourcePicPath2 = u'http://fancyqube.net:89/ShopElf/images/%s.jpg' % b_goods_objs[0].SKU.replace('OAS-', '').replace('FBA-', '')
        obj.Material = b_goods_objs[0].Material  # 材质
        obj.DevDate = b_goods_objs[0].DevDate
        obj.XGcontext = ''
        obj.InputBox = input_sku
        goodscat = b_goods_objs[0].CategoryCode.split('|')  # 类别code
        obj.LargeCategory = None
        obj.SmallCategory = None
        if len(goodscat) >= 3:
            py_b_goodscats_objs = py_b_goodscats.objects.filter(CategoryCode='|'.join(goodscat))
            if py_b_goodscats_objs.exists():
                if goodscat[2].strip() != '':
                    obj.LargeCategory = py_b_goodscats_objs[0].CategoryParentName
                    obj.SmallCategory = py_b_goodscats_objs[0].CategoryName
                else:
                    obj.LargeCategory = py_b_goodscats_objs[0].CategoryName
        obj.SQTimeing = datetime.now()
        obj.SQStaffNameing = request.user.first_name
        obj.Source = u'普源信息'
        obj.Mstatus = 'DSH'
        obj.Select = 7
        obj.save()
        return {'error_code': 0}
    except Exception, e:
        result = {'error_info': 'Exception=%s ex=%s;__LINE__=%s' % (Exception, e, sys._getframe().f_lineno), 'error_code': 1}
        return result


def check_sku_tortinfo(request):
    try:
        productSku = request.GET.get('productSKU', '')
        is_Tort, tort_lsit = validation_SKU_tortinfo(productSku)
        sResult = {'code': 1, 'data': is_Tort, 'tort_list': tort_lsit}
    except Exception, e:
        sResult = {'code': -1, 'errortext': u'%s' % e}

    return JsonResponse(sResult)

def get_template_amazon(request):
    from skuapp.table.t_config_amazon_template import t_config_amazon_template
    try:
        templates = []
        shopname = request.GET.get('shopname', '')
        shipping_group_sites = {'US': 'Migrated Template', 'DE': 'Standardvorlage Amazon',
                                'FR': 'Modèle par défaut Amazon', 'UK': 'Migrated Template',
                                'AU': 'Migrated Template', 'IN': 'Migrated Template'}
        if shopname:
            searchSite = shopname.split('-')[-1].split('/')[0]
            templates = [shipping_group_sites[searchSite]]
        templates_amazon = t_config_amazon_template.objects.filter(shopName__exact=shopname).values('template_name')
        if templates_amazon.exists():
            for template_amazon in templates_amazon:
                templates.append(template_amazon['template_name'].replace("u'", "'"))
            templates = list(set(templates))
        if templates:
            templates = json.dumps(templates)
        sResult = {'code': 1, 'data': templates}
    except Exception, e:
        sResult = {'code': -1, 'errortext': u'%s' % e}

    return JsonResponse(sResult)
    
    
    
def t_check_report_Plugin(request):
    try:
        result = {'errorcode': 0,'errortext': ''}
        hqdb_cursor = connection.cursor()
        str_hqdb_selectSql = "select a.Stocking_plan_number,a.Purchase_Order_No,a.ProductSKU,a.ProductName,a.ProductImage,a.Weight,a.Price,a.QTY,a.The_arrival_of_the_number,a.StorageDate," \
                             "c.Buyer,b.SalerName,b.SalerName2,a.Destination_warehouse,a.Demand_people " \
                             "from t_set_warehouse_storage_situation_list a left join t_stocking_purchase_order c  on a.Stocking_plan_number=c.Stocking_plan_number " \
                             "left join py_db.b_goods b on a.ProductSKU=b.sku " \
                             "where a.Storage_status='already' and a.Stocking_plan_number not in (select Stocking_plan_number from t_stocking_check_report); "
        hqdb_cursor.execute(str_hqdb_selectSql)
        tupple_hqdb_stockStatus = hqdb_cursor.fetchall()
        num = 0
        for obj in tupple_hqdb_stockStatus:
            strInsert = "insert  into t_stocking_check_report(Stocking_plan_number,Purchase_Order_No,ProductSKU,ProductName,ProductImage,ProductWeight,ProductPrice,PurchaseNumber,ArrivalNumber,Purchase_date,Purchaser,SalerName,SalerName2,isFBA,Demand_people) " \
                        "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            hqdb_cursor.execute(strInsert, obj)
            num += 1
        hqdb_cursor.execute('commit')
        result['errortext'] = u'成功刷新%s条'%(str(num))
        hqdb_cursor.close()
    except Exception as e:
        hqdb_cursor.close()
        result = {'errorcode': -1, 'errortext': u'%s' % e}
    messages.info(request, '%s' % result['errortext'])
    return HttpResponseRedirect('/Project/admin/skuapp/t_stocking_check_report/')

def t_stocking_purchase_Plugin(request):
    try:
        result = {'errorcode': 0,'errortext': '','count':0}
        from brick.pydata.py_syn.b_stockStatus import b_stockStatus
        obj_stockStatus = b_stockStatus()
        result = obj_stockStatus.deal_purchase_data()
    except Exception as e:
        result = {'errorcode': -1, 'errortext': u'%s' % e}
    messages.info(request, u'成功刷新%s条,%s' %(result['count'],result['errortext']))
    return HttpResponseRedirect('/Project/admin/skuapp/t_stocking_purchase_order/')

def deal_checkReportData(request):
    try:
        from skuapp.table.t_stocking_check_report import t_stocking_check_report
        from datetime import datetime as ddtime
        get_ProductSKU = request.GET.get('ProductSKU')
        get_id = request.GET.get('id')
        checkPart_Num = request.GET.get('checkPart_Num')
        checkPass_Num = request.GET.get('checkPass_Num')
        empty = request.GET.get('empty')
        selectCheck = request.GET.get('selectCheck')
        if str(selectCheck) in (0,1,2,'0','1','2'):
            t_stocking_check_report.objects.filter(id=get_id).update(isCheck=selectCheck,CheckMan = request.user.first_name,CheckTime=ddtime.now())
            return JsonResponse({'result': 'OK'})
        if str(empty) == "99999":
            t_stocking_check_report.objects.filter(id=get_id).update(CheckNumber=checkPart_Num,CheckQualified=checkPass_Num,PercentOfPass="0",CheckMan = request.user.first_name,CheckTime=ddtime.now())
            return JsonResponse({'result': 'OK','dataContent':0})
        if (checkPart_Num == 0 or int(checkPart_Num) < int(checkPass_Num)):
            return JsonResponse({'result': 'NG'})
        PercentOfPass = '%.2f'%((float(checkPass_Num)/float(checkPart_Num))*100)
        t_stocking_check_report.objects.filter(id=get_id).update(CheckNumber=checkPart_Num,CheckQualified=checkPass_Num,PercentOfPass=str(PercentOfPass),CheckMan = request.user.first_name,CheckTime=ddtime.now())
        return JsonResponse({'result': 'OK','dataContent':PercentOfPass})
    except Exception as e:
        #messages.info(request, u'id=%s,get_ProductSKU=%s,checkPart_Num=%s,checkPass_Num=%s error:%s,录入数据存在问题，请修正后重新计算。'% (get_id,get_ProductSKU,checkPart_Num,checkPass_Num,str(e)))
        return JsonResponse({'result': 'NG'})    
    
def transaction_text_amazon(request):
    # from langdetect import detect
    post = request.GET
    tra_to = post.get("tra_to", "")
    tra_type = post.get("tra_type", "")
    tra_data = post.get("tra_data", "")
    split_type = "========="
    tra_datas = [tra_data]
    if split_type in tra_data:
        tra_datas = tra_data.split(split_type)
    # messages.info(request, "tra_to: %s, tra_type: %s, tra_data: %s, "%(tra_to,tra_type,tra_data))
    sResult = ''
    # if detect(tra_data) != 'en':
    #     sResult = {'code': -1, 'errortext': u'待翻译语种需为英文...%s.....%s'%(tra_data,detect(tra_data))}
    # else:
    try:
        result_final = ""
        for transaction_data in tra_datas:
            host = 'http://jisuzxfy.market.alicloudapi.com'
            path = '/translate/translate'
            method = 'GET'
            appcode = "2cd4ea81891e4118bee6ecfae5d0f2f1"
            querys = "from=en&%s&to=%s&type=%s"%((urllib.urlencode({"text":transaction_data})),tra_to,tra_type)
            bodys = {}
            url = host + path + "?" + querys

            req = urllib2.Request(url)
            req.add_header('Authorization', 'APPCODE ' + appcode)
            req.add_header('Content-Type', 'application/json; charset=utf-8')
            response = urllib2.urlopen(req)
            _content = eval(response.read())
            if _content['status'] == '0' and _content['msg'] == 'ok':
                result = _content['result'].get('result', '').encode('unicode_escape').decode('string_escape')
                if ' ' not in transaction_data and '<br' in result:
                    result = result.split('<br')[0]
                if '\\' in result:
                    result = result.replace('\\', '')
            else:
                result = 'transaction error'
            result_final += result + split_type
        sResult = {'code': 1, 'data': result_final}
    except Exception, ex:
        sResult = {'code': -1, 'errortext': u'%s'%ex}
        print '%s_%s:%s' % (traceback.print_exc(), Exception, ex)
    return JsonResponse(sResult)    
    
    
# amazon价格调整
def amazon_product_price_modify(request):
    from django.db import connection
    from brick.amazon.product_refresh.get_auth_info import GetAuthInfo
    from brick.amazon.product_refresh.generate_feed_xml import GenerateFeedXml
    from brick.amazon.upload_product.message_to_rabbitmq import MessageToRabbitMq
    import json
    from skuapp.table.t_online_info_amazon import t_online_info_amazon
    import datetime
    import urllib
    from django.http import HttpResponseRedirect

    ids = request.POST.get('id','').split(',')
    modify_type = request.POST.get('modify_type', '')
    modify_base = request.POST.get('modify_base', '')
    modify_number = request.POST.get('modify_number', '')

    shop_sku = dict()
    fail_record = list()
    sku_str = ''
    refresh_type = 'product_price_modify_multi'

    for record in ids:
        t_online_info_amazon_ins = t_online_info_amazon.objects.filter(id=record)
        for obj in t_online_info_amazon_ins:
            seller_sku = obj.seller_sku
            sku_str = sku_str + seller_sku + ','  # 用于执行操作后显示相应条目
            shop_name = obj.ShopName

            # 获取基准价格
            if modify_base == 'price':
                base_price = obj.price
            elif modify_base == 'estimated_fee':
                base_price = obj.estimated_fee
            else:
                base_price = None

            # 计算调整后的价格，计算价格异常或调整后的价格小于等于0时跳过
            try:
                if modify_type == 'increase':
                    price_after = float('%.2f' % (float(base_price) + float(modify_number)))
                elif modify_type == 'reduce':
                    price_after = float('%.2f' % (float(base_price) - float(modify_number)))
                elif modify_type == 'reset':
                    price_after = float('%.2f' % float(modify_number))
                else:
                    continue
            except:
                fail_record.append(obj.seller_sku)
                continue

            try:
                if obj.estimated_fee:
                    lowest_price = float('%.2f' % float(obj.estimated_fee))
                else:
                    lowest_price = 0
            except:
                lowest_price = 0

            if price_after <= lowest_price:
                fail_record.append(obj.seller_sku)
                continue

            # 按店铺合成店铺下的商品sku价格调整字典: {店铺名1:[{sku1:price1, sku2:price2}], 店铺名2:[{sku3:price3, sku4:price4}]}，样例如下
            # {u'AMZ-0086-Jiquan-US/PJ': [{u'3_(}}445': 8.0}, {u'3_(}}444': 9.0}],  u'AMZ-0029-Taihexin-US/PJ': [{u'5591$43496': 12.0}, {u'5591$43495': 12.0}]}
            sku_price = dict()
            sku_price[seller_sku] = price_after
            if shop_name not in shop_sku:
                shop_sku[shop_name] = [sku_price]
            else:
                shop_sku[shop_name].append(sku_price)

            # 更新状态
            t_online_info_amazon_ins.update(deal_action='product_price_modify',
                                            deal_result=None,
                                            deal_result_info=None,
                                            UpdateTime=datetime.datetime.now())

    # shop_sku: {u'AMZ-0086-Jiquan-US/PJ': [{u'3_(}}445': 8.0}, {u'3_(}}444': 9.0}],  u'AMZ-0029-Taihexin-US/PJ': [{u'5591$43496': 12.0}, {u'5591$43495': 12.0}]}
    for key, value in shop_sku.items():
        get_auth_info_ins = GetAuthInfo(connection)
        auth_info = get_auth_info_ins.get_auth_info_by_shop_name(str(key))
        auth_info['IP'] = auth_info['ShopIP']
        auth_info['table_name'] = 't_online_info_amazon'
        auth_info['update_type'] = refresh_type
        auth_info['product_list'] = list()
        auth_info['price_info_dic'] = dict()
        for sku_price_dic in value:
            for sku, price in sku_price_dic.items():
                auth_info['product_list'].append(sku)
                auth_info['price_info_dic'][sku] = price

        # 获取货币单位
        sale_sites = {'US': 'USD', 'DE': 'EUR', 'FR': 'EUR', 'UK': 'GBP', 'AU': 'AUD', 'IN': 'INR'}
        shop_site = key.split('-')[-1].split('/')[0]
        if shop_site in sale_sites.keys():
            currency_type = sale_sites[shop_site]
        else:
            currency_type = 'USD'

        # 获取价格xml
        feed_xml_price_obj = GenerateFeedXml(auth_info)
        feed_xml_price = feed_xml_price_obj.get_price_xml_multi(value, currency_type)
        auth_info['feed_xml'] = feed_xml_price

        # 消息送至mq
        message_to_rabbit_obj = MessageToRabbitMq(auth_info, connection)
        auth_info_price = json.dumps(auth_info)
        message_to_rabbit_obj.put_message(auth_info_price)

    # 提示调价异常记录
    fail_str = ''
    if fail_record:
        for fail in fail_record:
            fail_str = fail_str + fail + ','
        messages.error(request, '以下商品计算调整后价格异常，不予调整：%s' %fail_str[:-1])

    # 不是所有调价都异常给调价中提示
    if len(ids) != len(fail_record):
        messages.success(request, '商品价格调整中')

    if sku_str == '':
        sku_str = ' '
    else:
        sku_str = sku_str[:-1]
    sku_str = urllib.quote(sku_str.decode('gbk', 'replace').encode('utf-8', 'replace'))
    return HttpResponseRedirect('/Project/admin/skuapp/t_online_info_amazon_listing/?SKU=%s' % sku_str)


def show_sku_price_detail(request):
    from skuapp.table.t_amazon_product_price_info import t_amazon_product_price_info
    product_sku = request.GET.get('product_sku', '')
    sku_price_obj = t_amazon_product_price_info.objects.filter(product_sku=product_sku).order_by('-total_price')
    return render(request, 'show_sku_price_detail.html', {'sku_price_obj': sku_price_obj})


def show_sku_remove_detail(request):
    from skuapp.table.t_amazon_product_remove_info import t_amazon_product_remove_info
    product_sku = request.GET.get('product_sku', '')
    sku_remove_obj = t_amazon_product_remove_info.objects.filter(product_sku=product_sku).order_by('-total_price')
    return render(request, 'show_sku_remove_detail.html', {'sku_remove_obj': sku_remove_obj})


def show_sku_pend_detail(request):
    from skuapp.table.t_amazon_product_order_pend_info import t_amazon_product_order_pend_info
    product_sku = request.GET.get('product_sku', '')
    sku_pend_obj = t_amazon_product_order_pend_info.objects.filter(product_sku=product_sku).order_by('-total_price')
    return render(request, 'show_sku_pend_detail.html', {'sku_pend_obj': sku_pend_obj})


def amazon_product_cost_refresh(request):
    from django.db import connection
    from django.http import HttpResponseRedirect
    refresh_type = request.GET.get('refresh_type', '')
    begin_time = request.GET.get('begin_time', '')
    end_time = request.GET.get('end_time', '')
    cursor = connection.cursor()
    return_url = 't_online_info_amazon_listing'
    if refresh_type == 'inventory_cost':
        cursor.execute("select f_amazon_product_inventory_cost()")
        return_url = 't_amazon_product_inventory_cost'
    elif refresh_type == 'remove_cost':
        cursor.execute("select f_amazon_product_remove_cost(%s,%s)",(begin_time, end_time))
        return_url = 't_amazon_product_remove_cost'
    elif refresh_type == 'pend_cost':
        cursor.execute("select f_amazon_product_pend_cost()")
        return_url = 't_amazon_product_order_pend_cost'

    row = cursor.fetchone()
    if row and row[0] == 0:
        messages.success(request, '数据刷新成功')
    else:
        messages.error(request, '数据刷新失败')

    return HttpResponseRedirect('/Project/admin/skuapp/' + return_url)


def show_seller_detail(request):
    from skuapp.table.t_amazon_orders_by_receive_day_info import t_amazon_orders_by_receive_day_info
    seller = request.GET.get('seller', '')
    seller_obj = t_amazon_orders_by_receive_day_info.objects.filter(seller=seller).order_by('-orders_after_14days')
    return render(request, 'show_seller_detail.html', {'seller_obj': seller_obj})
