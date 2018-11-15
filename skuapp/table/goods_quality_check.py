# coding:utf8
from __future__ import unicode_literals

from django.db import models


# Create your models here.

class Newshop_feedback(models.Model):
    """
    平台提交表
    """
    choice = [
        ('wish', 'wish'),
        ('ebay', 'ebay'),
        ('Amazon', 'Amazon'),
        ('速卖通', '速卖通'),
        ('Lazada', 'Lazada'),
        ('Cdiscount', 'Cdiscount'),
        ('Joom', 'Joom'),
        ('Shopee', 'Shopee'),
        ('Tophatter', 'Tophatter '),
        ('其它', '其它 '),

    ]

    choice1 = [
        ('仓储部-发错货', '仓储部-发错货'),
        ('仓储部-漏发货', '仓储部-漏发货'),
        ('仓储部-点货', '仓储部-点货'),
        ('仓储部-质检问题', '仓储部-质检问题'),
        ('质检问题', '仓储部-上错架'),
        ('产品部-尺寸问题', '产品部-尺寸问题'),
        ('产品部-质量问题', '产品部-质量问题'),
        ('产品部-预包问题', '产品部-预包问题'),
        ('侵权', '侵权'),
        ('产品已下架', '产品已下架 '),
        ('其它', '其它 '),
    ]

    choice2 = [
        ('C001-发错货（款式）', 'C001-发错货（款式）'),
        ('C001-发错货（颜色）', 'C001-发错货（颜色）'),
        ('C001-发错货（数量）', 'C001-发错货（数量）'),
        ('C002-漏发货（***）', 'C002-漏发货（***）'),
        ('C003-贴错SKU（***）', 'C003-贴错SKU（***）'),
        ('C004-(服装，产品破损，有污渍等)', 'C004-(服装，产品破损，有污渍等)'),
        ('C005-产品放错架导致发货错误(***)', 'C005-产品放错架导致发货错误(***)'),
        ('P001-尺寸太大(***)', 'P001-尺寸太大(***)'),
        ('P002-尺寸太小(***)', 'P002-尺寸太小(***)'),
        ('P003-产品本质问题（色差，实物与图片不符等）', 'P003-产品本质问题（色差，实物与图片不符等）'),
        ('P004-产品破损', 'P004-产品破损'),

    ]



    terrace = models.CharField(max_length=60, choices=choice, blank=True, null=False, verbose_name=u'平台')
    order_number = models.CharField(max_length=200, blank=True, null=False, verbose_name=u'浦沅订单编号')
    sku = models.CharField(max_length=60, blank=True, null=True, verbose_name='Sku')
    request_type = models.CharField(max_length=60, choices=choice1, blank=True, null=False, verbose_name=u'问题类型')
    requset_response = models.CharField(max_length=60, choices=choice2, blank=True, null=False, verbose_name=u'具体反馈')
    others=models.TextField(blank=True,null=False,default='此处填写备注原因',verbose_name=u'其他原因说明')
    picture = models.ImageField(upload_to='http://oss-cn-shanghai.aliyuncs.com/fancyqube-dev', verbose_name=u'图片上传1')
    picture1 = models.ImageField(upload_to='statics/images',blank=True,null=True,verbose_name=u'图片上传2')
    picture2 = models.ImageField(upload_to='static/img',blank=True,null=True,verbose_name=u'图片上传3')
    put_time = models.DateTimeField(auto_now_add=True, verbose_name=u'提交日期')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'更新日期')

    class Meta:
        verbose_name = u'平台提交'
        verbose_name_plural = u'平台提交'
        

    def __unicode__(self):
        return self.sku


class GoodsResponse_table(models.Model):
    """
    产品专员反馈表
    """
    choice1 = [
        ('通过', '通过'),
        ('未通过', '未通过'),
        ('未审核', '未审核'),

    ]
    sku = models.CharField(max_length=60, blank=True, null=True, verbose_name='sku')
    name = models.CharField(max_length=60, blank=True, null=True, verbose_name=u'产品专员')
    supplier_name = models.CharField(max_length=60, blank=True, null=True, verbose_name=u'供应商')
    goods_name = models.CharField(max_length=60, blank=True, null=True, verbose_name=u'产品名称')
    remark = models.TextField(blank=False, verbose_name=u'备注')
    time = models.DateTimeField(auto_now_add=True, verbose_name=u'反馈日期')
    updata_time = models.DateTimeField(auto_now=True, verbose_name=u'反馈更新日期')



    class Meta:
        verbose_name = u'产品专员反馈信息'
        verbose_name_plural = u'产品专员反馈信息'
        

    def __unicode__(self):
        return '%s,%s,%s,%s'%(self.name, self.supplier_name, self.goods_name, self.remark)


