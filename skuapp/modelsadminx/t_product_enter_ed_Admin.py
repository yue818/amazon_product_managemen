# -*- coding: utf-8 -*-
from .t_product_Admin import *
from skuapp.table.t_product_mainsku_sku import t_product_mainsku_sku
import logging
from datetime import datetime as ddtime
from brick.function.formatUrl import format_urls
from skuapp.table.t_product_depart_get_user import t_product_depart_get_user
from pyapp.models import t_log_sku_shopsku_apply
from django.db import connection as conn
from skuapp.table.t_product_mainsku_sku import t_product_mainsku_sku
from brick.classredis.classsku import classsku
from django_redis import get_redis_connection

redis_conn = get_redis_connection(alias='product')

class t_product_enter_ed_Admin(t_product_Admin):
    #enter_ed_user_flag = True
    enter_ed = True
    enter_ed_classification = True
    search_box1_flag = True
    downloadxls = True
    #py_search_system_flag = True
    #actions = ['to_depart_get','to_excel_old']
    actions = ['qy','to_excel_old']


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
    def show_status(self,obj):
        classskuobjs = classsku(connection, redis_conn)
        rt = '<ul>'
        ProductSKU_objs = t_product_mainsku_sku.objects.filter(MainSKU=obj.MainSKU).values_list('ProductSKU',flat=True)
        for ProductSKU in ProductSKU_objs:
            status = classskuobjs.get_goodsstatus_by_sku(ProductSKU)
            rt = '%s<li>%s&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%s</li>'%(rt,ProductSKU,status)
        rt = '%s</ul>'%rt
        return mark_safe(rt)
    show_status.short_description = u'<p align="center"style="color:#428bca;">--------子SKU/状态--------</p>'        

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






    def to_depart_use(self, request, queryset):
        cursor = connection.cursor() #
        for querysetid in queryset.all():

            sku = querysetid.SKU
            if sku != querysetid.MainSKU :
                sku = '%s%s'%(querysetid.MainSKU,querysetid.SKU)

            t_sys_department_staff_objs = t_sys_department_staff.objects.filter(StaffID=request.user.username)
            if  t_sys_department_staff_objs.count() <=  0 :
                messages.error(request,u'你没有员工数据,请联系管理员正确录入员工信息！')
                continue #没找到部门

            dptmtid = t_sys_department_staff_objs[0].DepartmentID
            t_product_depart_use_objs = t_product_depart_use.objects.filter(pid=querysetid.id,DepartmentID=dptmtid)
            if t_product_depart_use_objs.count() > 0 : #已领过
                messages.error(request,u'你没有员工数据,请联系管理员正确录入员工信息！')
                continue
            sql = 'insert into t_product_depart_use(SourcePicPath2,SKU,MainSKU,Name2,DepartmentID,UpdateTime,StaffID,StaffName,pid) '
            sql += ' values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'%(querysetid.SourcePicPath2,sku,querysetid.MainSKU,querysetid.Name2,dptmtid,ddtime.utcnow(),request.user.username,request.user.first_name,querysetid.id)
            cursor.execute(sql)
        cursor.close()
    to_depart_use.short_description = u'本部门领用'

    def department_use_log(self,obj):
        rt = ''
        t_product_depart_use_objs = t_product_depart_use.objects.filter(pid=obj.id).order_by('DepartmentID')
        for t_product_depart_use_obj in t_product_depart_use_objs:
            rt = u'%s{%s-%s},'%(rt,t_product_depart_use_obj.DepartmentID,t_product_depart_use_obj.StaffName)
        return rt
    department_use_log.short_description = u'部门领用记录'

    def to_depart_get(self, request, queryset):
        import copy
        staff_username = request.user.username
        staff_username2 = request.user.first_name
        staff_objs = t_sys_department_staff.objects.filter(StaffID=staff_username)
        if staff_objs.count() <= 0:
            messages.error(request, u'你没有员工数据,请联系管理员正确录入员工信息！')
            return  # 没找到部门

        dptmtid = staff_objs[0].DepartmentID
        for querysetid in queryset.filter(MGProcess__in=['2', '3', '6']):  # 过滤所有图片完成的记录
            objsTmp = copy.deepcopy(querysetid)

            old_objs = t_product_depart_get.objects.filter(pid=objsTmp.id, DepartmentID=dptmtid)
            
            if dptmtid == '6' and objsTmp.KFStaffName in ['吴景景', '刘冉']:
                if staff_username2 not in ['吴景景', '刘冉']:
                    messages.error(request, u'这是刘冉/吴景景 所开发的产品，只能他们可以领用！')
                    return           
            
            if not old_objs.exists():
                obj = t_product_depart_get()
                obj.__dict__ = objsTmp.__dict__
                obj.StaffName = request.user.first_name
                obj.SalesAttr = objsTmp.StaffName
                obj.DepartmentID = dptmtid
                obj.pid = objsTmp.id
                obj.LYTime = ddtime.now()
                obj.PublishedInfo = ''
                obj.PublishedA = ''
                obj.id = None
                obj.save()

                if dptmtid == '1':
                    querysetid.onebuOperation = '1'
                elif dptmtid == '2':
                    querysetid.twobuOperation = '1'
                elif dptmtid == '3':
                    querysetid.threebuOperation = '1'
                elif dptmtid == '4':
                    querysetid.fourbuOperation = '1'
                elif dptmtid == '5':
                    querysetid.fivebuOperation = '1'
                elif dptmtid == '6':
                    querysetid.sixbuOperation = '1'
                elif dptmtid == '7':
                    querysetid.sevenbuOperation = '1'
                elif dptmtid == '8':
                    querysetid.eightbuOperation = '1'
                elif dptmtid == '9':
                    querysetid.ninebuOperation = '1'
                elif dptmtid == '10':
                    querysetid.tenbuOperation = '1'
                elif dptmtid == '11':
                    querysetid.elevenbuOperation = '1'
                elif dptmtid == '12':
                    querysetid.twelvebuOperation = '1'
                elif dptmtid == '13':
                    querysetid.thirteenbuOperation = '1'

                querysetid.save()
            else:
                messages.info(request, u'你部门已经领用/弃用过,无须重复领用！')

            begin_t_product_oplog(request,objsTmp.MainSKU,'BMLY',objsTmp.Name2,objsTmp.id)

    to_depart_get.short_description = u'本部门领用'

    def to_depart_get2(self, request, queryset):
        #from datetime import datetime
        cursor = connection.cursor() #
        for querysetid in queryset.all():
            if querysetid.MGProcess in ('2','3','6'):
                sku = querysetid.SKU
                if sku != querysetid.MainSKU :
                    sku = '%s%s'%(querysetid.MainSKU,querysetid.SKU)
                t_sys_department_staff_objs = t_sys_department_staff.objects.filter(StaffID=request.user.username)
                if  t_sys_department_staff_objs.count() <=  0 :
                    messages.error(request,u'你没有员工数据,请联系管理员正确录入员工信息！')
                    continue #没找到部门
                else:
                    if t_sys_department_staff_objs[0].DepartmentID == '1':
                        querysetid.onebuOperation = '1'
                    elif t_sys_department_staff_objs[0].DepartmentID == '2':
                        querysetid.twobuOperation = '1'
                    elif t_sys_department_staff_objs[0].DepartmentID == '3':
                        querysetid.threebuOperation = '1'
                    elif t_sys_department_staff_objs[0].DepartmentID == '4':
                        querysetid.fourbuOperation = '1'
                    elif t_sys_department_staff_objs[0].DepartmentID == '5':
                        querysetid.fivebuOperation = '1'
                    elif t_sys_department_staff_objs[0].DepartmentID == '6':
                        querysetid.sixbuOperation = '1'
                    elif t_sys_department_staff_objs[0].DepartmentID == '7':
                        querysetid.sevenbuOperation = '1'
                    elif t_sys_department_staff_objs[0].DepartmentID == '8':
                        querysetid.eightbuOperation = '1'
                    elif t_sys_department_staff_objs[0].DepartmentID == '9':
                        querysetid.ninebuOperation = '1'
                    elif t_sys_department_staff_objs[0].DepartmentID == '10':
                        querysetid.tenbuOperation = '1'
                    elif t_sys_department_staff_objs[0].DepartmentID == '11':
                        querysetid.elevenbuOperation = '1'
                    elif t_sys_department_staff_objs[0].DepartmentID == '12':
                        querysetid.twelvebuOperation = '1'
                    elif t_sys_department_staff_objs[0].DepartmentID == '13':
                        querysetid.thirteenbuOperation = '1'
                dptmtid = t_sys_department_staff_objs[0].DepartmentID
                #本部门领用过
                old_objs = t_product_depart_get.objects.filter(pid = querysetid.id,DepartmentID=dptmtid )
                if not old_objs.exists():
                    querysetid.save()

                    obj = t_product_depart_get()
                    obj.__dict__ = querysetid.__dict__
                    obj.StaffName = request.user.first_name
                    obj.SalesAttr = obj.StaffName
                    obj.DepartmentID = dptmtid
                    obj.pid = querysetid.id
                    obj.LYTime = ddtime.now()
                    obj.PublishedInfo = ''
                    obj.PublishedA = ''
                    obj.id = None
                    obj.save()
                else:
                    messages.info(request,u'你部门已经领用/弃用过,无须重复领用！')

                begin_t_product_oplog(request,querysetid.MainSKU,'BMLY',querysetid.Name2,querysetid.id)
            else:
                messages.error(request,u'图片还没有完成，不允许领用。MainSKU:%s'%querysetid.MainSKU)
    to_depart_get.short_description = u'本部门领用'

    def do_Abandoned(self, request, queryset):
        cursor = connection.cursor() #
        for querysetid in queryset.all():

            sku = querysetid.SKU
            if sku != querysetid.MainSKU :
                sku = '%s%s'%(querysetid.MainSKU,querysetid.SKU)

            t_sys_department_staff_objs = t_sys_department_staff.objects.filter(StaffID=request.user.username)
            if  t_sys_department_staff_objs.count() <=  0 :
                messages.error(request,u'你没有员工数据,请联系管理员正确录入员工信息！')
                continue #没找到部门
            else:
                if t_sys_department_staff_objs[0].DepartmentID == '1':
                    querysetid.onebuOperation = '1'
                elif t_sys_department_staff_objs[0].DepartmentID == '2':
                    querysetid.twobuOperation = '1'
                elif t_sys_department_staff_objs[0].DepartmentID == '3':
                    querysetid.threebuOperation = '1'
                elif t_sys_department_staff_objs[0].DepartmentID == '4':
                    querysetid.fourbuOperation = '1'
                elif t_sys_department_staff_objs[0].DepartmentID == '5':
                    querysetid.fivebuOperation = '1'
                elif t_sys_department_staff_objs[0].DepartmentID == '6':
                    querysetid.sixbuOperation = '1'
                elif t_sys_department_staff_objs[0].DepartmentID == '7':
                    querysetid.sevenbuOperation = '1'
                elif t_sys_department_staff_objs[0].DepartmentID == '8':
                    querysetid.eightbuOperation = '1'
                elif t_sys_department_staff_objs[0].DepartmentID == '9':
                    querysetid.ninebuOperation = '1'
                elif t_sys_department_staff_objs[0].DepartmentID == '10':
                    querysetid.tenbuOperation = '1'
                elif t_sys_department_staff_objs[0].DepartmentID == '11':
                    querysetid.elevenbuOperation = '1'
                elif t_sys_department_staff_objs[0].DepartmentID == '12':
                    querysetid.twelvebuOperation = '1'
                elif t_sys_department_staff_objs[0].DepartmentID == '13':
                    querysetid.thirteenbuOperation = '1'

            dptmtid = t_sys_department_staff_objs[0].DepartmentID


            #本部门领用过
            old_objs = t_product_depart_get.objects.filter(pid = querysetid.id,DepartmentID=dptmtid)
            if not old_objs.exists():
                querysetid.save()
                
                obj = t_product_depart_get()
                obj.__dict__ = querysetid.__dict__
                obj.StaffName = u'%s-%s'%(request.user.first_name,u'弃用')
                obj.SalesAttr = obj.StaffName
                obj.DepartmentID = dptmtid
                obj.pid = querysetid.id
                obj.LYTime = ddtime.now()
                obj.PublishedInfo = ''
                obj.PublishedA = ''
                obj.id = None
                obj.save()
            else:
                messages.info(request,u'你部门已经领用/弃用过,无须重复弃用！')

            begin_t_product_oplog(request,querysetid.MainSKU,'BMLY',querysetid.Name2,querysetid.id)

    do_Abandoned.short_description = u'本部门弃用'

    def department_get_log(self,obj):
        rt=''
        t_product_depart_get_objs = t_product_depart_get.objects.filter(pid=obj.id).order_by('DepartmentID')
        for t_product_depart_get_obj in t_product_depart_get_objs:
            rt = u'%s%s:%s<br>%s,<br>'%(rt,t_product_depart_get_obj.DepartmentID,t_product_depart_get_obj.StaffName,str(t_product_depart_get_obj.LYTime)[0:10])
        return mark_safe(rt)
    department_get_log.short_description = u'部门领用记录'
    
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
    
    def qy(self, request, queryset):
        for querysetid in queryset.all():
            t_sys_department_staff_objs = t_sys_department_staff.objects.filter(StaffID=request.user.username)
            if  t_sys_department_staff_objs.count() <=  0 :
                messages.error(request,u'你没有员工数据,请联系管理员正确录入员工信息！')
                continue #没找到部门
            else:
                if t_sys_department_staff_objs[0].DepartmentID == '1': 
                    querysetid.onebuOperation = '2'
                elif t_sys_department_staff_objs[0].DepartmentID == '2':
                    querysetid.twobuOperation = '2'
                elif t_sys_department_staff_objs[0].DepartmentID == '3':
                    querysetid.threebuOperation = '2'
                elif t_sys_department_staff_objs[0].DepartmentID == '4':
                    querysetid.fourbuOperation = '2'
                elif t_sys_department_staff_objs[0].DepartmentID == '5':
                    querysetid.fivebuOperation = '2'
                elif t_sys_department_staff_objs[0].DepartmentID == '6':
                    querysetid.sixbuOperation = '2'
                elif t_sys_department_staff_objs[0].DepartmentID == '7':
                    querysetid.sevenbuOperation = '2'
                elif t_sys_department_staff_objs[0].DepartmentID == '8':
                    querysetid.eightbuOperation = '2'
                elif t_sys_department_staff_objs[0].DepartmentID == '9':
                    querysetid.ninebuOperation = '2'
                elif t_sys_department_staff_objs[0].DepartmentID == '10':
                    querysetid.tenbuOperation = '2'
                elif t_sys_department_staff_objs[0].DepartmentID == '11':
                    querysetid.elevenbuOperation = '2'
                elif t_sys_department_staff_objs[0].DepartmentID == '12':
                    querysetid.twelvebuOperation = '2'
                elif t_sys_department_staff_objs[0].DepartmentID == '13':
                    querysetid.thirteenbuOperation = '2'
                querysetid.save()
    qy.short_description = u'本部门弃用'

    def show_oplog(self,obj) :
        rt = ''
        t_product_oplog_objs = t_product_oplog.objects.filter(pid=obj.id).order_by('id')
        for t_product_oplog_obj in t_product_oplog_objs:
            rt = u'%s%s:%s,'%(rt,t_product_oplog_obj.StepName,t_product_oplog_obj.OpName)
        return rt
    show_oplog.short_description = u'操作历史'
    #
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
                rts = rts + u'%s,<br>'%t_product_mainsku_sku_obj.ProductSKU
            return mark_safe(rts)
        except:
            return mark_safe(rts)
    show_sku.short_description = u'子SKU信息'
    
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
            rt = '%s<tr><td>%s：</td><td>%s</td></tr>'%(rt,DepartmentID,t_log_sku_shopsku_apply_obj[1])
        info = '%s'%rt
        if obj.onebuOperation == '2':
            info = '%s一部弃用<br/>'%info
        if obj.twobuOperation == '2':
            info = '%s二部弃用<br/>'%info
        if obj.threebuOperation == '2':
            info = '%s三部弃用<br/>'%info
        if obj.fourbuOperation == '2':
            info = '%s四部弃用<br/>'%info
        if obj.fivebuOperation == '2':
            info = '%s五部弃用<br/>'%info
        if obj.sixbuOperation == '2':
            info = '%s六部弃用<br/>'%info
        if obj.sevenbuOperation == '2':
            info = '%s七部弃用<br/>'%info
        if obj.eightbuOperation == '2':
            info = '%s八部弃用<br/>'%info
        if obj.ninebuOperation == '2':
            info = '%s九部弃用<br/>'%info
        if obj.tenbuOperation == '2':
            info = '%s十部弃用<br/>'%info
        if obj.elevenbuOperation == '2':
            info = '%s十一部弃用<br/>'%info
        rt = '%s</table>'%info
        cur.close()
        return mark_safe(rt)
    show_sku_publish.short_description = u'----SKU绑定记录----'

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

    list_display= ('id','MainSKU','show_status','show_sku_publish','DYStaffName','MGProcess','MGTime',
                   'show_SourcePicPath','SpecialSell','show_more_information','ClothingNote','ShelveDay','OrdersLast7Days',
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
              'AI_FLAG','SourceURL2','IP_FLAG'
              )

    form_layout = (
        Fieldset(u'调研结果',
                    Row('SourceURL', 'SourceURL2'),
                    Row('OrdersLast7Days', 'Pricerange', ''),
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
                    Row('AI_FLAG','IP_FLAG',''),
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
        qs = super(t_product_enter_ed_Admin, self).get_list_queryset()
        qs=qs.filter(MGProcess__in=[2,3,6])

        t_sys_department_staff_objs = t_sys_department_staff.objects.filter(StaffID=request.user.username)
        if request.user.is_superuser:
            pass
        else:
            if  t_sys_department_staff_objs.count() <=  0 :
                messages.error(request,u'你没有员工数据,请联系管理员正确录入员工信息！')
            else:
                DepartmentID = t_sys_department_staff_objs[0].DepartmentID
                dep_flag = request.GET.get('dep', '')
                if dep_flag == '1': #未刊登
                    if DepartmentID == '1':
                        qs = qs.exclude(onebuOperation__in=('1','2'))
                    elif DepartmentID == '2':
                        qs = qs.exclude(twobuOperation__in=('1','2'))
                    elif DepartmentID == '3':
                        qs = qs.exclude(threebuOperation__in=('1','2'))
                    elif DepartmentID == '4':
                        qs = qs.exclude(fourbuOperation__in=('1','2'))
                    elif DepartmentID == '5':
                        qs = qs.exclude(fivebuOperation__in=('1','2'))
                    elif DepartmentID == '6':
                        qs = qs.exclude(sixbuOperation__in=('1','2'))
                    elif DepartmentID == '7':
                        qs = qs.exclude(sevenbuOperation__in=('1','2'))
                    elif DepartmentID == '8':
                        qs = qs.exclude(eightbuOperation__in=('1','2'))
                    elif DepartmentID == '9':
                        qs = qs.exclude(ninebuOperation__in=('1','2'))
                    elif DepartmentID == '10':
                        qs = qs.exclude(tenbuOperation__in=('1','2'))
                    elif DepartmentID == '11':
                        qs = qs.exclude(elevenbuOperation__in=('1','2'))
                    elif DepartmentID == '12':
                        qs = qs.exclude(twelvebuOperation__in=('1','2'))
                    elif DepartmentID == '13':
                        qs = qs.exclude(thirteenbuOperation__in=('1','2'))
                elif dep_flag == '2': #已刊登
                    if DepartmentID == '1':
                        qs = qs.filter(onebuOperation='1')
                    elif DepartmentID == '2':
                        qs = qs.filter(twobuOperation='1')
                    elif DepartmentID == '3':
                        qs = qs.filter(threebuOperation='1')
                    elif DepartmentID == '4':
                        qs = qs.filter(fourbuOperation='1')
                    elif DepartmentID == '5':
                        qs = qs.filter(fivebuOperation='1')
                    elif DepartmentID == '6':
                        qs = qs.filter(sixbuOperation='1')
                    elif DepartmentID == '7':
                        qs = qs.filter(sevenbuOperation='1')
                    elif DepartmentID == '8':
                        qs = qs.filter(eightbuOperation='1')
                    elif DepartmentID == '9':
                        qs = qs.filter(ninebuOperation='1')
                    elif DepartmentID == '10':
                        qs = qs.filter(tenbuOperation='1')
                    elif DepartmentID == '11':
                        qs = qs.filter(elevenbuOperation='1')
                    elif DepartmentID == '12':
                        qs = qs.filter(twelvebuOperation='1')
                    elif DepartmentID == '13':
                        qs = qs.filter(thirteenbuOperation='1')
                elif dep_flag == '3': #已弃用
                    if DepartmentID == '1':
                        qs = qs.filter(onebuOperation='2')
                    elif DepartmentID == '2':
                        qs = qs.filter(twobuOperation='2')
                    elif DepartmentID == '3':
                        qs = qs.filter(threebuOperation='2')
                    elif DepartmentID == '4':
                        qs = qs.filter(fourbuOperation='2')
                    elif DepartmentID == '5':
                        qs = qs.filter(fivebuOperation='2')
                    elif DepartmentID == '6':
                        qs = qs.filter(sixbuOperation='2')
                    elif DepartmentID == '7':
                        qs = qs.filter(sevenbuOperation='2')
                    elif DepartmentID == '8':
                        qs = qs.filter(eightbuOperation='2')
                    elif DepartmentID == '9':
                        qs = qs.filter(ninebuOperation='2')
                    elif DepartmentID == '10':
                        qs = qs.filter(tenbuOperation='2')
                    elif DepartmentID == '11':
                        qs = qs.filter(elevenbuOperation='2')
                    elif DepartmentID == '12':
                        qs = qs.filter(twelvebuOperation='2')
                    elif DepartmentID == '13':
                        qs = qs.filter(thirteenbuOperation='2')
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
        SourceURL   =   request.GET.get('SourceURL','')#反向链接平台
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
        BJP_FLAG        = request.GET.get('BJP_FLAG','')
        ME_FLAG = request.GET.get('ME_FLAG','')
        cur = conn.cursor()
        sql = 'SELECT MainSKU from py_db.t_log_sku_shopsku where Status="APPLYSUCCESS" and StaffName ="%s"'%request.user.first_name
        cur.execute(sql)
        rows = cur.fetchall()
        lis_mainsku = []
        for row in rows:
            lis_mainsku.append(row[0])
        if ME_FLAG == '1':
            qs = qs.filter(MainSKU__in=lis_mainsku)
        elif ME_FLAG == '0':
            qs = qs.exclude(MainSKU__in=lis_mainsku)  

        searchList = {'ContrabandAttribute__exact':ContrabandAttribute, 'Storehouse__exact':Storehouse,'MainSKU__in':MainSKU, 'LargeCategory__exact': LargeCategory,
                      'YNphoto__exact': YNphoto,'MGProcess__exact': MGProcess,'DYStaffName__exact': DYStaffName,'DYSHStaffName__exact': DYSHStaffName,
                      'XJStaffName__exact': XJStaffName,'KFStaffName__exact': KFStaffName,'MGStaffName__exact': MGStaffName,'Buyer__exact': Buyer,
                      'CreateStaffName__exact': CreateStaffName,'LRStaffName__exact': LRStaffName, 'JZLStaffName__exact':jZLStaffName,
                      'KFTime__gte': KFTimeStart, 'KFTime__lt': KFTimeEnd,'JZLTime__gte': JZLTimeStart, 'JZLTime__lt': JZLTimeEnd,
                      'MGTime__gte': MGTimeStart, 'MGTime__lt': MGTimeEnd,'Weight__gte': WeightStart, 'Weight__lt': WeightEnd,
                      'ClothingSystem1__exact':Cate1,'ClothingSystem2__exact': Cate2,'ClothingSystem3__exact':Cate3,
                      'PlatformName__exact':PlatformName, 'MainSKU__startswith':MainSKUPrefix,'BJP_FLAG':BJP_FLAG,
                      'LRTime__gte': LRTimeStart, 'LRTime__lt': LRTimeEnd,'SourceURL__icontains':SourceURL,
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
                qs = qs.filter(**sl).exclude(**searchexclude)
            except Exception,ex:
                messages.error(request,u'输入的查询数据有问题！')      
        if keywords:
            for k in keywords.split(','):
                qs = qs.filter(Q(Name__icontains=k) | Q(Keywords__icontains=k)) if k.strip() else qs
        if keywords2:
            for k2 in keywords2.split(','):
                qs = qs.filter(Q(Name2__icontains=k2) | Q(Keywords2__icontains=k2)) if k2.strip() else qs
        
        flag = 0
        try:
            flag = t_sys_staff_auth.objects.filter(StaffID=request.user.username,urltable="t_product_enter_ed").count()
        except:
            pass
        '''
        if request.user.is_superuser or flag != 0:
            qs = qs
        else:
            t_sys_department_staff_objs = t_sys_department_staff.objects.filter(StaffID=request.user.username)
            if t_sys_department_staff_objs.exists():
                DepartmentID = t_sys_department_staff_objs[0].DepartmentID
                
                if DepartmentID == '1':
                    qs = qs.exclude(onebuOperation='1')
                elif DepartmentID == '2':
                    qs = qs.exclude(twobuOperation='1')
                elif DepartmentID == '3':
                    qs = qs.exclude(threebuOperation='1')
                elif DepartmentID == '4':
                    qs = qs.exclude(fourbuOperation='1')
                elif DepartmentID == '5':
                    qs = qs.exclude(fivebuOperation='1')
                elif DepartmentID == '6':
                    qs = qs.exclude(sixbuOperation='1')
                elif DepartmentID == '7':
                    qs = qs.exclude(sevenbuOperation='1')
                elif DepartmentID == '8':
                    qs = qs.exclude(eightbuOperation='1')
                elif DepartmentID == '9':
                    qs = qs.exclude(ninebuOperation='1')
                elif DepartmentID == '10':
                    qs = qs.exclude(tenbuOperation='1')
                elif DepartmentID == '11':
                    qs = qs.exclude(elevenbuOperation='1')
                elif DepartmentID == '12':
                    qs = qs.exclude(twelvebuOperation='1')
                elif DepartmentID == '13':
                    qs = qs.exclude(thirteenbuOperation='1')
        '''

        catelist = [u'001.时尚女装', u'002.时尚男装', u'021.泳装', u'024.童装', u'025.内衣']

        if flagcloth == '1':
            return qs.filter(LargeCategory__in=catelist)
        elif flagcloth == '2':
            return qs.exclude(LargeCategory__in=catelist)
        else:
            return qs
        