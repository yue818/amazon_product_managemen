# -*- coding: utf-8 -*-
import datetime as pdttime
import errno
import json
import logging
import os
import sys
import urllib2
from bs4 import BeautifulSoup
from django.utils.safestring import mark_safe
from urllib2 import *
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field

from lxml import etree
from brick.aliexpress.ali_compirePrice import compirePrice
from brick.public.HTTP301_302_303_307_ERROR import urlopener
from brick.public.proxy import proxy
from skuapp.table.t_product_mainsku_sku import *
from skuapp.table.v_product_allsku import *
from skuapp.views import *
from brick.function.formatUrl import format_urls

WISH_URL    = 'wish.'
AMAZON_URL  = 'amazon.'
WWW1688_URL = '1688.'
EBAY_URL = 'ebay.'
ALIEXPRESS_URL = 'aliexpress.'
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5 (except OSError, exc: for Python <2.5)
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
            
class t_product_Admin(object):

    list_per_page=50
    #list_export =()
    list_display= ('id','MainSKU','DYTime','DYStaffName','show_SourcePicPath','Name2','Keywords','Keywords2','Pricerange','ShelveDay','OrdersLast7Days','JZLTime','JZLStaffName','show_SourcePicPath2','SpecialSell','SpecialRemark','show_urls',)
    #search_fields=('id','MainSKU','StaffID','Name2',)
    #list_display_links = None
    #readonly_fields = ('id',)
    #list_filter = ALL_FIELDS_TUPLE
    #list_filter = ('UpdateTime',
                    #'Weight',
                    #'Electrification','Powder','Liquid','Magnetism','Buyer',
                    #'Storehouse',
                    #'DYStaffName','KFStaffName','XJStaffName','JZLStaffName','PZStaffName','MGStaffName','LRStaffName','LargeCategory',
                    #'YNphoto',
                    #)
    #formfield_overrides ={
       # models.CharField: {'widget': TextInput(attrs={'size':'6'})},
        #models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':8})},
        #models.URLField:  {'widget': TextInput(attrs={'size':'6'})},
    #}
    search_fields = ('id','SKU','MainSKU','Keywords','Keywords2','StaffID','Name','Name2','Material',
                    'PlatformName','SourcePicRemark','SupplierID','SupplierArtNO','SupplierPColor','SupplierPDes',
                    'SourceURL','SupplierPUrl1','SupplierPUrl2',
                    'SpecialRemark','Remark' ,'InitialWord',
                    'Buyer','SupplierContact','Storehouse','Tags',
                    'possessMan2','LargeCategory','ReportName','ReportName2','PrepackMark',
                    'DYStaffName','DYSHStaffName','XJStaffName','KFStaffName','JZLStaffName',
                    'PZStaffName','MGStaffName','LRStaffName','YNphoto',
                    )
    fields =  ('id',)

    form_layout = (
        Fieldset(u'',
                       Row('id')

                )
                  )

    logger = logging.getLogger('sourceDns.webdns.views')

    def to_recycle(self, request, queryset):
        from datetime import datetime
        # messages.error(request,'-----%s'%self.model._meta.model_name)
        # messages.error(request,'-----%s'%self.model._meta.verbose_name)
        for querysetid in queryset.all():
            #下一步
            obj = t_product_recycle()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID = request.user.username
            obj.fromTDel = self.model._meta.verbose_name
            obj.save()
            end_t_product_oplog(request,querysetid.MainSKU,'DEL',querysetid.Name2,querysetid.id)

            t_product_mainsku_sku.objects.filter(pid=obj.id).delete()  # 删除主SKU下所有的子SKU属性
            querysetid.delete()
    to_recycle.short_description = u'扔进回收站'

    #colored_first_name.admin_order_field = '-first_name'
    def show_oplog(self,obj) :
        rt = ''
        t_product_oplog_objs = t_product_oplog.objects.filter(pid=obj.id).order_by('id')
        for t_product_oplog_obj in t_product_oplog_objs:
            rt = u'%s%s:%s,'%(rt,t_product_oplog_obj.StepName,t_product_oplog_obj.OpName)
        return rt
    show_oplog.short_description = u'操作历史'

    def show_SourcePicPath(self,obj) :
        rt =  '<img src="%s"  width="150" height="150"  alt = "%s"  title="%s"  />  '%(obj.SourcePicPath,obj.SourcePicPath,obj.SourcePicPath)
        return mark_safe(rt)

    show_SourcePicPath.short_description = u'调研图'

    def show_SourcePicPath2(self,obj) :
        rt =  '<img src="%s"  width="150" height="150"  alt = "%s"  title="%s"  />  '%(obj.SourcePicPath2,obj.SourcePicPath2,obj.SourcePicPath2)
        return mark_safe(rt)
    show_SourcePicPath2.short_description = u'供货商图'

    def show_skulist(self,obj) :
        from skuapp.table.B_PackInfo import B_PackInfo  
        rt = u'<table  style="text-align:center">' \
             u'<tr>' \
             u'<th style="text-align:center">子SKU-</th>' \
             u'<th style="text-align:center">属性-</th>' \
             u'<th style="text-align:center">单价-</th>' \
             u'<th style="text-align:center">克重-</th>' \
             u'<th style="text-align:center">包装规格-</th>' \
             u'<th style="text-align:center">内包装成本-</th>' \
             u'<th style="text-align:center">最小包装数-</th>' \
             u'<th style="text-align:center">服装类信息-</th>' \
             u'<th style="text-align:center">供应商链接</th>' \
             u'<th style="text-align:center">供应商货号</th>' \
             u'</tr>'
        t_product_mainsku_sku_objs = t_product_mainsku_sku.objects.filter(pid=obj.id).order_by('SKU')
        logger = logging.getLogger('sourceDns.webdns.views')    #刚才在setting.py中配置的logger
        for t_product_mainsku_sku_obj in t_product_mainsku_sku_objs:
            PackName =''
            CostPrice =0
            PackNID= t_product_mainsku_sku_obj.PackNID
            logger.error("PackNIDPackNIDPackNIDPackNIDPackNIDPackNID %s"%(PackNID))
            try:
                if PackNID > 0 :
                    B_PackInfo_obj = B_PackInfo.objects.get(id__exact = PackNID)
                    if B_PackInfo_obj is not None:
                        PackName =  B_PackInfo_obj.PackName
                        CostPrice = B_PackInfo_obj.CostPrice
            except Exception,ex:
                
                logger.error("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx %s =%s"%(Exception,ex))

            SupplierLink = t_product_mainsku_sku_obj.SupplierLink
            if not SupplierLink:
                SupplierLink = obj.SupplierPUrl1

            SupplierNum = t_product_mainsku_sku_obj.SupplierNum
            if not SupplierNum:
                SupplierNum = obj.SupplierArtNO
                
            rt =  u'%s <tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' \
                  u'<td><input value="%s" style="width: 100px;border:none;background-color:transparent;" type="text" readonly title="%s"/></td>' \
                  u'<td><input value="%s" style="width: 100px;border:none;background-color:transparent;" type="text" readonly title="%s"/></td>' \
                  u'</tr> '%\
                  (rt,t_product_mainsku_sku_obj.SKU,t_product_mainsku_sku_obj.SKUATTRS,t_product_mainsku_sku_obj.UnitPrice,
                   t_product_mainsku_sku_obj.Weight,PackName,CostPrice,t_product_mainsku_sku_obj.MinPackNum,
                   t_product_mainsku_sku_obj.DressInfo,SupplierLink,SupplierLink,SupplierNum,SupplierNum
                   )


        rt = '%s</table>'%rt
        return mark_safe(rt)
    show_skulist.short_description = mark_safe('<p align="center"> 子SKU信息</p>')

    # def show_urls(self,obj) :
    #     rt = ''
    #     v_product_allsku_objs = v_product_allsku.objects.filter(id=obj.id,MainSKU=obj.MainSKU)
    #     for v_product_allsku_obj in v_product_allsku_objs:
    #         rt = u'%s反向: %s<br>供货商: %s'%(rt,v_product_allsku_obj.SourceURL,v_product_allsku_obj.SupplierPUrl1)
    #     return mark_safe(rt)
    # show_urls.short_description = u'链接信息'
    def show_urls(self,obj) :
        Platform,linkurl = format_urls(obj.SourceURL if obj.SourceURL else '')
        if 'can not formate' in Platform:
            linkurl = 'reverse_url'

        Platform2, linkurl2 = format_urls(obj.SourceURL2 if obj.SourceURL2 else '')
        if 'can not formate' in Platform2:
            linkurl2 = 'reverse_url'

        pSupplier,pSupplierurl =format_urls(obj.SupplierPUrl1 if obj.SupplierPUrl1 else '')
        if 'can not formate' in pSupplier:
            pSupplierurl = 'Supplierurl'
        rt = u'反:<a href="%s" target="_blank" >%s:%s</a>' \
             u'<br>反2:<a href="%s" target="_blank" >%s:%s</a>' \
             u'<br>供:<a href="%s" target="_blank" >%s:%s</a>'%\
             (obj.SourceURL,Platform,linkurl,
              obj.SourceURL2, Platform2, linkurl2,
              obj.SupplierPUrl1,pSupplier,pSupplierurl)
        return mark_safe(rt)
    show_urls.short_description = u'链接信息'

    def save_select_pic(self, obj,pic):
        if pic is not None:
            auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
            bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_SV)
            bucket.put_object(u'%s/%s.jpg'%(obj.id,obj.id),pic)
            #保存图片
            obj.SourcePicPath =  u'%s%s.%s/%s/%s.jpg'%(PREFIX,BUCKETNAME_SV,ENDPOINT_OUT,obj.id,obj.id)
            obj.save()

    def format_urls(self,url):
        if url is None or url.strip()=='':
            return ''

        return_url = url
        #wish
        if url.find(WISH_URL)  >=0  :
            if url.find('=') >=0:
                PlatformPIDs = url.split(r'=')
                if len(PlatformPIDs) > 1 :
                    return_url = PlatformPIDs[-1]
                    return_url = 'wish.com/c/%s'%(return_url)
            return_url= return_url.replace('http://','').replace('https://','').replace('www.','').replace(' ','')
            return_url = 'https://www.%s'%(return_url)

        if url.find(AMAZON_URL)  >=0  :
            if url.find('?') >=0 :
                return_url = url.split(r'?')[0]
            return_url= return_url.replace('http://','').replace('https://','').replace('www.','').replace(' ','')
            return_url = 'https://www.%s'%(return_url)
            return return_url

        if  url.find(EBAY_URL)  >=0  :
            if url.find('?') >=0 :
                return_url = url.split(r'?')[0]
            return_url= return_url.replace('http://','').replace('https://','').replace('www.','').replace(' ','')
            return_url = 'https://www.%s'%(return_url)
            return return_url

        if  url.find(ALIEXPRESS_URL)  >=0  :
            if url.find('?') >=0 :
                return_url = url.split(r'?')[0]
            return_url= return_url.replace('http://','').replace('https://','').replace('www.','').replace(' ','')
            return_url = 'https://www.%s'%(return_url)
            return return_url

        if  url.find(WWW1688_URL)  >=0  :
            if  url.find('?') >=0 :
                return_url = url.split(r'?')[0]
            if  url.find('#') >=0 :
                return_url = url.split(r'#')[0]
            return_url= return_url.replace('http://','').replace('https://','').replace('www.','').replace(' ','')
            return_url = 'https://%s'%(return_url)
            return return_url

        return return_url

    def readWish(self,request,old_obj,obj):
        #判断新老url是否相等
        new_SourceURL = ''
        if obj is not None and obj.SourceURL is not None and obj.SourceURL.strip() !='':
            new_SourceURL = self.format_urls(obj.SourceURL)
        else:
            return

        old_SourceURL = ''
        if old_obj is not None and old_obj.SourceURL is not None and old_obj.SourceURL.strip() !='':
            old_SourceURL = self.format_urls(old_obj.SourceURL)

        if old_SourceURL.strip() == new_SourceURL.strip() and old_obj.SourcePicPath is not None and old_obj.SourcePicPath.strip() !='':
            #messages.error(request,'重复URL= %s   '%(new_SourceURL.strip()))
            return
        wishurls = new_SourceURL
        wishpicurls = None
        data_bytes = None
        jo = None

        #取网站数据

        opener = proxy.get_proxy()

        try:
            req = urllib2.Request(wishurls)
            data_bytes = opener.open(req, timeout = 30).read()
            #logger.error("workfunc_Wishworkfunc_Wishworkfunc_Wish 1111 obj = %s wishurls =%s"%(obj,wishurls))
            #self.message_user(request,data_bytes)
        except urllib2.HTTPError, e:
            messages.error(request,'反向链接读取错误.%s'%e.reason)
            return
        except urllib2.URLError, e:
            messages.error(request,'反向链接读取错误.%s'%e.reason)
            return
        if data_bytes is not None:
            data_bytes2 = data_bytes.split('pageParams')
            if data_bytes2 is not None and len(data_bytes2) > 2 and data_bytes2[2] is not None and len(data_bytes2[2]) > 25 :
                data_bytes3 =  data_bytes2[2][20:-2]
                jo = json.loads(data_bytes3)
            if jo:
                wishpicurls = jo['small_picture'].split('?')[0]
        #logger.error("workfunc_Wishworkfunc_Wishworkfunc_Wish 3333 obj = %s wishpicurls  =%s jo =%s"%(obj,wishpicurls,jo))
        #复制图片到本地
        if  wishpicurls is not None :
            try:
                req = urllib2.Request(wishpicurls)
                image_bytes = opener.open(req, timeout = 30).read()
                #logger.error("workfunc_Wishworkfunc_Wishworkfunc_Wish 4444 obj = %s wishpicurls =%s"%(obj,wishpicurls))
            except urllib2.HTTPError, e:
                messages.error(request,'反向链接数据获取错误，请选择手动上传图片或录入数据.%s'%e.reason)
                return
            except urllib2.URLError, e:
                messages.error(request,'反向链接数据获取错误，请选择手动上传图片或录入数据.%s'%e.reason)
                return
            if image_bytes is not None:
                    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
                    bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_SV)
                    bucket.put_object(u'%s/%s.jpg'%(obj.id,obj.id),image_bytes)
                    #保存图片
                    obj.SourcePicPath =  u'%s%s.%s/%s/%s.jpg'%(PREFIX,BUCKETNAME_SV,ENDPOINT_OUT,obj.id,obj.id)
                    obj.SourceURL = wishurls
                    #obj.SourceURL0 = wishurls
                    obj.save()
                    #logger.error('workfunc_Wishworkfunc_Wishworkfunc_Wish 5555 obj = %s obj.SourcePicPath = %s' %(obj,obj.SourcePicPath))
                    #self.message_user(request,u'采集图片ok！！图片地址[%s] '%(obj.SourcePicPath) )
        else:
            #logger.error('workfunc_Wishworkfunc_Wishworkfunc_Wish 6666 obj = %s jo = %s' %(obj,jo))
            #self.message_user(request,'url error! [%s]'%wishurls)
            return
        #logger.error('workfunc_Wishworkfunc_Wishworkfunc_Wish 7777 obj = %s jo = %s' %(obj,jo))
        if jo:
            #名称
            obj.Name = jo['name']

            #Keywords
            #obj.Keywords = jo['keywords']

            #TAGS
            obj.Tags = jo['keywords']
            #for tag in jo['tags']:
                #obj.Tags = u'%s %s'%(obj.Tags,tag['name'])
            #logger.error('workfunc_Wishworkfunc_Wishworkfunc_Wish 8888 obj.Tags = %s jo = %s' %(obj,obj.Tags))
            #ShelveDay 上架日期
            obj.ShelveDay = jo['generation_time'][0:10]

            #价格区间
            minprice = 999999
            maxprice = 0
            for variation in jo['commerce_product_info']['variations']:
                #self.message_user(request,u'original_price+original_shipping [%s,%s] '%(variation['original_price'],variation['original_shipping']) )
                tempprice = 0.0
                tempprice = variation['original_price'] + variation['original_shipping']
                if tempprice > maxprice:
                    maxprice = tempprice
                if tempprice < minprice:
                    minprice = tempprice
            obj.Pricerange = '[%s,%s]'%(minprice,maxprice)
            #购买量
            obj.NumBought = jo['num_bought']
            #WISH库存数
            obj.TotalInventory = jo['commerce_product_info']['total_inventory']
            #logger.error('workfunc_Wishworkfunc_Wishworkfunc_Wish 9999 obj = %s obj.Pricerange = %s' %(obj,obj.Pricerange))
            self.message_user(request,u'采集数据ok！！图片地址[%s] '%(obj.SourcePicPath) )
            obj.selectpic =''
            # obj.save()

    def readAmazon(self,request,old_obj,obj):
        #判断新老url是否相等
        new_SourceURL = ''
        if obj is not None and obj.SourceURL is not None and obj.SourceURL.strip() !='':
            new_SourceURL = self.format_urls(obj.SourceURL)
        else:
            return

        old_SourceURL = ''
        if old_obj is not None and old_obj.SourceURL is not None and old_obj.SourceURL.strip() !='':
            old_SourceURL = self.format_urls(old_obj.SourceURL)

        if old_SourceURL.strip() == new_SourceURL.strip() and old_obj.SourcePicPath is not None and old_obj.SourcePicPath.strip() !='':
            #messages.error(request,'重复URL= %s   '%(new_SourceURL.strip()))
            return

        amazonurls = new_SourceURL
        logger = logging.getLogger('sourceDns.webdns.views')    #刚才在setting.py中配置的logger
        logger.error("workfunc_Wishworkfunc_Wishworkfunc_Wish BEGIN obj = %s amazonurls =%s"%(obj,amazonurls))

        data_bytes = None

        opener = proxy.get_proxy()

        try:
            req = urllib2.Request(amazonurls)
            data_bytes = opener.open(req, timeout = 30).read()#.decode('gbk')
        except urllib2.HTTPError, e:
            messages.error(request,'反向链接读取错误1.%s'%e.reason)
            return
        except urllib2.URLError, e:
            messages.error(request,'反向链接读取错误.%s'%e.reason)
            return
        else:
            print "OK"

        if data_bytes is not None:
            soup = BeautifulSoup(data_bytes,"lxml")
            #图片
            if soup is None:
                return
            link_jpg = None

            try:
                link_jpg = dict(soup.html.find("div", id="imgTagWrapperId").find("img").attrs)['src']
                if link_jpg.endswith (('.jpg',)) == False:
                    link_jpg = dict(soup.html.find("div", id="imgTagWrapperId").find("img").attrs)['data-old-hires']
                req = urllib2.Request(link_jpg)
                image_bytes = opener.open(req, timeout = 30).read()
            except urllib2.HTTPError, e:
                messages.error(request,'反向链接数据获取错误，请选择手动上传图片或录入数据.%s'%e.reason)
                return
            except urllib2.URLError, e:
                messages.error(request,'反向链接数据获取错误，请选择手动上传图片或录入数据.%s'%e.reason)
                return
            if image_bytes is not None:
                auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
                bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_SV)
                bucket.put_object(u'%s/%s.jpg'%(obj.id,obj.id),image_bytes)
                #保存图片
                obj.SourcePicPath =  u'%s%s.%s/%s/%s.jpg'%(PREFIX,BUCKETNAME_SV,ENDPOINT_OUT,obj.id,obj.id)
                obj.SourceURL = amazonurls
                #obj.SourceURL0 = amazonurls
                obj.save()

    #1688调研图片
    def read1688(self,request, obj,url):
        #判断新老url是否相等
        #obj_original = self.model.objects.get(pk=obj.pk)
        #if obj_original.SourceURL == obj.SourceURL :
            #return
        self.logger.error("readAmazonreadAmazonreadAmazon")
        if url is None or url.strip() =='':
            return
        #self.logger.error("SourceURL0SourceURL0SourceURL0 =%s %s "%(obj.SourceURL0,obj.SourceURL))
        #去掉？后面的
        urlNew = url
        if url is not None and url.find('?') >=0 :
            urlNew = url.split(r'?')[0]

        www1688urls = urlNew

        data_bytes = None
        opener = proxy.get_proxy()

        #取网站数据
        try:
            #data_bytes = urllib2.urlopen(www1688urls, timeout = 10).read().decode('gbk')
            req = urllib2.Request(www1688urls)
            data_bytes = opener.open(req, timeout = 30).read().decode('gbk')
        except urllib2.HTTPError, e:
            messages.error(request,'供货商商品链接一读取错误.%s'%e.reason)
            return
        except urllib2.URLError, e:
            messages.error(request,'供货商商品链接一读取错误.%s'%e.reason)
            return
        if data_bytes is not None:
            soup = BeautifulSoup(data_bytes,"lxml")
            #file_object = open('thefile.txt', 'w')
            #file_object.write(soup.prettify())
            #file_object.close( )
            #供应商名称             #<a class="chinaname " href="https://hsfwcs.1688.com" style="color: ; font-family: 黑体; font-size: 30px;  ">  义乌市温略电子商务商行   </a>
            SupplierID = soup.html.find("a", attrs={'href':'#','class':'company-name'})
            #SupplierID = soup.html.find("a", class_="chinaname hidden")
            if SupplierID is not None:
                obj.SupplierID = SupplierID.string
                if obj.SupplierID is not None:
                    obj.SupplierID = obj.SupplierID.strip()
            #SupplierPDes 供货商商品标题
            obj.SupplierPDes = u'%s'%(dict(soup.html.find("a", class_="box-img").find("img").attrs)['alt'])
            #图片
            link_jpg = dict(soup.html.find("a", class_="box-img").find("img").attrs)['src']
            if link_jpg is not None:
                try:
                    req = urllib2.Request(link_jpg)
                    image_bytes = opener.open(req, timeout = 30).read()
                except urllib2.HTTPError, e:
                    messages.error(request,'供货商商品链接一数据获取错误，请选择手动上传图片或录入数据.%s'%e.reason)
                    return
                except urllib2.URLError, e:
                    messages.error(request,'供货商商品链接一数据获取错误，请选择手动上传图片或录入数据.%s'%e.reason)
                    return
                if image_bytes is not None:
                    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
                    bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_SV)
                    bucket.put_object(u'%s/%s.jpg'%(obj.id,obj.id),image_bytes)
                    #保存图片
                    obj.SourcePicPath =  u'%s%s.%s/%s/%s.jpg'%(PREFIX,BUCKETNAME_SV,ENDPOINT_OUT,obj.id,obj.id)
                    obj.SourceURL = www1688urls
                    #obj.SourceURL0 = www1688urls
                    obj.save()
    #供应商图片
    def read1688_2(self,request,old_obj,obj):
       #判断新老url是否相等
        new_SourceURL = ''
        if obj is not None and obj.SupplierPUrl1 is not None and obj.SupplierPUrl1.strip() !='':
            new_SourceURL = self.format_urls(obj.SupplierPUrl1)
        else:
            return
        old_SourceURL = ''
        if old_obj is not None and old_obj.SupplierPUrl1 is not None and old_obj.SupplierPUrl1.strip() !='':
            old_SourceURL = self.format_urls(old_obj.SupplierPUrl1)
        if old_SourceURL.strip() == new_SourceURL.strip() and old_obj.SourcePicPath2 is not None and old_obj.SourcePicPath2.strip() !='':
            #messages.error(request,'重复供应商URL= %s   '%(new_SourceURL.strip()))
            return
        data_bytes = None
        opener = proxy.get_proxy()
        #取网站数据
        try:
            # req = urllib2.Request(www1688urls)
            # data_bytes = opener.open(req, timeout = 30).read().decode('gbk')
            urllib2.install_opener(urlopener)
            req = urllib2.Request(new_SourceURL)
            data_bytes = urllib2.urlopen(req, timeout=30).read().decode('gbk')
        except urllib2.HTTPError, e:
            messages.error(request,'供货商商品链接二读取错误1.%s'%e.reason)
            return
        except urllib2.URLError, e:
            messages.error(request,'供货商商品链接二读取错误.%s'%e.reason)
            return
        except :
            messages.error(request,'获取网页链接数据失败！%s  '%new_SourceURL)
            return
        if data_bytes is not None:
            link_jpg =None
            soup = BeautifulSoup(data_bytes,"lxml")
            try:
                SupplierID = soup.html.find("a", attrs={'href':'#','class':'company-name'})
                if SupplierID is not None:
                    obj.SupplierID = SupplierID.string
                    if obj.SupplierID is not None:
                        obj.SupplierID = obj.SupplierID.strip()
                #SupplierPDes 供货商商品标题
                obj.SupplierPDes = u'%s'%(dict(soup.html.find("a", class_="box-img").find("img").attrs)['alt'])
                obj.Keywords2 = obj.SupplierPDes
                #图片
                link_jpg = dict(soup.html.find("a", class_="box-img").find("img").attrs)['src']
            except Exception,ex:
               messages.error(request,'提取数据失败 . %s : %s'%(Exception,ex))

            if link_jpg is not None:
                try:
                    req = urllib2.Request(link_jpg)
                    image_bytes = opener.open(req, timeout = 30).read()
                except urllib2.HTTPError, e:
                    messages.error(request,'供货商商品链接二数据获取错误，请选择手动上传图片或录入数据.%s'%e.reason)
                    return
                except urllib2.URLError, e:
                    messages.error(request,'供货商商品链接二数据获取错误，请选择手动上传图片或录入数据.%s'%e.reason)
                    return
                if image_bytes is not None:
                    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
                    bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_1688)
                    bucket.put_object(u'%s/%s.jpg'%(obj.id,obj.id),image_bytes)
                    #保存图片
                    obj.SourcePicPath2 =  u'%s%s.%s/%s/%s.jpg'%(PREFIX,BUCKETNAME_1688,ENDPOINT_OUT,obj.id,obj.id )
                    obj.SupplierPUrl1 = new_SourceURL
                    obj.save()
            else:
                messages.error(request, u'图片读取失败。。。')


    def readeBay(self,request,old_obj,obj):
        #判断新老url是否相等
        new_SourceURL = ''
        if obj is not None and obj.SourceURL is not None and obj.SourceURL.strip() !='':
            new_SourceURL = self.format_urls(obj.SourceURL)
        else:
            return
        old_SourceURL = ''
        if old_obj is not None and old_obj.SourceURL is not None and old_obj.SourceURL.strip() !='':
            old_SourceURL = self.format_urls(old_obj.SourceURL)
        if old_SourceURL.strip() == new_SourceURL.strip() and old_obj.SourcePicPath is not None and old_obj.SourcePicPath.strip() !='':
            #messages.error(request,'重复URL= %s   '%(new_SourceURL.strip()))
            return
        eBayurls = new_SourceURL
        logger = logging.getLogger('sourceDns.webdns.views')    #刚才在setting.py中配置的logger
        logger.error("workfunc_Wishworkfunc_Wishworkfunc_Wish BEGIN obj = %s eBayurls =%s"%(obj,eBayurls))
        data_bytes = None
        opener = proxy.get_proxy()
        try:
            req = urllib2.Request(eBayurls)
            data_bytes = opener.open(req, timeout = 30).read()#.decode('gbk')
        except urllib2.HTTPError, e:
            messages.error(request,'反向链接读取错误.%s'%e.reason)
            return
        except urllib2.URLError, e:
            messages.error(request,'反向链接读取错误.%s'%e.reason)
            return
        if data_bytes is not None:
            html = etree.HTML(data_bytes)
            keywords = '%s'%html.xpath('//*[@id="itemTitle"]/text()')
            obj.Keywords = keywords[2:-2]

            soup = BeautifulSoup(data_bytes,"lxml")
            #图片
            image_bytes =None
            try:
                link_jpg = dict(soup.find("div", id="vi_main_img_fs").find("td",class_="tdThumb").find("img").attrs)['src']
                req = urllib2.Request(link_jpg)
                image_bytes = opener.open(req, timeout = 30).read()
            except urllib2.HTTPError, e:
                messages.error(request,'反向链接数据获取错误，请选择手动上传图片或录入数据.%s'%e.reason)
                return
            except urllib2.URLError, e:
                messages.error(request,'反向链接数据获取错误，请选择手动上传图片或录入数据.%s'%e.reason)
                return
            if image_bytes is not None:
                auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
                bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_SV)
                bucket.put_object(u'%s/%s.jpg'%(obj.id,obj.id),image_bytes)
                #保存图片
                obj.SourcePicPath =  u'%s%s.%s/%s/%s.jpg'%(PREFIX,BUCKETNAME_SV,ENDPOINT_OUT,obj.id,obj.id)
                obj.SourceURL = eBayurls
                #obj.SourceURL0 = eBayurls
                #obj.save()
            self.read_ebay_detail(soup,obj)

    def read_ebay_detail(self,soup,obj):
        details_bytes = None
        detailsurl = ''
        for atemp in soup.find_all('a'):
            detailsurl = atemp.get('href','')
            urlstring = ('%s'%atemp.string).split(' ')
            if urlstring[-1] == 'sold' and detailsurl.find('http://') == 0:
                break
        if detailsurl:
            try:
                detreq = urllib2.Request(detailsurl)
                details_bytes = proxy.get_proxy().open(detreq, timeout=60).read()
            except urllib2.HTTPError, e:
                messages.error(request, '反向链接数据获取错误，请选择手动上传图片或录入数据.%s' % e.reason)
                return
            except urllib2.URLError, e:
                messages.error(request, '反向链接数据获取错误，请选择手动上传图片或录入数据.%s' % e.reason)
                return
        pirce_list = []
        time_list = []
        if details_bytes:
            soup_details = BeautifulSoup(details_bytes, "lxml")
            rows_table = soup_details.find('table',width="100%",border="0",cellspacing="0",cellpadding="5").find_all('tr')
            for i,row in enumerate(rows_table):
                if i == 0:
                    continue
                pricetmp = None
                timetmp = None
                for col in  row.find_all('td'):
                    # for pricecode in ['US $','C $','£ ',' EUR','AU $']: # 币种 'GBP ',
                    if ('%s'%col.string).startswith('US $') or ('%s'%col.string).startswith('C $') or \
                            ('%s'%col.string).startswith('£ ') or ('%s'%col.string).startswith('GBP') or \
                            ('%s' % col.string).startswith('AU $') or ('%s' % col.string).endswith(' EUR'):
                        pricetmp = col.string.replace('&nbsp;',' ')
                        # raise Exception(pricetmp)
                    if ('%s'%col.string).find(':') != -1:
                        timetmp = col.string
                if pricetmp:
                    pirce_list.append(pricetmp)
                if timetmp:
                    zone = timetmp.split(' ')[-1]
                    strdate = (pdttime.datetime.strptime(timetmp, '%b-%d-%y %H:%M:%S ' + zone) + pdttime.timedelta(hours=15)).strftime('%Y-%m-%d %H:%M:%S')
                    time_list.append(strdate)
        # 价格区间
        if pirce_list:
            minprice = min(pirce_list)
            maxprice = max(pirce_list)
            if minprice == maxprice:
                obj.Pricerange = '[%s]'%minprice
            else:
                obj.Pricerange = ('[%s,%s]' % (minprice, maxprice)).replace(' ','')
        # 7天order数量
        sorder = 0
        for mtime in time_list:
            if mtime >= (pdttime.datetime.now() + pdttime.timedelta(days=-15)).strftime('%Y-%m-%d %H:%M:%S'):
                sorder += 1
        obj.OrdersLast7Days = sorder
        # obj.save()

    def readAliexpress(self,request,old_obj,obj):
        #判断新老url是否相等
        new_SourceURL = ''
        if obj is not None and obj.SourceURL is not None and obj.SourceURL.strip() !='':
            new_SourceURL = self.format_urls(obj.SourceURL)
        else:
            return
        old_SourceURL = ''
        if old_obj is not None and old_obj.SourceURL is not None and old_obj.SourceURL.strip() !='':
            old_SourceURL = self.format_urls(old_obj.SourceURL)
        if old_SourceURL.strip() == new_SourceURL.strip() and old_obj.SourcePicPath is not None and old_obj.SourcePicPath.strip() !='':
            return
        aliexpressurls = new_SourceURL
        logger = logging.getLogger('sourceDns.webdns.views')    #刚才在setting.py中配置的logger
        logger.error("workfunc_Wishworkfunc_Wishworkfunc_Wish BEGIN obj = %s aliexpressurls =%s"%(obj,aliexpressurls))
        data_bytes = None
        opener = proxy.get_proxy()
        try:
            req = urllib2.Request(aliexpressurls)
            data_bytes = opener.open(req, timeout = 30).read()#.decode('gbk')
        except urllib2.HTTPError, e:
            messages.error(request,'反向链接读取错误.%s'%e.reason)
            return
        except urllib2.URLError, e:
            messages.error(request,'反向链接读取错误.%s'%e.reason)
            return
        if data_bytes is not None:
            html = etree.HTML(data_bytes)
            keywords = '%s'%html.xpath('//*[@id="j-product-detail-bd"]/div[1]/div/h1/text()')
            obj.Keywords = keywords[2:-2]

            soup = BeautifulSoup(data_bytes,"lxml")
            #图片
            if soup is None:
                return
            try:
                link_jpg = dict(soup.find("ul", id="j-image-thumb-list").find("img").attrs)['src']
                req = urllib2.Request(link_jpg)
                image_bytes = opener.open(req, timeout = 30).read()
            except urllib2.HTTPError, e:
                messages.error(request,'反向链接数据获取错误，请选择手动上传图片或录入数据.%s'%e.reason)
                return
            except urllib2.URLError, e:
                messages.error(request,'反向链接数据获取错误，请选择手动上传图片或录入数据.%s'%e.reason)
                return
            if image_bytes is not None:
                auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
                bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_SV)
                bucket.put_object(u'%s/%s.jpg'%(obj.id,obj.id),image_bytes)
                #保存图片
                obj.SourcePicPath =  u'%s%s.%s/%s/%s.jpg'%(PREFIX,BUCKETNAME_SV,ENDPOINT_OUT,obj.id,obj.id)
                obj.SourceURL = aliexpressurls
                #obj.SourceURL0 = aliexpressurls
                # obj.save()
            self.read_Aliexpress_detail(aliexpressurls,obj)

    def read_Aliexpress_detail(self,aliurl,obj):
        product_id = compirePrice.getIdFromUrl(aliurl)
        obj.Pricerange = compirePrice.getPriceSection(product_id)
        obj.OrdersLast7Days = compirePrice.getTheResultnum(product_id)
        # obj.save()

    def get_id(self):
        t_product_survey_ing_obj = t_product_survey_ing()
        t_product_survey_ing_obj.save()
        temp_id=t_product_survey_ing_obj.id
        t_product_survey_ing_obj.delete()
        return temp_id

