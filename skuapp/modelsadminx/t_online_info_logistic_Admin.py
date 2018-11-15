# -*- coding: utf-8 -*-
from .t_product_Admin import *
from django.utils.safestring import mark_safe
from skuapp.table.t_sys_param import *
from django.contrib import messages
from skuapp.table.t_config_logistic_express import t_config_logistic_express
import bs4
from bs4 import BeautifulSoup
import urllib2, urllib, httplib
from skuapp.table.t_config_logistic import t_config_logistic


class t_online_info_logistic_Admin(object):
    search_box_flag = True
    #show_yj = True
    
    def show_logisticInfo(self,obj):
        KeyInfo_list = t_config_logistic_express.objects.exclude(KeyInfo1='').values_list('KeyInfo1',flat=True).distinct()
        LogisticInfo = obj.LogisticInfo.replace('\t\n','</li><li>').replace('\t','<br>').replace('\n','<br>')
        for KeyInfo in KeyInfo_list:
            middle_var = '<font color = red>'+KeyInfo+'</font>'
            #messages.info(self.request,'<font color = red>'+KeyInfo+'</font>')
            LogisticInfo = LogisticInfo.replace(KeyInfo,middle_var)
        LogisticInfo = '<li>' + LogisticInfo + '</li>'
        return mark_safe(LogisticInfo)

    show_logisticInfo.short_description = u'物流信息'
    
    def update_logisticinfo(self, request, queryset):
        from skuapp.table.t_online_info_logistic import *
        for qs in queryset:
            LogisticName = qs.LogisticName
            trackno = qs.TrackNo
            cemskind = t_config_logistic.objects.get(LogisticName=LogisticName).ExpressID
            url = ('http://47.100.6.69/cgi-bin/GInfo.dll?MfcISAPICommand=EmmisTrackGenData&cemskind=%s&cno=%s' % (cemskind, trackno)).encode('GBK')
            req = urllib2.Request(url)
            try:
                xs = '<Root>' + urllib2.urlopen(req, timeout=200).read().decode('GBK') + '</Root>'
                soup = BeautifulSoup(xs, "xml")
                ErrorCode = soup.find('Root').text
                xml = soup.find('TRACK_DATA').text
                t_online_info_logistic.objects.filter(id=qs.id).update(LogisticInfo=xml,ErrorCode=ErrorCode,UpdateTime=datetime.datetime.now(),LogisticInfoFrom='快递公司')
                messages.info(request,'订单编号%s:物流信息已成功抓取！'%qs.OrderNum)
            except:
                cemskind = t_config_logistic.objects.get(LogisticName=LogisticName).ServiceID
                url = ('http://47.100.6.69/cgi-bin/GInfo.dll?MfcISAPICommand=EmmisTrackGenData&cemskind=%s&cno=%s' % (cemskind, trackno)).encode('GBK')
                req = urllib2.Request(url)
                xs = '<Root>' + urllib2.urlopen(req, timeout=200).read().decode('GBK') + '</Root>'
                soup = BeautifulSoup(xs, "xml")
                ErrorCode = soup.find('Root').text
                try:
                    xml = soup.find('TRACK_DATA').text
                    t_online_info_logistic.objects.filter(id=qs.id).update(LogisticInfo=xml,ErrorCode=ErrorCode,UpdateTime=datetime.datetime.now(),LogisticInfoFrom='承运商')
                    messages.info(request,'订单编号%s:已查询到该物流相关信息！'%qs.OrderNum)
                except:
                    t_online_info_logistic.objects.filter(id=qs.id).update(LogisticInfo='未查询到',ErrorCode=ErrorCode,UpdateTime=datetime.datetime.now(),LogisticInfoFrom='承运商')
                    messages.error(request,'订单编号%s:没有查询到该物流相关信息！'%qs.OrderNum)
    update_logisticinfo.short_description = u'手动更新物流信息'

    actions =  ['update_logisticinfo',]

        
    list_display= ('id','Country','ShopName','OrderNum','batchnum','TrackNo','LogisticName','ExpressName','OrderTime','TradeTime','ClosingDate','UpdateTime','show_logisticInfo',)
    #list_editable = ('TrackNo','LogisticName','ExpressName')
    list_filter = None#('id','Country','ShopName','TrackNo','batchnum','OrderNum','TradeTime','UpdateTime','LogisticName','ExpressName','OrderTime','ClosingDate','LogisticInfo','LogisticInfoFrom',)

    search_fields = None#('id','Country','ShopName','TrackNo','OrderNum','batchnum','TradeTime','UpdateTime','LogisticName','ExpressName','OrderTime','ClosingDate','LogisticInfo','LogisticInfoFrom',)

    readonly_fields = ()
    
    def get_list_queryset(self):
    
        request = self.request
        qs = super(t_online_info_logistic_Admin, self).get_list_queryset()

        id = request.GET.get('id', '')
        Country = request.GET.get('Country', '')
        ShopName = request.GET.get('ShopName', '')
        TrackNo = request.GET.get('TrackNo', '')
        TrackNo = re.split('[,，]', TrackNo.encode('utf-8'))
        OrderNum = request.GET.get('OrderNum', '')
        OrderNum = re.split('[,，]', OrderNum.encode('utf-8'))
        ExpressName = request.GET.get('ExpressName', '')
        batchnum = request.GET.get('batchnum', '')
        LogisticName = request.GET.get('LogisticName', '')
        LogisticInfo = request.GET.get('LogisticInfo', '')
        LogisticInfoFrom = request.GET.get('LogisticInfoFrom', '')

        TradeTimeStart = request.GET.get('TradeTimeStart', '')
        TradeTimeEnd = request.GET.get('TradeTimeEnd', '')
        
        UpdateTimeStart = request.GET.get('UpdateTimeStart', '')
        UpdateTimeEnd = request.GET.get('UpdateTimeEnd', '')
        
        OrderTimeStart = request.GET.get('OrderTimeStart', '')
        OrderTimeEnd = request.GET.get('OrderTimeEnd', '')
        
        ClosingDateStart = request.GET.get('ClosingDateStart', '')
        ClosingDateEnd = request.GET.get('ClosingDateEnd', '')
        



        searchList = {'id__exact': id, 'Country__exact': Country,
                      'ShopName__contains': ShopName,'TrackNo__in': TrackNo,
                      'OrderNum__in': OrderNum, 'ExpressName__exact': ExpressName,
                      'batchnum__exact': batchnum,'LogisticName__exact': LogisticName,
                      'LogisticInfo__exact': LogisticInfo, 'LogisticInfoFrom__exact': LogisticInfoFrom,

                      'TradeTime__gte': TradeTimeStart, 'TradeTime__lt': TradeTimeEnd,
                      'UpdateTime__gte': UpdateTimeStart, 'UpdateTime__lt': UpdateTimeEnd,
                      'OrderTime__gte': OrderTimeStart, 'OrderTime__lt': OrderTimeEnd,
                      'ClosingDate__gte': ClosingDateStart, 'ClosingDate__lt': ClosingDateEnd,
                      }
        sl = {}
        for k,v in searchList.items():
            if isinstance(v,list):
                v = [_.strip() for _ in v if _.strip()]
                if v :
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    #if k == 'ShopName__exact':
                        #v = 'Wish-' + v.zfill(4)
                        # messages.error(request, v)
                    sl[k] = v
        if sl is not None:
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
            except Exception,ex:
                messages.error(request,u'输入的查询数据有问题！')


        return qs





            
            
            
            
            
            
            
            