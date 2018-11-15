# -*- coding: utf-8 -*-

from django.utils.safestring import mark_safe

class t_report_sales_daily_Admin(object):

    sales_show_bytype_flag = True
    search_box_flag = True
    salesshowlisting_flag = True
  
    def show_pic(self, obj):
        try:
            rt = '<img src="%s"  width="120" height="120"  alt = "%s"  title="%s" />' % (obj.BmpUrl, obj.BmpUrl, u'商品图片') #alt 属性是一个必需的属性，它规定在图像无法显示时的替代文本 
        except:
            rt = ''
        return mark_safe(rt)
    show_pic.short_description = u'图片'
    
    list_display = (
        'OrderDay', 'PlatformName', 'ProductID', 'show_pic', 'MainSKU', 'ShopName', 'SKU', 'ShopSKU',
         'SalesVolume',)
    list_editable = None
    list_filter = None #过滤器list_filter
    search_fields = None #搜索功能
    readonly_fields = None #只读属性对象
    list_per_page = 50  #页面显示数量


    def get_list_queryset(self):
        request = self.request
        qs = super(t_report_sales_daily_Admin, self).get_list_queryset()

        ShopName1 = request.GET.get('ShopName1', '')
        ShopSKU = request.GET.get('ShopSKU', '')

        searchList = {'ShopName__exact': ShopName1, 'ShopSKU__exact': ShopSKU,}
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