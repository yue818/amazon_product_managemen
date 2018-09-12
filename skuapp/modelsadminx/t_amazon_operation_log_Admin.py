# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_operation_log_Admin.py
 @time: 2018/9/12 14:27
"""  
from django.utils.safestring import mark_safe
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


class t_amazon_operation_log_Admin(object):
    amazon_site_left_menu_tree_flag = True
    search_box_flag = True
    downloadxls = True

    def show_deal_result(self, obj):
        if obj.deal_result == -1:
            deal_result_txt = '失败'
        elif obj.deal_result == 0:
            deal_result_txt = '执行中'
        elif obj.deal_result == 1:
            deal_result_txt = '成功'
        return mark_safe(deal_result_txt)
    show_deal_result.short_description = mark_safe('<p style="color:#428BCA" align="center">操作结果</p>')

    list_display = ('batch_id', 'shop_name', 'seller_sku', 'price_before','price_after','deal_user', 'begin_time', 'end_time', 'show_deal_result','deal_result_info')

    actions = ['to_excel']

    def to_excel(self, request, queryset):
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))
        mkdir_p(path)
        os.popen('chmod 777 %s' % path)

        w = Workbook()
        sheet = w.add_sheet('price_modify')
        sheet.write(0, 0, u'操作批次号')
        sheet.write(0, 1, u'店铺')
        sheet.write(0, 2, u'店铺SKU')
        sheet.write(0, 3, u'调整前价格')
        sheet.write(0, 4, u'调整后价格')
        sheet.write(0, 5, u'操作人')
        sheet.write(0, 6, u'操作开始时间')
        sheet.write(0, 7, u'操作结束时间')
        sheet.write(0, 8, u'操作结果')
        sheet.write(0, 9, u'结果详情')

        # 写数据
        row = 0
        for qs in queryset:
            row = row + 1
            begin_time = qs.begin_time.strftime('%Y-%m-%d %H:%M')
            if qs.end_time:
                end_time = qs.end_time.strftime('%Y-%m-%d %H:%M')
            if qs.deal_result == -1:
                deal_result = u'失败'
            elif qs.deal_result == 0:
                deal_result = u'执行中'
            elif qs.deal_result == 1:
                deal_result = u'成功'
            excel_content_list = [qs.batch_id, qs.shop_name, qs.seller_sku, qs.price_before, qs.price_after, qs.deal_user, begin_time, end_time, deal_result, qs.deal_result_info]
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
        batch_id = request.GET.get('batch_id', '')
        seller_sku = request.GET.get('seller_sku', '')
        seller_sku = '' if seller_sku == '' else seller_sku.strip().replace(' ', '+').split(',')
        deal_user = request.GET.get('deal_user', '')
        begin_time_start = request.GET.get('begin_time_start', '')
        begin_time_end = request.GET.get('begin_time_end', '')
        deal_result = request.GET.get('deal_result', '')


        qs = super(t_amazon_operation_log_Admin, self).get_list_queryset()

        search_list = {
                      'shop_name__icontains': shop_name,
                      'batch_id__exact': batch_id,
                      'seller_sku__in':seller_sku,
                      'deal_user__icontains': deal_user,
                      'begin_time__gte': begin_time_start,
                      'begin_time__lte': begin_time_end,
                      'deal_result__exact': deal_result,
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
