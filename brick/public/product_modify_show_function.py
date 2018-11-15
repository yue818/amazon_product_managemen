# coding=utf-8

import os, oss2
from xlwt import *
from datetime import datetime
from django.utils.safestring import mark_safe
from django.contrib import messages
from Project.settings import MEDIA_ROOT, ACCESS_KEY_ID,ACCESS_KEY_SECRET, ENDPOINT, BUCKETNAME_XLS, PREFIX, ENDPOINT_OUT
from skuapp.modelsadminx.t_product_Admin import mkdir_p
from Project.settings import ITEM_DICT, ITEM_ORDER_LIST, WARNING_DICT

from django.db import connection
from brick.table.b_supplier import b_supplier

b_supplier_obj = b_supplier(db_conn=connection)

TYPE_DICT = {
    '1': u'换图片', '2': u'临时下架', '3': u'更改商品信息', '4': u'涨价', '5': u'清仓下架', '6': u'变更业绩归属人2',
    '7': u'SKU合并', '8': u'重新上架', '9': u'售完下架', '10': u'处理库尾', '12': u'清仓下架', '13': u'提前备货',
    '14': u'备面料供应链商品', '15': u'无面料供应链商品', '16': u'供货不稳商品', '17': u'待转供应链',
    '18': u'置回普通商品', '19': u'库存预警', '100': u'组合修改'
}


