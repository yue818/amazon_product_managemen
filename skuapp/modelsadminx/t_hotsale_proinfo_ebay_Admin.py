# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from skuapp.table.t_hotsale_proinfo_ebay import *
from skuapp.table.t_config_apiurl_asin_kf import *
from urllib import urlencode
from django.contrib import messages
from datetime import datetime
from django.forms import TextInput, Textarea

class t_hotsale_proinfo_ebay_Admin(object):
    search_cata_navigator = True
    cata_of_platform = 'ebay'
    department_desc = 'others'
    list_per_page=100
    def show_Image(self,obj) :
        url =u'%s'%(obj.Image)
        #<style type="text/css">img:hover{height:400px; width:400px;}</style>
        rt =  '<img src="%s" width="150" height="150"  alt = "%s"  title="%s"></img>'%(url,url,url)
        return mark_safe(rt)
    show_Image.short_description = u'图片'

    def title_url(self,obj) :
        rt = ''
        rt = u'<a href="%s"target="_blank">%s</a>'%(obj.URL,obj.Title)
        return mark_safe(rt)
    title_url.short_description = u'产品名称'
    
    def cata1_list(self,obj) :
        rt = ''
        if obj.cata1 is not None and obj.cata1 != '':
            rt = u'<a href="?%s"target="_blank">%s</a>'%(urlencode({'_p_cata1':obj.cata1}),obj.cata1)
        return mark_safe(rt)
    cata1_list.short_description = u'一级类目'
    
    def cata2_list(self,obj) :
        rt = ''
        if obj.cata2 is not None and obj.cata2 != '':
            rt = u'<a href="?%s"target="_blank">%s</a>'%(urlencode({'_p_cata1':obj.cata1, '_p_cata2':obj.cata2}),obj.cata2)
        return mark_safe(rt)
    cata2_list.short_description = u'二级类目'
    
    def cata3_list(self,obj) :
        rt = ''
        if obj.cata3 is not None and obj.cata3 != '':
            rt = u'<a href="?%s"target="_blank">%s</a>'%(urlencode({'_p_cata1':obj.cata1, '_p_cata2':obj.cata2, '_p_cata3':obj.cata3}),obj.cata3)
        return mark_safe(rt)
    cata3_list.short_description = u'三级类目'
    
    def cata4_list(self,obj) :
        rt = ''
        if obj.cata4 is not None and obj.cata4 != '':
            rt = u'<a href="?%s"target="_blank">%s</a>'%(urlencode({'_p_cata1':obj.cata1, '_p_cata2':obj.cata2, '_p_cata3':obj.cata3, '_p_cata4':obj.cata4}),obj.cata4)
        return mark_safe(rt)
    cata4_list.short_description = u'四级类目'
    
    def cata5_list(self,obj) :
        rt = ''
        if obj.cata5 is not None and obj.cata5 != '':
            rt = u'<a href="?%s"target="_blank">%s</a>'%(urlencode({'_p_cata1':obj.cata1, '_p_cata2':obj.cata2, '_p_cata3':obj.cata3, '_p_cata4':obj.cata4, '_p_cata5':obj.cata5}),obj.cata5)
        return mark_safe(rt)
    cata5_list.short_description = u'五级类目'
        
    list_display=('title_url','show_Image','Price','sold','shipping','region','CreateTime', 'lastRefreshTime', 'cata1_list', 'cata2_list', 'cata3_list', 'cata4_list', 'cata5_list','used','remark','tagTime','tagUser')
    list_editable  = ('remark','isDiscard','isStop')
    search_fields   =('CatagoryID','ProductID','URL','Title','cata1','cata2','cata3','cata4','cata5','location','tagUser')
    list_filter   =('CreateTime', 'lastRefreshTime','used','tagTime','tagUser','region', 'sold','CatagoryID','cata1','cata2','cata3','cata4','cata5', 'isStop')
    readonly_fields =('ProductID','Image','URL', 'SrcImage','Title','Price','CreateTime', 'lastRefreshTime','shipping','cata1','cata2','cata3','cata4','cata5','CatagoryID','location','region','ifDone','used','isDiscard','isStop','tagTime','tagUser','dRating','wRating')
    
    def get_list_queryset(self):
        request = self.request
        if request.user.is_authenticated():
            qs = super(t_hotsale_proinfo_ebay_Admin, self).get_list_queryset()
            if request.user.is_superuser:
                return qs.filter(department = 'Others')
            return qs.filter(isStop = 'N', department = 'Others').exclude(used='D')
        else:
            return render(request,'')

    actions =  ['to_KF','to_FX','DISCARD']
    
    def to_KF(self, request, queryset):
        nUsed = 0
        nFailed = 0
        for obj in queryset.all():
            if obj.used == 'U':
                nFailed = nFailed + 1
            elif obj.used == 'N' or obj.tagUser == request.user.first_name or request.user.is_superuser:
                obj.used = 'U'
                obj.tagUser = request.user.first_name
                obj.tagTime = datetime.now()
                strRemark = obj.tagUser+':'+obj.tagTime.strftime('%Y-%m-%d %H:%M:%S')+'>'+u'领用开发'
                if obj.remark is None or obj.remark == '':
                    obj.remark = strRemark
                else:
                    obj.remark = obj.remark + '\n' + strRemark
                obj.save()
                nUsed = nUsed + 1
            else:
                nFailed = nFailed + 1
        if nUsed > 0 and nFailed == 0:
            messages.info(request, str(u'您已成功领用%d个产品, 请开始开发')%(nUsed))
        elif nUsed == 0:
            messages.error(request, u'您所选取的产品已被领用开发或其他人已处理, 请勿重复处理')
        else:
            messages.warning(request, str(u'您已领用了%d个产品, 另外%d个产品因重复领用或已被其他人处理无法成功')%(nUsed,nFailed))
    to_KF.short_description = u'开始开发'

    def to_FX(self, request, queryset):
        nUsed = 0
        nFailed = 0
        for obj in queryset.all():
            if obj.used == 'Y':
                nFailed = nFailed + 1
            elif obj.used == 'N' or obj.tagUser == request.user.first_name or request.user.is_superuser:
                obj.used = 'Y'
                obj.tagUser = request.user.first_name
                obj.tagTime = datetime.now()
                strRemark = obj.tagUser+':'+obj.tagTime.strftime('%Y-%m-%d %H:%M:%S')+'>'+u'开始分析'
                if obj.remark is None or obj.remark == '':
                    obj.remark = strRemark
                else:
                    obj.remark = obj.remark + '\n' + strRemark
                obj.save()
                nUsed = nUsed + 1
            else:
                nFailed = nFailed + 1
        if nUsed > 0 and nFailed == 0:
            messages.info(request, str(u'您已成功标记%d个产品开始分析')%(nUsed))
        elif nUsed == 0:
            messages.error(request, u'您所选取的产品已被标记, 请勿重复标记')
        else:
            messages.warning(request, str(u'您已标记了%d个产品, 另外%d个产品因重复标记无法成功')%(nUsed,nFailed))        
        
    to_FX.short_description = u'开始分析'
    
    def DISCARD(self, request, queryset):
        nUsed = 0
        nFailed = 0
        for obj in queryset.all():
            if obj.used == 'N' or obj.tagUser == request.user.first_name or request.user.is_superuser:
                obj.used = 'D'
                obj.tagUser = request.user.first_name
                obj.tagTime = datetime.now()
                strRemark = obj.tagUser+':'+obj.tagTime.strftime('%Y-%m-%d %H:%M:%S')+'>'+u'弃用'
                if obj.remark is None or obj.remark == '':
                    obj.remark = strRemark
                else:
                    obj.remark = obj.remark + '\n' + strRemark
                obj.save()
                nUsed = nUsed + 1
            else:
                nFailed = nFailed + 1
            
        if nUsed > 0 and nFailed == 0:
            messages.info(request, str(u'您已成功弃用%d个产品')%(nUsed))
        elif nUsed == 0:
            messages.error(request, u'您所选取的产品已被其他人标记, 请联系对应处理人处理')
        else:
            messages.warning(request, str(u'您已弃用了%d个产品, 另外%d个产品因被其他人标记无法成功')%(nUsed,nFailed))
    DISCARD.short_description = u'弃用'
    
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':5, 'cols':50})},
        }
