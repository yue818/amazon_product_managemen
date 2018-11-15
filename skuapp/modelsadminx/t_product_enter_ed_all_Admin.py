# -*- coding: utf-8 -*-
from .t_product_Admin import *
from django.db import connection as conn
from skuapp.modelsadminx.t_product_Admin import *

class t_product_enter_ed_all_Admin(t_product_Admin):
    t_product_enter_ed_menu_flag = True
    t_product_enter_ed_all_left_flag = True
    search_box1_flag = True
    # downloadxls = True
    # search_box_flag = True
    list_display= ('id','MainSKU','show_sku_publish','DYStaffName','MGProcess','MGTime',
                   'show_SourcePicPath','SpecialSell','show_more_information','ClothingNote','ShelveDay','OrdersLast7Days',
                   'show_SourcePicPath2','SpecialRemark','show_urls')
    
    list_editable = ('SpecialRemark')

    actions = [
        'batch_Disuse',
        'batch_Edit_Category',
    ]

    def show_oplog(self, obj):
        rt = ''
        t_product_oplog_objs = t_product_oplog.objects.filter(pid=obj.id).order_by('id')
        for t_product_oplog_obj in t_product_oplog_objs:
            rt = u'%s%s:%s,' % (rt, t_product_oplog_obj.StepName, t_product_oplog_obj.OpName)
        return rt
    show_oplog.short_description = u'操作历史'

    
    def show_sku_publish(self,obj):
        #objProducts  = t_product_mainsku_sku.objects.filter(pid=obj.id).values_list('ProductSKU')
        #listProducts = [obj[0] for obj in objProducts]
        #t_log_sku_shopsku_apply_objs = t_log_sku_shopsku_apply.objects.filter(Status='APPLYSUCCESS',MainSKU=obj.MainSKU).exclude(StaffName='UPLOAD').values_list('ShopSKU','StaffName')
        cur = conn.cursor()
        sql = 'SELECT ShopSKU,StaffName from py_db.t_log_sku_shopsku where Status="APPLYSUCCESS" and MainSKU="%s" and StaffName != "UPLOAD" group by StaffName'%obj.MainSKU
        cur.execute(sql)
        rows = cur.fetchall()
        rt = '<table>'
        for t_log_sku_shopsku_apply_obj in rows:
            try:
                user_name = User.objects.filter(first_name=t_log_sku_shopsku_apply_obj[1]).values_list('username',flat=True)[0]
                DepartmentID = t_sys_department_staff.objects.filter(StaffID=user_name).values_list('DepartmentID',flat=True)[0]
            except:
                DepartmentID = '未知部门'
            rt = '%s<tr><td>%s：</td><td>%s</td></tr>' % (rt, DepartmentID, t_log_sku_shopsku_apply_obj[1])

        info = '%s' % rt
        if obj.onebuOperation == '2':
            info = '%s一部弃用<br/>' % info
        if obj.twobuOperation == '2':
            info = '%s二部弃用<br/>' % info
        if obj.threebuOperation == '2':
            info = '%s三部弃用<br/>' % info
        if obj.fourbuOperation == '2':
            info = '%s四部弃用<br/>' % info
        if obj.fivebuOperation == '2':
            info = '%s五部弃用<br/>' % info
        if obj.sixbuOperation == '2':
            info = '%s六部弃用<br/>' % info
        if obj.sevenbuOperation == '2':
            info = '%s七部弃用<br/>' % info
        if obj.eightbuOperation == '2':
            info = '%s八部弃用<br/>' % info
        if obj.ninebuOperation == '2':
            info = '%s九部弃用<br/>' % info
        if obj.tenbuOperation == '2':
            info = '%s十部弃用<br/>' % info
        if obj.elevenbuOperation == '2':
            info = '%s十一部弃用<br/>' % info
        rt = '%s</table>' % info
        rt = '%s<br/><span style="color:green;cursor: pointer;" id="Editcategory_%s_%s">修改品类</span>' % (
        rt, obj.MainSKU, obj.id)
        rt = "%s<script>$('#Editcategory_%s_%s').on('click',function()" \
             "{layer.open({type:2,skin:'layui-layer-lan',title:'修改品类'," \
             "fix:false,shadeClose: true,maxmin:true,area:['1500px','300px'],btn: ['关闭页面']," \
             "content:'/skuapp_getcategory/?flag_id=%s',});" \
             "})</script>;" % (rt, obj.MainSKU, obj.id, obj.id)
        cur.close()
        return mark_safe(rt)
    show_sku_publish.short_description = u'----SKU绑定记录----'

    def show_more_information(self, obj):
        rt = u'商品名称(中文):%s <br><span style="color:green;cursor: pointer;" id="more_id_%s">更 多</span>' % (
            obj.Name2, obj.id)
        rt = u"%s<script>$('#more_id_%s').on('click',function()" \
             u"{layer.open({type:2,skin:'layui-layer-lan',title:'更多信息'," \
             u"fix:false,shadeClose: true,maxmin:true,area:['1500px','300px'],btn: ['关闭页面']," \
             u"content:'/more_product_informations/?flag_obj=%s&flag=t_product_enter_ed',});" \
             u"});</script>" % (rt, obj.id, obj.id)
        return mark_safe(rt)
    show_more_information.short_description = u'<span style="color:#428bca;">商品信息</span>'

    def batch_Disuse(self, request, objs):
        t_sys_department_staff_objs = t_sys_department_staff.objects.filter(StaffID=request.user.username)
        if t_sys_department_staff_objs.count() <= 0:
            messages.error(request, u'你没有员工数据,请联系管理员正确录入员工信息！')
        else:
            for obj in objs:
                if t_sys_department_staff_objs[0].DepartmentID == '1':
                    obj.onebuOperation = '2'
                if t_sys_department_staff_objs[0].DepartmentID == '2':
                    obj.twobuOperation = '2'
                if t_sys_department_staff_objs[0].DepartmentID == '3':
                    obj.threebuOperation = '2'
                if t_sys_department_staff_objs[0].DepartmentID == '4':
                    obj.fourbuOperation = '2'
                if t_sys_department_staff_objs[0].DepartmentID == '5':
                    obj.fivebuOperation = '2'
                if t_sys_department_staff_objs[0].DepartmentID == '6':
                    obj.sixbuOperation = '2'
                if t_sys_department_staff_objs[0].DepartmentID == '7':
                    obj.sevenbuOperation = '2'
                if t_sys_department_staff_objs[0].DepartmentID == '8':
                    obj.eightbuOperation = '2'
                if t_sys_department_staff_objs[0].DepartmentID == '9':
                    obj.ninebuOperation = '2'
                if t_sys_department_staff_objs[0].DepartmentID == '10':
                    obj.tenbuOperation = '2'
                if t_sys_department_staff_objs[0].DepartmentID == '11':
                    obj.elevenbuOperation = '2'
                if t_sys_department_staff_objs[0].DepartmentID == '12':
                    obj.twelvebuOperation = '2'
                if t_sys_department_staff_objs[0].DepartmentID == '13':
                    obj.thirteenbuOperation = '2'
                obj.save()
    batch_Disuse.short_description = u'本部门弃用'

    def batch_Edit_Category(self, request, objs):
        # 批量修改速卖通品类
        result = {'message': False}
        information_title = ['业务流水号', '主SKU', '普元品类', '原品类(以逗号隔开)', '操作', '新的品类']
        result['information_title'] = information_title
        information_list = list()
        ali_list = list()
        for obj in objs:
            flag_id = obj.id
            try:
                from skuapp.table.t_config_aliexpress_pl import t_config_aliexpress_pl
                from aliapp.models import t_erp_aliexpress_shop_info
                LargeCategory = obj.LargeCategory
                Aliexpress_PL = obj.Aliexpress_PL
                aliexpress_l = []
                aliexpress_p_list = []
                aliexpress_data = t_config_aliexpress_pl.objects.all()
                aliexpress_pl = ''

                All_permissions = ['duanxiaodi', 'liucuixian']
                if request.user.is_superuser or request.user.username in All_permissions:
                    if Aliexpress_PL:
                        aliexpress_pl = Aliexpress_PL
                    else:
                        aliexpress_l = []
                        for ali in aliexpress_data:
                            py_pl_list = ali.py_pl.split(';')
                            if LargeCategory in py_pl_list:
                                aliexpress_l.append(ali.aliexpress_pl)
                        if '' in aliexpress_l:
                            aliexpress_l.remove('')
                        if aliexpress_l:
                            aliexpress_pl = ','.join(aliexpress_l)
                            obj.Aliexpress_PL = aliexpress_pl
                            obj.save()
                else:
                    t_sys_department_staff_objs = t_sys_department_staff.objects.filter(StaffID=request.user.username)
                    if t_sys_department_staff_objs.count > 0:
                        if Aliexpress_PL:
                            aliexpress_pl = Aliexpress_PL
                        else:
                            cata_zh_objs = t_erp_aliexpress_shop_info.objects.filter(
                                seller_zh=request.user.first_name).values('cata_zh').distinct()

                            for cata_zh_obj in cata_zh_objs:
                                py_pl_obj = t_config_aliexpress_pl.objects.get(
                                    aliexpress_pl=cata_zh_obj['cata_zh']).py_pl
                                py_pl_list = py_pl_obj.split(';')
                                if LargeCategory in py_pl_list:
                                    aliexpress_p_list.append(cata_zh_obj['cata_zh'])
                            if '' in aliexpress_p_list:
                                aliexpress_p_list.remove('')
                            if aliexpress_p_list:
                                aliexpress_pl = ','.join(aliexpress_p_list)
                                obj.Aliexpress_PL = aliexpress_pl
                                obj.save()
                    else:
                        result['message'] = u'没有权限查看和修改'
                        return render(request, 'skuapp_editcategory.html', context=result)

                aliexpress_list = list()
                for a_d in aliexpress_data:
                    aliexpress_dict = dict()
                    aliexpress_dict['id'] = a_d.aliexpress_pl
                    aliexpress_dict['text'] = a_d.aliexpress_pl
                    aliexpress_list.append(aliexpress_dict)
                information = {
                    'id': flag_id,
                    'MainSKU': obj.MainSKU,
                    'aliexpress_pl': aliexpress_pl,
                    'LargeCategory': LargeCategory
                }
                information_list.append(information)
                ali_dict = {
                    'id': flag_id,
                    'aliexpress_list': aliexpress_list,
                    'LargeCategory': LargeCategory,
                }
                ali_list.append(ali_dict)
            except Exception as e:
                result['message'] = repr(e)
                return render(request, 'skuapp_editcategoryMore.html', context=result)
        result['information'] = information_list
        result['ali_list'] = json.dumps(ali_list)
        result['url'] = request.get_full_path()
        return render(request, 'skuapp_editcategoryMore.html', context=result)
    batch_Edit_Category.short_description = u'批量修改品类'

    def get_list_queryset(self, ):
        from django.db.models import Q
        from skuapp.table.t_sys_staff_auth import t_sys_staff_auth
        from skuapp.table.t_config_aliexpress_pl import t_config_aliexpress_pl
        from aliapp.models import t_erp_aliexpress_shop_info
        logger = logging.getLogger('sourceDns.webdns.views')
        request = self.request
        flagcloth = request.GET.get('classCloth', '')
        qs = super(t_product_enter_ed_all_Admin, self).get_list_queryset()
        # qs = qs.filter(MGProcess__in=[2, 3, 6])
        pub = request.GET.get('pub', '').strip()
        if pub == '':
            qs = qs.all()
        elif pub == '0':
            qs = qs.filter(publish_count__exact=0).exclude(onebuOperation__exact=2).exclude(twobuOperation__exact=2).exclude(threebuOperation__exact=2).exclude(fourbuOperation__exact=2).exclude(fivebuOperation__exact=2).exclude(sixbuOperation__exact=2).exclude(sevenbuOperation__exact=2).exclude(eightbuOperation__exact=2).exclude(ninebuOperation__exact=2).exclude(tenbuOperation__exact=2).exclude(elevenbuOperation__exact=2).exclude(twelvebuOperation__exact=2).exclude(thirteenbuOperation__exact=2)
        elif pub == '1':
            qs = qs.filter(publish_count__exact=1).exclude(onebuOperation__exact=2).exclude(twobuOperation__exact=2).exclude(threebuOperation__exact=2).exclude(fourbuOperation__exact=2).exclude(fivebuOperation__exact=2).exclude(sixbuOperation__exact=2).exclude(sevenbuOperation__exact=2).exclude(eightbuOperation__exact=2).exclude(ninebuOperation__exact=2).exclude(tenbuOperation__exact=2).exclude(elevenbuOperation__exact=2).exclude(twelvebuOperation__exact=2).exclude(thirteenbuOperation__exact=2)
        elif pub == '2':
            qs = qs.filter(publish_count__exact=2).exclude(onebuOperation__exact=2).exclude(twobuOperation__exact=2).exclude(threebuOperation__exact=2).exclude(fourbuOperation__exact=2).exclude(fivebuOperation__exact=2).exclude(sixbuOperation__exact=2).exclude(sevenbuOperation__exact=2).exclude(eightbuOperation__exact=2).exclude(ninebuOperation__exact=2).exclude(tenbuOperation__exact=2).exclude(elevenbuOperation__exact=2).exclude(twelvebuOperation__exact=2).exclude(thirteenbuOperation__exact=2)
        elif pub == '3':
            qs = qs.filter(publish_count__exact=3).exclude(onebuOperation__exact=2).exclude(twobuOperation__exact=2).exclude(threebuOperation__exact=2).exclude(fourbuOperation__exact=2).exclude(fivebuOperation__exact=2).exclude(sixbuOperation__exact=2).exclude(sevenbuOperation__exact=2).exclude(eightbuOperation__exact=2).exclude(ninebuOperation__exact=2).exclude(tenbuOperation__exact=2).exclude(elevenbuOperation__exact=2).exclude(twelvebuOperation__exact=2).exclude(thirteenbuOperation__exact=2)
        elif pub == '4':
            qs = qs.filter(publish_count__gt=3).exclude(onebuOperation__exact=2).exclude(twobuOperation__exact=2).exclude(threebuOperation__exact=2).exclude(fourbuOperation__exact=2).exclude(fivebuOperation__exact=2).exclude(sixbuOperation__exact=2).exclude(sevenbuOperation__exact=2).exclude(eightbuOperation__exact=2).exclude(ninebuOperation__exact=2).exclude(tenbuOperation__exact=2).exclude(elevenbuOperation__exact=2).exclude(twelvebuOperation__exact=2).exclude(thirteenbuOperation__exact=2)
        elif pub == '5':
            qs = qs.filter(Q(onebuOperation__exact=2) | Q(twobuOperation__exact=2) | Q(threebuOperation__exact=2) | Q(fourbuOperation__exact=2) | Q(fivebuOperation__exact=2) | Q(sixbuOperation__exact=2) | Q(sevenbuOperation__exact=2) | Q(eightbuOperation__exact=2) | Q(ninebuOperation__exact=2) | Q(tenbuOperation__exact=2) | Q(elevenbuOperation__exact=2) | Q(twelvebuOperation__exact=2) | Q(thirteenbuOperation__exact=2))

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
        PlatformName = request.GET.get("PlatformName",'')  # 反向链接平台
        SourceURL = request.GET.get('SourceURL', '')  # 反向链接平台
        KFTimeStart = request.GET.get('KFTimeStart', '')  # 开发时间
        KFTimeEnd = request.GET.get('KFTimeEnd', '')

        JZLTimeStart = request.GET.get('JZLTimeStart', '')  # 建资料时间
        JZLTimeEnd = request.GET.get('JZLTimeEnd', '')

        MGTimeStart = request.GET.get('MGTimeStart', '')  # 图片完成时间
        MGTimeEnd = request.GET.get('MGTimeEnd', '')

        WeightStart = request.GET.get('WeightStart', '')  # 克重
        WeightEnd = request.GET.get('WeightEnd', '')

        keywords = request.GET.get('keywords', '')  # 关键词EN
        keywords2 = request.GET.get('keywords2', '')  # 关键词CH

        jZLStaffName = request.GET.get('jZLStaffName', '')  # 建资料员
        MainSKUPrefix = request.GET.get('MainSKUPrefix', '')  # 主SKU前缀搜索

        LRTimeStart = request.GET.get('LRTimeStart', '')  # 录入时间
        LRTimeEnd = request.GET.get('LRTimeEnd', '')  # 录入时间
        BJP_FLAG = request.GET.get('BJP_FLAG', '')

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
                      'Weight__lt': WeightEnd,
                      'ClothingSystem1__exact': Cate1, 'ClothingSystem2__exact': Cate2, 'ClothingSystem3__exact': Cate3,
                      'PlatformName__exact': PlatformName, 'MainSKU__startswith': MainSKUPrefix, 'BJP_FLAG': BJP_FLAG,
                      'LRTime__gte': LRTimeStart, 'LRTime__lt': LRTimeEnd, 'SourceURL__icontains': SourceURL,
                      }
        searchexclude = {}

        AI_FLAG = request.GET.get('AI_FLAG', '')
        if AI_FLAG == '1':
            searchList['AI_FLAG'] = '1'
        elif AI_FLAG == '0':
            searchexclude['AI_FLAG'] = '1'

        IP_FLAG = request.GET.get('IP_FLAG', '')
        if IP_FLAG == '1':
            searchList['IP_FLAG'] = '1'
        elif IP_FLAG == '0':
            searchexclude['IP_FLAG'] = '1'

        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    # if k == 'ShopName__exact':
                    # v = 'Wish-' + v.zfill(4)
                    # messages.error(request, v)
                    sl[k] = v
        if sl is not None:
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl).exclude(**searchexclude)
            except Exception, ex:
                messages.error(request, u'输入的查询数据有问题！')
        if keywords:
            qs = qs.filter(Q(Name__icontains=keywords) | Q(Keywords__icontains=keywords))
        if keywords2:
            qs = qs.filter(Q(Name2__icontains=keywords2) | Q(Keywords2__icontains=keywords2))

        flag = 0
        try:
            flag = t_sys_staff_auth.objects.filter(StaffID=request.user.username, urltable="t_product_enter_ed").count()
        except:
            pass

        catelist = [u'001.时尚女装', u'002.时尚男装', u'021.泳装', u'024.童装', u'025.内衣']

        if flagcloth == '1':
            return qs.filter(LargeCategory__in=catelist)
        elif flagcloth == '2':
            return qs.exclude(LargeCategory__in=catelist)
        else:
            return qs