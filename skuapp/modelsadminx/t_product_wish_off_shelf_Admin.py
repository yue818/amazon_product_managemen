# coding=utf-8

from datetime import datetime
from django.contrib import messages
import re

class t_product_wish_off_shelf_Admin(object):

    search_box_flag = True

    list_display = ('id', 'ProductSKU', 'ShopSKU', 'ShopName', 'Reason', 'CreateStaff', 'CreateTime',
                    'Result', 'ErrorInfo', 'ExcelFile')

    list_display_links = ('id',)

    fields = ('Reason', 'ExcelFile',)

    def save_models(self):
        obj = self.new_obj
        request = self.request
        file_obj = request.FILES.get('ExcelFile')
        now_time = datetime.now()
        first_name = request.user.first_name

        if obj.Reason is None or obj.Reason.strip() == '':
            messages.error(request, '操作原因不能为空，请重新导入！！！')
        else:
            from app_djcelery.tasks import wish_product_off_shelf_task
            wish_product_off_shelf_task.delay(file_obj, now_time, first_name, obj.Reason)
            messages.info(request, '表格正在处理中，请稍后刷新以查看结果…………')

    def get_list_queryset(self):
        request = self.request
        qs = super(t_product_wish_off_shelf_Admin, self).get_list_queryset()

        Reason = request.GET.get('Reason', '')
        CreateTimeStart = request.GET.get('CreateTimeStart', '')
        CreateTimeEnd = request.GET.get('CreateTimeEnd', '')
        ProductSKU = request.GET.get('ProductSKU', '')
        ShopName = request.GET.get('ShopName', '')
        CreateStaff = request.GET.get('CreateStaff', '')
        Result = request.GET.get('Result', '')
        ShopSKU =re.split('[,，]',request.GET.get('ShopSKU','').encode('utf-8'))

        searchList = {'Reason__exact': Reason, 'CreateTime__gte': CreateTimeStart,
                      'CreateTime__lt': CreateTimeEnd, 'ProductSKU__exact': ProductSKU,
                      'ShopName__exact':ShopName, 'CreateStaff__exact':CreateStaff,'Result__exact':Result,
                      'ShopSKU__in':ShopSKU}

        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                v=[_.strip() for _ in v if _.strip()]
                if v :
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

