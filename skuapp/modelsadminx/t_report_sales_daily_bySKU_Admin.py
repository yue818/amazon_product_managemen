# -*- coding: utf-8 -*-

class t_report_sales_daily_bySKU_Admin(object):

    salesshowlisting_flag = True

    sales_show_bytype_flag = True
    search_box_flag = True

    list_display = (
        'OrderDay', 'SKU', 'SalesVolume',)
    list_editable = None
    list_filter = None  # 过滤器list_filter
    search_fields = None  # 搜索功能
    readonly_fields = None  # 只读属性对象
    list_per_page = 50  # 页面显示数量

    def get_list_queryset(self):
        request = self.request
        qs = super(t_report_sales_daily_bySKU_Admin, self).get_list_queryset()

        SKU = request.GET.get('SKU', '')

        searchList = {
                      'SKU__exact': SKU,
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
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                from django.contrib import messages
                messages.error(request, u'输入的查询数据有问题！')

        return qs