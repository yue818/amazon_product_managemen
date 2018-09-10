# -*-coding:utf-8-*-
from skuapp.modelsadminx.t_online_info_amazon_Admin import *

"""  
 @desc:  amazon店铺Listing
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_templet_public_amazon_listing_Admin.py
 @time: 2017/12/15 19:22
"""

from django.utils.safestring import mark_safe
from django.contrib import messages
from app_djcelery.tasks import amazon_product_refresh
from skuapp.table.t_online_info_amazon import t_online_info_amazon
import datetime
# from brick.pydata.py_redis.py_SynRedis_pub import py_SynRedis_pub
from brick.classredis.classshopsku import classshopsku
from django_redis import get_redis_connection
from django.db import connection
from skuapp.table.t_shopsku_information_binding import t_shopsku_information_binding
from brick.classredis.classsku import classsku
from skuapp.table.t_amazon_cpc_ad import t_amazon_cpc_ad

# py_SynRedis_pub_obj = py_SynRedis_pub()
redis_conn = get_redis_connection(alias='product')
classshopskuobjs = classshopsku(connection, redis_conn)
classsku_obj = classsku()
import urllib

from django.utils.safestring import mark_safe
from django_redis import get_redis_connection
from django.contrib import messages
from django.db import connection
from django.db.models import Q
from django.http import HttpResponseRedirect

# from skuapp.table.t_store_marketplan_execution import t_store_marketplan_execution
# from skuapp.table.t_upload_shopname import t_upload_shopname
from brick.public.django_wrap import django_wrap
from brick.pydata.py_redis.py_SynRedis_tables import py_SynRedis_tables
from brick.classredis.classlisting import classlisting
from brick.classredis.classshopsku import classshopsku
from brick.classredis.classmainsku import classmainsku
# from mymall_app.table.t_mymall_online_info import t_mymall_online_info
from mymall_app.table.t_mymall_online_info_detail import t_mymall_online_info_detail
from mymall_app.views import syndata_by_mymall_api
# from mymall_app.table.t_mymall_cutprice_log import t_mymall_cutprice_log
from skuapp.table.t_store_configuration_file import t_store_configuration_file
from brick.classredis.classsku import classsku
from brick.pricelist.calculate_price import calculate_price

redis_conn = get_redis_connection(alias='product')
py_SynRedis_tables_obj = py_SynRedis_tables()
classsku_obj = classsku()
listingobjs = classlisting(connection, redis_conn)
classshopskuobjs = classshopsku(connection, redis_conn)
classmainsku_obj = classmainsku(connection, redis_conn)


