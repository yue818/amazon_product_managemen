# -*- coding: utf-8 -*-
"""
 @desc:joom营销留评效果跟踪，填写的店铺和sku以及产品id，刊登时间、营销时间、留评时间，几个要素，读出自刊登日后的日销量情况，并标注营销时间和留评时间
 @author: wangzhiyang
 @site:
 @software: PyCharm
 @file: t_marketing_revied_trace_Admin.py
 @time: 2018/5/29 8:53
"""
from .t_product_Admin import *
from django.contrib import messages
from skuapp.table.t_marketing_review_trace import t_marketing_review_trace
from django.utils.safestring import mark_safe
from datetime import datetime as LRDatetime
from brick.pricelist.calculate_price import calculate_price as joom_calculate_price
from django.db.models import Q

class t_marketing_review_trace_Admin(object):

    search_box_flag = True
    importfile_marketing = True
    def SalesTrend(self, obj):
        try:
            rt = u"<a id=SalesTrend%s>商品日订单量趋势</a><script>$('#SalesTrend%s').on('click',function(){layer.open(" \
                 u"{type:2,skin:'layui-layer-lan',title:'日订单量趋势',fix:false,shadeClose: true,maxmin:true," \
                 u"area:['1200px','800px'],content:'/sales_trend/?SKU=%s&ProductID=%s&SKUType=%s&MarketingTime=%s&ReviewTime=%s'});});</script>" % (
                obj.Id, obj.Id, obj.SKU,obj.ProductID,obj.SKUType,(str(obj.MarketingTime)[:10]).replace('-',''),(str(obj.ReviewTime)[:10]).replace('-',''))
        except Exception as e:
            messages.info(self.request, u'日销量趋势字段显示存在问题，请联系开发人员查看。')
        return mark_safe(rt)
    SalesTrend.short_description = mark_safe(u'<p style="width:100px;color:#428bca;" align="center">日订单量趋势</p>')

    def myInfo(self,obj):
        try:
            rt = u'零利润价格	:%s<br>初步定价:%s-%s<br>利润率:%s' % (
                obj.ZeroProfitPrice, obj.PrePrice,obj.MaxPrePrice, obj.ProfitPrice)
        except Exception as e:
            messages.info(self.request, u'获取我方信息出错，，请联系开发人员查看。')
        return mark_safe(rt)
    myInfo.short_description = mark_safe(u'<p style="width:120px;color:#428bca;" align="center">我方信息</p>')

    def opInfo(self,obj):
        try:
            rt = u'对手价格:%s<br>对手利润率:%s' % (
                obj.OpPrice, obj.OpProfitPrice)
        except Exception as e:
            messages.info(self.request, u'获取对手信息出错，，请联系开发人员查看。')
        return mark_safe(rt)
    opInfo.short_description = mark_safe(u'<p style="width:120px;color:#428bca;" align="center">对手信息</p>')

    def ReverseLinkInfo(self,obj):
        try:
            rt = u'<a href="%s" target="_blank">%s</a>' % (obj.ReverseLink, obj.ReverseLink)
        except Exception as e:
            messages.info(self.request, u'获取反向链接出错，，请联系开发人员查看。')
        return mark_safe(rt)
    ReverseLinkInfo.short_description = mark_safe(u'<p style="width:100px;color:#428bca;" align="center">反向链接</p>')

    def ProductIDLinkInfo(self,obj):
        try:
            rt = u'<a href="https://www.joom.com/en/products/%s" target="_blank">%s</a>' % (obj.ProductID, obj.ProductID)
        except Exception as e:
            messages.info(self.request, u'获取产品ID出错，，请联系开发人员查看。')
        return mark_safe(rt)
    ProductIDLinkInfo.short_description = mark_safe(u'<p style="width:100px;color:#428bca;" align="center">产品ID</p>')

    def showSKUPriceChange(self,obj):
        try:
            rt = ''
            rt = u'<table class="table table-condensed" style="text-align:center;">' \
                 u'<tr bgcolor="#C00">' \
                 u'<th style="text-align:center;">商品SKU</th>' \
                 u'<th style="text-align:center;">店铺SKU</th>' \
                 u'<th style="text-align:center;">老价格($)</th>' \
                 u'<th style="text-align:center;">新价格($)</th>' \
                 u'<th style="text-align:center;">变化时间</th>' \
                 u'</tr>'
            from joom_app.table.t_online_info_joom_detail import t_online_info_joom_detail
            from joom_app.table.t_joom_price_parity_log import t_joom_price_parity_log
            t_online_info_joom_detail_objs = t_online_info_joom_detail.objects.filter(PlatformName='Joom',MainSKU=obj.SKU,ProductID=obj.ProductID,Status='True').values_list('SKU','ShopSKU','Price','RefreshTime')
            flag = 0
            for obj_01 in t_online_info_joom_detail_objs:
                flag = 1
                t_joom_price_parity_log_objs = t_joom_price_parity_log.objects.filter(ProductID=obj.ProductID,ShopSKU=obj_01[1],ChangeFlag='True').values_list('OldPrice','NewPrice','ChangePriceDatetime')
                for obj_02 in t_joom_price_parity_log_objs:
                    flag = 2
                    rt = '%s <tr bgcolor="#FFFFFF"><td>%s</td><td>%s</td><td>%0.2f</td><td>%0.2f</td><td>%s</td></tr>' % (rt, obj_01[0], obj_01[1], float(obj_02[0]), float(obj_02[1]), str(obj_02[2])[:11])
            if flag == 1:
                rt = '%s <tr bgcolor="#FFFFFF"><td>%s</td><td>%s</td><td>%s</td><td>%0.2f</td><td>%s</td></tr>' % (rt, obj_01[0], obj_01[1], '', float(obj_01[2]), str(obj_01[3])[:11])
            rt = "%s</table>"%(rt)
        except Exception as e:
            messages.info(self.request, u'价格显示报错，请联系开发人员。%s' % (str(e)))
            rt = ''
        return mark_safe(rt)
    showSKUPriceChange.short_description = mark_safe(u'<p style="width:160px;color:#428bca;" align="center">商品价格变化</p>')

    list_display = (
        'SKU','ProductIDLinkInfo','ShopName','DYDate','PublishDate','EnKeys','myInfo',
        'opInfo','ReverseLinkInfo','MarketingTime','ReviewTime','showSKUPriceChange','SalesTrend',)

    list_per_page = 20  # 页面显示数量
    # 分组表单
    fields = ('SKU','ProductID','ShopName','DYDate','PublishDate','EnKeys',
            'PrePrice','MaxPrePrice','ReverseLink','MarketingTime','ReviewTime', 'SKUType',
              )
    list_filter = ()
    search_fields = ()
    form_layout = (
        Fieldset(u'调研跟踪SKU',
                 Row('SKUType','SKU', 'ProductID'),
                 Row('ShopName', 'PublishDate', 'DYDate'),
                 Row('PrePrice','MaxPrePrice',''),
                 css_class='unsort '
                 ),
        Fieldset(u'其他',
                 Row('EnKeys', 'ReverseLink', ''),
                 Row('MarketingTime', 'ReviewTime', ''),
                 css_class='unsort'
                 ),
    )
    list_editable = ('MarketingTime','ReviewTime')

    def save_models(self):
        try:
            obj = self.new_obj
            newdata = obj.__dict__
            #messages.info(self.request,newdata)
            if newdata['ProductID'].strip() == '':
                messages.info(self.request, u'productID 不能为空值')
                return

            # 通过我方ProductID获取对手价格、对手利润率、对手上架时间（页面抓取不到）、评论页面也抓取不到
            # JOOM 取7天销量最好的商品（如果有多个店铺销售同一个商品，取一个7天销量最好的主SKU）
            #t_online_info_joom表中的productID属于我方，competitor_ProductID属于对手方（在t_joom_competitor_product_info中查找对手信息）
            from joom_app.table.t_online_info_joom import t_online_info_joom
            from joom_app.table.t_joom_price_parity_log import t_joom_price_parity_log
            from joom_app.table.t_joom_competitor_product_info import t_joom_competitor_product_info
            strOpPrice = "0-0"
            strOpProfitRate = "0.0%-0.0%"
            CurrentPrice = newdata['PrePrice']
            list_t_online_info_objs = t_online_info_joom.objects.filter(ProductID=newdata['ProductID'].strip()).values_list('MainSKU',flat=True)
            if len(list_t_online_info_objs) > 0:
                mainSKU = list_t_online_info_objs[0]
                list_t_online_info_objs1 = t_online_info_joom.objects.filter(MainSKU=mainSKU).filter(~Q(competitor_ProductID = None)).order_by('-Orders7Days').values_list('competitor_ProductID', flat=True)
                if len(list_t_online_info_objs1) > 0:
                    list_t_joom_competitor_product_info_objs = t_joom_competitor_product_info.objects.filter(ProductID=list_t_online_info_objs1[0].strip())
                    if len(list_t_joom_competitor_product_info_objs) > 0:
                        strOpPrice = str(list_t_joom_competitor_product_info_objs[0].minPrice) + "-" + str(list_t_joom_competitor_product_info_objs[0].maxPrice)
                        strOpProfitRate = str(list_t_joom_competitor_product_info_objs[0].minProfitRate) + '%-' + str(list_t_joom_competitor_product_info_objs[0].maxProfitRate) + '%'
            list_t_joom_price_parity_log_objs = t_joom_price_parity_log.objects.filter(ProductID=newdata['ProductID'].strip()).order_by('-ChangePriceDatetime')
            if len(list_t_joom_price_parity_log_objs) > 0:
                CurrentPrice = list_t_joom_price_parity_log_objs[0].NewPrice
            obj.zeroSellingPrice = 0.0
            obj.ProfitPrice = '0.0%'
            if obj.SKUType == 'productsku':
                try:
                    # 通过SKU获取零利润价格、利润率
                    calculate_price_obj = joom_calculate_price(str(newdata['SKU']))
                    sellingPrice_info = calculate_price_obj.calculate_selling_price(0)
                    obj.zeroSellingPrice = float(sellingPrice_info['sellingPrice_us'])
                    profitRateMin_info = calculate_price_obj.calculate_profitRate(newdata['PrePrice'])
                    profitRateMax_info = calculate_price_obj.calculate_profitRate(newdata['MaxPrePrice'])
                    obj.ProfitPrice = str(float(profitRateMin_info['profitRate'])) + '%-' + str(float(profitRateMax_info['profitRate'])) +'%'
                except Exception as e:
                    messages.info(self.request, u'productsku=%s,获取零利润价格存有问题(%s)，请联系开发人员。' % (newdata['SKU'],str(e)))
                    return
            else:
                #主SKU类型，需要关联
                from skuapp.table.t_product_mainsku_sku import t_product_mainsku_sku
                listSKU = t_product_mainsku_sku.objects.filter(MainSKU=obj.SKU).values_list('ProductSKU',flat=True)
                insertinto = []
                if len(listSKU) == 0:
                    messages.info(self.request, u'主SKU(%s)未查找到对应商品SKU。' % (obj.SKU))
                    return
                for subSKU in listSKU:
                    try:
                        #通过SKU获取零利润价格、利润率
                        calculate_price_obj = joom_calculate_price(str(subSKU))
                        sellingPrice_info = calculate_price_obj.calculate_selling_price(0)
                        zeroSellingPrice = sellingPrice_info['sellingPrice_us']
                        profitRateMin_info = calculate_price_obj.calculate_profitRate(newdata['PrePrice'])
                        profitRateMax_info = calculate_price_obj.calculate_profitRate(newdata['MaxPrePrice'])
                        obj.ProfitPrice = str(float(profitRateMin_info['profitRate'])) + '%-' + str(float(profitRateMax_info['profitRate'])) + '%'
                        break
                    except Exception as e:
                        messages.info(self.request, u'mainsku=%s,获取零利润价格存有问题(%s)，请联系开发人员。' % (newdata['SKU'],str(e)))
                        return
            obj.OpPrice = strOpPrice
            obj.OpProfitPrice = strOpProfitRate
            obj.CurrentPrice = CurrentPrice
            obj.save()
        except Exception as e:
            messages.info(self.request, u'保存错误，请联系开发人员。%s'%(str(e)))
            return

    def get_list_queryset(self):
        request = self.request
        qs = super(t_marketing_review_trace_Admin, self).get_list_queryset()

        SKU = request.GET.get('SKU', '')
        ProductID = request.GET.get('ProductID', '')
        ShopName = request.GET.get('ShopName', '')
        EnKeys = request.GET.get('EnKeys', '')
        DYDateStart = request.GET.get('DYDateStart', '')
        DYDateEnd = request.GET.get('DYDateEnd', '')
        PublishDateStart = request.GET.get('PublishDateStart', '')
        PublishDateEnd = request.GET.get('PublishDateEnd', '')
        MarketingTimeStart = request.GET.get('MarketingTimeStart', '')
        MarketingTimeEnd = request.GET.get('MarketingTimeEnd', '')
        ReviewTimeStart = request.GET.get('ReviewTimeStart', '')
        ReviewTimeEnd = request.GET.get('ReviewTimeEnd', '')

        searchList = {'SKU__contains': SKU,
                      'EnKeys__contains': EnKeys,
                      'ProductID__exact': ProductID,
                      'ShopName__exact': ShopName,
                      'DYDate__gte': DYDateStart,
                      'DYDate__lt': DYDateEnd,
                      'PublishDate__gte': PublishDateStart,
                      'PublishDate__lt': PublishDateEnd,
                      'MarketingTime__gte': MarketingTimeStart,
                      'MarketingTime__lt': MarketingTimeEnd,
                      'ReviewTime__gte': ReviewTimeStart,
                      'ReviewTime__lt': ReviewTimeEnd,
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