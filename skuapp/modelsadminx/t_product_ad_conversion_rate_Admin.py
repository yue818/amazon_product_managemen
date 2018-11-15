# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from skuapp.table.t_store_configuration_file import t_store_configuration_file
from urllib import urlencode
from skuapp.table.t_sys_param import t_sys_param
from django.contrib import messages
from skuapp.table.t_product_ad_conversion_rate import t_product_ad_conversion_rate

ConversationRate_CPC_Obj=t_sys_param.objects.filter(Type=43,Seq=1)
class t_product_ad_conversion_rate_Admin(object):
    search_box_flag = True

    def Showe_image(self,obj) :
        rt =  '<img src="%s"  width="120" height="120"  alt = "%s"  title="%s"  />  '%(obj.image,obj.image,obj.image)
        return mark_safe(rt)
    Showe_image.short_description = u'图片'

    def Showe_Keyword(self,obj) :
        rt = u'<a href = "/Project/admin/skuapp/t_report_get_sp_mega_report_/?%s">%s</a>'%(urlencode({'_p_ShopName__exact':obj.ShopName,'_p_CampaignName__exact':obj.CampaignName,'_p_AdGroupName__exact':obj.AdGroupName,'_p_Keyword__exact':obj.Keyword,'_p_AdvertisedSKU__exact':obj.AdvertisedSKU}),obj.Keyword)
        return mark_safe(rt)
    Showe_Keyword.short_description = u'关键字'
    
    def Showe_AdvertisedSKU_ShopName_CampaignName_AdGroupName(self,obj) :
        rt = u'刊登SKU:%s<br>卖家简称:%s'%(obj.AdvertisedSKU,obj.ShopName)
        t_store_configuration_file_objs = t_store_configuration_file.objects.filter(ShopName = obj.ShopName)
        if t_store_configuration_file_objs.exists():
            if t_store_configuration_file_objs[0].Seller == '' or t_store_configuration_file_objs[0].Seller is None:
                rt = '%s<br>店长/销售员:%s'%(rt,t_store_configuration_file_objs[0].Operators)
            elif t_store_configuration_file_objs[0].Seller != '' and t_store_configuration_file_objs[0].Seller is not None :
                rt = '%s<br>店长/销售员:%s'%(rt,t_store_configuration_file_objs[0].Seller)
        else :
            rt = '%s<br>店长/销售员: '%(rt)
        rt = '%s<br>广告系列名称:%s<br>广告组名称:%s'%(rt,obj.CampaignName,obj.AdGroupName)
        return mark_safe(rt)
    Showe_AdvertisedSKU_ShopName_CampaignName_AdGroupName.short_description = u'详细'
    
    def Showe_Z(self,obj) :
        rt = ''
        if (obj.ZOrder == 0 and obj.TotalHits >=20) or (obj.TotalHits >20 and obj.TotalConversionRate<=5):
            rt = u'<font color="red">总订单量(个):%s<br>总点击量(次):%s</font>'%(obj.ZOrder,obj.TotalHits)
        else:
            rt = u'总订单量(个):%s<br>总点击量(次):%s'%(obj.ZOrder,obj.TotalHits)
        rt = u'%s<br>总转化率(%s):%s%s<br>总曝光:%s<br>总花费:%s<br>总产出:%s'%(rt,'%',obj.TotalConversionRate,'%',obj.ZImpressions,obj.ZTotalSpend,obj.ZDayOrderedProductSales)
        if obj.ZACoS > 30:
            rt = u'%s<br><font color="red">总ACOS:%s%s</font>'%(rt,obj.ZACoS,'%')
        else:
            rt = u'%s<br>总ACOS:%s%s'%(rt,obj.ZACoS,'%')
        if obj.ZCPC:
            if obj.ZCPC > float(ConversationRate_CPC_Obj[0].V):
                rt = u'%s<br><font color="red">总CPC:%s</font>'%(rt,'%.2f' % obj.ZCPC)
            else:
                rt = u'%s<br>总CPC:%s'%(rt,'%.2f' % obj.ZCPC)
        else:
                rt = u'%s<br>总CPC:%s'%(rt,obj.ZCPC)
        return mark_safe(rt)
    Showe_Z.short_description = u'总体数据'

    def Showe_M(self,obj) :
        rt = u'月订单量(个):%s<br>月点击量(次):%s<br>月转化率(%s):%s%s<br>月曝光:%s<br>月花费:%s<br>月产出:%s'%(obj.MOrder,obj.MTotalHits,'%',obj.MonthlyConversionRate,'%',obj.MImpressions,obj.MTotalSpend,obj.MDayOrderedProductSales)
        if obj.MACoS:
            if obj.MACoS>30:
                rt = u'%s<br><font color="red">月ACOS:%s%s</font>'%(rt,'%.2f' % obj.MACoS,'%')
            else:
                rt = u'%s<br>月ACOS:%s%s'%(rt,'%.2f' % obj.MACoS,'%')
        else:
                rt = u'%s<br>月ACOS:%s%s'%(rt,obj.MACoS,'%')
        if obj.MCPC:        
            if obj.MCPC > float(ConversationRate_CPC_Obj[0].V):
                rt = u'%s<br><font color="red">月CPC:%s</font>'%(rt,'%.2f' % obj.MCPC)
            else:
                rt = u'%s<br>月CPC:%s'%(rt,'%.2f' % obj.MCPC)
        else:
                rt = u'%s<br>月CPC:%s'%(rt,obj.MCPC)
        return mark_safe(rt)
    Showe_M.short_description = u'月数据'

    def Showe_W(self,obj) :
        rt = u'周订单量(个):%s<br>周点击量(次):%s<br>周转化率(%s):%s%s<br>周曝光:%s<br>周花费:%s<br>周产出:%s'%(obj.WOrder,obj.WTotalHits,'%',obj.WeeklyConversionRate,'%',obj.WImpressions,obj.WTotalSpend,obj.WDayOrderedProductSales)
        if obj.WACoS:
            if obj.WACoS>30:
                rt = u'%s<br><font color="red">周ACOS:%s%s</font>'%(rt,'%.2f' % obj.WACoS,'%')
            else:
                rt = u'%s<br>周ACOS:%s%s'%(rt,'%.2f' % obj.WACoS,'%')
        else:
                rt = u'%s<br>周ACOS:%s%s'%(rt,obj.WACoS,'%')
        if obj.WCPC:
            if obj.WCPC > float(ConversationRate_CPC_Obj[0].V):
                rt = u'%s<br><font color="red">周CPC:%s</font>'%(rt,'%.2f' % obj.WCPC)
            else:
                rt = u'%s<br>周CPC:%s'%(rt,'%.2f' % obj.WCPC)
        else:
                rt = u'%s<br>周CPC:%s'%(rt,obj.WCPC)
        return mark_safe(rt)
    Showe_W.short_description = u'周数据'
    
    def show_Remarks(self,obj) :
        Remark_obj = obj.Remarks
        #messages.error(self.request,Remark_obj)
        rt=''
        if Remark_obj is not None:
            if len(Remark_obj)>30:
                for i in range(0,15):
                    rt = u'%s<br>%s'%(rt,Remark_obj[10*i:10*(i+1)])
            else:
                rt = u'%s'%(Remark_obj)
            return mark_safe(rt)
    show_Remarks.short_description = u'备注'
    
    list_display = ('id','Showe_image','Showe_AdvertisedSKU_ShopName_CampaignName_AdGroupName','Showe_Keyword','MatchType','show_Remarks','ASIN','Showe_Z','Showe_M','Showe_W','KeywordRemarks','ADStatusRemarks')
    list_editable = ('Remarks','KeywordRemarks','ADStatusRemarks')
    list_filter = ('ADStatusRemarks','KeywordRemarks','AdvertisedSKU','ShopName','Keyword','CampaignName','AdGroupName','WTotalHits','MTotalHits','TotalHits','WOrder','MOrder','ZOrder','WeeklyConversionRate','MonthlyConversionRate','TotalConversionRate','ZImpressions','ZTotalSpend','ZDayOrderedProductSales','ZACoS','MImpressions','MTotalSpend','MDayOrderedProductSales','MACoS','WImpressions','WTotalSpend','WDayOrderedProductSales','WACoS',)
