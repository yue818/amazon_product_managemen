# -*-coding:utf-8-*-
"""  
 @desc:  amazon店铺Listing
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_templet_public_amazon_listing_Admin.py
 @time: 2017/12/15 19:22
"""
import urllib
from django.utils.safestring import mark_safe
from django.contrib import messages
from django_redis import get_redis_connection
from django.db import connection
from brick.pydata.py_redis.py_SynRedis_tables import py_SynRedis_tables
from brick.classredis.classlisting import classlisting
from brick.classredis.classshopsku import classshopsku
from brick.classredis.classmainsku import classmainsku
from brick.classredis.classsku import classsku
from brick.pricelist.calculate_price import calculate_price
from skuapp.table.t_online_amazon_fba_inventory import t_online_amazon_fba_inventory
from skuapp.table.t_amazon_cpc_ad import t_amazon_cpc_ad
from skuapp.table.t_amazon_operation_log import t_amazon_operation_log
from skuapp.table.t_combination_sku_log import t_combination_sku_log
from skuapp.public.check_permission_legality import check_permission_legality

from Project.settings import *
import os
import datetime
import errno
from xlwt import *
import oss2
import uuid

from brick.table.t_store_configuration_file import t_store_configuration_file
from brick.amazon.product_refresh.get_auth_info import GetAuthInfo
from brick.amazon.product_refresh.generate_feed_xml import GenerateFeedXml
from brick.amazon.upload_product.message_to_rabbitmq import MessageToRabbitMq
import json
from skuapp.table.t_online_info_amazon import t_online_info_amazon
import urllib
from django.http import HttpResponseRedirect
from django.db.models import Q

import traceback

redis_conn = get_redis_connection(alias='product')
py_SynRedis_tables_obj = py_SynRedis_tables()
classsku_obj = classsku()
listingobjs = classlisting(connection, redis_conn)
classshopskuobjs = classshopsku(connection, redis_conn)
classmainsku_obj = classmainsku(connection, redis_conn)
t_store_configuration_file_obj = t_store_configuration_file(connection)


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5 (except OSError, exc: for Python <2.5)
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


