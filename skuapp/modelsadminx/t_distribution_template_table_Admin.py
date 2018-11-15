# -*- coding: utf-8 -*-
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from skuapp.table.t_online_info import t_online_info
from skuapp.table.t_config_online_amazon import t_config_online_amazon
from skuapp.table.t_store_configuration_file import t_store_configuration_file
from skuapp.table.t_ShopName_ParentSKU import t_ShopName_ParentSKU
from skuapp.table.t_distribution_product_to_store import t_distribution_product_to_store
from skuapp.table.t_shopsku_information_binding import t_shopsku_information_binding
from pyapp.models import b_goodsskulinkshop as py_b_goodsskulinkshop
from pyapp.models import b_goodssku as py_b_goodssku
from datetime import datetime
import datetime as datime
import logging
from django.contrib import messages
import re
import requests
import random
import string

from skuapp.table.t_online_info_wish import t_online_info_wish
import csv
from skuapp.table.t_api_schedule_ing import t_api_schedule_ing
from django.utils.safestring import mark_safe
from skuapp.modelsadminx.t_online_info_wish_Admin import t_online_info_wish_Admin
from skuapp.table.t_sys_param import t_sys_param
from pyapp.models import b_goods as py_b_goods

from django.db.models import Q  
from  Project.settings import SQLSERVERDB
logger = logging.getLogger('sourceDns.webdns.views')
rate = t_sys_param.objects.filter(Type=40,Seq=1)[0].V  # 美元兑人民币汇率
from skuapp.table.t_tort_aliexpress import t_tort_aliexpress
import os
import oss2
from Project.settings import MEDIA_ROOT
from .t_product_Admin import *
import traceback
from skuapp.table.t_upload_shopname import t_upload_shopname
from skuapp.table.t_distribution_template_table_temp import t_distribution_template_table_temp



