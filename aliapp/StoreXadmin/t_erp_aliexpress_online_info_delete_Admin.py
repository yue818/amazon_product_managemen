#-*-coding:utf-8-*-
from django.utils.safestring import mark_safe
from django.contrib import messages
from django_redis import get_redis_connection
from django.db import connection
import logging,json,traceback
from datetime import datetime as mydatetime
import xadmin, traceback
from brick.pydata.py_redis.py_SynRedis_tables import py_SynRedis_tables
from brick.pricelist.calculate_price import calculate_price
from brick.pydata.py_redis.py_redis_ali_sku import py_redis_ali_sku
from brick.classredis.classshopsku import classshopsku
from brick.table.t_store_configuration_file import t_store_configuration_file
from aliapp.models import *

"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_erp_aliexpress_online_info_delete_Admin.py
 @time: 2018/7/11 16:27
"""
redis_conn = get_redis_connection(alias='product')
classshopskuobjs = classshopsku(connection, redis_conn)
py_SynRedis_tables_obj = py_SynRedis_tables()
py_redis_ali_sku_obj = py_redis_ali_sku()

t_store_configuration_file_obj = t_store_configuration_file(connection)
classshopsku_obj = classshopsku(connection)
class t_erp_aliexpress_online_info_delete_Admin(object):
    site_left_menu_tree_flag_ali = True
    list_per_page = 20

    def status(self, product_status,revoked):
        if revoked not in ('1',u'1',1):
            if product_status == 'onSelling':#offline
                rt = '<div title="在售" style="float:left;width: 20px;height: 20px;background-color: #66FF66;text-align: center;line-height: 20px;border-radius: 4px">售</div>'
            elif product_status == 'offline':
                rt = '<div title="已下架" style="float:left;width: 20px;height: 20px;background-color: #FFCC33;text-align: center;line-height: 20px;border-radius: 4px">下</div>'
            elif product_status == 'auditing':
                rt = '<div title="审核中" style="float:left;width: 20px;height: 20px;background-color: #FFCC33;text-align: center;line-height: 20px;border-radius: 4px">审</div>'
            elif product_status == 'editingRequired':
                rt = '<div title="审核不通过" style="float:left;width: 20px;height: 20px;background-color: #FF3333;text-align: center;line-height: 20px;border-radius: 4px">拒</div>'
            elif product_status == 'Delete':
                rt = '<div title="被删除" style="float:left;width: 20px;height: 20px;background-color: #FFCC33;text-align: center;line-height: 20px;border-radius: 4px">删</div>'
            else:
                rt = ''
        else:
            rt = '<div title="平台移除" style="float:left;width: 20px;height: 20px;background-color: #FF3333;text-align: center;line-height: 20px;border-radius: 4px">移</div>'
        return rt

    def show_main_pic(self, obj):
        if ';' in obj.image_urls:
            first_img = obj.image_urls.split(';')[0]
        else:
            if obj.image_urls:
                first_img = obj.image_urls
            else:
                first_img = ''
        rt = '<div><img id="image_click_%s" src="%s" style="width: 100px; height: 100px"></div>' % (obj.id, first_img)
        rt += '<div>' + self.status(obj.product_status_type,obj.revoked) + '</div>'
        return mark_safe(rt)

    show_main_pic.short_description = u'<p align="center"style="color:#428bca;">主图</p>'

    def show_child_sku(self, obj):
        rt = u'<table class="table table-condensed">' \
             u'<thead><tr><th></th>' \
             u'<th>商品SKU</th><th>商品状态</th>' \
             u'<th>店铺SKU</th><th>库存量</th><th>价格</th><th>折后价</th><th>利润率(%)</th>' \
             u'</tr>' \
             u'</thead><tbody>'
        sku_infos = json.loads(obj.product_skus)
        sku_info_list = sku_infos.get('aeop_ae_product_sku', '')
        infor = []
        shopsku_info_db = {}
        for sku_info in sku_info_list:
            if sku_info:
                shopsku = sku_info.get('sku_code', '')
                shopsku_info_db[shopsku] = {'sku_price': sku_info.get('sku_price', ''),
                                            'ipm_sku_stock': sku_info.get('ipm_sku_stock', ''),
                                            'sku_discount_price': sku_info.get('sku_discount_price', '')}
                eachinfor = {}
                eachinfor['SKU'] = classshopskuobjs.getSKU(shopsku)
                eachinfor['SKUKEY'] = ['NotInStore', 'GoodsStatus', 'Number', 'ReservationNum', 'CanSaleDay']
                eachinfor['ShopSKU'] = shopsku
                eachinfor['ShopSKUKEY'] = ['Quantity', 'Price', 'Shipping', 'Status']
                infor.append(eachinfor)
        # 这里调取redis数据
        sInfors = py_SynRedis_tables_obj.BatchReadRedis(infor)
        num = 0
        for a, sinfor in enumerate(sInfors):
            shop_sku = sinfor['ShopSKU'].replace('<', '&lt;').replace('>', '&gt;')
            sku_discount_price = shopsku_info_db[shop_sku]['sku_price']
            if shopsku_info_db[shop_sku]['sku_discount_price']:
                sku_discount_price = shopsku_info_db[shop_sku]['sku_discount_price']
            try:
                shopsku_info = py_redis_ali_sku_obj.hgetall_data(shop_sku)
                if len(shopsku_info) == 0:
                    shopsku_info = shopsku_info_db[shop_sku]
                sellingPrice = float(sku_discount_price)
                calculate_price_obj = calculate_price(str(sinfor['SKU']))
                profitrate_info = calculate_price_obj.calculate_profitRate(sellingPrice,
                                                                           platformCountryCode='ALIEXPRESS-RUS',
                                                                           DestinationCountryCode='RUS')
                profitrate = profitrate_info['profitRate']
            except:
                traceback.print_exc()
                profitrate = u'故障'
            profit_id = str(sinfor['SKU']) + str(num)
            num += 1

            goodsstatus = sinfor['SKUKEY'][1]
            if sinfor['SKUKEY'][1] == '1':
                goodsstatus = u'正常'
            if sinfor['SKUKEY'][1] == '2':
                goodsstatus = u'售完下架'
            if sinfor['SKUKEY'][1] == '3':
                goodsstatus = u'临时下架'
            if sinfor['SKUKEY'][1] == '4':
                goodsstatus = u'停售'

            style = ''
            if goodsstatus != u'正常':
                style = 'class ="danger"'  # 非正常为红色
            elif shopsku_info['ipm_sku_stock'] == 0:
                style = 'class ="active"'  # 正常  Disabled 为 灰色
            elif shopsku_info['ipm_sku_stock'] > 0:
                style = 'class ="success"'  # 正常  Disabled 为 绿色

            rt = u'%s <tr %s><td><label><input type="checkbox" name="shopskucheck" id="%s_%s"></label></td>' \
                 u'<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td><a><span id="%s">%s</span></a></td></tr>' % \
                 (rt, style, obj.id, sinfor['ShopSKU'].replace('<', '&lt;').replace('>', '&gt;'),
                  sinfor['SKU'], goodsstatus, sinfor['ShopSKU'].replace('<', '&lt;').replace('>', '&gt;'),
                  shopsku_info['ipm_sku_stock'],
                  shopsku_info_db[shop_sku]['sku_price'], sku_discount_price, profit_id, profitrate,)
            rt = u"%s<script>$('#%s').on('click',function()" \
                 u"{layer.open({type:2,skin:'layui-layer-lan',title:'算价表'," \
                 u"fix:false,shadeClose: true,maxmin:true,area:['1300px','900px']," \
                 u"content:'/price_list/?SKU=%s&sellingPrice=%s&platformCountryCode=%s" \
                 u"&DestinationCountryCode=%s&category=%s',});});</script>" % (
                     rt, profit_id, sinfor['SKU'], sellingPrice, 'ALIEXPRESS-RUS', 'RUS', 'non_ornament')
        rt += '</tbody></table>'
        edit_flag = 0
        if obj.online_status:
            operation_type = obj.online_status.split('_')[1]
            if operation_type == 'ing':
                edit_flag = 1
        if edit_flag == 0:
            rt = u'%s<a id="link_id_%s">编辑变体</a>' % (rt, obj.id)
            rt = u"%s<script>$('#link_id_%s').on('click',function()" \
                 u"{var index = layer.open({type:2,skin:'layui-layer-lan',title:'全部变体信息'," \
                 u"fix:false,shadeClose: true,maxmin:true,area:['1000px','800px'],btn: ['关闭页面']," \
                 u"content:'/t_erp_aliexpress_online_info/ShopSKU/?product_id=%s',end:function (){location.reload();}});" \
                 u"});</script>" % (rt, obj.id, obj.product_id)
        return mark_safe(rt)

    show_child_sku.short_description = mark_safe(u'<p align="center"style="color:#428bca;">变体详细信息</p>')

    def show_subject(self, obj):
        sku_infos = json.loads(obj.product_skus)
        sku_info_list = sku_infos.get('aeop_ae_product_sku', '')
        shopsku = sku_info_list[0].get('sku_code', '')
        submitter = classshopsku_obj.getPublished(shopsku)  # 按照店铺SKU来抓取刊登人
        if submitter is None:
            submitter = classshopsku_obj.getPublished(shopsku.split('\\')[0].split('*')[0])  # 按照店铺SKU来抓取刊登人
        seller = t_store_configuration_file_obj.getsellerbyshopcode(obj.shopName)
        rt = u'<a href="https://www.aliexpress.com/item/-/%s.html" title="商品售卖界面" target="_blank">%s</a>' % (
        obj.product_id, obj.subject)
        rt += u'<br/>产品ID：%s<br/>卖家简称：%s' % (obj.product_id, obj.shopName + '-' + obj.owner_member_id)
        rt += u'<br/>店长/销售员：%s<br/>刊登人：%s' % (seller, submitter)
        action_flags = {'enable': u'上架', 'disable': u'下架', 'enableSKU': u'SKU上架',
                        'disableSKU': u'SKU下架', 'editStock': u'库存修改', 'editPrice': u'价格修改'}
        if obj.online_status:
            online_status = obj.online_status.split('_')[0]
            action_end = ''
            styles = ''
            if 'ing' in obj.online_status:
                styles = 'color:#FFCC33;'
                action_end = u'中...'
            if 'success' in obj.online_status:
                styles = 'color:#00BB00;'
                action_end = u'成功'
            action_flag = action_flags.get(online_status) + action_end
            rt += u'<br/><p style="%s">%s</p>' % (styles, action_flag)
        if obj.is_syn:
            if obj.is_syn == 0:
                pass
            else:
                if obj.is_syn == 1:
                    styles = 'color:#FFCC33;'
                    action_end = u'同步中...'
                elif obj.is_syn == 200:
                    styles = 'color:#00BB00;'
                    action_end = u'同步成功'
                else:
                    styles = 'color:red;'
                    action_end = u'同步失败'
                rt += u'<p style="%s">%s</p>' % (styles, action_end)
        rt += u'<br/>平台发布时间：%s<br/>平台最近更新时间：%s' % (obj.gmt_create, obj.gmt_modified)
        rt += u'<br/>商品同步时间：%s' % (obj.updatetime)
        rt += u'<br/>产品分类ID：%s' % (obj.category_id)
        return mark_safe(rt)

    show_subject.short_description = mark_safe(u'<p align="center"style="color:#428bca;">产品标题</p>')

    def show_freight_template_name(self, obj):
        t_erp_aliexpress_freight_template_objs = t_erp_aliexpress_freight_template.objects.filter(
            template_id=obj.freight_template_id)
        rt = ''
        if t_erp_aliexpress_freight_template_objs.exists():
            rt = t_erp_aliexpress_freight_template_objs[0].template_name
        return mark_safe(rt)

    show_freight_template_name.short_description = mark_safe(u'<p align="center"style="color:#428bca;">运费模板</p>')
    list_display = ('show_main_pic', 'show_subject', 'Sales7Days', 'show_child_sku', 'show_freight_template_name', 'remark', 'gmt_create',)
    list_editable = ('remark')

    def get_list_queryset(self,):
        """显示可显示的，自己本人的"""
        from skuapp.table.t_sys_staff_auth import t_sys_staff_auth
        flag = 0
        try:
            flag = t_sys_staff_auth.objects.filter(StaffID=self.request.user.username,urltable="t_erp_aliexpress_online_info").count()
        except:
            pass
        request = self.request
        qs = super(t_erp_aliexpress_online_info_delete_Admin, self).get_list_queryset()
        t_erp_aliexpress_shop_info_obj = t_erp_aliexpress_shop_info.objects.filter(shop_status='online').values(
            'seller_zh', 'accountName')
        if self.request.user.is_superuser or flag != 0:
            pass
        else:
            print self.request.user.first_name
            t_erp_aliexpress_shop_info_obj = t_erp_aliexpress_shop_info_obj.filter(
                seller_zh=self.request.user.first_name)
            accountNames = t_erp_aliexpress_shop_info_obj.values('accountName')
            buttonlist = []
            for obj in accountNames:
                buttonlist.append(obj['accountName'])
            buttonlist.sort()
            qs = qs.filter(owner_member_id__in=buttonlist)
        return qs


