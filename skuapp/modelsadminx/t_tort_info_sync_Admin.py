#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: t_tort_info_sync_Admin.py
 @time: 2018-05-16 13:47
"""
import oss2
from datetime import datetime
from xlwt import *
from .t_product_Admin import mkdir_p, os
from django.utils.safestring import mark_safe
from django.contrib import messages
from skuapp.table.t_product_mainsku_sku import t_product_mainsku_sku
from Project.settings import *
from skuapp.public.const import tort
from django.http import HttpResponse
import json
from django.db import connection

class t_tort_info_sync_Admin(object):
    search_box_flag = True
    t_tort_tree_menu_flag = True
    downloadxls = True

    def show_ProductPicUrl(self, obj):
        url = u'%s%s.%s/%s/%s/%s' % (PREFIX, BUCKETNAME_TORT, ENDPOINT_OUT, 'aliexpress', obj.ID, str(obj.ProductPicUrl))
        alt = u'无法显示:%s,%s' % (obj.Site, obj.MainSKU)
        title = 'Site:%s,MainSKU:%s' % (obj.Site, obj.MainSKU)
        rt = '<img src="%s"  width="150" height="150"  alt = "%s"  title="%s"  />  ' % (url, alt, title)
        return mark_safe(rt)

    show_ProductPicUrl.short_description = u'<span style="color: #428bca">产品图片</span>'

    def show_ReceiveDetail(self, obj):
        rt = u'<span >%s</span>' % obj.ReceiveDetail
        return mark_safe(rt)

    show_ReceiveDetail.short_description = u'<span style="color: #428bca">领用详细信息</span>'
    
    def show_AttachmentUrls(self, obj):
        rt = ''
        if obj.AttachmentUrl1 is not None and str(obj.AttachmentUrl1).strip() !='' :
            attachmentUrl1 =  u'%s%s.%s/%s/%s/%s'%(PREFIX,BUCKETNAME_TORT,ENDPOINT_OUT,'aliexpress',obj.ID,str(obj.AttachmentUrl1))
            rt="%s<a href=%s>%s</a>;<br>"%(rt,attachmentUrl1, u'附件一')
        if obj.AttachmentUrl2 is not None and str(obj.AttachmentUrl2).strip() !='' :
            attachmentUrl2 =  u'%s%s.%s/%s/%s/%s'%(PREFIX,BUCKETNAME_TORT,ENDPOINT_OUT,'aliexpress',obj.ID,str(obj.AttachmentUrl2))
            rt="%s<a href=%s>%s</a>;<br>"%(rt,attachmentUrl2, u'附件二')
        if obj.AttachmentUrl3 is not None and str(obj.AttachmentUrl3).strip() !='' :
            attachmentUrl3 =  u'%s%s.%s/%s/%s/%s'%(PREFIX,BUCKETNAME_TORT,ENDPOINT_OUT,'aliexpress',obj.ID,str(obj.AttachmentUrl3))
            rt="%s<a href=%s>%s</a>;<br>"%(rt,attachmentUrl3, u'附件三')
        if obj.AttachmentUrl4 is not None and str(obj.AttachmentUrl4).strip() !='' :
            attachmentUrl4 =  u'%s%s.%s/%s/%s/%s'%(PREFIX,BUCKETNAME_TORT,ENDPOINT_OUT,'aliexpress',obj.ID,str(obj.AttachmentUrl4))
            rt="%s<a href=%s>%s</a>;<br>"%(rt,attachmentUrl4, u'附件四')
        if obj.AttachmentUrl5 is not None and str(obj.AttachmentUrl5).strip() !='' :
            attachmentUrl5 =  u'%s%s.%s/%s/%s/%s'%(PREFIX,BUCKETNAME_TORT,ENDPOINT_OUT,'aliexpress',obj.ID,str(obj.AttachmentUrl5))
            rt="%s<a href=%s>%s</a>;<br>"%(rt,attachmentUrl5, u'附件五')
        if obj.AttachmentUrl6 is not None and str(obj.AttachmentUrl6).strip() !='' :
            attachmentUrl6 =  u'%s%s.%s/%s/%s/%s'%(PREFIX,BUCKETNAME_TORT,ENDPOINT_OUT,'aliexpress',obj.ID,str(obj.AttachmentUrl6))
            rt="%s<a href=%s>%s</a>;<br>"%(rt,attachmentUrl6, u'附件六')

        return mark_safe(rt)
    show_AttachmentUrls.short_description = mark_safe('<p style="color:#428bca;">附件列表</p>')
    
    def show_Site(self, obj):
        return mark_safe(obj.Site)

    show_Site.short_description = mark_safe('<p style="color:#428bca;">侵权站点</p>')

    list_display = ('ID', 'show_ProductPicUrl', 'StaffID', 'Site',
                    'MainSKU', 'ProductTitle', 'Intellectual',
                    'SalerName2', 'Purchaser', 'show_AttachmentUrls'
                    )

    readonly_fields = ('ID',)

    actions = [ '_online_tort_syn_puyuan', 'to_sync',]


    def _online_tort_syn_puyuan(self, request, queryset):
        from brick.table.t_operation_log_online_syn_py import t_operation_log_online_syn_py
        operation_log_obj = t_operation_log_online_syn_py(DBConn=connection)
        from app_djcelery.tasks import online_tort_syn_to_puyuan_task

        first_name = request.user.first_name
        user_name = request.user.username
        now_time = datetime.now()

        sResult = {'rcode': '0', 'messages': ''}  # 初始状态
        opnum = 'sku_tort_%s_%s' % (now_time.strftime('%Y%m%d%H%M%S'), user_name)
        try:
            param = {}  # 操作日志的参数
            param['OpNum'] = opnum
            param['OpKey'] = queryset.values_list("MainSKU", flat=True)
            param['OpType'] = 'sku_tort'
            param['Status'] = 'runing'
            param['ErrorInfo'] = ''
            param['OpPerson'] = first_name
            param['OpTime'] = now_time
            param['OpStartTime'] = now_time
            param['OpEndTime'] = None
            param['aNum'] = len(queryset)
            param['rNum'] = 0
            param['eNum'] = 0
            iResult = operation_log_obj.createLog(param)
            assert iResult['errorcode'] == 0, "insert log error."

            all_data_list = []
            non_existent_mainsku = []
            for qs in queryset:
                main_sku = qs.MainSKU
                single_data_list = []
                if qs.Step not in [tort.TORT_LIST, tort.COM_TORT_LIST]:
                    messages.error(request, u'此主SKU(%s)暂不能导出,非侵权状态!' % (main_sku,))
                    continue
                sku_objs = t_product_mainsku_sku.objects.filter(MainSKU=qs.MainSKU)
                id_1 = 0
                id_2 = 0
                if sku_objs.exists():
                    for sku_obj in sku_objs:
                        if sku_obj.ProductSKU is not None and sku_obj.ProductSKU.strip() != '':
                            sku = sku_obj.ProductSKU
                            if qs.Intellectual == 'CopyRights':
                                link_url3 = '著作权(CopyRights)'
                            elif qs.Intellectual == 'TradeMark':
                                link_url3 = '商标(TradeMark)'
                            elif qs.Intellectual == 'DesignPatent':
                                link_url3 = '外观专利(DesignPatent)'
                            elif qs.Intellectual == 'Patent':
                                link_url3 = '专利(Patent)'
                            else:
                                link_url3 = '其它(Else)'
                            #link_url3 = qs.ComplainReason
                            link_url6 = qs.Site
                            temp_dict_1 = {'SKU': sku, 'columnname': 'LinkUrl3', 'columnvalue': link_url3}
                            temp_dict_2 = {'SKU': sku, 'columnname': 'LinkUrl6', 'columnvalue': link_url6}
                            single_data_list.append(temp_dict_1)
                            single_data_list.append(temp_dict_2)

                    if qs.Step in [tort.TORT_LIST]:
                        id_1 = int(qs.ID)
                    else:
                        id_2 = int(qs.ID)
                    all_data_list.append(
                        {'main_sku': main_sku, 'single_data_list': single_data_list, 'id_1': id_1, 'id_2': id_2}
                    )
                else:
                    all_data_list.append(
                        {'main_sku': main_sku, 'single_data_list': [], 'id_1': id_1, 'id_2': id_2}
                    )
            online_tort_syn_to_puyuan_task.delay(tort_data_list=all_data_list, opnum=opnum, now_time=now_time, user_name=user_name)
            sResult['rcode'] = 1
            sResult['KEY'] = opnum
        except Exception, e:
            sResult['rcode'] = -1
            sResult['messages'] = '%s:%s' % (Exception, e)
        return HttpResponse(json.dumps(sResult))
        # messages.info(request, '%s' % all_data_list)
    _online_tort_syn_puyuan.short_description = u'侵权统计同步普源'


    def to_sync(self, request, queryset):
        try:
            path = MEDIA_ROOT + 'download_xls/' + request.user.username
            mkdir_p(MEDIA_ROOT + 'download_xls')
            os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls', ))

            mkdir_p(path)
            os.popen('chmod 777 %s' % (path, ))

            w = Workbook()
            sheet = w.add_sheet(u'改侵权')

            sheet.write(0, 0, u'SKU')
            sheet.write(0, 1, u'网页URL6')
            sheet.write(0, 2, u'停售')
            sheet.write(0, 3, u'网页URL3')

            # 写数据
            row = 0
            id_list = []
            id_list_com = []
            for qs in queryset:
                if qs.Step not in [tort.TORT_LIST,tort.COM_TORT_LIST]:
                    messages.warning(request, u'此主SKU(%s)暂不能导出,非侵权状态!' % (qs.MainSKU,))
                    continue
                    
                sku_objs = t_product_mainsku_sku.objects.filter(MainSKU=qs.MainSKU)
                for sku_obj in sku_objs:
                    #if sku_obj.ProductSKU is not None and sku_obj.ProductSKU.strip() != '':
                    row = row + 1
                    column = 0
                    sheet.write(row, column, sku_obj.ProductSKU)  # 商品SKU

                    column = column + 1
                    sheet.write(row, column, qs.Site)  # 站点

                    column = column + 1
                    sheet.write(row, column, 'not edit')  # 停售

                    column = column + 1
                    if qs.Intellectual == 'CopyRights':
                        ComplainReason = '著作权(CopyRights)'
                    elif qs.Intellectual == 'TradeMark':
                        ComplainReason = '商标(TradeMark)'
                    elif qs.Intellectual == 'DesignPatent':
                        ComplainReason = '外观专利(DesignPatent)'
                    elif qs.Intellectual == 'Patent':
                        ComplainReason = '专利(Patent)'
                    else:
                        ComplainReason = '其它(Else)'
                    sheet.write(row, column, ComplainReason)  # 备注
                if qs.Step in [tort.TORT_LIST]:
                    id_list.append(qs.ID)
                else:
                    id_list_com.append(qs.ID)
                if row > 5000:
                    break

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

            #更新状态
            queryset.filter(ID__in=id_list).update(Step=tort.SYNC, SyncStaffID=request.user.username, SyncTime=datetime.now())
            queryset.filter(ID__in=id_list_com).update(Step=tort.SYNC_COM, SyncStaffID=request.user.username, SyncTime=datetime.now())
            messages.info(request, u'成功导出侵权数据%d条, 请及时下载维护!' % (row ,))
            messages.error(request, u'%s%s.%s/%s/%s' % (PREFIX, BUCKETNAME_XLS, ENDPOINT_OUT, request.user.username,
                                                        filename) + u':成功导出侵权数据,可点击Download下载到本地............................。')
        except Exception, e:
            messages.error(request, u'数据导出有误,Error:%s!' % (repr(e),))

    to_sync.short_description = u'导出同步失败数据'

    def to_sync_cancel(self, request, queryset):
        try:
            path = MEDIA_ROOT + 'download_xls/' + request.user.username
            mkdir_p(MEDIA_ROOT + 'download_xls')
            os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls', ))

            mkdir_p(path)
            os.popen('chmod 777 %s' % (path, ))

            w = Workbook()
            sheet = w.add_sheet(u'改侵权')

            sheet.write(0, 0, u'SKU')
            sheet.write(0, 1, u'网页URL6')
            sheet.write(0, 2, u'重新开售')
            sheet.write(0, 3, u'网页URL3')

            # 写数据
            row = 0
            id_list = []
            for qs in queryset:
                if qs.Step not in [tort.CANCEL_WAIT_RECEIVE, tort.CANCEL_ALREADY_RECEIVE]:
                    messages.warning(request, u'此主SKU(%s)暂不能导出,非侵权撤销状态!' % (qs.MainSKU,))
                    continue

                sku_objs = t_product_mainsku_sku.objects.filter(MainSKU=qs.MainSKU)
                for sku_obj in sku_objs:
                    if sku_obj.ProductSKU is not None and sku_obj.ProductSKU.strip() != '':
                        row = row + 1
                        column = 0
                        sheet.write(row, column, sku_obj.ProductSKU)  # 商品SKU

                        column = column + 1
                        sheet.write(row, column, ' ')  # 站点

                        column = column + 1
                        sheet.write(row, column, 'not edit')  # 重新开售

                        column = column + 1
                        sheet.write(row, column, ' ')  # 备注

                id_list.append(qs.ID)
                if row > 5000:
                    break

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

            #更新状态
            queryset.filter(ID__in=id_list).update(Step=tort.CANCEL_SYNC, SyncStaffID=request.user.username, SyncTime=datetime.now())

            messages.info(request, u'成功导出侵权撤销数据%d条, 请及时下载维护!' % (row ,))
            messages.error(request, u'%s%s.%s/%s/%s' % (PREFIX, BUCKETNAME_XLS, ENDPOINT_OUT, request.user.username,
                                                        filename) + u':成功导出侵权撤销数据,可点击Download下载到本地............................。')
        except Exception, e:
            messages.error(request, u'数据导出有误,Error:%s!' % (repr(e),))

    to_sync_cancel.short_description = u'导出侵权撤销数据'

    def get_list_queryset(self):
        request = self.request
        qs = super(t_tort_info_sync_Admin, self).get_list_queryset()

        Step = request.GET.get('Step', '')
        if Step != '':
            Step = Step.split(',')
        MainSKU = request.GET.get('MainSKU', '')
        Site = request.GET.get('Site', '')
        Intellectual = request.GET.get('Intellectual', '')
        StaffID = request.GET.get('StaffID', '')

        TimeStart = request.GET.get('TimeNameStart', '')
        TimeEnd = request.GET.get('TimeNameEnd', '')

        AuditTimeStart = request.GET.get('AuditTimeStart', '')
        AuditTimeEnd = request.GET.get('AuditTimeEnd', '')

        EnglishName = request.GET.get('EnglishName', '')
        ProductTitle = request.GET.get('ProductTitle', '')

        searchList = {'Step__in': Step,
                      'MainSKU__exact': MainSKU,
                      'Site__exact': Site,
                      'EnglishName__icontains': EnglishName,
                      'ProductTitle__icontains': ProductTitle,
                      'Intellectual__exact': Intellectual,
                      'StaffID__exact': StaffID,
                      'UpdateTime__gte': TimeStart,
                      'UpdateTime__lt': TimeEnd,
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
                messages.error(request, u'输入的查询数据有误！')
        return qs