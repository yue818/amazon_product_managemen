# coding=utf-8


from skuapp.table.t_online_info_wish import *

class t_templet_public_wish_listing(t_online_info_wish):
    class Meta:
        verbose_name = u'WISH铺货Listing'
        verbose_name_plural = verbose_name
        proxy = True

    def __unicode__(self):
        return u'id:%s' % (self.id)