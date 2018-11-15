#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: t_tort_info_result.py
 @time: 2018-05-07 13:57
"""
from t_tort_info import t_tort_info
class t_tort_info_result(t_tort_info):
    class Meta:
        verbose_name = u'严重侵权'
        verbose_name_plural = u'严重侵权'
        db_table = 't_tort_info'
        ordering = ['-DealTime1']
        proxy = True

    def __unicode__(self):
        return u'%s %s %s' % (self.ID, self.Site, self.MainSKU)