class t_distribution_template_table_Admin(object):
    select_checkbox_flag = True

    def show_picture(self,obj) :
        url = obj.Image.replace('-original','-medium')
        rt =  '<img src="%s"  width="120" height="120"  alt = "%s"  title="%s"  />  '%(url,url,url)
        return mark_safe(rt)
    show_picture.short_description = u'图片'

    def show_submit(self,obj) :
        if obj.SubStatus == '1':
            SubStatus = u'未铺货'
        else:
            SubStatus = u'已铺货'

        if obj.Type == '1':
            Type = u'全部铺货'
        elif obj.Type == '2':
            Type = u'更改铺货'
        elif obj.Type == '3':
            Type = u'原样铺货'
        elif obj.Type == '4':
            Type = u'已有数据铺货'
        else:
            Type = u'未选择'
        rt = u'提交人:%s<br>提交时间:<br>%s<br>提交状态:%s<br>铺货类型:%s'%(obj.Submitter,obj.SubTime,SubStatus,Type)
        return mark_safe(rt)
    show_submit.short_description = u'提交人/时间/状态'

    def show_shopName_seller(self, obj):
        rt = ''
        rt = u'%s卖家简称:<br>%s<br>店长/销售员:%s<br>产品ID:<br>%s' % (rt, obj.ShopName, obj.Seller, obj.ProductID)
        return mark_safe(rt)
    show_shopName_seller.short_description = u'卖家简称/店长/销售员/产品ID'

    def show_SKU_list(self,obj) :
        rt='<table   style="text-align:center;" border="1" cellpadding="3" cellspacing="1" bgcolor="#c1c1c1">' \
           '<tr bgcolor="#C00"><th style="text-align:center">子SKU</th><th style="text-align:center">子SKU状态</th>' \
           '<th style="text-align:center">店铺SKU</th><th style="text-align:center">库存量</th>' \
           '<th style="text-align:center">参考价格</th><th style="text-align:center">原价格</th><th style="text-align:center">标签价</th>' \
           '<th style="text-align:center">运费</th><th style="text-align:center">运输时间</th>' \
           '<th style="text-align:center">上下架</th></tr>'
        if t_distribution_template_table_temp.objects.filter(NID=obj.id).exists():
            shopName = t_distribution_template_table_temp.objects.filter(NID=obj.id)[0].ShopName
        else:
            shopName = ''
        store_temp_objs = t_distribution_template_table_temp.objects.values('SKU','ShopSKU','Quantity','Price','Status','msrp','ShippingTime','Shipping','oldPrice').filter(NID=obj.id,ShopName=shopName)
        i = 0
        for store_temp_obj in store_temp_objs:
            if i < 5:
                st = py_b_goods.objects.filter(SKU=store_temp_obj['SKU'])
                if st.exists():
                    st = st[0].GoodsStatus
                else:
                    st = u'未知'
                if store_temp_obj['Status'] =='Enabled':
                    tt = '上架'
                else:
                    tt = '下架'
                rt = '%s <tr bgcolor="#FFFFFF"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr> '%\
                     (rt,store_temp_obj['SKU'],st,store_temp_obj['ShopSKU'],store_temp_obj['Quantity'],store_temp_obj['Price'],store_temp_obj['oldPrice'],
                      store_temp_obj['msrp'],store_temp_obj['Shipping'],store_temp_obj['ShippingTime'],tt)
                i = i + 1
        rt = '%s<tr><td><a id="link_id_%s">点击修改</a></td></tr>'%(rt,obj.id)
        rt = "%s</table><script>$('#link_id_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'查看全部',fix:false,shadeClose: true,maxmin:true,area:['1200px','700px'],content:'/wish_change/?abc=%s',btn:['关闭页面'],end:function(){location.reload();}});});</script>"%(rt,obj.id,obj.id)
        return mark_safe(rt)
    show_SKU_list.short_description = mark_safe('<p align="center"> 子SKU</p>')

    def show_csvSKU_status(self,obj):
        csvsku = obj.csvSKU
        rt = '<div class="box" style="width: 80px;height: 30px;text-align: center;line-height: 30px;border-radius: 4px">%s</div>' % csvsku
        tort_objs = t_tort_aliexpress.objects.filter(MainSKU=csvsku)
        if tort_objs.exists():
            tortSiteList = []
            for tort_obj in tort_objs:
                tort_site = tort_obj.Site
                tortSiteList.append(tort_site)
            if 'Wish' in tortSiteList:
                site = 'Wish仿品'
                rt = '%s<br><div class="box" style="width: 80px;height: 30px;background-color: #FF3333;text-align: center;line-height: 30px;border-radius: 4px">%s</div>'%(rt,site)
            else:
                site = '其他仿品'
                rt = '%s<br><div class="box" style="width: 80px;height: 30px;background-color: #FFCC33;text-align: center;line-height: 30px;border-radius: 4px">%s</div>'%(rt,site)
        else:
            site = '非仿品'
            rt = '%s<br><div class="box" style="width: 80px;height: 30px;background-color: #66FF66;text-align: center;line-height: 30px;border-radius: 4px">%s</div>' % (rt, site)
        return mark_safe(rt)
    show_csvSKU_status.short_description = u'SKU及侵权状态'

    def show_csvShop1(self,obj):
        shopList = obj.csvShop1.split(',')
        rt = ''
        for i in range(len(shopList)):
            if (i + 1) % 10 == 0:
                rt = rt + shopList[i] + '<br>'
            else:
                rt = rt + shopList[i] + ','
        up = u"<a id='show_update_shopname_id_%s'>点击修改</a><script>$('#show_update_shopname_id_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'请修改铺货目标店铺',fix:false,shadeClose: true,maxmin:true,area:['900px','500px'],content:'/to_wish_store_distribution/?id=%s',btn:['关闭页面'],end:function(){location.reload();}});});</script>"%(obj.id,obj.id,obj.id)
        return mark_safe(u'%s<br><br><br>%s'%(rt[:-1],up))
    show_csvShop1.short_description = u'csv内店铺'

    def show_id(self,obj):
        if obj.SubStatus == '1':
            if obj.Type == None:
                rt = '<font color="#FF3333">%s</font>'%(obj.id)
            else:
                rt = '<font color="#FFE007">%s</font>' % (obj.id)
        else:
            rt = '<font color="#00BB00">%s</font>'%(obj.id)
        return mark_safe(rt)
    show_id.short_description = u'ID'

    list_display = ('show_id','show_picture','show_csvSKU_status','show_csvShop1','show_submit','show_shopName_seller',
                    'Title','Description','Tags','show_SKU_list','Remarks',)
    list_filter = ('id','csvSKU','Orders7Days','ProductID','Submitter','SubTime','SubStatus','Type')
    search_fields = ('id','csvSKU','ProductID','Submitter','SubStatus',)

    