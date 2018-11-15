# -*- coding: utf-8 -*-
"""
 @desc:
 @author: wangzhiyang
 @site:
 @software: PyCharm
 @file: t_cloth_factory_dispatch_overtobuild_Admin.py
 @time: 2018/4/28 8:53
"""
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from skuapp.table.t_cloth_factory_dispatch_overtobuild import t_cloth_factory_dispatch_overtobuild
from django.contrib import messages
from datetime import datetime
from django.db.models import Q
from django.utils.safestring import mark_safe
from datetime import datetime as overtobuildDate
from Project.settings import *
import oss2
from xlwt import *
from .t_product_Admin import *

class t_cloth_factory_dispatch_overtobuild_Admin(object):
    search_box_flag = True
    t_cloth_factory = True
    downloadxls = True
    actions = ['to_complete','to_import_execl'  ]

    def to_complete(self, request, objs):
        for obj in objs:
            t_cloth_factory_dispatch_overtobuild_obj = t_cloth_factory_dispatch_overtobuild()
            t_cloth_factory_dispatch_overtobuild_obj.__dict__ = obj.__dict__
            t_cloth_factory_dispatch_overtobuild_obj.closeMan = request.user.first_name
            t_cloth_factory_dispatch_overtobuild_obj.closeDate = overtobuildDate.now()
            t_cloth_factory_dispatch_overtobuild_obj.currentState = '28'
            t_cloth_factory_dispatch_overtobuild_obj.save()
    to_complete.short_description = u'完成普源采购单-关闭'

    def to_import_execl(self, request, objs):
        try:
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
            # 写入execl
            path = MEDIA_ROOT + 'download_xls/' + request.user.username
            # if not os.path.exists(path):
            mkdir_p(MEDIA_ROOT + 'download_xls')
            os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))
            mkdir_p(path)
            os.popen('chmod 777 %s' % (path))
            w = Workbook()
            row = 0
            sheet = w.add_sheet(u'校验交付数据')
            style = XFStyle()

            sheet.write(0, 0, u'日期', style)  # 日期
            sheet.write(0, 1, u'SKU', style)  # SKU
            sheet.write(0, 2, u'采购员', style)  # 采购员
            sheet.write(0, 3, u'商品名称', style)  # 商品名称
            sheet.write(0, 4, u'建议采购数量', style)  # 建议采购数量
            sheet.write(0, 5, u'采购数量', style)  # 采购数量
            sheet.write(0, 6, u'完成数量', style)  # 完成数量
            sheet.write(0, 7, u'采购备注', style)  # 采购备注
            sheet.write(0, 8, u'派发工厂', style)  # 派发工厂
            sheet.write(0, 9, u'订单编号', style)  # 排单备注
            sheet.write(0, 10, u'超出数量', style)  # 排单备注
            sheet.write(0, 11, u'其他信息', style)  # 排单备注
            sheet.write(0, 12, u'采购等级', style)  # 排单备注
            
            for obj in objs:
                row = row + 1
                if obj.createDate is not None:
                    sheet.write(row, 0, str(obj.createDate), style)  # 日期
                else:
                    sheet.write(row, 0, '', style)  # 日期
                sheet.write(row, 1, obj.SKU, style)  # SKU
                if obj.buyer is not None:
                    sheet.write(row, 2, obj.buyer, style)  # 采购员
                else:
                    sheet.write(row, 2, '', style)  # 采购员
                if obj.goodsName is not None:
                    sheet.write(row, 3, obj.goodsName, style)  # 商品名称
                else:
                    sheet.write(row, 3, '', style)  # 商品名称
                if obj.SuggestNum is not None:
                    sheet.write(row, 4, obj.SuggestNum, style)  # 建议采购数量
                else:
                    sheet.write(row, 4, 0, style)  # 建议采购数量
                if obj.productNumbers is not None:
                    sheet.write(row, 5, obj.productNumbers, style)  # 采购数量
                else:
                    sheet.write(row, 5, 0, style)  # 采购数量
                if obj.completeNumbers is not None:
                    sheet.write(row, 6, obj.completeNumbers, style)  # 完成数量
                else:
                    sheet.write(row, 6, 0, style)  # 完成数量
                strRemark = ''
                if obj.remarkApply is not None:
                    strRemark = obj.remarkApply
                    if obj.remarkAudit is not None:
                        strRemark = strRemark + "," +obj.remarkAudit
                        if obj.remarkConfirm is not None:
                            strRemark = strRemark + "," + obj.remarkConfirm
                    else:
                        if obj.remarkConfirm is not None:
                            strRemark = strRemark + "," + obj.remarkConfirm
                else:
                    if obj.remarkAudit is not None:
                        strRemark = strRemark + "," + obj.remarkAudit
                        if obj.remarkConfirm is not None:
                            strRemark = strRemark + "," + obj.remarkConfirm
                    else:
                        if obj.remarkConfirm is not None:
                            strRemark = strRemark + "," + obj.remarkConfirm
                sheet.write(row, 7, strRemark, style)  # 采购备注
                sheet.write(row, 8, obj.outFactory, style)  # 派发工厂
                if obj.remarkDisPatch:
                    remarkDisPatch = obj.remarkDisPatch.split('#@#')
                    for i in range(len(remarkDisPatch)):
                        sheet.write(row, 9+i, remarkDisPatch[i], style)  # 排单备注
                else:
                    sheet.write(row, 9, '', style)  # 排单备注
                    sheet.write(row, 10, '', style)
                    sheet.write(row, 11, '', style)
                if obj.OSCode is None or obj.OSCode == 'OS905': # 采购等级
                    sheet.write(row, 12, u'OS905:工期5天(建议采购15天量、联动采购16~17天量)', style)
                elif obj.OSCode == 'OS901': # 采购等级
                    sheet.write(row, 12, u'OS901:工期3天(建议采购10天量、联动采购11~14天量)', style)
                elif obj.OSCode == 'OS902': # 采购等级
                    sheet.write(row, 12, u'OS902:工期5天(建议采购15天量、联动采购16~17天量)', style)
                elif obj.OSCode == 'OS903': # 采购等级
                    sheet.write(row, 12, u'OS903:工期7天(建议采购15天量、联动采购16~19天量)', style)
                elif obj.OSCode == 'OS904': # 采购等级
                    sheet.write(row, 12, u'OS904:工期15天(建议采购20天)', style)
                elif obj.OSCode == 'OS906': # 采购等级
                    sheet.write(row, 12, u'OS906:工期5天(Amazon服装采购)', style)
                else:
                    sheet.write(row, 12, u'OS905:工期5天(建议采购15天量、联动采购16~17天量)', style)
            filename = request.user.username + '_' + overtobuildDate.now().strftime('%Y%m%d%H%M%S') + '.xls'
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
        except Exception as e:
            messages.info(self.request,"导出数据到execl报错:%s，请联系开发人员"%(str(e)))
    to_import_execl.short_description = u'导出数据到execl'

    def show_Picture(self,obj) :
        # self.update_status(obj)
        from Project.settings import BmpUrl
        # 获取图片的url
        picture_url = obj.BmpUrl  # 获取图片的url
        sku = obj.SKU  # 获取商品SKU
        if not picture_url:
            picture_url = BmpUrl + sku + '.jpg'

        rt = """<img src="%s"  width="120" height="120"  title="%s" onerror="this.title=''" />"""   % (picture_url, picture_url)
        return mark_safe(rt)
    show_Picture.short_description = mark_safe(u'<p style="width:120px;color:#428bca;" align="center">图片</p>')

    def show_rawNumbers(self, obj):
        rt = u'<strong>原材料数量:</strong>%s(%s)<br><strong>采购数量:</strong>%s<br><strong>外派工厂:</strong>%s<br><strong>采购备注:</strong>%s<br><strong>审核备注:</strong>%s<br><strong>交付备注:</strong>%s' % (
            obj.rawNumbers, obj.unit, obj.productNumbers, obj.outFactory, obj.remarkApply, obj.remarkAudit,str(obj.remarkDisPatch).replace('#@#',','))

        return mark_safe(rt)
    show_rawNumbers.short_description = mark_safe('<p align="center" style="width:180px;color:#428bca;">排单信息</p>')

    def GoodsOther(self,obj):
        rt = u'<p style="width:120px;"><strong>商品成本价:</strong>%s <br><strong>7天销量:</strong>%s <br><strong>预计库存量:</strong>%s<br><strong>采购未入库量:</strong>%s</p>' % (obj.goodsCostPrice,obj.sevenSales,obj.ailableNum,obj.PurchaseNotInNum)
        if obj.SpecialPurchaseFlag is not None and obj.SpecialPurchaseFlag != '':
            if obj.SpecialPurchaseFlag == 'firstorder':
                rt = rt + u'<br><strong>注:手动新增-网采转供应链排单(首单)</strong>'
            elif obj.SpecialPurchaseFlag == 'customermade':
                rt = rt + u'<br><strong>注:手动新增-客户定做</strong>'
            elif obj.SpecialPurchaseFlag == 'other':
                rt = rt + u'<br><strong>注:手动新增-浦江仓库</strong>'
        elif obj.OSCode == 'OS906' and obj.Stocking_plan_number is not None and obj.Stocking_plan_number != '':
            rt = rt + u'<br><strong>注:海外仓备货转服装排单</strong>'
        else:
            rt = rt + u'<br><strong>注:系统自动生成采购</strong>'
        return mark_safe(rt)
    GoodsOther.short_description = mark_safe(u'<p style="width:120px;color:#428bca;" align="center">商品其他信息</p>')

    def GoodsInfo(self,obj):
        rt = u'<p style="width:200px;"><strong>商品名称:</strong>%s <br><strong>供应商名:</strong>%s <br><strong>商品状态:</strong>%s<br><strong>商品类别:</strong>%s<br><strong>侵权站点:</strong>%s<br><strong>上一步处理人员:</strong>%s<br><strong>上一步处理时间:</strong>%s</p>' % (obj.goodsName,obj.Supplier, obj.goodsState,obj.goodsclass,obj.TortInfo,obj.confirmMan,obj.confirmDate)
        return mark_safe(rt)
    GoodsInfo.short_description = mark_safe(u'<p style="width:200px;color:#428bca;" align="center">商品及流程信息</p>')

    list_per_page = 20
    list_display = (
        'SKU','show_Picture', 'buyer','SalerName2', 'OSCode','GoodsInfo',
        'GoodsOther', 'show_rawNumbers','completeNumbers',)

    fields = (
        'SKU', 'goodsName', 'Supplier', 'goodsState', 'goodsCostPrice', 'oosNum', 'stockNum', 'ailableNum',
        'sevenSales', 'fifteenSales',
        'thirtySales', 'PurchaseNotInNum', 'buyer', 'productNumbers', 'loanMoney',
        'actualMoney', 'outFactory', 'rawNumbers', 'unit',
        'remarkApply', 'remarkApply', 'applyMan', 'auditMan', 'dispatchMan', 'remarkAudit', 'remarkDisPatch','createDate','closeDate','applyMan','auditMan','confirmMan',)


    def get_list_queryset(self):
        request = self.request
        qs = super(t_cloth_factory_dispatch_overtobuild_Admin, self).get_list_queryset()
        SKU = request.GET.get('SKU', '')

        Supplier = request.GET.get('Supplier', '')
        buyer = request.GET.get('buyer', '')
        buyer = buyer.split(',')
        if '' in buyer:
            buyer = ''
        oosNumStart = request.GET.get('oosNum_Start', '')
        oosNumEnd = request.GET.get('oosNum_End', '')

        goodsState = request.GET.get('goodsState', '')
        outFactory = request.GET.get('outFactory', '')
        from skuapp.table.goodsstatus_compare import goodsstatus_compare
        goodsstatus_compare_objs = goodsstatus_compare.objects.filter(py_GoodsStatus=goodsState).values_list(
            "hq_GoodsStatus", flat=True)

        createDateStart = request.GET.get('createDate_Start', '')
        createDateEnd = request.GET.get('createDate_End', '')

        searchList = {'SKU__contains': SKU,
                      'Supplier':Supplier,
                      'buyer__in': buyer,
                      'oosNum__gte': oosNumStart,
                      'oosNum__lt': oosNumEnd,
                      'goodsState__in':list(goodsstatus_compare_objs),
                      'createDate__gte': createDateStart,
                      'createDate__lt': createDateEnd,
                      'outFactory__contains': outFactory,
                      }

        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    # if k == 'ShopName__exact':
                    # v = 'Wish-' + v.zfill(4)
                    # messages.error(request, v)
                    sl[k] = v
        if sl is not None:
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'输入的查询数据有问题！')

        from django.contrib.auth.models import User
        userID = [each.id for each in User.objects.filter(groups__id__in=[48])]
        if request.user.is_superuser or request.user.id in userID:
            return qs.filter(currentState = 24)
        buyer = request.user.first_name
        return qs.filter(currentState = 24, buyer=buyer)
        #return qs.filter(currentState = 24)


