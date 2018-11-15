# -*- coding: utf-8 -*-
from .t_product_Admin import *
from datetime import datetime as datime
from skuapp.table.t_product_mainsku_sku import t_product_mainsku_sku
from skuapp.table.t_shopsku_information_binding import t_shopsku_information_binding

class t_product_depart_get_user_Admin(t_product_Admin):
    enter_ed = True
    depart_get_user_flag = True
    search_box_flag = True
    def show_urls(self,obj) :
        rt = u'<table border="1"><tr>'\
            u'<td style="width:80px">反向:</td><td style="width:250px;"><a target="_blank"  href="%s">%s</a></td></tr>'\
            u'<tr><td>供货商:</td><td><a target="_blank"  href="%s">%s</a></td></tr>'\
            %(obj.SourceURL,obj.SourceURL[0:30],obj.SupplierPUrl1,obj.SupplierPUrl1[0:30])
        sites = t_sys_param.objects.filter(Type=302).order_by('Seq')
        newSites = {}
        for site in sites:
            newSites[site.V] = ''
        if obj.URLwish is not None and obj.URLwish.strip() != '':
            try:
                URLS = eval(obj.URLwish)
                for k,v in URLS.items():
                   newSites[k] = v
                for k,v in newSites.items():
                    rt +=  u'<tr><td>%s:</td> <td><a target="_blank"  href="%s">%s</a></td></tr>'%(k,v,v[0:30])
            except Exception,ex:
                messages.error(self.request,u'%s:%s'%(Exception,ex))
        else:
            for k,v in newSites.items():
                rt +=  u'<tr><td>%s:</td> <td><a target="_blank"  href="%s">%s</a></td></tr>'%(k,v,v[0:30])
        rt += u'</table>'
        return mark_safe(rt)
    show_urls.short_description = u'链接信息'

    def endtime_PZ_MG(self,obj):
        rt = ''
        if obj.MGProcess == '0' or obj.MGProcess == '1':
            pass
        elif obj.MGProcess == '2' or obj.MGProcess == '3':
            if obj.YNphoto == '0':
                photo_objs = t_product_photograph.objects.filter(pid=obj.pid).order_by('MainSKU')
                if photo_objs.exists():
                    rt = u'%s%s'%(rt,photo_objs[0].PZTime)
            elif obj.YNphoto == '1':
                MG_objs = t_product_art_ing.objects.filter(id=obj.pid).order_by('MainSKU')
                if MG_objs.exists():
                    rt = u'%s%s'%(rt,MG_objs[0].MGTime)
        return rt
    endtime_PZ_MG.short_description = u'图片完成时间'
    
    def show_Secondary_research(self,obj) :
        rt =  u"<a id=show_Secondary_research_%s>添加</a><script>$('#show_Secondary_research_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'添加二次调研',fix:false,shadeClose: true,maxmin:true,area:['600px','500px'],content:'/t_product_depart_get/Secondary_research/?id=%s ',btn:['关闭页面'],end:function(){location.reload();}});});</script>"%(obj.id,obj.id,obj.id)
        return mark_safe(rt)
    show_Secondary_research.short_description = u'添加二次调研'
    
    #actions = ['do_delete','do_Abandoned',]
    
    def do_delete(self, request, queryset):
    
        for querysetid in queryset.all():
        #本部门领用过
            objs = t_product_enter_ed.objects.filter(id = querysetid.pid)
            if objs.exists():
                if querysetid.DepartmentID == '1':
                    objs.update(onebuOperation = '0')
                elif querysetid.DepartmentID == '2':
                    objs.update(twobuOperation = '0')
                elif querysetid.DepartmentID == '3':
                    objs.update(threebuOperation = '0')
                elif querysetid.DepartmentID == '4':
                    objs.update(fourbuOperation = '0')
                elif querysetid.DepartmentID == '5':
                    objs.update(fivebuOperation = '0')
                elif querysetid.DepartmentID == '6':
                    objs.update(sixbuOperation = '0')
                elif querysetid.DepartmentID == '7':
                    objs.update(sevenbuOperation = '0')
                elif querysetid.DepartmentID == '8':
                    objs.update(eightbuOperation = '0')
                elif querysetid.DepartmentID == '9':
                    objs.update(ninebuOperation = '0')
                elif querysetid.DepartmentID == '10':
                    objs.update(tenbuOperation = '0')
                elif querysetid.DepartmentID == '11':
                    objs.update(elevenbuOperation = '0')
                elif querysetid.DepartmentID == '12':
                    objs.update(twelvebuOperation = '0')
                elif querysetid.DepartmentID == '13':
                    objs.update(thirteenbuOperation = '0')
    
        queryset.delete()
    do_delete.short_description = u'转回待领用'
    
    def do_Abandoned(self, request, objs):
        for obj in objs:
            if obj.StaffName == request.user.first_name :
                obj.StaffName = u'%s-%s'%(request.user.first_name,u'弃用')
                obj.save()
            else :
                messages.error(request,u'抱歉！只有领用人才可以弃用。。。Pid: %s.'%obj.pid)
    do_Abandoned.short_description = u'点击弃用'
    
    def to_Published(self, request, objs):
        for obj in objs:
            time = '%s'%datime.now()
            if obj.PublishedA is not None and obj.PublishedA.strip() != '':
                if obj.PublishedInfo is not None and obj.PublishedInfo.strip() != '':
                    PublishedInfo_old = u'%s;%s-%s,%s'%(obj.PublishedInfo,obj.PublishedA.replace(',','，').replace('-','——'),self.request.user.first_name,time[0:19])
                else:
                    PublishedInfo_old = u'%s-%s,%s'%(obj.PublishedA.replace(',','，').replace('-','——'),self.request.user.first_name,time[0:19])
                objs.filter(id = obj.id).update(PublishedInfo=PublishedInfo_old,PublishedA = '')
            else:
                messages.error(request,u'请填写待刊登账号。。。')

    to_Published.short_description = u'刊登登记'
    
    def show_PublishedInfo(self,obj):
        rt = ''
        if obj.PublishedInfo is not None and obj.PublishedInfo.strip() != '':
            for Published in obj.PublishedInfo.split(';'):
                Pub = Published.split(',')
                Pub_T = Pub[0].split('-')
                Pub_l = ''
                Pub_T_l = ''
                if len(Pub)>=2:
                    Pub_l = Pub[1]
                if len(Pub_T)>=2:
                    Pub_T_l = Pub_T[1]
                rt = u"%s<a href='%s' target='_blank'>%s</a><br>%s-%s<br>"%(rt,Pub_T[0],Pub_T[0],Pub_T_l,Pub_l)

        return mark_safe(rt)
    show_PublishedInfo.short_description = u'-----------刊登信息-----------'

    def show_Pub_Info(self,obj):
        from pyapp.models import b_goodsskulinkshop
        rt = '<div title="未刊登" style="float:left;width: 60px;height: 20px;background-color: red;text-align: center;line-height: 20px;border-radius: 4px">未刊登</div>'
        skulist = t_product_mainsku_sku.objects.filter(MainSKU=obj.MainSKU).values_list('ProductSKU',flat=True)
        for sku in skulist:
            jubobjs = b_goodsskulinkshop.objects.filter(SKU=sku,PersonCode=obj.StaffName)
            if jubobjs.exists():
                rt = '<div title="已刊登" style="float:left;width: 60px;height: 20px;background-color: #66FF66;text-align: center;line-height: 20px;border-radius: 4px">已刊登</div>'
                break
        return mark_safe(rt)
    show_Pub_Info.short_description = u'刊登状态'

    def show_SalesAttr(self,obj):
        rt = ''
        if obj.SalesAttr :
            rt = '%s'%obj.SalesAttr
        if self.request.user.is_superuser:
            rt = u"<a id='show_SalesAttr_%s' title='编辑销售所属人'>%s</a>" \
                 u"<script>$('#show_SalesAttr_%s').on('click',function()" \
                 u"{layer.open({type:2,skin:'layui-layer-lan',title:'修改'," \
                 u"fix:false,shadeClose: true,maxmin:true,area:['400px','200px']," \
                 u"content:'/t_product_depart_get/show_SalesAttr/?id=%s',});});" \
                 u"</script>" % (obj.id, obj.SalesAttr,obj.id, obj.id)

        return mark_safe(rt)
    show_SalesAttr.short_description = u'销售归属人'

    def show_more_information(self, obj):
        rt = u'商品名称(中文):%s <br><span style="color:green;cursor: pointer;" id="more_id_%s">更 多</span>' % (
            obj.Name2, obj.id)
        rt = u"%s<script>$('#more_id_%s').on('click',function()" \
             u"{layer.open({type:2,skin:'layui-layer-lan',title:'更多信息'," \
             u"fix:false,shadeClose: true,maxmin:true,area:['1500px','300px'],btn: ['关闭页面']," \
             u"content:'/more_product_informations/?flag_obj=%s&flag=t_product_depart_get',});" \
             u"});</script>" % (rt, obj.id, obj.id)
        return mark_safe(rt)

    show_more_information.short_description = u'<span style="color:#428bca;">商品信息</span>'



    
    list_display= ('pid','StaffName','show_SalesAttr','show_Pub_Info','UpdateTime','MainSKU','MGProcess','MGTime','show_SourcePicPath','show_more_information','show_SourcePicPath2','SpecialSell','SpecialRemark','show_urls','show_Secondary_research',)
    list_editable = ('SpecialSell','SpecialRemark','PublishedA',)
    
    search_fields=()
    # list_display_links = ('',)
    #list_editable_all = ('Keywords',)
    #list_filter = ('UpdateTime',
                   # 'Weight',
                   # 'Electrification','Powder','Liquid','Magnetism','Buyer',
                   # 'Storehouse',
                   # 'DYStaffName','JZLStaffName','PZStaffName','MGStaffName','LRStaffName',
                   # 'StaffName','DepartmentID',
                   # )

    # list_filter = ('UpdateTime',
    #                 'Weight',
    #                 'Electrification','Powder','Liquid','Magnetism','Buyer',
    #                 'Storehouse',
    #                 'DYStaffName','KFStaffName','XJStaffName','JZLStaffName','PZTime','PZStaffName','MGTime','MGStaffName','LRStaffName','LargeCategory','StaffName','LYTime',
    #                 'YNphoto','MGProcess',
    #                 )
    search_fields =None
    # search_fields = ('Keywords','URLamazon','URLebay','URLexpress','URLwish',
    #                 'SKU','MainSKU','Keywords2','StaffID','Name','Name2','Material',
    #                 'PlatformName','SourcePicRemark','SupplierID','SupplierArtNO','SupplierPColor','SupplierPDes',
    #                 'SupplierPUrl1','SupplierPUrl2',
    #                 'SpecialRemark','Remark' ,'InitialWord',
    #                 'Buyer','SupplierContact','Storehouse','Tags',
    #                 'possessMan2','LargeCategory','ReportName','ReportName2','PrepackMark',
    #                 'DYStaffName','DYSHStaffName','XJStaffName','KFStaffName','JZLStaffName',
    #                 'PZStaffName','MGStaffName','LRStaffName','StaffName','DepartmentID','pid',
    #                 )

    readonly_fields = ('URLamazon','URLebay','URLexpress','URLwish',
                      'SourceURL','OrdersLast7Days','Keywords2','SpecialRemark',
                      'Pricerange','ShelveDay','Name','Tags', #u'调研结果',
                      'SupplierPUrl1','SupplierPDes','SupplierID', # u'开发结果',
                      'UnitPrice','Weight','SpecialSell', #u'询价结果',
                      'Name2','Material','Unit','MinOrder','SupplierArtNO',
                      'SupplierPColor','SupplierPUrl2','OrderDays','StockAlarmDays','LWH',
                      'SupplierContact','Storehouse','ReportName','ReportName2','MinPackNum',#建资料
                      'ContrabandAttribute',# 'Electrification','Powder','Liquid','Magnetism',  #u'违禁品',
                      'Remark', #备注
                      'MainSKU', #主SKU
                      'DYTime','DYStaffName','DYSHTime','DYSHStaffName','XJTime','XJStaffName','KFTime','KFStaffName','JZLTime','JZLStaffName',
                      'PZTime','PZStaffName','MGTime','MGStaffName','LRTime','LRStaffName','Keywords'
                    )

    # 分组表单
    fields = ('Keywords','URLamazon','URLebay','URLexpress','URLwish',
              'SourceURL','OrdersLast7Days','Keywords2','SpecialRemark',
              'Pricerange','ShelveDay','Name','Tags', #u'调研结果',
              'SupplierPUrl1','SupplierPDes','SupplierID', # u'开发结果',
              'UnitPrice','Weight','SpecialSell', #u'询价结果',
              'Name2','Material','Unit','MinOrder','SupplierArtNO',
              'SupplierPColor','SupplierPUrl2','OrderDays','StockAlarmDays','LWH',
              'SupplierContact','Storehouse','ReportName','ReportName2','MinPackNum',#建资料
              'ContrabandAttribute',#'Electrification','Powder','Liquid','Magnetism',  #u'违禁品',
              'Remark', #备注
              'MainSKU', #主SKU
              'DYTime','DYStaffName','DYSHTime','DYSHStaffName','XJTime','XJStaffName','KFTime','KFStaffName','JZLTime','JZLStaffName',
              'PZTime','PZStaffName','MGTime','MGStaffName','LRTime','LRStaffName'
              )

    form_layout = (
        Fieldset(u'关键字与二次调研链接',
                    Row('Keywords'),
                    Row('URLamazon','URLebay','URLexpress'),
                    Row('URLwish'),
                    css_class = 'unsort '
                ),
        Fieldset(u'调研结果',
                    Row('SourceURL','OrdersLast7Days','Pricerange'),
                    Row('Keywords2','Tags'),
                    Row('ShelveDay','Name','SpecialRemark'),
                    css_class = 'unsort '
                ),
        Fieldset(u'开发&询价',
                    Row('SupplierPUrl1','SupplierPDes','SupplierID'),
                    Row('UnitPrice','Weight','SpecialSell'),
                    css_class = 'unsort  '
                ),
        Fieldset(u'建资料',
                    Row('Name2','Material','Unit'),
                    Row('MinOrder','SupplierArtNO', 'SupplierPColor'),
                    Row('SupplierPUrl2','OrderDays','StockAlarmDays'),
                    Row('LWH', 'SupplierContact','Storehouse'),
                    Row('ReportName','ReportName2','MinPackNum'),
                    css_class = 'unsort '
                ),
        Fieldset(u'违禁品',
                    Row('ContrabandAttribute',),
                    css_class = 'unsort '
                ),
        Fieldset(u'备注信息',
                    Row('Remark'),
                    css_class = 'unsort '
                ),
        Fieldset(u'主SKU信息',
                    Row('MainSKU'),
                    css_class = 'unsort '
                ),

                  )
    show_detail_fields = ['id']
    def save_models(self):
        #obj = self.new_obj#'Keywords','URLamazon','URLebay','URLexpress','URLwish'
        #request = self.request
        pass
        #obj.save()

        #t_product_depart_get.objects.filter(pid=obj.pid).update(Keywords=obj.Keywords)



    def get_list_queryset(self):
        from django.db.models import Q
        request = self.request
        
        qs = super(t_product_depart_get_user_Admin, self).get_list_queryset()

        # Electrification = request.GET.get('Electrification', '')
        # Powder = request.GET.get('Powder', '')
        # Liquid = request.GET.get('Liquid', '')
        # Magnetism = request.GET.get('Magnetism', '')
        ContrabandAttribute  = request.GET.get('ContrabandAttribute','')    #商品属性
        Storehouse = request.GET.get('Storehouse', '')
        LargeCategory = request.GET.get('LargeCategory', '')
        MainSKU = request.GET.get('MainSKU', '')
        MainSKU = MainSKU.split(',')
        if '' in MainSKU:
            MainSKU=''

        YNphoto = request.GET.get('YNphoto', '')  # 图片处理 0实拍 1制作
        MGProcess = request.GET.get('MGProcess', '')  # 图片状态 0待实拍 1待制作 2完成实拍 3完成制作 4错误

        DYStaffName = request.GET.get('DYStaffName', '')  # 调研员
        DYSHStaffName = request.GET.get('DYSHStaffName', '')  # 调研审核员
        XJStaffName = request.GET.get('XJStaffName', '')  # 询价员
        KFStaffName = request.GET.get('KFStaffName', '')  # 开发员
        MGStaffName = request.GET.get('MGStaffName', '')  # 美工员
        Buyer = request.GET.get('Buyer', '')  # 采购员
        CreateStaffName = request.GET.get('CreateStaffName', '')  # 创建人
        LRStaffName = request.GET.get('LRStaffName', '')  # 录入员

        KFTimeStart = request.GET.get('KFTimeStart', '')  # 开发时间
        KFTimeEnd = request.GET.get('KFTimeEnd', '')

        LYTimeStart = request.GET.get('LYTimeStart', '')  # 领用时间
        LYTimeEnd = request.GET.get('LYTimeEnd', '')
        JZLTimeStart = request.GET.get('JZLTimeStart', '')  # 建资料时间
        JZLTimeEnd = request.GET.get('JZLTimeEnd', '')

        MGTimeStart = request.GET.get('MGTimeStart', '')  # 图片完成时间
        MGTimeEnd = request.GET.get('MGTimeEnd', '')

        WeightStart = request.GET.get('WeightStart', '')  # 克重
        WeightEnd = request.GET.get('WeightEnd', '')

        keywords = request.GET.get('keywords', '') #关键词EN
        keywords2 = request.GET.get('keywords2', '')  # 关键词CH
        staffName = request.GET.get('staffName','') #领用人

        jZLStaffName = request.GET.get('jZLStaffName', '')  # 建资料员

        searchList = {'ContrabandAttribute__exact':ContrabandAttribute, 'Storehouse__exact': Storehouse, 'MainSKU__in': MainSKU,
                      'LargeCategory__exact': LargeCategory,
                      'YNphoto__exact': YNphoto, 'MGProcess__exact': MGProcess, 'DYStaffName__exact': DYStaffName,
                      'DYSHStaffName__exact': DYSHStaffName, 'JZLStaffName__exact':jZLStaffName,
                      'XJStaffName__exact': XJStaffName, 'KFStaffName__exact': KFStaffName,
                      'MGStaffName__exact': MGStaffName, 'Buyer__exact': Buyer,
                      'CreateStaffName__exact': CreateStaffName, 'LRStaffName__exact': LRStaffName,
                      'KFTime__gte': KFTimeStart, 'KFTime__lt': KFTimeEnd, 'JZLTime__gte': JZLTimeStart,
                      'JZLTime__lt': JZLTimeEnd,'LYTime__gte': LYTimeStart, 'LYTime__lt': LYTimeEnd,
                      'MGTime__gte': MGTimeStart, 'MGTime__lt': MGTimeEnd, 'Weight__gte': WeightStart,
                      'Weight__lt': WeightEnd, 'StaffName__exact':staffName
                      }
        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    # if k == 'ShopName__exact':
                    # v = 'Wish-' + v.zfill(4)
                    # messages.error(request, v)
                    sl[k] = v
        if sl is not None:
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'输入的查询数据有问题！')
                
        if keywords:
            qs = qs.filter(Q(Name__icontains=keywords) | Q(Keywords__icontains=keywords))
        if keywords2:
            qs = qs.filter(Q(Name2__icontains=keywords2) | Q(Keywords2__icontains=keywords2))
            
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(GetStaffID=request.user.username)

            
            
            
            
            
            
            
            