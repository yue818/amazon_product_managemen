#-*-coding:utf-8-*-

"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_combination_sku_log_Admin.py
 @time: 2018-04-26 18:49
"""
import os,oss2
from xlwt import *
from Project.settings import MEDIA_ROOT,ACCESS_KEY_ID,ACCESS_KEY_SECRET,ENDPOINT,BUCKETNAME_XLS,PREFIX,ENDPOINT_OUT
from .t_product_Admin import mkdir_p
from pyapp.models import b_goods as py_b_goods
from datetime import datetime
from django.contrib import messages
from django.utils.safestring import mark_safe
from brick.public.django_wrap import django_wrap
from skuapp.table.t_product_mainsku_sku import t_product_mainsku_sku
from skuapp.table.t_combination_sku_log import t_combination_sku_log
import math
from pyapp.models import b_store as py_b_store

class t_combination_sku_log_Admin(object):
    downloadxls = True
    search_box_flag = True
    sku_apply_unbind_flag = True


    def show_Pro_SKU(self,obj) :
        rt = django_wrap(obj.Pro_SKU,'+',6)
        return mark_safe(rt)
    show_Pro_SKU.short_description = u'商品SKU合集'

    list_display   = ('id','Com_SKU','ZHName','show_Pro_SKU','CreateName','CreateTime','SynStatus')
    list_editable = ('ZHName',)

    actions = ['to_excel',]

    def to_excel(self,request,queryset):
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))

        mkdir_p(path)
        os.popen('chmod 777 %s' % (path))

        w = Workbook()
        sheet = w.add_sheet('sku')

        XLS_TITLE = [u'操作类型',u'商品编码',u'SKU',u'组成SKU',u'组成数量',u'是否有样品',u'样品数量',u'大类名称',u'小类名称',u'商品名称',
                     u'当前状态',u'材质',u'规格',u'型号',u'款式',u'品牌',u'单位',u'最小包装数',u'重量(G)',u'采购渠道',u'成本单价(元)',
                     u'批发价格(美元)',u'零售价格(美元)',u'最低售价(美元)',u'最高售价(美元)',u'市场参考价(美元)',u'备注',u'中文申报名',
                     u'英文申报名',u'申报价值(美元)',u'原产国代码',u'原产国',u'库存上限',u'库存下限',u'业绩归属人1',u'业绩归属人2',
                     u'包装规格',u'开发日期',u'发货仓库',u'图片URL',u'最低采购价格',u'责任归属人1',u'责任归属人2',u'内包装成本',u'商品SKU状态']

        for index, item in enumerate(XLS_TITLE):
            sheet.write(0, index, item)

        # 写数据
        row = 0
        for qs in queryset:
            SKU_List = []
            SKU_List_MainSKU = []
            if qs.Pro_SKU and qs.Pro_SKU.strip() != '':
                SKU_List = [ skun for skun in qs.Pro_SKU.strip().split('+') if skun ]
                SKU_List_MainSKU = [ skun.split('*')[0] for skun in qs.Pro_SKU.strip().split('+') if skun ]

            pyskuinfo = None
            if SKU_List_MainSKU:
                objsmainsku = t_product_mainsku_sku.objects.filter(ProductSKU__in=SKU_List_MainSKU).values_list('MainSKU',flat=True)
                if len(set(objsmainsku)) == 1:
                    pyskuinfo = py_b_goods.objects.filter(SKU=SKU_List_MainSKU[0])
            if qs.SynStatus == 'no':
                t_combination_sku_log.objects.filter(id=qs.id).update(SynStatus='yes')

            SKU_List.insert(0,'')
            for i,SKU_each in enumerate(SKU_List):
                row = row + 1
                column = 0 # A 操作类型
                sheet.write(row, column, u'add')

                column = column + 1
                if i == 0:  # 组合产品第一条 # B 商品编码
                    sheet.write(row, column, '%s'%qs.Com_SKU)

                column = column + 1 # C SKU
                sheet.write(row, column, '%s'%qs.Com_SKU)

                column = column + 1
                if i == 0:  # 组合产品第一条  # D 组成SKU
                    sheet.write(row, column, u'是')
                else:
                    sheet.write(row, column, '%s'%SKU_each.split('*')[0])

                column = column + 1 # E 组成数量
                if SKU_each.split('*')[-1] != SKU_each.split('*')[0]:
                    sheet.write(row, column, u'%s'%SKU_each.split('*')[-1])
                else:
                    sheet.write(row, column, u'1')

                column = column + 1 #F 是否有样品
                # sheet.write(row,column,'')

                column = column + 1  # G 样品数据
                # sheet.write(row, column, '%s'%pyskuinfo[0].SampleCount)

                column = column + 1  # H 大类名称
                if i == 0:  # 组合产品第一条
                    sheet.write(row, column, u'026.组合商品')

                column = column + 1  # I 小类名称
                if i == 0:
                    sheet.write(row, column, u'无小类')

                column = column + 1  # J 商品名称
                if i == 0:
                    sheet.write(row, column, u'%s'%qs.ZHName)

                column = column + 1  # K 当前状态
                if i == 0:
                    sheet.write(row, column, u'正常')

                column = column + 1  # L 材质
                if i == 0 and pyskuinfo:
                    sheet.write(row, column, '%s'%pyskuinfo[0].Material)

                column = column + 1  # M 规格

                column = column + 1  # N 型号
                if i == 0 and pyskuinfo:
                    sheet.write(row,column, '%s'%pyskuinfo[0].Model)

                column = column + 1  # O 款式

                column = column + 1  # P 品牌
                if i == 0 and pyskuinfo:
                    sheet.write(row, column, '%s'%pyskuinfo[0].Brand)

                column = column + 1  # Q 单位

                column = column + 1  # R 最小包装数

                column = column + 1  # S 重量(G)
                # if i == 0 and pyskuinfo:
                #     pro_weights = 0
                #     for j, each_pro in enumerate(SKU_List):
                #         if j == 0:
                #             pass
                #         else:
                #             pro_value = py_b_goods.objects.filter(SKU=each_pro.split('*')[0])[0].Weight
                #             if each_pro.split('*')[-1] != each_pro.split('*')[0]:
                #                 pro_weights += pro_value * (int(each_pro.split('*')[-1]))
                #             else:
                #                 pro_weights += pro_value
                #     sheet.write(row, column, '%s' % pro_weights)

                column = column + 1  # T 采购渠道
                if i == 0 and pyskuinfo:
                    sheet.write(row, column, '%s'%pyskuinfo[0].BarCode)

                column = column + 1  # U 成本单价(元)
                # if i == 0 and pyskuinfo:
                #     pro_costprices = 0
                #     for j, each_pro in enumerate(SKU_List):
                #         if j == 0:
                #             pass
                #         else:
                #             pro_value = py_b_goods.objects.filter(SKU=each_pro.split('*')[0])[0].CostPrice
                #             if each_pro.split('*')[-1] != each_pro.split('*')[0]:
                #                 pro_costprices += pro_value * (int(each_pro.split('*')[-1]))
                #             else:
                #                 pro_costprices += pro_value
                #     sheet.write(row, column, '%s'%pro_costprices)

                column = column + 1  # V 批发价格(美元)

                column = column + 1  # W 零售价格(美元)

                column = column + 1  # X 最低售价(美元)

                column = column + 1  # Y 最高售价(美元)

                column = column + 1  # Z 市场参考价(美元)

                column = column + 1  # AA 备注

                column = column + 1  # AB 中文申报名
                if i == 0 and pyskuinfo:
                    sheet.write(row, column, '%s'%pyskuinfo[0].AliasCnName)

                column = column + 1  # AC 英文申报名
                if i == 0 and pyskuinfo:
                    sheet.write(row, column, '%s'%pyskuinfo[0].AliasEnName)

                column = column + 1  # AD 申报价值(美元)
                if i == 0 and pyskuinfo:
                    pro_costprices = 0
                    for j, each_pro in enumerate(SKU_List):
                        if j == 0:
                            pass
                        else:
                            pro_value_obj = py_b_goods.objects.filter(SKU=each_pro.split('*')[0])
                            if pro_value_obj.exists():
                                pro_value = pro_value_obj[0].CostPrice
                                if each_pro.split('*')[-1] != each_pro.split('*')[0]:
                                    pro_costprices += pro_value * (int(each_pro.split('*')[-1]))
                                else:
                                    pro_costprices += pro_value
                            else:
                                messages.error(request,'ID: %s SKU: %s不存在' %(qs.id,each_pro.split('*')[0]) )
                    pro_declaredvalue = math.ceil(int(pro_costprices)/6.5)
                    sheet.write(row, column, '%s'%pro_declaredvalue)

                column = column + 1  # AE 原产国代码
                if i == 0 and pyskuinfo:
                    sheet.write(row, column, '%s'%pyskuinfo[0].OriginCountryCode)

                column = column + 1  # AF 原产国
                if i == 0 and pyskuinfo:
                    sheet.write(row, column, '%s'%pyskuinfo[0].OriginCountry)

                column = column + 1  # AG 库存上限

                column = column + 1  # AH 库存下限

                column = column + 1  # AI 业绩归属人1

                column = column + 1  # AJ 业绩归属人2

                column = column + 1  # AK 包装规格

                column = column + 1  # AL 开发日期
                if i == 0 and pyskuinfo:
                    sheet.write(row, column, '%s'%pyskuinfo[0].DevDate)

                column = column + 1  # AM 发货仓库
                if i == 0 and pyskuinfo:
                    storename = py_b_store.objects.filter(NID=pyskuinfo[0].StoreID)[0].StoreName
                    sheet.write(row, column, '%s' % storename)

                column = column + 1  # AN 图片URL

                column = column + 1  # AO 最低采购价格

                column = column + 1  # AP 责任归属人1
                if i == 0 and pyskuinfo:
                    sheet.write(row, column, '%s'%pyskuinfo[0].possessMan1)

                column = column + 1  # AQ 责任归属人2
                if i == 0 and pyskuinfo:
                    sheet.write(row, column, '%s'%pyskuinfo[0].possessMan2)

                column = column + 1  # AR 内包装成本

                column = column + 1  # AS 商品SKU状态
                if i == 0:
                    sheet.write(row, column, u'正常')

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

    def get_list_queryset(self,):
        request = self.request
        qs = super(t_combination_sku_log_Admin, self).get_list_queryset()
        Com_SKU = request.GET.get('Com_SKU','')
        CreateName = request.GET.get('CreateName','')
        ZHName = request.GET.get('ZHName','')
        SKU = request.GET.get('SKU','')
        SynStatus = request.GET.get('SynStatus','')
        CreateTimeStart = request.GET.get('CreateTimeStart','')
        CreateTimeEnd = request.GET.get('CreateTimeEnd', '')

        searchList = { 'Com_SKU__exact': Com_SKU,'CreateName__exact':CreateName,
                     'ZHName__contains': ZHName,'SynStatus__exact':SynStatus,'Pro_SKU__contains': SKU,
                      'CreateTime__gte': CreateTimeStart, 'CreateTime__lt': CreateTimeEnd,}


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
                messages.error(request, u'Please enter the correct content!')
        return qs



