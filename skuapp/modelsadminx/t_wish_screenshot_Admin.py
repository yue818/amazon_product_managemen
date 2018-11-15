# -*- coding: utf-8 -*-
from .t_product_Admin import *
from skuapp.table.t_store_configuration_file import *
from skuapp.public.producer import *
from skuapp.table.t_wish_honor import t_wish_honor
from django.db.models import Q

class t_wish_screenshot_Admin(object):
    search_box_flag = True
    actions = ['show_wish_screenshot', ]
    def show_wish_screenshot(self, request, queryset):
        from app_djcelery.tasks import show_wish_screenshot as xx
        for querysetid in queryset.all():
            #screenshot=Center()
            #screenshot.callback('wish_screenshot.exe 20',querysetid.ip)
            from skuapp.table.t_wish_screenshot import t_wish_screenshot
            t_wish_screenshot.objects.filter(id=querysetid.id).update(remark='正在抓取图片，请等待约2分钟')
            xx.delay(querysetid.ip,0)
            
    show_wish_screenshot.short_description = u'手动刷新截图'
    def show_firstPage(self, obj):
        import time
        firstPage = obj.screenshotUrl_firstPage
        orderPage = obj.screenshotUrl_orderPage
        today=time.strftime('%Y-%m-%d',time.localtime(time.time()))
        rt=''
        if today in str(obj.updateTime):
            if firstPage:
                rt+="<img src='%s' width=300 alt = '%s' title='%s'/>"%(firstPage, firstPage, firstPage)
            if orderPage:
                rt+="<img src='%s' width=300 alt = '%s' title='%s'/>"%(orderPage, orderPage, orderPage)
        if rt:
            rt+='''
                <script>
                    var flag = true,//状态true为正常的状态,false为放大的状态
                           imgH,//图片的高度
                           imgW,//图片的宽度
                           imgs = document.getElementsByTagName('img');//图片元素
                    for (var i = 0; i < imgs.length; i++) {   
                    (function(i){  
                        //var p = i      
                        img2=imgs[i]
                        //alert(img2.src)
                        var flag=true
                        img2.onclick = function() { 
                            //alert(i);  
                            img=imgs[i]
                            //alert(img.src)
                            imgH = img.height; //获取图片的高度
                       imgW = img.width; //获取图片的宽度
                       if(flag){
                           //图片为正常状态,设置图片宽高为现在宽高的2倍
                           flag = false;//把状态设为放大状态
                           img.height = imgH*4;
                           img.width = imgW*4;
                       }else{
                           //图片为放大状态,设置图片宽高为现在宽高的二分之一
                           flag = true;//把状态设为正常状态
                           img.height = imgH/4;
                           img.width = imgW/4;
                       }
                        }  
                    })(i);  
                    }
                </script>
        '''
        honor=t_wish_honor.objects.filter(ShopNameOfficial=obj.shopNameOfficial).filter(updateTime__startswith=today).values_list('ShopHonor', flat=True).order_by('-updateTime')
        #logger.info("rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr%s"%honor)
        if honor is not None and len(honor)>0:
            rt+="<br>"+'%s'%honor[0]
        else:
            rt+="<br>"+"今天获取诚信店铺失败"
        if obj.remark is not None:
            rt+="<br>"+obj.remark
        return mark_safe(rt)
    show_firstPage.short_description = u'图片'
    def getMstscdata(self,db_conn,t_config_mstsc_shopname):
        cursor = db_conn.cursor()
        sql = "SELECT id,  CloudName,  kvmName FROM hq_db.t_config_mstsc WHERE ShopName = %s"
        cursor.execute(sql,(t_config_mstsc_shopname,))
        t_config_mstsc_obj = cursor.fetchone()
        cursor.close()
        return t_config_mstsc_obj
            
            
    def login_DP(self, obj):
        from django.db import connection
        from brick.table.t_config_mstsc_log import t_config_mstsc_log
        rt = ''
        t_config_mstsc_log_obj = t_config_mstsc_log(connection)
        result_obj = t_config_mstsc_log_obj.getdata(obj.shopNameOfficial)   #找到此店铺最近的一次退出原因和用户名
        try:
            rea = result_obj[1]          
            using_name = result_obj[2]
        except:
            rea = ''
            using_name = ''
        
        #messages.info(self.request, rea)
        mstscdata_obj=self.getMstscdata(connection,obj.shopNameOfficial)
        #logger.info("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy%s"%(mstscdata_obj,))
        try:
            mstsc_id = mstscdata_obj[0]          
            mstsc_CloudName= mstscdata_obj[1]
            mstsc_kvmName= mstscdata_obj[2]
        except:
            mstsc_id = ''
            mstsc_CloudName = ''
            mstsc_kvmName=''
        #logger.info("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx%s  %s  %s"%(mstsc_id,mstsc_CloudName,mstsc_kvmName))
        
        if rea == 'IN':
            rt = '<br><input type="button" value="远程连接" onclick="if(confirm(\'用户:%s正在使用,是否强制登入\')) {window.open(\'/mstsc/?id=%s&staffID=%s&CloudName=%s&kvmName=%s\') }" target="_blank" />' % (using_name, mstsc_id, self.request.user.username, mstsc_CloudName, mstsc_kvmName)
        elif rea == 'TimeOut':
            rt = '<br><input type="button" value="远程连接" onclick="if(confirm(\'用户:%s可能正在使用,是否强制登入\')) {window.open(\'/mstsc/?id=%s&staffID=%s&CloudName=%s&kvmName=%s\') }" target="_blank" />' % (using_name, mstsc_id, self.request.user.username, mstsc_CloudName, mstsc_kvmName)
        else:
            rt = '<br><input type="button" value="远程连接" onclick="window.open(\'/mstsc/?id=%s&staffID=%s&CloudName=%s&kvmName=%s\')" target="_blank" />' % (mstsc_id, self.request.user.username, mstsc_CloudName, mstsc_kvmName)
        return mark_safe(rt)
    login_DP.short_description = u'远程操作'
    list_display = ('id', 'shopNameOfficial','show_firstPage','updateTime','seller','Published','Operators','login_DP')
    list_filter = None#('shopNameOfficial','updateTime','seller','Published','Operators')
    search_fields = ('shopNameOfficial','updateTime','seller','Published','Operators')

    def get_list_queryset(self):
    
        request = self.request
        qs = super(t_wish_screenshot_Admin, self).get_list_queryset()

        shopNameOfficial = request.GET.get('shopNameOfficial', '')
        seller = request.GET.get('seller', '')
        Published = request.GET.get('Published', '')
        Operators = request.GET.get('Operators', '')
        honor1 = request.GET.get('honor1', '')
        picture = request.GET.get('picture', '')

        updateTimeStart = request.GET.get('updateTimeStart', '')
        updateTimeEnd = request.GET.get('updateTimeEnd', '')



        searchList = {'shopNameOfficial__contains': shopNameOfficial, 'seller__exact': seller,
                      'Published__exact': Published,'Operators__exact': Operators,

                      'updateTime__gte': updateTimeStart, 'updateTime__lt': updateTimeEnd,
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
        
        today=time.strftime('%Y-%m-%d',time.localtime(time.time()))
        if picture == u'抓取到图片':
            qs = qs.filter(Q(updateTime__contains = today))
        elif picture == u'未抓取到图片':
            qs = qs.exclude(Q(updateTime__contains = today) )
        else :
            qs = qs
            

        return qs
