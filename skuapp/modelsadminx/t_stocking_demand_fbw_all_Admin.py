# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 王芝杨
 @site: 
 @software: PyCharm
 @file: t_stocking_demand_fbw_all_Admin.py
 @time: 2018-10-20

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

class t_stocking_demand_fbw_all_Admin(object):
    downloadxls = True
    fbw_tree_menu_flag=True
    search_box_flag = True
    def del_None(self,col):
        rt = col
        if not col:
            rt = ''
        return rt
    def show_goodsInfo(self,obj):
        rt = ''
        try:
            rt = u'<strong>商品SKU:</strong>%s<br><strong>商品名称:</strong>%s<br><strong>店铺SKU:</strong>%s<br><strong>店铺简称:</strong>%s<br>' \
                 u'<strong>成本价:</strong>%s<br><strong>产品克重:</strong>%s<br>' \
                 u'<strong>仓库位置:</strong>%s<br><strong>包装规格:</strong>%s' % (
                     self.del_None(obj.ProductSKU),self.del_None(obj.ProductName),self.del_None(obj.ShopSKU),self.del_None(obj.AccountNum),
                     self.del_None(obj.ProductPrice),self.del_None(obj.ProductWeight),
                     self.del_None(obj.position),self.del_None(obj.packFormat))

        except Exception, ex:
            messages.info(self.request, "加载商品信息报错:%s" % (str(ex)))
            rt = ''
        return mark_safe(rt)
    show_goodsInfo.short_description = mark_safe('<p align="center" style="width:100px;color:#428bca;">商品信息</p>')

    def show_ProductImage(self,obj) :
        rt = ''
        try:
            from Project.settings import BmpUrl
            # 获取图片的url
            picture_url = obj.ProductImage  # 获取图片的url
            sku = obj.ProductSKU  # 获取商品SKU
            if not picture_url:
                picture_url = BmpUrl + sku + '.jpg'
            rt = """<img src="%s"  width="120" height="120"  title="%s" onerror="this.title=''" />  """ % (picture_url, picture_url)
        except Exception, ex:
            messages.info(self.request, "加载图片报错:%s" % (str(ex)))
        return mark_safe(rt)
    show_ProductImage.short_description = mark_safe(u'<p style="width:120px;color:#428bca;" align="center">图片</p>')

    def show_sevenOrderCount(self,obj) :
        from brick.classredis.classsku import classsku
        classskuObj = classsku()
        sellCount1 = classskuObj.get_sellcount1_by_sku(obj.ProductSKU)  # 7天销量
        sellCount1 = 0 if (sellCount1 is None or sellCount1 == '') else sellCount1
        rt = u'%s'%(sellCount1)
        return mark_safe(rt)
    show_sevenOrderCount.short_description = mark_safe('<p align="center" style="width:100px;color:#428bca;">7天销量</p>')

    def show_canSellCount(self,obj) :
        from brick.classredis.classsku import classsku
        classskuObj = classsku()
        number = classskuObj.get_number_by_sku(obj.ProductSKU)
        reservationnum = classskuObj.get_reservationnum_by_sku(obj.ProductSKU)
        number = number if (number is not None and number != '') else 0
        reservationnum = reservationnum if (reservationnum is not None and reservationnum != '') else 0
        canSellCount = int(number) - int(reservationnum)
        rt = u'%s'%(canSellCount)
        return mark_safe(rt)
    show_canSellCount.short_description = mark_safe('<p align="center" style="width:100px;color:#428bca;">可售数量</p>')

    def set_value_info(self,obj) :
        rt = ''
        rt = u'<strong>发货量:</strong>%s<br><strong>实际发货量:</strong>%s<br><strong>批次号:</strong>%s' % (
            self.del_None(obj.Stocking_quantity),self.del_None(obj.QTY), self.del_None(obj.ListNumber))
        return mark_safe(rt)
    set_value_info.short_description = u'填写信息'

    list_display = ('Stocking_plan_number','Demand_people','Stock_plan_date','show_goodsInfo','show_ProductImage',
                    'AccountNum','Product_nature','Destination_warehouse','show_sevenOrderCount','show_canSellCount','set_value_info',
                    'DemandMoney','DeliverMoney','FBW_US','deliver_way','newold','Remarks')


    actions = ['get_excel_deliver_form']

    def get_excel_deliver_form(self,request,objs):
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
            sheet.write_merge(0, row, 0, 13, u'%s' % (objs[0].ListNumber), style)

            row = row + 1
            sheetlist = [u'序号', u'SKU',u'成本价', u'商品名称', u'店铺SKU',u'ProductID', u'商品属性', u'商品克重', u'发货数量',u'实际发货数量',
                         u'入库仓库', u'调拨仓库', u'仓位（库位）', u'店铺', u'包装规格', u'备注',u'批次号' ]

            for index, item in enumerate(sheetlist):
                sheet.write(row, index, item)

            # 写数据
            for qs in objs:

                row = row + 1
                column = 0
                sheet.write(row, column, row)  # 序号

                column = column + 1
                sheet.write(row, column, qs.ProductSKU)  # SKU

                column = column + 1
                sheet.write(row, column, qs.ProductPrice)  # 成本价

                column = column + 1
                sheet.write(row, column, qs.ProductName)  # 商品名称

                column = column + 1
                sheet.write(row, column, qs.ShopSKU)  # 店铺SKU

                column = column + 1
                sheet.write(row, column, qs.ProductID)  # ProductID

                Product_nature_value = ""
                for status in getChoices(ChoiceProductnature):
                    if status[0] == qs.Product_nature:
                        Product_nature_value = status[1]
                        break
                column = column + 1
                sheet.write(row, column, Product_nature_value)  # 商品属性

                column = column + 1
                sheet.write(row, column, qs.ProductWeight)  # 商品克重

                column = column + 1
                sheet.write(row, column, qs.Stocking_quantity)  # 发货数量

                column = column + 1
                sheet.write(row, column, qs.QTY)  # 发货数量

                column = column + 1
                Destination_warehouse = ''
                for warehouse in getChoices(ChoiceWarehouse):
                    if warehouse[1] is not None and qs.Destination_warehouse == warehouse[0].strip():
                        Destination_warehouse = warehouse[1].strip()
                sheet.write(row, column, Destination_warehouse)  # 仓库

                if qs.genDemandMan is not None:
                    column = column + 1
                    sheet.write(row, column, u'集货仓调拨')  # 调拨仓库
                else:
                    column = column + 1
                    sheet.write(row, column, u'浦江仓调拨')  # 调拨仓库

                column = column + 1
                sheet.write(row, column, qs.position)  # 仓位（库位）

                column = column + 1
                sheet.write(row, column, qs.AccountNum)  # 店铺

                column = column + 1
                sheet.write(row, column, qs.packFormat)  # 包装规格

                if qs.genDemandMan is not None:
                    column = column + 1
                    sheet.write(row, column, '%s' % (qs.Remarks + ",已提交备货需求"))  # 备注
                else:
                    column = column + 1
                    sheet.write(row, column, '%s' % (qs.Remarks + "浦江仓调拨"))  # 备注
                column = column + 1
                sheet.write(row, column, '%s' % qs.ListNumber)  # 批次号

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
            messages.info(request, u'%s%s.%s/%s/%s' % (PREFIX, BUCKETNAME_XLS, ENDPOINT_OUT, request.user.username,
                                                        filename) + u':成功导出,可点击Download下载到本地............................。')
        except Exception, ex:
            messages.info(self.request, "导出execl报错:%s" % (str(ex)))
    get_excel_deliver_form.short_description = u'导出execl'
        
    def get_list_queryset(self):
        request = self.request
        
        qs = super(t_stocking_demand_fbw_all_Admin, self).get_list_queryset()
        Status = request.GET.get('Status', '')  # 采购状态
        if ',' in Status:
            qs = qs.filter(Status__in=Status.split(','))
        elif Status != '':
            qs = qs.filter(Status__exact=Status)
        Stocking_plan_number = request.GET.get('Stocking_plan_number', '')   #备货计划号
        Stock_plan_dateStart      = request.GET.get('Stock_plan_dateStart', '')     # 备货计划时间
        Stock_plan_dateEnd      = request.GET.get('Stock_plan_dateEnd', '')     # 备货计划时间
        Demand_people = request.GET.get('Demand_people', '')             # 计划需求人
        Product_nature = request.GET.get('Product_nature', '')            #产品性质
        ProductSKU = request.GET.get('ProductSKU', '')                     #商品sku
        ProductName = request.GET.get('ProductName', '')                    # 商品名称
        ShopSKU = request.GET.get('ShopSKU', '')
        AccountNum = request.GET.get('AccountNum', '')                     # 帐号
        Destination_warehouse = request.GET.get('Destination_warehouse', '')# 目的地仓库
        ListNumber = request.GET.get('ListNumber', '')  # 批次号
        ProductID = request.GET.get('ProductID', '')  # 批次号
        genBatchTimeStart = request.GET.get('genBatchTimeStart','')  #记录生成时间
        genBatchTimeEnd =request.GET.get('genBatchTimeEnd','') #记录生成时间
        deliver_way = request.GET.get('deliver_way', '')  # 发货方式
        newold = request.GET.get('newold', '')  # 新老品
        deliverTimeStart = request.GET.get('deliverTimeStart', '')  # 记录生成时间
        deliverTimeEnd = request.GET.get('deliverTimeEnd', '')  # 记录生成时间


        searchList = {
                        'Stocking_plan_number__exact':Stocking_plan_number,
                        'Stock_plan_date__gte':Stock_plan_dateStart,'Stock_plan_date__lt':Stock_plan_dateEnd,
                        'Demand_people__exact':Demand_people,'Product_nature__exact':Product_nature,
                        'ProductSKU__exact': ProductSKU,'ProductName__exact':ProductName,
                        'ProductID__exact':ProductID,
                        'AccountNum__exact':AccountNum,'ShopSKU__exact':ShopSKU,
                        'ListNumber__contains':ListNumber,
					    'Destination_warehouse__exact': Destination_warehouse,
                        'deliver_way__exact':deliver_way,'newold__exact':newold,
                        'genBatchTime__gte':genBatchTimeStart,'genBatchTime__lt':genBatchTimeEnd,
                        'deliverTime__gte': deliverTimeStart, 'deliverTime__lt': deliverTimeEnd,
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

        return qs.order_by("-Stocking_plan_number")

