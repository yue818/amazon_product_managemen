# -*- coding: utf-8 -*-

from django.db import models


class t_supply_chain_production_basic(models.Model):
    MainSKU = models.CharField(u'主SKU', max_length=64, blank=True, null=True)
    Buyer = models.CharField(u'采购员', max_length=32, blank=True, null=True)
    CostPrice = models.DecimalField(u'成本单价', max_digits=12, decimal_places=2, blank=True, null=True)
    ProcessCosts = models.DecimalField(u'加工费', max_digits=12, decimal_places=2, blank=True, null=True)
    OffsetPrinting = models.CharField(u'胶印', max_length=255, blank=True, null=True)
    DigitalPrinting = models.CharField(u'数码批印', max_length=255, blank=True, null=True)
    DigitalCuts = models.CharField(u'数码裁片', max_length=255, blank=True, null=True)
    Watermark = models.CharField(u'水印', max_length=255, blank=True, null=True)
    Zipper = models.CharField(u'拉链', max_length=255, blank=True, null=True)
    Cap_rope_ball = models.CharField(u'帽绳/球', max_length=255, blank=True, null=True)
    Button = models.CharField(u'纽扣', max_length=255, blank=True, null=True)
    Elastic = models.CharField(u'橡筋', max_length=255, blank=True, null=True)
    Cornseye_SnapButton = models.CharField(u'鸡眼/四合扣', max_length=255, blank=True, null=True)
    LeatherCard = models.CharField(u'皮牌', max_length=255, blank=True, null=True)
    Lace = models.CharField(u'花边', max_length=255, blank=True, null=True)
    Webbing = models.CharField(u'织带', max_length=255, blank=True, null=True)
    ZhuanJi = models.CharField(u'专机', max_length=255, blank=True, null=True)
    LaTiao = models.CharField(u'拉条', max_length=255, blank=True, null=True)
    ShaoHua = models.CharField(u'烧花', max_length=255, blank=True, null=True)
    TangTu = models.CharField(u'烫图', max_length=255, blank=True, null=True)
    Other = models.CharField(u'其他', max_length=255, blank=True, null=True)
    DateTime = models.DateTimeField(u'日期',blank=True, null=True)
    Main_Pic=models.CharField(u'主图URL',max_length=255,blank=True,null=True)
    Lock=models.SmallIntegerField(u'锁定状态',default=1)
    EditFlag=models.CharField(u'是否可以编辑标识',max_length=255,blank=True, null=True)
    MainFabric=models.CharField(u'主面料',max_length=64,blank=True, null=True)

    A_fabric = models.CharField(u'A面料', max_length=255, blank=True, null=True)
    A_address = models.CharField(u'A档口地址', max_length=255, blank=True, null=True)
    A_dosage = models.CharField(u'A用量', max_length=255, blank=True, null=True)
    A_color = models.CharField(u'A色号', max_length=255, blank=True, null=True)

    B_fabric = models.CharField(u'B面料', max_length=255, blank=True, null=True)
    B_address = models.CharField(u'B档口地址', max_length=255, blank=True, null=True)
    B_dosage = models.CharField(u'B用量', max_length=255, blank=True, null=True)
    B_color = models.CharField(u'B色号', max_length=255, blank=True, null=True)

    C_fabric = models.CharField(u'C面料', max_length=255, blank=True, null=True)
    C_address = models.CharField(u'C档口地址', max_length=255, blank=True, null=True)
    C_dosage = models.CharField(u'C用量', max_length=255, blank=True, null=True)
    C_color = models.CharField(u'C色号', max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = u'供应链款生产基础资料'
        verbose_name_plural = verbose_name
        db_table = u't_supply_chain_production_basic'

    def __unicode__(self):
        return u'%s' % (self.MainSKU)
