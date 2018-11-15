# -*- coding: utf-8 -*-
from django.db import models
from skuapp.table.public import getChoices,ChoiceStatus_wish,ChoiceReviewState,ChoiceTortYN,ChoiceOperationState

class t_erp_aliexpress_goods_base(models.Model):
    #id = models.AutoField(u'id', max_length=11)
    data_src = models.CharField(u'商品信息来源', max_length=32,null=True,blank=True)
    product_id = models.CharField(u'商品ID', max_length=20,null=True,blank=True)
    category_id = models.CharField(u'产品所在类目的ID', max_length=20,null=True,blank=True)
    product_price = models.CharField(u'单品产品的价格', max_length=11,null=True,blank=True)
    subject = models.CharField(u'产品标题', max_length=128,null=True,blank=True)
    image_urls = models.CharField(u'图片地址', max_length=2000,null=True,blank=True)
    detail = models.TextField(u'商品详情描述',null=True,blank=True)
    owner_member_id = models.CharField(u'店铺名称/账号名称', max_length=64,null=True,blank=True)
    owner_member_seq = models.CharField(u'账号ID', max_length=64,null=True,blank=True)
    shopName = models.CharField(u'账号群名', max_length=64,null=True,blank=True)
    product_max_price = models.CharField(u'最高价', max_length=11,null=True,blank=True)
    product_min_price = models.CharField(u'最低价', max_length=11,null=True,blank=True)
    package_width = models.DecimalField(u'产品宽度', max_digits=13, decimal_places=2,null=True,blank=True)
    package_height = models.DecimalField(u'产品高度', max_digits=13, decimal_places=2,null=True,blank=True)
    package_length = models.DecimalField(u'产品长度', max_digits=13, decimal_places=2, blank=True, null=True)
    gmt_modified = models.CharField(u'平台更新时间', max_length=32,null=True,blank=True)
    gmt_create = models.CharField(u'平台发布时间', max_length=32,null=True,blank=True)
    is_pack_sell = models.CharField(u'自定义计重', max_length=10,null=True,blank=True)
    product_status_type = models.CharField(u'产品的状态', max_length=32,null=True,blank=True)
    lot_num = models.IntegerField(u'包装数', max_length=11,null=True,blank=True)
    group_id = models.CharField(u'产品所关联的产品分组ID', max_length=11,null=True,blank=True)
    group_ids = models.CharField(u'产品所在的产品分组列表', max_length=256,null=True,blank=True)
    product_unit = models.CharField(u'产品的单位', max_length=11,null=True,blank=True)
    promise_template_id = models.CharField(u'服务模板ID', max_length=11,null=True,blank=True)
    ws_display = models.CharField(u'商品下架原因', max_length=128,null=True,blank=True)
    ws_valid_num = models.IntegerField(u'商品有效天数',null=True,blank=True)
    ws_offline_date = models.CharField(u'产品的下架日期', max_length=32,null=True,blank=True)
    is_image_dynamic = models.CharField(u'动态图产品', max_length=11,null=True,blank=True)
    delivery_time = models.IntegerField(u'备货期', max_length=11,null=True,blank=True)
    gross_weight = models.CharField(u'商品毛重', max_length=11,null=True,blank=True)
    success = models.CharField(u'商品详情获取结果', max_length=11,null=True,blank=True)
    freight_template_id = models.CharField(u'运费模版ID', max_length=11,null=True,blank=True)
    package_type = models.CharField(u'打包销售', max_length=32,null=True,blank=True)
    reduce_strategy = models.CharField(u'库存扣减策略', max_length=128,null=True,blank=True)
    currency_code = models.CharField(u'货币单位', max_length=32,null=True,blank=True)
    product_skus = models.TextField(u'SKU信息列表',null=True,blank=True)
    product_properties = models.TextField(u'商品属性',null=True,blank=True)
    add_unit = models.CharField(u'每增加件数', max_length=4,null=True,blank=True)
    add_weight = models.CharField(u'增加重量(KG,null=True,blank=True)', max_length=12,null=True,blank=True)
    multimedia = models.TextField(u'商品多媒体信息',null=True,blank=True)
    base_unit = models.CharField(u'不增加运费件数', max_length=4,null=True,blank=True)
    bulk_discount = models.CharField(u'批发折扣', max_length=3,null=True,blank=True)
    bulk_order = models.CharField(u'批发最小数量', max_length=6,null=True,blank=True)
    coupon_end_date = models.CharField(u'卡券商品结束有效期', max_length=32,null=True,blank=True)
    coupon_start_date = models.CharField(u'卡券商品开始有效期', max_length=32,null=True,blank=True)
    keyword = models.CharField(u'关键词', max_length=256,null=True,blank=True)
    product_more_keywords1 = models.CharField(u'产品关键词1', max_length=256,null=True,blank=True)
    product_more_keywords2 = models.CharField(u'产品关键词2', max_length=256,null=True,blank=True)
    mobile_detail = models.TextField(u'mobile Detail详情',null=True,blank=True)
    sizechart_id = models.CharField(u'尺码表模版ID', max_length=64,null=True,blank=True)
    summary = models.TextField(u'产品概要',null=True,blank=True)
    error_message = models.TextField(u'错误信息',null=True,blank=True)
    error_code = models.CharField(u'错误代码', max_length=256,null=True,blank=True)
    national_quote_configuration = models.TextField(u'商品分国家报价的配置',null=True,blank=True)


    class Meta:
        app_label = 'aliapp'
        abstract = True
    def __unicode__(self):
        return u'id:%s'% (self.id)

