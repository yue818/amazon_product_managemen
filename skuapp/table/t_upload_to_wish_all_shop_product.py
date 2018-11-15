# -*- coding: utf-8 -*-
from skuapp.table.t_online_info_wish import t_online_info_wish


class t_upload_to_wish_all_shop_product(t_online_info_wish):
    
    class Meta:
        verbose_name=u'Wish铺货店铺全部商品表'
        verbose_name_plural=verbose_name
        db_table = 't_online_info_wish'
        proxy = True
        ordering = ['-Orders7Days']
    def __unicode__(self):
        return u'id:%s'%(self.id)