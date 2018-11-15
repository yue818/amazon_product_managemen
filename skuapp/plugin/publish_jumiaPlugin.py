# coding=utf-8

import urllib
from xadmin.views import BaseAdminPlugin
from django.template import loader
from skuapp.table.t_online_info_wish import *
from django.db.models import Q
from django.contrib import messages
import logging
from skuapp.table.t_online_info_wait_publish_jumia import *


class publish_jumiaPlugin(BaseAdminPlugin):
    jumia_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.jumia_flag)

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
        #messages.error(self.request,'---%s'%searchList)
        
        if searchList:
            for k,v in searchList.items():
                if k == 'FL__exact':
                    continue
                if k == 'ispublished__exact':
                    searchList.pop('ispublished__exact')
                elif newurl.find('?') != -1:
                    newurl = u'%s&%s=%s'%(newurl,k,v)
                else:
                    newurl = u'%s?%s=%s'%(newurl,k,v)


        paramList = ['&st=yy','&st=nn','&status=HedongCloth','&status=bl','&status=Gadget','&status=BabyToy','&status=WomenBeauty','&status=CoolBag','&status=BDDecor','&status=Shine','&status=Memo','&status=Liberty','&status=Thunder',
                       

                     'st=yy&','st=nn&','status=HedongCloth&','status=bl&','status=Gadget&','status=BabyToy&','status=WomenBeauty&','status=CoolBag&','status=BDDecor&','status=Shine&','status=Memo&','status=Liberty&','status=Thunder&',
                    
                     'st=yy','st=nn','status=HedongCloth','status=bl','status=Gadget','status=BabyToy','status=WomenBeauty','status=CoolBag','status=BDDecor','status=Shine','status=Memo','status=Liberty','status=Thunder',]

   

        if 'status=HedongCloth' in sourceURL:
            flag = 4
        elif 'status=bl' in sourceURL:
            flag = 5
        elif 'status=Gadget' in sourceURL:
            flag = 6
        elif 'status=BabyToy' in sourceURL:
            flag = 7
        elif 'status=WomenBeauty' in sourceURL:
            flag = 8
        elif 'status=CoolBag' in sourceURL:
            flag = 9    
        elif 'status=BDDecor' in sourceURL:
            flag = 10
        elif 'status=Shine' in sourceURL:
            flag = 11
        elif 'status=Memo' in sourceURL:
            flag = 12 
        elif 'status=Liberty' in sourceURL:
            flag = 13 
        elif 'status=Thunder' in sourceURL:
            flag = 14    
        elif 'st=yy' in sourceURL:
            flag = 15
        elif 'st=nn' in sourceURL:
            flag = 16
        

        
      
        else:
            flag = 0

        if '?' in sourceURL:
            for param in paramList:
                if param in sourceURL:
                    sourceURL = sourceURL.replace(param,'')
                    if sourceURL.split('?')[1] == '':
                        sourceURL = sourceURL
                    else:
                        sourceURL = sourceURL + '&'
        else:
            sourceURL = sourceURL + '?' 
   
        countsdict={}
        lm=[]
        oo = t_online_info_wait_publish_jumia.objects.values_list('FL',flat=True)
        #messages.error(self.request,'%s'%oo)
        for i in oo:
            
            if i in lm:
                continue
            else:      
                #print(i.encode('utf-8'))
                if i is not None and i != '':
                    counts = t_online_info_wait_publish_jumia.objects.filter(FL='%s'%i.encode('utf-8'),ispublished='未刊登').count()
                    #countsdict1={i:counts}
                    countsdict = dict( countsdict, **{i:counts})
                    lm.append(i)
        #messages.error(self.request,'%s'%i)
        #messages.error(self.request,'%s'%counts)
        #messages.error(self.request,'%s'%countsdict)
        
 
        nodes.append(loader.render_to_string('publish_jumia.html',{'url':newurl,'flag':flag,'countsdict':countsdict}))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
