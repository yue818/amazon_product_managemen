# -*- coding: utf-8 -*-
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from skuapp.table.t_shopsku_information_binding import t_shopsku_information_binding
#from brick.pydata.py_redis.py_SynRedis_pub import py_SynRedis_pub
from brick.classredis.classsku import classsku

from pyapp.models import b_goodsskulinkshop as py_b_goodsskulinkshop
from pyapp.models import b_goodssku as py_b_goodssku
import logging
from django.contrib import messages
import csv
from .t_product_Admin import *
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from datetime import datetime


classsku_obj = classsku()

class t_shopsku_information_binding_Admin(object):
    downloadxls = True
    search_box_flag = True
    list_display  =('id','SKU','ShopSKU','Memo','PersonCode','Filename','Submitter','SubmitTime','BindingStatus',)
    list_editable =('SKU','ShopSKU','Memo','PersonCode','BindingStatus',)
    list_filter   =('ShopSKU','Memo','PersonCode','Filename','Submitter','SubmitTime','BindingStatus',)
#    search_fields =('id','SKU','ShopSKU','Memo','PersonCode','Filename','Submitter','BindingStatus',)
    search_fields =None    
    fields = ('id',)

    form_layout = (
        Fieldset(u'导入文件-格式为"CSV"',
                    Row('id'),
                    css_class = 'unsort '
                ),
                  )
                  
    actions = ['to_shopsku_information_binding_excel',]
    
    def to_shopsku_information_binding_excel(self,request,queryset):
        allobj = User.objects.filter(groups__id__in=[6])
        userID = []
        for each in allobj:
            userID.append(each.id)
        if request.user.id in userID:
            from xlwt import *
            path = MEDIA_ROOT + 'download_xls/' + request.user.username
            #if not os.path.exists(path):
            mkdir_p(MEDIA_ROOT + 'download_xls')
            os.popen('chmod 777 %s'%(MEDIA_ROOT + 'download_xls'))

            mkdir_p(path)
            os.popen('chmod 777 %s'%(path))

            w = Workbook()
            sheet = w.add_sheet(u'店铺SKU信息绑定')

            sheet.write(0,0,u'商品SKU')
            sheet.write(0,1,u'店铺SKU')
            sheet.write(0,2,u'备注')
            sheet.write(0,3,u'销售员')
            sheet.write(0, 4, u'商品sku状态')

            #写数据
            id_list = []
            row = 0
            for qs in queryset:
                ShopSKU_list = []
                if qs.ShopSKU is not None and qs.ShopSKU.strip() != '':
                     for shoptmp in qs.ShopSKU.split('+'):
                        shopsku = shoptmp.split('\\\\')[0].split('*')[0]
                        ShopSKU_list.append(shopsku)
                for ShopSKU in ShopSKU_list:
                    row = row + 1
                    column = 0
                    sheet.write(row,column,qs.SKU)

                    column = column + 1
                    sheet.write(row,column,ShopSKU)

                    column = column + 1
                    sheet.write(row,column,qs.Memo)

                    column = column + 1
                    sheet.write(row,column,qs.PersonCode)

                    goodsstatus = classsku_obj.get_goodsstatus_by_sku(('%s' % qs.SKU).strip())



                    # py_SynRedis_pub_obj = py_SynRedis_pub()
                    # goodsstatus = py_SynRedis_pub_obj.getFromHashRedis('', ('%s'%qs.SKU).strip(), 'goodsstatus')
                    # if goodsstatus == '1' or goodsstatus == '1-正常':
                    #     goodsstatus = u'正常'
                    # if goodsstatus == '2' or goodsstatus == '2-售完下架':
                    #     goodsstatus = u'售完下架'
                    # if goodsstatus == '3' or goodsstatus == '3-临时下架':
                    #     goodsstatus = u'临时下架'
                    # if goodsstatus == '4' or goodsstatus == '4-停售':
                    #     goodsstatus = u'停售'
                    column = column + 1
                    sheet.write(row, column, goodsstatus)
					
                    id_list.append(qs.id)
                if row > 50000:
                    break
            filename = request.user.username + '_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.xls'
            w.save(path + '/' +  filename)
            os.popen(r'chmod 777 %s'%(path + '/' +  filename))

            #上传oss对象
            auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
            bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_XLS)
            bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)
            #删除现有的
            for  object_info in oss2.ObjectIterator(bucket,prefix='%s/%s_'%(request.user.username,request.user.username)):
                bucket.delete_object(object_info.key)
            bucket.put_object(u'%s/%s'%(request.user.username,filename),open(path + '/' +  filename))

            queryset.filter(id__in=set(id_list)).update(BindingStatus=2)

            messages.error(request,u'%s%s.%s/%s/%s'%(PREFIX,BUCKETNAME_XLS,ENDPOINT_OUT,request.user.username,filename) + u':成功导出,可点击Download下载到本地............................。' )
        else:
            messages.error(request,u'抱歉！非信息组用户不允许导出。。')
    to_shopsku_information_binding_excel.short_description = u'导出-店铺SKU信息绑定'
    
    
    def save_models(self):
        pass
        # obj     = self.new_obj
        # request = self.request
        #
        # logger  = logging.getLogger('sourceDns.webdns.views')
        #
        # try :
        #     if obj.Filename is not None and str(obj.Filename).strip() !='' :
        #         i = 0
        #         INSERT_INTO = []
        #         for row in csv.reader(obj.Filename):#obj.Status本身就是16进制字节流，直接reader
        #             if i < 1:
        #                 i = i + 1
        #                 continue
        #             i = i + 1
        #             if (row[0].decode("GBK")).strip() != '' and (row[1].decode("GBK")).strip() != '':
        #                 INSERT_INTO.append(t_shopsku_information_binding(SKU=row[0].decode("GBK"),ShopSKU=row[1].decode("GBK"),Memo=row[2].decode("GBK"),
        #                                             PersonCode=row[3].decode("GBK"),Filename = obj.Filename,Submitter = request.user.first_name,
        #                                             SubmitTime = datetime.now(),BindingStatus = u'wait'#等待处理
        #                                             )
        #                                     )
        #
        #         t_shopsku_information_binding.objects.bulk_create(INSERT_INTO)
        #
        # except Exception,ex :
        #     logger.error('%s============================%s'%(Exception,ex))
        #     messages.error(request,'%s============================%s'%(Exception,ex))


    def get_list_queryset (self,):
        request = self.request
        qs = super(t_shopsku_information_binding_Admin, self).get_list_queryset()
        SKU = request.GET.get('SKU','')
        ShopSKU = request.GET.get('ShopSKU','')
        Memo = request.GET.get('Memo','')
        PersonCode = request.GET.get('PersonCode','')
        Filename = request.GET.get('Filename','')
        Submitter = request.GET.get('Submitter','')
        SubmitTimeStart = request.GET.get('SubmitTimeStart','')
        SubmitTimeEnd = request.GET.get('SubmitTimeEnd', '')
        BindingStatus = request.GET.get('BindingStatus','')

        searchList = {'SKU__exact':SKU,'ShopSKU__exact':ShopSKU,'Memo__exact':Memo,'PersonCode__exact':PersonCode,'Filename__exact':Filename,
                      'Submitter__exact':Submitter,'BindingStatus__exact':BindingStatus,'SubmitTime__gte':SubmitTimeStart,'SubmitTime__lt':SubmitTimeEnd,}

        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    if k == 'ShopName__exact':
                        v = 'Wish-' + v.zfill(4)
                        # messages.error(request, v)
                    sl[k] = v
        if sl is not None:
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'输入的查询数据有问题！')
        return qs

            

            
            
            
            
