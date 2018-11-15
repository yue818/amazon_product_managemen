# -*-coding:utf-8-*-

from django.db import models
class t_amazon_pro_comment(models.Model):
    id             = models.IntegerField(u'流水号', primary_key=True)
    imageurl       = models.CharField(u'产品图片', max_length=255, blank=True, null=True)
    title          = models.CharField(u'产品标题', max_length=255, blank=True, null=True)
    asin           = models.CharField(u'产品asin号', max_length=32)
    star           = models.CharField(u'评论星级', max_length=32, blank=True, null=True)
    comment_title  = models.CharField(u'评论标题', max_length=255)
    customer       = models.CharField(u'评论人', max_length=255, blank=True, null=True)
    comment_time   = models.CharField(u'评论时间', max_length=32, blank=True, null=True)
    color          = models.CharField(u'产品颜色', max_length=64, blank=True, null=True)
    si             = models.CharField(u'产品尺寸', max_length=64, blank=True, null=True)
    other          = models.CharField(u'产品其他属性', max_length=64, blank=True, null=True)
    comment        = models.TextField(u'评论内容')
    get_time       = models.CharField(u'获取时间', max_length=255, blank=True, null=True)

    class Meta:
        db_table = 't_amazon_pro_comment'
        verbose_name = u'商品评论展示'
        verbose_name_plural = u'商品评论展示'

    def __unicode__(self):
        return u'%s' % (self.comment_title, )