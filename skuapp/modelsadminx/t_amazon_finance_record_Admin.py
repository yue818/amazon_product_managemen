# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site:
 @software: PyCharm
 @file: t_amazon_finance_record_Admin.py
 @time: 2018/11/19 9:43
"""
from django.contrib import messages
from Project.settings import *
from xlwt import *
import errno
import datetime
import oss2


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5 (except OSError, exc: for Python <2.5)
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


class t_amazon_finance_record_Admin(object):
    amazon_site_left_menu_tree_flag = True
    search_box_flag = True
    downloadxls = True
    list_display = ('shop_name', 'seller_sku', 'amazon_order_id', 'finance_type', 'order_adjustment_item_id', 'order_item_id', 'fee_type', 'fee_currency','fee_amount','quantity_shipped')
    list_display_links = ('',)
    actions = ['to_excel']

    def to_excel(self, request, queryset):
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))
        mkdir_p(path)
        os.popen('chmod 777 %s' % path)

        w = Workbook()
        sheet = w.add_sheet('amazon_finance')
        sheet.write(0, 0, u'店铺')
        sheet.write(0, 1, u'店铺SKU')
        sheet.write(0, 2, u'发布时间')
        sheet.write(0, 3, u'订单编号')
        sheet.write(0, 4, u'交易类型')
        sheet.write(0, 5, u'商城名称')
        sheet.write(0, 6, u'数量')
        sheet.write(0, 7, u'盘点商品编号')
        sheet.write(0, 8, u'订单商品编号')
        sheet.write(0, 9, u'费用类型')
        sheet.write(0, 10, u'费用货币')
        sheet.write(0, 11, u'费用金额')

        # 写数据
        row = 0
        for qs in queryset:
            row = row + 1
            posted_date = qs.posted_date.strftime('%Y-%m-%d %H:%M')

            excel_content_list = (qs.shop_name, qs.seller_sku, posted_date, qs.amazon_order_id, qs.finance_type, qs.marketplace_name, qs.quantity_shipped, qs.order_adjustment_item_id, qs.order_item_id, qs.fee_type, qs.fee_currency, qs.fee_amount,)
            column = 0
            for content in excel_content_list:
                sheet.write(row, column, content)
                column += 1
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

    def get_list_queryset(self, ):
        request = self.request
        shop_name = request.GET.get('shop_name', '')
        seller_sku = request.GET.get('seller_sku', '')
        seller_sku = '' if seller_sku == '' else seller_sku.strip().replace(' ', '+').split(',')
        amazon_order_id = request.GET.get('amazon_order_id', '')
        amazon_order_id = '' if amazon_order_id == '' else amazon_order_id.strip().split(',')
        order_item_id = request.GET.get('order_item_id', '')
        order_item_id = '' if order_item_id == '' else order_item_id.strip().split(',')
        posted_date_start = request.GET.get('posted_date_start', '')
        posted_date_end = request.GET.get('posted_date_end', '')
        finance_type = request.GET.get('finance_type', '')

        qs = super(t_amazon_finance_record_Admin, self).get_list_queryset()

        search_list = {
                      'shop_name__icontains':  shop_name,
                      'seller_sku__in': seller_sku,
                      'amazon_order_id__in': amazon_order_id,
                      'order_item_id__in': order_item_id,
                      'posted_date__gte': posted_date_start,
                      'posted_date__lte': posted_date_end,
                      'finance_type__exact': finance_type,
                      }
        sl = {}
        for k, v in search_list.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and str(v).strip() != '':
                    sl[k] = v
        if sl is not None:
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'Please enter the correct content!')
        return qs
