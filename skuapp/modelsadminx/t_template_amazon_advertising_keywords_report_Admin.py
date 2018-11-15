#-*-coding:utf-8-*-
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from django.utils.safestring import mark_safe
from django.contrib import messages
import decimal,xlrd
from xlrd import xldate_as_datetime
from datetime import datetime
from skuapp.table.t_template_amazon_advertising_report import t_template_amazon_advertising_report
from skuapp.table.t_template_amazon_advertising_keywords_report import t_template_amazon_advertising_keywords_report


"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_template_amazon_advertising_keywords_report_Admin.py
 @time: 2018/8/16 11:01
"""   
class t_template_amazon_advertising_keywords_report_Admin(object):
    site_left_menu_tree_amazon_advertising_flag = True
    amazon_shop_search_flag = True
    search_box_flag = True

    def show_main_info(self, obj):
        rt = u'广告组名称:%s<br>广告活动名称:%s<br>关键词周开始日期:%s<br>关键词周结束日期:%s<br>店铺名称:%s' \
             % (obj.advertising_group_name, obj.advertising_campaign_name, obj.advertising_keyword_start_date,
                obj.advertising_keyword_end_date, obj.shopname)
        return mark_safe(rt)
    show_main_info.short_description = u'<p style="width:40px;color:#428bca;" align="center">广告</p>'

    def show_CTR(self, obj):
        #点击率
        class_style = ''
        if float(obj.CTR) < 2:
            class_style = 'style="color:red"'
        rt = u'<span %s>%s</span>'% (class_style, obj.CTR)
        return mark_safe(rt)

    show_CTR.short_description = u'<p style="color:#428bca;" align="center">点击率(%)</p>'

    def show_CPC(self, obj):
        #每次点击成本($)
        class_style = ''
        if float(obj.CPC) > 0.7:
            class_style = 'style="color:red"'
        rt = u'<span %s>%s</span>'% (class_style, obj.CPC)
        return mark_safe(rt)

    show_CPC.short_description = u'<p style="color:#428bca;" align="center">每次点击成本($)</p>'

    def show_ACOS(self, obj):
        #ACOS(%)
        class_style = ''
        if float(obj.ACoS) > 35:
            class_style = 'style="color:red"'
        rt = u'<span %s>%s</span>'% (class_style, obj.ACoS)
        return mark_safe(rt)

    show_ACOS.short_description = u'<p style="color:#428bca;" align="center">ACOS(%)</p>'

    def show_conversion_7_rate(self, obj):
        #7天转化率(%)
        class_style = ''
        if float(obj.conversion_7_rate) < 10:
            class_style = 'style="color:red"'
        rt = u'<span %s>%s</span>'% (class_style, obj.conversion_7_rate)
        return mark_safe(rt)

    show_conversion_7_rate.short_description = u'<p style="color:#428bca;" align="center">7天转化率(%)</p>'

    list_display = ('show_main_info', 'keyword', 'search_words', 'display_count', 'click_count', 'show_CTR',
                    'show_CPC',  'cost', 'orders_7_count', 'sales_7_count','show_conversion_7_rate', 'show_ACOS',)

    list_display_links = ('id',)

    fields = ('upload_file', 'shopname', 'advertising_keyword_start_date', 'advertising_keyword_end_date')

    def save_models(self):
        obj = self.new_obj

        request = self.request
        user_name = request.user.first_name
        shopname = obj.shopname
        advertising_keyword_date = obj.advertising_keyword_date
        advertising_keyword_start_date = obj.advertising_keyword_start_date
        advertising_keyword_end_date = obj.advertising_keyword_end_date
        ExcelFile = xlrd.open_workbook(filename=None, file_contents=obj.upload_file.read())
        sheet = ExcelFile.sheet_by_index(0)
        nrows = sheet.nrows  # 行数
        for rownum in range(1, nrows):
            row = sheet.row_values(rownum)
            if row:
                new_obj = t_template_amazon_advertising_keywords_report()
                new_obj.upload_file = ''

                new_obj.start_date = xldate_as_datetime(row[0], 0)
                new_obj.end_date = xldate_as_datetime(row[1], 0)
                new_obj.currency = row[2]
                new_obj.advertising_group_name = row[4]
                new_obj.advertising_campaign_name = row[3]
                new_obj.keyword = row[5]
                new_obj.advertising_type = row[6]
                new_obj.search_words = row[7]
                new_obj.display_count = int(row[8])
                new_obj.click_count = int(row[9])
                CTR = 0.00
                if row[10]:
                    CTR = decimal.Decimal("%.2f" % (100 * float(row[10])))
                new_obj.CTR = str(CTR)
                cpc = 0.00
                if row[11]:
                    cpc = decimal.Decimal("%.2f" % float(row[11]))
                new_obj.CPC = cpc
                new_obj.cost = decimal.Decimal("%.2f" % float(row[12]))
                new_obj.sales_7_count = decimal.Decimal("%.2f" % float(row[13]))
                ACoS = 0.00
                if row[14]:
                    ACoS = decimal.Decimal("%.2f" % (100 * float(row[14])))
                new_obj.ACoS = str(ACoS)
                RoAS = 0.00
                if row[15]:
                    RoAS = decimal.Decimal("%.2f" % float(row[15]))
                new_obj.RoAS = str(RoAS)
                conversion_7_rate = 0.00
                if row[18]:
                    conversion_7_rate = decimal.Decimal("%.2f" % (100 * float(row[18])))
                new_obj.conversion_7_rate = str(conversion_7_rate)
                new_obj.orders_7_count = int(row[16])
                new_obj.ordered_7_count = int(row[17])
                new_obj.ordered_7_sku_in_count = int(row[19])
                new_obj.ordered_7_sku_out_count = int(row[20])
                new_obj.sales_7_sku_in_count = decimal.Decimal("%.2f" % float(row[21]))
                new_obj.sales_7_sku_out_count = decimal.Decimal("%.2f" % float(row[22]))

                new_obj.shopname = shopname
                new_obj.ShopSKU = row[3].split('-')[0]
                new_obj.action_remark = ''
                new_obj.remark = ''

                new_obj.upload_time = datetime.now()
                new_obj.upload_user = user_name
                new_obj.update_user = ''
                new_obj.update_time = None

                new_obj.advertising_keyword_date = advertising_keyword_date
                new_obj.advertising_keyword_start_date = advertising_keyword_start_date
                new_obj.advertising_keyword_end_date = advertising_keyword_end_date
                new_obj.save()

    def get_list_queryset(self, ):
        request = self.request
        qs = super(t_template_amazon_advertising_keywords_report_Admin, self).get_list_queryset()
        #'start_date', 'end_date', 'advertising_campaign_name', 'advertising_group_name', 'keyword', 'search_words'
        shopname = request.GET.get('shopname', '')
        advertising_campaign_name = request.GET.get('advertising_campaign_name', '')
        advertising_group_name = request.GET.get('advertising_group_name', '')
        keyword = request.GET.get('keyword', '')
        pdate_Start = request.GET.get('pdate_Start', '')
        pdate_End = request.GET.get('pdate_End', '')
        search_words = request.GET.get('search_words', '')

        searchList = {'shopname__icontains': shopname,
                      'advertising_campaign_name__icontains': advertising_campaign_name,
                      'advertising_group_name__icontains': advertising_group_name,
                      'keyword__icontains': keyword,
                      'search_words__icontains': search_words,
                      'start_date__gte': pdate_Start,
                      'end_date__lt': pdate_End,
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
