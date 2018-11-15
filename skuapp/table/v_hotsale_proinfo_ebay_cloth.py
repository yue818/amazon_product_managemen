# -*- coding: utf-8 -*-
from t_hotsale_proinfo_ebay import t_hotsale_proinfo_ebay
#17)    已录入商品信息 v_product_enter_ed
class v_hotsale_proinfo_ebay_cloth(t_hotsale_proinfo_ebay):
    class Meta:
        verbose_name=u'服装类热销产品'
        verbose_name_plural=u'服装类热销产品'
        proxy = True
    def __unicode__(self):
        return u'%s'%(self.id)