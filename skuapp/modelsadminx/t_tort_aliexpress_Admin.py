# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from Project.settings import *
from pyapp.models import b_goodsskulinkshop
import oss2
from skuapp.table.t_online_info import t_online_info
from .t_product_Admin import *
from skuapp.table.t_tort_aliexpress import t_tort_aliexpress
from skuapp.table.t_sys_param import t_sys_param
from skuapp.table.t_store_configuration_file import t_store_configuration_file
from skuapp.table.t_product_mainsku_sku import t_product_mainsku_sku
from pyapp.models import b_goods
from brick.classredis.classmainsku import classmainsku
from django.db import connection
from django_redis import get_redis_connection
from django.contrib import messages
from datetime import datetime

Dealstatus_obj=t_sys_param.objects.filter(Type=46,Seq=1)
class t_tort_aliexpress_Admin(object):
    show_tort = True
    downloadxls = True
    def show_ProductPicUrl(self,obj) :
        url =u'%s%s.%s/%s/%s/%s'%(PREFIX,BUCKETNAME_TORT,ENDPOINT_OUT,'aliexpress',obj.id,str(obj.ProductPicUrl))
        rt =  '<img src="%s"  width="150" height="150"  alt = "%s"  title="%s"  />  '%(url,url,url)
        return mark_safe(rt)
    show_ProductPicUrl.short_description = u'产品图片'

    def show_shop_id(self,obj) :
        rt =  "<a id=show_list_%s>店铺名称和产品ID</a><script>$('#show_list_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'查看全部',fix:false,shadeClose: true,maxmin:true,area:['600px','600px'],content:'/t_tort_aliexpress/aliexpress_info/?SKU=%s',});});</script>"%(obj.id,obj.id,obj.MainSKU)
        return mark_safe(rt)
    show_shop_id.short_description = u'查看信息'
    
    def show_AttachmentUrls(self,obj) :
        rt=''
        attachmentUrl1="";
        attachmentUrl2="";
        attachmentUrl3="";
        attachmentUrl4="";
        attachmentUrl5="";
        attachmentUrl6="";
        if obj.AttachmentUrl1 is not None and str(obj.AttachmentUrl1).strip() !='' :
            attachmentUrl1 =  u'%s%s.%s/%s/%s/%s'%(PREFIX,BUCKETNAME_TORT,ENDPOINT_OUT,'aliexpress',obj.id,str(obj.AttachmentUrl1))
            rt="%s附件一:<a href=%s>%s</a>;<br>"%(rt,attachmentUrl1,attachmentUrl1)
        if obj.AttachmentUrl2 is not None and str(obj.AttachmentUrl2).strip() !='' :
            attachmentUrl2 =  u'%s%s.%s/%s/%s/%s'%(PREFIX,BUCKETNAME_TORT,ENDPOINT_OUT,'aliexpress',obj.id,str(obj.AttachmentUrl2))
            rt="%s附件一:<a href=%s>%s</a>;<br>"%(rt,attachmentUrl2,attachmentUrl2)
        if obj.AttachmentUrl3 is not None and str(obj.AttachmentUrl3).strip() !='' :
            attachmentUrl3 =  u'%s%s.%s/%s/%s/%s'%(PREFIX,BUCKETNAME_TORT,ENDPOINT_OUT,'aliexpress',obj.id,str(obj.AttachmentUrl3))
            rt="%s附件一:<a href=%s>%s</a>;<br>"%(rt,attachmentUrl3,attachmentUrl3)
        if obj.AttachmentUrl4 is not None and str(obj.AttachmentUrl4).strip() !='' :
            attachmentUrl4 =  u'%s%s.%s/%s/%s/%s'%(PREFIX,BUCKETNAME_TORT,ENDPOINT_OUT,'aliexpress',obj.id,str(obj.AttachmentUrl4))
            rt="%s附件一:<a href=%s>%s</a>;<br>"%(rt,attachmentUrl4,attachmentUrl4)
        if obj.AttachmentUrl5 is not None and str(obj.AttachmentUrl5).strip() !='' :
            attachmentUrl5 =  u'%s%s.%s/%s/%s/%s'%(PREFIX,BUCKETNAME_TORT,ENDPOINT_OUT,'aliexpress',obj.id,str(obj.AttachmentUrl5))
            rt="%s附件一:<a href=%s>%s</a>;<br>"%(rt,attachmentUrl5,attachmentUrl5)
        if obj.AttachmentUrl6 is not None and str(obj.AttachmentUrl6).strip() !='' :
            attachmentUrl6 =  u'%s%s.%s/%s/%s/%s'%(PREFIX,BUCKETNAME_TORT,ENDPOINT_OUT,'aliexpress',obj.id,str(obj.AttachmentUrl6))
            rt="%s附件一:<a href=%s>%s</a>;<br>"%(rt,attachmentUrl6,attachmentUrl6)

        #rt =  "附件一:<a href=%s>%s</a>;<br>附件二:<a href=%s>%s</a><br>附件三:<a href=%s>%s</a><br>附件四:<a href=%s>%s</a><br>附件五:<a href=%s>%s</a><br>附件六:<a href=%s>%s</a>;"%(attachmentUrl1,attachmentUrl1,attachmentUrl2,attachmentUrl2,attachmentUrl3,attachmentUrl3,attachmentUrl4,attachmentUrl4,attachmentUrl5,attachmentUrl5,attachmentUrl6,attachmentUrl6)
        return mark_safe(rt)
    show_AttachmentUrls.short_description = u'附件'

    actions=['to_excel','to_excel_tort',]
    list_display=('id','show_ProductPicUrl','show_Deal_Info','Remark','Site','AccountStaffID','Account','StaffID','UpdateTime','SKU','ProductID','ListingTitle','ProductTitle','ComplainReason','ScoreDeducting',
                        'Complainant','Intellectual','IntellectualCode','Trademark','ContactWay','ComplainID','AcceptTime',
                        'show_AttachmentUrls','SalerName2','Purchaser'
                        )
    readonly_fields = ('id',)
    list_display_links = ('id',)

    search_fields=('id','Site','Account','AccountStaffID','StaffID','SKU','ProductID','ProductTitle','ComplainReason','Remark','ScoreDeducting',
                        'Complainant','Intellectual','IntellectualCode','Trademark','ContactWay','ComplainID',
                        'Describe','EmailTest','ListingTitle','DealStatus','SalerName2','Purchaser'  )

    list_filter = ('DealStatus','UpdateTime','Intellectual','AcceptTime','Site','SalerName2','Purchaser','OperationState',)

    list_editable=('Account','StaffID','SKU','ProductID','ProductTitle','ScoreDeducting','Remark',
                    'Intellectual','IntellectualCode','ComplainReason','Complainant','Trademark','Site',
                    'ContactWay','ComplainID','AcceptTime','AccountStaffID','ListingTitle',
                    )
    show_detail_fields = ['id']
    fields =  ('Account','StaffID','SKU','ProductID','ProductTitle','ScoreDeducting','ProductPicUrl','Remark',
                'Intellectual','IntellectualCode','ComplainReason','Complainant','Trademark',
                'ContactWay','ComplainID','AcceptTime','Site','Describe','EmailTest',
                'AttachmentUrl1','AttachmentUrl2','AttachmentUrl3','AccountStaffID','ListingTitle',
                'AttachmentUrl4','AttachmentUrl5','AttachmentUrl6',
                )
    form_layout = (
        Fieldset(u'我方信息',
                       Row('Site','Account',),
                       Row('AccountStaffID', 'SKU','ProductID'),
                       Row('ListingTitle','ProductTitle', ),
                       Row('ScoreDeducting','ProductPicUrl',),
                       Row( 'Remark'),
                       css_class = 'unsort '
                ),
        Fieldset(u'对方信息',
                       Row( 'Intellectual'),
                       Row( 'Trademark','AcceptTime',),
                       Row( 'ComplainReason','Complainant',),
                       Row( 'ComplainID','IntellectualCode',),
                       Row( 'ContactWay',),
                       Row( 'AttachmentUrl1','AttachmentUrl2'),
                       Row( 'AttachmentUrl3','AttachmentUrl4'),
                       Row( 'AttachmentUrl5','AttachmentUrl6'),
                       Row( 'Describe',),
                       Row( 'EmailTest',),
                       css_class = 'unsort  '
                )
                  )
    def getMainSKU(self,sku):
        v_Tmp = ''
        V_SZ = 0
        v_break = 0
        V_ZM =0
        for v in sku:
            if v_break < 0 :
                break
            if v >='0' and v <='9' :
                v_Tmp = v_Tmp + v
                V_SZ += 1
            else:
                V_ZM  +=1 
                if V_SZ > 0 :
                    v_break = -1
                else:
                    v_Tmp = v_Tmp +v
        return  v_Tmp
    
     

    def save_models(self):
        from brick.public.update_wish_tort_status import update_wish_tort_status

        obj = self.new_obj
        request = self.request
        obj.StaffID = request.user.username
        obj.MainSKU = self.getMainSKU(obj.SKU)
        b_goods_obj=b_goods.objects.filter(SKU__icontains=obj.MainSKU).values_list('SalerName2','Purchaser').order_by('SKU')[0]
        obj.SalerName2=b_goods_obj[0]
        obj.Purchaser=b_goods_obj[1]
        obj.OperationState = 'No'

        if obj.Site is not None and obj.Site.strip() != '':
            # redis  侵权
            #redis_conn = get_redis_connection(alias='product')
            #classmainsku_obj = classmainsku(connection,redis_conn)
            #tortsite = classmainsku_obj.get_tort_by_mainsku(obj.MainSKU)
            #if tortsite and obj.site not in tortsite:
             #   tortsite.append(obj.site)
             #   classmainsku_obj.set_tort_by_mainsku(obj.MainSKU,'|'.join(tortsite))

            obj.save()
            auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
            bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_TORT)
            try:
                if obj.ProductPicUrl is not None and str(obj.ProductPicUrl).strip() !='' :
                    bucket.put_object(u'%s/%s/%s'%('aliexpress',obj.id,str(obj.ProductPicUrl)),obj.ProductPicUrl)

                if obj.AttachmentUrl1 is not None and str(obj.AttachmentUrl1).strip() !='' :
                    bucket.put_object(u'%s/%s/%s'%('aliexpress',obj.id,str(obj.AttachmentUrl1)),obj.AttachmentUrl1)

                if obj.AttachmentUrl2 is not None and str(obj.AttachmentUrl2).strip() !='' :
                    bucket.put_object(u'%s/%s/%s'%('aliexpress',obj.id,str(obj.AttachmentUrl2)),obj.AttachmentUrl2)

                if obj.AttachmentUrl3 is not None and str(obj.AttachmentUrl3).strip() !='' :
                    bucket.put_object(u'%s/%s/%s'%('aliexpress',obj.id,str(obj.AttachmentUrl3)),obj.AttachmentUrl3)

                if obj.AttachmentUrl4 is not None and str(obj.AttachmentUrl4).strip() !='' :
                    bucket.put_object(u'%s/%s/%s'%('aliexpress',obj.id,str(obj.AttachmentUrl4)),obj.AttachmentUrl4)

                if obj.AttachmentUrl5 is not None and str(obj.AttachmentUrl5).strip() !='' :
                    bucket.put_object(u'%s/%s/%s'%('aliexpress',obj.id,str(obj.AttachmentUrl5)),obj.AttachmentUrl5)

                if obj.AttachmentUrl6 is not None and str(obj.AttachmentUrl6).strip() !='' :
                    bucket.put_object(u'%s/%s/%s'%('aliexpress',obj.id,str(obj.AttachmentUrl6)),obj.AttachmentUrl6)
            except:
                pass
            #obj.save()
            update_wish_tort_status(obj.Site, obj.MainSKU, connection)
        else:
            messages.error(request,u'没有填写 侵权站点，请重新填写并提交。。。')
    
    def show_Deal_Info(self,obj) :
        rt=''
        ds=''
        if obj.DealStatus==Dealstatus_obj[0].V:
            ds=Dealstatus_obj[0].VDesc
            rt = u'%s处理人员:<br>%s <br>处理时间:<br>%s <br>处理状态:<br>%s'%(rt,obj.DealStaffID,obj.DealTime,ds)
        else:
            rt = u'%s处理人员:<br>%s <br>处理时间:<br>%s <br>处理状态:<br>%s'%(rt,obj.DealStaffID,obj.DealTime,obj.DealStatus)
        return mark_safe(rt)
    show_Deal_Info.short_description = u'处理结果'
    
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

        sheet.write(0,0,u'店铺名称')
        sheet.write(0,1,u'销售员')
        sheet.write(0,2,u'产品ID')
        logger = logging.getLogger('sourceDns.webdns.views')
        #写数据
        row = 0
        for qs in queryset:
            t_online_info_objs = t_online_info.objects.filter(MainSKU__isnull=False,MainSKU = qs.MainSKU,Status='Enabled').values_list('ShopName','ProductID')#.distinct()
            t_online_info_objs_ll = t_online_info.objects.filter(MainSKU__isnull=False,MainSKU = qs.MainSKU,Status='Enabled').values_list('ShopName','ProductID')
            logger.error("t_online_info_objs_ll ======= %s"%(t_online_info_objs_ll))
            logger.error("list(set(t_online_info_objs)) ======= %s"%(list(set(t_online_info_objs))))
            if t_online_info_objs.exists():
                for t_online_info_obj in list(set(t_online_info_objs)):
                    shopname=t_online_info_obj[0]
                    t_store_configuration_file_objs=t_store_configuration_file.objects.filter(ShopName__contains=shopname)
                    if t_store_configuration_file_objs.exists():
                        row = row + 1
                        column = 0
                        sheet.write(row,column,t_online_info_obj[0])

                        column = column + 1
                        sheet.write(row,column,t_store_configuration_file_objs[0].Seller)

                        column = column + 1
                        sheet.write(row,column,t_online_info_obj[1])

            else:
                t_online_info_objs = t_online_info.objects.filter(MainSKU__isnull=True,ParentSKU = qs.MainSKU,Status='Enabled').values_list('ShopName','ProductID')
                for t_online_info_obj in list(set(t_online_info_objs)):
                    shopname=t_online_info_obj[0]
                    t_store_configuration_file_objs=t_store_configuration_file.objects.filter(ShopName__contains=shopname)
                    if t_store_configuration_file_objs.exists():
                        row = row + 1
                        column = 0
                        sheet.write(row,column,t_online_info_obj[0])

                        column = column + 1
                        sheet.write(row,column,t_store_configuration_file_objs[0].Seller)

                        column = column + 1
                        sheet.write(row,column,t_online_info_obj[1])
                
        filename = request.user.username + '_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.xls'
        w.save(path + '/' +  filename)
        os.popen(r'chmod 777 %s'%(path + '/' +  filename))
        queryset.update(DealStatus=Dealstatus_obj[0].V,DealStaffID=request.user.username,DealTime=datetime.now())
        
        #上传oss对象
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_XLS)
        bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)
        #删除现有的
        for  object_info in oss2.ObjectIterator(bucket,prefix='%s/%s_'%(request.user.username,request.user.username)):
            bucket.delete_object(object_info.key)
        bucket.put_object(u'%s/%s'%(request.user.username,filename),open(path + '/' +  filename))

        messages.error(request,u'%s%s.%s/%s/%s'%(PREFIX,BUCKETNAME_XLS,ENDPOINT_OUT,request.user.username,filename) + u':成功导出,可点击Download下载到本地............................。' )
    to_excel.short_description = u'导出处理'
    
    
    def to_excel_tort(self, request, queryset):
        from xlwt import *
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        #if not os.path.exists(path):
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s'%(MEDIA_ROOT + 'download_xls'))

        mkdir_p(path)
        os.popen('chmod 777 %s'%(path))

        w = Workbook()
        sheet = w.add_sheet(u'改侵权')

        sheet.write(0,0,u'SKU')
        sheet.write(0,1,u'网页URL6')
        sheet.write(0,2,u'停售')
        sheet.write(0,3,u'网页URL3')

        #写数据
        row = 0
        id_list = []
        for qs in queryset:
            remarkslist = []
            Sitelist = []
            t_tort_aliexpress_objs = t_tort_aliexpress.objects.filter(MainSKU=qs.MainSKU).values_list('Site','ComplainReason')
            for t_tort_aliexpress_obj in t_tort_aliexpress_objs:
                Sitelist.append('%s'%t_tort_aliexpress_obj[0])
                remarkslist.append('%s'%t_tort_aliexpress_obj[1])
                
            t_product_mainsku_sku_objs = t_product_mainsku_sku.objects.filter(MainSKU=qs.MainSKU)
            for t_product_mainsku_sku_obj in t_product_mainsku_sku_objs:
                if t_product_mainsku_sku_obj.ProductSKU is not None and t_product_mainsku_sku_obj.ProductSKU.strip() != '':
                    row = row + 1
                    column = 0
                    sheet.write(row,column,t_product_mainsku_sku_obj.ProductSKU) #商品SKU

                    column = column + 1
                    sheet.write(row,column,';'.join(set(Sitelist))) #站点

                    column = column + 1
                    sheet.write(row,column,'not edit') #停售

                    column = column + 1
                    sheet.write(row,column,';'.join(set(remarkslist))) #备注
                else:
                    messages.error(request,'该ID:%s没有查到商品SKU'%qs.id)
            id_list.append(qs.id)
            if row > 5000:
                break
            
        filename = request.user.username + '_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.xls'
        w.save(path + '/' +  filename)
        os.popen(r'chmod 777 %s'%(path + '/' +  filename))

        #上传oss对象
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_XLS)
        bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)
        
        queryset.filter(id__in=id_list).update(OperationState = 'Yes')
        #删除现有的
        for  object_info in oss2.ObjectIterator(bucket,prefix='%s/%s_'%(request.user.username,request.user.username)):
            bucket.delete_object(object_info.key)
        bucket.put_object(u'%s/%s'%(request.user.username,filename),open(path + '/' +  filename))

        messages.error(request,u'%s%s.%s/%s/%s'%(PREFIX,BUCKETNAME_XLS,ENDPOINT_OUT,request.user.username,filename) + u':成功导出,可点击Download下载到本地............................。' )
    to_excel_tort.short_description = u'导出EXCEL(侵权)'