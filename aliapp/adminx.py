# -*- coding: utf-8 -*-
from app_djcelery.tasks import refresh_online_info_by_ali_api,enable_products_by_ali_api,disable_products_by_ali_api,syn_products_by_ali_api
from app_djcelery.tasks import edit_productSKU_stock_by_ali_api,edit_productSKU_price_by_ali_api,edit_product_by_ali_api,upload_product_by_ali_api
from django.utils.safestring import mark_safe
from django.contrib import messages
from django_redis import get_redis_connection
from django.db import connection
import logging,json,traceback
from datetime import datetime as mydatetime
import xadmin, traceback
from aliapp.plugin.refresh_online_info_Plugin import *
from brick.classredis.classshopsku import classshopsku
from xadmin.views import ListAdminView,BaseAdminView,ModelFormAdminView
from datetime import datetime as timetime
logger = logging.getLogger('sourceDns.webdns.views')
from aliapp.models import *
from urllib import urlencode
from aliapp.plugin.site_left_menu_tree_Plugin_ali import *
from brick.pydata.py_redis.py_SynRedis_tables import py_SynRedis_tables
from brick.pricelist.calculate_price import calculate_price
from aliapp.StoreXadmin.t_erp_aliexpress_product_announcing_Admin import *
from aliapp.StoreXadmin.t_erp_aliexpress_product_upload_result_Admin import *
from aliapp.StoreXadmin.t_erp_aliexpress_product_draft_box_Admin import *
from aliapp.StoreXadmin.t_erp_aliexpress_product_recycle_bin_Admin import *
from aliapp.StoreXadmin.t_erp_aliexpress_product_released_Admin import *
from aliapp.StoreXadmin.t_erp_aliexpress_action_log_Admin import *
from aliapp.StoreXadmin.t_erp_aliexpress_shop_info_Admin import *
from aliapp.StoreXadmin.t_erp_aliexpress_online_info_delete_Admin import *
from aliapp.StoreXadmin.t_erp_aliexpress_shop_link_daily_Admin import *
from aliapp.StoreXadmin.t_erp_aliexpress_activation_rate_Admin import *
from aliapp.StoreXadmin.t_erp_aliexpress_activation_rate_overview_Admin import *
from aliapp.StoreXadmin.v_erp_aliexpress_mutation_coefficient_Admin import v_erp_aliexpress_mutation_coefficient_Admin
from aliapp.plugin.mutation_coefficient_plugin import mutation_coefficient_plugin
from aliapp.models import v_erp_aliexpress_mutation_coefficient
from brick.pydata.py_redis.py_redis_ali_sku import py_redis_ali_sku
from brick.classredis.classshopsku import classshopsku
from aliapp.plugin.activation_rate_plugin import activation_rate_plugin
from brick.table.t_store_configuration_file import t_store_configuration_file
from django.db.models import Q
redis_conn = get_redis_connection(alias='product')
classshopskuobjs = classshopsku(connection, redis_conn)
py_SynRedis_tables_obj = py_SynRedis_tables()
py_redis_ali_sku_obj = py_redis_ali_sku()

t_store_configuration_file_obj = t_store_configuration_file(connection)
classshopsku_obj = classshopsku(connection)


import inspect

def check_permission_legality(self):
    """
    :param self:
    :return:
    """
    funcName = inspect.stack()[1][3]
    permname = '{}.Can_{}_{}'.format(self.model._meta.app_label, self.model._meta.model_name, funcName)
    if self.request.user.is_superuser or self.request.user.has_perm(permname):
        return True
    return False




