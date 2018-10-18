#-*-coding:utf-8-*-
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from django.utils.safestring import mark_safe
from django.contrib import messages
from datetime import datetime
import csv
import decimal
from skuapp.table.t_template_amazon_advertising_business_report import t_template_amazon_advertising_business_report
from skuapp.table.t_online_info_amazon import t_online_info_amazon
from skuapp.table.t_template_amazon_advertising_report import t_template_amazon_advertising_report
from skuapp.table.t_template_amazon_business_report import t_template_amazon_business_report
from skuapp.table.t_template_amazon_advertising_business_count_report import t_template_amazon_advertising_business_count_report

"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_template_amazon_advertising_business_count_shop_report_Admin.py
 @time: 2018/8/21 10:37
"""
#点击率=点击量/曝光量     点击成本=花费/点击量   ACOS=花费/销售额， AT=订单数/已订购商品数量   AS=花费/链接销售额
class t_template_amazon_advertising_business_count_shop_report_Admin(object):
    site_left_menu_tree_amazon_advertising_flag = True
    amazon_shop_search_flag = True

    # def show_main_info(self,obj):
    #     """展示产品详情信息"""
    #     rt = u'店铺名称:%s<br>汇总日期:%s' \
    #          % (obj.shopname,obj.advertising_business_date)
    #     return mark_safe(rt)
    #
    # show_main_info.short_description = u'<p style="width:40px;color:#428bca;" align="center">详情</p>'

    def show_advertising_info(self,obj):
        """展示广告信息"""
        rt = u'<table class="table table-condensed">' \
             u'<thead><tr><th>预算</th>' \
             u'<th>曝光量</th><th>点击量</th>' \
             u'<th>点击率(%)</th><th>花费($)</th><th>点击成本($)</th><th>订单数</th><th>销售额($)</th><th>ACOS(%)</th>' \
             u'</tr>' \
             u'</thead><tbody>'
        rt = u'%s <tr><td>%s</td><td>%s</td>' \
             u'<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'%\
             (rt, obj.CNY, obj.display_count, obj.click_count, obj.CTR, obj.cost, obj.CPC, obj.orders_count, obj.sales_count, obj.ACoS)
        # if obj.advertising_more != '0':
        #     advertising_reports = t_template_amazon_advertising_report.objects.filter(shopname__exact=obj.shopname,ShopSKU__exact=obj.ShopSKU)
        #     for advertising_report in advertising_reports:
        #         if advertising_report:
        #             temp1 = u'自'
        #             if advertising_report.serving == 'MANUAL':
        #                 temp1 = u'手'
        #             rt = u'%s <tr><td>%s</td><td>%s</td><td>%s</td>' \
        #                 u'<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'%\
        #                 (rt, temp1, advertising_report.CNY, advertising_report.display_count, advertising_report.click_count, advertising_report.CTR,
        #                  advertising_report.cost, advertising_report.CPC, advertising_report.orders_count, advertising_report.sales_count, advertising_report.ACoS)

        rt = u'%s</tbody></table>'%rt
        return mark_safe(rt)

    show_advertising_info.short_description = u'<p style="width:40px;color:#428bca;" align="center">广告详情</p>'

    def show_business_info(self,obj):
        """展示业务信息"""
        rt = u'<table class="table table-condensed">' \
             u'<thead><tr><th>访问量</th>' \
             u'<th>订购量</th><th>销售额($)</th>' \
             u'<th>转化率(%)</th>' \
             u'</tr>' \
             u'</thead><tbody>'
        rt = u'%s<tr><td>%s</td><td>%s</td>' \
             u'<td>%s</td><td>%s</td></tr>' % \
             (rt, obj.visit_count, obj.ordered_count, obj.ordered_sales, obj.ordered_count_Conversion_rate)
        # if obj.business_more != '0':
        #     business_reports = t_template_amazon_business_report.objects.filter(shopname__exact=obj.shopname,parent_ASIN__exact=obj.parent_ASIN)
        #     for business_report in business_reports:
        #         if business_report:
        #             rt = u'%s<tr><td>%s</td><td>%s</td><td>%s</td>' \
        #                 u'<td>%s</td><td>%s</td></tr>'%\
        #                  (rt, business_report.child_ASIN, business_report.visit_count, business_report.ordered_count, business_report.ordered_sales, business_report.ordered_count_Conversion_rate)

        rt = u'%s</tbody></table>'%rt
        return mark_safe(rt)

    show_business_info.short_description = u'<p style="width:40px;color:#428bca;" align="center">业务详情</p>'

    def href_advertising(self, obj):
        rt = u'/Project/admin/skuapp/t_template_amazon_advertising_business_daily_report/?_p_shopname=%s&is_viewed=1&datatype=day'%(obj.shopname)
        rt = u'<a href="%s" title="展示该店铺所有日统计历史数据">日统计历史详情</a>' % rt
        return mark_safe(rt)
    href_advertising.short_description = u'<p style="width:40px;color:#428bca;" align="center">日统计历史详情</p>'

    list_display = ('shopname', 'show_advertising_info', 'show_business_info',
                    'AT_amazon', 'AS_amazon', 'action_remark', 'remark', 'href_advertising')

    list_display_links = ('id',)

    list_editable = ('action_remark', 'remark')

    # fields = ('upload_advertising_file', 'upload_business_file', 'shopname', 'advertising_business_date')

    def get_list_queryset(self, ):
        request = self.request
        qs = super(t_template_amazon_advertising_business_count_shop_report_Admin, self).get_list_queryset()

        shopname = request.GET.get('shopname', '')
        if shopname == '':
            shopname = request.GET.get('shopname', '')
        pdate_Start = request.GET.get('pdate_Start', '')
        pdate_End = request.GET.get('pdate_End', '')

        searchList = {'shopname__icontains': shopname,
                      'advertising_business_date__gte': pdate_Start,
                      'advertising_business_date__lt': pdate_End,
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