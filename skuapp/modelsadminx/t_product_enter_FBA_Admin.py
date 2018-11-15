# -*- coding: utf-8 -*-
from datetime import datetime as fbaDateTime
from skuapp.table.t_product_enter_FBA import t_product_enter_FBA
from skuapp.table.t_product_build_FBA import t_product_build_FBA
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field, Div, FormActions, Submit, Button, ButtonHolder, InlineRadios, Reset, StrictButton, HTML, Hidden, Alert

from django.contrib import messages
from Project.settings import *
import oss2
from xlwt import *
from .t_product_Admin import *
from django.utils.safestring import mark_safe
from brick.pydata.py_syn.public import public
import pymssql
from django.db import connection as hqdbconn
from brick.pydata.py_syn.py_conn import py_conn

class t_product_enter_FBA_Admin(object):

    search_box_flag = True

    downloadxls = True

    actions = [ 'to_recycle','to_export_excel','to_next','to_export_py', ]

    def showStatus(self, obj):
        rt = ""
        if obj.isflag == 0:
            rt = u"<font color='red'>建资料未提交</font>"
        elif obj.isflag == 1:
            rt = u"<font color='red'>待录入</font>"
        elif obj.isflag == 2:
            rt = u"<font color='red'>已录入</font>"
        else:
            rt = u"<font color='red'>不录入</font>"
        return mark_safe(rt)
    showStatus.short_description = u'FBA状态'

    def to_export_py(self,request, queryset):
        pyconn = py_conn()
        sqlserverinfo = pyconn.py_conn_database()
        try:
            result = {'errorcode':0,'errortext':''}
            strAllSKU = ""
            data_list = []
            for qs in queryset:
                #获取大类、小类名称
                if qs.LRTime is None:
                    qs.LRTime = fbaDateTime.now()
                b_goods_data = {
                    'GoodsCategoryID': '', 'CategoryCode': '', 'GoodsCode': qs.SKU, 'GoodsName': qs.Name2,'ShopTitle': '', 'SKU': qs.SKU, 'BarCode': qs.BarCode,
                    'FitCode': '', 'MultiStyle': qs.MultiStyle,'Material': qs.Material, 'Class': qs.Class, 'Model': qs.Model, 'Unit': qs.Unit, 'Style': qs.Style, 'Brand': qs.Brand,
                    'LocationID': '', 'Quantity': qs.Quantity, 'SalePrice': qs.SalePrice, 'CostPrice': qs.CostPrice,'AliasCnName': qs.ReportName2,'AliasEnName': qs.ReportName,
                    'Weight': qs.Weight, 'DeclaredValue': qs.DeclaredValue,'OriginCountry': qs.OriginCountry, 'OriginCountryCode': qs.OriginCountryCode, 'ExpressID': '',
                    'Used': '', 'BmpFileName': '', 'BmpUrl': qs.BmpUrl, 'MaxNum': qs.MaxNum, 'MinNum': qs.MinNum, 'GoodsCount': '','SupplierID': '','Notes': qs.Remark,
                    'SampleFlag': qs.SampleFlag, 'SampleCount': qs.SampleCount, 'SampleMemo': '', 'CreateDate': str(qs.LRTime)[:10],'GroupFlag': '', 'SalerName': qs.SalerName,
                    'SellCount': '', 'SellDays': qs.SellDays,'PackFee': qs.InnerPrice, 'PackName': qs.PackingID, 'GoodsStatus':qs.GoodsStatus,
                    'DevDate': str(qs.LRTime)[:10], 'SalerName2': qs.SalerName2,'BatchPrice': qs.BatchPrice, 'MaxSalePrice': qs.MaxSalePrice, 'RetailPrice': qs.RetailPrice,
                    'MarketPrice': qs.MarketPrice,'PackageCount': qs.MinPackNum,'ChangeStatusTime': '', 'StockDays': qs.StockDays, 'StoreID': '', 'Purchaser': qs.Purchaser,
                    'LinkUrl': qs.LinkUrl, 'LinkUrl2': qs.LinkUrl2, 'LinkUrl3': qs.LinkUrl3, 'StockMinAmount': qs.StockMinAmount, 'MinPrice': qs.MinPrice,
                    'HSCODE': qs.HSCODE, 'ViewUser': '', 'InLong': qs.InLong, 'InWide': qs.InWide, 'InHigh': qs.InHigh, 'InGrossweight': qs.InGrossweight,
                    'InNetweight': qs.InNetweight, 'OutLong': qs.OutLong, 'OutWide': qs.OutWide, 'OutHigh': qs.OutHigh, 'OutGrossweight': qs.OutGrossweight,'OutNetweight': qs.OutNetweight,
                    'ShopCarryCost': qs.ShopFreight, 'ExchangeRate': qs.ExchangeRate, 'WebCost': '', 'PackWeight': qs.PackWeight, 'LogisticsCost': '','GrossRate': '',
                    'CalSalePrice': '', 'CalYunFei': '', 'CalSaleAllPrice': '', 'PackMsg': qs.PackMsg,'ItemUrl': qs.ItemUrl,'IsCharged': qs.Electrification,'DelInFile': '',
                    'Season': qs.Season, 'IsPowder': qs.Powder, 'IsLiquid': qs.Liquid, 'possessMan1': qs.possessMan1,'possessMan2': qs.possessMan2, 'LinkUrl4': qs.LinkUrl4,
                    'LinkUrl5': qs.LinkUrl5, 'LinkUrl6': qs.LinkUrl6, 'isMagnetism': '','NoSalesDate': '', 'NotUsedReason': '', 'PackingRatio': qs.DegreeOfDifficulty,
                    'shippingType': '', 'FreightRate': qs.LogisticsPrice,'USEDueDate': '', 'SupplierName': qs.SupplierName, 'LargeCategoryName': qs.LargeCategory,
                    'SmallCategoryName': qs.SmallCategory, 'Storehouse': qs.Storehouse, 'ProductAttr': qs.ContrabandAttribute
                }
                strAllSKU = strAllSKU + qs.SKU + ","
                data_list.append(b_goods_data)

            from brick.table.t_operation_log_online_syn_py import t_operation_log_online_syn_py
            from django.db import connection
            operation_log_obj = t_operation_log_online_syn_py(DBConn=connection)
            param = {}  # 操作日志的参数
            param['OpNum'] = 'add_fbasku_%s_%s' % (fbaDateTime.now().strftime('%Y%m%d%H%M%S'), request.user.username)
            param['OpKey'] = ['FBA_Main',]
            param['OpType'] = 'FBA'
            param['Status'] = 'runing'
            param['ErrorInfo'] = "sucess syn_SKU:" + str(queryset.values_list("SKU",flat=True))
            param['OpPerson'] = request.user.first_name
            param['OpTime'] = fbaDateTime.now()
            param['OpStartTime'] = fbaDateTime.now()
            param['OpEndTime'] = fbaDateTime.now()
            param['aNum'] = len(queryset)
            param['rNum'] = 0
            param['eNum'] = 0
            param['SKU'] = strAllSKU
            iResult = operation_log_obj.createLog(param)

            # 写入普源
            public_obj = public()
            result = public_obj.sku_info_to_pydb(b_goods_data_list=data_list, sqlserverInfo=sqlserverinfo,mainsku=qs.MainSKU, pydb_connect=hqdbconn)

            if result['errorcode'] != 0 and result['errortext'].find('FBA') == -1:
                error_info = result['errortext']
                messages.error(request, "同步普源错误，请联系开发人员；错误信息:%s" % (error_info))
                operation_log_obj.update_error(param['OpNum'],"errorcode:" + str(result['errorcode']) + ";errortext:" +str(result['errortext']))
            else:
                self.t_product_mainsku_sku_deal(request, queryset)
                if len(result['errortext']) > 0:
                    messages.info(request, "已存在普源SKU:%s，不需要重复做同步,已更新为已录入。" % (result['errortext']))
                else:
                    # 将状态设置为已录入
                    messages.info(request, "选中商品已成功同步普源，并将当前数据更新为已录入。" )
                operation_log_obj.update_success(param['OpNum'],param['ErrorInfo'],param['aNum'],0)
            pyconn.py_close_conn_database()
        except Exception, ex:
            messages.error(request,"同步普源错误，请联系开发人员:%s,%s"%(Exception,ex))
            operation_log_obj.update_error(param['OpNum'],str(Exception)+str(ex) + ";errorcode:" + str(result['errorcode']) + ";errortext:" +str(result['errortext']))
            pyconn.py_close_conn_database()
    to_export_py.short_description = u'FBA-同步普源'

    def to_recycle(self, request, objs):
        arrFBA = []
        for obj in objs:
            # 下一步
            if obj.isflag == 1:
                obj.isflag = 3
                obj.OpStaffName = request.user.first_name
                obj.OpDatetime = fbaDateTime.now()
                obj.save()
            else:
                arrFBA.append(obj.SKU)
        if len(arrFBA) > 0:
            messages.info(request,u"以下FBASKU：%s 不能执行FBA-不录入操作。")
    to_recycle.short_description = u'FBA-不录入'

    def t_product_mainsku_sku_deal(self, request, objs):
        arrFBA = []
        for obj in objs:
            try:
                if obj.isflag == 1:
                    obj.isflag = 2
                    obj.FBAFinshTime = fbaDateTime.now()
                    obj.OpStaffName = request.user.first_name
                    obj.OpDatetime = fbaDateTime.now()
                    strProductSKU = obj.OldSKU
                    strFBASKU = obj.SKU
                    strMainSKU = obj.SKU
                    from skuapp.table.t_product_mainsku_sku import t_product_mainsku_sku
                    t_product_mainsku_sku_obj = t_product_mainsku_sku.objects.filter(ProductSKU=strProductSKU).values(
                        'MainSKU', 'SKU', 'ProductSKU', 'pid', 'SKUATTRS',
                        'UnitPrice', 'Weight', 'PackNID', 'MinPackNum', 'DressInfo')
                    # 根据商品SKU在t_product_mainsku_sku表中获取结果
                    if len(t_product_mainsku_sku_obj) != 0:
                        strFBAMainSKU = ""
                        strFBASKUAttr = ""
                        # 如果主SKU与商品SKU相等，需要对主SKU、商品SKU以及商品属性都需要添加"FBA-",如果不相等 只需对主SKU、商品SKU添加"FBA-"
                        if t_product_mainsku_sku_obj[0]['MainSKU'] == t_product_mainsku_sku_obj[0]['ProductSKU']:
                            strFBAMainSKU = "FBA-" + t_product_mainsku_sku_obj[0]['MainSKU']
                            if t_product_mainsku_sku_obj[0]['SKU'] is None:
                                strFBASKUAttr = t_product_mainsku_sku_obj[0]['SKU']
                            else:
                                strFBASKUAttr = "FBA-" + t_product_mainsku_sku_obj[0]['SKU']
                        else:
                            strFBAMainSKU = "FBA-" + t_product_mainsku_sku_obj[0]['MainSKU']
                            strFBASKUAttr = t_product_mainsku_sku_obj[0]['SKU']
                        # 查看在t_product_mainsku_sku表中是否已录入FBA对应的SKU,如果录入取出pid，没有则获取t_product_build_fba表对应记录id
                        t_product_mainsku_fbasku_obj = t_product_mainsku_sku.objects.filter(MainSKU=strFBAMainSKU).values(
                            'pid')
                        if len(t_product_mainsku_fbasku_obj) != 0:
                            pid = t_product_mainsku_fbasku_obj[0]['pid']
                        else:
                            pid = obj.id
                        strMainSKU = strFBAMainSKU
                        # messages.info(request, str(strFBAMainSKU)+";"+strFBASKU)
                        t_product_mainsku_sku.objects.filter(MainSKU=strFBAMainSKU, ProductSKU=strFBASKU).delete()
                        t_product_mainsku_sku_new = t_product_mainsku_sku(MainSKU=strFBAMainSKU, SKU=strFBASKUAttr, pid=pid,
                                                                          SKUATTRS=t_product_mainsku_sku_obj[0]['SKUATTRS'],
                                                                          UnitPrice=t_product_mainsku_sku_obj[0][
                                                                              'UnitPrice'],
                                                                          Weight=t_product_mainsku_sku_obj[0]['Weight'],
                                                                          PackNID=t_product_mainsku_sku_obj[0]['PackNID'],
                                                                          MinPackNum=t_product_mainsku_sku_obj[0][
                                                                              'MinPackNum'],
                                                                          DressInfo=t_product_mainsku_sku_obj[0][
                                                                              'DressInfo'], ProductSKU=strFBASKU)
                        t_product_mainsku_sku_new.save()
                    else:
                        # 查看在t_product_mainsku_sku表中是否已录入FBA对应的SKU,如果录入取出pid，没有则获取t_product_build_fba表对应记录id
                        t_product_mainsku_fbasku_obj = t_product_mainsku_sku.objects.filter(ProductSKU=strFBASKU).values(
                            'pid', 'MainSKU')
                        if len(t_product_mainsku_fbasku_obj) != 0:
                            pid = t_product_mainsku_fbasku_obj[0]['pid']
                            strMainSKU = t_product_mainsku_fbasku_obj[0]['MainSKU']
                        else:
                            pid = obj.id
                            strMainSKU = strFBASKU
                        # messages.info(request, str(strFBAMainSKU)+";"+strFBASKU)
                        t_product_mainsku_sku.objects.filter(MainSKU=strMainSKU, ProductSKU=strFBASKU).delete()
                        t_product_mainsku_sku_new = t_product_mainsku_sku(MainSKU=strMainSKU, SKU=strFBASKU, pid=pid,
                                                                          SKUATTRS=None,
                                                                          UnitPrice=obj.CostPrice,
                                                                          Weight=obj.Weight,
                                                                          PackNID=0,
                                                                          MinPackNum=obj.MinPackNum,
                                                                          DressInfo=obj.Name2, ProductSKU=strFBASKU)
                        t_product_mainsku_sku_new.save()

                    obj.MainSKU = strMainSKU
                    obj.save()

                else:
                    arrFBA.append(obj.SKU)
            except Exception, ex:
                messages.info(request, "生成主SKU与SKU对应关系报错，请联系开发人员，报错信息:%s,%s" % (Exception, ex))
        if len(arrFBA) > 0:
            messages.info(request, u"以下FBASKU：%s 不能执行FBA-不录入操作。"%(arrFBA))

    def to_next(self, request, objs):
        arrFBA = []
        for obj in objs:
            # 下一步
            if obj.isflag == 1:
                obj.isflag = 2
                obj.FBAFinshTime = datetime.datetime.now()
                obj.OpStaffName = request.user.first_name
                obj.OpDatetime = datetime.datetime.now()
                strProductSKU = obj.OldSKU
                strFBASKU = obj.SKU
                strMainSKU = obj.SKU
                from skuapp.table.t_product_mainsku_sku import t_product_mainsku_sku
                t_product_mainsku_sku_obj = t_product_mainsku_sku.objects.filter(ProductSKU=strProductSKU).values('MainSKU','SKU','ProductSKU','pid','SKUATTRS',
                                                                                                                  'UnitPrice','Weight','PackNID','MinPackNum','DressInfo')
                #messages.info(request, str(t_product_mainsku_sku_obj))
                #根据商品SKU在t_product_mainsku_sku表中获取结果
                if len(t_product_mainsku_sku_obj) != 0:
                    strFBAMainSKU = ""
                    strFBASKUAttr = ""
                    #如果主SKU与商品SKU相等，需要对主SKU、商品SKU以及商品属性都需要添加"FBA-",如果不相等 只需对主SKU、商品SKU添加"FBA-"
                    if t_product_mainsku_sku_obj[0]['MainSKU'] == t_product_mainsku_sku_obj[0]['ProductSKU']:
                        strFBAMainSKU = "FBA-" + t_product_mainsku_sku_obj[0]['MainSKU']
                        if t_product_mainsku_sku_obj[0]['SKU'] is None:
                            strFBASKUAttr = t_product_mainsku_sku_obj[0]['SKU']
                        else:
                            strFBASKUAttr = "FBA-" + t_product_mainsku_sku_obj[0]['SKU']
                    else:
                        strFBAMainSKU = "FBA-" + t_product_mainsku_sku_obj[0]['MainSKU']
                        strFBASKUAttr = t_product_mainsku_sku_obj[0]['SKU']
                    #查看在t_product_mainsku_sku表中是否已录入FBA对应的SKU,如果录入取出pid，没有则获取t_product_build_fba表对应记录id
                    t_product_mainsku_fbasku_obj = t_product_mainsku_sku.objects.filter(MainSKU=strFBAMainSKU).values('pid')
                    if len(t_product_mainsku_fbasku_obj) != 0:
                        pid = t_product_mainsku_fbasku_obj[0]['pid']
                    else:
                        pid = obj.id
                    strMainSKU = strFBAMainSKU
                    #messages.info(request, str(strFBAMainSKU)+";"+strFBASKU)
                    t_product_mainsku_sku.objects.filter(MainSKU=strFBAMainSKU,ProductSKU=strFBASKU).delete()
                    t_product_mainsku_sku_new = t_product_mainsku_sku(MainSKU=strFBAMainSKU, SKU=strFBASKUAttr, pid=pid, SKUATTRS=t_product_mainsku_sku_obj[0]['SKUATTRS'],
                                                                      UnitPrice = t_product_mainsku_sku_obj[0]['UnitPrice'], Weight=t_product_mainsku_sku_obj[0]['Weight'],
                                                                      PackNID=t_product_mainsku_sku_obj[0]['PackNID'],MinPackNum=t_product_mainsku_sku_obj[0]['MinPackNum'],
                                                                      DressInfo=t_product_mainsku_sku_obj[0]['DressInfo'],ProductSKU=strFBASKU)
                    t_product_mainsku_sku_new.save()
                else:
                    # 查看在t_product_mainsku_sku表中是否已录入FBA对应的SKU,如果录入取出pid，没有则获取t_product_build_fba表对应记录id
                    t_product_mainsku_fbasku_obj = t_product_mainsku_sku.objects.filter(ProductSKU=strFBASKU).values('pid','MainSKU')
                    if len(t_product_mainsku_fbasku_obj) != 0:
                        pid = t_product_mainsku_fbasku_obj[0]['pid']
                        strMainSKU = t_product_mainsku_fbasku_obj[0]['MainSKU']
                    else:
                        pid = obj.id
                        strMainSKU = strFBASKU
                    # messages.info(request, str(strFBAMainSKU)+";"+strFBASKU)
                    t_product_mainsku_sku.objects.filter(MainSKU=strMainSKU, ProductSKU=strFBASKU).delete()
                    t_product_mainsku_sku_new = t_product_mainsku_sku(MainSKU=strMainSKU, SKU=strFBASKU, pid=pid,
                                                                      SKUATTRS=None,
                                                                      UnitPrice=obj.CostPrice,
                                                                      Weight=obj.Weight,
                                                                      PackNID=0,
                                                                      MinPackNum=obj.MinPackNum,
                                                                      DressInfo=obj.Name2, ProductSKU=strFBASKU)
                    t_product_mainsku_sku_new.save()

                obj.MainSKU = strMainSKU
                obj.save()

            else:
                arrFBA.append(obj.SKU)
        if len(arrFBA) > 0:
            messages.info(request,u"以下FBASKU：%s 不能执行FBA-不录入操作。"%(arrFBA))
    to_next.short_description = u'FBA-录入完成'

    def to_export_excel(self, request, queryset):
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        # if not os.path.exists(path):
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))

        mkdir_p(path)
        os.popen('chmod 777 %s' % (path))

        w = Workbook()
        sheet = w.add_sheet('FBA_sku')
        XLS_FIELDS = (u'操作类型',u'商品编码',u'SKU',u'多款式',u'是否有样品',u'样品数量',u'大类名称',u'小类名称',u'商品名称',u'当前状态',u'材质',
                      u'规格',u'型号',u'款式',u'品牌',u'单位',u'最小包装数',u'重量(G)',u'采购渠道',u'供应商名称',u'成本单价(元)',u'批发价格(美元)',
                      u'零售价格(美元)',u'最低售价(美元)',u'最高售价(美元)',u'市场参考价(美元)',u'数量',u'备注',u'中文申报名',u'英文申报名',u'申报价值(美元)',
                      u'原产国代码',u'原产国',u'库存上限',u'库存下限',u'业绩归属人1',u'业绩归属人2',u'包装规格',u'开发日期',u'SKU款式1',u'SKU款式2',
                      u'SKU款式3',u'SKU描述',u'图片URL',u'采购员',u'发货仓库',u'采购到货天数',u'内包装成本',u'网页URL',u'网页URL2',u'网页URL3',
                      u'最低采购价格',u'海关编码',u'库存预警销售周期',u'采购最小订货量',u'内盒长',u'内盒宽',u'内盒高',u'内盒毛重',u'内盒净重',
                      u'外箱长',u'外箱宽',u'外箱高',u'外箱毛重',u'外箱净重',u'商品URL',u'包装事项',u'是否带电',u'商品SKU状态',u'工号权限',u'季节',
                      u'是否粉末',u'是否液体',u'责任归属人1',u'责任归属人2',u'商品属性',u'包装难度系数',u'店铺名称',u'网页URL4',u'网页URL5',u'网页URL6',
                      u'店铺运费',u'包装材料重量',u'汇率',u'物流公司价格',u'交易费',u'毛利率',u'计算售价' )
        for index, item in enumerate(XLS_FIELDS):
            sheet.write(0, index, item)

        # 写数据
        row = 0
        #'DevDate','SKU','LRStaffName','Name2', 'ReportName2','ReportName','Purchaser','CostPrice','Weight','SalerName','SalerName',
        arrFBA = []
        for qs in queryset:
            if qs.isflag == 0 or qs.isflag == 3:
                arrFBA.append(qs.SKU)
                continue
            row += 1
            sheet.write(row, 0, 'add')  # 开发日期
            sheet.write(row, 1, qs.SKU)  # 商品编码
            sheet.write(row, 2, qs.SKU)  # FBA  SKU
            sheet.write(row, 3, qs.MultiStyle)  # 多款式
            sheet.write(row, 4, qs.SampleFlag)  # 是否有样品
            sheet.write(row, 5, qs.SampleCount)  # 样品数量
            # 大类名称
            if str(qs.LargeCategory) == "None":
                sheet.write(row, 6, '')
            else:
                sheet.write(row, 6, qs.LargeCategory)

            # 小类名称
            if str(qs.SmallCategory) == "None":
                sheet.write(row, 7, '')
            else:
                sheet.write(row, 7, qs.SmallCategory)
            sheet.write(row, 8, qs.Name2)  # 商品名称
            sheet.write(row, 9, qs.GoodsStatus)  # 当前状态
            sheet.write(row, 10, qs.Material)  # 材质 第一行 [0-10]

            sheet.write(row, 11, qs.Class)  # 规格
            sheet.write(row, 12, qs.Model)  # 型号
            sheet.write(row, 13, qs.Style)  # 款式
            sheet.write(row, 14, qs.Brand)  # 品牌
            sheet.write(row, 15, qs.Unit)  # 单位
            sheet.write(row, 16, qs.MinPackNum)  # 最小包装数
            sheet.write(row, 17, qs.Weight)  # 重量(G)
            sheet.write(row, 18, qs.BarCode)  # 采购渠道
            sheet.write(row, 19, qs.SupplierName)  # 供应商名称
            sheet.write(row, 20, qs.CostPrice)  # 成本单价(元)
            sheet.write(row, 21, qs.BatchPrice)  # 批发价格(美元) 第2行 [11-21]

            sheet.write(row, 22, qs.RetailPrice)  # '零售价格(美元)
            sheet.write(row, 23, qs.SalePrice)  # 最低售价(美元)'
            sheet.write(row, 24, qs.MaxSalePrice)  # 最高售价(美元)
            sheet.write(row, 25, qs.MarketPrice)  # 市场参考价(美元)
            sheet.write(row, 26, qs.Quantity)  # 数量
            sheet.write(row, 27, qs.Remark)  # 备注
            sheet.write(row, 28, qs.ReportName2)  # 中文申报名
            sheet.write(row, 29, qs.ReportName)  # 英文申报名
            sheet.write(row, 30, qs.DeclaredValue)  # 申报价值(美元)第3行 [22-30]

            sheet.write(row, 31, qs.OriginCountryCode)  # 原产国代码
            sheet.write(row, 32, qs.OriginCountry)  # 原产国
            sheet.write(row, 33, qs.MaxNum)  # 库存上限
            sheet.write(row, 34, qs.MinNum)  # 库存下限
            sheet.write(row, 35, qs.SalerName)  # 业绩归属人1
            sheet.write(row, 36, qs.SalerName2)  # 业绩归属人2
            sheet.write(row, 37, qs.PackingID)  # 包装规格
            sheet.write(row, 38, str(qs.LRTime)[:10])  # 开发日期
            sheet.write(row, 39, qs.SKUStyle1)  # SKU款式1
            sheet.write(row, 40, qs.SKUStyle2)  # SKU款式2第4行 [31-40]

            sheet.write(row, 41, qs.SKUStyle3)  # SKU款式3
            sheet.write(row, 42, qs.SKUDescribe)  # SKU描述
            sheet.write(row, 43, qs.BmpUrl)  # 图片URL
            sheet.write(row, 44, qs.Purchaser)  # 采购员
            sheet.write(row, 45, qs.Storehouse)  # 发货仓库
            sheet.write(row, 46, qs.StockDays)  # 采购到货天数
            sheet.write(row, 47, qs.InnerPrice)  # 内包装成本
            sheet.write(row, 48, qs.LinkUrl)  # 网页URL
            sheet.write(row, 49, qs.LinkUrl2)  # 网页URL2
            sheet.write(row, 50, qs.LinkUrl3)  # 网页URL3  第5行 [41-50]

            sheet.write(row, 51, qs.MinPrice)  # 最低采购价格
            sheet.write(row, 52, qs.HSCODE)  # 海关编码
            sheet.write(row, 53, qs.SellDays)  # 库存预警销售周期
            sheet.write(row, 54, qs.StockMinAmount)  # 采购最小订货量
            sheet.write(row, 55, qs.InLong)  # 内盒长
            sheet.write(row, 56, qs.InWide)  # 内盒宽
            sheet.write(row, 57, qs.InHigh)  # 内盒高
            sheet.write(row, 58, qs.InGrossweight)  # 内盒毛重
            sheet.write(row, 59, qs.InNetweight)  # 内盒净重
            sheet.write(row, 60, qs.OutLong)  # 外箱长
            sheet.write(row, 61, qs.OutWide)  # 外箱宽
            sheet.write(row, 62, qs.OutHigh)  # 外箱高
            sheet.write(row, 63, qs.OutGrossweight)  # 外箱毛重
            sheet.write(row, 64, qs.OutNetweight)  # 外箱净重
            sheet.write(row, 65, qs.ItemUrl)  # 商品URL
            sheet.write(row, 66, qs.PackMsg)  # 包装事项
            sheet.write(row, 67, qs.Electrification)  # 是否带电
            sheet.write(row, 68, qs.GoodsStatus)  # 商品SKU状态
            sheet.write(row, 69, qs.JobPower)  # 工号权限
            sheet.write(row, 70, qs.Season)  # 季节  第6\7行 [51-70]

            sheet.write(row, 71, qs.Powder)  # 是否粉末
            sheet.write(row, 72, qs.Liquid)  # 是否液体
            sheet.write(row, 73, qs.possessMan1)  # 责任归属人1
            sheet.write(row, 74, qs.possessMan2)  # 责任归属人2
            sheet.write(row, 75, qs.ContrabandAttribute)  # 商品属性
            sheet.write(row, 76, qs.DegreeOfDifficulty)  # 包装难度系数
            sheet.write(row, 77, qs.ShopName)  #店铺名称
            sheet.write(row, 78, qs.LinkUrl4)  # 网页URL4
            sheet.write(row, 79, qs.LinkUrl5)  # 网页URL5
            sheet.write(row, 80, qs.LinkUrl6)  # 网页URL6
            sheet.write(row, 81, qs.ShopFreight)  # 店铺运费
            sheet.write(row, 82, qs.PackWeight)  # 包装材料重量
            sheet.write(row, 83, qs.ExchangeRate)  # 汇率
            sheet.write(row, 84, qs.LogisticsPrice)  # 物流公司价格
            sheet.write(row, 85, qs.TransactionFee)  # 交易费
            sheet.write(row, 86, qs.ProfitRate)  # 毛利率
            sheet.write(row, 87, qs.SellingPrice)  # 计算售价

        if len(arrFBA) > 0:
            messages.info(request,u"以下FBASKU：%s 属于建立FBA未提交或不开发FBA，不能导出到execl操作，其他选项已导出。")
        filename = request.user.username + '_' + fbaDateTime.now().strftime('%Y%m%d%H%M%S') + '.xls'
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

    to_export_excel.short_description = u'导出EXCEL'


    list_per_page = 20

    list_display = ( 'DevDate','SKU','LRStaffName','Name2', 'ReportName','ReportName2','Purchaser','CostPrice','Weight','SalerName','Storehouse','showStatus','auditnote')
    list_editable = ('auditnote',)

    def get_list_queryset(self,):
        request = self.request
        qs = super(t_product_enter_FBA_Admin, self).get_list_queryset()

        sku = request.GET.get('SKU', '')
        isflag = request.GET.get('isflag', '')
        DevDateStart = request.GET.get('DevDateStart', '')  # 建资料时间
        DevDateEnd = request.GET.get('DevDateEnd', '')

        searchList = { 'SKU__exact': sku,'isflag__exact': isflag,'DevDate__gte': DevDateStart, 'DevDate__lt': DevDateEnd,}

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
        return qs
