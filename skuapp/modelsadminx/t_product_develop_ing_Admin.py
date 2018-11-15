# -*- coding: utf-8 -*-

from .t_product_Admin import *
from datetime import datetime as ddtime

#from skuapp.table.v_product_allsku import *
#from skuapp.views import *
from django.db.models import Q
from brick.function.formatUrl import format_urls

class t_product_develop_ing_Admin(t_product_Admin):

    search_box1_flag = True
    show_prompt_develop = True
    show_pic = True
    #save_on_top =True
    Three_Class_flag = True
    Large_Small_flag = True
    actions = ['to_wait_enquiry','to_recycle' ]
    def to_recycle(self, request, queryset):
        super(t_product_develop_ing_Admin, self).to_recycle(request, queryset)
    to_recycle.short_description = u'扔进回收站'

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




    def to_wait_enquiry(self, request, queryset):
        from skuapp.table.t_product_develop_ing import t_product_develop_ing
        for querysetid in queryset.all():
            if querysetid.LargeCategory is not None and querysetid.LargeCategory.strip() != '' and querysetid.SmallCategory is not None and querysetid.SmallCategory.strip() != '':
                #下一步
                '''
                obj = t_product_wait_enquiry()
                obj.__dict__ = querysetid.__dict__
                obj.id = querysetid.id
                obj.CreateTime = ddtime.now()
                obj.CreateStaffName = request.user.first_name
                obj.StaffID = request.user.username
                obj.save()
                '''

                end_t_product_oplog(request,querysetid.MainSKU,'KF',querysetid.Name2,querysetid.id)

                #记录调研调研历史
                t_product_survey_history_obj = t_product_survey_history(SourcePicPath=querysetid.SourcePicPath,SourceURL=querysetid.SourceURL,SourcePicPath2=querysetid.SourcePicPath2,SupplierPUrl1=querysetid.SupplierPUrl1,StaffID=request.user.username,StaffName=request.user.first_name,pid=querysetid.id)
                t_product_survey_history_obj.save()

                t_product_develop_ing_obj = t_product_develop_ing()
                t_product_develop_ing_obj.__dict__ = querysetid.__dict__
                t_product_develop_ing_obj.CreateTime = ddtime.now()
                t_product_develop_ing_obj.CreateStaffName = request.user.first_name
                t_product_develop_ing_obj.StaffID = request.user.username
                t_product_develop_ing_obj.AuditStaffName = 'commitaudit'
                t_product_develop_ing_obj.save()
            else:
                messages.error(request,u'大类或小类为空，请选择，并再次提交。')

    to_wait_enquiry.short_description = u'提交审核'

 
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


    #调研显示和编辑字段
    #list_display=('id','show_SourcePicPath','OrdersLast7Days','Pricerange','ShelveDay','Keywords','Keywords2','SpecialRemark','show_urls',)
    #list_editable=('OrdersLast7Days','Keywords','Keywords2','SpecialRemark','ShelveDay','Pricerange',)
    list_per_page=20
    list_display= ('id','KFStaffName','KFTime','SpecialSell','show_SourcePicPath','ShelveDay','OrdersLast7Days','ClothingSystem1','ClothingSystem2','ClothingSystem3','ClothingNote','Pricerange','Keywords','LargeCategory','show_SourcePicPath2','SupplierPDes','SupplierID','BJP_FLAG','show_urls',)
    # readonly_fields = ('SourcePicPath','SourcePicPath2','Pricerange','OrdersLast7Days','Keywords','Keywords2',)
    list_editable=('ClothingSystem1','ClothingSystem2','ClothingSystem3','ShelveDay','LargeCategory','SpecialSell','SupplierPDes','SupplierID','BJP_FLAG')

    fields =  ('SourcePicPath','SourcePicPath2','SpecialRemark','SourceURL','OrdersLast7Days','Pricerange','ShelveDay','ClothingNote','Keywords','Keywords2','SpecialSell','SupplierPDes','SupplierID','SupplierPUrl1','SupplierPUrl2','BJP_FLAG','SourceURL2','IP_FLAG')
    list_filter = ()
    search_fields = ()
    form_layout = (
        Fieldset(u'调研结果',
                       Row('SourceURL', 'SourceURL2',),
                       Row('OrdersLast7Days', 'Pricerange',),
                       Row('Keywords', 'Keywords2',),
                       Row( 'ShelveDay','',),
                       css_class = 'unsort '
                ),
        Fieldset(u'开发结果',
                       Row( 'SupplierPUrl1','SupplierPUrl2',),
                       Row( 'SupplierPDes','SupplierID',),
                       Row( 'SpecialRemark','IP_FLAG',),
                       Row( 'ClothingNote','SpecialSell',),
                       css_class = 'unsort  '
                )
                  )
 

    #def save_model(self, request, obj, form, change):
    def save_models(self):
        obj = self.new_obj

        request = self.request

        old_obj = None

        if obj is None or obj.id is None or obj.id <=0:
            obj.id = self.get_id()
        else:
            old_obj = self.model.objects.get(pk=obj.pk)
        obj.save()
        #messages.error(request,'  old_obj = %s obj=%s '%(old_obj,obj))
        #return
        ##begin_t_product_oplog(request,obj.MainSKU,'KF',obj.Name,obj.id)
        #logger = logging.getLogger('sourceDns.webdns.views')    #刚才在setting.py中配置的logger
        #判断新老url是否相等
        #obj_original = None
        #if obj is not None and obj.pk is not None:
            #obj_original = t_product_develop_ing.objects.filter(id=obj.id)
        #

        if obj.SourceURL.find('wish.') != -1:
            obj.PlatformName = 'Wish'
        elif obj.SourceURL.find('ebay.') != -1:
            obj.PlatformName = 'eBay'
        elif obj.SourceURL.find('amazon.') != -1:
            obj.PlatformName = 'Amazon'
        elif obj.SourceURL.find('aliexpress.') != -1:
            obj.PlatformName = 'Aliexpress'
        else:
            obj.PlatformName = 'Others'

        obj.StaffID = request.user.username
        obj.CreateTime = ddtime.now()
        obj.CreateStaffName = request.user.first_name

        obj.KFTime = ddtime.now()
        obj.KFStaffName = request.user.first_name
        if obj.DYStaffName is None or obj.DYStaffName.strip() == '':
            obj.DYTime = ddtime.now()
            obj.DYStaffName = request.user.first_name

        obj.ClothingSystem1 = request.POST.get('ClothingSystem1_copy','')
        obj.ClothingSystem2 = request.POST.get('ClothingSystem2_copy','')
        obj.ClothingSystem3 = request.POST.get('ClothingSystem3_copy','')

        obj.LargeCategory = request.POST.get('LargeCategory_copy')

        url = obj.SourceURL
        url1688 = obj.SupplierPUrl1
        from brick.requestproxy.formatUrl import format_urls
        try:
            platform, return_url = format_urls(url)
            if platform in ("wish", "amazon", "ebay", "aliexpress"):
                if platform == "wish":
                    obj.SourceURL = "https://www.wish.com/c/%s" % return_url
                if platform == "amazon":
                    obj.SourceURL = "https://www.amazon.com/dp/%s" % return_url
                if platform == "ebay":
                    if url.find('www.ebay.co.uk') >= 0:
                        obj.SourceURL = "https://www.ebay.co.uk/itm/%s" % return_url
                    elif url.find('www.ebay.ca') >= 0:
                        obj.SourceURL = "https://www.ebay.ca/itm/%s" % return_url
                    elif url.find('www.ebay.com.au') >= 0:
                        obj.SourceURL = "https://www.ebay.com.au/itm/%s" % return_url
                    elif url.find('www.ebay.de') >= 0:
                        obj.SourceURL = "https://www.ebay.de/itm/%s" % return_url
                    else:
                        obj.SourceURL = "https://www.ebay.com/itm/%s" % return_url
                if platform == "aliexpress":
                    obj.SourceURL = "https://www.aliexpress.com/item//%s.html" % return_url
        except:
            pass

        try:
            platform, return_url = format_urls(url1688)
            if platform == "1688":
                obj.SupplierPUrl1 = "https://detail.1688.com/offer/%s.html" % return_url
        except Exception, e:
            pass
        obj.save()

        if obj.LargeCategory is None or obj.LargeCategory.strip() == '':
            messages.error(request, u'错误:请选择大类!!!')
            return
        obj.SmallCategory = request.POST.get('SmallCategory_copy')
        if obj.SmallCategory is None or obj.SmallCategory.strip() == '':
            messages.error(request, u'错误:请选择小类!!!')
            return
        obj.save()
        #判断是否调研过
        if obj.SourceURL is not None :
            #1688不允许调研
            if  obj.SourceURL.find(WWW1688_URL)  >=0  : # 1688的数据采集
                messages.error(request,u'错误:请不要利用1688做反向链接调研!!!')
                return

            urlNew = obj.SourceURL
            if obj.SourceURL.find('?') >=0:
                urlNew = obj.SourceURL.split(r'?')[0]
            t_product_survey_history_objs = t_product_survey_history.objects.filter(SourceURL= urlNew)
            if t_product_survey_history_objs.count() > 0 :
                messages.error(request,'url已经调研过！ . %s  urlNew=%s '%(obj.SourceURL,urlNew))
                #obj.delete()
                #return
            t_product_survey_ing_objs = t_product_survey_ing.objects.filter(SourceURL= urlNew)
            if t_product_survey_ing_objs.count() > 1 :
                messages.error(request,'url已经调研过！ . %s count=%d '%(obj.SourceURL,t_product_survey_ing_objs.count()))
                #obj.delete()
                #return
        #obj.savexxx()
        select_picxx = False #表示True表示用户选择了图片
        if obj.selectpic is not None and str(obj.selectpic).strip() != ''  :
            auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
            bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_SV)
            bucket.put_object(u'%s/%s.jpg'%(obj.id,obj.id),obj.selectpic)
            #保存图片
            obj.SourcePicPath =  u'%s%s.%s/%s/%s.jpg'%(PREFIX,BUCKETNAME_SV,ENDPOINT_OUT,obj.id,obj.id)

            obj.save()
            select_picxx = True

        url = obj.SourceURL
        # if obj.SourcePicPath is None or obj.SourcePicPath.strip() == "":
        #     try:
        #         if  url.find(WISH_URL)  >=0  : # wish的数据采集
        #             self.readWish(request,old_obj,obj)
        #         if  url.find(AMAZON_URL)  >=0  : # amazon的数据采集
        #             self.readAmazon(request,old_obj,obj)
        #         if  url.find(EBAY_URL)  >=0  : # EBAY的数据采集
        #             self.readeBay(request,old_obj,obj)
        #         if  url.find(ALIEXPRESS_URL)  >=0  : # aliexpress的数据采集
        #             self.readAliexpress(request,old_obj,obj)
        #         obj.save()
        #     except Exception,ex:
        #        #print Exception,":",ex
        #        print u'%s:%s,自动获取数据错误，请选择手动上传图片或录入数据!!!'%(Exception,ex)
        #        messages.error(request,'提取数据失败 . %s : %s'%(Exception,ex))

        # if obj.SupplierPUrl1 is not None and obj.SupplierPUrl1.strip() != '' and obj.SupplierPUrl1.find(
        #         '1688.com') == -1:
        #     messages.error(request, u'错误:非1688,不可以做供应商!!!')
        #     return
        #读取供应商信息
        # messages.error(request, 'SourcePicPath2. %s' % (obj.SourcePicPath2))
        # if obj.SourcePicPath2 is None or obj.SourcePicPath2.strip() == "":
        #     try:
        #         self.read1688_2(request,old_obj,obj)
        #         obj.save()
        #     except:
        #         pass

        try:
            if obj.selectpic2 is not None and str(obj.selectpic2).strip() != ''  :
                auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
                bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_1688)
                bucket.put_object(u'%s/%s.jpg'%(obj.id,obj.id),obj.selectpic2)
                #保存图片
                obj.SourcePicPath2 =  u'%s%s.%s/%s/%s.jpg'%(PREFIX,BUCKETNAME_1688,ENDPOINT_OUT,obj.id,obj.id)

                obj.save()
        except:
            pass

    #def get_queryset(self, request):
    def get_list_queryset(self):
        request = self.request
        from skuapp.table.t_sys_staff_auth import t_sys_staff_auth
        qs = super(t_product_develop_ing_Admin, self).get_list_queryset()

        Cate1 = request.GET.get('cate1','')
        Cate2 = request.GET.get('cate2','')
        Cate3 = request.GET.get('cate3','')
        # Electrification = request.GET.get('Electrification','')     # 是否带电
        # Powder          = request.GET.get('Powder','')              # 是否粉末
        # Liquid          = request.GET.get('Liquid','')              # 是否液体
        # Magnetism       = request.GET.get('Magnetism','')           # 是否带磁
        ContrabandAttribute  = request.GET.get('ContrabandAttribute','')    #商品属性
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
        BJP_FLAG        = request.GET.get('BJP_FLAG','')
        
        WeightStart = request.GET.get('WeightStart','')#克重
        WeightEnd = request.GET.get('WeightEnd','')
    
        updateTimeStart = request.GET.get('updateTimeStart','')#更新时间
        updateTimeEnd = request.GET.get('updateTimeEnd', '')

        searchList = {  'MainSKU__exact':MainSKU,'ContrabandAttribute__exact':ContrabandAttribute,
                        'Storehouse__exact':Storehouse, 'LargeCategory__exact':LargeCategory,
                        'YNphoto__exact': YNphoto,'YNphoto__exact':YNphoto,'Buyer__exact':Buyer, 'DYStaffName__exact':DYStaffName,
                        'KFStaffName__exact':KFStaffName, 'XJStaffName__exact':XJStaffName, 'JZLStaffName__exact':JZLStaffName,
                        'PZStaffName__exact':PZStaffName, 'MGStaffName__exact':MGStaffName, 'LRStaffName__exact':LRStaffName,
                        'Weight__gte':WeightStart, 'Weight__lt':WeightEnd,
                        'UpdateTime__gte': updateTimeStart, 'UpdateTime__lt': updateTimeEnd,'ClothingSystem1__exact':Cate1,
                       'ClothingSystem2__exact': Cate2,'ClothingSystem3__exact':Cate3,'BJP_FLAG_exact':BJP_FLAG,
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
        flag = 0
        try:
            flag = t_sys_staff_auth.objects.filter(StaffID=request.user.username,urltable="t_product_develop_ing").count()
        except:
            pass
        if request.user.is_superuser or flag != 0:
            return qs.filter(~Q(AuditStaffName = 'commitaudit'))
        if Cate1 !='':
            if Cate2 !='':
                if Cate3 !='':
                    qs = qs.filter(ClothingSystem3 = Cate3)
                else:
                    qs = qs.filter(ClothingSystem2 = Cate2)
            else:
                qs = qs.filter(ClothingSystem1 = Cate1)
        return qs.filter(~Q(AuditStaffName = 'commitaudit'),StaffID = request.user.username)
