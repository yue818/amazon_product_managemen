# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from django.contrib import messages
import logging
import xadmin
import urllib2
from pyapp.models import b_goods as py_b_goods
from django.db.models import Q
from xadmin.views import ListAdminView,BaseAdminView,ModelFormAdminView
from django_redis import get_redis_connection
from django.db import connection
from urllib import urlencode
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.http import HttpResponse
import json


from storeapp.models import t_online_info_wish_store,t_add_variant_information,t_wish_product_api_log
from skuapp.table.t_store_configuration_file import t_store_configuration_file
from skuapp.table.t_store_marketplan_execution import t_store_marketplan_execution
from skuapp.table.t_wish_pb import t_wish_pb
from skuapp.table.t_upload_shopname import t_upload_shopname
from skuapp.table.t_online_info import t_online_info
from brick.pydata.py_redis.py_SynRedis_tables import py_SynRedis_tables
# from brick.pydata.py_redis.py_SynRedis_pub import py_SynRedis_pub
from brick.public.django_wrap import django_wrap
from brick.classredis.classlisting import classlisting
from brick.classredis.classshopsku import classshopsku
from skuapp.table.t_product_depart_get import t_product_depart_get
from skuapp.table.t_product_enter_ed import t_product_enter_ed
from storeapp.StoreXadmin.t_add_variant_information_admin import t_add_variant_information_admin
from brick.classredis.classsku import classsku
from storeapp.table.t_online_info_wish_fbw import t_online_info_wish_fbw as django_fbw

from storeapp.plugin.t_online_info_wish_store_plugin import t_online_info_wish_store_plugin
from storeapp.plugin.t_online_info_wish_store_secondplugin import t_online_info_wish_store_secondplugin
from storeapp.plugin.syn_the_shop_data_by_api_plugin import syn_the_shop_data_by_api_plugin
from storeapp.plugin.site_left_menu_plugin_wish import site_left_menu_Plugin_wish
from storeapp.plugin.change_shipping_plugin import change_shipping_plugin
from storeapp.plugin.site_left_menu_tree_Plugin_wish import site_left_menu_tree_Plugin_wish

from storeapp.plugin.wish_store_sort_bar_plugin import wish_store_sort_bar_plugin
from storeapp.plugin.help_select_plugin import help_select_plugin

from app_djcelery.tasks import syndata_by_wish_api
from brick.classredis.classprocess_wish import classprocess_wish
from brick.pricelist.calculate_price import calculate_price

from brick.table.t_wish_store_oplogs import t_wish_store_oplogs
from brick.table.t_online_info_wish_fbw import t_online_info_wish_fbw

from storeapp.plugin.wish_listing_readonly import wish_listing_readonly_P
from skuapp.table.t_wish_pb_campaignproductstats import t_wish_pb_campaignproductstats
# from chart_app.table.t_chart_wish_listing_refund_statistics import t_chart_wish_listing_refund_statistics as wish_score
from skuapp.public.check_permission_legality import check_permission_legality
# from brick.wish.wishlisting.refresh_fbw_flag import warehousecode

# from brick.classredis.class_tortword import class_tortword
from storeapp.public.show_tort_title import tortwords, show_tort_title

from datetime import datetime as timetime, timedelta
logger = logging.getLogger('sourceDns.webdns.views')

redis_conn = get_redis_connection(alias='product')
py_SynRedis_tables_obj = py_SynRedis_tables()
# py_SynRedis_pub_obj = py_SynRedis_pub()
classsku_obj = classsku()
listingobjs = classlisting(connection, redis_conn)

classprocess_wish_obj = classprocess_wish(redis_conn)

t_wish_store_oplogs_obj = t_wish_store_oplogs(connection)

t_online_info_wish_fbw_obj = t_online_info_wish_fbw(connection=connection)

fbw_country_code = ['FBW-US', 'FBW-EU']
warehouse_code_list = ['LAX', 'TLL', 'CVG']

