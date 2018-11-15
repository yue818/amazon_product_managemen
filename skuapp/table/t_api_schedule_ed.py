# -*- coding: utf-8 -*-
from t_api_schedule import t_api_schedule
#API指令执行计划完成表
class t_api_schedule_ed(t_api_schedule):
    class Meta:
        verbose_name=u'API指令执行计划完成表'
        verbose_name_plural=u'API指令执行计划完成表'
        db_table = 't_api_schedule_ed'
        ordering =  ['id']
    def __unicode__(self):
        return u'id:%s CMDID:%s'%(self.id,self.CMDID)
