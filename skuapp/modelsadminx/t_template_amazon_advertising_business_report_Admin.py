#-*-coding:utf-8-*-
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from django.utils.safestring import mark_safe
from django.contrib import messages
from datetime import datetime
import csv
import decimal,chardet
from skuapp.table.t_template_amazon_advertising_business_report import t_template_amazon_advertising_business_report
from skuapp.table.t_online_info_amazon import t_online_info_amazon
from skuapp.table.t_template_amazon_advertising_report import t_template_amazon_advertising_report
from skuapp.table.t_template_amazon_business_report import t_template_amazon_business_report
from skuapp.table.t_template_amazon_advertising_business_count_report import t_template_amazon_advertising_business_count_report
from skuapp.table.t_template_amazon_advertising_business_daily_report import t_template_amazon_advertising_business_daily_report
from skuapp.table.t_template_amazon_advertising_business_count_shop_report import t_template_amazon_advertising_business_count_shop_report

"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_template_amazon_advertising_business_report_Admin.py
 @time: 2018/8/21 10:37
"""
#点击率=点击量/曝光量     点击成本=花费/点击量   ACOS=花费/销售额， AT=订单数/已订购商品数量   AS=花费/链接销售额
class t_template_amazon_advertising_business_report_Admin(object):
    site_left_menu_tree_amazon_advertising_flag = True
    amazon_advertising_report_flag = True
    amazon_shop_search_flag = True
    search_box_flag = True

    def show_main_info(self,obj):
        """展示产品详情信息"""
        rt = u'产品ASIN(父):%s<br>广告名称:%s<br>店铺SKU/ASIN:%s<br>广告开始时间:%s<br>店铺名称:%s<br>业务广告时间:%s' \
             % (obj.parent_ASIN, obj.advertising_campaign_name, obj.ShopSKU, obj.start_date, obj.shopname, obj.advertising_business_date)
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

    def show_advertising_info(self,obj):
        """展示广告信息"""
        rt = u'<table class="table table-condensed">' \
             u'<thead><tr><th></th><th>预算</th>' \
             u'<th>曝光量</th><th>点击量</th>' \
             u'<th>点击率(%)</th><th>花费($)</th><th>点击成本($)</th><th>订单数</th><th>销售额($)</th><th>ACOS(%)</th>' \
             u'</tr>' \
             u'</thead><tbody>'
        rt = u'%s <tr><td>总</td><td>%s</td><td>%s</td>' \
             u'<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'%\
             (rt, obj.CNY, obj.display_count, obj.click_count, obj.CTR, obj.cost, obj.CPC, obj.orders_count, obj.sales_count, obj.ACoS)
        # if obj.advertising_more != '0':
        advertising_reports = t_template_amazon_advertising_report.objects.filter(shopname__exact=obj.shopname,
                                                                                  ShopSKU__iexact=obj.ShopSKU,
                                                                                  advertising_data__exact=obj.advertising_business_date)
        for advertising_report in advertising_reports:
            if advertising_report:
                temp1 = u'自'
                if advertising_report.serving == 'MANUAL':
                    temp1 = u'手'
                rt = u'%s <tr><td>%s</td><td>%s</td><td>%s</td>' \
                    u'<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'%\
                    (rt, temp1, advertising_report.CNY, advertising_report.display_count, advertising_report.click_count, advertising_report.CTR,
                     advertising_report.cost, advertising_report.CPC, advertising_report.orders_count, advertising_report.sales_count, advertising_report.ACoS)

        rt = u'%s</tbody></table>'%rt
        return mark_safe(rt)

    show_advertising_info.short_description = u'<p style="width:40px;color:#428bca;" align="center">广告详情</p>'

    def show_business_info(self,obj):
        """展示业务信息"""
        rt = u'<table class="table table-condensed">' \
             u'<thead><tr><th></th><th>访问量</th>' \
             u'<th>订购量</th><th>销售额($)</th>' \
             u'<th>转化率(%)</th>' \
             u'</tr>' \
             u'</thead><tbody>'
        rt = u'%s<tr><td>总</td><td>%s</td><td>%s</td>' \
             u'<td>%s</td><td>%s</td></tr>' % \
             (rt, obj.visit_count, obj.ordered_count, obj.ordered_sales, obj.ordered_count_Conversion_rate)
        if obj.business_more != '0':
            business_reports = t_template_amazon_business_report.objects.filter(shopname__exact=obj.shopname,
                                                                                parent_ASIN__exact=obj.parent_ASIN,
                                                                                business_date__exact=obj.advertising_business_date)
            new_rt = rt
            for business_report in business_reports[0:4]:
                if business_report:
                    rt = u'%s<tr><td>%s</td><td>%s</td><td>%s</td>' \
                        u'<td>%s</td><td>%s</td></tr>'%\
                         (rt, business_report.ShopSKU, business_report.visit_count, business_report.ordered_count, business_report.ordered_sales, business_report.ordered_count_Conversion_rate)

            if len(business_reports) > 4:
                for business_report in business_reports:
                    if business_report:
                        new_rt = u'%s<tr><td>%s</td><td>%s</td><td>%s</td>' \
                             u'<td>%s</td><td>%s</td></tr>' % \
                             (new_rt, business_report.ShopSKU, business_report.visit_count, business_report.ordered_count,
                              business_report.ordered_sales, business_report.ordered_count_Conversion_rate)
                new_rt = u'%s</tbody></table>' % new_rt
                rt += u'<tr><td><a id="more_id_%s">更多</a></td></tr></tbody></table>' % obj.id
                rt = u"%s<script>$('#more_id_%s').on('click',function(){" \
                     u"layer.open({type: 1,skin:'layui-layer-lan',title: '%s业务详情',fix:false," \
                     u"shadeClose: true,maxmin: true,area: ['893px', '600px'],content: '%s',btn: ['关闭页面']," \
                     u"yes: function(index){layer.close(index);},cancel: function(){},end:function (){}});})</script>" % (rt, obj.id, obj.ShopSKU,new_rt)
            else:
                rt = u'%s</tbody></table>' % rt
        else:
            rt = u'%s</tbody></table>'%rt
        return mark_safe(rt)

    show_business_info.short_description = u'<p style="width:40px;color:#428bca;" align="center">业务详情</p>'

    list_display = ('show_image', 'show_main_info', 'show_status', 'show_advertising_info', 'show_business_info',
                    'AT_amazon', 'AS_amazon', 'action_remark', 'remark',)

    list_display_links = ('id',)

    list_editable = ('action_remark', 'remark')

    fields = ('upload_advertising_file', 'upload_business_file', 'shopname', 'advertising_business_date')


    def caculate_all_and_insert(self, shopname, insert_date, upload_time):
        user_name = self.request.user.first_name
        advertising_business_reports = t_template_amazon_advertising_business_report.objects.filter(shopname__exact=shopname,advertising_business_date__exact=insert_date)
        advertising_business_report_list = []
        for advertising_business_report in advertising_business_reports:
            if advertising_business_report:
                advertising_business_report_dict = advertising_business_report.__dict__
                advertising_business_report_list.append(advertising_business_report_dict)
        advertising_business_count_reports = t_template_amazon_advertising_business_count_report.objects.filter(shopname__exact=shopname)
        advertising_business_count_report_dict1 = {}
        advertising_business_count_name_report_list = []
        advertising_business_count_name_report_status_dict = {}
        for advertising_business_count_report in advertising_business_count_reports:
            if advertising_business_count_report:
                advertising_business_count_report_dict = advertising_business_count_report.__dict__
                if advertising_business_count_name_report_status_dict.has_key(
                        advertising_business_count_report_dict['ShopSKU'].upper()) and advertising_business_count_name_report_status_dict[
                    advertising_business_count_report_dict['ShopSKU'].upper()] != 'Stoping_ad':
                    pass
                else:
                    advertising_business_count_report_dict1[advertising_business_count_report_dict[
                        'ShopSKU'].upper()] = advertising_business_count_report_dict
                    advertising_business_count_name_report_status_dict[advertising_business_count_report_dict['ShopSKU'].upper()] = advertising_business_count_report_dict['advertising_online_status']
                    advertising_business_count_name_report_list.append(advertising_business_count_report_dict['ShopSKU'].upper())

        CNY_daily = 0
        display_count_daily = 0
        click_count_daily = 0
        cost_daily = decimal.Decimal("%.2f" % float(0.00))
        orders_count_daily = 0
        sales_count_daily = decimal.Decimal("%.2f" % float(0.00))
        visit_count_daily = 0
        ordered_count_daily = 0
        ordered_sales_daily = decimal.Decimal("%.2f" % float(0.00))
        advertising_business_date_daily = None

        for advertising_business_report_each in advertising_business_report_list:
            advertising_business_date_daily = advertising_business_report_each['advertising_business_date']
            is_new = 0
            if advertising_business_report_each['ShopSKU'].upper() in advertising_business_count_name_report_list:
                if advertising_business_count_name_report_status_dict[advertising_business_report_each['ShopSKU'].upper()] != 'Stoping_ad':
                    abc_dict = advertising_business_count_report_dict1[advertising_business_report_each['ShopSKU'].upper()]
                    CNY = abc_dict['CNY'] + advertising_business_report_each['CNY']
                    display_count = abc_dict['display_count'] + advertising_business_report_each['display_count']
                    click_count = abc_dict['click_count'] + advertising_business_report_each['click_count']
                    cost = abc_dict['cost'] + advertising_business_report_each['cost']
                    orders_count = abc_dict['orders_count'] + advertising_business_report_each['orders_count']
                    sales_count = abc_dict['sales_count'] + advertising_business_report_each['sales_count']
                    CTR = '0'
                    if display_count > 0:
                        CTR = str('%.4f' % (float(100 * click_count) / float(display_count)))
                    CPC = 0.00
                    if click_count > 0:
                        CPC = '%.2f' % float(cost / click_count)
                    ACoS = '0.00'
                    if sales_count > 0:
                        ACoS = str('%.2f' % float(100 * cost / sales_count))

                    visit_count = abc_dict['visit_count'] + advertising_business_report_each['visit_count']
                    ordered_count = abc_dict['ordered_count'] + advertising_business_report_each['ordered_count']
                    ordered_sales = abc_dict['ordered_sales'] + advertising_business_report_each['ordered_sales']
                    ordered_count_Conversion_rate = '0.00'
                    if ordered_count != 0 and visit_count != 0:
                        ordered_count_Conversion_rate = str('%.2f' % (float(ordered_count) * 100 / float(visit_count)))
                    AS_amazon = '0.00'
                    if ordered_sales != 0.00 and cost != 0.00:
                        AS_amazon = str('%.2f' % (float(100 * cost / ordered_sales)))
                    AT_amazon = '0.00'
                    if ordered_count != 0 and orders_count != 0:
                        AT_amazon = str('%.2f' % (float(100 * orders_count / ordered_count)))
                    t_template_amazon_advertising_business_count_report.objects.filter(shopname__exact=shopname,
                         ShopSKU__exact=advertising_business_report_each['ShopSKU'].upper(),
                        advertising_status__exact=advertising_business_report_each['advertising_status']).update(CNY=CNY,
                        display_count=display_count,click_count=click_count,cost=cost,orders_count=orders_count,sales_count=sales_count,
                        CTR=CTR,CPC=CPC,ACoS=ACoS,visit_count=visit_count,ordered_count=ordered_count,ordered_sales=ordered_sales,
                        ordered_count_Conversion_rate=ordered_count_Conversion_rate,AS_amazon=AS_amazon,AT_amazon=AT_amazon,
                        )
                else:
                    is_new = 1
            else:
                is_new = 1
            if is_new == 1:
                advertising_business_count_obj = t_template_amazon_advertising_business_count_report()
                advertising_business_count_obj.parent_ASIN = advertising_business_report_each['parent_ASIN']
                advertising_business_count_obj.child_ASIN = advertising_business_report_each['child_ASIN']
                advertising_business_count_obj.item_name = advertising_business_report_each['item_name']
                advertising_business_count_obj.ShopSKU = advertising_business_report_each['ShopSKU'].upper()
                advertising_business_count_obj.visit_count = advertising_business_report_each['visit_count']
                advertising_business_count_obj.visit_percent = advertising_business_report_each['visit_percent']
                advertising_business_count_obj.viewed_count = advertising_business_report_each['viewed_count']
                advertising_business_count_obj.viewed_percent = advertising_business_report_each['viewed_percent']
                advertising_business_count_obj.buyed_button_percent = advertising_business_report_each[
                    'buyed_button_percent']
                advertising_business_count_obj.ordered_count = advertising_business_report_each['ordered_count']
                advertising_business_count_obj.ordered_count_Conversion_rate = advertising_business_report_each[
                    'ordered_count_Conversion_rate']
                advertising_business_count_obj.ordered_sales = advertising_business_report_each['ordered_sales']
                advertising_business_count_obj.ordered_types = advertising_business_report_each['ordered_types']
                advertising_business_count_obj.shopname = advertising_business_report_each['shopname']
                advertising_business_count_obj.action_remark = advertising_business_report_each['action_remark']
                advertising_business_count_obj.remark = advertising_business_report_each['remark']

                advertising_business_count_obj.advertising_status = advertising_business_report_each[
                    'advertising_status']
                advertising_business_count_obj.advertising_campaign_name = advertising_business_report_each[
                    'advertising_campaign_name']
                advertising_business_count_obj.advertising_cost_status = advertising_business_report_each[
                    'advertising_cost_status']
                advertising_business_count_obj.advertising_type = advertising_business_report_each['advertising_type']
                advertising_business_count_obj.serving = advertising_business_report_each['serving']
                advertising_business_count_obj.start_date = advertising_business_report_each['start_date']
                advertising_business_count_obj.end_date = advertising_business_report_each['end_date']
                advertising_business_count_obj.CNY = advertising_business_report_each['CNY']
                advertising_business_count_obj.display_count = advertising_business_report_each['display_count']
                advertising_business_count_obj.click_count = advertising_business_report_each['click_count']
                advertising_business_count_obj.CTR = advertising_business_report_each['CTR']
                advertising_business_count_obj.cost = advertising_business_report_each['cost']
                advertising_business_count_obj.CPC = advertising_business_report_each['CPC']
                advertising_business_count_obj.orders_count = advertising_business_report_each['orders_count']
                advertising_business_count_obj.sales_count = advertising_business_report_each['sales_count']
                advertising_business_count_obj.ACoS = advertising_business_report_each['ACoS']
                advertising_business_count_obj.AS_amazon = advertising_business_report_each['AS_amazon']
                advertising_business_count_obj.AT_amazon = advertising_business_report_each['AT_amazon']
                advertising_business_count_obj.upload_advertising_file = advertising_business_report_each[
                    'upload_advertising_file']
                advertising_business_count_obj.upload_business_file = advertising_business_report_each[
                    'upload_business_file']
                advertising_business_count_obj.upload_time = advertising_business_report_each['upload_time']
                advertising_business_count_obj.upload_user = advertising_business_report_each['upload_user']
                advertising_business_count_obj.update_user = advertising_business_report_each['update_user']
                advertising_business_count_obj.update_time = advertising_business_report_each['update_time']
                advertising_business_count_obj.advertising_business_date = advertising_business_report_each[
                    'advertising_business_date']
                advertising_business_count_obj.image_url = advertising_business_report_each['image_url']
                advertising_business_count_obj.advertising_more = advertising_business_report_each['advertising_more']
                advertising_business_count_obj.business_more = advertising_business_report_each['business_more']
                advertising_online_status = 'Selection_ad'
                if advertising_business_report_each['advertising_status'] == 'PAUSED':
                    advertising_online_status = 'Stoping_ad'
                advertising_business_count_obj.advertising_online_status = advertising_online_status
                advertising_business_count_obj.save()
            CNY_daily += advertising_business_report_each['CNY']
            display_count_daily += advertising_business_report_each['display_count']
            click_count_daily += advertising_business_report_each['click_count']
            cost_daily += advertising_business_report_each['cost']
            orders_count_daily += advertising_business_report_each['orders_count']
            sales_count_daily += advertising_business_report_each['sales_count']
            visit_count_daily += advertising_business_report_each['visit_count']
            ordered_count_daily += advertising_business_report_each['ordered_count']
            ordered_sales_daily += advertising_business_report_each['ordered_sales']
        CTR_daily = '0'
        if display_count_daily > 0:
            CTR_daily = str('%.4f' % (float(100 * click_count_daily) / float(display_count_daily)))
        CPC_daily = 0.00
        if click_count_daily > 0:
            CPC_daily = '%.2f' % float(cost_daily / click_count_daily)
        ACoS_daily = '0.00'
        if sales_count_daily > 0:
            ACoS_daily = str('%.2f' % float(100 * cost_daily / sales_count_daily))
        ordered_count_Conversion_rate_daily = '0.00'
        if ordered_count_daily != 0 and visit_count_daily != 0:
            ordered_count_Conversion_rate_daily = str('%.2f' % (float(ordered_count_daily) * 100 / float(visit_count_daily)))
        AS_amazon_daily = '0.00'
        if ordered_sales_daily != 0.00 and cost_daily != 0.00:
            AS_amazon_daily = str('%.2f' % (float(100 * cost_daily / ordered_sales_daily)))
        AT_amazon_daily = '0.00'
        if ordered_count_daily != 0 and orders_count_daily != 0:
            AT_amazon_daily = str('%.2f' % (float(100 * orders_count_daily / ordered_count_daily)))
        if advertising_business_date_daily:
            advertising_business_daily_obj = t_template_amazon_advertising_business_daily_report()
            advertising_business_daily_obj.visit_count = visit_count_daily
            advertising_business_daily_obj.ordered_count = ordered_count_daily
            advertising_business_daily_obj.ordered_count_Conversion_rate = ordered_count_Conversion_rate_daily
            advertising_business_daily_obj.ordered_sales = ordered_sales_daily
            advertising_business_daily_obj.shopname = shopname
            advertising_business_daily_obj.CNY = CNY_daily
            advertising_business_daily_obj.display_count = display_count_daily
            advertising_business_daily_obj.click_count = click_count_daily
            advertising_business_daily_obj.CTR = CTR_daily
            advertising_business_daily_obj.cost = cost_daily
            advertising_business_daily_obj.CPC = CPC_daily
            advertising_business_daily_obj.orders_count = orders_count_daily
            advertising_business_daily_obj.sales_count = sales_count_daily
            advertising_business_daily_obj.ACoS = ACoS_daily
            advertising_business_daily_obj.AS_amazon = AS_amazon_daily
            advertising_business_daily_obj.AT_amazon = AT_amazon_daily
            advertising_business_daily_obj.upload_time = upload_time
            advertising_business_daily_obj.upload_user = user_name
            advertising_business_daily_obj.advertising_business_date = advertising_business_date_daily
            advertising_business_daily_obj.save()
            count_shop_report_obj = t_template_amazon_advertising_business_count_shop_report.objects.filter(shopname__exact=shopname)
            if count_shop_report_obj.exists():
                abc_dict = count_shop_report_obj[0].__dict__
                CNY = abc_dict['CNY'] + CNY_daily
                display_count = abc_dict['display_count'] + display_count_daily
                click_count = abc_dict['click_count'] + click_count_daily
                cost = abc_dict['cost'] + cost_daily
                orders_count = abc_dict['orders_count'] + orders_count_daily
                sales_count = abc_dict['sales_count'] + sales_count_daily
                CTR = '0'
                if display_count > 0:
                    CTR = str('%.4f' % (float(100 * click_count) / float(display_count)))
                CPC = 0.00
                if click_count > 0:
                    CPC = '%.2f' % float(cost / click_count)
                ACoS = '0.00'
                if sales_count > 0:
                    ACoS = str('%.2f' % float(100 * cost / sales_count))

                visit_count = abc_dict['visit_count'] + visit_count_daily
                ordered_count = abc_dict['ordered_count'] + ordered_count_daily
                ordered_sales = abc_dict['ordered_sales'] + ordered_sales_daily
                ordered_count_Conversion_rate = '0.00'
                if ordered_count != 0 and visit_count != 0:
                    ordered_count_Conversion_rate = str('%.2f' % (float(ordered_count) * 100 / float(visit_count)))
                AS_amazon = '0.00'
                if ordered_sales != 0.00 and cost != 0.00:
                    AS_amazon = str('%.2f' % (float(100 * cost / ordered_sales)))
                AT_amazon = '0.00'
                if ordered_count != 0 and orders_count != 0:
                    AT_amazon = str('%.2f' % (float(100 * orders_count / ordered_count)))
                t_template_amazon_advertising_business_count_shop_report.objects.filter(shopname__exact=shopname).update(
                    CNY=CNY,
                    display_count=display_count, click_count=click_count, cost=cost, orders_count=orders_count,
                    sales_count=sales_count,
                    CTR=CTR, CPC=CPC, ACoS=ACoS, visit_count=visit_count, ordered_count=ordered_count,
                    ordered_sales=ordered_sales,
                    ordered_count_Conversion_rate=ordered_count_Conversion_rate, AS_amazon=AS_amazon,
                    AT_amazon=AT_amazon)
            else:
                count_shop_report = t_template_amazon_advertising_business_count_shop_report()
                count_shop_report.visit_count = visit_count_daily
                count_shop_report.ordered_count = ordered_count_daily
                count_shop_report.ordered_count_Conversion_rate = ordered_count_Conversion_rate_daily
                count_shop_report.ordered_sales = ordered_sales_daily
                count_shop_report.shopname = shopname
                count_shop_report.CNY = CNY_daily
                count_shop_report.display_count = display_count_daily
                count_shop_report.click_count = click_count_daily
                count_shop_report.CTR = CTR_daily
                count_shop_report.cost = cost_daily
                count_shop_report.CPC = CPC_daily
                count_shop_report.orders_count = orders_count_daily
                count_shop_report.sales_count = sales_count_daily
                count_shop_report.ACoS = ACoS_daily
                count_shop_report.AS_amazon = AS_amazon_daily
                count_shop_report.AT_amazon = AT_amazon_daily
                count_shop_report.upload_time = upload_time
                count_shop_report.upload_user = user_name
                count_shop_report.advertising_business_date = advertising_business_date_daily
                count_shop_report.save()


    def deal_with_advertising_report(self,row,shopname,user_name,advertising_business_dict,advertising_key,advertising_business_date,upload_time):
        advertising_dict = {}
        advertising_campaign_name_ending_list = ['-a', '-A', '-m', '-M']
        advertising_campaign_name_ending = str(row[1])[-2:]
        advertising_campaign_name = str(row[1])
        if advertising_campaign_name_ending in advertising_campaign_name_ending_list:
            advertising_campaign_name = advertising_campaign_name[:-2]
        advertising_dict['advertising_status'] = str(row[0])
        advertising_dict['advertising_campaign_name'] = advertising_campaign_name
        advertising_dict['advertising_cost_status'] = str(row[2])
        advertising_dict['advertising_type'] = str(row[3])
        advertising_dict['serving'] = str(row[4])
        time_str = '%y-%m-%d'
        if '-' in str(row[5]):
            time_year = str(row[5]).split('-')[0]
            if len(time_year) == 4:
                time_str = '%Y-%m-%d'
        if '/' in str(row[5]):
            time_str = '%Y/%m/%d'
            time_year = str(row[5]).split('-')[0]
            if len(time_year) == 2:
                time_str = '%y/%m/%d'
        advertising_dict['start_date'] = datetime.strptime(row[5], time_str)
        end_date = None
        if row[6]:
            end_date = datetime.strptime(row[6], time_str)
        advertising_dict['end_date'] = end_date

        CNY = row[7]
        if '.' in CNY:
            CNY = CNY.split('.')[0]
        advertising_dict['CNY'] = int(CNY.replace(',', ''))
        advertising_dict['display_count'] = int(row[8].replace(',', ''))
        advertising_dict['click_count'] = int(row[9].replace(',', ''))
        advertising_dict['CTR'] = str(row[10])
        advertising_dict['cost'] = decimal.Decimal("%.2f" % float(row[11].replace(',', '')))
        advertising_dict['CPC'] = decimal.Decimal("%.2f" % float(row[12].replace(',', '')))
        advertising_dict['orders_count'] = int(row[13].replace(',', ''))
        advertising_dict['sales_count'] = decimal.Decimal("%.2f" % float(row[14].replace(',', '')))
        advertising_dict['ACoS'] = decimal.Decimal("%.2f" % float(row[15].replace(',', '')))
        advertising_dict['advertising_count'] = 1
        advertising_dict['upload_advertising_file'] = ''

        ad_obj = t_template_amazon_advertising_report()

        ad_obj.advertising_status = advertising_dict['advertising_status']
        ad_obj.advertising_campaign_name = str(row[1])
        ad_obj.advertising_cost_status = advertising_dict['advertising_cost_status']
        ad_obj.advertising_type = advertising_dict['advertising_type']
        ad_obj.serving = advertising_dict['serving']
        ad_obj.start_date = advertising_dict['start_date']
        ad_obj.end_date = advertising_dict['end_date']
        ad_obj.CNY = advertising_dict['CNY']
        ad_obj.display_count = advertising_dict['display_count']
        ad_obj.click_count = advertising_dict['click_count']
        ad_obj.CTR = str('%.4f' %(float(advertising_dict['CTR'])))
        ad_obj.cost = advertising_dict['cost']
        ad_obj.CPC = '%.2f' %float(advertising_dict['CPC'])
        ad_obj.orders_count = advertising_dict['orders_count']
        ad_obj.sales_count = advertising_dict['sales_count']
        ad_obj.ACoS = str('%.2f' %float(advertising_dict['ACoS']))
        ad_obj.shopname = shopname
        ad_obj.upload_time = upload_time
        ad_obj.upload_user = user_name
        ad_obj.update_user = ''
        ad_obj.update_time = None
        ad_obj.ShopSKU = str(row[1]).split('-')[0]
        ad_obj.advertising_data = advertising_business_date
        ad_obj.save()

        if advertising_business_dict.has_key(advertising_key):
            old_advertising_dict = advertising_business_dict[advertising_key]
            advertising_dict['advertising_count'] = old_advertising_dict['advertising_count'] + 1
            advertising_dict['CNY'] = int(CNY.replace(',', '')) + old_advertising_dict['CNY']
            advertising_dict['advertising_campaign_name'] = old_advertising_dict['advertising_campaign_name']
            advertising_dict['display_count'] = int(row[8].replace(',', '')) + old_advertising_dict['display_count']
            advertising_dict['click_count'] = int(row[9].replace(',', '')) + old_advertising_dict['click_count']
            advertising_dict['CTR'] = str(float(row[10].replace(',', '')) + float(old_advertising_dict['CTR']))
            advertising_dict['cost'] = decimal.Decimal("%.2f" % float(row[11].replace(',', ''))) + old_advertising_dict[
                'cost']
            advertising_dict['CPC'] = decimal.Decimal("%.2f" % float(row[12].replace(',', ''))) + old_advertising_dict[
                'CPC']
            advertising_dict['orders_count'] = int(row[13].replace(',', '')) + old_advertising_dict['orders_count']
            advertising_dict['sales_count'] = decimal.Decimal("%.2f" % float(row[14].replace(',', ''))) + \
                                              old_advertising_dict['sales_count']
            advertising_dict['ACoS'] = decimal.Decimal("%.2f" % float(row[15].replace(',', ''))) + old_advertising_dict[
                'ACoS']
        if advertising_key:
            advertising_business_dict[advertising_key] = advertising_dict
        else:
            advertising_business_obj = t_template_amazon_advertising_business_report()
            advertising_business_obj.advertising_status = advertising_dict['advertising_status']
            code_type = chardet.detect(advertising_dict['advertising_campaign_name'])
            advertising_campaign_name = advertising_dict['advertising_campaign_name']
            if code_type['encoding'] == 'ISO-8859-1' or code_type['encoding'] is None:
                advertising_campaign_name = advertising_campaign_name.decode('GBK').encode('utf8')
            advertising_business_obj.advertising_campaign_name = advertising_campaign_name
            advertising_business_obj.advertising_cost_status = advertising_dict['advertising_cost_status']
            advertising_business_obj.advertising_type = advertising_dict['advertising_type']
            advertising_business_obj.serving = advertising_dict['serving']
            advertising_business_obj.start_date = advertising_dict['start_date']
            advertising_business_obj.end_date = advertising_dict['end_date']
            advertising_business_obj.CNY = advertising_dict['CNY']
            advertising_business_obj.display_count = advertising_dict['display_count']
            advertising_business_obj.click_count = advertising_dict['click_count']
            CTR = '0'
            if advertising_dict['display_count'] > 0:
                CTR = str('%.4f' %(float(100 * advertising_dict['click_count']) / float(advertising_dict['display_count'])))
            advertising_business_obj.CTR = CTR
            advertising_business_obj.cost = advertising_dict['cost']
            CPC = 0.00
            if advertising_dict['click_count'] > 0:
                CPC = '%.2f' %float(advertising_dict['cost'] / advertising_dict['click_count'])
            advertising_business_obj.CPC = CPC
            advertising_business_obj.orders_count = advertising_dict['orders_count']
            advertising_business_obj.sales_count = advertising_dict['sales_count']
            ACoS = '0.00'
            if advertising_dict['sales_count'] > 0:
                ACoS = str('%.2f' %float(100 * advertising_dict['cost'] / advertising_dict['sales_count']))
            advertising_business_obj.ACoS = ACoS
            advertising_business_obj.ShopSKU = advertising_campaign_name.split('-')[0].upper()
            t_online_info_amazon_obj = t_online_info_amazon.objects.filter(ShopName__exact=shopname,
                                           seller_sku__iexact=advertising_campaign_name.split('-')[0].upper())
            image_url = None
            if t_online_info_amazon_obj.exists():
                image_url = t_online_info_amazon_obj[0].image_url
            else:
                t_online_info_amazon_obj = t_online_info_amazon.objects.filter(ShopName__exact=shopname,
                                                                               asin1__iexact=advertising_campaign_name.split('-')[0].upper())
                if t_online_info_amazon_obj.exists():
                    image_url = t_online_info_amazon_obj[0].image_url
            advertising_business_obj.image_url = image_url
            advertising_more = '0'
            if advertising_dict['advertising_count'] > 1:
                advertising_more = '1'
            advertising_business_obj.advertising_more = advertising_more
            advertising_business_obj.parent_ASIN = ''
            advertising_business_obj.child_ASIN = ''
            advertising_business_obj.item_name = ''
            advertising_business_obj.visit_count = 0
            advertising_business_obj.visit_percent = '0%'
            advertising_business_obj.viewed_count = 0
            advertising_business_obj.viewed_percent = '0%'
            advertising_business_obj.buyed_button_percent = '0%'
            advertising_business_obj.ordered_count = 0
            advertising_business_obj.ordered_count_Conversion_rate = '0.00'
            advertising_business_obj.ordered_sales = 0.00
            advertising_business_obj.ordered_types = 0
            advertising_business_obj.business_more = '0'
            advertising_business_obj.AS_amazon = '0.00'
            advertising_business_obj.AT_amazon = '0.00'
            advertising_business_obj.upload_advertising_file = ''
            advertising_business_obj.upload_business_file = ''
            advertising_business_obj.upload_time = upload_time
            advertising_business_obj.upload_user = user_name
            advertising_business_obj.shopname = shopname
            advertising_business_obj.update_user = ''
            advertising_business_obj.update_time = None
            advertising_business_obj.advertising_business_date = advertising_business_date
            advertising_business_obj.save()
        return advertising_business_dict

    def deal_with_business_report(self,row,business_dict_final,user_name,advertising_business_date,shopname,upload_time):
        business_dict = {}
        business_dict['parent_ASIN'] = str(row[0])
        business_dict['child_ASIN'] = str(row[1])
        business_dict['item_name'] = str(row[2])
        business_dict['ShopSKU'] = str(row[0])
        business_dict['visit_count'] = int(row[3].replace(',', ''))
        business_dict['visit_percent'] = str(row[4])
        business_dict['viewed_count'] = int(row[5].replace(',', ''))
        business_dict['viewed_percent'] = str(row[6].replace('%', ''))
        business_dict['buyed_button_percent'] = str(row[7])
        business_dict['ordered_count'] = int(row[8].replace(',', ''))
        business_dict['ordered_count_Conversion_rate'] = str(row[9])
        business_dict['ordered_sales'] = decimal.Decimal("%.2f" % float(row[10].replace('US$', '').replace(',', '')))
        business_dict['ordered_types'] = int(row[11].replace(',', ''))
        business_dict['business_count'] = 1
        if business_dict_final.has_key(str(row[0])):
            old_business_dict = business_dict_final[str(row[0])]
            business_dict['business_count'] = 1 + old_business_dict['business_count']
            business_dict['visit_count'] = int(row[3].replace(',', '')) + old_business_dict['visit_count']
            business_dict['visit_percent'] = str((float(row[4].replace('%', '')) + float(old_business_dict['visit_percent'].replace('%', ''))))
            business_dict['viewed_count'] = int(row[5].replace(',', '')) + old_business_dict['viewed_count']
            business_dict['viewed_percent'] = str((float(row[6].replace('%', '')) + float(old_business_dict['viewed_percent'].replace('%', ''))))
            business_dict['buyed_button_percent'] = str((float(row[7].replace('%', '')) + float(old_business_dict['buyed_button_percent'].replace('%', ''))))
            business_dict['ordered_count'] = int(row[8].replace(',', '')) + old_business_dict['ordered_count']
            ordered_count_Conversion_rate = '0.00'
            if old_business_dict['visit_count'] != 0:
                ordered_count_Conversion_rate = str('%.2f' % (float(old_business_dict['ordered_count']) * 100 / float(old_business_dict['visit_count'])))
            business_dict['ordered_count_Conversion_rate'] = ordered_count_Conversion_rate
            business_dict['ordered_sales'] = decimal.Decimal(
                "%.2f" % float(row[10].replace('US$', '').replace(',', ''))) + old_business_dict['ordered_sales']
            business_dict['ordered_types'] = int(row[11].replace(',', '')) + old_business_dict['ordered_types']
        business_dict_final[str(row[0])] = business_dict

        t_online_info_amazon_objs = t_online_info_amazon.objects.filter(ShopName__exact=shopname,
                                                                        asin1__exact=str(row[1])).values('SKU')
        sku = ''
        if t_online_info_amazon_objs.exists():
            sku = t_online_info_amazon_objs[0]['SKU']

        business_obj = t_template_amazon_business_report()
        business_obj.parent_ASIN = str(row[0])
        business_obj.child_ASIN = str(row[1])
        business_obj.item_name = str(row[2])
        business_obj.ShopSKU = sku
        business_obj.visit_count = int(row[3].replace(',', ''))
        business_obj.visit_percent = str(row[4])
        business_obj.viewed_count = int(row[5].replace(',', ''))
        business_obj.viewed_percent = str(row[6])
        business_obj.buyed_button_percent = str(row[7])
        business_obj.ordered_count = int(row[8].replace(',', ''))
        business_obj.ordered_count_Conversion_rate = str(row[9])
        business_obj.ordered_sales = decimal.Decimal("%.2f" % float(row[10].replace('US$', '').replace(',', '')))
        business_obj.ordered_types = int(row[11].replace(',', ''))
        business_obj.upload_file = ''
        business_obj.upload_time = upload_time
        business_obj.upload_user = user_name
        business_obj.update_user = ''
        business_obj.update_time = None
        business_obj.shopname = shopname
        business_obj.business_date = advertising_business_date
        business_obj.save()
        return business_dict_final

    def save_models(self):
        obj = self.new_obj
        upload_time = datetime.now()
        request = self.request
        user_name = request.user.first_name
        shopname = obj.shopname
        advertising_business_date = obj.advertising_business_date
        # try:
        advertising_business_dict = {}
        i = 0
        for row in csv.reader(obj.upload_advertising_file):
            if i < 1:
                i += 1
                continue
            if row:
                t_online_info_amazon_objs = t_online_info_amazon.objects.filter(ShopName__exact=shopname,seller_sku__iexact=str(row[1]).split('-')[0])
                advertising_key = ''
                if t_online_info_amazon_objs.exists():
                    advertising_key = t_online_info_amazon_objs[0].asin1
                else:
                    advertising_key = str(row[1]).split('-')[0].upper()
                advertising_business_dict= self.deal_with_advertising_report(row,shopname,user_name,advertising_business_dict,advertising_key,advertising_business_date,upload_time)
            i += 1
        error_list = []
        business_dict_final = {}
        j = 0
        for row in csv.reader(obj.upload_business_file):
            if j < 1:
                j += 1
                continue
            if row:
                business_dict_final = self.deal_with_business_report(row,business_dict_final,user_name,advertising_business_date,shopname,upload_time)
            j += 1

        ret_asins_in = [i for i in advertising_business_dict.keys() if i in business_dict_final.keys()]
        for ret_asin_in in ret_asins_in:
            if ret_asin_in not in error_list:
                error_list.append(ret_asin_in)
                new_advertising_dict = advertising_business_dict[ret_asin_in]
                advertising_business_report = t_template_amazon_advertising_business_report()
                new_business_dict = business_dict_final[ret_asin_in]
                advertising_business_report.parent_ASIN = new_business_dict['parent_ASIN']
                advertising_business_report.child_ASIN = new_business_dict['child_ASIN']
                advertising_business_report.item_name = new_business_dict['item_name']
                advertising_business_report.ShopSKU = new_advertising_dict['advertising_campaign_name'].split('-')[0].upper()
                advertising_business_report.visit_count = new_business_dict['visit_count']
                advertising_business_report.visit_percent = str(float(new_business_dict['visit_percent'].replace('%', ''))/new_business_dict['business_count']) + '%'
                advertising_business_report.viewed_count = new_business_dict['viewed_count']
                advertising_business_report.viewed_percent = str(float(new_business_dict['viewed_percent'].replace('%', ''))/new_business_dict['business_count']) + '%'
                advertising_business_report.buyed_button_percent = str(float(new_business_dict['buyed_button_percent'].replace('%', ''))/new_business_dict['business_count']) + '%'
                advertising_business_report.ordered_count = new_business_dict['ordered_count']
                ordered_count_Conversion_rate = '0.00'
                if new_business_dict['visit_count'] != 0:
                    ordered_count_Conversion_rate = str('%.2f' %(float(new_business_dict['ordered_count']) * 100/float(new_business_dict['visit_count'])))
                advertising_business_report.ordered_count_Conversion_rate = ordered_count_Conversion_rate
                advertising_business_report.ordered_sales = new_business_dict['ordered_sales']
                advertising_business_report.ordered_types = new_business_dict['ordered_types']
                advertising_business_report.shopname = shopname
                advertising_business_report.action_remark = ''
                advertising_business_report.remark = ''
                advertising_business_report.advertising_status = new_advertising_dict['advertising_status']
                advertising_business_report.advertising_campaign_name = new_advertising_dict['advertising_campaign_name']
                advertising_business_report.advertising_cost_status = new_advertising_dict['advertising_cost_status']
                advertising_business_report.advertising_type = new_advertising_dict['advertising_type']
                advertising_business_report.serving = new_advertising_dict['serving']
                advertising_business_report.start_date = new_advertising_dict['start_date']
                advertising_business_report.end_date = new_advertising_dict['end_date']
                advertising_business_report.CNY = new_advertising_dict['CNY']
                advertising_business_report.display_count = new_advertising_dict['display_count']
                advertising_business_report.click_count = new_advertising_dict['click_count']
                CTR = '0'
                if new_advertising_dict['display_count'] > 0:
                    CTR = str('%.4f' %(float(100 * new_advertising_dict['click_count']) / float(new_advertising_dict['display_count'])))
                advertising_business_report.CTR = CTR
                advertising_business_report.cost = new_advertising_dict['cost']
                CPC = 0.00
                if new_advertising_dict['click_count'] > 0:
                    CPC = '%.2f' %float(new_advertising_dict['cost'] / new_advertising_dict['click_count'])
                advertising_business_report.CPC = CPC
                advertising_business_report.orders_count = new_advertising_dict['orders_count']
                advertising_business_report.sales_count = new_advertising_dict['sales_count']
                ACoS = '0.00'
                if new_advertising_dict['sales_count'] > 0:
                    ACoS = str('%.2f' %float(100 * new_advertising_dict['cost'] / new_advertising_dict['sales_count']))
                advertising_business_report.ACoS = ACoS
                AS_amazon = '0.00'
                if new_business_dict['ordered_sales'] != 0.00 and new_advertising_dict['cost'] != 0.00:
                    AS_amazon = str('%.2f' % (float(100 * new_advertising_dict['cost'] / new_business_dict['ordered_sales'])))
                AT_amazon = '0.00'
                if new_business_dict['ordered_count'] != 0 and new_advertising_dict['orders_count'] != 0:
                    AT_amazon = str('%.2f' % (float(100 * new_advertising_dict['orders_count'] / new_business_dict['ordered_count'])))
                advertising_business_report.AS_amazon = AS_amazon
                advertising_business_report.AT_amazon = AT_amazon
                advertising_business_report.upload_advertising_file = ''
                advertising_business_report.upload_business_file = ''
                advertising_business_report.upload_time = upload_time
                advertising_business_report.upload_user = user_name
                advertising_business_report.update_user = ''
                advertising_business_report.update_time = None
                advertising_business_report.advertising_business_date = advertising_business_date
                t_online_info_amazon_obj = t_online_info_amazon.objects.filter(ShopName__exact=shopname,
                                               seller_sku__exact=new_advertising_dict['advertising_campaign_name'].split('-')[0])
                image_url = None
                if t_online_info_amazon_obj.exists():
                    image_url = t_online_info_amazon_obj[0].image_url
                else:
                    t_online_info_amazon_obj = t_online_info_amazon.objects.filter(ShopName__exact=shopname,
                                                                                   asin1__iexact=new_advertising_dict['advertising_campaign_name'].split('-')[0].upper())
                    if t_online_info_amazon_obj.exists():
                        image_url = t_online_info_amazon_obj[0].image_url
                if image_url and 'no-img-sm' in image_url:
                    image_url = t_online_info_amazon.objects.filter(ShopName__exact=shopname,Parent_asin__exact=t_online_info_amazon_obj[0].asin1)[0].image_url
                advertising_business_report.image_url = image_url
                advertising_more = '0'
                if new_advertising_dict['advertising_count'] > 1:
                    advertising_more = '1'
                advertising_business_report.advertising_more = advertising_more
                business_more = '0'
                if new_business_dict['business_count'] > 1:
                    business_more = '1'
                advertising_business_report.business_more = business_more
                advertising_business_report.save()

        ret_asins = [i for i in advertising_business_dict.keys() if i not in error_list]
        for ret_asin in ret_asins:
            new_obj1 = t_template_amazon_advertising_business_report()
            new_advertising_dict = advertising_business_dict[ret_asin]
            new_obj1.parent_ASIN = ret_asin
            new_obj1.child_ASIN = ''
            new_obj1.item_name = ''
            new_obj1.ShopSKU = ''
            new_obj1.visit_count = 0
            new_obj1.visit_percent = '0%'
            new_obj1.viewed_count = 0
            new_obj1.viewed_percent = '0%'
            new_obj1.buyed_button_percent = '0%'
            new_obj1.ordered_count = 0
            new_obj1.ordered_count_Conversion_rate = '0.00'
            new_obj1.ordered_sales = 0.00
            new_obj1.ordered_types = 0
            new_obj1.advertising_status = new_advertising_dict['advertising_status']
            new_obj1.advertising_campaign_name = new_advertising_dict['advertising_campaign_name']
            new_obj1.advertising_cost_status = new_advertising_dict['advertising_cost_status']
            new_obj1.advertising_type = new_advertising_dict['advertising_type']
            new_obj1.serving = new_advertising_dict['serving']
            new_obj1.start_date = new_advertising_dict['start_date']
            new_obj1.end_date = new_advertising_dict['end_date']
            new_obj1.CNY = new_advertising_dict['CNY']
            new_obj1.display_count = new_advertising_dict['display_count']
            new_obj1.click_count = new_advertising_dict['click_count']
            CTR = '0'
            if new_advertising_dict['display_count'] > 0:
                CTR = str('%.4f' %(float(100 * new_advertising_dict['click_count']) / float(new_advertising_dict['display_count'])))
            new_obj1.CTR = CTR
            new_obj1.cost = new_advertising_dict['cost']
            CPC = 0.00
            if new_advertising_dict['click_count'] > 0:
                CPC = '%.2f' %float(new_advertising_dict['cost'] / new_advertising_dict['click_count'])
            new_obj1.CPC = CPC
            new_obj1.orders_count = new_advertising_dict['orders_count']
            new_obj1.sales_count = new_advertising_dict['sales_count']
            ACoS = '0.00'
            if new_advertising_dict['sales_count'] > 0:
                ACoS = str('%.2f' %float(100 * new_advertising_dict['cost'] / new_advertising_dict['sales_count']))
            new_obj1.ACoS = ACoS
            new_obj1.AS_amazon = "0.00"
            new_obj1.AT_amazon = "0.00"
            new_obj1.upload_advertising_file = ''
            new_obj1.upload_business_file = ''
            new_obj1.upload_time = upload_time
            new_obj1.upload_user = user_name
            new_obj1.shopname = shopname
            new_obj1.update_user = ''
            new_obj1.update_time = None
            new_obj1.advertising_business_date = advertising_business_date
            new_obj1.ShopSKU = new_advertising_dict['advertising_campaign_name'].split('-')[0].upper()
            t_online_info_amazon_obj = t_online_info_amazon.objects.filter(ShopName__exact=shopname,seller_sku__exact=new_advertising_dict['advertising_campaign_name'].split('-')[0])
            image_url = None
            if t_online_info_amazon_obj.exists():
                image_url = t_online_info_amazon_obj[0].image_url
            else:
                t_online_info_amazon_obj = t_online_info_amazon.objects.filter(ShopName__exact=shopname,
                                                                               asin1__iexact=new_advertising_dict['advertising_campaign_name'].split('-')[0].upper())
                if t_online_info_amazon_obj.exists():
                    image_url = t_online_info_amazon_obj[0].image_url
            if image_url and 'no-img-sm' in image_url:
                image_url = t_online_info_amazon.objects.filter(ShopName__exact=shopname,Parent_asin__exact=t_online_info_amazon_obj[0].asin1)[0].image_url
            new_obj1.image_url = image_url
            advertising_more = '0'
            if new_advertising_dict['advertising_count'] > 1:
                advertising_more = '1'
            new_obj1.advertising_more = advertising_more
            new_obj1.business_more = '0'
            new_obj1.save()
        self.caculate_all_and_insert(shopname,advertising_business_date,upload_time)

            # except Exception, e:
            #     messages.error(request, u'李杨杨')

    def get_list_queryset(self, ):
        request = self.request
        qs = super(t_template_amazon_advertising_business_report_Admin, self).get_list_queryset()

        shopname = request.GET.get('shopname', '')
        if shopname == '':
            shopname = request.GET.get('_p_shopname', '')
        ShopSKU = request.GET.get('ShopSKU', '')
        if ShopSKU == '':
            ShopSKU = request.GET.get('_p_ShopSKU', '')
        pdate_Start = request.GET.get('pdate_Start', '')
        pdate_End = request.GET.get('pdate_End', '')
        uploadtime_End = request.GET.get('uploadtime_End', '')
        ad_status = request.GET.get('ad_status', '')
        parent_ASIN = request.GET.get('parent_ASIN', '')

        searchList = {'shopname__icontains': shopname,
                      'ShopSKU__contains': ShopSKU,
                      'advertising_status__exact': ad_status,
                      'advertising_business_date__gte': pdate_Start,
                      'advertising_business_date__lt': pdate_End,
                      'upload_time__lte': uploadtime_End,
                      'parent_ASIN__icontains': parent_ASIN,
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