# coding=utf-8


from skuapp.table.t_distribution_product_to_store_result import t_distribution_product_to_store_result as store_result
from t_product_Admin import *



class t_distribution_product_to_store_result_Admin(object):
    downloadxls = True
    search_box_flag = True
    list_display = ('id', 'PlatformName', 'PID', 'SKU', 'ShopName','ParentSKU', 'Submitter', 'SubTime','ScheduleTime', 'Type','Status','ErrorMessage')
    search_fields = ('PlatformName', 'PID', 'SKU', 'ShopName', 'Submitter','Type', 'Status','ParentSKU')
    list_filter = ('PlatformName', 'PID', 'SKU', 'ShopName', 'Submitter', 'SubTime','ScheduleTime',  'Status','ParentSKU','Type')

    actions = ['to_excel',]

    def to_excel(self,request,queryset):
        from xlwt import *
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))

        mkdir_p(path)
        os.popen('chmod 777 %s' % (path))

        w = Workbook()
        sheet = w.add_sheet('store')
        sheet.write(0, 0, u'铺货ID')
        sheet.write(0, 1, u'提交人')
        sheet.write(0, 2, u'提交时间')
        sheet.write(0, 3, u'平台名称')
        sheet.write(0, 4, u'SKU')
        sheet.write(0, 5, u'铺货店铺')
        sheet.write(0, 6, u'铺货状态')
        sheet.write(0, 7, u'铺货类型')

        # 写数据
        row = 0

        for qs in queryset:
            row = row + 1
            column = 0
            sheet.write(row, column, qs.PID)

            column = column + 1
            sheet.write(row, column, qs.Submitter)

            column = column + 1
            sheet.write(row, column, qs.SubTime)

            column = column + 1
            sheet.write(row, column, qs.PlatformName)

            column = column + 1
            sheet.write(row, column, qs.SKU)

            column = column + 1
            sheet.write(row, column, qs.ShopName)

            column = column + 1
            sheet.write(row, column, qs.Status)

            column = column + 1
            sheet.write(row, column, qs.Type)


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

        messages.error(request, u'%s%s.%s/%s/%s' % (PREFIX, BUCKETNAME_XLS, ENDPOINT_OUT, request.user.username,
                                                    filename) + u':成功导出,可点击Download下载到本地............................。')
    to_excel.short_description = u'导出EXCEL'




    def get_list_queryset (self,):
        request = self.request
        qs = super(t_distribution_product_to_store_result_Admin,self).get_list_queryset()
        PID = request.GET.get('PID','')
        SKU = request.GET.get('SKU','')
        ShopName = request.GET.get('ShopName', '')
        Submitter = request.GET.get('Submitter','')
        Type = request.GET.get('Type', '')
        SubStatus = request.GET.get('SubStatus','')
        #messages.error(request,'---------%s'%  SubStatus)
        ParentSKU = request.GET.get('ParentSKU','')
        SubTimeStart = request.GET.get('SubTimeStart', '')
        SubTimeEnd = request.GET.get('SubTimeEnd', '')
        ScheduleTimeStart = request.GET.get('ScheduleTimeStart', '')
        ScheduleTimeEnd = request.GET.get('ScheduleTimeEnd', '')



        searchList = {'SKU__exact':SKU,'PID__exact':PID,'ParentSKU__exact':ParentSKU,'ShopName__exact':ShopName,'Submitter__exact':Submitter,
                      'Status__exact':SubStatus,'Type__exact':Type, 'SubTime__gte': SubTimeStart, 'SubTime__lte': SubTimeEnd, 'ScheduleTime__gte': ScheduleTimeStart, 'ScheduleTime__lte': ScheduleTimeEnd,
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
                        # messages.error(request, v)
                    sl[k] = v
        if sl is not None:
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
                return qs
            except Exception, ex:
                messages.error(request, u'输入的查询数据有问题！')
                return qs