class t_erp_aliexpress_online_info_Admin(object):
    refresh_online_info_flag = True
    site_left_menu_tree_flag_ali = True
    list_per_page = 20

    search_box_flag = True
    shopobjs=t_erp_aliexpress_shop_info.objects.values_list('accountName','cata_zh')
    shop_cata_dict={obj[0]:obj[1] for obj in shopobjs}

    def status(self, product_status,revoked,product_id,product_status_type):
        objs = t_erp_aliexpress_product_sku.objects.filter(product_id=product_id).values('Infringing','InfringingSite')
        tmp={-1,}
        for obj in objs:
            if obj['Infringing'] in ('1', 1, u'1'):  #侵权
                tmp.add(1)
            elif obj['Infringing'] in ('0',0,u'0'):  #未侵权
                if obj['InfringingSite']:   #其他平台侵权
                    tmp.add(0)
        if revoked not in ('1',u'1',1) and product_status_type not in ('service-delete',u'service-delete'):
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
        if max(tmp)==1:
            rt=rt+'<div title="速卖通禁用" style="float:left;width: 20px;height: 20px;background-color: #FF3333;text-align: center;line-height: 20px;border-radius: 4px">A</div>'
        elif max(tmp)==0:
            rt = rt + '<div title="其他平台禁用" style="float:left;width: 20px;height: 20px;background-color: #FFCC33;text-align: center;line-height: 20px;border-radius: 4px">O</div>'
        return rt


    def show_main_pic(self,obj):
        if ';' in obj.image_urls:
            first_img = obj.image_urls.split(';')[0]
        else:
            if obj.image_urls:
                first_img = obj.image_urls
            else:
                first_img = ''
        rt = '<div><img id="image_click_%s" src="%s" style="width: 100px; height: 100px"></div>' % (obj.id, first_img)
        rt += '<div>' + self.status(obj.product_status_type,obj.revoked,obj.product_id,obj.product_status_type) + '</div>'
        return mark_safe(rt)
    show_main_pic.short_description = u'<p align="center"style="color:#428bca;">主图</p>'


    def deal_with_obj(self, obj):

        rt = ''
        if check_permission_legality(self):
            update = u"<a id='edit_update_%s' title='编辑该listing的其他信息'>编辑</a><br>" \
                     u"<script>$('#edit_update_%s').on('click',function(){layer.open(" \
                     u"{type:2,skin:'layui-layer-lan',title:'编辑-更新',fix:false,shadeClose: " \
                     u"true,maxmin:true,area:['1400px','800px'],btn: ['关闭页面']," \
                     u"content:'/edit_update_by_ali_api_productid/?%s',});});" \
                     u"</script>" % (
                     obj.id, obj.id, urlencode({'productid': obj.product_id, 'shopname': obj.owner_member_id}))
            syn = u'<a onclick= "static_refresh(\'%s\')" title="同步在线数据">同步</a><br>' % (
                u'/syndata_by_ali_api/?%s' % (urlencode({'syn': obj.id, 'shopname': obj.shopName,
                                                         'accountName': obj.owner_member_id,
                                                         'product_id': obj.product_id})))

            up = u'<a onclick="enable_id(\'%s\',\'%s\',\'%s\',\'%s\')"title="对整个listing做上架操作">上架</a>' % (
                obj.id, obj.shopName, obj.owner_member_id, obj.product_id)
            down = u'<br><a onclick="disable_id(\'%s\',\'%s\',\'%s\',\'%s\')"title="对整个listing做下架操作">下架</a>' % (
                obj.id, obj.shopName, obj.owner_member_id, obj.product_id)
            # delete = u'<br><a onclick="delete_id(\'%s\',\'%s\',\'%s\',\'%s\')"title="标记整个listing已删除操作">删除</a>' % (
            #     obj.id, obj.shopName, obj.owner_member_id, obj.product_id)
            if obj.online_status:
                operation_type = obj.online_status.split('_')[1]
                if operation_type == 'ing':
                    update = u'<p>编辑</p>'
                    up = u'<p>上架</p>'
                    down = u'<p>下架</p>'

            rt = syn + up + down
        # rt = syn + update + up + down + delete
        return mark_safe(rt)

    deal_with_obj.short_description = mark_safe(u'<p style="width:40px;color:#428bca;" align="center">操作</p>')

    def show_child_sku(self,obj):
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
                shopsku_info_db[shopsku] = {'sku_price': sku_info.get('sku_price', ''), 'ipm_sku_stock': sku_info.get('ipm_sku_stock', ''),
                                            'sku_discount_price': sku_info.get('sku_discount_price', '')}
                eachinfor = {}
                SKU=classshopskuobjs.getSKU(shopsku)
                if SKU is None:
                    eachinfor['SKU'] = None
                else:
                    eachinfor['SKU'] = SKU.split('*')[0]
                eachinfor['SKUKEY'] = ['NotInStore', 'GoodsStatus', 'Number', 'ReservationNum', 'CanSaleDay']
                eachinfor['ShopSKU'] = shopsku
                eachinfor['ShopSKUKEY'] = ['Quantity', 'Price', 'Shipping', 'Status']
                infor.append(eachinfor)
        # 这里调取redis数据
        sInfors = py_SynRedis_tables_obj.BatchReadRedis(infor)
        num = 0
        request=self.request
        stopsales=request.GET.get('StopSales')
        skustock_isempty=request.GET.get('skustock_isempty')
        if stopsales and stopsales.startswith('1-') and skustock_isempty=='0':
            flag=True
        else:
            flag=False
        for a, sinfor in enumerate(sInfors):
            shop_sku = sinfor['ShopSKU'].replace('<', '&lt;').replace('>', '&gt;')
            sku_discount_price = shopsku_info_db[shop_sku]['sku_price']
            if shopsku_info_db[shop_sku]['sku_discount_price']:
                sku_discount_price = shopsku_info_db[shop_sku]['sku_discount_price']
            try:
                # shopsku_info = py_redis_ali_sku_obj.hgetall_data(shop_sku)
                # if len(shopsku_info) == 0:
                shopsku_info = shopsku_info_db[shop_sku]
                sellingPrice = float(sku_discount_price)
                calculate_price_obj = calculate_price(str(sinfor['SKU']))
                profitrate_info = calculate_price_obj.calculate_profitRate(sellingPrice, platformCountryCode='ALIEXPRESS-RUS',
                                                                           DestinationCountryCode='US',category='non_ornament')
                profitrate = profitrate_info['profitRate']
            except:
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

            rt = u'%s <tr %s><td><label><input type="checkbox" name="shopskucheck" id="%s_ywp_%s"></label></td>' \
                 u'<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td><a><span id="%s">%s</span></a></td></tr>' % \
                 (rt, style, obj.id, sinfor['ShopSKU'].replace('<', '&lt;').replace('>', '&gt;'),
                  sinfor['SKU'], goodsstatus,sinfor['ShopSKU'].replace('<', '&lt;').replace('>', '&gt;'),
                  shopsku_info['ipm_sku_stock'],
                  shopsku_info_db[shop_sku]['sku_price'], sku_discount_price, profit_id, profitrate,)
            rt = u"%s<script>$('#%s').on('click',function()" \
                 u"{layer.open({type:2,skin:'layui-layer-lan',title:'算价表'," \
                 u"fix:false,shadeClose: true,maxmin:true,area:['1300px','900px']," \
                 u"content:'/price_list/?SKU=%s&sellingPrice=%s&platformCountryCode=%s" \
                 u"&DestinationCountryCode=%s&category=%s',});});</script>" % (
                 rt, profit_id, sinfor['SKU'], sellingPrice, 'ALIEXPRESS-RUS', 'US', 'non_ornament')
        rt += '</tbody></table>'
        edit_flag = 0
        if obj.online_status:
            operation_type = obj.online_status.split('_')[1]
            if operation_type == 'ing':
                edit_flag = 1
        if edit_flag == 0:
            if check_permission_legality(self):
                rt = u'%s<a id="link_id_%s">编辑变体</a>' % (rt, obj.id)
                rt = u"%s<script>$('#link_id_%s').on('click',function()" \
                     u"{var index = layer.open({type:2,skin:'layui-layer-lan',title:'全部变体信息'," \
                     u"fix:false,shadeClose: true,maxmin:true,area:['1000px','800px'],btn: ['关闭页面']," \
                     u"content:'/t_erp_aliexpress_online_info/ShopSKU/?product_id=%s'});" \
                     u"});</script>" % (rt, obj.id, obj.product_id)
        return mark_safe(rt)

    show_child_sku.short_description = mark_safe(u'<p align="center"style="color:#428bca;">变体详细信息</p>')

    def show_subject(self,obj):
        sku_infos = json.loads(obj.product_skus)
        # sku_info_list = sku_infos.get('aeop_ae_product_sku', '')
        #shopsku = sku_info_list[0].get('sku_code', '')
        submitter=obj.submitter
        #submitter = classshopsku_obj.getPublished(shopsku)  # 按照店铺SKU来抓取刊登人
        # if submitter is None:
        #     submitter = classshopsku_obj.getPublished(shopsku.split('\\')[0].split('*')[0])  # 按照店铺SKU来抓取刊登人
        seller = t_store_configuration_file_obj.getsellerbyshopcode(obj.shopName)
        rt = u'<a href="https://www.aliexpress.com/item/-/%s.html" title="商品售卖界面" target="_blank">%s</a>'%(obj.product_id,obj.subject)
        rt += u'<br/>产品ID：%s<br/>卖家简称：%s'%(obj.product_id,obj.shopName+ '-' +obj.owner_member_id)
        rt += u'<br/>店长/销售员：%s<br/>刊登人：%s'%(seller, submitter)
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
        rt += u'<br/>店铺品类:{}'.format(self.shop_cata_dict.get(obj.owner_member_id))
        return mark_safe(rt)

    show_subject.short_description = mark_safe(u'<p align="center"style="color:#428bca;">产品标题</p>')

    def show_product_status(self,obj):
        status_flags = {'onSelling': u'在售', 'offline': u'已下架', 'auditing': u'审核中','editingRequired': u'审核不通过'}
        rt = status_flags[obj.product_status_type]
        return mark_safe(rt)
    show_product_status.short_description = mark_safe(u'<p align="center"style="color:#428bca;">产品状态</p>')

    def show_freight_template_name(self, obj):
        t_erp_aliexpress_freight_template_objs = t_erp_aliexpress_freight_template.objects.filter(template_id=obj.freight_template_id)
        rt = ''
        if t_erp_aliexpress_freight_template_objs.exists():
            rt = t_erp_aliexpress_freight_template_objs[0].template_name
        return mark_safe(rt)
    show_freight_template_name.short_description = mark_safe(u'<p align="center"style="color:#428bca;">运费模板</p>')
    list_display = ('show_main_pic', 'show_subject', 'Sales7Days','Viewed7Days','Exposed7Days','show_child_sku','show_freight_template_name', 'gmt_create',  'deal_with_obj',)
    # list_editable = ('Remarks')
    list_display_links = ('',)

    actions = ['syn_data_by_ali_api_batch', 'enable_data_by_ali_api_batch', 'disable_data_by_ali_api_batch',]



    def deal_with_product_batch(self,request, shopDict, operation):
        user = request.user.first_name
        sResult = {}
        try:
            for each_shop,productIds in shopDict.items():
                new_productids = ','.join(productIds)
                t_erp_aliexpress_action_temp_obj = t_erp_aliexpress_action_temp()
                t_erp_aliexpress_action_temp_obj.shopName = ''
                t_erp_aliexpress_action_temp_obj.accountName = each_shop
                t_erp_aliexpress_action_temp_obj.action_type = operation
                t_erp_aliexpress_action_temp_obj.action_param = json.dumps({"product_id": new_productids})
                t_erp_aliexpress_action_temp_obj.action_result = ''
                t_erp_aliexpress_action_temp_obj.action_time = mydatetime.now()
                t_erp_aliexpress_action_temp_obj.action_user = user
                t_erp_aliexpress_action_temp_obj.table_name = 't_erp_aliexpress_online_info'
                t_erp_aliexpress_action_temp_obj.field_name = ''
                t_erp_aliexpress_action_temp_obj.old_value = ''
                t_erp_aliexpress_action_temp_obj.action_id = 0
                t_erp_aliexpress_action_temp_obj.save()
                id = t_erp_aliexpress_action_temp_obj.id
                online_status = operation + '_ing'
                if operation == 'syn':
                    for productid in productIds:
                        t_erp_aliexpress_online_info.objects.filter(product_id=productid).update(is_syn=1)
                    syn_products_by_ali_api.delay(id)
                else:
                    for productid in productIds:
                        t_erp_aliexpress_online_info.objects.filter(product_id=productid).update(online_status=online_status)
                    if operation == 'enable':
                        enable_products_by_ali_api.delay(id)
                    else:
                        disable_products_by_ali_api.delay(id)

            # storeResult = ''
            sResult['resultCode'] = '1'
            sResult['messages'] = u'努力同步中...'
        except Exception, e:
            sResult['resultCode'] = -1
            sResult['messages'] = '%s:%s' % (Exception, e)
        return sResult

    def syn_data_by_ali_api_batch(self, request, queryset):
        shopDict = {}
        for obj in queryset:
            if obj:
                if shopDict.has_key(obj.owner_member_id):
                    shopDict_value = shopDict.get(obj.owner_member_id)
                    shopDict_value.append(str(obj.product_id))
                    shopDict[obj.owner_member_id] = shopDict_value
                else:
                    shopDict[obj.owner_member_id] = [str(obj.product_id),]
        if shopDict:
            sResult = self.deal_with_product_batch(request,shopDict, 'syn')
            if sResult['resultCode'] == -1:
                messages.error(request, u'商品同步失败，请联系相关IT人员%s'%sResult['messages'])
        else:
            messages.error(request, u'请先选中需要同步的商品')
    syn_data_by_ali_api_batch.short_description = u'同步商品信息'

    def enable_data_by_ali_api_batch(self, request, queryset):
        shopDict = {}
        for obj in queryset:
            if obj:
                if obj.online_status:
                    operation_type = obj.online_status.split('_')[1]
                    if operation_type == 'ing':
                        messages.error(request,u'%s API调用中，请稍后'%obj.product_id)
                        continue
                if shopDict.has_key(obj.owner_member_id):
                    shopDict_value = shopDict.get(obj.owner_member_id)
                    shopDict_value.append(str(obj.product_id))
                    shopDict[obj.owner_member_id] = shopDict_value
                else:
                    shopDict[obj.owner_member_id] = [str(obj.product_id),]
        if shopDict:
            sResult = self.deal_with_product_batch(request,shopDict, 'enable')
            if sResult['resultCode'] == -1:
                messages.error(request, u'商品上架失败，请联系相关IT人员')
        else:
            messages.error(request, u'请先选中需要上架的商品')

    enable_data_by_ali_api_batch.short_description = u'上架'

    def disable_data_by_ali_api_batch(self, request, queryset):
        shopDict = {}
        for obj in queryset:
            if obj:
                if obj.online_status:
                    operation_type = obj.online_status.split('_')[1]
                    if operation_type == 'ing':
                        messages.error(request,u'%s API调用中，请稍后'%obj.product_id)
                        continue
                if shopDict.has_key(obj.owner_member_id):
                    shopDict_value = shopDict.get(obj.owner_member_id)
                    shopDict_value.append(str(obj.product_id))
                    shopDict[obj.owner_member_id] = shopDict_value
                else:
                    shopDict[obj.owner_member_id] = [str(obj.product_id),]
        if shopDict:
            sResult = self.deal_with_product_batch(request,shopDict, 'disable')
            if sResult['resultCode'] == -1:
                messages.error(request, u'商品下架失败，请联系相关IT人员')
        else:
            messages.error(request, u'请先选中需要下架的商品')

    disable_data_by_ali_api_batch.short_description = u'下架'

    #
    # def tort_info(self,obj):
    #     objs=t_erp_aliexpress_product_sku.objects.filter(product_id=obj.product_id).values('MainSKU','InfringingSite').distinct()
    #     tmp=u''
    #     for oj in objs:
    #         tmp+=u'<tr><td>{}</td><td>{}</td></tr>'.format(oj[u'MainSKU'],oj[u'InfringingSite'] if oj[u'InfringingSite'] else u'未侵权')
    #     rt=u'<table border="1"><tr><th>主SKU</th><th>禁用平台</th></tr>{}</table>'.format(tmp)
    #     return mark_safe(rt)
    #
    # tort_info.short_description = mark_safe(u'<p align="center"style="color:#428bca;">侵权信息</p>')
    #
    #
    #



    def get_list_queryset(self,):
        """显示可显示的，自己本人的"""
        from skuapp.table.t_sys_staff_auth import t_sys_staff_auth
        flag = 0
        try:
            flag = t_sys_staff_auth.objects.filter(StaffID=self.request.user.username,urltable="t_erp_aliexpress_online_info").count()
        except:
            pass
        request = self.request
        qs = super(t_erp_aliexpress_online_info_Admin, self).get_list_queryset()


        product_id = request.GET.get('product_id', '')
        shopSKU = request.GET.get('shopSKU', '')
        SKU = request.GET.get('SKU', '')
        MainSKU = request.GET.get('MainSKU', '').split(',')
        Revoked=request.GET.get('revoked','')
        skustock_isempty=request.GET.get('skustock_isempty','')
        skustatus = request.GET.get('skustatus','')  # 商品SKU状态
        tortinfo=request.GET.get('tortinfo','')
        shopcategory=request.GET.get('shopcategory','')
        shoplist=[]
        if shopcategory:
            cata_switch={u'家居家具': u'家居&家具',
             u'运动鞋服包户外配附': u'运动鞋服包/户外配附',
             u'母婴玩具': u'母婴&玩具',
             u'电脑网络办公文教': u'电脑网络&办公文教',
             u'家装灯具工具': u'家装&灯具&工具'}
            shopcategory=cata_switch.get(shopcategory,shopcategory)
            print(shopcategory)

            for shop,cata_zh in self.shop_cata_dict.items():
                if cata_zh==shopcategory:
                    shoplist.append(shop)



        if tortinfo:
            if tortinfo=='-1':
                qs=qs.filter(Infringement=0)
            elif tortinfo=='1':
                qs=qs.filter(Infringement=1)
            else:
                objs = t_erp_aliexpress_product_sku.objects.filter(Infringing=0,InfringingSite__isnull=False).values('product_id')
                tort_product = {x['product_id'] for x in objs}
                qs = qs.filter(product_id__in=tort_product)
        goodsstatus = []
        if skustatus == '1':
            goodsstatus = [1000, 1100, 1010, 1001, 1110, 1101, 1011, 1111]  # 正常
        if skustatus == '2':
            goodsstatus = [100, 1100, 110, 101, 1110, 1101, 111, 1111]  # 售完下架
        if skustatus == '3':
            goodsstatus = [10, 1010, 110, 11, 1011, 1110, 111, 1111]  # 临时下架
        if skustatus == '4':
            goodsstatus = [1, 1001, 101, 11, 1101, 111, 1011, 1111]  # 停售

        flag=False
        if skustatus and skustock_isempty:
            flag=True
            tmp={'1':'skustatus1_stock__in','2':'skustatus2_stock__in','3':'skustatus3_stock__in','4':'skustatus4_stock__in'}

            if skustock_isempty in ('0',u'0',0):
                qs=qs.filter(**{tmp[skustatus]:[1,10]})
            elif skustock_isempty in ('1',u'1',1):
                qs = qs.filter(**{tmp[skustatus]: [0,10]})


        if MainSKU !=['',]:
            mutilSKU=t_erp_aliexpress_product_sku.objects.filter(mutilSKUFlag=1).values('MainSKU')
            for mutilsku in mutilSKU:
                mainsku_list=mutilsku.get('MainSKU','').split("+")
                for mainsku in mainsku_list:
                    if mainsku in MainSKU:
                        MainSKU.append(mutilsku.get('MainSKU'))
            if len(MainSKU) > 300:
                MainSKU = MainSKU[:300]
                messages.error(request, u'MainSKU个数最大为300！')
            t_erp_aliexpress_product_sku_objs = t_erp_aliexpress_product_sku.objects.filter(MainSKU__in=MainSKU).values('product_id').distinct()
            qs = qs.filter(product_id__in=t_erp_aliexpress_product_sku_objs)




        stopsales=request.GET.get('StopSales')
        if stopsales:
            StopSales=stopsales.split('-')[1]
            StopSalesFlag=stopsales.split('-')[0]
        else:
            StopSales=None
            StopSalesFlag=None


        if product_id:
            product_ids = [product_id]
            if ',' in product_id:
                product_ids = product_id.split(',')
            qs = qs.filter(product_id__in=product_ids)

        if shopSKU:
            sku_list = [shopSKU]
            if ',' in shopSKU:
                sku_list = shopSKU.split(',')
            t_erp_aliexpress_product_sku_objs = t_erp_aliexpress_product_sku.objects.filter(ShopSKU__in=sku_list).values(
                'product_id').distinct()
            qs = qs.filter(product_id__in=t_erp_aliexpress_product_sku_objs)
        if SKU:
            sku_list = [SKU]
            if ',' in SKU:
                sku_list = SKU.split(',')
                if len(sku_list) > 300:
                    sku_list=sku_list[:300]
                    messages.error(request, u'SKU个数最大为300！')
            mutilSKU = t_erp_aliexpress_product_sku.objects.filter(mutilSKUFlag=1).values('SKU')
            for mutilsku in mutilSKU:
                skus_list = mutilsku.get('SKU','').split("+")
                for sku in skus_list:
                    if sku in sku_list:
                        sku_list.append(mutilsku.get('SKU'))

            t_erp_aliexpress_product_sku_objs = t_erp_aliexpress_product_sku.objects.filter(SKU__in=sku_list).values('product_id').distinct()
            qs = qs.filter(product_id__in=t_erp_aliexpress_product_sku_objs)

        shopname = request.GET.get('shopname', '')
        accountName = request.GET.get('accountName', '').split(',')
        if shopname == 'all':
            shopname = ''

        Title_blurry = request.GET.get('Title_blurry', '')
        Title_exact = request.GET.get('Title_exact', '')
        Sales7Days_start = request.GET.get('Sales7Days_start', '')
        Sales7Days_end = request.GET.get('Sales7Days_end', '')
        Gmt_create_start = request.GET.get('Gmt_create_start', '')
        Gmt_create_end = request.GET.get('Gmt_create_end', '')
        Gmt_modified_start = request.GET.get('Gmt_modified_start', '')
        Gmt_modified_end = request.GET.get('Gmt_modified_end', '')
        UpdateTime_start = request.GET.get('UpdateTime_start', '')
        UpdateTime_end = request.GET.get('UpdateTime_end', '')
        product_status_type = request.GET.get('product_status_type', '')

        category = request.GET.get('category', '')
        tmpdict={}
        if isinstance(StopSales,(str,unicode)):
            if StopSales.isdigit() and int(StopSales)<100:
                tmpdict={'StopSales__range':[1,99]}
            elif StopSales.isdigit() and int(StopSales)==100:
                tmpdict={'StopSales':StopSales}
            elif StopSales.isdigit() and int(StopSales)>100:
                tmpdict = {'StopSales__range': [1,100]}

        if category == 0 or category == '0':
            category = ''
        searchList = {'subject__iexact': Title_exact, 'subject__icontains': Title_blurry,
                      'Sales7Days__gte': Sales7Days_start, 'Sales7Days__lt': Sales7Days_end,
                      'gmt_create__gte': Gmt_create_start, 'gmt_create__lt': Gmt_create_end,
                      'gmt_modified__gte': Gmt_modified_start, 'gmt_modified__lt': Gmt_modified_end,
                      'updatetime__gte': UpdateTime_start, 'updatetime__lt': UpdateTime_end,
                      'product_status_type__exact': product_status_type, 'category_id__exact': category,
                       'shopName__exact': shopname,
                      }
        if shoplist:
            searchList.update({'owner_member_id__in':shoplist})

        if not flag:
            if skustock_isempty:
                searchList.update({'skustock_isempty':skustock_isempty,})
            elif goodsstatus:
                searchList.update({'GoodsFlag__in':goodsstatus})
        if accountName and accountName !=['',]:
            searchList.update({'owner_member_id__in': accountName,})
        if Revoked:
            if Revoked in (1,'1',u'1'):
                qs=qs.filter(Q(revoked=1) | Q(revoked=0,product_status_type='service-delete'))
            else:
                searchList.update({'revoked__exact':Revoked})

        else:
            if product_status_type:
                searchList.update({'revoked__exact': '0'})

        if StopSalesFlag:
            searchList.update({'StopSalesFlag__exact':StopSalesFlag,})
        # 商品状态查询
        if tmpdict:
            searchList.update(tmpdict)
        # else:
        #     qs = qs.exclude(product_status_type='Delete')

        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    sl[k] = v
        if sl:
            # try:
            qs = qs.filter(**sl)
            # except Exception, ex:
            #     messages.error(request, u'输入的查询数据有问题！')
        return qs