class t_erp_aliexpress_product_draft_box(t_erp_aliexpress_goods_base):

    class Meta:
        verbose_name = u'速卖通草稿箱'
        verbose_name_plural = u'速卖通草稿箱'
        db_table = u't_erp_aliexpress_product_draft_box'
        ordering = ['-id']

    def __unicode__(self):
        return u'id:%s'%(self.id)

class t_erp_aliexpress_product_recycle_bin(t_erp_aliexpress_goods_base):

    class Meta:
        verbose_name = u'速卖通回收站'
        verbose_name_plural = u'速卖通回收站'
        db_table = u't_erp_aliexpress_product_recycle_bin'
        ordering = ['-id']

    def __unicode__(self):
        return u'id:%s'%(self.id)

class t_erp_aliexpress_product_released(t_erp_aliexpress_goods_base):

    class Meta:
        verbose_name = u'速卖通待发布商品信息表'
        verbose_name_plural = u'速卖通待发布商品信息表'
        db_table = u't_erp_aliexpress_product_released'
        ordering = ['-id']

    def __unicode__(self):
        return u'id:%s'%(self.id)

class t_erp_aliexpress_product_announcing(t_erp_aliexpress_goods_base):

    class Meta:
        verbose_name = u'速卖通发布中商品信息表'
        verbose_name_plural = u'速卖通发布中商品信息表'
        db_table = u't_erp_aliexpress_product_announcing'
        ordering = ['-id']

    def __unicode__(self):
        return u'id:%s'%(self.id)

class t_erp_aliexpress_product_upload_result(t_erp_aliexpress_goods_base):
    online_status = models.CharField(u'online系统状态', max_length=32, null=True, blank=True)

    class Meta:
        verbose_name = u'速卖通商品发布结果信息表'
        verbose_name_plural = u'速卖通商品发布结果信息表'
        db_table = u't_erp_aliexpress_product_upload_result'
        ordering = ['-id']

    def __unicode__(self):
        return u'id:%s'%(self.id)

class t_erp_aliexpress_online_info(t_erp_aliexpress_goods_base):
    Sales7Days = models.IntegerField(u'7天销量', max_length=12,null=True,blank=True)
    Viewed7Days=models.IntegerField(u'7日浏览量', max_length=12,null=True,blank=True)
    Exposed7Days = models.IntegerField(u'7日曝光量', max_length=12, null=True, blank=True)
    skustock_isempty=models.SmallIntegerField(u'是否有库存')
    StopSales=models.SmallIntegerField(u'停售百分比')
    StopSalesFlag=models.SmallIntegerField(u'停售标识')
    online_status = models.CharField(u'online系统状态', max_length=32,null=True,blank=True)
    updatetime = models.DateTimeField(u'同步时间', null=True)
    is_syn = models.PositiveIntegerField(u'同步状态', max_length=4, null=True, blank=True)
    is_modify = models.PositiveIntegerField(u'编辑状态', max_length=4, null=True, blank=True)
    GoodsFlag = models.PositiveIntegerField(u'商品SKU状态', max_length=11, null=True, blank=True)
    product_daily_refresh_date=models.DateField(u'每日销量刷新时间',null=True,blank=True)
    revoked = models.SmallIntegerField(u'是否被移除', max_length=4, null=True, blank=True)
    submitter=models.CharField(u'刊登人',max_length=64,null=True,blank=True)
    skustatus1_stock=models.SmallIntegerField(u'sku正常是否有库存')
    skustatus2_stock=models.SmallIntegerField(u'sku售完下架是否有库存')
    skustatus3_stock=models.SmallIntegerField(u'sku临时下架是否有库存')
    skustatus4_stock=models.SmallIntegerField(u'sku停售是否有库存')
    activation_flag=models.SmallIntegerField(u'是否激活')
    Infringement=models.SmallIntegerField()
    class Meta:
        verbose_name = u'速卖通在线商品信息表'
        verbose_name_plural = u'速卖通在线商品信息表'
        db_table = u't_erp_aliexpress_online_info'
        ordering = ['-gmt_create']

    def __unicode__(self):
        return u'id:%s'%(self.id)

