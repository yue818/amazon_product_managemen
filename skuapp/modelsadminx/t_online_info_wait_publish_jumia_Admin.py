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
from skuapp.table.t_online_info_wait_publish_jumia import *
from skuapp.table.t_distribution_product_to_store_result import *
from skuapp.table.t_online_info_publish_joom import *
from Project.settings import *
from .t_product_Admin import *
from django.contrib import messages
from django.db.models import Q
from skuapp.table.t_online_info_joom_shopSKU import *
from pyapp.models import b_goods as py_b_goods
from pyapp.models import kc_currentstock
from datetime import datetime
from pyapp.models import b_goods as py_b_goods


class t_online_info_wait_publish_jumia_Admin(object):
    downloadxls = True
    import_flag = False
    jumia_flag = True

    def show_Picture(self,obj) :
        #url = u'https://contestimg.wish.com/api/webimage/%s-medium.jpg'%str(obj.ProductID)
        try:
            rt =  '<img src="%s"  width="120" height="120"/>  '%(obj.Image)
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
        #rt = "%s<br><br><br><br>"%(rt)
        #rt = "%s<a href='/Project/admin/skuapp/t_online_info_publish_joom/?_q_=%s'>编辑</a>"%(rt,obj.ProductID)
        return mark_safe(rt)

    show_orders7days.short_description = u'操作'

    #list_per_page=150
    list_display = ('id','show_Picture','show_ShopName_Seller','Orders7Days','OfSales','show_Title_ProductID','show_SKU_list','Status','show_time','show_orders7days')
    list_editable = ('show_Title')
    fields = ('id',)
    #list_filter = ('Seller','Orders7Days','RefreshTime','Status','ReviewState','DateUploaded','LastUpdated',)
    #readonly_fields = ('ProductID','ShopIP','ShopName','Quantity','Orders7Days','ParentSKU','SKU','ShopSKU')
    search_fields = ('id','PlatformName','ProductID','ShopIP','ShopName','Title','SKU','Orders7Days','Status','ReviewState','ParentSKU','Seller',)

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':5, 'cols':50})},
        }



    #actions = ('to_excel','INSERT_INTO_SCHEDULE1','INSERT_INTO_SCHEDULE2','INSERT_INTO_SCHEDULE3','INSERT_INTO_SCHEDULE4','INSERT_INTO_SCHEDULE5')
    actions = ('to_excel',)       

    def get_list_queryset(self,):
        request = self.request
        qs = super(t_online_info_wait_publish_jumia_Admin, self).get_list_queryset()
        status = request.GET.get('status')
        st = request.GET.get('st')
        
        if st == 'yy':
            qs = qs.filter(ispublished='已刊登')
        if st == 'nn':
            qs = qs.exclude(ispublished="已刊登")
            if status == 'HedongCloth':
                qs = qs.filter(MainSKU__startswith='M').exclude(Q(MainSKU__startswith='MU')|Q(MainSKU__startswith='MI'))
            elif status == 'bl':
                qs = qs.filter(Q(MainSKU__startswith='BDY')|Q(MainSKU__startswith='BL')|Q(MainSKU__startswith='BRH')|Q(MainSKU__startswith='CFL')|Q(MainSKU__startswith='EAR')|Q(MainSKU__startswith='FAN')|Q(MainSKU__startswith='JA')|Q(MainSKU__startswith='JR')|Q(MainSKU__startswith='KEY')|Q(MainSKU__startswith='NL')|Q(MainSKU__startswith='PD')|Q(MainSKU__startswith='RG'))
            elif status == 'Gadget':
                qs = qs.filter(Q(MainSKU__startswith='HG')|Q(MainSKU__startswith='WS')|Q(MainSKU__startswith='PET')|Q(MainSKU__startswith='WF')|Q(MainSKU__startswith='CAR')|Q(MainSKU__startswith='TL')|Q(MainSKU__startswith='XMA')|Q(MainSKU__startswith='PY'))
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
                qs = qs.filter(Q(MainSKU__startswith='WS')|Q(MainSKU__startswith='XMA')|Q(MainSKU__startswith='PY')|Q(MainSKU__startswith='WDS')|Q(MainSKU__startswith='COA'))
            elif status == 'Liberty':
                qs = qs.filter(Q(MainSKU__startswith='W')|Q(MainSKU__startswith='Bra')).exclude(Q(MainSKU__startswith='WH')|Q(MainSKU__startswith='WF')|Q(MainSKU__startswith='WS'))
            elif status == 'Thunder':
                qs = qs.filter(Q(MainSKU__startswith='OSS')|Q(MainSKU__startswith='CYC')|Q(MainSKU__startswith='BI')|Q(MainSKU__startswith='SPT')|Q(MainSKU__startswith='FH'))
            else:
                qs = qs
                

        return qs

    def to_excel(self, request, queryset):
        from datetime import datetime as datime
        from xlwt import *
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        #if not os.path.exists(path):
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s'%(MEDIA_ROOT + 'download_xls'))

        mkdir_p(path)
        os.popen('chmod 777 %s'%(path))

        w = Workbook()
        sheet = w.add_sheet('information_deal')
        
        sheet.write(0, 0, u'Unique ID')#SKU
        sheet.write(0, 1, u'普源图片')#附图        
        sheet.write(0, 2, u'CostPrice')#成本价
        sheet.write(0, 3, u'Weight')#重量
        sheet.write(0, 4, u'Product Unique ID') #Wish店铺主SKU
        sheet.write(0, 5, u'Variation Unique ID') #Wish店铺子SKU
        sheet.write(0, 6, u'Category') #类目(空)
        sheet.write(0, 7, u'SKU')#SKU(空)
        sheet.write(0, 8, u'group_id')#空
        sheet.write(0, 9, u'enable')#True
        sheet.write(0, 10, u'stock')#999
        sheet.write(0, 11, u'name')#标题
        sheet.write(0, 12, u'price')#空
        sheet.write(0, 13, u'old_price')#空
        sheet.write(0, 14, u'color')#颜色
        sheet.write(0, 15, u'size')#尺寸
        sheet.write(0, 16, u'weight')#重量(kg)
        sheet.write(0, 17, u'packaging_size')#空
        sheet.write(0, 18, u'brand')#空
        sheet.write(0, 19, u'tags')#标签
        sheet.write(0, 20, u'upc')#空
        sheet.write(0, 21, u'description')#描述       
        sheet.write(0, 22, u'description')#描述   
        sheet.write(0, 23, u'main_image_url')#主图
        sheet.write(0, 24, u'Extra_Image_URL_1')#附图1
        sheet.write(0, 25, u'Extra_Image_URL_2')#2
        sheet.write(0, 26, u'Extra_Image_URL_3')#3
        sheet.write(0, 27, u'Extra_Image_URL_4')#4
        sheet.write(0, 28, u'Extra_Image_URL_5')#5
        sheet.write(0, 29, u'Extra_Image_URL_6')#6
        sheet.write(0, 30, u'Extra_Image_URL_7')#7
        sheet.write(0, 31, u'Extra_Image_URL_8')#8
        sheet.write(0, 32, u'Extra_Image_URL_9')#9
        sheet.write(0, 33, u'Extra_Image_URL_10')#10
        sheet.write(0, 34, u'shipping_template_id')#主图
        sheet.write(0, 35, u'shipping_time')#附图 
        sheet.write(0, 36, u'langing_page_url')#附图
        


        #写数据
        row = 0
        for qs in queryset:
            t_online_info_objs = t_online_info_publish_joom.objects.filter(ProductID=qs.ProductID,SKUStatus=0)#.distinct()
            info_objs = t_online_info_objs.values('SKU','CostPrice','Weight','ParentSKU','ShopSKU','Title','Color','Size','Tags','Description','ExtraImages')
            for t_online_info_obj in info_objs:
                row = row + 1
                column = 0
                sheet.write(row,column,t_online_info_obj['SKU'])
                
                try:
                    BmpUrl = py_b_goods.objects.get(SKU=t_online_info_obj['SKU']).BmpUrl
                except:
                    BmpUrl = ''
                column = column + 1
                sheet.write(row,column,BmpUrl)
                                    
                column = column + 1
                sheet.write(row,column,t_online_info_obj['CostPrice'])
                    
                column = column + 1
                sheet.write(row,column,t_online_info_obj['Weight'])

                column = column + 1
                sheet.write(row,column,t_online_info_obj['ParentSKU'])

                column = column + 1
                sheet.write(row,column,t_online_info_obj['ShopSKU'])
                
                column = column + 1
                sheet.write(row,column,'')
                
                column = column + 1
                sheet.write(row,column,'')
                
                column = column + 1
                sheet.write(row,column,'')

                column = column + 1
                sheet.write(row,column,'True')

                column = column + 1
                sheet.write(row,column,'999')

                column = column + 1
                sheet.write(row,column,t_online_info_obj['Title'])
                
                column = column + 1
                sheet.write(row,column,'')
                
                column = column + 1
                sheet.write(row,column,'')

                column = column + 1
                sheet.write(row,column,t_online_info_obj['Color'])

                column = column + 1
                sheet.write(row,column,t_online_info_obj['Size'])

                column = column + 1
                try:
                    weight = float(t_online_info_obj['Weight'])/1000
                    new_weight = round(weight,2)
                except:
                    new_weight = ''
                sheet.write(row,column,new_weight)

                column = column + 1
                sheet.write(row,column,'')
                    
                column = column + 1
                sheet.write(row,column,'')

                column = column + 1
                sheet.write(row,column,t_online_info_obj['Tags'])

                column = column + 1
                sheet.write(row,column,'')

                column = column + 1
                sheet.write(row,column,'<ul><li>' + t_online_info_obj['Description'].replace('\n','</li><li>')  + '</li></ul>')
                
                column = column + 1
                sheet.write(row,column,t_online_info_obj['Description'])

                column = column + 1
                sheet.write(row,column,qs.Image)

                lis=t_online_info_obj['ExtraImages'].split('|')
                n = 0
                for i in range(0,len(lis)):
                    column = column + 1
                    sheet.write(row,column,lis[i])
                    n+=1
                    if n == 10:
                        continue
                        
                column = column + 1
                sheet.write(row,column,'')
                
                column = column + 1
                sheet.write(row,column,'')
                
                column = column + 1
                sheet.write(row,column,'')
            t_online_info_wait_publish_jumia.objects.filter(ProductID=qs.ProductID).update(ispublished='已刊登')

        filename = request.user.username + '_' + datime.now().strftime('%Y%m%d%H%M%S') + '.xls'
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
















