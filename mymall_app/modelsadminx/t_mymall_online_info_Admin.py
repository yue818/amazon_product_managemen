#!/usr/bin/python
# -*- coding: utf-8 -*-

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


class t_mymall_online_info_Admin(object):
    # site_left_menu_flag_joom = True
    mymall_listing_plugin = True
    mymall_search_box_flag = True
    mymall_site_left_menu_tree_flag = True

    list_display = (
        'show_Picture',
        'show_Title_ProductID',
        # 'show_Remarks',
        'Orders7Days',
        # 'OfSales',
        'Status',
        # 'ReviewState',
        'show_SKU_list',
        'show_time',
        # 'discount',
        # 'threshold',
        # 'cutprice_flag',
        # 'CutPriceDetail',
        'show_orders7days',
    )
    list_display_links = ('',)
    list_per_page = 20
    list_max_show_all = 100

    actions = [
        'batch_update_data_by_mymall_api',
        'batch_change_data_action',
        # 'batch_recover_cut_price_data',
    ]

    def has_add_permission(self, ):
        return False

    def has_delete_permission(self, obj=None):
        return False

    # def tortInfo(self, TortInfo):
    #     if TortInfo == 'WY':
    #         rt = u'<div title="Joom侵权" style="float:left;width: 20px;height: 20px;background-color: #FF3333;text-align: center;line-height: 20px;border-radius: 4px">W</div>'
    #     elif TortInfo == 'N':
    #         rt = u'<div title="未侵权" style="float:left;width: 20px;height: 20px;background-color: #66FF66;text-align: center;line-height: 20px;border-radius: 4px">N</div>'
    #     else:
    #         rt = u'<div title="其他平台侵权" style="float:left;width: 20px;height: 20px;background-color: #FFCC33;text-align: center;line-height: 20px;border-radius: 4px">O</div>'
    #     return rt

    # def status(self, ReviewState):
    #     if ReviewState == 'approved' or ReviewState == '0':
    #         rt = '<div title="已批准" style="float:left;width: 20px;height: 20px;background-color: #66FF66;text-align: center;line-height: 20px;border-radius: 4px">已</div>'
    #     elif ReviewState == 'pending' or ReviewState == '2':
    #         rt = '<div title="待审核" style="float:left;width: 20px;height: 20px;background-color: #FFCC33;text-align: center;line-height: 20px;border-radius: 4px">审</div>'
    #     elif ReviewState == 'rejected' or ReviewState == '1':
    #         rt = '<div title="被拒绝" style="float:left;width: 20px;height: 20px;background-color: #FF3333;text-align: center;line-height: 20px;border-radius: 4px">拒</div>'
    #     else:
    #         rt = ''
    #     return rt

    # def show_Remarks(self, obj):
    #     rt = ''
    #     Remarks_objs = t_store_marketplan_execution.objects.filter(ProductID=obj.ProductID).values_list('Remarks')
    #     if len(Remarks_objs) > 0:
    #         Remarks_objs = eval(Remarks_objs[0][0])
    #         for ktime, v in Remarks_objs.items():
    #             rt = u'<font color="red">%s%s:%s单</font><br>' % (rt, ktime, v)
    #     return mark_safe(rt)

    # show_Remarks.short_description = mark_safe(u'<p align="center"style="color:#428bca;">营销时间/单</p>')

    def show_Picture(self, obj):
        url = str(obj.Image).replace('https', 'http')
        rt = '<div><img src="%s" width="120" height="120" alt = "%s" title="%s"/></div>' % (url, url, url)
        return mark_safe(rt)

    show_Picture.short_description = mark_safe(u'<p align="center"style="color:#428bca;">图片</p>')

    def show_Title_ProductID(self, obj):
        rt = django_wrap(obj.Title, ' ', 6)
        rt = u'%s<br>产品ID:<a href=" https://pandao.ru/product/%s" target="_blank">%s</a>' % (rt, obj.ProductID, obj.ProductID)
        rt = u'%s<br>卖家简称:%s' % (rt, obj.ShopName)
        if obj.Published:
            rt = u'%s<br>铺货人:%s' % (rt, obj.Published)
        if obj.Seller:
            seller = obj.Seller
        else:
            seller = t_store_configuration_file.objects.get(ShopName__exact=obj.ShopName).Seller
        rt = u'%s<br>店长/销售员:%s' % (rt, seller)
        rt = u'%s<br>刊登人:%s' % (rt, seller)
        return mark_safe(rt)

    show_Title_ProductID.short_description = mark_safe(u'<p align="center"style="color:#428bca;">详情</p>')

    def show_time(self, obj):
        rt = u'在线数据刷新:<br>%s <br>上架:<br>%s <br>平台最近更新:<br>%s' % \
             (obj.RefreshTime, obj.DateUploaded, obj.LastUpdated)
        # for shopsku in obj.ShopSKU.split(','):
        #     sku = classshopskuobjs.getSKU(shopsku)
        #     if sku is not None:
        #         rt = rt + u'<br>商品最近刷新:<br>%s' % (classsku_obj.get_updatetime_by_sku(sku))
        #         break
        return mark_safe(rt)

    show_time.short_description = mark_safe('<p align="center" style="width:150px;color:#428bca;">时间</p>')

    def show_SKU_list(self, obj):
        rt = u'<table class="table table-condensed">' \
             u'<thead>' \
             u'<tr bgcolor="#C00">' \
             u'<th style="text-align:center;">子SKU</th>' \
             u'<th style="text-align:center;">商品状态</th>' \
             u'<th style="text-align:center;">可卖天数</th>' \
             u'<th style="text-align:center;">店铺SKU</th>' \
             u'<th style="text-align:center;">库存量</th>' \
             u'<th style="text-align:center;">价格</th>' \
             u'<th style="text-align:center;">运费</th>' \
             u'<th style="text-align:center;">利润率</th>' \
             u'<th style="text-align:center;">启用状态</th>' \
             u'</tr>' \
             u'</thead><tbody>'
        # u'<th style="text-align:center;">采购未入库</th>' \
        # u'<th style="text-align:center;">库存</th>' \
        # u'<th style="text-align:center;">占用</th>' \
        # u'<th style="text-align:center;">可用数量</th>' \
        # u'<th style="text-align:center;">操作</th>' \
        shopskulist = obj.ShopSKU.split(',')
        infor = []
        for i, shopsku in enumerate(shopskulist):
            if i >= 5:
                break
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
        for sinfor in sInfors:
            mymall_product_shop_sku_info = t_mymall_online_info_detail.objects.filter(ProductID=obj.ProductID, ShopSKU=sinfor['ShopSKU']).values('Quantity', 'Price', 'Shipping', 'Status')

            if mymall_product_shop_sku_info:
                shopskuQuantity = mymall_product_shop_sku_info[0]['Quantity']
                shopskuPrice = '%.2f' % float(mymall_product_shop_sku_info[0]['Price'])
                shopskuShipping = mymall_product_shop_sku_info[0]['Shipping']
                shopskuStatus = mymall_product_shop_sku_info[0]['Status']
                if shopskuStatus == '1':
                    shopskuStatus = 'True'
                else:
                    shopskuStatus = 'False'
            else:
                shopskuQuantity = ''
                shopskuPrice = ''
                shopskuShipping = ''
                shopskuStatus = ''

            inventory = sinfor['SKUKEY'][2]
            if inventory is None or inventory == -1:
                inventory = 0
            else:
                inventory = str(inventory).split('.')[0]
                if inventory == '':
                    inventory = '0'
            occupyNum = sinfor['SKUKEY'][3]
            if occupyNum is None or occupyNum == -1:
                occupyNum = 0
            else:
                occupyNum = str(occupyNum).split('.')[0]
                if occupyNum == '':
                    occupyNum = '0'

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
            elif shopskuStatus == 'False':
                style = 'class="active"'  # 正常  Disabled 为 灰色
            elif shopskuStatus == 'True':
                style = 'class="success"'  # 正常  Enabled 为 绿色

            if not shopskuPrice:
                shopskuPrice = 0

            if not shopskuShipping:
                shopskuShipping = 0

            try:
                sellingPrice = float(shopskuPrice) + float(shopskuShipping)
                calculate_price_obj = calculate_price(str(sinfor['SKU']))
                profitrate_info = calculate_price_obj.calculate_profitRate(sellingPrice, platformCountryCode='MALL', DestinationCountryCode='RUS')
            except:
                profitrate_info = ''
            if profitrate_info:
                profitrate = '%.2f' % float(profitrate_info['profitRate'])
            else:
                profitrate = ''

            profit_id = 'profit_id' + '_' + str(num) + '_' + str(sinfor['SKU'])
            num += 1

            # u'<td>%s</td>' \
            # u'<td>%s</td>' \
            # u'<td>%s</td>' \
            # u'<td>%s</td>' \
            rt = u'%s <tr %s>' \
                 u'<td>%s</td>' \
                 u'<td>%s</td>' \
                 u'<td>%s</td>' \
                 u'<td style="BORDER-LEFT: #DDDDDD 1px solid;">%s</td>' \
                 u'<td>%s</td>' \
                 u'<td>%s</td>' \
                 u'<td>%s</td>' \
                 u'<td><a><span id="%s">%s</span></a></td>' \
                 u'<td style="BORDER-RIGHT: #DDDDDD 1px solid;">%s</td></tr>' % \
                 (rt, style, sinfor['SKU'],
                  # sinfor['SKUKEY'][0],
                  goodsstatus,
                  # inventory, occupyNum, int(inventory) - int(occupyNum),
                  can_sold_days, sinfor['ShopSKU'].replace('<', '&lt;').replace('>', '&gt;'),
                  shopskuQuantity, shopskuPrice, shopskuShipping, profit_id, profitrate, shopskuStatus)

            rt = u"%s<script>$('#%s').on('click',function()" \
                 u"{layer.open({type:2,skin:'layui-layer-lan',title:'算价表'," \
                 u"fix:false,shadeClose: true,maxmin:true,area:['1300px','900px']," \
                 u"content:'/price_list/?SKU=%s&sellingPrice=%s&platformCountryCode=%s&DestinationCountryCode=%s',});});" \
                 u"</script>" % (rt, profit_id, sinfor['SKU'], shopskuPrice, 'MALL', 'RUS')

            # shopsku = sinfor['ShopSKU'].replace('#', '%23')

            # rt = u'%s<td style="text-align:center;"><a onclick="en_id_%s(\'%s\')">上架</a>' % (rt, obj.id, shopsku) + \
            #      u'//<a onclick="dis_id_%s(\'%s\')">下架</a></td></tr> ' % (obj.id, shopsku)
        rt = u'%s<tr><td><a id="link_id_%s">编辑变体</a></td></tr>' % (rt, obj.id)
        rt = u"%s</tbody></table><script>$('#link_id_%s').on('click',function()" \
             u"{layer.open({type:2,skin:'layui-layer-lan',title:'全部变体信息'," \
             u"fix:false,shadeClose: true,maxmin:true,area:['1600px','800px']," \
             u"content:'/mymallapp/t_mymall_online_info/ShopSKU/?abc=%s',});});</script>" % (rt, obj.id, obj.ProductID)

        # rt = rt + u"<script>function en_id_%s(shopsku) {layer.confirm(shopsku + '  请问确定要进行上架吗？'," \
        #           u"{btn: ['确定','算了'],btn1:function(){shopsku=shopsku.replace('#', '%%23');static_refresh('/mymallapp/up_dis_by_mymall_api_shopsku/?enshopsku='+shopsku+" \
        #           u"'&shopname=%s&flag=0');},});}</script>" % (obj.id, obj.ShopName)
        # rt = rt + u"<script>function dis_id_%s(shopsku) {layer.confirm(shopsku + '  请问确定要进行下架吗？'," \
        #           u"{btn: ['确定','算了'],btn1:function(){shopsku=shopsku.replace('#', '%%23');static_refresh('/mymallapp/up_dis_by_mymall_api_shopsku/?disshopsku='+shopsku+" \
        #           u"'&shopname=%s&flag=0')},});}</script>" % (obj.id, obj.ShopName)
        return mark_safe(rt)

    show_SKU_list.short_description = mark_safe('<p align="center"style="color:#428bca;">子SKU</p>')

    def show_orders7days(self, obj):
        # rt = u"<a id='show_orderlist_%s' title='查看日销量趋势图'>销量</a>" \
        #      u"<script>$('#show_orderlist_%s').on('click',function()" \
        #      u"{layer.open({type:2,skin:'layui-layer-lan',title:'查看全部'," \
        #      u"fix:false,shadeClose: true,maxmin:true,area:['1000px','600px']," \
        #      u"content:'/t_online_info_wish/order1day/?aID=%s',});});" \
        #      u"</script>" % (obj.id, obj.id, obj.ProductID)
        # update = u"<br><a id='edit_update_%s' title='编辑该listing的其他信息'>编辑</a>" \
        #          u"<script>$('#edit_update_%s').on('click',function()" \
        #          u"{layer.open({type:2,skin:'layui-layer-lan',title:'编辑-更新'," \
        #          u"fix:false,shadeClose: true,maxmin:true,area:['1200px','800px'],btn: ['关闭页面']," \
        #          u"content:'/edit_update_by_wish_api_listid/?productid=%s&parentsku=%s&shopname=%s',});});" \
        #          u"</script>" % (obj.id, obj.id, obj.ProductID, obj.ParentSKU, obj.ShopName)
        syn = u'<br><a onclick= "static_refresh(\'%s\')" title="同步在线数据">同步</a>' % ('/mymallapp/syndata_by_mymall_api/?syn=%s&shopname=%s' % (obj.ProductID, obj.ShopName))

        # pb_objs = t_wish_pb.objects.filter(ProductID=obj.ProductID).values_list('Duration', 'PbFee', 'PbCount','id').order_by('id')
        # if pb_objs.exists():
        #     pb = u'<br><a id="ll_%s" title="点击查看广告备注信息" style="color:red;" >广告</a>'%obj.id

        #     pb_more = u"<script>$('#ll_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan'," \
        #               u"title:'全部广告备注',fix:false,shadeClose: true,maxmin:true,area:['500px','800px']," \
        #               u"content:'/t_online_info_wish/PB/?pb=%s',});});</script>"%(obj.id, obj.ProductID)
        # else:
        #     pb = ''
        #     pb_more = ''

        # More= u'<br><a style="cursor:hand" onclick="isHidden(\'More_%s\')" title="展开更多" >更多<b class="caret"></b></a>'%obj.id

        # HiddenDiv1 = u'<br><div id="More_%s" style="display:none">'%obj.id

        up = u'<br><a onclick="enable_id_%s(\'%s\', \'%s\')"title="对整个listing做上架操作">上架</a>' % (obj.id, obj.ProductID, obj.ShopName)
        down = u'<br><a onclick="disable_id_%s(\'%s\', \'%s\')"title="对整个listing做下架操作">下架</a>' % (obj.id, obj.ProductID, obj.ShopName)

        en = u"<script>function enable_id_%s(listingid, shopname) {layer.confirm(listingid + '  请问确定要进行上架吗？'," \
             u"{btn: ['确定','算了'],btn1:function(){static_refresh('/mymallapp/syndata_by_mymall_api/?enable='+listingid+'&shopname='+shopname)},});}" \
             u"</script>" % (obj.id)

        dis = u"<script>function disable_id_%s(listingid, shopname) {layer.confirm(listingid + '  请问确定要进行下架吗？'," \
              u"{btn: ['确定','算了'],btn1:function(){static_refresh('/mymallapp/syndata_by_mymall_api/?disable='+listingid+'&shopname='+shopname)},});}" \
              u"</script>" % (obj.id)

        # HiddenDiv2 = '</div>'

        # rt = rt + update + syn + pb + pb_more + More + HiddenDiv1 + synproduct + up + down + en + dis + HiddenDiv2
        rt = syn + up + down + en + dis
        return mark_safe(rt)

    show_orders7days.short_description = mark_safe(u'<p style="width:40px;color:#428bca;" align="center">操作</p>')

    # def CutPriceDetail(self, obj):
    #     Cutprice_Datetime = ''
    #     SetResult = ''
    #     Recover_Datetime = ''
    #     RecoverResult = ''
    #     ResMess = ''
    #     RecoverMess = ''
    #     cutprice_log = t_mymall_cutprice_log.objects.get(ProductID=obj.ProductID)
    #     if cutprice_log:
    #         Cutprice_Datetime = cutprice_log.Cutprice_Datetime
    #         SetResult = cutprice_log.SetResult
    #         Recover_Datetime = cutprice_log.Recover_Datetime
    #         RecoverResult = cutprice_log.RecoverResult
    #         if SetResult == 'ALL SUCCESS':
    #             ResMess = SetResult
    #         else:
    #             ResMess = str(cutprice_log.ResMess)
    #         if RecoverResult == 'ALL SUCCESS':
    #             RecoverMess = RecoverResult
    #         else:
    #             RecoverMess = str(cutprice_log.RecoverMess)

    #     rt = u'降价时间:<br>%s<br>降价操作结果:<br>%s<br>降价操作结果详情:<br>%s<br>' \
    #         u'恢复时间:<br>%s<br>恢复操作结果:<br>%s<br>恢复操作结果详情:<br>%s<br>' % \
    #         (Cutprice_Datetime, SetResult, ResMess, Recover_Datetime, RecoverResult, RecoverMess)
    #     return mark_safe(rt)

    # CutPriceDetail.short_description = mark_safe('<p align="center" style="width:150px;color:#428bca;">降价详情</p>')

    def batch_update_data_by_mymall_api(self, request, objs):
        success_list = list()
        error_dict = dict()
        for i, obj in enumerate(objs):
            api_res = syndata_by_mymall_api([obj.ProductID], obj.ShopName, 'syn')
            if api_res['Code'] != 0:
                error_dict[obj.ProductID] = api_res['messages']
            else:
                success_list.append(obj.ProductID)
        messages.success(request, u'同步完成，成功 %s 个，失败 %s 个，失败信息：%s' % (len(success_list), len(error_dict.keys()), error_dict))

    batch_update_data_by_mymall_api.short_description = u'同步选中商品数据'

    def batch_change_data_action(self, request, objs):
        param = request.get_full_path()
        idList = []
        for obj in objs:
            idList.append(str(obj.ProductID))
        return HttpResponseRedirect('/mymallapp/show_mymall_change_data/?ProductID=%s&param=%s' % (idList, param))

    batch_change_data_action.short_description = u'批量修改选中商品价格和库存'

    def batch_recover_cut_price_data(self, request, objs):
        for obj in objs:
            obj.cutprice_flag = False
            obj.save()

    batch_recover_cut_price_data.short_description = u'恢复选中降价商品'

    def get_list_queryset(self, ):
        request = self.request
        qs = super(t_mymall_online_info_Admin, self).get_list_queryset()
        qs = qs.order_by('-Orders7Days')

        shopname = request.GET.get('shopname', '').strip()
        seller = request.GET.get('seller', '').strip()
        productId = request.GET.get('productID', '').strip()
        mainSKU = request.GET.get('mainSKU', '').strip()
        shopsku = request.GET.get('ShopSKU', '').strip()
        title = request.GET.get('Title', '').strip()
        Published = request.GET.get('Published', '').strip()

        reviewState = request.GET.get('reviewState', '')
        tortinfo = request.GET.get('tortInfo', '')
        Estatus = request.GET.get('Estatus', '')
        dataSources = request.GET.get('dataSources', '')
        # status = request.GET.get('status', '')
        # cutprice = request.GET.get('cutprice', '')

        orders7DaysStart = request.GET.get('orders7DaysStart', '')
        orders7DaysEnd = request.GET.get('orders7DaysEnd', '')
        refreshTimeStart = request.GET.get('refreshTimeStart', '')
        refreshTimeEnd = request.GET.get('refreshTimeEnd', '')
        dateUploadedStart = request.GET.get('dateUploadedStart', '')
        dateUploadedEnd = request.GET.get('dateUploadedEnd', '')
        lastUpdatedStart = request.GET.get('lastUpdatedStart', '')
        lastUpdatedEnd = request.GET.get('lastUpdatedEnd', '')
        OfSalesStart = request.GET.get('OfSalesStart', '')
        OfSalesEnd = request.GET.get('OfSalesEnd', '')

        market_timeStart = request.GET.get('market_timeStart', '')
        market_timeEnd = request.GET.get('market_timeEnd', '')

        if shopsku.strip() != '':
            t_online_info_objs = t_mymall_online_info_detail.objects.filter(ShopSKU=shopsku.strip()).values('ProductID')
            prodilist = set()
            for t_online_info_obj in t_online_info_objs:
                prodilist.add(t_online_info_obj['ProductID'])
            qs = qs.filter(ProductID__in=prodilist)

        if mainSKU.strip() != '':
            t_online_info_objs = t_mymall_online_info_detail.objects.filter(MainSKU=mainSKU.strip()).values('ProductID')
            prodilist = set()
            for t_online_info_obj in t_online_info_objs:
                prodilist.add(t_online_info_obj['ProductID'])
            qs = qs.filter(ProductID__in=prodilist)

        if Estatus == 'Enabled':
            Estatus = '1'
        elif Estatus == 'Disabled':
            Estatus = '0'

        if reviewState == 'approved':
            reviewState = '0'
        elif reviewState == 'rejected':
            reviewState = '1'
        elif reviewState == 'pending':
            reviewState = '2'

        searchList = {
            'ShopName__exact': shopname,
            'Seller__exact': seller,
            'ReviewState__exact': reviewState,
            'TortInfo__exact': tortinfo,
            'Status__exact': Estatus,
            'DataSources__exact': dataSources,
            'ProductID__exact': productId,
            'Orders7Days__gte': orders7DaysStart,
            'Orders7Days__lt': orders7DaysEnd,
            'RefreshTime__gte': refreshTimeStart,
            'RefreshTime__lt': refreshTimeEnd,
            'DateUploaded__gte': dateUploadedStart,
            'DateUploaded__lt': dateUploadedEnd,
            'LastUpdated__gte': lastUpdatedStart,
            'LastUpdated__lt': lastUpdatedEnd,
            'Title__icontains': title,
            'Published__exact': Published,
            'market_time__gte': market_timeStart,
            'market_time__lt': market_timeEnd,
            'OfSales__gte': OfSalesStart,
            'OfSales__lt': OfSalesEnd,
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
            except Exception:
                messages.error(request, u'输入的查询数据有问题！')

        # # 在线
        # if status == 'online':
        #     # qs = qs.filter(ReviewState='approved', Status='True')
        #     qs = qs.filter(ReviewState='0', Status='1')
        # # 不在线
        # elif status == 'offline':
        #     # qs = qs.filter(Q(ReviewState='approved', Status='False') | Q(ReviewState='pending'))
        #     qs = qs.filter(Q(ReviewState='0', Status='0') | Q(ReviewState='2'))
        # # 拒绝
        # elif status == 'reject':
        #     # qs = qs.filter(ReviewState='rejected')
        #     qs = qs.filter(ReviewState='1')
        # else:
        #     qs = qs

        # 降价筛选
        # if cutprice == 'cut_price_ing':
        #     qs = qs.filter(cutprice_flag=True)
        # elif cutprice == 'not_cut_price':
        #     qs = qs.filter(Q(cutprice_flag=False) | Q(cutprice_flag__isnull=True))
        # elif cutprice == 'cut_price_falied':
        #     product_list = list()
        #     if shopname:
        #         cps = t_mymall_cutprice_log.objects.filter(ShopName=shopname).exclude(SetResult="ALL SUCCESS").values('ProductID', 'OfSales')
        #     else:
        #         cps = t_mymall_cutprice_log.objects.exclude(SetResult="ALL SUCCESS").values('ProductID', 'OfSales')
        #     if cps:
        #         for i in cps:
        #             try:
        #                 pro_info = t_mymall_online_info.objects.get(ProductID=i['ProductID'])
        #             except t_mymall_online_info.DoesNotExist:
        #                 continue
        #             if pro_info.OfSales != i['OfSales']:
        #                 product_list.append(pro_info.ProductID)
        #     qs = qs.filter(ProductID__in=product_list)
        # elif cutprice == 'cut_price_orders':
        #     product_list = list()
        #     if shopname:
        #         cps = t_mymall_cutprice_log.objects.filter(ShopName=shopname, RecoverResult__isnull=True).values('ProductID', 'OfSales')
        #     else:
        #         cps = t_mymall_cutprice_log.objects.filter(RecoverResult__isnull=True).values('ProductID', 'OfSales')
        #     if cps:
        #         for i in cps:
        #             try:
        #                 pro_info = t_mymall_online_info.objects.get(ProductID=i['ProductID'])
        #             except t_mymall_online_info.DoesNotExist:
        #                 continue
        #             if pro_info.OfSales != i['OfSales']:
        #                 product_list.append(pro_info.ProductID)
        #     qs = qs.filter(ProductID__in=product_list)
        # elif cutprice == 'recover_price':
        #     product_list = list()
        #     if shopname:
        #         cps = t_mymall_cutprice_log.objects.filter(ShopName=shopname, RecoverResult__isnull=False).values('ProductID')
        #     else:
        #         cps = t_mymall_cutprice_log.objects.filter(RecoverResult__isnull=False).values('ProductID')
        #     if cps:
        #         for i in cps:
        #             product_list.append(i['ProductID'])
        #     qs = qs.filter(ProductID__in=product_list)
        # elif cutprice == 'recover_price_falied':
        #     product_list = list()
        #     failed_list = ['SOME SUCCESS', "ALL FAILED", "ERROR"]
        #     if shopname:
        #         cps = t_mymall_cutprice_log.objects.filter(ShopName=shopname, RecoverResult__in=failed_list).values('ProductID')
        #     else:
        #         cps = t_mymall_cutprice_log.objects.filter(RecoverResult__in=failed_list).values('ProductID')
        #     if cps:
        #         for i in cps:
        #             product_list.append(i['ProductID'])
        #     qs = qs.filter(ProductID__in=product_list)
        # else:
        #     qs = qs

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
