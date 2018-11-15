# coding=utf-8


from django.utils.safestring import mark_safe
from datetime import datetime
from django.contrib import messages
from random import choice


class t_templet_joom_wait_upload_Admin(object):
    search_box_flag = True
    plateform_distribution_navigation = True

    def show_picture(self,obj) :
        """展示主图"""
        from brick.wish.wish_distribution.admin_function import show_picture
        rt = show_picture(obj=obj, plateform='joom')
        return mark_safe(rt)
    show_picture.short_description = u'<span style="color: #428bca">图片</span>'

    def show_variants(self, obj):
        """展示修改变体信息"""
        from brick.wish.wish_distribution.admin_function import show_variants
        rt = show_variants(obj=obj, plateform='joom', page='wait_upload')
        return mark_safe(rt)
    show_variants.short_description = mark_safe('<p align="center">变体信息</p>')

    list_display = ('id', 'MainSKU', 'show_picture', 'Title', 'CoreWords', 'Tags', 'show_variants')

    actions = ['export_excel', 'export_excel_2']

    def export_excel(self, request, queryset):
        shopname = request.GET.get('shopname', '')
        if shopname == '':
            messages.error(request, '请 先 选 择 去 铺 货 的 店 铺！！！')
        else:
            id_list = []
            export_user = request.user.username
            export_time = datetime.now()
            shopname = 'joom' + shopname

            from app_djcelery.tasks import joom_export_excel
            for obj in queryset:
                id_list.append(int(obj.id))
                obj.Status = 'YES'
                obj.ExportTime = export_time
                obj.save()

            # 判断选择导出的数量，大于10随机去掉20%再导出
            result_id_list = []
            if len(id_list) >= 10:
                result_length = int(len(id_list) * 0.8)
                for i in range(result_length):
                    id_choice = choice(id_list)
                    result_id_list.append(id_choice)
                    id_list.remove(id_choice)
            else:
                result_id_list = id_list
            result_id_list.sort()
            calculate_flag = 0
            joom_export_excel.delay(result_id_list, export_user, export_time, shopname, calculate_flag)
    export_excel.short_description = u'导出表格'


    def export_excel_2(self, request, queryset):
        shopname = request.GET.get('shopname', '')
        if shopname == '':
            messages.error(request, '请 先 选 择 去 铺 货 的 店 铺！！！')
        else:
            id_list = []
            export_user = request.user.username
            export_time = datetime.now()
            shopname = 'joom' + shopname

            from app_djcelery.tasks import joom_export_excel
            for obj in queryset:
                id_list.append(int(obj.id))
                obj.Status = 'YES'
                obj.ExportTime = export_time
                obj.save()

            # 判断选择导出的数量，大于10随机去掉20%再导出
            result_id_list = []
            if len(id_list) >= 10:
                result_length = int(len(id_list) * 0.8)
                for i in range(result_length):
                    id_choice = choice(id_list)
                    result_id_list.append(id_choice)
                    id_list.remove(id_choice)
            else:
                result_id_list = id_list
            result_id_list.sort()
            calculate_flag = 1
            joom_export_excel.delay(result_id_list, export_user, export_time, shopname, calculate_flag)
    export_excel_2.short_description = u'按最高价导出表格'


    def get_list_queryset(self, ):
        request = self.request
        qs = super(t_templet_joom_wait_upload_Admin, self).get_list_queryset()
        qs = qs.filter(Status='NO')
        shopname = request.GET.get('shopname', '')
        cate = request.GET.get('Cate', '')
        sku = request.GET.get('sku', '')

        if shopname:
            qs = qs.filter(Used_shopname=shopname)
        if cate:
            qs = qs.filter(Cate=cate)
        if sku:
            qs = qs.filter(MainSKU__startswith=sku.upper())
        return qs
