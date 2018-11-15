#-*-coding:utf-8-*-

"""
 @desc:  
 @author: changyang  
 @site: 
 @software: PyCharm
 @file: t_wish_pb_earnings_Plugin.py
 @time: 2018-09-28 13:11
"""
import datetime
from xadmin.views import BaseAdminPlugin
from django.template import loader

class t_wish_pb_earnings_Plugin(BaseAdminPlugin):
    t_wishpb_repdesc_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.t_wishpb_repdesc_flag)

    def block_luru(self, context, nodes):

        lastday = datetime.date.today() - datetime.timedelta(days=datetime.date.today().day)
        lastday = lastday.strftime('%Y-%m-%d')

        repdesc = u'PS: 总体数据为2018-03-01~%s交易期间做过广告的链接....' % lastday

        nodes.append(loader.render_to_string('SKU.html', {'rt': repdesc}))