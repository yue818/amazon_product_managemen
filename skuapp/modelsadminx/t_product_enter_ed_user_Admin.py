# -*- coding: utf-8 -*-
from .t_product_Admin import *
from skuapp.table.t_product_mainsku_sku import *
import logging
from datetime import datetime as ddtime
from brick.function.formatUrl import format_urls
from skuapp.table.t_product_depart_get_user import *
from django.db import connection as conn

class t_product_enter_ed_user_Admin(t_product_Admin):
    enter_ed_user_flag = True
    enter_ed = True
    enter_ed_classification = True
    search_box1_flag = True
    downloadxls = True
    #py_search_system_flag = True
    actions = ['to_depart_get','to_excel_old']


    # ('Wish', 'Wish'),
    # ('Amazon', 'Amazon'),
    # ('Aliexpress', 'Aliexpress'),
    # ('eBay', 'eBay'),
    # ('Lazada', 'Lazada'),
    # ('1688', '1688'),
    #  ('Esty', 'Esty'),
    #  ('Others', 'Others'),
    #

#
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


    def to_excel_old(self, request, queryset):
        from xlwt import *
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        # if not os.path.exists(path):
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))

        mkdir_p(path)
        os.popen('chmod 777 %s' % (path))

        w = Workbook()
        sheet = w.add_sheet('t_product_enter_ed')

        sheet.write(0, 0, u'id')
        sheet.write(0, 1, u'主SKU')
        sheet.write(0, 2, u'调研时间')
        sheet.write(0, 3, u'调研员')
        sheet.write(0, 4, u'服装一级分类')
        sheet.write(0, 5, u'服装二级分类')
        sheet.write(0, 6, u'服装三级分类')
        sheet.write(0, 7, u'建资料员')
        sheet.write(0, 8, u'商品信息备注')

        #写数据
        row = 0
        for qs in queryset:

            #t_product_mainsku_sku_objs = t_product_mainsku_sku.objects.filter(MainSKU=qs.MainSKU).order_by('SKU')

            #for t_product_mainsku_sku_obj in  t_product_mainsku_sku_objs:

                row = row + 1
                column = 0
                sheet.write(row,column,qs.id)


                column = column + 1
                sheet.write(row, column, qs.MainSKU)


                column = column + 1
                rt = ''
                rt = u'%s%s' % (rt, qs.DYTime)
                sheet.write(row,column,u'%s' % rt)

                column = column + 1
                sheet.write(row,column,qs.DYStaffName)

                column = column + 1
                sheet.write(row,column,qs.ClothingSystem1)

                column = column + 1
                sheet.write(row, column, qs.ClothingSystem2)

                column = column + 1
                sheet.write(row, column, qs.ClothingSystem3)

                column = column + 1
                sheet.write(row,column,qs.JZLStaffName)

                column = column + 1
                sheet.write(row,column,qs.SpecialSell)

        filename = request.user.username + '_' + ddtime.now().strftime('%Y%m%d%H%M%S') + '.xls'
        w.save(path + '/' + filename)
        os.popen(r'chmod 777 %s' % (path + '/' + filename))

        # 上传oss对象
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT, BUCKETNAME_XLS)
        bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)
        # 删除现有的
        for object_info in oss2.ObjectIterator(bucket,prefix='%s/%s_' % (request.user.username, request.user.username)):
            bucket.delete_object(object_info.key)
        bucket.put_object(u'%s/%s' % (request.user.username, filename), open(path + '/' + filename))

        messages.error(request, u'%s%s.%s/%s/%s' % (PREFIX, BUCKETNAME_XLS, ENDPOINT_OUT, request.user.username,
                                                    filename) + u':成功导出,可点击Download下载到本地............................。')

    to_excel_old.short_description = u'导出EXCEL'

    def department_use_log(self,obj):
        rt = ''
        t_product_depart_use_objs = t_product_depart_use.objects.filter(pid=obj.id).order_by('DepartmentID')
        for t_product_depart_use_obj in t_product_depart_use_objs:
            rt = u'%s{%s-%s},'%(rt,t_product_depart_use_obj.DepartmentID,t_product_depart_use_obj.StaffName)
        return rt
    department_use_log.short_description = u'部门领用记录'
 
    def user_log(self,obj):
        t_product_depart_get_user_objs = t_product_depart_get_user.objects.filter(pid=obj.id).order_by('id')
        rt = ''
        sum = 0
        for t_product_depart_get_user_obj in t_product_depart_get_user_objs:
            sum += 1
            rt += u'<font color="red">%s</font>.%s&nbsp;&nbsp;&nbsp;%s<br>'%(sum,t_product_depart_get_user_obj.StaffName,str(t_product_depart_get_user_obj.LYTime)[0:10])
        #t_product_enter_ed_user.objects.filter(id=obj.id).update(UserCount=sum)
        obj.UserCount = sum
        obj.save()           
        return mark_safe(rt)
    user_log.short_description = u'------个人领用记录------'

    def to_depart_get(self, request, queryset):
        #from datetime import datetime
        for querysetid in queryset.all():
            if querysetid.MGProcess in ('2','3','6'):
                #个人领用过
                old_objs = t_product_depart_get_user.objects.filter(pid = querysetid.id,GetStaffID=request.user.username)
                if not old_objs.exists():
                    obj = t_product_depart_get_user()
                    obj.__dict__ = querysetid.__dict__
                    obj.GetStaffID = request.user.username
                    obj.StaffName = request.user.first_name
                    obj.SalesAttr = obj.StaffName
                    obj.DepartmentID = None
                    obj.pid = querysetid.id
                    obj.LYTime = ddtime.now()
                    obj.PublishedInfo = ''
                    obj.PublishedA = ''
                    obj.id = None
                    obj.save()
                else:
                    messages.info(request,u'你已经领用,无须重复领用！')
            else:
                messages.error(request,u'图片还没有完成，不允许领用。MainSKU:%s'%querysetid.MainSKU)
    to_depart_get.short_description = u'个人领用'




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

    def show_sku(self,obj):
        t_product_mainsku_sku_objs = t_product_mainsku_sku.objects.filter(pid=obj.id).order_by('SKU')
        rts = ''
        try:
            for t_product_mainsku_sku_obj in t_product_mainsku_sku_objs:
                rts = rts + u'%s,<br>'%t_product_mainsku_sku_obj.SKU
            return mark_safe(rts)
        except:
            return mark_safe(rts)
    show_sku.short_description = u'子SKU信息'

    def endtime_PZ_MG(self,obj):
        rt = ''
        if obj.MGProcess == '0' or obj.MGProcess == '1':
            pass
        elif obj.MGProcess == '2' or obj.MGProcess == '3':
            if obj.YNphoto == '0':
                photo_objs = t_product_photograph.objects.filter(pid=obj.id).order_by('MainSKU')
                if photo_objs.exists():
                    rt = u'%s%s'%(rt,photo_objs[0].PZTime)
            elif obj.YNphoto == '1':
                MG_objs = t_product_art_ing.objects.filter(id=obj.id).order_by('MainSKU')
                if MG_objs.exists():
                    rt = u'%s%s'%(rt,MG_objs[0].MGTime)
        return rt
    endtime_PZ_MG.short_description = u'图片完成时间'

    def department_get_log(self,obj):
        rt=''
        t_product_depart_get_objs = t_product_depart_get.objects.filter(pid=obj.id).order_by('GetStaffID')
        for t_product_depart_get_obj in t_product_depart_get_objs:
            rt = u'%s%s:%s<br>%s,<br>'%(rt,t_product_depart_get_obj.GetStaffID,t_product_depart_get_obj.StaffName,str(t_product_depart_get_obj.LYTime)[0:10])
        return mark_safe(rt)
    department_get_log.short_description = u'个人领用记录'

    def show_more_information(self,obj):
        rt = u'商品名称(中文):%s <br><span style="color:green;cursor: pointer;" id="more_id_%s">更 多</span>' % (
        obj.Name2, obj.id)
        rt = u"%s<script>$('#more_id_%s').on('click',function()" \
             u"{layer.open({type:2,skin:'layui-layer-lan',title:'更多信息'," \
             u"fix:false,shadeClose: true,maxmin:true,area:['1500px','300px'],btn: ['关闭页面']," \
             u"content:'/more_product_informations/?flag_obj=%s&flag=t_product_enter_ed',});" \
             u"});</script>" % (rt, obj.id, obj.id)
        return mark_safe(rt)
    show_more_information.short_description = u'<span style="color:#428bca;">商品信息</span>'

    list_display= ('id','MainSKU','DYStaffName','user_log','MGProcess','MGTime',
                   'show_SourcePicPath','SpecialSell','show_more_information',
                   'ClothingNote','ShelveDay','OrdersLast7Days',
                   'show_SourcePicPath2','SpecialRemark','show_urls',)
    list_editable = ('SpecialSell','SpecialRemark','ClothingNote',)
    readonly_fields = ('SourcePicPath','SourcePicPath2','Pricerange','OrdersLast7Days',)
    #list_display= ('id','JZLTime','JZLStaffName','show_SourcePicPath2','MainSKU','show_skulist','Keywords','Keywords2','Pricerange','SupplierPUrl1','SupplierPDes','UnitPrice','Weight','SpecialSell','show_oplog','department_get_log',)
    #list_display_links=('id','SourcePicPath2','Keywords','Keywords2','Pricerange','SupplierPUrl1','SupplierPDes','UnitPrice','Weight','SpecialSell',)
    # 分组表单
    list_filter = ()
    #list_display_links = ('',)
    # list_filter = ('UpdateTime',
    #                 'Weight',
    #                 'Electrification','Powder','Liquid','Magnetism','Buyer',
    #                 'Storehouse',
    #                 'DYStaffName','KFStaffName','XJStaffName','JZLStaffName','JZLTime','PZTime','PZStaffName','MGTime','MGStaffName','LRStaffName','LargeCategory',
    #                 'YNphoto','MGProcess',
    #                 )
    search_fields = ()
    # search_fields = ('id','SKU','MainSKU','Keywords','Keywords2','StaffID','Name','Name2','Material',
    #                 'PlatformName','SourcePicRemark','SupplierID','SupplierArtNO','SupplierPColor','SupplierPDes',
    #                 'SourceURL','SupplierPUrl1','SupplierPUrl2',
    #                 'SpecialRemark','Remark' ,'InitialWord',
    #                 'Buyer','SupplierContact','Storehouse','Tags',
    #                 'possessMan2','LargeCategory','ReportName','ReportName2','PrepackMark',
    #                 'DYStaffName','DYSHStaffName','XJStaffName','KFStaffName','JZLStaffName',
    #                 'PZStaffName','MGStaffName','LRStaffName','YNphoto','MGProcess',
    #                 )
    search_fields =None
    fields = ('SourceURL','OrdersLast7Days','Keywords','Keywords2','SpecialRemark',
              'Pricerange','ShelveDay','Name','Tags', #u'调研结果',
              'SupplierPUrl1','SupplierPDes','SupplierID', # u'开发结果',
              'UnitPrice','Weight','SpecialSell', #u'询价结果',
              'Name2','Material','Unit','MinOrder','SupplierArtNO',
              'SupplierPColor','SupplierPUrl2','OrderDays','StockAlarmDays','LWH',
              'SupplierContact','Storehouse','ReportName','ReportName2','MinPackNum',#建资料
              # 'Electrification','Powder','Liquid','Magnetism',  #u'违禁品',
              'ContrabandAttribute',
              'Remark', #备注
              'MainSKU', #主SKU
              'DYTime','DYStaffName','DYSHTime','DYSHStaffName','XJTime','XJStaffName','KFTime','KFStaffName','JZLTime','JZLStaffName',
              'PZTime','PZStaffName','MGTime','MGStaffName','LRTime','LRStaffName','ClothingSystem1','ClothingSystem2','ClothingSystem3',
              )

    form_layout = (
        Fieldset(u'调研结果',
                    Row('SourceURL','OrdersLast7Days','Pricerange'),
                    Row('Keywords','Keywords2','Tags'),
                    Row('ShelveDay','Name','SpecialRemark'),
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
                    css_class = 'unsort '
                ),
        Fieldset(u'违禁品',
                    # Row('Electrification','Powder','Liquid','Magnetism'),
                    Row('ContrabandAttribute',),
                    css_class = 'unsort '
                ),
        Fieldset(u'备注信息',
                    Row('Remark'),
                    css_class = 'unsort '
                ),
        Fieldset(u'主SKU信息',
                    Row('MainSKU'),
                    css_class = 'unsort '
                ),

                  )
    show_detail_fields = ['id']
    #def save_model(self, request, obj, form, change):
    def save_models(self):
        pass

    def get_list_queryset(self,):
        from django.db.models import Q
        from skuapp.table.t_sys_staff_auth import t_sys_staff_auth
        logger = logging.getLogger('sourceDns.webdns.views')
        request = self.request
        flagcloth = request.GET.get('classCloth', '')
        qs = super(t_product_enter_ed_user_Admin, self).get_list_queryset()
        
        Cate1 = request.GET.get('cate1','')
        Cate2 = request.GET.get('cate2','')
        Cate3 = request.GET.get('cate3','')
        # Electrification = request.GET.get('Electrification', '')
        # Powder = request.GET.get('Powder','')
        # Liquid = request.GET.get('Liquid','')
        # Magnetism = request.GET.get('Magnetism','')
        ContrabandAttribute = request.GET.get('ContrabandAttribute', '')
        Storehouse = request.GET.get('Storehouse','')
        LargeCategory = request.GET.get('LargeCategory','')
        MainSKU = request.GET.get('MainSKU','')
        MainSKU = MainSKU.split(',')
        if '' in MainSKU:
            MainSKU=''
        #messages.error(request,'......%s'%MainSKU)

        YNphoto = request.GET.get('YNphoto','') # 图片处理 0实拍 1制作 
        MGProcess = request.GET.get('MGProcess','')#图片状态 0待实拍 1待制作 2完成实拍 3完成制作 4错误
        
        DYStaffName = request.GET.get('DYStaffName','')#调研员
        DYSHStaffName = request.GET.get('DYSHStaffName','')#调研审核员
        XJStaffName = request.GET.get('XJStaffName','')#询价员
        KFStaffName = request.GET.get('KFStaffName','')#开发员
        MGStaffName = request.GET.get('MGStaffName','')#美工员 
        Buyer = request.GET.get('Buyer','')#采购员
        CreateStaffName = request.GET.get('CreateStaffName','')#创建人
        LRStaffName = request.GET.get('LRStaffName','')#录入员
        PlatformName = request.GET.get('PlatformName','')#反向链接平台
        
        KFTimeStart = request.GET.get('KFTimeStart','')#开发时间
        KFTimeEnd = request.GET.get('KFTimeEnd','')
        
        JZLTimeStart = request.GET.get('JZLTimeStart','')#建资料时间
        JZLTimeEnd = request.GET.get('JZLTimeEnd','')

        MGTimeStart = request.GET.get('MGTimeStart','')#图片完成时间
        MGTimeEnd = request.GET.get('MGTimeEnd','')
        
        WeightStart = request.GET.get('WeightStart','')#克重
        WeightEnd = request.GET.get('WeightEnd','')

        keywords = request.GET.get('keywords', '')  # 关键词EN
        keywords2 = request.GET.get('keywords2', '')  # 关键词CH

        jZLStaffName = request.GET.get('jZLStaffName', '')  # 建资料员
        MainSKUPrefix = request.GET.get('MainSKUPrefix','') # 主SKU前缀搜索

        LRTimeStart = request.GET.get('LRTimeStart','') # 录入时间
        LRTimeEnd = request.GET.get('LRTimeEnd','') # 录入时间
        
        UserCount = request.GET.get('UserCount','') # 个人领用次数


        searchList = {'ContrabandAttribute__exact':ContrabandAttribute, 'Storehouse__exact':Storehouse,'MainSKU__in':MainSKU, 'LargeCategory__exact': LargeCategory,
                      'YNphoto__exact': YNphoto,'MGProcess__exact': MGProcess,'DYStaffName__exact': DYStaffName,'DYSHStaffName__exact': DYSHStaffName,
                      'XJStaffName__exact': XJStaffName,'KFStaffName__exact': KFStaffName,'MGStaffName__exact': MGStaffName,'Buyer__exact': Buyer,
                      'CreateStaffName__exact': CreateStaffName,'LRStaffName__exact': LRStaffName, 'JZLStaffName__exact':jZLStaffName,
                      'KFTime__gte': KFTimeStart, 'KFTime__lt': KFTimeEnd,'JZLTime__gte': JZLTimeStart, 'JZLTime__lt': JZLTimeEnd,
                      'MGTime__gte': MGTimeStart, 'MGTime__lt': MGTimeEnd,'Weight__gte': WeightStart, 'Weight__lt': WeightEnd,
                      'ClothingSystem1__exact':Cate1,'ClothingSystem2__exact': Cate2,'ClothingSystem3__exact':Cate3,
                      'PlatformName__exact':PlatformName, 'MainSKU__startswith':MainSKUPrefix,
                      'LRTime__gte': LRTimeStart, 'LRTime__lt': LRTimeEnd, 'UserCount__exact':UserCount,
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
        if keywords:
            qs = qs.filter(Q(Name__icontains=keywords) | Q(Keywords__icontains=keywords))
        if keywords2:
            qs = qs.filter(Q(Name2__icontains=keywords2) | Q(Keywords2__icontains=keywords2))
        
        flag = 0
        try:
            flag = t_sys_staff_auth.objects.filter(StaffID=request.user.username,urltable="t_product_enter_ed").count()
        except:
            pass
        if request.user.is_superuser or flag != 0:
            qs = qs
        else:
            cc_lis = []
            cur = conn.cursor()
            sql = 'SELECT SKU,count(SKU) from t_product_depart_get_user group by SKU'
            cur.execute(sql)
            rows = cur.fetchall()
            for row in rows:
                if int(row[1]) >=10:
                    cc_lis.append(str(row[0]))
            sku_list = t_product_depart_get_user.objects.filter(GetStaffID=request.user.username).values_list('SKU')        
                    
            if len(cc_lis) == 0:
                qs = qs.exclude(SKU__in=sku_list)
            else:
                qs = qs.exclude(SKU__in=cc_lis).exclude(SKU__in=sku_list)
            cur.close()
            conn.close()

        catelist = [u'001.时尚女装', u'002.时尚男装', u'021.泳装', u'024.童装', u'025.内衣']

        if flagcloth == '1':
            return qs.filter(LargeCategory__in=catelist)
        elif flagcloth == '2':
            return qs.exclude(LargeCategory__in=catelist)
        else:
            return qs
        
