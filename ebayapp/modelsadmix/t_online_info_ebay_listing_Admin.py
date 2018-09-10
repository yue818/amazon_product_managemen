# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from django.contrib import messages
from brick.classredis.classlisting import classlisting
from brick.classredis.classshopsku import classshopsku
from django.db import connection
from django_redis import get_redis_connection
from brick.pydata.py_redis.py_SynRedis_tables import py_SynRedis_tables
from brick.pricelist.calculate_price import calculate_price
from django.contrib import messages
from skuapp.table.t_online_info_ebay_subsku import t_online_info_ebay_subsku
from ebayapp.table.t_config_site_ebay import t_config_site_ebay
from brick.classredis.classsku import classsku
from ebayapp.table.t_online_info_ebay_listing import t_online_info_ebay_listing
from pyapp.models import b_goodsskulinkshop
from pyapp.models import b_goods
from django.http import HttpResponseRedirect


from Project.settings import *
import errno
import oss2
import os
from pyapp.table.kc_currentstock_sku import kc_currentstock_sku

redis_conn = get_redis_connection(alias='product')
listingobjs = classlisting(connection, redis_conn)
classsku_obj = classsku()
classshopskuobjs = classshopsku(connection, redis_conn)
py_SynRedis_tables_obj = py_SynRedis_tables()
from skuapp.table.t_config_store_ebay import t_config_store_ebay
from datetime import  datetime as timetime
from app_djcelery.tasks import refresh_syn_ebayapp_shopdata
from brick.table.t_wish_store_oplogs import t_wish_store_oplogs
from django.http import HttpResponse
from skuapp.table.t_store_configuration_file import t_store_configuration_file
import json
t_wish_store_oplogs_obj = t_wish_store_oplogs(connection)
import inspect

def check_permission_legality(self):
    funcName = inspect.stack()[1][3]
    permname = '{}.Can_{}_{}'.format(self.model._meta.app_label, self.model._meta.model_name, funcName)
    if self.request.user.is_superuser or self.request.user.has_perm(permname):
        return True
    return False

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5 (except OSError, exc: for Python <2.5)
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