class t_online_info_amazon_listing_Admin(object):
    amazon_listing_plugin = True
    search_box_flag = True
    amazon_site_left_menu_tree_flag = True
    downloadxls = True
    amzon_sort_bar = True

    def show_sku_list(self, obj):
        try:
            if obj.is_fba == 0:
                fba_heard_name = 'FBM'
            elif obj.is_fba == 1:
                fba_heard_name = 'FBA'
            else:
                fba_heard_name = ''

            rt = '''
                <table class="table table-condensed" style="text-align:center;">
                 <thead>
                 <tr bgcolor="#C00">
                 <th style="text-align:center;">商品SKU</th>
                 <th style="text-align:center;">商品状态</th>
                 <th style="text-align:center;">可卖天数</th>
                 <th style="text-align:center;">店铺SKU</th>
                 <th style="text-align:center;">%s库存量</th>
                 ''' % fba_heard_name

            if obj.is_fba == 1:
                rt += '<th style="text-align:center;">库存成本</th>'
                rt += '<th style="text-align:center;">到货时间</th>'
                rt += '<th style="text-align:center;">预览价格</th>'
            elif obj.is_fba == 0:
                rt += '<th style="text-align:center;">浦江库存</th>'
            rt += '''
                 <th style="text-align:center;">价格</th>
                 <th style="text-align:center;">运费</th>
                 <th style="text-align:center;">利润率</th>
                 </tr>
                 </thead><tbody>'''

            infor = []
            shopsku = obj.seller_sku
            eachinfor = {}
            eachinfor['SKU'] = classshopskuobjs.getSKU(shopsku)
            eachinfor['SKUKEY'] = ['NotInStore', 'GoodsStatus', 'Number', 'ReservationNum', 'CanSaleDay']
            eachinfor['ShopSKU'] = shopsku
            eachinfor['ShopSKUKEY'] = ['Quantity', 'Price', 'Shipping', 'Status']
            infor.append(eachinfor)
            sInfors = py_SynRedis_tables_obj.BatchReadRedis(infor)

            for sinfor in sInfors:
                if obj.is_fba == 0:
                    shopskuQuantity = obj.quantity
                    pj_quantity = classsku_obj.get_skuallattrvalue_by_sku(str(sinfor['SKU']))['Number']
                elif obj.is_fba == 1:
                    shopskuQuantity = obj.afn_warehouse_quantity
                else:
                    shopskuQuantity = ''
                shopskuPrice = obj.price
                shopskuShipping = obj.shipping_price
                shopskuStatus = obj.Status
                goodsstatus = sinfor['SKUKEY'][1]

                if obj.product_status == '1':
                    goodsstatus = u'正常'
                elif obj.product_status == '2':
                    goodsstatus = u'售完下架'
                elif obj.product_status == '3':
                    goodsstatus = u'临时下架'
                elif obj.product_status == '4':
                    goodsstatus = u'停售'
                else:
                    goodsstatus = ''

                can_sold_days = sinfor['SKUKEY'][-1]
                if not can_sold_days:
                    can_sold_days = ''

                style = ''
                if goodsstatus and goodsstatus != u'正常':
                    style = 'class="danger"'  # 非正常为红色
                elif shopskuStatus == 'Inactive':
                    style = 'class="active"'  # 正常  Disabled 为 灰色
                elif shopskuStatus == 'Active':
                    style = 'class="success"'  # 正常  Enabled 为 绿色

                if not shopskuPrice:
                    shopskuPrice = 0

                if not shopskuShipping:
                    shopskuShipping = 0

                if '+' in shopsku:
                    count_sku = len(shopsku.split('+'))
                else:
                    count_sku = shopsku.split('*')[-1]
                try:
                    count_sku = float(count_sku)
                except:
                    count_sku = 0

                CountryCode = obj.ShopName.split('-')[-1].split('/')[0]
                if CountryCode == 'JP':
                    CountryCode = 'JPN'
                elif CountryCode == 'AU':
                    CountryCode = 'AUS'
                elif CountryCode == 'DE':
                    CountryCode = 'GER'
                elif CountryCode == 'FR':
                    CountryCode = 'FRA'
                elif not CountryCode:
                    CountryCode = 'US'

                if obj.is_fba == 0:
                    try:
                        if count_sku:
                            sellingPrice = (float(shopskuPrice) + float(shopskuShipping)) / count_sku
                        else:
                            sellingPrice = (float(shopskuPrice) + float(shopskuShipping))
                        calculate_price_obj = calculate_price(str(sinfor['SKU']))
                        profitrate_info = calculate_price_obj.calculate_profitRate(sellingPrice, platformCountryCode='AMAZONGNZF', DestinationCountryCode=CountryCode)
                    except:
                        profitrate_info = ''
                    if profitrate_info:
                        profitrate = '%.2f' % float(profitrate_info['profitRate'])
                    else:
                        profitrate = ''
                else:
                    profitrate = ''

                profit_id = 'profit_id' + '_' + str(sinfor['SKU'])

                if obj.is_fba == 1:
                    inventory_html = u'<td><a><span id="inventory_%s">%s</span></a></td>' % (obj.id, shopskuQuantity)
                    if obj.inventory_received_date:
                        receive_day = str(obj.inventory_received_date)[0:10]
                    else:
                        receive_day = ''
                    receive_date_html = u'<td>%s</td>' % receive_day
                    # estimated_fee_html = u'<td>%s</td>' % obj.estimated_fee
                    if obj.product_size_tier and 'Oversize' in obj.product_size_tier:
                        fee_color_style = 'style = "color:red; font-weight: bold;"'
                    elif obj.product_size_tier and 'Sm-Std-Non-Media' in obj.product_size_tier:
                        fee_color_style = 'style = "color:green"'
                    else:
                        fee_color_style = ''
                    estimated_fee_html = u'<td><a><span id="estimated_%s" %s>%s</span></a></td>' % (obj.id, fee_color_style, obj.estimated_fee)
                else:
                    inventory_html = u'<td>%s</td>' % shopskuQuantity
                    receive_date_html = ''
                    estimated_fee_html = ''

                if not obj.last_price:
                    price_html = shopskuPrice
                else:
                    price_html = str(obj.last_price) + '->' + shopskuPrice

                if obj.is_fba == 1:
                    try:
                        total_price = 0
                        for product_sku_each in sinfor['SKU'].split('+'):
                            sku_count = product_sku_each.split('*')
                            if len(sku_count) == 1:
                                sku_this = sku_count[0]
                                count_this = 1
                            else:
                                sku_this = sku_count[0]
                                count_this = sku_count[1]
                            price_this = classsku_obj.get_price_by_sku(sku_this.strip())
                            inventory_cost_this = float(price_this)*float(count_this)
                            total_price += inventory_cost_this
                        inventory_cost = float(total_price) * float(shopskuQuantity)
                    except Exception as e:
                        inventory_cost = e
                elif obj.is_fba == 0:
                    inventory_cost = pj_quantity
                else:
                    inventory_cost = ''

                product_sku_html = obj.SKU
                if obj.SKU is not None and obj.SKU != '' and obj.SKU[0:2] == 'ZH':
                    zh_sku_obj = t_combination_sku_log.objects.filter(Com_SKU=sinfor['SKU'])
                    if zh_sku_obj:
                        product_sku_html = str(obj.SKU) + '<br/>↓<br/>' + str(zh_sku_obj[0].Pro_SKU)

                rt = '''
                    %s <tr %s>
                     <td style="word-break:break-all;">%s</td>
                     <td>%s</td>
                     <td>%s</td>
                     <td style="word-break:break-all;">%s</td>
                     %s
                     <td>%s</td>
                     %s
                     %s
                     <td>%s</td>
                     <td>%s</td>
                     <td><a><span id="%s">%s</span></a></td></tr>
                ''' % (rt, style,
                       product_sku_html,
                       goodsstatus,
                       can_sold_days,
                       sinfor['ShopSKU'].replace('<', '&lt;').replace('>', '&gt;'),
                       inventory_html,
                       inventory_cost,
                       receive_date_html,
                       estimated_fee_html,
                       price_html,
                       shopskuShipping,
                       profit_id, profitrate
                       )

                rt = u"%s<script>$('#%s').on('click',function()" \
                     u"{layer.open({type:2,skin:'layui-layer-lan',title:'算价表'," \
                     u"fix:false,shadeClose: true,maxmin:true,area:['1300px','900px']," \
                     u"content:'/price_list/?SKU=%s&sellingPrice=%s&platformCountryCode=%s&DestinationCountryCode=%s',});});" \
                     u"</script>" % (rt, profit_id, sinfor['SKU'], shopskuPrice, 'AMAZONGNZF', CountryCode)
                seller_sku = urllib.quote(obj.seller_sku.decode('gbk', 'replace').encode('utf-8', 'replace'))

                if obj.is_fba == 1:
                    rt += '''
                                <script>
                                    a = screen.width*0.8
                                    b = screen.height*0.3
                                     $("#inventory_%s").on("click", function(){
                                      layer.open({
                                       type: 2,
                                       skin: "layui-layer-lan",
                                       title: "库存详情",
                                       fix: false,
                                       shadeClose: true,
                                       maxmin: true,
                                       area: [a+'px', b+'px'],
                                       content: "/show_inventory_detail/?seller_sku=%s&shopname=%s",
                                       btn: ["关闭页面"],
                                       });
                                   })
                               </script>
                               ''' % (obj.id, seller_sku, obj.ShopName)

                    rt += '''
                            <script>
                                    a = screen.width*0.8
                                    b = screen.height*0.3
                                     $("#estimated_%s").on("click", function(){
                                      layer.open({
                                       type: 2,
                                       skin: "layui-layer-lan",
                                       title: "包装尺寸情况",
                                       fix: false,
                                       shadeClose: true,
                                       maxmin: true,
                                       area: [a+'px', b+'px'],
                                       content: "/show_estimated_detail/?seller_sku=%s&shopname=%s",
                                       btn: ["关闭页面"],
                                       });
                                   })
                               </script>
                    ''' % (obj.id, seller_sku, obj.ShopName)

            rt += u"</tbody></table>"
        except Exception as e:
            rt = traceback.format_exc()
        return mark_safe(rt)
    show_sku_list.short_description = mark_safe('<p align="center"style="color:#428bca;">子SKU</p>')

    def show_image_url(self, obj):
        if obj.Status == 'Incomplete':
            rt = '<div style="display: inline-block;width: 0;height: 0; line-height: 0;border: 8px solid transparent; border-top-color: #7a7c76; border-bottom-width: 0;"></div><span style="padding-left: 20px">变体</span>'
        else:
            url = u'%s' % obj.image_url
            rt = '<img src="%s"  width="69" height="69"  alt = "%s"  title="%s"  />' % (url, url, url)
        return mark_safe(rt)
    show_image_url.short_description = u'<span style="color:#428BCA">图片</span>'

    def show_item_name_and_product_id(self, obj):
        from skuapp.table.t_cloth_factory_dispatch_needpurchase import t_cloth_factory_dispatch_needpurchase
        site_url_dict = {'US': 'https://www.amazon.com/',
                         'UK': 'https://www.amazon.co.uk/',
                         'JP': 'https://www.amazon.co.jp/',
                         'DE': 'https://www.amazon.de/',
                         'FR': 'https://www.amazon.fr/',
                         'AU': 'https://www.amazon.com.au/',
                         'IN': 'https://www.amazon.in/'}
        if obj.ShopSite and obj.ShopSite in site_url_dict:
            site_url = site_url_dict[obj.ShopSite]
        else:
            site_url = 'https://www.amazon.com/'
        rt = u'<p style="word-break:break-all;">%s</p><br>店铺:%s<br>店长/销售员:%s<br>销售排名：%s<br><a href="%sdp/%s" target="_blank">%s</a><br><br>' % (obj.item_name, obj.ShopName, obj.seller, obj.sale_rank, site_url, obj.asin1, obj.asin1)

        if obj.is_fba == 1 or obj.is_fba == 0:
            t_cloth_factory_dispatch_needpurchase_objs = t_cloth_factory_dispatch_needpurchase.objects.filter(SKU=obj.SKU).\
                filter(Q(currentState=8) | Q(currentState=16) | Q(currentState=18) | Q(currentState=20) | Q(currentState=22) | Q(currentState=24)).\
                order_by('-createDate').values_list('SKU','productNumbers', 'currentState', 'createDate', 'closeDate', 'completeNumbers')

            if t_cloth_factory_dispatch_needpurchase_objs:
                rt += '''<table class="table table-condensed" style="text-align:center;">
                             <thead>
                             <tr bgcolor="#C00">
                             <th style="text-align:center;">商品SKU</th>
                             <th style="text-align:center;">需采购数量</th>
                             <th style="text-align:center;">当前状态</th>
                             <th style="text-align:center;">创建时间</th>
                             <th style="text-align:center;">关闭时间</th>
                             <th style="text-align:center;">完成件数</th>
                        '''
                for rowObj in t_cloth_factory_dispatch_needpurchase_objs:
                    if rowObj[2] == '8':
                        current_state = '采购计划审核'
                    elif rowObj[2] in ('16', '18'):
                        current_state = '服装工厂排单'
                    elif rowObj[2] in ('20', '22'):
                        current_state = '检验交付数量和单价'
                    elif rowObj[2] == '24':
                        current_state = '生产完成可建普源采购单'
                    else:
                        current_state = rowObj[2]

                    rt += '''<tr>
                             <td style="word-break:break-all;">%s</td>
                             <td>%s</td>
                             <td style="word-break:break-all;">%s</td>
                             <td style="word-break:break-all;">%s</td>
                             <td style="word-break:break-all;">%s</td>
                             <td>%s</td>
                             </tr>
                          ''' % (rowObj[0], rowObj[1], current_state, rowObj[3], rowObj[4], rowObj[5])
                rt += u"</tbody></table>"
            else:
                if obj.is_fba == 1 and (obj.orders_7days/7 + obj.orders_15days/15 + obj.orders_30days/30) > 0 and obj.afn_warehouse_quantity*3/(obj.orders_7days/7 + obj.orders_15days/15 + obj.orders_30days/30) < 20:
                    # rt += '<a href = "/Project/admin/skuapp/t_cloth_factory_dispatch_plan" target = "_blank" > <p style="color:red;"><b>请及时制定采购计划</b></p> </a>'
                    rt += '<p style="color:red;"><b>请及时制定采购计划</b></p> '
        return mark_safe(rt)
    show_item_name_and_product_id.short_description = u'<span style="color:#428BCA; width:50px">标题/产品ID</span>'

    def show_order(self, obj):
        if obj.is_fba == 1 and obj.refund_rate > 5:
            style = 'style="color:#FF0000;font-weight:bold;"'
        else:
            style = ''
        order_html = u'''<table class="table table-condensed">
                                     <tr><td>7天</td> <td>%s</td></tr>
                                     <tr><td>15天</td> <td>%s</td></tr>
                                     <tr><td>30天</td> <td>%s</td></tr>  
                                     <tr><td>总</td> <td>%s</td></tr> 
                                     <tr ><td %s>退款率</td> <td %s>%s <br> (%s)</td></tr> 
                                   </table>
                                 ''' % (obj.orders_7days, obj.orders_15days, obj.orders_30days, obj.orders_total, style, style, str(obj.refund_rate)+'%', obj.orders_refund_total)
        return mark_safe(order_html)
    show_order.short_description = u'<span style="color:#428BCA; width:200px">订单量</span>'

    def show_time(self, obj):
        try:
            action = ''
            if obj.deal_action == 'refresh_product':
                deal_action_cn = '产品刷新'
            elif obj.deal_action == 'load_product':
                deal_action_cn = '产品上架'
            elif obj.deal_action == 'unload_product':
                deal_action_cn = '产品下架'
            elif obj.deal_action == 'product_info_modify':
                deal_action_cn = '产品信息修改'
            elif obj.deal_action == 'product_price_modify':
                deal_action_cn = '产品价格修改'
            elif obj.deal_action == 'product_image_modify':
                deal_action_cn = '产品图片修改'
            else:
                deal_action_cn = obj.deal_action

            if obj.deal_result is not None:
                if obj.deal_action is not None:
                    action = deal_action_cn + ' '
                action += obj.deal_result
                if obj.deal_result != 'Success' and obj.deal_result_info is not None:
                    action += '.<br/>Reason: &nbsp;' + obj.deal_result_info
            elif obj.deal_action is not None:
                action = deal_action_cn + '中'
            else:
                action = ''
            # upload_time = None
            # sku_single_obj = t_templet_amazon_upload_result.objects.filter(item_sku=obj.seller_sku)
            # if sku_single_obj:
            #     upload_time = sku_single_obj[0].createTime.strftime('%Y-%m-%d')
            # else:
            #     sku_child_obj = t_templet_amazon_published_variation.objects.filter(child_sku=obj.seller_sku)
            #     if sku_child_obj:
            #         upload_time = sku_child_obj[0].createTime
            #         if upload_time:
            #             upload_time = upload_time.strftime('%Y-%m-%d')
            #         else:
            #             sku_parent_obj = t_templet_amazon_upload_result.objects.filter(item_sku=sku_child_obj[0].parent_sku)
            #             if sku_parent_obj:
            #                 upload_time = sku_parent_obj[0].createTime.strftime('%Y-%m-%d')
            #             else:
            #                 upload_time = None
            #     else:
            #         upload_time = None

            if obj.upload_time:
                upload_html = u'<br>刊登日期:%s' % obj.upload_time.strftime('%Y-%m-%d')
            else:
                upload_html = ''
            rt = u'最近更新时间:<br>%s %s<br>操作状态:<br> %s ' % (obj.UpdateTime, upload_html, action)
        except Exception as e:
            rt = ''
        return mark_safe(rt)
    show_time.short_description = mark_safe('<p align="center" style="width:150px;color:#428bca;">时间</p>')

    def product_change(self, obj):
        if check_permission_legality(self):
            return u'<br><a href = "/syndata_by_amazon_api/?operation_type=%s&pri_id=%s" style=" padding-top: 10px;">修改</a>' % ('change', obj.id)
        else:
            return ''

    def show_operations(self, obj):
        # syn = u'<a href = "/syndata_by_amazon_api/?operation_type=%s&shopName=%s&seller_sku=%s" style="padding-top: 10px;">同步</a>' % ('sync', obj.ShopName, obj.seller_sku)
        # up = u'<br><a href = "/syndata_by_amazon_api/?operation_type=%s&shopName=%s&seller_sku=%s" style=" padding-top: 10px;">上架</a>' % ('upload', obj.ShopName, obj.seller_sku)
        # down = u'<br><a href = "/syndata_by_amazon_api/?operation_type=%s&shopName=%s&seller_sku=%s" style=" padding-top: 10px;">下架</a>' % ('download', obj.ShopName, obj.seller_sku)
        # change = u'<br><a href = "/syndata_by_amazon_api/?operation_type=%s&pri_id=%s" style=" padding-top: 10px;">修改</a>' % ('change', obj.id)
        # rt = syn + up + down + change
        # rt = change
        rt = self.product_change(obj)
        return mark_safe(rt)
    show_operations.short_description = u'<span style="color:#428BCA">操作</span>'

    def show_deal_result(self, obj):
        rt = ''
        if obj.deal_action == 'refresh_product':
            deal_action_cn = '产品刷新'
        elif obj.deal_action == 'load_product':
            deal_action_cn = '产品上架'
        elif obj.deal_action == 'unload_product':
            deal_action_cn = '产品下架'
        elif obj.deal_action == 'product_info_modify':
            deal_action_cn = '产品信息修改'
        elif obj.deal_action == 'product_price_modify':
            deal_action_cn = '产品价格修改'
        elif obj.deal_action == 'product_image_modify':
            deal_action_cn = '产品图片修改'
        else:
            deal_action_cn = obj.deal_action

        if obj.deal_result is not None:
            if obj.deal_action is not None:
                rt = deal_action_cn + ' '
            rt += obj.deal_result
            if obj.deal_result != 'Success' and obj.deal_result_info is not None:
                rt += '.<br/>Reason: &nbsp;' + obj.deal_result_info
        elif obj.deal_action is not None:
            rt = deal_action_cn + '中'
        else:
            rt = ''
        return mark_safe(rt)
    show_deal_result.short_description = u'<span style="color:#428BCA">处理状态</span>'

    actions = ['to_excel', 'change_price', 'load_amazon_products']

    def change_price(self, request, objs):
        modify_type = request.POST.get('modify_type', '')
        modify_base = request.POST.get('modify_base', '')
        modify_number = request.POST.get('modify_number', '')

        shop_sku = dict()
        fail_record = list()
        sku_str = ''
        refresh_type = 'product_price_modify_multi'
        batch_id = uuid.uuid4()

        for record in objs:
            log_dic = dict()
            t_online_info_amazon_ins = t_online_info_amazon.objects.filter(id=record.id)
            for obj in t_online_info_amazon_ins:
                seller_sku = obj.seller_sku
                sku_str = sku_str + seller_sku + ','  # 用于执行操作后显示相应条目
                shop_name = obj.ShopName
                # 记录操作日志
                log_dic['batch_id'] = batch_id
                log_dic['shop_name'] = shop_name
                log_dic['seller_sku'] = seller_sku
                log_dic['deal_user'] = request.user.username
                log_dic['deal_action'] = refresh_type
                log_dic['price_before'] = obj.price
                log_dic['begin_time'] = datetime.datetime.now()
                log_dic['deal_result'] = 0
                log_dic['remark'] = 'modify_type: %s, modify_base: %s, modify_number: %s' % (modify_type, modify_base, modify_number)

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
                        price_after = None
                    log_dic['price_after'] = price_after
                except Exception as e:
                    log_dic['end_time'] = datetime.datetime.now()
                    log_dic['deal_result'] = -1
                    log_dic['deal_result_info'] = 'Calculating adjusted price failure'
                    log_dic['remark'] = e
                    fail_record.append(obj.seller_sku)
                    t_amazon_operation_log.objects.create(**log_dic)
                    continue

                try:
                    if obj.estimated_fee:
                        lowest_price = float('%.2f' % float(obj.estimated_fee))
                    else:
                        lowest_price = 0
                except:
                    lowest_price = 0

                if price_after <= lowest_price:
                    log_dic['price_after'] = price_after
                    log_dic['end_time'] = datetime.datetime.now()
                    log_dic['deal_result'] = -1
                    log_dic['deal_result_info'] = 'price_after error, less than lowest_price: %s' % lowest_price
                    fail_record.append(obj.seller_sku)
                    t_amazon_operation_log.objects.create(**log_dic)
                    continue

                t_amazon_operation_log.objects.create(**log_dic)

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
            auth_info['batch_id'] = str(batch_id)
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
            messages.error(request, '以下商品计算调整后价格异常，不予调整：%s' % fail_str[:-1])

        # 不是所有调价都异常给调价中提示
        if len(objs) != len(fail_record):
            messages.success(request, '商品价格调整中, 调整批次号为：' + '<a href = "/Project/admin/skuapp/t_amazon_operation_log/?batch_id=%s" target = "_blank" > %s </a>' % (str(batch_id),str(batch_id)))


        if sku_str == '':
            sku_str = ' '
        else:
            sku_str = sku_str[:-1]
        sku_str = urllib.quote(sku_str.decode('gbk', 'replace').encode('utf-8', 'replace'))
        if len(objs) <= self.list_per_page:
            return HttpResponseRedirect('/Project/admin/skuapp/t_online_info_amazon_listing/?SKU=%s' % sku_str)
    change_price.short_description = u' '

    def load_amazon_products(self, request, objs):
        from django.db import connection
        from brick.amazon.product_refresh.get_auth_info import GetAuthInfo
        from brick.amazon.product_refresh.generate_feed_xml import GenerateFeedXml
        from brick.amazon.upload_product.message_to_rabbitmq import MessageToRabbitMq
        import json
        from skuapp.table.t_online_info_amazon import t_online_info_amazon
        import datetime
        import urllib
        from django.http import HttpResponseRedirect

        syn_type = request.POST.get('syn_type', '')
        shop_sku = {}
        sku_str = ''
        if syn_type == 'load':  # 产品上架
            refresh_type = 'load_product'
            for record in objs:
                t_online_info_amazon_ins = t_online_info_amazon.objects.filter(id=record.id)
                for obj in t_online_info_amazon_ins:
                    seller_sku = obj.seller_sku
                    sku_str = sku_str + seller_sku + ','
                    shop_name = obj.ShopName
                    if shop_name not in shop_sku:
                        shop_sku[shop_name] = [seller_sku]
                    else:
                        shop_sku[shop_name].append(seller_sku)
                    t_online_info_amazon_ins.update(deal_action='load_product',
                                                    deal_result=None,
                                                    deal_result_info=None,
                                                    UpdateTime=datetime.datetime.now())
        elif syn_type == 'unload':  # 产品下架
            refresh_type = 'unload_product'
            for record in objs:
                t_online_info_amazon_ins = t_online_info_amazon.objects.filter(id=record.id)
                for obj in t_online_info_amazon_ins:
                    seller_sku = obj.seller_sku
                    sku_str = sku_str + seller_sku + ','
                    shop_name = obj.ShopName
                    if shop_name not in shop_sku:
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
        if len(objs) <= self.list_per_page:
            return HttpResponseRedirect('/Project/admin/skuapp/t_online_info_amazon_listing/?SKU=%s' % sku_str)

    load_amazon_products.short_description = u' '

    def to_excel(self, request, queryset):
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))
        mkdir_p(path)
        os.popen('chmod 777 %s' % path)

        w = Workbook()
        sheet = w.add_sheet('amazon_listing_record')
        sheet.write(0, 0, u'店铺')
        sheet.write(0, 1, u'店铺SKU')
        sheet.write(0, 2, u'商品SKU')
        sheet.write(0, 3, u'ASIN')
        sheet.write(0, 4, u'到货时间')
        sheet.write(0, 5, u'库存量')
        sheet.write(0, 6, u'可售数')
        sheet.write(0, 7, u'预览价格')
        sheet.write(0, 8, u'当前价格')
        sheet.write(0, 9, u'当前价格刷新时间')
        sheet.write(0, 10, u'历史价格')
        sheet.write(0, 11, u'历史价格刷新时间')
        sheet.write(0, 12, u'7天销量')
        sheet.write(0, 13, u'15天销量')
        sheet.write(0, 14, u'30天销量')
        sheet.write(0, 15, u'库存成本')
        sheet.write(0, 16, u'状态')
        sheet.write(0, 17, u'店长/销售员')
        sheet.write(0, 18, u'操作备注')
        sheet.write(0, 19, u'标题')

        # 写数据
        row = 0
        for qs in queryset:
            row = row + 1

            if qs.is_fba == 1:
                inventory_objs = t_online_amazon_fba_inventory.objects.filter(sku=qs.seller_sku)
                if inventory_objs:
                    fulfillable_quantity = inventory_objs[0].afn_fulfillable_quantity
                else:
                    fulfillable_quantity = ''
                receive_day = str(qs.inventory_received_date)[0:10]
                quantity_excel = qs.afn_warehouse_quantity
            else:
                fulfillable_quantity = ''
                receive_day = ''
                quantity_excel = qs.quantity

            if qs.UpdateTime:
                update_time = qs.UpdateTime.strftime('%Y-%m-%d %H:%M')
            else:
                update_time = ''

            if qs.last_price_time:
                last_price_time = qs.last_price_time.strftime('%Y-%m-%d %H:%M')
            else:
                last_price_time = ''

            product_sku = classshopskuobjs.getSKU(qs.seller_sku)

            order_obj = t_amazon_cpc_ad.objects.filter(shop_name=qs.ShopName, seller_sku=qs.seller_sku)
            if order_obj:
                order_7day = order_obj[0].orders_7days
                order_15day = order_obj[0].orders_15days
                order_30day = order_obj[0].orders_30days
            else:
                order_7day = ''
                order_15day = ''
                order_30day = ''

            try:
                total_price = 0
                for product_sku_each in product_sku.split('+'):
                    sku_count = product_sku_each.split('*')
                    if len(sku_count) == 1:
                        sku_this = sku_count[0]
                        count_this = 1
                    else:
                        sku_this = sku_count[0]
                        count_this = sku_count[1]
                    price_this = classsku_obj.get_price_by_sku(sku_this.strip())
                    inventory_cost_this = float(price_this)*float(count_this)
                    total_price += inventory_cost_this
                inventory_cost = float(total_price) * float(quantity_excel)
            except Exception as e:
                inventory_cost = None

            Department, seller, Published = t_store_configuration_file_obj.getinfobyshopcode(qs.ShopName)

            excel_content_list = [qs.ShopName, qs.seller_sku, product_sku, qs.asin1, receive_day, quantity_excel, fulfillable_quantity,
                                  qs.estimated_fee, qs.price, update_time, qs.last_price, last_price_time, order_7day, order_15day, order_30day,
                                  inventory_cost, str(qs.Status), seller, qs.action_remark, qs.item_name]
            column = 0
            for content in excel_content_list:
                sheet.write(row, column, content)
                column += 1
        filename = request.user.username + '_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.xls'
        w.save(path + '/' + filename)
        os.popen(r'chmod 777 %s' % (path + '/' + filename))

        # 上传oss对象
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT, BUCKETNAME_XLS)
        bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)
        # 删除现有的
        for object_info in oss2.ObjectIterator(bucket,
                                               prefix='%s/%s_' % (request.user.username, request.user.username)):
            bucket.delete_object(object_info.key)
        bucket.put_object(u'%s/%s' % (request.user.username, filename), open(path + '/' + filename))
        messages.success(request, u'%s%s.%s/%s/%s' % (PREFIX, BUCKETNAME_XLS, ENDPOINT_OUT, request.user.username, filename) + u':成功导出,可点击Download下载到本地............................。')
    to_excel.short_description = u'导出库存价格数据'

    list_display = ('id', 'show_image_url', 'show_item_name_and_product_id', 'show_order', 'Status', 'show_sku_list', 'show_time', 'action_remark')
    search_fields = None
    list_filter = None
    list_editable = ('action_remark',)

    def get_list_queryset(self, ):
        request = self.request
        qs = super(t_online_info_amazon_listing_Admin, self).get_list_queryset()
        qs = qs.filter(Status__in=('Active', 'Inactive'))

        is_fba = self.request.GET.get('_p_is_fba', '')
        ShopName = request.GET.get('shopname', '')
        SKU = request.GET.get('SKU', '')
        SKU = '' if SKU == '' else SKU.strip().replace(' ', '+').split(',')
        ASIN = request.GET.get('ASIN', '')
        ASIN = '' if ASIN == '' else ASIN.split(',')
        parent_asin = request.GET.get('parent_asin', '')
        product_sku = request.GET.get('product_sku', '')
        product_sku_multi = request.GET.get('product_sku_multi', '')
        product_sku_multi = '' if product_sku_multi == '' else product_sku_multi.strip().replace(' ', '+').split(',')
        status = request.GET.get('Status', '')
        if status == 'ALL':
            status = ''
        mfn_fulfillable_quantity_start = request.GET.get('mfn_fulfillable_quantity_start', '')
        mfn_fulfillable_quantity_end = request.GET.get('mfn_fulfillable_quantity_end', '')
        if is_fba == '1':
            mfn_fulfillable_quantity_start = ''
            mfn_fulfillable_quantity_end = ''
        afn_warehouse_quantity_start = request.GET.get('afn_warehouse_quantity_start', '')
        afn_warehouse_quantity_end = request.GET.get('afn_warehouse_quantity_end', '')
        if is_fba == '0':
            afn_warehouse_quantity_start = ''
            afn_warehouse_quantity_end = ''
        price_start = request.GET.get('price_start', '')
        price_end = request.GET.get('price_end', '')
        ship_price_start = request.GET.get('ship_price_start', '')
        ship_price_end = request.GET.get('ship_price_end', '')
        orders_start = request.GET.get('orders_start', '')
        orders_end = request.GET.get('orders_end', '')
        date_refresh_start = request.GET.get('date_refresh_start', '')
        date_refresh_end = request.GET.get('date_refresh_end', '')
        date_receive_start = request.GET.get('date_receive_start', '')
        date_receive_end = request.GET.get('date_receive_end', '')
        item_name = request.GET.get('item_name', '')

        seller = request.GET.get('seller', '')
        product_status = request.GET.get('product_status', '')

        orders_refund_total_start = request.GET.get('orders_refund_total_start', '')
        orders_refund_total_end = request.GET.get('orders_refund_total_end', '')
        refund_rate_start = request.GET.get('refund_rate_start', '')
        refund_rate_end = request.GET.get('refund_rate_end', '')

        product_size_tier = request.GET.get('product_size_tier', '')
        shop_site = request.GET.get('shop_site', '')

        if product_sku:
            qs = qs.filter(Q(SKU__icontains=product_sku) | Q(com_pro_sku__icontains=product_sku))

        searchList = {'ShopName__icontains': ShopName,
                      'item_name__icontains': item_name,
                      'asin1__in': ASIN,
                      'seller_sku__in': SKU,
                      'afn_warehouse_quantity__gte': afn_warehouse_quantity_start,
                      'afn_warehouse_quantity__lte': afn_warehouse_quantity_end,
                      'quantity__gte': mfn_fulfillable_quantity_start,
                      'quantity__lte': mfn_fulfillable_quantity_end,
                      'price__gte': price_start,
                      'price__lte': price_end,
                      'shipping_price__gte': ship_price_start,
                      'shipping_price__lte': ship_price_end,
                      'orders_7days__gte': orders_start,
                      'orders_7days__lte': orders_end,
                      'Status__exact': status,
                      'UpdateTime__gte': date_refresh_start,
                      'UpdateTime__lte': date_refresh_end,
                      'inventory_received_date__gte': date_receive_start,
                      'inventory_received_date__lte': date_receive_end,
                      'product_status__exact': product_status,
                      'seller__exact': seller,
                      'Parent_asin__exact': parent_asin,
                      'SKU__in': product_sku_multi,
                      'orders_refund_total__gte': orders_refund_total_start,
                      'orders_refund_total__end': orders_refund_total_end,
                      'refund_rate__gte': refund_rate_start,
                      'refund_rate__lte': refund_rate_end,
                      'product_size_tier__icontains': product_size_tier,
                      'ShopSite__exact': shop_site,
                      }
        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    sl[k] = v
        if sl is not None:
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'Please enter the correct content!')
        return qs



