#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: t_report_sales_clothingsystem_Admin.py.py
 @time: 2018-04-09 9:58
"""
from django.utils.safestring import mark_safe
from Project.settings import *
from datetime import datetime
import oss2, errno, os
from django.contrib import messages

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5 (except OSError, exc: for Python <2.5)
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

class t_report_sales_clothingsystem_Admin(object):
    sales_clothingsystem_chart = True
    search_box_flag = True
    downloadxls = True

    def show_pic(self, obj):
        try:
            rt = '<img src="%s"  width="120" height="120"  alt = "%s"  title="%s" />' % (obj.BmpUrl, obj.BmpUrl, u'商品图片')
        except:
            rt = ''
        return mark_safe(rt)
    show_pic.short_description = u'图片'

    list_display = ('TimeName', 'PlatformName', 'ProductID', 'MainSKU', 'ShopName', 'show_pic', 'SalesVolume')

    list_display_links = ('ID')

    list_per_page = 50

    actions = ['to_excel', ]

    def to_excel(self, request, queryset):
        from xlwt import *
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))
        mkdir_p(path)
        os.popen('chmod 777 %s' % (path))

        w = Workbook()
        timetypecha = {'month': u'销售月份', 'week': u'销售周别', 'day': u'销售日期'}
        timetype = request.GET.get('cate', 'day')

        sheet = w.add_sheet(u'服装体系销售数据')

        sheet.write(0, 0, timetypecha[timetype])
        sheet.write(0, 1, u'销售平台')
        sheet.write(0, 2, u'产品ID')
        sheet.write(0, 3, u'主SKU')
        sheet.write(0, 4, u'店铺名称')
        sheet.write(0, 5, u'销售量')

        # 写数据
        row = 0
        for qs in queryset:
            row = row + 1
            column = 0
            sheet.write(row, column, qs.TimeName)  # 销售日期

            column = column + 1
            sheet.write(row, column, qs.PlatformName)

            column = column + 1
            sheet.write(row, column, qs.ProductID)

            column = column + 1
            sheet.write(row, column, qs.MainSKU)

            column = column + 1
            sheet.write(row, column, qs.ShopName)

            column = column + 1
            sheet.write(row, column, qs.SalesVolume)

        filename = request.user.username + '_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.xls'
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

        messages.success(request, u'%s%s.%s/%s/%s' % (PREFIX, BUCKETNAME_XLS, ENDPOINT_OUT, request.user.username,
                                                      filename) + u':成功导出,可点击Download下载到本地............................。')

    to_excel.short_description = u'导出EXCEL'

    def _get_timename(self, tt, cate):
        format = {'day': '%Y-%m-%d', 'week': '%Y-%W', 'month': '%Y-%m'}
        t1 = tt.split('-')
        tt = datetime(year=int(t1[0]), month=int(t1[1]), day=int(t1[2]))

        return tt.strftime(format[cate])

    def get_list_queryset(self):
        request = self.request
        qs = super(t_report_sales_clothingsystem_Admin, self).get_list_queryset()

        searchList = {}
        timetypecha= {'month': 3, 'week': 2, 'day': 1}
        timetype     = request.GET.get('cate', 'day')
        searchList['TimeType__exact'] = timetypecha[timetype]
        PlatformName = request.GET.get('PlatformName', '')
        if PlatformName != '':
            searchList['PlatformName__exact'] = PlatformName
        MainSKU      = request.GET.get('MainSKU', '')
        if MainSKU != '':
            searchList['MainSKU__exact'] = MainSKU
        ShopName     = request.GET.get('ShopName', '')
        if ShopName != '':
            searchList['ShopName__icontains'] = ShopName
        ProductID    = request.GET.get('ProductID', '')
        if ProductID != '':
            searchList['ProductID__exact'] = ProductID
        TimeNameStart= request.GET.get('TimeNameStart', '')
        if TimeNameStart != '':
            searchList['TimeName__gte'] = self._get_timename(TimeNameStart, timetype)
        TimeNameEnd  = request.GET.get('TimeNameEnd', '')
        if TimeNameEnd != '':
            searchList['TimeName__lte'] = self._get_timename(TimeNameEnd, timetype)

        try:
            qs = qs.filter(**searchList)
        except Exception, ex:
            from django.contrib import messages
            messages.error(request, u'输入的查询数据有问题！')

        return qs