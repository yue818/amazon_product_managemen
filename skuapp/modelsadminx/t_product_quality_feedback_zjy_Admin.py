# coding=utf-8


from django.utils.safestring import mark_safe
from django.contrib import messages
from datetime import datetime
from skuapp.table.t_product_quality_feedback_ck import t_product_quality_feedback_ck as feedback_ck
from skuapp.table.t_product_quality_feedback_final_sh import t_product_quality_feedback_final_sh as feedback_final_sh
from skuapp.table.t_product_quality_feedback_submit import t_product_quality_feedback_submit as feedback_submit
from skuapp.table.t_product_quality_feedback_cpzy import t_product_quality_feedback_cpzy as feedback_cpzy
from skuapp.table.t_product_quality_feedback_cgy import t_product_quality_feedback_cgy as feedback_cgy


class t_product_quality_feedback_zjy_Admin(object):
    quality_feedback_flag = True
    search_box_flag = True

    def show_img(self, obj):
        rt = u'<img src="%s"  width="120" height="120"><style>img{cursor: pointer; transition: all 0.6s;} ' \
             u'img:hover{transform: scale(4);}</style>' % obj.Picture_1
        if obj.Picture_2 or obj.Picture_3 or obj.Picture_4 or obj.Picture_5:
            rt = u"%s<br><a id=pic_%s>全部图片</a><script>$('#pic_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan'," \
                 u"title:'全部图片',fix:false,shadeClose: true,maxmin:true,area:['800px','600px']," \
                 u"content:'/show_feedback_picture/?id=%s&page=zjy',});});</script>" % (rt, obj.id, obj.id, obj.id)
        return mark_safe(rt)
    show_img.short_description = u'<span style="color: #428bca">提交人图片</span>'


    def show_img_zjy(self, obj):
        rt = u'<img src="%s"  width="120" height="120"><style>img{cursor: pointer; transition: all 0.6s;} ' \
             u'img:hover{transform: scale(4);}</style>' % 1
        if obj.ZJY_Pic:
            pic_list = obj.ZJY_Pic.split('|')
            rt = u'<img src="%s"  width="120" height="120"><style>img{cursor: pointer; transition: all 0.6s;} ' \
                 u'img:hover{transform: scale(2.2);}</style>' % pic_list[0]
        rt = u"%s<br><a id=img_%s>操作</a><script>$('#img_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan'," \
             u"title:'全部图片',fix:false,shadeClose: true,maxmin:true,area:['800px','600px']," \
             u"content:'/feedback_zjy_picture/?id=%s&page=zjy',});});</script>" % (rt, obj.id, obj.id, obj.id)
        return mark_safe(rt)
    show_img_zjy.short_description = u'<span style="color: #428bca">质检员图片</span>'


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


    list_display = ('id', 'show_product', 'show_submit', 'show_img', 'show_img_zjy', 'ProblemType', 'show_detail',
                    'CPZY', 'CGY', 'ZJY', 'ZJY_Note', 'State', 'Reject_Reason')
    list_display_links = ('',)
    list_editable = ('ZJY_Note', 'Reject_Reason')
    actions = ['to_cpzy', 'to_cgy', 'to_ck', 'to_review', 'to_reject']


    def set_step(self, next_step, next_name, next_state, this_state, this_name, this_note, this_reject, source_origin, source_id):
        """
        判断该信息最初的来源，分别写入到最初来源的处理流程
        :param next_step: 下一步处理流程
        :param next_name: 下一步处理人
        :param next_state: 下一步状态
        :param this_state: 这一步状态
        :param this_name: 这一步处理人
        :param this_note: 这一步备注
        :param this_reject: 这一步驳回原因
        :param source_origin: 最初信息来源表
        :param source_id: 最初来源ID
        :return:
        """
        time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        table_contrast_dict = {'submit': feedback_submit, 'cpzy': feedback_cpzy, 'cgy': feedback_cgy}
        table_objs = table_contrast_dict[source_origin].objects.filter(id=source_id)
        if table_objs:
            step_list = eval(table_objs[0].Step)
            if step_list:
                this_step_dict = step_list[-1]
                this_step_dict['state'] = this_state
                this_step_dict['name'] = this_name
                this_step_dict['note'] = this_note
                this_step_dict['reject_reason'] = this_reject

            temp_dict = {'time': time_now, 'step': next_step, 'name': next_name, 'state': next_state,
                         'note': '', 'reject_reason': ''}
            step_list.append(temp_dict)
            table_objs.update(Step=step_list)


    def to_cpzy(self, request, queryset):
        user_cn = request.user.first_name
        for query in queryset:
            if query.State in ['wcl', 'bbh']:
                if query.ZJY_Note:
                    feedback_cpzy.objects.create(SubmitTime=query.SubmitTime, Submitter=query.Submitter,
                                                 SKU=query.SKU, Plateform=query.Plateform, OrderID=query.OrderID,
                                                 ProblemType=query.ProblemType, Detail=query.Detail,
                                                 CPZY=query.CPZY, CPZY_Note='',
                                                 CGY=query.CGY, CGY_Note='',
                                                 ZJY=user_cn, ZJY_Note=query.ZJY_Note,
                                                 CKY='', CK_Note='',
                                                 State='wcl', Reject_Reason='',
                                                 Source_Origin=query.Source_Origin, Source_ID=query.Source_ID,
                                                 Picture_1=query.Picture_1, Picture_2=query.Picture_2,
                                                 Picture_3=query.Picture_3, Picture_4=query.Picture_4,
                                                 Picture_5=query.Picture_5, Last_ID=query.id, ZJY_Pic=query.ZJY_Pic,
                                                 ClothingFlag=query.ClothingFlag)
                    query.State = 'tjdcpzy'
                    query.ZJY = user_cn
                    query.save()
                    self.set_step(u'产品专员反馈', query.CPZY, u'未处理', u'提交到产品专员', user_cn, query.ZJY_Note,
                                  query.Reject_Reason, query.Source_Origin, query.Source_ID)
                else:
                    messages.error(request, '编号：%s  未填写质检员备注，请填写后再提交！！！' % query.id)
            else:
                messages.error(request, '编号：%s  已经处理，请勿重复提交！！！' % query.id)
    to_cpzy.short_description = u'提交到产品专员'


    def to_cgy(self, request, queryset):
        user_cn = request.user.first_name
        for query in queryset:
            if query.State in ['wcl', 'bbh']:
                if query.ZJY_Note:
                    feedback_cgy.objects.create(SubmitTime=query.SubmitTime, Submitter=query.Submitter,
                                                SKU=query.SKU, Plateform=query.Plateform, OrderID=query.OrderID,
                                                ProblemType=query.ProblemType, Detail=query.Detail,
                                                CPZY=query.CPZY, CPZY_Note='',
                                                CGY=query.CGY, CGY_Note='',
                                                ZJY=user_cn, ZJY_Note=query.ZJY_Note,
                                                CKY='', CK_Note='',
                                                State='wcl', Reject_Reason='',
                                                Source_Origin=query.Source_Origin, Source_ID=query.Source_ID,
                                                Picture_1=query.Picture_1, Picture_2=query.Picture_2,
                                                Picture_3=query.Picture_3, Picture_4=query.Picture_4,
                                                Picture_5=query.Picture_5, Last_ID=query.id, ZJY_Pic=query.ZJY_Pic,
                                                ClothingFlag=query.ClothingFlag)
                    query.State = 'tjdcgy'
                    query.ZJY = user_cn
                    query.save()
                    self.set_step(u'采购员反馈', query.CGY, u'未处理', u'提交到采购员', user_cn, query.ZJY_Note,
                                  query.Reject_Reason, query.Source_Origin, query.Source_ID)
                else:
                    messages.error(request, '编号：%s  未填写质检员备注，请填写后再提交！！！' % query.id)
            else:
                messages.error(request, '编号：%s  已经处理，请勿重复提交！！！' % query.id)
    to_cgy.short_description = u'提交到采购员'


    def to_ck(self, request, queryset):
        user_cn = request.user.first_name
        for query in queryset:
            if query.State in ['wcl', 'bbh']:
                if query.ZJY_Note:
                    feedback_ck.objects.create(SubmitTime=query.SubmitTime, Submitter=query.Submitter,
                                               SKU=query.SKU, Plateform=query.Plateform, OrderID=query.OrderID,
                                               ProblemType=query.ProblemType, Detail=query.Detail,
                                               CPZY=query.CPZY, CPZY_Note='',
                                               CGY=query.CGY, CGY_Note='',
                                               ZJY=user_cn, ZJY_Note=query.ZJY_Note,
                                               CKY='', CK_Note='',
                                               State='wcl', Reject_Reason='',
                                               Source_Origin=query.Source_Origin, Source_ID=query.Source_ID,
                                               Picture_1=query.Picture_1, Picture_2=query.Picture_2,
                                               Picture_3=query.Picture_3, Picture_4=query.Picture_4,
                                               Picture_5=query.Picture_5, Last_ID=query.id, ZJY_Pic=query.ZJY_Pic,
                                               ClothingFlag=query.ClothingFlag)
                    query.State = 'tjdck'
                    query.ZJY = user_cn
                    query.save()
                    self.set_step(u'仓库反馈', '', u'未处理', u'提交到仓库', user_cn, query.ZJY_Note,
                                  query.Reject_Reason, query.Source_Origin, query.Source_ID)
                else:
                    messages.error(request, '编号：%s  未填写质检员备注，请填写后再提交！！！' % query.id)
            else:
                messages.error(request, '编号：%s  已经处理，请勿重复提交！！！' % query.id)
    to_ck.short_description = u'提交到仓库'


    def to_review(self, request, queryset):
        user_cn = request.user.first_name
        for query in queryset:
            if query.State in ['wcl', 'bbh']:
                if query.ZJY_Note:
                    feedback_final_sh.objects.create(SubmitTime=query.SubmitTime, Submitter=query.Submitter,
                                                     SKU=query.SKU, Plateform=query.Plateform,
                                                     OrderID=query.OrderID, ProblemType=query.ProblemType,
                                                     Detail=query.Detail,
                                                     CPZY=query.CPZY, CPZY_Note='',
                                                     CGY=query.CGY, CGY_Note='',
                                                     ZJY=user_cn, ZJY_Note=query.ZJY_Note,
                                                     CKY='', CK_Note='',
                                                     ZJY_Final='', Final_Note='',
                                                     State='wcl', Reject_Reason='',
                                                     Source_Origin=query.Source_Origin, Source_ID=query.Source_ID,
                                                     Picture_1=query.Picture_1, Picture_2=query.Picture_2,
                                                     Picture_3=query.Picture_3, Picture_4=query.Picture_4,
                                                     Picture_5=query.Picture_5, Last_ID=query.id, ZJY_Pic=query.ZJY_Pic,
                                                     Last_Source='zjy', ClothingFlag=query.ClothingFlag)
                    query.State = 'tjdzzsh'
                    query.ZJY = user_cn
                    query.save()
                    self.set_step(u'质检员最终审核', '', u'未处理', u'提交到最终审核', user_cn, query.ZJY_Note,
                                  query.Reject_Reason, query.Source_Origin, query.Source_ID)
                else:
                    messages.error(request, '编号：%s  未填写质检员备注，请填写后再提交！！！' % query.id)
            else:
                messages.error(request, '编号：%s  已经处理，请勿重复提交！！！' % query.id)
    to_review.short_description = u'提交到最终审核'


    def to_reject(self, request, queryset):
        user_cn = request.user.first_name
        for query in queryset:
            if query.State in ['wcl', 'bbh']:
                if query.Reject_Reason:
                    feedback_submit.objects.filter(id=query.Last_ID).update(State='bbh', Reject_Reason=query.Reject_Reason)
                    query.State = 'bh'
                    query.ZJY = user_cn
                    query.save()
                    self.set_step(u'提交质量反馈', query.Submitter, u'被驳回', u'驳回到提交质量反馈', user_cn, query.ZJY_Note,
                                  query.Reject_Reason, query.Source_Origin, query.Source_ID)
                else:
                    messages.error(request, '编号：%s  未填写驳回备注，请填写后再提交！！！' % query.id)
            else:
                messages.error(request, '编号：%s  已经处理，请勿重复提交！！！' % query.id)
    to_reject.short_description = u'驳回到提交人'


    def get_list_queryset(self, ):
        request = self.request
        from skuapp.table.t_sys_staff_auth import t_sys_staff_auth
        qs = super(t_product_quality_feedback_zjy_Admin, self).get_list_queryset()
        cate = request.GET.get('cate', '')
        flag = 0
        try:
            flag = t_sys_staff_auth.objects.filter(StaffID=request.user.username,urltable="t_product_quality_feedback_zjy").count()
        except:
            pass
        if cate == '' or cate == 'wcl':
            qs = qs.filter(State='wcl')
        elif cate == 'all':
            if request.user.is_superuser or flag != 0:
                qs = qs
            else:
                qs = qs.filter(ZJY=request.user.first_name)
        else:
            if request.user.is_superuser or flag != 0:
                qs = qs.filter(State=cate)
            else:
                qs = qs.filter(State=cate, ZJY=request.user.first_name)

        plateform = request.GET.get('plateform', '')
        clothing = request.GET.get('clothing', '')
        searchList = {'Plateform__exact': plateform, 'ClothingFlag': clothing}
        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    if k == 'ShopName__exact':
                        if v.find('Wish-') == -1:
                            v = 'Wish-' + v.zfill(4)
                    sl[k] = v
        if sl:
            qs = qs.filter(**sl)
        return qs
