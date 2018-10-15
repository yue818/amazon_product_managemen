# -*- coding: utf-8 -*-
from t_sys_param import t_sys_param

ChoicePackName=8
ChoicePlatformName=24
ChoiceUnit=4
ChoiceCategory2=9
ChoiceIF=10
ChoiceStorehouse=11
ChoiceYNphoto=15
ChoiceMGProcess=17
ChoicePPosition=16
ChoicePZRemake=14
ChoicePublishStatus=12
ChoicePriority=5
ChoiceStatus=6
ChoiceGoodsStatus=18
ChoiceSeason=19
ChoiceIntellectual=2
ChoiceSite=1
ChoiceStatus1=20
ChoiceStatus2=21
ChoiceStatus3=22
ChoiceStatus4=23
ChoiceSelectModifyFields=3
ChoiceState=26
ChoiceLargeCategory=25
ChoiceYN=27
ChoiceStatus_wish=28
ChoiceReviewState =49
ChoiceAbandoned = 30
ChoiceCollar = 31
ChoiceIp = 37
ChoiceDev = 32
ChoiceDealStat = 33
ChoiceItemLoction = 34
ChoiceOrderState=35
ChoiceRegionId=41
ChoiceCloudName=42
ChoiceBindingStatus = 999
ChoiceADStatus = 888
ChoiceOperationState = 890
ChoiceExportState = 891
ChoiceKeyWordsStatus = 889
ChoiceTortDealstatus = 46
ChoicePublish = 998
ChoiceType=44
ChoiceTortYN=301
ChoiceK=50
ChoiceDep=939
ChoiceIPApplication=63
TrackChannel=303
ExternalProductIdType=304
UpdateOrDelete=305
MfgMinimumUnitOfMeasure=306
AmazonVariationTheme=307
ColorMap=308
SizeMap=309
TargetAudienceKeywords=310
ChoiceDepartmentName=311
ChoiceExportState1=1996
ChoiceProductType = 320
ChoiceUploadProductType = 321
ChoiceDistributionResult = 60
ChoiceDistributionType = 61
ChoiceDistributionStatus = 62
ChoiceApplyType = 991
ChoiceFromLanguage = 996
ChoiceToLanguage = 997
ChoiceProcess = 995
ChoiceAPIState = 1000
ChoiceResult = 994
OverSea = 498
OP = 499
PR = 497
ChoiceGoodStatus = 496
ChoiceHandleStatus = 800
ChoiceBStatus = 9999
ChoiceEStatus = 6666
ChoicePlanStatus = 9998
ChoicePurchStatus = 9997
ChoiceDeliveryStatus = 9996
Choicebatchstatus = 9995
ChoiceWarehouse = 6667
Choicebandstate = 6668
ChoiceArrivalStatus = 6669
ChoiceLevel = 7000
ChoiceStorageStatus = 9994
ChoiceCategory = 1997

ChoiceYNDone = 480
ChoiceSupplierID = 485
ChoiceCgStatus = 8800
ChoiceStocking = 313
Condition_t_set_warehouse_storage_situation_list = 10001
Condition_t_stocking_purchase_order              = 10002
Condition_t_stocking_demand_list                 = 10003
Condition_t_shipping_management                  = 10004

ChoiceDeadStatus = 315
Jump_t_set_warehouse_storage_situation_list = 10005
Jump_t_stocking_purchase_order              = 10005
Jump_t_stocking_demand_list                 = 10005
Jump_t_shipping_management                  = 10005
ChoiceOffShelfReason = 6670
ChoiceOffShelfResult = 6671
ChoiceProductnature = 10007
ChoiceTaskOperation = 234
ChoiceFlow = 232
ChoiceDemand = 231
ChoiceCheck = 233
ChoiceSampleState = 10008
ChoiceCgCategory = 8899
Choicecate1 = 20181
Choicecate2 = 20182
Choicecate3 = 20183
ChoiceSiteconfiguration = 350
ChoicedealStatus = 100
ChoiceStoreID = 316
ChoicePurchaser = 955
ChoiceIsCg = 956
ChoiceContraband = 355
ChoiceQualityFeedbackType = 6672
ChoiceQualityFeedbackPlateform = 6673
ChoiceQualityFeedbackState = 6674
ChoiceClothDispatchState = 20185
ChoiceRefundReason = 8875
ChoiceSystemConfirm = 10011
ChoiceShopStatus = 20192
ChoiceNewOld = 20189
Condition_t_weekly_collar_and_publication_statistics_table = 20187
ChoiceRawUnit = 20188
ProductSubtype = 20190
ChoiceSelectCategory = 20191
ChoiceTortLevel = 20193
ChoiceForbiddenSite = 20194
CpcProductState = 20195
ChoiceAutoRenew = 20196
wish_pb_max_budget = 20197
ChoiceCampaignState = 20198
ChioceWishExpressType = 30000
ChoiceNoNeedPurchaseRemark = 30001
ChoiceCgRemark = 12345
ChoiceCgSuggestRemark = 12346
item_weight_unit = 30002
ChoiceWarningFlag = 12347
ChoiceSkuSales = 10101

