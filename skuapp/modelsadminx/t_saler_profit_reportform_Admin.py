# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 王芝杨
 @site: 
 @software: PyCharm
 @file: t_saler_profit_reportform_Admin.py
 @time: 2018-08-29

"""
from xadmin.layout import Fieldset, Row
import datetime as tmpDate,random
from pyapp.models import b_goods as py_b_goods,B_Supplier as py_b_Supplier
from django.contrib import messages
from django.utils.safestring import mark_safe
from datetime import datetime as ddtime
from skuapp.table.public import *
from django.db import connection as hqdb_conn
from .t_product_Admin import *
from Project.settings import *

class t_saler_profit_reportform_Admin(object):
    saler_profit = True
    downloadxls = True
    list_display = ['StatisticsMonth','platform','SaleVolume','SaleCost','EbayTransFee','PPCharge','PackCost','FreightCost','Profit','RefundAmount','ShopSKU','ProductSKU'
                    , 'StockAveragePrice', 'Purchaser', 'Supplier', 'Specifications', 'Style1','Style2','GoodsCode','CreateDate','Category','ProductName','ActualAmount','SaleNum',
                    'Salers','Model','BuyerPayFreight', 'SalerName1', 'SalerName2', 'SalerName',]
    search_fields = []

    fields = ('SalerName','StatisticsMonth','ShopSKU','ProductSKU','StockAveragePrice')

    form_layout = (
        Fieldset(u'请认真填写备货需求',
                 Row('SalerName'),
                 css_class='unsort '
                 ),)

    actions = ['exportExecl']

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
            sheet = w.add_sheet(u'业绩销售报表2')

            sheetlist = [u'销售额',u'销售成本',u'ebay成交费',u'PP手续费',u'包装成本',u'运费成本',u'实收利润', u'退款金额',u'店铺SKU', u'SKU',
                 u'库存平均单价',u'采购员',u'供应商',u'规格', u'款式1', u'款式2',u'商品编码',u'商品创建时间',u'商品类别',u'商品名称',u'实得金额',
                 u'销售数量',u'销售员',u'型号',u'买家付运费',u'业绩归属人1', u'业绩归属人2',
                 u'业绩归属人', u'统计月份',u'汇率改变开始时间', u'汇率改变结束时间', ]

            for index, item in enumerate(sheetlist):
                sheet.write(0, index, item)

            # 写数据
            idlist = []
            row = 0
            for qs in objs:
                row = row + 1
                column = 0
                sheet.write(row, column, qs.SaleVolume)  # 销售额
                column = column + 1
                sheet.write(row, column, qs.SaleCost)  # 销售成本
                column = column + 1
                sheet.write(row, column, qs.EbayTransFee)  # ebay成交费
                column = column + 1
                sheet.write(row, column, qs.PPCharge)  # PP手续费
                column = column + 1
                sheet.write(row, column, qs.PackCost)  # 包装成本
                column = column + 1
                sheet.write(row, column, qs.FreightCost)  # 运费成本
                column = column + 1
                sheet.write(row, column, qs.Profit)  # 实收利润
                column = column + 1
                sheet.write(row, column, qs.RefundAmount)  # 退款金额
                column = column + 1
                sheet.write(row, column, qs.ShopSKU)  # 店铺SKU
                column = column + 1
                sheet.write(row, column, qs.ProductSKU)  # SKU

                column = column + 1
                sheet.write(row, column, qs.StockAveragePrice)  # 库存平均单价
                column = column + 1
                sheet.write(row, column, qs.Purchaser)  # 采购员
                column = column + 1
                sheet.write(row, column, qs.Supplier)  # 供应商
                column = column + 1
                sheet.write(row, column, qs.Specifications)  # 规格
                column = column + 1
                sheet.write(row, column, qs.Style1)  # 款式1
                column = column + 1
                sheet.write(row, column, qs.Style2)  # 款式2
                column = column + 1
                sheet.write(row, column, qs.GoodsCode)  # 商品编码
                column = column + 1
                sheet.write(row, column, qs.CreateDate, datastyle)  # 商品创建时间
                column = column + 1
                sheet.write(row, column, qs.Category)  # 商品类别
                column = column + 1
                sheet.write(row, column, qs.ProductName)  # 商品名称
                column = column + 1
                sheet.write(row, column, qs.ActualAmount)  # 实得金额

                column = column + 1
                sheet.write(row, column, qs.SaleNum)  # 销售数量
                column = column + 1
                sheet.write(row, column, qs.Salers)  # 销售员
                column = column + 1
                sheet.write(row, column, qs.Model)  # 型号
                column = column + 1
                sheet.write(row, column, qs.BuyerPayFreight)  # 买家付运费
                column = column + 1
                sheet.write(row, column, qs.SalerName1)  # 业绩归属人1
                column = column + 1
                sheet.write(row, column, qs.SalerName2)  # 业绩归属人2

                column = column + 1
                sheet.write(row, column, qs.SalerName)  # 业绩归属人
                column = column + 1
                sheet.write(row, column, qs.StatisticsMonth)  # 统计月份
                column = column + 1
                sheet.write(row, column, str(qs.effdate), datastyle)  # 生效时间
                column = column + 1
                sheet.write(row, column, str(qs.expdate), datastyle)  # 失效时间

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

    def save_models(self,):
        pass

    def get_list_queryset(self):
        request = self.request

        qs = super(t_saler_profit_reportform_Admin, self).get_list_queryset()
        searchList = {}
        StatisticsMonth = request.GET.get('selmonth', '')
        SalerName = request.GET.get('salerman', '')
        ShopSKU = request.GET.get('shopname', '')
        ShopSKU = ShopSKU.replace('~~!!','#')

        
        searchList = {
            'StatisticsMonth__exact': StatisticsMonth,
            'SalerName__exact': SalerName,
            'ShopSKU__exact': ShopSKU,
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

