# -*- coding: utf-8 -*-
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
import math
import logging
from django.contrib import messages
from django.utils.safestring import mark_safe
from Project.settings import *
from .t_product_Admin import *
import logging
from django.contrib import messages
from django.db.models import Count
from datetime import datetime
from skuapp.table.t_store_execution_aliexpress import t_store_execution_aliexpress


class t_store_execution_aliexpressAdmin(object):
    downloadxls = True

    list_display = (
    'id', 'createtime', 'shopname', 'createman', 'MainSKU', 'productid', 'money', 'count', 'remark', 'reason',
    'ordernum', 'tracenum', 'sd_time','sd_man','jd_man', 'yx_fee', 'route_name', 'ip', 'buyer_account',
    'pay_account', 'pj_time_man',)
    list_filter = (
    'shopname', 'productid', 'MainSKU', 'money', 'count', 'remark', 'reason', 'createman', 'createtime', 'ordernum',
    'tracenum', 'sd_time','sd_man', 'jd_man', 'yx_fee', 'route_name', 'ip', 'buyer_account', 'pay_account', 'pj_time_man')
    actions = ['to_excel']
    list_editable = ('createtime', 'shopname', 'createman', 'MainSKU', 'productid', 'money', 'count', 'remark', 'reason',
    'ordernum', 'tracenum', 'sd_time','sd_man','jd_man', 'yx_fee', 'route_name', 'ip', 'buyer_account',
    'pay_account', 'pj_time_man',)
    fields = (
    'shopname', 'productid', 'MainSKU', 'money', 'count', 'remark', 'reason', 'createman', 'createtime', 'ordernum',
    'tracenum', 'sd_time','sd_man', 'jd_man', 'yx_fee', 'route_name', 'ip', 'buyer_account', 'pay_account', 'pj_time_man',)

    def show_shopname(self, obj):
        if int(obj.type_num) % 2 == 0:
            rt = '<div style="text-align:center;width:100px;height:40px;background:#CCCCCC";display:block>%s</div>' % obj.shopname
        else:
            rt = '<div style="text-align:center;width:100px;height:40px;background:#33FF00";display:block>%s</div>' % obj.shopname
        return mark_safe(rt)

    show_shopname.short_description = u'店铺名称'

    def add_seats(self, obj):
        rt = '<input type="button" value="新增同单号产品" onclick="if(confirm(\'是否新增？\')) {window.open(\'/addseats?type_num=%s \')}" target="_blank" />' % (
        obj.type_num)
        # new_obj = t_store_marketplan_execution_aliexpress()
        # new_obj.type_num = obj.type_num
        # new_obj.save()
        # id = new_obj.latest("id").id
        # request = self.request
        # post = request.POST
        # post['_redirect'] = '/Project/admin/skuapp/t_store_marketplan_execution_aliexpress/%s/update/'%id
        return mark_safe(rt)

    add_seats.short_description = u'新增同单号产品'

    def save_models(self):
        obj = self.new_obj
        obj.createtime = datetime.now()
        if obj.createman is None or obj.createman == '':
            obj.createman = self.request.user.first_name

        if obj.type_num is None or obj.type_num == '':
            try:
                type_num = t_store_execution_aliexpress.objects.latest("type_num").type_num
                type_num = type_num + 1
                obj.type_num = type_num
            except:
                obj.type_num = 1
        obj.save()

    def to_excel(self, request, queryset):
        from xlwt import *
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        # if not os.path.exists(path):
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))

        mkdir_p(path)
        os.popen('chmod 777 %s' % (path))

        w = Workbook()
        sheet = w.add_sheet('information_deal')

        sheet.write(0, 0, u'ID')
        sheet.write(0, 1, u'提交日期')
        sheet.write(0, 2, u'店铺名称')
        sheet.write(0, 3, u'提交人')
        sheet.write(0, 4, u'主SKU')
        sheet.write(0, 5, u'产品ID')
        sheet.write(0, 6, u'金额($)')
        sheet.write(0, 7, u'数量')
        sheet.write(0, 8, u'备注')
        sheet.write(0, 9, u'营销原因')
        sheet.write(0, 10, u'订单号')
        sheet.write(0, 11, u'跟踪号')
        sheet.write(0, 12, u'刷单日期')
        sheet.write(0, 13, u'刷单人')
        sheet.write(0, 14, u'截单人')
        sheet.write(0, 15, u'营销费用(美金)')
        sheet.write(0, 16, u'线路名称')
        sheet.write(0, 17, u'ip地址')
        sheet.write(0, 18, u'买家账号')
        sheet.write(0, 19, u'支付卡账号')
        sheet.write(0, 20, u'评价日期/评价人')

        logger = logging.getLogger('sourceDns.webdns.views')
        # 写数据
        row = 0
        for qs in queryset:
            row = row + 1
            column = 0
            sheet.write(row, column, qs.id)

            column = column + 1
            try:
                t1 = qs.createtime.strftime('%Y-%m-%d %H:%M:%S')
            except:
                t1 = ''
            sheet.write(row, column,t1)

            column = column + 1
            sheet.write(row, column, qs.shopname)

            column = column + 1
            sheet.write(row, column, qs.createman)

            column = column + 1
            sheet.write(row, column, qs.MainSKU)

            column = column + 1
            sheet.write(row, column, qs.productid)

            column = column + 1
            sheet.write(row, column, qs.money)

            column = column + 1
            sheet.write(row, column, qs.count)

            column = column + 1
            sheet.write(row, column, qs.remark)

            column = column + 1
            sheet.write(row, column, qs.reason)

            column = column + 1
            sheet.write(row, column, qs.ordernum)

            column = column + 1
            sheet.write(row, column, qs.tracenum)

            column = column + 1
            try:
                t2 = qs.sd_time.strftime('%Y-%m-%d')
            except:
                t2 = ''
            sheet.write(row, column, t2)
            
            column = column + 1
            sheet.write(row, column, qs.sd_man)

            column = column + 1
            sheet.write(row, column, qs.jd_man)

            column = column + 1
            sheet.write(row, column, qs.yx_fee)

            column = column + 1
            sheet.write(row, column, qs.route_name)

            column = column + 1
            sheet.write(row, column, qs.ip)

            column = column + 1
            sheet.write(row, column, qs.buyer_account)

            column = column + 1
            sheet.write(row, column, qs.pay_account)

            column = column + 1
            sheet.write(row, column, qs.pj_time_man)

        filename = request.user.username + '_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.xls'
        w.save(path + '/' + filename)
        os.popen(r'chmod 777 %s' % (path + '/' + filename))
        # queryset.update(DealStatus=Dealstatus_obj[0].V,DealStaffID=request.user.username,DealTime=datetime.now())

        # 上传oss对象
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT, BUCKETNAME_XLS)
        bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)
        # 删除现有的
        for object_info in oss2.ObjectIterator(bucket,
                                               prefix='%s/%s_' % (request.user.username, request.user.username)):
            bucket.delete_object(object_info.key)
        bucket.put_object(u'%s/%s' % (request.user.username, filename), open(path + '/' + filename))

        messages.error(request, u'%s%s.%s/%s/%s' % (
        PREFIX, BUCKETNAME_XLS, ENDPOINT_OUT, request.user.username, filename) + u':成功导出,可点击Download下载到本地~~~~~~')

    to_excel.short_description = u'导出Excel'





