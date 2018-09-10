#-*-coding:utf-8-*-
from django.db import models
from .public import *
from skuapp.table.t_config_apiurl_amazon import *
from skuapp.table.t_template_product_config_amazon import *
"""  
 @desc:  amazon铺货采集基础表字段
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_templet_amazon_base.py
 @time: 2017/12/15 19:12
"""
def getSelect():
    return t_config_apiurl_amazon.objects.values_list('category','category')

def getSelectProductType():
    return t_template_product_config_amazon.objects.values_list('product_type', 'product_type')

PRODUCTCLOTHING_SEASON = (('Frühling-Sommer', 'Frühling-Sommer'),('Ganzjahresartikel', 'Ganzjahresartikel'),('Herbst-Winter', 'Herbst-Winter'),
                          ('automne-hiver', 'automne-hiver'), ('printemps-été', 'printemps-été'))

class t_templet_amazon_base(models.Model):
    upload_product_type             = models.CharField(u'刊登种类', choices=getSelectProductType(), max_length=64, blank=True, null=True)
    recommended_browse_nodes        = models.CharField(u'商品类型', max_length=200, blank=True, null=True)
    recommended_browse_nodes_id     = models.CharField(u'节点ID', max_length=32, blank=True, null=True)
    dataFromUrl                     = models.CharField(u'反向链接地址', max_length=200, blank=True, null=True)
    item_sku                        = models.CharField(u'店铺SKU', max_length=100, blank=True, null=True)
    external_product_id             = models.CharField(u'产品ID', max_length=64, blank=True, null=True)
    external_product_id_type        = models.CharField(u'产品ID类型', max_length=12, choices=getChoices(ExternalProductIdType),default=u'UPC', blank=True, null=True)
    item_name                       = models.CharField(u'产品标题', max_length=200, blank=True, null=True)
    manufacturer                    = models.CharField(u'制造商', max_length=48, blank=True, null=True)
    part_number                     = models.CharField(u'制造商零件编号', max_length=40, blank=True, null=True)
    feed_product_type               = models.CharField(u'商品种类', max_length=100, blank=True, null=True)
    item_type                       = models.CharField(u'节点类型', max_length=100, blank=True, null=True)
    product_subtype                 = models.CharField(u'服装类型', max_length=64, choices=getChoices(ProductSubtype),blank=True, null=True)
    product_description             = models.TextField(u'产品描述', max_length=2000, blank=True, null=True)
    brand_name                      = models.CharField(u'商品品牌', max_length=48, blank=True, null=True)
    update_delete                   = models.CharField(u'更新删除', max_length=32, choices=getChoices(UpdateOrDelete), default=u'Update',blank=True, null=True)
    item_package_quantity           = models.CharField(u'包装数', max_length=12, default=u'1',blank=True, null=True)
    standard_price                  = models.DecimalField(u'商品价格', max_digits=10, decimal_places=2, blank=True, null=True)
    sale_price                      = models.DecimalField(u'促销价格', max_digits=10, decimal_places=2, blank=True, null=True)
    sale_from_date                  = models.DateTimeField(u'促销开始时间', blank=True, null=True)
    sale_end_date                   = models.DateTimeField(u'促销结束时间', blank=True, null=True)
    condition_type                  = models.CharField(u'产品新旧', max_length=32, default=u'New', blank=True, null=True)
    quantity                        = models.CharField(u'产品数量', max_length=32, blank=True, null=True)
    merchant_shipping_group_name    = models.CharField(u'运输模板', max_length=200, blank=True, null=True)
    bullet_point1                   = models.CharField(u'产品描述1', max_length=500, blank=True, null=True)
    bullet_point2                   = models.CharField(u'产品描述2', max_length=500, blank=True, null=True)
    bullet_point3                   = models.CharField(u'产品描述3', max_length=500, blank=True, null=True)
    bullet_point4                   = models.CharField(u'产品描述4', max_length=500, blank=True, null=True)
    bullet_point5                   = models.CharField(u'产品描述5', max_length=500, blank=True, null=True)
    # bullet_point6                   = models.CharField(u'商品描述6', max_length=248, blank=True, null=True)
    # bullet_point7                   = models.CharField(u'商品描述7', max_length=248, blank=True, null=True)
    generic_keywords                = models.TextField(u'关键词', blank=True, null=True)
    main_image_url                  = models.ImageField(u'主图', max_length=1000, blank=True, null=True)
    other_image_url1                = models.ImageField(u'附图1', max_length=1000, blank=True, null=True)
    other_image_url2                = models.ImageField(u'附图2', max_length=1000, blank=True, null=True)
    other_image_url3                = models.ImageField(u'附图3', max_length=1000, blank=True, null=True)
    other_image_url4                = models.ImageField(u'附图4', max_length=1000, blank=True, null=True)
    other_image_url5                = models.ImageField(u'附图5', max_length=1000, blank=True, null=True)
    other_image_url6                = models.ImageField(u'附图6', max_length=1000, blank=True, null=True)
    other_image_url7                = models.ImageField(u'附图7', max_length=1000, blank=True, null=True)
    other_image_url8                = models.ImageField(u'附图8', max_length=1000, blank=True, null=True)
    fulfillment_center_id           = models.CharField(u'履行中心ID', max_length=200, blank=True, null=True)
    model_name                      = models.CharField(u'系列', max_length=200, blank=True, null=True)
    warranty_description            = models.TextField(u'制造商保修说明', blank=True, null=True)
    variation_theme                 = models.CharField(u'变体分辨类型', max_length=32, blank=True, null=True)
    model                           = models.CharField(u'型号/样式编号', max_length=64, blank=True, null=True)
    mfg_minimum                     = models.CharField(u'最小使用年龄', max_length=32, blank=True, null=True)
    mfg_minimum_unit_of_measure     = models.CharField(u'年龄单位', max_length=32, default=u'years', choices=getChoices(MfgMinimumUnitOfMeasure), blank=True, null=True)
    swatch_image_url                = models.CharField(u'色板图片网址', max_length=200, blank=True, null=True)
    department_name                 = models.CharField(u'款式选择', max_length=32, blank=True, null=True)
    fit_type                        = models.CharField(u'服装适合类型(IN)', max_length=32, blank=True, null=True)
    unit_count                      = models.CharField(u'单位数量', max_length=32, blank=True, null=True)
    unit_count_type                 = models.CharField(u'单位名称', max_length=32, blank=True, null=True)
    fulfillment_latency             = models.CharField(u'产品处理时间', max_length=32, blank=True, null=True)
    display_dimensions_unit_of_measure = models.CharField(u'显示尺寸单位', max_length=32, blank=True, null=True)
    generic_keywords1               = models.CharField(u'关键词1', max_length=249, blank=True, null=True)
    generic_keywords2               = models.CharField(u'关键词2', max_length=199, blank=True, null=True)
    generic_keywords3               = models.CharField(u'关键词3', max_length=199, blank=True, null=True)
    generic_keywords4               = models.CharField(u'关键词4', max_length=199, blank=True, null=True)
    generic_keywords5               = models.CharField(u'关键词5', max_length=199, blank=True, null=True)
    department_name1                = models.CharField(u'适用性别1', max_length=32, default=u'mens', choices=getChoices(ChoiceDepartmentName), blank=True, null=True)
    department_name2                = models.CharField(u'适用性别2', max_length=32, choices=getChoices(ChoiceDepartmentName), blank=True, null=True)
    department_name3                = models.CharField(u'适用性别3', max_length=32, choices=getChoices(ChoiceDepartmentName), blank=True, null=True)
    department_name4                = models.CharField(u'适用性别4', max_length=32, choices=getChoices(ChoiceDepartmentName), blank=True, null=True)
    department_name5                = models.CharField(u'适用性别5', max_length=32, choices=getChoices(ChoiceDepartmentName), blank=True, null=True)
    material_type                   = models.CharField(u'材料种类', max_length=64, blank=True, null=True)
    metal_type                      = models.CharField(u'金属类型', max_length=64, blank=True, null=True)
    setting_type                    = models.CharField(u'设置类型', max_length=64, blank=True, null=True)
    ring_size                       = models.CharField(u'戒指尺寸', max_length=32, blank=True, null=True)
    clothing_size                   = models.CharField(u'服装尺寸', max_length=32, blank=True, null=True)
    clothing_color                  = models.CharField(u'服装颜色', max_length=32, blank=True, null=True)
    toy_color                       = models.CharField(u'玩具颜色(IN)', max_length=32, blank=True, null=True)
    jewerly_color                   = models.CharField(u'饰品颜色(IN)', max_length=32, blank=True, null=True)
    homes_color                     = models.CharField(u'家居品颜色(IN)', max_length=32, blank=True, null=True)
    homes_size                      = models.CharField(u'家居品尺寸(IN)', max_length=32, blank=True, null=True)
    gem_type                        = models.CharField(u'宝石类型', max_length=64, blank=True, null=True)
    item_shape                      = models.CharField(u'商品形状(IN)', max_length=64, blank=True, null=True)
    target_audience_keywords1       = models.CharField(u'目标人群1',  max_length=64, default=u'boys', choices=getChoices(TargetAudienceKeywords), blank=True, null=True)
    target_audience_keywords2       = models.CharField(u'目标人群2', max_length=64, default=u'girls', choices=getChoices(TargetAudienceKeywords), blank=True, null=True)
    target_audience_keywords3       = models.CharField(u'目标人群3', max_length=64, default=u'unisex-children', choices=getChoices(TargetAudienceKeywords), blank=True, null=True)
    productSKU                      = models.CharField(u'商品SKU', max_length=200, blank=True, null=True)
    createUser                      = models.CharField(u'创建人', max_length=32, blank=True, null=True)
    createTime                      = models.DateTimeField(u'创建时间', blank=True, null=True)
    updateUser                      = models.CharField(u'更新人', max_length=32, blank=True, null=True)
    updateTime                      = models.DateTimeField(u'更新时间', blank=True, null=True)
    status                          = models.CharField(u'状态', max_length=32, blank=True, null=True)
    prodcut_variation_id            = models.CharField(u'主从关系',max_length=32,blank=True,null=True)
    can_upload                      = models.CharField(u'能否刊登状态', max_length=32, blank=True, null=True)
    number_of_pieces = models.IntegerField(u'拼图块数', max_length=5, blank=True, null=True)
    item_weight = models.DecimalField(u'重量', max_digits=10, decimal_places=2, blank=True, null=True)
    item_weight_unit = models.CharField(u'重量单位', max_length=32, default=u'KG', choices=getChoices(item_weight_unit), blank=True, null=True)
    color_name_public = models.CharField(u'颜色', max_length=32, blank=True, null=True)
    mrp = models.DecimalField(u'最大销售价格(MRP)', max_digits=10, decimal_places=2, blank=True, null=True)
    sleeve_type = models.CharField(u'服装袖筒类型(IN)', max_length=32, blank=True, null=True)
    item_type_name = models.CharField(u'产品类型(IN)', max_length=64, blank=True, null=True)
    season                          = models.CharField(u'季节(德法)', choices=PRODUCTCLOTHING_SEASON, max_length=32, blank=True, null=True)
    material_composition            = models.CharField(u'材料成分(德法)', max_length=1000, blank=True, null=True)
    remark                          = models.TextField(u'备注', blank=True, null=True)
    class Meta:
        app_label = 'skuapp'
        abstract = True
    def __unicode__(self):
        return u'id:%s'% (self.id)