#-*-coding:utf-8-*-

"""  
 @author: wushiyang 
 @email:2881591222@qq.com
 @time: 2018-04-29 15:43
 @desc: 
"""


class t_aliexpress_distribution_shop_Admin(object):
    list_display=[u"ShopCode",u"ShopName",u"AccountGroup"]
    list_editable=[u"ShopCode",u"ShopName",u"AccountGroup"]
    search_fields=[u"ShopCode",u"ShopName",u"AccountGroup"]