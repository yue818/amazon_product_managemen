# -*- coding: utf-8 -*-

from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from public import *

def getChoicesalluser():
    userobjs = User.objects.values_list('username','first_name').filter(is_staff=1).order_by('id')

    sArray = []
    for obj in userobjs:
        stmp = (obj[0],obj[0]+"/"+obj[1])
        sArray.append(stmp)
        del stmp

    return  tuple(sArray)

def getChoicesuser(sUsername):
    userobjs = User.objects.values_list('username','first_name').filter(username=sUsername).order_by('id')
    sFirstName = ""
    for obj in userobjs:
        sFirstName = obj[1]
    return  sFirstName
    
from skuapp.table.t_Large_Small_Corresponding_Cate import t_Large_Small_Corresponding_Cate
from skuapp.table.t_Three_Grade_Classification_Of_Clothing import t_Three_Grade_Classification_Of_Clothing

def getLargeCate():
    return t_Large_Small_Corresponding_Cate.objects.values_list('LCode','LargeClass').distinct().order_by('LargeClass')

def getSmallCate():
    return t_Large_Small_Corresponding_Cate.objects.values_list('SCode','SmallClass').distinct().order_by('LargeClass')

def getClothingSystem(type):
    cate_objs = t_Three_Grade_Classification_Of_Clothing.objects.values_list(type).order_by('id')
    catelist = []
    for cate_obj in cate_objs:
        eachlist = [cate_obj[0],cate_obj[0]]
        if eachlist not in catelist:
            catelist.append(eachlist)
    return catelist



