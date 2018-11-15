# coding=utf-8

from xadmin.views import BaseAdminPlugin
from django.template import loader
from skuapp.table.t_product_inventory_warnning import *
import decimal
from django.contrib import messages
import urllib

class kc_get_money(BaseAdminPlugin):
    kc_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.kc_flag)
        
    def block_search_cata_nav(self, context, nodes):
        sourceURL = str(context['request']).split("'")[1]
        
        qs = t_product_inventory_warnning.objects.all()
        allMoney = decimal.Decimal("%.2f" % float(0.0))
        if '?' in sourceURL:
            searchList = sourceURL.split('?')[1].split('&')
            searchDict = {}
            if searchList:
                for eachSearch in searchList:
                    searchDict[eachSearch.split('=')[0]] = eachSearch.split('=')[1]
            
            testList = {'MainSKU':'','Purchaser':'','radio':'','tortinfo':'','storeName':'',
                        'SalerName':'','HandleResults':'','orders7DaysStart':'','orders7DaysEnd':'','GoodsCategoryID':'',
						'AllAvailableNumberStart':'','AllAvailableNumberEnd':''}
            for k,v in searchDict.items():
                for testKey,testValue in testList.items():
                    if k == testKey:
                        testList[testKey] = v
            searchAllList = {'MainSKU__exact': testList['MainSKU'],'Purchaser__in': testList['Purchaser'],
                            'radio__lte': testList['radio'],'SalerName__exact': testList['SalerName'],
							'AllAvailableNumber__gte': testList['AllAvailableNumberStart'], 'AllAvailableNumber__lt': testList['AllAvailableNumberEnd'],
                            'storeName__icontains': testList['storeName'],'GoodsCategoryID__exact': testList['GoodsCategoryID'],
                            'HandleResults__exact': testList['HandleResults'],'tortinfo__exact': testList['tortinfo'],
                            'order7daysAll__gte': testList['orders7DaysStart'], 'order7daysAll__lt': testList['orders7DaysEnd']}
            sl = {}
            for k,v in searchAllList.items():
                if isinstance(v,list):
                    if v:
                        sl[k] = v
                else:
                    if v is not None and v.strip() != '':
                        sl[k] = urllib.unquote(v)
            if sl is not None:
                #messages.error(self.request, sl)
                try:
                    qs = qs.filter(**sl)
                except:
                    pass
        #messages.error(self.request, qs)    
        for eachQs in qs:
            allMoney += eachQs.AllMoney
        
        nodes.append(loader.render_to_string('kc_get_money.html',
                                             {'allMoney': allMoney}))