class t_online_info_wish_store_Admin(object):
    #syn_data = True
    search_box_flag = True
    wish_listing_secondplugin =True
    # site_left_menu_flag_wish = False
    show_per_page = True
    site_left_menu_tree_flag_wish = True
    sort_bar = True
    help_select = True

    list_per_page = 20
    tortwordsdict = {}
    def tortInfo(self, TortInfo):
        if TortInfo == 'WY':
            rt = u'<div title="Wish侵权" style="float:left;width: 20px;height: 20px;background-color: #FF3333;text-align: center;line-height: 20px;border-radius: 4px">W</div>'
        elif TortInfo == 'N':
            rt = u'<div title="未侵权" style="float:left;width: 20px;height: 20px;background-color: #66FF66;text-align: center;line-height: 20px;border-radius: 4px">N</div>'
        else:
            rt = u'<div title="其他平台侵权" style="float:left;width: 20px;height: 20px;background-color: #FFCC33;text-align: center;line-height: 20px;border-radius: 4px">O</div>'
        return rt

    def status(self, ReviewState):
        if ReviewState == 'approved' or ReviewState == '1':
            rt = '<div title="已批准" style="float:left;width: 20px;height: 20px;background-color: #66FF66;text-align: center;line-height: 20px;border-radius: 4px">已</div>'
        elif ReviewState == 'pending' or ReviewState == '3':
            rt = '<div title="待审核" style="float:left;width: 20px;height: 20px;background-color: #FFCC33;text-align: center;line-height: 20px;border-radius: 4px">审</div>'
        elif ReviewState == 'rejected' or ReviewState == '2':
            rt = '<div title="被拒绝" style="float:left;width: 20px;height: 20px;background-color: #FF3333;text-align: center;line-height: 20px;border-radius: 4px">拒</div>'
        else:
            rt = ''
        return rt

    def rating(self,rating):
        if rating is not None:
            score = rating
            color = '#66FF66'
        else:
            score = ''
            color = 'red'
        rt = '<div title="评分:%s" style="float:left;width: 20px;height: 20px;background-color: %s;' \
             'text-align: center;line-height: 20px;border-radius: 4px">%s</div>' % (score,color, score)
        return rt

    def change_remarks(self,obj):
        remarks = u'<a id="remark_%s" title="点击编辑备注" >备注</a>:<a id="remark_content_%s">%s</a>' % \
                  (obj.id, obj.id, obj.Remarks)

        show_url = 'productid={}'.format(obj.ProductID)
        if not check_permission_legality(self):
            show_url = show_url + '&readonly=readonly'

        remarks_show = u"<script>$('#remark_%s').on('click',function(){to_lock(1);layer.open({type:2,skin:'layui-layer-lan'," \
                       u"title:'编辑备注',fix:false,shadeClose: true,maxmin:true,area:['500px','300px']," \
                       u"content:'/t_online_info_wish/w_remark/?%s',end:function(){to_lock(0);}});});</script>" % (
                       obj.id, show_url)

        return remarks + remarks_show

    def select_wishexpresstype(self,obj):
        if self.request.GET.get('EXPRESS', 'STANDARD') == 'US':
            option = u"<option value =''></option><option value ='real'>真实</option><option value ='virtual'>虚拟</option>"
            if obj.WishExpressType == 'real':
                option = u"<option value =''></option><option value ='real' selected>真实</option>" \
                         u"<option value ='virtual'>虚拟</option>"
            elif obj.WishExpressType == 'virtual':
                option = u"<option value =''></option><option value ='real' >真实</option>" \
                         u"<option value ='virtual' selected>虚拟</option>"

            onchange_text = u"onchange='setExpressType(this,\"%s\")'>" % obj.ProductID
            if not check_permission_legality(self):
                onchange_text = '>'

            wishexpresstype = u"</br></br>" \
                              u"<select class='text-field admintextinputwidget form-control' style='width: 88px;'" + \
                              onchange_text + option + \
                              u"</select>"

            type_show = u"</br><span id='%s'></span>" % obj.ProductID

            return wishexpresstype + type_show

        return ''

    def show_Remarks(self, obj):
        return mark_safe(self.change_remarks(obj) + self.select_wishexpresstype(obj))
    show_Remarks.short_description = mark_safe(u'<p align="center"style="color:#428bca;">备注</br>海外仓类型</p>')

    def show_Picture(self, obj):
        url = u'%s' % str(obj.Image)
        rt = '<div><img src="%s" width="120" height="120"/></div>' % (url,)
        z_url = u'http://fancyqube-wish.oss-cn-shanghai.aliyuncs.com/Wish_Diamonds_pic%5Chuangzuan.png'
        h_url = u'https://fancyqube-wish.oss-cn-shanghai.aliyuncs.com/badge.png'
        if obj.is_promoted == 'True':
            rt = rt + '<div style="float:left"><img src="%s"  width="20" height="20"  alt = "%s"  title="%s" /></div>' % (
            z_url, z_url, obj.is_promoted)
        if obj.WishExpress is not None and obj.WishExpress != '[]':
            rt = rt + '<div style="float:left"><img src="%s"  width="20" height="20"  alt = "%s"  title="%s" /></div>' % (
            h_url, h_url, obj.WishExpress)
        rt = rt + '<div>' + self.tortInfo(obj.TortInfo) + self.status(obj.ReviewState) + self.rating(obj.Rating) + '</div>'
        return mark_safe(rt)

    show_Picture.short_description = mark_safe(u'<p align="center"style="color:#428bca;">图片</p>')

    def show_Title_ProductID(self, obj):
        rt = u'<div style="max-width: 300px;">{}</div>'.format(show_tort_title(obj.Title, self.tortwordsdict))

        rt = u'%s<br>产品ID:<a href=" https://www.wish.com/c/%s" target="_blank">%s</a>'%(rt,obj.ProductID,obj.ProductID)
        if obj.ReviewState == 'rejected' and obj.BeforeReviewState in ['approved', 'pending']:
            rt = rt + u'<br><span style="color:red">拒绝前状态:%s</span>' % obj.BeforeReviewState
        if obj.AdStatus in ['-1', '-2'] and obj.SName != '-1':
            einfor = t_wish_store_oplogs_obj.selectLogsByIDError(obj.ProductID)
            if einfor['errorcode'] == 0:
                rt = rt + u'<br><span style="color:red">异常原因:%s</span>'% '<br>'.join(einfor['einfors'])
        rt = u'%s<br>卖家简称:%s' % (rt, obj.ShopName)
        rt = u'%s<br>店长/销售员:%s' % (rt, obj.Seller)
        rt = u'%s<br>刊登人:%s' % (rt, obj.Published)

        return mark_safe(rt)
    show_Title_ProductID.short_description = mark_safe(u'<p align="center"style="color:#428bca;">详情</p>')

    def show_time(self, obj):
        classshopskuobjs = classshopsku(db_conn=connection, redis_conn=redis_conn, shopname=obj.ShopName)
        rt = u'在线数据刷新:<br>%s <br>上架(UTC):<br>%s <br>平台最近更新(UTC):<br>%s' % \
             (obj.RefreshTime, obj.DateUploaded, obj.LastUpdated)
        for shopsku in listingobjs.getShopSKUList(obj.ProductID):
            sku = classshopskuobjs.getSKU(shopsku)
            if sku is not None:
                # rt = rt + u'<br>商品最近刷新:<br>%s' % (py_SynRedis_pub_obj.getFromHashRedis('', sku, 'KC_updateTime'))
                rt = rt + u'<br>商品最近刷新:<br>%s' % (classsku_obj.get_updatetime_by_sku(str(sku).split('*')[0]))
                break
        return mark_safe(rt)

    show_time.short_description = mark_safe(u'<p align="center" style="width:150px;color:#428bca;">时间</p>')

    def not_fbw_shopsku_attrinfor(self,activeflag,obj):
        try:
            classshopskuobjs = classshopsku(db_conn=connection, redis_conn=redis_conn, shopname=obj.ShopName)
            rt = u'<table class="table table-condensed">' \
                 u'<thead><tr><th></th>' \
                 u'<th>商品SKU</th><th>商品状态</th><th>可卖天数</th>' \
                 u'<th>店铺SKU</th><th>价格</th>'

            if activeflag == 'DE':
                rt = rt + u'<th>德国仓运费</th><th>德国仓库存</th>'
            elif activeflag == 'GB':
                rt = rt + u'<th>英国仓运费</th><th>英国仓库存</th>'
            elif activeflag == 'US':
                rt = rt + u'<th>美国仓运费</th><th>美国仓库存</th>'
            else:
                rt = rt + u'<th>标准仓运费</th><th>标准仓库存</th>'

            rt = rt + u'<th>利润率(%)</th><th>变体状态</th></tr></thead>' \
                      u'<tbody>'
            shopskulist = listingobjs.getShopSKUList(obj.ProductID)
            infor = []
            for i, shopsku in enumerate(shopskulist):
                eachinfor = {}
                eachinfor['SKU'] = classshopskuobjs.getSKU(shopsku)
                eachinfor['SKUKEY'] = ['GoodsStatus', 'CanSaleDay', 'CostPrice', 'Weight']
                eachinfor['ShopSKU'] = shopsku

                if activeflag == 'DE':
                    eachinfor['ShopSKUKEY'] = ['{}.Price'.format(obj.ShopName), '{}.DEShipping'.format(obj.ShopName), '{}.DEQuantity'.format(obj.ShopName),'{}.Shipping'.format(obj.ShopName), '{}.Status'.format(obj.ShopName)]
                elif activeflag == 'GB':
                    eachinfor['ShopSKUKEY'] = ['{}.Price'.format(obj.ShopName), '{}.GBShipping'.format(obj.ShopName), '{}.GBQuantity'.format(obj.ShopName),'{}.Shipping'.format(obj.ShopName), '{}.Status'.format(obj.ShopName)]
                elif activeflag == 'US':
                    eachinfor['ShopSKUKEY'] = ['{}.Price'.format(obj.ShopName), '{}.USShipping'.format(obj.ShopName), '{}.USQuantity'.format(obj.ShopName),'{}.Shipping'.format(obj.ShopName), '{}.Status'.format(obj.ShopName)]
                else:
                    eachinfor['ShopSKUKEY'] = ['{}.Price'.format(obj.ShopName), '{}.Shipping'.format(obj.ShopName), '{}.Quantity'.format(obj.ShopName), '{}.Status'.format(obj.ShopName)]

                infor.append(eachinfor)
            # 这里调取redis数据
            # sInfors = py_SynRedis_tables_obj.BatchReadRedis(infor)
            sInfors = py_SynRedis_tables_obj.readData_Redis_table(infor)
            num = 0
            for a,sinfor in enumerate(sInfors):
                fbw_flag = ''
                if obj.FBW_Flag == 'True':
                    f_list = []
                    for warehouse_code in warehouse_code_list:
                        iResult = t_online_info_wish_fbw_obj.select_some_infor_api(obj.ProductID, sinfor['ShopSKU'], warehouse_code)
                        if iResult['errorcode'] == 1:
                            f_list.append(warehouse_code)
                    if f_list:
                        fbw_flag = u'<span class="glyphicon glyphicon-asterisk" title="{}"></span>'.format(','.join(f_list))
                try:
                    if activeflag == 'STANDARD':
                        yf = sinfor['ShopSKUKEY'][1]
                    else:
                        if activeflag in obj.WishExpress:
                            yf = sinfor['ShopSKUKEY'][1]
                        elif activeflag not in obj.WishExpress:
                            yf = sinfor['ShopSKUKEY'][3]
                    cb = sinfor['ShopSKUKEY'][0]

                    if cb is None or cb.strip() == '':
                        cb = 0
                    if yf is None or yf.strip() == '':
                        yf = 0
                    sellingPrice = float(cb) + float(yf)
                    calculate_price_obj = calculate_price(str(sinfor['SKU']),float(sinfor['SKUKEY'][2]),float(sinfor['SKUKEY'][3]))
                    profitrate_info = calculate_price_obj.calculate_profitRate(sellingPrice,platformCountryCode='WISH-US', DestinationCountryCode='US')
                    profitrate = profitrate_info['profitRate']
                except:
                    sellingPrice = ''
                    profitrate = ' '
                profit_id = str(sinfor['SKU']) + str(num)
                num += 1

                goodsstatus = sinfor['SKUKEY'][0]
                if goodsstatus == '1':
                    goodsstatus = u'正常'
                if goodsstatus == '2':
                    goodsstatus = u'售完下架'
                if goodsstatus == '3':
                    goodsstatus = u'临时下架'
                if goodsstatus == '4':
                    goodsstatus = u'停售'

                style = ''
                if goodsstatus != u'正常':
                    style = 'class ="danger"'  # 非正常为红色
                elif sinfor['ShopSKUKEY'][-1] == 'Disabled':
                    style = 'class ="active"'  # 正常  Disabled 为 灰色
                elif sinfor['ShopSKUKEY'][-1] == 'Enabled':
                    style = 'class ="success"'  # 正常  Enabled 为 绿色

                if not sinfor['ShopSKUKEY'][1]:
                    sinfor['ShopSKUKEY'][1] = ''

                if not sinfor['ShopSKUKEY'][2]:
                    sinfor['ShopSKUKEY'][2] = ''

                rt = u'%s <tr name="detail_infors" %s><td><label><input type="checkbox" name="shopskucheck" id="%s_%s_%s"></label></td>' \
                     u'<td>%s</td><td>%s</td><td>%s</td><td>%s</td>' \
                     u'<td>%s</td><td>%s</td><td>%s</td><td><a><span id="%s">%s</span></a></td><td>%s</td><td>%s</td>' % \
                     (rt,style,obj.id,a,obj.ShopName, sinfor['SKU'], goodsstatus,
                      sinfor['SKUKEY'][1],sinfor['ShopSKU'].replace('<','&lt;').replace('>','&gt;'),sinfor['ShopSKUKEY'][0],
                      sinfor['ShopSKUKEY'][1], sinfor['ShopSKUKEY'][2], profit_id,profitrate,sinfor['ShopSKUKEY'][-1],fbw_flag)
                rt = u"%s<script>$('#%s').on('click',function()" \
                     u"{to_lock(1);layer.open({type:2,skin:'layui-layer-lan',title:'算价表'," \
                     u"fix:false,shadeClose: true,maxmin:true,area:['1300px','900px']," \
                     u"content:'/price_list/?SKU=%s&sellingPrice=%s&platformCountryCode=%s&DestinationCountryCode=%s',end:function(){to_lock(0);}});});</script>" % (rt, profit_id, sinfor['SKU'], sellingPrice,'WISH-US','US')

            rt = u'%s<tr><td></td><td><a id="link_id_%s">编辑变体</a></td></tr>' % (rt, obj.id)

            url_param = u'abc={}&express={}'.format(obj.ProductID, activeflag)
            if not check_permission_legality(self):
                url_param = url_param + '&readonly=readonly'

            rt = u"%s</tbody></table><script>$('#link_id_%s').on('click',function()" \
                 u"{to_lock(1);var index = layer.open({type:2,skin:'layui-layer-lan',title:'%s'," \
                 u"fixed :false,shadeClose: true,maxmin:true,area:['90%%','80%%'],btn: ['关闭页面']," \
                 u"content:'/t_online_info_wish_store/ShopSKU/?%s',end:function(){to_lock(0);}});" \
                 u"});</script>" % (rt, obj.id, activeflag, url_param)

            rt = rt + u"<script>function en_id_%s(shopsku) {to_lock(1);layer.confirm(shopsku + '  请问确定要进行上架吗？'," \
                      u"{btn: ['确定','算了'],btn1:function(){static_refresh('/up_dis_by_wish_api_shopsku/?enshopsku='+shopsku+" \
                      u"'&shopname=%s&flag=0');},end:function(){to_lock(0);}});}</script>" % (obj.id, obj.ShopName)
            rt = rt + u"<script>function dis_id_%s(shopsku) {to_lock(1);layer.confirm(shopsku + '  请问确定要进行下架吗？'," \
                      u"{btn: ['确定','算了'],btn1:function(){static_refresh('/up_dis_by_wish_api_shopsku/?disshopsku='+shopsku+" \
                      u"'&shopname=%s&flag=0')},end:function(){to_lock(0);}});}</script>" % (obj.id, obj.ShopName)
        except Exception as error:
            rt = u'{}'.format(error)

        return rt

    def fbw_shopsku_attrinfor(self, obj):
        change_text = u"/wish_store_management/get_fbw_shipping/"
        main_change_text = u"{}?shopname={}&product_id={}".format(change_text, obj.ShopName, obj.ProductID)

        rt = u'<table class="table table-bordered table-striped table-hover">' \
             u'<thead>' \
             u'<tr>' \
             u'<th rowspan="2">店铺SKU</th>' \
             u'<th rowspan="2">价格</th>' \
             u'<th colspan="3">FBW-US-LAX (美国)</th>' \
             u'<th colspan="3">FBW-EU-TLL (欧洲)</th>' \
             u'<th colspan="3">FBW-US-CVG (美国)</th>' \
             u'</tr>' \
             u'<tr>' \
             u'<th>活动</th><th>待确认</th><th><a onclick="change_fbw_shipping_show(\'{}&fbw_warehouse=LAX\')">运费</a></th>' \
             u'<th>活动</th><th>待确认</th><th><a onclick="change_fbw_shipping_show(\'{}&fbw_warehouse=TLL\')">运费</a></th>' \
             u'<th>活动</th><th>待确认</th><th><a onclick="change_fbw_shipping_show(\'{}&fbw_warehouse=CVG\')">运费</a></th>' \
             u'</tr>' \
             u'</thead><tbody>'.format(main_change_text, main_change_text, main_change_text)

        if obj.FBW_Flag == 'True':
            shopskulist = listingobjs.getShopSKUList(obj.ProductID)
            classshopskuobjs = classshopsku(db_conn=connection, redis_conn=redis_conn, shopname=obj.ShopName)
            for shopsku in shopskulist:
                rt = rt + u'<tr><td>{}</td><td>{}</td>'.format(shopsku.replace('<','&lt;').replace('>','&gt;'),classshopskuobjs.getPrice(shopsku))
                for warehouse_code in warehouse_code_list:
                    vani_change_text = u"{}?{}".format(change_text, urlencode({'shopsku': shopsku, 'shopname': obj.ShopName}))
                    iResult = t_online_info_wish_fbw_obj.select_some_infor_api(obj.ProductID,shopsku,warehouse_code)
                    if iResult['errorcode'] != -1:
                        rt = rt + u'<td>{}</td><td>{}</td><td><a onclick="change_fbw_shipping_show(\'{}&fbw_warehouse={}\')">运费</a></td>'\
                            .format(iResult['datadict'].get('active', 0),
                                    iResult['datadict'].get('pending', 0),
                                    vani_change_text, warehouse_code
                                    )
                rt = rt + u'</tr>'
        rt = rt + u'</tbody></table>'
        return rt


    def show_SKU_list(self, obj):
        activeflag = self.request.GET.get('EXPRESS', 'STANDARD')
        if activeflag != 'FBW':
            rt = self.not_fbw_shopsku_attrinfor(activeflag=activeflag,obj=obj)
        else:
            rt = self.fbw_shopsku_attrinfor(obj)
        return mark_safe(rt)

    show_SKU_list.short_description = mark_safe(u'<p align="center"style="color:#428bca;">变体详细信息<br>(FBW显示库存相关信息)</p>')

    def pb_text(self, obj):
        pb_show = ''
        pb_look = ''
        if obj.ADShow == 1 and check_permission_legality(self):
            pcount = t_wish_pb_campaignproductstats.objects.filter(
                product_id=obj.ProductID,campaign_state__in=['PENDING', 'NEW', 'SAVED','STARTED']
            ).count()
            pb_show = u'<br>广告<b class="caret"></b>'
            if pcount > 0:
                pb_look = u'<br><a href="/Project/admin/skuapp/t_wish_pb_campaignproductstats/?product_id=%s" ' \
                          u'title="点击查看正在运行的广告" target="_blank" style="color: green;">运行</a>' % obj.ProductID
            else:
                pb_look = u'<br><a href="/Project/admin/skuapp/t_wish_pb_campaignproductstats/?product_id=%s" ' \
                          u'title="点击查看已经停止的广告" target="_blank" style="color: red;">停止</a>' % obj.ProductID
        return pb_show + pb_look

    def sync_skudata(self,obj):
        if check_permission_legality(self):
            return u'<a onclick="static_refresh(\'%s\')"title="同步商品SKU信息">同步</a>' % ('/refresh_sku_info/?productid=%s' % obj.ProductID,)
        return ''

    def enable_id(self,obj):
        if check_permission_legality(self):
            return u'<br><a onclick="enable_id_%s(\'%s\')"title="对整个listing做上架操作">上架</a>' % (obj.id, obj.ProductID,) + \
                   u"<script>function enable_id_%s(listingid) {to_lock(1);layer.confirm(listingid + '  请问确定要进行上架吗？'," \
                   u"{btn: ['确定','算了'],btn1:function(){static_refresh('/syndata_by_wish_api/?enable='+listingid)},end:function(){to_lock(0);}});}" \
                   u"</script>" % (obj.id)
        return ''

    def disable_id(self,obj):
        if check_permission_legality(self):
            down = u'<br><a onclick="disable_id_%s(\'%s\')"title="对整个listing做下架操作">下架</a>' % (obj.id, obj.ProductID,)
            dis = u"<script>function disable_id_%s(listingid) {to_lock(1);layer.confirm(listingid + '  请问确定要进行下架吗？'," \
                  u"{btn: ['确定','算了'],btn1:function(){static_refresh('/syndata_by_wish_api/?disable='+listingid)},end:function(){to_lock(0);}});}" \
                  u"</script>" % (obj.id)
            return down + dis
        return ''

    def sync_online_data(self, obj):
        if check_permission_legality(self):
            return u'<br><a onclick= "static_refresh(\'%s\')" title="同步在线数据">同步</a>' % ('/syndata_by_wish_api/?syn=%s&warehouse=%s' % (obj.ProductID, self.request.GET.get('EXPRESS', 'STANDARD')))
        return ''

    def update_online_data(self, obj):
        if check_permission_legality(self):
            dict_param = {'productid': obj.ProductID, 'shopname': obj.ShopName}
        else:
            dict_param = {'productid': obj.ProductID, 'shopname': obj.ShopName, 'readonly': 'readonly'}

        update = u"<br><a id='edit_update_%s' title='编辑该listing的其他信息'>编辑</a>" \
                 u"<script>$('#edit_update_%s').on('click',function()" \
                 u"{to_lock(1);layer.open({type:2,skin:'layui-layer-lan',title:'编辑-更新'," \
                 u"fixed :false,shadeClose: true,maxmin:true,area:['70%%','80%%'],btn: ['关闭页面']," \
                 u"content:'/edit_update_by_wish_api_listid/?%s',end:function(){to_lock(0);}});});" \
                 u"</script>" % (obj.id, obj.id, urlencode(dict_param))
        return update

    def edit_shipping_other_country(self,obj):
        warehouse = self.request.GET.get('EXPRESS', 'STANDARD')
        if check_permission_legality(self):
            dict_param = {'product_id': obj.ProductID, 'shopname': obj.ShopName, 'warehouse': warehouse}
        else:
            dict_param = {'product_id': obj.ProductID, 'shopname': obj.ShopName, 'readonly': 'readonly', 'warehouse': warehouse}

        update_shipping = u"<br><a id='edit_shipping_%s' title='编辑该listing的国家运费'>运费</a>" \
                 u"<script>$('#edit_shipping_%s').on('click',function()" \
                 u"{to_lock(1);layer.open({type:2,skin:'layui-layer-lan',title:'运费编辑'," \
                 u"fixed :false,shadeClose: true,maxmin:true,area:['1000px','80%%'],btn: ['关闭页面']," \
                 u"content:'/wish_store/edit_shipping_other_country/?%s',end:function(){to_lock(0);}});});" \
                 u"</script>" % (obj.id, obj.id, urlencode(dict_param))
        return update_shipping

    def show_orders7days(self, obj):
        rt = u"<a id='show_orderlist_%s' title='查看日销量趋势图'>销量</a>" \
             u"<script>$('#show_orderlist_%s').on('click',function()" \
             u"{to_lock(1);layer.open({type:2,skin:'layui-layer-lan',title:'查看全部'," \
             u"fix:false,scrollbar: false,shadeClose: true,maxmin:true,area:['1000px','600px']," \
             u"content:'/t_online_info_wish/order1day/?aID=%s&express=%s',end:function(){to_lock(0);}});});" \
             u"</script>" % (obj.id, obj.id, obj.ProductID, self.request.GET.get('EXPRESS', 'STANDARD'))

        More= u'<br><a style="cursor:hand" onclick="isHidden(\'More_%s\')" title="展开更多" >更多<b class="caret"></b></a>'%obj.id

        HiddenDiv1 = u'<br><div id="More_%s" style="display:none">'%obj.id
        hidden_text = self.sync_skudata(obj) + self.enable_id(obj) + self.disable_id(obj) + self.edit_shipping_other_country(obj)
        HiddenDiv2 = '</div>'

        next = More + HiddenDiv1 + hidden_text + HiddenDiv2 if hidden_text else ''

        rt = rt + self.update_online_data(obj) + self.sync_online_data(obj) + next + self.pb_text(obj)
        return mark_safe(rt)

    show_orders7days.short_description = mark_safe(u'<p style="width:40px;color:#428bca;" align="center">操作</p>')

    def show_different_orders7days(self, obj):
        activeflag = self.request.GET.get('EXPRESS', 'STANDARD')
        if activeflag == 'STANDARD':
            return obj.Orders7Days
        elif activeflag == 'DE':
            return obj.Order7daysDE
        elif activeflag == 'GB':
            return obj.Order7daysGB
        elif activeflag == 'US':
            return obj.Order7daysUS
        elif activeflag == 'FBW':
            return obj.Order7daysFBW
        else:
            return 0

    show_different_orders7days.short_description = mark_safe(u'<p style="color:#428bca;" align="center">7天order数</p>')

    def show_different_OfSales(self, obj):
        activeflag = self.request.GET.get('EXPRESS', 'STANDARD')
        if activeflag == 'STANDARD':
            return obj.OfSales
        elif activeflag == 'DE':
            return obj.OfsalesDE
        elif activeflag == 'GB':
            return obj.OfsalesGB
        elif activeflag == 'US':
            return obj.OfsalesUS
        elif activeflag == 'FBW':
            return obj.OfsalesFBW
        else:
            return 0
    show_different_OfSales.short_description = mark_safe(u'<p style="color:#428bca;" align="center">总销量<br>(海外仓总订单量,偏小)</p>')

    list_display = ('show_Picture', 'show_Title_ProductID', 'show_Remarks','show_different_orders7days', 'show_different_OfSales',
                    'show_SKU_list', 'show_time', 'show_orders7days',)
    # list_editable = ('Remarks')
    list_display_links = ('',)

    actions = ['_batch_update_data_by_api', '_batch_en_data_by_api', '_batch_dis_data_by_api',
               'batch_update_title_by_api', '_batch_download_excel', '_batch_to_publish', 'batch_update_shipping',
               'TortWordsDealWith']
    
    def _batch_update_data_by_api(self, request, objs):
        warehouse = self.request.GET.get('EXPRESS', 'STANDARD')
        sResult = {'rcode': '0', 'messages': ''}  # 初始状态
        opnum = 'Syn_%s_%s' % (timetime.now().strftime('%Y%m%d%H%M%S'), request.user.username)
        try:
            param = {}  # 操作日志的参数
            param['OpNum']=opnum
            param['OpKey'] = objs.values_list("ProductID",flat=True)
            param['OpType']='SynID'
            param['Status']='runing'
            param['ErrorInfo']=''
            param['OpPerson']=request.user.first_name
            param['OpTime']=timetime.now()
            param['OpStartTime']=timetime.now()
            param['OpEndTime']=None
            param['aNum']=len(objs)
            param['rNum']=0
            param['eNum']=0

            iResult = t_wish_store_oplogs_obj.createLog(param)
            assert iResult['errorcode'] == 0, "insert log error."
            for obj in objs:
                syndata_by_wish_api([obj.ShopName, obj.ProductID, obj.ParentSKU, warehouse], 'syn', opnum)
            sResult['rcode'] = 1
            sResult['KEY'] = opnum
        except Exception, ex:
            sResult['rcode'] = -1
            sResult['messages'] = '%s:%s' % (Exception, ex)
            # dResult = t_wish_store_oplogs_obj.deleteLog(opnum)
            # if dResult['errorcode'] == -1:
            #     sResult['messages'] = sResult['messages'] + 'DelError:%s,该操作记录编号删除错误'%opnum
        return HttpResponse(json.dumps(sResult))

    _batch_update_data_by_api.short_description = u'同步选中商品数据'


    def _batch_en_data_by_api(self, request, objs):
        # sResult = {'rcode': '0', 'messages': ''}  # 初始状态
        # try:
        #     synname = 'En_%s_%s' % (timetime.now().strftime('%Y%m%d%H%M%S'),request.user.username)
        #     productlist = objs.values_list('ProductID', flat=True)
        #
        #     sResult['rcode'] = 1
        #     mytime = timetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #     t_wish_product_api_log.objects.create(
        #         SynName=synname, StartTime=mytime, Person=request.user.first_name, Time=mytime,
        #         Status='runing', elogs=json.dumps([]), aNum=len(productlist), rNum=0, eNum=0, Type=u'EnID'
        #     )
        #     sResult['KEY'] = synname
        #
        #     syndata_by_wish_api.delay(productlist, 'enable', synname)
        # except Exception, ex:
        #     sResult['rcode'] = -1
        #     sResult['messages'] = '%s:%s' % (Exception, ex)
        sResult = {'rcode': '0', 'messages': ''}  # 初始状态
        opnum = 'En_%s_%s' % (timetime.now().strftime('%Y%m%d%H%M%S'), request.user.username)
        try:
            param = {}  # 操作日志的参数
            param['OpNum'] = opnum
            param['OpKey'] = objs.values_list("ProductID", flat=True)
            param['OpType'] = 'EnID'
            param['Status'] = 'runing'
            param['ErrorInfo'] = ''
            param['OpPerson'] = request.user.first_name
            param['OpTime'] = timetime.now()
            param['OpStartTime'] = timetime.now()
            param['OpEndTime'] = None
            param['aNum'] = len(objs)
            param['rNum'] = 0
            param['eNum'] = 0

            iResult = t_wish_store_oplogs_obj.createLog(param)
            assert iResult['errorcode'] == 0, "insert log error."
            for obj in objs:
                syndata_by_wish_api([obj.ShopName, obj.ProductID, obj.ParentSKU], 'enable', opnum)
            sResult['rcode'] = 1
            sResult['KEY'] = opnum
        except Exception, ex:
            sResult['rcode'] = -1
            sResult['messages'] = '%s:%s' % (Exception, ex)
            # dResult = t_wish_store_oplogs_obj.deleteLog(opnum)
            # if dResult['errorcode'] == -1:
            #     sResult['messages'] = sResult['messages'] + 'DelError:%s,该操作记录编号删除错误' % opnum
        return HttpResponse(json.dumps(sResult))

    _batch_en_data_by_api.short_description = u'选中商品批量上架'


    def _batch_dis_data_by_api(self, request, objs):
        # sResult = {'rcode': '0', 'messages': ''}  # 初始状态
        # try:
        #     synname = 'Dis_%s_%s' % (timetime.now().strftime('%Y%m%d%H%M%S'),request.user.username)
        #     productlist = objs.values_list('ProductID', flat=True)
        #
        #     sResult['rcode'] = 1
        #     mytime = timetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #     t_wish_product_api_log.objects.create(
        #         SynName=synname, StartTime=mytime, Person=request.user.first_name, Time=mytime,
        #         Status='runing', elogs=json.dumps([]), aNum=len(productlist), rNum=0, eNum=0, Type=u'DisID'
        #     )
        #     sResult['KEY'] = synname
        #
        #     syndata_by_wish_api.delay(productlist, 'disable', synname)
        # except Exception, ex:
        #     sResult['rcode'] = -1
        #     sResult['messages'] = '%s:%s' % (Exception, ex)
        sResult = {'rcode': '0', 'messages': ''}  # 初始状态
        opnum = 'Dis_%s_%s' % (timetime.now().strftime('%Y%m%d%H%M%S'), request.user.username)
        try:
            param = {}  # 操作日志的参数
            param['OpNum'] = opnum
            param['OpKey'] = objs.values_list("ProductID", flat=True)
            param['OpType'] = 'DisID'
            param['Status'] = 'runing'
            param['ErrorInfo'] = ''
            param['OpPerson'] = request.user.first_name
            param['OpTime'] = timetime.now()
            param['OpStartTime'] = timetime.now()
            param['OpEndTime'] = None
            param['aNum'] = len(objs)
            param['rNum'] = 0
            param['eNum'] = 0

            iResult = t_wish_store_oplogs_obj.createLog(param)
            assert iResult['errorcode'] == 0, "insert log error."
            for obj in objs:
                syndata_by_wish_api([obj.ShopName, obj.ProductID, obj.ParentSKU], 'disable', opnum)
            sResult['rcode'] = 1
            sResult['KEY'] = opnum
        except Exception, ex:
            sResult['rcode'] = -1
            sResult['messages'] = '%s:%s' % (Exception, ex)
            # dResult = t_wish_store_oplogs_obj.deleteLog(opnum)
            # if dResult['errorcode'] == -1:
            #     sResult['messages'] = sResult['messages'] + 'DelError:%s,该操作记录编号删除错误' % opnum
        return HttpResponse(json.dumps(sResult))

    _batch_dis_data_by_api.short_description = u'选中商品批量下架'


    def _batch_download_excel(self, request, objs):
        sResult = {'rcode': '0', 'messages': ''}  # 初始状态
        opnum = 'download_%s_%s' % (timetime.now().strftime('%Y%m%d%H%M%S'), request.user.username)
        try:
            param = {}  # 操作日志的参数
            param['OpNum'] = opnum
            param['OpKey'] = [opnum]
            param['OpType'] = 'download_by_id'
            param['Status'] = 'runing'
            param['ErrorInfo'] = ''
            param['OpPerson'] = request.user.first_name
            param['OpTime'] = timetime.now()
            param['OpStartTime'] = timetime.now()
            param['OpEndTime'] = None
            param['aNum'] = len(objs)
            param['rNum'] = 0
            param['eNum'] = 0

            iResult = t_wish_store_oplogs_obj.createLog(param)
            assert iResult['errorcode'] == 0, "insert log error."

            warehouse = request.GET.get('EXPRESS', 'STANDARD')
            plist = []
            for obj in objs:
                plist.append([obj.ShopName, obj.ProductID, obj.ParentSKU])
            syndata_by_wish_api(plist, 'download', opnum, warehouse)
            sResult['rcode'] = 1
            sResult['KEY'] = opnum
        except Exception, ex:
            sResult['rcode'] = -1
            sResult['messages'] = '%s:%s' % (Exception, ex)
        return HttpResponse(json.dumps(sResult))

    _batch_download_excel.short_description = u'选中商品导出表格'


    def batch_update_title_by_api(self, request, objs):
        productList = []
        for obj in objs:
            productList.append(obj.ProductID)
        if productList:
            return HttpResponseRedirect("/t_online_info_wish_store_update_title/?%s"%(urlencode({'productid':'|'.join(productList)}),))
        else:
            messages.error(request,u'请选择要替换修改的记录。')

    batch_update_title_by_api.short_description = u'批量替换修改标题'


    def batch_update_shipping(self, request, objs):
        sResult = {'rcode': '0', 'messages': ''}  # 初始状态
        opnum = 'BU_Shipping_%s_%s' % (timetime.now().strftime('%Y%m%d%H%M%S'), request.user.username)
        try:
            json_str = request.POST.get('update_data_json_str', '[]')
            DataList = eval(json_str)
            product_id_list = objs.values_list("ProductID", flat=True)
            keylist = ['{}_{}'.format(product_id, tmp['country']) for product_id in product_id_list for tmp in DataList]

            param = {}  # 操作日志的参数
            param['OpNum'] = opnum
            param['OpKey'] = keylist
            param['OpType'] = 'BU_Shipping'
            param['Status'] = 'runing'
            param['ErrorInfo'] = ''
            param['OpPerson'] = request.user.first_name
            param['OpTime'] = timetime.now()
            param['OpStartTime'] = timetime.now()
            param['OpEndTime'] = None
            param['aNum'] = len(keylist)
            param['rNum'] = 0
            param['eNum'] = 0

            iResult = t_wish_store_oplogs_obj.createLog(param)
            assert iResult['errorcode'] == 0, "insert log error."

            warehouse = request.GET.get('warehouse', 'STANDARD')
            for obj in objs:
                syndata_by_wish_api([obj.ShopName, obj.ProductID, json_str], 'BU_Shipping', opnum, warehouse)

            sResult['rcode'] = 1
            sResult['KEY'] = opnum
        except Exception, ex:
            sResult['rcode'] = -1
            sResult['messages'] = '%s:%s' % (Exception, ex)

        return HttpResponse(json.dumps(sResult))
    batch_update_shipping.short_description = u'批量更新产品运费'


    def _batch_to_publish(self, request, objs):
        sResult = {'rcode': '0', 'messages': ''}  # 初始状态
        opnum = 'Topub_%s_%s' % (timetime.now().strftime('%Y%m%d%H%M%S'), request.user.username)
        try:
            param = {}  # 操作日志的参数
            param['OpNum'] = opnum
            param['OpKey'] = objs.values_list("ProductID", flat=True)
            param['OpType'] = 'Topub'
            param['Status'] = 'runing'
            param['ErrorInfo'] = ''
            param['OpPerson'] = request.user.first_name
            param['OpTime'] = timetime.now()
            param['OpStartTime'] = timetime.now()
            param['OpEndTime'] = None
            param['aNum'] = len(objs)
            param['rNum'] = 0
            param['eNum'] = 0

            iResult = t_wish_store_oplogs_obj.createLog(param)
            assert iResult['errorcode'] == 0, "insert log error."
            for obj in objs:
                syndata_by_wish_api([obj.ShopName, obj.ProductID, obj.ParentSKU], 'topub', opnum, opPerson=request.user.first_name)
            sResult['rcode'] = 1
            sResult['KEY'] = opnum
        except Exception, ex:
            sResult['rcode'] = -1
            sResult['messages'] = '%s:%s' % (Exception, ex)
        return HttpResponse(json.dumps(sResult))

    _batch_to_publish.short_description = u'选中转到---待刊登'


    def TortWordsDealWith(self, request, objs):
        tortremark = request.POST.get('batch_remark_text')
        # messages.error(request, tortremark)
        for i, obj in enumerate(objs):
            if obj.Status == 'Enabled' and obj.TortFlag == 1:
                if not obj.Remarks and not tortremark:
                    messages.error(request, u'ProductID: {}, 修改侵权处理标记前，请输入备注！'.format(obj.ProductID))
                else:
                    obj.Remarks = u'{};{}'.format(obj.Remarks, tortremark)
                    obj.TortFlag=2
                    obj.save()
            if i >= 20:
                break

    TortWordsDealWith.short_description = u'修改侵权词处理标记'


    def get_list_queryset(self,):
        self.tortwordsdict = tortwords(connection, redis_conn)

        request = self.request
        qs = super(t_online_info_wish_store_Admin, self).get_list_queryset()
        try:
            express = request.GET.get('EXPRESS', 'STANDARD')
            # 获取用户要显示的页数
            perpage = request.GET.get('showperpage', 20)
            try:
                if int(perpage) >= 1:
                    self.list_per_page = int(perpage)
                else:
                    self.list_per_page = 20
            except:
                self.list_per_page = 20
                messages.error(request,"你输入了一个不合法的整数！")

            seachfilter = {}

            status = request.GET.get('status')
            # eShopList = t_store_configuration_file.objects.filter(Status='-1').values_list('ShopName_temp', flat=True)
            if status == 'online':# 在线
                seachfilter['AdStatus'] = '1'
                seachfilter['SName'] = '0'

                # qs = qs.exclude(SName='-1').exclude(AdStatus__in=['-1', '-2'])
                # # .filter(ReviewState='approved', Status='Enabled')

            elif status == 'offline':# 不在线
                seachfilter['AdStatus'] = '0'
                seachfilter['SName'] = '0'
                # qs = qs.exclude(ReviewState='approved', Status='Enabled').exclude(SName='-1').exclude(AdStatus__in=['-1', '-2'])

            elif status == 'storeError': # 店铺状态异常
                seachfilter['SName'] = '-1'

            elif status == 'doError':# 单条状态异常的
                seachfilter['AdStatus__in'] = ['-1', '-2']
                seachfilter['SName'] = '0'

            shopname = request.GET.get('shopname')
            if shopname:
                seachfilter['ShopName__exact'] = shopname
                # qs = qs.filter(ShopName__exact=shopname)

            seller = request.GET.get('seller')
            if seller:
                seachfilter['Seller__exact'] = seller
                # qs = qs.filter(Seller__exact=seller)

            reviewState = request.GET.get('reviewState')
            if reviewState:
                reviewList = [rev for rev in reviewState.split(',') if rev]
                if reviewList:
                    seachfilter['ReviewState__in'] = reviewList
                    # qs = qs.filter(ReviewState__in=reviewList)

            rejected = request.GET.get('rejected')
            if rejected == 'rejected_approved':
                seachfilter['ReviewState__exact'] = 'rejected'
                seachfilter['BeforeReviewState__exact'] = 'approved'

            if rejected == 'rejected_pending':
                seachfilter['ReviewState__exact'] = 'rejected'
                seachfilter['BeforeReviewState__exact'] = 'pending'

            if rejected == 'rejected_others':
                seachfilter['ReviewState__exact'] = 'rejected'
                qs = qs.exclude(BeforeReviewState__in=['approved', 'pending'])

            tortinfo = request.GET.get('tortInfo')
            if tortinfo:
                seachfilter['TortInfo__exact'] = tortinfo
                # qs = qs.filter(TortInfo__exact=tortinfo)

            Estatus = request.GET.get('Estatus')
            if Estatus:
                seachfilter['Status__exact'] = Estatus
                # qs = qs.filter(Status__exact=Estatus)

            dataSources = request.GET.get('dataSources')
            if dataSources:
                seachfilter['DataSources__exact'] = dataSources
                # qs = qs.filter(DataSources__exact=dataSources)

            refreshTimeStart = request.GET.get('refreshTimeStart')
            if refreshTimeStart:
                seachfilter['RefreshTime__gte'] = refreshTimeStart
                # qs = qs.filter(RefreshTime__gte=refreshTimeStart)

            refreshTimeEnd = request.GET.get('refreshTimeEnd')
            if refreshTimeEnd:
                seachfilter['RefreshTime__lt'] = refreshTimeEnd
                # qs = qs.filter(RefreshTime__lt=refreshTimeEnd)

            dateUploadedStart = request.GET.get('dateUploadedStart')
            if dateUploadedStart:
                seachfilter['DateUploaded__gte'] = dateUploadedStart
                # qs = qs.filter(DateUploaded__gte=dateUploadedStart)

            dateUploadedEnd = request.GET.get('dateUploadedEnd')
            if dateUploadedEnd:
                seachfilter['DateUploaded__lt'] = dateUploadedEnd
                # qs = qs.filter(DateUploaded__lt=dateUploadedEnd)

            lastUpdatedStart = request.GET.get('lastUpdatedStart')
            if lastUpdatedStart:
                seachfilter['LastUpdated__gte'] = lastUpdatedStart
                # qs = qs.filter(LastUpdated__gte=lastUpdatedStart)

            lastUpdatedEnd = request.GET.get('lastUpdatedEnd')
            if lastUpdatedEnd:
                seachfilter['LastUpdated__lt'] = lastUpdatedEnd
                # qs = qs.filter(LastUpdated__lt=lastUpdatedEnd)

            titles = request.GET.get('Title')
            if titles:
                for title in titles.split(','):
                    qs = qs.filter(Title__icontains=title.strip())  if title.strip() else qs

                # seachfilter['Title__icontains'] = title
                # qs = qs.filter(Title__icontains=title)

            Published = request.GET.get('Published')
            if Published:
                seachfilter['Published__exact'] = Published
                # qs = qs.filter(Published__exact=Published)

            is_promoted = request.GET.get('is_promoted')
            if is_promoted:
                seachfilter['is_promoted__exact'] = is_promoted
                # qs = qs.filter(is_promoted__exact=is_promoted)

            WishExpress=request.GET.get('WishExpress')
            if WishExpress:
                seachfilter['WishExpress__icontains'] = WishExpress

            WishExpressYN=request.GET.get('WishExpressYN')
            if WishExpressYN == 'Y':
                if express == 'STANDARD':
                    qs = qs.exclude(WishExpress__exact='[]')
                else:
                    seachfilter['WishExpress__icontains'] = express

            if WishExpressYN == 'N':
                if express == 'STANDARD':
                    seachfilter['WishExpress__exact'] = '[]'
                else:
                    qs = qs.exclude(WishExpress__icontains=express)

            MHmainSKU = request.GET.get('MHmainSKU')  # 主SKU模糊搜索
            if MHmainSKU:
                seachfilter['MainSKU__contains'] = MHmainSKU
                # qs = qs.filter(MainSKU__contains=MHmainSKU)

            MHremark = request.GET.get('MHremark')  # 备注模糊搜索
            if MHremark:
                seachfilter['Remarks__icontains'] = MHremark

            Band = request.GET.get('Band')  # 绑定状态
            if Band:
                seachfilter['BindingFlag__exact'] = Band
                # qs = qs.filter(BindingFlag__exact=Band)

            ZHMainSKU = request.GET.get('ZHMainSKU')  # 组合主SKU
            if ZHMainSKU == '1':
                seachfilter['MainSKU__icontains'] = ','
                # qs = qs.filter(MainSKU__icontains=',')
            if ZHMainSKU == '2':
                qs = qs.exclude(MainSKU__icontains=',')

            USExpressType = request.GET.get('USExpressType')
            if USExpressType and USExpressType in ['virtual', 'real']:
                seachfilter['WishExpressType__exact'] = USExpressType
            elif USExpressType and USExpressType in ['null', '']:
                qs = qs.exclude(WishExpressType__in=['virtual', 'real'])

            adshow = request.GET.get('adshow')
            if adshow:
                seachfilter['ADShow__exact'] = adshow

            salestrend = request.GET.get('salestrend')
            if salestrend:
                seachfilter['SalesTrend__exact'] = salestrend

            ratingStart = request.GET.get('ratingStart')
            if ratingStart:
                seachfilter['Rating__gte'] = ratingStart

            ratingEnd = request.GET.get('ratingEnd')
            if ratingEnd:
                seachfilter['Rating__lt'] = ratingEnd

            if express == 'FBW':  # fbw
                seachfilter['FBW_Flag__exact'] = 'True'

            tortflag = request.GET.get('tortflag')   # 新加的标题关键词侵权标记 用于左侧菜单的过滤
            if tortflag == '1':
                seachfilter['TortFlag__exact'] = 1
                seachfilter['Status__exact'] = 'Enabled'
            elif tortflag == '2':
                seachfilter['TortFlag__exact'] = 2
                seachfilter['Status__exact'] = 'Enabled'

            # 商品状态查询
            skustatus = request.GET.get('skustatus')  # 商品SKU状态
            goodsstatus = []
            if skustatus == '1':
                goodsstatus = [1000, 1100, 1010, 1001, 1110, 1101, 1011, 1111]  # 正常
            elif skustatus == '2':
                goodsstatus = [100, 1100, 110, 101, 1110, 1101, 111, 1111]  # 售完下架
            elif skustatus == '3':
                goodsstatus = [10, 1010, 110, 11, 1011, 1110, 111, 1111]  # 临时下架
            elif skustatus == '4':
                goodsstatus = [1, 1001, 101, 11, 1101, 111, 1011, 1111]  # 停售
            if goodsstatus:
                seachfilter['GoodsFlag__in'] = goodsstatus
                # qs = qs.filter(GoodsFlag__in=goodsstatus)

            riskgrade = request.GET.get('riskgrade')  # 侵权风险等级
            risklist = []
            if riskgrade == '3':
                risklist = [8, 9, 10, 11, 12, 13, 14, 15]  # 绝对禁止
            elif riskgrade == '2':
                risklist = [4, 5, 6, 7, 12, 13, 14, 15]  # 限定范围
            elif riskgrade == '1':
                risklist = [2, 3, 6, 7, 10, 11, 14, 15]  # 潜在风险
            elif riskgrade == '0':
                risklist = [1, 3, 5, 7, 9, 11, 13, 15]   # 其它
            elif riskgrade == 'o':
                risklist = [1, 2, 3, 4, 5, 6, 7]   # 除了绝对禁止 以外的
            if risklist:
                seachfilter['RiskGrade__in'] = risklist

            # 店铺SKU状态查询
            shopskustatus = request.GET.get('shopskustatus')  # 店铺SKU状态
            shopssList = []
            if shopskustatus == 'Enabled':
                shopssList = [10, 11]  # 启用
            if shopskustatus == 'Disabled':
                shopssList = [1, 11]  # 未启用
            if shopssList:
                seachfilter['ShopsFlag__in'] = shopssList
                # qs = qs.filter(ShopsFlag__in=shopssList)

            mainSKU = request.GET.get('mainSKU')
            mainskulist = []
            if mainSKU:
                mainskulist = [mainSKU for mainSKU in mainSKU.split(',') if mainSKU]  # 多主SKU查询

            CrossMainSKU = []
            JZLTimeStart = request.GET.get('JZLTimeStart')  # 主SKU建资料时间
            JZLTimeEnd = request.GET.get('JZLTimeEnd')
            # 主SKU建资料时间 查询
            JZLDict = {}
            if JZLTimeStart:
                JZLDict['JZLTime__gte'] = JZLTimeStart
            if JZLTimeEnd:
                JZLDict['JZLTime__lt'] = JZLTimeEnd
            if JZLDict:
                CrossMainSKU = t_product_enter_ed.objects.filter(**JZLDict).values_list('MainSKU',flat=True)

            # 领用人 查询
            MainSKUClaim = request.GET.get('MainSKUClaim')  # 主SKU领用人查询
            MainSKULISTClaim = []
            if MainSKUClaim:
                MainSKULISTClaim = t_product_depart_get.objects.filter(StaffName=MainSKUClaim, DepartmentID__in=('4', '5')).values_list('MainSKU',flat=True)

            LargeCategory = request.GET.get('LargeCategory')  # 大类
            SmallCategory = request.GET.get('SmallCategory')  # 小类
            if LargeCategory:
                seachfilter['MainSKULargeCate__exact'] = LargeCategory
            if SmallCategory:
                seachfilter['MainSKUSmallCate__exact'] = SmallCategory

            # orders7DaysStart = request.GET.get('orders7DaysStart')
            # if orders7DaysStart:
            #     seachfilter['Orders7Days__gte'] = orders7DaysStart
            #     # qs = qs.filter(Orders7Days__gte=orders7DaysStart)
            #
            # orders7DaysEnd = request.GET.get('orders7DaysEnd')
            # if orders7DaysEnd:
            #     seachfilter['Orders7Days__lt'] = orders7DaysEnd
            #     # qs = qs.filter(Orders7Days__lt=orders7DaysEnd)

            orders7DaysStart = request.GET.get('orders7DaysStart')
            kcStart = request.GET.get("kcStart")
            ShippingStart = request.GET.get('ShippingStart')
            onlinedict = {}
            fbw_filter = {}
            if kcStart :
                if express != 'STANDARD' and express != 'FBW':
                    onlinedict['%sExpressInventory__gte' % express] = kcStart
                elif express == 'FBW':
                    fbw_filter['online_stock__gte'] = kcStart

            if ShippingStart and express != 'STANDARD' and express != 'FBW':
                onlinedict['%sExpressShipping__gte' % express] = ShippingStart
            if orders7DaysStart:
                if express == 'STANDARD':
                    seachfilter['Orders7Days__gte'] = orders7DaysStart
                else:
                    seachfilter['Order7days{}__gte'.format(express)] = orders7DaysStart

            orders7DaysEnd = request.GET.get('orders7DaysEnd')
            kcEnd = request.GET.get("kcEnd")
            ShippingEnd = request.GET.get('ShippingEnd')
            if kcEnd :
                if express != 'STANDARD' and express != 'FBW':
                    onlinedict['%sExpressInventory__lt' % express] = kcEnd
                elif express == 'FBW':
                    fbw_filter['online_stock__lt'] = kcEnd

            if ShippingEnd and express != 'STANDARD' and express != 'FBW':
                onlinedict['%sExpressShipping__lt' % express] = ShippingEnd
            if orders7DaysEnd:
                if express == 'STANDARD':
                    seachfilter['Orders7Days__lt'] = orders7DaysEnd
                else:
                    seachfilter['Order7days{}__lt'.format(express)] = orders7DaysEnd

            shopsku = request.GET.get('ShopSKU')  # 店铺SKU
            if shopsku:
                onlinedict['ShopSKU__exact'] = shopsku

            productlist = []
            mflag = 0
            # 所有用主SKU搜索的
            online_objs = t_online_info.objects.all()
            if mainSKU:
                mflag = 1
                online_objs = online_objs.filter(MainSKU__in=mainskulist)
            if JZLDict:
                mflag = 1
                online_objs = online_objs.filter(MainSKU__in=CrossMainSKU)
            if MainSKUClaim:
                mflag = 1
                online_objs = online_objs.filter(MainSKU__in=MainSKULISTClaim)
            # if express == 'FBW':  # fbw
            #     mflag = 1
            #     online_objs = online_objs.filter(FBW_Flag__exact='True')
            if onlinedict:
                mflag = 1
                online_objs = online_objs.filter(**onlinedict)
            if mflag == 1:
                mflag = 2
                list_objs = online_objs.values_list('ProductID')
                productlist = set([list_obj[0] for list_obj in list_objs])

            productId = request.GET.get('productID')  # 所有productid搜索
            if productId:
                productidlist = [productid for productid in productId.split(',') if productid]
                qs = qs.filter(ProductID__in=productidlist)
            if mflag == 2:
                qs = qs.filter(ProductID__in=productlist)
            if fbw_filter:
                fbw_porduct_list = django_fbw.objects.filter(**fbw_filter).values_list('product_id', flat=True)
                qs = qs.filter(ProductID__in=fbw_porduct_list)

            if seachfilter:
                qs = qs.filter(**seachfilter)

            if request.user.is_superuser:
                return qs
            else:
                userID = [each.id for each in User.objects.filter(groups__id__in=[38])]
                if request.user.id in userID:
                    return qs
                objs = t_store_configuration_file.objects.filter(
                    Q(Seller=request.user.first_name) | Q(Published=request.user.first_name) | Q(
                        Operators=request.user.first_name)).values('ShopName_temp')
                if objs.exists():
                    shoplist = []
                    for obj in objs:
                        shoplist.append(obj['ShopName_temp'])
                    return qs.filter(ShopName__in=shoplist)
                else:
                    return qs.none()
        except Exception, e:
            messages.error(request, u'查询条件错误，请联系IT人员！%s' % e)
            return qs

