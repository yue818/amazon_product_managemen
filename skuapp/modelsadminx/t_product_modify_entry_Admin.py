# -*- coding: utf-8 -*-

from .t_product_Admin import *
from datetime import datetime
from brick.public.product_modify_show_function import product_modify_show_function


class t_product_modify_entry_Admin(product_modify_show_function):
    search_box_flag = True
    enter_ed_classification = True
    downloadxls = True

    list_display = (
        'id', 'MainSKU', 'show_SKU_InputBox', 'show_PIC', 'show_product', 'Select',
        'show_XGcontext', 'show_details', 'Mstatus', 'show_sq', 'show_sh', 'BHRemark'
    )
    list_editable = ('BHRemark',)
    list_display_links = ('',)
    actions = ['to_rebut', 'to_LR', 'to_excel', 'to_excel_new', 'to_excel_reduction', '_complete_to_modify_puyuan']

    def to_rebut(self, request, queryset):
        for querysetid in queryset.all():
            t_product_information_modify.objects.filter(id=querysetid.id).\
                update(Mstatus="BBH", LQTime=datetime.now(), LQStaffName=request.user.first_name)
    to_rebut.short_description = u"驳回"

    def to_LR(self, request, queryset):
        for querysetid in queryset.all():
            if querysetid.Mstatus == "DXG":
                t_product_information_modify.objects.filter(id=querysetid.id).\
                    update(Mstatus="WCXG", XGTime=datetime.now(), XGStaffName=request.user.first_name)
    to_LR.short_description = u"信息录入完成"

    def _complete_to_modify_puyuan(self, request, queryset):
        from brick.table.t_operation_log_online_syn_py import t_operation_log_online_syn_py
        operation_log_obj = t_operation_log_online_syn_py(DBConn=connection)
        from app_djcelery.tasks import online_modify_puyuan_task

        first_name = request.user.first_name
        user_name = request.user.username
        now_time = datetime.now()

        sResult = {'rcode': '0', 'messages': ''}  # 初始状态
        opnum = 'modify_sku_%s_%s' % (now_time.strftime('%Y%m%d%H%M%S'), user_name)
        try:
            param = {}  # 操作日志的参数
            param['OpNum'] = opnum
            param['OpKey'] = queryset.values_list("MainSKU", flat=True)
            param['OpType'] = 'modify_sku'
            param['Status'] = 'runing'
            param['ErrorInfo'] = ''
            param['OpPerson'] = request.user.first_name
            param['OpTime'] = now_time
            param['OpStartTime'] = now_time
            param['OpEndTime'] = None
            param['aNum'] = len(queryset)
            param['rNum'] = 0
            param['eNum'] = 0
            iResult = operation_log_obj.createLog(param)
            assert iResult['errorcode'] == 0, "insert log error."
            modify_data_list = []
            for qs in queryset:
                modify_id = int(qs.id)
                details = eval(qs.Details) if qs.Details else {}
                modify_status = qs.Mstatus
                main_sku = qs.MainSKU
                apply_name = qs.SQStaffNameing if qs.SQStaffNameing else ''
                select = qs.Select
                temp_dict = {
                    'modify_id': modify_id, 'details': details, 'modify_status': modify_status,
                    'main_sku': main_sku, 'apply_name': apply_name, 'select': select
                }
                modify_data_list.append(temp_dict)
            online_modify_puyuan_task.delay(modify_data_list=modify_data_list, first_name=first_name, opnum=opnum)
            sResult['rcode'] = 1
            sResult['KEY'] = opnum
        except Exception, e:
            sResult['rcode'] = -1
            sResult['messages'] = '%s:%s' % (Exception, e)
            messages.error(request, '------%s' % sResult['messages'])
        return HttpResponse(json.dumps(sResult))
    _complete_to_modify_puyuan.short_description = u'录入完成(同步普源)'

    def get_list_queryset(self):
        request = self.request
        qs = super(t_product_modify_entry_Admin, self).get_list_queryset()
        qs = qs.filter(Mstatus='DXG')

        flagcloth = request.GET.get('classCloth', '')
        MainSKU = request.GET.get('MainSKU', '')
        SKU = request.GET.get('SKU', '')
        Name2 = request.GET.get('Name2', '')
        KFTimeStart = request.GET.get('KFTimeStart', '')
        KFTimeEnd = request.GET.get('KFTimeEnd', '')
        Select = request.GET.get('Select', '')
        SQStaffNameing = request.GET.get('SQStaffNameing', '')
        SQTimeingStart = request.GET.get('SQTimeingStart', '')
        SQTimeingEnd = request.GET.get('SQTimeingEnd', '')
        SHStaffName = request.GET.get('SHStaffName', '')
        SHTimeStart = request.GET.get('SHTimeStart', '')
        SHTimeEnd = request.GET.get('SHTimeEnd', '')

        if Select == '22':
            qs = qs.filter(CostReduction__isnull=False)
            searchList = {
                'MainSKU__exact': MainSKU, 'SKU__contains': SKU, 'Name2__exact': Name2, 'DevDate__gte': KFTimeStart,
                'DevDate__lt': KFTimeEnd, 'SQStaffNameing__exact': SQStaffNameing, 'SQTimeing__gte': SQTimeingStart,
                'SQTimeing__lt': SQTimeingEnd, 'SHStaffName__exact': SHStaffName, 'SHTime__gte': SHTimeStart,
                'SHTime__lt': SHTimeEnd
            }
        else:
            if Select == '1000':
                searchList = {
                    'MainSKU__exact': MainSKU, 'SKU__contains': SKU, 'Name2__exact': Name2, 'DevDate__gte': KFTimeStart,
                    'DevDate__lt': KFTimeEnd, 'PackFlag__exact': '1', 'SQStaffNameing__exact': SQStaffNameing,
                    'SQTimeing__gte': SQTimeingStart, 'SQTimeing__lt': SQTimeingEnd, 'SHStaffName__exact': SHStaffName,
                    'SHTime__gte': SHTimeStart, 'SHTime__lt': SHTimeEnd
                }

            else:
                searchList = {
                    'MainSKU__exact': MainSKU, 'SKU__contains': SKU, 'Name2__exact': Name2, 'DevDate__gte': KFTimeStart,
                    'DevDate__lt': KFTimeEnd, 'Select__exact': Select, 'SQStaffNameing__exact': SQStaffNameing,
                    'SQTimeing__gte': SQTimeingStart, 'SQTimeing__lt': SQTimeingEnd, 'SHStaffName__exact': SHStaffName,
                    'SHTime__gte': SHTimeStart, 'SHTime__lt': SHTimeEnd
                }

        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    if k == 'ShopName__exact':
                        v = 'Wish-' + v.zfill(4)
                    sl[k] = v
        if sl is not None:
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'输入的查询数据有问题！')

        catelist = [u'001.时尚女装', u'002.时尚男装', u'021.泳装', u'024.童装', u'025.内衣']

        if flagcloth == '1':
            return qs.filter(LargeCategory__in=catelist)
        elif flagcloth == '2':
            return qs.exclude(LargeCategory__in=catelist)
        else:
            return qs



