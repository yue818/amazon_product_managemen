#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: t_tort_info_result_Admin.py
 @time: 2018-05-07 14:03
"""

from datetime import datetime
from django.utils.safestring import mark_safe
from Project.settings import *
from django.contrib import messages
from skuapp.table.t_sys_department_staff import t_sys_department_staff
from skuapp.table.t_tort_info_result import t_tort_info_result
from skuapp.table.t_online_info_wish import t_online_info_wish
from skuapp.table.public import *
from skuapp.public.const import tort
from skuapp.public.MyException import MyException as myerr


class t_tort_info_result_Admin(object):
    search_box_flag = True
    t_tort_tree_menu_flag = True

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
    
    def show_IPForbiddenSite(self, obj):

        choices = getChoices(ChoiceForbiddenSite)
        ipfvalue = u'请点击选择' if obj.IPForbiddenSite is None else obj.IPForbiddenSite

        rt = '<input type="text" id="box_%s" value="%s" style="width:140px;" readonly="readonly">'%(obj.ID, ipfvalue,)
        rt = '%s<div id = "selectBox_%s" ><ul>'%(rt, obj.ID,)
        for k, v in choices:
            checked = 'checked="checked"' if k in ipfvalue else ''
            rt = '%s<li><input type="checkbox" name="ck_%s" value="%s" %s>%s</li>'%(rt, obj.ID, k, checked, v)

        rt = '%s</ul><input type="button" id="btn_%s" value="确定" style="width:50px;"> <p id="result_%s" style="color:green;"></p></div>'%(rt, obj.ID, obj.ID)

        tt = """%s<script>
            $(document).ready(function(){
            var arr=[];
            $(function(){
            $("#selectBox_%s").hide();$("input:checkbox[name='ck_%s']:checked").each(function(){arr.push($(this).val());});
            })
            $("#box_%s").click(function(){
            $("#selectBox_%s").toggle();document.getElementById("result_%s").innerHTML="";
            })
            $('input:checkbox[name="ck_%s"]').change(function(){
            if($(this).prop("checked")){
                if($(this).val()=="All"){
                    if(arr.length>=1){
                        $(this).attr("checked",false)
                        }
                    else{
                    arr.push($(this).val());
                    }}
                else{
                    var index=getIndex(arr,"All")
                    if(index>=0){
                        $(this).attr("checked",false)
                        }
                    else{
                        arr.push($(this).val());
                        }
                    }
                }
            else{
            var index=getIndex(arr,$(this).val())
            arr.splice(index,1);
            }
            if(arr.length<=0){
                $("#box_%s").val("请选择")
                }
            else{
                $("#box_%s").val(arr)
                }
                })
            
            function getIndex(arr,value){
            for(var i=0;i<arr.length;i++){
                if(arr[i]==value){
                return i}
                }
            return-1
            }
            $('#btn_%s').click(function(){
            $.ajax({url:"/t_tort_info_audit_ipfp/",type:"GET",contentType:"application/x-www-form-urlencoded:charset=UTF-8",dataType:"json",data:{"ipfvalue":arr.join(","),"ID":"%s"},
            success:function(data){if(data.result=="OK"){document.getElementById("result_%s").innerHTML="Success!";}},
            error:function(data){document.getElementById("result_%s").innerHTML="Fail!";}}
            );
            })})</script>"""
        rt = tt % (rt, obj.ID, obj.ID, obj.ID, obj.ID, obj.ID, obj.ID, obj.ID, obj.ID, obj.ID, obj.ID, obj.ID, obj.ID)

        return mark_safe(rt)

    show_IPForbiddenSite.short_description = mark_safe('<span style="width:150px;color:#428bca;">IP禁用平台</span>')
    
    def show_Site(self, obj):
        return mark_safe(obj.Site)

    show_Site.short_description = mark_safe('<p style="color:#428bca;">侵权站点</p>')
    
    def show_detail(self,obj):
        rt = "申请人:<br>%s<br>申请时间:<br>%s<br>采购员:%s<br>业绩归属人2:%s" % (obj.StaffID, obj.UpdateTime,obj.Purchaser, obj.SalerName2)
        
        return mark_safe(rt)
    show_detail.short_description = mark_safe('<span style="width:150px;color:#428bca;">详情</span>')
    
    list_display = ('ID', 'show_ProductPicUrl', 'show_detail', 'Site',
                    'MainSKU', 'ProductTitle', 'Trademark','Intellectual','SourceUrl','show_IPForbiddenSite','IPRange','KeyWord','WordCategory',
                    'ProductID','show_AttachmentUrls', 'Suggestion',
                    )

    readonly_fields = ('ID', 'to_reject_audit')
    list_display_links = ()
    list_editable = ('WordCategory', 'KeyWord',)
    
    actions = ['to_combine', 'to_reject_audit']
    def get_actions(self, request):
        Step = request.GET.get('Step', '')
        if '12,13,22' in Step:
            actions = []
        else:
            actions = ['to_combine', 'to_reject_audit']

        return actions
        
    def to_combine(self, request, objs):

        cnt = 0
        for obj in objs:
            try:
                '''if obj.IPForbiddenSite:
                    messages.error(request, "请取消选择IP禁用平台:%s,侵权流水号:%s,主SKU:%s"%(obj.IPForbiddenSite,obj.ID,obj.MainSKU))
                    continue'''
                #res = self.to_syn_tort_info(obj.Site, obj.MainSKU)
                #if res < 0:
                    #raise (myerr('10006', 'Site:%s,MainSKU:%s'%(obj.Site, obj.MainSKU)))  # 同步侵权信息有误

                t_tort_info_result_obj = t_tort_info_result()
                t_tort_info_result_obj.__dict__ = obj.__dict__
                t_tort_info_result_obj.AttacheID = request.user.first_name
                t_tort_info_result_obj.DealTime1 = datetime.now()
                
                if not t_tort_info_result_obj.IPForbiddenSite or len(t_tort_info_result_obj.IPForbiddenSite) == 0:
                    t_tort_info_result_obj.Step = tort.NO_TORT_LIST#不侵权
                else:
                    t_tort_info_result_obj.Step = tort.COM_TORT_LIST#一般侵权
                t_tort_info_result_obj.OperationState = 'N'
                t_tort_info_result_obj.save()
                cnt += 1
            except myerr, e:
                messages.error(request, e+e.todo)
                continue

        messages.info(request, u'审核%d条,成功完成%d条.' % (objs.count(), cnt))

    to_combine.short_description = u'转入一般侵权'
    
    def to_reject_audit(self, request, objs):

        cnt = 0
        for obj in objs:
            t_tort_info_audit_obj = t_tort_info_result()
            t_tort_info_audit_obj.__dict__ = obj.__dict__
            t_tort_info_audit_obj.AttacheID = request.user.first_name
            t_tort_info_audit_obj.DealTime1 = datetime.now()
            t_tort_info_audit_obj.Step = tort.WAIT_AUDIT
            t_tort_info_audit_obj.OperationState = 'N'
            t_tort_info_audit_obj.save()
            cnt += 1

        messages.info(request, u'驳回%d条,成功驳回%d条.' % (cnt, cnt))

    to_reject_audit.short_description = u'驳回侵权审核'
    
    def save_models(self):

        obj = self.new_obj
        request = self.request
        Step = obj.Step
        obj.save()
        if Step in (2, 11):
            Step = '2,11'
        else:
            Step = '3,11'

        post = request.POST
        post['_redirect'] = '/Project/admin/skuapp/t_tort_info_result/?Step=%s'%(Step,)

    def get_list_queryset(self):
        request = self.request
        qs = super(t_tort_info_result_Admin, self).get_list_queryset()

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
        KeyWord = request.GET.get('KeyWord', '')
        
        searchList = {'Step__in': Step,
                      'MainSKU__exact': MainSKU,
                      'Site__exact': Site,
                      'EnglishName__icontains': EnglishName,
                      'ProductTitle__icontains': ProductTitle,
                      'Intellectual__exact': Intellectual,
                      'StaffID__exact': StaffID,
                      'UpdateTime__gte': TimeStart,
                      'UpdateTime__lt': TimeEnd,
                      'KeyWord__icontains': KeyWord,
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




