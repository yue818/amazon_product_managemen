# -*- coding: utf-8 -*-
from .t_product_Admin import *

from django.db import connection



class t_config_mstscfinance_Admin(object):

    #top_top_navbar = False
    show_report = False
    def show_user(self,obj):
        t_config_mstsc_log_objs = t_config_mstsc_log.objects.filter(ShopName=obj.ShopName,LoginOutTime__isnull=True).values_list("FirstName",'LoginInTime','QuitReason').order_by("-LoginInTime")
        listlog=list(t_config_mstsc_log_objs)
        #t_config_mstsc_reboot=t_config_mstsc_log.objects.filter(ShopName=obj.ShopName,QuitReason="Reboot").values_list("FirstName",'LoginInTime','QuitReason').order_by("-LoginInTime")
        #if len(t_config_mstsc_reboot)>0:
            #listlog.append(t_config_mstsc_reboot[0])
        #messages.info(self.request,len(t_config_mstsc_log_objs))
        rt = u''
        if len(listlog) <1 :
            rt='<font color="#007500">%s%s</font>'%(rt,u'空闲')
            return mark_safe(rt)

        for t_config_mstsc_log_obj in listlog:
                #rt = u'<font color="#FF2D2D">%s %s %s </font><br>'%(rt,t_config_mstsc_log_obj[0],t_config_mstsc_log_obj[1])
            rt = u'<font color="#FF2D2D">%s %s %s %s</font><br>'%(rt,t_config_mstsc_log_obj[0],t_config_mstsc_log_obj[1],t_config_mstsc_log_obj[2])
        return mark_safe(rt)
    show_user.short_description = u'最近登陆信息'
    '''
    def show_reboot(self,obj):
        t_config_mstsc_log_objs = t_config_mstsc_log.objects.filter(ShopName=obj.ShopName,LoginOutTime__isnull=True).values_list("FirstName",'LoginInTime','QuitReason').order_by("-LoginInTime")
        if len(t_config_mstsc_log_objs) <1 :
            rt='<font color="#007500">%s%s</font>'%(rt,u'空闲')
            return mark_safe(rt)
        for t_config_mstsc_log_obj in t_config_mstsc_log_objs:
            rt = u'<font color="#FF2D2D">%s %s %s %s</font><br>'%(rt,t_config_mstsc_log_obj[0],t_config_mstsc_log_obj[1],t_config_mstsc_log_obj[2])
        return mark_safe(rt)
    show_reboot.short_description = u'最近重启时间'
    '''
    actions =  ['show_status_actions',]
    #from skuapp.public.aliyun_reboot import *
    def show_status_actions(self, request, queryset):
        for querysetid in queryset.all():
            rt=''
            if querysetid.CloudName=='aliyun':
                if querysetid.InstanceId is not None:
                    str_content=get_regions("ecs.aliyuncs.com","DescribeInstances",{"RegionId":querysetid.RegionId,"InstanceIds":"['%s',]"%querysetid.InstanceId},str("wjEIGuPnRjSURzUDYUmBXrFv3ijk8f"),"FP60l5Rd7FBHDNAZ","2014-05-26")
                    #true=''
                    #false=''
                    str_content=str_content.replace(': null',': 0').replace(': true',': 1').replace(': false',': 0').replace(':null',':0').replace(':true',':1').replace(':false',':0')

                    if str_content<>'':
                        content =eval(str_content)
                    else:
                        messages.error(self.request,"此主机不能查询状态,请检查主机编号及地区是否错误")
                        break
                    if content.has_key("Instances"):
                        contentList=content["Instances"]["Instance"]
                    else:
                        contentList=''
                    if len(contentList)>0:
                        for lis in contentList:
                            rt=u'%s状态:%s <br>CPU:%s 内存:%s 带宽:%s<br> 创建时间:%s<br> 到期时间:%s '%(rt,lis['Status'],lis['Cpu'],lis['Memory'],lis['InternetMaxBandwidthOut'],lis['CreationTime'],lis['ExpiredTime'])
            elif querysetid.CloudName=='tengxunyun':
                SecretId='AKIDJWaWGsByFRVN3Wo7NX9apskRXYROoSXY'
                YOUR_PARAMS = {
                        'SecretId': SecretId,
                        'Timestamp': int(time.time()),
                        'Nonce': random.randint(1, sys.maxint),
                        'Region': querysetid.RegionId,
                        'Action': 'DescribeInstances',
                        'Limit':100,
                        'InstanceIds.0':querysetid.InstanceId,
                        'Version':'2017-03-12'
                        }
                YOUR_PARAMS2 = {
                        'SecretId': SecretId,
                        'Timestamp': int(time.time()),
                        'Nonce': random.randint(1, sys.maxint),
                        'Region': querysetid.RegionId,
                        'Action': 'DescribeInstancesStatus',
                        'Limit':100,
                        'InstanceIds.0':querysetid.InstanceId,
                        'Version':'2017-03-12'
                        }
                content=main('c7eBvePFzjVKA4naOC0kWJ6seQBriaTE',YOUR_PARAMS)
                content2=main('c7eBvePFzjVKA4naOC0kWJ6seQBriaTE',YOUR_PARAMS2)
                #status2=eval(content)['Response']['InstanceSet'][0]['InstanceState']
                content=content.replace(': null',': 0').replace(': true',': 1').replace(': false',': 0').replace(':null',':0').replace(':true',':1').replace(':false',':0')
                content2=content2.replace(': null',': 0').replace(': true',': 1').replace(': false',': 0').replace(':null',':0').replace(':true',':1').replace(':false',':0')
                rt=''
                content=eval(content)
                content2=eval(content2)
                if content.has_key("Response"):
                    contentList=content['Response']['InstanceSet']
                    contentList2=content2['Response']['InstanceStatusSet']
                else:
                    contentList=''
                    contentList2=''
                if len(contentList)>0:
                    for lis in contentList:
                        rt=u'%s状态:%s <br>CPU:%s 内存:%s 带宽:%s<br> 创建时间:%s<br> 到期时间:%s '%(rt,contentList2[0]['InstanceState'],lis['CPU'],lis['Memory'],lis['InternetAccessible']['InternetMaxBandwidthOut'],lis['CreatedTime'],lis['ExpiredTime'])
                        logger = logging.getLogger('sourceDns.webdns.views')
                        logger.error("999999999999999999999999999999999999999999999999999  %s "%rt)
            else:
                pass
            t_config_mstsc_log_objs = t_config_mstsc_log.objects.filter(ShopName=querysetid.ShopName,QuitReason="Reboot").values_list("FirstName",'LoginInTime','QuitReason').order_by("-LoginInTime")
            if len(t_config_mstsc_log_objs) >0 :
                rt = u'%s<br>%s %s %s<br>'%(rt,t_config_mstsc_log_objs[0][0],t_config_mstsc_log_objs[0][1],"重启")
            t_config_mstsc_remarks_obj = t_config_mstsc.objects.get(id=querysetid.id)
            t_config_mstsc_remarks_obj.remarks=rt
            t_config_mstsc_remarks_obj.save()
    show_status_actions.short_description = u'查看主机状态'
    def show_status(self,obj):
        if obj.RegionId=='cn-qingdao':
            region='华北 1'
        elif obj.RegionId=='cn-beijing':
            region='华北 2'
        elif obj.RegionId=='cn-zhangjiakou':
            region='华北 3'
        elif obj.RegionId=='cn-hangzhou':
            region='华东 1'
        elif obj.RegionId=='cn-shanghai':
            region='华东 2'
        elif obj.RegionId=='cn-shenzhen':
            region='华南 1'
        else:
            region=str(obj.RegionId)
        if obj.remarks is not None and obj.InstanceId <>'':
            return  mark_safe("编号:"+obj.InstanceId+"<br>"+"地区："+region+'<br>'+obj.remarks)
        elif obj.InstanceId <>'':
            return  mark_safe("编号:"+obj.InstanceId+"<br>"+"地区："+region+'<br>')
        else:
            return  ''
    show_status.short_description = u'主机状态'
    def login_DP(self, obj):

        from django.db import connection
        from brick.table.t_config_mstsc_log import t_config_mstsc_log
        rt = ''
        t_config_mstsc_log_obj = t_config_mstsc_log(connection)
        result_obj = t_config_mstsc_log_obj.getdata(obj.ShopName)
        try:
            rea = result_obj[1]
            using_name = result_obj[2]
        except:
            rea = ''
            using_name = ''
        #messages.info(self.request, rea)

        if rea == 'IN':
            rt = '<br><input type="button" value="远程连接" onclick="if(confirm(\'用户:%s正在使用,是否强制登入\')) {window.open(\'/mstsc/?id=%s&staffID=%s&CloudName=%s&kvmName=%s\') }" target="_blank" />' % (using_name, obj.id, self.request.user.username, obj.CloudName, obj.kvmName)
        elif rea == 'TimeOut':
            rt = '<br><input type="button" value="远程连接" onclick="if(confirm(\'用户:%s可能正在使用,是否强制登入\')) {window.open(\'/mstsc/?id=%s&staffID=%s&CloudName=%s&kvmName=%s\') }" target="_blank" />' % (using_name, obj.id, self.request.user.username, obj.CloudName, obj.kvmName)
        else:
            rt = '<br><input type="button" value="远程连接" onclick="window.open(\'/mstsc/?id=%s&staffID=%s&CloudName=%s&kvmName=%s\')" target="_blank" />' % (obj.id, self.request.user.username, obj.CloudName, obj.kvmName)

        rt = '%s<br><br><input type="button" value="主机重启" onclick="if(confirm(\'是否重启\')) {window.location.href=\'/mstscReboot/?id=%s&staffID=%s\'} " /><br><br>' % (rt, obj.id, self.request.user.username)
        return mark_safe(rt)

    login_DP.short_description = u'远程操作'

    #list_per_page=2000
    list_display=('id','PlatformName','ShopName','seller','IP','out_ip','UserName','Password','show_user','DepartmentName','CloudName','login_DP','shop_status','clean_status')
    #list_display=('id','PlatformName','ShopName','IP','UserName','Password','show_user','InstanceId','RegionId','DepartmentName','CloudName','remarks','login_DP',)
    list_filter=('PlatformName','ShopName','seller','IP','out_ip','DepartmentName','InstanceId','RegionId','CloudName','shop_status','clean_status')
    search_fields=('PlatformName','ShopName','seller','IP','out_ip','UserName','Password','DepartmentName','InstanceId','RegionId','CloudName','shop_status','clean_status')
    list_editable=('PlatformName','ShopName','seller','IP','out_ip','UserName','Password','DepartmentName','InstanceId','RegionId','CloudName','kvmName','shop_status','clean_status')