xadmin.site.register(t_online_info_wish_store, t_online_info_wish_store_Admin)
xadmin.site.register(t_add_variant_information, t_add_variant_information_admin)
xadmin.site.register_plugin(site_left_menu_Plugin_wish,BaseAdminView)
xadmin.site.register_plugin(t_online_info_wish_store_plugin,ListAdminView)
xadmin.site.register_plugin(change_shipping_plugin,ListAdminView)
xadmin.site.register_plugin(t_online_info_wish_store_secondplugin,ListAdminView)
xadmin.site.register_plugin(site_left_menu_tree_Plugin_wish,ListAdminView)
xadmin.site.register_plugin(wish_listing_readonly_P,ListAdminView)

xadmin.site.register_plugin(wish_store_sort_bar_plugin,ListAdminView)
xadmin.site.register_plugin(help_select_plugin,ListAdminView)

# Wish日总销售额统计
from storeapp.StoreXadmin.t_wish_daily_sales_statistics_Admin import t_wish_daily_sales_statistics_Admin
from storeapp.table.t_wish_daily_sales_statistics import t_wish_daily_sales_statistics
xadmin.site.register(t_wish_daily_sales_statistics, t_wish_daily_sales_statistics_Admin)


# Wish日总销售额统计图表插件
from storeapp.plugin.wish_daily_sales_statistics_chart_plugin import wish_daily_sales_statistics_chart_plugin
xadmin.site.register_plugin(wish_daily_sales_statistics_chart_plugin, ListAdminView)


