# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 王芝杨
 @site: 
 @software: PyCharm
 @file: t_stocking_reject_fba_Admin.py
 @time: 2018-08-08

"""
from xadmin.layout import Fieldset, Row
import datetime as tmpDate,random
from pyapp.models import b_goods as py_b_goods,B_Supplier as py_b_Supplier
from django.contrib import messages
from django.utils.safestring import mark_safe
from datetime import datetime as ddtime
from skuapp.table.public import *
from django.db import connection as hqdb_conn
from Project.settings import *
from .t_product_Admin import *

class t_stocking_rejecting_fba_Admin(object):
    search_box_flag = True
    fba_tree_menu_flag = True
    hide_page_action = True
    downloadxls = True

    def del_None(self,col):
        rt = col
        if not col:
            rt = ''
        return rt

    def show_ProductImage(self,obj) :
        from Project.settings import BmpUrl
        # 获取图片的url
        picture_url = obj.ProductImage  # 获取图片的url
        sku = obj.ProductSKU  # 获取商品SKU
        if not picture_url:
            picture_url = BmpUrl + sku + '.jpg'

        rt = """<img src="%s"  width="120" height="120"  title="%s" onerror="this.title=''" />  """ % (picture_url, picture_url)
        return mark_safe(rt)
    show_ProductImage.short_description = mark_safe('<p align="center" style="width:120px;color:#428bca;">商品图片</p>')

    def reject_numberInfo(self,obj) :
        try:
            rt = '<table>'
            if obj.Status == 'rejecting':
                rt = u'%s<tr><th>转退单号：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_rejecting_fba\')" %s title="%s"/><span id="%s"></span></th> </tr>' \
                     u'<tr><th>转退数量：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_rejecting_fba\')" %s title="%s"/><span id="%s"></span></th></tr> '% \
                     (rt,self.del_None(obj.ReturnNumber),obj.id,'ReturnNumber','',self.del_None(obj.ReturnNumber),str(obj.id)+'_ReturnNumber',
                      self.del_None(obj.RejectNum),obj.id,'RejectNum','readonly',self.del_None(obj.RejectNum),str(obj.id)+'_RejectNum')
                rt = u'%s<tr><th>转退备注：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_rejecting_fba\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
                     (rt, self.del_None(obj.Remarks), obj.id, 'Remarks', '',self.del_None(obj.Remarks), str(obj.id) + '_Remarks')
            else:
                rt = u'%s<tr><th>转退单号：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_rejecting_fba\')" %s title="%s"/><span id="%s"></span></th> </tr>' \
                     u'<tr><th>转退数量：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_rejecting_fba\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
                     (rt, self.del_None(obj.ReturnNumber), obj.id, 'ReturnNumber', 'readonly', self.del_None(obj.ReturnNumber),
                      str(obj.id) + '_ReturnNumber',
                      self.del_None(obj.RejectNum), obj.id, 'RejectNum', 'readonly', self.del_None(obj.RejectNum),
                      str(obj.id) + '_RejectNum')
                rt = u'%s<tr><th>转退备注：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_rejecting_fba\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
                     (rt, self.del_None(obj.Remarks), obj.id, 'Remarks', 'readonly', self.del_None(obj.Remarks),
                      str(obj.id) + '_Remarks')
            rt = rt + '</table>'
        except Exception, ex:
            messages.info(self.request,"转退信息加载错误,请联系IT解决:%s"%(str(ex)))
            rt = ""
        return mark_safe(rt)
    reject_numberInfo.short_description = u'转退信息填写'


    list_display = ('PurchaseOrderNum','RejectNumber','RejectDate','RejectMan','ProductSKU','ProductName','show_ProductImage','reject_numberInfo','RejectStatus')

    fields = ()
    list_editable = ()

    actions = ['tran_return','back_return','genExecl']

    def tran_return(self,request,objs):
        for obj in objs:
            if obj.Status == "rejecting" and obj.RejectStatus=='return':
                obj.RejectStatus = 'turn'
                obj.save()
    tran_return.short_description = u'转仓处理'


    def back_return(self,request,objs):
        for obj in objs:
            if obj.Status == "rejecting":
                obj.Status = 'reject'
                obj.save()
    back_return.short_description = u'驳回'

    def genExecl(self,request,objs):
        try:
            from xlwt import *
            path = MEDIA_ROOT + 'download_xls/' + request.user.username
            # if not os.path.exists(path):
            mkdir_p(MEDIA_ROOT + 'download_xls')
            os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))

            mkdir_p(path)
            os.popen('chmod 777 %s' % (path))

            #datastyle = xlwt.XFStyle()
            #datastyle.num_format_str = 'yyyy-mm-dd'
            w = Workbook()
            sheet = w.add_sheet(u'转退数据')
            sheetlist = [u'退货计划号',u'退货人',u'商品SKU', u'商品名称', u'采购订单号', u'退货数量', u'转退标志', u'转仓和退货单号',u'备注' ]

            for index, item in enumerate(sheetlist):
                sheet.write(0, index, item)
            row = 0
            for obj in objs:
                row = row + 1
                column = 0
                sheet.write(row, column, obj.RejectNumber)  # 退货计划号

                column = column + 1
                sheet.write(row, column, '%s'%obj.RejectMan)  # 退货人

                column = column + 1
                sheet.write(row, column, obj.ProductSKU)  # 商品SKU

                column = column + 1
                sheet.write(row, column, obj.ProductName)  # 商品名称

                column = column + 1
                sheet.write(row, column, obj.PurchaseOrderNum)  # 采购订单号

                column = column + 1
                sheet.write(row, column, obj.RejectNum)  # 退货数量

                column = column + 1
                if obj.RejectStatus == 'turn':
                    sheet.write(row, column, u'转仓')  # 转退标志
                else:
                    sheet.write(row, column, u'退货')

                column = column + 1
                sheet.write(row, column, obj.ReturnNumber)  # 转仓和退货单号

                column = column + 1
                sheet.write(row, column, '%s'%obj.Remarks)  # 备注

            filename = request.user.username + '_' + ddtime.now().strftime('%Y%m%d%H%M%S') + '.xls'
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
            messages.error(request, u'%s%s.%s/%s/%s' % (PREFIX, BUCKETNAME_XLS, ENDPOINT_OUT, request.user.username,
                                                        filename) + u':成功导出,可点击Download下载到本地............................。')
        except Exception, ex:
            messages.info(self.request, "导出execl错误,请联系IT解决:%s" % (str(ex)))
    genExecl.short_description = u'导出execl'

    def save_models(self,):
        try:
            pass
        except Exception, ex:
            messages.info(self.request,"保存报错:%s"%(str(ex)))

    def get_list_queryset(self):
        request = self.request
        
        qs = super(t_stocking_rejecting_fba_Admin, self).get_list_queryset()
        from django.contrib.auth.models import User
        userID = [each.id for each in User.objects.filter(groups__id__in=[65])]
        # if request.user.is_superuser or request.user.id in userID:
        if request.user.id in userID:
            qs = qs.filter(RejectMan=request.user.first_name)
        Status = request.GET.get('Status', '')  # 采购状态
        RejectNumber = request.GET.get('RejectNumber', '')   #转退计划号
        RejectDateStart      = request.GET.get('RejectDateStart', '')     # 转退计划时间
        RejectDateEnd      = request.GET.get('RejectDateEnd', '')     # 转退计划时间
        RejectMan = request.GET.get('RejectMan', '')             # 转退申请人
        PurchaseOrderNum = request.GET.get('PurchaseOrderNum', '')            #采购单号
        ProductSKU = request.GET.get('ProductSKU', '')                     #商品sku
        ProductName = request.GET.get('ProductName', '')                    # 商品名称
        RejectNumStart = request.GET.get('RejectNumStart', '')
        RejectNumEnd = request.GET.get('RejectNumEnd', '')                #转退数量
        RejectStatus = request.GET.get('RejectStatus', '')                         # 转退状态


        searchList = {
                        'RejectNumber__exact':RejectNumber,
                        'Status__exact': Status,
                        'RejectMan__exact': RejectMan,
                        'PurchaseOrderNum__icontains': PurchaseOrderNum,
                        'ProductSKU__icontains': ProductSKU,
                        'ProductName__icontains': ProductName,
                        'RejectStatus__exact': RejectStatus,
                        'RejectDateStart__gte': RejectDateStart, 'RejectDateEnd__lt': RejectDateEnd,
                        'RejectNumStart__gte': RejectNumStart, 'RejectNumEnd__lt': RejectNumEnd,
                      }

        sl = {}
        for k,v in searchList.items():
            if isinstance(v,list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    sl[k] = v
        if sl is not None:
            try:
                qs = qs.filter(**sl)
            except Exception,ex:
                messages.error(request,u'输入的查询数据有问题！')

        return qs

