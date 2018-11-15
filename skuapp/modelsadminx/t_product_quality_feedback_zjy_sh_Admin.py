# coding=utf-8


from django.utils.safestring import mark_safe
from django.contrib import messages
from datetime import datetime
from skuapp.table.t_product_quality_feedback_zjy import t_product_quality_feedback_zjy as feedback_zjy
from skuapp.table.t_product_quality_feedback_cgy import t_product_quality_feedback_cgy as feedback_cgy
from skuapp.table.t_product_quality_feedback_cpzy import t_product_quality_feedback_cpzy as feedback_cpzy
from skuapp.table.t_product_quality_feedback_submit import t_product_quality_feedback_submit as feedback_submit


class t_product_quality_feedback_zjy_sh_Admin(object):
    quality_feedback_flag = True

    def show_img(self, obj):
        rt = u'<img src="%s"  width="120" height="120"><style>img{cursor: pointer; transition: all 0.6s;} ' \
             u'img:hover{transform: scale(2.2);}</style>' % obj.Picture_1
        if obj.Picture_2 or obj.Picture_3 or obj.Picture_4 or obj.Picture_5:
            rt = u"%s<br><a id=pic_%s>全部图片</a><script>$('#pic_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan'," \
                 u"title:'全部图片',fix:false,shadeClose: true,maxmin:true,area:['800px','600px']," \
                 u"content:'/show_feedback_picture/?id=%s&page=zjy_sh',});});</script>" % (rt, obj.id, obj.id, obj.id)
        return mark_safe(rt)

    show_img.short_description = u'<span style="color: #428bca">提交人图片</span>'

    def show_submit(self, obj):
        rr = '<span>提交日期：%s</span><br><span>提交人：%s<span>' % (obj.SubmitTime, obj.Submitter)
        return mark_safe(rr)

    show_submit.short_description = u'<span style="color: #428bca">提交信息</span>'

    def show_product(self, obj):
        sku = u'<span>SKU：%s<span>' % obj.SKU
        plateform = u'<span>平台：%s<span>' % obj.Plateform
        order_id = u'<span>订单号：%s<span>' % obj.OrderID
        rr = u'%s<br>%s<br>%s' % (sku, plateform, order_id)
        return mark_safe(rr)
    show_product.short_description = u'<span style="color: #428bca">订单信息</span>'

    def show_detail(self, obj):
        detail_list = obj.Detail.split('\n')
        rr = ''
        for detail in detail_list:
            if rr == '':
                rr = '<span >%s</span>' % detail
            else:
                rr = '%s<br><span >%s</span>' % (rr, detail)
        return mark_safe(rr)
    show_detail.short_description = u'<span style="color: #428bca">具体反馈</span>'

    list_display = ('id', 'show_product', 'show_submit', 'show_img', 'ProblemType', 'show_detail',
                    'CPZY', 'CPZY_Note', 'CGY', 'CGY_Note', 'Reject_Reason', 'State')
    list_display_links = ('',)
    list_editable = ('Reject_Reason',)
    actions = ['to_receive', 'to_reject']

    def set_step(self, query, to_step, rt, user_name):
        time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        table_contrast_dict = {'submit': feedback_submit, 'cpzy': feedback_cpzy, 'cgy': feedback_cgy}
        table_objs = table_contrast_dict[query.Source_Origin].objects.filter(id=query.Source_ID)
        if table_objs:
            step_list = eval(table_objs[0].Step)
            last_step_dict = step_list[-1]
            if rt == 'lq':
                last_step_dict['state'] = u'领取'
                last_step_dict['reject_reason'] = query.Reject_Reason
                last_step_dict['name'] = user_name
                temp_dict = {'time': time_now, 'step': to_step, 'name': user_name, 'state': u'未处理',
                             'note': '', 'reject_reason': query.Reject_Reason}
            else:
                last_step_dict['reject_reason'] = query.Reject_Reason
                last_step_dict['name'] = user_name
                if rt == 'bhcg':
                    last_step_dict['state'] = u'驳回到采购员反馈'
                    temp_dict = {'time': time_now, 'step': to_step, 'name': query.CGY, 'state': u'被驳回',
                                 'note': '', 'reject_reason': query.Reject_Reason}
                else:
                    last_step_dict['state'] = u'驳回到产品专员反馈'
                    temp_dict = {'time': time_now, 'step': to_step, 'name': query.CPZY, 'state': u'被驳回',
                                 'note': '', 'reject_reason': query.Reject_Reason}

            step_list.append(temp_dict)
            table_objs.update(Step=step_list)

    def to_receive(self, request, queryset):
        for query in queryset:
            if query.State == 'wcl':
                user_name = request.user.first_name
                feedback_zjy.objects.create(SubmitTime=query.SubmitTime, Submitter=query.Submitter,
                                            SKU=query.SKU, Plateform=query.Plateform, OrderID=query.OrderID,
                                            ProblemType=query.ProblemType, Detail=query.Detail,
                                            CPZY=query.CPZY, CPZY_Note=query.CPZY_Note,
                                            CGY=query.CGY, CGY_Note=query.CGY_Note,
                                            ZJY=user_name, ZJY_Note='', State='wcl', Reject_Reason='',
                                            Source_Origin=query.Source_Origin, Source_ID=query.Source_ID,
                                            Picture_1=query.Picture_1, Picture_2=query.Picture_2,
                                            Picture_3=query.Picture_3, Picture_4=query.Picture_4,
                                            Picture_5=query.Picture_5, Last_ID=query.id)
                query.State = 'ylq'
                query.ZJY = user_name
                query.save()
                self.set_step(query, u'质检员反馈', 'lq', user_name)
            else:
                messages.error(request, '编号：%s  已经领取，请勿重复领取！！！' % query.id)

    to_receive.short_description = u'领取'

    def to_reject(self, request, queryset):
        for query in queryset:
            if query.State == 'wcl':
                if query.Reject_Reason:
                    user_name = request.user.first_name
                    if query.CGY_Note:
                        feedback_cgy.objects.filter(id=query.Last_ID).update(State='bh',
                                                                             Reject_Reason=query.Reject_Reason)
                        self.set_step(query, u'采购员反馈', 'bhcg', user_name)
                    else:
                        feedback_cpzy.objects.filter(id=query.Last_ID).update(State='bh',
                                                                              Reject_Reason=query.Reject_Reason)
                        self.set_step(query, u'产品专员反馈', 'bhcp', user_name)
                    query.ZJY = user_name
                    query.State = 'bh'
                    query.save()
                else:
                    messages.error(request, '编号：%s  未填写驳回原因，请填写后再提交！！！' % query.id)
            else:
                messages.error(request, '编号：%s  已经被处理，您无法再进行驳回！！！' % query.id)

    to_reject.short_description = u'驳回'

    def get_list_queryset(self, ):
        request = self.request
        qs = super(t_product_quality_feedback_zjy_sh_Admin, self).get_list_queryset()
        cate = request.GET.get('cate', '')

        if cate == '':
            qs = qs.filter(State='wcl')
        elif cate == 'all':
            qs = qs
        else:
            qs = qs.filter(State=cate)

        return qs