# Wish 低库存数据展示
from storeapp.table.t_online_info_wish_low_inventory import t_online_info_wish_low_inventory
from storeapp.StoreXadmin.t_online_info_wish_low_inventory_admin import t_online_info_wish_low_inventory_admin
xadmin.site.register(t_online_info_wish_low_inventory, t_online_info_wish_low_inventory_admin)


# Wish 订单罚款信息
from storeapp.table.t_wish_information_of_order_fine import t_wish_information_of_order_fine
from storeapp.StoreXadmin.t_wish_information_of_order_fine_admin import t_wish_information_of_order_fine_admin
xadmin.site.register(t_wish_information_of_order_fine, t_wish_information_of_order_fine_admin)


# Wish_FBW运输计划管理
from storeapp.table.t_wish_fbw_shipping_plan_list import t_wish_fbw_shipping_plan_list
from storeapp.StoreXadmin.t_wish_fbw_shippng_plan_list_admin import t_wish_fbw_shippng_plan_list_admin
xadmin.site.register(t_wish_fbw_shipping_plan_list, t_wish_fbw_shippng_plan_list_admin)


# Wish FBW低库存预警
from storeapp.table.t_online_info_wish_fbw_api_low_inventory import t_online_info_wish_fbw_api_low_inventory
from storeapp.StoreXadmin.t_online_info_wish_fbw_api_low_inventory_admin import t_online_info_wish_fbw_api_low_inventory_admin
xadmin.site.register(t_online_info_wish_fbw_api_low_inventory, t_online_info_wish_fbw_api_low_inventory_admin)


