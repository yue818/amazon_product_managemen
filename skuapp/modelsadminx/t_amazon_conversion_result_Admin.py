# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_conversion_result_Admin.py
 @time: 2018/12/5 16:34
"""
from django.utils.safestring import mark_safe
from django.contrib import messages
from Project.settings import *
from xlwt import *
import errno
import datetime
import oss2
from skuapp.table.t_amazon_conversion_detail import t_amazon_conversion_detail


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5 (except OSError, exc: for Python <2.5)
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


class t_amazon_conversion_result_Admin(object):
    amazon_site_left_menu_tree_flag = True
    downloadxls = True
    amazon_product_cost_refresh_plugin = True

    def show_statistic_type(self, obj):
        if obj.conversion_type == 1:
            type_html = '商品SKU'
        elif obj.conversion_type == 2:
            type_html = '店铺'
        else:
            type_html = '销售员'
        return mark_safe(type_html)
    show_statistic_type.short_description = mark_safe('<p style="color:#428BCA" align="center">统计维度</p>' )

    def show_statistic_content(self, obj):
        if obj.conversion_type == 1:
            type_html = obj.product_sku
        elif obj.conversion_type == 2:
            type_html = obj.shop_name
        else:
            type_html = obj.seller
        return mark_safe(type_html)
    show_statistic_content.short_description = mark_safe('<p style="color:#428BCA" align="center">名称</p>' )

    list_display = ('id', 'show_statistic_type', 'show_statistic_content', 'order_cost', 'inventory_cost','conversion_rate','time_span', 'refresh_time')
    list_filter = ('conversion_type', 'shop_name', 'seller', 'product_sku')
    search_fields = ('conversion_type', 'shop_name', 'seller', 'product_sku')

    actions = ['to_excel']

    def to_excel(self, request, queryset):
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))
        mkdir_p(path)
        os.popen('chmod 777 %s' % path)

        w = Workbook()
        sheet = w.add_sheet('conversion_result')
        sheet.write(0, 0, u'统计维度')
        sheet.write(0, 1, u'名称')
        sheet.write(0, 2, u'出单成本')
        sheet.write(0, 3, u'库存成本')
        sheet.write(0, 4, u'周转率')
        sheet.write(0, 5, u'时间范围')
        sheet.write(0, 6, u'刷新时间')

        sheet_detail = w.add_sheet('conversion_detail')
        sheet_detail.write(0, 0, u'店铺')
        sheet_detail.write(0, 1, u'销售员')
        sheet_detail.write(0, 2, u'店铺SKU')
        sheet_detail.write(0, 3, u'商品SKU')
        sheet_detail.write(0, 4, u'组合SKU')
        sheet_detail.write(0, 5, u'组合SKU组合量')
        sheet_detail.write(0, 6, u'商品组合量')
        sheet_detail.write(0, 7, u'订单商品量')
        sheet_detail.write(0, 8, u'FBA库存')
        sheet_detail.write(0, 9, u'集合仓库存')
        sheet_detail.write(0, 10, u'商品成本')
        sheet_detail.write(0, 11, u'时间范围')
        sheet_detail.write(0, 12, u'刷新时间')

        # 写数据
        row = 0
        row_detail = 0
        for qs in queryset:
            row = row + 1
            if qs.conversion_type == 1:
                type_id = u'商品SKU'
                type_content =  qs.product_sku
            elif qs.conversion_type == 2:
                type_id = u'店铺'
                type_content = qs.shop_name
            else:
                type_id = u'销售员'
                type_content = qs.seller
            refresh_time = qs.refresh_time.strftime('%Y-%m-%d %H:%M')
            excel_content_list = [type_id, type_content, qs.order_cost, qs.inventory_cost, qs.conversion_rate, qs.time_span, refresh_time]
            column = 0
            for content in excel_content_list:
                sheet.write(row, column, content)
                column += 1

        sku_conversion_detail = t_amazon_conversion_detail.objects.all()
        if sku_conversion_detail.exists():
            for detail in sku_conversion_detail:
                row_detail += 1
                sheet_detail.write(row_detail, 0, detail.shop_name)
                sheet_detail.write(row_detail, 1, detail.seller)
                sheet_detail.write(row_detail, 2, detail.seller_sku)
                sheet_detail.write(row_detail, 3, detail.product_sku)
                sheet_detail.write(row_detail, 4, detail.product_sku_zh)
                sheet_detail.write(row_detail, 5, detail.product_sku_zh_multiply)
                sheet_detail.write(row_detail, 6, detail.quantity_multiply)
                sheet_detail.write(row_detail, 7, detail.order_quantity)
                sheet_detail.write(row_detail, 8, detail.afn_quantity)
                sheet_detail.write(row_detail, 9, detail.warehouse_quantity)
                sheet_detail.write(row_detail, 10, detail.product_price)
                sheet_detail.write(row_detail, 11, detail.time_span)
                sheet_detail.write(row_detail, 12, detail.refresh_time.strftime('%Y-%m-%d %H:%M'))

        filename = request.user.username + '_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.xls'
        w.save(path + '/' + filename)
        os.popen(r'chmod 777 %s' % (path + '/' + filename))

        # 上传oss对象
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT, BUCKETNAME_XLS)
        bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)
        # 删除现有的
        for object_info in oss2.ObjectIterator(bucket,
                                               prefix='%s/%s_' % (request.user.username, request.user.username)):
            bucket.delete_object(object_info.key)
        bucket.put_object(u'%s/%s' % (request.user.username, filename), open(path + '/' + filename))
        messages.success(request, u'%s%s.%s/%s/%s' % (PREFIX, BUCKETNAME_XLS, ENDPOINT_OUT, request.user.username, filename) + u':成功导出,可点击Download下载到本地............................。')

    to_excel.short_description = u'导出数据'