class BugerResponse_table(models.Model):
    """
    采购员反馈表

    """


    choice1 = [
        ('通过', '通过'),
        ('未通过', '未通过'),
        ('未审核', '未审核'),

    ]
    sku = models.CharField(max_length=60, blank=True, null=True, verbose_name='sku')
    name = models.CharField(max_length=60, blank=True, null=True, verbose_name=u'采购专员')
    supplier_name = models.CharField(max_length=60, blank=True, null=True, verbose_name=u'供应商')
    goods_name = models.CharField(max_length=60, blank=True, null=True, verbose_name=u'产品名称')
    goods_category = models.CharField(max_length=60, blank=True, null=True, verbose_name=u'产品分类')

    remark = models.TextField(blank=False, verbose_name=u'备注')
    time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'更新时间')



    class Meta:
        verbose_name = u'采购员反馈信息'
        verbose_name_plural = u'采购员反馈信息'
        

    def __unicode__(self):
        return '%s'%(self.name)


class WarehouseSpecialist_table(models.Model):
    """
    仓库负责人

    """
    choice1 = [
        ('通过', '通过'),
        ('未通过', '未通过'),
        ('未审核', '未审核'),

    ]
    sku = models.CharField(max_length=60, blank=True, null=True, verbose_name='sku')
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name='仓库负责人')
    # charge_number = models.ForeignKey(BugerResponse_table, verbose_name=u'采购详情')
    # admin中设置自定义字段  仓库剩余产品数量
    goods_numbers = models.IntegerField(blank=True, null=True, verbose_name=u'采购数量')
    remark = models.TextField(blank=False, verbose_name=u'备注')
    time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'更新时间')



    class Meta:
        verbose_name = u'仓库反馈信息'
        verbose_name_plural = u'仓库反馈信息'
       

    def __unicode__(self):
        return '%s' % (self.sku)



class GoodsCheck_table(models.Model):
    """
    品控组审核

    """
    choice1 = [
    ('通过', '通过'),
    ('未通过', '未通过'),
    ('未审核', '未审核'),

    ]


    sku = models.CharField(max_length=60, blank=True, null=True, verbose_name='sku')
    name = models.CharField(max_length=60, blank=False, verbose_name='审核人')
    # goodsResponse_relation = models.ForeignKey(GoodsResponse_table, verbose_name=u'产品专员反馈信息')
    goodsResponse_result = models.CharField(max_length=60, choices=choice1, verbose_name=u'产品专员反馈审核')
    # bugerResponse_relation = models.ForeignKey(BugerResponse_table, verbose_name=u'采购员反馈信息')
    bugerResponse_result = models.CharField(max_length=60, choices=choice1, verbose_name=u'采购反馈审核')
    # warehouseSpecialist_relation = models.ForeignKey(WarehouseSpecialist_table, verbose_name=u'仓库反馈信息')
    warehouseSpecialist_result = models.CharField(max_length=60, choices=choice1, verbose_name=u'仓库负责人反馈审核')
    time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'更新时间')

    class Meta:
        verbose_name = u'品控组审核'
        verbose_name_plural = u'品控组审核'
        

    def __unicode__(self):
        return '%s'%(self.sku)







class Result_table(models.Model):
    """
    结果规整表
    """

    choice1 = [
        ('通过', '通过'),
        ('未通过', '未通过'),
        ('未审核', '未审核'),

    ]
    sku = models.CharField(max_length=60, blank=True, null=True, verbose_name='sku')
    gooods_check_man=models.CharField(max_length=60,blank=True,null='True',verbose_name=u'产品审核反馈人')
    goodsResponse_result = models.CharField(max_length=60, choices=choice1, default=3,verbose_name=u'产品专员反馈审核')
    buger_check_man = models.CharField(max_length=60, blank=True,null='True', verbose_name=u'产品审核反馈人')
    bugerResponse_result = models.CharField(max_length=60, choices=choice1,default=3, verbose_name=u'采购反馈审核')
    warehouse_check_man = models.CharField(max_length=60, blank=True,null='True', verbose_name=u'产品审核反馈人')
    warehouseSpecialist_result = models.CharField(max_length=60, choices=choice1,default=3,verbose_name=u'仓库负责人反馈审核')
    # GoodsResponse = models.ForeignKey(GoodsResponse_table, verbose_name=u'产品专员反馈与处理结果')
    # BugerResponse = models.ForeignKey(BugerResponse_table, verbose_name=u'采购反馈与处理结果')
    # WarehouseSpecialist = models.ForeignKey(WarehouseSpecialist_table, verbose_name=u'仓库负责人反馈与处理结果')
    time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'更新时间')

    class Meta:
        verbose_name = u'结果规整信息'
        verbose_name_plural = u'结果规整信息'
        

    def __unicode__(self):
        return '%s'%(self.gooods_check_man)