#0) base表 t_base
class t_base(models.Model):
    #id            =   models.AutoField(primary_key=True)
    id             =   models.AutoField(u'业务流水号',primary_key=True)
    SKU            =   models.CharField(u'子SKU',max_length=16,blank = True,null = True)
    MainSKU        =   models.CharField(u'主SKU*',max_length=255,blank = True,null = True)
    Keywords       =   models.CharField(u'英文标题',max_length=255,blank = True,null = True)
    Keywords2      =   models.CharField(u'中文标题',max_length=255,blank = True,null = True)
    UpdateTime     =   models.DateTimeField(u'更新时间',auto_now=True,blank = True,null = True)
    StaffID        =   models.CharField(u'工号',max_length=16,blank = True,null = True,db_index =True)
    Name           =   models.CharField(u'ListingTitle',max_length=100,blank = True,null = True) #models.TextField(u'ListingTitle',blank = True,null = True) #
    Name2          =   models.CharField(mark_safe(u'商品名称<br>(中文)'),max_length=256,blank = True,null = True)
    Material       =   models.CharField(u'材质',max_length=128,blank = True,null = True)
    Length         =   models.PositiveSmallIntegerField(u'长(cm)',blank = True,null = True)
    Width          =   models.PositiveSmallIntegerField(u'宽(cm)',blank = True,null = True)
    Height         =   models.PositiveSmallIntegerField(u'高(cm)',blank = True,null = True)
    LWH            =   models.CharField(u'长*宽*高',max_length=128,blank = True,null = True)
    Weight         =   models.PositiveSmallIntegerField(u'克重(g)',blank = True,null = True)
    SourceURL      =   models.URLField(u'反向链接*',blank = True,null = True)
    SourceURL2     =   models.URLField(u'反向链接2*',blank = True,null = True)  # 新增字段
    PlatformName   =   models.CharField(u'反向链接平台',choices=getChoices(ChoicePlatformName),max_length=16,blank = True,null = True)
    PlatformPID    =   models.CharField(u'产品平台ID',max_length=24,blank = True,null = True)
    SourcePicPath  =   models.CharField(u'调研图',max_length=200,blank = True,null = True)
    SourcePicRemark=   models.TextField(u'原始图片描述',blank = True,null = True)
    ArtPicPath     =   models.TextField(u'最终图片名称',blank = True,null = True)
    UnitPrice      =   models.DecimalField(u'单价(¥元)',max_digits=6,decimal_places=2,blank = True,null = True)
    Unit           =   models.CharField(u'单位',choices=getChoices(ChoiceUnit),max_length=4,blank = True,null = True)
    #PackingID      =   models.ForeignKey(t_sys_packing,blank = True,null=True,on_delete = models.DO_NOTHING,verbose_name=u'包装规格')
    #PackingID2     =   models.ForeignKey(t_sys_packing2,blank=True,null=True,on_delete = models.DO_NOTHING,verbose_name=u'附加包装规格')
    PackingID2Num  =   models.PositiveSmallIntegerField(u'附加包装数量(层或CM)',default = 0,blank=True,null=True)
    MinPackNum     =   models.PositiveSmallIntegerField(mark_safe(u'最小包<br>装数量'),default = 1,blank = True,null = True)
    MinOrder       =   models.PositiveSmallIntegerField(u'采购最小订货量',blank = True,null = True)
    SupplierID     =   models.CharField(u'供货商名称',max_length=64,blank = True,null = True)
    SupplierArtNO  =   models.CharField(u'供货商货号',max_length=32,blank = True,null = True)
    SupplierPColor =   models.CharField(u'供货商商品颜色',max_length=64,blank = True,null = True)
    SupplierPDes   =   models.CharField(u'供货商商品标题',max_length=64,blank = True,null = True)
    SupplierPUrl1  =   models.URLField(u'供货商商品URL一',blank = True,null = True)
    SupplierPUrl2  =   models.URLField(u'供货商商品URL二',blank = True,null = True)
    OrderDays      =   models.PositiveSmallIntegerField(u'到货天数',default = 10,blank = True,null = True)
    StockAlarmDays =   models.PositiveSmallIntegerField(u'库存预警天数',default = 10,blank = True,null = True)
    SpecialRemark  =   models.CharField(mark_safe(u'调研选品备注（销售员）'),max_length=64,blank = True,null = True)
    Remark         =   models.TextField(u'备注',max_length=300,blank = True,null = True)
    InitialWord    =   models.CharField(u'起始词(空格分割)',max_length=64,blank = True,null = True)
    SourceURLPrice =   models.DecimalField(u'反向价格(美元)',max_digits=7,decimal_places=2,blank = True,null = True)
    ShelveDay      =   models.DateField(u'上架日期',max_length=16,blank = True,null = True)
    OrdersLast7Days=   models.PositiveSmallIntegerField(u'15天order数',blank = True,null = True)
    SpecialSell    =   models.TextField(u'商品信息备注（产品专员）',blank = True,null = True)
    ClothingNote    =   models.TextField(u'服装体系备注',blank = True,null = True)
    OldSKU         =   models.CharField(u'原有SKU',max_length=16,blank = True,null = True)
    #Category1      =   models.CharField(u'一级分类',max_length=16,blank = True,null = True)
    Category2      =   models.CharField(u'二级分类',max_length=16,choices=getChoices(ChoiceCategory2),blank = True,null = True)
    Category3      =   models.CharField(u'三级分类',max_length=16,blank = True,null = True)
    Electrification=   models.CharField(u'是否带电',choices=getChoices(ChoiceIF),max_length=4,default=u'否',blank = True,null = True)
    Powder         =   models.CharField(u'是否粉末',choices=getChoices(ChoiceIF),max_length=4,default=u'否',blank = True,null = True)
    Liquid         =   models.CharField(u'是否液体',choices=getChoices(ChoiceIF),max_length=4,default=u'否',blank = True,null = True)
    Magnetism      =   models.CharField(u'是否带磁',choices=getChoices(ChoiceIF),max_length=4,default=u'否',blank = True,null = True)
    Buyer          =   models.CharField(u'采购员',max_length=8,blank = True,null = True)
    SupplierContact=   models.CharField(u'供货商ID',max_length=32,blank = True,null = True)
    SourcePicPath2 =   models.CharField(u'供货商图',max_length=100,blank = True,null = True)
    Storehouse     =   models.CharField(u'发货仓库',max_length=16,choices=getChoices(ChoiceStorehouse),default=u'浦江仓库',blank = True,null = True)
    URLamazon      =   models.URLField(u'AMAZON反向链接',blank = True,null = True)
    URLebay        =   models.URLField(u'EBAY反向链接',blank = True,null = True)
    URLexpress     =   models.URLField(u'ALIEXPRESS反向链接',blank = True,null = True)
    URLwish        =   models.URLField(u'WISH反向链接',blank = True,null = True)
    Pricerange     =   models.CharField(u'价格区间',max_length=20,blank = True,null = True)
    NumBought      =   models.PositiveIntegerField(u'总购买数量',blank = True,null = True)
    TotalInventory =   models.PositiveIntegerField(u'Wish库存数',blank = True,null = True)
    Tags           =   models.CharField(u'TAGS',max_length=100,blank = True,null = True)#models.TextField(u'TAGS',blank = True,null = True) #
    SurveyRemark   =   models.CharField(u'调研备注',max_length=24,blank = True,null = True)
    PackNID        =   models.PositiveSmallIntegerField(u'包装NID',default = 0,blank = True,null = True)
    possessMan2    =   models.CharField(u'责任归属人2',max_length=8,blank = True,null = True)
    LargeCategory  =   models.CharField(u'大类名称',choices=getLargeCate(),max_length=32,blank = False,null = False)
    SmallCategory  =   models.CharField(u'小类名称',choices=getSmallCate(),max_length=32,blank = False,null = False)
    ReportName     =   models.CharField(u'英文申报名',max_length=32,blank = True,null = True)
    ReportName2    =   models.CharField(u'中文申报名',max_length=32,blank = True,null = True)
    fromT          =   models.CharField(u'上一步来源',max_length=32,blank = True,null = True)
    PrepackMark    =   models.CharField(u'预包符号',max_length=2,blank = True,null = True)
    CreateTime     =   models.DateField(u'创建时间',blank = True,null = True)
    CreateStaffName=   models.CharField(u'创建人',max_length=16,blank = True,null = True)
    selectpic      =   models.ImageField(u'上传调研图',upload_to='media/',blank=True, null=True)
    selectpic2     =   models.ImageField(u'上传供应商图',upload_to='media/',blank=True, null=True)
    DYTime         =   models.DateField(u'调研时间',blank = True,null = True)
    DYStaffName    =   models.CharField(u'调研员',max_length=16,blank = True,null = True)
    DYSHTime       =   models.DateField(u'调研审核时间',blank = True,null = True)
    DYSHStaffName  =   models.CharField(u'调研审核员',max_length=16,blank = True,null = True)
    XJTime         =   models.DateField(u'询价时间',blank = True,null = True)
    XJStaffName    =   models.CharField(u'询价员',max_length=16,blank = True,null = True)
    KFTime         =   models.DateTimeField(u'开发时间',blank = True,null = True)
    KFStaffName    =   models.CharField(u'开发员',max_length=16,blank = True,null = True)
    JZLTime        =   models.DateField(u'建资料时间',blank = True,null = True)
    JZLStaffName   =   models.CharField(u'建资料员',max_length=16,blank = True,null = True)
    PZTime         =   models.DateField(u'拍照时间',blank = True,null = True)
    PZStaffName    =   models.CharField(u'拍照员',max_length=16,blank = True,null = True)
    MGTime         =   models.DateField(u'图片完成时间',blank = True,null = True)
    MGStaffName    =   models.CharField(u'美工员',max_length=16,blank = True,null = True)
    LRTime         =   models.DateField(u'录入时间',blank = True,null = True)
    LRStaffName    =   models.CharField(u'录入员',max_length=16,blank = True,null = True)
    YNphoto          = models.CharField(u'图片处理',choices=getChoices(ChoiceYNphoto),default='1',max_length=6,blank = True,null = True)
    MGProcess        = models.CharField(u'图片状态',choices=getChoices(ChoiceMGProcess),default='1',max_length=6,blank = True,null = True)
    PPosition        = models.CharField(u'拍照位置',choices=getChoices(ChoicePPosition),default='1',max_length=6,blank = True,null = True)
    PictureRequest   = models.TextField(u'图片要求',blank = True,null = True)

    ContrabandAttribute = models.CharField(u'商品属性',choices=getChoices(ChoiceContraband),default=u'普货',max_length=32,blank = True,null = True)

    ClothingSystem1 = models.CharField(u'服装一级分类', choices=getClothingSystem('CateOne'),max_length=255,blank=True, null=True)
    ClothingSystem2 = models.CharField(u'服装二级分类', choices=getClothingSystem('CateTwo'),max_length=255, blank=True, null=True)
    ClothingSystem3 = models.CharField(u'服装三级分类', choices=getClothingSystem('CateThree'),max_length=255, blank=True, null=True)
    YJGS2StaffName = models.CharField(u'业绩归属人2',choices=getChoicesalluser(), max_length=16, blank=True, null=True)
    AuditStaffName = models.CharField(u'审核人', max_length=16,blank = True,null = True)
    AuditTime = models.DateTimeField(u'审核时间',blank = True,null = True)
    AI_FLAG   = models.CharField(u'精准调研标记',choices=getChoices(ChoiceAI), default='0',max_length=1, blank=True, null=True)
    BJP_FLAG  = models.IntegerField(u'是否为半精品',choices=((1,'是'),(0,'否')),blank=True,null=True)
    IP_FLAG   = models.CharField(u'IP产品标记',choices=getChoices(ChoiceIP_FLAG),default='0',max_length=1, blank=True,null=True)

    class Meta:
        app_label = 'skuapp'
        abstract = True
    def __unicode__(self):
        return u'id:%s MainSKU:%s'%(self.id,self.MainSKU)