EBAY_SITE_DICT = {'0': 'US', '2': 'CA', '3': 'UK', '100': 'eBayMotors', '101': 'IT', '71': 'FR', '77': 'DE', '15': 'AU', '186': 'ES'}
class t_online_info_ebay_listing_Admin(object):
    wish_key_words = True
    ebay_listing_plugin2 = True
    #sort_item = True
    sort_bar = True
    site_left_menu_flag_ebay = True
    search_box_flag = True

    def has_delete_permission(self, obj=None):
        if self.request.user.is_superuser:
            return True
        else:
            return False

    def show_Picture(self, obj):
        ZSHWCL = ['Ottendorf-Okrilla', 'Rowland Heights,CA/Dayton,NJ', 'Rowland Heights, California','Dayton, New Jersey', 'Dandenong', 'Walsall', 'Leicestershire']
        url = u'%s' % (obj.img)
        rt = u'<div><img src="%s" width="150" height="150"  alt = "%s" title="%s" style="cursor:pointer;"/></div>'% (url, url, url)
        if obj.status == u'Active':
            rt += u'<br><span style="width: 20px;height: 20px;background-color: green;color: white;text-align: center;line-height: 20px;border-radius:4px" title="链接状态为Active">Active</span>'
        elif obj.status == u'Unsold':
            rt += u'<br><span style="width: 20px;height: 20px;background-color:orange;color: white;text-align: center;line-height: 20px;border-radius:4px" title="链接状态为Unsold">Unsold</span>'
        elif obj.status == u'Drafts':
            rt += u'<br><span style="width: 20px;height: 20px;background-color:blue;color: white;text-align: center;line-height: 20px;border-radius:4px" title="链接状态为Drafts">Drafts</span>'
        elif obj.status == u'Ended':
            rt += u'<br><span style="width: 20px;height: 20px;background-color:red;color: white;text-align: center;line-height: 20px;border-radius:4px" title="链接状态为Ended">Ended</span>'
        elif obj.status == u'Scheduled':
            rt += u'<br><span style="width: 20px;height: 20px;background-color:indigo;color: white;text-align: center;line-height: 20px;border-radius:4px" title="链接状态为Scheduled">Scheduled</span>'
        elif obj.status == u'Completed':
            rt += u'<br><span style="width: 20px;height: 20px;background-color:gray;color: white;text-align: center;line-height: 20px;border-radius:4px" title="链接状态为Completed">Completed</span>'

        if obj.Country and obj.Country == u'CN':
            rt += u'<span style="width: 20px;height: 20px;background-color:green;color: white;text-align: center;line-height: 20px;border-radius:4px" title="自发货">&nbsp;自&nbsp;</span>'
        elif obj.Country and obj.Country != u'CN' and obj.Location not in ZSHWCL:
            rt += u'<span width: 20px;height: 20px;span style="background-color:indigo;color: white;text-align: center;line-height: 20px;border-radius:4px" title="虚拟海外仓">&nbsp;虚&nbsp;</span>'
        elif obj.Country and obj.Country != u'CN' and obj.Location in ZSHWCL:
            rt += u'<span width: 20px;height: 20px;span style="background-color:orange;color: white;text-align: center;line-height: 20px;border-radius:4px" title="真实海外仓">&nbsp;真&nbsp;</span>'

        #TortInfo:  N：未侵权，EY:eBay侵权，Y:其他侵权
        if obj.TortInfo == u'N':
            rt += u'<span style="width: 20px;height: 20px;background-color:green;color: white;text-align: center;line-height: 20px;border-radius:4px" title="未侵权">&nbsp;N&nbsp;</span>'
        elif obj.TortInfo == u'EY':
            rt += u'<span style="width: 20px;height: 20px;background-color:red;color: white;text-align: center;line-height: 20px;border-radius: 4px" title="eBay侵权">&nbsp;EY&nbsp;</span>'
        elif obj.TortInfo == u'EY':
            rt += u'<span style="width: 20px;height: 20px;background-color:red;color: white;text-align: center;line-height: 20px;border-radius: 4px" title="其他侵权">&nbsp;Y&nbsp;</span>'

        return mark_safe(rt)
    show_Picture.short_description = u'<p align="center"style="color:#428bca;">图片</p>'

    def show_SKU_list(self, obj):
        autoSelect = self.request.GET.get('autoSelect','')
        EXPRESS = self.request.GET.get('EXPRESS', '')
        ZSHWCL = ['Ottendorf-Okrilla', 'Rowland Heights,CA/Dayton,NJ', 'Rowland Heights, California','Dayton, New Jersey', 'Dandenong', 'Walsall', 'Leicestershire']
        rt = u'<table class="table table-condensed">' \
             u'<thead><tr><th></th><th>商品SKU</th><th>商品状态</th><th>可用数量</th><th>可售天数</th>' \
             u'<th>店铺SKU</th><th>库存</th><th>销量</th><th>价格</th><th>利润率(%)</th></tr></thead><tbody>'
        t_online_info_ebay_subsku_objs = t_online_info_ebay_subsku.objects.filter(itemid=obj.itemid)
        t_config_site_ebay_objs = t_config_site_ebay.objects.all().values('siteID','siteName')
        site_dict = {}
        
        sku_status = {u'1':u'正常',u'2':u'售完下架',u'3':u'临时下架', u'4':u'停售',u'':u'--',None:u'--'}
        for t_config_site_ebay_obj in t_config_site_ebay_objs:
            site_dict[t_config_site_ebay_obj['siteID']] = t_config_site_ebay_obj['siteName']
        if len(t_online_info_ebay_subsku_objs) > 0:
            for t_online_info_ebay_subsku_obj in t_online_info_ebay_subsku_objs:
                # pSKU = classshopskuobjs.getSKU(t_online_info_ebay_subsku_obj.subSKU)
                # pgoodstatus = classsku_obj.get_goodsstatus_by_sku(str(pSKU))
                # pCanSaleDay = classsku_obj.get_cansaleday_by_sku(str(pSKU))
                pSKU = t_online_info_ebay_subsku_obj.productsku
                pgoodstatus = t_online_info_ebay_subsku_obj.productstatus
                pUseNumber = t_online_info_ebay_subsku_obj.UseNumber
                pCanSaleDay = t_online_info_ebay_subsku_obj.SaleDay
                try:
                    profitrate = ''
                    startprice = t_online_info_ebay_subsku_obj.startprice
                    calculate_price_obj = calculate_price(str(pSKU))
                    if obj.Country and obj.Country != u'CN' and obj.Location not in ZSHWCL:
                        t_cfg_platform_country = u'EBAYXNHWC'
                    elif obj.Country and obj.Country != u'CN' and obj.Location in ZSHWCL:
                        t_cfg_platform_country = u'EBAYZSHWC'
                    else:
                        b_goods_objs = b_goods.objects.filter(SKU=str(pSKU)).values('AttributeName')
                        if len(b_goods_objs) > 0:
                            AttributeName = b_goods_objs[0]['AttributeName']
                            if AttributeName:
                                if u'特货' in AttributeName:
                                    t_cfg_platform_country = u'EBAYGNZFTH'
                                else:
                                    t_cfg_platform_country = u'EBAYGNZF'
                            else:
                                t_cfg_platform_country = u'EBAYGNZF'
                        else:
                            t_cfg_platform_country = u'EBAYGNZF'

                    profitrate_info = calculate_price_obj.calculate_profitRate(startprice,platformCountryCode=t_cfg_platform_country, DestinationCountryCode=site_dict[long(obj.site)])
                    profitrate = profitrate_info['profitRate']
                except Exception,ex:
                    profitrate = ''

                try:
                    # available = int(t_online_info_ebay_subsku_obj.total) - int(t_online_info_ebay_subsku_obj.sold)
                    realavailable = t_online_info_ebay_subsku_obj.realavailable
                except:
                    realavailable = 0
                if realavailable == 0:
                    sub_style = u'background:red;'
                else:
                    sub_style = ''
                isSelected = u''
                u""""
                    自发货：
                       下架：链接状态Active,状态非正常 库存数量>0 自动勾选 
                       上架：链接状态Active,状态正常  库存数量为0 自动勾选
                    海外：
                       下架：链接状态Active,状态非正常或可用数量<=0 库存数量>0 自动勾选 
                       上架：链接状态Active,可用数量>0,状态正常  库存数量为0 自动勾选
                """
                if realavailable or realavailable == 0:
                    if (EXPRESS == u'ALL' or not EXPRESS) and obj.Location in ZSHWCL:
                        isSelected = ''
                    else:
                        if obj.Country and obj.Country == u'CN':
                            if obj.status == u'Active' and pgoodstatus in [u'2',u'3',u'4'] and realavailable > 0 and autoSelect in [u'endsku',u'allendsku']:
                                isSelected = 'checked'
                            elif obj.status == u'Active' and pgoodstatus == u'1' and realavailable <= 0 and autoSelect in [u'relistsku',u'allrelistsku']:
                                isSelected = 'checked'
                        elif obj.Country and obj.Country != u'CN':
                            if obj.status == u'Active' and autoSelect in [u'endsku',u'allendsku']:
                                if ((pUseNumber is not None and pUseNumber <= 0) or pgoodstatus in [u'2',u'3',u'4']) and realavailable > 0:
                                    isSelected = 'checked'
                            elif obj.status == u'Active' and autoSelect in [u'relistsku',u'allrelistsku']:
                                if pUseNumber > 0 and realavailable is not None and realavailable <= 0 and pgoodstatus == '1':
                                    isSelected = 'checked'

                style = ''
                if pgoodstatus == u'1' :
                    style = 'class ="success"'
                elif pgoodstatus == None or pgoodstatus == '':
                    style = ''
                else:
                    style = 'class ="danger"'  # 非正常为红色

                try:
                    pgoodstatus = sku_status[pgoodstatus]
                except:
                    pgoodstatus = u'--'

                rt += u'<tr %s><td><label><input type="checkbox" name="ebayapp_shopskucheck" %s id="%s_||_%s_||_%s_||_%s_||_%s_||_%s_||_%s_||_%s"></label></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td style="BORDER-LEFT: #DDDDDD 1px solid;">%s</td>' \
                      u'<td style="%s">%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (style,isSelected,obj.id,obj.itemid,obj.ShopName,obj.site,t_online_info_ebay_subsku_obj.subSKU,
                                                                              t_online_info_ebay_subsku_obj.total if t_online_info_ebay_subsku_obj.total else 0,
                                                                                         t_online_info_ebay_subsku_obj.sold if t_online_info_ebay_subsku_obj.sold else 0,u'yes',
                                                                              pSKU,pgoodstatus,pUseNumber,pCanSaleDay,t_online_info_ebay_subsku_obj.subSKU,
                                                                                                      sub_style,realavailable,t_online_info_ebay_subsku_obj.sold,t_online_info_ebay_subsku_obj.startprice,profitrate)
        else:
            # pSKU = classshopskuobjs.getSKU(obj.SKU)
            # # messages.success(self.request,'SKU== %s  pSKU=== %s' % (obj.SKU, pSKU))
            # pgoodstatus = classsku_obj.get_goodsstatus_by_sku(str(pSKU))
            # pCanSaleDay = classsku_obj.get_cansaleday_by_sku(str(pSKU))
            pSKU = obj.Productsku
            pgoodstatus = obj.Productstatus
            pUseNumber = obj.UseNumber
            pCanSaleDay = obj.SaleDay
            try:
                profitrate = ''
                currentprice = obj.currentprice
                calculate_price_obj = calculate_price(str(pSKU))
                if obj.Country and obj.Country != u'CN' and obj.Location not in ZSHWCL:
                    t_cfg_platform_country = u'EBAYXNHWC'
                elif obj.Country and obj.Country != u'CN' and obj.Location in ZSHWCL:
                    t_cfg_platform_country = u'EBAYZSHWC'
                else:
                    b_goods_objs = b_goods.objects.filter(SKU=str(pSKU)).values('AttributeName')
                    if len(b_goods_objs) > 0:
                        AttributeName = b_goods_objs[0]['AttributeName']
                        if AttributeName:
                            if u'特货' in AttributeName:
                                t_cfg_platform_country = u'EBAYGNZFTH'
                            else:
                                t_cfg_platform_country = u'EBAYGNZF'
                        else:
                            t_cfg_platform_country = u'EBAYGNZF'
                    else:
                        t_cfg_platform_country = u'EBAYGNZF'
                profitrate_info = calculate_price_obj.calculate_profitRate(currentprice,platformCountryCode=t_cfg_platform_country, DestinationCountryCode=site_dict[long(obj.site)])
                profitrate = profitrate_info['profitRate']
            except:
                profitrate = ''
            try:
                # available = int(obj.available)-int(obj.sold)
                realavailable = obj.realavailable
            except:
                realavailable = 0

            if realavailable == 0:
                sub_style = u'background:red;'
            else:
                sub_style = ''

            isSelected = ''
            if realavailable or realavailable == 0:
                if (EXPRESS == u'ALL' or not EXPRESS) and obj.Location in ZSHWCL:
                    isSelected = ''
                else:
                    if obj.Country and obj.Country == u'CN':
                        if obj.status == u'Active' and pgoodstatus in [u'2', u'3', u'4'] and realavailable > 0 and autoSelect in [u'endsku', u'allendsku']:
                            isSelected = 'checked'
                        elif obj.status == u'Active' and pgoodstatus == u'1' and realavailable <= 0 and autoSelect in [u'relistsku', u'allrelistsku']:
                            isSelected = 'checked'
                    elif obj.Country and obj.Country != u'CN':
                        if obj.status == u'Active' and autoSelect in [u'endsku', u'allendsku']:
                            if ((pUseNumber is not None and pUseNumber <= 0) or pgoodstatus in [u'2', u'3',u'4']) and realavailable > 0:                                isSelected = 'checked'
                        elif obj.status == u'Active' and autoSelect in [u'relistsku', u'allrelistsku']:
                            if pUseNumber > 0 and realavailable is not None and realavailable <= 0 and pgoodstatus == '1':
                                isSelected = 'checked'

            style = ''
            if pgoodstatus == u'1':
                style = 'class ="success"'
            elif pgoodstatus == None or pgoodstatus == '':
                style = ''
            else:
                style = 'class ="danger"'  # 非正常为红色

            try:
                pgoodstatus = sku_status[pgoodstatus]
            except:
                pgoodstatus = u'--'

            rt += u'<tr %s><td><label><input type="checkbox" name="ebayapp_shopskucheck" %s id="%s_||_%s_||_%s_||_%s_||_%s_||_%s_||_%s_||_%s"></label></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td style="BORDER-LEFT: #DDDDDD 1px solid;">%s</td>' \
                  u'<td style="%s">%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (style, isSelected,obj.id, obj.itemid, obj.ShopName,obj.site, obj.SKU,obj.available,obj.sold if obj.sold  else 0,u'no',
                                                                                     pSKU, pgoodstatus,pUseNumber, pCanSaleDay, obj.SKU,
                                                                                     sub_style,realavailable,obj.sold if obj.sold  else 0 ,obj.currentprice, profitrate)
        # rt += u'<tr><td></td><td><a id="vlink_id_%s">编辑变体</a></td><td><a id="alink_id_%s">sku上架</a></td><td><a id="clink_id_%s">sku下架</a></td></tr>' % (obj.id,obj.id,obj.id)
        rt += u'</tbody></table>'
        return mark_safe(rt)
    show_SKU_list.short_description = u'<p align="center"style="color:#428bca;">链接信息</p>'

    def show_Title_itemid(self, obj):
        rt = u''
        try:
            ssStore = t_store_configuration_file.objects.filter(ShopName=obj.ShopName)
            seller = ssStore[0].Seller if ssStore else ''
            Operators = ssStore[0].Operators if ssStore else ''
            
            l = obj.title.split(' ')
            aa = len(l)
            ll = ''
            if aa <= 6:
                rt = u'标题: %s <br>' % obj.title
            elif aa > 6:
                newe_Title_list = []
                for i in range(0, len(l), 6):
                    min_list = ''
                    for a in l[i:i + 6]:
                        min_list = u'%s%s ' % (min_list, a)
                    newe_Title_list.append(min_list)
                for newe_Title in newe_Title_list:
                    ll = u'%s%s<br>' % (ll, newe_Title)
                rt = u'%s标题: %s' % (rt, ll)
            rt = u'%s<br>标识ID:<a href="https://www.ebay.com/itm/%s" target="_blank">%s</a><br>卖家简称: %s<br> 店长/销售员:%s <br>%s <br>运营人员:%s' % (
                rt, obj.itemid, obj.itemid, obj.ShopName, seller,u'刊登人:%s'% obj.Published if obj.Published else u'刊登人:',Operators)
        except:
            rt += u'标识ID:<a href="https://www.ebay.com/itm/%s" target="_blank">%s</a><br>卖家简称: %s'% (obj.itemid, obj.itemid,obj.ShopName)
        # rt += (u'<br>发货地:%s'% obj.Location) if obj.Country and obj.Country != 'CN' else ''

        try:
            rt += u'<br>站点&发货地:<span style="color:green;">%s</span> %s' % (EBAY_SITE_DICT[obj.site],obj.Location)
        except:
            rt += u'<br>发货地:%s' % obj.Location

        if obj.dostatus == 'doError' or obj.dostatus == 'shopError':
            rt += u'<br><span style="color:red;">错误信息:%s <span>' % str(obj.info).replace("'","")
        return mark_safe(rt)

    show_Title_itemid.short_description = u'<p align="center"style="color:#428bca;">详情<p>'

    def show_operations(self, obj):
        syn = """
            <br><a id='syn_item_ebayapp_%s' title='单条同步'>同步</a>
            <script>
                $('#syn_item_ebayapp_%s').on('click',function(){
                    alert('start to synchronization')
                     $.getJSON(
                        "/syn_itemid_ebayapp/",
                        {'id':'%s','ShopName':'%s','ItemID':'%s'},
                         function(data){
                            alert(data.messages);
                         }
                     );
                 });
            </script>
        """% (obj.id,obj.id,obj.id, obj.ShopName, obj.itemid)

        up = u'<br><a onclick="enable_id_%s(\'%s\')"title="对整个listing做上架操作">上架</a>' % (obj.id, obj.itemid)
        en = u"<script>function enable_id_%s(listingid) {layer.confirm('itemid:'+listingid + '  请问确定要进行上架吗？'," \
              u"{btn: ['确定','算了'],btn1:function(id){ window.location.href = '/relist_end_item_ebayapp/?type=relistItem&id=%s';},});}" \
              u"</script>" % (obj.id,obj.id)

        down = u'<br><a onclick="disable_id_%s(\'%s\')"title="对整个listing做下架操作">下架</a>' % (obj.id, obj.itemid,)
        dis = u"<script>function disable_id_%s(listingid) {layer.confirm('itemid'+listingid + '  请问确定要进行下架吗？'," \
              u"{btn: ['确定','算了'],btn1:function(){ window.location.href = '/relist_end_item_ebayapp/?type=endItem&id=%s';},});}" \
              u"</script>" % (obj.id,obj.id)

        if check_permission_legality(self):
            rt = syn + up + en + down + dis
        else:
            rt = u'无权操作'
        return mark_safe(rt)
    show_operations.short_description = u'<p align="center"style="color:#428bca;">操作</p>'

    def show_Operatoion(self, obj):
        OperaType = ''
        if obj.OperaType == u'synShop':
            OperaType = u'店铺级同步'
        elif obj.OperaType == u'synItem':
            OperaType = u'单条同步'
        elif obj.OperaType == u'relistItem':
            OperaType = u'全链接上架'
        elif obj.OperaType == u'endItem':
            OperaType = u'全链接下架'
        elif obj.OperaType == u'endItemSKU':
            OperaType = u'SKU下架'
        elif  obj.OperaType == u'ReListItemSKU':
            OperaType = u'SKU上架'
        rt = u'%s<br>%s <br>%s <br> %s' % (obj.lastRefreshTime,u'自动' if obj.Operator == u'auto' else obj.Operator,OperaType,u'成功' if obj.dostatus==u'doSuccess' else u'失败')
        return mark_safe(rt)
    show_Operatoion.short_description = u'<p align="center"style="color:#428bca;">操作时间/人/类型/时间</p>'

    def show_time(self, obj):
        rt = u'在线刷新时间:<br>%s' % obj.lastRefreshTime
        try:
            rt += u'<br>商品最近刷新:<br>%s' % obj.SKURefreshTime
            rt += u'<br>上架(UTC):<br>%s' % obj.starttime
            rt += u'<br>下架(UTC):<br>%s' % obj.endtime
        except:
            pass
        return mark_safe(rt)
    show_time.short_description = mark_safe(u'<p align="center" style="width:150px;color:#428bca;">时间</p>')

    def show_count(self,obj):
        rt = u'<table class="table table-condensed"><tr><td>七天销量</td><td>%s</td></tr><tr>' \
             u'<td>浏览量</td><td>%s</td></tr><tr><td>收藏量</td><td>%s</td></tr>' \
             u'<tr><td>总销量</td><td>%s</td></tr>' \
             u'</table>'%(obj.Orders7Days if obj.Orders7Days else 0,obj.hitCount,obj.watchCount,obj.sold)
        return mark_safe(rt)
    show_count.short_description = mark_safe(u'<p align="center" style="width:150px;color:#428bca;">浏览量</p>')

    def show_Orders7Days(self,obj):
        rt = u''
        t_online_info_ebay_subsku_objs = t_online_info_ebay_subsku.objects.filter(itemid=obj.itemid)
        if len(t_online_info_ebay_subsku_objs) > 0 :
            rt = obj.Orders7Days
        else:
            rt = u'--'
        return mark_safe(rt)
    show_Orders7Days.short_description = mark_safe(u'<p align="center" style="color:#428bca;">七天销量</p>')

    def show_sold(self,obj):
        rt = u''
        t_online_info_ebay_subsku_objs = t_online_info_ebay_subsku.objects.filter(itemid=obj.itemid)
        if len(t_online_info_ebay_subsku_objs) > 0 :
            rt = obj.sold
        else:
            rt = u'--'
        return mark_safe(rt)
    show_sold.short_description = mark_safe(u'<p align="center" style="color:#428bca;">总销量</p>')

    def show_Orders7Days(self, obj):
        rt = u''
        # t_online_info_ebay_subsku_objs = t_online_info_ebay_subsku.objects.filter(itemid=obj.itemid)
        # if len(t_online_info_ebay_subsku_objs) > 0:
        #     rt = obj.Orders7Days
        # else:
        #     rt = u'--'
        rt = obj.Orders7Days if obj.Orders7Days else 0
        return mark_safe(rt)
    show_Orders7Days.short_description = mark_safe(u'<p align="center" style="color:#428bca;">七天销量</p>')

    listing_link_id = (u'id',)
    list_display = (u'show_Picture', u'show_Title_itemid',u'show_count',
                u'show_SKU_list',u'show_time', u'show_Operatoion', u'show_operations',)

    actions = [u'_batch_syn_data_by_api',u'_batch_Completed_data_by_api',u'_batch_Active_data_by_api',
               u'cexport_excel_item_information',u'get_item_to_collection_box',u'autoSelect_sku']

    def autoSelect_sku(self, request, objs):
        from app_djcelery.tasks import relist_end_item_ebayapp
        ZSHWCL = ['Ottendorf-Okrilla', 'Rowland Heights,CA/Dayton,NJ', 'Rowland Heights, California','Dayton, New Jersey', 'Dandenong', 'Walsall', 'Leicestershire']
        pautoSelect = request.POST.get('pautoSelect','')
        pautoSelect_flag = request.POST.get('pautoSelect_flag','')
        EXPRESS = request.GET.get('EXPRESS','')
        # sResult = {}
        alldatas = self.get_list_queryset()
        params_list = []
        all_auto_select = 0
        for qs in alldatas:
            if qs.Location in ZSHWCL and (EXPRESS == 'ALL' or not EXPRESS):
                continue
            t_online_info_ebay_subsku_objs = t_online_info_ebay_subsku.objects.filter(itemid=qs.itemid)
            if len(t_online_info_ebay_subsku_objs) > 0:
                for t_online_info_ebay_subsku_obj in t_online_info_ebay_subsku_objs:
                    param = {}
                    param['reviseData'] = []
                    reviseData = {}
                    flag = 0

                    pgoodstatus = t_online_info_ebay_subsku_obj.productstatus
                    pUseNumber = t_online_info_ebay_subsku_obj.UseNumber
                    try:
                        realavailable = t_online_info_ebay_subsku_obj.realavailable
                    except:
                        realavailable = 0

                    if not realavailable and realavailable <> 0:
                        continue

                    reviseData['ItemID'] = qs.itemid
                    param['ShopName'] = qs.ShopName
                    param['Site'] = qs.site
                    reviseData['SKU'] = t_online_info_ebay_subsku_obj.subSKU
                    param['Operator'] = request.user.username
                    # aQuantity = int(t_online_info_ebay_subsku_obj.total) - int(t_online_info_ebay_subsku.sold)
                    aQuantity = int(realavailable)

                    if qs.Country and qs.Country == u'CN':
                        if qs.status == u'Active' and pgoodstatus in [u'2', u'3',u'4'] and realavailable > 0 and pautoSelect == u'allendsku':
                            if aQuantity > 0:
                                reviseData['Quantity'] = 0
                                reviseData['realQuantity'] = int(t_online_info_ebay_subsku_obj.sold)
                                reviseData['sold'] = int(t_online_info_ebay_subsku_obj.sold)
                                reviseData['isVariations'] = 'yes'
                            else:
                                continue
                            param['Type'] = 'endItemSKU'
                            flag = 1
                        elif qs.status == u'Active' and pgoodstatus == u'1' and realavailable <= 0 and pautoSelect == u'allrelistsku':
                            Quantity = aQuantity + 1 if aQuantity > 0 else 5
                            reviseData['Quantity'] = Quantity
                            reviseData['realQuantity'] = Quantity + int(t_online_info_ebay_subsku_obj.sold)
                            reviseData['sold'] = int(t_online_info_ebay_subsku_obj.sold)
                            reviseData['isVariations'] = 'yes'
                            param['Type'] = 'ReListItemSKU'
                            flag = 1

                    elif qs.Country and qs.Country != u'CN':
                        if qs.status == u'Active' and pautoSelect == u'allendsku':
                            if ((pUseNumber is not None and pUseNumber <= 0) or pgoodstatus in [u'2', u'3',u'4']) and realavailable > 0:
                                if aQuantity > 0:
                                    reviseData['Quantity'] = 0
                                    reviseData['realQuantity'] = int(t_online_info_ebay_subsku_obj.sold)
                                    reviseData['sold'] = int(t_online_info_ebay_subsku_obj.sold)
                                    reviseData['isVariations'] = 'yes'
                                else:
                                    continue
                                param['Type'] = 'endItemSKU'
                                flag = 1

                        elif qs.status == u'Active' and pautoSelect == u'allrelistsku':
                            if pUseNumber > 0 and realavailable is not None and realavailable <= 0 and pgoodstatus == u'1':
                                Quantity = aQuantity + 1 if aQuantity > 0 else 5
                                reviseData['Quantity'] = Quantity
                                reviseData['realQuantity'] = Quantity + int(t_online_info_ebay_subsku_obj.sold)
                                reviseData['sold'] = int(t_online_info_ebay_subsku_obj.sold)
                                reviseData['isVariations'] = 'yes'
                                param['Type'] = 'ReListItemSKU'
                                flag = 1

                    if flag == 1:
                        all_auto_select += 1
                        param['reviseData'].append(reviseData)
                        is_exist = 0
                        for pl in params_list:
                            if param['ShopName'] == pl['ShopName'] and param['Site'] == pl['Site'] and param['Type'] == pl['Type'] and len(pl['reviseData']) < 3:
                                pl['reviseData'].append(reviseData)
                                is_exist = 1
                            else:
                                continue
                        if is_exist == 1:
                            continue
                        elif is_exist == 0:
                            params_list.append(param)

            else:
                param = {}
                param['reviseData'] = []
                reviseData = {}
                flag = 0

                pgoodstatus = qs.Productstatus
                pUseNumber = qs.UseNumber
                try:
                    realavailable = qs.realavailable
                except:
                    realavailable = 0

                if not realavailable and realavailable <> 0:
                    continue

                reviseData['ItemID'] = qs.itemid
                param['ShopName'] = qs.ShopName
                param['Site'] = qs.site
                reviseData['SKU'] = qs.SKU
                param['Operator'] = request.user.username
                aQuantity = int(realavailable)
                if qs.Country and qs.Country == u'CN':
                    if qs.status == u'Active' and pgoodstatus in [u'2', u'3',u'4'] and realavailable > 0 and pautoSelect == u'allendsku':
                        if aQuantity > 0:
                            reviseData['Quantity'] = 0
                            reviseData['realQuantity'] = int(qs.sold)
                            reviseData['sold'] = int(qs.sold)
                            reviseData['isVariations'] = 'no'
                        else:
                            continue
                        param['Type'] = 'endItemSKU'
                        flag = 1
                    elif qs.status == u'Active' and pgoodstatus == u'1' and realavailable <= 0 and pautoSelect == u'allrelistsku':
                        Quantity = aQuantity + 1 if aQuantity > 0 else 5
                        reviseData['Quantity'] = Quantity
                        reviseData['realQuantity'] = Quantity + int(qs.sold)
                        reviseData['sold'] = int(qs.sold)
                        reviseData['isVariations'] = 'no'
                        param['Type'] = 'ReListItemSKU'
                        flag = 1
                elif qs.Country and qs.Country != u'CN':
                    if qs.status == u'Active' and pautoSelect == u'allendsku':
                        if ((pUseNumber is not None and pUseNumber <= 0) or pgoodstatus in [u'2', u'3',u'4']) and realavailable > 0:
                            if aQuantity > 0:
                                reviseData['Quantity'] = 0
                                reviseData['realQuantity'] = int(qs.sold)
                                reviseData['sold'] = int(qs.sold)
                                reviseData['isVariations'] = 'no'
                            else:
                                continue
                            param['Type'] = 'endItemSKU'
                            flag = 1
                    elif qs.status == u'Active' and pautoSelect == u'allrelistsku':
                        if pUseNumber > 0 and realavailable is not None and realavailable <= 0 and pgoodstatus == u'1':
                            Quantity = aQuantity + 1 if aQuantity > 0 else 5
                            reviseData['Quantity'] = Quantity
                            reviseData['realQuantity'] = Quantity + int(qs.sold)
                            reviseData['sold'] = int(qs.sold)
                            reviseData['isVariations'] = 'no'
                            param['Type'] = 'ReListItemSKU'
                            param['Type'] = 'ReListItemSKU'
                            flag = 1

                if flag == 1:
                    all_auto_select += 1
                    param['reviseData'].append(reviseData)
                    is_exist = 0
                    for pl in params_list:
                        if param['ShopName'] == pl['ShopName'] and param['Site'] == pl['Site'] and param['Type'] == pl['Type'] and len(pl['reviseData']) < 3:
                            pl['reviseData'].append(reviseData)
                            is_exist = 1
                        else:
                            continue
                    if is_exist == 1:
                        continue
                    elif is_exist == 0:
                        params_list.append(param)

        # sResult['hhhh'] = len(params_list)
        # sResult['params_list'] = params_list
        # sResult['pautoSelect'] = pautoSelect
        # sResult['all_auto_select'] = all_auto_select
        # sResult['url']= self.request.get_full_path()
        # sResult['pautoSelect_flag'] = pautoSelect_flag
        # if pautoSelect == u'allrelistsku':
        #     sResult['pautoSelect=allrelistsku'] = 'is'
        if pautoSelect_flag == u"1":
            return HttpResponseRedirect(request.get_full_path()+'&Select_flag='+str(all_auto_select))
        else:
            # return HttpResponse(json.dumps(sResult))
            if len(params_list) > 0:
                relist_end_item_ebayapp(params_list)

    autoSelect_sku.short_description = u''


    def _batch_syn_data_by_api(self, request, objs):
        sResult = {'rcode': '0', 'messages': ''}  # 初始状态
        opnum = 'ebayapp_synItem_%s_%s' % (timetime.now().strftime('%Y%m%d%H%M%S'), request.user.username)
        try:
            param = {}  # 操作日志的参数
            param['OpNum'] = opnum
            param['OpKey'] = objs.values_list("itemid", flat=True)
            param['OpType'] = 'synItem'
            param['Status'] = 'runing'
            param['ErrorInfo'] = ''
            param['OpPerson'] = request.user.username
            param['OpTime'] = timetime.now()
            param['OpStartTime'] = timetime.now()
            param['OpEndTime'] = None
            param['aNum'] = len(objs)
            param['rNum'] = 0
            param['eNum'] = 0

            iResult = t_wish_store_oplogs_obj.createLog(param)
            assert iResult['errorcode'] == 0, "insert log error."
            synparams = []
            for obj in objs:
                param = {}
                id = obj.id
                param['ShopName'] = obj.ShopName
                param['ItemID'] = obj.itemid
                param['synType'] = 'synItem'
                param['OpNum'] = opnum
                param['operator'] = request.user.username
                synparams.append(param)
            # refresh_syn_ebayapp_shopdata.delay(params=synparams)
            refresh_syn_ebayapp_shopdata(params=synparams)
            sResult['rcode'] = 1
            sResult['KEY'] = opnum
            sResult['messages'] = 'Now Start synItem !!!'
        except Exception, ex:
            sResult['rcode'] = -1
            sResult['messages'] = '%s:%s' % (Exception, ex)
        return HttpResponse(json.dumps(sResult))
    _batch_syn_data_by_api.short_description =  u'批量同步选中商品'

    def _batch_Completed_data_by_api(self,request, objs):
        from app_djcelery.tasks import relist_end_item_ebayapp
        sResult = {'rcode': '0', 'messages': ''}  # 初始状态
        opnum = 'ebayapp_complete_Item_%s_%s' % (timetime.now().strftime('%Y%m%d%H%M%S'), request.user.username)
        try:
            param = {}  # 操作日志的参数
            param['OpNum'] = opnum
            param['OpKey'] = objs.values_list("itemid", flat=True)
            param['OpType'] = 'endItem'
            param['Status'] = 'runing'
            param['ErrorInfo'] = ''
            param['OpPerson'] = request.user.username
            param['OpTime'] = timetime.now()
            param['OpStartTime'] = timetime.now()
            param['OpEndTime'] = None
            param['aNum'] = len(objs)
            param['rNum'] = 0
            param['eNum'] = 0

            iResult = t_wish_store_oplogs_obj.createLog(param)
            assert iResult['errorcode'] == 0, "insert log error."
            Completedparams = []
            for obj in objs:
                param = {}
                param['ItemID'] = obj.itemid
                # param['id'] = qs.id
                param['ShopName'] = obj.ShopName
                param['Site'] = obj.site
                param['Type'] = 'endItem'
                param['Operator'] = request.user.username
                param['OpNum'] = opnum
                Completedparams.append(param)
            relist_end_item_ebayapp(params=Completedparams)
            sResult['rcode'] = 1
            sResult['KEY'] = opnum
            sResult['messages'] = 'Now Start endItem !!!'
        except Exception, ex:
            sResult['rcode'] = -1
            sResult['messages'] = '%s:%s' % (Exception, ex)
        return HttpResponse(json.dumps(sResult))

    _batch_Completed_data_by_api.short_description = u'批量下架选中商品'

    def _batch_Active_data_by_api(self,request, objs):
        from app_djcelery.tasks import relist_end_item_ebayapp
        sResult = {'rcode': '0', 'messages': ''}  # 初始状态
        opnum = 'ebayapp_Active_Item_%s_%s' % (timetime.now().strftime('%Y%m%d%H%M%S'), request.user.username)
        try:
            param = {}  # 操作日志的参数
            param['OpNum'] = opnum
            param['OpKey'] = objs.values_list("itemid", flat=True)
            param['OpType'] = 'endItem'
            param['Status'] = 'runing'
            param['ErrorInfo'] = ''
            param['OpPerson'] = request.user.username
            param['OpTime'] = timetime.now()
            param['OpStartTime'] = timetime.now()
            param['OpEndTime'] = None
            param['aNum'] = len(objs)
            param['rNum'] = 0
            param['eNum'] = 0

            iResult = t_wish_store_oplogs_obj.createLog(param)
            assert iResult['errorcode'] == 0, "insert log error."
            Activeparams = []
            for obj in objs:
                param = {}
                param['ItemID'] = obj.itemid
                # param['id'] = qs.id
                param['ShopName'] = obj.ShopName
                param['Site'] = obj.site
                param['Type'] = 'relistItem'
                param['Operator'] = request.user.username
                param['OpNum'] = opnum
                Activeparams.append(param)
            # relist_end_item_ebayapp.delay(params=Completedparams)
            relist_end_item_ebayapp(params=Activeparams)
            sResult['rcode'] = 1
            sResult['KEY'] = opnum
            sResult['messages'] = 'Now Start endItem !!!'
        except Exception, ex:
            sResult['rcode'] = -1
            sResult['messages'] = '%s:%s' % (Exception, ex)
        return HttpResponse(json.dumps(sResult))
    _batch_Active_data_by_api.short_description = u'批量上架选中商品'

    def cexport_excel_item_information(self,request, queryset):
        sku_status = {u'1': u'正常', u'2': u'售完下架', u'3': u'临时下架', u'4': u'停售', u'': u'--', None: u'--'}
        try:
            from xlwt import *
            DOWNLOAD_KEY_WORDS = 'ebay_excel'

            path = MEDIA_ROOT + 'download_xls/' + request.user.username
            mkdir_p(MEDIA_ROOT + 'download_xls')
            os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))

            mkdir_p(path)
            os.popen('chmod 777 %s' % (path))

            w = Workbook()
            sheet = w.add_sheet('ebay_excel')

            sheet.write(0, 0, u'itemid')
            sheet.write(0, 1, u'商品SKU')
            sheet.write(0, 2, u'商品状态')
            sheet.write(0, 3, u'可用数量')
            sheet.write(0, 4, u'可售天数')
            sheet.write(0, 5, u'店铺SKU')
            sheet.write(0, 6, u'库存')
            sheet.write(0, 7, u'销量')
            sheet.write(0, 8, u'价格')

            # 写数据
            row = 0
            for qs in queryset:
                try:
                    t_online_info_ebay_subsku_objs = t_online_info_ebay_subsku.objects.filter(itemid=qs.itemid)
                    if len(t_online_info_ebay_subsku_objs) > 0:
                        # v_flag = 0
                        for t_online_info_ebay_subsku_obj in t_online_info_ebay_subsku_objs:
                            row += 1
                            column = 0
                            sheet.write(row, column, qs.itemid)
                            # if v_flag == 0:
                            #     sheet.write(row, column, qs.itemid)
                            #     v_flag  += 1
                            column += 1
                            sheet.write(row, column, t_online_info_ebay_subsku_obj.productsku if t_online_info_ebay_subsku_obj.productsku else '')
                            column += 1
                            try:
                                pgoodstatus = sku_status[t_online_info_ebay_subsku_obj.productstatus]
                            except:
                                pgoodstatus = u'--'
                            sheet.write(row, column, pgoodstatus)
                            column += 1
                            sheet.write(row, column, t_online_info_ebay_subsku_obj.UseNumber)
                            column += 1
                            sheet.write(row, column, t_online_info_ebay_subsku_obj.SaleDay)
                            column += 1
                            sheet.write(row, column, t_online_info_ebay_subsku_obj.subSKU)
                            column += 1
                            try:
                                available = int(t_online_info_ebay_subsku_obj.total) - int(t_online_info_ebay_subsku_obj.sold)
                            except:
                                available = 0
                            sheet.write(row, column, available if available else 0)
                            column += 1
                            sheet.write(row, column, t_online_info_ebay_subsku_obj.sold)
                            column += 1
                            sheet.write(row, column, t_online_info_ebay_subsku_obj.startprice)

                    else:
                        # messages.success(request,'asdhasjdgahgsdgasda')
                        row += 1
                        column = 0
                        sheet.write(row, column, qs.itemid)
                        column += 1
                        sheet.write(row, column, qs.Productsku)
                        column += 1
                        try:
                            pgoodstatus = sku_status[qs.Productstatus]
                        except:
                            pgoodstatus = u'--'
                        sheet.write(row, column, pgoodstatus)
                        column += 1
                        sheet.write(row, column, qs.UseNumber)
                        column += 1
                        sheet.write(row, column, qs.SaleDay)
                        column += 1
                        sheet.write(row, column, qs.SKU)
                        column += 1
                        sheet.write(row, column, qs.available)
                        column += 1
                        sheet.write(row, column, qs.sold)
                        column += 1
                        sheet.write(row, column, qs.currentprice)
                except Exception,ex:
                    messages.error(request,str(repr(ex)))
                    continue
            filename = request.user.username + '_' + timetime.now().strftime('%Y%m%d%H%M%S') + '.xls'
            w.save(path + '/' + filename)
            os.popen(r'chmod 777 %s' % (path + '/' + filename))

            # 上传oss对象
            auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
            bucket = oss2.Bucket(auth, ENDPOINT_OUT, BUCKETNAME_XLS)
            bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)
            # 删除现有的
            for object_info in oss2.ObjectIterator(bucket, prefix='%s/%s_' % (DOWNLOAD_KEY_WORDS, request.user.username)):
                bucket.delete_object(object_info.key)
            bucket.put_object(u'%s/%s' % (DOWNLOAD_KEY_WORDS, filename), open(path + '/' + filename))
            messages.success(request, u'%s%s.%s/%s/%s' % (PREFIX, BUCKETNAME_XLS, ENDPOINT_OUT, DOWNLOAD_KEY_WORDS, filename) + u':成功导出,可点击Download下载到本地............................。')
        except Exception,ex:
            messages.error(request, u'导出出错...。%s'%repr(ex))


    cexport_excel_item_information.short_description = u'导出商品信息EXCEL'

    def cexport_excel_item_information_shopee(self, objs):
        for obj in objs:
            pass

    cexport_excel_item_information_shopee.short_description = u'导出商品信息SHOPEE'


    def get_item_to_collection_box(self, request, objs):
        from brick.ebay.ebay_pulish.ebay_get_item import ebay_get_item
        success = list()
        failed = list()
        for obj in objs:
            item_id = obj.itemid
            shopname = obj.ShopName
            username = request.user.first_name
            try:
                storename = t_config_store_ebay.objects.get(ShopName=shopname).storeName
            except t_config_store_ebay.DoesNotExist:
                error_msg = "This ItemID %s ShopName: %s is not in t_config_store_ebay, Please connect with IT." % (item_id, shopname)
                messages.error(request, error_msg)
                break
            res = ebay_get_item(storename, item_id, username=username)
            if res['code'] == 0:
                success.append({'item_id': item_id})
            else:
                failed.append({'item_id': item_id, 'error': res['message']})

        ret_mess_ok = 'Success Number: %s, Success Info: %s' % (len(success), str(success))
        ret_mess_no = 'Failed Number: %s, Failed Info: %s' % (len(failed), str(failed))
        if success:
            messages.success(request, ret_mess_ok)
        elif failed:
            messages.error(request, ret_mess_no)
        else:
            messages.info(request, u'No item handle.')

    get_item_to_collection_box.short_description = u'获取商品信息至铺货采集箱'


    def get_itemID(self,type,skus):
        ItemID = []
        if len(skus) < 1:
            return ItemID
        skus_list = skus.split(',')
        if type == 'productsku':
            for sku in skus_list:
                sub_itemids = t_online_info_ebay_subsku.objects.filter(productsku=sku.strip()).values('itemid')
                if len(sub_itemids) > 0:
                    for sub_itemid in sub_itemids:
                        ItemID.append(sub_itemid['itemid'])
                p_itemids = t_online_info_ebay_listing.objects.filter(Productsku=sku.strip(),isVariations='NO').values('itemid')
                if len(p_itemids) > 0:
                    for p_itemid in p_itemids:
                        ItemID.append(p_itemid['itemid'])
        elif type == 'shopsku':
            for sku in skus_list:
                sub_itemids = t_online_info_ebay_subsku.objects.filter(subSKU=sku.strip()).values('itemid')
                if len(sub_itemids) > 0:
                    for sub_itemid in sub_itemids:
                        ItemID.append(sub_itemid['itemid'])
                p_itemids = t_online_info_ebay_listing.objects.filter(SKU=sku.strip(),isVariations='NO').values('itemid')
                if len(p_itemids) > 0:
                    for p_itemid in p_itemids:
                        ItemID.append(p_itemid['itemid'])
        return ItemID

    def getintersectionItemID(self,all_item_list):
        flag = 0
        if len(all_item_list) == 1:
            return all_item_list[0]
        elif len(all_item_list) == 0:
            return []
        for item_list in all_item_list:
            if len(item_list) > 0:
                pass
            else:
                flag = 1
        if flag == 1:
            return []
        else:
            all_item_list.append(list(set(all_item_list[0]).intersection(set(all_item_list[1]))))
            all_item_list.remove(all_item_list[0])
            all_item_list.remove(all_item_list[0])
            all_item_lists = self.getintersectionItemID(all_item_list)
            return all_item_lists


    def get_list_queryset(self,):
        request = self.request
        qs = super(t_online_info_ebay_listing_Admin, self).get_list_queryset()
        itemid = request.GET.get('itemid', '').strip()
        title = request.GET.get('title', '')
        ShopName = request.GET.get('ShopName', '')
        status = request.GET.get('status', '')
        skustatus = request.GET.get('skustatus','')
        Location = request.GET.get('Location','')
        seller = request.GET.get('seller', '')
        Published = request.GET.get('Published','')
        realavailableStart = request.GET.get('realavailableStart','')
        realavailableEnd = request.GET.get('realavailableEnd', '')
        # SKURefreshTimeStart = request.GET.get('SKURefreshTimeStart', '')
        # SKURefreshTimeEnd = request.GET.get('SKURefreshTimeEnd', '')
        orders7DaysStart = request.GET.get('orders7DaysStart', '')
        orders7DaysEnd = request.GET.get('orders7DaysEnd', '')
        soldStart = request.GET.get('soldStart', '')
        soldEnd = request.GET.get('soldEnd', '')
        starttimeStart = request.GET.get('starttimeStart', '')
        starttimeEnd = request.GET.get('starttimeEnd', '')
        # endtimeStart = request.GET.get('endtimeStart', '')
        # endtimeEnd = request.GET.get('endtimeEnd', '')
        ShopSKUS = request.GET.get('ShopSKU', '')
        dostatus = request.GET.get('dostatus','')
        productSKUs = request.GET.get('productSKU', '')
        lastRefreshTimeStart = request.GET.get('lastRefreshTimeStart', '')
        lastRefreshTimeEnd = request.GET.get('lastRefreshTimeEnd', '')
        watchCountStart = request.GET.get('watchCountStart', '')
        watchCountEnd = request.GET.get('watchCountEnd', '')
        Operator = request.GET.get('Operator', '')
        EXPRESS = request.GET.get('EXPRESS','')
        UseNumberStart = request.GET.get('UseNumberStart', '')
        UseNumberEnd = request.GET.get('UseNumberEnd', '')
        isVariations = request.GET.get('isVariations', '')
        psite = request.GET.get('psite', '')
        TortInfo = request.GET.get('TortInfo', '')

        rItemID = []
        if realavailableStart or realavailableEnd:
            if realavailableStart and realavailableEnd:
                rt_online_info_ebay_subsku_objs = t_online_info_ebay_subsku.objects.filter(realavailable__gte=int(realavailableStart),realavailable__lte=int(realavailableEnd)).values('itemid')
                rt_online_info_ebay_listing_objs = t_online_info_ebay_listing.objects.filter(realavailable__gte=int(realavailableStart), realavailable__lte=int(realavailableEnd),isVariations='NO').values('itemid')
            elif realavailableStart and not realavailableEnd:
                rt_online_info_ebay_subsku_objs = t_online_info_ebay_subsku.objects.filter(realavailable__gte=int(realavailableStart)).values('itemid')
                rt_online_info_ebay_listing_objs = t_online_info_ebay_listing.objects.filter(realavailable__gte=int(realavailableStart),isVariations='NO').values('itemid')
            elif not realavailableStart and realavailableEnd:
                rt_online_info_ebay_subsku_objs = t_online_info_ebay_subsku.objects.filter(realavailable__lte=int(realavailableEnd)).values('itemid')
                rt_online_info_ebay_listing_objs = t_online_info_ebay_listing.objects.filter(realavailable__lte=int(realavailableEnd),isVariations='NO').values('itemid')
            # messages.info(request, t_online_info_ebay_subsku_objs.query)
            # messages.info(request, t_online_info_ebay_listing_objs.query)
            if len(rt_online_info_ebay_subsku_objs) > 0:
                rItemID = [obj['itemid'] for obj in rt_online_info_ebay_subsku_objs] # 列表推导式
            if len(rt_online_info_ebay_listing_objs) > 0:
                r = [obj['itemid'] for obj in rt_online_info_ebay_listing_objs]
                rItemID.extend(r)
        # messages.success(self.request, rItemID)
        uItemID = []
        if UseNumberStart or UseNumberEnd:
            if UseNumberStart and UseNumberEnd:
                t_online_info_ebay_subsku_objs = t_online_info_ebay_subsku.objects.filter(UseNumber__gte=int(UseNumberStart),UseNumber__lte=int(UseNumberEnd)).values('itemid')
                t_online_info_ebay_listing_objs = t_online_info_ebay_listing.objects.filter( UseNumber__gte=int(UseNumberStart), UseNumber__lte=int(UseNumberEnd),isVariations='NO').values('itemid')
            elif UseNumberStart and not UseNumberEnd:
                t_online_info_ebay_subsku_objs = t_online_info_ebay_subsku.objects.filter(UseNumber__gte=int(UseNumberStart)).values('itemid')
                t_online_info_ebay_listing_objs = t_online_info_ebay_listing.objects.filter(UseNumber__gte=int(UseNumberStart),isVariations='NO').values('itemid')
            elif not UseNumberStart and UseNumberEnd:
                t_online_info_ebay_subsku_objs = t_online_info_ebay_subsku.objects.filter(UseNumber__lte=int(UseNumberEnd)).values('itemid')
                t_online_info_ebay_listing_objs = t_online_info_ebay_listing.objects.filter(UseNumber__lte=int(UseNumberEnd),isVariations='NO').values('itemid')
            # messages.info(request, t_online_info_ebay_subsku_objs.query)
            # messages.info(request, t_online_info_ebay_listing_objs.query)
            if len(t_online_info_ebay_subsku_objs) > 0:
                uItemID = [obj['itemid'] for obj in t_online_info_ebay_subsku_objs] # 列表推导式
            if len(t_online_info_ebay_listing_objs) > 0:
                x = [obj['itemid'] for obj in t_online_info_ebay_listing_objs]
                uItemID.extend(x)

        Shop_Name = []
        if seller:
            store_config = t_store_configuration_file.objects.filter(Seller=seller)
            for sc in store_config:
                store_ebay = t_config_store_ebay.objects.filter(ShopName=sc.ShopName)
                if store_ebay:
                    Shop_Name.append(store_ebay[0].storeName)
        if ShopName:
            Shop_Name.append(ShopName)

        shop_itemid = self.get_itemID(type='shopsku', skus=ShopSKUS)
        product_itemid = self.get_itemID(type='productsku',skus=productSKUs)
        sItemID = []
        if itemid:
            sItemID = itemid.split(',')

        searchList = { 'title__contains': title,
                      'status__exact': status,'Location__contains':Location,
                      'Published__exact':Published,'Operator__exact':Operator,
                      'Orders7Days__gte': orders7DaysStart, 'Orders7Days__lte': orders7DaysEnd,
                      'sold__gte': soldStart, 'sold__lte': soldEnd,
                      'starttime__gte': starttimeStart, 'starttime__lt': starttimeEnd,
                      'lastRefreshTime__gte': lastRefreshTimeStart, 'lastRefreshTime__lt': lastRefreshTimeEnd,
                      'watchCount__gte': watchCountStart, 'watchCount__lte': watchCountEnd,
                      'isVariations__exact':isVariations,'site__exact':psite,'TortInfo__exact':TortInfo,
                      # 'SKURefreshTime__gte': SKURefreshTimeStart, 'SKURefreshTime__lt': SKURefreshTimeEnd,
                      'dostatus__exact':dostatus,
                      }
        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    sl[k] = v
        skuItemID = []
        if skustatus:
            if skustatus == u'5':
                # messages.success(request,'sssssss')
                st_online_info_ebay_subsku_objs = t_online_info_ebay_subsku.objects.filter(productstatus=None).values('itemid')
                st_online_info_ebay_listing_objs = t_online_info_ebay_listing.objects.filter(Productstatus=None).values('itemid')
                if len(st_online_info_ebay_subsku_objs) > 0:
                    skuItemID = [obj['itemid'] for obj in st_online_info_ebay_subsku_objs] # 列表推导式
                if len(st_online_info_ebay_listing_objs) > 0:
                    x = [obj['itemid'] for obj in st_online_info_ebay_listing_objs]
                    skuItemID.extend(x)
                qs = qs.filter(itemid__in=skuItemID)
            else:
                qs = qs.filter(Productstatus__contains=skustatus)
        else:
            pass
        if itemid or ShopSKUS or productSKUs or realavailableStart or realavailableEnd or UseNumberStart or UseNumberEnd:
            all_item_list = []
            all_item_list.append(sItemID) if itemid else ''
            all_item_list.append(shop_itemid) if ShopSKUS else ''
            all_item_list.append(product_itemid) if productSKUs else ''
            all_item_list.append(rItemID) if realavailableStart or realavailableEnd else ''
            all_item_list.append(uItemID) if UseNumberStart or UseNumberEnd else ''
            # messages.success(request,all_item_list)
            # itemids = self.getintersectionItemID(all_item_list)
            fn = lambda x, y: list(set(x).intersection(set(y))) if isinstance(x, list) and isinstance(y, list) else 'error'
            fy = lambda x: x[0] if len(x) == 1 else [] if len(x) == 0 else reduce(fn, tuple(y for y in x))
            itemids = fy(all_item_list)
            if isinstance(itemids,list):
                qs = qs.filter(itemid__in=itemids)
        if len(Shop_Name) > 0:
            qs = qs.filter(ShopName__in=Shop_Name)

        ZSHWCL = ['Ottendorf-Okrilla','Rowland Heights,CA/Dayton,NJ','Rowland Heights, California',
                  'Dayton, New Jersey','Dandenong','Walsall','Leicestershire']
        if EXPRESS == 'CN':
            qs = qs.filter(Country='CN')
        elif EXPRESS == 'NCN':
            qs = qs.exclude(Country='CN')
            qs = qs.exclude(Location__in=ZSHWCL)
        elif EXPRESS == 'ZSHWC':
            qs = qs.exclude(Country='CN')
            qs = qs.filter(Location__in=ZSHWCL)
        else:
            pass
        if sl is not None:
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'Please enter the correct content!')
        return qs