class t_online_info_amazon_listing_Admin(object):
    amazon_listing_plugin = True
    # search_box_flag = True
    # amazon_listing_secondplugin = True

    # site_left_menu_flag = True
    search_box_flag = True
    amazon_site_left_menu_tree_flag = True

    def show_SKU_list(self, obj):
        if obj.is_fba == 0:
            fba_heard_name = u'FBM'
        elif obj.is_fba == 1:
            fba_heard_name = 'FBA'
        else:
            fba_heard_name = ''
        # rt = u'<table class="table table-condensed" style="text-align:center;">' \
        #      u'<thead>' \
        #      u'<tr bgcolor="#C00">' \
        #      u'<th style="text-align:center;">子SKU</th>' \
        #      u'<th style="text-align:center;">商品状态</th>' \
        #      u'<th style="text-align:center;">可卖天数</th>' \
        #      u'<th style="text-align:center;">店铺SKU</th>' \
        #      u'<th style="text-align:center;">%s库存量</th>' \
        #      u'<th style="text-align:center;">价格</th>' \
        #      u'<th style="text-align:center;">利润率</th>' \
        #      u'</tr>' \
        #      u'</thead><tbody>' % (fba_heard_name)

        rt = '''
            <table class="table table-condensed" style="text-align:center;">
             <thead>
             <tr bgcolor="#C00">
             <th style="text-align:center;">子SKU</th>
             <th style="text-align:center;">商品状态</th>
             <th style="text-align:center;">可卖天数</th>
             <th style="text-align:center;">店铺SKU</th>
             <th style="text-align:center;">%s库存量</th>''' % fba_heard_name

        if obj.is_fba == 1:
            rt += '<th style="text-align:center;">到货时间</th>'

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
            elif obj.is_fba == 1:
                shopskuQuantity = obj.afn_warehouse_quantity
            else:
                shopskuQuantity = ''
            shopskuPrice = obj.price
            shopskuShipping = obj.shipping_price
            shopskuStatus = obj.Status
            goodsstatus = sinfor['SKUKEY'][1]
            if sinfor['SKUKEY'][1] == '1':
                goodsstatus = u'正常'
            elif sinfor['SKUKEY'][1] == '2':
                goodsstatus = u'售完下架'
            elif sinfor['SKUKEY'][1] == '3':
                goodsstatus = u'临时下架'
            elif sinfor['SKUKEY'][1] == '4':
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
            else:
                inventory_html = u'<td>%s</td>' % shopskuQuantity
                receive_date_html = ''
            # u'<td>%s</td>' \
            # u'<td style="BORDER-RIGHT: #DDDDDD 1px solid;">%s</td></tr>' % \
            # rt = u'%s <tr %s>' \
            #      u'<td>%s</td>' \
            #      u'<td>%s</td>' \
            #      u'<td>%s</td>' \
            #      u'<td style="BORDER-LEFT: #DDDDDD 1px solid;">%s</td>' + inventory_html
            #      # u'<td><a><span id="inventory_%s">%s</span></a></td>' \
            #      u'<td>%s</td>' \
            #      u'<td><a><span id="%s">%s</span></a></td>' % \
            #      (rt, style, sinfor['SKU'],
            #       # sinfor['SKUKEY'][0],
            #       goodsstatus,
            #       # inventory, occupyNum, int(inventory) - int(occupyNum),
            #       can_sold_days,  sinfor['ShopSKU'].replace('<', '&lt;').replace('>', '&gt;'),
            #       obj.id,shopskuQuantity, shopskuPrice, profit_id, profitrate)

            rt = '''
                %s <tr %s>
                 <td>%s</td>
                 <td>%s</td>
                 <td>%s</td>
                 <td style="BORDER-LEFT: #DDDDDD 1px solid;">%s</td>
                 %s
                 %s
                 <td>%s</td>
                 <td>%s</td>
                 <td><a><span id="%s">%s</span></a></td></tr>
            ''' % (rt, style,
                   sinfor['SKU'],
                   goodsstatus,
                   can_sold_days,
                   sinfor['ShopSKU'].replace('<', '&lt;').replace('>', '&gt;'),
                   inventory_html,
                   receive_date_html,
                   shopskuPrice,
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
                                   content: "/show_inventory_detail/?seller_sku=%s",
                                   btn: ["关闭页面"],
                                   });
                               })
                           </script>
                           ''' % (obj.id, seller_sku)

        rt += u"</tbody></table>"

        return mark_safe(rt)

    show_SKU_list.short_description = mark_safe('<p align="center"style="color:#428bca;">子SKU</p>')

    def show_7days_order(self, obj):
        order_7day = 0
        t_amazon_cpc_ad_obj = t_amazon_cpc_ad.objects.filter(seller_sku=obj.seller_sku)
        if t_amazon_cpc_ad_obj:
            order_7day = t_amazon_cpc_ad_obj[0].orders_7days
        return mark_safe(order_7day)

    show_7days_order.short_description = u'<span style="color:#428BCA">7天order数</span>'

    def show_image_url(self, obj):
        if obj.Status == 'Incomplete':
            rt = '<div style="display: inline-block;width: 0;height: 0; line-height: 0;border: 8px solid transparent; border-top-color: #7a7c76; border-bottom-width: 0;"></div><span style="padding-left: 20px">变体</span>'
        else:
            url = u'%s' % obj.image_url
            rt = '<img src="%s"  width="69" height="69"  alt = "%s"  title="%s"  />' % (url, url, url)
        return mark_safe(rt)

    show_image_url.short_description = u'<span style="color:#428BCA">图片</span>'

    def show_Item_name_and_product_id(self, obj):
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

        l = obj.item_name.split(' ')
        aa = len(l)
        ll = ''
        rt = ''
        if aa <= 6:
            rt = u'%s<br>店铺:%s<br><a href="%sdp/%s" target="_blank">%s</a>' % (obj.item_name, obj.ShopName, site_url, obj.asin1, obj.asin1)
        elif aa > 6:
            newe_Title_list = []
            isSupplierID = ''
            for i in range(0, len(l), 6):
                min_list = ''
                for a in l[i:i + 6]:
                    min_list = u'%s%s ' % (min_list, a)
                newe_Title_list.append(min_list)
            for newe_Title in newe_Title_list:
                ll = u'%s%s<br>' % (ll, newe_Title)
            rt = u'%s<br>店铺:%s<br><a href="%sdp/%s" target="_blank">%s</a>' % (ll, obj.ShopName, site_url, obj.asin1, obj.asin1)
        return mark_safe(rt)

    show_Item_name_and_product_id.short_description = u'<span style="color:#428BCA; width:200px">标题/产品ID</span>'

    def show_sku(self, obj):
        rt = ''
        if obj.Status == 'Incomplete':  # 主体
            pass
        else:
            shopsku = obj.seller_sku
            sku = None
            # sku = classshopskuobjs.getSKU(shopsku)
            rt = u'<table style="text-align:center;" border="1px" bordercolor="#CCCACA" cellpadding="3" cellspacing="1" bgcolor="#c1c1c1"">' \
                 u'<tr style="color: #7a7c76"><td>商品SKU</td><td>采购未入库</td><td>状态</td><td>库存</td><td>占用</td><td>可用数量</td><td>可售天数</td>' \
                 u'<td>店铺SKU</td><td>库存量</td><td>价格</td><td>运费</td><td>状态</td></tr>'
            t_shopsku_information_binding_obj = t_shopsku_information_binding.objects.filter(ShopSKU=obj.seller_sku)
            if t_shopsku_information_binding_obj.exists():
                sku = t_shopsku_information_binding_obj[0].SKU
            if sku:
                # inventory = py_SynRedis_pub_obj.getFromHashRedis('', sku, 'Number') # 商品库存
                inventory = classsku_obj.get_number_by_sku(sku)  # 商品库存
                if inventory is None or inventory == -1:
                    inventory = 0
                else:
                    inventory = str(inventory).split('.')[0]
                    if inventory == '':
                        inventory = '0'
                # occupyNum = py_SynRedis_pub_obj.getFromHashRedis('', sku, 'ReservationNum') #商品占用
                occupyNum = classsku_obj.get_reservationnum_by_sku(sku)  # 商品占用
                if occupyNum is None or occupyNum == -1:
                    occupyNum = 0
                else:
                    occupyNum = str(occupyNum).split('.')[0]
                    if occupyNum == '':
                        occupyNum = '0'

                product_status = ''  # 店铺商品状态
                if obj.Status == 'Inactive':
                    product_status = '不可售'
                elif obj.Status == 'Active':
                    product_status = '可售'
                elif obj.Status == 'Incomplete':
                    product_status = ''
                else:
                    product_status = obj.Status
                '''
                rt += u'<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' \
                      u'<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' \
                      u'</table>' %(sku,py_SynRedis_pub_obj.getFromHashRedis('', sku, '19'),
                               py_SynRedis_pub_obj.getFromHashRedis('', sku, 'goodsstatus'),
                               inventory,occupyNum,int(inventory) - int(occupyNum),
                               # py_SynRedis_pub_obj.getFromHashRedis('', sku, 'CanUseCount'),
                               py_SynRedis_pub_obj.getFromHashRedis('', sku, 'CanSaleDay'),
                               shopsku,obj.quantity,obj.price,obj.zshop_shipping_fee,product_status)
                '''
                rt += u'<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' \
                      u'<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' \
                      u'</table>' % (sku, classsku_obj.get_uninstore_by_sku(sku),
                                     classsku_obj.get_goodsstatus_by_sku(sku),
                                     inventory, occupyNum, int(inventory) - int(occupyNum),
                                     classsku_obj.get_cansaleday_by_sku(sku),
                                     shopsku, obj.quantity, obj.price, obj.zshop_shipping_fee, product_status)
            else:
                rt += u'</table>'
        return mark_safe(rt)

    show_sku.short_description = mark_safe(u'<p style="color:#428BCA" align="center">SKU</p>')

    def show_time(self, obj):

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

        rt = u'最近更新时间:<br>%s <br>操作状态:<br> %s ' % (obj.UpdateTime, action)

        return mark_safe(rt)

    show_time.short_description = mark_safe('<p align="center" style="width:150px;color:#428bca;">时间</p>')

    def show_operations(self, obj):
        syn = u'<a href = "/syndata_by_amazon_api/?operation_type=%s&shopName=%s&seller_sku=%s" style="padding-top: 10px;">同步</a>' % ('sync', obj.ShopName, obj.seller_sku)
        up = u'<br><a href = "/syndata_by_amazon_api/?operation_type=%s&shopName=%s&seller_sku=%s" style=" padding-top: 10px;">上架</a>' % ('upload', obj.ShopName, obj.seller_sku)
        down = u'<br><a href = "/syndata_by_amazon_api/?operation_type=%s&shopName=%s&seller_sku=%s" style=" padding-top: 10px;">下架</a>' % ('download', obj.ShopName, obj.seller_sku)
        change = u'<br><a href = "/syndata_by_amazon_api/?operation_type=%s&pri_id=%s" style=" padding-top: 10px;">修改</a>' % ('change', obj.id)
        # rt = syn + up + down + change
        rt = change
        return mark_safe(rt)

    show_operations.short_description = u'操作'

    # def show_order(self, obj):
    #     rt = ''
    #     if obj.Status == 'Incomplete':  # 主体
    #         pass
    #     else:
    #         rt = u'<table style="text-align:center;" border="1" bordercolor="#CCCACA" cellpadding="3" cellspacing="1" bgcolor="#c1c1c1"">' \
    #              u'<tr style="color: #7a7c76"><td>昨日销量</td><td>今日销量</td><td>销量差值</td><td>7天销量</td><td>总销量</td></tr>' \
    #              u'<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' \
    #              u'</table>' % (obj.orderydays, obj.ordertdays, obj.ordercdays, obj.order7days, obj.allorder)
    #     return mark_safe(rt)
    # show_order.short_description = mark_safe(u'<p style="color:#428BCA" align="center">销量</p>')

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

    # def show_product_status(self,obj) :
    #     if obj.Status == 'Inactive':
    #         product_status = '不可售'
    #     elif obj.Status == 'Active':
    #         product_status = '可售'
    #     elif obj.Status == 'Incomplete':
    #         product_status = ''
    #     else:
    #         product_status = obj.Status
    #     return mark_safe(product_status)
    # show_product_status.short_description = u'产品状态'

    # list_display = ('id', 'show_image_url', 'show_Item_name_and_product_id','asin1','quantity','seller_sku','price','ShopName','show_order','show_deal_result','show_product_status','UpdateTime')# , 'show_operations')
    list_display = ('id', 'show_image_url', 'show_Item_name_and_product_id', 'orders_7days', 'Status', 'show_SKU_list', 'show_time', 'show_operations')
    search_fields = None
    list_filter = None

    # actions = ['batch_update_data_by_api', 'batch_en_data_by_api', 'batch_dis_data_by_api']

    def batch_update_data_by_api(self, request, queryset):
        """
        shop_sku为店铺下的seller_sku列表：
            {'店铺1'：[seller_sku1, seller_sku2], '店铺2'：[seller_sku3, seller_sku4]}
        """
        print request.user.username

        shop_sku = {}
        for record in queryset.all():
            t_online_info_amazon_ins = t_online_info_amazon.objects.filter(id=record.id)
            seller_sku = record.seller_sku
            shop_name = record.ShopName
            if not shop_sku.has_key(shop_name):
                shop_sku[shop_name] = [seller_sku]
            else:
                shop_sku[shop_name].append(seller_sku)
            t_online_info_amazon_ins.update(deal_action='refresh_product',
                                            deal_result=None,
                                            deal_result_info=None,
                                            UpdateTime=datetime.datetime.now())
        print shop_sku
        amazon_product_refresh.delay(shop_sku, 'refresh_product')

    batch_update_data_by_api.short_description = u'同步产品数据'

    def batch_en_data_by_api(self, request, queryset):
        print request.user.username
        shop_sku = {}
        for record in queryset.all():
            t_online_info_amazon_ins = t_online_info_amazon.objects.filter(id=record.id)
            seller_sku = record.seller_sku
            shop_name = record.ShopName
            if not shop_sku.has_key(shop_name):
                shop_sku[shop_name] = [seller_sku]
            else:
                shop_sku[shop_name].append(seller_sku)
            t_online_info_amazon_ins.update(deal_action='load_product',
                                            deal_result=None,
                                            deal_result_info=None,
                                            UpdateTime=datetime.datetime.now())
        print shop_sku
        amazon_product_refresh.delay(shop_sku, 'load_product')

    batch_en_data_by_api.short_description = u'产品上架'

    def batch_dis_data_by_api(self, request, queryset):
        print request.user.username
        shop_sku = {}
        for record in queryset.all():
            t_online_info_amazon_ins = t_online_info_amazon.objects.filter(id=record.id)
            seller_sku = record.seller_sku
            shop_name = record.ShopName
            if not shop_sku.has_key(shop_name):
                shop_sku[shop_name] = [seller_sku]
            else:
                shop_sku[shop_name].append(seller_sku)
            t_online_info_amazon_ins.update(deal_action='unload_product',
                                            deal_result=None,
                                            deal_result_info=None,
                                            UpdateTime=datetime.datetime.now())
        print shop_sku
        amazon_product_refresh.delay(shop_sku, 'unload_product')

    batch_dis_data_by_api.short_description = u'产品下架'

    def get_list_queryset(self, ):
        request = self.request
        qs = super(t_online_info_amazon_listing_Admin, self).get_list_queryset()
        is_fba = self.request.GET.get('_p_is_fba', '')

        qs = qs.filter(Status__in=('Active', 'Inactive')).exclude(ShopSite='JP')

        ShopName = request.GET.get('shopname', '')

        SKU = request.GET.get('SKU', '')
        SKU = '' if SKU == '' else SKU.strip().replace(' ', '+').split(',')

        ASIN = request.GET.get('ASIN', '')
        ASIN = '' if ASIN == '' else ASIN.split(',')

        product_sku = request.GET.get('product_sku', '')
        product_sku = '' if product_sku == '' else product_sku.strip().replace(' ', '+').split(',')

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
        product_id = request.GET.get('product_id', '')
        asin1 = request.GET.get('asin1', '')
        seller_sku = request.GET.get('seller_sku', '')
        seller_sku = seller_sku.split(',')
        # if '' in seller_sku:
        #     seller_sku = ''
        # SKU = request.GET.get('SKU', '')
        updatetime_str = request.GET.get('updatetime_str', '')
        updatetime_end = request.GET.get('updatetime_end', '')
        price_str = request.GET.get('priceLift', '')
        # price_end = request.GET.get('priceRight', '')
        shopsite = request.GET.get('searchSite', '')

        if shopsite == 'ALL':
            shopsite = ''
        product_type = request.GET.get('sellingforms')
        if product_type == 'ALL':
            product_type = ''

        searchList = {'ShopName__contains': ShopName, 'item_name__contains': item_name, 'ShopSite__exact': shopsite, 'product_type__exact': product_type,
                      'product_id__exact': product_id, 'asin1__in': ASIN, 'seller_sku__in': SKU,
                      'UpdateTime__gte': updatetime_str, 'UpdateTime__lt': updatetime_end,
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
                      'SKU__in': product_sku,
                      'UpdateTime__gte': date_refresh_start,
                      'UpdateTime__lte': date_refresh_end,
                      'inventory_received_date__gte': date_receive_start,
                      'inventory_received_date__lte': date_receive_end,

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
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                # messages.error(request, ex)
                messages.error(request, u'Please enter the correct content!')
        return qs



