# -*- coding: utf-8 -*-

import oss2, os
from datetime import datetime
from xlwt import *
from django.contrib import messages
from django.utils.safestring import mark_safe
from Project.settings import MEDIA_ROOT, ACCESS_KEY_ID,ACCESS_KEY_SECRET, ENDPOINT, BUCKETNAME_XLS, PREFIX, ENDPOINT_OUT
from skuapp.modelsadminx.t_product_Admin import mkdir_p
from skuapp.table.t_store_configuration_file import t_store_configuration_file


class t_upload_shopname_Admin(object):
    downloadxls = True

    def show_chart(self, obj):
        rt = u"<a id=refund_%s>订单数趋势图</a><script>$('#refund_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan'," \
             u"title:'查看全部',fix:false,shadeClose: true,maxmin:true,area:['1600px','600px']," \
             u"content:'/t_upload_shopname_chart/?id=%s&type=order',});});</script>" % (obj.id, obj.id, obj.id)
        rt = u"%s<br><br><a id=rating_%s>销售额趋势图</a><script>$('#rating_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan'," \
             u"title:'查看全部',fix:false,shadeClose: true,maxmin:true,area:['1600px','600px']," \
             u"content:'/t_upload_shopname_chart/?id=%s&type=sales',});});</script>" % (rt, obj.id, obj.id, obj.id)
        return mark_safe(rt)
    show_chart.short_description = u'<span style="color: #428bca">操作<span>'


    def show_status(self, obj):
        rt = u'未知'
        store_config_objs = t_store_configuration_file.objects.filter(ShopName_temp=obj.ShopName)
        if store_config_objs.exists():
            store_staus = store_config_objs[0].Status
            rt = u'正常' if store_staus == '0' else u'异常'
        return mark_safe(rt)
    show_status.short_description = u'<span style="color: #428bca">店铺状态<span>'

    list_display = ('id', 'ShopName', 'show_status', 'uploader', 'IsAvailable', 'LastOrderNumber', 'LastSalesVolume', 'show_chart', 'UpdateTime')
    list_filter = ('ShopName', 'uploader', 'IsAvailable')
    search_fields = ('id', 'ShopName', 'uploader', 'IsAvailable')
    fields = ('ShopName', 'uploader', 'IsAvailable')
    actions = ['mark_available', 'mark_unavailable', 'excel_shopname']


    def mark_available(self, request, queryset):
        queryset.update(IsAvailable=1)
    mark_available.short_description = u'标记为可铺货'


    def mark_unavailable(self, request, queryset):
        queryset.update(IsAvailable=0)
    mark_unavailable.short_description = u'标记为不可铺货'


    def excel_shopname(self, request, queryset):
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))
        mkdir_p(path)
        os.popen('chmod 777 %s' % (path))

        w = Workbook()
        sheet = w.add_sheet(u'铺货店铺')
        sheet.write(0, 0, u'店铺名称')

        row = 0
        column = 0
        for qs in queryset:
            row = row + 1
            sheet.write(row, column, qs.ShopName)

        filename = request.user.username + '_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.xls'
        w.save(path + '/' + filename)
        os.popen(r'chmod 777 %s' % (path + '/' + filename))

        # 上传oss对象
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT, BUCKETNAME_XLS)
        bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)
        # 删除现有的
        for object_info in oss2.ObjectIterator(bucket,prefix='%s/%s_' % (request.user.username, request.user.username)):
            bucket.delete_object(object_info.key)
        bucket.put_object(u'%s/%s' % (request.user.username, filename), open(path + '/' + filename))
        messages.error(request, u'%s%s.%s/%s/%s' % (PREFIX, BUCKETNAME_XLS, ENDPOINT_OUT, request.user.username,filename) + u':成功导出,可点击Download下载到本地............................。')

    excel_shopname.short_description = u'导出店铺'