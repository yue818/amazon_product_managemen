#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: t_tort_info_audit.py
 @time: 2018-05-07 13:44
"""
from t_tort_info import t_tort_info
class t_tort_info_audit(t_tort_info):
    class Meta:
        verbose_name = u'侵权审核'
        verbose_name_plural = u'侵权审核'
        db_table = 't_tort_info'
        ordering = ['-ID','MainSKU', 'Site']
        proxy = True

    def __unicode__(self):
        return u'%s %s %s' % (self.ID, self.Site, self.MainSKU)


