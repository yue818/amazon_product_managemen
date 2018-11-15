# -*- coding: utf-8 -*-
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field

#from skuapp.table.t_online_info_wish import t_online_info_wish
#from skuapp.table.t_sys_department_staff import t_sys_department_staff
#from skuapp.table.t_store_status import t_store_status
  
#import logging
#from django.contrib import messages
from django.contrib.auth.models import *
from skuapp.table.t_config_user_buyer_task import *
from skuapp.table.t_store_marketplan_execution_log import *
from django.utils.safestring import mark_safe
from skuapp.table.t_config_user_buyer import *
from Project.settings import *
from .t_product_Admin import * 
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from datetime import datetime

class t_store_marketplan_execution_log_Admin(object):

    search_box_flag = True

    downloadxls = True

    def get_list_queryset(self):
        request = self.request
        qs = super(t_store_marketplan_execution_log_Admin, self).get_list_queryset()
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(StaffId=request.user.username)
            
    def show_person(self,obj):     
        FirstName_objs = t_config_user_buyer_task.objects.get(StaffId=obj.StaffId)
        return FirstName_objs.FirstName
    show_person.short_description=u'中文名'
    
    def show_picture(self,obj):
        return mark_safe(u'<img style="width:90px;height:90px" src=%s/>'%(obj.PicURL))
    show_picture.short_description=u'产品图片'

    def show_userid(self,obj):
        try:
            user_id_objs = t_config_user_buyer.objects.filter(BuyerAccount=obj.BuyerAccount.strip(),StaffId=obj.StaffId)[0]
            return user_id_objs.UserID
        except:
            return ''
    show_userid.short_description=u'UserID'
    
    def show_PaypalAccount(self,obj):
        try:     
            PaypalAccount_objs = t_config_user_buyer.objects.filter(BuyerAccount=obj.BuyerAccount.strip(),StaffId=obj.StaffId)[0]
            return PaypalAccount_objs.PaypalAccount
        except:
            return ''
    show_PaypalAccount.short_description=u'卡号'        
    
    actions = ('to_excel',)    
    list_display =('id','show_picture','BuyerAccount','show_userid','ProductID','show_PaypalAccount','Status','Exetime','ShopName','ShopSKU','StaffId','show_person','Price','Price2','Result','Remark')
#    search_fields = ('id','BuyerAccount','ProductID','Status','Exetime','ShopName','ShopSKU','StaffId','Price','Price2','Result','Remark')
    list_filter =('id','BuyerAccount','ProductID','Status','Exetime','ShopName','ShopSKU','StaffId','Price','Price2','Result','Remark')
    list_display_links = ('id')
    list_editable = ('Price2','Remark')            
    #readonly_fields = ('id','PicURL','BuyerAccount','ProductID','Status','Exetime','ShopName','ShopSKU','StaffId','Price','Price2','Result','Pid')
    search_fields =None

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
        
        sheet.write(0,0,u'执行时间')
        sheet.write(0,1,u'营销人')
        sheet.write(0,2,u'买家账号')
        sheet.write(0,3,u'产品ID')
        sheet.write(0,4,u'卖家简称')
        sheet.write(0,5,u'UserID')
        sheet.write(0,6,u'店铺SKU')
        sheet.write(0,7,u'商品价格')
        sheet.write(0,8,u'实际刷单金额')
        sheet.write(0,9,u'执行结果')
        sheet.write(0,10,u'卡号')
        sheet.write(0,11,u'营销备注')

        logger = logging.getLogger('sourceDns.webdns.views')
        #写数据
        row = 0
        for qs in queryset:
            row = row + 1
            column = 0
            sheet.write(row,column,qs.Exetime.strftime('%Y-%m-%d'))
                    
            column = column + 1
            sheet.write(row,column,qs.StaffId)
                    
            column = column + 1
            sheet.write(row,column,qs.BuyerAccount)
            column = column + 1
            sheet.write(row,column,qs.ProductID)

            column = column + 1
            sheet.write(row,column,qs.ShopName)

            column = column + 1
            try:
                aa=t_config_user_buyer.objects.filter(BuyerAccount=qs.BuyerAccount.strip(),StaffId=qs.StaffId)[0].UserID
                sheet.write(row,column,aa)
            except:
                sheet.write(row,column,'')

            column = column + 1
            sheet.write(row,column,qs.ShopSKU)

            column = column + 1
            sheet.write(row,column,qs.Price)

            column = column + 1
            sheet.write(row,column,qs.Price2)

            column = column + 1
            sheet.write(row,column,qs.Result)

            column = column + 1
            try:
                bb=t_config_user_buyer.objects.filter(BuyerAccount=qs.BuyerAccount.strip(),StaffId=qs.StaffId)[0].PaypalAccount
                sheet.write(row,column,bb)
            except:
                sheet.write(row,column,'')

            column = column + 1
            sheet.write(row,column,qs.Remark)

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
    to_excel.short_description = u'导出Excel截单处理'
 
        
    def get_list_queryset(self, ):
        request = self.request
        qs = super(t_store_marketplan_execution_log_Admin, self).get_list_queryset()
        id = request.GET.get('ID', '')
        buyerAccount = request.GET.get('BuyerAccount', '')
        productID = request.GET.get('ProductID', '')
        status = request.GET.get('Status', '')
        exetimeStart = request.GET.get('ExetimeStart', '')
        exetimeEnd = request.GET.get('ExetimeEnd', '')
        shopName = request.GET.get('ShopName', '')
        shopSKU = request.GET.get('ShopSKU', '')
        staffId = request.GET.get('StaffId', '')
        price = request.GET.get('Price', '')
        price2 = request.GET.get('Price2', '')
        result = request.GET.get('Result', '')
        remark = request.GET.get('Remark', '')

        searchList = {'id__exact': id, 'BuyerAccount__contains': buyerAccount,
                      'ProductID__exact': productID, 'Status__exact': status,
                      'Exetime__gte': exetimeStart, 'Exetime__lt': exetimeEnd,
                      'ShopName__contains': shopName, 'ShopSKU__contains': shopSKU, 'StaffId__exact': staffId,
                      'Price__exact': price, 'Price2__exact': price2, 'Result__exact': result,'Remark__contains': remark
                      }

        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    if k == 'Price__exact':
                        if '.00' in v:
                            v = v
                        else:
                            v += '.00'
                    sl[k] = v
        if sl is not None:            
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'输入的查询数据有问题！')
        return qs