class t_erp_aliexpress_online_info_delete(t_erp_aliexpress_goods_base):
    online_status = models.CharField(u'online系统状态', max_length=32,null=True,blank=True)
    updatetime = models.DateTimeField(u'更新时间', null=True, blank=True)
    is_syn = models.PositiveIntegerField(u'同步状态', max_length=4, null=True, blank=True)
    is_modify = models.PositiveIntegerField(u'编辑状态', max_length=4, null=True, blank=True)
    GoodsFlag = models.PositiveIntegerField(u'商品SKU状态', max_length=11, null=True, blank=True)
    updateUser = models.CharField(u'更新人', max_length=32,null=True,blank=True)
    createUser = models.CharField(u'创建人', max_length=32, null=True, blank=True)
    createTime = models.DateTimeField(u'创建时间', null=True, blank=True)
    remark = models.TextField(u'备注',null=True,blank=True)

    class Meta:
        verbose_name = u'速卖通商品删除标记表'
        verbose_name_plural = u'速卖通商品删除标记表'
        db_table = u't_erp_aliexpress_online_info_delete'
        ordering = ['-gmt_create']

    def __unicode__(self):
        return u'id:%s'%(self.id)


class v_erp_aliexpress_online_info_delete(t_erp_aliexpress_goods_base):
    online_status = models.CharField(u'online系统状态', max_length=32,null=True,blank=True)
    updatetime = models.DateTimeField(u'更新时间', null=True, blank=True)
    is_syn = models.PositiveIntegerField(u'同步状态', max_length=4, null=True, blank=True)
    is_modify = models.PositiveIntegerField(u'编辑状态', max_length=4, null=True, blank=True)
    GoodsFlag = models.PositiveIntegerField(u'商品SKU状态', max_length=11, null=True, blank=True)
    # updateUser = models.CharField(u'更新人', max_length=32,null=True,blank=True)
    # createUser = models.CharField(u'创建人', max_length=32, null=True, blank=True)
    # createTime = models.DateTimeField(u'创建时间', null=True, blank=True)
    revoked = models.SmallIntegerField(u'是否被移除', max_length=4, null=True, blank=True)

    remark = models.TextField(u'备注',null=True,blank=True)

    class Meta:
        verbose_name = u'速卖通商品删除标记表'
        verbose_name_plural = u'速卖通商品删除标记表'
        db_table = u'v_erp_aliexpress_online_info_delete'
        ordering = ['-gmt_create']

    def __unicode__(self):
        return u'id:%s'%(self.id)

class t_erp_aliexpress_authorize_info(models.Model):
    user_id = models.CharField(u'Ali账号ID', max_length=32, null=True)
    user_nick = models.CharField(u'店铺账号', max_length=32, null=True)
    access_token = models.CharField(u'授权信息', max_length=128, null=True)
    refresh_token = models.CharField(u'刷新授权token', max_length=128, null=True)
    w1_valid = models.CharField(u'W1有效时间', max_length=32, null=True)
    r1_valid = models.CharField(u'R1有效时间', max_length=32, null=True)
    w2_valid = models.CharField(u'W2有效时间', max_length=32, null=True)
    r2_valid = models.CharField(u'R2有效时间', max_length=32, null=True)
    refresh_token_valid_time = models.CharField(u'刷新授权时间', max_length=32, null=True)
    expire_time = models.CharField(u'失效时间', max_length=32, null=True)

    class Meta:
        verbose_name = u'账号店铺授权信息表'
        verbose_name_plural = u'账号店铺授权信息表'
        db_table = u't_erp_aliexpress_authorize_info'
    def __unicode__(self):
        return u'id:%s'%(self.id)


