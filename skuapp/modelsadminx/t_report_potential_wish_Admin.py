# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
import time
import datetime
from django.forms import TextInput, Textarea
from skuapp.table.t_report_potential_wish import *
from skuapp.table.t_online_info import *
from skuapp.table.t_store_configuration_file import *
from skuapp.modelsadminx.t_online_info_wish_Admin import t_online_info_wish_Admin
from django.db.models import Q

class t_report_potential_wish_Admin(t_online_info_wish_Admin):
    wish_listing_secondplugin = False
    wish_listing_readonly_f = False
    search_fields =None
    search_flag = True
    
    def get_list_queryset(self,):
        request = self.request
        qs = super(t_report_potential_wish_Admin, self).get_list_queryset().filter(DateUploaded__lte=(datetime.datetime.utcnow()+datetime.timedelta(days=-1)).strftime('%Y-%m-%d'),DateUploaded__gte=(datetime.datetime.utcnow()+datetime.timedelta(days=-15)).strftime('%Y-%m-%d'))
        status = request.GET.get('status', '')
        shopname = request.GET.get('shopname','')
        seller = request.GET.get('seller','')
        reviewState = request.GET.get('reviewState','')
        reviewState = reviewState.split(',')
        if '' in reviewState:
            reviewState = ''
        tortinfo = request.GET.get('tortInfo','')
        Estatus = request.GET.get('Estatus','')
        dataSources = request.GET.get('dataSources','')
        productId = request.GET.get('productID','')
        mainSKU = request.GET.get('mainSKU','')
        orders7DaysStart = request.GET.get('orders7DaysStart','')
        orders7DaysEnd = request.GET.get('orders7DaysEnd','')
        refreshTimeStart = request.GET.get('refreshTimeStart','')
        refreshTimeEnd = request.GET.get('refreshTimeEnd', '')
        dateUploadedStart = request.GET.get('dateUploadedStart','')
        dateUploadedEnd = request.GET.get('dateUploadedEnd', '')
        lastUpdatedStart = request.GET.get('lastUpdatedStart', '')
        lastUpdatedEnd = request.GET.get('lastUpdatedEnd', '')
        Title = request.GET.get('Title','')
        Published = request.GET.get('Published','')

        #ExetStart = request.GET.get('ExetStart','')
        #ExetEnd = request.GET.get('ExetEnd','')
        #messages.error(request,'ExetStart&&&&&&&&**%s'%ExetStart)
        #messages.error(request,'ExetEnd&&&&&&&&**%s'%ExetEnd)
        #if ExetStart and ExetEnd:  
            #Pids = t_store_marketplan_execution_log.objects.filter(Exetime__gte=ExetStart,Exetime__lte=ExetEnd,Result=u'成功')
            #pid_list = []
            #for Pid in Pids:
                #pid_list.append(Pid.ProductID)
            #qs=qs.filter(ProductID__in=pid_list)
            #messages.error(request,'......$$$$$$$$$%s'%Pid)    
 
        searchList = {'ShopName__exact': shopname, 'Seller__exact': seller, 'ReviewState__in': reviewState,
                      'TortInfo__exact': tortinfo, 'Status__exact':Estatus, 'DataSources__exact': dataSources,
                      'ProductID__exact': productId, 'MainSKU__exact':mainSKU,
                      'Orders7Days__gte': orders7DaysStart, 'Orders7Days__lt': orders7DaysEnd,
                      'RefreshTime__gte': refreshTimeStart, 'RefreshTime__lt': refreshTimeEnd,
                      'DateUploaded__gte':dateUploadedStart,'DateUploaded__lt':dateUploadedEnd,
                      'LastUpdated__gte': lastUpdatedStart, 'LastUpdated__lt': lastUpdatedEnd,
                      'Title__icontains':Title,'Published__exact':Published,
                      }
        sl = {}
        for k,v in searchList.items():
            if isinstance(v,list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    if k == 'ShopName__exact':
                        v = 'Wish-' + v.zfill(4)
                        # messages.error(request, v)
                    sl[k] = v
        if sl is not None:
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
            except Exception,ex:
                messages.error(request,u'输入的查询数据有问题！')

        # 在线
        if status == 'online':
            qs = qs.filter(ReviewState='approved',Status='Enabled')
        # 不在线
        elif status == 'offline':
            qs = qs.filter(Q(ReviewState='approved',Status='Disabled')|Q(ReviewState='pending'))
        # 拒绝
        elif status == 'reject':
            qs = qs.filter(ReviewState='rejected')
        else:
            qs = qs

        return qs
        
        
        

