# -*- coding: utf-8 -*-
from datetime import datetime as ddtime

from django.contrib import messages
from skuapp.views import show_data_by_user
from Project.settings import *
# from skuapp.admin import mkdir_p, oss2

import oss2
from xlwt import *
from .t_product_Admin import *
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field


class b_costprice_modify_Admin(object):
    downloadxls = True
    search_box_flag = True  # 搜索功能
    # costprice_modify = True

    list_display = ('NID','SKU','oriPrice','curPrice','applyMan','supplierID','modifyTime','modifyMan','remark')
    list_editable = {}
    # fields = ('SKU','oriPrice','curPrice')
    # search_fields = ['SKU','oriPrice','curPrice']

    actions = ['exportExecl']

    # 导出excel
    def exportExecl(self, request, objs):
        try:
            import xlwt
            from xlwt import *
            datastyle = xlwt.XFStyle()
            datastyle.num_format_str = 'yyyy-mm-dd hh:mm:ss'
            path = MEDIA_ROOT + 'download_xls/' + request.user.username
            # if not os.path.exists(path):
            mkdir_p(MEDIA_ROOT + 'download_xls')
            os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))

            mkdir_p(path)
            os.popen('chmod 777 %s' % (path))

            w = Workbook()
            sheet = w.add_sheet(u'价格变动表')

            sheetlist = [u'商品SKU',u'修改前价格',u'修改后的价格',u'申请人',u'供应商ID',u'修改时间',u'修改人', u'备注' ]

            for index, item in enumerate(sheetlist):
                sheet.write(0, index, item)

            # 写数据
            idlist = []
            row = 0
            for qs in objs:
                row = row + 1
                column = 0
                sheet.write(row, column, qs.SKU)  # 商品SKU
                column = column + 1
                sheet.write(row, column, qs.oriPrice)  # 修改前价格
                column = column + 1
                sheet.write(row, column, qs.curPrice)  # 修改后的价格
                column = column + 1
                sheet.write(row, column, qs.applyMan)  # 申请人
                column = column + 1
                sheet.write(row, column, qs.supplierID)  # 供应商ID
                column = column + 1
                sheet.write(row, column, qs.modifyTime)  # 修改时间
                column = column + 1
                sheet.write(row, column, qs.modifyMan)  # 修改人
                column = column + 1
                sheet.write(row, column, qs.remark)  # 备注

            filename = request.user.username + '_' + ddtime.now().strftime('%Y%m%d%H%M%S') + '.xls'
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
        except Exception, ex:
            messages.error(request, "导出错误,请联系IT解决:%s" % (str(ex)))
    exportExecl.short_description = u'选中导出数据'

    #  搜索功能
    def get_list_queryset(self):
        request = self.request
        qs = super(b_costprice_modify_Admin, self).get_list_queryset()
        searchList = {}

        SKU = request.GET.get('SKU', '')   # 商品SKU
        applyMan = request.GET.get('applyMan', '')
        supplierID = request.GET.get('supplierID', '')
        modifyBeginTime = request.GET.get('modifyTimeStart', '')
        modifyEndTime = request.GET.get('modifyTimeEnd', '')
        modifyMan = request.GET.get('modifyMan', '')

        searchList = {'SKU__exact': SKU,
                      'applyMan__exact': applyMan,
                      'supplierID__exact': supplierID,
                      'modifyTime__gte': modifyBeginTime,
                      'modifyTime__lt': modifyEndTime,
                      'modifyMan__exact': modifyMan,
                      }
        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    # if k == 'ShopName__exact':
                    #  v = 'Wish-' + v.zfill(4)
                    # messages.error(request, v)
                    sl[k] = v
        if sl is not None:
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'输入的查询数据有问题！')

        return qs