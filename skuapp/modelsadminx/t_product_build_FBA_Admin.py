# -*- coding: utf-8 -*-
from datetime import datetime
import time
from skuapp.table.t_product_build_FBA import t_product_build_FBA
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field, Div, FormActions, Submit, Button, ButtonHolder, InlineRadios, Reset, StrictButton, HTML, Hidden, Alert
from django.contrib import messages
import sys
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect
import copy
import pymssql

class t_product_build_FBA_Admin(object):
    search_box_flag = True
    show_product_build_FBAPlugin = True
    list_per_page = 20
    actions = ['updateInfoToNext',]

    '''
    说明：修改表t_product_build_fba  FBA建资料流程到FBA信息录入流程
    '''
    def updateInfoToNext(self,request, queryset):
        for querysetid in queryset.all():
            # 下一步
            obj = t_product_build_FBA()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.LRStaffName = str(request.user.first_name)
            obj.LRTime = datetime.now()
            obj.isflag = 1
            obj.save()

        return HttpResponseRedirect("/Project/admin/skuapp/t_product_build_fba?flag=1")
    updateInfoToNext.short_description = u'下一步 FBA-信息录入'

    list_display = ( 'SKU','Name2','GoodsStatus','CostPrice','ReportName', 'ReportName2','Purchaser','SalerName','Weight','Storehouse',)
    # 分组表单
    '''
    fields = ('OldSKU','MainSKU','SKU','LargeCategory', 'SmallCategory','Name2','GoodsStatus','Material', 'Model','Brand','Unit','MinPackNum','Weight',
              'SupplierName','CostPrice','Remark','ReportName2','ReportName','DeclaredValue','OriginCountryCode','OriginCountry','MaxNum','MinNum','SalerName',
              'SalerName2','PackingID','DevDate','Purchaser','Storehouse','StockDays','InnerPrice','LinkUrl','LinkUrl2','SellDays','StockMinAmount','Electrification',
              'Powder','Liquid','possessMan1','possessMan2','ContrabandAttribute','DegreeOfDifficulty','ShopName','LinkUrl4','LinkUrl5','LinkUrl6','ShopFreight',
              'PackWeight','ExchangeRate','LogisticsPrice','TransactionFee','ProfitRate','SellingPrice',)
    '''
    fields = ('OldSKU','SKU','Name2','GoodsStatus','CostPrice','ReportName', 'ReportName2','Purchaser','SalerName','Weight','Storehouse','DevDate',)
    form_layout = (
        Fieldset(u'查询条件',
                 Row('OldSKU'),
                 css_class='unsort '
                 ),
        Fieldset(u'普源关联FBA内容',
                 Row('SKU','Name2','GoodsStatus','CostPrice',),
                 Row('ReportName', 'ReportName2','Purchaser','SalerName',),
                 Row('Weight','Storehouse','DevDate',),
                 css_class='unsort ',
                 ),
        '''
        Fieldset(u'普源关联FBA其他内容',
                 Row('MainSKU', 'LargeCategory', 'SmallCategory', 'Material', ),
                 Row('Model', 'Brand', 'Unit', 'MinPackNum', ),
                 Row('SupplierName', 'DeclaredValue', 'OriginCountryCode', 'OriginCountry', ),
                 Row('MaxNum', 'MinNum', 'OriginCountryCode', 'OriginCountry', ),
                 Row('SalerName2', 'PackingID','DevDate','StockDays', ),
                 Row('InnerPrice', 'LinkUrl', 'LinkUrl2', 'SellDays', ),
                 Row('StockMinAmount', 'Electrification', 'Powder', 'Liquid', ),
                 Row('possessMan1', 'possessMan2', 'ContrabandAttribute', 'DegreeOfDifficulty', ),
                 Row('ShopName', 'LinkUrl4', 'LinkUrl5', 'LinkUrl6', ),
                 Row('ShopFreight', 'PackWeight', 'ExchangeRate', 'LogisticsPrice', ),
                 Row('TransactionFee','ProfitRate','SellingPrice','Remark' ),
                 css_class='unsort '
                 ),
        '''
    )

    def save_models(self):
        obj = self.new_obj
        obj.save()
        request = self.request
        obj.LRStaffName = request.user.first_name
        obj.LRTime = datetime.now()
        obj.save()

    '''
    说明：1、商品SKU拼接字符串查询mysql数据库是否已存在流程FBA建资料或FBA录入中（如果存在不重复做）
         2、商品SKU+FBA字符串查看普元数据库是否已建立（如果已建立不需要再做）
         3、把1、2两个都过滤出来的数据录入t_product_build_fba建资料表中
    参数：skuList：商品 
    返回：return_existFBA：普元存在FBA建资料SKU, return_notexistFBA：普元不存在FBA建资料SKU,existCurTab：建资料流程中已存在的SKU
    '''
    def getPyGoodsInfo(self,skuList):
        # 根据子SKU获取普源商品信息
        reload(sys)
        sys.setdefaultencoding('utf8')
        request = self.request

        conn = pymssql.connect(host='122.226.216.10', user='fancyqube', password='K120Esc1',database='ShopElf',port='18793')
        cursor = conn.cursor()
        return_value = {}
        return_existFBA = []
        return_notexistFBA = []

        tmpList = []
        existCurTab = []
        for rowInfo in skuList:
            t_product_build_FBA_objs = t_product_build_FBA.objects.filter(OldSKU=rowInfo)
            if len(t_product_build_FBA_objs) == 0:
                tmpList.append(rowInfo)
            else:
                existCurTab.append(rowInfo)
        del skuList[:]
        skuList = []
        skuList = copy.deepcopy(tmpList)
        if len(skuList) == 0:
            cursor.close()
            conn.close()
            return return_existFBA, return_notexistFBA,existCurTab
        strSKU = "'"
        strFBASKU = "'"
        for rowInfo in skuList:
            strSKU = strSKU + str(rowInfo) + "','"
            strFBASKU = strFBASKU + "FBA-" + str(rowInfo) + "','"
        if len(strSKU) > 2:
            strSKU = strSKU[:-2]
        if len(strFBASKU) > 2:
            strFBASKU = strFBASKU[:-2]
            str_b_goods = "select sku from b_goods where sku in (%s)" % (strFBASKU)
            cursor.execute(str_b_goods)
            objSkus = cursor.fetchall()
            for objRow in objSkus:
                return_existFBA.append(objRow[0])
                tmpSubSKU = str(objRow[0])[4:]
                n = skuList.index(tmpSubSKU)
                if n >= 0 :
                    del skuList[n]

            if len(skuList) == 0:
                cursor.close()
                conn.close()
                return return_existFBA,return_notexistFBA,existCurTab
            else:
                sql = '''select  bg.goodscode as '商品编码0',bg.sku as 'SKU1',convert(nvarchar(64), bg.GoodsName) as '商品名称2',
                            convert(nvarchar(20), bg.GoodsStatus) as '当前状态3',convert(nvarchar(20), bg.Material) as '材质4',
                            convert(nvarchar(20), bg.Model) as '型号5',convert(nvarchar(20), bg.Brand) as '品牌6',bg.Unit as '单位7',
                            bg.PackageCount as '最小包装数8',bg.Weight as '重量9',bs.SupplierName as '供应商名称10' ,bg.CostPrice as '成本单价(元)11',
                            bg.Notes as '备注12',convert(nvarchar(32), bg.AliasCnName) as '中文申报名13',bg.AliasEnName as '英文申报名14',
                            bg.DeclaredValue as '申报价值(美元)15',bg.OriginCountryCode as '原产国代码16',convert(nvarchar(20), bg.OriginCountry) as '原产国17',
                            bg.MaxNum as '库存上限18',bg.MinNum as '库存下限19',convert(nvarchar(20), bg.SalerName) as '业绩归属人120',
                            convert(nvarchar(20), bg.SalerName2) as '业绩归属人221',bg.PackName as '包装规格22',bg.DevDate as '开发日期23',
                            convert(nvarchar(20), bg.Purchaser) as '采购员24',bg.StockDays as '采购到货天数25',bg.PackFee as '内包装成本26',bg.LinkUrl as '网页URL27',
                            bg.LinkUrl2 as '网页URL228',bg.SellDays as '库存预警销售周期29',bg.StockMinAmount as '采购最小订货量30',
                            bg.IsCharged as '是否带电31',bg.IsPowder as '是否粉末32',bg.IsLiquid as '是否液体33',
                            convert(nvarchar(20),bg.possessMan1) as '责任归属人134',convert(nvarchar(20),bg.possessMan2) as '责任归属人235',
                            (SELECT
									AttributeName + ';'
								FROM
									B_GoodsAttribute
								WHERE
									GoodsID = bg.nid FOR XML PATH ('')
							) AS '商品属性36',
							bg.PackingRatio as '包装难度系数37','' as '店铺名称38',bg.LinkUrl4 as '网页URL439',bg.LinkUrl5 as '网页URL540',
							bg.LinkUrl6 as '网页URL641',bg.ShopCarryCost as '店铺运费42',bg.PackWeight as '包装材料重量43',ExchangeRate as '汇率44',
							FreightRate as '物流公司价格45','' as '交易费46','' AS  '毛利率47','' as '计算售价48' ,convert(nvarchar(20),bgc.CategoryName) as '大类名称49',
							convert(nvarchar(20),bgc.CategoryName) as '小类名称50',bg.MultiStyle as '多款式51',bg.SampleFlag as '是否有样品52',bg.SampleCount as '样品数量53',
							bg.Class as '规格54',bg.Style as '款式55',bg.BarCode as '采购渠道56',bg.BatchPrice as '批发价格(美元)57',bg.RetailPrice as '零售价格(美元)58',
							bg.SalePrice as '最低售价(美元)59',bg.MaxSalePrice as '最高售价(美元)60',bg.MarketPrice as '市场参考价(美元)61',bg.Quantity as '数量62',
							'' as 'SKU款式163','' as 'SKU款式264','' as 'SKU款式365','' as 'SKU描述66',bg.BmpUrl as '图片URL67',
							bg.LinkUrl3 as '网页URL368',bg.MinPrice as '最低采购价格69',bg.HSCODE as '海关编码70',bg.InLong as '内盒长71',bg.InWide as '内盒宽72',
							bg.InHigh as '内盒高73',bg.InGrossweight as '内盒毛重74',bg.InNetweight as '内盒净重75',bg.OutLong as '外箱长76',bg.OutWide as '外箱宽77',
							bg.OutHigh as '外箱高78',bg.OutGrossweight as '外箱毛重79',bg.OutNetweight as '外箱净重80',bg.ItemUrl as '商品URL81',bg.PackMsg as '包装事项82','' as '工号权限83',
							bg.Season as '季节84',bgc.CategoryLevel as '类别等级85',bgc.CategoryParentID as '大类ID86'
                            from b_goods(nolock) bg left JOIN b_supplier(nolock) bs on bg.SupplierID = bs.nid
							left join B_GoodsCats(nolock) bgc on bg.CategoryCode = bgc.CategoryCode
                            where bg.sku in(%s)
                             '''%(strSKU)
                cursor.execute(sql)
                objs = cursor.fetchall()
                for objRow in objs:
                    strLargeName = objRow[49]
                    if objRow[85] is not None and str(objRow[85]) == "2" and objRow[86] is not None and str(objRow[86]) != "0":
                        strCatSql = "select CategoryName from B_GoodsCats(nolock) where NID=%s"%(objRow[86])
                        cursor.execute(strCatSql)
                        LargeName = cursor.fetchone()
                        if LargeName:
                            strLargeName = LargeName[0]
                    return_notexistFBA.append(objRow[1])
                    obj = t_product_build_FBA()
                    obj.save()
                    obj.SKU = "FBA-" + str(objRow[1])
                    obj.OldSKU = str(objRow[1])
                    obj.LargeCategory = strLargeName
                    obj.SmallCategory = objRow[50]
                    obj.Name2 = str(objRow[2])
                    obj.ReportName = str(objRow[14])
                    obj.ReportName2 = str(objRow[13])
                    obj.GoodsStatus = str(objRow[3])
                    obj.Purchaser = str(objRow[24])
                    obj.CostPrice = objRow[11]
                    obj.Weight = objRow[9]
                    obj.SalerName = objRow[20]
                    obj.Storehouse = u'亚马逊仓库'
                    obj.MainSKU = objRow[0]
                    obj.Material = objRow[4]
                    obj.Model = objRow[5]
                    obj.Brand = objRow[6]
                    obj.Unit = objRow[7]
                    obj.MinPackNum = objRow[8]
                    obj.SupplierName = objRow[10]
                    obj.Remark = objRow[12]
                    obj.DeclaredValue = objRow[15]
                    obj.OriginCountryCode = objRow[16]
                    obj.OriginCountry = objRow[17]
                    obj.MaxNum = objRow[18]
                    obj.MinNum = objRow[19]
                    obj.SalerName2 = objRow[21]
                    obj.PackingID = objRow[22]
                    obj.DevDate = str(datetime.now())[:10]
                    obj.Purchaser = objRow[24]
                    obj.StockDays = objRow[25]
                    obj.InnerPrice = objRow[26]
                    obj.LinkUrl = objRow[27]
                    obj.LinkUrl2 = objRow[28]
                    obj.SellDays = objRow[29]
                    obj.StockMinAmount = objRow[30]
                    obj.Electrification = objRow[31]
                    obj.Powder = objRow[32]
                    obj.Liquid = objRow[33]
                    obj.possessMan1 = objRow[34]
                    obj.possessMan2 = objRow[35]
                    obj.ContrabandAttribute = objRow[36]
                    obj.DegreeOfDifficulty = objRow[37]
                    obj.ShopName =objRow[38]
                    obj.LinkUrl4 = objRow[39]
                    obj.LinkUrl5 = objRow[40]
                    obj.LinkUrl6 = objRow[41]
                    obj.ShopFreight = objRow[42]
                    obj.PackWeight = objRow[43]
                    obj.ExchangeRate = objRow[44]
                    obj.LogisticsPrice = objRow[45]
                    obj.TransactionFee = 0
                    obj.ProfitRate = 0
                    obj.SellingPrice = 0
                    obj.isflag = 0
                    obj.MultiStyle = objRow[51]
                    obj.SampleFlag = objRow[52]
                    obj.SampleCount = objRow[53]
                    obj.Class = objRow[54]
                    obj.Style = objRow[55]
                    obj.BarCode = objRow[56]
                    obj.BatchPrice = objRow[57]
                    obj.RetailPrice = objRow[58]
                    obj.SalePrice = objRow[59]
                    obj.MaxSalePrice = objRow[60]
                    obj.MarketPrice = objRow[61]
                    obj.Quantity = objRow[62]
                    obj.SKUStyle1 = objRow[63]
                    obj.SKUStyle2 = objRow[64]
                    obj.SKUStyle3 = objRow[65]
                    obj.SKUDescribe = objRow[66]
                    obj.BmpUrl = objRow[67]
                    obj.LinkUrl3 = objRow[68]
                    obj.MinPrice = objRow[69]
                    obj.HSCODE = objRow[70]
                    obj.InLong = objRow[71]
                    obj.InWide = objRow[72]
                    obj.InHigh = objRow[73]
                    obj.InGrossweight = objRow[74]
                    obj.InNetweight = objRow[75]
                    obj.OutLong = objRow[76]
                    obj.OutWide = objRow[77]
                    obj.OutHigh = objRow[78]
                    obj.OutGrossweight = objRow[79]
                    obj.OutNetweight = objRow[80]
                    obj.ItemUrl = objRow[81]
                    obj.PackMsg = objRow[82]
                    obj.JobPower = objRow[83]
                    obj.Season = objRow[84]
                    obj.save()
        cursor.close()
        conn.close()
        if len(return_notexistFBA) == 0:
            messages.info(request,"商品SKU:%s 在普元未关联到！"%(str(skuList)))
        return return_existFBA, return_notexistFBA,existCurTab

    '''
    说明：根据选中处理主SKU，在主SKU与商品SKU对应，生成商品SKU列表、商品SKU字符串、商品SKU+FBA字符串
    返回：getPyGoodsInfo函数调用结果
    '''
    def dealMainSku(self,skuList):
        request = self.request
        from skuapp.table.t_product_mainsku_sku import t_product_mainsku_sku
        subSkuList = []
        notExistMainSKU = []
        for rowInfo in skuList:
            t_product_mainsku_sku_objs = t_product_mainsku_sku.objects.filter(MainSKU=rowInfo)
            if len(t_product_mainsku_sku_objs) == 0:
                notExistMainSKU.append(rowInfo)
            for t_product_mainsku_sku_objs_row in t_product_mainsku_sku_objs:
                subSkuList.append(t_product_mainsku_sku_objs_row.ProductSKU)

        if len(notExistMainSKU) > 0:
            messages.info(request, "主SKU:%s 不存在"%(str(notExistMainSKU)))
        return self.getPyGoodsInfo(subSkuList)

    def get_list_queryset(self,):
        #获取子SKU
        request = self.request
        sku = request.GET.get('OldSKU', '')
        strSelFlag = request.GET.get('selFlag', '')
        if sku != "" :
            skuList = []
            skuList = sku.split(",")
            #多个子SKU
            return_existFBA = []
            return_notexistFBA = []
            existCurTab = []
            if strSelFlag != "" and int(strSelFlag) == 2:
                return_existFBA, return_notexistFBA,existCurTab = self.getPyGoodsInfo(skuList)
            else:
                return_existFBA, return_notexistFBA,existCurTab = self.dealMainSku(skuList)

            if len(return_existFBA) > 0 and strSelFlag != "" and int(strSelFlag) == 2:
                messages.info(request,u"以下商品SKU:%s 在普元已经建立FBA流程，请勿重复建立"%(return_existFBA))
            elif len(return_existFBA) > 0 and strSelFlag != "" and int(strSelFlag) == 1:
                messages.info(request, u"主SKU中包含的商品SKU:%s 在普元已经建立FBA流程，请对未建立的建立FBA流程" % (return_existFBA))
            elif len(existCurTab) > 0  and strSelFlag != "":
               messages.info(request, u"以下商品SKU:%s 该商品已在[FBA-录入流程]，请在[FBA-录入流程]查看" % (existCurTab))

        qs = super(t_product_build_FBA_Admin, self).get_list_queryset()

        return qs.filter(isflag = 0)
