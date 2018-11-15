# coding=utf-8

from django.contrib import messages
from Project.settings import MEDIA_ROOT, ACCESS_KEY_ID, ACCESS_KEY_SECRET, ENDPOINT, BUCKETNAME_XLS, PREFIX, ENDPOINT_OUT
import oss2, os
from datetime import datetime
from skuapp.modelsadminx.t_product_Admin import mkdir_p
from skuapp.table.t_online_info import t_online_info


class b_goods_sku_status_change_Admin(object):
    search_box_flag = True
    downloadxls = True

    list_display = ('id', 'SKU', 'LastGoodsStatus', 'NowGoodsStatus', 'ChangeStatusTime')
    list_display_links = ('',)
    actions = ['to_excel_on', 'to_excel_off', 'sign_already_operate']


    def sign_already_operate(self, request, queryset):
        username_cn = request.user.first_name
        for query in queryset:
            sign_time = datetime.now()
            query.DisplayFlag = 0
            query.LastOperator = username_cn
            query.LastOperateTime = sign_time
            query.save()
    sign_already_operate.short_description = u'标记为忽略'


    def to_excel_on(self, request, queryset):
        username_en = request.user.username
        username_cn = request.user.first_name
        already_operate_list = []
        need_operate_list = []
        for query in queryset:
            if query.OperationFlag == 0:
                need_operate_list.append(query.SKU)
                export_time = datetime.now()
                query.OperationFlag = 1
                query.LastOperator = username_cn
                query.LastOperateTime = export_time
                query.save()
            else:
                already_operate_list.append(str(int(query.id)))
        if need_operate_list:
            out_url = self.excel_operate(need_operate_list, username_en, 'Disabled')
            messages.error(request, out_url + u':成功导出,可点击Download下载到本地')
        if already_operate_list:
            messages.error(request, u'编号：%s 已经处理过！！！' % ','.join(already_operate_list))
    to_excel_on.short_description = u'导出去上架'


    def to_excel_off(self, request, queryset):
        username_en = request.user.username
        username_cn = request.user.first_name
        already_operate_list = []
        need_operate_list = []
        for query in queryset:
            if query.OperationFlag == 0:
                need_operate_list.append(query.SKU)
                export_time = datetime.now()
                query.OperationFlag = 1
                query.LastOperator = username_cn
                query.LastOperateTime = export_time
                query.save()
            else:
                already_operate_list.append(str(int(query.id)))
        if need_operate_list:
            out_url = self.excel_operate(need_operate_list, username_en, 'Enabled')
            messages.error(request, out_url + u':成功导出,可点击Download下载到本地')
        if already_operate_list:
            messages.error(request, u'编号：%s 已经处理过！！！' % ','.join(already_operate_list))
    to_excel_off.short_description = u'导出去下架'


    def excel_operate(self, need_operate_list, username_en, status):
        from xlwt import *
        path = MEDIA_ROOT + 'download_xls/' + username_en
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))
        mkdir_p(path)
        os.popen('chmod 777 %s' % (path))

        w = Workbook()
        sheet = w.add_sheet('shelf')

        # 写数据
        row = -1
        for sku in need_operate_list:
            online_info_objs = t_online_info.objects.filter(SKU=sku, Status=status)
            if online_info_objs:
                for online_info_obj in online_info_objs:
                    row = row + 1
                    column = 0
                    sheet.write(row, column, online_info_obj.ShopSKU)

                    column = column + 1
                    sheet.write(row, column, online_info_obj.ShopName)

        if status == 'Enabled':
            ss = 'Disabled'
        else:
            ss = 'Enabled'
        filename = username_en + '_' + datetime.now().strftime('%Y%m%d%H%M%S') + '_' + ss + '.xls'
        w.save(path + '/' + filename)
        os.popen(r'chmod 777 %s' % (path + '/' + filename))

        # 上传oss对象
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT, BUCKETNAME_XLS)
        bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)
        # 删除现有的
        for object_info in oss2.ObjectIterator(bucket, prefix='%s/%s_' % (username_en, username_en)):
            bucket.delete_object(object_info.key)
        bucket.put_object(u'%s/%s' % (username_en, filename), open(path + '/' + filename))
        out_url = u'%s%s.%s/%s/%s' % (PREFIX, BUCKETNAME_XLS, ENDPOINT_OUT, username_en, filename)
        return out_url


    def get_list_queryset(self, ):
        qs = super(b_goods_sku_status_change_Admin, self).get_list_queryset()
        qs = qs.filter(OperationFlag=0, DisplayFlag=1)

        sku = self.request.GET.get('SKU', '')
        time_start = self.request.GET.get('time_start', '')
        time_end = self.request.GET.get('time_end', '')

        searchList = {'SKU__exact': sku, 'ChangeStatusTime__gte': time_start, 'ChangeStatusTime__lt': time_end}
        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    if k == 'ShopName__exact':
                        if v.find('Wish-') == -1:
                            v = 'Wish-' + v.zfill(4)
                    sl[k] = v
        if sl:
            qs = qs.filter(**sl)
        return qs

