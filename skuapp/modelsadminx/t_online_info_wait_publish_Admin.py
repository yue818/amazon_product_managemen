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
from datetime import datetime
from skuapp.table.t_online_info_wait_publish import *
from skuapp.table.t_distribution_product_to_store_result import *
from skuapp.table.t_online_info_publish_joom import *
from Project.settings import *
from .t_product_Admin import *


class t_online_info_wait_publish_Admin(object):
    downloadxls = True

    def show_Picture(self,obj) :
        url = u'https://contestimg.wish.com/api/webimage/%s-medium.jpg'%str(obj.ProductID)
        rt =  '<img src="%s"  width="120" height="120"  alt = "%s"  title="%s"  />  '%(url,url,url)
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
            rt = u'%s标题:<br>%s产品ID:<br><a href=" https://www.wish.com/c/%s" target="_blank">%s</a>'%(rt,ll,obj.ProductID,obj.ProductID)
        return mark_safe(rt)
    show_Title_ProductID.short_description = u'标题/产品ID'


    
    def show_time(self,obj) :
        rt=''
        rt = u'%s刷新时间:<br>%s <br>上架时间:<br>%s <br>最近更新时间:<br>%s'%(rt,obj.RefreshTime,obj.DateUploaded,obj.LastUpdated)
        return mark_safe(rt)
    show_time.short_description = u'时间'
    
    def show_SKU_list(self,obj) :
        rt='<table   style="text-align:center;" border="1" cellpadding="3" cellspacing="1" bgcolor="#c1c1c1"><tr bgcolor="#C00"><th style="text-align:center">子SKU</th><th style="text-align:center">店铺SKU</th><th style="text-align:center">库存量</th><th style="text-align:center">价格</th></tr>'
        t_online_info_wish_objs = t_online_info_publish_joom.objects.values('SKU','ShopSKU','Quantity','Price').filter(ProductID=obj.ProductID).distinct()
        i = 0
        for t_online_info_wish_obj in t_online_info_wish_objs:
            if i < 5:
                rt = '%s <tr bgcolor="#FFFFFF"><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr> '%(rt,t_online_info_wish_obj['SKU'],t_online_info_wish_obj['ShopSKU'],t_online_info_wish_obj['Quantity'],t_online_info_wish_obj['Price'])
                i = i + 1
        if len(t_online_info_wish_objs)>5:
            rt = '%s<tr><td><a id="link_id_%s">查看更多</a></td></tr>'%(rt,obj.id)
        else:
            rt = rt
        rt = "%s</table><script>$('#link_id_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'查看全部',fix:false,shadeClose: true,maxmin:true,area:['500px','500px'],content:'/t_online_info_wish/SKU/?abc=%s',});});</script>"%(rt,obj.id,obj.ProductID)
        return mark_safe(rt)
    show_SKU_list.short_description = mark_safe('<p align="center"> 子SKU</p>')
    
    def show_orders7days(self,obj) :

        rt =  "<a id=show_orderlist_%s>日销量</a><script>$('#show_orderlist_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'查看全部',fix:false,shadeClose: true,maxmin:true,area:['1000px','600px'],content:'/t_online_info_wish/order1day/?aID=%s',});});</script>"%(obj.id,obj.id,obj.ProductID)
        rt = "%s<br><br><br><br>"%(rt)
        rt = "%s<a href='/Project/admin/skuapp/t_online_info_publish_joom/?_q_=%s'>编辑</a>"%(rt,obj.ProductID)
        return mark_safe(rt)
        
    show_orders7days.short_description = u'操作'
    
    list_display = ('id','show_Picture','show_ShopName_Seller','Orders7Days','OfSales','show_Title_ProductID','show_SKU_list','Status','show_time','show_orders7days')
    list_editable = ('show_Title')
    fields = ('id',)
    list_filter = ('Seller','Orders7Days','RefreshTime','Status','ReviewState','DateUploaded','LastUpdated',)
    #readonly_fields = ('ProductID','ShopIP','ShopName','Quantity','Orders7Days','ParentSKU','SKU','ShopSKU')
    search_fields = ('id','PlatformName','ProductID','ShopIP','ShopName','Title','SKU','Orders7Days','Status','ReviewState','ParentSKU','Seller',)
    
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':5, 'cols':50})},
        }



    #actions = ('to_excel','INSERT_INTO_SCHEDULE1','INSERT_INTO_SCHEDULE2','INSERT_INTO_SCHEDULE3','INSERT_INTO_SCHEDULE4','INSERT_INTO_SCHEDULE5')
    actions = ('to_excel',)
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
    
    def get_list_queryset(self):
        request = self.request
        qs = super(t_online_info_wait_publish_Admin, self).get_list_queryset()
        return qs.exclude(ispublished=u'已刊登')
    
    def to_excel(self, request, queryset):
        from xlwt import *
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        #if not os.path.exists(path):
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s'%(MEDIA_ROOT + 'download_xls'))

        mkdir_p(path)
        os.popen('chmod 777 %s'%(path))

        w = Workbook()
        sheet = w.add_sheet('information_deal')

        sheet.write(0,0,u'Parent Unique ID')
        sheet.write(0,1,u'Product Name')
        sheet.write(0,2,u'Description')
        sheet.write(0,3,u'Tags')
        sheet.write(0,4,u'Unique ID')
        sheet.write(0,5,u'Color')
        sheet.write(0,6,u'Size')
        sheet.write(0,7,u'Quantity')
        sheet.write(0,8,u'Price')      
        sheet.write(0,9,u'MSRP')
        sheet.write(0,10,u'Shipping')
        sheet.write(0,11,u'Shipping Time(enter without " ",just the estimated days)')
        sheet.write(0,12,u'Product Main Image URL')
        sheet.write(0,13,u'Variant Main Image URL')
        sheet.write(0,14,u'Extra Image URL')

        logger = logging.getLogger('sourceDns.webdns.views')
        #写数据
        row = 0
        for qs in queryset:
            t_online_info_objs = t_online_info_publish_joom.objects.filter(ProductID=qs.ProductID)#.distinct()
            #t_online_info_objs_ll = t_online_info.objects.filter(MainSKU__isnull=False,MainSKU = qs.MainSKU,Status='Enabled').values_list('ShopName','ProductID')
            #logger.error("t_online_info_objs_ll ======= %s"%(t_online_info_objs_ll))
            #logger.error("list(set(t_online_info_objs)) ======= %s"%(list(set(t_online_info_objs))))
            if t_online_info_objs.exists():
                for t_online_info_obj in t_online_info_objs:
                    row = row + 1
                    column = 0
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
                    sheet.write(row,column,t_online_info_obj.Image)
                        
                    column = column + 1
                    lis=t_online_info_obj.ExtraImages.split('|')
                    for i in range(0,len(lis)):
                        column = column + 1
                        sheet.write(row,column,lis[i])
                    
                    t_online_info_wait_publish.objects.filter(ProductID=qs.ProductID).update(ispublished='已刊登')
                
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
    to_excel.short_description = u'导出Excel处理'
    

  
 
 
 
 
 
 
 
 
 
 
 
    