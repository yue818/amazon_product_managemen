#-*-coding:utf-8-*-
from skuapp.table.t_online_info_amazon import *
"""  
 @desc:  amazon店铺铺货列表
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_templet_public_amazon_listing.py
 @time: 2017/12/15 19:25
"""

class t_templet_public_amazon_listing(t_online_info_amazon):
    class Meta:
        verbose_name = u'amazon铺货Listing'
        verbose_name_plural = verbose_name
        proxy = True

    def __unicode__(self):
        return u'id:%s' % (self.id)