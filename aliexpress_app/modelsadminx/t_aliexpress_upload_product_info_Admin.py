#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import datetime
# import xlrd
from django.db.models import Q
from django.contrib import messages
from django.conf import settings
from django.utils.safestring import mark_safe

# from brick.aliexpress.aliexpress_import_products import aliexpress_import_products
from brick.public.upload_to_oss import upload_to_oss
from app_djcelery.tasks import aliexpress_import_products_task
from skuapp.table.t_store_configuration_file import t_store_configuration_file


class t_aliexpress_upload_product_info_Admin(object):
    aliexpress_upload_product_info_plugin = True

    list_display = ['ShopName', 'UploadUser', 'UploadDatetime', 'show_salling_file', 'show_disable_file', 'ImportFlag', 'ImportUser', 'ImportDatetime', 'ImportRes']
    fields = ['SallingFile', 'DisableFile', 'ShopName']
    list_display_links = ['', ]
    # actions = ['import_product_info', 'delete_model', ]
    actions = ['delete_model', ]

    def show_salling_file(self, obj):
        rt = obj.SallingFile.name.split('/')[-1]
        return mark_safe(rt)

    show_salling_file.short_description = mark_safe(u'<p align="left"style="color:#428bca;">销售中商品数据</p>')

    def show_disable_file(self, obj):
        rt = obj.DisableFile.name.split('/')[-1]
        return mark_safe(rt)

    show_disable_file.short_description = mark_safe(u'<p align="left"style="color:#428bca;">下架商品数据</p>')

    def has_delete_permission(self, obj=None):
        return False

    def import_product_info(self, request, objs):
        # if request.user.is_superuser:
        for obj in objs:
            salling_file = ''
            disable_file = ''
            if obj.SallingFile:
                salling_file = os.path.join(settings.MEDIA_ROOT, obj.SallingFile.name)
            if obj.DisableFile:
                disable_file = os.path.join(settings.MEDIA_ROOT, obj.DisableFile.name)

            # obj.ImportFlag = True
            # obj.ImportUser = request.user.first_name
            # obj.ImportDatetime = datetime.datetime.now()
            # obj.save()

            uploadfile_id = obj.id
            import_user = request.user.first_name

            aliexpress_import_products_task(
                salling_file=salling_file,
                disable_file=disable_file,
                shopname=obj.ShopName,
                uploadfile_id=uploadfile_id,
                import_user=import_user
            )
        # else:
        #     messages.error(self.request, u'导入功能将被取消，目前上传文件后会自动导入数据，无需手动导入')
        messages.info(self.request, u'商品数据导入完成')
        # messages.info(self.request, u'商品数据正在导入中......')

    import_product_info.short_description = u'导入选中上传数据'

    def delete_model(self, request, objs):
        for obj in objs:
            if request.user.first_name == obj.UploadUser or request.user.is_superuser:
                SallingFile_name = obj.SallingFile
                DisableFile_name = obj.DisableFile
                if SallingFile_name:
                    try:
                        os.remove(os.path.join(settings.MEDIA_ROOT, SallingFile_name.name))
                    except:
                        pass
                if DisableFile_name:
                    try:
                        os.remove(os.path.join(settings.MEDIA_ROOT, DisableFile_name.name))
                    except:
                        pass
                obj.delete()
            else:
                messages.error(request, u'非管理员只可删除自己上传的商品信息文件')
                break
        messages.info(request, u'删除成功')

    delete_model.short_description = u'删除选中上传数据'

    def save_models(self):
        request = self.request
        obj = self.new_obj
        SallingFile_obj = request.FILES.get('SallingFile')
        DisableFile_obj = request.FILES.get('DisableFile')
        ShopName = request.POST.get('ShopName')
        now_time = datetime.datetime.now().strftime('%H_%M_%S')
        first_name = request.user.first_name
        if SallingFile_obj:
            SallingFile_obj.name = first_name + '-' + now_time + '-' + SallingFile_obj.name
            obj.SallingFile = SallingFile_obj
        if DisableFile_obj:
            DisableFile_obj.name = first_name + '-' + now_time + '-' + DisableFile_obj.name
            obj.DisableFile = DisableFile_obj
        if ShopName:
            obj.ShopName = ShopName
        if not SallingFile_obj and not DisableFile_obj and not obj.SallingFile and not obj.DisableFile:
            messages.error(request, u'请上传对应Excel文件')
            return
        obj.UploadUser = first_name
        obj.UploadDatetime = datetime.datetime.now()
        obj.ImportRes = 'Importing File, Please Wait a little later'
        obj.save()

        # 导入数据
        salling_file = ''
        disable_file = ''

        if obj.SallingFile:
            salling_file = os.path.join(settings.MEDIA_ROOT, obj.SallingFile.name)

        if obj.DisableFile:
            disable_file = os.path.join(settings.MEDIA_ROOT, obj.DisableFile.name)

        # Upload File To OSS
        upload_oss_obj = upload_to_oss(settings.BUCKETNAME_XLS)
        salling_params = dict()
        disable_params = dict()
        if SallingFile_obj:
            salling_params['del'] = 0
            salling_params['path'] = 'aliexpress_products/%s/salling_file' % ShopName
            salling_params['name'] = SallingFile_obj.name
            salling_params['byte'] = open(salling_file)
            salling_res = upload_oss_obj.upload_to_oss(salling_params)
            print 'salling_res', salling_res
            try:
                os.remove(salling_file)
            except:
                pass
        if DisableFile_obj:
            disable_params['del'] = 0
            disable_params['path'] = 'aliexpress_products/%s/disable_file' % ShopName
            disable_params['name'] = DisableFile_obj.name
            disable_params['byte'] = open(disable_file)
            disable_res = upload_oss_obj.upload_to_oss(disable_params)
            print 'disable_res', disable_res
            try:
                os.remove(disable_file)
            except:
                pass

        uploadfile_id = obj.id
        import_user = request.user.first_name

        # TODO delay
        # aliexpress_import_products_task(
        aliexpress_import_products_task.delay(
            salling_file=salling_params,
            disable_file=disable_params,
            shopname=obj.ShopName,
            uploadfile_id=uploadfile_id,
            import_user=import_user
        )

        messages.info(request, u'正在导入商品数据，请稍后...')

    def get_list_queryset(self):
        request = self.request
        qs = super(t_aliexpress_upload_product_info_Admin, self).get_list_queryset()

        shopname = request.GET.get('shopname', '').strip()
        uploadPerson = request.GET.get('uploadPerson', '').strip()
        importPerson = request.GET.get('importPerson', '').strip()
        uploadTimeStart = request.GET.get('uploadTimeStart', '')
        uploadTimeEnd = request.GET.get('uploadTimeEnd', '')
        importTimeStart = request.GET.get('importTimeStart', '')
        importTimeEnd = request.GET.get('importTimeEnd', '')
        importFlag = request.GET.get('importFlag', '')

        searchList = {
            'ShopName__exact': shopname,
            'UploadUser__exact': uploadPerson,
            'ImportUser__exact': importPerson,
            'UploadDatetime__gte': uploadTimeStart,
            'UploadDatetime__lt': uploadTimeEnd,
            'ImportDatetime__gte': importTimeStart,
            'ImportDatetime__lt': importTimeEnd,
        }

        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    sl[k] = v

        if importFlag:
            if importFlag == 'True':
                importFlag = True
            elif importFlag == 'False':
                importFlag = False
            else:
                importFlag = ''

            if importFlag != '':
                sl['ImportFlag__exact'] = importFlag
            else:
                pass

        if sl is not None:
            try:
                qs = qs.filter(**sl)
            except Exception:
                messages.error(request, u'输入的查询数据有问题！')

        if request.user.is_superuser or (23, u'组长') in request.user.groups.values_list():
            return qs
        else:
            objs = t_store_configuration_file.objects.filter(
                Q(Seller=request.user.first_name) | Q(Published=request.user.first_name) | Q(
                    Operators=request.user.first_name)).values('ShopName')
            if objs.exists():
                shoplist = []
                for obj in objs:
                    shoplist.append(obj['ShopName'])
                return qs.filter(ShopName__in=shoplist)
            else:
                return qs.none()
