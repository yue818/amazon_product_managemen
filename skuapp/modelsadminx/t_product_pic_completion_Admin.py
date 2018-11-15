# -*- coding: utf-8 -*-
from .t_product_Admin import *
from pyapp.models import b_goods as py_b_goods
from skuapp.table.t_product_enter_ed import t_product_enter_ed
from skuapp.table.t_product_depart_get import t_product_depart_get
from skuapp.table.t_product_oplog import t_product_oplog
from skuapp.table.t_product_mainsku_sku import  t_product_mainsku_sku
from pyapp.models import xxxb_packinfo
from datetime import datetime
from brick.function.formatUrl import format_urls
# from django.db.models import Q
# from django_redis import get_redis_connection
# redis_coon = get_redis_connection(alias='has_oss_image_sku')

class t_product_pic_completion_Admin(t_product_Admin):
    enter_ed_classification = True
    search_box_flag = True

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





    def show_skuattrs(self,obj) :
        rt = '<table  style="text-align:center"><tr><th style="text-align:center">子SKU-</th><th style="text-align:center">属性</th></tr>'
        if obj.PZRemake == '1':
            t_product_mainsku_sku_objs = t_product_mainsku_sku.objects.filter(pid=obj.pid).order_by('SKU')
            for t_product_mainsku_sku_obj in t_product_mainsku_sku_objs:
                PackName =''
                CostPrice =0
                PackNID= t_product_mainsku_sku_obj.PackNID
                try:
                    if PackNID > 0 :
                        B_PackInfo_obj = B_PackInfo.objects.get(id__exact = PackNID)
                        if B_PackInfo_obj is not None:
                            PackName =  B_PackInfo_obj.PackName
                            CostPrice = B_PackInfo_obj.CostPrice
                except:
                    pass
                rt =  '%s <tr><td>%s</td><td>%s</td></tr> '%(rt,t_product_mainsku_sku_obj.SKU,t_product_mainsku_sku_obj.SKUATTRS)

        elif obj.PZRemake == '0':
            b_goods_objs = py_b_goods.objects.values('SKU','GoodsName').filter(SKU__startswith=obj.MainSKU)
            for b_goods_obj in b_goods_objs :
                rt =  '%s <tr><td>%s</td><td>%s</td></tr> '%(rt,b_goods_obj['SKU'],b_goods_obj['GoodsName'])

        rt = '%s</table>'%rt
        return mark_safe(rt)
    show_skuattrs.short_description = mark_safe('<p align="center"> 子SKU</p>')

    def show_Request(self,obj) :
        piclist = list((u'%s'%(obj.PictureRequest,)).replace('<br>',''))
        num = 0
        while True:
            num = num + 32
            if num >= len(piclist):
                break
            piclist.insert(num, '<br>')
        return mark_safe(''.join( piclist ))
    show_Request.short_description = u'图片要求备注'
    
    # def show_urls(self, obj):
    #     Platform, linkurl = format_urls(obj.SourceURL if obj.SourceURL else '')
    #     if 'can not formate' in Platform:
    #         linkurl = 'reverse_url'
    #     pSupplier, pSupplierurl = format_urls(obj.SupplierPUrl1 if obj.SupplierPUrl1 else '')
    #     if 'can not formate' in pSupplier:
    #         pSupplierurl = 'Supplierurl'
    #     rt = u'反:<a href="%s" target="_blank" >%s:%s</a><br>供:<a href="%s" target="_blank" >%s:%s</a>' % (
    #     obj.SourceURL, Platform, linkurl, obj.SupplierPUrl1, pSupplier, pSupplierurl)
    #     return mark_safe(rt)
    # show_urls.short_description = u'链接信息'

    def show_oplog(self,obj) :
        rt = ''
        t_product_oplog_objs = t_product_oplog.objects.filter(pid=obj.pid,MainSKU=obj.MainSKU).order_by('id')
        for t_product_oplog_obj in t_product_oplog_objs:
            rt = u'%s%s:%s,'%(rt,t_product_oplog_obj.StepName,t_product_oplog_obj.OpName)
        return rt
    show_oplog.short_description = u'操作历史'

    def show_skulist_XG(self, obj):
        rt = u'<table  style="text-align:center">' \
             u'<tr>' \
             u'<th style="text-align:center">子SKU-</th>' \
             u'<th style="text-align:center">属性-</th>' \
             u'<th style="text-align:center">单价-</th>' \
             u'<th style="text-align:center">克重-</th>' \
             u'<th style="text-align:center">包装规格-</th>' \
             u'<th style="text-align:center">内包装成本-</th>' \
             u'<th style="text-align:center">最小包装数-</th>' \
             u'<th style="text-align:center">服装类信息-</th>' \
             u'<th style="text-align:center">供应商链接</th>' \
             u'<th style="text-align:center">供应商货号</th>' \
             u'</tr>'
        if obj.MainSKU is not None:
            t_product_mainsku_sku_objs = t_product_mainsku_sku.objects.filter(pid=obj.pid,MainSKU=obj.MainSKU).order_by('SKU')
            for t_product_mainsku_sku_obj in t_product_mainsku_sku_objs:
                PackName = ''
                CostPrice = 0
                PackNID = t_product_mainsku_sku_obj.PackNID

                try:
                    if PackNID > 0:
                        B_PackInfo_obj = B_PackInfo.objects.get(id__exact=PackNID)
                        if B_PackInfo_obj is not None:
                            PackName = B_PackInfo_obj.PackName
                            CostPrice = B_PackInfo_obj.CostPrice
                except Exception, ex:
                    pass

                SupplierLink = t_product_mainsku_sku_obj.SupplierLink
                if not SupplierLink:
                    SupplierLink = obj.SupplierPUrl1

                SupplierNum = t_product_mainsku_sku_obj.SupplierNum
                if not SupplierNum:
                    SupplierNum = obj.SupplierArtNO

                # sku = t_product_mainsku_sku_obj.SKU
                # product_sku = obj.MainSKU + sku
                # picture = r'https://fancyqube-goodspic.oss-cn-shanghai.aliyuncs.com/%s.jpg' % product_sku
                #
                # image = u'<img src="%s" id="image_%s" width="60" height="60" onclick="javascrip:$(\'#image_upload_%s\').click();">' \
                #         u'<input type="file" id="image_upload_%s" onchange="to_upload_goods_pic(this,\'%s\')" accept="image/gif, ' \
                #         u'image/jpeg, image/png, image/gif" style="display: none">' % (picture, product_sku, product_sku, product_sku, product_sku)
                #

                # op = u"<a id=upload_pic_%s_%s><p>上传</p></a>" \
                #      u"<script>$('#upload_pic_%s_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan'," \
                #      u"title:'上传图片',fix:false,shadeClose: true,maxmin:true,area:['510px','600px']," \
                #      u"content:'/upload_goods_pic/?sku=%s',end:function(){location.reload();}});});;</script>" % (
                #      obj.id, product_sku, obj.id, product_sku, product_sku)

                rt = u'%s <tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' \
                     u'<td><input value="%s" style="width: 100px;border:none;background-color:transparent;" type="text" readonly title="%s"/></td>' \
                     u'<td><input value="%s" style="width: 100px;border:none;background-color:transparent;" type="text" readonly title="%s"/></td>' \
                     u'</tr> ' % \
                     (
                         rt, t_product_mainsku_sku_obj.SKU, t_product_mainsku_sku_obj.SKUATTRS,
                         t_product_mainsku_sku_obj.UnitPrice,
                         t_product_mainsku_sku_obj.Weight, PackName, CostPrice, t_product_mainsku_sku_obj.MinPackNum,
                         t_product_mainsku_sku_obj.DressInfo, SupplierLink, SupplierLink,SupplierNum,SupplierNum
                     )

        rt = '%s</table>' % rt
        return mark_safe(rt)

    show_skulist_XG.short_description = mark_safe('<p align="center"> 子SKU信息</p>')

    def show_MainSKU(self,obj) :
        from brick.public.django_wrap import django_wrap
        rt = django_wrap(obj.MainSKU,',',3)
        return mark_safe(rt)
    show_MainSKU.short_description = u'*主SKU'
    
    # list_display = ('pid', 'MainSKU','SampleState', 'MGProcess', 'MGTime', 'DYTime', 'DYStaffName', 'show_SourcePicPath',
    #         'Name2', 'Keywords', 'Keywords2', 'Pricerange', 'ShelveDay', 'OrdersLast7Days', 'JZLTime', 'JZLStaffName',
    #         'show_SourcePicPath2', 'SpecialSell', 'SpecialRemark', 'show_urls','show_oplog')
    list_display = (
    'pid', 'show_Request', 'MGProcess', 'MGStaffName', 'MGTime', 'JZLTime', 'JZLStaffName', 'show_SourcePicPath2',
    'show_MainSKU', 'show_skulist_XG', 'Name2', 'Material', 'SpecialSell','show_urls','show_oplog')
    readonly_fields = ('id','SKU','MainSKU','Keywords','Keywords2','UpdateTime','StaffID',
            'Name','Name2','Material','Length','Width','Height','LWH','Weight',
            'SourceURL','PlatformName','PlatformPID','SourcePicPath','SourcePicRemark',
            'ArtPicPath','UnitPrice','Unit','#PackingID','#PackingID2','PackingID2Num',
            'MinPackNum','MinOrder','SupplierID','SupplierArtNO','SupplierPColor',
            'SupplierPDes','SupplierPUrl1','SupplierPUrl2','OrderDays','StockAlarmDays',
            'SpecialRemark','Remark','InitialWord','SourceURLPrice','ShelveDay',
            'OrdersLast7Days','SpecialSell','OldSKU','#Category1','Category2',
            'Category3','ContrabandAttribute','Buyer',
            'SupplierContact','SourcePicPath2','Storehouse','URLamazon','URLebay',
            'URLexpress','URLwish','Pricerange','NumBought','TotalInventory','Tags',
            'SurveyRemark','PackNID','possessMan2','LargeCategory','SmallCategory',
            'ReportName','ReportName2','fromT','PrepackMark','CreateTime','CreateStaffName',
            'selectpic','selectpic2','DYTime','DYStaffName','DYSHTime','DYSHStaffName',
            'XJTime','XJStaffName','KFTime','KFStaffName','JZLTime','JZLStaffName','PZTime',
            'PZStaffName','MGTime','MGStaffName','LRTime','LRStaffName','YNphoto','MGProcess',
            'PPosition','PictureRequest','PZRemake','PZTimeing','PZStaffNameing','SampleState',
            'pid')

    show_detail_fields = ['id']

    list_per_page = 20

            
    def get_list_queryset(self,):
        request = self.request
        qs = super(t_product_pic_completion_Admin, self).get_list_queryset()
        
        # Electrification = request.GET.get('Electrification','')
        # Powder          = request.GET.get('Powder','')
        # Liquid          = request.GET.get('Liquid','')
        # Magnetism       = request.GET.get('Magnetism','')
        ContrabandAttribute  = request.GET.get('ContrabandAttribute','')    #商品属性
        Storehouse      = request.GET.get('Storehouse','')
        LargeCategory   = request.GET.get('LargeCategory','')
        MainSKU = request.GET.get('MainSKU','')
        MHMainSKU = request.GET.get('MHMainSKU','')

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
        flagcloth = request.GET.get('classCloth', '')
        
        WeightStart = request.GET.get('WeightStart','')#克重
        WeightEnd = request.GET.get('WeightEnd','')
    
        orders7DaysStart = request.GET.get('orders7DaysStart','')
        orders7DaysEnd = request.GET.get('orders7DaysEnd','')
        updateTimeStart = request.GET.get('updateTimeStart','')#refreshTimeStart
        updateTimeEnd = request.GET.get('updateTimeEnd', '')
        BJP_FLAG        = request.GET.get('BJP_FLAG','')

        searchList = {  'MainSKU__exact':MainSKU,'ContrabandAttribute__exact':ContrabandAttribute,
                        'Storehouse__exact':Storehouse, 'LargeCategory__exact':LargeCategory,
                        'YNphoto__exact': YNphoto,'MGProcess__exact':MGProcess, 'Buyer__exact':Buyer, 'DYStaffName__exact':DYStaffName,
                        'KFStaffName__exact':KFStaffName, 'XJStaffName__exact':XJStaffName, 'JZLStaffName__exact':JZLStaffName,
                        'PZStaffName__exact':PZStaffName, 'MGStaffName__exact':MGStaffName, 'LRStaffName__exact':LRStaffName,
                        'Weight__gte':WeightStart, 'Weight__lt':WeightEnd, 'Orders7DaysAll__gte': orders7DaysStart, 'Orders7DaysAll__lt': orders7DaysEnd,
                        'UpdateTime__gte': updateTimeStart, 'UpdateTime__lt': updateTimeEnd,'MainSKU__contains':MHMainSKU,'BJP_FLAG__exact':BJP_FLAG,
                        }

        sl = {}
        for k,v in searchList.items():
            if isinstance(v,list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    sl[k] = v
        if sl is not None:
            try:
                qs = qs.filter(**sl)
            except Exception,ex:
                messages.error(request,u'输入的查询数据有问题！')

        # HasImage = request.GET.get('HasImage', '')
        # if HasImage:
        #     HasOssImageMainSKU = redis_coon.get('HasOssImageMainSKU')
        #     try:
        #         mainsku_list = HasOssImageMainSKU.split(',')
        #     except:
        #         mainsku_list = []
        #     if HasImage == '1':
        #         qs = qs.filter(MainSKU__in=mainsku_list)
        #     else:
        #         qs = qs.filter(~Q(MainSKU__in=mainsku_list))

        catelist = [u'001.时尚女装', u'002.时尚男装', u'021.泳装', u'024.童装', u'025.内衣']

        if flagcloth == '1':
            return qs.filter(LargeCategory__in=catelist)
        elif flagcloth == '2':
            return qs.exclude(LargeCategory__in=catelist)
        else:
            return qs