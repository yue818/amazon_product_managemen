#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: t_tort_info_sync.py
 @time: 2018-05-16 13:43
"""

from t_tort_info import t_tort_info
class t_tort_info_sync(t_tort_info):
    class Meta:
        verbose_name = u'侵权信息同步'
        verbose_name_plural = u'侵权信息同步'
        db_table = 't_tort_info'
        ordering = ['-ID']
        proxy = True

    def __unicode__(self):
        return u'%s %s %s' % (self.ID, self.Site, self.MainSKU)