class product_modify_show_function(object):

    def show_PIC(self, obj):
        rt = u'<img src="%s"  width="120" height="120" />' % (obj.SourcePicPath2)
        return mark_safe(rt)
    show_PIC.short_description = u'<span style="color: #428bca; width:150px">商品图片</span>'

    def show_SKU_InputBox(self, obj):
        InputBox_list = obj.InputBox.split(',')
        rt = u''
        for InputBox in InputBox_list:
            rt = u'%s<input style="width:100px;border:none;background-color:transparent;" value="%s"><br>' % (rt, InputBox)
        return mark_safe(rt)
    show_SKU_InputBox.short_description = u'<span style="color: #428bca; width:300px">商品编码</span>'

    def show_oldvalue(self, obj):
        oldvalue_list = obj.oldvalue.split(',')
        rt = u''
        for oldvalue in oldvalue_list:
            rt = u'%s%s<br>' % (rt, oldvalue)
        return mark_safe(rt)
    show_oldvalue.short_description = u'<span style="color: #428bca">旧值</span>'

    def show_newvalue(self, obj):
        newvalue_list = obj.newvalue.split(',')
        rt = u''
        for newvalue in newvalue_list:
            rt = u'%s%s<br>' % (rt, newvalue)
        return mark_safe(rt)
    show_newvalue.short_description = u'<span style="color: #428bca">新值</span>'

    def show_product(self, obj):
        product_name = obj.Name2 if obj.Name2 else ''
        dev_date = str(obj.DevDate)[:10] if obj.Name2 else ''
        en_title = obj.Keywords if obj.Keywords else ''
        material = obj.Material if obj.Material else ''
        rr = u'<span>商品名称:%s</span><br><span>英文标题:%s<span><br><span>材质:%s<span><br><span>开发日期:%s<span>' % \
             (product_name, en_title, material, dev_date)
        return mark_safe(rr)
    show_product.short_description = u'<span style="color: #428bca">商品信息</span>'

    def show_sq(self, obj):
        sq_name = obj.SQStaffNameing if obj.SQStaffNameing else ''
        sq_time = obj.SQTimeing if obj.SQTimeing else ''
        rr = u'<span>申请人:%s</span><br><span>申请时间:<br>%s<span>' % (sq_name, sq_time)
        return mark_safe(rr)
    show_sq.short_description = u'<span style="color: #428bca">----申请信息----</span>'

    def show_sh(self, obj):
        sh_name = obj.SHStaffName if obj.SHStaffName else ''
        sh_time = obj.SHTime if obj.SHTime else ''
        rr = u'<span>审核人:%s</span><br><span>审核时间:<br>%s<span>' % (sh_name, sh_time)
        return mark_safe(rr)
    show_sh.short_description = u'<span style="color: #428bca">----审核信息-----</span>'

    def show_lq(self, obj):
        lq_name = obj.LQStaffName if obj.LQStaffName else ''
        lq_time = obj.LQTime if obj.LQTime else ''
        rr = u'<span>领取人:%s</span><br><span>领取时间:<br>%s<span>' % (lq_name, lq_time)
        return mark_safe(rr)
    show_lq.short_description = u'<span style="color: #428bca">----领取信息----</span>'

    def show_xg(self, obj):
        xg_name = obj.XGStaffName if obj.XGStaffName else ''
        xg_time = obj.XGTime if obj.XGTime else ''
        rr = u'<span>修改人:%s</span><br><span>修改时间:<br>%s<span>' % (xg_name, xg_time)
        return mark_safe(rr)
    show_xg.short_description = u'<span style="color: #428bca">----修改信息----</span>'

    def show_content(self, obj):
        rr = u'<input readonly="true" type="text" ' \
             u'style="border:none;background-color:transparent;overflow:hidden;text-overflow: ellipsis;" ' \
             u'onmouseover="this.title=this.value" value="%s">' % obj.XGcontext
        return mark_safe(rr)
    show_content.short_description = u'<span style="color: #428bca">修改描述(原)</span>'

    def show_XGcontext(self, obj):
        rt = u'%s' % (obj.XGcontext)
        return mark_safe(rt)
    show_XGcontext.short_description = u'<span style="color: #428bca">修改描述(原)</span>'

    def show_details(self, obj):
        page = self.request.get_full_path().split('/')[-2]
        details = eval(obj.Details) if obj.Details else ''
        if details:
            if obj.Select == '7':
                rr = u'<style>#modify{height:20px;border:none;margin: 0;line-height:100%;width: 100%;}</style>'
                rr = u'%s<table style="text-align:center;" border="1" cellpadding="3" cellspacing="1" bgcolor="#c1c1c1">' \
                     u'<tr bgcolor="#C00">' \
                     u'<th style="text-align:center">待合并SKU</th><th style="text-align:center">合并到SKU</th>' \
                     u'<th style="text-align:center">描述</th><th style="text-align:center">修改类型</th></tr>' % rr
                modify_type = u'SKU合并(需审核)'
                for detail in details:
                    delete_sku = detail['delete_sku']
                    retain_sku = detail['retain_sku']
                    describe = detail['describe']
                    rr = u'%s<tr bgcolor="#FFFFFF">' \
                         u'<td><input type="text" id="modify" readonly="True" value="%s"></td>' \
                         u'<td><input type="text" id="modify" readonly="True" value="%s"></td>' \
                         u'<td><input type="text" id="modify" readonly="True" value="%s" onmouseover="this.title=this.value"></td>' \
                         u'<td><input type="text" id="modify" readonly="True" value="%s" ></td></tr>' % \
                         (rr, delete_sku, retain_sku, describe, modify_type)
            else:
                i = 0
                break_flag = 0
                rr = u'<style>#modify{height:20px;border:none;margin: 0;line-height:100%;width: 100%;}</style>'
                rr = u'%s<table style="text-align:center;" border="1" cellpadding="3" cellspacing="1" bgcolor="#c1c1c1">' \
                     u'<tr bgcolor="#C00"><th style="text-align:center">SKU</th><th style="text-align:center">修改项目</th>' \
                     u'<th style="text-align:center">旧值</th><th style="text-align:center">新值</th>' \
                     u'<th style="text-align:center">描述</th><th style="text-align:center">修改类型</th>' \
                     u'<th style="text-align:center"></th></tr>' % rr
                for k1, v1 in details.items():
                    sku = k1
                    for k2, v2 in v1.items():
                        name = v2[0]
                        if k2 == 'WarningCats':
                            old_val = WARNING_DICT.get(v2[1], '') if v2[1] else ''
                            new_val = WARNING_DICT.get(v2[2], '') if v2[2] else ''
                        else:
                            old_val = v2[1]
                            new_val = v2[2]

                        SupplierUSED = ''
                        if k2 == 'SupplierName':
                            uf = b_supplier_obj.GetSupplierStatus(new_val)
                            if uf and int(uf) == 1:
                                SupplierUSED = u'已停用'
                            elif uf and int(uf) == 0:
                                SupplierUSED = u'正常'
                            else:
                                SupplierUSED = u'新'
                        describe = v2[3]
                        modify_type = v2[4]
                        rr = u'%s<tr bgcolor="#FFFFFF">' \
                             u'<td><input type="text" id="modify" readonly="True" value="%s"></td>' \
                             u'<td><input type="text" id="modify" readonly="True" value="%s"></td>' \
                             u'<td><input type="text" id="modify" readonly="True" value="%s" onmouseover="this.title=this.value"></td>' \
                             u'<td><input type="text" id="modify" readonly="True" value="%s" onmouseover="this.title=this.value"></td>' \
                             u'<td><input type="text" id="modify" readonly="True" value="%s" onmouseover="this.title=this.value"></td>' \
                             u'<td><input type="text" id="modify" readonly="True" value="%s" onmouseover="this.title=this.value"></td>' \
                             u'<td><input type="text" id="modify" readonly="True" value="%s" onmouseover="this.title=\'供应商状态：\'+this.value"></td>' \
                             u'</tr>' % \
                             (rr, sku, name, old_val, new_val, describe, modify_type, SupplierUSED)
                        i += 1
                        if i > 4:
                            break_flag = 1
                            break
                    if break_flag == 1:
                        break
            rr = u'%s<tr><td><a id="link_id_%s">点击查看</a></td></tr>' % (rr, obj.id)
            if page == 't_product_information_modify':
                rr = u"%s</table><script>$('#link_id_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan'," \
                     u"title:'查看全部',fix:false,shadeClose: true,maxmin:true,area:['1200px','700px']," \
                     u"content:'/show_modify_detail/?modify_id=%s&page=%s',btn:['关闭页面'],end:function(){location.reload();}});});</script>" % (
                         rr, obj.id, obj.id, page)
            else:
                rr = u"%s</table><script>$('#link_id_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan'," \
                     u"title:'查看全部',fix:false,shadeClose: true,maxmin:true,area:['1200px','700px']," \
                     u"content:'/show_modify_detail/?modify_id=%s&page=%s',btn:['关闭页面']});});</script>" % (
                         rr, obj.id, obj.id, page)
        else:
            rr = ''
        return mark_safe(rr)
    show_details.short_description = u'<span style="color: #428bca">修改描述(新)</span>'


    def to_excel_new(self, request, queryset):
        modify_details_list = []
        modify_sq_name_list = []
        merge_details_list = []
        merge_sq_name_list = []
        old_id_list = []
        for qs in queryset:
            details = eval(qs.Details) if qs.Details else {}
            if details:
                if qs.Select == '7':
                    merge_details_list.append(details)
                    merge_sq_name_list.append(qs.SQStaffNameing)
                else:
                    modify_details_list.append(details)
                    modify_sq_name_list.append(qs.SQStaffNameing)
            else:
                old_id_list.append(str(int(qs.id)))
        if old_id_list:
            old_id_str = ','.join(old_id_list)
            messages.error(request, '您当前使用的“新版导出Excel”功能,下列ID：%s 信息修改为旧版申请记录，已为您剔除。如果您仍想要导出这部分，请选择“导出Excel(旧版)”导出这部分' % old_id_str)
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))
        mkdir_p(path)
        os.popen('chmod 777 %s' % (path))
        w = Workbook()

        self.excel_modify(w, modify_details_list, modify_sq_name_list)
        self.excel_merge(w, merge_details_list, merge_sq_name_list)

        filename = request.user.username + '_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.xls'
        w.save(path + '/' + filename)
        os.popen(r'chmod 777 %s' % (path + '/' + filename))
        # 上传oss对象
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT, BUCKETNAME_XLS)
        bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)
        # 删除现有的
        for object_info in oss2.ObjectIterator(bucket, prefix='%s/%s_' % (request.user.username, request.user.username)):
            bucket.delete_object(object_info.key)
        bucket.put_object(u'%s/%s' % (request.user.username, filename), open(path + '/' + filename))
        messages.error(request, u'%s%s.%s/%s/%s' % (PREFIX, BUCKETNAME_XLS, ENDPOINT_OUT, request.user.username, filename) + u':成功导出,可点击Download下载到本地............................。')
    to_excel_new.short_description = u'导出EXCEL(新版)'


    def excel_modify(self, w, modify_details_list, modify_sq_name_list):
        sheet = w.add_sheet(u'商品信息修改')
        sheet.write(0, 0, u'SKU')
        row = 0
        i = 1
        # 写列名
        for key in ITEM_ORDER_LIST:
            column_name = ITEM_DICT.get(key, '')
            if column_name:
                sheet.write(0, i, u'%s' % column_name)
                i += 1
        sheet.write(0, i, u'申请人')
        i += 1
        sheet.write(0, i, u'修改描述')

        # 每列填值
        j = 0
        for details in modify_details_list:
            for key_1, value_1 in details.items():
                row += 1
                sheet.write(row, 0, key_1)
                describe_list = []
                for key_2, value_2 in value_1.items():
                    column = 1
                    for item in ITEM_ORDER_LIST:
                        if key_2 == item:
                            if item == 'WarningCats':
                                sheet.write(row, column, WARNING_DICT.get(value_2[2], ''))
                            elif item == 'BmpUrl':
                                sheet.write(row, column, value_2[3].strip())
                            else:
                                sheet.write(row, column, u'{}'.format(value_2[2]).split('(')[0])
                            describe_list.append(value_2[3].strip())
                        column += 1
                sheet.write(row, column, modify_sq_name_list[j])
                column += 1
                sheet.write(row, column, ';'.join(describe_list))
            j += 1


    def excel_merge(self, w, merge_details_list, merge_sq_name_list):
        sheet = w.add_sheet(u'SKU合并')
        sheet.write(0, 0, u'待合并SKU')
        sheet.write(0, 1, u'合并到SKU')
        sheet.write(0, 2, u'申请人')
        sheet.write(0, 3, u'修改描述')

        row = 1
        for i in range(len(merge_details_list)):
            for each in merge_details_list[i]:
                column = 0
                sheet.write(row, column, each['delete_sku'])

                column += 1
                sheet.write(row, column, each['retain_sku'])

                column += 1
                sheet.write(row, column, merge_sq_name_list[i])

                column += 1
                sheet.write(row, column, each['describe'])

                row += 1


    def to_excel(self, request, queryset):
        # new_id_list = []
        # for qs in queryset:
            # xg_content = qs.XGcontext if qs.XGcontext else ''
            # if not xg_content:
            #     new_id_list.append(str(int(qs.id)))
        # if new_id_list:
        #     new_id_str = ','.join(new_id_list)
        #     messages.error(request, '您当前使用的“旧版导出Excel”功能,下列ID：%s 信息修改为新版申请记录，请剔除后再使用旧功能导出！！！' % new_id_str)
        # else:
        #     details = eval(qs.Details) if qs.Details else {}
        #     if not details:
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))
        mkdir_p(path)
        os.popen('chmod 777 %s' % (path))

        w = Workbook()
        sheet = w.add_sheet('information_modify')

        sheet.write(0, 0, u'id')
        sheet.write(0, 1, u'商品编码')
        sheet.write(0, 2, u'商品名称')
        sheet.write(0, 3, u'英文Keywords')
        sheet.write(0, 4, u'中文Keywords')
        sheet.write(0, 5, u'申请人')
        sheet.write(0, 6, u'申请时间')
        sheet.write(0, 7, u'修改类型')
        sheet.write(0, 8, u'修改描述')
        sheet.write(0, 9, u'旧值')
        sheet.write(0, 10, u'新值')

        sheet.write(0, 11, u'一部领用人')
        sheet.write(0, 12, u'一部领用日期')
        sheet.write(0, 13, u'一部领用状态')
        sheet.write(0, 14, u'二部领用人')
        sheet.write(0, 15, u'二部领用日期')
        sheet.write(0, 16, u'二部领用状态')
        sheet.write(0, 17, u'三部领用人')
        sheet.write(0, 18, u'三部领用日期')
        sheet.write(0, 19, u'三部领用状态')
        sheet.write(0, 20, u'四部领用人')
        sheet.write(0, 21, u'四部领用日期')
        sheet.write(0, 22, u'四部领用状态')
        sheet.write(0, 23, u'五部领用人')
        sheet.write(0, 24, u'五部领用日期')
        sheet.write(0, 25, u'五部领用状态')

        new_id_list = []
        # 写数据
        row = 0
        for qs in queryset:
            details = eval(qs.Details) if qs.Details else {}
            if details:
                new_id_list.append(str(int(qs.id)))
                continue

            InputBox_list_s = []
            if qs.InputBox is not None:
                InputBox_list_s = qs.InputBox.split(',')
            num = 0
            qs_id = ''
            for InputBox_list_l in InputBox_list_s:
                if InputBox_list_l.strip() != '':
                    row = row + 1
                    column = 0
                    sheet.write(row, column, qs.id)

                    column = column + 1
                    sheet.write(row, column, InputBox_list_l)

                    column = column + 1
                    sheet.write(row, column, qs.Name2)

                    column = column + 1
                    sheet.write(row, column, qs.Keywords)

                    column = column + 1
                    sheet.write(row, column, qs.Keywords2)

                    column = column + 1
                    sheet.write(row, column, qs.SQStaffNameing)

                    column = column + 1
                    rt = ''
                    rt = u'%s%s' % (rt, qs.SQTimeing)
                    sheet.write(row, column, u'%s' % rt)

                    column = column + 1
                    sheet.write(row, column, TYPE_DICT.get(qs.Select, ''))

                    column = column + 1
                    sheet.write(row, column, qs.XGcontext)

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

                    column = column + 1
                    sheet.write(row, column, qs.Dep1)

                    column = column + 1
                    sheet.write(row, column, u'%s' % qs.Dep1Date)

                    column = column + 1
                    sheet.write(row, column, qs.Dep1Sta)

                    column = column + 1
                    sheet.write(row, column, qs.Dep2)

                    column = column + 1
                    sheet.write(row, column, u'%s' % qs.Dep2Date)

                    column = column + 1
                    sheet.write(row, column, qs.Dep2Sta)

                    column = column + 1
                    sheet.write(row, column, qs.Dep3)

                    column = column + 1
                    sheet.write(row, column, u'%s' % qs.Dep3Date)

                    column = column + 1
                    sheet.write(row, column, qs.Dep3Sta)

                    column = column + 1
                    sheet.write(row, column, qs.Dep4)

                    column = column + 1
                    sheet.write(row, column, u'%s' % qs.Dep4Date)

                    column = column + 1
                    sheet.write(row, column, qs.Dep4Sta)

                    column = column + 1
                    sheet.write(row, column, qs.Dep5)

                    column = column + 1
                    sheet.write(row, column, u'%s' % qs.Dep5Date)

                    column = column + 1
                    sheet.write(row, column, qs.Dep5Sta)

        filename = request.user.username + '_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.xls'
        w.save(path + '/' + filename)
        os.popen(r'chmod 777 %s' % (path + '/' + filename))

        # 上传oss对象
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT, BUCKETNAME_XLS)
        bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)
        # 删除现有的
        for object_info in oss2.ObjectIterator(bucket, prefix='%s/%s_' % (request.user.username, request.user.username)):
            bucket.delete_object(object_info.key)
        bucket.put_object(u'%s/%s' % (request.user.username, filename), open(path + '/' + filename))
        messages.error(request, u'%s%s.%s/%s/%s' % (PREFIX, BUCKETNAME_XLS, ENDPOINT_OUT, request.user.username, filename) + u':成功导出,可点击Download下载到本地............................。')
        if new_id_list:
            new_id_str = ','.join(new_id_list)
            messages.error(request, '您当前使用的“旧版导出Excel”功能,下列ID：%s 信息修改为新版申请记录，已为您剔除。如果您仍想要导出这部分，请选择“导出Excel(新版)”导出这部分' % new_id_str)
    to_excel.short_description = u'导出EXCEL(旧版)'


    def to_excel_reduction(self, request, queryset):
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))
        mkdir_p(path)
        os.popen('chmod 777 %s' % (path))

        w = Workbook()
        sheet = w.add_sheet('cost_reduction')
        sheet.write(0, 0, u'id')
        sheet.write(0, 1, u'商品编码')
        sheet.write(0, 2, u'商品名称')
        sheet.write(0, 3, u'原价')
        sheet.write(0, 4, u'现价')
        sheet.write(0, 5, u'申请人')
        sheet.write(0, 6, u'申请时间')

        row = 0
        for qs in queryset:
            cost_reduction = eval(qs.CostReduction) if qs.CostReduction else {}
            for key, val in cost_reduction.items():
                row = row + 1
                column = 0
                sheet.write(row, column, qs.id)

                column = column + 1
                sheet.write(row, column, key)

                column = column + 1
                sheet.write(row, column, qs.Name2)

                column = column + 1
                sheet.write(row, column, val['old_price'])

                column = column + 1
                sheet.write(row, column, val['new_price'])

                column = column + 1
                sheet.write(row, column, qs.SQStaffNameing)

                column = column + 1
                sheet.write(row, column, str(qs.SQTimeing))
        filename = request.user.username + '_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.xls'
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
        messages.error(request, u'%s%s.%s/%s/%s' % (PREFIX, BUCKETNAME_XLS, ENDPOINT_OUT, request.user.username,filename) + u':成功导出,可点击Download下载到本地............................。')
    to_excel_reduction.short_description = u'导出降价'