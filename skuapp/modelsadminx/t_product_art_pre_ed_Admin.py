# -*- coding: utf-8 -*-
from .t_product_Admin import *
from datetime import datetime



class t_product_art_pre_ed_Admin(t_product_Admin):
    search_box_flag = False
    
    actions = ['to_review_pre_ed', ]
    def to_review_pre_ed(self, request, queryset):
        for querysetid in queryset.all():
            obj = t_product_art_ed()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID= request.user.username
            obj.save()
            begin_t_product_oplog(request,querysetid.MainSKU,'SH',querysetid.Name2,querysetid.id)

            querysetid.delete()

    to_review_pre_ed.short_description = u'领去审核'

    def delete_models(self, queryset):
        from skuapp.table.Delete_Log_model import Delete_Log_Model
        from django.forms.models import model_to_dict
        import datetime
        insert_list=[]
        fmt_str_list=[]
        for obj in queryset:
            result=obj.delete()
            if result[0]==1:
                params=model_to_dict(obj)
                for k,v in params.items():
                    if isinstance(v, datetime.datetime):
                        v = v.strftime('%Y-%m-%d %H:%M:%S')
                    fmt_str=r'"{}":"{}"'.format(str(k),str(v))
                    fmt_str_list.append(fmt_str)
                delete_content='{'+','.join(fmt_str_list)+'}'
                sku=params.get('MainSKU')
                insert_row=Delete_Log_Model(actiontime=datetime.datetime.now(),username=self.user,sku=sku,where=self.model_name,delete_content=delete_content)
                insert_list.append(insert_row)
        try:
            Delete_Log_Model.objects.bulk_create(insert_list)
        except:
            pass




    def show_oplog(self,obj) :
        rt = ''
        t_product_oplog_objs = t_product_oplog.objects.filter(pid=obj.id,StepID='JZL',MainSKU=obj.MainSKU).order_by('id')
        for t_product_oplog_obj in t_product_oplog_objs:
            rt = u'%s%s:%s,'%(rt,t_product_oplog_obj.StepName,t_product_oplog_obj.OpName)
        return rt
    show_oplog.short_description = u'操作历史'






    def show_Remark(self,obj) :
        return mark_safe(u'【%s】<br>%s<br>%s<br>%s'%(obj.LWH,obj.Remark,obj.SupplierPUrl1,obj.SupplierPUrl2 ))
    show_Remark.short_description = u'备注'

    def show_wjp(self,obj) :
        rt = obj.ContrabandAttribute if obj.ContrabandAttribute <> '普货' else ''
        return rt
    show_wjp.short_description = u'违禁品'

    def show_name2(self,obj) :
        PrepackMark = obj.PrepackMark
        if PrepackMark is None:
            PrepackMark=''
        Name2 = obj.Name2
        if obj.ContrabandAttribute and obj.ContrabandAttribute != u'普货':
            if obj.SmallCategory != u'手表': #手表特殊
                wjp = u'-违禁品'
                return u'%s%s%s'%(Name2,wjp,PrepackMark)
        return u'%s%s'%(Name2,PrepackMark)
    show_name2.short_description = mark_safe(u'商品<br>名称<br>(中文)')


    list_per_page=10
    list_display= ('id','JZLTime','JZLStaffName','show_SourcePicPath','show_SourcePicPath2','MainSKU','Buyer','possessMan2','SpecialRemark','show_skulist','LargeCategory','SmallCategory','show_name2','Material','SupplierArtNO','Unit','MinPackNum','SupplierID','ReportName','ReportName2','show_oplog','show_wjp','show_Remark','auditnote')
    #list_display_links= ('SourcePicPath2',)#,'MainSKU','LargeCategory','SmallCategory','Name2','Material','SupplierArtNO','Unit','MinPackNum','SupplierID','Keywords2','Keywords',)
    readonly_fields = ('id',)
    list_editable = ('auditnote',)
    #search_fields=('id','MainSKU','Name2','StaffID',)

    def get_list_queryset(self,):
        request = self.request
        qs = super(t_product_art_pre_ed_Admin, self).get_list_queryset()

        # Electrification = request.GET.get('Electrification','')     # 是否带电
        # Powder          = request.GET.get('Powder','')              # 是否粉末
        # Liquid          = request.GET.get('Liquid','')              # 是否液体
        # Magnetism       = request.GET.get('Magnetism','')           # 是否带磁
        ContrabandAttribute = request.GET.get('ContrabandAttribute', '')
        Storehouse      = request.GET.get('Storehouse','')          # 发货仓库
        LargeCategory   = request.GET.get('LargeCategory','')       # 大类名称
        MainSKU = request.GET.get('MainSKU','')                     # 主SKU
        
        YNphoto = request.GET.get('YNphoto','') # 图片处理 0实拍 1制作 
        
        Buyer           = request.GET.get('Buyer','')           #采购员
        DYStaffName     = request.GET.get('DYStaffName','')     #调研员
        KFStaffName     = request.GET.get('KFStaffName','')     #开发员
        XJStaffName     = request.GET.get('XJStaffName','')     #询价员
        JZLStaffName    = request.GET.get('JZLStaffName','')    #建资料员
        PZStaffName     = request.GET.get('PZStaffName','')     #拍照员
        MGStaffName     = request.GET.get('MGStaffName','')     #美工员
        LRStaffName     = request.GET.get('LRStaffName','')     #录入员
        
        WeightStart = request.GET.get('WeightStart','')#克重
        WeightEnd = request.GET.get('WeightEnd','')
    
        updateTimeStart = request.GET.get('updateTimeStart','')#更新时间
        updateTimeEnd = request.GET.get('updateTimeEnd', '')

        searchList = { 'MainSKU__exact':MainSKU,'ContrabandAttribute__exact':ContrabandAttribute,
                        'Storehouse__exact':Storehouse, 'LargeCategory__exact':LargeCategory,
                        'YNphoto__exact': YNphoto,'YNphoto__exact':YNphoto,'Buyer__exact':Buyer, 'DYStaffName__exact':DYStaffName,
                        'KFStaffName__exact':KFStaffName, 'XJStaffName__exact':XJStaffName, 'JZLStaffName__exact':JZLStaffName,
                        'PZStaffName__exact':PZStaffName, 'MGStaffName__exact':MGStaffName, 'LRStaffName__exact':LRStaffName,
                        'Weight__gte':WeightStart, 'Weight__lt':WeightEnd, 
                        'UpdateTime__gte': updateTimeStart, 'UpdateTime__lt': updateTimeEnd,
                        }

        sl = {}
        for k,v in searchList.items():
            if isinstance(v,list):
                if v:
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