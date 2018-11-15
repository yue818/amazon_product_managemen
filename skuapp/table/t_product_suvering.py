# -*-coding:utf-8 -*-
from django.db import models
class t_product_suvering(models.Model):
	id               =          models.AutoField(u'业务流水号',primary_key=True)
	suvering_time    =          models.DateTimeField(u'调研时间',blank=True,null=True)
	sourcepic_path   =          models.CharField(u'图片',max_length=200,blank=True,null=True)
	product_id       =			models.CharField(u'产品id',max_length=200,blank=True,null=True)
	title		     =			models.CharField(u'标题',max_length=2048,blank=True,null=True)
	category		 = 			models.CharField(u'所属分类',max_length=255,blank=True,null=True)
	price			 =    		models.CharField(u'反向售价',max_length=10,blank=True,null=True)
	price2			 =			models.CharField(u'入口价',max_length=10,blank=True,null=True)
	link			 = 			models.CharField(u'对手链接情况',max_length=100,null=True)
	sale_time		 =			models.DateField(u'上架时间',blank=True,null=True)
	sale_number		 = 			models.IntegerField(u'boughtthis',max_length=11,blank=True,null=True)
	comment_number   =			models.IntegerField(u'rating_num',max_length=11,blank=True,null=True)
	point			 =			models.DecimalField(u'rating',max_digits=6,decimal_places=2,blank=True,null=True)
	little_flames	 =			models.CharField(u'小火苗',max_length=200,blank=True,null=True)
	rank			 =	  		models.CharField(u'排名',max_length=100,blank=True,null=True)
	PB				 =			models.IntegerField(u'有无PB',max_length=2,blank=True,null=True)
	saler            =			models.CharField(u'调研人员',max_length=20,blank=True,null=True)
	suvering_is		 =			models.CharField(u'调研状态',max_length=100,blank=True,null=True)
	rating_details   =          models.TextField(u'评论详情',blank=True,null=True)
	getinfo_time     =          models.DateTimeField(u'更新时间',blank=True,null=True)
	getinfo_status   =          models.CharField(u'更新状态', max_length=255, blank=True, null=True)
	sevenratingnum   =          models.IntegerField(u'7天评论数', max_length=11, blank=True, null=True)
	status           =          models.IntegerField(u'状态标识', max_length=2, blank=True, null=True)
	getinfo_remark   =          models.CharField(u'调研备注', max_length=1024, blank=True, null=True)
	getinfo_cate     =          models.CharField(u'调研分类', max_length=255, blank=True, null=True)
	link_1688        =          models.CharField(u'1688链接', max_length=2048, blank=True, null=True)

	class Meta:
		verbose_name =u'竞品调研'
		verbose_name_plural =verbose_name
		db_table = 't_product_suvering'
		ordering = ['-id']

	def __unicode__(self):
		return u'%s' % (self.id)


