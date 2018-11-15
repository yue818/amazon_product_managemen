# -*- coding: utf-8 -*-
"""
 @desc:
 @author: wangzhiyang
 @site:
 @software: PyCharm
 @file: t_cloth_factory_dispatch_needpurchase.py
 @time: 2018/4/28 8:53
"""
from django.db import models
from public import getChoices,ChoiceClothDispatchState,ChoiceRawUnit,ChoiceSelectCategory,ChoicePurchaseType

def getFactory():
    from t_cloth_factory import t_cloth_factory
    return  t_cloth_factory.objects.values_list('name','value')
#API指令执行计划完成表
class t_cloth_factory_dispatch_needpurchase(models.Model):
    id = models.AutoField(u'业务流水号', primary_key=True)
    SKU = models.CharField(u'商品SKU', max_length=32)
    goodsName = models.CharField(u'商品名称', max_length=256, blank=True, null=True)
    Supplier = models.CharField(u'供应商', max_length=64, blank=True, null=True)
    goodsState = models.CharField(u'商品状态', max_length=32, blank=True, null=True)
    goodsCostPrice = models.DecimalField(u'商品成本单价', max_digits=10, decimal_places=2, blank=True, null=True)
    oosNum = models.DecimalField(u'缺货及未派单数量', max_digits=8, decimal_places=0, blank=True, null=True)
    occupyNum = models.DecimalField(u'占有数量', max_digits=8, decimal_places=0, blank=True, null=True)
    stockNum = models.DecimalField(u'库存数量', max_digits=8, decimal_places=0, blank=True, null=True)
    ailableNum = models.DecimalField(u'预计可用库存', max_digits=8, decimal_places=0, blank=True, null=True)
    sevenSales = models.DecimalField(u'7天销量', max_digits=8, decimal_places=0, blank=True, null=True)
    fifteenSales = models.DecimalField(u'15天销量', max_digits=8, decimal_places=0, blank=True, null=True)
    thirtySales = models.DecimalField(u'30天销量', max_digits=8, decimal_places=0, blank=True, null=True)
    PurchaseNotInNum = models.DecimalField(u'采购未入库', max_digits=8, decimal_places=0, blank=True, null=True)
    UseNumber = models.PositiveSmallIntegerField(u'可用数量',max_length=11, blank=True,null=True)
    SuggestNum = models.PositiveSmallIntegerField(u'建议采购数量', max_length=11)
    SaleDay = models.DecimalField(u'预计可卖天数',  max_digits=10, decimal_places=1, blank=True, null=True)

    buyer = models.CharField(u'采购员', max_length=128, blank=True, null=True)
    girard = models.CharField(u'款号', max_length=32, blank=True, null=True)
    colour = models.CharField(u'颜色', max_length=32, blank=True, null=True)
    size = models.CharField(u'尺寸', max_length=32, null=True)
    productNumbers = models.PositiveSmallIntegerField(u'需采购数量',max_length=8, blank=True,null=True)
    loanMoney = models.DecimalField(u'借款金额', max_digits=10, decimal_places=4, blank=True, null=True)
    actualMoney = models.DecimalField(u'实际金额', max_digits=10, decimal_places=4, blank=True, null=True)
    outFactory = models.CharField(u'派发工厂', choices=getFactory(), max_length=256, blank=True, null=True)
    rawNumbers = models.DecimalField(u'原材料数', max_digits=8, decimal_places=2, blank=True, null=True)
    unit = models.CharField(u'原材料单位', choices=getChoices(ChoiceRawUnit) ,max_length=8, blank=True, null=True)
    remarkApply = models.TextField(u'预采购备注', blank=True, null=True)
    genPurchaseMan = models.CharField(u'生成采购员', max_length=32, blank=True, null=True)
    genPurchaseDate = models.DateTimeField(u'生成采购时间', blank=True, null=True)
    remarkGenPurchase = models.TextField(u'备注', blank=True, null=True)
    distributeMan = models.CharField(u'分发人员', max_length=32, blank=True, null=True)
    distributeDate = models.DateTimeField(u'分发日期', blank=True, null=True)
    applyMan = models.CharField(u'申请人', max_length=32, blank=True, null=True)
    applyDate = models.DateTimeField(u'申请时间', blank=True, null=True)
    auditMan = models.CharField(u'审核人', max_length=32, blank=True, null=True)
    auditNoPass = models.CharField(u'采购审核计划未通过', max_length=32, blank=True, null=True)
    auditDate = models.DateTimeField(u'审核时间', blank=True, null=True)
    remarkAudit = models.TextField(u'采购计划备注', blank=True, null=True)
    speModifyMan = models.CharField(u'修订专员', max_length=32, blank=True, null=True)
    speModifyDate = models.DateTimeField(u'专员修订时间', blank=True, null=True)
    remarkSpeModify = models.TextField(u'修订备注', blank=True, null=True)
    dispatchMan = models.CharField(u'排单人', max_length=32, blank=True, null=True)
    disPatchDate = models.DateTimeField(u'排单时间', blank=True, null=True)
    remarkDisPatch = models.TextField(u'排单备注', blank=True, null=True)
    confirmMan = models.CharField(u'确认完成人', max_length=32, blank=True, null=True)
    confirmDate = models.DateTimeField(u'确认完成时间', blank=True, null=True)
    remarkConfirm = models.TextField(u'确认交付备注', blank=True, null=True)
    closeMan = models.CharField(u'关闭人', max_length=32, blank=True, null=True)
    closeDate = models.DateTimeField(u'关闭时间', blank=True, null=True)
    remarkClose = models.TextField(u'关闭备注', blank=True, null=True)
    createDate = models.DateTimeField(u'创建时间', blank=True, null=True)
    currentState = models.PositiveSmallIntegerField(u'当前状态', choices=getChoices(ChoiceClothDispatchState), blank=True,
                                                    null=True)
    completeNumbers = models.PositiveSmallIntegerField(u'完成件数',max_length=8, blank=True,null=True)
    BmpUrl = models.CharField(u'图片网址', max_length=255, blank=True, null=True)
    SalerName2 = models.CharField(u'业绩归属人2', max_length=16, blank=True, null=True)
    TortInfo = models.CharField(u'侵权站点', max_length=64, blank=True, null=True)
    goodsclass = models.CharField(u'商品类别', choices=getChoices(ChoiceSelectCategory), max_length=32, blank=True, null=True)
    AverageNumber = models.DecimalField(u'日销量', max_digits=8, decimal_places=2, blank=True, null=True)
    flag = models.PositiveSmallIntegerField(u'联动数据标志',max_length=2, blank=True,null=True)
    OSCode      =   models.CharField(u'采购等级码',max_length=8,blank = True,null = True)
    Stocking_plan_number = models.CharField(u'采购计划单号', max_length=32, blank=True, null=True)
    SpecialPurchaseFlag = models.CharField(u'排单类型',choices=getChoices(ChoicePurchaseType), max_length=16)
    OrderNo = models.CharField(u'订单号', max_length=16, blank=True, null=True)
    GenRecordMan = models.CharField(u'手动单个和批量导入人', max_length=32, blank=True, null=True)
    GenRecordDate = models.DateTimeField(u'手动单个和批量导入时间', blank=True, null=True)
    FactoryRemark = models.TextField(u'提交工厂备注', blank=True, null=True)
    
    class Meta:
        verbose_name=u'需采购供应链服装列表'
        verbose_name_plural=verbose_name
        db_table = 't_cloth_factory_dispatch'
        ordering =  ['-id']
    def __unicode__(self):
        return u'id:%s sku:%s'%(self.id,self.SKU)