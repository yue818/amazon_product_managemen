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
from pyapp.models import b_goods
from skuapp.table.t_amazon_estimated_fba_fees import t_amazon_estimated_fba_fees
from storeapp.public.show_tort_title import tortwords, show_tort_title
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
    tortwordsdict = {}

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
                    # params = calculate_price(SKU='WF-2304-BK-S').calculate_profitRate_fba(sellingPrice='25.74', PackWeight='245', cm='10*10*10', logistic_way='PT', platformCountryCode='AMAZON-FBA',DestinationCountryCode='US', cp='FFZ')
                    size_obj = t_amazon_estimated_fba_fees.objects.filter(shop_name=obj.ShopName, sku=obj.seller_sku)
                    longest_side,median_side,shortest_side,unit_of_dimension,item_package_weight,unit_of_weight = \
                        (size_obj[0].longest_side, size_obj[0].median_side, size_obj[0].shortest_side,
                         size_obj[0].unit_of_dimension, size_obj[0].item_package_weight, size_obj[0].unit_of_weight) if size_obj.exists() else (0, 0, 0, 0, 0, 0)

                    longest_side, median_side, shortest_side = (float(longest_side)*2.54, float(median_side)*2.54, float(shortest_side)*2.54) if unit_of_dimension == 'inches' else (longest_side, median_side, shortest_side)
                    item_package_weight = float(item_package_weight)*454 if unit_of_weight == 'pounds' else item_package_weight

                    price_all = 0
                    weight_all = 0
                    sku_for_calc = obj.com_pro_sku if obj.com_pro_sku is not None and obj.com_pro_sku != '' else obj.SKU
                    for sku in sku_for_calc.split('+'):
                        sku_this, num = (sku.split('*')[0], sku.split('*')[1]) if len(sku.split('*')) == 2 else (sku, 1)
                        b_goods_obj = b_goods.objects.filter(SKU=sku_this).values('CostPrice', 'Weight')
                        this_price = float(b_goods_obj[0]['CostPrice']) * float(num) if b_goods_obj.exists() else 0
                        this_weight = float(b_goods_obj[0]['Weight']) * float(num) if b_goods_obj.exists() else 0
                        price_all += this_price
                        weight_all += this_weight

                    calculate_price_obj = calculate_price(SKU='', Money=str(price_all), Weight=str(weight_all))
                    profit_result = calculate_price_obj.calculate_profitRate_fba(
                        sellingPrice=str(obj.price),
                        PackWeight=str(item_package_weight),
                        cm=str(longest_side) + '*' + str(median_side) + '*' + str(shortest_side),
                        logistic_way='PT',
                        platformCountryCode='AMAZON-FBA',
                        DestinationCountryCode='US',
                        cp='FFZ')

                    profitrate = profit_result['profit_qxj'] if 'profit_qxj' in profit_result else profit_result['profit_fba']

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
                    zh_sku_obj = t_combination_sku_log.objects.filter(Com_SKU=obj.SKU)
                    if zh_sku_obj:
                        product_sku_html = str(obj.SKU) + '<br/>↓<br/>' + str(zh_sku_obj[0].Pro_SKU)

                if obj.merge_pro_sku is not None and obj.merge_pro_sku != '':
                    product_sku_html += '<br/>↓<br/>' + str(obj.merge_pro_sku)

                goods_status_html = goodsstatus
                if obj.SKU is not None and obj.SKU != '' and (obj.SKU[0:2] == 'ZH' or '+' in obj.SKU) and obj.product_status != '1':
                    goods_status_html = str(goodsstatus) + '<br/>↓<br/>' + str(obj.generic_keywords5)

                rt = '''
                    %s <tr %s>
                     <td style="word-break:break-all;">%s</td>
                     <td style="word-break:break-all;">%s</td>
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
                       goods_status_html,
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
                if obj.is_fba != 1:
                    rt = u"%s<script>$('#%s').on('click',function()" \
                         u"{layer.open({type:2,skin:'layui-layer-lan',title:'算价表'," \
                         u"fix:false,shadeClose: true,maxmin:true,area:['1300px','900px']," \
                         u"content:'/price_list/?SKU=%s&sellingPrice=%s&platformCountryCode=%s&DestinationCountryCode=%s',});});" \
                         u"</script>" % (rt, profit_id, sinfor['SKU'], shopskuPrice, 'AMAZONGNZF', CountryCode)

                seller_sku = urllib.quote(obj.seller_sku.decode('gbk', 'replace').encode('utf-8', 'replace'))
                if obj.is_fba == 1:
                    rt += '''<script> $('#%s').on('click',
                                    function() {
                                        layer.open({
                                            type: 2,
                                            skin: 'layui-layer-lan',
                                            title: '算价表',
                                            fix: false,
                                            shadeClose: true,
                                            maxmin: true,
                                            area: ['1300px', '900px'],
                                            content: '/price_list_new/?SKU=%s&Money=%s&Weight=%s&sellingPrice=%s&PackWeight=%s&cm=%s&logistic_way=%s&platformCountryCode=%s&DestinationCountryCode=%s&cp=%s',
                                        });
                                    }); </script>
                    ''' % (profit_id, '', str(price_all), str(weight_all), str(obj.price), str(item_package_weight),
                           str(longest_side) + '*' + str(median_side) + '*' + str(shortest_side), 'PT', 'AMAZON-FBA', 'US', 'FFZ')
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
            rt = '/price_list_new/?SKU=%s&Money=%s&Weight=%s&sellingPrice=%s&PackWeight=%s&cm=%s&logistic_way=%s&platformCountryCode=%s&DestinationCountryCode=%s&cp=%s' % ('', str(price_all), str(weight_all), str(obj.price), str(item_package_weight),
                           str(longest_side) + '*' + str(median_side) + '*' + str(shortest_side), 'PT', 'AMAZON-FBA', 'US', 'FFZ')
            rt += traceback.format_exc()
        return mark_safe(rt)
    show_sku_list.short_description = mark_safe('<p align="center"style="color:#428bca;">子SKU</p>')

    def show_image_url(self, obj):
        if obj.Status == 'Incomplete':
            rt = '<div style="display: inline-block;width: 0;height: 0; line-height: 0;border: 8px solid transparent; border-top-color: #7a7c76; border-bottom-width: 0;"></div><span style="padding-left: 20px">变体</span>'
        else:
            url = u'%s' % obj.image_url
            rt = '<img src="%s"  width="69" height="69"  alt = "%s"  title="%s"  />' % (url, url, url)
        if obj.ShopName in ('AMZ-0013-GBY-US/PJ','AMZ-0017-LXY-US/PJ','AMZ-0052-Bohonan-US/PJ','AMZ-0056-Chengcaifengye01-US/PJ','AMZ-0061-Peoria-US/PJ','AMZ-0078-Fuyamp-US/PJ','AMZ-0099-Fuguan-US/PJ','AMZ-0143-KZXX-US/PJ','AMZ-0145-SH-US/PJ','AMZ-0152-DL-US/PJ','AMZ-0154-HY-US/PJ','AMZ-0162-ZS-US/PJ','AMZ-0173-XL-US/PJ','AMZ-0182-FXXR-JP/HF','AMZ-0186-BL-US/HF','AMZ-0208-CHT-US/HF','AMZ-9900-YWGM-US/HF', 'AMZ-0084-Solvang-US/PJ','AMZ-0006-ZYN-US/PJ','AMZ-0222-SY-DE/HF'):
            rt += '<div title="跟卖" style="float:left;width: 20px;height: 20px;background-color: #FFCC33;text-align: center;line-height: 20px;border-radius: 4px; font-weight:bold;">跟</div>'
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
        rt = u'<div style="max-width: 300px;">{}</div>'.format(show_tort_title(obj.item_name, self.tortwordsdict))
        rt += u'<br>店铺:%s<br>店长/销售员:%s<br>销售排名：%s<br><a href="%sdp/%s" target="_blank">%s</a><br/>' % ( obj.ShopName, obj.seller, obj.sale_rank, site_url, obj.asin1, obj.asin1)

        #  轻小件标识展示
        if obj.lg_flag > 0:
            if obj.lg_flag == 1:
                _rt = u' <div title="轻小件已注册" style="float:left;width: 80px;height: 20px;background-color: #7FFF00;text-align: center;line-height: 20px;border-radius: 4px">轻小件已注册</div><br/>'
            elif obj.lg_flag == 2:
                _rt = u' <div title="轻小件可注册" style="float:left;width: 80px;height: 20px;background-color: #00BFFF;text-align: center;line-height: 20px;border-radius: 4px">轻小件可注册</div><br/>'
            elif obj.lg_flag == 3:
                _rt = u' <div title="轻小件销量不足" style="float:left;width: 100px;height: 20px;background-color: #FF4500;text-align: center;line-height: 20px;border-radius: 4px">轻小件销量不足</div><br/>'
            elif obj.lg_flag == 4:
                _rt = u' <div title="轻小件库存过高" style="float:left;width: 100px;height: 20px;background-color: #FFD700;text-align: center;line-height: 20px;border-radius: 4px">轻小件库存过高</div><br/>'
            else:
                _rt = u' <div title="不建议注册轻小件" style="float:left;width: 100px;height: 20px;background-color: #FFFF80;text-align: center;line-height: 20px;border-radius: 4px">不建议注册轻小件</div><br/>'

            rt += _rt
        elif obj.is_fba == 1 and obj.ShopSite in ('US', 'UK', 'DE', 'JP') and obj.product_size_tier:
            if 'Oversize' in obj.product_size_tier:
                size_tier = u'大件'
            else:
                size_tier = u'标件'

            _rt = u' <div title="%s" style="float:left;width: 30px;height: 20px;background-color: #AAAAAA;text-align: center;line-height: 20px;border-radius: 4px">%s</div><br/>'%(obj.product_size_tier, size_tier)

            rt += _rt

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

        # rt_test = u'<div style="max-width: 300px;">{}</div>'.format(show_tort_title(obj.item_name, self.tortwordsdict))
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
                if obj.online_upload_flag == 1:
                    upload_html = u'<br>刊登(online):%s' % obj.upload_time.strftime('%Y-%m-%d')
                elif obj.online_upload_flag == 0:
                    upload_html = u'<br>刊登(绑):%s' % obj.upload_time.strftime('%Y-%m-%d')
            else:
                upload_html = u'<br>刊登(无)'
            rt = u'最近更新时间:<br>%s %s<br>操作状态:<br> %s ' % (obj.UpdateTime, upload_html, action)
        except Exception as e:
            rt = ''
        return mark_safe(rt)
    show_time.short_description = mark_safe('<p align="center" style="width:150px;color:#428bca;">时间</p>')

    def product_change(self, obj):
        if check_permission_legality(self):
            # return u'<br><a href = "/syndata_by_amazon_api/?operation_type=%s&pri_id=%s" style=" padding-top: 10px;">修改</a>' % ('change', obj.id)
            # <a href = "/syndata_by_amazon_api/?operation_type=change&ShopName=%s&seller_sku=%s" style=" padding-top: 10px;">修改</a>
            sku_str = urllib.quote(str(obj.seller_sku).decode('gbk', 'replace').encode('utf-8', 'replace'))
            return '''<a href = "/syndata_by_amazon_api/?operation_type=change&ShopName=%s&seller_sku=%s" style=" padding-top: 10px;">修改</a>
                          <br/>
                          <a onclick="enable_id_%s(\'%s\', \'%s\')">上架</a>
                          <script>
                            function enable_id_%s(ShopName, seller_sku) {
                                to_lock(1);
                                layer.confirm(seller_sku + '  请问确定要进行上架吗？',
                                    {
                                        btn: ['确定','取消'],
                                        btn1:function(){
                                           
                                            $.get(
                                                "/syndata_by_amazon_api/",
                                                {'operation_type':'load','ShopName':ShopName,'seller_sku':seller_sku},
                                                 function(data){
                                                    window.location.href = window.location.href;
                                                 }
                                             );
                                        },
                                        end:function(){
                                            to_lock(0);
                                        }
                                    }
                                );
                            }
                          </script>
                        
                          <br />
                          <a onclick="disable_id_%s(\'%s\', \'%s\')">下架</a>
                          <script>
                            function disable_id_%s(ShopName, seller_sku) {
                                to_lock(1);
                                layer.confirm(seller_sku + '  请问确定要进行下架吗？',
                                    {
                                        btn: ['确定','取消'],
                                        btn1:function(){
                                            $.get(
                                                "/syndata_by_amazon_api/",
                                                {'operation_type':'unload','ShopName':ShopName,'seller_sku':seller_sku},
                                                 function(data){
                                                    window.location.href = window.location.href;
                                                 }
                                             );
                                        },
                                        end:function(){
                                            to_lock(0);
                                        }
                                    }
                                );
                            }
                          </script>''' % (obj.ShopName, sku_str, obj.id, obj.ShopName, obj.seller_sku, obj.id, obj.id, obj.ShopName, obj.seller_sku,obj.id,)
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

    actions = ['to_excel', 'get_stocking_demand', 'deal_tort_word',  'change_price', 'load_amazon_products']

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
        from skuapp.table.t_amazon_auto_load import t_amazon_auto_load
        import uuid

        syn_type = request.POST.get('syn_type', '')
        batch_id = str(uuid.uuid4())
        shop_sku = {}
        sku_str = ''
        if syn_type == 'load':  # 产品上架
            refresh_type = 'auto_load_product'
            upload_record_list = list()
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
                    upload_record_list.append(t_amazon_auto_load(batch_id=batch_id, shop_name=obj.ShopName, seller_sku=obj.seller_sku, status=obj.Status, insert_time=datetime.datetime.now(), deal_type='load', deal_user=request.user.username))
            t_amazon_auto_load.objects.bulk_create(upload_record_list)
        elif syn_type == 'unload':  # 产品下架
            refresh_type = 'auto_unload_product'
            unload_record_list = list()
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
                    unload_record_list.append(t_amazon_auto_load(batch_id=batch_id, shop_name=obj.ShopName, seller_sku=obj.seller_sku, status=obj.Status, insert_time=datetime.datetime.now(), deal_type='unload', deal_user=request.user.username))
            t_amazon_auto_load.objects.bulk_create(unload_record_list)

        for key, value in shop_sku.items():
            get_auth_info_ins = GetAuthInfo(connection)
            auth_info = get_auth_info_ins.get_auth_info_by_shop_name(str(key))
            auth_info['IP'] = auth_info['ShopIP']
            auth_info['table_name'] = 't_online_info_amazon'
            auth_info['update_type'] = refresh_type
            auth_info['product_list'] = value
            auth_info['batch_id'] = batch_id

            if refresh_type == 'auto_load_product':
                feed_xml_ins = GenerateFeedXml(auth_info)
                feed_xml = feed_xml_ins.get_inventory_xml(value, 999)
            elif refresh_type == 'auto_unload_product':
                feed_xml_ins = GenerateFeedXml(auth_info)
                feed_xml = feed_xml_ins.get_inventory_xml(value, 0)
            else:
                feed_xml = None

            auth_info['feed_xml'] = feed_xml

            message_to_rabbit_obj = MessageToRabbitMq(auth_info, connection)
            auth_info = json.dumps(auth_info)
            message_to_rabbit_obj.put_message(auth_info)

        if refresh_type == 'auto_load_product':
            messages.success(request, '商品上架中')
        elif refresh_type == 'auto_unload_product':
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

    def get_stocking_demand(self, request, queryset):
        from pyapp.models import b_goods
        from pyapp.models import B_Supplier
        from skuapp.table.t_stocking_demand_fba import t_stocking_demand_fba
        from skuapp.table.t_stocking_demand_fba_detail import t_stocking_demand_fba_detail
        from django.db.models import Sum
        from brick.pydata.py_syn.py_conn import py_conn

        demand_record = list()
        detail_record = list()
        fail_record = list()
        row = 0
        for obj in queryset:
            try:
                inventory_objs = t_online_amazon_fba_inventory.objects.filter(sku=obj.seller_sku, ShopName=obj.ShopName)
                if inventory_objs.exists():
                    afn_total_quantity = inventory_objs[0].afn_total_quantity
                else:
                    afn_total_quantity = 0
                product_sku = obj.com_pro_sku if (obj.com_pro_sku is not None and obj.com_pro_sku != '') else obj.SKU
                if product_sku:
                    for product_sku_each in product_sku.split('+'):
                        row += 1
                        product_sku_for_query = product_sku_each.split('*')[0]
                        # 备货计划号(一键备货的，在序号前加0)
                        stocking_plan_number = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '_0' + str(row)
                        # 获取商品图片、商品名称、商品成本价、商品重量、供应商链接、供应商名
                        py_b_goods_objs = b_goods.objects.filter(SKU=product_sku_for_query)
                        if py_b_goods_objs.exists():
                            product_image = u'http://fancyqube.net:89/ShopElf/images/%s.jpg' % py_b_goods_objs[0].SKU.replace('OAS-', '').replace('FBA-', '')
                            product_name = py_b_goods_objs[0].GoodsName
                            product_price = py_b_goods_objs[0].CostPrice
                            product_weight = py_b_goods_objs[0].Weight
                            supplier_link = py_b_goods_objs[0].LinkUrl
                            buyer = py_b_goods_objs[0].Purchaser
                        py_b_supplier_objs = B_Supplier.objects.filter(NID=py_b_goods_objs[0].SupplierID)
                        if py_b_supplier_objs.exists():
                            supplier = py_b_supplier_objs[0].SupplierName
                        # 目的仓库
                        destination_warehouse = 'FBA-' + str(obj.ShopSite)
                        # 紧急程度
                        level = 'urgent'
                        # 产品性质
                        nature = 'generalcargo'
                        pyconn = py_conn()
                        sqlserver_info = pyconn.py_conn_database()
                        if sqlserver_info['errorcode'] != 0:
                            raise Exception('普元库链接失败，请重新提交;')
                        else:
                            str_sql = "select AttributeName from B_GoodsAttribute where GoodsID = (select nid from B_Goods where SKU='%s')" % product_sku_for_query
                            sqlserver_info['py_cursor'].execute(str_sql)
                            return_result = sqlserver_info['py_cursor'].fetchone()
                            if return_result:
                                if str(return_result[0]).replace(";", "") == u"其余违禁品":
                                    nature = 'contraband'
                                elif str(return_result[0]).replace(";", "") == u"纯电池商品":
                                    nature = 'pureelectric'
                                elif str(return_result[0]).replace(";", "") == u"内置电池商品" or str(return_result[0]).replace(";", "") == u"带电商品" or str(return_result[0]).replace(";", "") == u"纽扣电池商品":
                                    nature = 'withelectric'
                                elif str(return_result[0]).replace(";", "") == u"粉末商品" or str(return_result[0]).replace(";", "") == u"其余化妆品":
                                    nature = 'powderpaste'
                                elif str(return_result[0]).replace(";", "") == u"带磁商品":
                                    nature = 'withmagnetism'
                                elif str(return_result[0]).replace(";", "") == u"液体商品":
                                    nature = 'liquid'
                                elif str(return_result[0]).replace(";", "") == u"普货":
                                    nature = 'generalcargo'
                                else:
                                    nature = 'specialclass'
                            else:
                                nature = 'generalcargo'
                        pyconn.py_close_conn_database()

                        amazon_factory = 'no'
                        stocking_neworold = '2'

                        # 建议采购数量=4*7天销量-库存量-采购未入库量-FBA系统正在备货数量
                        # number = classsku_obj.get_number_by_sku(product_sku_for_query)
                        number = afn_total_quantity
                        uninstore = classsku_obj.get_uninstore_by_sku(product_sku_for_query)
                        stocking_already_obj = t_stocking_demand_fba.objects.filter(ProductSKU=product_sku_for_query,
                                                                                    Status__in=('completegenbatch', 'genbatch', 'purchasing', 'check'))
                        stocking_already = 0
                        if stocking_already_obj.exists():
                            stocking_already = stocking_already_obj.aggregate(Sum('Stocking_quantity'))['Stocking_quantity__sum']

                        messages.success(request, product_sku_for_query+': 7天销量 %s, 库存 %s, 采购未入库 %s, FBA系统正在备货 %s' % (str(obj.orders_7days), str(number), str(uninstore), str(stocking_already)))

                        stocking_quantity = 4 * (0 if obj.orders_7days is None or obj.orders_7days == '' else obj.orders_7days) - int(number) - int(uninstore) - int(stocking_already)
                        stocking_quantity = 0 if stocking_quantity < 0 else stocking_quantity

                        demand_record.append(t_stocking_demand_fba(
                            Stocking_plan_number=stocking_plan_number,  Stock_plan_date=datetime.datetime.now(),
                            Demand_people=request.user.first_name, ProductSKU=product_sku_for_query,
                            ProductImage=product_image,  ProductName=product_name,
                            ProductPrice=product_price, ProductWeight=product_weight, Supplier=supplier,
                            Supplierlink=supplier_link,  Buyer=buyer, Status='notgenpurchase',
                            Stocking_quantity=stocking_quantity, QTY=stocking_quantity,
                            Destination_warehouse=destination_warehouse,
                            AccountNum=obj.ShopName, Site='', level=level, Product_nature=nature,
                            Remarks='stocking from listing', ShopSKU=obj.seller_sku, neworold=stocking_neworold,
                            AmazonFactory=amazon_factory, Number=int(number), lg_flag=obj.lg_flag, isCheck='0'
                        ))
                        detail_record.append(t_stocking_demand_fba_detail(ProductSKU=product_sku_for_query,
                                                                          Stocking_plan_number=stocking_plan_number,
                                                                          CreateDate=datetime.datetime.now(), Status='notgenpurchase',
                                                                          AuditFlag=0))
            except Exception as e:
                # import traceback
                # messages.error(request, str(traceback.format_exc()))
                fail_record.append(obj.seller_sku)
                continue

        fail_str = ''
        if fail_record:
            for fail in fail_record:
                fail_str = fail_str + fail + ','
            messages.error(request, '以下商品一键备货异常：%s' % fail_str[:-1])

        if len(queryset) != len(fail_record):
            t_stocking_demand_fba.objects.bulk_create(demand_record)
            t_stocking_demand_fba_detail.objects.bulk_create(detail_record)
            messages.success(request, '一键备货结果:' + '<a href = "/Project/admin/skuapp/t_stocking_demand_fba/?Status=notgenpurchase&_p_Remarks=stocking%20from%20listing" target = "_blank" > 备货记录 </a>')
    get_stocking_demand.short_description = u'一键备货'

    def deal_tort_word(self, request, queryset):
        for obj in queryset:
            obj.tortflag = 2
            obj.save()
        # tortremark = request.POST.get('batch_remark_text')
        # for i, obj in enumerate(objs):
        #     if obj.Status == 'Enabled' and obj.TortFlag == 1:
        #         if not obj.Remarks and not tortremark:
        #             messages.error(request, u'ProductID: {}, 修改侵权处理标记前，请输入备注！'.format(obj.ProductID))
        #         else:
        #             obj.Remarks = u'{};{}'.format(obj.Remarks, tortremark)
        #             obj.TortFlag=2
        #             obj.save()
        #     if i >= 20:
        #         break
    deal_tort_word.short_description = u'修改侵权词处理标记'

    list_display = ('id', 'show_image_url', 'show_item_name_and_product_id', 'show_order', 'Status', 'show_sku_list', 'show_time', 'action_remark', 'show_operations')
    search_fields = None
    list_filter = None
    list_editable = ('action_remark',)

    def get_list_queryset(self, ):
        self.tortwordsdict = tortwords(connection, redis_conn)
        # messages.info(self.request, u'{}'.format(self.tortwordsdict))

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
        product_status = '' if product_status == '' else product_status.strip().replace(' ', '+').split(',')

        orders_refund_total_start = request.GET.get('orders_refund_total_start', '')
        orders_refund_total_end = request.GET.get('orders_refund_total_end', '')
        refund_rate_start = request.GET.get('refund_rate_start', '')
        refund_rate_end = request.GET.get('refund_rate_end', '')

        product_size_tier = request.GET.get('product_size_tier', '')
        shop_site = request.GET.get('shop_site', '')

        shop_follow = request.GET.get('shop_follow', '')
        lg_flag = request.GET.get('lgflag', '')
        upload_time_start = request.GET.get('upload_time_start', '')
        upload_time_end = request.GET.get('upload_time_end', '')

        package_weight_start = request.GET.get('package_weight_start', '')
        package_weight_end = request.GET.get('package_weight_end', '')

        riskgrade = request.GET.get('riskgrade')  # 侵权风险等级
        risklist = []
        if riskgrade == '3':
            risklist = [8, 9, 10, 11, 12, 13, 14, 15]  # 绝对禁止
        elif riskgrade == '2':
            risklist = [4, 5, 6, 7, 12, 13, 14, 15]  # 限定范围
        elif riskgrade == '1':
            risklist = [2, 3, 6, 7, 10, 11, 14, 15]  # 潜在风险
        elif riskgrade == '0':
            risklist = [1, 3, 5, 7, 9, 11, 13, 15]  # 其它
        elif riskgrade == 'o':
            risklist = [1, 2, 3, 4, 5, 6, 7]  # 除了绝对禁止 以外的

        if product_sku:
            qs = qs.filter(Q(SKU__icontains=product_sku)
                           | Q(com_pro_sku__icontains=product_sku)
                           | Q(merge_pro_sku__icontains=product_sku))

        if shop_follow and not ShopName:
            qs = qs.filter(ShopName__exact=shop_follow)

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
                      'upload_time__gte': upload_time_start,
                      'upload_time__lte': upload_time_end,
                      'inventory_received_date__gte': date_receive_start,
                      'inventory_received_date__lte': date_receive_end,
                      'product_status__in': product_status,
                      'seller__exact': seller,
                      'Parent_asin__exact': parent_asin,
                      'SKU__in': product_sku_multi,
                      'orders_refund_total__gte': orders_refund_total_start,
                      'orders_refund_total__end': orders_refund_total_end,
                      'refund_rate__gte': refund_rate_start,
                      'refund_rate__lte': refund_rate_end,
                      'product_size_tier__icontains': product_size_tier,
                      'ShopSite__exact': shop_site,
                      'lg_flag__exact': lg_flag,
                      'package_weight__gte': package_weight_start,
                      'package_weight__lte': package_weight_end,
                      }
        if risklist:
            searchList['RiskGrade__in'] = risklist
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