ChoiceAI = 40000  # 精准调研标记选择  0 默认；1 精准

Choice_examine_status = 40001  # 克重审核 审核状态 0：未审核；1 已审核
ChoiceCheckStatus = 40002 #质检状态 notcheck:未质检  partcheck:抽样质检 allcheck:全部质检

ChoiceIP_FLAG = 40003  # IP产品标记 '0'：非IP产品；'1' 是IP产品
ChoiceAmazonFactory = 40004 #亚马逊服装 yes是 no 不是
ChoiceFBAPlanStatus = 40005  # FBA备货流程状态
ChoiceFBWPlanFBWUS = 40006  # 有 无
ChoiceFBWPlanStatus = 40007  # '未生成清单':'notyet','已生成清单':'genbatch','已生成备货需求':'gendemand','已发货':'deliver','不需备货':'nodemand'
ChoiceRejectFBAStatus = 40008 #转退状态 转仓turn  退货return
ChoicePurchaseType = 40009 #排单类型  首单:firstorder  定做:customermade 其他:other
ChoiceFBWPlanDELIVER = 40010  # 发货方式 '随机':'random','正常':'normal'
ChoiceFBWPlanNEWOLD = 40011  # 新品老品 '新品':'new','老品':'old'

ChoiceAmazonShopType = 40012  # 亚马逊店铺类型：自刊登，跟卖
ChoiceAmazonShopStatus = 40013  # 亚马逊店铺状态


def getChoices(typeid):
    return t_sys_param.objects.values_list('V','VDesc').filter(Type=typeid).order_by('Seq')

ALL_FIELDS = 'id,SKU,MainSKU,Keywords,Keywords2,UpdateTime,StaffID,Name,Name2,Material,Length,Width,'
ALL_FIELDS += 'Height,Weight,SourceURL,PlatformName,PlatformPID,SourcePicPath,SourcePicRemark,ArtPicPath,UnitPrice,Unit,'
ALL_FIELDS += 'MinPackNum,MinOrder,SupplierID,SupplierArtNO,SupplierPColor,SupplierPDes,SupplierPUrl1,SupplierPUrl2,'
ALL_FIELDS += 'OrderDays,StockAlarmDays,SpecialRemark,Remark ,InitialWord,SourceURLPrice,ShelveDay,OrdersLast7Days,SpecialSell,OldSKU,'
ALL_FIELDS += 'Category3,Electrification,Powder,Liquid,Magnetism,PackingID2Num,LWH,Buyer,'
ALL_FIELDS += 'SupplierContact,SourcePicPath2,Storehouse,URLamazon,URLebay,URLexpress,URLwish,Pricerange,NumBought,TotalInventory,'
ALL_FIELDS += 'Tags,SurveyRemark,PackNID,possessMan2,LargeCategory,SmallCategory,ReportName,ReportName2,fromT,PrepackMark,'
ALL_FIELDS += 'CreateTime,CreateStaffName,DYTime,DYStaffName,DYSHTime,DYSHStaffName,XJTime,XJStaffName,KFTime,KFStaffName,'
ALL_FIELDS += 'JZLTime,JZLStaffName,PZTime,PZStaffName,MGTime,MGStaffName,LRTime,LRStaffName '


ALL_FIELDS_TUPLE = ('id','SKU','MainSKU','Keywords','Keywords2','UpdateTime','StaffID','Name','Name2','Material','Length','Width',
                    'Height','Weight','SourceURL','PlatformName','PlatformPID','SourcePicPath','SourcePicRemark','ArtPicPath','UnitPrice','Unit',
                    'MinPackNum','MinOrder','SupplierID','SupplierArtNO','SupplierPColor','SupplierPDes','SupplierPUrl1','SupplierPUrl2',
                    'OrderDays','StockAlarmDays','SpecialRemark','Remark' ,'InitialWord','SourceURLPrice','ShelveDay','OrdersLast7Days','SpecialSell','OldSKU',
                    'Category3','Electrification','Powder','Liquid','Magnetism','PackingID2Num','LWH','Buyer',
                    'SupplierContact','SourcePicPath2','Storehouse','URLamazon','URLebay','URLexpress','URLwish','Pricerange','NumBought','TotalInventory','Tags','SurveyRemark',
                    'PackNID','possessMan2','LargeCategory','SmallCategory','ReportName','ReportName2','fromT','PrepackMark','CreateTime','CreateStaffName',
                    'DYTime','DYStaffName','DYSHTime','DYSHStaffName','XJTime','XJStaffName','KFTime','KFStaffName','JZLTime','JZLStaffName',
                    'PZTime','PZStaffName','MGTime','MGStaffName','LRTime','LRStaffName',
                    )