class t_erp_aliexpress_action_temp(models.Model):
    shopName = models.CharField(u'店铺群号', max_length=64, null=True)
    accountName = models.CharField(u'店铺账号', max_length=64, null=True)
    action_type = models.CharField(u'操作类型', max_length=128, null=True)
    action_param = models.TextField(u'操作数据', null=True,blank=True)
    action_result = models.CharField(u'操作结果', max_length=256, null=True)
    action_time = models.DateTimeField(u'操作时间', null=True)
    action_user = models.CharField(u'执行人', max_length=64, null=True)
    table_name = models.CharField(u'表名', max_length=64, null=True)
    field_name = models.CharField(u'字段名', max_length=64, null=True)
    old_value = models.TextField(u'原始数据', null=True,blank=True)
    action_id = models.PositiveSmallIntegerField(u'操作数据ID', max_length=11, null=True)
    done_time = models.DateTimeField(u'完成时间', null=True)

    class Meta:
        verbose_name = u'AliExpress操作日志中间表'
        verbose_name_plural = u'AliExpress操作日志中间表'
        db_table = u't_erp_aliexpress_action_temp'
    def __unicode__(self):
        return u'id:%s'%(self.id)

class t_erp_aliexpress_action_log(models.Model):
    shopName = models.CharField(u'店铺群号', max_length=64, null=True)
    accountName = models.CharField(u'店铺账号', max_length=64, null=True)
    action_type = models.CharField(u'操作类型', max_length=128, null=True)
    action_param = models.TextField(u'操作数据', null=True,blank=True)
    action_result = models.CharField(u'操作结果', max_length=256, null=True)
    action_time = models.DateTimeField(u'操作时间', null=True)
    action_user = models.CharField(u'执行人', max_length=64, null=True)
    table_name = models.CharField(u'表名', max_length=64, null=True)
    field_name = models.CharField(u'字段名', max_length=64, null=True)
    old_value = models.TextField(u'原始数据', null=True,blank=True)
    action_id = models.PositiveSmallIntegerField(u'操作数据ID', max_length=11, null=True)
    done_time = models.DateTimeField(u'完成时间', null=True)
    remark = models.TextField(u'备注', null=True,blank=True)

    class Meta:
        verbose_name = u'AliExpress操作日志表'
        verbose_name_plural = u'AliExpress操作日志表'
        db_table = u't_erp_aliexpress_action_log'
    def __unicode__(self):
        return u'id:%s'%(self.id)

