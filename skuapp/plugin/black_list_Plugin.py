# coding=utf-8

from xadmin.views import BaseAdminPlugin
from django.template import loader
from skuapp.table.p_trade_blacklist_zip import *
from django.db.models import Q
from django.contrib import messages
import logging
from urllib import unquote


class black_list_Plugin(BaseAdminPlugin):
    bla = False

    def init_request(self, *args, **kwargs):
        return bool(self.bla)

    def get_media(self, media):
        media.add_js([self.static('xadmin/js/xadmin.plugin.button.color.js')])
        return media

    def block_search_cata_nav(self, context, nodes):
        sourceURL = str(context['request']).split("'")[1]
        searchList = {}
        param_seach = ''
        #if sourceURL.find('?_p_FL__exact=') != -1:
        # /Project/admin/skuapp/t_online_info_wait_publish/?_p_FL__exact=Bra&_cols=id.show_Picture.show_ShopName_Seller.Orders7Days.OfSales.show_Title_ProductID.show_SKU_list.Status.show_time.show_orders7days.FL
        newurl = ''
        if sourceURL.find('_p_FL__exact=') != -1:
            #sourceURL.replace('_p_FL__exact=',)
            URL_list = sourceURL.split('?')
            newurl = URL_list[0]
            if len(URL_list)>=2 and URL_list[1].strip() != '': #   and URL_list[1].find('&') != -1 
                param_list = URL_list[1].split('&') # 不管有多个参数 都来一发
                for param in param_list:
                    if param.find('_q_=') != -1 :
                        param_seach = param.split('_q_=')[1]#发现搜索框内 内容  唯一
                    elif param.find('_p_') != -1 :
                        if param.split('_p_')[1].find('=') != -1:
                            param_k_v = param.split('_p_')[1].split('=')  #  ['staTime__gte','2017-10-16']
                            #param_k = param_k_v[0].split('__')[0]
                            if param_k_v[1].strip() != '' and param_k_v[1].strip() != 'True' and param_k_v[1].strip() != 'False':
                                searchList[param_k_v[0]] = urllib.unquote(param_k_v[1])
                            elif param_k_v[1].strip() == 'True':
                                searchList[param_k_v[0]] = True
                            elif param_k_v[1].strip() == 'False':
                                searchList[param_k_v[0]] = False

                    else:
                        continue
        if searchList:
            for k,v in searchList.items():
                if k == 'Operate':
                    continue
                elif newurl.find('?') != -1:
                    newurl = u'%s?%s=%s'%(newurl,k,v)
                else:
                    newurl = u'%s&%s=%s'%(newurl,k,v)
            newurl = newurl + '?'
        else:
            newurl = newurl
            
        paramList = ['&Operate=0','&Operate=1','&Operate=2',
                    'Operate=0&','Operate=1&','Operate=2&',
                     'Operate=0','Operate=1','Operate=2',]

   

        if 'Operate=0' in sourceURL:
            flag = 1
        elif 'Operate=1' in sourceURL:
            flag = 2
        elif 'Operate=2' in sourceURL:
            flag = 3
        else:
            flag = 0
        try:    
            show_time_obj = p_trade_blacklist_zip.objects.latest('NID').TbTime
        except:
            show_time_obj=''

        nodes.append(loader.render_to_string('bl.html',
                                             {'url':newurl, 'flag':flag,'show_time_obj':show_time_obj}))
