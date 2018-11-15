# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from django.contrib import messages
from skuapp.table.t_config_apiurl_asin import *
from skuapp.table.t_config_apiurl_asin_kf import *
from urllib import urlencode
from datetime import datetime

class t_config_apiurl_asinAdmin(object):
    list_per_page=50
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

    list_display   =('id','show_SmallImage','Collar','Remarks','show_asin_urls','Rank','show_rank','Status','Title','Serial','ListPrice','UplsitTime','RefreshTime','Added_Time','show_group1_urls','show_group2_urls','group3','group4','group5')
    list_editable  = ('Remarks',)
    search_fields   =('id','ASIN','URL','Status','Collar','DealName','Title','Brand','Feature','ListPrice','SmallImage','ProductGroup','Error','Serial','Rank','group1','group2','group3','group4','group5')
    list_filter   =('URL','Status','UplsitTime','RefreshTime','Title','Brand','Collar','YNEnabled','DealName','DealTime','Feature','ProductGroup','Error','Serial','Rank','group1','group2','group3','group4','group5')
    readonly_fields =('id','SmallImage','ProductGroup','ASIN','URL','Status','Collar','Title','Brand','ListPrice','UplsitTime','RefreshTime','Feature','Error','Serial','Rank','group1','group2','group3','group4','group5')
    list_display_links = ('id',)

    actions =  ['to_start','to_suspend','to_complete','to_abandaned',]
    
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



        return super(t_config_apiurl_asinAdmin, self).get_list_queryset().filter(category = u'nocloth')

    
    