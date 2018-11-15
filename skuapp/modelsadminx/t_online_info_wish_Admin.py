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

from storeapp.plugin.t_online_info_wish_store_plugin import t_online_info_wish_store_plugin
from storeapp.plugin.t_online_info_wish_store_secondplugin import t_online_info_wish_store_secondplugin
from storeapp.plugin.syn_the_shop_data_by_api_plugin import syn_the_shop_data_by_api_plugin
from storeapp.plugin.site_left_menu_plugin_wish import site_left_menu_Plugin_wish
from storeapp.plugin.change_shipping_plugin import change_shipping_plugin
from storeapp.plugin.site_left_menu_tree_Plugin_wish import site_left_menu_tree_Plugin_wish

from app_djcelery.tasks import syndata_by_wish_api
from brick.classredis.classprocess_wish import classprocess_wish
from brick.pricelist.calculate_price import calculate_price

from brick.table.t_wish_store_oplogs import t_wish_store_oplogs
from skuapp.table.t_wish_pb_campaignproductstats import t_wish_pb_campaignproductstats
# from chart_app.table.t_chart_wish_listing_refund_statistics import t_chart_wish_listing_refund_statistics as wish_score

from datetime import datetime as timetime
logger = logging.getLogger('sourceDns.webdns.views')

redis_conn = get_redis_connection(alias='product')
py_SynRedis_tables_obj = py_SynRedis_tables()
# py_SynRedis_pub_obj = py_SynRedis_pub()
classsku_obj = classsku()
listingobjs = classlisting(connection, redis_conn)


classprocess_wish_obj = classprocess_wish(redis_conn)

t_wish_store_oplogs_obj = t_wish_store_oplogs(connection)

