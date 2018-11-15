# -*- coding: utf-8 -*-
from .t_product_Admin import *
from datetime import datetime
from pyapp.models import B_Supplier
from pyapp.models import b_goods
from brick.function.formatUrl import format_urls
from skuapp.table.t_product_photograph import t_product_photograph
from skuapp.table.t_product_photo_ing import t_product_photo_ing
from skuapp.table.t_product_art_ing import t_product_art_ing
from skuapp.table.t_product_develop_ed import t_product_develop_ed
from skuapp.table.t_product_pic_completion import t_product_pic_completion
import copy
class t_product_build_ing_Admin(t_product_Admin):

    search_box1_flag = True
    #show_category = True
    say_hello = True
    show_pic = True
    Large_Small_flag = True
    enter_ed_classification = True
    #save_on_top =True
    # def getInfoFromSupplier(self,request,queryset) : #根据供货商获取信息,采购，
    #     #连接 sqlserver数据库
    #     import pyodbc
    #     conn= pyodbc.connect(SQLSERVERDB)
    #     cursor = conn.cursor();
    #     for qs in queryset:
    #         #获取采购员和责任归属人2
    #         cgy =''
    #         zrgs2 =''
    #
    #         sql= 'select NID ,SupplierName from B_Supplier '
    #
    #         cursor.execute(sql);
    #
    #         B_Supplier_obj = cursor.fetchone()
    #         while B_Supplier_obj is not None   :
    #
    #             if B_Supplier_obj.SupplierName == qs.SupplierID:
    #                 sql2=u'select Purchaser,possessMan2 from B_Goods where SupplierID =  %d  order by CreateDate desc '%( B_Supplier_obj.NID)
    #                 cursor.execute(sql2);
    #                 B_Goods_obj = cursor.fetchone()
    #                 if B_Goods_obj :
    #                     cgy = B_Goods_obj.Purchaser
    #                     zrgs2=B_Goods_obj.possessMan2
    #                     messages.error(request,u'cgy=[%s] zrgs2=[%s]'%(cgy,zrgs2) )
    #                 break
    #             else:
    #                 B_Supplier_obj = cursor.fetchone()
    #         obj = t_product_build_ing.objects.get(id__exact=qs.id)
    #         if obj :
    #             obj.Buyer = cgy
    #             obj.possessMan2 = zrgs2
    #             obj.save()
    #         cursor.close
    #     #关闭数据库连接
    #     conn.close()
    def getInfoFromSupplier(self, request, queryset):  # 根据供货商获取信息,采购
        for qs in queryset:
            cgy = ''
            zrgs2 = ''
            B_Supplier_obj = B_Supplier.objects.filter(SupplierName=qs.SupplierID)
            if B_Supplier_obj.exists():
                B_Goods_obj = b_goods.objects.filter(SupplierID=B_Supplier_obj[0].NID).order_by('-CreateDate')
                if B_Goods_obj.exists():
                    cgy = B_Goods_obj[0].Purchaser
                    zrgs2 = B_Goods_obj[0].possessMan2
                    messages.error(request, u'cgy=[%s] zrgs2=[%s]' % (cgy, zrgs2))
            qs.Buyer = cgy
            qs.possessMan2 = zrgs2
            qs.save()


    actions = ['to_art_pre','to_recycle','to_copy','to_repeats',]


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


    def to_repeats(self, request, queryset):
        for querysetid in queryset.all():
            obj = t_product_repeats()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID = request.user.username
            obj.fromT = self.model._meta.verbose_name
            obj.save()
            end_t_product_oplog(request,querysetid.MainSKU,'XJ',querysetid.Name2,querysetid.id)
            t_product_mainsku_sku.objects.filter(pid=obj.id).delete()  # 删除主SKU下所有的子SKU属性
            querysetid.delete()
    to_repeats.short_description = u'不开发产品'


    def to_copy(self, request, queryset): #

        for querysetid in queryset.all():

            obj = t_product_build_ing()
            obj.__dict__ = querysetid.__dict__
            obj.id = self.get_id()
            obj.MainSKU = ''
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID= request.user.username
            obj.save()
    to_copy.short_description = u'复制-该款产品'

    def to_check(self, request, obj):
        params = [
            {'id': obj.SupplierPUrl1, 'name': u'供货商商品URL一'},
            {'id': obj.SupplierPDes, 'name': u'供货商商品标题'},
            {'id': obj.SupplierID, 'name': u'供货商名称'},
            {'id': obj.UnitPrice, 'name': u'单价'},
            {'id': obj.Weight, 'name': u'克重'},
            {'id': obj.Name2, 'name': u'商品名称'},
            {'id': obj.Material, 'name': u'材质'},
            {'id': obj.Unit, 'name': u'单位'},
            {'id': obj.MinOrder, 'name': u'最小订货量'},
            {'id': obj.SupplierArtNO, 'name': u'供货商货号'},
            {'id': obj.LWH, 'name': u'长*宽*高'},
            {'id': obj.SupplierContact, 'name': u'供货商ID'},
            {'id': obj.ReportName, 'name': u'英文申报名'}, # 英文
            {'id': obj.ReportName2, 'name': u'中文申报名'}, # 中文
            {'id': obj.MinPackNum, 'name': u'最小包装数量'},
            {'id': obj.Material, 'name': u'材质'},
        ]

        for param in params:
            if not param['id']:
                messages.error(request, u'id:%s,MainSKU:%s,%s, 不能为空！' % (obj.id,obj.MainSKU,param['name']))
                return False

        return True


    def to_art_pre(self, request, queryset): #
        from datetime import datetime
        self.getInfoFromSupplier(request,queryset)
        for querysetid in queryset.all():
            if self.is_valid(request,querysetid) == False :
                continue

            if not self.to_check(request,querysetid):
                continue

            #下一步
            flag=False
            existflag = False
            if querysetid.LRStaffName is None or querysetid.LRStaffName.strip() == '' or querysetid.PZStaffName is None or querysetid.PZStaffName.strip() == '':
                obj = t_product_art_pre_ed()
                obj.__dict__ = copy.deepcopy(querysetid.__dict__)
                obj.id = querysetid.id
                obj.CreateTime = datetime.now()
                obj.CreateStaffName = request.user.first_name
                obj.StaffID = request.user.username
                obj.JZLTime = datetime.now()
                obj.JZLStaffName = request.user.first_name
                # 存在审核不通过写入到拍照人员和录入人员信息，在该步骤置空 add by wangzy 20180307
                obj.PZStaffName = None
                obj.LRStaffName = None

                if obj.DYStaffName is None or obj.DYStaffName.strip() == '':
                    obj.DYTime = datetime.now()
                    obj.DYStaffName = request.user.first_name
                if obj.KFStaffName is None or obj.KFStaffName.strip() == '':
                    obj.KFTime = datetime.now()
                    obj.KFStaffName = request.user.first_name
                if obj.XJStaffName is None or obj.XJStaffName.strip() == '':
                    obj.XJTime = datetime.now()
                    obj.XJStaffName = request.user.first_name
                obj.save()
            else:
                flag=True
                obj = t_product_art_ed()
                obj.__dict__ = copy.deepcopy(querysetid.__dict__)
                obj.id = querysetid.id
                obj.CreateTime = datetime.now()
                #审核不通过写入到拍照人员和录入人员信息取出,创建人修改后将拍照人和录入人置为空处理 add by wangzy 20180307


                obj.StaffID = querysetid.PZStaffName           #工号
                obj.CreateStaffName = querysetid.LRStaffName   #创建人
                obj.PZStaffName = None
                obj.LRStaffName = None

                obj.JZLTime = datetime.now()
                obj.JZLStaffName = request.user.first_name
                if obj.DYStaffName is None or obj.DYStaffName.strip() == '':
                    obj.DYTime = datetime.now()
                    obj.DYStaffName = request.user.first_name
                if obj.KFStaffName is None or obj.KFStaffName.strip() == '':
                    obj.KFTime = datetime.now()
                    obj.KFStaffName = request.user.first_name
                if obj.XJStaffName is None or obj.XJStaffName.strip() == '':
                    obj.XJTime = datetime.now()
                    obj.XJStaffName = request.user.first_name
                obj.save()
            if querysetid.YNphoto == '0':  # 实拍
                if flag:
                    obj1=t_product_photograph.objects.filter(pid=querysetid.id,MainSKU=querysetid.MainSKU).values('MainSKU')
                    obj2=t_product_photo_ing.objects.filter(pid=querysetid.id,MainSKU=querysetid.MainSKU).values('MainSKU')
                    obj3=t_product_pic_completion.objects.filter(pid=querysetid.id,MainSKU=querysetid.MainSKU).values('MainSKU')
                    obj4=t_product_develop_ed.objects.filter(pid=querysetid.id,MainSKU=querysetid.MainSKU).values('MainSKU')
                    obj5=t_product_art_ing.objects.filter(pid=querysetid.id,MainSKU=querysetid.MainSKU).values('MainSKU')
                    if obj1.exists() or obj2.exists() or obj3.exists() or obj4.exists() or obj5.exists():
                        existflag = True
                if not existflag:
                    photo_obj = t_product_photograph()
                    photo_obj.__dict__ = copy.deepcopy(querysetid.__dict__)
                    try:
                        del photo_obj.auditnote
                    except Exception:
                        pass
                    #photo_obj.id = querysetid.id
                    photo_obj.SalesApplicant=None
                    photo_obj.Entertime = datetime.now()
                    photo_obj.CreateTime = datetime.now()
                    photo_obj.CreateStaffName = request.user.first_name
                    photo_obj.StaffID = request.user.username
                    photo_obj.LRTime = datetime.now()
                    photo_obj.LRStaffName = request.user.first_name
                    photo_obj.PZRemake = '1'
                    # photo_obj.MGProcess = '0'
                    photo_obj.PZTimeing = querysetid.JZLTime
                    photo_obj.PZStaffNameing = querysetid.JZLStaffName
                    photo_obj.SampleState = 'notyet'
                    photo_obj.pid = querysetid.id
                    photo_obj.id = None
                    photo_obj.save()

            elif querysetid.YNphoto == '1':  # 制作
                if flag:
                    obj4=t_product_develop_ed.objects.filter(pid=querysetid.id,MainSKU=querysetid.MainSKU).values('MainSKU')
                    obj5=t_product_art_ing.objects.filter(pid=querysetid.id,MainSKU=querysetid.MainSKU).values('MainSKU')
                    obj6 = t_product_pic_completion.objects.filter(pid=querysetid.id,MainSKU=querysetid.MainSKU).values('MainSKU')
                    if obj4.exists() or obj5.exists() or obj6.exists():
                        existflag=True
                if not existflag:
                    MG_obj = t_product_develop_ed()
                    MG_obj.__dict__ = copy.deepcopy(querysetid.__dict__)
                    MG_obj.SalesApplicant=None
                    MG_obj.Entertime = datetime.now()
                    try:
                        del MG_obj.auditnote
                    except Exception:
                        pass
                    #MG_obj.id = querysetid.id
                    MG_obj.CreateTime = datetime.now()
                    MG_obj.CreateStaffName = request.user.first_name
                    MG_obj.StaffID = request.user.username
                    MG_obj.LRTime = datetime.now()
                    MG_obj.LRStaffName = request.user.first_name
                    MG_obj.PZRemake = None
                    MG_obj.PZTimeing = None
                    MG_obj.PZStaffNameing = None
                    MG_obj.SampleState = None
                    MG_obj.pid = querysetid.id
                    MG_obj.id = None
                    # MG_obj.MGProcess = '1'
                    MG_obj.save()


            # else:
            #     obj = t_product_art_ed()
            #     obj.__dict__ = querysetid.__dict__
            #     obj.id = querysetid.id
            #     obj.CreateTime = datetime.now()
            #     #审核不通过写入到拍照人员和录入人员信息取出,创建人修改后将拍照人和录入人置为空处理 add by wangzy 20180307
            #
            #
            #     obj.StaffID = querysetid.PZStaffName
            #     obj.CreateStaffName = querysetid.LRStaffName
            #     obj.PZStaffName = None
            #     obj.LRStaffName = None
            #
            #     obj.JZLTime = datetime.now()
            #     obj.JZLStaffName = request.user.first_name
            #     if obj.DYStaffName is None or obj.DYStaffName.strip() == '':
            #         obj.DYTime = datetime.now()
            #         obj.DYStaffName = request.user.first_name
            #     if obj.KFStaffName is None or obj.KFStaffName.strip() == '':
            #         obj.KFTime = datetime.now()
            #         obj.KFStaffName = request.user.first_name
            #     if obj.XJStaffName is None or obj.XJStaffName.strip() == '':
            #         obj.XJTime = datetime.now()
            #         obj.XJStaffName = request.user.first_name
            #     obj.save()

            end_t_product_oplog(request,querysetid.MainSKU,'JZL',querysetid.Name2,querysetid.id)
            querysetid.delete()
    to_art_pre.short_description = u'下一步(信息审核)'


    def to_getback(self, request, queryset): #找回资料
        if request.user.is_superuser:
            t_product_build_ing_objs = t_product_build_ing.objects.all()
            for t_product_build_ing_obj in t_product_build_ing_objs:
                t_product_oplog_objs = t_product_oplog.objects.filter(pid=t_product_build_ing_obj.id,StepID='JZL')
                if t_product_oplog_objs.count() > 0 and t_product_oplog_objs[0].OpID != t_product_build_ing_obj.StaffID :
                    t_product_build_ing_obj.StaffID = t_product_oplog_objs[0].OpID
                    t_product_build_ing_obj.save()
        else:
            t_product_build_ing_objs = t_product_build_ing.objects.filter(StaffID= request.user.username)
            for t_product_build_ing_obj in t_product_build_ing_objs:
                t_product_oplog_objs = t_product_oplog.objects.filter(pid=t_product_build_ing_obj.id,StepID='JZL')
                if t_product_oplog_objs.count() > 0 and t_product_oplog_objs[0].OpID != t_product_build_ing_obj.StaffID :
                    t_product_build_ing_obj.StaffID = t_product_oplog_objs[0].OpID
                    t_product_build_ing_obj.save()
    to_getback.short_description = u'找回被驳回信息'


    def to_develop_ed(self, request, queryset): #大的开发概念完成

        self.getInfoFromSupplier(request,queryset)
        for querysetid in queryset.all():
            if self.is_valid(request,querysetid) ==False :
                continue

            obj = None
            if querysetid.fromT is not None and querysetid.fromT.strip() == 't_product_art_ed' :
                #下一步
                obj = t_product_art_ed()
            else:
                #下一步
                obj = t_product_develop_ed()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID= request.user.username
            obj.save()

            end_t_product_oplog(request,querysetid.MainSKU,'JZL',querysetid.Name2,querysetid.id)

            querysetid.delete()
    to_develop_ed.short_description = u'下一步(美工或信息审核)'


    def to_photograph(self, request, queryset): #大的开发概念完成
        self.getInfoFromSupplier(request,queryset)
        for querysetid in queryset.all():
            if self.is_valid(request,querysetid) ==False :
                continue
            #下一步
            obj = t_product_photograph()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID= request.user.username
            obj.save()

            end_t_product_oplog(request,querysetid.MainSKU,'JZL',querysetid.Name2,querysetid.id)
            begin_t_product_oplog(request, querysetid.MainSKU, 'PZ', querysetid.Name2, querysetid.id)
            querysetid.delete()
    to_photograph.short_description = u'下一步(需要去拍照)'


    def to_recycle(self, request, queryset):
        super(t_product_build_ing_Admin, self).to_recycle(request, queryset)
    to_recycle.short_description = u'扔进回收站'


    def show_oplog(self,obj) :
        rt = ''
        t_product_oplog_objs = t_product_oplog.objects.filter(pid=obj.id).order_by('id')
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
    
    list_per_page=20
    
    def show_product_messages(self,obj):
        rt = u'商品名称(中文):%s <br><span style="color:green;cursor: pointer;" id="more_id_%s">更 多</span>'%(obj.Name2,obj.id)
        rt = u"%s<script>$('#more_id_%s').on('click',function()" \
                     u"{layer.open({type:2,skin:'layui-layer-lan',title:'更多信息'," \
                     u"fix:false,shadeClose: true,maxmin:true,area:['1500px','300px'],btn: ['关闭页面']," \
                     u"content:'/more_product_informations/?flag_obj=%s&flag=t_product_building',});" \
                     u"});</script>" % (rt,obj.id, obj.id)
        return mark_safe(rt)
    show_product_messages.short_description = u'<span style="color:#428bca;">商品信息</span>'

    def show_ClothingSystem(self, obj):
        rt = u'一级:%s <br>二级:%s <br>三级:%s ' % (obj.ClothingSystem1, obj.ClothingSystem2, obj.ClothingSystem3)
        return mark_safe(rt)

    show_ClothingSystem.short_description = u'<span style="color:#428bca">服装分类</span>'

    def show_KFStaffName(self,obj):
        rt = u'开发: %s<br> 时间:%s <br>审核: %s <br> 时间:%s <br>询价: %s <br> 时间:%s' % (obj.KFStaffName,obj.KFTime,obj.DYSHStaffName,obj.DYSHTime,obj.XJStaffName,obj.XJTime)
        return mark_safe(rt)
    show_KFStaffName.short_description = u'<span style="color:#428bca">开发-时间/审核-时间/询价-时间</span>'

    list_display= ('id','show_KFStaffName','show_SourcePicPath','SpecialSell','SpecialRemark','show_SourcePicPath2','MainSKU',
                   'show_skulist','show_product_messages','show_ClothingSystem','ClothingNote','show_urls',)
    #list_display_links=('id','Keywords','Keywords2','Pricerange','SupplierPUrl1','SupplierPDes','SpecialSell',)
    list_editable=('SpecialRemark','ClothingNote','SpecialSell',)
    #search_fields=('id','MainSKU','Name2','StaffID',)
    # readonly_fields = ('id','SourcePicPath','SourcePicPath2','Pricerange','OrdersLast7Days','Keywords', 'Keywords2',)
    # 分组表单
    readonly_fields = ('auditnote',)
    fields = ('SourceURL','OrdersLast7Days','Keywords','Keywords2','SpecialRemark',
              'Pricerange','ShelveDay','Name','Tags', #u'调研结果',
              'SupplierPUrl1','SupplierPDes','SupplierID', # u'开发结果',
              'UnitPrice','Weight','SpecialSell', #u'询价结果',
              'Name2','Material','Unit','MinOrder','SupplierArtNO',
              'SupplierPColor','SupplierPUrl2','OrderDays','StockAlarmDays','LWH',
              'SupplierContact','Storehouse','ReportName','ReportName2','MinPackNum',#建资料
              'ContrabandAttribute', #'Electrification','Powder','Liquid','Magnetism',  #u'违禁品',
              'Remark', #备注
              'YNphoto','PPosition',#实拍选择
              'PictureRequest',#图片要求
              'MainSKU', #主SKU
              'YJGS2StaffName',#业绩归属人2
              'SourcePicPath', 'SourcePicPath2','AI_FLAG',#精准调研标记
              'SourceURL2', 'IP_FLAG',
              )
    list_filter = ()
    search_fields = ()
    form_layout = (
        Fieldset(u'调研结果',
                    Row('SourceURL','SourceURL2',),
                    Row('OrdersLast7Days','Pricerange',''),
                    Row('Keywords','Keywords2','Tags'),
                    Row('ShelveDay','Name','SpecialRemark'),
                    Row('ClothingSystem1','ClothingSystem2','ClothingSystem3'),
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
                    Row('YJGS2StaffName','AI_FLAG', 'IP_FLAG'),
                    css_class = 'unsort '
                ),
        Fieldset(u'违禁品',
                    Row('ContrabandAttribute',),#'Electrification','Powder','Liquid','Magnetism', ),
                    css_class = 'unsort '
                ),
        Fieldset(u'备注信息(字段长度300)',
                    Row('Remark'),
                    css_class = 'unsort '
                ),
        Fieldset(u'图片处理',
                    Row('YNphoto','PPosition'),
                    Row('PictureRequest'),
                    css_class = 'unsort '
                ),
        Fieldset(u'主SKU信息',
                    Row('MainSKU','',''),
                    css_class = 'unsort '
                ),

                  )

    def save_pic_mainsku(self, request, obj, form, change):

        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_DEV)

        if request.method == 'POST':
            files = request.FILES.getlist('myfiles','')
            if files is None or len(files)== 0 :
                return
            for f in files :
                #bucket.put_object(u'%s/%s'%(obj.id,f.name),f) #obj.Category1_id
                bucket.put_object(u'%s/PUB/%s'%(obj.MainSKU,f.name),f)

                obj.SourcePicPath =  u'%s%s.%s/%s/PUB/%s'%(PREFIX,BUCKETNAME_DEV,ENDPOINT_OUT,obj.MainSKU,f.name)
                if f.name.strip().find('0000') >= 0:
                    obj.SourcePicPath =  u'%s%s.%s/%s/PUB/%s'%(PREFIX,BUCKETNAME_DEV,ENDPOINT_OUT,obj.MainSKU,f.name)
                    #obj.SourcePicPath =  u'%s/%s'%(obj.id,f.name)
                    messages.error(request,obj.SourcePicPath )
                obj.save()


    #上传图片 子skuname,行index，request，obj
    def save_pic(self,skuname, i,request, obj):
        MainSKU = obj.MainSKU

        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_DEV)

        #加上子SKU
        path =  u'%s/%s'%(MainSKU,skuname)

        #写文件
        picfiles = request.FILES.getlist('file_%s_file'%i,'')
        for picfile in picfiles :
            if picfile is None or picfile.name.strip()=='' :
                continue
            bucket.put_object('%s/%s'%(path,picfile.name),picfile)


    def save_sku(self, request, obj, form, change):
        #先删除后头信息
        logger = logging.getLogger('sourceDns.webdns.views')    #刚才在setting.py中配置的logger

        logger.error("headnameheadnameheadnameheadnameheadnameheadname")


        #图片
        picfiles = request.FILES.getlist('file')
        for picfile in picfiles :
            logger.error(u'picfile= %s'%picfile.name)


        headnames = request.POST.getlist('headname','')
        for headname in headnames :
            logger.error(headname)

        logger.error("save_skusave_skusave_skusave_skusave_skusave_sku")
        skunames = request.POST.getlist('skuname','')
        for skuname in skunames :
            logger.error('skuname=%s'%skuname)

        logger.error("attrvalueattrvalueattrvalueattrvalueattrvalueattrvalueattrvalue")
        attrvalues = request.POST.getlist('attrvalue','')
        for attrvalue in attrvalues :
            logger.error('attrvalue=%s'%attrvalue)

        #删除插入表头,字段名称
        t_product_mainsku_arrt_name.objects.filter(MainSKU=obj.MainSKU).delete()



        j=0
        for headname in headnames :
            t_product_mainsku_arrt_name_obj= t_product_mainsku_arrt_name(MainSKU=obj.MainSKU,Attrid=j,AttrName=headname, pid=obj.id)
            t_product_mainsku_arrt_name_obj.save()
            j+=1

        t_product_sku_attr_value.objects.filter(MainSKU=obj.MainSKU).delete()
        t_product_mainsku_sku.objects.filter(MainSKU=obj.MainSKU).delete()

        #bucket = oss2.Bucket(oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET), ENDPOINT,BUCKETNAME_DEV)
        #for  object_info in oss2.ObjectIterator(bucket,prefix='%s/'%(obj.MainSKU)):
            #logger.error("object_infoobject_infoobject_infoobject_infoobject_info %s"%object_info.key)
            #if object_info.key.find('PUB') < 0 : #  PUB不删除
                #bucket.delete_object(object_info.key)

        i =0
        for skuname in skunames :
            if skuname is None or skuname.strip()=='' :
                i +=1
                continue

            #t_product_sku_attr_value_obj= t_product_sku_attr_value(MainSKU=obj.MainSKU,SKU=skuname,Attrid=0,AttrValue= skuxxxxxxxxxx)
            #t_product_sku_attr_value_obj.save()
            #插入对应关系

            t_product_mainsku_sku_obj = t_product_mainsku_sku(MainSKU=obj.MainSKU,SKU=skuname,pid=obj.id)
            t_product_mainsku_sku_obj.save()

            jj =0
            for headname in headnames :
                t_product_sku_attr_value_obj= t_product_sku_attr_value(MainSKU=obj.MainSKU,SKU=skuname,Attrid=jj,AttrValue=attrvalues[i*len(headnames) +jj])
                t_product_sku_attr_value_obj.save()
                jj +=1
            self.save_pic(skuname,i,request,obj)
            i+=1


    #判断主SKU是否合法
    def is_valid(self,request,obj):
        #主SKU不存在
        if obj.MainSKU is None or  obj.MainSKU.strip()=='':
            messages.error(request,u'错误:主SKU(%s)为空!!!'%obj.MainSKU)
            return False

        #重复
        #if t_product_oplog.objects.filter(MainSKU = obj.MainSKU,StepID='JZL').count() >0 :
            #messages.error(request,u'ERROR:MainSKU(%s) repeat!!!'%obj.MainSKU )
            #return False

        #包装规格
        if obj.PackNID is None or obj.PackNID == 0 or obj.PackNID == '0':
            messages.error(request,u'错误:请选择包装规格!!!' )
            return False

        #大类
        if obj.LargeCategory is None or obj.LargeCategory == u'请选择大类' or obj.LargeCategory.strip() =='':
            messages.error(request,u'错误:请选择大类!!!' )
            return False
    #def save_model(self, request, obj, form, change):
    def save_models(self):
        obj = self.new_obj
        request = self.request

        old_obj = None
        if obj is None or obj.id is None or obj.id <=0:
            obj.id = self.get_id()
        else:
            old_obj = self.model.objects.get(pk=obj.pk)

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
        obj.SKU = obj.MainSKU
        obj.PackNID = request.POST.get('select_mainsku',0)

        obj.MGProcess = obj.YNphoto # 实拍=待实拍，制作=待制作

        obj.JZLTime = datetime.now()
        obj.JZLStaffName = request.user.first_name

        if obj.DYStaffName is None or obj.DYStaffName.strip() == '':
            obj.DYTime = datetime.now()
            obj.DYStaffName = request.user.first_name
        if obj.KFStaffName is None or obj.KFStaffName.strip() == '':
            obj.KFTime = datetime.now()
            obj.KFStaffName = request.user.first_name
        if obj.XJStaffName is None or obj.XJStaffName.strip() == '':
            obj.XJTime = datetime.now()
            obj.XJStaffName = request.user.first_name

        obj.save()

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

        if obj.PackNID == 0 or  obj.PackNID == '0':
            messages.error(request,u'错误:请选择包装规格!!!' )
            #return
        obj.LargeCategory = request.POST.get('LargeCategory_copy',u'请选择大类')
        if obj.LargeCategory == u'请选择大类' or obj.LargeCategory == u'None':
            messages.error(request, u'错误:请选择大类!!!')
            #return
        obj.SmallCategory = request.POST.get('SmallCategory_copy',u'请选择小类')
        if obj.SmallCategory == u'请选择小类':
            messages.error(request, u'错误:请选择小类!!!')

        if obj.MainSKU is None or  obj.MainSKU.strip()=='':
            messages.error(request,u'错误:请填写正确的主SKU!!!' )
            #return

        #t_product_mainsku_sku.objects.filter(pid=obj.id).delete()
        t_product_mainsku_sku_objs = t_product_mainsku_sku.objects.filter(pid=obj.id)
        count = t_product_mainsku_sku_objs.count()
        t_product_mainsku_sku_objs.delete()
        skunum = 0

        for index in range(0, count):
            #self.message_user(request,u'index=%s'%(index))
            sku = request.POST.get('SKU_%s'%index,'')
            #self.message_user(request,u'index=%s,sku=%s'%(index,sku))
            if sku is None or sku =='' or sku=='None' or sku ==0 or sku.strip() =='':
                #t_product_mainsku_sku_objs[index].delete()
                continue

            skuattr = request.POST.get('SKUATTRS_%s'%index,obj.SupplierPColor)
            #self.message_user(request,u'index=%s,skuattr=%s'%(index,skuattr))
            if skuattr is None or skuattr.strip()=='':
                skuattr= obj.SupplierPColor

            unitprice = request.POST.get('UnitPrice_%s'%index,obj.UnitPrice)
            #self.message_user(request,u'index=%s,unitprice=%s'%(index,unitprice))
            if unitprice is None or str(unitprice).strip()=='' or  str(unitprice).strip()=='None':
                unitprice=obj.UnitPrice
            #unitprice = filter(lambda ch: ch in '0123456789.', unitprice)


            weight =   request.POST.get('Weight_%s'%index,obj.Weight)
            #self.message_user(request,u'index=%s,weight=%s'%(index,weight))
            if weight is None  or  str(weight).strip()=='':
                weight=obj.Weight
            #weight = filter(lambda ch: ch in '0123456789.', weight)
            NID  =   request.POST.get('select_%s'%index,obj.PackNID)
            if NID is None  or NID <=0 or str(NID).strip()=='':
                NID=obj.PackNID

            minPackNum =   request.POST.get('MinPackNum_%s'%index,obj.MinPackNum)
            #self.message_user(request,u'index=%s,weight=%s'%(index,weight))
            if minPackNum is None  or  str(minPackNum).strip()=='':
                minPackNum=1
            dressInfo =   request.POST.get('DressInfo_%s'%index,'')
            if dressInfo is None  or  str(dressInfo).strip()==''  or  str(dressInfo).strip()=='None':
                dressInfo=''
            ProductSKU_new = ''
            if obj.MainSKU == sku:
                ProductSKU_new = sku
            elif obj.MainSKU != sku: 
                ProductSKU_new = u'%s%s'%(obj.MainSKU,sku)

            SupplierLink = request.POST.get('SupplierLink_%s' % index, '')
            if SupplierLink.strip() == 'None':
                SupplierLink = ''

            SupplierNum = request.POST.get('SupplierNum_%s' % index, '')
            if SupplierNum.strip() == 'None':
                SupplierNum = ''
                
            t_product_mainsku_sku_obj = t_product_mainsku_sku(
                MainSKU=obj.MainSKU,SKU=sku,ProductSKU=ProductSKU_new,SKUATTRS= skuattr,UnitPrice=unitprice,
                Weight= float(weight),PackNID=NID,MinPackNum=minPackNum,pid = obj.id,DressInfo=dressInfo,
                SupplierLink = SupplierLink,SupplierNum=SupplierNum
            )
            t_product_mainsku_sku_obj.save()


            #self.message_user(request,u'index=%s,t_product_mainsku_sku_obj=%s'%(index,t_product_mainsku_sku_obj))
            skunum +=1

        if skunum < 1 :
            if obj.SupplierPColor is None :
                obj.SupplierPColor=''
            if obj.UnitPrice is None :
                obj.UnitPrice=0
            if obj.Weight is None :
                obj.Weight=0
            if obj.MainSKU is not None and  obj.MainSKU.strip()!='':
                t_product_mainsku_sku.objects.filter(pid=obj.id).delete()
                t_product_mainsku_sku_obj = t_product_mainsku_sku(
                    MainSKU=obj.MainSKU,SKU=obj.MainSKU,ProductSKU=obj.MainSKU,SKUATTRS= obj.SupplierPColor,
                    UnitPrice=obj.UnitPrice,Weight=float(obj.Weight),pid = obj.id,PackNID=obj.PackNID,
                    MinPackNum=obj.MinPackNum,SupplierLink=obj.SupplierPUrl1,DressInfo='',SupplierNum=obj.SupplierArtNO
                )
                t_product_mainsku_sku_obj.save()

        if obj.YJGS2StaffName is None or obj.YJGS2StaffName.strip() == '':
            obj.YJGS2StaffName = request.user.username

        obj.save()

        begin_t_product_oplog(request,obj.MainSKU,'JZL',obj.Name2,obj.id)

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


        # url = obj.SourceURL
        # try:
        #     if  url.find(WISH_URL)  >=0  : # wish的数据采集
        #         self.readWish(request,old_obj,obj)
        #         obj.save()
        #         #return
        #     if  url.find(AMAZON_URL)  >=0  : # amazon的数据采集
        #         self.readAmazon(request,old_obj,obj)
        #         obj.save()
        #         #return
        #     #if  url.find(WWW1688_URL)  >=0  : # 1688的数据采集
        #         #self.read1688(request, obj,url)
        #         #obj.save()
        #         #return
        #     if  url.find(EBAY_URL)  >=0  : # EBAY的数据采集
        #         self.readeBay(request,old_obj,obj)
        #         obj.save()
        #         #return
        #     if  url.find(ALIEXPRESS_URL)  >=0  : # aliexpress的数据采集
        #         self.readAliexpress(request,old_obj,obj)
        #         obj.save()
        #         #return
        # except Exception,ex:
        #    print Exception,":",ex
        #    messages.error(request,'提取数据失败 . %s : %s'%(Exception,ex))

        # if obj.SupplierPUrl1 is not None and obj.SupplierPUrl1.strip() != '' and obj.SupplierPUrl1.find(
        #         '1688.com') == -1:
        #     messages.error(request, u'错误:非1688,不可以做供应商!!!')
        #     return
        #读取供应商信息
        # self.read1688_2(request,old_obj,obj)
        try:
            if obj.selectpic2 is not None and str(obj.selectpic2).strip() != ''  :
                auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
                bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_1688)
                bucket.put_object(u'%s/%s.jpg'%(obj.id,obj.id),obj.selectpic2)
                #保存图片
                obj.SourcePicPath2 =  u'%s%s.%s/%s/%s.jpg'%(PREFIX,BUCKETNAME_1688,ENDPOINT_OUT,obj.id,obj.id)
                obj.save()

            if obj.selectpic is not None and str(obj.selectpic).strip() != ''  :
                auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
                bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_SV)
                bucket.put_object(u'%s/%s.jpg'%(obj.id,obj.id),obj.selectpic)
                #保存图片
                obj.SourcePicPath  =  u'%s%s.%s/%s/%s.jpg'%(PREFIX,BUCKETNAME_SV,ENDPOINT_OUT,obj.id,obj.id)
                obj.save()
        except:
            pass

    def get_list_queryset(self,):
        request = self.request
        from skuapp.table.t_sys_staff_auth import t_sys_staff_auth
        qs = super(t_product_build_ing_Admin, self).get_list_queryset()

        flagcloth = request.GET.get('classCloth', '')
        Cate1 = request.GET.get('cate1','')
        Cate2 = request.GET.get('cate2','')
        Cate3 = request.GET.get('cate3','')
        # Electrification = request.GET.get('Electrification','')     # 是否带电
        # Powder          = request.GET.get('Powder','')              # 是否粉末
        # Liquid          = request.GET.get('Liquid','')              # 是否液体
        # Magnetism       = request.GET.get('Magnetism','')           # 是否带磁
        ContrabandAttribute  = request.GET.get('ContrabandAttribute','')   # 发货仓库
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
        
        WeightStart = request.GET.get('WeightStart','')#克重
        WeightEnd = request.GET.get('WeightEnd','')
    
        updateTimeStart = request.GET.get('updateTimeStart','')#更新时间
        updateTimeEnd = request.GET.get('updateTimeEnd', '')

        searchList = { 'MainSKU__exact':MainSKU,'ContrabandAttribute__exact':ContrabandAttribute,
                        'Storehouse__exact':Storehouse, 'LargeCategory__exact':LargeCategory,
                        'YNphoto__exact': YNphoto,'YNphoto__exact':YNphoto,'Buyer__exact':Buyer, 'DYStaffName__exact':DYStaffName,
                        'KFStaffName__exact':KFStaffName, 'XJStaffName__exact':XJStaffName, 'JZLStaffName__exact':JZLStaffName,
                        'PZStaffName__exact':PZStaffName, 'MGStaffName__exact':MGStaffName, 'LRStaffName__exact':LRStaffName,
                        'Weight__gte':WeightStart, 'Weight__lt':WeightEnd, 
                        'UpdateTime__gte': updateTimeStart, 'UpdateTime__lt': updateTimeEnd,'ClothingSystem1__exact':Cate1,
                        'ClothingSystem2__exact': Cate2,'ClothingSystem3__exact':Cate3,
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
                
        if Cate1 != '':
            if Cate2 != '':
                if Cate3 != '':
                    qs = qs.filter(ClothingSystem3=Cate3)
                else:
                    qs = qs.filter(ClothingSystem2=Cate2)
            else:
                qs = qs.filter(ClothingSystem1=Cate1)

        catelist = [u'001.时尚女装', u'002.时尚男装', u'021.泳装', u'024.童装', u'025.内衣']

        if flagcloth == '1':
            qs = qs.filter(LargeCategory__in=catelist)
        elif flagcloth == '2':
            qs = qs.exclude(LargeCategory__in=catelist)
        flag = 0
        try:
            flag = t_sys_staff_auth.objects.filter(StaffID=request.user.username,urltable="t_product_build_ing").count()
        except:
            pass
        if request.user.is_superuser or flag != 0:
            return qs
        return qs.filter(StaffID = request.user.username)