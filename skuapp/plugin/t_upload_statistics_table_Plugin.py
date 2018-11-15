# -*- coding: utf-8 -*-
import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView,ModelFormAdminView,CommAdminView,BaseAdminView
from skuapp.table.t_upload_statistics_table import t_upload_statistics_table
from django.template import loader
from django.db.models import Q
from django.db.models import Sum
import logging
from django.contrib import messages

class t_upload_statistics_table_Plugin(BaseAdminPlugin):
    upload_statistics = False

    def init_request(self, *args, **kwargs):
        return bool(self.upload_statistics)

    # def get_media(self, media):
        # media.add_js([self.static('xadmin/js/xadmin.plugin.button.color.js')])
        # return media
        
    # def not_empty(self,s):
        # return s and s.strip()
    # filter(not_empty, ['A', '', 'B', None, 'C', '  '])

    def block_search_cata_nav(self, context, nodes):
        logger = logging.getLogger('sourceDns.webdns.views')
        
        searchList = {}
        param_seach = ''
        strUrl = str(context['request']).split("'")[1]
        # ?  _p_   staTime__gte=2017-10-16     _p_staTime__lt=2017-10-25     _q_=17935
        URL_list = strUrl.split('?')
        if len(URL_list)>=2 and URL_list[1].strip() != '': #   and URL_list[1].find('&') != -1 
            param_list = URL_list[1].split('&') # 不管有多个参数 都来一发
            for param in param_list:
                if param.find('_q_=') != -1 :
                    param_seach = param.split('_q_=')[1]#发现搜索框内 内容  唯一
                elif param.find('_p_') != -1 :
                    param_k_v = param.split('_p_')[1].split('=')  #  ['staTime__gte','2017-10-16']
                    if param_k_v[1].strip() != '' and param_k_v[1].strip() != 'True' and param_k_v[1].strip() != 'False':
                        searchList[param_k_v[0]] = param_k_v[1]
                    elif param_k_v[1].strip() == 'True':
                        searchList[param_k_v[0]] = True
                    elif param_k_v[1].strip() == 'False':
                        searchList[param_k_v[0]] = False
                else:
                    continue
                    
        if searchList:
            objs = t_upload_statistics_table.objects.filter(**searchList)
        else:
            objs = t_upload_statistics_table.objects.all()
            
        logger.error("---------------------%s"%(objs))
        shopname_all = []
        for obj in objs:
            shoplist = []
            if obj.ShopName is not None:
                shoplist = obj.ShopName.split(',')
            shopname_all = shopname_all + shoplist
            
        while '' in shopname_all:
            shopname_all.remove('')
            
        shopname_nub = len(set(shopname_all))
        Summary = objs.aggregate(UplLoad=Sum('UplLoad_nub'),Upload_suc=Sum('Upload_suc_nub'),SKU=Sum('SKU_nub'),online=Sum('online_nub'),order=Sum('order_nub'),orderofday=Sum('orderofeday'),orders_nu=Sum('orders'),soldofday=Sum('soldofeay'),sold_all=Sum('sold'),Integrity=Sum('Integrity_nub'))#.values('UplLoad', 'Shop','SKU', 'online','order','rate','orders_nu', 'sold_all','Integrity')
        
        vs = []
        vs.append(u'铺货店铺总数:%s'%shopname_nub) 
        if Summary['order'] is not None and Summary['Upload_suc'] is not None:
            vs.append(u'总出单链接率:%s'%(Summary['order']*1.0/Summary['Upload_suc'])) 
        else:
            vs.append(u'总出单链接率:0')
        # {'Shop': 3911, 'SKU': 1185, 'sold_all': 277, 'orders_nu': 94, 'rate': 0, 'UplLoad': 99076, 'online': 4225, 'Integrity': 0, 'order': 60}
        for k,v in Summary.items():
            if k == 'UplLoad':
                vs.append(u'铺货总数:%s'%v)
            if k == 'SKU':
                vs.append(u'铺货SKU总数:%s'%v)
            if k == 'online':
                vs.append(u'铺货在线总数:%s'%v)
            if k == 'order':
                vs.append(u'出单链接总数:%s'%v)
            if k == 'orders_nu':
                vs.append(u'链接订单总数:%s'%v)
            if k == 'sold_all':
                vs.append(u'链接销售总金额:%s'%v)
            if k == 'Integrity':
                vs.append(u'诚信店铺总数:%s'%v)
            if k == 'orderofday':
                vs.append(u'日订单总数:%s'%v)
            if k == 'soldofday':
                vs.append(u'日销售总金额:%s'%v)
            if k == 'Upload_suc':
                vs.append(u'铺货成功总数:%s'%v)
        #vs = sorted(vs)
        # 铺货总数:
        # 铺货店铺总数:
        # 铺货SKU总数:
        # 铺货在线总数:
        # 出单链接总数:
        # 总出单链接率:
        # 总订单数:
        # 销售总金额:
        # 诚信店铺总数:
        
        nodes.append(loader.render_to_string('upload_statistics_table.html',{ 'vs': vs}))