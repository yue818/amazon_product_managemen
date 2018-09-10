# -*- coding: utf-8 -*-
import sys
defaultencoding = 'utf-8'
from django.utils.safestring import mark_safe
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from skuapp.table.t_product_mainsku_sku import *
from skuapp.table.t_product_information_modify import *
from pyapp.models import b_goods as xxxx
from pyapp.models import b_goods as py_b_goods
from pyapp.models import kc_currentstock
from .t_product_Admin import *
from skuapp.table.t_product_develop_ed import t_product_develop_ed
from skuapp.table.t_product_oplog import t_product_oplog
from django.db.models import Q
from datetime import datetime
from skuapp.table.t_shopsku_information_binding import t_shopsku_information_binding
from skuapp.table.t_online_info_amazon_listing import t_online_info_amazon_listing
from app_djcelery.tasks import amazon_product_refresh

class t_product_modify_ed_Admin(object):
    downloadxls = True
    search_box_flag = True
    enter_ed_classification = True
    def show_skulist_XG(self,obj) :
        rt = '<table  style="text-align:center"><tr><th style="text-align:center">子SKU-</th><th style="text-align:center">属性</th></tr>'
        if obj.Source == '录入完成':
            t_product_mainsku_sku_objs = t_product_mainsku_sku.objects.filter(MainSKU=obj.MainSKU).order_by('SKU')
            for t_product_mainsku_sku_obj in t_product_mainsku_sku_objs:
                rt =  '%s <tr><td>%s</td><td>%s</td></tr> '%(rt,t_product_mainsku_sku_obj.SKU,t_product_mainsku_sku_obj.SKUATTRS)
        elif obj.Source == '普源信息':
            b_goods_objs = py_b_goods.objects.values('SKU','GoodsName').filter(SKU__startswith=obj.MainSKU)
            for b_goods_obj in b_goods_objs :
                rt =  '%s <tr><td>%s</td><td>%s</td></tr> '%(rt,b_goods_obj['SKU'],b_goods_obj['GoodsName'])

        rt = '%s</table>'%rt
        return mark_safe(rt)
    show_skulist_XG.short_description = mark_safe('<p align="center"> 子SKU</p>')

    def show_PIC(self,obj):
        t_product_information_modify_objs = t_product_information_modify.objects.filter(id = obj.id)
        rt = '<img src="%s" width="120" height="120" alt = "%s" title="%s" />'%(t_product_information_modify_objs[0].SourcePicPath2,t_product_information_modify_objs[0].SourcePicPath2,t_product_information_modify_objs[0].SourcePicPath2)
        return mark_safe(rt)
    show_PIC.short_description = u'商品图片'


    def show_SKU_InputBox(self,obj):
        InputBox_list = obj.InputBox.split(',')
        rt = ''
        for InputBox in InputBox_list:
            rt = u'%s%s<br>'%(rt,InputBox)
        return mark_safe(rt)
    show_SKU_InputBox.short_description = u'商品编码'
    
    
    def show_oldvalue(self,obj) :
        oldvalue_list = obj.oldvalue.split(',')
        rt = ''
        for oldvalue in oldvalue_list:
            rt = u'%s%s<br>'%(rt,oldvalue)
        return mark_safe(rt)
    show_oldvalue.short_description = u'旧值'
    
    def show_newvalue(self,obj) :
        newvalue_list = obj.newvalue.split(',')
        rt = ''
        for newvalue in newvalue_list:
            rt = u'%s%s<br>'%(rt,newvalue)
        return mark_safe(rt)
    show_newvalue.short_description = u'新值'
    
    
    def show_remarks(self,obj) :
        rt = ''
        t_product_information_modify_objs = t_product_information_modify.objects.filter(id = obj.id)
        if t_product_information_modify_objs.exists() and t_product_information_modify_objs[0].remarks is not None:
            rt = u'%s'%t_product_information_modify_objs[0].remarks
        return mark_safe(rt)
    show_remarks.short_description = u'销售备注'

    def show_product_messages(self, obj):
        a = 1
        XGcontext = ''
        for i in obj.XGcontext:
            XGcontext += i
            if a % 25 == 0:
                XGcontext += '<br>'
            a += 1
        rt = u'修改描述:%s <br><span style="color:green;cursor: pointer;" id="more_id_%s">更 多</span>' % (
            XGcontext, obj.id)
        rt = u"%s<script>$('#more_id_%s').on('click',function()" \
             u"{layer.open({type:2,skin:'layui-layer-lan',title:'更多信息'," \
             u"fix:false,shadeClose: true,maxmin:true,area:['1500px','450px'],btn: ['关闭页面']," \
             u"content:'/more_product_informations/?flag_obj=%s&flag=t_product_modify_ed',});" \
             u"});</script>" % (rt, obj.id, obj.id)
        return mark_safe(rt)

    show_product_messages.short_description = u'<span style="color:#428bca;">更多信息</span>'
    

    list_display = ('id','MainSKU','show_SKU_InputBox','show_PIC','show_oldvalue','show_newvalue','show_product_messages','DevDate','Select','Mstatus','show_remarks','BHRemark')
    readonly_fields = ('id','SourcePicPath','SourcePicPath2','Pricerange','OrdersLast7Days',)
    search_fields =None

    actions = ['to_excel_all','not_online','to_remark','to_excel','to_excel_old','batch_dis_data_by_api','batch_en_data_by_api']
    
    
    def to_remark(self, request, queryset):
        rr = ''
        qq = ''
        xx = ''
        for querysetid in queryset.all():
            t_product_information_modify_objs = t_product_information_modify.objects.filter(id = querysetid.id) #为了获取该记录原来的‘备注’
            t_sys_department_staff_objs = t_sys_department_staff.objects.filter(StaffID = request.user.username)#为了获取该记录 备注 修改人的 部门编号
            if t_sys_department_staff_objs.exists():
                rr = t_sys_department_staff_objs[0].DepartmentID #部门编号
                xx = u'%s:%s(%s)'%(rr,request.user.first_name,str(datetime.now())[0:10]) #现 备注
                if t_product_information_modify_objs.exists() and t_product_information_modify_objs[0].remarks is not None :
                    qq = t_product_information_modify_objs[0].remarks #原 备注
                    t_product_information_modify_objs.update(remarks = u'%s<br>%s'%(qq,xx))
                elif t_product_information_modify_objs.exists() and t_product_information_modify_objs[0].remarks is None :
                    t_product_information_modify_objs.update(remarks = u'%s'%(xx))
                    
                if rr == '1':
                    t_product_information_modify.objects.filter(id = querysetid.id).update(Dep1=request.user.first_name,Dep1Date=datetime.now(),Dep1Sta='修改完成')
                if rr == '2':
                    t_product_information_modify.objects.filter(id = querysetid.id).update(Dep2=request.user.first_name,Dep2Date=datetime.now(),Dep2Sta='修改完成')
                if rr == '3':
                    t_product_information_modify.objects.filter(id = querysetid.id).update(Dep3=request.user.first_name,Dep3Date=datetime.now(),Dep3Sta='修改完成')
                if rr == '4':
                    t_product_information_modify.objects.filter(id = querysetid.id).update(Dep4=request.user.first_name,Dep4Date=datetime.now(),Dep4Sta='修改完成')
                if rr == '5':
                    t_product_information_modify.objects.filter(id = querysetid.id).update(Dep5=request.user.first_name,Dep5Date=datetime.now(),Dep5Sta='修改完成')
                
            else:
                messages.error(request, '对不起！没有你的部门记录！请联系相关人员')

    to_remark.short_description = u'修改完成(销售部门操作)'
    
    def not_online(self, request, queryset):
        rr = ''
        qq = ''
        xx = ''
        for querysetid in queryset.all():
            t_product_information_modify_objs = t_product_information_modify.objects.filter(id = querysetid.id) #为了获取该记录原来的‘备注’
            t_sys_department_staff_objs = t_sys_department_staff.objects.filter(StaffID = request.user.username)#为了获取该记录 备注 修改人的 部门编号
            if t_sys_department_staff_objs.exists():
                rr = t_sys_department_staff_objs[0].DepartmentID #部门编号
                xx = u'%s:%s(%s)'%(rr,request.user.first_name,str(datetime.now())[0:10]) #现 备注
                if t_product_information_modify_objs.exists() and t_product_information_modify_objs[0].remarks is not None:
                    qq = t_product_information_modify_objs[0].remarks #原 备注
                    t_product_information_modify_objs.update(remarks = u'%s<br>%s(不在线)'%(qq,xx))
                elif t_product_information_modify_objs.exists() and t_product_information_modify_objs[0].remarks is None :
                    t_product_information_modify_objs.update(remarks = u'%s不在线'%(xx))
                    
                if rr == '1':
                    t_product_information_modify.objects.filter(id = querysetid.id).update(Dep1=request.user.first_name,Dep1Date=datetime.now(),Dep1Sta='不在线')
                if rr == '2':
                    t_product_information_modify.objects.filter(id = querysetid.id).update(Dep2=request.user.first_name,Dep2Date=datetime.now(),Dep2Sta='不在线')
                if rr == '3':
                    t_product_information_modify.objects.filter(id = querysetid.id).update(Dep3=request.user.first_name,Dep3Date=datetime.now(),Dep3Sta='不在线')
                if rr == '4':
                    t_product_information_modify.objects.filter(id = querysetid.id).update(Dep4=request.user.first_name,Dep4Date=datetime.now(),Dep4Sta='不在线')
                if rr == '5':
                    t_product_information_modify.objects.filter(id = querysetid.id).update(Dep5=request.user.first_name,Dep5Date=datetime.now(),Dep5Sta='不在线')
                
            else:
                messages.error(request, '对不起！没有你的部门记录！请联系相关人员')

    not_online.short_description = '不在线(销售部门操作)'
    
    
    
    
    def to_excel(self, request, queryset):
        from xlwt import *
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        #if not os.path.exists(path):
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s'%(MEDIA_ROOT + 'download_xls'))

        mkdir_p(path)
        os.popen('chmod 777 %s'%(path))

        w = Workbook()
        sheet = w.add_sheet('information_modify')

        sheet.write(0,0,u'id')
        sheet.write(0,1,u'商品编码')
        sheet.write(0,2,u'商品名称')
        sheet.write(0,3,u'英文Keywords')
        sheet.write(0,4,u'中文Keywords')
        sheet.write(0,5,u'申请人')
        sheet.write(0,6,u'申请时间')
        sheet.write(0,7,u'修改类型')
        sheet.write(0,8,u'修改描述')
        sheet.write(0, 9, u'旧值')
        sheet.write(0, 10, u'新值')
        sheet.write(0, 11, u'销售备注')
        


        #写数据
        row = 0
        for qs in queryset:

            InputBox_list_s = []
            if qs.InputBox is not None:
                InputBox_list_s = qs.InputBox.split(',')
            num = 0
            qs_id = ''
            for InputBox_list_l in  InputBox_list_s:
                if InputBox_list_l.strip()!='':
                    row = row + 1
                    column = 0
                    sheet.write(row,column,qs.id)

                    column = column + 1
                    sheet.write(row, column, InputBox_list_l)  # 商品编码

                    column = column + 1
                    sheet.write(row,column,qs.Name2)

                    column = column + 1
                    sheet.write(row,column,qs.Keywords)

                    column = column + 1
                    sheet.write(row,column,qs.Keywords2)

                    column = column + 1
                    sheet.write(row,column,qs.SQStaffNameing)

                    column = column + 1
                    rt = ''
                    rt = u'%s%s'%(rt,qs.SQTimeing)
                    sheet.write(row,column,u'%s'%rt)

                    column = column + 1
                    if qs.Select == '1':
                       sheet.write(row,column,u'换图片')
                    elif qs.Select == '2':
                         sheet.write(row,column,u'临时下架')
                    elif qs.Select == '3':
                         sheet.write(row,column,u'更改商品信息')
                    elif qs.Select == '4':
                         sheet.write(row,column,u'涨价')
                    elif qs.Select == '5':
                         sheet.write(row,column,u'清仓下架')
                    elif qs.Select == '6':
                         sheet.write(row,column,u'变更业绩归属人2')
                    elif qs.Select == '7':
                         sheet.write(row,column,u'SKU合并')
                    elif qs.Select == '8':
                         sheet.write(row,column,u'重新上架')
                    elif qs.Select == '9':
                         sheet.write(row,column,u'售完下架')
                    elif qs.Select == '10':
                         sheet.write(row,column,u'处理库尾')
                    elif qs.Select == '11':
                         sheet.write(row,column,u'降价')
                    elif qs.Select == '11':
                         sheet.write(row,column,u'降价')
                    elif qs.Select == '12':
                         sheet.write(row,column,u'清仓下架')
                    elif qs.Select == '13':
                         sheet.write(row,column,u'提前备货')
                    elif qs.Select == '14':
                         sheet.write(row,column,u'备面料供应链商品')
                    elif qs.Select == '15':
                         sheet.write(row,column,u'无面料供应链商品')
                    elif qs.Select == '16':
                         sheet.write(row,column,u'供货不稳商品')
                    elif qs.Select == '17':
                         sheet.write(row,column,u'待转供应链')

                    column = column + 1
                    sheet.write(row,column,qs.XGcontext)

                    if qs.newvalue and qs.oldvalue:
                        oldvalues = qs.oldvalue.split(',')
                        newvalues = qs.newvalue.split(',')
                        if not qs_id or not qs_id == qs.id:
                            qs_id = qs.id
                            num = 0
                            oldvalue = oldvalues[num]
                            newvalue = newvalues[num]
                            num += 1
                        else:
                            try:
                                oldvalue = oldvalues[num]
                            except:
                                oldvalue = ''
                            try:
                                newvalue = newvalues[num]
                            except:
                                newvalue = ''
                            num += 1
                    else:
                        oldvalue = ''
                        newvalue = ''

                    column = column + 1
                    sheet.write(row, column, oldvalue)

                    column = column + 1
                    sheet.write(row, column, newvalue)
                    
                    #column = column + 1
                    #sheet.write(row,column,qs.remarks)
                    column = column + 1
                    rt =''
                    rt = u'%s%s'%(rt,qs.remarks)
                    sheet.write(row,column,u'%s'%rt)




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

        messages.error(request,u'%s%s.%s/%s/%s'%(PREFIX,BUCKETNAME_XLS,ENDPOINT_OUT,request.user.username,filename) + u':成功导出,可点击Download下载到本地............................。' )
    to_excel.short_description = u'导出EXCEL(简单模式)'
    
    
    def to_excel_old(self, request, queryset):
        from xlwt import *
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        #if not os.path.exists(path):
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s'%(MEDIA_ROOT + 'download_xls'))

        mkdir_p(path)
        os.popen('chmod 777 %s'%(path))

        w = Workbook()
        sheet = w.add_sheet('information_modify')

        sheet.write(0,0,u'id')
        sheet.write(0,1,u'商品编码')
        sheet.write(0,2,u'商品名称')
        sheet.write(0,3,u'英文Keywords')
        sheet.write(0,4,u'中文Keywords')
        sheet.write(0,5,u'申请人')
        sheet.write(0,6,u'申请时间')
        sheet.write(0,7,u'修改类型')
        sheet.write(0,8,u'修改描述')
        sheet.write(0, 9, u'旧值')
        sheet.write(0, 10, u'新值')
        sheet.write(0, 11, u'销售备注')
        


        #写数据
        row = 0
        for qs in queryset:

            #t_product_mainsku_sku_objs = t_product_mainsku_sku.objects.filter(MainSKU=qs.MainSKU).order_by('SKU')
            #for t_product_mainsku_sku_obj in  t_product_mainsku_sku_objs:
            InputBox_list_s = []
            if qs.InputBox is not None:
                InputBox_list_s = qs.InputBox.split(',')
            num = 0
            qs_id = ''
            for InputBox_list_l in  InputBox_list_s:
                if InputBox_list_l.strip()!='':
                    row = row + 1
                    column = 0
                    sheet.write(row,column,qs.id)

                    column = column + 1
                    sheet.write(row, column, InputBox_list_l)  # 商品编码


                    column = column + 1
                    sheet.write(row,column,qs.Name2)

                    column = column + 1
                    sheet.write(row,column,qs.Keywords)

                    column = column + 1
                    sheet.write(row,column,qs.Keywords2)

                    column = column + 1
                    sheet.write(row,column,qs.SQStaffNameing)

                    column = column + 1
                    rt = ''
                    rt = u'%s%s'%(rt,qs.SQTimeing)
                    sheet.write(row,column,u'%s'%rt)

                    column = column + 1
                    if qs.Select == '1':
                       sheet.write(row,column,u'换图片')
                    elif qs.Select == '2':
                         sheet.write(row,column,u'临时下架')
                    elif qs.Select == '3':
                         sheet.write(row,column,u'更改商品信息')
                    elif qs.Select == '4':
                         sheet.write(row,column,u'涨价')
                    elif qs.Select == '5':
                         sheet.write(row,column,u'清仓下架')
                    elif qs.Select == '6':
                         sheet.write(row,column,u'变更业绩归属人2')
                    elif qs.Select == '7':
                         sheet.write(row,column,u'SKU合并')
                    elif qs.Select == '8':
                         sheet.write(row,column,u'重新上架')
                    elif qs.Select == '9':
                         sheet.write(row,column,u'售完下架')
                    elif qs.Select == '10':
                         sheet.write(row,column,u'处理库尾')
                    elif qs.Select == '11':
                         sheet.write(row,column,u'降价')
                    elif qs.Select == '12':
                         sheet.write(row,column,u'清仓下架')
                    elif qs.Select == '13':
                         sheet.write(row,column,u'提前备货')
                    elif qs.Select == '14':
                         sheet.write(row,column,u'备面料供应链商品')
                    elif qs.Select == '15':
                         sheet.write(row,column,u'无面料供应链商品')
                    elif qs.Select == '16':
                         sheet.write(row,column,u'供货不稳商品')
                    elif qs.Select == '17':
                         sheet.write(row,column,u'待转供应链')

                    column = column + 1
                    sheet.write(row,column,qs.XGcontext)

                    if qs.newvalue and qs.oldvalue:
                        oldvalues = qs.oldvalue.split(',')
                        newvalues = qs.newvalue.split(',')
                        if not qs_id or not qs_id == qs.id:
                            qs_id = qs.id
                            num = 0
                            oldvalue = oldvalues[num]
                            newvalue = newvalues[num]
                            num += 1
                        else:
                            try:
                                oldvalue = oldvalues[num]
                            except:
                                oldvalue = ''
                            try:
                                newvalue = newvalues[num]
                            except:
                                newvalue = ''
                            num += 1
                    else:
                        oldvalue = ''
                        newvalue = ''

                    column = column + 1
                    sheet.write(row, column, oldvalue)

                    column = column + 1
                    sheet.write(row, column, newvalue)
                    
                    #column = column + 1
                    #sheet.write(row,column,qs.remarks)
                    
                    column = column + 1
                    rt =''
                    rt = u'%s%s'%(rt,qs.remarks)
                    sheet.write(row,column,u'%s'%rt)

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

        messages.error(request,u'%s%s.%s/%s/%s'%(PREFIX,BUCKETNAME_XLS,ENDPOINT_OUT,request.user.username,filename) + u':成功导出,可点击Download下载到本地............................。' )
    to_excel_old.short_description = u'导出EXCEL(全部)'

    
    def to_excel_all(self, request, queryset):
        from xlwt import *
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        #if not os.path.exists(path):
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s'%(MEDIA_ROOT + 'download_xls'))

        mkdir_p(path)
        os.popen('chmod 777 %s'%(path))

        w = Workbook()
        sheet = w.add_sheet('information_modify')

        sheet.write(0,0,u'id')
        sheet.write(0,1,u'商品编码')
        sheet.write(0,2,u'商品名称')
        sheet.write(0,3,u'英文Keywords')
        sheet.write(0,4,u'中文Keywords')
        sheet.write(0,5,u'申请人')
        sheet.write(0,6,u'申请时间')
        sheet.write(0,7,u'修改类型')
        sheet.write(0,8,u'修改描述')
        sheet.write(0, 9, u'旧值')
        sheet.write(0, 10, u'新值')
        sheet.write(0, 11, u'销售备注')
       

        #写数据
        row = 0
        for qs in queryset:
            InputBox_list_s = []
            if qs.InputBox is not None:
            #b_goods_objs = py_b_goods.objects.filter(SKU__startswith=qs.MainSKU)
                InputBox_list_s = qs.InputBox.split(',')
            num = 0
            qs_id = ''
            for InputBox_list_l in  InputBox_list_s:
                if InputBox_list_l.strip()!='':
                    row = row + 1
                    column = 0
                    sheet.write(row,column,qs.id)

                    column = column + 1
                    sheet.write(row,column,InputBox_list_l)#商品编码

                    column = column + 1
                    sheet.write(row,column,qs.Name2)

                    column = column + 1
                    sheet.write(row,column,qs.Keywords)

                    column = column + 1
                    sheet.write(row,column,qs.Keywords2)

                    column = column + 1
                    sheet.write(row,column,qs.SQStaffNameing)

                    column = column + 1
                    rt = ''
                    rt = u'%s%s'%(rt,qs.SQTimeing)
                    sheet.write(row,column,u'%s'%rt)

                    column = column + 1
                    if qs.Select == '1':
                       sheet.write(row,column,u'换图片')
                    elif qs.Select == '2':
                         sheet.write(row,column,u'临时下架')
                    elif qs.Select == '3':
                         sheet.write(row,column,u'更改商品信息')
                    elif qs.Select == '4':
                         sheet.write(row,column,u'涨价')
                    elif qs.Select == '5':
                         sheet.write(row,column,u'清仓下架')
                    elif qs.Select == '6':
                         sheet.write(row,column,u'变更业绩归属人2')
                    elif qs.Select == '7':
                         sheet.write(row,column,u'SKU合并')
                    elif qs.Select == '8':
                         sheet.write(row,column,u'重新上架')
                    elif qs.Select == '9':
                        sheet.write(row, column, u'售完下架')
                    elif qs.Select == '10':
                        sheet.write(row, column, u'处理库尾')
                    elif qs.Select == '11':
                         sheet.write(row,column,u'降价')
                    elif qs.Select == '12':
                         sheet.write(row,column,u'清仓下架')
                    elif qs.Select == '13':
                         sheet.write(row,column,u'提前备货')
                    elif qs.Select == '14':
                         sheet.write(row,column,u'备面料供应链商品')
                    elif qs.Select == '15':
                         sheet.write(row,column,u'无面料供应链商品')
                    elif qs.Select == '16':
                         sheet.write(row,column,u'供货不稳商品')
                    elif qs.Select == '17':
                         sheet.write(row,column,u'待转供应链')

                    column = column + 1
                    sheet.write(row,column,qs.XGcontext)
                    
                    if qs.newvalue and qs.oldvalue:
                        oldvalues = qs.oldvalue.split(',')
                        newvalues = qs.newvalue.split(',')
                        if not qs_id or not qs_id == qs.id:
                            qs_id = qs.id
                            num = 0
                            oldvalue = oldvalues[num]
                            newvalue = newvalues[num]
                            num += 1

                        else:
                            try:
                                oldvalue = oldvalues[num]
                            except:
                                oldvalue = ''
                            try:
                                newvalue = newvalues[num]
                            except:
                                newvalue = ''
                            num += 1

                    else:
                        oldvalue = ''
                        newvalue = ''

                    column = column + 1
                    sheet.write(row, column, oldvalue)

                    column = column + 1
                    sheet.write(row, column, newvalue)
                    
                    #column = column + 1
                    #sheet.write(row,column,qs.remarks)
                    
                    column = column + 1
                    rt =''
                    rt = u'%s%s'%(rt,qs.remarks)
                    sheet.write(row,column,u'%s'%rt)


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

        messages.error(request,u'%s%s.%s/%s/%s'%(PREFIX,BUCKETNAME_XLS,ENDPOINT_OUT,request.user.username,filename) + u':成功导出,可点击Download下载到本地............................。' )
    to_excel_all.short_description = u'导出EXCEL'

    def batch_en_data_by_api(self, request, queryset):
        from django.http import HttpResponseRedirect
        import urllib
        import datetime
        print request.user.username
        shop_sku = {}
        sku_select = []
        for record in queryset.all():
            sku_list = record.InputBox.split(',')
            print '0sku_list is: %s' % str(sku_list)
            for sku in sku_list:
                print '     1sku_list ->this sku is:%s' % sku
                sku_bind_obj = t_shopsku_information_binding.objects.filter(SKU=sku)
                for seller_sku_obj in sku_bind_obj:
                    print "         2sku_list ->this sku -> shop_sku is: %s" % seller_sku_obj.ShopSKU
                    amazon_list_obj = t_online_info_amazon_listing.objects.filter(seller_sku=seller_sku_obj.ShopSKU)
                    for list_obj in amazon_list_obj:
                        seller_sku = list_obj.seller_sku
                        shop_name = list_obj.ShopName
                        sku_select.append(seller_sku)
                        print '             3sku_list ->this sku -> shop_sku -> shop_name is: %s' % shop_name
                        if not shop_sku.has_key(shop_name):
                            shop_sku[shop_name] = [seller_sku]
                            print '                 4-1sku_list: shop_sku is:%s ' % str(shop_sku)
                        else:
                            shop_sku[shop_name].append(seller_sku)
                            print '                 4-2sku_list: shop_sku is:%s ' % str(shop_sku)
        print 'shop_sku_dict is:'
        print shop_sku
        print 'sku_select is:%s' % str(sku_select)
        sku_str = ''
        for sku_each in sku_select:
            t_online_info_amazon_listing.objects.filter(seller_sku=sku_each).update(deal_action='load_product', deal_result=None, deal_result_info=None, UpdateTime=datetime.datetime.now())
            sku_str = sku_str + sku_each + ','
        if sku_str == '':
            sku_str = ' '
        else:
            sku_str = sku_str[:-1]
        sku_str = urllib.quote(sku_str.decode('gbk', 'replace').encode('utf-8', 'replace'))
        if shop_sku:
            amazon_product_refresh(shop_sku, 'load_product')
        return HttpResponseRedirect('/Project/admin/skuapp/t_online_info_amazon_listing/?all=&seller_sku=%s' % sku_str)
    batch_en_data_by_api.short_description = u'产品上架'

    def batch_dis_data_by_api(self, request, queryset):
        from django.http import HttpResponseRedirect
        import urllib
        import datetime
        shop_sku = {}
        sku_select = []
        for record in queryset.all():
            sku_list = record.InputBox.split(',')
            for sku in sku_list:
                sku_bind_obj = t_shopsku_information_binding.objects.filter(SKU=sku)
                for seller_sku_obj in sku_bind_obj:
                    amazon_list_obj = t_online_info_amazon_listing.objects.filter(seller_sku=seller_sku_obj.ShopSKU)
                    for list_obj in amazon_list_obj:
                        seller_sku = list_obj.seller_sku
                        shop_name = list_obj.ShopName
                        sku_select.append(seller_sku)
                        if not shop_sku.has_key(shop_name):
                            shop_sku[shop_name] = [seller_sku]
                        else:
                            shop_sku[shop_name].append(seller_sku)
        sku_str = ''
        for sku_each in sku_select:
            t_online_info_amazon_listing.objects.filter(seller_sku=sku_each).update(deal_action='unload_product', deal_result=None, deal_result_info=None, UpdateTime=datetime.datetime.now())
            sku_str = sku_str + sku_each + ','
        if sku_str == '':
            sku_str = ' '
        else:
            sku_str = sku_str[:-1]
        sku_str = urllib.quote(sku_str.decode('gbk', 'replace').encode('utf-8', 'replace'))
        if shop_sku:
            amazon_product_refresh(shop_sku, 'unload_product')
        return HttpResponseRedirect('/Project/admin/skuapp/t_online_info_amazon_listing/?all=&seller_sku=%s' % sku_str)
    batch_dis_data_by_api.short_description = u'产品下架'


    def get_list_queryset(self):
        request = self.request
        qs = super(t_product_modify_ed_Admin,self).get_list_queryset()

        flagcloth = request.GET.get('classCloth', '')
        MainSKU = request.GET.get('MainSKU','')
        DepartmentalState = request.GET.get('DepartmentalState','')   # 部门状态
        Name2 = request.GET.get('Name2','')
        KFTimeStart = request.GET.get('KFTimeStart','')
        KFTimeEnd = request.GET.get('KFTimeEnd','')
        Keywords = request.GET.get('Keywords','')
        Keywords2 = request.GET.get('Keywords2','')
        SQStaffNameing = request.GET.get('SQStaffNameing','')
        SQTimeingStart = request.GET.get('SQTimeingStart','')
        SQTimeingEnd = request.GET.get('SQTimeingEnd','')
        Select = request.GET.get('Select','')
        XGcontext = request.GET.get('XGcontext','')
        Mstatus = request.GET.get('Mstatus','')
        XGStaffName = request.GET.get('XGStaffName','')
        XGTimeStart = request.GET.get('XGTimeStart','')
        XGTimeEnd = request.GET.get('XGTimeEnd','')     
        SHStaffName = request.GET.get('SHStaffName','')
        SKU = request.GET.get('SKU','')

        
        searchList = {'MainSKU__exact': MainSKU, 'Name2__exact': Name2, 
                      'SKU__contains': SKU,   
                      'DevDate__gte': KFTimeStart,'DevDate__lt': KFTimeEnd, 
                      'Keywords__exact':Keywords, 'Keywords2__exact': Keywords2,
                      'SQStaffNameing__exact': SQStaffNameing, 
                      'SQTimeing__gte': SQTimeingStart, 'SQTimeing__lt': SQTimeingEnd,
                      'Select__exact': Select, 'XGcontext__exact': XGcontext,
                      'Mstatus__exact': Mstatus,
                      'XGStaffName__exact': XGStaffName,
                      'XGTime__gte':XGTimeStart,'XGTime__lt':XGTimeEnd,
                      }
        sl = {}
        for k,v in searchList.items():
            if isinstance(v,list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    #if k == 'ShopName__exact':
                      #  v = 'Wish-' + v.zfill(4)
                        # messages.error(request, v)
                    sl[k] = v
        if sl is not None:
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
            except Exception,ex:
                messages.error(request,u'输入的查询数据有问题！')
        
        if DepartmentalState == u'一部已领用':
            qs = qs.filter(Dep1__isnull=False)
        if DepartmentalState == u'一部未领用':
            qs = qs.filter(Dep1__isnull=True)
        if DepartmentalState == u'二部已领用':
            qs = qs.filter(Dep2__isnull=False)
        if DepartmentalState == u'二部未领用':
            qs = qs.filter(Dep2__isnull=True)
        if DepartmentalState == u'三部已领用':
            qs = qs.filter(Dep3__isnull=False)
        if DepartmentalState == u'三部未领用':
            qs = qs.filter(Dep3__isnull=True)
        if DepartmentalState == u'四部已领用':
            qs = qs.filter(Dep4__isnull=False)
        if DepartmentalState == u'四部未领用':
            qs = qs.filter(Dep4__isnull=True)
        if DepartmentalState == u'五部已领用':
            qs = qs.filter(Dep5__isnull=False)
        if DepartmentalState == u'五部未领用':
            qs = qs.filter(Dep5__isnull=True)
            
#        if DepartmentalState == u'全部已领用':
#            qs = qs.filter(Dep1__isnull=False | Dep2__isnull=False | Dep3__isnull=False | Dep4__isnull=False | Dep5__isnull=False )
#        if DepartmentalState == u'全部未领用':
#            qs = qs.filter(Dep1__isnull=True | Dep2__isnull=True | Dep3__isnull=True | Dep4__isnull=True | Dep5__isnull=True | )
        catelist = [u'001.时尚女装', u'002.时尚男装',u'021.泳装', u'024.童装', u'025.内衣']

        if flagcloth == '1':
            qs = qs.filter(LargeCategory__in=catelist)
        elif flagcloth == '2':
            qs = qs.exclude(LargeCategory__in=catelist)
        
        if Mstatus:
            return qs
        else:
            return qs.filter(Q(Mstatus='WCXG')|Q(Mstatus='WCHT'))

