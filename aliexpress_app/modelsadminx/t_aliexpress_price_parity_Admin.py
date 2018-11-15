#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime

from django.utils.safestring import mark_safe
from django_redis import get_redis_connection
from django.db.models import Q
from django.db import connection
from django.contrib import messages
from django.http import HttpResponseRedirect

from brick.db.dbconnect import run, execute_db
from brick.public.django_wrap import django_wrap
from brick.pydata.py_redis.py_SynRedis_tables import py_SynRedis_tables
from brick.classredis.classlisting import classlisting
from brick.classredis.classshopsku import classshopsku
from brick.classredis.classmainsku import classmainsku
from brick.pricelist.calculate_price import calculate_price
from brick.aliexpress.aliexpress_import_products import get_aliexpress_profitrate
from app_djcelery.tasks import get_aliexpress_competitor_product_by_request_task
from app_djcelery.tasks import get_aliexpress_product_ratingvalue_by_request_task
# from brick import joom

# from skuapp.table.t_upload_shopname import t_upload_shopname
from skuapp.table.t_store_configuration_file import t_store_configuration_file
from skuapp.table.t_product_enter_ed import t_product_enter_ed
from aliexpress_app.table.t_aliexpress_competitor_product_info import t_aliexpress_competitor_product_info
from aliexpress_app.table.t_aliexpress_price_parity_log import t_aliexpress_price_parity_log
from aliexpress_app.table.t_aliexpress_online_info_detail import t_aliexpress_online_info_detail
# from aliexpress_app.views import get_aliexpress_competitor_product_by_request
# from aliexpress_app.views import get_aliexpress_product_ratingvalue_by_request
from brick.classredis.classsku import classsku
# joom.monkey_patch()
# del joom

redis_conn = get_redis_connection(alias='product')
py_SynRedis_tables_obj = py_SynRedis_tables()
classsku_obj = classsku()
listingobjs = classlisting(connection, redis_conn)
classshopskuobjs = classshopsku(connection, redis_conn)
classmainsku_obj = classmainsku(connection, redis_conn)


