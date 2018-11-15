# coding=utf-8
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from django.utils.safestring import mark_safe
from skuapp.table.t_product_mainsku_sku import *
from skuapp.table.t_product_price_check import *
from skuapp.table.t_product_recycle import t_product_recycle
from skuapp.table.t_sys_department_staff import *
from pyapp.models import b_goods as py_b_goods
from skuapp.table.B_PackInfo import *
from pyapp.models import B_Supplier as skuapp_b_supplier
from datetime import datetime
from .t_product_Admin import *
from oss2 import *
import os
import oss2
import xadmin
import logging
from xadmin.views import BaseAdminPlugin, ListAdminView,ModelFormAdminView,CommAdminView,BaseAdminView
from django.template import loader
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from pyapp.models import B_Supplier as sku_b_supplier
from skuapp.table.t_product_price_check_recycle import *
from django.db.models import F
from skuapp.table.t_product_price_check import *
from datetime import datetime

# 核价信息修改
class t_product_price_check_admin(object):
    downloadxls = True
    show_detail = True
    category_flag = True

    # 显示子SKU
    def show_skulist(self,obj) :
        rt = '<table  style="text-align:center"><tr><th style="text-align:center">子SKU-</th><th style="text-align:center">属性</th></tr>'
        if obj.Source == '录入完成':
            t_product_mainsku_sku_objs = t_product_mainsku_sku.objects.filter(MainSKU=obj.MainSKU).order_by('SKU')
            for t_product_mainsku_sku_obj in t_product_mainsku_sku_objs:
                PackName =''
                CostPrice =0
                PackNID= t_product_mainsku_sku_obj.PackNID
                try:
                    if PackNID > 0 :
                        B_PackInfo_obj = B_PackInfo.objects.get(id__exact = PackNID)
                        if B_PackInfo_obj is not None:
                            PackName =  B_PackInfo_obj.PackName
                            CostPrice = B_PackInfo_obj.CostPrice
                except:
                    pass
                rt =  '%s <tr><td>%s</td><td>%s</td></tr> '%(rt,t_product_mainsku_sku_obj.SKU,t_product_mainsku_sku_obj.SKUATTRS)

        elif obj.Source == '普源信息':
            b_goods_objs = py_b_goods.objects.values('SKU','GoodsName').filter(SKU__startswith=obj.MainSKU)
            for b_goods_obj in b_goods_objs :
                rt =  '%s <tr><td>%s</td><td>%s</td></tr> '%(rt,b_goods_obj['SKU'],b_goods_obj['GoodsName'])

        rt = '%s</table>'%rt
        return mark_safe(rt)
    show_skulist.short_description = mark_safe('<p align="center"> 子SKU</p>')
    
    def show_HJcount(self,obj):
        import datetime
        HJcount = 0
        if obj.XGTime is not None:
            HJcount = t_product_price_check.objects.filter(GoodsSKU=obj.GoodsSKU,Mstatus='完成修改',XGTime__gte=(datetime.datetime.now()+(datetime.timedelta(days=-30))).strftime('%Y-%m-%d %H:%M:%S')).count()
            #messages.error(self.request,'%s--%s'%(obj.GoodsSKU,HJcount))
            t_product_price_check.objects.filter(GoodsSKU=obj.GoodsSKU,Mstatus='完成修改').update(HJcount=HJcount)
        return HJcount
    show_HJcount.short_description = u'30天核价次数'

    def show_goodsName(self, obj):
        goodsName_obj = py_b_goods.objects.filter(SKU=obj.GoodsSKU)
        if len(goodsName_obj) != 0:
            goodsName = goodsName_obj[0].GoodsName
        else:
            goodsName = None
        return goodsName
    show_goodsName.short_description = u'商品名称'

    def floating(self, obj):
        oldPrice = obj.OldPrice  # 普源当前价（成本价）
        newPrice = obj.NowPrice
        if oldPrice == None and newPrice == None:
            percent = '%.2f%%' % 0
        elif oldPrice != None and newPrice == None:
            percent = '%.2f%%' % (-100)
        elif oldPrice == None and newPrice != None:
            percent = '%.2f%%' % 100
        else:
            deltPrice = newPrice-oldPrice
            percent = '%.2f%%' % (deltPrice/oldPrice*100)
        return percent
    floating.short_description = u'浮动百分比'

    def show_PIC(self, obj):
        if obj.SourcePicPath2 == None:
            rt = u''
        else:
            rt = '<img src="%s"  width="120" height="120"  alt = "%s"  title="%s"  />  ' % (
                obj.SourcePicPath2, obj.SourcePicPath2,obj.SourcePicPath2)
        return mark_safe(rt)
    show_PIC.short_description = u'商品图片'

    def show_GoodsSKU(self,obj):
        rt = ''
        SKUList = obj.GoodsSKU.split(';').pop()
        for eachSKU in SKUList:
            rt = eachSKU + ''
        return mark_safe(rt)
    show_GoodsSKU.short_description = u'SKU'

    def show_remarks(self,obj) :
        rt = ''
        objs = t_product_price_check.objects.filter(id = obj.id)
        if objs.exists() and objs[0].remarks is not None:
            rt = u'%s'%objs[0].remarks
        return mark_safe(rt)
    show_remarks.short_description = u'--------销售备注--------'

    list_display = ('GoodsSKU','show_goodsName','HJcount','OldPrice','NowPrice','PricePercent','OldWeight','NowWeight','SQStaffName','SQTime','Mstatus','OldSupplier','NewSupplier','XGStaffName','XGTime','XGcontext','remarks2','show_remarks')

    list_filter = ('GoodsSKU','HJcount','Mstatus', 'SQStaffName','SQTime','XGStaffName', 'XGTime','LQStaffName','LQTime','OldSupplier','NewSupplier')

    search_fields = ('GoodsSKU','SQStaffName','XGStaffName', 'Mstatus','LQStaffName','OldSupplier','NewSupplier')

    actions = ['to_modify','to_finish','to_rebut','to_remark','not_online','to_excel','to_recycle']

    list_display_links = ('id')

    fields = ('GoodsSKU',)

    def to_recycle(self, request, queryset):
        allobj = User.objects.filter(groups__id__in=[17,24])
        userID = []
        for each in allobj:
            userID.append(each.id)
        if (request.user.id in userID) or (request.user.is_superuser == 1):
            for querysetid in queryset.all():
                obj                  = t_product_price_check_recycle()
                obj.id               = querysetid.id
                obj.GoodsSKU         = querysetid.GoodsSKU
                obj.GoodsCode        = querysetid.GoodsCode
                obj.RecycleTime      = datetime.now()
                obj.RecycleStaffName = request.user.first_name
                obj.SQStaffName      = querysetid.SQStaffName
                obj.SQTime           = querysetid.SQTime
                obj.XGStaffName      = querysetid.XGStaffName
                obj.XGTime           = querysetid.XGTime
                obj.LQStaffName      = querysetid.LQStaffName
                obj.LQTime           = querysetid.LQTime
                obj.Mstatus          = querysetid.Mstatus
                obj.OldPrice         = querysetid.OldPrice
                obj.NowPrice         = querysetid.NowPrice
                obj.OldSupplier      = querysetid.OldSupplier
                obj.OldSupplierURL   = querysetid.OldSupplierURL
                obj.NewSupplier      = querysetid.NewSupplier
                obj.NewSupplierURL   = querysetid.NewSupplierURL
                obj.remarks          = querysetid.remarks
                obj.XGcontext        = querysetid.XGcontext
                obj.remarks2         = querysetid.remarks2
                obj.save()
                querysetid.delete()
        else:
            messages.error(request, u'您不是采购组或产品组成员，没有这个权限')
    to_recycle.short_description = u'扔进回收站'

    def to_rebut(self, request, queryset):
        allobj = User.objects.filter(groups__id__in=[6])
        userID = []
        for each in allobj:
            userID.append(each.id)
        if (request.user.id in userID) or (request.user.is_superuser == 1):
            for querysetid in queryset.all():
                if querysetid.Mstatus == '在修改':
                    t_product_price_check.objects.filter(id=querysetid.id).update(Mstatus="驳回", XGStaffName=request.user.first_name,XGTime=datetime.now())
                else:
                    messages.error(request, '对不起！该核价信息不可被驳回')
        else:
            messages.error(request, u'您不是信息组成员，不能执行驳回操作！！')
    to_rebut.short_description = u"驳回(信息组操作)"

    def to_finish(self, request, queryset):
        allobj = User.objects.filter(groups__id__in=[6])
        userID = []
        for each in allobj:
            userID.append(each.id)
        if (request.user.id in userID) or (request.user.is_superuser == 1):
            for querysetid in queryset.all():
                if querysetid.Mstatus == '在修改':
                    t_product_price_check.objects.filter(id=querysetid.id).update(Mstatus="完成修改", XGStaffName=request.user.first_name,XGTime=datetime.now())
                else:
                    messages.error(request, '对不起！该核价信息不可被完成修改')
        else:
            messages.error(request, u'您不是信息组成员，不能执行完成修改操作！！')
    to_finish.short_description = u"完成修改(信息组操作)"

    def not_online(self, request, queryset):
        allobj = User.objects.filter(groups__id__in=[13])
        userID = []
        for each in allobj:
            userID.append(each.id)
        if (request.user.id in userID) or (request.user.is_superuser == 1):
            rr = ''
            qq = ''
            xx = ''
            for querysetid in queryset.all():
                t_product_price_check_objs = t_product_price_check.objects.filter(id=querysetid.id)
                t_sys_department_staff_objs = t_sys_department_staff.objects.filter(StaffID=request.user.username)
                if t_sys_department_staff_objs.exists():
                    rr = t_sys_department_staff_objs[0].DepartmentID  # 部门编号
                    xx = u'%s:%s(%s)' % (rr, request.user.first_name, str(datetime.now())[0:10])  # 现 备注
                    if t_product_price_check_objs.exists() and t_product_price_check_objs[0].remarks is not None:
                        qq = t_product_price_check_objs[0].remarks  # 原 备注
                        t_product_price_check_objs.update(remarks=u'%s<br>%s(不在线)' % (qq, xx))
                    elif t_product_price_check_objs.exists() and t_product_price_check_objs[0].remarks is None:
                        t_product_price_check_objs.update(remarks=u'%s(不在线)' % (xx))

                    if rr == '1':
                        t_product_price_check.objects.filter(id=querysetid.id).update(Dep1=request.user.first_name,Dep1Date=datetime.now(),Dep1Sta='不在线')
                    if rr == '2':
                        t_product_price_check.objects.filter(id=querysetid.id).update(Dep2=request.user.first_name,Dep2Date=datetime.now(),Dep2Sta='不在线')
                    if rr == '3':
                        t_product_price_check.objects.filter(id=querysetid.id).update(Dep3=request.user.first_name,Dep3Date=datetime.now(),Dep3Sta='不在线')
                    if rr == '4':
                        t_product_price_check.objects.filter(id=querysetid.id).update(Dep4=request.user.first_name,Dep4Date=datetime.now(),Dep4Sta='不在线')
                    if rr == '5':
                        t_product_price_check.objects.filter(id=querysetid.id).update(Dep5=request.user.first_name,Dep5Date=datetime.now(),Dep5Sta='不在线')
                else:
                    messages.error(request, '对不起！没有你的部门记录！请联系相关人员')
        else:
            messages.error(request, u'您不是销售组成员，不能执行不在线操作！！')
    not_online.short_description = u'不在线(销售部门操作)'

    def to_remark(self, request, queryset):
        allobj = User.objects.filter(groups__id__in=[13])
        userID = []
        for each in allobj:
            userID.append(each.id)
        if (request.user.id in userID) or (request.user.is_superuser == 1):
            rr = ''
            qq = ''
            xx = ''
            for querysetid in queryset.all():
                t_product_price_check_objs = t_product_price_check.objects.filter(id=querysetid.id)
                t_sys_department_staff_objs = t_sys_department_staff.objects.filter(StaffID=request.user.username)
                if t_sys_department_staff_objs.exists():
                    rr = t_sys_department_staff_objs[0].DepartmentID  # 部门编号
                    xx = u'%s:%s(%s)' % (rr, request.user.first_name, str(datetime.now())[0:10])  # 现 备注
                    if t_product_price_check_objs.exists() and t_product_price_check_objs[0].remarks is not None:
                        qq = t_product_price_check_objs[0].remarks  # 原 备注
                        t_product_price_check_objs.update(remarks=u'%s<br>%s(已备注)' % (qq, xx))
                    elif t_product_price_check_objs.exists() and t_product_price_check_objs[0].remarks is None:
                        t_product_price_check_objs.update(remarks=u'%s(已备注)' % (xx))

                    if rr == '1':
                        t_product_price_check.objects.filter(id=querysetid.id).update(Dep1=request.user.first_name,Dep1Date=datetime.now(),Dep1Sta='不在线')
                    if rr == '2':
                        t_product_price_check.objects.filter(id=querysetid.id).update(Dep2=request.user.first_name,Dep2Date=datetime.now(),Dep2Sta='不在线')
                    if rr == '3':
                        t_product_price_check.objects.filter(id=querysetid.id).update(Dep3=request.user.first_name,Dep3Date=datetime.now(),Dep3Sta='不在线')
                    if rr == '4':
                        t_product_price_check.objects.filter(id=querysetid.id).update(Dep4=request.user.first_name,Dep4Date=datetime.now(),Dep4Sta='不在线')
                    if rr == '5':
                        t_product_price_check.objects.filter(id=querysetid.id).update(Dep5=request.user.first_name,Dep5Date=datetime.now(),Dep5Sta='不在线')
                else:
                    messages.error(request, '对不起！没有你的部门记录！请联系相关人员')
        else:
            messages.error(request, u'您不是销售组成员，不能执行完成备注操作！！')
    to_remark.short_description = u'完成备注(销售部门操作)'

    def to_modify(self, request, queryset):
        allobj = User.objects.filter(groups__id__in=[6])
        userID = []
        for each in allobj:
            userID.append(each.id)
        if (request.user.id in userID) or (request.user.is_superuser == 1):
            for querysetid in queryset.all():
                if querysetid.Mstatus == '待修改' or querysetid.Mstatus == '驳回':
                    if request.user.has_perm('skuapp.change_t_product_price_check'):
                        t_product_price_check.objects.filter(id=querysetid.id).update(Mstatus='在修改', LQTime=datetime.now(),
                                                                                      LQStaffName=request.user.first_name)
                    else:
                        messages.error(request, '对不起！您没有领取的权限！ ID：%s' % querysetid.id)
                elif querysetid.Mstatus == '在修改':
                    messages.error(request, '对不起！信息组已领取，正在修改中！ ID：%s' % querysetid.id)
                elif querysetid.Mstatus == '完成修改':
                    messages.error(request, '对不起！该记录已经完成修改！ ID：%s' % querysetid.id)
        else:
            messages.error(request, u'您不是信息组成员，不能执行领去修改操作！！')
    to_modify.short_description = u'领去修改(信息组操作)'

    def to_excel(self, request, queryset):
        from xlwt import *
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))

        mkdir_p(path)
        os.popen('chmod 777 %s' % (path))

        w = Workbook()
        sheet1 = w.add_sheet('price_check_1')
        sheet1.write(0, 0, u'SKU')
        sheet1.write(0, 1, u'商品编码')
        sheet1.write(0, 2, u'商品名称')
        sheet1.write(0, 3, u'原价')
        sheet1.write(0, 4, u'现价')
        sheet1.write(0, 5, u'申请人')
        sheet1.write(0, 6, u'申请时间')

        sheet2 = w.add_sheet('price_check_2')
        sheet2.write(0, 0, u'SKU')
        sheet2.write(0, 1, u'新供应商名称')
        sheet2.write(0, 2, u'采购人')
        sheet2.write(0, 3, u'责任归属人2')

        sheet3 = w.add_sheet('price_check_3')
        sheet3.write(0, 0, u'SKU')
        sheet3.write(0, 1, u'商品编码')
        sheet3.write(0, 2, u'新采购链接')

        sheet4 = w.add_sheet('price_check_4')
        sheet4.write(0, 0, u'SKU')
        sheet4.write(0, 1, u'商品编码')
        sheet4.write(0, 2, u'商品名称')
        sheet4.write(0, 3, u'原克重')
        sheet4.write(0, 4, u'现克重')

        # 写数据
        row1 = 0
        row2 = 0
        row3 = 0
        row4 = 0

        for qs in queryset:

            b_goods_obj = py_b_goods.objects.filter(SKU=qs.GoodsSKU)
            if b_goods_obj.exists():
                goodsname = b_goods_obj[0].GoodsName
            else:
                goodsname = None

            obj = sku_b_supplier.objects.filter(SupplierName=qs.NewSupplier)
            if obj.exists():
                purchaser = obj[0].SupPurchaser
                possessMan2 = obj[0].Recorder
            else:
                purchaser = ''
                possessMan2 = ''

            row1 = row1 + 1
            column1 = 0
            sheet1.write(row1, column1, qs.GoodsSKU)

            column1 = column1 + 1
            sheet1.write(row1, column1, qs.GoodsCode)

            column1 = column1 + 1
            sheet1.write(row1, column1, goodsname)

            column1 = column1 + 1
            sheet1.write(row1, column1, qs.OldPrice)

            column1 = column1 + 1
            sheet1.write(row1, column1, qs.NowPrice)

            column1 = column1 + 1
            sheet1.write(row1, column1, qs.SQStaffName)

            column1 = column1 + 1
            sheet1.write(row1, column1, u'%s'%qs.SQTime)

            if qs.NewSupplier != '':
                row2 = row2 + 1
                column2 = 0
                sheet2.write(row2, column2, qs.GoodsSKU)

                column2 = column2 + 1
                sheet2.write(row2, column2, qs.NewSupplier)

                column2 = column2 + 1
                sheet2.write(row2, column2, purchaser)

                # 责任归属人2
                column2 = column2 + 1
                sheet2.write(row2, column2, possessMan2)

            if qs.NewSupplier != '' and qs.NewSupplierURL != None:
                row3 = row3 + 1
                column3 = 0
                sheet3.write(row3, column3, qs.GoodsSKU)

                column3 = column3 + 1
                sheet3.write(row3, column3, qs.GoodsCode)

                column3 = column3 + 1
                sheet3.write(row3, column3, qs.NewSupplierURL)
            if qs.NowWeight != '':
                row4 = row4 + 1
                column4 = 0
                sheet4.write(row4, column4, qs.GoodsSKU)

                column4 = column4 + 1
                sheet4.write(row4, column4, qs.GoodsCode)

                column4 = column4 + 1
                sheet4.write(row4, column4, goodsname)

                column4 = column4 + 1
                sheet4.write(row4, column4, qs.OldWeight)

                column4 = column4 + 1
                sheet4.write(row4, column4, qs.NowWeight)

        filename = request.user.username + '_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.xls'
        w.save(path + '/' + filename)
        os.popen(r'chmod 777 %s' % (path + '/' + filename))

        # 上传oss对象
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT, BUCKETNAME_XLS)
        bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)
        # 删除现有的
        for object_info in oss2.ObjectIterator(bucket,
                                               prefix='%s/%s_' % (request.user.username, request.user.username)):
            bucket.delete_object(object_info.key)
        bucket.put_object(u'%s/%s' % (request.user.username, filename), open(path + '/' + filename))

        messages.error(request, u'%s%s.%s/%s/%s' % (PREFIX, BUCKETNAME_XLS, ENDPOINT_OUT, request.user.username,
                                                    filename) + u':成功导出,可点击Download下载到本地............................。')
    to_excel.short_description = u'导出EXCEL'

    def get_list_queryset(self,):
        request = self.request
        qs = super(t_product_price_check_admin, self).get_list_queryset()
        cate = request.GET.get('cate')

        # 价格
        if cate == 'price':
            qs = qs.filter(NowWeight='')
        # 克重
        elif cate == 'weight':
            qs = qs.filter(NowPrice=F('OldPrice'))
        # 两者
        elif cate == 'both':
            qs = qs.exclude(NowWeight='').exclude(NowPrice=F('OldPrice'))
        else:
            qs = qs

        return qs
