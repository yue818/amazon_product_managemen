# -*- coding: utf-8 -*-
import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView,ModelFormAdminView,CommAdminView,BaseAdminView
from skuapp.table.t_upload_statistics_table import t_upload_statistics_table
from django.template import loader,Context  
from django.db.models import Q
from django.db.models import Sum
import logging
from django.contrib import messages
from django.template import RequestContext
import urllib

class t_goods_shelves_search_Plugin(BaseAdminPlugin):
    shelves_search = False
    def init_request(self, *args, **kwargs):
        return bool(self.shelves_search)

    # def get_media(self, media):
        # media.add_js([self.static('xadmin/js/xadmin.plugin.button.color.js')])
        # return media
        
    # def not_empty(self,s):
        # return s and s.strip()
    # filter(not_empty, ['A', '', 'B', None, 'C', '  '])

    def block_search_cata_nav(self, context, nodes):
        request = self.request
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
                    if param.split('_p_')[1].find('=') != -1:
                        param_k_v = param.split('_p_')[1].split('=')  #  ['staTime__gte','2017-10-16']
                        #logger.error("---------------------%s"%(param_k_v))
                        if param_k_v[0].find('__gte') != -1 or param_k_v[0].find('__lt') != -1 :
                            if param_k_v[1].strip() != '' and param_k_v[1].strip() != 'True' and param_k_v[1].strip() != 'False':
                                searchList[param_k_v[0]] = urllib.unquote(param_k_v[1])
                            elif param_k_v[1].strip() == 'True':
                                searchList[param_k_v[0]] = True
                            elif param_k_v[1].strip() == 'False':
                                searchList[param_k_v[0]] = False
                                
                        else:
                            param_k = param_k_v[0].split('__')[0]
                            if param_k_v[1].strip() != '' and param_k_v[1].strip() != 'True' and param_k_v[1].strip() != 'False':
                                searchList[param_k] = urllib.unquote(param_k_v[1])
                            elif param_k_v[1].strip() == 'True':
                                searchList[param_k] = True
                            elif param_k_v[1].strip() == 'False':
                                searchList[param_k] = False

                else:
                    continue
                    
        searchs = [
                {'id':'ShopName','descri':'店铺名','values':''},
                {'id':'SKU','descri':'商品SKU','values':''},
                {'id':'MainSKU','descri':'主SKU','values':''}
                ]#输入框
                
        selects = [{'id':'GoodsStatus','descri':'商品状态',
                 'defultvalue': {u'清仓下架': 'Clearance', u'售完下架': 'over', u'处理库尾': 'Handle',
                                 u'临时下架': 'temporary', u'清仓合并': 'merge', u'正常': 'normal',u'全部': 'all'},
                 'values':'all'},
                 ]#多选框
                 
        search_range = [{'id':'Orders7Days','descri':'7天order数','values_Start': '', 'values_End': ''},
                        {'id':'OfSales','descri':'订单量','values_Start': '', 'values_End': ''}
                         ]#范围输入框
                         
        selects_one = [{'id':'APIState','descri':'API执行状态',
                         'defultvalue': {u'还未执行': 'nothing',u'执行失败': 'Error', u'正在执行': 'runing',u'等待执行': 'wait',u'全部': 'all'},
                         'values':'all'},
                         ]#单选框
                
        if searchList:
            for search in searchs:
                if searchList.has_key(search['id']):
                    search['values'] = searchList[search['id']] #输入框 值

            for select in selects:
                if searchList.has_key(select['id']):
                    select['values'] = searchList[select['id']].split(',') #多选框 值
            
            for search_r in search_range: # Orders7Days__gte
                kl = '%s__gte'%search_r['id']
                kz = '%s__lt'%search_r['id']
                if searchList.has_key(kl):
                    search_r['values_Start'] = searchList[kl]#范围输入框 值
                if searchList.has_key(kz):
                    search_r['values_End'] = searchList[kz]
            
            for select_one in selects_one:
                if searchList.has_key(select_one['id']):
                    select_one['values'] = searchList[select_one['id']] #单选框 值

        logger.error("1---------------------%s"%(search_range))
        logger.error("2---------------------%s"%(searchList))

        nodes.append(loader.render_to_string('shelves_search.html',{ 'searchList': searchList,'searchs':searchs,
                                                                     'selects':selects,'search_range':search_range,
                                                                     'selects_one':selects_one,'URL_list':URL_list[0]},
                                                                    context_instance=RequestContext(request)))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        