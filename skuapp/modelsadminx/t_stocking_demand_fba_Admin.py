# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 王芝杨
 @site: 
 @software: PyCharm
 @file: t_stocking_demand_fba_Admin.py
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
from skuapp.table.t_stocking_demand_fba_detail import t_stocking_demand_fba_detail

class t_stocking_demand_fba_Admin(object):
    search_box_flag = True
    importfile_plugin =True
    fba_tree_menu_flag = True
    hide_page_action = True

    def getHopeNum(self, productSKU):
        try:
            strSql = '''
            		with Goods as 
                    (
                    select  gs.nid  as GoodsSKUID,gs.SKU,g.Purchaser,gs.maxnum,gs.minnum,g.sellDays,
                    gs.CostPrice,g.CostPrice as CostPrice1,gs.GoodsSKUStatus,g.LinkUrl5
                    from B_GoodsSKU(nolock) gs, B_Goods(nolock) g                  
                    where g.NID=gs.GoodsID and g.used=0 
                    ),
                    /*采购未入库数*/--已完全入库订单商品
                    InStoreD as 
                    (  
                    select  om.NID as StockOrderID, m.StoreID, d.GoodsSKUID, sum(d.Amount) as Number   
                    from CG_StockInD(nolock) d    
                    inner join CG_StockInM(nolock) m on d.StockInNID = m.NID and m.StoreID=49  
                    inner  join Goods g on d.GoodsSKUID = g.GoodsSKUID     
                    left join CG_StockOrderM(nolock) om on m.StockOrder = om.BillNumber    
                    where m.CheckFlag = 1 and m.MakeDate > (GETDATE()-365)    
                    group by om.NID, m.StoreID, d.GoodsSKUID
                    ),
                    --未入库商品    
                    UnInStore AS
                    ( 
                    select  d.GoodsSKUID,  m.StoreID,    
                    SUM(case when (d.Amount - isnull(id.Number,0)) <= 0 then null else (d.Amount - isnull(id.Number,0)) end ) as UnInNum   
                    from CG_StockOrderD(nolock) d    
                    inner join Goods g on d.GoodsSKUID = g.GoodsSKUID    
                    left join CG_StockOrderM(nolock) m on d.StockOrderNID = m.NID    
                    left join InStoreD id on d.StockOrderNID = id.StockOrderID and d.GoodsSKUID = id.GoodsSKUID and id.StoreID=m.StoreID    
                    where   m.MakeDate > (GETDATE()-365) and  (m.CheckFlag = 1)--审核通过的订单    
                    and (m.Archive = 0)--不统计归档订单    
                    group by d.GoodsSKUID,m.StoreID
                    ),
                    UnPaiDNum as (
                    SELECT GoodsSKUID, SUM(SaleNum) AS UnPaiDNum,SUM(SalereNum) AS SalereNum, StoreID      
                    FROM (    
                        SELECT gs.GoodsSKUID,     
                        SUM(ptd.L_QTY) AS SaleNum,    
                        SUM(case when pt.RestoreStock=-1 then ptd.L_QTY else 0 end) AS SalereNum,ISNULL(ptd.StoreID,0)AS StoreID    
                        FROM P_TradeDt(nolock) ptd     
                        inner join P_trade(nolock) pt on pt.NID=ptd.TradeNID    
                        inner join Goods gs on gs.SKU=ptd.SKU               
                        WHERE pt.FilterFlag <= 5     
                        GROUP BY gs.GoodsSKUID,ISNULL(ptd.StoreID,0)     
                        UNION all
                        SELECT  gs.GoodsSKUID,     
                        SUM(ptdu.L_QTY) AS SaleNum,    
                        SUM(case when pt.RestoreStock=-1 then ptdu.L_QTY else 0 end) AS SalereNum, ISNULL(ptdu.StoreID,0) AS StoreID    
                        FROM P_TradeDtUn(nolock) ptdu     
                        inner join P_TradeUn(nolock) pt on pt.NID=ptdu.TradeNID     
                        inner join Goods gs on gs.SKU=ptdu.SKU         
                        WHERE pt.FilterFlag = 1                             
                        GROUP BY gs.GoodsSKUID,ISNULL(ptdu.StoreID,0)     
                        ) AS C    
                    GROUP BY GoodsSKUID,StoreID
                    ),
                    --调拨单保存之后的预期入库    
                    StockChange as 
                    (    
                    select cd.GoodsSKUID,sum(cd.amount) as hopenum,cm.StoreInID 
                    from  KC_StockChangeD(nolock) cd     
                    inner join KC_StockChangeM(nolock) cm on cm.nid=cd.StockChangenid and cm.checkflag=0  and cm.StoreInID=49  
                    inner  join Goods g on cd.GoodsSKUID = g.GoodsSKUID        
                    where  cm.MakeDate > (GETDATE()-45)       
                    group by cd.GoodsSKUID,cm.StoreInID 
                    ),
                    --今天实际采购数量
                    PurchaseNum as 
                    (
                     select  d.GoodsSKUID, sum(d.Amount) as Amount,max(m.makedate) as Makedate,max(AudieDate) as AudieDate,
                     case min(m.checkflag) when 1 then '审核通过' when 3 then '作废' else '未审核' end as Checkflag
                     from CG_StockOrderD(nolock) d 
                     inner join CG_StockOrderM(nolock) m 
                     on m.NID=d.StockOrderNID and m.StoreID=49 and m.makedate>=CONVERT(VARCHAR(20),GETDATE()-1,23)+' 16:40:00'
                     group by d.GoodsSKUID
                    ),

                    Result as 
                    (
                    SELECT
                    case when d.KcMaxNum=0 then g.maxnum else d.KcMaxNum end   as 'KcMaxNum',    
                    case when d.KcMinNum=0 then g.minnum else d.KcMinNum end   as 'KcMinNum',    
                    d.SellCount1, d.SellCount2, d.SellCount3, 
                    round((d.SellCount1/7.0+d.SellCount2/15.0+d.SellCount3/30.0)/3.00,2) as 'AvgDayNum', 
                    d.Number , d.ReservationNum, (d.Number-d.ReservationNum) as 'UseNumber',    
                    case when g.CostPrice<>0 then g.CostPrice else g.CostPrice1 end as 'CostPrice', 
                    d.Price,
                    d.Money, 
                    isnull(u.UnInNum,0) as 'NotInStore',
                    d.Number-d.ReservationNum+isnull(u.UnInNum,0)-ISNULL(up.UnPaiDNum,0) + isnull(sc.hopenum,0)+isnull(up.SaleReNum,0) as 'hopeUseNum', 
                    isnull(up.UnPaiDNum,0) as 'UnPaiDNum', 
                    case when     
                     (case when d.KcMaxNum>0 then d.KcMaxNum else g.MaxNum end)    
                     -(d.Number-d.ReservationNum+isnull(up.SaleReNum,0))+    
                     (case when d.KcMinNum>0 then d.KcMinNum else g.MinNum end)    
                     -isnull(u.UnInNum,0)+ISNULL(up.UnPaiDNum,0)<0 then  0     
                     else    
                     (case when d.KcMaxNum>0 then d.KcMaxNum else g.MaxNum end)    
                     -(d.Number-d.ReservationNum+isnull(up.SaleReNum,0))+    
                     (case when d.KcMinNum>0 then d.KcMinNum else g.MinNum end)    
                     -isnull(u.UnInNum,0)+ISNULL(up.UnPaiDNum,0) end  as 'SuggestNum',
                     isnull((select max(DATEDIFF(DAY,Dateadd(hour,8,bb.ORDERTIME), GETDATE()))     
                             from P_TradeDtUn(nolock) aa left join P_TradeUn(nolock) bb on aa.TradeNID = bb.NID      
                             where bb.FilterFlag = 1 and aa.SKU=g.SKU),0) as 'MaxDelayDays',
                     isnull(up.SaleReNum,0) as 'SaleReNum',
                    (SELECT TOP 1 bsl.LocationName FROM B_StoreLocation bsl WHERE bsl.nid = isNull(bgs.LocationID,0) ) AS 'LocationName',
                    IsNull(g.GoodsSKUStatus,'') as GoodsStatus,g.Purchaser, g.SKU,g.LinkUrl5,pnum.Amount,pnum.Checkflag,pnum.Makedate,pnum.AudieDate,
                    round(d.Number * case when IsNull(g.CostPrice,0) <> 0 then g.CostPrice else IsNull(g.CostPrice1,0) end ,2) as 'AllCostPrice',
                            round(cast(d.SellCount1 as float)/nullif(cast(d.SellCount2 as float)-cast(d.SellCount1 as float),0),2) as 'Ratio'
                    From  kc_Currentstock_ExcludeBlacklist d with(nolock)
                    inner join Goods g on d.GoodsSKUID = g.GoodsSKUID and d.StoreID =49    
                    left join UnInStore u on d.GoodsSKUID = u.GoodsSKUID and d.StoreID = u.StoreID
                    left join UnPaiDNum up on up.GoodsSKUID = d.GoodsSKUID and d.StoreID = up.StoreID
                    left join StockChange sc on sc.goodsskuid = d.goodsskuid and sc.storeinid = d.storeid
                    left join B_GoodsSKULocation(nolock) bgs ON g.GoodsSKUID = bgs.GoodsSKUID AND bgs.StoreID =49
                    left join PurchaseNum pnum on d.GoodsSKUID = pnum.GoodsSKUID 
                    where g.SKU='%s'
                    )

                    select KcMaxNum,KcMinNum,SellCount1,SellCount2,SellCount3, Number,ReservationNum,UseNumber,NotInStore,hopeUseNum,UnPaiDNum,SuggestNum,
                    case when AvgDayNum=0.0 then case when hopeUseNum=0.0 then 0.0 when hopeUseNum <0.0 then -99999.0 else 99999.0 end 
                    else round(hopeUseNum/(AvgDayNum*case when Ratio is null then 1 when Ratio>2 then 2 when Ratio=0 then 0.1 else Ratio end),2) end as SaleDay,
                    MaxDelayDays,SaleReNum,LocationName,hopeUseNum-SellCount2 as 'StockDiff15', Ratio,GoodsStatus,Purchaser,SKU,AllCostPrice,
                    round(AvgDayNum*case when Ratio is null then 1 when Ratio>2 then 2 when Ratio=0 then 0.1 else Ratio end,2) as AvgDayNum,
                    isnull(LinkUrl5,'无') as LinkUrl5,isnull(Amount,0) as Amount,isnull(Checkflag,' ') as Checkflag, Makedate, AudieDate
                    from Result ;
            ''' % (productSKU)
            reslut = {'errorcode': -1, 'errortext': '', 'returnConent': ()}
            from brick.pydata.py_syn.py_conn import py_conn
            py_connObj = py_conn()
            sqlServerInfo = py_connObj.py_conn_database()
            if sqlServerInfo['errorcode'] == 0:
                sqlServerInfo['py_cursor'].execute(strSql)
                returnContent = sqlServerInfo['py_cursor'].fetchone()
                if returnContent:
                    reslut['errorcode'] = 0
                    # 库存量、占有量、 未入库量、预计可用数量、未派单量、建议采购数量、可卖天数、日平均销量
                    reslut['returnConent'] = (
                    returnContent[5], returnContent[6], returnContent[8], returnContent[9], returnContent[10],
                    returnContent[11], returnContent[12], returnContent[22])
            else:
                pass
            py_connObj.py_close_conn_database()
        except Exception, ex:
            messages.info(self.request, "获取库存量、占有量、 未入库量、预计可用数量、未派单量、建议采购数量、可卖天数失败,请联系IT解决:%s" % (str(ex)))
            py_connObj.py_close_conn_database()
        return reslut

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

    def show_Status(self, obj):
        try:
            rt = ""
            strStatus = ""
            diffDate = 0
            for status in getChoices(ChoiceFBAPlanStatus):
                if status[0] == obj.Status:
                    strStatus = status[1]
                    break
            if obj.Status == 'notgenpurchase':
                diffDate = (ddtime.now() - obj.Stock_plan_date).days if obj.Stock_plan_date is not None else 0
                flag = 1 if ((obj.Stock_plan_date is not None) and (str(ddtime.now()) > str(obj.Stock_plan_date + tmpDate.timedelta(days=1)))) else 0
                if flag == 1:
                    rt = '<div class="box" style="width: 150px;height: 80px;background-color: red;text-align: center;line-height: 20px;border-radius: 4px"><br>%s<br>超期%s天</div>' % (
                    strStatus, diffDate)
                else:
                    rt = '<div class="box" style="width: 150px;height: 80px;text-align: center;line-height: 20px;border-radius: 4px"><br>%s<br>超期%s天</div>' % (strStatus,diffDate)
            else:
                rt = strStatus
                if obj.Status == 'giveup':
                    strTmp = obj.Remarks if obj.Remarks == u'转退' else "备货"
                    rt = rt + '(' + strTmp + ')'
        except Exception, ex:
            messages.info(self.request,"采购状态加载错误,请联系IT解决:%s"%(str(ex)))
            rt = ""
        return mark_safe(rt)
    show_Status.short_description = mark_safe('<p align="center" style="width:120px;color:#428bca;">采购状态</p>')

    def show_opInfo(self, obj):
        try:
            rt = u'<table border="1"><tr><th>操作员</th><th>告警信息</th><th>操作时间</th></tr>'
            if obj.Status == 'giveup':
                #rt = u'<div style="width:120px"><strong>计划需求人:</strong>%s' % (obj.Demand_people)
                diffDate1 = (obj.giveupDate - obj.Stock_plan_date).days if (obj.Stock_plan_date is not None and obj.giveupDate is not None) else 0
                if diffDate1 > 1:
                    rt = rt + u'<tr style="color:red"><th>需求:%s</th><th> 延迟%s天</th><th>%s</th></tr>'%(obj.Demand_people,diffDate1,obj.Stock_plan_date)
                else:
                    rt = rt + u'<tr style=""><th>需求:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (obj.Demand_people, diffDate1, obj.Stock_plan_date)
                rt = rt + u'<tr style=""><th>废弃:%s</th><th> </th><th>%s</th></tr>' % (obj.giveupMan, obj.giveupDate)
            elif obj.Status == 'notgenpurchase':
                diffDate1 = (ddtime.now() - obj.Stock_plan_date).days if obj.Stock_plan_date is not None else 0
                if diffDate1 > 1:
                    rt = rt + u'<tr style="color:red"><th>需求:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (obj.Demand_people, diffDate1, obj.Stock_plan_date)
                else:
                    rt = rt + u'<tr style=""><th>需求:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (obj.Demand_people, diffDate1, obj.Stock_plan_date)
            rt = rt + "</table>"
        except Exception, ex:
            messages.info(self.request,"操作记录加载错误,请联系IT解决:%s"%(str(ex)))
            rt = ""
        return mark_safe(rt)
    show_opInfo.short_description = mark_safe('<p align="center" style="width:100px;color:#428bca;">操作记录信息</p>')

    list_display = ('Stocking_plan_number','show_Status','Stock_plan_date','Product_nature','ProductSKU','ProductName','Supplier','show_ProductImage','Number','Stocking_quantity','Destination_warehouse','level','Demand_people','AccountNum','neworold','AmazonFactory','show_opInfo')

    fields = ('ProductSKU', 'Stocking_quantity', 'AccountNum', 'Site','Demand_people',
              'Destination_warehouse', 'level','Remarks','Product_nature','ShopSKU','neworold','AmazonFactory')
    list_editable = ('Stocking_quantity',)
    form_layout = (
        Fieldset(u'请认真填写备货需求',
                 Row('ProductSKU', 'Stocking_quantity','Product_nature',),
                 Row('AccountNum', 'Site','Demand_people',),
                 Row('Destination_warehouse', 'level','ShopSKU',),
                 Row('neworold', 'AmazonFactory', '', ),
                 Row('Remarks', '','',),
                 css_class='unsort '
                 ),)

    actions = ['purchasing_plan_audit','get_excel_product_registration_form','not_demand','againdemand','summit_AmazonFactory']

    def not_demand(self,request,objs):
        skuinto = []
        for obj in objs:
            if obj.Status == "notgenpurchase":
                obj.Status = 'giveup' # 未审核
                obj.giveupMan = request.user.first_name
                obj.giveupDate=ddtime.now()
                obj.OplogTime = ddtime.now()
                obj.save()
                t_stocking_demand_fba_detail.objects.filter(Stocking_plan_number=obj.Stocking_plan_number).update(
                    Status='giveup')
            else:
                skuinto.append(obj.ProductSKU)
    not_demand.short_description = u'不需备货'

    def againdemand(self,request,objs):
        skuinto = []
        for obj in objs:
            if obj.Status == "giveup" and obj.Remarks != u"转退":
                obj.Status = 'notgenpurchase' # 未审核
                obj.giveupMan = request.user.first_name
                obj.giveupDate=ddtime.now()
                obj.OplogTime = ddtime.now()
                obj.save()
                t_stocking_demand_fba_detail.objects.filter(Stocking_plan_number=obj.Stocking_plan_number).update(
                    Status='notgenpurchase')
            else:
                skuinto.append(obj.ProductSKU)
        if len(skuinto) > 0:
            messages.info(request,u'以下SKU:%s,不能重新生成备货'%(skuinto))
    againdemand.short_description = u'重新生成备货'

    def purchasing_plan_audit(self,request,objs):
        skuinto = []
        for obj in objs:
            if obj.Status == "notgenpurchase":
                obj.Status = 'notpurchase' # 生成采购计划未采购
                obj.genPurchasePlanMan = request.user.first_name
                obj.genPurchasePlanDate=ddtime.now()
                obj.OplogTime = ddtime.now()
                obj.save()

                t_stocking_demand_fba_detail.objects.filter(Stocking_plan_number=obj.Stocking_plan_number).update(
                    Status='notpurchase')
            else:
                skuinto.append(obj.ProductSKU)
        if len(skuinto) > 0:
            messages.info(request,"以下商品：%s 已生成采购计划，不需要再生成。"%(str(skuinto)))
    purchasing_plan_audit.short_description = u'生成采购计划'

    def get_excel_product_registration_form(self,request,objs):
        from app_djcelery.tasks import fba_product_registration_form_excel_task
        getexcel = []
        for obj in objs:
            ProductPrice = obj.ProductPrice
            if obj.ProductPrice is None:
                ProductPrice = '0'
            ProductWeight = obj.ProductWeight
            if obj.ProductWeight is None:
                ProductWeight = '0'
            objlist = [obj.ProductName,obj.ProductSKU,obj.ProductSKU,'%.2f'%(float(ProductPrice)/6.5),
                       '','','USD','',u'包裹','zh','',float(ProductWeight)/1000,'','',3,0]
            getexcel.append(objlist)
            #fba_product_registration_form_excel_task.delay(getexcel,request.user.username)
            fba_product_registration_form_excel_task(getexcel, request.user.username)
        messages.success(request,u'请稍后到“下载中心”，下载文件。。。')
    get_excel_product_registration_form.short_description = u'导出商品注册表'


    def summit_AmazonFactory(self,request,objs):
        try:
            cursor = hqdb_conn.cursor()
            listProductSKU = []
            insertinto = []
            sucessInfo = []
            FBAList = []
            for obj in objs:
                Number = 0 if obj.Number is None else obj.Number
                if obj.ProductSKU[:4] == "FBA-":
                    FBAList.append(obj.ProductSKU)
                    continue
                if obj.Status == "notgenpurchase"  and  obj.AmazonFactory == "yes" and int(Number) < int(obj.Stocking_quantity):
                    strSql = '''
                        SELECT a.BmpUrl,a.SKU,a.TortInfo,a.GoodsStatus,a.Purchaser,a.SalerName2,a.SellCount1,a.SellCount2,a.SellCount3,a.UseNumber,
                        ifnull(c.OnlineNotIn,0)+a.NotInStore as NotInStore,a.CostPrice,
                        aa.SuggestNum*a.SellCount1-a.Number-a.NotInStore-ifnull(c.OnlineNotIn,0) as SuggestNum,
                        ifnull(c.OnlineNotIn,0)+a.hopeUseNum as hopeUseNum,
                        a.UnPaiDNum,a.ReservationNum,a.Number,a.GoodsName,a.SupplierName,a.Model,
                        (a.hopeUseNum+ifnull(c.OnlineNotIn,0))/a.AverageNumber as SaleDay,
                        a.CgCategory,a.AverageNumber, 
                        if(((a.hopeUseNum+ifnull(c.OnlineNotIn,0))/a.AverageNumber)<=aa.SuggestMin,1,2) as flag,aa.OSCode
                        FROM py_db.kc_currentstock_sku a inner join py_db.kc_currentstock_sku_oscode aa on a.SourceOSCode=aa.OSCode and aa.OSCode in ('OS906')
                        left join ( select SKU, SUM(if(currentState=22,productNumbers - completeNumbers, ifnull(completeNumbers,productNumbers))) AS OnlineNotIn
                                                from t_cloth_factory_dispatch 
                                                where currentState in (20,22)
                                                group by SKU) c on a.SKU=c.SKU
                        where a.sku='%s' and  a.SupplierName in ('广州工厂','易臻工厂','马俊杰') and a.used=0 and a.storeID = 1 ;
                        '''%(obj.ProductSKU)
                    cursor.execute(strSql)
                    tuppleKcCurrent = cursor.fetchone()

                    if tuppleKcCurrent:
                        # 获取FBA和非FBA 7天销量、15天销量、30天销量 累计
                        sevenSales = tuppleKcCurrent[6]
                        fifteenSales = tuppleKcCurrent[7]
                        thirtySales = tuppleKcCurrent[8]
                        FBASKU = "FBA-" + obj.ProductSKU
                        if len(FBASKU) > 0:
                            strSql = "select sellcount1,sellcount2,sellcount3 from py_db.kc_currentstock_sku where sku='%s' and storeID=2;"%(FBASKU)
                            cursor.execute(strSql)
                            tuppleNoSKUCurrent = cursor.fetchone()
                            if tuppleNoSKUCurrent:
                                sevenSales = sevenSales + tuppleNoSKUCurrent[0]
                                fifteenSales = fifteenSales + tuppleNoSKUCurrent[1]
                                thirtySales = thirtySales + tuppleNoSKUCurrent[2]

                        getOtherInfo = self.getHopeNum(obj.ProductSKU) # 库存量、占有量、 未入库量、预计可用数量、未派单量、建议采购数量、可卖天数、日平均销量
                        stockNum =tuppleKcCurrent[16]
                        occupyNum = tuppleKcCurrent[15]
                        PurchaseNotInNum = tuppleKcCurrent[10]
                        ailableNum = tuppleKcCurrent[13]
                        oosNum = tuppleKcCurrent[14]
                        SuggestNum = tuppleKcCurrent[12]
                        SaleDay = tuppleKcCurrent[20]
                        AverageNumber = tuppleKcCurrent[22]
                        if getOtherInfo['errorcode'] != -1:
                            stockNum = getOtherInfo['returnConent'][0]
                            occupyNum = getOtherInfo['returnConent'][1]
                            PurchaseNotInNum = getOtherInfo['returnConent'][2]
                            ailableNum = getOtherInfo['returnConent'][3]
                            oosNum = getOtherInfo['returnConent'][4]
                            SuggestNum = getOtherInfo['returnConent'][5]
                            SaleDay = getOtherInfo['returnConent'][6]
                            AverageNumber = getOtherInfo['returnConent'][7]

                        strInsert = '''
                            INSERT INTO t_cloth_factory_dispatch(BmpUrl,SKU,TortInfo,goodsState,buyer,SalerName2,sevenSales,fifteenSales,thirtySales,
                                UseNumber,PurchaseNotInNum,goodsCostPrice,SuggestNum,ailableNum,oosNum,occupyNum,stockNum,goodsName,Supplier,girard,SaleDay,
                                goodsclass,AverageNumber,flag,OSCode,Stocking_plan_number,createDate) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,date_add(NOW(),interval 1 day))
                        '''
                        param = (tuppleKcCurrent[0],tuppleKcCurrent[1],tuppleKcCurrent[2],tuppleKcCurrent[3],tuppleKcCurrent[4],tuppleKcCurrent[5],sevenSales,fifteenSales,thirtySales,
                                 tuppleKcCurrent[9],PurchaseNotInNum,tuppleKcCurrent[11],obj.Stocking_quantity,ailableNum,oosNum,occupyNum,stockNum,tuppleKcCurrent[17],tuppleKcCurrent[18],tuppleKcCurrent[19],SaleDay,
                                 tuppleKcCurrent[21],AverageNumber,tuppleKcCurrent[23],tuppleKcCurrent[24],obj.Stocking_plan_number)
                        cursor.execute(strInsert,param)

                        obj.OplogTime = ddtime.now()
                        obj.Status = 'purchasing'  # 计划已生成，未采购
                        obj.genPurchasePlanDate = ddtime.now()  # 生成采购计划时间
                        obj.genPurchasePlanMan = request.user.first_name  # 生成采购计划人
                        obj.recordPurchaseCodeMan = request.user.first_name
                        obj.recordPurchaseCodeDate = ddtime.now()
                        obj.TransFactory = 'yes'
                        obj.save()

                        sucessInfo.append(obj.ProductSKU)
                        cursor.execute("commit")

                        t_stocking_demand_fba_detail.objects.filter(Stocking_plan_number=obj.Stocking_plan_number).update(Status='purchasing')
                    else:
                        listProductSKU.append(obj.ProductSKU)
                else:
                    listProductSKU.append(obj.ProductSKU)
            if listProductSKU:
                messages.info(request,"商品SKU:%s,不能提交供应链服装采购;原因：非亚马逊服装、服装排单流程存在未审核记录、在库存表未关联到商品SKU或者浦江库存数量>采购数量(生成采购计划进行调拨处理)."%(listProductSKU))
            if FBAList:
                messages.info(request,"商品SKU:%s,不能带前缀FBA提交供应链服装采购,请重新去除前缀FBA-提交备货需求."%(FBAList))
            cursor.close()
            if sucessInfo:
                messages.success(request, '商品SKU:%s,已流转供应链服装采购，可在[4-采购计划]中查看处理进度.'%(sucessInfo))
        except Exception, ex:
            messages.error(request,"提交到供应链服装采购错误,请联系IT解决:%s"%(str(ex)))
    summit_AmazonFactory.short_description = u'提交供应链服装采购'

    def save_models(self,):
        try:
            from django.contrib.auth.models import User
            userID = [each.id for each in User.objects.filter(groups__id__in=[65])]
            #if request.user.is_superuser or request.user.id in userID:
            if self.request.user.id in userID:
                obj = self.new_obj
                request = self.request

                old_obj = None

                if obj is None or obj.id is None or obj.id <= 0:
                    pass
                else:
                    old_obj = self.model.objects.get(pk=obj.pk)
                obj.save()

                obj.Stocking_plan_number = ddtime.now().strftime('%Y%m%d%H%M%S') + '_' + str(obj.id)
                obj.Stock_plan_date      = ddtime.now()
                obj.OplogTime            = ddtime.now()
                obj.QTY = obj.Stocking_quantity
                from brick.classredis.classsku import classsku
                classskuObj = classsku()
                Number =  classskuObj.get_number_by_sku(obj.ProductSKU)
                obj.Number = 0 if (Number is None or Number=='') else Number

                if obj.Demand_people is None or obj.Demand_people.strip() == "":
                    obj.Demand_people = request.user.first_name

                py_b_goods_objs = py_b_goods.objects.filter(SKU=obj.ProductSKU)
                if py_b_goods_objs.exists():
                    obj.ProductImage = u'http://fancyqube.net:89/ShopElf/images/%s.jpg'%py_b_goods_objs[0].SKU.replace('OAS-','').replace('FBA-','')
                    obj.ProductName  = py_b_goods_objs[0].GoodsName
                    obj.ProductPrice = py_b_goods_objs[0].CostPrice
                    obj.ProductWeight= py_b_goods_objs[0].Weight
                    obj.Supplierlink = py_b_goods_objs[0].LinkUrl

                    py_b_Supplier_objs = py_b_Supplier.objects.filter(NID=py_b_goods_objs[0].SupplierID)
                    if py_b_Supplier_objs.exists():
                        obj.Supplier     = py_b_Supplier_objs[0].SupplierName

                obj.Buyer = ''

                obj.Status = u'notgenpurchase' # 未生成采购计划

                obj.save()

                #插入详细信息表
                insertSKU = []
                insertSKU.append(t_stocking_demand_fba_detail(ProductSKU=obj.ProductSKU, Stocking_plan_number=obj.Stocking_plan_number,
                                                              CreateDate=ddtime.now(), Status='notgenpurchase',AuditFlag=0))
                t_stocking_demand_fba_detail.objects.bulk_create(insertSKU)
            else:
                messages.error(self.request, "无权限操作。")
        except Exception, ex:
            messages.info(self.request,"保存报错:%s"%(str(ex)))

    def get_list_queryset(self):
        request = self.request
        
        qs = super(t_stocking_demand_fba_Admin, self).get_list_queryset()

        from django.contrib.auth.models import User
        userID = [each.id for each in User.objects.filter(groups__id__in=[65])]
        # if request.user.is_superuser or request.user.id in userID:
        if request.user.id in userID:
            qs = qs.filter(Demand_people=request.user.first_name)
        Status = request.GET.get('Status', '')  # 采购状态
        Stocking_plan_number = request.GET.get('Stocking_plan_number', '')   #备货计划号
        Stock_plan_dateStart      = request.GET.get('Stock_plan_dateStart', '')     # 备货计划时间
        Stock_plan_dateEnd      = request.GET.get('Stock_plan_dateEnd', '')     # 备货计划时间
        Demand_people = request.GET.get('Demand_people', '')             # 计划需求人
        Product_nature = request.GET.get('Product_nature', '')            #产品性质
        ProductSKU = request.GET.get('ProductSKU', '')                     #商品sku
        ProductName = request.GET.get('ProductName', '')                    # 商品名称
        ProductWeightStart = request.GET.get('ProductWeightStart', '')
        ProductWeightEnd = request.GET.get('ProductWeightEnd', '')                #商品克重
        Supplier = request.GET.get('Supplier', '')                         # 供应商
        AccountNum = request.GET.get('AccountNum', '')                     # 帐号
        Destination_warehouse = request.GET.get('Destination_warehouse', '')# 目的地仓库
        level = request.GET.get('level', '')                                # 紧急程度
        Buyer = request.GET.get('Buyer', '')                                #采购人

        neworold = request.GET.get('neworold', '')  # 新品备货
        OplogTimeStart = request.GET.get('OplogTimeStart','')  #记录生成时间
        OplogTimeEnd =request.GET.get('OplogTimeEnd','') #记录生成时间
        AmazonFactory = request.GET.get('AmazonFactory', '')  # 是否亚马逊服装


        searchList = {
                        'Stocking_plan_number__exact':Stocking_plan_number,
                        'Stock_plan_date__gte':Stock_plan_dateStart,'Stock_plan_date__lt':Stock_plan_dateEnd,
                        'Demand_people__exact':Demand_people,'Product_nature__exact':Product_nature,
                        'ProductSKU__icontains': ProductSKU,'ProductName__exact':ProductName,
                        'ProductWeight__gte':ProductWeightStart,
                        'ProductWeight__lt':ProductWeightEnd,
                        'Supplier__exact':Supplier,
                        'AccountNum__exact':AccountNum,
					    'Destination_warehouse__exact': Destination_warehouse,
                        'level__exact':level,
                        'Buyer__exact':Buyer,
                        'Status__exact':Status,
                        'OplogTime__gte':OplogTimeStart,'OplogTime__lt':OplogTimeEnd,
                        'neworold__exact': neworold,'AmazonFactory__exact':AmazonFactory,
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

