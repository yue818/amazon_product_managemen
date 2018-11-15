# -*- coding: utf-8 -*-
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from django.utils.safestring import mark_safe
from skuapp.table.t_online_info import *
import logging
from django.forms import TextInput, Textarea
from skuapp.table.t_online_info_wish import *
from skuapp.table.t_store_configuration_file import *
import requests
from django.contrib import messages
from skuapp.wish_joom_data import *
from skuapp.table.t_api_schedule_ing import t_api_schedule_ing
from skuapp.table.t_online_info_wait_publish_joom2 import *
from skuapp.table.t_distribution_product_to_store_result import *
from skuapp.table.t_online_info_publish_joom import *
from Project.settings import *
from .t_product_Admin import *
from django.contrib import messages
from django.db.models import Q
from datetime import datetime


class t_online_info_wait_publish_joom2_Admin(object):
    downloadxls = True
    import_flag = False
    pp_flag2 = True

    def show_Picture(self,obj) :
        #url = u'https://contestimg.wish.com/api/webimage/%s-medium.jpg'%str(obj.ProductID)
        try:
            rt =  '<img src="%s"  width="120" height="120" />  '%(obj.Image.replace('-original', '-medium'))
        except:
            rt = ''
        return mark_safe(rt)
    show_Picture.short_description = u'图片'


    def get_product_ID_link(self,obj) :
        return mark_safe('<a href=https://www.amazon.com/dp/%s>%s</a>'%(obj.ProductID,obj.ProductID))
    get_product_ID_link.short_description = u'产品ID'

    def show_ShopName_Seller(self,obj) :
        rt=''
        rt = u'%s卖家简称:<br>%s<br>店长/销售员:<br>%s'%(rt,obj.ShopName,obj.Seller)
        return mark_safe(rt)
    show_ShopName_Seller.short_description = u'卖家简称/店长/销售员'


    def show_Title_ProductID(self,obj) :
        l = obj.Title.split(' ')
        aa = len(l)
        ll = ''
        rt=''
        logger = logging.getLogger('sourceDns.webdns.views')
        #
        if aa <= 6:
            rt = u'%s标题: %s<br>产品ID: <a href=" https://www.wish.com/c/%s" target="_blank">%s</a>'%(rt,obj.Title,obj.ProductID,obj.ProductID)
        elif aa > 6:
            newe_Title_list = []
            for i in range(0, len(l), 6):
                min_list = ''
                for a in l[i:i+6]:
                    min_list = u'%s%s '%(min_list,a)
                newe_Title_list.append(min_list)
                #logger.error("newe_Title_list===================xxxxxxxxxxxxxxx=%s "%(newe_Title_list))
            for newe_Title  in newe_Title_list:
                ll = u'%s%s<br>'%(ll,newe_Title)
            if len(ll) >= 100:
                rt = u'%s标题:<br><font color="red">%s</font>产品ID:<br><a href=" https://www.wish.com/c/%s" target="_blank">%s</a>'%(rt,ll,obj.ProductID,obj.ProductID)
            else:
                rt = u'%s标题:<br>%s产品ID:<br><a href=" https://www.wish.com/c/%s" target="_blank">%s</a>'%(rt,ll,obj.ProductID,obj.ProductID)
        return mark_safe(rt)
    show_Title_ProductID.short_description = u'标题/产品ID'



    def show_time(self,obj) :
        rt=''
        rt = u'%s刷新时间:<br>%s <br>上架时间:<br>%s <br>最近更新时间:<br>%s'%(rt,obj.RefreshTime,obj.DateUploaded,obj.LastUpdated)
        return mark_safe(rt)
    show_time.short_description = u'时间'

    def show_SKU_list(self,obj) :
        rt='<table style="text-align:center;float:left" border="1" cellpadding="3" cellspacing="1" bgcolor="#c1c1c1"><tr bgcolor="#C00"><th style="text-align:center">子SKU</th><th style="text-align:center">店铺SKU</th><th style="text-align:center">库存量</th><th style="text-align:center">价格</th></tr>'
        t_online_info_wish_objs = t_online_info_publish_joom.objects.values('SKU','ShopSKU','Quantity','Price').filter(ProductID=obj.ProductID,SKUStatus=0).distinct()
        i = 0
        for t_online_info_wish_obj in t_online_info_wish_objs:
            if i < 5:
                rt = '%s <tr bgcolor="#FFFFFF"><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr> '%(rt,t_online_info_wish_obj['SKU'],t_online_info_wish_obj['ShopSKU'],t_online_info_wish_obj['Quantity'],t_online_info_wish_obj['Price'])
                i = i + 1
        if len(t_online_info_wish_objs)>5:
            rt = '%s<tr><td><a id="link_id_%s">查看更多</a></td></tr>'%(rt,obj.id)
            
        rt='%s<table style="text-align:center;float:right" border="1" cellpadding="3" cellspacing="1" bgcolor="#c1c1c1"><tr bgcolor="#C00"><th style="text-align:center">子SKU</th><th style="text-align:center">店铺SKU</th><th style="text-align:center">库存量</th><th style="text-align:center">价格</th></tr>'%rt
        t_online_info_wish_objs2 = t_online_info_publish_joom.objects.values('SKU','ShopSKU','Quantity','Price').filter(ProductID=obj.ProductID,SKUStatus=1).distinct()
        i = 0
        for t_online_info_wish_obj in t_online_info_wish_objs2:
            if i < 5:
                rt = '%s <tr bgcolor="#FFFFFF"><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr> '%(rt,t_online_info_wish_obj['SKU'],t_online_info_wish_obj['ShopSKU'],t_online_info_wish_obj['Quantity'],t_online_info_wish_obj['Price'])
                i = i + 1
        if len(t_online_info_wish_objs)>5:
            rt = '%s<tr><td><a id="link_id_%s">查看更多</a></td></tr>'%(rt,obj.id)
        else:
            rt = rt
        rt = "%s</table><script>$('#link_id_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'查看全部',fix:false,shadeClose: true,maxmin:true,area:['500px','500px'],content:'/t_online_info_wish/SKU/?abc=%s',});});</script>"%(rt,obj.id,obj.ProductID)
        return mark_safe(rt)
    show_SKU_list.short_description = mark_safe('<span align="left" style="color:green;float:left"><span style="background:#CCCCCC;font-size: medium">正常</span></span><span align="right" style="float:right"><span style="background:#CCCCCC;color:red;font-size: medium">非正常</span></span>')

    def show_orders7days(self,obj) :

        rt =  "<a id=show_orderlist_%s>日销量</a><script>$('#show_orderlist_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'查看全部',fix:false,shadeClose: true,maxmin:true,area:['1000px','600px'],content:'/t_online_info_wish/order1day/?aID=%s',});});</script>"%(obj.id,obj.id,obj.ProductID)
        #rt = "%s<br><br><br><br>"%(rt)
        #rt = "%s<a href='/Project/admin/skuapp/t_online_info_publish_joom/?_q_=%s'>编辑</a>"%(rt,obj.ProductID)
        return mark_safe(rt)

    show_orders7days.short_description = u'操作'

    list_per_page=150
    list_display = ('id','show_Picture','show_ShopName_Seller','Orders7Days','show_Title_ProductID','show_SKU_list','show_orders7days')
    list_editable = ('show_Title')
    fields = ('id',)
    #list_filter = ('Seller','Orders7Days','RefreshTime','Status','ReviewState','DateUploaded','LastUpdated',)
    #readonly_fields = ('ProductID','ShopIP','ShopName','Quantity','Orders7Days','ParentSKU','SKU','ShopSKU')
    search_fields = ('id','PlatformName','ProductID','ShopIP','ShopName','Title','SKU','Orders7Days','Status','ReviewState','ParentSKU','Seller',)

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':5, 'cols':50})},
        }



    #actions = ('to_excel','INSERT_INTO_SCHEDULE1','INSERT_INTO_SCHEDULE2','INSERT_INTO_SCHEDULE3','INSERT_INTO_SCHEDULE4','INSERT_INTO_SCHEDULE5')
    actions = ('to_excel1','to_excel2')
    '''
    def INSERT_INTO_SCHEDULE1(self,request,objs):
        for obj in objs:
            json_str = get_joom_data(obj.ProductID,'Joom-002-hedongbl/YW')
            #messages.error(request,json_str)
            t_online_info_publish_joom_obj = t_online_info_publish_joom.objects.filter(ProductID=obj.ProductID).values_list('MainSKU')
            time=datetime.now()

            t_distribution_product_to_store_result_obj=t_distribution_product_to_store_result.objects.create(PlatformName='Joom',PID=obj.id,SKU=t_online_info_publish_joom_obj[0][0],ShopName='Joom-002-hedongbl/YW',Submitter=request.user.username,Status='正在刊登',Params=json_str)
            json_str = eval(json_str)
            json_str['id'] = t_distribution_product_to_store_result_obj.id
            t_api_schedule_ing.objects.create(Status='0',ShopName='Joom-002-hedongbl/YW',PlatformName='Joom',CMDID='UPLOAD',ScheduleTime=time,InsertTime=time,Params=json_str,Processed=0,Successful=0,WithError=0,WithWarning=0)
        t_online_info_wait_publish.objects.filter(ProductID=obj.ProductID).update(ispublished='已刊登')
    INSERT_INTO_SCHEDULE1.short_description = u'刊登Joom-002-hedongbl/YW'

    def INSERT_INTO_SCHEDULE2(self,request,objs):
        for obj in objs:
            json_str = get_joom_data(obj.ProductID,'Joom-002-hedongcloth/YW')
            #messages.error(request,json_str)
            t_online_info_publish_joom_obj = t_online_info_publish_joom.objects.filter(ProductID=obj.ProductID).values_list('MainSKU')
            time=datetime.now()

            t_distribution_product_to_store_result_obj=t_distribution_product_to_store_result.objects.create(PlatformName='Joom',PID=obj.id,SKU=t_online_info_publish_joom_obj[0][0],ShopName='Joom-002-hedongbl/YW',Submitter=request.user.username,Status='正在刊登',Params=json_str)
            json_str = eval(json_str)
            json_str['id'] = t_distribution_product_to_store_result_obj.id
            t_api_schedule_ing.objects.create(Status='0',ShopName='Joom-002-hedongcloth/YW',PlatformName='Joom',CMDID='UPLOAD',ScheduleTime=time,InsertTime=time,Params=json_str,Processed=0,Successful=0,WithError=0,WithWarning=0)
        t_online_info_wait_publish.objects.filter(ProductID=obj.ProductID).update(ispublished='已刊登')
    INSERT_INTO_SCHEDULE2.short_description = u'刊登Joom-002-hedongcloth/YW'

    def INSERT_INTO_SCHEDULE3(self,request,objs):
        for obj in objs:
            json_str = get_joom_data(obj.ProductID,'Joom-002-hedonggadget/YW')
            #messages.error(request,json_str)
            t_online_info_publish_joom_obj = t_online_info_publish_joom.objects.filter(ProductID=obj.ProductID).values_list('MainSKU')
            time=datetime.now()

            t_distribution_product_to_store_result_obj=t_distribution_product_to_store_result.objects.create(PlatformName='Joom',PID=obj.id,SKU=t_online_info_publish_joom_obj[0][0],ShopName='Joom-002-hedongbl/YW',Submitter=request.user.username,Status='正在刊登',Params=json_str)
            json_str = eval(json_str)
            json_str['id'] = t_distribution_product_to_store_result_obj.id
            t_api_schedule_ing.objects.create(Status='0',ShopName='Joom-002-hedonggadget/YW',PlatformName='Joom',CMDID='UPLOAD',ScheduleTime=time,InsertTime=time,Params=json_str,Processed=0,Successful=0,WithError=0,WithWarning=0)
        t_online_info_wait_publish.objects.filter(ProductID=obj.ProductID).update(ispublished='已刊登')
    INSERT_INTO_SCHEDULE3.short_description = u'刊登Joom-002-hedonggadget/YW'

    def INSERT_INTO_SCHEDULE4(self,request,objs):
        for obj in objs:
            json_str = get_joom_data(obj.ProductID,'Joom-002-hedongbabytoy/YW')
            #messages.error(request,json_str)
            t_online_info_publish_joom_obj = t_online_info_publish_joom.objects.filter(ProductID=obj.ProductID).values_list('MainSKU')
            time=datetime.now()

            t_distribution_product_to_store_result_obj=t_distribution_product_to_store_result.objects.create(PlatformName='Joom',PID=obj.id,SKU=t_online_info_publish_joom_obj[0][0],ShopName='Joom-002-hedongbl/YW',Submitter=request.user.username,Status='正在刊登',Params=json_str)
            json_str = eval(json_str)
            json_str['id'] = t_distribution_product_to_store_result_obj.id
            t_api_schedule_ing.objects.create(Status='0',ShopName='Joom-002-hedongbabytoy/YW',PlatformName='Joom',CMDID='UPLOAD',ScheduleTime=time,InsertTime=time,Params=json_str,Processed=0,Successful=0,WithError=0,WithWarning=0)
        t_online_info_wait_publish.objects.filter(ProductID=obj.ProductID).update(ispublished='已刊登')
    INSERT_INTO_SCHEDULE4.short_description = u'刊登Joom-002-hedongbabytoy/YW'

    def INSERT_INTO_SCHEDULE5(self,request,objs):
        for obj in objs:
            json_str = get_joom_data(obj.ProductID,'Joom-002-hedongwomenbeauty/YW')
            #messages.error(request,json_str)
            t_online_info_publish_joom_obj = t_online_info_publish_joom.objects.filter(ProductID=obj.ProductID).values_list('MainSKU')
            time=datetime.now()

            t_distribution_product_to_store_result_obj=t_distribution_product_to_store_result.objects.create(PlatformName='Joom',PID=obj.id,SKU=t_online_info_publish_joom_obj[0][0],ShopName='Joom-002-hedongbl/YW',Submitter=request.user.username,Status='正在刊登',Params=json_str)
            json_str = eval(json_str)
            json_str['id'] = t_distribution_product_to_store_result_obj.id
            t_api_schedule_ing.objects.create(Status='0',ShopName='Joom-002-hedongwomenbeauty/YW',PlatformName='Joom',CMDID='UPLOAD',ScheduleTime=time,InsertTime=time,Params=json_str,Processed=0,Successful=0,WithError=0,WithWarning=0)
        t_online_info_wait_publish.objects.filter(ProductID=obj.ProductID).update(ispublished='已刊登')
    INSERT_INTO_SCHEDULE5.short_description = u'刊登Joom-002-hedongwomenbeauty/YW'
    '''
        

    def get_list_queryset(self,):
        request = self.request
        qs = super(t_online_info_wait_publish_joom2_Admin, self).get_list_queryset()
        status = request.GET.get('status')
        st = request.GET.get('st')
        
        if st == 'yy':
            qs = qs.filter(ispublished='已刊登')
        if st == 'nn':
            qs = qs.exclude(ispublished="已刊登")
            if status == 'HedongCloth':
                qs = qs.filter(MainSKU__startswith='M').exclude(Q(MainSKU__startswith='MU')|Q(MainSKU__startswith='MI'))
            #elif status == 'bl':
                #qs = qs.filter(Q(MainSKU__startswith='BDY')|Q(MainSKU__startswith='BL')|Q(MainSKU__startswith='BRH')|Q(MainSKU__startswith='CFL')|Q(MainSKU__startswith='EAR')|Q(MainSKU__startswith='FAN')|Q(MainSKU__startswith='JA')|Q(MainSKU__startswith='JR')|Q(MainSKU__startswith='KEY')|Q(MainSKU__startswith='NL')|Q(MainSKU__startswith='PD')|Q(MainSKU__startswith='RG'))
            #elif status == 'Gadget':
                #qs = qs.filter(Q(MainSKU__startswith='HG')|Q(MainSKU__startswith='WS')|Q(MainSKU__startswith='PET')|Q(MainSKU__startswith='WF')|Q(MainSKU__startswith='CAR')|Q(MainSKU__startswith='TL')|Q(MainSKU__startswith='XMA')|Q(MainSKU__startswith='PY'))
            elif status == 'BabyToy':
                qs = qs.filter(Q(MainSKU__startswith='CEA')|Q(MainSKU__startswith='MI')|Q(MainSKU__startswith='TOY')|Q(MainSKU__startswith='SX')|Q(MainSKU__startswith='PA')|Q(MainSKU__startswith='FH')|Q(MainSKU__startswith='SPT')|Q(MainSKU__startswith='WH')|Q(MainSKU__startswith='COA'))
            elif status == 'WomenBeauty':
                qs = qs.filter(Q(MainSKU__startswith='MU')|Q(MainSKU__startswith='NA')|Q(MainSKU__startswith='HHC')|Q(MainSKU__startswith='HA')|Q(MainSKU__startswith='HC')|Q(MainSKU__startswith='HB'))
            elif status == 'CoolBag':
                qs = qs.filter(Q(MainSKU__startswith='BG'))
            elif status == 'BDDecor':
                qs = qs.filter(Q(MainSKU__startswith='Kids')|Q(MainSKU__startswith='SC')|Q(MainSKU__startswith='HT')|Q(MainSKU__startswith='BT')|Q(MainSKU__startswith='SW')|Q(MainSKU__startswith='BET')|Q(MainSKU__startswith='HDR')|Q(MainSKU__startswith='GSH')|Q(MainSKU__startswith='GS')|Q(MainSKU__startswith='SH')|Q(MainSKU__startswith='SK')|Q(MainSKU__startswith='K')|Q(MainSKU__startswith='BB')|Q(MainSKU__startswith='GLV'))
            elif status == 'Shine':
                qs = qs.filter(Q(MainSKU__startswith='BL')|Q(MainSKU__startswith='BRH')|Q(MainSKU__startswith='EAR')|Q(MainSKU__startswith='NL')|Q(MainSKU__startswith='PD')|Q(MainSKU__startswith='RG')|Q(MainSKU__startswith='JA')|Q(MainSKU__startswith='JR')|Q(MainSKU__startswith='FAC')|Q(MainSKU__startswith='Body')|Q(MainSKU__startswith='RING')|Q(MainSKU__startswith='GZSB'))
            elif status == 'Memo':
                qs = qs.filter(Q(MainSKU__startswith='WS')|Q(MainSKU__startswith='XMA')|Q(MainSKU__startswith='PY')|Q(MainSKU__startswith='WDS')|Q(MainSKU__startswith='COA')|Q(MainSKU__startswith='HG'))
            elif status == 'Liberty':
                qs = qs.filter(Q(MainSKU__startswith='W')|Q(MainSKU__startswith='Bra')|Q(MainSKU__startswith='GS')|Q(MainSKU__startswith='HT')).exclude(Q(MainSKU__startswith='WH')|Q(MainSKU__startswith='WF')|Q(MainSKU__startswith='WS'))
            elif status == 'Thunder':
                qs = qs.filter(Q(MainSKU__startswith='OSS')|Q(MainSKU__startswith='CYC')|Q(MainSKU__startswith='BI')|Q(MainSKU__startswith='SPT')|Q(MainSKU__startswith='FH'))
            
            elif status == 'Destiny':
                qs = qs.filter(Q(MainSKU__startswith='BL')|Q(MainSKU__startswith='BRH')|Q(MainSKU__startswith='ERA')|Q(MainSKU__startswith='NL')|Q(MainSKU__startswith='PD')|Q(MainSKU__startswith='RG')|Q(MainSKU__startswith='JA')|Q(MainSKU__startswith='JR')|Q(MainSKU__startswith='FAC')|Q(MainSKU__startswith='Body')|Q(MainSKU__startswith='RING'))
            elif status == 'Grace':
                qs = qs.filter(Q(MainSKU__startswith='BL')|Q(MainSKU__startswith='BRH')|Q(MainSKU__startswith='ERA')|Q(MainSKU__startswith='NL')|Q(MainSKU__startswith='PD')|Q(MainSKU__startswith='RG')|Q(MainSKU__startswith='JA')|Q(MainSKU__startswith='JR')|Q(MainSKU__startswith='FAC')|Q(MainSKU__startswith='Body')|Q(MainSKU__startswith='RING'))
            elif status == 'Cheirsh':
                qs = qs.filter(Q(MainSKU__startswith='BL')|Q(MainSKU__startswith='BRH')|Q(MainSKU__startswith='ERA')|Q(MainSKU__startswith='NL')|Q(MainSKU__startswith='PD')|Q(MainSKU__startswith='RG')|Q(MainSKU__startswith='JA')|Q(MainSKU__startswith='JR')|Q(MainSKU__startswith='FAC')|Q(MainSKU__startswith='Body')|Q(MainSKU__startswith='RING'))               
            elif status == 'Fire':
                qs = qs.filter(Q(MainSKU__startswith='HG')|Q(MainSKU__startswith='WS')|Q(MainSKU__startswith='PET')|Q(MainSKU__startswith='WF')|Q(MainSKU__startswith='CAR')|Q(MainSKU__startswith='TL')|Q(MainSKU__startswith='XMA')|Q(MainSKU__startswith='PY'))
            elif status == 'Cosy':
                qs = qs.filter(Q(MainSKU__startswith='HG')|Q(MainSKU__startswith='WS')|Q(MainSKU__startswith='PET')|Q(MainSKU__startswith='WF')|Q(MainSKU__startswith='CAR')|Q(MainSKU__startswith='TL')|Q(MainSKU__startswith='XMA')|Q(MainSKU__startswith='PY'))
            else:
                qs = qs
                

        return qs





    def to_excel1(self, request, queryset):
        from xlwt import *
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        #if not os.path.exists(path):
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s'%(MEDIA_ROOT + 'download_xls'))

        mkdir_p(path)
        os.popen('chmod 777 %s'%(path))

        w = Workbook()
        sheet = w.add_sheet('information_deal')
        
        sheet.write(0,0,u'ShopSKU')
        sheet.write(0,1,u'CostPrice')
        sheet.write(0,2,u'Weight')
        sheet.write(0,3,u'Parent Unique ID')
        sheet.write(0,4,u'Product Name')
        sheet.write(0,5,u'Description')
        sheet.write(0,6,u'Tags')
        sheet.write(0,7,u'Unique ID')
        sheet.write(0,8,u'Color')
        sheet.write(0,9,u'Size')
        sheet.write(0,10,u'Quantity')
        sheet.write(0,11,u'Price')
        sheet.write(0,12,u'MSRP')
        sheet.write(0,13,u'Shipping')
        sheet.write(0,14,u'Shipping Time(enter without " ",just the estimated days)')
        sheet.write(0,15,u'Product Main Image URL')
        sheet.write(0,16,u'Variant Main Image URL')
        sheet.write(0,17,u'Extra Image URL1')
        sheet.write(0,18,u'Extra Image URL2')
        sheet.write(0,19,u'Extra Image URL3')
        sheet.write(0,20,u'Extra Image URL4')
        sheet.write(0,21,u'Extra Image URL5')
        sheet.write(0,22,u'Extra Image URL6')
        sheet.write(0,23,u'Extra Image URL7')
        sheet.write(0,24,u'Extra Image URL8')
        sheet.write(0,25,u'Extra Image URL9')
        sheet.write(0,26,u'Extra Image URL10')

        logger = logging.getLogger('sourceDns.webdns.views')
        #写数据
        row = 0
        for qs in queryset:
            t_online_info_objs = t_online_info_publish_joom.objects.filter(ProductID=qs.ProductID,SKUStatus=0)#.distinct()
            #t_online_info_objs_ll = t_online_info.objects.filter(MainSKU__isnull=False,MainSKU = qs.MainSKU,Status='Enabled').values_list('ShopName','ProductID')
            #logger.error("t_online_info_objs_ll ======= %s"%(t_online_info_objs_ll))
            #logger.error("list(set(t_online_info_objs)) ======= %s"%(list(set(t_online_info_objs))))
            if t_online_info_objs.exists():
                for t_online_info_obj in t_online_info_objs:
                    row = row + 1
                    column = 0
                    sheet.write(row,column,t_online_info_obj.ShopSKU)
                    
                    column = column + 1
                    sheet.write(row,column,t_online_info_obj.CostPrice)
                    
                    column = column + 1
                    sheet.write(row,column,t_online_info_obj.Weight)
                    column = column + 1
                    sheet.write(row,column,t_online_info_obj.ParentSKU)

                    column = column + 1
                    sheet.write(row,column,t_online_info_obj.Title)

                    column = column + 1
                    sheet.write(row,column,t_online_info_obj.Description)

                    column = column + 1
                    sheet.write(row,column,t_online_info_obj.Tags)

                    column = column + 1
                    sheet.write(row,column,t_online_info_obj.SKU)

                    column = column + 1
                    sheet.write(row,column,t_online_info_obj.Color)

                    column = column + 1
                    sheet.write(row,column,t_online_info_obj.Size)

                    column = column + 1
                    sheet.write(row,column,t_online_info_obj.Quantity)

                    column = column + 1
                    sheet.write(row,column,t_online_info_obj.Price)

                    column = column + 1
                    sheet.write(row,column,t_online_info_obj.msrp)

                    column = column + 1
                    sheet.write(row,column,t_online_info_obj.Shipping)

                    column = column + 1
                    sheet.write(row,column,t_online_info_obj.ShippingTime)

                    column = column + 1
                    try:
                        pp = t_online_info_wait_publish_joom2.objects.filter(ProductID=t_online_info_obj.ProductID).values_list('Image',flat=True)[0]
                    except:
                        pp=''
                    sheet.write(row,column,pp)

                    column = column + 1
                    lis=t_online_info_obj.ExtraImages.split('|')
                    for i in range(0,len(lis)):
                        column = column + 1
                        sheet.write(row,column,lis[i])

                    t_online_info_wait_publish_joom2.objects.filter(ProductID=qs.ProductID).update(ispublished='已刊登')

        filename = request.user.username + '_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.xls'
        w.save(path + '/' +  filename)
        os.popen(r'chmod 777 %s'%(path + '/' +  filename))
        #queryset.update(DealStatus=Dealstatus_obj[0].V,DealStaffID=request.user.username,DealTime=datetime.now())

        #上传oss对象
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_XLS)
        bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)
        #删除现有的
        for  object_info in oss2.ObjectIterator(bucket,prefix='%s/%s_'%(request.user.username,request.user.username)):
            bucket.delete_object(object_info.key)
        bucket.put_object(u'%s/%s'%(request.user.username,filename),open(path + '/' +  filename))

        messages.error(request,u'%s%s.%s/%s/%s'%(PREFIX,BUCKETNAME_XLS,ENDPOINT_OUT,request.user.username,filename) + u':成功导出,可点击Download下载到本地~~~~~~' )
    to_excel1.short_description = u'导出正常状态的商品==>刊登处理'
    
    def to_excel2(self, request, queryset):
        from xlwt import *
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        #if not os.path.exists(path):
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s'%(MEDIA_ROOT + 'download_xls'))

        mkdir_p(path)
        os.popen('chmod 777 %s'%(path))

        w = Workbook()
        sheet = w.add_sheet('information_deal')
        
        sheet.write(0,0,u'ShopSKU')
        sheet.write(0,1,u'CostPrice')
        sheet.write(0,2,u'Weight')
        sheet.write(0,3,u'Parent Unique ID')
        sheet.write(0,4,u'Product Name')
        sheet.write(0,5,u'Description')
        sheet.write(0,6,u'Tags')
        sheet.write(0,7,u'Unique ID')
        sheet.write(0,8,u'Color')
        sheet.write(0,9,u'Size')
        sheet.write(0,10,u'Quantity')
        sheet.write(0,11,u'Price')
        sheet.write(0,12,u'MSRP')
        sheet.write(0,13,u'Shipping')
        sheet.write(0,14,u'Shipping Time(enter without " ",just the estimated days)')
        sheet.write(0,15,u'Product Main Image URL')
        sheet.write(0,16,u'Variant Main Image URL')
        sheet.write(0,17,u'Extra Image URL1')
        sheet.write(0,18,u'Extra Image URL2')
        sheet.write(0,19,u'Extra Image URL3')
        sheet.write(0,20,u'Extra Image URL4')
        sheet.write(0,21,u'Extra Image URL5')
        sheet.write(0,22,u'Extra Image URL6')
        sheet.write(0,23,u'Extra Image URL7')
        sheet.write(0,24,u'Extra Image URL8')
        sheet.write(0,25,u'Extra Image URL9')
        sheet.write(0,26,u'Extra Image URL10')


        logger = logging.getLogger('sourceDns.webdns.views')
        #写数据
        row = 0
        for qs in queryset:
            t_online_info_objs = t_online_info_publish_joom.objects.filter(ProductID=qs.ProductID,SKUStatus=1)#.distinct()
            #t_online_info_objs_ll = t_online_info.objects.filter(MainSKU__isnull=False,MainSKU = qs.MainSKU,Status='Enabled').values_list('ShopName','ProductID')
            #logger.error("t_online_info_objs_ll ======= %s"%(t_online_info_objs_ll))
            #logger.error("list(set(t_online_info_objs)) ======= %s"%(list(set(t_online_info_objs))))
            if t_online_info_objs.exists():
                for t_online_info_obj in t_online_info_objs:
                    row = row + 1
                    column = 0
                    sheet.write(row,column,t_online_info_obj.ShopSKU)
                    
                    column = column + 1
                    sheet.write(row,column,t_online_info_obj.CostPrice)
                    
                    column = column + 1
                    sheet.write(row,column,t_online_info_obj.Weight)
                    column = column + 1
                    sheet.write(row,column,t_online_info_obj.ParentSKU)

                    column = column + 1
                    sheet.write(row,column,t_online_info_obj.Title)

                    column = column + 1
                    sheet.write(row,column,t_online_info_obj.Description)

                    column = column + 1
                    sheet.write(row,column,t_online_info_obj.Tags)

                    column = column + 1
                    sheet.write(row,column,t_online_info_obj.SKU)

                    column = column + 1
                    sheet.write(row,column,t_online_info_obj.Color)

                    column = column + 1
                    sheet.write(row,column,t_online_info_obj.Size)

                    column = column + 1
                    sheet.write(row,column,t_online_info_obj.Quantity)

                    column = column + 1
                    sheet.write(row,column,t_online_info_obj.Price)

                    column = column + 1
                    sheet.write(row,column,t_online_info_obj.msrp)

                    column = column + 1
                    sheet.write(row,column,t_online_info_obj.Shipping)

                    column = column + 1
                    sheet.write(row,column,t_online_info_obj.ShippingTime)

                    column = column + 1
                    try:
                        pp = t_online_info_wait_publish_joom2.objects.filter(ProductID=t_online_info_obj.ProductID).values_list('Image',flat=True)[0]
                    except:
                        pp = ''
                    sheet.write(row,column,pp)

                    column = column + 1
                    lis=t_online_info_obj.ExtraImages.split('|')
                    for i in range(0,len(lis)):
                        column = column + 1
                        sheet.write(row,column,lis[i])

            t_online_info_publish_joom.objects.filter(ProductID=qs.ProductID,SKUStatus=1).update(ToExcel=0)

        filename = request.user.username + '_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.xls'
        w.save(path + '/' +  filename)
        os.popen(r'chmod 777 %s'%(path + '/' +  filename))
        #queryset.update(DealStatus=Dealstatus_obj[0].V,DealStaffID=request.user.username,DealTime=datetime.now())

        #上传oss对象
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_XLS)
        bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)
        #删除现有的
        for  object_info in oss2.ObjectIterator(bucket,prefix='%s/%s_'%(request.user.username,request.user.username)):
            bucket.delete_object(object_info.key)
        bucket.put_object(u'%s/%s'%(request.user.username,filename),open(path + '/' +  filename))

        messages.error(request,u'%s%s.%s/%s/%s'%(PREFIX,BUCKETNAME_XLS,ENDPOINT_OUT,request.user.username,filename) + u':成功导出,可点击Download下载到本地~~~~~~' )
    to_excel2.short_description = u'导出异常状态的商品==>下架处理'
















