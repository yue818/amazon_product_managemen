# -*- coding: utf-8 -*-

from .t_product_Admin import *
class t_product_survey_ing_Admin(t_product_Admin):

    actions =  ['survey_ed_to_self','survey_ed', 'show_pic','to_recycle',]

    save_on_top =True


    def survey_ed_to_self(self, request, queryset):

        for querysetid in queryset.all():
            obj = t_product_develop_ing()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID = request.user.username

            obj.DYTime = datetime.now()
            obj.DYStaffName = request.user.first_name

            obj.save()


            #记录操作历史
            #end_oplog(request,querysetid,self)
            end_t_product_oplog(request,querysetid.MainSKU,'DY',querysetid.Name2,querysetid.id)
            begin_t_product_oplog(request,querysetid.MainSKU,'KF',querysetid.Name2,querysetid.id)

            querysetid.delete()
    survey_ed_to_self.short_description = u'调研完成直接开发'

    def survey_ed(self, request, queryset):
        for querysetid in queryset.all():
            #下一步
            obj = t_product_survey_ed()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name

            obj.DYTime = datetime.now()
            obj.DYStaffName = request.user.first_name

            obj.save()

            #记录操作历史
            #end_oplog(request,querysetid,self)
            end_t_product_oplog(request,querysetid.MainSKU,'DY',querysetid.Name2,querysetid.id)
            begin_t_product_oplog(request,querysetid.MainSKU,'DYSH',querysetid.Name2,querysetid.id)

            querysetid.delete()
    survey_ed.short_description = u'调研完成去审核'


    # def show_urls(self,obj) :
    #     rt = u'反向:<a href="%s" target="_blank" >%s</a><br>供货商:<a href="%s" target="_blank" >%s</a>'%(obj.SourceURL,obj.SourceURL,obj.SupplierPUrl1,obj.SupplierPUrl1)
    #     return mark_safe(rt)
    # show_urls.short_description = u'链接信息'

    #change_list_template = 'skuapp/templates/t_product_survey_ing/change_list.html'

    #forms = t_product_survey_ing_Form
    list_display=('id','show_SourcePicPath','OrdersLast7Days','Pricerange','ShelveDay','Keywords','SpecialRemark','show_urls',)
    #list_display_links=('SourcePicPath',)
    list_editable=('SpecialRemark','ShelveDay','Pricerange',)
    #search_fields=('id',)
    #show_detail_fields  =  [ 'id',]

    fields =  ('SourceURL','selectpic','OrdersLast7Days','Pricerange','Keywords','ShelveDay','SpecialRemark')

    form_layout = (
        Fieldset(u'调研结果',
                       Row('SourceURL', 'selectpic'),
                       Row('OrdersLast7Days', 'Pricerange'),
                       Row('Keywords'),
                       Row( 'ShelveDay'),
                       Row( 'SpecialRemark'),
                       css_class = 'unsort '
                )
                  )



    #def save_model(self, request, obj, form, change):
    def save_models(self):

        obj = self.new_obj
        request = self.request

        old_obj = None
        if obj is None or obj.id is None or obj.id <=0:
            pass
        else:
            old_obj = self.model.objects.get(pk=obj.pk)
        ##begin_t_product_oplog(request,obj.MainSKU,'DY',obj.Name,obj.id)
        logger = logging.getLogger('sourceDns.webdns.views')    #刚才在setting.py中配置的logger
        #
        #判断新老url是否相等
        #obj_original = None
        #if obj is not None and obj.pk is not None:
            #obj_original = self.model.objects.get(pk=obj.pk)

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
        obj.CreateTime = datetime.now()
        obj.CreateStaffName = request.user.first_name
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
                messages.error(request,'url已经调研过！ . %s  =%d次 '%(obj.SourceURL,t_product_survey_ing_objs.count()))
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
        try:
            if  url.find(WISH_URL)  >=0  : # wish的数据采集
                self.readWish(request,old_obj,obj)
                obj.save()
                #return
            if  url.find(AMAZON_URL)  >=0  : # amazon的数据采集
                self.readAmazon(request,old_obj,obj)
                obj.save()
                #return
            #if  url.find(WWW1688_URL)  >=0  : # 1688的数据采集
                #self.read1688(request, obj,url)
                #obj.save()
                #return
            if  url.find(EBAY_URL)  >=0  : # EBAY的数据采集
                self.readeBay(request,old_obj,obj)
                obj.save()
                #return
            if  url.find(ALIEXPRESS_URL)  >=0  : # aliexpress的数据采集
                self.readAliexpress(request,old_obj,obj)
                obj.save()
                #return
        except Exception,ex:
           print Exception,":",ex
           messages.error(request,'提取数据失败 . %s : %s'%(Exception,ex))

    #def get_queryset(self, request):
    def get_list_queryset(self):
        request = self.request


        qs = super(t_product_survey_ing_Admin, self).get_list_queryset()
        if request.user.is_superuser:
            return qs
        return qs.filter(StaffID = request.user.username)
