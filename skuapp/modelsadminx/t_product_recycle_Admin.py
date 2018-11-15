# -*- coding: utf-8 -*-
from .t_product_Admin import *
class t_product_recycle_Admin(t_product_Admin):
    enter_ed = True
    enter_ed_classification = True
    search_box1_flag = True
    def department_get_log(self,obj):
        rt=''
        t_product_depart_get_objs = t_product_depart_get.objects.filter(pid=obj.id).order_by('DepartmentID')
        for t_product_depart_get_obj in t_product_depart_get_objs:
            rt = u'%s%s:%s<br>%s,<br>'%(rt,t_product_depart_get_obj.DepartmentID,t_product_depart_get_obj.StaffName,str(t_product_depart_get_obj.LYTime)[0:10])
        return mark_safe(rt)
    department_get_log.short_description = u'部门领用记录'

    def show_oplog(self,obj) :
        rt = ''
        t_product_oplog_objs = t_product_oplog.objects.filter(pid=obj.id).order_by('id')
        for t_product_oplog_obj in t_product_oplog_objs:
            rt = u'%s%s:%s,'%(rt,t_product_oplog_obj.StepName,t_product_oplog_obj.OpName)
        return rt
    show_oplog.short_description = u'操作历史'

    # def show_urls(self,obj) :
    #     rt = u'反向:<a href="%s" target="_blank" >%s</a><br>供货商:<a href="%s" target="_blank" >%s</a>'%(obj.SourceURL,obj.SourceURL,obj.SupplierPUrl1,obj.SupplierPUrl1)
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

    list_display= ('id','fromTDel','MainSKU','department_get_log','MGProcess','MGTime','DYTime','DYStaffName','show_SourcePicPath','Name2','Keywords','ClothingSystem1','ClothingSystem2','ClothingSystem3','ClothingNote','Pricerange','ShelveDay','OrdersLast7Days','JZLTime','JZLStaffName','show_SourcePicPath2','SpecialSell','SpecialRemark','show_urls',)
    search_fields = None
    list_filter = None
    def save_models(self):
        pass

    def get_list_queryset(self, ):
        from django.db.models import Q
        logger = logging.getLogger('sourceDns.webdns.views')
        request = self.request
        flagcloth = request.GET.get('classCloth', '')
        qs = super(t_product_recycle_Admin, self).get_list_queryset()

        Cate1 = request.GET.get('cate1', '')
        Cate2 = request.GET.get('cate2', '')
        Cate3 = request.GET.get('cate3', '')
        ContrabandAttribute = request.GET.get('ContrabandAttribute', '')
        Storehouse = request.GET.get('Storehouse', '')
        LargeCategory = request.GET.get('LargeCategory', '')
        MainSKU = request.GET.get('MainSKU', '')
        MainSKU = MainSKU.split(',')
        if '' in MainSKU:
            MainSKU = ''

        YNphoto = request.GET.get('YNphoto', '')  # 图片处理 0实拍 1制作
        MGProcess = request.GET.get('MGProcess', '')  # 图片状态 0待实拍 1待制作 2完成实拍 3完成制作 4错误

        DYStaffName = request.GET.get('DYStaffName', '')  # 调研员
        DYSHStaffName = request.GET.get('DYSHStaffName', '')  # 调研审核员
        XJStaffName = request.GET.get('XJStaffName', '')  # 询价员
        KFStaffName = request.GET.get('KFStaffName', '')  # 开发员
        MGStaffName = request.GET.get('MGStaffName', '')  # 美工员
        Buyer = request.GET.get('Buyer', '')  # 采购员
        CreateStaffName = request.GET.get('CreateStaffName', '')  # 创建人
        LRStaffName = request.GET.get('LRStaffName', '')  # 录入员
        PlatformName = request.GET.get('PlatformName', '')  # 反向链接平台

        KFTimeStart = request.GET.get('KFTimeStart', '')  # 开发时间
        KFTimeEnd = request.GET.get('KFTimeEnd', '')

        JZLTimeStart = request.GET.get('JZLTimeStart', '')  # 建资料时间
        JZLTimeEnd = request.GET.get('JZLTimeEnd', '')

        MGTimeStart = request.GET.get('MGTimeStart', '')  # 图片完成时间
        MGTimeEnd = request.GET.get('MGTimeEnd', '')

        UpdateTimeStart = request.GET.get('UpdateTimeStart', '')  # 更新时间
        UpdateTimeEnd = request.GET.get('UpdateTimeEnd', '')

        WeightStart = request.GET.get('WeightStart', '')  # 克重
        WeightEnd = request.GET.get('WeightEnd', '')

        keywords = request.GET.get('keywords', '')  # 关键词EN
        keywords2 = request.GET.get('keywords2', '')  # 关键词CH

        jZLStaffName = request.GET.get('jZLStaffName', '')  # 建资料员
        MainSKUPrefix = request.GET.get('MainSKUPrefix', '')  # 主SKU前缀搜索

        fromTDel = request.GET.get('fromTDel', '')  # 删除来源

        searchList = {'ContrabandAttribute__exact': ContrabandAttribute, 'Storehouse__exact': Storehouse,
                      'MainSKU__in': MainSKU, 'LargeCategory__exact': LargeCategory,
                      'YNphoto__exact': YNphoto, 'MGProcess__exact': MGProcess, 'DYStaffName__exact': DYStaffName,
                      'DYSHStaffName__exact': DYSHStaffName,
                      'XJStaffName__exact': XJStaffName, 'KFStaffName__exact': KFStaffName,
                      'MGStaffName__exact': MGStaffName, 'Buyer__exact': Buyer,
                      'CreateStaffName__exact': CreateStaffName, 'LRStaffName__exact': LRStaffName,
                      'JZLStaffName__exact': jZLStaffName,
                      'KFTime__gte': KFTimeStart, 'KFTime__lt': KFTimeEnd, 'JZLTime__gte': JZLTimeStart,
                      'JZLTime__lt': JZLTimeEnd,
                      'MGTime__gte': MGTimeStart, 'MGTime__lt': MGTimeEnd, 'Weight__gte': WeightStart,
                      'Weight__lt': WeightEnd,'UpdateTime__gte': UpdateTimeStart, 'UpdateTime__lt': UpdateTimeEnd,
                      'ClothingSystem1__exact': Cate1, 'ClothingSystem2__exact': Cate2, 'ClothingSystem3__exact': Cate3,
                      'PlatformName__exact': PlatformName, 'MainSKU__startswith': MainSKUPrefix,'fromTDel__contains':fromTDel
                      }
        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    sl[k] = v
        if sl is not None:
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'输入的查询数据有问题！')
        if keywords:
            qs = qs.filter(Q(Name__icontains=keywords) | Q(Keywords__icontains=keywords))
        if keywords2:
            qs = qs.filter(Q(Name2__icontains=keywords2) | Q(Keywords2__icontains=keywords2))

        catelist = [u'001.时尚女装', u'002.时尚男装', u'021.泳装', u'024.童装', u'025.内衣']

        if flagcloth == '1':
            return qs.filter(LargeCategory__in=catelist)
        elif flagcloth == '2':
            return qs.exclude(LargeCategory__in=catelist)
        else:
            return qs

