#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: t_tort_info_cancel.py
 @time: 2018-05-08 17:42
"""

from t_tort_info import t_tort_info
class t_tort_info_cancel(t_tort_info):
    class Meta:
        verbose_name = u'撤销侵权'
        verbose_name_plural = u'撤销侵权'
        db_table = 't_tort_info'
        ordering = ['-ID']
        proxy = True

    def __unicode__(self):
        return u'%s %s %s' % (self.ID, self.Site, self.MainSKU)