class t_online_info_wish_Admin(object):
    # syn_data = True
    search_box_flag = True
    wish_listing_secondplugin = True
    # site_left_menu_flag_wish = False
    show_per_page = True
    wish_listing_readonly_f = True

    list_per_page = 20

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

    def rating(self, rating):
        if rating is not None:
            score = rating
            color = '#66FF66'
        else:
            score = ''
            color = 'red'
        rt = '<div title="评分:%s" style="float:left;width: 20px;height: 20px;background-color: %s;' \
             'text-align: center;line-height: 20px;border-radius: 4px">%s</div>' % (score, color, score)
        return rt

    def show_Remarks(self, obj):
        remarks = u'<a id="remark_%s" title="点击查看备注" >备注</a>:<a id="remark_content_%s">%s</a>' % \
                  (obj.id, obj.id, obj.Remarks)
        remarks_show = u"<script>$('#remark_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan'," \
                       u"title:'查看备注',fix:false,shadeClose: true,maxmin:true,area:['500px','300px']," \
                       u"content:'/t_online_info_wish/w_remark/?productid=%s&readonly=readonly',});});</script>" % (obj.id, obj.ProductID)

        wishexpresstype = ''
        if self.request.GET.get('EXPRESS', 'STANDARD') == 'US':
            option = u"<option value =''></option><option value ='real'>真实</option><option value ='virtual'>虚拟</option>"
            if obj.WishExpressType == 'real':
                option = u"<option value =''></option><option value ='real' selected>真实</option>" \
                         u"<option value ='virtual'>虚拟</option>"
            elif obj.WishExpressType == 'virtual':
                option = u"<option value =''></option><option value ='real' >真实</option>" \
                         u"<option value ='virtual' selected>虚拟</option>"

            wishexpresstype = u"</br></br>" \
                              u"<select readonly class='text-field admintextinputwidget form-control' style='width: 88px;' >" \
                              + option + \
                              u"</select>"

        type_show = u"</br><span id='%s'></span>" % obj.ProductID

        return mark_safe(remarks + remarks_show + wishexpresstype + type_show)

    show_Remarks.short_description = mark_safe(u'<p align="center"style="color:#428bca;">备注</br>海外仓类型</p>')

    def show_Picture(self, obj):
        url = u'https://contestimg.wish.com/api/webimage/%s-medium.jpg' % str(obj.ProductID)
        rt = '<div><img src="%s" width="120" height="120"/></div>' % (url,)
        z_url = u'http://fancyqube-wish.oss-cn-shanghai.aliyuncs.com/Wish_Diamonds_pic%5Chuangzuan.png'
        h_url = u'http://main.cdn.wish.com/4fe4c5486817/img/product_badges/express_shipping/badge.png?v=13'
        if obj.is_promoted == 'True':
            rt = rt + '<div style="float:left"><img src="%s"  width="20" height="20"  alt = "%s"  title="%s" /></div>' % (
                z_url, z_url, obj.is_promoted)
        if obj.WishExpress is not None and obj.WishExpress != '[]':
            rt = rt + '<div style="float:left"><img src="%s"  width="20" height="20"  alt = "%s"  title="%s" /></div>' % (
                h_url, h_url, obj.WishExpress)
        rt = rt + '<div>' + self.tortInfo(obj.TortInfo) + self.status(obj.ReviewState) + self.rating(
            obj.Rating) + '</div>'
        return mark_safe(rt)

    show_Picture.short_description = mark_safe(u'<p align="center"style="color:#428bca;">图片</p>')

    def show_Title_ProductID(self, obj):
        rt = django_wrap(obj.Title, ' ', 6)
        rt = u'%s<br>产品ID:<a href=" https://www.wish.com/c/%s" target="_blank">%s</a>' % (
        rt, obj.ProductID, obj.ProductID)
        if obj.ReviewState == 'rejected' and obj.BeforeReviewState in ['approved', 'pending']:
            rt = rt + u'<br><span style="color:red">拒绝前状态:%s</span>' % obj.BeforeReviewState
        if obj.AdStatus in ['-1', '-2'] and obj.SName != '-1':
            einfor = t_wish_store_oplogs_obj.selectLogsByIDError(obj.ProductID)
            if einfor['errorcode'] == 0:
                rt = rt + u'<br><span style="color:red">异常原因:%s</span>' % '<br>'.join(einfor['einfors'])
        rt = u'%s<br>卖家简称:%s' % (rt, obj.ShopName)
        rt = u'%s<br>店长/销售员:%s' % (rt, obj.Seller)
        rt = u'%s<br>刊登人:%s' % (rt, obj.Published)

        return mark_safe(rt)

    show_Title_ProductID.short_description = mark_safe(u'<p align="center"style="color:#428bca;">详情</p>')

    def show_time(self, obj):
        classshopskuobjs = classshopsku(connection, redis_conn, obj.ShopName)
        rt = u'在线数据刷新:<br>%s <br>上架(UTC):<br>%s <br>平台最近更新(UTC):<br>%s' % \
             (obj.RefreshTime, obj.DateUploaded, obj.LastUpdated)
        for shopsku in listingobjs.getShopSKUList(obj.ProductID):
            sku = classshopskuobjs.getSKU(shopsku)
            if sku is not None:
                # rt = rt + u'<br>商品最近刷新:<br>%s' % (py_SynRedis_pub_obj.getFromHashRedis('', sku, 'KC_updateTime'))
                rt = rt + u'<br>商品最近刷新:<br>%s' % (classsku_obj.get_updatetime_by_sku(sku))
                break
        return mark_safe(rt)

    show_time.short_description = mark_safe('<p align="center" style="width:150px;color:#428bca;">时间</p>')

    def show_SKU_list(self, obj):  # <label><input type="checkbox" name="shopskucheck_%s_%s"></label>
        classshopskuobjs = classshopsku(connection, redis_conn, obj.ShopName)
        activeflag = self.request.GET.get('EXPRESS', 'STANDARD')
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
        sInfors = py_SynRedis_tables_obj.readData_Redis_table(infor)
        num = 0
        for a, sinfor in enumerate(sInfors):
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
                calculate_price_obj = calculate_price(str(sinfor['SKU']), float(sinfor['SKUKEY'][2]),
                                                      float(sinfor['SKUKEY'][3]))
                profitrate_info = calculate_price_obj.calculate_profitRate(sellingPrice, platformCountryCode='WISH-US',
                                                                           DestinationCountryCode='US')
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

            rt = u'%s <tr %s><td><label><input type="checkbox" name="shopskucheck" id="%s_%s_%s" ></label></td>' \
                 u'<td>%s</td><td>%s</td><td>%s</td><td>%s</td>' \
                 u'<td>%s</td><td>%s</td><td>%s</td><td><a><span id="%s">%s</span></a></td><td>%s</td>' % \
                 (rt, style, obj.id, a, obj.ShopName, sinfor['SKU'], goodsstatus,
                  sinfor['SKUKEY'][1], sinfor['ShopSKU'].replace('<', '&lt;').replace('>', '&gt;'),
                  sinfor['ShopSKUKEY'][0],
                  sinfor['ShopSKUKEY'][1], sinfor['ShopSKUKEY'][2], profit_id, profitrate, sinfor['ShopSKUKEY'][-1],)
            rt = u"%s<script>$('#%s').on('click',function()" \
                 u"{layer.open({type:2,skin:'layui-layer-lan',title:'算价表'," \
                 u"fix:false,shadeClose: true,maxmin:true,area:['1300px','900px']," \
                 u"content:'/price_list/?SKU=%s&sellingPrice=%s&platformCountryCode=%s&DestinationCountryCode=%s',});});</script>" % (
                 rt, profit_id, sinfor['SKU'], sellingPrice, 'WISH-US', 'US')

        rt = u'%s<tr><td></td><td><a id="link_id_%s">查看变体</a></td></tr>' % (rt, obj.id)
        rt = u"%s</tbody></table><script>$('#link_id_%s').on('click',function()" \
             u"{var index = layer.open({type:2,skin:'layui-layer-lan',title:'%s'," \
             u"fix:false,shadeClose: true,maxmin:true,area:['90%%','80%%'],btn: ['关闭页面']," \
             u"content:'/t_online_info_wish_store/ShopSKU/?abc=%s&express=%s&readonly=readonly',});" \
             u"});</script>" % (rt, obj.id, activeflag, obj.ProductID, activeflag)

        # rt = rt + u"<script>function en_id_%s(shopsku) {layer.confirm(shopsku + '  请问确定要进行上架吗？'," \
        #           u"{btn: ['确定','算了'],btn1:function(){static_refresh('/up_dis_by_wish_api_shopsku/?enshopsku='+shopsku+" \
        #           u"'&shopname=%s&flag=0');},});}</script>" % (obj.id, obj.ShopName)
        # rt = rt + u"<script>function dis_id_%s(shopsku) {layer.confirm(shopsku + '  请问确定要进行下架吗？'," \
        #           u"{btn: ['确定','算了'],btn1:function(){static_refresh('/up_dis_by_wish_api_shopsku/?disshopsku='+shopsku+" \
        #           u"'&shopname=%s&flag=0')},});}</script>" % (obj.id, obj.ShopName)
        return mark_safe(rt)

    show_SKU_list.short_description = mark_safe(u'<p align="center"style="color:#428bca;">变体详细信息</p>')

    def show_orders7days(self, obj):
        rt = u"<a id='show_orderlist_%s' title='查看日销量趋势图'>销量查看</a>" \
             u"<script>$('#show_orderlist_%s').on('click',function()" \
             u"{layer.open({type:2,skin:'layui-layer-lan',title:'查看全部'," \
             u"fix:false,shadeClose: true,maxmin:true,area:['1000px','600px']," \
             u"content:'/t_online_info_wish/order1day/?aID=%s',});});" \
             u"</script>" % (obj.id, obj.id, obj.ProductID)
        update = u"<br><a id='edit_update_%s' title='查看链接主信息'>链接信息</a>" \
                 u"<script>$('#edit_update_%s').on('click',function()" \
                 u"{layer.open({type:2,skin:'layui-layer-lan',title:'查看'," \
                 u"fix:false,shadeClose: true,maxmin:true,area:['70%%','80%%'],btn: ['关闭页面']," \
                 u"content:'/edit_update_by_wish_api_listid/?%s',});});" \
                 u"</script>" % (obj.id, obj.id, urlencode({'productid': obj.ProductID, 'shopname': obj.ShopName, 'readonly': 'readonly'}))
        # syn = u'<br><a onclick= "static_refresh(\'%s\')" title="同步在线数据">同步链接</a>' % (
        # '/syndata_by_wish_api/?syn=%s' % obj.ProductID,)
        #
        # More = u'<br><a style="cursor:hand" onclick="isHidden(\'More_%s\')" title="展开更多" >点击更多<b class="caret"></b></a>' % obj.id
        #
        # HiddenDiv1 = u'<br><div id="More_%s" style="display:none">' % obj.id
        #
        # synproduct = u'<a onclick="static_refresh(\'%s\')"title="同步商品SKU信息">同步商品</a>' % (
        # '/refresh_sku_info/?productid=%s' % obj.ProductID,)
        # up = u'<br><a onclick="enable_id_%s(\'%s\')"title="对整个listing做上架操作">链接上架</a>' % (obj.id, obj.ProductID,)
        # down = u'<br><a onclick="disable_id_%s(\'%s\')"title="对整个listing做下架操作">链接下架</a>' % (obj.id, obj.ProductID,)
        #
        # en = u"<script>function enable_id_%s(listingid) {layer.confirm(listingid + '  请问确定要进行上架吗？'," \
        #      u"{btn: ['确定','算了'],btn1:function(){static_refresh('/syndata_by_wish_api/?enable='+listingid)},});}" \
        #      u"</script>" % (obj.id)
        #
        # dis = u"<script>function disable_id_%s(listingid) {layer.confirm(listingid + '  请问确定要进行下架吗？'," \
        #       u"{btn: ['确定','算了'],btn1:function(){static_refresh('/syndata_by_wish_api/?disable='+listingid)},});}" \
        #       u"</script>" % (obj.id)

        pb_show = ''
        pb_look = ''
        if obj.ADShow == 1:
            pcount = t_wish_pb_campaignproductstats.objects.filter(product_id=obj.ProductID,
                                                                   campaign_state__in=['STOPPED', 'STARTED']).count()
            pb_show = u'<br>广告查看'
            if pcount > 0:
                pb_look = u'<br><a href="/Project/admin/skuapp/t_wish_pb_campaignproductstats/?product_id=%s&campaign_state=STOPPED,STARTED" ' \
                          u'title="点击查看正在运行的广告" target="_blank" style="color: green;">在运行中</a>' % obj.ProductID
            else:
                pb_look = u'<br><a href="/Project/admin/skuapp/t_wish_pb_campaignproductstats/?product_id=%s&campaign_state=CANCELLED,PENDING,NEW,SAVED,ENDED" ' \
                          u'title="点击查看已经停止的广告" target="_blank" style="color: red;">已经停止</a>' % obj.ProductID

        HiddenDiv2 = '</div>'

        rt = rt + update + HiddenDiv2 + pb_show + pb_look
        return mark_safe(rt)

    show_orders7days.short_description = mark_safe(u'<p style="width:40px;color:#428bca;" align="center">操作选项</p>')

    list_display = ('show_Picture', 'show_Title_ProductID', 'show_Remarks', 'Orders7Days', 'OfSales',
                    'show_SKU_list', 'show_time', 'show_orders7days',)
    # list_editable = ('Remarks')
    list_display_links = ('',)

    def get_list_queryset(self, ):
        request = self.request
        qs = super(t_online_info_wish_Admin, self).get_list_queryset()
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
                messages.error(request, "你输入了一个不合法的整数！")

            seachfilter = {}

            status = request.GET.get('status')
            # eShopList = t_store_configuration_file.objects.filter(Status='-1').values_list('ShopName_temp', flat=True)
            if status == 'online':  # 在线
                seachfilter['AdStatus'] = '1'
                seachfilter['SName'] = '0'

                # qs = qs.exclude(SName='-1').exclude(AdStatus__in=['-1', '-2'])
                # # .filter(ReviewState='approved', Status='Enabled')

            elif status == 'offline':  # 不在线
                seachfilter['AdStatus'] = '0'
                seachfilter['SName'] = '0'
                # qs = qs.exclude(ReviewState='approved', Status='Enabled').exclude(SName='-1').exclude(AdStatus__in=['-1', '-2'])

            elif status == 'storeError':  # 店铺状态异常
                seachfilter['SName'] = '-1'

            elif status == 'doError':  # 单条状态异常的
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

            orders7DaysStart = request.GET.get('orders7DaysStart')
            if orders7DaysStart:
                seachfilter['Orders7Days__gte'] = orders7DaysStart
                # qs = qs.filter(Orders7Days__gte=orders7DaysStart)

            orders7DaysEnd = request.GET.get('orders7DaysEnd')
            if orders7DaysEnd:
                seachfilter['Orders7Days__lt'] = orders7DaysEnd
                # qs = qs.filter(Orders7Days__lt=orders7DaysEnd)

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

            title = request.GET.get('Title')
            if title:
                seachfilter['Title__icontains'] = title
                # qs = qs.filter(Title__icontains=title)

            Published = request.GET.get('Published')
            if Published:
                seachfilter['Published__exact'] = Published
                # qs = qs.filter(Published__exact=Published)

            is_promoted = request.GET.get('is_promoted')
            if is_promoted:
                seachfilter['is_promoted__exact'] = is_promoted
                # qs = qs.filter(is_promoted__exact=is_promoted)

            WishExpress = request.GET.get('WishExpress')
            if WishExpress:
                seachfilter['WishExpress__icontains'] = WishExpress

            WishExpressYN = request.GET.get('WishExpressYN')
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
            if USExpressType:
                seachfilter['WishExpressType__exact'] = USExpressType

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

            # 商品状态查询
            skustatus = request.GET.get('skustatus')  # 商品SKU状态
            goodsstatus = []
            if skustatus == '1':
                goodsstatus = [1000, 1100, 1010, 1001, 1110, 1101, 1011, 1111]  # 正常
            if skustatus == '2':
                goodsstatus = [100, 1100, 110, 101, 1110, 1101, 111, 1111]  # 售完下架
            if skustatus == '3':
                goodsstatus = [10, 1010, 110, 11, 1011, 1110, 111, 1111]  # 临时下架
            if skustatus == '4':
                goodsstatus = [1, 1001, 101, 11, 1101, 111, 1011, 1111]  # 停售
            if goodsstatus:
                seachfilter['GoodsFlag__in'] = goodsstatus
                # qs = qs.filter(GoodsFlag__in=goodsstatus)

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
                CrossMainSKU = t_product_enter_ed.objects.filter(**JZLDict).values_list('MainSKU', flat=True)

            # 领用人 查询
            MainSKUClaim = request.GET.get('MainSKUClaim')  # 主SKU领用人查询
            MainSKULISTClaim = []
            if MainSKUClaim:
                MainSKULISTClaim = t_product_depart_get.objects.filter(StaffName=MainSKUClaim,
                                                                       DepartmentID__in=('4', '5')).values_list(
                    'MainSKU', flat=True)

            LargeCategory = request.GET.get('LargeCategory')  # 大类
            SmallCategory = request.GET.get('SmallCategory')  # 小类
            if LargeCategory:
                seachfilter['MainSKULargeCate__exact'] = LargeCategory
            if SmallCategory:
                seachfilter['MainSKUSmallCate__exact'] = SmallCategory

            kcStart = request.GET.get("kcStart")
            ShippingStart = request.GET.get('ShippingStart')
            onlinedict = {}
            if kcStart and express != 'STANDARD':
                onlinedict['%sExpressInventory__gte' % express] = kcStart
            if ShippingStart and express != 'STANDARD':
                onlinedict['%sExpressShipping__gte' % express] = ShippingStart

            kcEnd = request.GET.get("kcEnd")
            ShippingEnd = request.GET.get('ShippingEnd')
            if kcEnd and express != 'STANDARD':
                onlinedict['%sExpressInventory__lt' % express] = kcEnd
            if ShippingEnd and express != 'STANDARD':
                onlinedict['%sExpressShipping__lt' % express] = ShippingEnd
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

            if seachfilter:
                qs = qs.filter(**seachfilter)

            return qs
        except Exception, e:
            messages.error(request, u'查询条件错误，请联系IT人员！%s' % e)
            return qs