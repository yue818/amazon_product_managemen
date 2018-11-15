# -*- coding: utf-8 -*-
from t_api_schedule import t_api_schedule
#API指令执行计划
class t_api_schedule_ing(t_api_schedule):

    class Meta:
        verbose_name=u'API指令执行计划'
        verbose_name_plural=u'API指令执行计划'
        db_table = 't_api_schedule_ing'
        ordering =  ['id']
    def __unicode__(self):
        return u'id:%s CMDID:%s'%(self.id,self.CMDID)