#    search_fields = ('id','ADStatusRemarks','image','AdvertisedSKU','ShopName','Keyword','CampaignName','AdGroupName','ASIN','WTotalHits','MTotalHits','TotalHits','WOrder','MOrder','ZOrder','WeeklyConversionRate','MonthlyConversionRate','TotalConversionRate',)
    search_fields =None
    
    def get_list_queryset(self,):
        request = self.request
        return super(t_product_ad_conversion_rate_Admin, self).get_list_queryset().exclude(Keyword = '*')
        
    def save_models(self):
        t_product_ad_conversion_rate.objects.filter(ADStatusRemarks='zanting').update(KeywordRemarks='zanting')
        t_product_ad_conversion_rate.objects.filter(ADStatusRemarks='zaitou').update(KeywordRemarks='zaitou')
        t_product_ad_conversion_rate.objects.filter(ADStatusRemarks='guidang').update(KeywordRemarks='guidang')
        obj = self.new_obj
        obj.save()

    def get_list_queryset(self,):
        request = self.request
        qs = super(t_product_ad_conversion_rate_Admin, self).get_list_queryset()
        
        keywordRemarks = request.GET.get('keywordRemarks','')
        aDStatusRemarks          = request.GET.get('aDStatusRemarks','')
                
        advertisedSKU          = request.GET.get('advertisedSKU','')
        keyword       = request.GET.get('keyword','')
        ShopName      = request.GET.get('ShopName','')
        ShopName      = ShopName.decode('utf-8')
        adGroupName   = request.GET.get('adGroupName','')
        
        wOrderStart = request.GET.get('wOrderStart','')#周订单数
        wOrderEnd = request.GET.get('wOrderEnd','')
        
        mOrderStart = request.GET.get('mOrderStart','')#月订单数(个)
        mOrderEnd = request.GET.get('mOrderEnd','')
        
        weeklyConversionRateStart = request.GET.get('weeklyConversionRateStart','')#周转化率(%)
        weeklyConversionRateEnd = request.GET.get('weeklyConversionRateEnd','')
        
        monthlyConversionRateStart = request.GET.get('monthlyConversionRateStart','')#月转化率(%)
        monthlyConversionRateEnd = request.GET.get('monthlyConversionRateEnd','')
        
        wCPCStart = request.GET.get('wCPCStart','')#周CPC
        if wCPCStart:
            a = int(wCPCStart)
            b= a / 100.0
            wCPCStart = str(b)
        wCPCEnd = request.GET.get('wCPCEnd','')
        if wCPCEnd:
            a = int(wCPCEnd)
            b = a / 100.0
            wCPCEnd = str(b)
        
        mCPCStart = request.GET.get('mCPCStart','')#月CPC
        if mCPCStart:
            a= int(mCPCStart)
            b = a / 100.0
            mCPCStart = str(b)
        mCPCEnd = request.GET.get('mCPCEnd','')
        if mCPCEnd:
            a = int(mCPCEnd)
            b = a /100.0
            mCPCEnd =str(b)
        
        mTotalSpendStart = request.GET.get('mTotalSpendStart','')#月花费
        mTotalSpendEnd = request.GET.get('mTotalSpendEnd','')
        
        mDayOrderedProductSalesStart = request.GET.get('mDayOrderedProductSalesStart','')#月产出
        mDayOrderedProductSalesEnd = request.GET.get('mDayOrderedProductSalesEnd','')
        
        mACoSStart = request.GET.get('mACoSStart','')#月ACoS
        mACoSEnd = request.GET.get('mACoSEnd','')

        searchList = { 'KeywordRemarks__exact':keywordRemarks, 'ADStatusRemarks__exact':aDStatusRemarks,
        
                        'ShopName__contains':ShopName,'Keyword__exact':keyword,
                        'AdvertisedSKU__exact':advertisedSKU, 'AdGroupName__exact':adGroupName,
                        
                        'WOrder__gte':wOrderStart, 'WOrder__lt':wOrderEnd, 
                        'MOrder__gte':mOrderStart, 'MOrder__lt':mOrderEnd, 
                        'WeeklyConversionRate__gte':weeklyConversionRateStart, 'WeeklyConversionRate__lt':weeklyConversionRateEnd, 
                        'MonthlyConversionRate__gte':monthlyConversionRateStart, 'MonthlyConversionRate__lt':monthlyConversionRateEnd, 
                        'WCPC__gte':wCPCStart, 'WCPC__lt':wCPCEnd, 
                        'MCPC__gte':mCPCStart, 'MCPC__lt':mCPCEnd, 
                        'MTotalSpend__gte':mTotalSpendStart, 'MTotalSpend__lt':mTotalSpendEnd, 
                        'MDayOrderedProductSales__gte':mDayOrderedProductSalesStart, 'MDayOrderedProductSales__lt':mDayOrderedProductSalesEnd, 
                        'MACoS__gte':mACoSStart, 'MACoS__lt':mACoSEnd, 

                        }

        sl = {}
        for k,v in searchList.items():
            if isinstance(v,list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    #if k == 'ShopName__exact':
                        #v = 'AMZ-' + v.zfill(4)
                        #messages.error(request, v)
                    sl[k] = v
        if sl is not None:
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
            except Exception,ex:
                messages.error(request,u'输入的查询数据有问题！')
    
        return qs
