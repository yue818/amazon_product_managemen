# -*- coding: utf-8 -*-
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from skuapp.table.t_cloth_factory_dispatch_apply import *
from datetime import datetime
from skuapp.table.t_product_depart_get import t_product_depart_get
from pyapp.models import b_goods as py_b_goods
from django.contrib import messages
from django.utils.safestring import mark_safe

class t_cloth_factory_dispatch_apply_Admin(object):
    #actions = ['to_distribute',  ]
    search_box_flag = True
    t_cloth_factory = True
    '''
    def to_distribute(self, request, objs):
        from skuapp.table.t_cloth_factory_dispatch_audit import t_cloth_factory_dispatch_audit
        for obj in objs:

            #t_cloth_factory_dispatch_obj.__dict__ = obj.__dict__
            #t_cloth_factory_dispatch_apply_obj.__dict__ = obj.__dict__
            #根据SKU查看t_cloth_factory_dispatch表是否存在已有申请记录
            #t_cloth_factory_dispatch_objs = t_cloth_factory_dispatch.objects.filter(SKU=obj.SKU)
            #messages.success(request, t_cloth_factory_dispatch_objs)
            t_cloth_factory_dispatch_audit_objs = t_cloth_factory_dispatch_audit.objects.filter(SKU=obj.SKU,currentState=None)
            if t_cloth_factory_dispatch_audit_objs is None or t_cloth_factory_dispatch_audit_objs.count() == 0:
                messages.error(request, "sku=%s 没有该改商品填写派单信息，请先填写派单信息"%(obj.SKU))
            else:
                i = 0
                for t_cloth_factory_dispatch_audit_obj in t_cloth_factory_dispatch_audit_objs:
                    i += 1
                    if i > 1:
                        t_cloth_factory_dispatch_audit_obj.delete()
                    t_cloth_factory_dispatch_audit_obj.applyMan = request.user.first_name
                    t_cloth_factory_dispatch_audit_obj.applyDate = datetime.now()
                    t_cloth_factory_dispatch_audit_obj.currentState = '2'
                    t_cloth_factory_dispatch_audit_obj.save()
            # 修改操作记录
            #t_product_oplog.objects.filter(pid=querysetid.id, StepID='JZL').update(MainSKU='', EndTime=datetime.now())
    to_distribute.short_description = u'派单申请'
    '''

    def updateApplyInfo(self, obj):
        rt = ''
        from skuapp.table.t_cloth_factory_dispatch_audit import t_cloth_factory_dispatch_audit
        t_cloth_factory_dispatch_audit_objs = t_cloth_factory_dispatch_audit.objects.filter(SKU=obj.SKU,
                                                                                                currentState='2')
        from skuapp.table.t_cloth_factory_dispatch_no_audit import t_cloth_factory_dispatch_no_audit
        t_cloth_factory_dispatch_no_audit_objs = t_cloth_factory_dispatch_no_audit.objects.filter(SKU=obj.SKU,
                                                                                            currentState='1')
        if t_cloth_factory_dispatch_audit_objs.count() != 0:
            rt = u"<font color:#3C3C3C>已申请</font> \t\t<a href='/Project/admin/skuapp/t_cloth_factory_dispatch_audit'>跳转至审核</a>"
            return mark_safe(rt)
        elif t_cloth_factory_dispatch_no_audit_objs.count() != 0:
            rt = u"<font color:#3C3C3C>已申请</font> \t\t<a href='/Project/admin/skuapp/t_cloth_factory_dispatch_no_audit'>跳转至审核未通过</a>"
            return mark_safe(rt)
        else:
            rt = u"<a id=update_applyInfo%s>新增派单信息</a><script>$('#update_applyInfo%s').on('click',function(){layer.open(" \
                 u"{type:2,skin:'layui-layer-lan',title:'申请编辑',fix:false,shadeClose: true,maxmin:true," \
                 u"area:['1200px','800px'],content:'/t_cloth_factor_eidt/update_applyInfo/?sku=%s',end: function(){ location.reload(); }});});</script>" % (
                obj.id, obj.id, obj.SKU)

        return mark_safe(rt)

    updateApplyInfo.short_description = mark_safe(u'<p style="width:160px;color:#428bca;" align="center">申请编辑信息</p>')

    list_per_page = 20
    list_display = ('id','SKU', 'goodsname','Supplier','OSCode','goodsstate','goodsCostPrice','oosNum','buyer','updateApplyInfo',)
    #readonly_fields = ('id','SKU', 'goodsname','Supplier','goodsstate','goodsCostPrice','oosNum','occupyNum','stockNum','ailableNum','sevenSales','fifteenSales', 'thirtySales','PurchaseNotInNum','buyer',)
    #show_detail_fields = ['id']


    def get_list_queryset(self):
        request = self.request
        qs = super(t_cloth_factory_dispatch_apply_Admin, self).get_list_queryset()

        #PurchaseNotInNum = request.GET.get('PurchaseNotInNum', '')
        SKU = request.GET.get('SKU', '')
        PurchaseNotInNumStart = request.GET.get('PurchaseNotInNumStart', '')
        PurchaseNotInNumEnd = request.GET.get('PurchaseNotInNumEnd', '')

        searchList = {'SKU__exact': SKU,
                      'PurchaseNotInNum__gte': PurchaseNotInNumStart, 'PurchaseNotInNum__lt': PurchaseNotInNumEnd,
                      }
        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    # if k == 'ShopName__exact':
                    #  v = 'Wish-' + v.zfill(4)
                    # messages.error(request, v)
                    sl[k] = v
        if sl is not None:
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'输入的查询数据有问题！')

        '''
        'PurchaseNotInNum': PurchaseNotInNum,
        allobj = User.objects.filter(groups__id__in=[6])
        userID = []
        for each in allobj:
            userID.append(each.id)
        if (request.user.id in userID) or (request.user.is_superuser == 1):
            qs = qs.filter(Q(Mstatus='DLQ') | Q(Mstatus='BBH') | Q(Mstatus='DHT'))
        else:
            qs = qs.filter(SQStaffNameing=request.user.first_name).filter(
                Q(Mstatus='DLQ') | Q(Mstatus='BBH') | Q(Mstatus='DHT'))
        '''
        return qs

