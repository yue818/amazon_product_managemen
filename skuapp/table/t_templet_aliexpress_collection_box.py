# coding=utf-8


from django.db import models

class t_templet_aliexpress_collection_box(models.Model):
    ProductID               =   models.CharField(u'商品ID', max_length=20, blank=True, null=True)
    Name                    =   models.CharField(u'商品名称', max_length=255, blank=True, null=True)
    KeyWord                 =   models.CharField(u'商品关键字', max_length=255, blank=True, null=True)
    KeyWord_1               =   models.CharField(u'商品其他关键字一', max_length=255, blank=True, null=True)
    KeyWord_2               =   models.CharField(u'商品其他关键字二', max_length=255, blank=True, null=True)
    Images                  =   models.TextField(u'商品图片', blank=True, null=True)
    Type                    =   models.CharField(u'商品类型', max_length=20, blank=True, null=True)
    Group                   =   models.CharField(u'商品分组', max_length=20, blank=True, null=True)
    Brief                   =   models.TextField(u'商品简述', blank=True, null=True)
    Description             =   models.TextField(u'商品详述', blank=True, null=True)
    SystemProperty          =   models.TextField(u'系统属性', blank=True, null=True)
    CustomProperty          =   models.TextField(u'自定义属性', blank=True, null=True)
    Unit                    =   models.CharField(u'最小计量单位', max_length=50, blank=True, null=True)
    SalesMethod             =   models.CharField(u'销售方式', max_length=50, blank=True, null=True)
    PackageNumber           =   models.CharField(u'每包数量', max_length=10, blank=True, null=True)
    Price                   =   models.CharField(u'零售价', max_length=20, blank=True, null=True)
    WholesalePriceFlag      =   models.CharField(u'是否支持批发价', max_length=10, blank=True, null=True)
    WholesaleMiniNum        =   models.CharField(u'批发最小数量', max_length=10, blank=True, null=True)
    WholesaleDiscount       =   models.CharField(u'批发优惠百分比', max_length=10, blank=True, null=True)
    DeliveryTime            =   models.CharField(u'交货时间', max_length=10, blank=True, null=True)
    ShopSKU                 =   models.CharField(u'商品编码', max_length=255, blank=True, null=True)
    PriceInfo               =   models.TextField(u'价格信息', blank=True, null=True)
    WeightMethod            =   models.CharField(u'自定义计重', max_length=10, blank=True, null=True)
    Weight                  =   models.CharField(u'产品包装后的重量', max_length=10, blank=True, null=True)
    ShippingNum             =   models.CharField(u'最少多少包内按单件运费', max_length=10, blank=True, null=True)
    AddNum                  =   models.CharField(u'增加件数', max_length=10, blank=True, null=True)
    AddWeight               =   models.CharField(u'增加重量', max_length=10, blank=True, null=True)
    Length                  =   models.CharField(u'产品包装尺寸(长)', max_length=10, blank=True, null=True)
    Width                   =   models.CharField(u'产品包装尺寸(宽)', max_length=10, blank=True, null=True)
    Height                  =   models.CharField(u'产品包装尺寸(高)', max_length=10, blank=True, null=True)
    ShippingTemplet         =   models.CharField(u'运费模板', max_length=20, blank=True, null=True)
    Validity                =   models.CharField(u'有效期', max_length=10, blank=True, null=True)
    Alipay                  =   models.CharField(u'支付宝', max_length=20, blank=True, null=True)
    DataSource              =   models.CharField(u'数据来源', max_length=255, blank=True, null=True)
    Quantity                =   models.CharField(u'库存', max_length=10, blank=True, null=True)
    ServiceTemplet          =   models.TextField(u'服务模板', blank=True, null=True)
    PhoneDescription        =   models.TextField(u'产品手机描述', blank=True, null=True)
    RegionalPricing         =   models.TextField(u'区域调价', blank=True, null=True)
    ZipFile                 =   models.FileField(u'采集数据导入',blank = True,null = True)
    CreateTime              =   models.DateTimeField(u'采集时间', blank=True, null=True)
    CreateStaff             =   models.CharField(u'采集人', max_length=16, blank=True, null=True)
    UpdateTime              =   models.DateTimeField(u'更新时间', blank=True, null=True)
    UpdateStaff             =   models.CharField(u'更新人', max_length=16, blank=True, null=True)
    Status                  =   models.CharField(u'状态', max_length=32, blank=True, null=True)
    OssUrl                  =   models.CharField(u'OSS压缩包地址', max_length=255, blank=True, null=True)
    Flag                    =   models.IntegerField(u'显示标识', max_length=2, blank=True, null=True)
    CoreWords               =   models.TextField(u'核心标题', blank=True, null=True)


    class Meta:
        verbose_name = u'AliExpress采集箱'
        verbose_name_plural = verbose_name
        db_table = 't_templet_aliexpress_collection_box'
        ordering = ['-id']
        app_label = 'skuapp'

    def __unicode__(self):
        return u'%s' % (self.id)
