# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from skuapp.table.t_sys_param import *
from skuapp.table.t_task_trunk import *
from skuapp.table.t_task_details import *
from skuapp.table.t_task_operation_log import *
from django.contrib import messages
from django.db.models import Q
import time,datetime
import oss2
from Project.settings import *
from skuapp.table.t_sys_param import *
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field, Div, FormActions, Submit, Button, ButtonHolder, InlineRadios, Reset, StrictButton, HTML, Hidden, Alert
import logging
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.db.models import F
from skuapp.table.t_task_trunk_case import t_task_trunk_case
#import re

class t_task_trunk_Admin(object):
    task_flag = True
    show_task_details = True
    search_box_flag = True

    class Media:
        js = {
            '/static/xadmin/js/kindeditor/lang/zh-CN.js',
            '/static/xadmin/js/kindeditor/kindeditor-all-min.js',
            '/static/xadmin/js/kindeditor/config.js',
        }
        
    def show_Demand_description(self,obj) :
        #rt = ''
        #aa = len(obj.Demand_description)
        #if aa <= 20:
            #rt = u'%s'%obj.Demand_description
        #else:
            #for i in range(0, aa, 40): 
        rt = u'%s'%(obj.Demand_description)
        #rt = re.Replace(rt, "<[^>]*>", "");
        return mark_safe(rt)   
    show_Demand_description.short_description = mark_safe(u'<center>问题备注<center>')
    
    def show_all_man(self,obj):
        try:
            all_man = t_task_trunk.objects.filter(Original_number=obj.Original_number).values_list('Pre_Identifier',flat=True)[0]
            all_m = User.objects.filter(username=all_man).values_list('first_name',flat=True)[0]
        except:
            all_man = t_task_trunk.objects.filter(Original_number=obj.Original_number).values_list('Create_man',flat=True)[0]
            all_m = User.objects.filter(username=all_man).values_list('first_name',flat=True)[0]
        rt = u'<b>总负责人：</b><font color="red">%s</font><br><b>当前责任人：</b>%s'%(all_m,self.show_chargeman(obj))
        return mark_safe(rt)
    show_all_man.short_description = u'总负责人/当前责任人'
    
    
    def show_Check_man(self,obj) :
        try:
            user_obj = User.objects.filter(username=obj.Check_man).values_list('first_name',flat=True)[0]
        except:
            user_obj = ''
        if obj.Flow_Status == 'SH':
            rt = u'<div style="background-color:#FFD700">审核人：%s<br>审核通过时间：%s<br>要求完成时间：%s</div>'%(user_obj,obj.Check_time,self.show_Ask_time(obj))
        else:
            rt = u'审核人：%s<br>审核通过时间：%s<br>要求完成时间：%s'%(user_obj,obj.Check_time,self.show_Ask_time(obj))
        return mark_safe(rt)
    show_Check_man.short_description = u'---------------审核阶段---------------' 
    
    
    def show_Task_handler(self,obj) :
        try:
            user_obj = User.objects.filter(username=obj.Task_handler).values_list('first_name',flat=True)[0]
        except:
            user_obj = ''
        try:
            user_obj2 = User.objects.filter(username=obj.Task_handler_review).values_list('first_name',flat=True)[0]
        except:
            user_obj2 = ''
        if obj.Flow_Status == 'CL':
            rt = u'<div style="background-color:#FFD700">处理人：%s<br>处理复核人:%s<br>处理结束时间：%s</div>'%(user_obj,user_obj2,self.show_handler_time(obj))
        else:
            rt = u'处理人：%s<br>处理复核人:%s<br>处理结束时间：%s'%(user_obj,user_obj2,self.show_handler_time(obj))
        return mark_safe(rt)
    show_Task_handler.short_description = u'---------------处理阶段---------------'  

    def show_In_Identifier(self,obj) :
        try:
            user_obj = User.objects.filter(username=obj.In_Identifier).values_list('first_name',flat=True)[0]
        except:
            user_obj = ''
        if obj.Identifier_In_result is None:
            re = ''
        elif obj.Identifier_In_result == 'success':
            re = '<font color="green">验证全部通过</font>'
        elif obj.Identifier_In_result == 'fail':
            re = '<font color="red">验证不通过</font>'
        if obj.Flow_Status == 'NYZ':
            rt = u'<div style="background-color:#FFD700">IT自验证人：%s<br>IT自验证结果：%s</div>'%(user_obj,re)
        else:
            rt = u'IT自验证人：%s<br>IT自验证结果：%s'%(user_obj,re)
        return mark_safe(rt)
    show_In_Identifier.short_description = u'---------------IT自验证阶段---------------'  
    
    def show_Identifier(self,obj) :
        try:
            user_obj = User.objects.filter(username=obj.Identifier).values_list('first_name',flat=True)[0]
        except:
            user_obj = ''
        if obj.Flow_Status == 'YZ':
            rt = u'<div style="background-color:#FFD700">验证人：%s<br>验证通过时间：%s<br>最后更新时间：%s</div>'%(user_obj,obj.Identifier_result,obj.Update_time)
        else:
            rt = u'验证人：%s<br>验证通过时间：%s<br>最后更新时间：%s'%(user_obj,obj.Identifier_time,obj.Update_time)
        return mark_safe(rt)
    show_Identifier.short_description = u'---------------业务对接验证阶段---------------'    
    
        
    def show_AttachmentUrls(self,obj) :
        from datetime import *  
        import time
        nows = date.today() 
        attachmentUrl1="";
        attachmentUrl2="";
        attachmentUrl3="";
        if obj.Ask_time is not None and obj.Task_handler_time is not None and obj.Ask_time < obj.Task_handler_time:
            rt='<b><font color="red">%s</font></b><br><br>'%obj.Demand_name
        elif obj.Ask_time is not None and obj.Task_handler_time is None and obj.Ask_time < nows:
            rt='<b><font color="red">%s</font></b><br><br>'%obj.Demand_name
        else:
            rt='<b><font color="green">%s</font></b><br><br>'%obj.Demand_name
        if obj.AttachmentUrl1 is not None and str(obj.AttachmentUrl1).strip() !='' :
            attachmentUrl1 =  u'%s%s.%s/%s/%s/%s'%(PREFIX,BUCKETNAME_TORT,ENDPOINT_OUT,'questions',obj.Original_number,str(obj.AttachmentUrl1))
            rt="%s附件一:<a href=%s>%s</a>;<br>"%(rt,attachmentUrl1,attachmentUrl1)
        if obj.AttachmentUrl2 is not None and str(obj.AttachmentUrl2).strip() !='' :
            attachmentUrl2 =  u'%s%s.%s/%s/%s/%s'%(PREFIX,BUCKETNAME_TORT,ENDPOINT_OUT,'questions',obj.Original_number,str(obj.AttachmentUrl2))
            rt="%s附件二:<a href=%s>%s</a>;<br>"%(rt,attachmentUrl2,attachmentUrl2)
        if obj.AttachmentUrl3 is not None and str(obj.AttachmentUrl3).strip() !='' :
            attachmentUrl3 =  u'%s%s.%s/%s/%s/%s'%(PREFIX,BUCKETNAME_TORT,ENDPOINT_OUT,'questions',obj.Original_number,str(obj.AttachmentUrl3))
            rt="%s附件三:<a href=%s>%s</a>;<br>"%(rt,attachmentUrl3,attachmentUrl3)

        #rt =  "附件一:<a href=%s>%s</a>;<br>附件二:<a href=%s>%s</a><br>附件三:<a href=%s>%s</a><br>附件四:<a href=%s>%s</a><br>附件五:<a href=%s>%s</a><br>附件六:<a href=%s>%s</a>;"%(attachmentUrl1,attachmentUrl1,attachmentUrl2,attachmentUrl2,attachmentUrl3,attachmentUrl3,attachmentUrl4,attachmentUrl4,attachmentUrl5,attachmentUrl5,attachmentUrl6,attachmentUrl6)
        return mark_safe(rt)
    show_AttachmentUrls.short_description = mark_safe(u'<center>问题名称<br>(<font color="green">绿色：</font>按计划进行|<font color="red">红色：</font>已经逾期)<center>')
    
             
    list_display= ('Original_number','Flow_Status','show_AttachmentUrls','show_Demand_description','show_all_man','show_create_man','show_Check_man','show_Task_handler','show_In_Identifier','show_Identifier')
    #list_editable = ()

    fields = ('Flow_type','Demand_name','AttachmentUrl1','AttachmentUrl2','AttachmentUrl3','Demand_description','Create_man','Create_time','Pre_Identifier','Hope_time',  #提出
              'Check_man','Check_time','Check_info','Check_result','Ask_time',#审核
              'Task_handler','Task_status','Task_info','Task_handler_time','Task_handler_review','Identifier_In_result','In_Identifier',#处理
              'Identifier','Identifier_info','Identifier_result','Identifier_time', #验证
              
              )

    #list_filter = ('Demand_name','Flow_type','Flow_Status','Current_chargeman','Create_man','Create_time','Check_man','Check_time','Task_handler','Task_handler_time','Identifier','Identifier_time','Update_time',)

    #search_fields = ('Original_number','Create_man','Current_chargeman','Task_name_original','Task_status',)

    readonly_fields = ('Flow_type','Demand_name','Create_man','Create_time','Check_man',   'Check_result','Check_time','Task_handler',  'Task_status','Task_handler_time','Identifier',  'Identifier_result','Identifier_time')

    #show_detail_fields = ['Original_number']
    list_display_links = ['Original_number','Demand_name','Flow_Status']
    
    form_layout = (
        Div(''),
        TabHolder(
            Tab(u'a.提出',
                Row('Flow_type'),
                Row('Demand_name'),             
                Row('Demand_description'),
                Row( 'AttachmentUrl1','AttachmentUrl2','AttachmentUrl3'),
                Row('Check_man','Pre_Identifier'),
                Row('Hope_time'),
                Row('Create_man','Create_time'),
                #Hidden('Current_chargeman','{{ Check_man.value  }}'),
                #Hidden('Flow_Status', 'TC'),
                FormActions(                        
                    #Reset('reset', u'重置'),                                    
                    Button('wtqx', '问题取消',css_class="btn-danger",css_id='wtqx'),                  
                    Button('tc_bccg', '保存草稿',css_class="btn-warning",css_id="tc_bccg"),                   
                    Submit('save', u'✓提交',css_id='tc'),
                )
            ),
            Tab(u'b.审核',            
                Row('Check_result',),
                Row('Check_info'),
                Row('Ask_time'),              
                Row('Check_time'),
                Row('Task_handler'),
                FormActions(
                    #Hidden('Current_chargeman', 'TC'),
                    #Submit('save', u'上一步:提出'),
                    #Hidden('Current_chargeman', 'SH'),
                    Button('sh_bccg', '保存草稿',css_class="btn-warning",css_id="sh_bccg"),
                    Submit('save', u'✓提交',css_id='sh'),               
                )
            ),
            Tab(u'c.处理',
                Row('Task_status'),
                Row('Task_info'),
                Row('Task_handler_review'),            
                Row('Task_handler_time'),
                Row('In_Identifier'),
                #Row('show_operation'),
                #Div('show_operation'),
                FormActions(
                    #Hidden('Current_chargeman', 'SH'),
                    #Submit('save', u'上一步:审核'),
                    #Reset('reset', u'重置'),
                    #Hidden('Current_chargeman', 'CL'),
                    Button('bhtc', '驳回任务提出处',css_class="btn-danger",css_id='bhtc'),
                    Button('zf', '转发',css_class="btn-success",css_id='zf'),
                    Button('cl_bccg', '保存草稿',css_class="btn-warning",css_id='cl_bccg'),
                    Submit('save', '✓提交',css_id='cl'),
                ),
            ),
            Tab(u'd.IT自验证',
                Row('Identifier_In_result'),
                Row('Identifier'),
                FormActions(
                    Submit('save', u'✓提交',css_id='nyz'),
                )
            ),
            Tab(u'e.业务对接验证',
                Row('Identifier_result'),
                Row('Identifier_info'),
                Row('Identifier_time'),
                FormActions(
                    #Hidden('Current_chargeman', 'YZ'),
                    #Submit('save', u'上一步:处理'),
                    #Reset('reset', u'重置'),
                    #Hidden('Current_chargeman', 'GB'),
                    Button('yz_bccg', '保存草稿',css_class="btn-warning",css_id="yz_bccg"),
                    Submit('save', u'✓提交',css_id='yz'),
                )
            ),
            Tab(u'f.关闭/日志',             
                #StrictButton(u"失败", name="go", value="go", css_class="extra"),
                StrictButton(u'日志记录：', css_id="log"),
                #HTML("<div id=log>日志记录</div>")
            ),
        )
    )    
    
    def show_Ask_time(self,obj):
        if obj.Ask_time is not None:
            rt = u'<font color="red">%s</font>'%(obj.Ask_time)
        else:
            rt = ''
        return mark_safe(rt)
    show_Ask_time.short_description = u'要求完成时间'

    def show_handler_time(self,obj):
        if obj.Task_handler_time is not None:
            rt = u'<font color="red">%s</font>'%(obj.Task_handler_time)
        else:
            rt = ''
        return mark_safe(rt)
    show_handler_time.short_description = u'处理结束时间'

    
    def show_chargeman(self,obj):
        rt = ''
        try:
            s_obj = User.objects.filter(username=obj.Current_chargeman).values_list('first_name',flat=True)[0]
        except:
            s_obj = ''
        rt = '<font color="red">%s</font>'%s_obj
        return mark_safe(rt)
    show_chargeman.short_description = u'当前责任人'
    
    def show_create_man(self,obj):
        try:
            user_obj = User.objects.filter(username=obj.Create_man).values_list('first_name',flat=True)[0]
        except:
            user_obj = ''
        if obj.Flow_Status == 'TC':
            rt = u'<div style="background-color:#FFD700">创建人：%s<br>创建时间：%s<br>期望解决时间：%s</div>'%(user_obj,obj.Create_time,obj.Hope_time)
        else:
            rt = u'创建人：%s<br>创建时间：%s<br>期望解决时间：%s'%(user_obj,obj.Create_time,obj.Hope_time)
        return mark_safe(rt)
    show_create_man.short_description = u'---------------提出阶段---------------'
    
    def show_pic(self,obj):
        rt = u'<style>th,td{text-align:center;}</style><table cellspacing=0 width=300px height=150 align=center border=1>'
        t_task_details_objs = t_task_details.objects.filter(Original_number=obj.Original_number)
        task_obj_p = t_task_details_objs.filter(Task_name_parent='顶级任务')
        try:
            task_obj = task_obj_p.values_list('Task_name_current')[0][0]
        except:
            task_obj = ''
        #messages.error(self.request,task_obj)
        task_count_s = task_obj_p.count()
        if task_count_s == 1 and task_obj is None or task_obj == '':
            rt = '%s<tr><th scope="col">顶级任务</th><th colspan="2" scope="col">子任务</th></tr><tr><th scope="row">%s</th><td colspan="2"></td></tr>'%(rt,obj.Task_name_original)
        else:
            task_objs = task_obj_p.values_list('Task_name_current')
            count_a = 0
            for task_obj in task_objs:
                count_a += t_task_details_objs.filter(Task_name_parent=task_obj[0]).count()
            #messages.error(self.request,count_a)   
            if count_a == 0:
                rt = u'%s<tr><th scope="col">顶级任务</th><th>子任务</th></tr><tr><th rowspan="%s" scope="row">%s'%(rt,task_count_s,obj.Task_name_original)
                Task_name_current_objs = task_obj_p.values_list('Task_name_current','Task_handler','Task_status')
                for Task_name_current_obj in Task_name_current_objs:
                    curr_name = Task_name_current_obj[0]
                    curr_chargeman = Task_name_current_obj[1]
                    curr_status = Task_name_current_obj[2]
                    curr_status_name = t_sys_param.objects.values_list('VDesc').filter(Type=42,V=curr_status)[0][0]
                    rt = '%s<td>%s(%s/%s)</td></tr>'%(rt,curr_name,curr_status_name,curr_chargeman)
                rt = '%s</th>'%rt
            else:
                rt = u'%s<tr><th scope="col">顶级任务</th><th colspan="2">子任务</th></tr><tr><th rowspan="%s" scope="row">%s</th>'%(rt,count_a,obj.Task_name_original)
                Task_name_current_objs = t_task_details_objs.filter(Task_name_parent='顶级任务')
                for Task_name_current_obj in Task_name_current_objs:
                    Task_name_current_child_objs = t_task_details_objs.filter(Task_name_parent=Task_name_current_obj.Task_name_current)
                    sta = t_sys_param.objects.values_list('VDesc').filter(Type=42,V=Task_name_current_obj.Task_status)[0][0]
                    rt = '%s<td rowspan="%s" >%s<br>(%s/%s)</td>'%(rt,len(Task_name_current_child_objs),Task_name_current_obj.Task_name_current,sta,Task_name_current_obj.Task_handler)
                    if len(Task_name_current_child_objs) > 1:
                        for i in range(0,len(Task_name_current_child_objs)):
                            sta = t_sys_param.objects.values_list('VDesc').filter(Type=42,V=Task_name_current_child_objs[i].Task_status)[0][0]
                            if i == 0:
                                rt += '<td>%s(%s/%s)</td></tr>'%(Task_name_current_child_objs[i].Task_name_current,sta,Task_name_current_child_objs[i].Task_handler)
                            else:
                                rt += '<tr><td >%s(%s/%s)</td></tr>'%(Task_name_current_child_objs[i].Task_name_current,sta,Task_name_current_child_objs[i].Task_handler)
                    else:
                        if len(Task_name_current_child_objs) == 1:
                            sta = t_sys_param.objects.values_list('VDesc').filter(Type=42,V=Task_name_current_child_objs[0].Task_status)[0][0]
                            rt += '<td>%s(%s/%s)</td></tr>'%(Task_name_current_child_objs[0].Task_name_current,sta,Task_name_current_child_objs[0].Task_handler)
                        else:
                            rt += '<td> </td></tr>'
                
                #messages.error(self.request,'%s----a--'%count_a)
                #messages.error(self.request,'%s----b--'%count_b)

                rt = '%s</th>'%rt
        
        rt = '%s</table>'%rt
        return mark_safe(rt)
    show_pic.short_description = u'任务分发流程图表'
    
    def show_operation(self,obj):
        try:
            Original_number_obj = t_task_details.objects.filter(Original_number=obj.Original_number).values_list('Task_name_current')[0][0]
        except:
            Original_number_obj = ''
        if Original_number_obj is None or Original_number_obj == '':
            rt = '<input type="button" value="创建首个子任务" onclick="if(confirm(\'是否创建子任务？\')) {window.open(\'/Project/admin/skuapp/t_task_details/%s/update \')}" target="_blank" />'%(obj.Son_number)
        else:
            rt = '<input type="button" value="创建子任务" onclick="if(confirm(\'是否创建子任务？\')) {window.open(\'t_task_son/?original_num=%s&original_name=%s \')}" target="_blank" />'%(obj.Original_number,obj.Task_name_original)
            rt = '%s&nbsp;&nbsp;&nbsp;&nbsp;<input type="button" value="查看子任务" onclick="window.open(\'/Project/admin/skuapp/t_task_details/?_p_Original_number__exact=%s \')" target="_blank" />'%(rt,obj.Original_number)
        rt = '%s&nbsp;&nbsp;&nbsp;&nbsp;<input type="button" value="操作历史" onclick="window.location.href=\'www.baidu.com\'" />'%(rt)
        return mark_safe(rt)
    show_operation.short_description = u'操作'

    def get_readonly_fields(self):
        logger = logging.getLogger('sourceDns.webdns.views')
        readonly_fields = super(t_task_trunk_Admin, self).get_readonly_fields()
        
        request = self.request
        models_objs = (u'%s'%request).split('/')
        if models_objs[1] == 'Project' and models_objs[2] == 'admin':
            task_id = models_objs[5]
        elif models_objs[1] == 'xadmin':
            task_id = models_objs[4]
        
        # messages.error(request,'xxx---%s'%Flow_objs)
        #logger.info('*******====%s'%(request,))
        #logger.info('ccccccccc====%s'%(task_id,))
        try:
            Original_number = int(task_id)
            Flow_obj = t_task_trunk.objects.filter(Original_number=Original_number).values_list('Flow_Status',flat=True)[0]
            if Flow_obj == '' or Flow_obj == 'TC':
                Create_man_obj = t_task_trunk.objects.filter(Original_number=Original_number).values_list('Create_man',flat=True)[0]
                if request.user.username == Create_man_obj:
                    readonly_fields = ['In_Identifier','Task_handler_review','Identifier_In_result','Ask_time','Create_man','Create_time','Check_result','Check_time','Task_handler',  'Task_status','Task_handler_time','Identifier',  'Identifier_result','Identifier_time']
                else:
                    readonly_fields = ['In_Identifier','Task_handler_review','Identifier_In_result','Ask_time','Hope_time','AttachmentUrl1','AttachmentUrl2','AttachmentUrl3','Flow_type','Demand_name','Create_man','Create_time','Check_man',   'Check_result','Check_time','Task_handler',  'Task_status','Task_handler_time','Identifier',  'Identifier_result','Identifier_time']
            elif Flow_obj == 'SH':
                Check_man_obj = t_task_trunk.objects.filter(Original_number=Original_number).values_list('Check_man',flat=True)[0]
                if request.user.username == Check_man_obj:
                    readonly_fields = ('In_Identifier','Task_handler_review','Identifier_In_result','Hope_time','Pre_Identifier','AttachmentUrl1','AttachmentUrl2','AttachmentUrl3','Flow_type','Demand_name','Create_man','Create_time','Check_man',   'Check_time',  'Task_status','Task_handler_time','Identifier',  'Identifier_result','Identifier_time')
                else:
                    readonly_fields = ('In_Identifier','Task_handler_review','Identifier_In_result','Ask_time','Hope_time','Pre_Identifier','Flow_type','Demand_name','Create_man','Create_time','Check_man',   'Check_result','Check_time','Task_handler',  'Task_status','Task_handler_time','Identifier',  'Identifier_result','Identifier_time')
            elif Flow_obj == 'CL':
                Task_handler_obj = t_task_trunk.objects.filter(Original_number=Original_number).values_list('Task_handler',flat=True)[0]
                if request.user.username == Task_handler_obj:
                    readonly_fields = ('Identifier','Identifier_In_result','Ask_time','Hope_time','Pre_Identifier','AttachmentUrl1','AttachmentUrl2','AttachmentUrl3','Flow_type','Demand_name','Create_man','Create_time','Check_man',   'Check_result','Check_time','Task_handler',  'Task_handler_time',  'Identifier_result','Identifier_time')
                else:
                    readonly_fields = ('In_Identifier','Identifier_In_result','Task_handler_review','Ask_time','Hope_time','Pre_Identifier','Flow_type','Demand_name','Create_man','Create_time','Check_man',   'Check_result','Check_time','Task_handler',  'Task_status','Task_handler_time','Identifier',  'Identifier_result','Identifier_time')          
            elif Flow_obj == 'NYZ':
                In_Identifier_obj = t_task_trunk.objects.filter(Original_number=Original_number).values_list('In_Identifier',flat=True)[0]
                if request.user.username == In_Identifier_obj:
                    readonly_fields = ['In_Identifier','Task_handler_review','Ask_time','Hope_time','Pre_Identifier','AttachmentUrl1','AttachmentUrl2','AttachmentUrl3','Flow_type','Demand_name','Create_man','Create_time','Check_man',   'Check_result','Check_time','Task_handler',  'Task_status','Task_handler_time','Identifier_time']
                else:
                    readonly_fields = ('In_Identifier','Task_handler_review','Identifier_In_result','Pre_Identifier','Ask_time','Hope_time','Flow_type','Demand_name','Create_man','Create_time','Check_man',   'Check_result','Check_time','Task_handler',  'Task_status','Task_handler_time','Identifier',  'Identifier_result','Identifier_time')
            
            elif Flow_obj == 'YZ':
                Identifier_obj = t_task_trunk.objects.filter(Original_number=Original_number).values_list('Identifier',flat=True)[0]
                if request.user.username == Identifier_obj:
                    readonly_fields = ['In_Identifier','Task_handler_review','Identifier_In_result','Ask_time','Hope_time','Pre_Identifier','AttachmentUrl1','AttachmentUrl2','AttachmentUrl3','Flow_type','Demand_name','Create_man','Create_time','Check_man',   'Check_result','Check_time','Task_handler',  'Task_status','Task_handler_time','Identifier', 'Identifier_time']
                else:
                    readonly_fields = ('In_Identifier','Task_handler_review','Identifier_In_result','Pre_Identifier','Ask_time','Hope_time','Flow_type','Demand_name','Create_man','Create_time','Check_man',   'Check_result','Check_time','Task_handler',  'Task_status','Task_handler_time','Identifier',  'Identifier_result','Identifier_time')
            else:
                readonly_fields = ['In_Identifier','Task_handler_review','Identifier_In_result','Ask_time','Hope_time','Pre_Identifier','AttachmentUrl1','AttachmentUrl2','AttachmentUrl3','Flow_type','Demand_name','Create_man','Create_time','Check_man',   'Check_result','Check_time','Task_handler',  'Task_status','Task_handler_time','Identifier',  'Identifier_result','Identifier_time']
        except:
            readonly_fields = ['In_Identifier','Task_handler_review','Identifier_In_result','Ask_time','Create_man','Create_time','Check_result','Check_time','Task_handler',  'Task_status','Task_handler_time','Identifier',  'Identifier_result','Identifier_time']  
        
        return readonly_fields
    
    def save_models(self):
        obj = self.new_obj
        request = self.request
        # obj.Task_status='create'
        obj.save()
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_TORT)
        try:

            if obj.AttachmentUrl1 is not None and str(obj.AttachmentUrl1).strip() !='' :
                bucket.put_object(u'%s/%s/%s'%('questions',obj.Original_number,str(obj.AttachmentUrl1)[2:]),obj.AttachmentUrl1)
                #messages.error(request,u'%s/%s/%s'%('questions',obj.Original_number,str(obj.AttachmentUrl1)[2:]))

            if obj.AttachmentUrl2 is not None and str(obj.AttachmentUrl2).strip() !='' :
                bucket.put_object(u'%s/%s/%s'%('questions',obj.Original_number,str(obj.AttachmentUrl2)[2:]),obj.AttachmentUrl2)

            if obj.AttachmentUrl3 is not None and str(obj.AttachmentUrl3).strip() !='' :
                bucket.put_object(u'%s/%s/%s'%('questions',obj.Original_number,str(obj.AttachmentUrl3)[2:]),obj.AttachmentUrl3)

        except:
            pass
        
        if obj.Original_number is None:
            try:
                max_id = int(t_task_trunk.objects.latest('Original_number').Original_number) + 1
            except:
                max_id = 1 
        else:
            max_id = obj.Original_number
        #if obj.Create_man is None:
            #obj.Current_chargeman = ''
            #obj.Create_man = request.user.username
            #obj.Create_time = datetime.datetime.now()      
        if obj.Check_man and obj.Task_handler is None:
            if obj.Check_result is None:
                obj.Create_man = request.user.username
                obj.Create_time = datetime.datetime.now()  
                obj.Current_chargeman = obj.Check_man
                Create_man = User.objects.filter(username=obj.Create_man).values_list('first_name',flat=True)[0]  
                obj.Flow_Status = 'SH'
                if obj.Pre_Identifier is None:
                    obj.Identifier = obj.Create_man
                else:
                    obj.Identifier = obj.Pre_Identifier   
                t_task_operation_log.objects.create(Original_number=max_id,Flow_way_status='提出==>审核',Flow_handle_result='/',Flow_handle_remark='/',Flow_handle_man=Create_man,Flow_handle_time=datetime.datetime.now())  
            elif obj.Check_result == 'fail':
                Check_man = User.objects.filter(username=obj.Check_man).values_list('first_name',flat=True)[0]
                obj.Flow_Status = 'TC'
                obj.Current_chargeman = obj.Create_man                  
                t_task_operation_log.objects.create(Original_number=max_id,Flow_way_status='审核==>提出',Flow_handle_result='不通过',Flow_handle_remark=obj.Check_info,Flow_handle_man=Check_man,Flow_handle_time=datetime.datetime.now())
                obj.Check_result = None               
                obj.Check_info = None
        
        elif obj.Create_man and obj.Check_man and obj.Task_handler:
            obj.Current_chargeman = obj.Task_handler         
            if obj.Task_status == 'finished':
                obj.Task_handler_time = datetime.datetime.now()
                Identifier = User.objects.filter(username=obj.In_Identifier).values_list('first_name',flat=True)[0]             
                if obj.In_Identifier:
                    if obj.Identifier_In_result is None:
                        obj.Flow_Status = 'NYZ'     
                        Task_handler = User.objects.filter(username=obj.Task_handler).values_list('first_name',flat=True)[0]                                
                        obj.Current_chargeman = obj.In_Identifier
                        t_task_operation_log.objects.create(Original_number=max_id,Flow_way_status='处理==>IT自验证',Flow_handle_result='通过',Flow_handle_remark=obj.Task_info,Flow_handle_man=Task_handler,Flow_handle_time=datetime.datetime.now())
                    elif obj.Identifier_In_result == 'success' and obj.Identifier_result is None:
                        obj.Flow_Status = 'YZ'
                        obj.Current_chargeman = obj.Identifier
                        In_Identifier = User.objects.filter(username=obj.In_Identifier).values_list('first_name',flat=True)[0]
                        t_task_operation_log.objects.create(Original_number=max_id,Flow_way_status='IT自验证==>业务对接验证',Flow_handle_result='通过',Flow_handle_remark='pass',Flow_handle_man=In_Identifier,Flow_handle_time=datetime.datetime.now())
                    elif obj.Identifier_In_result == 'fail' and obj.Identifier_result is None:
                        obj.Flow_Status = 'CL'
                        obj.Current_chargeman = obj.Task_handler
                        In_Identifier = User.objects.filter(username=obj.In_Identifier).values_list('first_name',flat=True)[0]
                        t_task_operation_log.objects.create(Original_number=max_id,Flow_way_status='IT自验证==>处理',Flow_handle_result='不通过',Flow_handle_remark='reject',Flow_handle_man=In_Identifier,Flow_handle_time=datetime.datetime.now())
                        obj.Identifier_In_result = None
                    elif obj.Identifier_result == 'success':
                        obj.Flow_Status = 'GB'
                        obj.Current_chargeman = obj.Identifier
                        obj.Identifier_time = datetime.datetime.now()
                        t_task_operation_log.objects.create(Original_number=max_id,Flow_way_status='业务对接验证==>关闭',Flow_handle_result='通过',Flow_handle_remark=obj.Identifier_info,Flow_handle_man=Identifier,Flow_handle_time=datetime.datetime.now())
                    elif obj.Identifier_result == 'fail':
                        obj.Flow_Status = 'CL'
                        obj.Current_chargeman = obj.Task_handler
                        ouser = User.objects.filter(username=obj.Identifier).values_list('first_name',flat=True)[0]        
                        t_task_operation_log.objects.create(Original_number=max_id,Flow_way_status='业务对接验证==>IT自验证',Flow_handle_result='不通过',Flow_handle_remark='reject',Flow_handle_man=ouser,Flow_handle_time=datetime.datetime.now())
                        obj.Identifier_result = None            
                        obj.Identifier_info = None
                        obj.In_Identifier = None
                        obj.Identifier_In_result = None
                else:
                    Check_man = User.objects.filter(username=obj.Check_man).values_list('first_name',flat=True)[0]
                    obj.Flow_Status = 'CL'
                    obj.Current_chargeman = obj.Identifier
                    t_task_operation_log.objects.create(Original_number=max_id,Flow_way_status='审核==>处理',Flow_handle_result='通过',Flow_handle_remark=obj.Check_info,Flow_handle_man=Check_man,Flow_handle_time=datetime.datetime.now())
            elif obj.Task_status == 'refused':
                obj.Flow_Status = 'SH'
                obj.Current_chargeman = obj.Check_man
                Task_handler = User.objects.filter(username=obj.Task_handler).values_list('first_name',flat=True)[0]
                t_task_operation_log.objects.create(Original_number=max_id,Flow_way_status='处理==>审核',Flow_handle_result='不通过',Flow_handle_remark=obj.Task_info,Flow_handle_man=Task_handler,Flow_handle_time=datetime.datetime.now())
                obj.Task_status = None           
                obj.Task_info = None
            else:
                Check_man = User.objects.filter(username=obj.Check_man).values_list('first_name',flat=True)[0]
                if obj.Check_result == 'success':
                    t_task_operation_log.objects.create(Original_number=max_id,Flow_way_status='审核==>处理',Flow_handle_result='通过',Flow_handle_remark=obj.Check_info,Flow_handle_man=Check_man,Flow_handle_time=datetime.datetime.now())
                    obj.Check_time = datetime.datetime.now()
                    obj.Current_chargeman = obj.Task_handler
                    #messages.error(request,'%s---'%max_id)
                    obj.Flow_Status = 'CL'
                elif obj.Check_result == 'fail':
                    obj.Flow_Status = 'TC'
                    obj.Current_chargeman = obj.Create_man                  
                    t_task_operation_log.objects.create(Original_number=max_id,Flow_way_status='审核==>提出',Flow_handle_result='不通过',Flow_handle_remark=obj.Check_info,Flow_handle_man=Check_man,Flow_handle_time=datetime.datetime.now())
                    obj.Check_result = None               
                    obj.Check_info = None
               
        else:
            obj.Flow_Status = 'GB'
        fs                                =    request.POST.get('fs')
        ts_id                             =    request.POST.get('ts_id')
        Test_sight_list                   =    request.POST.getlist('Test_sight')
        Test_case_list                    =    request.POST.getlist('Test_case')
        Test_hope_result_list             =    request.POST.getlist('Test_hope_result')
        Test_result_list                  =    request.POST.getlist('Test_result')
        Test_developer_list               =    request.POST.getlist('Test_developer')
        Test_verifier_list                =    request.POST.getlist('Test_verifier')
        Test_verifier_time                =    request.POST.getlist('Test_verifier_time')
        #messages.error(request,'fs-------%s'%fs)
        if fs == '' or fs == 'TC' or fs == 'SH' or fs == 'CL':
            #messages.error(request,'1111111111------')
            for i in range(len(Test_sight_list)):
                t_task_trunk_case.objects.update_or_create(Original_number=ts_id,Test_sight=Test_sight_list[i],Test_case=Test_case_list[i],Test_hope_result=Test_hope_result_list[i])
        if fs == 'NYZ':
            #messages.error(request,'22222222222------')
            date_list = []
            if len(Test_result_list) > 0:
                for i in range(len(Test_result_list)):
                    if len(Test_verifier_time) == 0:
                        dt = datetime.datetime.now()
                    elif Test_verifier_time[i] == '' or Test_verifier_time[i] is None:
                        dt = datetime.datetime.now()
                    else:
                        dt = datetime.datetime.strptime(Test_verifier_time[i], "%Y-%m-%d")
                    date_list.append(dt)
                    messages.error(request,'xxxxxxxxxx-----%s'%dt)
                    case_objs = t_task_trunk_case.objects.filter(Original_number=int(ts_id)).values('Test_sight','Test_case','Test_hope_result')
                    for case_obj in case_objs:
                        t_task_trunk_case.objects.filter(Original_number=ts_id,Test_sight=case_obj['Test_sight'],Test_case=case_obj['Test_case'],Test_hope_result=case_obj['Test_hope_result']).update(Test_result=Test_result_list[i],Test_developer=Test_developer_list[i],Test_verifier=Test_verifier_list[i],Test_verifier_time=date_list[i])
                
        obj.save()
        post = request.POST
        post['_redirect'] = '/Project/admin/skuapp/t_task_trunk?status=mytask&Flow_Status=TC,SH,CL,NYZ,YZ'
        
        # return HttpResponseRedirect("/Project/admin/skuapp/t_task_trunk?status=mytask")
        # t_task_details.objects.create(Original_number=obj.Original_number,Parent_number=obj.Original_number,Task_name_original=obj.Task_name_original,
        #                                 Task_name_parent='顶级任务',Create_man=obj.Create_man,Current_chargeman=obj.Current_chargeman,
        #                                 Task_status=obj.Task_status,Create_time=obj.Create_time,Update_time=obj.Update_time)
        # try:
        #     Current_number = t_task_details.objects.filter(Original_number=obj.Original_number).values_list('Current_number')[0][0]
        #     obj.Son_number = int(Current_number)
        #     obj.save()
        # except:
        #     pass

    def get_list_queryset(self, ):
        from datetime import *  
        import time
        nows = date.today() 
        request = self.request
        qs = super(t_task_trunk_Admin, self).get_list_queryset()
        
        status = request.GET.get('status', '')
        
        Demand_name             =    request.GET.get('Demand_name','')     # 问题名称
        Flow_type               =    request.GET.get('Flow_type','')              # 类型
        Flow_Status             =    request.GET.get('Flow_Status','')          # 流程进度
        Flow_Status = Flow_Status.split(',')
        if '' in Flow_Status:
            Flow_Status = ''
        Current_chargeman       =    request.GET.get('Current_chargeman','') # 当前责任人
        import re
        zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
        #一个小应用，判断一段文本中是否包含简体中：
        contents=u'一个小应用，判断一段文本中是否包含简体中：'
        match = zhPattern.search(Current_chargeman)
        if match:
            Current_chargemanCn     =    Current_chargeman
            objs      =    User.objects.filter(first_name__icontains=Current_chargemanCn).values('username','first_name') 
            Current_chargemanA = None           
            if not objs.exists():
                messages.error(self.request,u'没有该用户')
            else:
                if objs[0]['first_name'] == Current_chargemanCn :
                    Current_chargemanA = objs[0]['username']
            Current_chargeman = Current_chargemanA
        
        Create_man              =    request.GET.get('Create_man','')          # 创建人
        match = zhPattern.search(Create_man)
        if match:
            Current_chargemanCn     =    Create_man
            objs      =    User.objects.filter(first_name__icontains=Current_chargemanCn).values('username','first_name') 
            Current_chargemanA = None           
            if not objs.exists():
                messages.error(self.request,u'没有该用户')
            else:
                if objs[0]['first_name'] == Current_chargemanCn :
                    Current_chargemanA = objs[0]['username']
            Create_man = Current_chargemanA
        
        Check_man               =    request.GET.get('Check_man','')                     # 审核人    
           
        Task_handler            =    request.GET.get('Task_handler','') #处理人 
        match = zhPattern.search(Task_handler)
        if match:
            Current_chargemanCn     =    Task_handler
            objs      =    User.objects.filter(first_name__icontains=Current_chargemanCn).values('username','first_name') 
            Current_chargemanA = None           
            if not objs.exists():
                messages.error(self.request,u'没有该用户')
            else:
                if objs[0]['first_name'] == Current_chargemanCn :
                    Current_chargemanA = objs[0]['username']
            Task_handler = Current_chargemanA
                
        Identifier              =    request.GET.get('Identifier','')           #验证人
        match = zhPattern.search(Identifier)
        if match:
            Current_chargemanCn     =    Identifier
            objs      =    User.objects.filter(first_name__icontains=Current_chargemanCn).values('username','first_name') 
            Current_chargemanA = None           
            if not objs.exists():
                messages.error(self.request,u'没有该用户')
            else:
                if objs[0]['first_name'] == Current_chargemanCn :
                    Current_chargemanA = objs[0]['username']
            Identifier = Current_chargemanA
 
        Create_timeStart        =    request.GET.get('Create_timeStart','')#创建时间
        Create_timeEnd          =    request.GET.get('Create_timeEnd','')   
        Check_timeStart         =    request.GET.get('Check_timeStart','')#审核通过时间
        Check_timeEnd           =    request.GET.get('Check_timeEnd', '')     
        Task_handler_timeStart  =    request.GET.get('Task_handler_timeStart','')#处理结束时间
        Task_handler_timeEnd    =    request.GET.get('Task_handler_timeEnd', '')      
        Identifier_timeStart    =    request.GET.get('Identifier_timeStart','')#验证时间
        Identifier_timeEnd      =    request.GET.get('Identifier_timeEnd', '')       
        Update_timeStart        =    request.GET.get('Update_timeStart','')#最后更新时间
        Update_timeEnd          =    request.GET.get('Update_timeEnd', '')

        searchList = { 'Demand_name__contains':Demand_name, 'Flow_type__exact':Flow_type,'Flow_Status__in':Flow_Status, 'Current_chargeman__exact':Current_chargeman,
                        'Create_man__exact':Create_man, 'Check_man__exact':Check_man, 'Task_handler__exact':Task_handler,
                        'Identifier__exact': Identifier,
                        'Create_time__gte':Create_timeStart, 'Create_time__lt':Create_timeEnd, 
                        'Check_time__gte':Check_timeStart, 'Check_time__lt':Check_timeEnd, 
                        'Task_handler_time__gte':Task_handler_timeStart, 'Task_handler_time__lt':Task_handler_timeEnd, 
                        'Identifier_time__gte':Identifier_timeStart, 'Identifier_time__lt':Identifier_timeEnd, 
                        'Update_time__gte': Update_timeStart, 'Update_time__lt': Update_timeEnd,
                        }

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
                qs = qs.filter(**sl)
            except Exception,ex:
                messages.error(request,u'输入的查询数据有问题！')

        #Original_number_objs = t_task_details.objects.filter(Task_handler=request.user.first_name).values_list('Original_number')

        if status == 'mycreate':
            qs = qs.filter(Create_man=request.user.username)
        elif status == 'mytask':
            qs = qs.filter(Q(Current_chargeman=request.user.username)|Q(Pre_Identifier=request.user.username))
        elif status == 'taskout':
            qs = qs.filter(Q(Ask_time__lt=F('Task_handler_time'))|Q(Ask_time__lt=nows))
        elif status == 'all':
            qs = qs
        elif status == 'myjoin':
            qs = qs.filter(Q(Create_man=request.user.username)|Q(Check_man=request.user.username)|Q(Task_handler=request.user.username)|Q(Identifier=request.user.username))
        else:
            qs = qs

        return qs
        
    





            
            
            
            
            
            
            
            