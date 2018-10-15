# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_cpc_ad_Admin.py
 @time: 2018-06-07 9:23
"""
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from django.utils.safestring import mark_safe
from skuapp.table.t_shopsku_information_binding import t_shopsku_information_binding
from skuapp.table.t_online_amazon_fba_inventory import t_online_amazon_fba_inventory
from skuapp.table.t_combination_sku_log import t_combination_sku_log
from django.contrib import messages
from skuapp.table.t_amazon_cpc_ad import t_amazon_cpc_ad
import datetime
from brick.public.django_wrap import django_wrap


class t_amazon_cpc_ad_Admin(object):

    search_box_flag = True
    amazon_cpc_ad = True

    def show_image_url(self, obj):
        url = u'%s' % obj.image_url
        site_url_dict = {'US': 'https://www.amazon.com/',
                         'UK': 'https://www.amazon.co.uk/',
                         'JP': 'https://www.amazon.co.jp/',
                         'DE': 'https://www.amazon.de/',
                         'FR': 'https://www.amazon.fr/',
                         'AU': 'https://www.amazon.com.au/'}

        if obj.shop_site and obj.shop_site in site_url_dict:
            site_url = site_url_dict[obj.shop_site]
        else:
            site_url = 'https://www.amazon.com/'

        if obj.Status == 'Incomplete':
            rt = '<div style="display: inline-block;width: 0;height: 0; line-height: 0;border: 8px solid transparent; border-top-color: #7a7c76; border-bottom-width: 0;"></div><span style="padding-left: 20px">变体</span>'
        else:
            rt = '<a href="%sdp/%s" target="_blank"><img src="%s"  width="150" height="150"  alt = "%s"  title="%s"  /></a>' % (site_url, obj.asin, url, url, url)
        return mark_safe(rt)
    show_image_url.short_description = mark_safe(u'<p style="color:#428BCA" align="center">图片</p>')

    def show_title(self, obj):
        if obj.Status == 'Incomplete':
            status = ''
        else:
            status = obj.Status

        if '+' not in obj.seller_sku and '*' in obj.seller_sku:
            seller_sku = obj.seller_sku.split('*')[0]
        else:
            seller_sku = obj.seller_sku
        t_shopsku_information_binding_obj = t_shopsku_information_binding.objects.filter(ShopSKU=seller_sku)
        if t_shopsku_information_binding_obj:
            sku = t_shopsku_information_binding_obj[0].SKU
            # 组合产品显示商品SKU合集
            if len(sku) == 6 and sku[0:2] == 'ZH':
                zh_obj = t_combination_sku_log.objects.filter(Com_SKU=sku)
                if zh_obj:
                    sku = zh_obj[0].Pro_SKU
        else:
            sku = obj.seller_sku

        count = 0
        sku_show = ''
        if sku:
            for i in sku:
                count += 1
                sku_show += i
                if count % 6 == 0:
                    sku_show += '<br>'

        count = 0
        seller_sku_show = ''
        if sku:
            for i in sku:
                count += 1
                seller_sku_show += i
                if count % 10 == 0:
                    seller_sku_show += '<br>'

        title_show = django_wrap(obj.title, ' ', 4)
        title = u'%s<br>ASIN: %s <br>SKU: %s<br>店铺SKU:  %s<br>状态:%s<br>店铺:%s' % (obj.title, obj.asin,  obj.sku, obj.seller_sku, status, obj.shop_name)
        # title = django_wrap(title, ' ', 3)
        if len(title) < 400:
            rt = title
        else:
            rt = """<script type="text/javascript">
                       $(document).ready(function(){
                         $("#but%s").click(function(){
                         $("#d%s").toggle();
                         $("#dd%s").toggle();
                         });
                       });
                       </script>
                       <p id="d%s" >%s......</p>
                       <p id="dd%s" hidden="hidden">%s</p>
                       <br/>
                       <button type="button" id="but%s">隐藏/全显</button>        
                       """ % (obj.id, obj.id, obj.id, obj.id, title[:400], obj.id, title, obj.id)
        return mark_safe(rt)
    # show_title.short_description = mark_safe(u'<p style="color:#428BCA" align="center">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;标题&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</p>')
    # show_title.short_description = mark_safe(u'<p style="color:#428BCA" align="center">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;标题&nbsp;&nbsp;&nbsp;&nbsp;&nbsp</p>')
    show_title.short_description = mark_safe(u'<p style="color:#428BCA" align="center">标题</p>')

    def show_score(self, obj):
        score_review = u'%s<br>%s<br>%s' % (None, obj.review_cnt, obj.score)
        return mark_safe(score_review)
    show_score.short_description = mark_safe(u'<p style="color:#428BCA" align="center">中差评数<br>评价总数<br>总评分</p>')

    def if_fba(self, obj):
        is_fba = u'否'
        fba_inventory_obj = t_online_amazon_fba_inventory.objects.filter(sku=obj.seller_sku, ShopName=obj.shop_name)
        if fba_inventory_obj and fba_inventory_obj[0].afn_listing_exists == 'Yes':
            is_fba = u'是'
        return mark_safe(is_fba)
    if_fba.short_description = mark_safe(u'<p style="color:#428BCA" align="center">FBA</p>')

    def show_is_fbm(self, obj):
        is_fbm = u'是'
        fba_inventory_obj = t_online_amazon_fba_inventory.objects.filter(sku=obj.seller_sku, ShopName=obj.shop_name)
        if fba_inventory_obj and fba_inventory_obj[0].afn_listing_exists == 'Yes':
            is_fbm = u'否'
        return mark_safe(is_fbm)
    show_is_fbm.short_description = mark_safe(u'<p style="color:#428BCA" align="center">FBM</p>')

    def show_fbm_quantity(self, obj):
        fbm_quantity = obj.quantity
        fba_inventory_obj = t_online_amazon_fba_inventory.objects.filter(sku=obj.seller_sku, ShopName=obj.shop_name)
        if fba_inventory_obj and fba_inventory_obj[0].afn_listing_exists == 'Yes':
            fbm_quantity = 0
        return mark_safe(fbm_quantity)
    show_fbm_quantity.short_description = mark_safe(u'<p style="color:#428BCA" align="center">库存</p>')

    def show_on_sale_date(self, obj):
        if obj.on_sale_date:
            sale_date = obj.on_sale_date
        else:
            sale_date = obj.create_date
        rt = u'%s<br><br><p><font  color="green">%s</p></font>' % (obj.create_date, sale_date)
        return mark_safe(rt)
    show_on_sale_date.short_description = mark_safe(u'<p style="color:#428BCA" align="center">创建日期</br>开售日期</p>')

    def show_inventory(self, obj):
        import urllib

        # is_fba = u'否'
        # fba_inventory_obj = t_online_amazon_fba_inventory.objects.filter(sku=obj.seller_sku)
        # if fba_inventory_obj and fba_inventory_obj[0].afn_listing_exists == 'Yes':
        #     is_fba = u'是'

        inventory = 0

        if obj.quantity:
            inventory = obj.quantity

        fba_inventory_obj = t_online_amazon_fba_inventory.objects.filter(ShopName=obj.shop_name, sku=obj.seller_sku)

        if fba_inventory_obj and fba_inventory_obj[0].afn_listing_exists == 'Yes':
            inventory = int(fba_inventory_obj[0].afn_fulfillable_quantity)

        if not obj.orders_15days:
            order_15 = 0
        else:
            order_15 = int(obj.orders_15days)

        if inventory < order_15 * 1.5:
            rt = u'<p id="inventory_%s"><font  color="red">%s</font><p/>' % (obj.id, inventory)
        else:
            rt = u'<p id="inventory_%s"><font  color="blue">%s</font><p/>' % (obj.id, inventory)
        seller_sku = urllib.quote(obj.seller_sku.decode('gbk', 'replace').encode('utf-8', 'replace'))
        rt_script = '''
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
        rt = rt + rt_script
        return mark_safe(rt)
    show_inventory.short_description = mark_safe(u'<p style="color:#428BCA" align="center">库存</p>')

    def show_sales(self, obj):
        import urllib
        try:
            if obj.Status == 'Incomplete':
                rt = ''
            else:
                seller_sku = urllib.quote(obj.seller_sku.decode('gbk', 'replace').encode('utf-8', 'replace'))
                rt = u'<p id="orders_%s"><font  color="blue">%s/%s/%s/%s</font><p/>' % (obj.id, obj.orders_7days, obj.orders_15days, obj.orders_30days, obj.orders_total)
                rt_script = '''
                                        <script>
                                            a = screen.width*0.8
                                            b = screen.height*0.7
                                             $("#orders_%s").on("click", function(){
                                              layer.open({
                                               type: 2,
                                               skin: "layui-layer-lan",
                                               title: "销量详情",
                                               fix: false,
                                               shadeClose: true,
                                               maxmin: true,
                                               area: ['1000px', '600px'],
                                               content: "/show_orders_detail/?seller_sku=%s&shopname=%s&asin=%s",
                                               btn: ["关闭页面"],
                                               });
                                           })
                                       </script>
                                       ''' % (obj.id, seller_sku, obj.shop_name, obj.asin)
                rt = rt + rt_script
        except Exception as e:
            rt = e
        return mark_safe(rt)

    show_sales.short_description = mark_safe(u'<p style="color:#428BCA" align="center">销量信息<br>(7/15/30/总)</p>')

    def show_ads_info(self, obj):
        rt = ''
        if obj.Status == 'Incomplete':  # 主体
            pass
        else:
            # rt = u'<table style="text-align:center;" border="1px" bordercolor="#CCCACA" cellpadding="3" cellspacing="1" bgcolor="#c1c1c1"">'
            # rt += u'<tr ><td style="width:70px">天数</td><td style="width:70px">销量</td><td style="width:70px">曝光</td><td style="width:70px">点击</td><td style="width:70px">CTR</td><td style="width:70px">广告花费</td> <td style="width:70px">销售额</td><td style="width:70px">转化率</td><td style="width:70px">Acos</td><td style="width:70px">广告依赖度</td></tr>'
            # rt += u'<tr><td style="width:70px">%s</td><td style="width:70px">%s</td><td style="width:70px">%s</td><td style="width:70px">%s</td><td style="width:70px">%s</td><td style="width:70px">%s</td>  <td style="width:70px">%s</td><td style="width:70px">%s</td><td style="width:70px">%s</td><td style="width:70px">%s</td></tr>' \
            #       % ('7', obj.ad_orders, obj.ad_sales, obj.ad_cost, obj.expose_cnt, obj.click_cnt, None, None, None, None)
            # rt += u'<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>  <td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' \
            #       % ('15', obj.ad_orders, obj.ad_sales, obj.ad_cost, obj.expose_cnt, obj.click_cnt, None, None, None, None)
            # rt += u'<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>  <td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' \
            #       % ('30', obj.ad_orders, obj.ad_sales, obj.ad_cost, obj.expose_cnt, obj.click_cnt, None, None, None, None)
            # rt += u'<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>  <td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' \
            #       u'</table>' % ('total', obj.ad_orders, obj.ad_sales, obj.ad_cost, obj.expose_cnt, obj.click_cnt, None, None, None, None)

            rt = u'未获取到广告数据'

            rt += u'<br><input id="ad_%s" type="button" value="广告管理" />' % obj.id

            rt_script = '''
                                <script>
                                    a = screen.width*0.8
                                    b = screen.height*0.7
                                     $("#ad_%s").on("click", function(){
                                      layer.open({
                                       type: 2,
                                       skin: "layui-layer-lan",
                                       title: "广告管理",
                                       fix: false,
                                       shadeClose: true,
                                       maxmin: true,
                                       area: ['1500px', '600px'],
                                       content: "/show_ads_detail",
                                       btn: ["关闭页面"],
                                       });
                                   })
                               </script>
                               ''' % (obj.id)
            rt += rt_script
        return mark_safe(rt)
    show_ads_info.short_description = mark_safe(u'<p style="color:#428BCA" align="center">广告数据</p>')

    def show_ad_remark(self, obj):
        v_remark = obj.ad_remark
        count = 0
        b = ''
        if v_remark:
            for i in v_remark:
                count += 1
                b += i
                if count % 10 == 0:
                    b += '<br>'
        return mark_safe(b)
    show_ad_remark.short_description = mark_safe(u'<p style="color:#428BCA" align="center">广告备注</p>')

    def show_operation_record(self, obj):
        v_remark = obj.operation_record
        count = 0
        b = ''
        if v_remark:
            for i in v_remark:
                count += 1
                b += i
                if count % 10 == 0:
                    b += '<br>'
        return mark_safe(b)
    show_operation_record.short_description = mark_safe(u'<p style="color:#428BCA;" align="center">操作记录</p>')

    def show_price_profit(self, obj):
        price_profit = u'%s/%s' %(obj.price, obj.profit_rate)
        return mark_safe(price_profit)
    show_price_profit.short_description = mark_safe(u'<p style="color:#428BCA" align="center">价格/利润率</p>')



    list_display = ('id', 'show_image_url','show_title',  'price','profit_rate', 'show_sales', 'show_is_fbm','show_fbm_quantity','if_fba', 'afn_warehouse_quantity','afn_fulfillable_quantity','afn_unsellable_quantity', 'afn_reserved_quantity','afn_total_quantity','afn_inbound_working_quantity','afn_inbound_shipped_quantity','afn_inbound_receiving_quantity', 'product_state', 'ad_remark', 'show_operation_record','RefreshTime')
    list_editable = ('ad_remark', 'product_state')

    form_layout = (
        Fieldset(u'基本信息',
                 Row('shop_name', 'seller_sku', 'asin', 'price'),
                 Row('create_date', 'on_sale_date'),
                 Row('score', 'review_cnt'),
                 Row('product_state', 'inventory'),
                 css_class='unsort '
                 ),
        Fieldset(u'广告信息',
                 Row('link_orders', 'ad_orders', ),
                 Row('link_sales', 'ad_sales'),
                 Row('expose_cnt', 'click_cnt'),
                 Row('ad_cost', ),
                 css_class='unsort  '
                 ),
        Fieldset(u'备注',
                 Row('sale_remark', ),
                 Row('ad_remark', ),
                 css_class='unsort '
                 )
    )

    def save_models(self):
        obj = self.new_obj
        request = self.request
        updateUser = request.user.username
        updateTime = datetime.datetime.now()

        if obj is None or obj.id is None or obj.id <= 0:
            pass
        else:
            old_obj = self.model.objects.get(pk=obj.pk)
            old_obj.operation_record = old_obj.operation_record + '\n' + '%s 于 %s 修改' %(updateUser, updateTime)
            old_obj.save()

    def get_list_queryset(self, ):
        request = self.request
        shop_name1 = request.GET.get('ShopName', '')
        shop_name2 = request.GET.get('shop_name', '')
        if shop_name1 and shop_name1 != '全部':
            shopname = shop_name1
        else:
            shopname = shop_name2

        searchSite = request.GET.get('searchSite', '')
        status = request.GET.get('Status', '')
        if status == 'ALL':
            status = ''
        SKU = request.GET.get('SKU', '')
        SKU = '' if SKU == '' else SKU.split(',')

        ASIN = request.GET.get('ASIN', '')
        ASIN = '' if ASIN == '' else ASIN.split(',')

        is_fba = request.GET.get('FBA', '')
        if is_fba == 'YES':
            is_fba = 1
        elif is_fba == 'NO':
            is_fba = 0
        else:
            is_fba = ''

        SKU = request.GET.get('SKU', '')
        SKU = '' if SKU == '' else SKU.strip().replace(' ', '+').split(',')

        product_sku = request.GET.get('product_sku', '')
        product_sku = '' if product_sku == '' else product_sku.strip().replace(' ', '+').split(',')
        # messages.success(request, 'sku is:%s' %SKU)
        ASIN = request.GET.get('ASIN', '')
        ASIN = '' if ASIN == '' else ASIN.split(',')

        afn_fulfillable_quantity_start = request.GET.get('afn_fulfillable_quantity_start', '')
        afn_fulfillable_quantity_end = request.GET.get('afn_fulfillable_quantity_end', '')
        afn_unsellable_quantity_start = request.GET.get('afn_unsellable_quantity_start', '')
        afn_reserved_quantity_start = request.GET.get('afn_reserved_quantity_start', '')
        afn_total_quantity_start = request.GET.get('afn_total_quantity_start', '')
        mfn_fulfillable_quantity_start = request.GET.get('mfn_fulfillable_quantity_start', '')
        afn_warehouse_quantity_start = request.GET.get('afn_warehouse_quantity_start', '')
        afn_unsellable_quantity_end = request.GET.get('afn_unsellable_quantity_end', '')
        afn_reserved_quantity_end = request.GET.get('afn_reserved_quantity_end', '')
        afn_total_quantity_end = request.GET.get('afn_total_quantity_end', '')
        mfn_fulfillable_quantity_end = request.GET.get('mfn_fulfillable_quantity_end', '')
        afn_warehouse_quantity_end = request.GET.get('afn_warehouse_quantity_end', '')

        orders_total_start = request.GET.get('orders_total_start', '')
        orders_total_end = request.GET.get('orders_total_end', '')

        qs = super(t_amazon_cpc_ad_Admin, self).get_list_queryset()
        qs = qs.filter(Status__in=('Active', 'Inactive'))
        searchList = {'shop_name__contains': shopname,
                      'shop_site__exact': searchSite,
                      'Status__exact': status,
                      'seller_sku__in':SKU,
                      'sku__in': product_sku,
                      'asin__in':ASIN,
                      'is_fba__exact': is_fba,

                      'afn_fulfillable_quantity__gte': afn_fulfillable_quantity_start,
                      'afn_fulfillable_quantity__lte': afn_fulfillable_quantity_end,

                      'afn_unsellable_quantity__gte': afn_unsellable_quantity_start,
                      'afn_unsellable_quantity__lte': afn_unsellable_quantity_end,

                      'afn_reserved_quantity__gte': afn_reserved_quantity_start,
                      'afn_reserved_quantity__lte': afn_reserved_quantity_end,

                      'afn_total_quantity__gte': afn_total_quantity_start,
                      'afn_total_quantity__lte': afn_total_quantity_end,

                      'quantity__gte': mfn_fulfillable_quantity_start,
                      'quantity__lte': mfn_fulfillable_quantity_end,

                      'afn_warehouse_quantity__gte': afn_warehouse_quantity_start,
                      'afn_warehouse_quantity__lte': afn_warehouse_quantity_end,

                      'orders_total__gte': orders_total_start,
                      'orders_total__lte': orders_total_end,
                      }
        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and str(v).strip() != '':
                    sl[k] = v
        if sl is not None:
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'Please enter the correct content!')
        return qs