#-*-coding:utf-8-*-

"""  
 @author: wushiyang 
 @email:2881591222@qq.com
 @time: 2018-04-21 16:03
 @desc: 
"""


from django.db import models

class t_aliexpress_distribution_shop(models.Model):
    ShopCode=models.CharField(u'卖家编号',max_length=16)
    ShopName=models.CharField(u'卖家简称',max_length=32)
    AccountGroup=models.CharField(u'账号群',max_length=8)
    #UpdateTime=models.DateTimeField(u'最近铺货时间')


    class Meta:
        verbose_name=u'填写铺货店铺'
        verbose_name_plural=u'填写铺货店铺'
        db_table = 't_aliexpress_distribution_shop'
        ordering =  ['AccountGroup']
    def __unicode__(self):
        return u'%s'%(self.ShopCode,)
