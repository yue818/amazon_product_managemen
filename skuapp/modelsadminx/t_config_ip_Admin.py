# -*- coding: utf-8 -*-
from .t_product_Admin import *
from skuapp.table.t_config_ip_ext import *
from django.utils.safestring import mark_safe
from skuapp.table.t_sys_param import *
from django.contrib import messages


class t_config_ip_Admin(object):

    def show_ip_affect(self,obj):
        rt = ''
        num = 1
        affect_names = t_config_ip_ext.objects.filter(IP=obj.IP).values_list('K',flat=True)
        if len(affect_names) != 0:
            for affect_name in affect_names:
                if affect_name is None:
                    rt = ''
                else:
                    try:
                        aa = t_sys_param.objects.filter(V=affect_name).values_list('VDesc',flat=True)[0]
                        rt += str(num)+'.'+aa+'<br>'
                        num = num+1
                    except:
                        pass                           

        else:
            rt=''
        return mark_safe(rt)
    show_ip_affect.short_description = u'云主机用途'
    
    def show_ip_affect2(self,obj) :
        rt = '<table align="center" style="text-align:center;" border="1" cellpadding="3" cellspacing="1" bgcolor="#c1c1c1">'\
        '<tr bgcolor="#C00"><th style="text-align:center">***</th><th style="text-align:center;width:60px">Amazon</th>'\
        '<th style="text-align:center;width:60px"">Wish</th><th style="text-align:center;width:60px"">ebay</th>'\
        '<th style="text-align:center;width:60px"">Tophatter</th><th style="text-align:center;width:60px"">lazada</th>'\
        '<th style="text-align:center;width:60px"">CD</th><th style="text-align:center;width:60px"">ALIEXPRESS</th>'\
        '<th style="text-align:center;width:60px"">Shopee</th><th style="text-align:center;width:60px"">Joom</th>'\
        '<th style="text-align:center;width:60px"">Jumia</th><th style="text-align:center;width:60px"">沃尔玛</th>'\
        '<th style="text-align:center;width:60px"">舒克</th><th style="text-align:center;width:60px"">Q10</th>'\
        '<th style="text-align:center;width:60px"">mymall</th>'\
        '<th style="text-align:center;width:60px"">wadi</th>'\
        '<th style="text-align:center;width:60px"">Vova</th>'\
        '<th style="text-align:center;width:60px"">执御</th><th style="text-align:center;width:60px"">Qoo10</th></tr>'
        try:
            affect_names = t_config_ip_ext.objects.filter(IP__contains=obj.IP).values_list('K',flat=True)

        #messages.error(self.request,affect_names)
            if len(affect_names) != 0: 
                rt = u'%s<tr><th style="text-align:center;">店铺</th>'%(rt)
                             
                if u'AMAZON_INSTALLED' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)
                if u'WISH_INSTALLED' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)
                if u'EBAY_INSTALLED' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)
                if u'TOPHEATER_INSTALLED' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)
                if u'LZD_INSTALLED' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)    
                if u'CD_INSTALLED' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)
                if u'ALIEXPRESS_INSTALLED' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)    
                if u'SHOPEE_INSTALLED' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)   
                if u'JOOM_INSTALLED' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)   
                if u'JUMIA_INSTALLED' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)   
                if u'WOM_INSTALLED' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)   
                if u'SK_INSTALLED' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)   
                if u'QT_INSTALLED' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)
                if u'MYMALL_INSTALLED' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)
                if u'WADI_INSTALLED' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)
                if u'VOVA_INSTALLED' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)   
                if u'ZY_INSTALLED' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)
                if u'QO_INSTALLED' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td></tr>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td></tr>'%(rt)      
                    
                rt = u'%s<tr><th style="text-align:center;">普源抓单程序</th>'%(rt)
                if u'AMAZON_API_PY' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)
                if u'WISH_API_PY' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)
                if u'EBAY_API_PY' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)
                if u'TOPHEATER_API_PY' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)
                if u'LZD_API_PY' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)
                if u'CD_API_PY' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)
                if u'ALIEXPRESS_API_PY' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)
                if u'SHOPEE_API_PY' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)
                if u'JOOM_API_PY' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)   
                if u'JUMIA_API_PY' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)   
                if u'WOM_API_PY' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)   
                if u'SK_API_PY' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)   
                if u'QT_API_PY' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt) 
                if u'MYMALL_API_PY' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt) 
                if u'WADI_API_PY' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt) 
                if u'VOVA_API_PY' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)   
                if u'ZY_API_PY' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)  
                if u'QO_API_PY' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td></tr>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td></tr>'%(rt)   

                rt = u'%s<tr><th style="text-align:center;">账号异常情况</th>'%(rt)
                if u'AMAZON_FAILED' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">正常</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">异常</button></td>'%(rt)
                if u'WISH_FAILED' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">正常</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">异常</button></td>'%(rt)
                if u'EBAY_FAILED' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">正常</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">异常</button></td>'%(rt)
                if u'TOPHEATER_FAILED' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">正常</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">异常</button></td>'%(rt)
                if u'LZD_FAILED' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">正常</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">异常</button></td>'%(rt)
                if u'CD_FAILED' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">正常</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">异常</button></td>'%(rt)
                if u'ALIEXPRESS_FAILED' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">正常</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">异常</button></td>'%(rt)
                if u'SHOPEE_FAILED' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">正常</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">异常</button></td>'%(rt)
                if u'JOOM_FAILED' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)   
                if u'JUMIA_FAILED' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)   
                if u'WOM_FAILED' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)   
                if u'SK_FAILED' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)   
                if u'QT_FAILED' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)   
                if u'MYMALL_FAILED' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)
                if u'WADI_FAILED' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)
                if u'VOVA_FAILED' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)
                if u'ZY_FAILED' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)
                if u'QO_FAILED' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td></tr>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td></tr>'%(rt)   
                
                rt = u'%s<tr><th style="text-align:center;">Online系统的API程序</th>'%(rt)
                if u'AMAZON_API_ONLINE' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)
                if u'WISH_API_ONLINE' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)
                if u'EBAY_API_ONLINE' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)
                if u'TOPHEATER_API_ONLINE' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)
                if u'LZD_API_ONLINE' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)
                if u'CD_API_ONLINE' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)
                if u'ALIEXPRESS_API_ONLINE' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)
                if u'SHOPEE_API_ONLINE' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)
                if u'JOOM_API_ONLINE' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)   
                if u'JUMIA_API_ONLINE' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)   
                if u'WOM_API_ONLINE' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)   
                if u'SK_API_ONLINE' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)   
                if u'QT_API_ONLINE' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)
                if u'MYMALL_API_ONLINE' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt) 
                if u'WADI_API_ONLINE' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt) 
                if u'VOVA_API_ONLINE' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt)    
                if u'ZY_API_ONLINE' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td>'%(rt) 
                if u'QO_API_ONLINE' not in affect_names:
                    rt=u'%s<td><button type="button" style="background:#00FF7F">空闲</button></td></tr>'%(rt)
                else:
                    rt=u'%s<td><button type="button" style="background:red">占用</button></td></tr>'%(rt)    

            else:
                rt= u'%s<tr><th style="text-align:center;">店铺</th><td><button type="button" style="background:#00FF7F">空闲</button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">空闲</button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">空闲</button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">空闲</button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">空闲</button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">空闲</button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">空闲</button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">空闲</button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">空闲</button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">空闲</button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">空闲</button></td></tr>'\
                    u'%s<tr><th style="text-align:center;">普源抓单程序</th><td><button type="button" style="background:#00FF7F">空闲</button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">空闲</button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">空闲</button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">空闲</button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">空闲</button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">空闲</button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">空闲</button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">空闲</button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">空闲</button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">空闲</button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">空闲</button></td></tr>'\
                    u'%s<tr><th style="text-align:center;">账号异常情况</th><td><button type="button" style="background:#00FF7F"></button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">正常</button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">正常</button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">正常</button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">正常</button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">空闲</button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">空闲</button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">空闲</button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">正常</button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">正常</button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">正常</button></td></tr>'\
                    u'<tr><th style="text-align:center;">Online系统的API程序</th>'\
                    u'<td><button type="button" style="background:#00FF7F">空闲</button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">空闲</button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">空闲</button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">空闲</button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">空闲</button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">空闲</button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">空闲</button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">空闲</button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">空闲</button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">空闲</button></td>'\
                    u'<td><button type="button" style="background:#00FF7F">空闲</button></td></tr>'%(rt)
        except:
            rt='%s'%(rt)
        
   
        rt='%s</table>'%(rt)
        return mark_safe(rt)
    show_ip_affect2.short_description = mark_safe('<p align="center">云主机用途</p>')

    
    def show_cz(self,obj) :
        rt='<input type="button" value="主机用途更换" onclick="window.location.href=\'/Project/admin/skuapp/t_config_ip_ext/?_q_=%s\'" />'%(obj.IP)
        return mark_safe(rt)

    show_cz.short_description = u'操作'
    
    list_display= ('IP','CloudName','show_ip_affect2','show_cz','UpdateTime',)
    list_editable = ('CloudName',)
    #list_editable_all = ('Keywords',)
    #list_filter = ('UpdateTime',
                   # 'Weight',
                   # 'Electrification','Powder','Liquid','Magnetism','Buyer',
                   # 'Storehouse',
                   # 'DYStaffName','JZLStaffName','PZStaffName','MGStaffName','LRStaffName',
                   # 'StaffName','DepartmentID',
                   # )

    list_filter = ('IP','CloudName',)

    search_fields = ('IP','CloudName',)

    readonly_fields = ()

    show_detail_fields = ['id']



            
            
            
            
            
            
            
            