class t_erp_aliexpress_product_sku(models.Model):
    product_id  = models.CharField(u'商品ID', max_length=64, null=True)
    SKU         = models.CharField(u'商品SKU', max_length=64, null=True)
    ShopSKU     = models.CharField(u'店铺SKU', max_length=128, null=True)
    mutilSKUFlag=models.SmallIntegerField(u'组合SKU标记')
    MainSKU=models.CharField(u'主SKU',max_length=32,blank=True,null=True)
    shopsku_id = models.CharField(u'店铺SKU ID', max_length=128, blank=True, null=True)
    updatetime = models.DateTimeField(u'更新时间')
    GoodsStatus = models.IntegerField(u'sku状态')
    Infringing=models.SmallIntegerField(u'本平台是否侵权')
    InfringingSite=models.CharField(u'侵权站点',max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = u'AliExpress商品ID与SKU对应表'
        verbose_name_plural = u'AliExpress商品ID与SKU对应表'
        db_table = u't_erp_aliexpress_product_sku'
    def __unicode__(self):
        return u'id:%s'%(self.id)

class t_erp_aliexpress_shop_info(models.Model):
    shopName = models.CharField(u'账号(普源)', max_length=64, null=False, blank=False)
    accountName = models.CharField(u'店铺账号', max_length=64, null=False, blank=False)
    sessionkey = models.CharField(u'授权信息', max_length=256, null=True, blank=True)
    user_id = models.CharField(u'账号ID', max_length=32, null=True, blank=True)
    seller_zh = models.CharField(u'销售员(中文)', max_length=32, null=False, blank=False)
    seller_en = models.CharField(u'销售员(英文)', max_length=32, null=True, blank=True)
    session_out_time = models.DateTimeField(u'授权失效时间', null=True, blank=True)
    reflash_online_info_time = models.DateTimeField(u'商品信息刷新时间', null=True, blank=True)
    reflash_order_info_time = models.DateTimeField(u'订单信息刷新时间', null=True, blank=True)
    cata_zh = models.CharField(u'类目', max_length=64, null=False, blank=False)
    shop_status = models.CharField(u'店铺状态', choices=((u'online', u'在用'),(u'offline', u'停用')), default=u'online', max_length=32, null=False, blank=False)
    session_create_time = models.DateTimeField(u'授权生效时间', null=True, blank=True)

    class Meta:
        verbose_name = u'AliExpress账号店铺配置信息表'
        verbose_name_plural = u'AliExpress账号店铺配置信息表'
        db_table = u't_erp_aliexpress_shop_info'
    def __unicode__(self):
        return u'id:%s'%(self.id)

class t_erp_aliexpress_platform_product_unit(models.Model):
    product_unit_id = models.CharField(u'Ali单位ID', max_length=64, null=True)
    product_unit_name_zh = models.CharField(u'单位名(中文)', max_length=64, null=True)
    product_unit_name_en = models.CharField(u'单位名(英文)', max_length=256, null=True)

    class Meta:
        verbose_name = u'AliExpress单位配置信息表'
        verbose_name_plural = u'AliExpress单位配置信息表'
        db_table = u't_erp_aliexpress_platform_product_unit'
    def __unicode__(self):
        return u'id:%s'%(self.id)

class t_erp_aliexpress_freight_template(models.Model):
    shopName = models.CharField(u'账号店铺ALI', max_length=64, null=True)
    template_name = models.CharField(u'模板名称', max_length=64, null=True)
    is_default = models.CharField(u'默认模板', max_length=256, null=True)
    template_id = models.CharField(u'模板ID', max_length=256, null=True)
    accountName = models.CharField(u'账号名称', max_length=256, null=True)

    class Meta:
        verbose_name = u'AliExpress用户运费模板配置表'
        verbose_name_plural = u'AliExpress用户运费模板配置表'
        db_table = u't_erp_aliexpress_freight_template'
    def __unicode__(self):
        return u'id:%s'%(self.id)

class t_erp_aliexpress_shop_promise_template(models.Model):
    shopName = models.CharField(u'账号店铺ALI', max_length=64, null=True)
    template_name = models.CharField(u'模板名称', max_length=64, null=True)
    template_id = models.CharField(u'模板ID', max_length=256, null=True)
    accountName = models.CharField(u'账号名称', max_length=256, null=True)

    class Meta:
        verbose_name = u'AliExpress服务模板配置表'
        verbose_name_plural = u'AliExpress服务模板配置表'
        db_table = u't_erp_aliexpress_shop_promise_template'
    def __unicode__(self):
        return u'id:%s'%(self.id)

class t_erp_aliexpress_shop_product_groups(models.Model):
    shopName = models.CharField(u'账号店铺ALI', max_length=64, null=True)
    group_name = models.CharField(u'分组名称', max_length=64, null=True)
    group_id = models.CharField(u'分组ID', max_length=256, null=True)
    accountName = models.CharField(u'账号名称', max_length=256, null=True)

    class Meta:
        verbose_name = u'AliExpress产品分组配置表'
        verbose_name_plural = u'AliExpress产品分组配置表'
        db_table = u't_erp_aliexpress_shop_product_groups'
    def __unicode__(self):
        return u'id:%s'%(self.id)


class t_erp_aliexpress_config_category(models.Model):
    category_id = models.CharField(u'AliExpress类目ID', max_length=32, null=True)
    category_name_zh = models.CharField(u'类目中文名', max_length=256, null=True)
    category_name_en = models.CharField(u'类目英文名', max_length=256, null=True)
    parent_category_id = models.CharField(u'类目父节点', max_length=32, null=True)
    category_level = models.PositiveSmallIntegerField(u'类目等级', max_length=2, null=True)
    is_leaf = models.CharField(u'叶子节点', max_length=2, null=True)
    full_path_en = models.CharField(u'类目全路径(英文)', max_length=512, null=True)
    full_path_zh = models.CharField(u'类目全路径(中文)', max_length=512, null=True)
    root_category_id = models.CharField(u'根目录ID', max_length=32, null=True)

    class Meta:
        verbose_name = u'AliExpress类目配置表'
        verbose_name_plural = u'AliExpress类目配置表'
        db_table = u't_erp_aliexpress_config_category'

    def __unicode__(self):
        return u'id:%s' % (self.id)

class t_erp_aliexpress_shop_link_daily(models.Model):
    shopName = models.CharField(u'账号(普源)', max_length=64, null=True)
    accountName = models.CharField(u'账号名称', max_length=256, null=True)
    gmt_create = models.CharField(u'统计日期', max_length=256, null=True)
    link_number = models.IntegerField(u'统计数量', max_length=256, null=True)
    seller_zh = models.CharField(u'销售员(中文)', max_length=32, null=False, blank=False)
    submitter = models.CharField(u'刊登人', max_length=32, null=False, blank=False)

    class Meta:
        verbose_name = u'AliExpress链接数统计'
        verbose_name_plural = u'AliExpress链接数统计'
        db_table = u't_erp_aliexpress_shop_link_daily'
        ordering = ['-gmt_create','shopName']
    def __unicode__(self):
        return u'id:%s' % (self.id)

class t_erp_aliexpress_activation_rate(models.Model):
    activation_rate=models.FloatField(u'激活率',max_length=32,null=True,blank=True)
    submitter=models.CharField(u'刊登人',max_length=64,null=True,blank=True)
    category=models.CharField(u'品类',max_length=32,null=True,blank=True)
    updatetime=models.DateField(u'更新日期')
    activation_count=models.IntegerField(u'激活数')
    product_count=models.IntegerField(u'产品数')
    gmt_time = models.CharField(u'刊登日期', max_length=32)


    class Meta:
        verbose_name = u'AliExpress激活率明细'
        verbose_name_plural = u'AliExpress激活率明细'
        db_table = u't_erp_aliexpress_activation_rate'



class t_erp_aliexpress_activation_rate_overview(models.Model):
    rate=models.FloatField(u'激活率')
    updatetime=models.DateField(u'更新日期')
    name=models.CharField(u'名称',max_length=64)
    type=models.SmallIntegerField(u'类别')
    activation_count=models.IntegerField(u'激活数')
    product_count=models.IntegerField(u'产品数')
    gmt_time=models.CharField(u'刊登日期',max_length=32)
    flag=models.SmallIntegerField(u'刊登区间是否已全部更新')


    class Meta:
        verbose_name = u'AliExpress激活率'
        verbose_name_plural = u'AliExpress激活率'
        db_table = u't_erp_aliexpress_activation_rate_overview'


class t_erp_aliexpress_product_daily(models.Model):
    product_id=models.BigIntegerField(u'产品ID',null=True,blank=True)
    shopname=models.CharField(u'店铺名',max_length=64,null=True,blank=True)
    date=models.DateField(u'日期',null=True,blank=True)
    updatetime=models.DateTimeField(u'刷新时间',null=True,blank=True)
    sales=models.IntegerField(u'销量',null=True,blank=True)
    exposed=models.IntegerField(u'曝光量',null=True,blank=True)
    viewed=models.IntegerField(u'浏览量',null=True,blank=True)

    class Meta:
        verbose_name = u'每日销量'
        verbose_name_plural = u'每日销量'
        db_table = u't_erp_aliexpress_product_daily'


    def __unicode__(self):
        return self.product_id


class v_erp_aliexpress_mutation_coefficient(models.Model):
    product_id=models.BigIntegerField(u'产品id')
    week=models.SmallIntegerField(u'周数')
    sales=models.IntegerField(u'周销量')
    wow_sales=models.IntegerField(u'环比增长')
    wow_rate=models.FloatField(u'环比增长率')
    lastweek_sales=models.IntegerField(u'上周销量')
    owner_member_id=models.CharField(u'店铺账号',max_length=32)
    shopName=models.CharField(u'店铺名',max_length=32)
    cata_zh=models.CharField(u'品类',max_length=32)
    submitter=models.CharField(u'刊登人',max_length=32)

    class Meta:
        ordering = [u'-week']
        verbose_name = u'速卖通突变系数'
        verbose_name_plural = u'速卖通突变系数'
        db_table = u'v_erp_aliexpress_mutation_coefficient'


class t_erp_aliexpress_online_info_shelf(t_erp_aliexpress_online_info):

    class Meta:
        verbose_name = u'AliExpress下架'
        verbose_name_plural = verbose_name
        proxy = True
        ordering = ['-id']

    def __unicode__(self):
        return u'id:%s' % (self.id)