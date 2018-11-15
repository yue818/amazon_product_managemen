# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: wangzhiyang
 @site: 
 @software: PyCharm
 @file: t_stocking_demand_fbw_management_Admin.py
 @time: 2018-10-18 16:35

"""
from xadmin.layout import Fieldset, Row
import datetime as tmpDate,random
from pyapp.models import b_goods as py_b_goods,B_Supplier as py_b_Supplier
from django.contrib import messages
from django.utils.safestring import mark_safe
from datetime import datetime as ddtime
from skuapp.table.public import *
from Project.settings import *
from .t_product_Admin import *
from django.db.models import Q
from brick.public.django_wrap import django_wrap

class t_stocking_demand_fbw_management_Admin(object):
    search_box_flag = True
    downloadxls = True
    fbw_tree_menu_flag = True
    hide_page_action = True

    def del_None(self,col):
        rt = col
        if not col:
            rt = ''
        return rt

    def show_Stocking_plan_number(self,obj):
        rt = django_wrap(obj.Stocking_plan_number, '|', 3)
        return mark_safe(rt)
    show_Stocking_plan_number.short_description = mark_safe('<p align="center" style="width:100px;color:#428bca;">计划备货号</p>')

    def show_All_ProductSKU_Num(self,obj):
        rt = django_wrap(obj.All_ProductSKU_Num,';',3)
        return mark_safe(rt)
    show_All_ProductSKU_Num.short_description = mark_safe('<p align="center" style="width:100px;color:#428bca;">商品SKU*数量集合</p>')

    def set_LogisticsNumber(self,obj) :
        rt = ''
        rt = '<table>'
        rt = u'%s<tr><th>物流单号：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fbw_management\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
             (rt, self.del_None(obj.LogisticsNumber), obj.id, 'LogisticsNumber', '', self.del_None(obj.LogisticsNumber),
              str(obj.id) + '_LogisticsNumber',)
        rt = u'%s<tr><th>备注：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fbw_management\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
             (rt, self.del_None(obj.remarks), obj.id, 'remarks', '', self.del_None(obj.remarks),
              str(obj.id) + '_remarks',)
        rt = rt + '</table>'
        if obj.LogisticsNumber is not None and  obj.LogisticsNumber != "":
            rt = u'%s<br><strong>链接地址:</strong><a target="_blank" href="http://139.224.60.129:8321/track_query.aspx?track_number=%s">%s</a><br>' % (rt,
                     obj.LogisticsNumber, obj.LogisticsNumber)
        return mark_safe(rt)
    set_LogisticsNumber.short_description = mark_safe('<p align="center" style="width:100px;color:#428bca;">物流单号</p>')

    list_display = ('Delivery_lot_number','show_Stocking_plan_number','show_All_ProductSKU_Num','Destination_warehouse','Sender','Delivery_date',
                    'set_LogisticsNumber','Status')
    list_editable = ('Status','Delivery_date',)
    actions = ['get_excel_from_management']

    def get_excel_from_management(self,request,objs):
        try:
            from xlwt import *
            path = MEDIA_ROOT + 'download_xls/' + request.user.username
            mkdir_p(MEDIA_ROOT + 'download_xls')
            os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))

            mkdir_p(path)
            os.popen('chmod 777 %s' % (path))

            w = Workbook()
            sheet = w.add_sheet(u'发货清单')

            row = 0
            style = XFStyle()
            sheet.write_merge(0, row, 0, 13, u'%s' % (objs[0].Delivery_lot_number), style)

            row = row + 1
            sheetlist = [u'序号', u'所有SKU', u'所有备货计划号', u'物流单号',u'物流状态',u'发货仓库', u'发货人', u'发货时间' ]

            for index, item in enumerate(sheetlist):
                sheet.write(row, index, item)

            # 写数据
            for qs in objs:

                row = row + 1
                column = 0
                sheet.write(row, column, row)  # 序号

                column = column + 1
                sheet.write(row, column, qs.All_ProductSKU_Num)  # 所有SKU

                column = column + 1
                sheet.write(row, column, qs.Stocking_plan_number)  # 所有备货计划号

                column = column + 1
                sheet.write(row, column, qs.LogisticsNumber)  # 物流单号

                LogisticsNumberSatatus = ""
                for status in getChoices(Choicedeliverstatus):
                    if status[0] == qs.Status:
                        LogisticsNumberSatatus = status[1]
                        break
                column = column + 1
                sheet.write(row, column, LogisticsNumberSatatus)  # 物流状态

                column = column + 1
                Destination_warehouse = ''
                for warehouse in getChoices(ChoiceWarehouse):
                    if warehouse[1] is not None and qs.Destination_warehouse == warehouse[0].strip():
                        Destination_warehouse = warehouse[1].strip()
                sheet.write(row, column, Destination_warehouse)  # 仓库

                column = column + 1
                sheet.write(row, column, qs.Sender)  # 发货人

                column = column + 1
                sheet.write(row, column, qs.Delivery_date)  # 发货时间

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
            messages.info(request, u'%s%s.%s/%s/%s' % (PREFIX, BUCKETNAME_XLS, ENDPOINT_OUT, request.user.username,
                                                        filename) + u':成功导出,可点击Download下载到本地............................。')
        except Exception, ex:
            messages.info(self.request,"导出发货清单报错，错误原因:%s"%(str(ex)))
    get_excel_from_management.short_description = u'导出execl'

    def get_list_queryset(self):
        request = self.request
        
        qs = super(t_stocking_demand_fbw_management_Admin, self).get_list_queryset()
        AllStatus = request.GET.get('allStatus', '')
        if AllStatus == 'all':
            Status = 'onload'
        TmpStatus = request.GET.get('Status', '')
        if TmpStatus != "":
            Status = TmpStatus
        Stocking_plan_number=request.GET.get('Stocking_plan_number','')
        LogisticsNumber=request.GET.get('LogisticsNumber','')
        Sender=request.GET.get('Sender','')

        Delivery_lot_number=request.GET.get('Delivery_lot_number','')
        Delivery_dateStart=request.GET.get('Delivery_dateStart','')
        Delivery_dateEnd=request.GET.get('Delivery_dateEnd','')
        Destination_warehouse=request.GET.get('Destination_warehouse','')
        All_ProductSKU_Num=request.GET.get('All_ProductSKU_Num','')

        searchList = {
                      'Status__exact': Status,
                      'Stocking_plan_number__icontains':Stocking_plan_number,
                      'LogisticsNumber__icontains':LogisticsNumber,
                      'Destination_warehouse__exact':Destination_warehouse,
                      'Delivery_lot_number__icontains':Delivery_lot_number,
                      'Sender__exact':Sender,
                      'Delivery_date__gte':Delivery_dateStart, 'Delivery_date__lt':Delivery_dateEnd,
                      'All_ProductSKU_Num__icontains':All_ProductSKU_Num,
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