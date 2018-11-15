# coding=utf-8


from skuapp.table.t_online_info_ebay import *

class t_templet_public_ebay_listing(t_online_info_ebay):
    class Meta:
        verbose_name = u'eBay铺货Listing'
        verbose_name_plural = verbose_name
        proxy = True

    def __unicode__(self):
        return u'id:%s' % (self.id)