xadmin.site.register(t_erp_aliexpress_shop_link_daily, t_erp_aliexpress_shop_link_daily_Admin)
xadmin.site.register(t_erp_aliexpress_online_info, t_erp_aliexpress_online_info_Admin)
# xadmin.site.register(v_erp_aliexpress_online_info_delete, t_erp_aliexpress_online_info_delete_Admin)
xadmin.site.register(t_erp_aliexpress_product_announcing, t_erp_aliexpress_product_announcing_Admin)
xadmin.site.register(t_erp_aliexpress_product_draft_box, t_erp_aliexpress_product_draft_box_Admin)
xadmin.site.register(t_erp_aliexpress_product_recycle_bin, t_erp_aliexpress_product_recycle_bin_Admin)
xadmin.site.register(t_erp_aliexpress_product_released, t_erp_aliexpress_product_released_Admin)
xadmin.site.register(t_erp_aliexpress_product_upload_result, t_erp_aliexpress_product_upload_result_Admin)
xadmin.site.register(t_erp_aliexpress_action_log, t_erp_aliexpress_action_log_Admin)
xadmin.site.register(t_erp_aliexpress_shop_info, t_erp_aliexpress_shop_info_Admin)
xadmin.site.register_plugin(refresh_online_info_Plugin,ListAdminView)
xadmin.site.register_plugin(site_left_menu_tree_Plugin_ali,BaseAdminView)
xadmin.site.register_plugin(activation_rate_plugin,BaseAdminView)
xadmin.site.register(t_erp_aliexpress_activation_rate,t_erp_aliexpress_activation_rate_Admin)
xadmin.site.register(t_erp_aliexpress_activation_rate_overview,t_erp_aliexpress_activation_rate_overview_Admin)
xadmin.site.register(v_erp_aliexpress_mutation_coefficient, v_erp_aliexpress_mutation_coefficient_Admin)
xadmin.site.register_plugin(mutation_coefficient_plugin,BaseAdminView)

# 速卖通下架
from aliapp.models import t_erp_aliexpress_online_info_shelf
from aliapp.StoreXadmin.t_erp_aliexpress_online_info_shelf_Admin import t_erp_aliexpress_online_info_shelf_Admin
xadmin.site.register(t_erp_aliexpress_online_info_shelf, t_erp_aliexpress_online_info_shelf_Admin)