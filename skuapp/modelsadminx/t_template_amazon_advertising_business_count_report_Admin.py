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
 @file: t_template_amazon_advertising_business_count_report_Admin.py
 @time: 2018/8/21 10:37
"""
#点击率=点击量/曝光量     点击成本=花费/点击量   ACOS=花费/销售额， AT=订单数/已订购商品数量   AS=花费/链接销售额
class t_template_amazon_advertising_business_count_report_Admin(object):
    site_left_menu_tree_amazon_advertising_flag = True
    amazon_shop_search_flag = True
    search_box_flag = True

    actions = ['to_Continuous_ad', 'to_Stoping_ad']

    def check_time_info(self,obj):
        over_flag = 0
        start_date_str = obj.start_date.strftime('%Y-%m-%d')
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        now_date_str = datetime.now().strftime('%Y-%m-%d')
        now_date = datetime.strptime(now_date_str, '%Y-%m-%d')
        num = (now_date - start_date).days
        if num > 15:
            over_flag = 1
        return over_flag


    def show_main_info(self,obj):
        """展示产品详情信息"""
        site_url_dict = {'US': 'https://www.amazon.com/',
                         'UK': 'https://www.amazon.co.uk/',
                         'JP': 'https://www.amazon.co.jp/',
                         'DE': 'https://www.amazon.de/',
                         'FR': 'https://www.amazon.fr/',
                         'AU': 'https://www.amazon.com.au/',
                         'IN': 'https://www.amazon.in/'}
        shop_site = obj.shopname.split('-')[-1].split('/')[0]
        if shop_site and shop_site in site_url_dict:
            site_url = site_url_dict[shop_site]
        else:
            site_url = 'https://www.amazon.com/'

        over_flag = self.check_time_info(obj)
        font_style = ''
        if over_flag == 1:
            font_style = 'style="color:red"'
        rt = u'产品ASIN(父):<a href="%sdp/%s" target="_blank">%s</a><br>广告名称:%s<br>店铺SKU/ASIN:%s<br><span %s>广告开始时间:%s</span><br>店铺名称:%s' \
             % (site_url, obj.parent_ASIN, obj.parent_ASIN, obj.advertising_campaign_name, obj.ShopSKU, font_style, obj.start_date, obj.shopname)
        rt = u'%s<br/><input type="button" value="修改广告名称" onclick="change_ad_title(\'%s\',\'%s\')">'%(rt, obj.id, obj.shopname)
        return mark_safe(rt)

    show_main_info.short_description = u'<p style="width:40px;color:#428bca;" align="center">详情</p>'

    def show_image(self, obj):
        """展示产品图片信息"""
        rt = '<img id="image_click_%s" src="%s" style="width: 100px; height: 100px">' % (obj.id, obj.image_url)
        return mark_safe(rt)

    show_image.short_description = u'<p style="width:40px;color:#428bca;" align="center">图片</p>'

    def show_status(self, obj):
        """展示产品状态信息"""
        rt = ''
        if obj.advertising_status == 'PAUSED':
            rt = u'暂停'
        if obj.advertising_status == 'ENABLED':
            rt = u'启用'
        return mark_safe(rt)

    show_status.short_description = u'<p style="width:40px;color:#428bca;" align="center">状态</p>'

    def check_ad_info(self,obj):
        request_path = self.request.GET.get('_p_advertising_online_status', '')
        check_result = 0
        if request_path == 'Selection_ad':
            check_result = 1
            if float(obj.AS_amazon) > 15:
                check_result = -1
        return check_result


    def show_advertising_info(self,obj):
        """展示广告信息"""
        rt = u'<table class="table table-condensed">' \
             u'<thead><tr><th>预算</th>' \
             u'<th>曝光量</th><th>点击量</th>' \
             u'<th>点击率(%)</th><th>花费($)</th><th>点击成本($)</th><th>订单数</th><th>销售额($)</th><th>ACOS(%)</th>' \
             u'</tr>' \
             u'</thead><tbody>'
        check_result = self.check_ad_info(obj)
        style = ''
        if check_result == 1:
            style = 'class ="success"'  # 正常  Disabled 为 绿色
        if check_result == -1:
            style = 'class ="danger"'  # 非正常为红色
        rt = u'%s <tr %s><td>%s</td><td>%s</td>' \
             u'<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'%\
             (rt, style, obj.CNY, obj.display_count, obj.click_count, obj.CTR, obj.cost, obj.CPC, obj.orders_count, obj.sales_count, obj.ACoS)
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
        check_result = self.check_ad_info(obj)
        style = ''
        if check_result == 1:
            style = 'class ="success"'  # 正常  Disabled 为 绿色
        if check_result == -1:
            style = 'class ="danger"'  # 非正常为红色
        rt = u'%s<tr %s><td>%s</td><td>%s</td>' \
             u'<td>%s</td><td>%s</td></tr>' % \
             (rt, style, obj.visit_count, obj.ordered_count, obj.ordered_sales, obj.ordered_count_Conversion_rate)
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
        import urllib
        keyword_url = u'/Project/admin/skuapp/t_template_amazon_advertising_keywords_report/?shopname=%s&' \
                      u'advertising_campaign_name=%s'%(obj.shopname,urllib.quote(obj.advertising_campaign_name.encode('utf8')))

        rt = u'/Project/admin/skuapp/t_template_amazon_advertising_business_report/?_p_ShopSKU=%s&_p_shopname=%s' \
             u'&is_single=1&datatype=day&pdate_Start=%s'%(urllib.quote(obj.ShopSKU.encode('utf8')),
                                                                       obj.shopname,obj.advertising_business_date)
        if obj.advertising_online_status == 'Stoping_ad' and obj.action_time:
            rt = u'%s&uploadtime_End=%s'%(rt,obj.action_time)
        rt = u'<a href="%s" title="展示该广告所有历史数据">广告历史详情</a>' \
             u'<br/><br/><br/><a href="%s" title="展示该广告所有关键词数据">关键词详情</a>' % (rt,keyword_url)
        return mark_safe(rt)
    href_advertising.short_description = u'<p style="color:#428bca;" align="center">广告历史详情</p>'

    def show_remark(self, obj):
        text_value = ''
        if obj.remark:
            text_values = obj.remark.split('\r\n')
            if len(text_values) > 1:
                text_value = text_values[-2].split(':')[-1]
        rt = u'<textarea style="width:100%;border:none;background-color:transparent" rows="6" id="edit_remark_'+str(obj.id)+u'" title="">'+text_value + '\r\n'+u'</textarea>'
        rt += u'<br/><input id="edit_remark_bt_%s" type="button" value="保存" onclick="edit_remark(%s,this.id)">' \
              u'<input id="show_remark_bt_%s" type="button" value="详情" onclick="show_remark(%s,this.id)">'%(obj.id,obj.id,obj.id,obj.id)
        return mark_safe(rt)
    show_remark.short_description = u'<p style="width:40px;color:#428bca;" align="center">备注</p>'

    def show_action_remark(self, obj):
        text_value = ''
        if obj.action_remark:
            text_values = obj.action_remark.split('\r\n')
            if len(text_values) > 1:
                text_value = text_values[-2].split(':')[-1]
        rt = u'<textarea style="width:100%;border:none;background-color:transparent" rows="6" id="edit_action_remark_'+str(obj.id)+u'" title="">'+text_value + '\r\n'+u'</textarea>'
        rt += u'<br/><input id="edit_action_remark_bt_%s" type="button" value="保存" onclick="edit_action_remark(%s,this.id)">' \
              u'<input id="show_action_remark_bt_%s" type="button" value="详情" onclick="show_action_remark(%s,this.id)">'%(obj.id,obj.id,obj.id,obj.id)
        return mark_safe(rt)
    show_action_remark.short_description = u'<p style="width:40px;color:#428bca;" align="center">操作备注</p>'

    list_display = ('show_image', 'show_main_info', 'show_status', 'show_advertising_info', 'show_business_info',
                    'AT_amazon', 'AS_amazon', 'show_action_remark', 'show_remark', 'href_advertising')

    list_display_links = ('id',)

    # list_editable = ('action_remark', 'remark')

    fields = ('upload_advertising_file', 'upload_business_file', 'shopname', 'advertising_business_date')


    def to_Continuous_ad(self, request, queryset):
        for obj in queryset:
            if obj:
                t_template_amazon_advertising_business_count_report.objects.filter(id=obj.id).update(
                    advertising_online_status='Continuous_ad',update_user=request.user.first_name,
                    update_time=datetime.now(),action_time=datetime.now())

    to_Continuous_ad.short_description = u'移到连续广告'

    def to_Stoping_ad(self, request, queryset):
        for obj in queryset:
            if obj:
                t_template_amazon_advertising_business_count_report.objects.filter(id=obj.id).update(
                    advertising_online_status='Stoping_ad',advertising_status='PAUSED',update_user=request.user.first_name,
                    update_time=datetime.now(),action_time=datetime.now())

    to_Stoping_ad.short_description = u'停止广告'


    def get_list_queryset(self, ):
        request = self.request
        qs = super(t_template_amazon_advertising_business_count_report_Admin, self).get_list_queryset()

        shopname = request.GET.get('shopname', '')
        ShopSKU = request.GET.get('ShopSKU', '')
        parent_ASIN = request.GET.get('parent_ASIN', '')
        item_name = request.GET.get('item_name', '')
        pdate_Start = request.GET.get('pdate_Start', '')
        pdate_End = request.GET.get('pdate_End', '')
        ad_status = request.GET.get('ad_status', '')

        searchList = {'shopname__icontains': shopname,
                      'ShopSKU__contains': ShopSKU,
                      'advertising_status__exact': ad_status,
                      'advertising_campaign_name__icontains': item_name,
                      'parent_ASIN__icontains': parent_ASIN,
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