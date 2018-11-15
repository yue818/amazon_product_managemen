# -*- coding: utf-8 -*-
from .t_product_Admin import *
from brick.function.formatUrl import format_urls
#16)    未录入商品信息 v_product_allsku
class v_product_allsku_Admin(t_product_Admin):
    search_box_flag = True
    def show_oplog(self,obj) :
        rt = ''
        t_product_oplog_objs = t_product_oplog.objects.filter(pid=obj.id).order_by('-id')
        for t_product_oplog_obj in t_product_oplog_objs:
            rt = u'%s%s:%s,'%(rt,t_product_oplog_obj.StepName,t_product_oplog_obj.OpName)
        return rt
    show_oplog.short_description = u'操作历史'

    # def show_urls(self,obj) :
    #     Platform,linkurl = format_urls(obj.SourceURL if obj.SourceURL else '')
    #     if 'can not formate' in Platform:
    #         linkurl = 'reverse_url'
    #     pSupplier,pSupplierurl =format_urls(obj.SupplierPUrl1 if obj.SupplierPUrl1 else '')
    #     if 'can not formate' in pSupplier:
    #         pSupplierurl = 'Supplierurl'
    #     rt = u'反:<a href="%s" target="_blank" >%s:%s</a><br>供:<a href="%s" target="_blank" >%s:%s</a>'%(obj.SourceURL,Platform,linkurl,obj.SupplierPUrl1,pSupplier,pSupplierurl)
    #     return mark_safe(rt)
    # show_urls.short_description = u'链接信息'

    def show_more_information(self,obj):
        rt = u'商品名称(中文):%s <br><span style="color:green;cursor: pointer;" id="more_id_%s">更 多</span>' % (
        obj.Name2, obj.id)
        rt = u"%s<script>$('#more_id_%s').on('click',function()" \
             u"{layer.open({type:2,skin:'layui-layer-lan',title:'更多信息'," \
             u"fix:false,shadeClose: true,maxmin:true,area:['1500px','300px'],btn: ['关闭页面']," \
             u"content:'/more_product_informations/?flag_obj=%s&flag=v_product_allsku',});" \
             u"});</script>" % (rt, obj.id, obj.id)
        return mark_safe(rt)
    show_more_information.short_description = u'<span style="color:#428bca;">商品信息</span>'

    #list_display= ('id','T','CreateTime','CreateStaffName','SourcePicPath2','MainSKU','show_skulist','UpdateTime','StaffID','Name2','fromT','show_oplog',)
    list_display= ('id','T','show_SourcePicPath','SpecialSell','show_SourcePicPath2','MainSKU','show_skulist',
                   'show_more_information','SpecialRemark','show_urls',)
    #list_display= ('id','MainSKU','DYTime','DYStaffName','show_SourcePicPath','Name2','Keywords','Keywords2','Pricerange','ShelveDay','OrdersLast7Days','JZLTime','JZLStaffName','show_SourcePicPath2','SpecialSell','SpecialRemark','show_urls',)
    search_fields =None
    # 分组表单
    fields = ('SourceURL','OrdersLast7Days','Keywords','Keywords2','SpecialRemark',
              'Pricerange','ShelveDay','Name','Tags', #u'调研结果',
              'SupplierPUrl1','SupplierPDes','SupplierID', # u'开发结果',
              'UnitPrice','Weight','SpecialSell', #u'询价结果',
              'Name2','Material','Unit','MinOrder','SupplierArtNO',
              'SupplierPColor','SupplierPUrl2','OrderDays','StockAlarmDays','LWH',
              'SupplierContact','Storehouse','ReportName','ReportName2','MinPackNum',  #建资料
              'ContrabandAttribute',# 'Electrification','Powder','Liquid','Magnetism',  #u'违禁品',
              'Remark',  #备注
              'MainSKU',  #主SKU
              'DYTime','DYStaffName','DYSHTime','DYSHStaffName','XJTime','XJStaffName','KFTime','KFStaffName','JZLTime','JZLStaffName',
              'PZTime','PZStaffName','MGTime','MGStaffName','LRTime','LRStaffName'
              )

    form_layout = (
        Fieldset(u'调研结果',
                    Row('SourceURL','OrdersLast7Days','Pricerange'),
                    Row('Keywords','Keywords2','Tags'),
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
    
    
    def get_list_queryset(self,):
        request = self.request
        qs = super(v_product_allsku_Admin, self).get_list_queryset()
        
        # Electrification = request.GET.get('Electrification','')
        # Powder          = request.GET.get('Powder','')
        # Liquid          = request.GET.get('Liquid','')
        # Magnetism       = request.GET.get('Magnetism','')
        ContrabandAttribute = request.GET.get('ContrabandAttribute', '')  # 商品属性
        Storehouse      = request.GET.get('Storehouse','')
        LargeCategory   = request.GET.get('LargeCategory','')
        MainSKU = request.GET.get('MainSKU','')
        
        YNphoto = request.GET.get('YNphoto','') # 图片处理 0实拍 1制作 
        MGProcess       = request.GET.get('MGProcess','')#图片状态 0待实拍 1待制作 2完成实拍 3完成制作 4错误
        
        Buyer           = request.GET.get('Buyer','')#采购员
        DYStaffName     = request.GET.get('DYStaffName','')#调研员
        KFStaffName     = request.GET.get('KFStaffName','')#开发员
        XJStaffName     = request.GET.get('XJStaffName','')#询价员
        JZLStaffName    = request.GET.get('JZLStaffName','')#建资料员
        PZStaffName     = request.GET.get('PZStaffName','')#拍照员
        MGStaffName     = request.GET.get('MGStaffName','')#美工员
        LRStaffName     = request.GET.get('LRStaffName','')#录入员
        
        WeightStart = request.GET.get('WeightStart','')#克重
        WeightEnd = request.GET.get('WeightEnd','')
    
        orders7DaysStart = request.GET.get('orders7DaysStart','')
        orders7DaysEnd = request.GET.get('orders7DaysEnd','')
        updateTimeStart = request.GET.get('updateTimeStart','')#refreshTimeStart
        updateTimeEnd = request.GET.get('updateTimeEnd', '')

        searchList = {  'MainSKU__exact':MainSKU,'ContrabandAttribute__exact':ContrabandAttribute,
                        'Storehouse__exact':Storehouse, 'LargeCategory__exact':LargeCategory,
                        'YNphoto__exact': YNphoto,'YNphoto__exact':YNphoto,'MGProcess__exact':MGProcess, 'Buyer__exact':Buyer, 'DYStaffName__exact':DYStaffName,
                        'KFStaffName__exact':KFStaffName, 'XJStaffName__exact':XJStaffName, 'JZLStaffName__exact':JZLStaffName,
                        'PZStaffName__exact':PZStaffName, 'MGStaffName__exact':MGStaffName, 'LRStaffName__exact':LRStaffName,
                        'Weight__gte':WeightStart, 'Weight__lt':WeightEnd, 'Orders7DaysAll__gte': orders7DaysStart, 'Orders7DaysAll__lt': orders7DaysEnd,
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

