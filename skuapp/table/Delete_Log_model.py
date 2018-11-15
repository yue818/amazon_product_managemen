#-*-coding:utf-8-*-

"""  
 @author: wushiyang 
 @email:2881591222@qq.com
 @time: 2018-05-17 17:15
 @desc: 
"""

from django.db import models

class Delete_Log_Model(models.Model):
    username=models.CharField(u'姓名',max_length=32,null=True)
    actiontime=models.DateTimeField(u'操作日期',null=True)
    actiontype=models.CharField(u'操作类型',default=u'delete',max_length=16)
    delete_content=models.TextField(u'被删除内容')
    where=models.CharField(u'被操作页',max_length=64,null=True)
    sku=models.CharField(u'sku',max_length=32,null=True)

    class Meta:
        verbose_name=u'删除信息表'
        verbose_name_plural=u'删除信息表'
        db_table = u'delete_action_log'

