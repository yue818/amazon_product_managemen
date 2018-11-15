# coding=utf-8


from skuapp.table.t_order_out_of_stock import t_order_out_of_stock
from django.contrib import messages
from Project.settings import MEDIA_ROOT, ACCESS_KEY_ID, ACCESS_KEY_SECRET, ENDPOINT, BUCKETNAME_XLS, PREFIX, ENDPOINT_OUT
import oss2, os
from datetime import datetime
from skuapp.modelsadminx.t_product_Admin import mkdir_p
from django.utils.safestring import mark_safe


class t_order_out_of_stock_Admin(object):
    search_box_flag = True
    downloadxls = True


    def show_details(self, obj):

        detail_list = obj.Details.split(';')
        if detail_list[-1] == ';':
            detail_list.pop()
        i = 0
        for detail in detail_list:
            if i == 0:
                rr = '%s;' % detail
            elif not i % 5:
                rr = '%s<br>%s;' % (rr[:-1], detail)
            else:
                rr = '%s%s;' % (rr, detail)
            i += 1
        rr = '<span>%s<span>' % rr[:-1]
        return mark_safe(rr)
    show_details.short_description = u'<span style="color: #428bca">商品明细</span>'


    list_display = ('Plateform', 'ExportDate', 'OrderId', 'DelayDays', 'Seller', 'show_details', 'TradingTime', 'ExcelFile',
                    'CreateStaff', 'CreateTime')

    list_display_links = ('id',)

    fields = ('Plateform', 'ExcelFile',)

    actions = ['delete_error', 'to_excel']


    def save_models(self):
        obj = self.new_obj
        request = self.request
        file_obj = request.FILES.get('ExcelFile')
        now_time = datetime.now()
        first_name = request.user.first_name

        if obj.Plateform is None or obj.Plateform.strip() == '':
            messages.error(request, '平台不能为空，请重新导入！！！')
        else:
            from app_djcelery.tasks import order_out_of_stock_task
            order_out_of_stock_task(file_obj, now_time, first_name, obj.Plateform)
            messages.info(request, '表格正在处理中，请稍后刷新以查看结果…………')


    def delete_error(self, request, queryset):
        wait_delete_id_list = []
        for query in queryset:
            wait_delete_id_list.append(int(query.id))
        t_order_out_of_stock.objects.filter(id__in=wait_delete_id_list).delete()
        messages.info(request, '-----删除成功！！！')
    delete_error.short_description = '删除'


    def to_excel(self,request,queryset):
        from xlwt import *
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))

        mkdir_p(path)
        os.popen('chmod 777 %s' % (path))

        w = Workbook()
        sheet = w.add_sheet('store')
        sheet.write(0, 0, u'平台')
        sheet.write(0, 1, u'导出日期')
        sheet.write(0, 2, u'订单编号')
        sheet.write(0, 3, u'延迟天数')
        sheet.write(0, 4, u'卖家简称')
        sheet.write(0, 5, u'商品明细')
        sheet.write(0, 6, u'交易时间')
        sheet.write(0, 7, u'导入人')
        sheet.write(0, 8, u'导入Online时间')

        row = 0
        for qs in queryset:
            row = row + 1
            column = 0
            sheet.write(row, column, qs.Plateform)

            column = column + 1
            sheet.write(row, column, str(qs.ExportDate))

            column = column + 1
            sheet.write(row, column, str(qs.OrderId))

            column = column + 1
            sheet.write(row, column, str(qs.DelayDays))

            column = column + 1
            sheet.write(row, column, qs.Seller)

            column = column + 1
            sheet.write(row, column, qs.Details)

            column = column + 1
            sheet.write(row, column, str(qs.TradingTime))

            column = column + 1
            sheet.write(row, column, qs.CreateStaff)

            column = column + 1
            sheet.write(row, column, str(qs.CreateTime))
        filename = request.user.username + '_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.xls'
        w.save(path + '/' + filename)
        os.popen(r'chmod 777 %s' % (path + '/' + filename))

        # 上传oss对象
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT, BUCKETNAME_XLS)
        bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)
        # 删除现有的
        for object_info in oss2.ObjectIterator(bucket, prefix='%s/%s_' % (request.user.username, request.user.username)):
            bucket.delete_object(object_info.key)
        bucket.put_object(u'%s/%s' % (request.user.username, filename), open(path + '/' + filename))
        messages.error(request, u'%s%s.%s/%s/%s' % (PREFIX, BUCKETNAME_XLS, ENDPOINT_OUT, request.user.username,filename) + u':成功导出,可点击Download下载到本地............................。')
    to_excel.short_description = u'导出EXCEL'


    def get_list_queryset(self):
        request = self.request
        qs = super(t_order_out_of_stock_Admin, self).get_list_queryset()

        plateform = request.GET.get('Plateform', '')
        create_staff = request.GET.get('CreateStaff', '')
        create_time_start = request.GET.get('CreateTimeStart', '')
        create_time_end = request.GET.get('CreateTimeEnd', '')
        export_date_start = request.GET.get('ExportDateStart', '')
        export_date_end = request.GET.get('ExportDateEnd', '')

        searchList = {
            'Plateform__exact': plateform, 'CreateStaff__exact': create_staff,
            'CreateTime__gte': create_time_start, 'CreateTime__lt': create_time_end,
            'ExportDate__gte': export_date_start, 'ExportDate__lt': export_date_end,
        }

        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    if k == 'ShopName__exact':
                        v = 'Wish-' + v.zfill(4)
                    sl[k] = v
        if sl is not None:
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'输入的查询数据有问题！')
        return qs
