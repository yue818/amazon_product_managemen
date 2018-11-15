# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from django.contrib import messages
from skuapp.table.t_config_apiurl_asin import *
from skuapp.table.t_config_apiurl_asin_kf import *
from skuapp.table.t_product_survey_ing import *
from skuapp.table.t_product_develop_ing import *
from urllib import urlencode
from datetime import datetime
import datetime as datime
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.contrib import messages
from skuapp.table.t_config_apiurl_asin_operation import t_config_apiurl_asin_operation
from django.db.models import F

class t_config_apiurl_asin_xprx_Admin(object):
    search_box_flag = True
    list_per_page=50
    
    def get_id(self):
        t_product_survey_ing_obj = t_product_survey_ing()
        t_product_survey_ing_obj.save()
        temp_id=t_product_survey_ing_obj.id
        t_product_survey_ing_obj.delete()
        return temp_id
        
    def show_SmallImage(self,obj) :
        url =u'%s'%(obj.SmallImage)
        rt =  '<img src="%s"  width="150" height="150"  alt = "%s"  title="%s"  />  '%(url,url,url)
        return mark_safe(rt)
    show_SmallImage.short_description = u'图片'

    def show_asin_urls(self,obj) :
        rt = ''
        asin_objs = t_config_apiurl_asin.objects.filter(id=obj.id)
        for asin_obj in asin_objs:
            rt_url = u'https://www.amazon.com/dp/%s'%asin_obj.ASIN
            rt = u'%s<a href="%s"target="_blank">%s</a>'%(rt,rt_url,asin_obj.ASIN)
        return mark_safe(rt)
    show_asin_urls.short_description = u'ASIN'


    def show_ranklist(self,obj) :

        t_config_apiurl_asin_objs = t_config_apiurl_asin.objects.filter(ASIN = obj.ASIN)
        if t_config_apiurl_asin_objs[0].Rank is not None and t_config_apiurl_asin_objs[0].Rank.strip() !='':
            rt_tr = '<table  style="text-align:center;" border="1" cellpadding="3" cellspacing="1" bgcolor="#c1c1c1"><tr bgcolor="#C00"><th style="text-align:center">类目</th>'
            tt = ''
            rank = ''
            Rank_objs = t_config_apiurl_asin_objs[0].Rank
            Rank_dict = eval(Rank_objs)
            a = 0
            for Rank_k,Rank_v in Rank_dict.iteritems():
                rt_tr_k_obj = '<td>%s</td>'%Rank_k
                t = 0
                Rank_v_obj = ''
                for Rank in Rank_v:
                    t = t + 1
                    Rank_v_obj = '%s<td>%s</td>'%(Rank_v_obj,Rank)
                rank = '<tr bgcolor="#FFFFFF">%s%s</tr>%s'%(rt_tr_k_obj,Rank_v_obj,rank)
                a = t
            i = 0
            while i < a:
                i = i + 1
                tt = '%s<th style="text-align:center">->Rank%d</th>'%(tt,i)
            title = '%s%s</tr>'%(rt_tr,tt)
            ii = '%s%s</table>'%(title,rank)
        else:
            ii = ''
        return mark_safe(ii)
    show_ranklist.short_description = mark_safe('<p align="center"> Rank信息</p>')
    
    def show_rank(self,obj):
        rt =  u"<a id=show_rank_%s>查看</a><script>$('#show_rank_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'历史排名',fix:false,shadeClose: true,maxmin:true,area:['1000px','600px'],content:'/t_config_apiurl_asin/show_rank/?ASIN=%s',});});</script>"%(obj.id,obj.id,obj.ASIN)
        return mark_safe(rt)
    show_rank.short_description=u'历史排名'
        
        
    def show_group1_urls(self,obj) :
        rt_url = u'<a href="/Project/admin/skuapp/t_config_apiurl_asin/?%s">%s</a>'%(urlencode({'_p_group1__exact':obj.group1}),obj.group1)
        return mark_safe(rt_url)
    show_group1_urls.short_description = u'一级分类'
    
    def show_group2_urls(self,obj) :
        rt_url = u'<a href="/Project/admin/skuapp/t_config_apiurl_asin/?%s">%s</a>'%(urlencode({'_p_group1__exact':obj.group1,'_p_group2__exact':obj.group2}),obj.group2)
        return mark_safe(rt_url)
    show_group2_urls.short_description = u'二级分类'
    
    def show_Remarks(self,obj) :
        rt =''
        rt = u'<table border="1"><tr>'\
            u'<tr><td>备注:</td><td><a>%s</a></td></tr>'\
            %(obj.Remarks)
       
        rt +=  u'<tr><td>处理人:</td> <td><a>%s</a></td></tr>'%(obj.DealName)
        
        rt +=  u'<tr><td>处理时间:</td> <td><a>%s</a></td></tr>'%(obj.DealTime)
        rt += u'</table>'   
        return mark_safe(rt)
    show_Remarks.short_description = u'备注'
    
    def show_add_Remarks(request,obj) :
        rt =''
        if obj.DealName == None and obj.DealTime == None or obj.DealName == request.user.first_name:
            rt =  u"<a id=show_Remarks_%s>添加</a><script>$('#show_Remarks_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'添加备注',fix:false,shadeClose: true,maxmin:true,area:['600px','500px'],content:'/t_config_apiurl_asin_xprx/Remarks/?id=%s ',btn:['关闭页面'],end:function(){location.reload();}});});</script>"%(obj.id,obj.id,obj.id)
        else :
            rt +=  u'已有备注'
        return mark_safe(rt)
    show_add_Remarks.short_description = u'添加备注'

    list_display   =('id','show_SmallImage','Remarks','show_add_Remarks','DealName','DealTime','dealStatus','Collar','show_asin_urls','Rank','show_rank','Status','Title','Serial','ListPrice','UplsitTime','RefreshTime','Added_Time','show_group1_urls','show_group2_urls','group3','group4','group5')
    list_editable  = None
    search_fields   =('id','ASIN','URL','Status','Collar','DealName','Title','Brand','Feature','ListPrice','SmallImage','ProductGroup','Error','Serial','Rank','group1','group2','group3','group4','group5')
    list_filter   =('URL','Status','UplsitTime','RefreshTime','Title','Brand','Collar','YNEnabled','DealName','DealTime','Feature','ProductGroup','Error','Serial','Rank','group1','group2','group3','group4','group5')
    readonly_fields =('id','SmallImage','ProductGroup','ASIN','URL','Status','Collar','Title','Brand','ListPrice','UplsitTime','RefreshTime','Feature','Error','Serial','Rank','group1','group2','group3','group4','group5')

    actions =  ['to_t_product_develop_ing','to_t_config_apiurl_asin_cf',]
    
    
    def to_t_product_develop_ing(self, request, queryset):
        
        for querysetid in queryset.all():
            #到 t_product_develop_ing 正在开发
            t_product_develop_ing_objs = t_product_develop_ing()
            #obj = t_product_build_ing()
            #obj.__dict__ = querysetid.__dict__
            t_product_develop_ing_objs.id = self.get_id()
            t_product_develop_ing_objs.MainSKU = ''
            t_product_develop_ing_objs.CreateTime = datetime.now()
            t_product_develop_ing_objs.CreateStaffName = request.user.first_name
            t_product_develop_ing_objs.StaffID= request.user.username
            t_product_develop_ing_objs.SourcePicPath =querysetid.SmallImage
            
            if querysetid.URL.find('amazon.') != -1:
                t_product_develop_ing_objs.SourceURL = u'https://www.amazon.com/dp/%s'%querysetid.ASIN
            if querysetid.URL.find('ebay.') != -1:
                t_product_develop_ing_objs.SourceURL = u'http://www.ebay.com/itm/%s'%querysetid.ASIN
            
            t_product_develop_ing_objs.Name =querysetid.Title
            t_product_develop_ing_objs.Pricerange=querysetid.ListPrice
            t_product_develop_ing_objs.SpecialRemark = 'ASIN=%s'%(querysetid.ASIN)
            t_product_develop_ing_objs.DYStaffName=request.user.first_name
            t_product_develop_ing_objs.DYTime=datetime.now()
            t_product_develop_ing_objs.save()
            
            if querysetid.DevelopName is None:
                b = t_config_apiurl_asin_operation.objects.filter(OperationMan=request.user.first_name,OperationWeek=datetime.now().strftime('%Y%W'))
                if b.exists() :
                    t_config_apiurl_asin_operation.objects.filter(OperationMan=request.user.first_name,OperationWeek=datetime.now().strftime('%Y%W')).update(Developed=F('Developed')+1)                
                else :
                    t_config_apiurl_asin_operation.objects.filter().create(Developed=1,Repeation=0,Handled=0,OperationMan=request.user.first_name,OperationWeek=datetime.now().strftime('%Y%W'))
            
            querysetid.Collar= 'developing'
            querysetid.DevelopName = request.user.first_name
            querysetid.DevelopTime =datetime.now()
            querysetid.save()


    to_t_product_develop_ing.short_description = u'转到-正在开发'
    
    
    def to_t_config_apiurl_asin_cf(self, request, queryset):
        for querysetid in queryset.all():
            if querysetid.dealStatus == 'alreadyprocessed' and (querysetid.DevelopName is None or querysetid.DevelopName != request.user.first_name):
                querysetid.Collar = 'duplication' # 重复产品
                querysetid.DevelopName = request.user.first_name
                querysetid.DevelopTime=datetime.now()
                querysetid.save()
                
                b = t_config_apiurl_asin_operation.objects.filter(OperationMan=request.user.first_name,OperationWeek=datetime.now().strftime('%Y%W'))
                if b.exists() :
                    t_config_apiurl_asin_operation.objects.filter(OperationMan=request.user.first_name,OperationWeek=datetime.now().strftime('%Y%W')).update(Repeation=F('Repeation')+1)                
                else :
                    t_config_apiurl_asin_operation.objects.filter().create(Developed=0,Repeation=1,Handled=0,OperationMan=request.user.first_name,OperationWeek=datetime.now().strftime('%Y%W'))
                    
            elif querysetid.dealStatus == 'alreadyprocessed' and (querysetid.DevelopName is None or querysetid.DevelopName == request.user.first_name):
                querysetid.Collar = 'duplication' # 重复产品
                querysetid.DevelopName = request.user.first_name
                querysetid.DevelopTime=datetime.now()
                querysetid.save()
                
                b = t_config_apiurl_asin_operation.objects.filter(OperationMan=request.user.first_name,OperationWeek=datetime.now().strftime('%Y%W'))
                if b.exists() :
                    t_config_apiurl_asin_operation.objects.filter(OperationMan=request.user.first_name,OperationWeek=datetime.now().strftime('%Y%W')).update(Repeation=F('Repeation')+1)                
                else :
                    t_config_apiurl_asin_operation.objects.filter().create(Developed=0,Repeation=1,Handled=0,OperationMan=request.user.first_name,OperationWeek=datetime.now().strftime('%Y%W'))
                
            elif querysetid.dealStatus != 'alreadyprocessed' :
                messages.error(request, '对不起！未处理状态的产品，无法确认重复。 ID：%s'%querysetid.id)
            elif querysetid.DevelopName is not None :
                messages.error(request, '对不起！只有开发领用人员为空，才能操作。 ID：%s'%querysetid.id)
    to_t_config_apiurl_asin_cf.short_description = u'重复产品'
    
    def to_start(self, request, queryset):
        for querysetid in queryset.all():
            if querysetid.Collar in ['2','suspend'] and (querysetid.DealName is None or querysetid.DealName == request.user.first_name):
                querysetid.Collar = 'start' # 开始开发
                querysetid.DealName = request.user.first_name
                querysetid.DealTime=datetime.now()
                querysetid.save()
                
            elif querysetid.Collar not in ['2','suspend']:
                messages.error(request, '对不起！非待开发状态的产品，无法领用开发。 ID：%s'%querysetid.id)
            elif querysetid.DealName is not None and  querysetid.DealName != request.user.first_name:
                messages.error(request, '对不起！只有开发领用人员为空或为本人，才能开始开发。 ID：%s'%querysetid.id)
    to_start.short_description = u'开始开发'
    
    def to_suspend(self, request, queryset):
        for querysetid in queryset.all():
            if querysetid.Collar == 'start' and querysetid.Remarks is not None and querysetid.Remarks.strip() != '' and querysetid.DealName == request.user.first_name :
                querysetid.Collar = 'suspend' # 暂停开发
                querysetid.DealTime=datetime.now()
                querysetid.save()
                
            elif querysetid.Collar != 'start':
                messages.error(request, '对不起！只有已经开始开发的产品，才可以暂停开发。 ID：%s'%querysetid.id)
            elif querysetid.Remarks is None or querysetid.Remarks.strip() == '':
                messages.error(request, '对不起！请填写暂停开发的原因。 ID：%s'%querysetid.id)
            elif querysetid.DealName != request.user.first_name:
                messages.error(request, '对不起！只有开发领用人员，才能暂停开发。 ID：%s'%querysetid.id)
    to_suspend.short_description = u'暂停开发'
    
    def to_complete(self, request, queryset):
        for querysetid in queryset.all():
            if querysetid.Collar == 'start' and querysetid.Remarks is not None and querysetid.Remarks.strip() != '' and querysetid.DealName == request.user.first_name :
                querysetid.Collar = 'complete'
                querysetid.DealTime=datetime.now()
                querysetid.save()
                
            elif querysetid.Collar != 'start':
                messages.error(request, '对不起！只有已经开始开发的产品，才可以完成开发。 ID：%s'%querysetid.id)
            elif querysetid.Remarks is None or querysetid.Remarks.strip() == '':
                messages.error(request, '对不起！请填写完成开发的落地SKU。 ID：%s'%querysetid.id)
            elif querysetid.DealName != request.user.first_name:
                messages.error(request, '对不起！只有开发领用人员，才能执行完成开发动作。 ID：%s'%querysetid.id)
    to_complete.short_description = u'完成开发'
    
    def to_abandaned(self, request, queryset):
        for querysetid in queryset.all():
            if querysetid.Remarks is not None and querysetid.Remarks.strip() != '':
                querysetid.Collar = 'adandaned'
                querysetid.DealName = request.user.first_name
                querysetid.DealTime = datetime.now()
                querysetid.save()
            elif querysetid.Remarks is None or querysetid.Remarks.strip() == '':
                messages.error(request, '对不起！请填写弃用的原因。 ID：%s'%querysetid.id)
    to_abandaned.short_description = u'弃用'
    
    def get_list_queryset(self,):
        request = self.request
        qs =  super(t_config_apiurl_asin_xprx_Admin, self).get_list_queryset().filter(category = u'nocloth',Rank__lte=20000).exclude(Added_Time__lt=(datime.datetime.now()+datime.timedelta(days=-180)).strftime('%Y-%m-%d'))

        DealName    = request.GET.get('DealName','')
        dealStatus      = request.GET.get('dealStatus','')
        group1      = request.GET.get('group1','')
        group1=group1.decode('utf-8')
        group2      = request.GET.get('group2','')
        group2=group2.decode('utf-8')
        
        DealTimeStart = request.GET.get('DealTimeStart','')#处理时间
        DealTimeEnd = request.GET.get('DealTimeEnd','')
        

        

        searchList = {'DealName__exact':DealName, 'group1__exact':group1,
                      'dealStatus__exact':dealStatus,'group2__exact':group2,
                      'DealTime__gte':DealTimeStart, 'DealTime__lt':DealTimeEnd, 
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
        
        return qs.filter(Q(Collar = '2'))    