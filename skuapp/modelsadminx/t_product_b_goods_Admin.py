#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-14 13:01:30
# @Author  : ZhangYu (292724306@qq.com)
# @Link    : https://github.com/vissssa
# @Version : $Id$

from .t_product_Admin import *
from skuapp.table.t_product_b_goods_all_productsku import *
from skuapp.table.B_PackInfo import *
import logging
from skuapp.table.t_product_mainsku_sku import *
# from skuapp.table.b_goodsskulinkshop import *
# from skuapp.table.t_main_pic_public import *
from pyapp.models import *
import re

class t_product_b_goods_Admin(object):
    search_box_flag = True

    def show_Picture(self, obj):
        rt = ''
        picture=''
        # t_main_pic_public_objs = t_main_pic_public.objects.filter(MainSKU=obj.MainSKU)
        # for t_main_pic_public_obj in t_main_pic_public_objs:
        db_conn = MySQLdb.Connect(DATABASES['default']['HOST'], DATABASES['default']['USER'],
                                  DATABASES['default']['PASSWORD'], db='pic_db')
        if db_conn:
            cursor = db_conn.cursor()
            pictureSql = "Select OssPath from t_main_pic_public WHERE MainSKU ='%s'" % obj.MainSKU
            cursor.execute(pictureSql)
            pictures = cursor.fetchone()
            if pictures:
                picture = pictures[0]
            if cursor:
                cursor.close()
            db_conn.close()

        rt = '<img src="%s"  width="120" height="120"  alt = "%s"  title="%s"  />  ' %(picture, picture, picture)
        return mark_safe(rt)
    show_Picture.short_description = mark_safe('<p align="center">图片</p>')

    def show_sku(self, obj):
        # rt = '<table  style="text-align:center"><tr><th style="text-align:center">子SKU-</th><th style="text-align:center">服装类信息</th></tr>'
        rt = '<table  style="text-align:center" border="1" cellpadding="1" cellspacing="1" bgcolor="#c1c1c1">' \
             '<tr><th style="text-align:center" width=100px>&nbsp&nbspSKU-&nbsp&nbsp</th><th style="text-align:center" width=100px>' \
             '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp-属性-&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</th><th style="text-align:center">-单价-</th>' \
             '<th style="text-align:center" width=250px>-包装规格-</th>' \
             '<th style="text-align:center">-内包装成本-</th><th style="text-align:center">-最小包装数-</th>' \
             '<th style="text-align:center">-服装类信息-</th><th style="text-align:center">-商品状态-</th></tr>'
        t_product_b_goods_all_productsku_objs = t_product_b_goods_all_productsku.objects.filter(MainSKU=obj.MainSKU)
        # logger = logging.getLogger('sourceDns.webdns.views')
        i = 0
        for t_product_b_goods_all_productsku_obj in t_product_b_goods_all_productsku_objs:
            if i < 5:
                rt =  '%s <tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr> '\
                    % (rt, t_product_b_goods_all_productsku_obj.SKU, t_product_b_goods_all_productsku_obj.GoodsName, t_product_b_goods_all_productsku_obj.RetailPrice,
                         t_product_b_goods_all_productsku_obj.PackName, t_product_b_goods_all_productsku_obj.PackFee, t_product_b_goods_all_productsku_obj.PackageCount, t_product_b_goods_all_productsku_obj.Style,t_product_b_goods_all_productsku_obj.GoodsStatus)
                i += 1
        if len(t_product_b_goods_all_productsku_objs) > 5:
            rt = '%s<tr><td><a id="link_NID_%s">查看更多</a></td></tr>' % (
                rt, obj.id)
        rt = "%s</table><script>$('#link_NID_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'查看全部',fix:false,shadeClose: true,maxmin:true,area:['805px','500px'],content:'/t_product_mainsku_all/SKUB/?abc=%s',});});</script>" % (
            rt, obj.id, obj.MainSKU)
        return mark_safe(rt)
        # PackName = ''
        # CostPrice = 0
        # PackNID = t_product_mainsku_sku_obj.PackNID
        # logger.error(
        #     "PackNIDPackNIDPackNIDPackNIDPackNIDPackNID %s" % (PackNID))
        # try:
        #     if PackNID > 0:
        #         B_PackInfo_obj = B_PackInfo.objects.get(id__exact=PackNID)  #严格对比 ==  id=PackNID
        #         if B_PackInfo_obj is not None:
        #             PackName = B_PackInfo_obj.PackName
        #             CostPrice = B_PackInfo_obj.CostPrice
        # except Exception, ex:
        #     logger.error(
        #         "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx %s =%s" % (Exception, ex))
    show_sku.short_description = mark_safe('<p align="center"> 子SKU信息</p>')

    def show_shopSKU(self,obj):
        rt =  "<a id=show_shopSKU_%s><p align='center'>查看</p></a><script>$('#show_shopSKU_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'查看全部',fix:false,shadeClose: true,maxmin:true,area:['500px','600px'],content:'/t_product_b_goods_shopSKU/shopSKU/?aID=%s',});});</script>"%(obj.id,obj.id,obj.MainSKU)
        return mark_safe(rt)
    show_shopSKU.short_description = mark_safe("<p align='center'>店铺SKU信息</p>")
    list_display= ('id', 'MainSKU', 'show_Picture', 'show_sku', 'Material','UnitPrice','Storehouse','KFStaffName', 'JZLStaffName','Buyer','DeclaredValue','MarketPrice','SalePrice','SupplierID', 'OrderDays', 'ReportName', 'ReportName2', 'SupplierID', 'StockAlarmDays', 'Remark','show_shopSKU')
    # list_editable = ('Remark',)
    # 分组表单
    # list_filter = ()
    # search_fields = ('id','MainSKU', )

    # list_display_links = None
    list_display_links = ("",)
    # fields = ('SourceURL','OrdersLast7Days','Keywords','Keywords2','SpecialRemark',
    #           'Pricerange','ShelveDay','Name','Tags', #u'调研结果',
    #           'SupplierPUrl1','SupplierPDes','SupplierID', # u'开发结果',
    #           'UnitPrice','Weight','SpecialSell', #u'询价结果',
    #           'Name2','Material','Unit','MinOrder','SupplierArtNO',
    #           'SupplierPColor','SupplierPUrl2','OrderDays','StockAlarmDays','LWH',
    #           'SupplierContact','Storehouse','ReportName','ReportName2','MinPackNum',#建资料
    #           'Electrification','Powder','Liquid','Magnetism',  #u'违禁品',
    #           'Remark', #备注
    #           'MainSKU', #主SKU
    #           'DYTime','DYStaffName','DYSHTime','DYSHStaffName','XJTime','XJStaffName','KFTime','KFStaffName','JZLTime','JZLStaffName',
    #           'PZTime','PZStaffName','MGTime','MGStaffName','LRTime','LRStaffName'
    #           )
    #
    # form_layout = (
    #     Fieldset(u'调研结果',
    #                 Row('SourceURL','OrdersLast7Days','Pricerange'),
    #                 Row('Keywords','Keywords2','Tags'),
    #                 Row('ShelveDay','Name','SpecialRemark'),
    #                 css_class = 'unsort '
    #             ),
    #     Fieldset(u'开发&询价',
    #                 Row('SupplierPUrl1','SupplierPDes','SupplierID'),
    #                 Row('UnitPrice','Weight','SpecialSell'),
    #                 css_class = 'unsort  '
    #             ),
    #     Fieldset(u'建资料',
    #                 Row('Name2','Material','Unit'),
    #                 Row('MinOrder','SupplierArtNO', 'SupplierPColor'),
    #                 Row('SupplierPUrl2','OrderDays','StockAlarmDays'),
    #                 Row('LWH', 'SupplierContact','Storehouse'),
    #                 Row('ReportName','ReportName2','MinPackNum'),
    #                 css_class = 'unsort '
    #             ),
    #     Fieldset(u'违禁品',
    #                 Row('Electrification','Powder','Liquid','Magnetism'),
    #                 css_class = 'unsort '
    #             ),
    #     Fieldset(u'备注信息',
    #                 Row('Remark'),
    #                 css_class = 'unsort '
    #             ),
    #     Fieldset(u'主SKU信息',
    #                 Row('MainSKU'),
    #                 css_class = 'unsort '
    #             ),
    #
    #               )
    # show_detail_fields = ['id']

    '''
    因为通过SKU查询MainSKU速度过慢  所以选择通过正则匹配  str[i]是数字且str[i+1]不是数字来匹配的
    
    '''
    def get_list_queryset(self,):
        from django.db.models import Q
        logger = logging.getLogger('sourceDns.webdns.views')
        request = self.request
        flagcloth = request.GET.get('classCloth', '')
        qs = super(t_product_b_goods_Admin, self).get_list_queryset()
        flag = 0
        # Electrification = request.GET.get('Electrification', '')
        # Powder = request.GET.get('Powder','')
        # Liquid = request.GET.get('Liquid','')
        # Magnetism = request.GET.get('Magnetism','')
        ContrabandAttribute = request.GET.get('ContrabandAttribute', '')
        Storehouse = request.GET.get('Storehouse','')
        if(Storehouse == '浦江仓库'):
            Storehouse = ['19']
        if(Storehouse == '亚马逊仓库'):
            Storehouse = ['49']
        if(Storehouse == '海外仓库'):
            Storehouse = ['38']
        if(Storehouse == '其他仓库'):
            Storehouse = ['42','0','23','57','']
        LargeCategory = request.GET.get('LargeCategory','')
        MainSKU = request.GET.get('MainSKU','')
        if MainSKU != '':
            MainSKU = MainSKU.replace("，",",")
            flag = 2
            if ',' in MainSKU:
                MainSKU = MainSKU.split(',')
                flag = 1

        YNphoto = request.GET.get('YNphoto','') # 图片处理 0实拍 1制作
        # MGProcess = request.GET.get('MGProcess','')#图片状态 0待实拍 1待制作 2完成实拍 3完成制作 4错误

        DYStaffName = request.GET.get('DYStaffName','')#调研员



        #根据子SKU获取MainSKU
        MainSKUTmp = ''
        SKU = request.GET.get('SKU','')
        SKU = SKU.replace("，",",")

        ShopSKU = request.GET.get('ShopSKU', '')
        ShopSKU = ShopSKU.replace("，", ",")
        if ShopSKU != "":
            ShopSKU = ShopSKU.split(",")
            for ShopSKU_obj in ShopSKU:
                b_goodsskulinkshop_objs = b_goodsskulinkshop.objects.filter(ShopSKU=ShopSKU_obj)
                for b_goodsskulinkshop_obj in b_goodsskulinkshop_objs:
                    SKUtmp = b_goodsskulinkshop_obj.SKU
                SKU = SKU + "," + SKUtmp

        ShopName_ZY = request.GET.get('ShopName_ZY', '')
        ShopName_ZY = ShopName_ZY.replace("，", ",")
        ShopName_ZY = ShopName_ZY.replace("%2F","/")
        ShopName_ZY = ShopName_ZY.replace("%20", " ")
        # ShopName_ZY = ShopName_ZY.replace(" ","")
        # if r"%2F" in ShopName:
        #     ShopName = ShopName.replace(r"%2F",r"/")
        if ShopName_ZY != "":
            # if "," in ShopName_ZY:
            #     ShopName_ZY = ShopName_ZY.split(",")
            #     for ShopName_ZY_obj in ShopName_ZY:
            #         b_goodsskulinkshop_objs = b_goodsskulinkshop.objects.filter(Memo=ShopName_ZY_obj)
            #         for b_goodsskulinkshop_obj in b_goodsskulinkshop_objs:
            #             SKUtmp1 = b_goodsskulinkshop_obj.SKU
            #             SKU = SKU + "," + SKUtmp1

            # if ',' not in ShopName_ZY:
            b_goodsskulinkshop_objs = b_goodsskulinkshop.objects.filter(Memo=ShopName_ZY)
            for b_goodsskulinkshop_obj in b_goodsskulinkshop_objs:
                SKUtmp1 = b_goodsskulinkshop_obj.SKU
                SKU = SKU + "," + SKUtmp1

        value = re.compile(r'\d')
        value1 = re.compile(r'\D')

        if SKU != '':
            if "," in SKU:
                SKU = SKU.split(",")
                for SKU_obj in SKU:
                    # t_product_b_goods_all_productsku_objs = t_product_b_goods_all_productsku.objects.filter(SKU=SKU_obj)
                    # for t_product_b_goods_all_productsku_obj in t_product_b_goods_all_productsku_objs:
                    #     MainSKUTmp = t_product_b_goods_all_productsku_obj.MainSKU
                    # MainSKUTmp = t_product_b_goods_all_productsku_objs[0]

                    for i in range(0, len(SKU_obj)):
                        rt = SKU_obj[i]
                        if i < (len(SKU_obj) - 1):
                            rt1 = SKU_obj[i + 1]
                            if value.match(rt) and value1.match(rt1):
                                MainSKUTmp=str(SKU_obj[:(i + 1)])
                                break
                    if MainSKUTmp:
                        if flag == 1:
                            MainSKU.append(MainSKUTmp)
                        if flag == 2:
                            # MainSKU = list(MainSKU)
                            # MainSKU.append(MainSKUTmp)
                            MainSKU = MainSKU + ',' + MainSKUTmp
                            MainSKU = MainSKU.split(',')
                            flag = 1
                            continue
                        if flag == 0:
                            MainSKU = MainSKUTmp
                            flag = 2
                            continue




            if "," not in SKU:
                t_product_b_goods_all_productsku_objs = t_product_b_goods_all_productsku.objects.filter(SKU=SKU)
                for t_product_b_goods_all_productsku_obj in t_product_b_goods_all_productsku_objs:
                    MainSKUTmp = t_product_b_goods_all_productsku_obj.MainSKU
                # MainSKUTmp = t_product_b_goods_all_productsku_objs[0]['MainSKU']
                if flag == 1 :
                    MainSKU.append(MainSKUTmp)
                if flag == 2 :
                    MainSKU = MainSKU + ',' + MainSKUTmp
                    MainSKU = MainSKU.split(',')
                    flag = 1
                if flag == 0:
                    MainSKU = MainSKUTmp
                    flag = 2

        GoodsStatus = request.GET.get('GoodsStatus','')#商品状态

        DYSHStaffName = request.GET.get('DYSHStaffName','')#调研审核员
        XJStaffName = request.GET.get('XJStaffName','')#询价员
        KFStaffName = request.GET.get('KFStaffName','')#开发员
        MGStaffName = request.GET.get('MGStaffName','')#美工员
        Buyer = request.GET.get('Buyer','')#采购员
        CreateStaffName = request.GET.get('CreateStaffName','')#创建人
        LRStaffName = request.GET.get('LRStaffName','')#录入员

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

        SupplierID = request.GET.get('SupplierID', '') #供应商名称

        CreateTimeStart = request.GET.get('CreateTimeStart','') #创建时间
        CreateTimeEnd = request.GET.get('CreateTimeEnd','')

        ReportName = request.GET.get('ReportName','')  #英文申报名
        ReportName2 = request.GET.get('ReportName2','') #英文申报名

        searchList = {'ContrabandAttribute__exact':ContrabandAttribute,
                      'Storehouse__in':Storehouse,'LargeCategory__contains': LargeCategory,
                      'YNphoto__exact': YNphoto,'GoodsStatus__exact': GoodsStatus,'DYStaffName__exact': DYStaffName,'DYSHStaffName__exact': DYSHStaffName,
                      'XJStaffName__exact': XJStaffName,'KFStaffName__exact': KFStaffName,'MGStaffName__exact': MGStaffName,'Buyer__exact': Buyer,
                      'CreateStaffName__exact': CreateStaffName,'LRStaffName__exact': LRStaffName, 'JZLStaffName__exact':jZLStaffName,
                      'KFTime__gte': KFTimeStart, 'KFTime__lt': KFTimeEnd,'JZLTime__gte': JZLTimeStart, 'JZLTime__lt': JZLTimeEnd,
                      'MGTime__gte': MGTimeStart, 'MGTime__lt': MGTimeEnd,'Weight__gte': WeightStart, 'Weight__lt': WeightEnd,'Keywords__icontains':keywords,
                      'Keywords2__icontains':keywords2, 'SupplierID__contains':SupplierID, 'CreateTime__gte':CreateTimeStart, 'CreateTime__lt':CreateTimeEnd,
                      'ReportName':ReportName, 'ReportName2':ReportName2
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
                if flag == 1:
                    qs = qs.filter(**sl).filter(MainSKU__in=MainSKU)
                if flag == 2:
                    qs = qs.filter(**sl).filter(MainSKU__exact=MainSKU)
                if flag == 0:
                    qs = qs.filter(**sl)
            except Exception,ex:
                messages.error(request,u'输入的查询数据有问题！')


        if request.user.is_superuser:
            qs = qs
        else:
            t_sys_department_staff_objs = t_sys_department_staff.objects.filter(StaffID=request.user.username)
            if t_sys_department_staff_objs.exists():
                DepartmentID = t_sys_department_staff_objs[0].DepartmentID

                t_product_depart_get_objs = t_product_depart_get.objects.filter(DepartmentID = DepartmentID)
                id_list = []
                for t_product_depart_get_obj in t_product_depart_get_objs:
                    id_list.append(t_product_depart_get_obj.pid)

                qs = qs.exclude(id__in = id_list)
            else:
                qs = qs

        if flagcloth == '1':
            return qs.filter(Q(LargeCategory=u'001.时尚女装') | Q(LargeCategory=u'002.时尚男装'))
        elif flagcloth == '2':
            return qs.exclude(Q(LargeCategory=u'001.时尚女装') | Q(LargeCategory=u'002.时尚男装'))
        else:
            return qs