class t_aliexpress_price_parity_Admin(object):
    aliexpress_price_parity_plugin = True
    site_left_menu_flag_price_parity_aliexpress = True

    list_display = ['show_Picture', 'show_Title_ProductID', 'Orders7Days', 'Weight', 'our_product_price_range_and_profitrate_range',
                    'priceParity_Status_text', 'priceParity_Datetime',
                    'show_SKU_list', 'show_Competitor_image', 'competitor_ProductID', 'show_competitor_price_range',
                    'show_competitor_Orders7Days', 'priceParity_Remarks', ]

    list_editable = ('competitor_ProductID', 'priceParity_Remarks')
    list_per_page = 20
    list_max_show_all = 200
    list_display_links = ('',)

    actions = [
        'batch_joom_competitor_products',
        'set_joom_product_price_parity_status_wait',
        'set_joom_product_price_parity_status_no',
        'set_joom_product_price_parity_status_todo',
        'batch_joom_price_parity',
    ]

    def has_add_permission(self):
        return False

    def has_delete_permission(self, obj=None):
        return False

    def show_Picture(self, obj):
        url = str(obj.Image).replace('https', 'http')
        rt = '<div><img src="%s" width="120" height="120" alt = "%s" title="%s"/></div>' % (url, url, url)
        return mark_safe(rt)

    show_Picture.short_description = mark_safe(u'<p align="center"style="color:#428bca;">图片</p>')

    def our_product_price_range_and_profitrate_range(self, obj):
        rt = "<span>%s</span><br><br>" % obj.Price
        profitrate = ''
        if obj.ProfitRate:
            profitrate = obj.ProfitRate
        else:
            if obj.Price:
                price = obj.Price
                sku = ''
                if price.find('-') != -1:
                    price = price.replace('-', '~')
                if obj.SKU:
                    sku = obj.SKU.split(',')[0]
                if price and sku:
                    profitrate = get_aliexpress_profitrate(price, sku)
        rt = "%s<span>%s</span>" % (rt, profitrate)
        return mark_safe(rt)

    our_product_price_range_and_profitrate_range.short_description = mark_safe(u'<p align="center"style="color:#428bca;">我方价格($)<br>利润率区间</p>')

    def show_Title_ProductID(self, obj):
        rt = django_wrap(obj.Title, ' ', 6)
        rt = u'%s<br>产品ID:<a href=" https://www.aliexpress.com/item/abc/%s.html" target="_blank">%s</a>' % (rt, obj.ProductID, obj.ProductID)
        rt = u'%s<br>卖家简称:%s' % (rt, obj.ShopName)
        # t_upload_shopname_objs = t_upload_shopname.objects.filter(ShopName=obj.ShopName)
        # if t_upload_shopname_objs.exists():
        #     rt = u'%s<br>铺货人:%s' % (rt, t_upload_shopname_objs[0].uploader)
        # else:
        #     rt = u'%s<br>店长/销售员:%s' % (rt, obj.Seller)
        # rt = u'%s<br>刊登人:%s' % (rt, obj.Seller)
        rt = u'%s<br>比价人:%s' % (rt, obj.priceParity_Person)
        if obj.ratingValue:
            rv = obj.ratingValue / 10.0 / 10.0
        else:
            rv = ''
        rt = u'%s<br>我方商品评分:%s' % (rt, rv)
        return mark_safe(rt)

    show_Title_ProductID.short_description = mark_safe(u'<p align="center"style="color:#428bca;">详情</p>')

    def priceParity_Status_text(self, obj):
        if obj.priceParity_Status == 'WAIT':
            rt = u'正在比价'
        elif obj.priceParity_Status == 'NO':
            rt = u'无需比价'
        elif obj.priceParity_Status == 'TODO':
            rt = u'待比价执行'
        elif obj.priceParity_Status == 'SUCCESS':
            rt = u'完成'
        elif obj.priceParity_Status == 'FAILED':
            rt = u'失败'
        else:
            rt = u''

        return mark_safe(rt)

    priceParity_Status_text.short_description = mark_safe(u'<p align="center"style="color:#428bca;">比价状态</p>')

    def show_time(self, obj):
        rt = u'在线数据刷新:<br>%s' % (obj.RefreshTime)
        for shopsku in obj.ShopSKU.split(','):
            sku = classshopskuobjs.getSKU(shopsku)
            if sku is not None:
                rt = rt + u'<br>商品最近刷新:<br>%s' % (classsku_obj.get_updatetime_by_sku(sku))
                break
        rt = u'%s<br>比价时间:<br>%s' % (rt, obj.priceParity_Datetime)
        return mark_safe(rt)

    show_time.short_description = mark_safe('<p align="center" style="width:150px;color:#428bca;">时间</p>')

    def show_SKU_list(self, obj):
        rt = u'<table class="table table-condensed" style="text-align:center;">' \
             u'<thead>' \
             u'<tr bgcolor="#C00">' \
             u'<th style="text-align:center;">子SKU</th>' \
             u'<th style="text-align:center;">店铺SKU</th>' \
             u'<th style="text-align:center;">库存量</th>' \
             u'<th style="text-align:center;">实际销售价($)</th>' \
             u'<th style="text-align:center;">调后价($)</th>' \
             u'<th style="text-align:center;">我方利润率(%)</th>' \
             u'<th style="text-align:center;">启用状态</th>' \
             u'</tr>' \
             u'</thead><tbody>'
        # u'<th style="text-align:center;">原价($)</th>' \
        # u'<th style="text-align:center;">运费($)</th>' \
        shopskulist = obj.ShopSKU.split(',')
        infor = []
        for i, shopsku in enumerate(shopskulist):
            eachinfor = {}
            eachinfor['SKU'] = classshopskuobjs.getSKU(shopsku)
            # eachinfor['SKUKEY'] = ['19', 'goodsstatus', 'Number', 'ReservationNum', 'CanSaleDay']
            eachinfor['SKUKEY'] = ['NotInStore', 'GoodsStatus', 'Number', 'ReservationNum', 'CanSaleDay']
            eachinfor['ShopSKU'] = shopsku
            eachinfor['ShopSKUKEY'] = ['Quantity', 'Price', 'Shipping', 'Status']
            infor.append(eachinfor)
        # 这里调取redis数据
        num = 0
        sInfors = py_SynRedis_tables_obj.BatchReadRedis(infor)
        aliexpress_product_shop_sku_info = t_aliexpress_online_info_detail.objects.filter(ProductID=obj.ProductID).values('ShopSKU', 'Quantity', 'Price', 'Status', 'RealPrice')
        aliexpress_pro_dict = dict()
        if aliexpress_product_shop_sku_info:
            for i in aliexpress_product_shop_sku_info:
                aliexpress_pro_dict[i['ShopSKU']] = i

        # 判断MainSKU个数确定是否为组合商品
        count_mainsku = 0
        if obj.MainSKU:
            count_mainsku = len(obj.MainSKU.split(','))
        ms_num = 0

        for sinfor in sInfors:
            if count_mainsku > 1:
                ms_num += 1
            else:
                pass

            if ms_num > 5:
                break

            if aliexpress_pro_dict.get(sinfor['ShopSKU']):
                shopskuQuantity = aliexpress_pro_dict[sinfor['ShopSKU']]['Quantity']
                if aliexpress_pro_dict[sinfor['ShopSKU']]['Price']:
                    shopskuPrice = '%.2f' % float(aliexpress_pro_dict[sinfor['ShopSKU']]['Price'])
                else:
                    shopskuPrice = ''
                shopskuStatus = aliexpress_pro_dict[sinfor['ShopSKU']]['Status']
                realprice = aliexpress_pro_dict[sinfor['ShopSKU']]['RealPrice']
            else:
                shopskuQuantity = ''
                shopskuPrice = ''
                shopskuStatus = ''
                realprice = ''

            if not realprice:
                realprice = ''

            newPrice = ''
            try:
                newPrice = t_aliexpress_price_parity_log.objects.get(ProductID=obj.ProductID, ShopSKU=sinfor['ShopSKU'], ChangeFlag='False').NewPrice
            except t_aliexpress_price_parity_log.DoesNotExist:
                pass

            input_id = obj.ProductID + '_' + str(num)
            show_input_res = input_id + '_' + str(num)
            profit_id = show_input_res + '_' + str(num)

            real_price_id = obj.ProductID + '_realprice_' + str(num)
            real_price_input_res = real_price_id + '_' + str(num)

            # shipping_id = obj.ProductID + '_shipping_' + str(num)
            # shipping_input_res = shipping_id + '_' + str(num)
            num += 1

            # shipping_rt = u'<td><input type="text" style="width:40px" id="%s" value=""/><span id="%s"  style="color:#F00"></span></td>' % (shipping_id, shipping_input_res)

            if self.request.get_full_path().find('priceParity_Status=WAIT') != -1:
                realprice_rt = u'<td><input type="text" style="width:40px" id="%s" value="%s" onkeyup="this.value=this.value.replace(/[^\d\.]/g,\'\')"/><span id="%s" style="color:#F00"></span></td>' % (real_price_id, realprice, real_price_input_res)
                input_rt = u'<td><input type="text" style="width:40px" id="%s" value="%s" onkeyup="this.value=this.value.replace(/[^\d\.]/g,\'\')"/><span id="%s" style="color:#F00"></span></td>'
                if not newPrice:
                    if realprice:
                        newPrice = realprice
                    else:
                        newPrice = shopskuPrice
            else:
                input_rt = u'<td id="%s">%s<span id="%s"></span></td>'
                realprice_rt = u'<td id="%s">%s<span id="%s"></span></td>' % (real_price_id, realprice, real_price_input_res)

            if newPrice:
                sellingPrice = float(newPrice.split('-')[0])
            else:
                if shopskuPrice:
                    sellingPrice = float(shopskuPrice)
                else:
                    sellingPrice = ''
            if sellingPrice:
                try:
                    calculate_price_obj = calculate_price(str(sinfor['SKU']))
                    profitrate_info = calculate_price_obj.calculate_profitRate(sellingPrice, platformCountryCode='ALIEXPRESS-RUS', DestinationCountryCode='RUS')
                except:
                    profitrate_info = ''
            else:
                profitrate_info = ''
            if profitrate_info:
                profitrate = '%.2f' % float(profitrate_info['profitRate'])
            else:
                profitrate = ''

            if self.request.get_full_path().find('priceParity_Status=SUCCESS') != -1:
                newPrice = shopskuPrice

            rt_tmp = u'%s <tr bgcolor="#FFFFFF">' \
                     u'<td>%s</td>' \
                     u'<td style="BORDER-LEFT: #DDDDDD 1px solid;">%s</td>' \
                     u'<td>%s</td>' + \
                     realprice_rt + \
                     input_rt + \
                     u'<td><a><span id="%s">%s</span></a></td>' \
                     u'<td style="BORDER-RIGHT: #DDDDDD 1px solid;">%s</td></tr>'
            # u'<td>%s</td>' \
            # shipping_rt + \
            rt = rt_tmp % (rt, sinfor['SKU'], sinfor['ShopSKU'].replace('<', '&lt;').replace('>', '&gt;'),
                           shopskuQuantity,
                           # shopskuPrice,
                           input_id, newPrice, show_input_res,
                           profit_id, profitrate, shopskuStatus)

            rt = u"%s<script>$('#%s').on('click',function()" \
                 u"{layer.open({type:2,skin:'layui-layer-lan',title:'算价表'," \
                 u"fix:false,shadeClose: true,maxmin:true,area:['1300px','900px']," \
                 u"content:'/price_list/?SKU=%s&sellingPrice=%s&platformCountryCode=%s&DestinationCountryCode=%s',});" \
                 "});</script>" % (rt, profit_id, sinfor['SKU'], sellingPrice, 'ALIEXPRESS-RUS', 'RUS')

            if self.request.get_full_path().find('priceParity_Status=WAIT') != -1:
                rt = '%s<script>$(document).ready(function(){$("#%s").blur(function(){' \
                     'var newprice = $("#%s").val();if(newprice!=""){' \
                     '$.ajax({url:"/aliexpress/aliexpress_price_parity/",type:"POST",contentType:"application/x-www-form-urlencoded:charset=UTF-8",' \
                     'dataType: "json",data: {"newprice":newprice,"productid":"%s","ShopSKU":"%s",' \
                     '"oldprice":"%s","person":"%s","SKU":"%s"},' \
                     'success:function(result){var res_mess="";var profitrate="";' \
                     'if(result.resultCode==0){res_mess="SUCCESS";profitrate=result.profitrate;}' \
                     'else if(result.resultCode==-2){res_mess="SAMEPRICE NOCHANGE";}' \
                     'else{res_mess=result.messages;}$("#%s").html(res_mess);$("#%s").html(profitrate);},' \
                     'error:function(XMLHttpRequest,textStatus,errorThrown){' \
                     'alert("错误信息："+XMLHttpRequest.responseText);}' \
                     '});}else{}' \
                     '});});</script>' % (rt, input_id, input_id, obj.ProductID, sinfor['ShopSKU'].replace('<', '&lt;').replace('>', '&gt;').replace('\\', '\\\\'),
                                          shopskuPrice, self.request.user.first_name, sinfor['SKU'], show_input_res, profit_id)

            if self.request.get_full_path().find('priceParity_Status=WAIT') != -1:
                realprice_script = '<script>$(document).ready(function(){$("#%s").blur(' \
                                   'function(){var realprice = $("#%s").val();if(realprice!=""){' \
                                   '$.ajax({url:"/aliexpress/aliexpress_realprice_update/",' \
                                   'type:"POST",contentType:"application/x-www-form-urlencoded:charset=UTF-8",' \
                                   'dataType:"json",data:{"realprice":realprice,"productid":"%s","ShopSKU":"%s","SKU":"%s"' \
                                   '},success:function(result){var res_mess="";var profitrate="";' \
                                   'if(result.resultCode==0){res_mess="SUCCESS";profitrate=result.profitrate;' \
                                   '}else if(result.resultCode==-2){res_mess="SAMEPRICE NOCHANGE";}else{' \
                                   'res_mess=result.messages;}$("#%s").html(res_mess);$("#%s").html(profitrate);},' \
                                   'error:function(XMLHttpRequest,textStatus,errorThrown)' \
                                   '{console.log("错误信息："+XMLHttpRequest.responseText);}});}else{}});});</script>' % \
                                   (real_price_id, real_price_id, obj.ProductID, sinfor['ShopSKU'].replace('<', '&lt;').replace('>', '&gt;').replace('\\', '\\\\'),
                                    sinfor['SKU'], real_price_input_res, profit_id)

                rt = rt + realprice_script

        rt = u'%s</tbody></table>' % (rt)

        if count_mainsku > 1:
            rt += u'<span style="color:#F00">组合商品不进行比价, 最多只显示五条信息</span>'

        return mark_safe(rt)

    show_SKU_list.short_description = mark_safe('<p align="center"style="color:#428bca;">子SKU</p>')

    def show_Competitor_image(self, obj):
        if obj.competitor_ProductID:
            jcp = t_aliexpress_competitor_product_info.objects.get(ProductID=obj.competitor_ProductID)
            url = jcp.Image
            if not url:
                url = ''
            RefreshDate = jcp.RefreshDate
            if not RefreshDate:
                RefreshDate = ''
            LastRefreshDate = jcp.LastRefreshDate
            if not LastRefreshDate:
                LastRefreshDate = ''
            ratingValue = jcp.ratingValue
            RefreshStatus = jcp.RefreshStatus
            if not RefreshStatus:
                RefreshStatus = 'Refresh over. You can refresh again'
            if not ratingValue:
                ratingValue = u'无'
            url = url.replace('https', 'http')
            rt = u'<div><img src="%s" width="120" height="120" alt = "%s" title="%s"/>' % (url, url, url)
            rt = u'%s<br><span>上次刷新时间: %s</span>' % (rt, LastRefreshDate)
            rt = u'%s<br><span>本次刷新时间: %s</span>' % (rt, RefreshDate)
            rt = u'%s<br><span>刷新状态: %s</span>' % (rt, RefreshStatus)
            rt = u'%s<br><span>商品评分: %s</span>' % (rt, ratingValue)
            rt = rt + u'</div>'
        else:
            rt = ''
        return mark_safe(rt)

    show_Competitor_image.short_description = mark_safe('<p align="center"style="color:#428bca;">对手图片</p>')

    def show_competitor_price_range(self, obj):
        # unit = ''
        minPrice = ''
        maxPrice = ''
        minProfitRate = ''
        maxProfitRate = ''
        if obj.competitor_ProductID:
            competitor_info = t_aliexpress_competitor_product_info.objects.get(ProductID=obj.competitor_ProductID)
            # if competitor_info.Unit:
            #     unit = competitor_info.Unit
            if competitor_info.maxPrice:
                maxPrice = competitor_info.maxPrice
                if not maxPrice:
                    maxPrice = ''
            if competitor_info.minPrice:
                minPrice = competitor_info.minPrice
                if not minPrice:
                    minPrice = ''
            if competitor_info.minProfitRate:
                minProfitRate = ('%.2f' % float(competitor_info.minProfitRate)) + '%'
            if competitor_info.maxProfitRate:
                maxProfitRate = ('%.2f' % float(competitor_info.maxProfitRate)) + '%'

            minprice_id = 'minprice_id_' + obj.competitor_ProductID
            minprice_input_res = 'minprice_input_res_' + obj.competitor_ProductID
            maxprice_id = 'maxprice_id_' + obj.competitor_ProductID
            maxprice_input_res = 'maxprice_input_res_' + obj.competitor_ProductID
            minprofit_id = 'minprofit_id_' + obj.competitor_ProductID
            maxprofit_id = 'maxprofit_id_' + obj.competitor_ProductID

            if self.request.get_full_path().find('priceParity_Status=WAIT') != -1:
                rt = u'<span>价格区间: </span><br>'
                rt = u'%s<span>最低价($): </span><input type="text" style="width:40px" id="%s" value="%s" onkeyup="this.value=this.value.replace(/[^\d\.]/g,\'\')"/><span id="%s" ' \
                     u'style="color:#F00"></span><br>' % (rt, minprice_id, minPrice, minprice_input_res)
                rt = u'%s<span>最高价($): </span><input type="text" style="width:40px" id="%s" value="%s" onkeyup="this.value=this.value.replace(/[^\d\.]/g,\'\')"/><span id="%s" ' \
                     u'style="color:#F00"></span>' % (rt, maxprice_id, maxPrice, maxprice_input_res)

                rt = u'%s<br><br><span>利润率区间: </span><span id="%s">%s</span>~<span id="%s">%s</span>' % (rt, minprofit_id, minProfitRate, maxprofit_id, maxProfitRate)

                minprice_rt = u'<script>$(document).ready(function(){$("#%s").blur(' \
                              u'function(){var minprice = $("#%s").val();if(minprice!=""){' \
                              u'$.ajax({url:"/aliexpress/aliexpress_competitor_update/",' \
                              u'type:"POST",contentType:"application/x-www-form-urlencoded:charset=UTF-8",' \
                              u'dataType:"json",data:{"minprice":minprice,"competitor_productid":"%s","productid":"%s",' \
                              u'},success:function(result){var res_mess="";var profitrate="";' \
                              u'if(result.resultCode==0){res_mess="SUCCESS";if(result.hasOwnProperty("profitrate"))' \
                              u'{profitrate=result.profitrate;}}else{' \
                              u'res_mess=result.messages;}$("#%s").html(res_mess);if(profitrate!=""){$("#%s").html(profitrate);}},' \
                              u'error:function(XMLHttpRequest,textStatus,errorThrown)' \
                              u'{alert("错误信息："+XMLHttpRequest.responseText);}});}else{}});});</script>' % \
                              (minprice_id, minprice_id, obj.competitor_ProductID, obj.ProductID, minprice_input_res, minprofit_id)

                maxprice_rt = u'<script>$(document).ready(function(){$("#%s").blur(' \
                              u'function(){var maxprice = $("#%s").val();if(maxprice!=""){' \
                              u'$.ajax({url:"/aliexpress/aliexpress_competitor_update/",' \
                              u'type:"POST",contentType:"application/x-www-form-urlencoded:charset=UTF-8",' \
                              u'dataType:"json",data:{"maxprice":maxprice,"competitor_productid":"%s","productid":"%s",' \
                              u'},success:function(result){var res_mess="";var profitrate="";' \
                              u'if(result.resultCode==0){res_mess="SUCCESS";if(result.hasOwnProperty("profitrate"))' \
                              u'{profitrate=result.profitrate;}}else{' \
                              u'res_mess=result.messages;}$("#%s").html(res_mess);if(profitrate!=""){$("#%s").html(profitrate);}},' \
                              u'error:function(XMLHttpRequest,textStatus,errorThrown)' \
                              u'{alert("错误信息："+XMLHttpRequest.responseText);}});}else{}});});</script>' % \
                              (maxprice_id, maxprice_id, obj.competitor_ProductID, obj.ProductID, maxprice_input_res, maxprofit_id)

                rt = rt + minprice_rt + maxprice_rt
            else:
                rt = u'<span>价格区间: </span><br>'
                rt = u'%s<span>最低价($): </span><span id="%s">%s</span><span id="%s"  style="color:#F00"></span><br>' % (rt, minprice_id, minPrice, minprice_input_res)
                rt = u'%s<span>最高价($): </span><span id="%s">%s</span><span id="%s"  style="color:#F00"></span>' % (rt, maxprice_id, maxPrice, maxprice_input_res)

                rt = u'%s<br><br><span>利润率区间: </span><span id="%s">%s</span>~<span id="%s">%s</span>' % (rt, minprofit_id, minProfitRate, maxprofit_id, maxProfitRate)

        else:
            rt = u''

        return mark_safe(rt)

    show_competitor_price_range.short_description = mark_safe('<p align="center"style="color:#428bca;">对手价格($)/利润率区间</p>')

    def show_competitor_Orders7Days(self, obj):
        Orders7Days = ''
        if obj.competitor_ProductID:
            Orders7Days = t_aliexpress_competitor_product_info.objects.get(ProductID=obj.competitor_ProductID).Orders7Days
            if not Orders7Days:
                Orders7Days = ''

            if self.request.get_full_path().find('priceParity_Status=WAIT') != -1:
                seven_orders_id = 'seven_orders_id_' + obj.competitor_ProductID
                seven_orders_input_res = 'seven_orders_input_res_' + obj.competitor_ProductID
                seven_orders_rt = u'<input type="text" style="width:40px" id="%s" value="%s" onkeyup="this.value=this.value.replace(/[^\d]/g,\'\')"/><span id="%s" style="color:#F00" ' \
                                  u'></span>' % (seven_orders_id, Orders7Days, seven_orders_input_res)
                maxprice_rt = u'<script>$(document).ready(function(){$("#%s").blur(' \
                              u'function(){var sevenorders = $("#%s").val();if(sevenorders!=""){' \
                              u'$.ajax({url:"/aliexpress/aliexpress_competitor_update/",' \
                              u'type:"POST",contentType:"application/x-www-form-urlencoded:charset=UTF-8",' \
                              u'dataType:"json",data:{"sevenorders":sevenorders,"competitor_productid":"%s","productid":"%s",' \
                              u'},success:function(result){var res_mess="";var profitrate="";' \
                              u'if(result.resultCode==0){res_mess="SUCCESS";if(result.hasOwnProperty("profitrate"))' \
                              u'{profitrate=result.profitrate;}}else{' \
                              u'res_mess="FAILED";}$("#%s").html(res_mess);},' \
                              u'error:function(XMLHttpRequest,textStatus,errorThrown)' \
                              u'{alert("错误信息："+XMLHttpRequest.responseText);}});}else{}});});</script>' % \
                              (seven_orders_id, seven_orders_id, obj.competitor_ProductID, obj.ProductID, seven_orders_input_res)

                seven_orders_rt += maxprice_rt
            else:
                seven_orders_rt = u"<span>%s</span>" % Orders7Days
        else:
            seven_orders_rt = ''
        return mark_safe(seven_orders_rt)

    show_competitor_Orders7Days.short_description = mark_safe('<p align="center"style="color:#428bca;">对手7天order数</p>')

    def batch_joom_price_parity(self, request, objs):
        for i, obj in enumerate(objs):
            if obj.priceParity_Status == 'TODO':
                obj.priceParity_Status = "SUCCESS"
                obj.priceParity_Datetime = datetime.datetime.now()
                obj.priceParity_Person = request.user.first_name
                obj.save()

                pp_log = t_aliexpress_price_parity_log.objects.filter(ProductID=obj.ProductID, ChangeFlag='False')
                if pp_log:
                    for i in pp_log:
                        newPrice = i.NewPrice
                        shopsku = i.ShopSKU
                        i.ChangeFlag = 'True'
                        i.OldSales = obj.OfSales
                        i.save()
                        joom_detail_obj = t_aliexpress_online_info_detail.objects.get(ProductID=obj.ProductID, ShopSKU=shopsku)
                        joom_detail_obj.Price = newPrice
                        joom_detail_obj.save()
            else:
                messages.error(request, u'只可以对 待比价执行 商品 比价执行')
                return
        return HttpResponseRedirect('/Project/admin/aliexpress_app/t_aliexpress_price_parity/?priceParity_Status=SUCCESS')

    batch_joom_price_parity.short_description = u'设置选中商品比价执行完成'

    def batch_joom_competitor_products(self, request, objs):
        for obj in objs:
            if obj.competitor_ProductID:
                competitor_product_id = obj.competitor_ProductID
                res = get_aliexpress_competitor_product_by_request_task.delay(competitor_product_id, obj.ProductID)
                # res = get_aliexpress_competitor_product_by_request_task(competitor_product_id, obj.ProductID)
                print res
            else:
                pass
            if obj.ProductID:
                res = get_aliexpress_product_ratingvalue_by_request_task.delay(obj.ProductID)
                # res = get_aliexpress_product_ratingvalue_by_request_task(obj.ProductID)
                print res
            else:
                pass

        messages.success(request, u'正在获取/更新 对手信息, 请稍后刷新页面。。。')

    batch_joom_competitor_products.short_description = u'刷新选中我方&对手商品信息'

    def set_joom_product_price_parity_status_no(self, request, objs):
        for obj in objs:
            obj.priceParity_Status = 'NO'
            obj.priceParity_Datetime = datetime.datetime.now()
            obj.priceParity_Person = request.user.first_name
            obj.save()
        messages.success(request, u'设置选中商品为无需比价商品成功')

    set_joom_product_price_parity_status_no.short_description = u'设置选中商品为无需比价'

    def set_joom_product_price_parity_status_wait(self, request, objs):
        for obj in objs:
            obj.priceParity_Status = 'WAIT'
            obj.save()
        messages.success(request, u'设置选中商品为正在比价商品成功')

    set_joom_product_price_parity_status_wait.short_description = u'设置选中商品为正在比价'

    def set_joom_product_price_parity_status_todo(self, request, objs):
        for obj in objs:
            obj.priceParity_Status = 'TODO'
            obj.save()
        messages.success(request, u'设置选中商品为待比价执行商品成功')

    set_joom_product_price_parity_status_todo.short_description = u'设置选中商品为待比价执行'

    def get_duplicate_pros_by_sevenordernum(self):
        db_res = run({})
        if db_res['errorcode'] == -1:
            print "result['errortext']: %s" % db_res['errortext']
            return

        # sql = "SELECT id FROM (SELECT id, MainSKU FROM t_aliexpress_online_info AS a WHERE Orders7Days=(SELECT MAX(b.Orders7Days) FROM " \
        #     "t_aliexpress_online_info AS b WHERE b.MainSKU IS NOT NULL AND b.MainSKU<>'' AND a.MainSKU = b.MainSKU AND b.`Status`='True' AND " \
        #     "b.ReviewState='approved')) AS c GROUP BY MainSKU"
        sql = "SELECT max(a.id) AS id FROM t_aliexpress_online_info a,( SELECT MAX(b.Orders7Days) AS maxorder7days,b.MainSKU " \
            "FROM t_aliexpress_online_info AS b WHERE b.MainSKU IS NOT NULL AND b.MainSKU <> '' AND b.`Status` = 'True' " \
            "GROUP BY b.MainSKU) c WHERE a.MainSKU=c.MainSKU AND a.Orders7Days=c.maxorder7days GROUP BY a.MainSKU"
        duplicate_infos = execute_db(sql, db_res['db_conn'], 'select')
        ids = list()
        for i in duplicate_infos:
            ids.append(i['id'])
        return ids

    def get_list_queryset(self):
        request = self.request
        qs = super(t_aliexpress_price_parity_Admin, self).get_list_queryset()
        qs = qs.order_by('-Orders7Days')

        search_dict = dict()

        # search_dict['Status__exact'] = 'True'
        search_dict['Status__exact'] = '1'

        priceParity_Status = request.GET.get('priceParity_Status', '')

        if priceParity_Status in ['NO', 'WAIT', 'TODO', 'SUCCESS', 'FAILED']:
            search_dict['priceParity_Status__exact'] = priceParity_Status
        elif priceParity_Status == 'DONE':
            search_dict['priceParity_Status__in'] = ['SUCCESS', 'FAILED']
        elif priceParity_Status == 'ALL':
            # ids = self.get_duplicate_pros_by_sevenordernum()
            # search_dict['pk__in'] = ids
            search_dict['CanPriceParity__exact'] = True
        else:
            pass

        priceOption = request.GET.get('priceOption', '')

        if priceParity_Status == 'ALL' or priceParity_Status == '':
            if priceOption == 'True':
                qs = qs.filter(priceParity_Status__in=['NO', 'WAIT', 'TODO', 'SUCCESS', 'FAILED'])
            elif priceOption == 'False':
                qs = qs.exclude(priceParity_Status__in=['NO', 'WAIT', 'TODO', 'SUCCESS', 'FAILED'])
            else:
                pass

        shopname = request.GET.get('shopname', '').strip()
        productId = request.GET.get('productID', '').strip()
        mainSKU = request.GET.get('mainSKU', '').strip()
        shopsku = request.GET.get('shopsku', '').strip()
        title = request.GET.get('Title', '').strip()
        parityPerson = request.GET.get('parityPerson', '').strip()

        orders7DaysStart = request.GET.get('orders7DaysStart', '')
        orders7DaysEnd = request.GET.get('orders7DaysEnd', '')
        ratingValueStart = request.GET.get('ratingValueStart', '')
        ratingValueEnd = request.GET.get('ratingValueEnd', '')
        JZLTimeStart = request.GET.get('JZLTimeStart', '')  # 主SKU建资料时间
        JZLTimeEnd = request.GET.get('JZLTimeEnd', '')
        WeightStart = request.GET.get('WeightStart', '')
        WeightEnd = request.GET.get('WeightEnd', '')
        priceParityTimeStart = request.GET.get('priceParityTimeStart', '')
        priceParityTimeEnd = request.GET.get('priceParityTimeEnd', '')

        # 主SKU建资料时间
        CrossMainSKU = []
        JZLDict = {}
        if JZLTimeStart != '':
            JZLDict['JZLTime__gte'] = JZLTimeStart
        if JZLTimeEnd != '':
            JZLDict['JZLTime__lte'] = JZLTimeEnd
        if JZLDict:
            for enter_ed in t_product_enter_ed.objects.filter(**JZLDict).values('MainSKU'):
                CrossMainSKU.append(enter_ed['MainSKU'])

        if CrossMainSKU:
            proset = set()
            for online_info in t_aliexpress_online_info_detail.objects.filter(MainSKU__in=CrossMainSKU).values('ProductID'):
                proset.add(online_info['ProductID'])

            if proset:
                qs = qs.filter(ProductID__in=proset)
            else:
                qs = qs.none()

        if shopsku != '':
            t_online_info_objs = t_aliexpress_online_info_detail.objects.filter(ShopSKU=shopsku.strip()).values('ProductID')
            prodilist = set()
            for t_online_info_obj in t_online_info_objs:
                prodilist.add(t_online_info_obj['ProductID'])
            qs = qs.filter(ProductID__in=prodilist)

        if mainSKU != '':
            t_online_info_objs = t_aliexpress_online_info_detail.objects.filter(MainSKU=mainSKU.strip()).values('ProductID')
            prodilist = set()
            for t_online_info_obj in t_online_info_objs:
                prodilist.add(t_online_info_obj['ProductID'])
            qs = qs.filter(ProductID__in=prodilist)

        if ratingValueStart:
            ratingValueStart = str(int(float(ratingValueStart) * 10 * 10))
        if ratingValueEnd:
            ratingValueEnd = str(int(float(ratingValueEnd) * 10 * 10))

        if WeightStart:
            WeightStart = float(WeightStart)
        if WeightEnd:
            WeightEnd = float(WeightEnd)

        searchList = {
            'ShopName__exact': shopname,
            'ProductID__exact': productId,
            'Orders7Days__gte': orders7DaysStart,
            'Orders7Days__lte': orders7DaysEnd,
            'Title__icontains': title,
            'priceParity_Person__exact': parityPerson,
            'Orders7Days__gte': orders7DaysStart,
            'Orders7Days__lte': orders7DaysEnd,
            'ratingValue__gte': ratingValueStart,
            'ratingValue__lte': ratingValueEnd,
            'Weight__gte': WeightStart,
            'Weight__lte': WeightEnd,
            'priceParity_Datetime__gte': priceParityTimeStart,
            'priceParity_Datetime__lte': priceParityTimeEnd,
        }

        searchList.update(search_dict)

        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v:
                    sl[k] = v
        if sl is not None:
            try:
                qs = qs.filter(**sl)
            except Exception:
                messages.error(request, u'输入的查询数据有问题！')

        if request.user.is_superuser or (23, u'组长') in request.user.groups.values_list():
            return qs
        else:
            objs = t_store_configuration_file.objects.filter(
                Q(Seller=request.user.first_name) | Q(Published=request.user.first_name) | Q(
                    Operators=request.user.first_name)).values('ShopName')
            if objs.exists():
                shoplist = []
                for obj in objs:
                    shoplist.append(obj['ShopName'])
                return qs.filter(ShopName__in=shoplist)
            else:
                return qs.none()
