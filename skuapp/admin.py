# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)
from django.contrib import admin
from django.core import serializers
from django.db import transaction,connection
# Register your models here.

from skuapp.models import *
from skuapp.forms import *
from skuapp.views import *
import json

import logging
import django.utils.log
import logging.handlers
from Project.settings import *
import os,errno,sys
#def decode(info):
#      return info.decode('utf-8')
from datetime import datetime

import re
import math
from django.utils.timezone import utc
import oss2
from urllib2 import *
import urllib2
import socket
socket.setdefaulttimeout(10.0)
from bs4 import BeautifulSoup

from django.forms import TextInput, Textarea
import copy
from multiprocessing import Process,cpu_count
import multiprocessing
from django.utils.safestring import mark_safe

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
    StepID = 'QT'
    StepName = u'其他'

    list_display= ('id','CreateTime','CreateStaffName','SourcePicPath2','MainSKU','show_skulist','Name2','Material','SpecialSell','StaffID','show_oplog',)
    search_fields=('id','MainSKU','StaffID','Name2',)

    formfield_overrides ={
        models.CharField: {'widget': TextInput(attrs={'size':'6'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':8})},
        models.URLField:  {'widget': TextInput(attrs={'size':'6'})},
    }

    logger = logging.getLogger('sourceDns.webdns.views')

    def to_recycle(self, request, queryset):
        for querysetid in queryset.all():
            #下一步
            obj = t_product_recycle()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID = request.user.username
            obj.save()
            end_t_product_oplog(request,querysetid.MainSKU,'DEL',querysetid.Name2,querysetid.id)
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


class t_product_survey_ing_Admin(t_product_Admin):
    StepID = 'DY'
    StepName = u'调研'
    actions =  ['survey_ed_to_self','survey_ed', 'show_pic','to_recycle',]

    #save_on_top =True


    def survey_ed_to_self(self, request, queryset):
        for querysetid in queryset.all():
            obj = t_product_develop_ing()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID = request.user.username
            obj.save()


            #记录操作历史
            #end_oplog(request,querysetid,self)
            end_t_product_oplog(request,querysetid.MainSKU,'DY',querysetid.Name2,querysetid.id)
            begin_t_product_oplog(request,querysetid.MainSKU,'KF',querysetid.Name2,querysetid.id)

            #记录调研历史
            t_product_survey_history_obj = t_product_survey_history(SourcePicPath=querysetid.SourcePicPath,SourceURL=querysetid.SourceURL,StaffID=request.user.username,StaffName=request.user.first_name,pid=querysetid.id)
            t_product_survey_history_obj.save()

            querysetid.delete()
    survey_ed_to_self.short_description = u'调研完成直接开发'

    def survey_ed(self, request, queryset):
        for querysetid in queryset.all():
            #下一步
            obj = t_product_survey_ed()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name
            obj.save()

            #记录操作历史
            #end_oplog(request,querysetid,self)
            end_t_product_oplog(request,querysetid.MainSKU,'DY',querysetid.Name2,querysetid.id)
            begin_t_product_oplog(request,querysetid.MainSKU,'DYSH',querysetid.Name2,querysetid.id)
            #记录调研历史
            t_product_survey_history_obj = t_product_survey_history(SourcePicPath=querysetid.SourcePicPath,SourceURL=querysetid.SourceURL,StaffID=request.user.username,StaffName=request.user.first_name,pid=querysetid.id)
            t_product_survey_history_obj.save()

            querysetid.delete()
    survey_ed.short_description = u'调研完成去审核'



    #forms = t_product_survey_ing_Form
    list_display=('id','SourcePicPath','selectpic','SourceURL','OrdersLast7Days','Pricerange','ShelveDay','Keywords','Keywords2','SpecialRemark','show_oplog',)#,'TotalInventory','SpecialRemark',)   #指定要显示的字段
    list_display_links=('SourcePicPath',)
    list_editable=('selectpic','SourceURL','OrdersLast7Days','Keywords','Keywords2','SpecialRemark','ShelveDay','Pricerange',)
    search_fields=('id','StaffID','Keywords','Keywords2')





    def save_select_pic(self, obj,pic):
        if pic is not None:
            auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
            bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_SV)
            bucket.put_object(u'%s/%s.jpg'%(obj.id,obj.id),pic)
            #保存图片
            obj.SourcePicPath =  u'%s%s.%s/%s/%s.jpg'%(PREFIX,BUCKETNAME_SV,ENDPOINT_OUT,obj.id,obj.id)
            obj.save()

    def readWish(self,request, obj,url):
        self.logger.error("readWishreadWishreadWishreadWish")
        if url is None or url.strip() =='':
            return
        self.logger.error("SourceURL0SourceURL0SourceURL0 =%s %s "%(obj.SourceURL0,obj.SourceURL))

        urlNew = url
        if url is not None and url.find('=') >=0 :
            PlatformPID = url.split(r'=')
            if len(PlatformPID) > 1 :
                urlNew = PlatformPID[-1]
                urlNew = 'https://www.wish.com/c/%s'%(urlNew)
        wishurls = urlNew
        logger = logging.getLogger('sourceDns.webdns.views')    #刚才在setting.py中配置的logger
        logger.error("workfunc_Wishworkfunc_Wishworkfunc_Wish BEGIN obj = %s wishurls =%s"%(obj,wishurls))
        wishpicurls = None
        data_bytes = None
        jo = None
        if wishurls is None:
            return
        #取网站数据

        try:
            req = urllib2.Request(wishurls)
            data_bytes = urllib2.urlopen(req, timeout = 15).read()
            logger.error("workfunc_Wishworkfunc_Wishworkfunc_Wish 1111 obj = %s wishurls =%s"%(obj,wishurls))
            #self.message_user(request,data_bytes)
        except urllib2.URLError, e:
            #self.message_user(request,e.reason)
            logger.error("workfunc_Wishworkfunc_Wishworkfunc_Wish 2222 obj = %s wishurls =%s"%(obj,wishurls))
            return
        if data_bytes is not None:
            data_bytes2 = data_bytes.split('pageParams')
            if data_bytes2 is not None and len(data_bytes2) > 2 and data_bytes2[2] is not None and len(data_bytes2[2]) > 25 :
                data_bytes3 =  data_bytes2[2][20:-2]
                jo = json.loads(data_bytes3)
            if jo:
                wishpicurls = jo['small_picture'].split('?')[0]
        logger.error("workfunc_Wishworkfunc_Wishworkfunc_Wish 3333 obj = %s wishpicurls  =%s jo =%s"%(obj,wishpicurls,jo))
        #复制图片到本地
        if  wishpicurls is not None :
            try:
                req = urllib2.Request(wishpicurls)
                image_bytes = urllib2.urlopen(req, timeout = 15).read()
                logger.error("workfunc_Wishworkfunc_Wishworkfunc_Wish 4444 obj = %s wishpicurls =%s"%(obj,wishpicurls))
            except urllib2.URLError, e:
                #self.message_user(request,e.reason)
                return
            if image_bytes is not None:
                    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
                    bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_SV)
                    bucket.put_object(u'%s/%s.jpg'%(obj.id,obj.id),image_bytes)
                    #保存图片
                    obj.SourcePicPath =  u'%s%s.%s/%s/%s.jpg'%(PREFIX,BUCKETNAME_SV,ENDPOINT_OUT,obj.id,obj.id)
                    obj.SourceURL = wishurls
                    obj.SourceURL0 = wishurls
                    obj.save()
                    logger.error('workfunc_Wishworkfunc_Wishworkfunc_Wish 5555 obj = %s obj.SourcePicPath = %s' %(obj,obj.SourcePicPath))
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
            logger.error('workfunc_Wishworkfunc_Wishworkfunc_Wish 8888 obj.Tags = %s jo = %s' %(obj,obj.Tags))
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
            logger.error('workfunc_Wishworkfunc_Wishworkfunc_Wish 9999 obj = %s obj.Pricerange = %s' %(obj,obj.Pricerange))
            #self.message_user(request,u'采集数据ok！！图片地址[%s] '%(obj.SourcePicPath) )
            obj.selectpic =''
            obj.save()
            #processes = multiprocessing.Process(target=workfunc_Wish,args=(request, obj,urlNew))
            #processes.start()
            #processes.join()

    def readAmazon(self,request, obj,url):
        self.logger.error("readAmazonreadAmazonreadAmazon")
        if url is None or url.strip() =='':
            return
        self.logger.error("SourceURL0SourceURL0SourceURL0 =%s %s "%(obj.SourceURL0,obj.SourceURL))
        #去掉？后面的
        urlNew = url
        if url is not None and url.find('?') >=0 :
            urlNew = url.split(r'?')[0]

        amazonurls = urlNew
        logger = logging.getLogger('sourceDns.webdns.views')    #刚才在setting.py中配置的logger
        logger.error("workfunc_Wishworkfunc_Wishworkfunc_Wish BEGIN obj = %s amazonurls =%s"%(obj,amazonurls))

        data_bytes = None

        try:
            req = urllib2.Request(amazonurls)
            data_bytes = urllib2.urlopen(req, timeout = 15).read()#.decode('gbk')
        except urllib2.HTTPError, e:
            print e.code
        except urllib2.URLError, e:
            #self.message_user(request,e.reason)
            print e.reason
            print urllib2.URLError
            return
        else:
            print "OK"

        if data_bytes is not None:
            soup = BeautifulSoup(data_bytes,"lxml")
            #图片
            if soup is None:
                return

            link_jpg = dict(soup.html.find("div", id="imgTagWrapperId").find("img").attrs)['src']
            if link_jpg.endswith (('.jpg',)) == False:
                link_jpg = dict(soup.html.find("div", id="imgTagWrapperId").find("img").attrs)['data-old-hires']
            print link_jpg

            try:
                req = urllib2.Request(link_jpg)
                image_bytes = urllib2.urlopen(req, timeout = 15).read()
            except urllib2.HTTPError, e:
                print e.code
            except urllib2.URLError, e:
                #self.message_user(request,e.reason)
                print e.reason
                print urllib2.URLError
                return
            if image_bytes is not None:
                auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
                bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_SV)
                bucket.put_object(u'%s/%s.jpg'%(obj.id,obj.id),image_bytes)
                #保存图片
                obj.SourcePicPath =  u'%s%s.%s/%s/%s.jpg'%(PREFIX,BUCKETNAME_SV,ENDPOINT_OUT,obj.id,obj.id)
                obj.SourceURL = amazonurls
                obj.SourceURL0 = amazonurls
                obj.save()

    def read1688(self,request, obj,url):
        self.logger.error("readAmazonreadAmazonreadAmazon")
        if url is None or url.strip() =='':
            return
        self.logger.error("SourceURL0SourceURL0SourceURL0 =%s %s "%(obj.SourceURL0,obj.SourceURL))
        #去掉？后面的
        urlNew = url
        if url is not None and url.find('?') >=0 :
            urlNew = url.split(r'?')[0]

        www1688urls = urlNew

        data_bytes = None

        #取网站数据
        try:
            #data_bytes = urllib2.urlopen(www1688urls, timeout = 10).read().decode('gbk')
            req = urllib2.Request(www1688urls)
            data_bytes = urllib2.urlopen(req, timeout = 15).read().decode('gbk')
        except urllib2.HTTPError, e:
            self.message_user(request,e.reason)
            return
        except urllib2.URLError, e:
            self.message_user(request,e.reason)
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
                    image_bytes = urllib2.urlopen(req, timeout = 15).read()
                except urllib2.HTTPError, e:
                    print e.code
                except urllib2.URLError, e:
                    #self.message_user(request,e.reason)
                    print e.reason
                    print urllib2.URLError
                if image_bytes is not None:
                    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
                    bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_SV)
                    bucket.put_object(u'%s/%s.jpg'%(obj.id,obj.id),image_bytes)
                    #保存图片
                    obj.SourcePicPath =  u'%s%s.%s/%s/%s.jpg'%(PREFIX,BUCKETNAME_SV,ENDPOINT_OUT,obj.id,obj.id)
                    obj.SourceURL = www1688urls
                    obj.SourceURL0 = www1688urls
                    obj.save()

    def readeBay(self,request, obj,url):
        self.logger.error("readAmazonreadAmazonreadAmazon")
        if url is None or url.strip() =='':
            return
        self.logger.error("SourceURL0SourceURL0SourceURL0 =%s %s "%(obj.SourceURL0,obj.SourceURL))
        #去掉？后面的
        urlNew = url
        if url is not None and url.find('?') >=0 :
            urlNew = url.split(r'?')[0]

        eBayurls = urlNew
        logger = logging.getLogger('sourceDns.webdns.views')    #刚才在setting.py中配置的logger
        logger.error("workfunc_Wishworkfunc_Wishworkfunc_Wish BEGIN obj = %s eBayurls =%s"%(obj,eBayurls))

        data_bytes = None

        try:
            req = urllib2.Request(eBayurls)
            data_bytes = urllib2.urlopen(req, timeout = 15).read()#.decode('gbk')
        except urllib2.HTTPError, e:
            print e.code
        except urllib2.URLError, e:
            #self.message_user(request,e.reason)
            print e.reason
            print urllib2.URLError
            return
        else:
            print "OK"

        if data_bytes is not None:
            soup = BeautifulSoup(data_bytes,"lxml")
            #图片
            if soup is None:
                return

            link_jpg = dict(soup.find("div", id="vi_main_img_fs").find("td",class_="tdThumb").find("img").attrs)['src']

            if link_jpg is None:
                return
            try:
                req = urllib2.Request(link_jpg)
                image_bytes = urllib2.urlopen(req, timeout = 15).read()
            except urllib2.HTTPError, e:
                print e.code
            except urllib2.URLError, e:
                #self.message_user(request,e.reason)
                print e.reason
                print urllib2.URLError
                return
            if image_bytes is not None:
                auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
                bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_SV)
                bucket.put_object(u'%s/%s.jpg'%(obj.id,obj.id),image_bytes)
                #保存图片
                obj.SourcePicPath =  u'%s%s.%s/%s/%s.jpg'%(PREFIX,BUCKETNAME_SV,ENDPOINT_OUT,obj.id,obj.id)
                obj.SourceURL = eBayurls
                obj.SourceURL0 = eBayurls
                obj.save()

    def readAliexpress(self,request, obj,url):
        self.logger.error("readAmazonreadAmazonreadAmazon")
        if url is None or url.strip() =='':
            return
        self.logger.error("SourceURL0SourceURL0SourceURL0 =%s %s "%(obj.SourceURL0,obj.SourceURL))
        #去掉？后面的
        urlNew = url
        if url is not None and url.find('?') >=0 :
            urlNew = url.split(r'?')[0]

        aliexpressurls = urlNew
        logger = logging.getLogger('sourceDns.webdns.views')    #刚才在setting.py中配置的logger
        logger.error("workfunc_Wishworkfunc_Wishworkfunc_Wish BEGIN obj = %s aliexpressurls =%s"%(obj,aliexpressurls))

        data_bytes = None

        try:
            req = urllib2.Request(aliexpressurls)
            data_bytes = urllib2.urlopen(req, timeout = 15).read()#.decode('gbk')
        except urllib2.HTTPError, e:
            print e.code
        except urllib2.URLError, e:
            #self.message_user(request,e.reason)
            print e.reason
            print urllib2.URLError
            return
        else:
            print "OK"

        if data_bytes is not None:
            soup = BeautifulSoup(data_bytes,"lxml")
            #图片
            if soup is None:
                return

            link_jpg = dict(soup.find("ul", id="j-image-thumb-list").find("img").attrs)['src']

            if link_jpg is None:
                return
            try:
                req = urllib2.Request(link_jpg)
                image_bytes = urllib2.urlopen(req, timeout = 15).read()
            except urllib2.HTTPError, e:
                print e.code
            except urllib2.URLError, e:
                #self.message_user(request,e.reason)
                print e.reason
                print urllib2.URLError
                return
            if image_bytes is not None:
                auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
                bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_SV)
                bucket.put_object(u'%s/%s.jpg'%(obj.id,obj.id),image_bytes)
                #保存图片
                obj.SourcePicPath =  u'%s%s.%s/%s/%s.jpg'%(PREFIX,BUCKETNAME_SV,ENDPOINT_OUT,obj.id,obj.id)
                obj.SourceURL = aliexpressurls
                obj.SourceURL0 = aliexpressurls
                obj.save()

    #def save_model(self, request, obj, form, change):
    def save_models(self):
        obj = self.new_obj
        request = self.request

        begin_t_product_oplog(request,obj.MainSKU,'DY',obj.Name,obj.id)
        logger = logging.getLogger('sourceDns.webdns.views')    #刚才在setting.py中配置的logger
        #
        obj.StaffID = request.user.username
        obj.CreateTime = datetime.now()
        obj.CreateStaffName = request.user.first_name
        obj.save()

        #判断是否调研过
        if obj.SourceURL is not None :
            #1688不允许调研
            if  obj.SourceURL.find(WWW1688_URL)  >=0  : # 1688的数据采集
                messages.error(request,u'ERROR:请不要利用1688做反向链接调研!!!')
                return

            urlNew = obj.SourceURL
            if obj.SourceURL.find('?') >=0:
                urlNew = obj.SourceURL.split(r'?')[0]
            t_product_survey_history_objs = t_product_survey_history.objects.filter(SourceURL= urlNew)
            if t_product_survey_history_objs.count() > 0 :
                self.message_user(request,'url已经调研过！ . %s  urlNew=%s '%(obj.SourceURL,urlNew))
                #obj.delete()
                #return
            t_product_survey_ing_objs = t_product_survey_ing.objects.filter(SourceURL= urlNew)
            if t_product_survey_ing_objs.count() > 1 :
                self.message_user(request,'url已经调研过！ . %s count=%d '%(obj.SourceURL,t_product_survey_ing_objs.count()))
                #obj.delete()
                #return
        #obj.savexxx()
        select_picxx = False #表示True表示用户选择了图片
        if obj.selectpic is not None and str(obj.selectpic).strip() != ''  :
            auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
            bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_SV)
            bucket.put_object(u'%s/%s.jpg'%(obj.id,obj.id),obj.selectpic)
            #保存图片
            obj.SourcePicPath =  u'%s%s.%s/%s/%s.jpg'%(PREFIX,BUCKETNAME_SV,ENDPOINT_OUT,obj.id,obj.id)

            obj.save()
            select_picxx = True

        url = obj.SourceURL
        if url is None or url.strip() =='' or  obj.SourceURL0 == obj.SourceURL  :
            return
        try:
            if  url.find(WISH_URL)  >=0  : # wish的数据采集
                self.readWish(request, obj,url)
                obj.save()
                return
            if  url.find(AMAZON_URL)  >=0  : # amazon的数据采集
                self.readAmazon(request, obj,url)
                obj.save()
                return
            if  url.find(WWW1688_URL)  >=0  : # 1688的数据采集
                self.read1688(request, obj,url)
                obj.save()
                return
            if  url.find(EBAY_URL)  >=0  : # EBAY的数据采集
                self.readeBay(request, obj,url)
                obj.save()
                return
            if  url.find(ALIEXPRESS_URL)  >=0  : # aliexpress的数据采集
                self.readAliexpress(request, obj,url)
                obj.save()
                return
        except Exception,ex:
           print Exception,":",ex
           self.message_user(request,'提取数据失败 . %s : %s'%(Exception,ex))

    def get_queryset(self, request):
        qs = super(t_product_survey_ing_Admin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(StaffID = request.user.username)

class t_product_survey_ed_Admin(t_product_Admin):
    StepID = 'DYSH'
    StepName = u'调研审核'
    #save_on_top =True
    #actions = ['unique_ed', 'to_repeats','pass','notpass',]
    actions = ['to_pass','to_notpass',]
    def to_pass(self, request, queryset):
        cursor = connection.cursor() # 得到处理的游标对象
        for querysetid in queryset.all():
            obj = t_product_unique_ed()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name
            obj.save()

            end_t_product_oplog(request,querysetid.MainSKU,'DYSH',querysetid.Name2,querysetid.id)

            querysetid.delete()
    to_pass.short_description = u'审核通过'

    def to_notpass(self, request, queryset):
        self.to_recycle(request, queryset)
    to_notpass.short_description = u'审核不通过'



    list_display=('id','CreateTime','CreateStaffName','SourcePicPath','OrdersLast7Days','Pricerange','ShelveDay','Keywords','Keywords2','SpecialRemark','SourceURL')
    list_display_links=('SourcePicPath',)
    search_fields=('id','MainSKU','StaffID','Keywords','Keywords2',)
    #list_filter = ('UpdateTime','StaffID',)
    list_editable=('OrdersLast7Days','Keywords','Keywords2','ShelveDay','Pricerange','SpecialRemark',)



class t_product_unique_ed_Admin(t_product_Admin):
    StepID = 'KF'
    StepName = u'开发'
    #save_on_top =True
    actions = ['develop_ing', 'to_recycle',]
    def develop_ing(self, request, queryset):
        for querysetid in queryset.all():
            #下一步
            obj = t_product_develop_ing()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID = request.user.username
            obj.save()

            begin_t_product_oplog(request,querysetid.MainSKU,'KF',querysetid.Name2,querysetid.id)
            querysetid.delete()
    develop_ing.short_description = u'领用去开发'

    def to_recycle(self, request, queryset):
        super(t_product_unique_ed_Admin, self).to_recycle(request, queryset)
    to_recycle.short_description = u'扔进回收站'



    list_display=('id','CreateTime','CreateStaffName','SourcePicPath','SourceURL','OrdersLast7Days','Keywords','Keywords2','Tags','ShelveDay','Pricerange','SpecialRemark',)
    list_display_links=('SourcePicPath',)
    search_fields=('id','MainSKU','StaffID','Keywords','Keywords2',)

class t_product_develop_ing_Admin(t_product_Admin):
    StepID = 'KF'
    StepName = u'开发'
    #save_on_top =True
    actions = ['to_wait_enquiry','to_recycle' ,]
    def to_recycle(self, request, queryset):
        super(t_product_develop_ing_Admin, self).to_recycle(request, queryset)
    to_recycle.short_description = u'扔进回收站'

    def to_wait_enquiry(self, request, queryset):
        for querysetid in queryset.all():
            #下一步
            obj = t_product_wait_enquiry()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID = request.user.username
            obj.save()

            end_t_product_oplog(request,querysetid.MainSKU,'KF',querysetid.Name2,querysetid.id)

            querysetid.delete()

    to_wait_enquiry.short_description = u'开发完成待询价'


    #list_select_related = True
    list_display= ('id','CreateTime','CreateStaffName','SourcePicPath','SourceURL','OrdersLast7Days','ShelveDay','Keywords','Keywords2','Pricerange','SourcePicPath2','SupplierPUrl1','SpecialRemark','SupplierPDes','SupplierID',)
    list_display_links=('SourcePicPath','SourcePicPath2',)
    list_editable=('SourceURL','OrdersLast7Days','SupplierPUrl1','SupplierPDes','ShelveDay','Keywords','Keywords2','Pricerange','SpecialRemark',)

    search_fields=('id','MainSKU','StaffID','Name2','SupplierPUrl1',)
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':10})},
        models.URLField:  {'widget': TextInput(attrs={'size':'20'})},
        }
    #def save_model(self, request, obj, form, change):
    def save_models(self):
        obj = self.new_obj
        request = self.request


        if obj.SupplierPUrl1 is not None :
            obj.SupplierPUrl1 =  obj.SupplierPUrl1.split(r'?')[0]
        obj.save()
        www1688head = '.1688.com'
        www1688urls = obj.SupplierPUrl1 #r'https://www.wish.com/c/%s'%(obj.PlatformPID.strip())
        if www1688urls is None or www1688urls.strip() =='' or www1688urls.find(www1688head) <0 : #
            return



        #obj.savexx()
        www1688picurls = None
        data_bytes = None

        #取网站数据
        try:
            #data_bytes = urllib2.urlopen(www1688urls, timeout = 10).read().decode('gbk')
            req = urllib2.Request(www1688urls)
            data_bytes = urllib2.urlopen(req, timeout = 15).read().decode('gbk')
        except urllib2.HTTPError, e:
            self.message_user(request,e.reason)
            return
        except urllib2.URLError, e:
            self.message_user(request,e.reason)
            return
        if data_bytes is not None:
            soup = BeautifulSoup(data_bytes,"lxml")
            #file_object = open('thefile.txt', 'w')
            #file_object.write(soup.prettify())
            #file_object.close( )
            #供应商名称             #<a class="chinaname " href="https://hsfwcs.1688.com" style="color: ; font-family: 黑体; font-size: 30px;  ">  义乌市温略电子商务商行   </a>
            SupplierID = soup.html.find("a", attrs={'href':'#','class':'company-name'})
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
                    image_bytes = urllib2.urlopen(req, timeout = 15).read()
                except urllib2.HTTPError, e:
                    print e.code
                except urllib2.URLError, e:
                    #self.message_user(request,e.reason)
                    print e.reason
                    print urllib2.URLError
                if image_bytes is not None:
                    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
                    bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_1688)
                    bucket.put_object(u'%s/%s.jpg'%(obj.id,obj.id),image_bytes)
                    #保存图片
                    obj.SourcePicPath2 =  u'%s%s.%s/%s/%s.jpg'%(PREFIX,BUCKETNAME_1688,ENDPOINT_OUT,obj.id,obj.id )
                    #<a class="box-img" hidefocus="true" href="https://detail.1688.com/pic/538587081376.html" target="_blank" title="点击查看大图：欧美风 时尚非洲地图项链 精致金银色地图吊坠 男女款饰品 嘻哈风" trace="largepic">
                    #<img alt="欧美风 时尚非洲地图项链 精致金银色地图吊坠 男女款饰品 嘻哈风" src="https://cbu01.alicdn.com/img/ibank/2016/069/423/3451324960_185810081.400x400.jpg"/>
                    #<i class="zoom-mask">
                    #</i>
                    #</a>

        #self.message_user(request,data_bytes)
        obj.save()



    def get_queryset(self, request):
        qs = super(t_product_develop_ing_Admin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(StaffID = request.user.username)


class t_product_wait_enquiry_Admin(t_product_Admin):

    actions = ['to_enquiry_ing', 'to_recycle','to_repeats',]
    def to_repeats(self, request, queryset):
        for querysetid in queryset.all():
            #下一步
            obj = t_product_repeats()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID = request.user.username
            obj.save()

            end_t_product_oplog(request,querysetid.MainSKU,'XJ',querysetid.Name2,querysetid.id)

            querysetid.delete()
    to_repeats.short_description = u'重复产品'

    def to_recycle(self, request, queryset):
        super(t_product_wait_enquiry_Admin, self).to_recycle(request, queryset)
    to_recycle.short_description = u'扔进回收站'

    def to_enquiry_ing(self, request, queryset):
        for querysetid in queryset.all():
            #下一步
            obj = t_product_enquiry_ing()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID= request.user.username
            obj.save()
            begin_t_product_oplog(request,querysetid.MainSKU,'XJ',querysetid.Name2,querysetid.id)
            querysetid.delete()
    to_enquiry_ing.short_description = u'领取去询价'



    list_display= ('id','CreateTime','CreateStaffName','SourcePicPath','SpecialRemark','Keywords','Keywords2','Pricerange','SourcePicPath2','SupplierPUrl1','SupplierPDes','SupplierID','SourceURL',)
    list_display_links=('SourcePicPath','SourcePicPath2',)
    list_editable=('SpecialRemark',)

class t_product_enquiry_ing_Admin(t_product_Admin):
    StepID = 'XJ'
    StepName = u'询价'
    actions = ['enquiry_ed', 'to_recycle',]
    def enquiry_ed(self, request, queryset):
        for querysetid in queryset.all():
            #下一步
            obj = t_product_build_ing()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID= request.user.username
            obj.save()

            end_t_product_oplog(request,querysetid.MainSKU,'XJ',querysetid.Name2,querysetid.id)
            begin_t_product_oplog(request,querysetid.MainSKU,'JZL',querysetid.Name2,querysetid.id)
            querysetid.delete()
    enquiry_ed.short_description = u'询价完成'

    def to_recycle(self, request, queryset):
        super(t_product_enquiry_ing_Admin, self).to_recycle(request, queryset)
    to_recycle.short_description = u'扔进回收站'
    def show_oplog(self,obj) :
        rt = ''
        t_product_oplog_objs = t_product_oplog.objects.filter(pid=obj.id).order_by('id')
        for t_product_oplog_obj in t_product_oplog_objs:
            rt = u'%s%s:%s,'%(rt,t_product_oplog_obj.StepName,t_product_oplog_obj.OpName)
        return rt
    show_oplog.short_description = u'操作历史'


    list_display= ('id','CreateTime','CreateStaffName','SourcePicPath','SourceURL','OrdersLast7Days','Keywords','Keywords2','Pricerange','SourcePicPath2','SupplierPUrl1','SupplierID','SupplierPDes','UnitPrice','Weight','SpecialSell','show_oplog',)
    list_display_links=('SourcePicPath','SourcePicPath2',)
    list_editable=('SupplierPDes','UnitPrice','Weight','SpecialSell','SupplierPUrl1',)
    search_fields=('id','MainSKU','StaffID','Name2',)
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'6'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':8})},
        models.URLField:  {'widget': TextInput(attrs={'size':'6'})},
        models.DecimalField:  {'widget': TextInput(attrs={'size':'6'})},
        }

    def get_queryset(self, request):
        qs = super(t_product_enquiry_ing_Admin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(StaffID = request.user.username)

    #def save_model(self, request, obj, form, change):
    def save_models(self):
        obj = self.new_obj
        request = self.request

        logger = logging.getLogger('sourceDns.webdns.views')    #刚才在setting.py中配置的logger
        if obj.SupplierPUrl1 is not None :
            obj.SupplierPUrl1 =  obj.SupplierPUrl1.split(r'?')[0]
        obj.save()
        www1688head = '.1688.com'
        www1688urls = obj.SupplierPUrl1 #r'https://www.wish.com/c/%s'%(obj.PlatformPID.strip())
        if www1688urls is None or www1688urls.strip() =='' or www1688urls.find(www1688head) <0 : #
            return



        #obj.savexx()
        www1688picurls = None
        data_bytes = None

        #取网站数据
        try:
            #data_bytes = urllib2.urlopen(www1688urls, timeout = 10).read().decode('gbk')
            req = urllib2.Request(www1688urls)
            data_bytes = urllib2.urlopen(req, timeout = 15).read().decode('gbk')
        except urllib2.HTTPError, e:
            self.message_user(request,e.reason)
            return
        except urllib2.URLError, e:
            self.message_user(request,e.reason)
            return
        if data_bytes is not None:
            soup = BeautifulSoup(data_bytes,"lxml")
            #file_object = open('thefile.txt', 'w')
            #file_object.write(soup.prettify())
            #file_object.close( )
            #供应商名称             #<a class="chinaname " href="https://hsfwcs.1688.com" style="color: ; font-family: 黑体; font-size: 30px;  ">  义乌市温略电子商务商行   </a>
            SupplierID = soup.html.find("a", attrs={'href':'#','class':'company-name'})
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
                    image_bytes = urllib2.urlopen(req, timeout = 15).read()
                except urllib2.HTTPError, e:
                    print e.code
                except urllib2.URLError, e:
                    #self.message_user(request,e.reason)
                    print e.reason
                    print urllib2.URLError
                if image_bytes is not None:
                    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
                    bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_1688)
                    bucket.put_object(u'%s/%s.jpg'%(obj.id,obj.id),image_bytes)
                    #保存图片
                    obj.SourcePicPath2 =  u'%s%s.%s/%s/%s.jpg'%(PREFIX,BUCKETNAME_1688,ENDPOINT_OUT,obj.id,obj.id )
                    #<a class="box-img" hidefocus="true" href="https://detail.1688.com/pic/538587081376.html" target="_blank" title="点击查看大图：欧美风 时尚非洲地图项链 精致金银色地图吊坠 男女款饰品 嘻哈风" trace="largepic">
                    #<img alt="欧美风 时尚非洲地图项链 精致金银色地图吊坠 男女款饰品 嘻哈风" src="https://cbu01.alicdn.com/img/ibank/2016/069/423/3451324960_185810081.400x400.jpg"/>
                    #<i class="zoom-mask">
                    #</i>
                    #</a>

        #self.message_user(request,data_bytes)
        obj.save()

class t_product_build_ing_Admin(t_product_Admin):
    StepID = 'JZL'
    StepName = u'建资料'
    #save_on_top =True
    def getInfoFromSupplier(self,request,queryset) : #根据供货商获取信息,采购，
        #连接 sqlserver数据库
        import pyodbc
        conn= pyodbc.connect(SQLSERVERDB)
        cursor = conn.cursor();
        for qs in queryset:
            #获取采购员和责任归属人2
            cgy =''
            zrgs2 =''
            logger = logging.getLogger('sourceDns.webdns.views')    #刚才在setting.py中配置的logger

            sql= 'select NID ,SupplierName from B_Supplier '

            cursor.execute(sql);

            B_Supplier_obj = cursor.fetchone()
            while B_Supplier_obj is not None   :

                #logger.error('B_Supplier_objB_Supplier_objB_Supplier_objB_Supplier_obj=%s'%B_Supplier_obj)
                if B_Supplier_obj.SupplierName == qs.SupplierID:
                    sql2=u'select Purchaser,possessMan2 from B_Goods where SupplierID =  %d  order by CreateDate desc '%( B_Supplier_obj.NID)
                    cursor.execute(sql2);
                    B_Goods_obj = cursor.fetchone()
                    if B_Goods_obj :
                        cgy = B_Goods_obj.Purchaser
                        zrgs2=B_Goods_obj.possessMan2
                        self.message_user(request,u'cgy=[%s] zrgs2=[%s]'%(cgy,zrgs2) )
                    break
                else:
                    B_Supplier_obj = cursor.fetchone()
            obj = t_product_build_ing.objects.get(id__exact=qs.id)
            if obj :
                obj.Buyer = cgy
                obj.possessMan2 = zrgs2
                obj.save()
            cursor.close
        #关闭数据库连接
        conn.close()

    actions = ['to_develop_ed','to_photograph', 'to_recycle','to_getback',]
    def to_getback(self, request, queryset): #找回资料
        if request.user.is_superuser:
            t_product_build_ing_objs = t_product_build_ing.objects.all()
            for t_product_build_ing_obj in t_product_build_ing_objs:
                t_product_oplog_objs = t_product_oplog.objects.filter(pid=t_product_build_ing_obj.id,StepID='JZL')
                if t_product_oplog_objs.count() > 0 and t_product_oplog_objs[0].OpID != t_product_build_ing_obj.StaffID :
                    t_product_build_ing_obj.StaffID = t_product_oplog_objs[0].OpID
                    t_product_build_ing_obj.save()
        else:
            t_product_build_ing_objs = t_product_build_ing.objects.filter(StaffID= request.user.username)
            for t_product_build_ing_obj in t_product_build_ing_objs:
                t_product_oplog_objs = t_product_oplog.objects.filter(pid=t_product_build_ing_obj.id,StepID='JZL')
                if t_product_oplog_objs.count() > 0 and t_product_oplog_objs[0].OpID != t_product_build_ing_obj.StaffID :
                    t_product_build_ing_obj.StaffID = t_product_oplog_objs[0].OpID
                    t_product_build_ing_obj.save()
    to_getback.short_description = u'找回被驳回信息'

    def to_develop_ed(self, request, queryset): #大的开发概念完成

        self.getInfoFromSupplier(request,queryset)
        for querysetid in queryset.all():
            if self.is_valid(request,querysetid) ==False :
                continue

            obj = None
            if querysetid.fromT is not None and querysetid.fromT.strip() == 't_product_art_ed' :
                #下一步
                obj = t_product_art_ed()
            else:
                #下一步
                obj = t_product_develop_ed()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID= request.user.username
            obj.save()

            end_t_product_oplog(request,querysetid.MainSKU,'JZL',querysetid.Name2,querysetid.id)

            querysetid.delete()
    to_develop_ed.short_description = u'下一步(美工或信息审核)'

    def to_photograph(self, request, queryset): #大的开发概念完成
        self.getInfoFromSupplier(request,queryset)
        for querysetid in queryset.all():
            if self.is_valid(request,querysetid) ==False :
                continue
            #下一步
            obj = t_product_photograph()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID= request.user.username
            obj.save()

            end_t_product_oplog(request,querysetid.MainSKU,'JZL',querysetid.Name2,querysetid.id)
            begin_t_product_oplog(request, querysetid.MainSKU, 'PZ', querysetid.Name2, querysetid.id)
            querysetid.delete()
    to_photograph.short_description = u'下一步(需要去拍照)'

    def to_recycle(self, request, queryset):
        super(t_product_build_ing_Admin, self).to_recycle(request, queryset)
    to_recycle.short_description = u'扔进回收站'
    def show_oplog(self,obj) :
        rt = ''
        t_product_oplog_objs = t_product_oplog.objects.filter(pid=obj.id).order_by('id')
        for t_product_oplog_obj in t_product_oplog_objs:
            rt = u'%s%s:%s,'%(rt,t_product_oplog_obj.StepName,t_product_oplog_obj.OpName)
        return rt
    show_oplog.short_description = u'操作历史'

    def show_skulist(self,obj) :
        rt = '<table  style="text-align:center"><tr><th style="text-align:center">子SKU</th><th style="text-align:center">属性</th><th style="text-align:center">单价</th><th style="text-align:center">克重</th><th style="text-align:center">包装规格</th><th style="text-align:center">内包装成本</th></tr>'
        t_product_mainsku_sku_objs = t_product_mainsku_sku.objects.filter(pid=obj.id).order_by('SKU')

        for t_product_mainsku_sku_obj in t_product_mainsku_sku_objs:
            PackName =''
            CostPrice =0
            PackNID= t_product_mainsku_sku_obj.PackNID
            try:
                if PackNID > 0 :
                    B_PackInfo_obj = B_PackInfo.objects.get(id__exact = PackNID)
                    if B_PackInfo_obj is not None:
                        PackName =  B_PackInfo_obj.PackName
                        CostPrice = B_PackInfo_obj.CostPrice
            except:
                pass
            rt =  '%s <tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr> '%(rt,t_product_mainsku_sku_obj.SKU,t_product_mainsku_sku_obj.SKUATTRS,t_product_mainsku_sku_obj.UnitPrice,t_product_mainsku_sku_obj.Weight,PackName,CostPrice)


        rt = '%s</table>'%rt
        return mark_safe(rt)
    show_skulist.short_description = mark_safe('<p align="center"> 子SKU信息</p>')

    formfield_overrides = {
    models.CharField: {'widget': TextInput(attrs={'size':'20'})},
    models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':30})},
    }

    list_display= ('id','CreateTime','CreateStaffName','SourcePicPath2','MainSKU','show_skulist','Keywords','Keywords2','Pricerange','SupplierPUrl1','SupplierPDes','SpecialSell','SpecialRemark','StaffID','show_oplog',)
    list_display_links=('id','SourcePicPath2','Keywords','Keywords2','Pricerange','SupplierPUrl1','SupplierPDes','SpecialSell',)
    list_editable=('SpecialRemark',)
    search_fields=('id','MainSKU','Name2','StaffID',)
    readonly_fields = ('id','SKU',)
    # 分组表单

    fieldsets = (
        (u'调研结果', {
            'fields': (
                ('id',),
                ('SourceURL','OrdersLast7Days','Keywords','Keywords2','SurveyRemark','Pricerange','ShelveDay', ),
                ('Name','Tags',),
                ('SourcePicPath',),
                       ),
                }),

        (u'开发结果', {
            'fields': (
                ('SupplierPUrl1','SupplierPDes','SupplierID',),
                ('SourcePicPath2',)
                       ),
                }),

        (u'询价结果', {
            'fields': (
                ('UnitPrice','Weight','SpecialSell',),
                       ),
                }),

       	(u'建资料', {
            'fields': (
                    ('Name2','Material','Unit',),
                    ('MinOrder','SupplierArtNO','SupplierPColor','SupplierPUrl2',),
                    ('OrderDays','StockAlarmDays',),
                    ('LWH','SupplierContact','Storehouse',),
                    ('ReportName','ReportName2',),
                       ),
                }),
        (u'包装规格', {
            'fields': (
                ('MinPackNum',),
                       ),
                }),
        (u'违禁品属性', {
            'fields': (
                ('Electrification','Powder','Liquid','Magnetism',),
                       ),
                }),
        (u'备注信息', {'fields': ('Remark',)}),

        (u'大类名称/小类名称', {
            'fields': (

                       ),
                }),
        (u'SKU信息', {
            'fields': (
                ('MainSKU',),
                       ),
                }),


     )
    # SourcePicRemark ArtPicPath,SourceURLPrice ,'PlatformName','PlatformPID','SourcePicPath','InitialWord','Buyer','SpecialRemark','OldSKU','Length','Width','Height'
    #'NumBought','TotalInventory',URLamazon,URLebay,URLexpress,URLwish

    def save_pic_mainsku(self, request, obj, form, change):

        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_DEV)



        if request.method == 'POST':
            files = request.FILES.getlist('myfiles','')
            if files is None or len(files)== 0 :
                return


            for f in files :
                #bucket.put_object(u'%s/%s'%(obj.id,f.name),f) #obj.Category1_id
                bucket.put_object(u'%s/PUB/%s'%(obj.MainSKU,f.name),f)

                obj.SourcePicPath =  u'%s%s.%s/%s/PUB/%s'%(PREFIX,BUCKETNAME_DEV,ENDPOINT_OUT,obj.MainSKU,f.name)
                if f.name.strip().find('0000') >= 0:
                    obj.SourcePicPath =  u'%s%s.%s/%s/PUB/%s'%(PREFIX,BUCKETNAME_DEV,ENDPOINT_OUT,obj.MainSKU,f.name)
                    #obj.SourcePicPath =  u'%s/%s'%(obj.id,f.name)
                    self.message_user(request,obj.SourcePicPath )
                obj.save()

    #上传图片 子skuname,行index，request，obj
    def save_pic(self,skuname, i,request, obj):
        MainSKU = obj.MainSKU

        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_DEV)

        #加上子SKU
        path =  u'%s/%s'%(MainSKU,skuname)

        #写文件
        picfiles = request.FILES.getlist('file_%s_file'%i,'')
        for picfile in picfiles :
            if picfile is None or picfile.name.strip()=='' :
                continue
            bucket.put_object('%s/%s'%(path,picfile.name),picfile)



    def save_sku(self, request, obj, form, change):
        #先删除后头信息
        logger = logging.getLogger('sourceDns.webdns.views')    #刚才在setting.py中配置的logger

        logger.error("headnameheadnameheadnameheadnameheadnameheadname")


		#图片
        picfiles = request.FILES.getlist('file')
        for picfile in picfiles :
            logger.error(u'picfile= %s'%picfile.name)


        headnames = request.POST.getlist('headname','')
        for headname in headnames :
            logger.error(headname)

        logger.error("save_skusave_skusave_skusave_skusave_skusave_sku")
        skunames = request.POST.getlist('skuname','')
        for skuname in skunames :
            logger.error('skuname=%s'%skuname)

        logger.error("attrvalueattrvalueattrvalueattrvalueattrvalueattrvalueattrvalue")
        attrvalues = request.POST.getlist('attrvalue','')
        for attrvalue in attrvalues :
            logger.error('attrvalue=%s'%attrvalue)

        #删除插入表头,字段名称
        t_product_mainsku_arrt_name.objects.filter(MainSKU=obj.MainSKU).delete()



        j=0
        for headname in headnames :
            t_product_mainsku_arrt_name_obj= t_product_mainsku_arrt_name(MainSKU=obj.MainSKU,Attrid=j,AttrName=headname, pid=obj.id)
            t_product_mainsku_arrt_name_obj.save()
            j+=1

        t_product_sku_attr_value.objects.filter(MainSKU=obj.MainSKU).delete()
        t_product_mainsku_sku.objects.filter(MainSKU=obj.MainSKU).delete()

        #bucket = oss2.Bucket(oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET), ENDPOINT,BUCKETNAME_DEV)
        #for  object_info in oss2.ObjectIterator(bucket,prefix='%s/'%(obj.MainSKU)):
            #logger.error("object_infoobject_infoobject_infoobject_infoobject_info %s"%object_info.key)
            #if object_info.key.find('PUB') < 0 : #  PUB不删除
                #bucket.delete_object(object_info.key)

        i =0
        for skuname in skunames :
            if skuname is None or skuname.strip()=='' :
                i +=1
                continue

            #t_product_sku_attr_value_obj= t_product_sku_attr_value(MainSKU=obj.MainSKU,SKU=skuname,Attrid=0,AttrValue= skuxxxxxxxxxx)
            #t_product_sku_attr_value_obj.save()
            #插入对应关系

            t_product_mainsku_sku_obj = t_product_mainsku_sku(MainSKU=obj.MainSKU,SKU=skuname,pid=obj.id)
            t_product_mainsku_sku_obj.save()

            jj =0
            for headname in headnames :
                t_product_sku_attr_value_obj= t_product_sku_attr_value(MainSKU=obj.MainSKU,SKU=skuname,Attrid=jj,AttrValue=attrvalues[i*len(headnames) +jj])
                t_product_sku_attr_value_obj.save()
                jj +=1
            self.save_pic(skuname,i,request,obj)
            i+=1

    #判断主SKU是否合法
    def is_valid(self,request,obj):
        #主SKU不存在
        if obj.MainSKU is None or  obj.MainSKU.strip()=='':
            messages.error(request,u'ERROR:MainSKU(%s)is None!!!'%obj.MainSKU)
            return False

        #重复
        #if t_product_oplog.objects.filter(MainSKU = obj.MainSKU,StepID='JZL').count() >0 :
            #messages.error(request,u'ERROR:MainSKU(%s) repeat!!!'%obj.MainSKU )
            #return False

        #包装规格
        if obj.PackNID is None or obj.PackNID == 0 or obj.PackNID == '0':
            messages.error(request,u'ERROR:请选择包装规格!!!' )
            return False

        #大类
        if obj.LargeCategory is None or obj.LargeCategory == u'请选择大类' or obj.LargeCategory.strip() =='':
            messages.error(request,u'ERROR:请选择大类!!!' )
            return False
    #def save_model(self, request, obj, form, change):
    def save_models(self):
        obj = self.new_obj
        request = self.request

        obj.StaffID = request.user.username
        obj.SKU = obj.MainSKU
        obj.PackNID = request.POST.get('select_mainsku',0)
        obj.save()

        if obj.PackNID == 0 or  obj.PackNID == '0':
            messages.error(request,u'ERROR:请选择包装规格!!!' )
            return
        obj.LargeCategory = request.POST.get('province','')
        if obj.LargeCategory == u'请选择大类':
            messages.error(request,u'ERROR:请选择大类!!!' )
            return
        obj.SmallCategory = request.POST.get('city','')
        if obj.SmallCategory == u'请选择小类':
            obj.SmallCategory = ''


        self.applymainsku(request, obj, form, change)
        if obj.MainSKU is None or  obj.MainSKU.strip()=='':
            messages.error(request,u'ERROR:MainSKU is None!!!' )
            return

        #t_product_mainsku_sku.objects.filter(pid=obj.id).delete()
        t_product_mainsku_sku_objs = t_product_mainsku_sku.objects.filter(pid=obj.id)
        count = t_product_mainsku_sku_objs.count()
        t_product_mainsku_sku_objs.delete()
        skunum = 0

        for index in range(0, count):
            #self.message_user(request,u'index=%s'%(index))
            sku = request.POST.get('SKU_%s'%index,'')
            #self.message_user(request,u'index=%s,sku=%s'%(index,sku))
            if sku is None or sku =='':
                #t_product_mainsku_sku_objs[index].delete()
                continue

            skuattr = request.POST.get('SKUATTRS_%s'%index,obj.SupplierPColor)
            #self.message_user(request,u'index=%s,skuattr=%s'%(index,skuattr))
            if skuattr is None or skuattr.strip()=='':
                skuattr= obj.SupplierPColor

            unitprice = request.POST.get('UnitPrice_%s'%index,obj.UnitPrice)
            #self.message_user(request,u'index=%s,unitprice=%s'%(index,unitprice))
            if unitprice is None or str(unitprice).strip()=='':
                unitprice=obj.UnitPrice
            #unitprice = filter(lambda ch: ch in '0123456789.', unitprice)


            weight =   request.POST.get('Weight_%s'%index,obj.Weight)
            #self.message_user(request,u'index=%s,weight=%s'%(index,weight))
            if weight is None  or  str(weight).strip()=='':
                weight=obj.Weight
            #weight = filter(lambda ch: ch in '0123456789.', weight)
            NID  =   request.POST.get('select_%s'%index,obj.PackNID)
            if NID is None  or NID <=0 or str(NID).strip()=='':
                NID=obj.PackNID

            t_product_mainsku_sku_obj = t_product_mainsku_sku(MainSKU=obj.MainSKU,SKU=sku,SKUATTRS= skuattr,UnitPrice=unitprice,Weight= weight,PackNID=NID,pid = obj.id)
            t_product_mainsku_sku_obj.save()


            #self.message_user(request,u'index=%s,t_product_mainsku_sku_obj=%s'%(index,t_product_mainsku_sku_obj))
            skunum +=1

        if skunum < 1 :
            if obj.SupplierPColor is None :
                obj.SupplierPColor=''
            t_product_mainsku_sku.objects.filter(pid=obj.id).delete()
            t_product_mainsku_sku_obj = t_product_mainsku_sku(MainSKU=obj.MainSKU,SKU=obj.MainSKU,SKUATTRS= obj.SupplierPColor,UnitPrice=obj.UnitPrice,Weight= obj.Weight,pid = obj.id,PackNID=obj.PackNID)
            t_product_mainsku_sku_obj.save()

        #obj.aaaaa()
        #先保存sku的信息
        #self.save_sku( request, obj, form, change)
        #self.applymainsku(request, obj, form, change)
        #self.save_pic_mainsku(request, obj, form, change)
        #obj.StaffID = request.user.username

        obj.save()

        begin_t_product_oplog(request,obj.MainSKU,'JZL',obj.Name,obj.id)

    def applymainsku(self, request, obj, form, change):
    	#判断是否已经分配mainsku
        '''
        Category2New = request.POST.get('Category2','')
        if Category2New =='':
            return
        if obj.MainSKU is not None and obj.MainSKU.find(Category2New) >=0 :
                return

        Category2_seq = t_sys_sku_seq.objects.filter(CategoryName=Category2New);
        if Category2_seq.count() <=0 :
            t_sys_sku_seq_obj = t_sys_sku_seq(CategoryName=Category2New,CategoryDesc=Category2New,CategoryPrefix='A',CurValue=1000)

            obj.MainSKU = '%s%s%s'%(Category2New , t_sys_sku_seq_obj.CategoryPrefix, t_sys_sku_seq_obj.CurValue)
            obj.SKU = obj.MainSKU
            obj.Category2 = Category2New

            t_sys_sku_seq_obj.CurValue = t_sys_sku_seq_obj.CurValue + 1

            t_sys_sku_seq_obj.save()
            obj.save()
        else:
            obj.MainSKU = '%s%s%s'%(Category2New,Category2_seq[0].CategoryPrefix ,Category2_seq[0].CurValue)
            obj.SKU = obj.MainSKU
            obj.Category2 = Category2New

            Category2_seq.update(CurValue = Category2_seq[0].CurValue + 1)
            obj.save()
        '''
        #t_product_mainsku_sku.objects.filter(pid=obj.id).delete()
        #t_product_mainsku_sku_obj = t_product_mainsku_sku(MainSKU=obj.MainSKU,SKU=obj.MainSKU,SKUATTRS= obj.Name2,UnitPrice=obj.UnitPrice,Weight= obj.Weight,pid = obj.id)
        #t_product_mainsku_sku_obj.save()

    def get_queryset(self, request):
        qs = super(t_product_build_ing_Admin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(StaffID = request.user.username)

class t_product_photograph_Admin(t_product_Admin):
    StepID = 'PZ'
    StepName = u'拍照'
    #save_on_top =True

    actions = ['to_develop_ed', 'to_recycle',]
    def to_develop_ed(self, request, queryset): #大的开发概念完成

        for querysetid in queryset.all():
            #下一步
            obj = t_product_develop_ed()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID= request.user.username
            obj.save()

            end_t_product_oplog(request,querysetid.MainSKU,'PZ',querysetid.Name2,querysetid.id)
            querysetid.delete()

    to_develop_ed.short_description = u'拍照完成'
    def to_recycle(self, request, queryset):
        super(t_product_photograph_Admin, self).to_recycle(request, queryset)
    to_recycle.short_description = u'扔进回收站'

    def show_oplog(self,obj) :
        rt = ''
        t_product_oplog_objs = t_product_oplog.objects.filter(pid=obj.id).order_by('id')
        for t_product_oplog_obj in t_product_oplog_objs:
            rt = u'%s%s:%s,'%(rt,t_product_oplog_obj.StepName,t_product_oplog_obj.OpName)
        return rt
    show_oplog.short_description = u'操作历史'
    formfield_overrides = {
    models.CharField: {'widget': TextInput(attrs={'size':'20'})},
    models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':30})},
    }

    list_display = (
        'id','CreateTime','CreateStaffName', 'SourcePicPath2', 'Keywords', 'Keywords2', 'Pricerange', 'SupplierPUrl1', 'SupplierPDes', 'UnitPrice',
        'Weight', 'SpecialSell', 'SpecialRemark','show_oplog',)
    list_display_links = (
        'id', 'SourcePicPath2', 'Keywords', 'Keywords2', 'Pricerange', 'SupplierPUrl1', 'SupplierPDes', 'UnitPrice',
        'Weight', 'SpecialSell','SpecialRemark',)

    readonly_fields = ('id', 'SKU',)
    search_fields=('id','MainSKU','StaffID','Name2',)
    def get_queryset(self, request):
        qs = super(t_product_photograph_Admin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(StaffID=request.user.username)


class t_product_develop_ed_Admin(t_product_Admin):
    StepID = 'MG'
    StepName = u'美工'
    actions = ['art_ing','to_recycle', ]
    def art_ing(self, request, queryset):

        for querysetid in queryset.all():
            #下一步
            obj = t_product_art_ing()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID= request.user.username
            obj.save()
            begin_t_product_oplog(request,querysetid.MainSKU,'MG',querysetid.Name2,querysetid.id)
            querysetid.delete()

    art_ing.short_description = u'领用美工任务'

    def to_recycle(self, request, queryset):
        super(t_product_develop_ed_Admin, self).to_recycle(request, queryset)
    to_recycle.short_description = u'扔进回收站'

    def show_oplog(self,obj) :
        rt = ''
        t_product_oplog_objs = t_product_oplog.objects.filter(pid=obj.id).order_by('id')
        for t_product_oplog_obj in t_product_oplog_objs:
            rt = u'%s%s:%s,'%(rt,t_product_oplog_obj.StepName,t_product_oplog_obj.OpName)
        return rt
    show_oplog.short_description = u'操作历史'

    def show_skulist(self,obj) :
        rt = '<table  style="text-align:center"><tr><th style="text-align:center">子SKU</th><th style="text-align:center">属性</th><th style="text-align:center">单价</th><th style="text-align:center">克重</th><th style="text-align:center">包装规格</th><th style="text-align:center">内包装成本</th></tr>'
        t_product_mainsku_sku_objs = t_product_mainsku_sku.objects.filter(pid=obj.id).order_by('SKU')

        for t_product_mainsku_sku_obj in t_product_mainsku_sku_objs:
            PackName =''
            CostPrice =0
            PackNID= t_product_mainsku_sku_obj.PackNID
            try:
                if PackNID > 0 :
                    B_PackInfo_obj = B_PackInfo.objects.get(id__exact = PackNID)
                    if B_PackInfo_obj is not None:
                        PackName =  B_PackInfo_obj.PackName
                        CostPrice = B_PackInfo_obj.CostPrice
            except:
                pass
            rt =  '%s <tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr> '%(rt,t_product_mainsku_sku_obj.SKU,t_product_mainsku_sku_obj.SKUATTRS,t_product_mainsku_sku_obj.UnitPrice,t_product_mainsku_sku_obj.Weight,PackName,CostPrice)


        rt = '%s</table>'%rt
        return mark_safe(rt)
    show_skulist.short_description = mark_safe('<p align="center"> 子SKU信息</p>')

    formfield_overrides = {
    models.CharField: {'widget': TextInput(attrs={'size':'20'})},
    models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':30})},
    }

    list_display= ('id','CreateTime','CreateStaffName','SourcePicPath2','MainSKU','show_skulist','Name2','Material','SpecialSell','StaffID','show_oplog',)
    list_display_links=('SourcePicPath2',)

    readonly_fields = ('id','SKU',)
    search_fields=('id','MainSKU','StaffID','Name2',)
     # 分组表单
    fieldsets = (
        (u'调研结果', {
            'fields': (
                ('id',),
                ('SourceURL','OrdersLast7Days','Keywords','Keywords2','SurveyRemark','Pricerange','ShelveDay', ),
                ('Name','Tags',),
                ('SourcePicPath',),
                       ),
                }),

        (u'开发结果', {
            'fields': (
                ('SupplierPUrl1','SupplierPDes','SupplierID',),
                ('SourcePicPath2',)
                       ),
                }),

        (u'询价结果', {
            'fields': (
                ('UnitPrice','Weight','SpecialSell',),
                       ),
                }),

       	(u'建资料', {
            'fields': (
                    ('Name2','Material','Unit',),
                    ('MinPackNum','MinOrder','SupplierArtNO','SupplierPColor','SupplierPUrl2',),
                    ('OrderDays','StockAlarmDays',),
                    ('LWH','SupplierContact','Storehouse',),
                       ),
                }),

        (u'违禁品属性', {
            'fields': (
                ('Electrification','Powder','Liquid','Magnetism',),
                       ),
                }),
        (u'备注信息', {'fields': ('Remark',)}),

        (u'SKU信息', {
            'fields': (
                ('LargeCategory','SmallCategory','Category3','MainSKU','SKU',),
                       ),
                }),


     )

    #def save_model(self, request, obj, form, change):
    def save_models(self):
        obj = self.new_obj
        request = self.request
        obj.StaffID = request.user.username
        obj.save()
        if request.method == 'POST':
            files = request.FILES.getlist('myfiles')
            if obj.ArtPicPath is None :
                obj.ArtPicPath = ' '
            for f in files :
                if  obj.ArtPicPath.find(f.name) < 0 :
                    obj.ArtPicPath  += f.name+ r'; '
                obj.save()

                path = MEDIA_ROOT + 'upload_imgs/' + str(obj.id)
                if not os.path.exists(path):
                    os.mkdir(path)
                destination = open(path + '/' +  f.name,'wb+')
                for chunk in f.chunks():
                  destination.write(chunk)
                destination.close()

                #先删除重复的图片路径
                t_product_pictures.objects.filter(TradeID=obj.id,ArtPicPath='upload_imgs/' + str(obj.id) + '/'  +  f.name).delete()
				#保存数据库 t_product_pictures 路径
                t_product_pictures_obj = t_product_pictures(TradeID=obj.id,ArtPicPath='upload_imgs/' + str(obj.id) + '/'  +  f.name)
                t_product_pictures_obj.save()


class t_product_art_ing_Admin(t_product_Admin):
    #save_on_top =True
    StepID = 'MG'
    StepName = u'美工'
    actions = ['art_ed','to_recycle', 'to_building',]
    def to_building(self, request, queryset):
        for querysetid in queryset.all():
            #下一步
            obj = t_product_build_ing()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID= request.user.username
            obj.save()

            #修改操作记录
            t_product_oplog.objects.filter(StepID='JZL',pid = querysetid.id).update(MainSKU  = '',EndTime = datetime.now())

            querysetid.delete()

    to_building.short_description = u'返回建资料'

    def to_recycle(self, request, queryset):
       super(t_product_art_ing_Admin, self).to_recycle(request, queryset)
    to_recycle.short_description = u'扔进回收站'
    def download_pic(self, request, queryset):
        import zipfile

        mkdir_p(r'media')
        os.popen('chmod 777 media')

        mkdir_p(r'media/downloadartingpic')
        os.popen('chmod 777 media/downloadartingpic')

        #情况现有目录
        os.popen('rm -rf media/downloadartingpic/%s_20*'%(request.user.username))

        dirname0 = r'%s_%s'%(request.user.username,datetime.now().strftime('%Y%m%d%H%M%S'))
        dirname = r'media/downloadartingpic/%s'%(dirname0)
        mkdir_p(dirname)
        os.popen('chmod 777 %s'%(dirname))

        zfilename = r'%s.zip'%(dirname)
        z = zipfile.ZipFile(zfilename, 'w')



        for qs in queryset.all():
            if qs.MainSKU is None or qs.MainSKU.strip()=='' :
                continue
            MainSKU = qs.MainSKU

            auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
            bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_DEV)

            #获取子SKU图片
            t_product_mainsku_sku_objs = t_product_mainsku_sku.objects.filter(MainSKU =  qs.MainSKU)
            for t_product_mainsku_sku_obj in t_product_mainsku_sku_objs :
                SKU = t_product_mainsku_sku_obj.SKU
                for  object_info in oss2.ObjectIterator(bucket,prefix='%s/%s/'%(MainSKU,SKU)):
                    if object_info.key.endswith (('.jpg','.png',)) :
                        filename = '%s'%(object_info.key)
                        filename2=filename
                        skudirname = r'%s/%s'%(MainSKU,SKU)
                        mkdir_p(r'%s/%s'%(dirname,skudirname))
                        os.popen(r'chmod 777 %s/%s'%(dirname,skudirname))
                        filename3  = r'%s/%s__%s'%(dirname,skudirname,filename2.split(r'/')[-1])
                        bucket.get_object_to_file(object_info.key,filename3)
                        z.write(r'%s'%(filename3))

            #获取公共图片
            SKU = 'PUB'
            for  object_info in oss2.ObjectIterator(bucket,prefix='%s/%s/'%(MainSKU,SKU)):
                if object_info.key.endswith (('.jpg','.png',)) :
                    filename = '%s'%(object_info.key)
                    filename2=filename
                    skudirname = r'%s/%s'%(MainSKU,SKU)
                    mkdir_p(r'%s/%s'%(dirname,skudirname))
                    os.popen(r'chmod 777 %s/%s'%(dirname,skudirname))
                    filename3  = r'%s/%s__%s'%(dirname,skudirname,filename2.split(r'/')[-1])
                    bucket.get_object_to_file(object_info.key,filename3)
                    z.write(r'%s'%(filename3))
        z.close()
        #上传zip文件
        #上传oss对象
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_ZIP)
        bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)

        #删除现有的
        for  object_info in oss2.ObjectIterator(bucket,prefix='%s/media/downloadartingpic/%s_'%(request.user.username,request.user.username)):
            bucket.delete_object(object_info.key)

        bucket.put_object(u'%s/%s'%(request.user.username,zfilename),open(zfilename))
        #删除临时ecp上面zip文件
        #os.popen(' rm -f %s'%zfilename)

        self.message_user(request,u'%s%s.%s/%s/%s'%(PREFIX,BUCKETNAME_ZIP,ENDPOINT_OUT,request.user.username,zfilename) + u':成功导出,可点击Download下载到本地............................。' )
    download_pic.short_description = u'下载待美工图片'

    def art_ed(self, request, queryset):
        for querysetid in queryset.all():
            #下一步
            obj = t_product_art_pre_ed()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID= request.user.username
            obj.save()
            end_t_product_oplog(request,querysetid.MainSKU,'MG',querysetid.Name2,querysetid.id)
            querysetid.delete()
    art_ed.short_description = u'美工完成'

    def show_oplog(self,obj) :
        rt = ''
        t_product_oplog_objs = t_product_oplog.objects.filter(pid=obj.id).order_by('id')
        for t_product_oplog_obj in t_product_oplog_objs:
            rt = u'%s%s:%s,'%(rt,t_product_oplog_obj.StepName,t_product_oplog_obj.OpName)
        return rt
    show_oplog.short_description = u'操作历史'

    def show_skulist(self,obj) :
        rt = '<table  style="text-align:center"><tr><th style="text-align:center">子SKU</th><th style="text-align:center">属性</th><th style="text-align:center">单价</th><th style="text-align:center">克重</th><th style="text-align:center">包装规格</th><th style="text-align:center">内包装成本</th></tr>'
        t_product_mainsku_sku_objs = t_product_mainsku_sku.objects.filter(pid=obj.id).order_by('SKU')

        for t_product_mainsku_sku_obj in t_product_mainsku_sku_objs:
            PackName =''
            CostPrice =0
            PackNID= t_product_mainsku_sku_obj.PackNID
            try:
                if PackNID > 0 :
                    B_PackInfo_obj = B_PackInfo.objects.get(id__exact = PackNID)
                    if B_PackInfo_obj is not None:
                        PackName =  B_PackInfo_obj.PackName
                        CostPrice = B_PackInfo_obj.CostPrice
            except:
                pass
            rt =  '%s <tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr> '%(rt,t_product_mainsku_sku_obj.SKU,t_product_mainsku_sku_obj.SKUATTRS,t_product_mainsku_sku_obj.UnitPrice,t_product_mainsku_sku_obj.Weight,PackName,CostPrice)


        rt = '%s</table>'%rt
        return mark_safe(rt)
    show_skulist.short_description = mark_safe('<p align="center"> 子SKU信息</p>')
    formfield_overrides = {
    models.CharField: {'widget': TextInput(attrs={'size':'20'})},
    models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':30})},
    }

    list_display= ('id','CreateTime','CreateStaffName','SourcePicPath2','MainSKU','show_skulist','Name2','Material','SpecialSell','show_oplog',)
    list_display_links=('id','SourcePicPath2','MainSKU','Name2','Material','SpecialSell',)

    readonly_fields = ('id','SKU',)
    search_fields=('id','MainSKU','StaffID','Name2',)
     # 分组表单
    fieldsets = (
        (u'调研结果', {
            'fields': (
                ('id',),
                ('SourceURL','OrdersLast7Days','Keywords','Keywords2','SurveyRemark','Pricerange','ShelveDay', ),
                ('Name','Tags',),
                ('SourcePicPath',),
                       ),
                }),

        (u'开发结果', {
            'fields': (
                ('SupplierPUrl1','SupplierPDes','SupplierID',),
                ('SourcePicPath2',)
                       ),
                }),

        (u'询价结果', {
            'fields': (
                ('UnitPrice','Weight','SpecialSell',),
                       ),
                }),

       	(u'建资料', {
            'fields': (
                    ('Name2','Material','Unit',),
                    ('MinPackNum','MinOrder','SupplierArtNO','SupplierPColor','SupplierPUrl2',),
                    ('OrderDays','StockAlarmDays',),
                    ('LWH','SupplierContact','Storehouse',),
                       ),
                }),

        (u'违禁品属性', {
            'fields': (
                ('Electrification','Powder','Liquid','Magnetism',),
                       ),
                }),
        (u'备注信息', {'fields': ('Remark',)}),

        (u'SKU信息', {
            'fields': (
                ('LargeCategory','SmallCategory','Category3','MainSKU','SKU',),
                       ),
                }),


     )
    #def save_model(self, request, obj, form, change):
    def save_models(self):
        obj = self.new_obj
        request = self.request
        obj.StaffID = request.user.username
        obj.save()

    def get_queryset(self, request):
        qs = super(t_product_art_ing_Admin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(StaffID = request.user.username)

class t_product_art_pre_ed_Admin(t_product_Admin):
    StepID = 'LR'
    StepName = u'录入'
    actions = ['to_review', ]
    def to_review(self, request, queryset):
        for querysetid in queryset.all():
            obj = t_product_art_ed()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID= request.user.username
            obj.save()
            begin_t_product_oplog(request,querysetid.MainSKU,'LR',querysetid.Name2,querysetid.id)
            querysetid.delete()
        cursor.close()

    to_review.short_description = u'领去审核'



    def show_oplog(self,obj) :
        rt = ''
        t_product_oplog_objs = t_product_oplog.objects.filter(pid=obj.id,StepID='JZL').order_by('id')
        for t_product_oplog_obj in t_product_oplog_objs:
            rt = u'%s%s:%s,'%(rt,t_product_oplog_obj.StepName,t_product_oplog_obj.OpName)
        return rt
    show_oplog.short_description = u'操作历史'

    def show_skulist(self,obj) :
        rt = '<table  style="text-align:center"><tr><th style="text-align:center">子SKU</th><th style="text-align:center">属性</th><th style="text-align:center">单价</th><th style="text-align:center">克重</th><th style="text-align:center">包装规格</th><th style="text-align:center">内包装成本</th></tr>'
        t_product_mainsku_sku_objs = t_product_mainsku_sku.objects.filter(pid=obj.id).order_by('SKU')

        for t_product_mainsku_sku_obj in t_product_mainsku_sku_objs:
            PackName =''
            CostPrice =0
            PackNID= t_product_mainsku_sku_obj.PackNID
            try:
                if PackNID >= 0 :
                    B_PackInfo_obj = B_PackInfo.objects.get(id__exact = PackNID)
                    if B_PackInfo_obj is not None:
                        PackName =  B_PackInfo_obj.PackName
                        CostPrice = B_PackInfo_obj.CostPrice
            except:
                pass
            rt =  '%s <tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr> '%(rt,t_product_mainsku_sku_obj.SKU,t_product_mainsku_sku_obj.SKUATTRS,t_product_mainsku_sku_obj.UnitPrice,t_product_mainsku_sku_obj.Weight,PackName,CostPrice)


        rt = '%s</table>'%rt
        return mark_safe(rt)
    show_skulist.short_description = mark_safe('<p align="center"> 子SKU信息</p>')




    def show_Remark(self,obj) :
        return mark_safe(u'%s<br>%s<br>%s<br>%s'%(obj.Remark,obj.LWH,obj.SupplierPUrl1,obj.SupplierPUrl2 ))
    show_Remark.short_description = u'备注'

    def show_wjp(self,obj) :
        rt =''
        if obj.Electrification ==u'是' :
            rt = rt + u'带电;'
        if  obj.Powder ==u'是' :
            rt = rt + u'粉末;'
        if  obj.Liquid ==u'是' :
            rt = rt + u'液体;'
        if obj.Magnetism ==u'是' :
            rt = rt + u'带磁;'
        return rt
    show_wjp.short_description = u'违禁品'

    def show_name2(self,obj) :
        PrepackMark = obj.PrepackMark
        if PrepackMark is None:
            PrepackMark=''
        Name2 = obj.Name2
        if obj.Electrification ==u'是' or obj.Powder ==u'是' or obj.Liquid ==u'是' or obj.Magnetism ==u'是' :
            if obj.SmallCategory != u'手表': #手表特殊
                wjp = u'-违禁品'
                return u'%s%s%s'%(Name2,wjp,PrepackMark)
        return u'%s%s'%(Name2,PrepackMark)
    show_name2.short_description = mark_safe(u'商品<br>名称<br>(中文)')

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'6'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':6})},
        models.URLField:  {'widget': TextInput(attrs={'size':'6'})},
        }

    list_display= ('id','CreateTime','CreateStaffName','SourcePicPath2','MainSKU','Buyer','possessMan2','SpecialRemark','show_skulist','LargeCategory','SmallCategory','show_name2','Material','SupplierArtNO','Unit','MinPackNum','SupplierID','ReportName','ReportName2','show_oplog','show_wjp','show_Remark',)
    list_display_links= ('id','SourcePicPath2',)#,'MainSKU','LargeCategory','SmallCategory','Name2','Material','SupplierArtNO','Unit','MinPackNum','SupplierID','Keywords2','Keywords',)
    readonly_fields = ('id',)
    search_fields=('id','MainSKU','Name2','StaffID',)


class t_product_art_ed_Admin(t_product_Admin):
    StepID = 'LR'
    StepName = u'录入'
    actions = ['to_repeats','to_not_pass','to_pass','to_recycle',]
    def to_repeats(self, request, queryset):

        for querysetid in queryset.all():
            obj = t_product_repeats()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID= request.user.username
            obj.save()

            end_t_product_oplog(request,querysetid.MainSKU,'LR',querysetid.Name2,querysetid.id)
            querysetid.delete()

    to_repeats.short_description = u'重复产品'

    def to_recycle(self, request, queryset):
        super(t_product_art_ed_Admin, self).to_recycle(request, queryset)
    to_recycle.short_description = u'扔进回收站'
    def to_not_pass(self, request, queryset):

        for querysetid in queryset.all():
            obj = t_product_build_ing()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID= request.user.username
            obj.save()

            #修改操作记录
            t_product_oplog.objects.filter(StepID='JZL',pid = querysetid.id).update(MainSKU  = '',EndTime = datetime.now())

            querysetid.delete()

    to_not_pass.short_description = u'审核不通过'

    def to_pass(self, request, queryset):

        for querysetid in queryset.all():
            obj = t_product_enter_ing()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID= request.user.username
            obj.save()

            querysetid.delete()

    to_pass.short_description = u'审核通过'

    def show_oplog(self,obj) :
        rt = ''
        t_product_oplog_objs = t_product_oplog.objects.filter(pid=obj.id,StepID='JZL').order_by('id')
        for t_product_oplog_obj in t_product_oplog_objs:
            rt = u'%s%s:%s,'%(rt,t_product_oplog_obj.StepName,t_product_oplog_obj.OpName)
        return rt
    show_oplog.short_description = u'操作历史'

    def show_skulist(self,obj) :
        rt = '<table  style="text-align:center"><tr><th style="text-align:center">子SKU</th><th style="text-align:center">属性</th><th style="text-align:center">单价</th><th style="text-align:center">克重</th><th style="text-align:center">包装规格</th><th style="text-align:center">内包装成本</th></tr>'
        t_product_mainsku_sku_objs = t_product_mainsku_sku.objects.filter(pid=obj.id).order_by('SKU')

        for t_product_mainsku_sku_obj in t_product_mainsku_sku_objs:
            PackName =''
            CostPrice =0
            PackNID= t_product_mainsku_sku_obj.PackNID
            try:
                if PackNID >= 0 :
                    B_PackInfo_obj = B_PackInfo.objects.get(id__exact = PackNID)
                    if B_PackInfo_obj is not None:
                        PackName =  B_PackInfo_obj.PackName
                        CostPrice = B_PackInfo_obj.CostPrice
            except:
                pass
            rt =  '%s <tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr> '%(rt,t_product_mainsku_sku_obj.SKU,t_product_mainsku_sku_obj.SKUATTRS,t_product_mainsku_sku_obj.UnitPrice,t_product_mainsku_sku_obj.Weight,PackName,CostPrice)


        rt = '%s</table>'%rt
        return mark_safe(rt)
    show_skulist.short_description = mark_safe('<p align="center"> 子SKU信息</p>')

    def show_PackName(self,obj) :
        rt = ''
        PackNID= obj.PackNID
        if PackNID <=0 :
            return rt
        B_PackInfo_obj = B_PackInfo.objects.get(id__exact = PackNID)
        if B_PackInfo_obj is not None:
            rt =  B_PackInfo_obj.PackName
        return rt
    show_PackName.short_description = u'包装规格'

    def show_CostPrice(self,obj) :
        rt = ''
        PackNID= obj.PackNID
        if PackNID <=0 :
            return rt
        B_PackInfo_obj = B_PackInfo.objects.get(id__exact = PackNID)
        if B_PackInfo_obj is not None:
            rt =  B_PackInfo_obj.CostPrice
        return rt
    show_CostPrice.short_description = u'内包装成本'

    def show_Remark(self,obj) :
        return mark_safe(u'%s<br>%s<br>%s<br>%s'%(obj.Remark,obj.LWH,obj.SupplierPUrl1,obj.SupplierPUrl2 ))
    show_Remark.short_description = u'备注'

    def show_wjp(self,obj) :
        rt =''
        if obj.Electrification ==u'是' :
            rt = rt + u'带电;'
        if  obj.Powder ==u'是' :
            rt = rt + u'粉末;'
        if  obj.Liquid ==u'是' :
            rt = rt + u'液体;'
        if obj.Magnetism ==u'是' :
            rt = rt + u'带磁;'
        return rt
    show_wjp.short_description = u'违禁品'

    def show_name2(self,obj) :
        PrepackMark = obj.PrepackMark
        if PrepackMark is None:
            PrepackMark=''
        Name2 = obj.Name2
        if obj.Electrification ==u'是' or obj.Powder ==u'是' or obj.Liquid ==u'是' or obj.Magnetism ==u'是' :
            if obj.SmallCategory != u'手表': #手表特殊
                wjp = u'-违禁品'
                return u'%s%s%s'%(Name2,wjp,PrepackMark)
        return u'%s%s'%(Name2,PrepackMark)
    show_name2.short_description = mark_safe(u'商品<br>名称<br>(中文)')

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'6'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':6})},
        models.URLField:  {'widget': TextInput(attrs={'size':'6'})},
        }

    list_display= ('id','CreateTime','CreateStaffName','SourcePicPath2','MainSKU','Buyer','possessMan2','SpecialRemark','PrepackMark','show_skulist','LargeCategory','SmallCategory','show_name2','Material','SupplierArtNO','Unit','MinPackNum','SupplierID','ReportName','ReportName2','show_oplog','show_wjp','show_Remark',)
    list_display_links= ('id','SourcePicPath2',)#,'MainSKU','LargeCategory','SmallCategory','Name2','Material','SupplierArtNO','Unit','MinPackNum','SupplierID','Keywords2','Keywords',)
    list_editable=('SpecialRemark','Buyer','possessMan2','PrepackMark',)
    readonly_fields = ('id',)
    search_fields=('id','MainSKU','Name2','StaffID',)
    #list_filter = ('UpdateTime',)
     # 分组表单

    fieldsets = (
        (u'调研结果', {
            'fields': (
                ('id',),
                ('SourceURL','OrdersLast7Days','Keywords','Keywords2','SurveyRemark','Pricerange','ShelveDay', ),
                ('Name','Tags',),
                ('SourcePicPath',),
                       ),
                }),

        (u'开发结果', {
            'fields': (
                ('SupplierPUrl1','SupplierPDes','SupplierID',),
                ('SourcePicPath2',)
                       ),
                }),

        (u'询价结果', {
            'fields': (
                ('UnitPrice','Weight','SpecialSell',),
                       ),
                }),

       	(u'建资料', {
            'fields': (
                    ('Name2','PrepackMark','Material','Unit',),
                    ('MinOrder','SupplierArtNO','SupplierPColor','SupplierPUrl2',),
                    ('OrderDays','StockAlarmDays',),
                    ('LWH','SupplierContact','Storehouse',),
                    ('ReportName','ReportName2',),
                       ),
                }),
        (u'包装规格', {
            'fields': (
                ('MinPackNum',),
                       ),
                }),
        (u'违禁品属性', {
            'fields': (
                ('Electrification','Powder','Liquid','Magnetism',),
                       ),
                }),
        (u'备注信息', {'fields': ('Remark',)}),

        (u'大类名称/小类名称', {
            'fields': (

                       ),
                }),
        (u'SKU信息', {
            'fields': (
                ('MainSKU',),
                       ),
                }),
     )
    def applymainsku(self, request, obj, form, change):
        pass

    #def save_model(self, request, obj, form, change):
    def save_models(self):
        obj = self.new_obj
        request = self.request



        obj.save()
        PackNID = request.POST.get('select_mainsku',None)
        if PackNID is None:
            return
        obj.PackNID = PackNID
        if obj.PackNID == 0 or  obj.PackNID == '0':
            messages.error(request,u'ERROR:请选择包装规格!!!' )
            return
        obj.LargeCategory = request.POST.get('province','')
        if obj.LargeCategory == u'请选择大类':
            messages.error(request,u'ERROR:请选择大类!!!' )
            return
        obj.SmallCategory = request.POST.get('city','')
        if obj.SmallCategory == u'请选择小类':
            obj.SmallCategory = ''


        self.applymainsku(request, obj, form, change)
        if obj.MainSKU is None or  obj.MainSKU.strip()=='':
            messages.error(request,u'ERROR:MainSKU is None!!!' )
            return

        #t_product_mainsku_sku.objects.filter(pid=obj.id).delete()
        t_product_mainsku_sku_objs = t_product_mainsku_sku.objects.filter(pid=obj.id)
        count = t_product_mainsku_sku_objs.count()
        t_product_mainsku_sku_objs.delete()
        skunum = 0

        for index in range(0, count):
            #self.message_user(request,u'index=%s'%(index))
            sku = request.POST.get('SKU_%s'%index,'')
            #self.message_user(request,u'index=%s,sku=%s'%(index,sku))
            if sku is None or sku =='':
                #t_product_mainsku_sku_objs[index].delete()
                continue

            skuattr = request.POST.get('SKUATTRS_%s'%index,obj.SupplierPColor)
            #self.message_user(request,u'index=%s,skuattr=%s'%(index,skuattr))
            if skuattr is None or skuattr.strip()=='':
                skuattr= obj.SupplierPColor

            unitprice = request.POST.get('UnitPrice_%s'%index,obj.UnitPrice)
            #self.message_user(request,u'index=%s,unitprice=%s'%(index,unitprice))
            if unitprice is None or str(unitprice).strip()=='':
                unitprice=obj.UnitPrice
            #unitprice = filter(lambda ch: ch in '0123456789.', unitprice)


            weight =   request.POST.get('Weight_%s'%index,obj.Weight)
            #self.message_user(request,u'index=%s,weight=%s'%(index,weight))
            if weight is None  or  str(weight).strip()=='':
                weight=obj.Weight
            #weight = filter(lambda ch: ch in '0123456789.', weight)
            NID  =   request.POST.get('select_%s'%index,obj.PackNID)
            if NID is None  or NID <=0 or str(NID).strip()=='':
                NID=obj.PackNID

            t_product_mainsku_sku_obj = t_product_mainsku_sku(MainSKU=obj.MainSKU,SKU=sku,SKUATTRS= skuattr,UnitPrice=unitprice,Weight= weight,PackNID=NID,pid = obj.id)
            t_product_mainsku_sku_obj.save()


            #self.message_user(request,u'index=%s,t_product_mainsku_sku_obj=%s'%(index,t_product_mainsku_sku_obj))
            skunum +=1

        if skunum < 1 :
            if obj.SupplierPColor is None :
                obj.SupplierPColor=''
            t_product_mainsku_sku.objects.filter(pid=obj.id).delete()
            t_product_mainsku_sku_obj = t_product_mainsku_sku(MainSKU=obj.MainSKU,SKU=obj.MainSKU,SKUATTRS= obj.SupplierPColor,UnitPrice=obj.UnitPrice,Weight= obj.Weight,pid = obj.id,PackNID=obj.PackNID)
            t_product_mainsku_sku_obj.save()


        obj.save()



    def get_queryset(self, request):
        qs = super(t_product_art_ed_Admin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(StaffID = request.user.username)

class t_product_enter_ing_Admin(t_product_Admin):
    StepID = 'LR'
    StepName = u'录入'
    actions = ['to_not_pass','to_exort_ed','to_enter_ed','to_recycle',]
    def to_not_pass(self, request, queryset):

        for querysetid in queryset.all():
            obj = t_product_build_ing()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID= request.user.username
            obj.save()

            #修改操作记录
            t_product_oplog.objects.filter(StepID='JZL',pid = querysetid.id).update(MainSKU  = '',EndTime = datetime.now())

            querysetid.delete()

    to_not_pass.short_description = u'审核不通过'

    def to_recycle(self, request, queryset):
        super(t_product_enter_ing_Admin, self).to_recycle(request, queryset)
    to_recycle.short_description = u'扔进回收站'
    def to_exort_ed(self, request, queryset):
        from xlwt import *
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        #if not os.path.exists(path):
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s'%(MEDIA_ROOT + 'download_xls'))

        mkdir_p(path)
        os.popen('chmod 777 %s'%(path))

        w = Workbook()
        sheet = w.add_sheet('sku')

        for index,item in enumerate(XLS_FIELDS):
            sheet.write(0,index,item)

        #写数据
        row = 0

        for qs in queryset:


            #根据主SKU查找子sku
            t_product_mainsku_sku_objs = t_product_mainsku_sku.objects.filter(MainSKU =  qs.MainSKU,pid= qs.id)

            for  mainsku_sku_obj in t_product_mainsku_sku_objs :
                row = row +1
                column = 0
                sheet.write(row,column,u'add') #A 操作类型

                column = column +1
                if qs.MainSKU == mainsku_sku_obj.SKU :
                    sheet.write(row,column,'%s'%(qs.MainSKU)) #B 商品编码
                else:
                    sheet.write(row,column,'%s%s'%(qs.MainSKU,mainsku_sku_obj.SKU)) #B 商品编码

                column = column +1
                if qs.MainSKU == mainsku_sku_obj.SKU :
                    sheet.write(row,column,'%s'%(qs.MainSKU)) #C SKU
                else:
                    sheet.write(row,column,'%s%s'%(qs.MainSKU,mainsku_sku_obj.SKU)) #C SKU


                column = column +1
                sheet.write(row,column,u'否') #D 多款式

                column = column +1
                sheet.write(row,column,u'否') #E 是否有样品

                column = column +1
                #sheet.write(row,column,1) #F 样品数量

                column = column +1
                sheet.write(row,column,qs.LargeCategory) #G 大类名称

                column = column +1
                sheet.write(row,column,qs.SmallCategory) #H 小类名称



                column = column +1
                #sheet.write(row,column,qs.Name) #I 商品名称
                wjp = ''
                if qs.Electrification ==u'是' or qs.Powder ==u'是' or qs.Liquid ==u'是' or qs.Magnetism ==u'是' :
                    if qs.SmallCategory != u'手表': #手表特殊
                        wjp = u'-违禁品'
                PrepackMark = qs.PrepackMark
                if PrepackMark is None:
                    PrepackMark=''
                sheet.write(row,column,u'%s-%s%s%s'%(qs.Name2,mainsku_sku_obj.SKUATTRS,wjp,PrepackMark)) #I 商品名称


                column = column +1
                sheet.write(row,column,u'正常') #J 当前状态

                column = column +1
                sheet.write(row,column,qs.Material) #K 材质

                column = column +1
                #sheet.write(row,column,'%s'%(qs.LWH) ) #L 规格


                column = column +1
                sheet.write(row,column, '%s'%(qs.SupplierArtNO)) #M 型号

                column = column +1
                #sheet.write(row,column, u'款式' ) #N 款式

                column = column +1
                sheet.write(row,column, 'fancyqube' ) #O 品牌

                column = column +1
                sheet.write(row,column, qs.Unit) #P 单位

                column = column +1
                #zxbzs = 1
                #if qs.Unit ==u'对':
                #    zxbzs = 2
                #sheet.write(row,column, zxbzs ) #Q 最小包装数
                sheet.write(row,column, qs.MinPackNum )

                column = column +1

                weight = 0
                if  qs.Weight is not None and qs.Weight >0:
                    weight = qs.Weight
                if  mainsku_sku_obj.Weight is not None and mainsku_sku_obj.Weight >0:
                    weight = mainsku_sku_obj.Weight

                PackNID= mainsku_sku_obj.PackNID
                if PackNID <=0 :
                    PackNID = qs.PackNID
                B_PackInfo_obj = None
                try:
                    B_PackInfo_obj = B_PackInfo.objects.get(id__exact = PackNID)
                    if B_PackInfo_obj is not None:
                        weight = weight + B_PackInfo_obj.Weight

                except:
                    pass
                sheet.write(row,column,u'%s'%(weight)) #R 重量(G)
                """
                t_sys_packing_obj = None
                t_sys_packing2_obj = None
                if qs.PackingID_id is not None :
                    t_sys_packing_obj  = t_sys_packing.objects.get(id__exact = qs.PackingID_id)
                    if  t_sys_packing_obj is not None and t_sys_packing_obj.Weight is not None  :
                        weight = weight + t_sys_packing_obj.Weight

                #附加包装
                if qs.PackingID2Num is not None and qs.PackingID2Num > 0 and qs.PackingID2_id is not None:
                    t_sys_packing2_obj  = t_sys_packing2.objects.get(id__exact = qs.PackingID2_id)
                    if  t_sys_packing2_obj is not None  and t_sys_packing2_obj.Weight is not None and qs.PackingID2Num is not None :
                        weight = weight + t_sys_packing2_obj.Weight * qs.PackingID2Num
                sheet.write(row,column,u'%s'%(weight)) #R 重量(G)
                """

                column = column +1
                #sheet.write(row,column, ) #S 采购渠道

                column = column +1
                sheet.write(row,column,qs.SupplierID ) #T 供应商名称

                column = column +1
                #先找子sku有没有
                dj = qs.UnitPrice
                if  mainsku_sku_obj.UnitPrice is not None and mainsku_sku_obj.UnitPrice >0:
                    dj = mainsku_sku_obj.UnitPrice
                sheet.write(row,column,dj ) #U 成本单价(元)  就是单价 子SKU简单覆盖

                column = column +1
                #sheet.write(row,column,qs.UnitPrice ) #V 批发价格(美元)

                column = column +1
                #sheet.write(row,column,qs.UnitPrice ) #W 零售价格(美元)

                column = column +1
                #sheet.write(row,column,qs.UnitPrice ) #X 最低售价(美元)

                column = column +1
                #sheet.write(row,column,qs.UnitPrice ) #Y 最高售价(美元)

                column = column +1
                #sheet.write(row,column,qs.UnitPrice ) #Z 市场参考价(美元)

                column = column +1
                sheet.write(row,column,u'%s  \n  %s  \n   %s   \n %s'%(qs.Remark,qs.LWH,qs.SupplierPUrl1,qs.SupplierPUrl2 )) #AA 备注

                column = column +1
                sheet.write(row,column,qs.ReportName2 ) #AB 中文申报名

                column = column +1
                sheet.write(row,column,qs.ReportName ) #AC 英文申报名

                column = column +1
                if dj is None:
                    dj =0
                sheet.write(row,column,int(float(dj)/SBBL)+1  ) #AD 申报价值(美元)

                column = column +1
                sheet.write(row,column,'CN' ) #AE 原产国代码

                column = column +1
                sheet.write(row,column,'China' ) #AF 原产国

                column = column +1
                #sheet.write(row,column,100 ) #AG 库存上限

                column = column +1
                #sheet.write(row,column,5 ) #AH 库存下限

                column = column +1
                #sheet.write(row,column,qs.StaffID ) #AI 业绩归属人1
                t_product_oplog_obj1=t_product_oplog.objects.filter(StepID='DY',pid=qs.id)[0:1]
                t_product_oplog_obj2=t_product_oplog.objects.filter(MainSKU=qs.MainSKU,StepID='JZL',pid=qs.id)[0:1]
                #修改相同的业绩归属人1和2
                if t_product_oplog_obj1 is not None and len(t_product_oplog_obj1) > 0 and t_product_oplog_obj2 is not None and len(t_product_oplog_obj2) > 0 and t_product_oplog_obj1[0].OpName == t_product_oplog_obj2[0].OpName:
                    #sheet.write(row,column,t_product_oplog_obj1[0].OpName) #AI 业绩归属人1
                    pass
                else:
                    sheet.write(row,column,t_product_oplog_obj1[0].OpName) #AI 业绩归属人1

                column = column +1
                #sheet.write(row,column,qs.StaffID )
                if t_product_oplog_obj2 is not None and len(t_product_oplog_obj2) > 0:
                    sheet.write(row,column,t_product_oplog_obj2[0].OpName) #AJ 业绩归属人2


                column = column +1
                gg = ''
                if B_PackInfo_obj is not None:
                    gg =  B_PackInfo_obj.PackName
                sheet.write(row,column,gg ) #AK 包装规格
                """
                #包装1 14*14快递袋2g+3层起泡沫6g
                if t_sys_packing_obj is not None :
                    if t_sys_packing_obj.PackName == u'共济膜信封':
                        gg = gg + u'%s%s%sg'%(t_sys_packing_obj.PackStandard,t_sys_packing_obj.PackName,round(t_sys_packing_obj.Weight,1))
                    else:
                        gg = gg + u'%s%s%dg'%(t_sys_packing_obj.PackStandard,t_sys_packing_obj.PackName,round(t_sys_packing_obj.Weight))

               #附加包装
                if t_sys_packing2_obj is not None :
                    if t_sys_packing2_obj.Unit == u'层':
                        gg = gg + u'+%s%s%s%dg'%(qs.PackingID2Num,t_sys_packing2_obj.Unit,t_sys_packing2_obj.PackName,round(qs.PackingID2Num*t_sys_packing2_obj.Weight))
                    else:
                        gg = gg + u'+%s%s%s%s%dg'%(t_sys_packing2_obj.PackStandard,t_sys_packing2_obj.PackName,qs.PackingID2Num,t_sys_packing2_obj.Unit,round(qs.PackingID2Num*t_sys_packing2_obj.Weight))

                sheet.write(row,column,gg ) #AK 包装规格
                """
                column = column +1
                sheet.write(row,column,qs.UpdateTime.strftime('%Y-%m-%d') ) #AL 开发日期

                column = column +1
                #sheet.write(row,column,qs.UpdateTime ) #AM SKU款式1

                column = column +1
                #sheet.write(row,column,qs.UpdateTime ) #AN SKU款式2

                column = column +1
                #sheet.write(row,column,qs.UpdateTime ) #AO SKU款式3

                column = column +1
                #sheet.write(row,column,qs.UpdateTime ) #AP SKU描述

                column = column +1
                #sheet.write(row,column,qs.UpdateTime ) #AQ 图片URL

                column = column +1
                sheet.write(row,column,qs.Buyer ) #AR 采购员

                column = column +1
                sheet.write(row,column, qs.Storehouse) #AS 发货仓库

                column = column +1
                sheet.write(row,column,qs.OrderDays ) #AT 采购到货天数

                column = column +1
                #计算内包装成本
                cb = 0
                if B_PackInfo_obj is not None:
                    cb = cb + B_PackInfo_obj.CostPrice
                sheet.write(row,column,u'%s'%(cb) ) #AU 内包装成本
                """
                #包装1
                if t_sys_packing_obj is not None and t_sys_packing_obj.Price is not None:
                    cb = cb + t_sys_packing_obj.Price
                #附加包装
                if t_sys_packing2_obj is not None and t_sys_packing2_obj.Price is not None and  qs.PackingID2Num is not None:
                    cb = cb + t_sys_packing2_obj.Price * qs.PackingID2Num

                sheet.write(row,column,u'%s'%(cb) ) #AU 内包装成本
                """

                column = column +1
                #sheet.write(row,column, qs.SourceURL ) #AV 网页URL

                column = column +1
                #sheet.write(row,column,qs.SupplierPUrl1 ) #AW 网页URL2

                column = column +1
                #sheet.write(row,column, qs.SupplierPUrl2 ) #AX 网页URL3

                column = column +1
                #sheet.write(row,column,u'待定' ) #AY 最低采购价格

                column = column +1
                #sheet.write(row,column,u'待定' ) #AZ 海关编码

                column = column +1
                sheet.write(row,column,qs.StockAlarmDays ) #BA 库存预警销售周期

                column = column +1
                sheet.write(row,column,qs.MinOrder ) #BB 采购最小订货量

                column = column +1
                #sheet.write(row,column,qs.MinOrder ) #BC 内盒长
                column = column +1
                #sheet.write(row,column,qs.MinOrder ) #BD 内盒宽
                column = column +1
                #sheet.write(row,column,qs.MinOrder ) #BE 内盒高
                column = column +1
                #sheet.write(row,column,qs.MinOrder ) #BF 内盒毛重
                column = column +1
                #sheet.write(row,column,qs.MinOrder ) #BG 内盒净重
                column = column +1
                #sheet.write(row,column,qs.MinOrder ) #BH 外箱长
                column = column +1
                #sheet.write(row,column,qs.MinOrder ) #BI 外箱宽
                column = column +1
                #sheet.write(row,column,qs.MinOrder ) #BJ 外箱高
                column = column +1
                #sheet.write(row,column,qs.MinOrder ) #BK 外箱毛重
                column = column +1
                #sheet.write(row,column,qs.MinOrder ) #BL 外箱净重
                column = column +1
                #sheet.write(row,column,qs.MinOrder ) #BM 商品URL
                column = column +1
                #sheet.write(row,column,qs.MinOrder ) #BN 包装事项

                column = column +1
                sheet.write(row,column,qs.Electrification ) #BO 是否带电

                column = column +1
                sheet.write(row,column,u'正常' ) #BP 商品SKU状态

                column = column +1
                #sheet.write(row,column,u'正常' ) #BQ 工号权限

                column = column +1
                #sheet.write(row,column,u'正常' ) #BR 季节

                column = column +1
                sheet.write(row,column,qs.Powder ) #BS 是否粉末

                column = column +1
                sheet.write(row,column,qs.Liquid ) #BT 是否液体

                column = column +1
                #sheet.write(row,column,u'正常' ) #BU 责任归属人1

                column = column +1
                sheet.write(row,column,qs.possessMan2 ) #BV 责任归属人2

                column = column +1
                #sheet.write(row,column,u'正常' ) #BW 店铺名称
                column = column +1
                #sheet.write(row,column,u'正常' ) #BX UPC码
                column = column +1
                #sheet.write(row,column,u'正常' ) #BY ASIN码
                column = column +1
                #sheet.write(row,column,u'正常' ) #BZ 网页URL4
                column = column +1
                #sheet.write(row,column,u'正常' ) #CA 网页URL5
                column = column +1
                #sheet.write(row,column,u'正常' ) #CB 网页URL6
                column = column +1
                #sheet.write(row,column,u'正常' ) #CC 店铺运费
                column = column +1
                #sheet.write(row,column,u'正常' ) #CD 包装材料重量
                column = column +1
                #sheet.write(row,column,u'正常' ) #CE 汇率
                column = column +1
                #sheet.write(row,column,u'正常' ) #CF 物流公司价格
                column = column +1
                #sheet.write(row,column,u'正常' ) #CG 交易费
                column = column +1
                #sheet.write(row,column,u'正常' ) #CH 毛利率
                column = column +1
                #sheet.write(row,column,u'正常' ) #CI 计算售价



        filename = request.user.username + '_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.xls'
        w.save(path + '/' +  filename)
        os.popen(r'chmod 777 %s'%(path + '/' +  filename))

        #上传oss对象
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_XLS)
        bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)
        #删除现有的
        for  object_info in oss2.ObjectIterator(bucket,prefix='%s/%s_'%(request.user.username,request.user.username)):
            bucket.delete_object(object_info.key)
        bucket.put_object(u'%s/%s'%(request.user.username,filename),open(path + '/' +  filename))

        self.message_user(request,u'%s%s.%s/%s/%s'%(PREFIX,BUCKETNAME_XLS,ENDPOINT_OUT,request.user.username,filename) + u':成功导出,可点击Download下载到本地............................。' )
    to_exort_ed.short_description = u'导出EXCEL'

    def to_enter_ed(self, request, queryset):
        for querysetid in queryset.all():
            obj = t_product_enter_ed()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID= request.user.username
            obj.save()

            end_t_product_oplog(request,querysetid.MainSKU,'LR',querysetid.Name2,querysetid.id)
            begin_t_product_oplog(request,querysetid.MainSKU,'BMLY',querysetid.Name2,querysetid.id)
            querysetid.delete()
    to_enter_ed.short_description = u'录入完成'

    def show_oplog(self,obj) :
        rt = ''
        t_product_oplog_objs = t_product_oplog.objects.filter(pid=obj.id,StepID='JZL').order_by('id')
        for t_product_oplog_obj in t_product_oplog_objs:
            rt = u'%s%s:%s,'%(rt,t_product_oplog_obj.StepName,t_product_oplog_obj.OpName)
        return rt
    show_oplog.short_description = u'操作历史'

    def show_skulist(self,obj) :
        rt = '<table  style="text-align:center"><tr><th style="text-align:center">子SKU</th><th style="text-align:center">属性</th><th style="text-align:center">单价</th><th style="text-align:center">克重</th><th style="text-align:center">包装规格</th><th style="text-align:center">内包装成本</th></tr>'
        t_product_mainsku_sku_objs = t_product_mainsku_sku.objects.filter(pid=obj.id).order_by('SKU')

        for t_product_mainsku_sku_obj in t_product_mainsku_sku_objs:
            PackName =''
            CostPrice =0
            PackNID= t_product_mainsku_sku_obj.PackNID
            try:
                if PackNID > 0 :
                    B_PackInfo_obj = B_PackInfo.objects.get(id__exact = PackNID)
                    if B_PackInfo_obj is not None:
                        PackName =  B_PackInfo_obj.PackName
                        CostPrice = B_PackInfo_obj.CostPrice
            except:
                pass
            rt =  '%s <tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr> '%(rt,t_product_mainsku_sku_obj.SKU,t_product_mainsku_sku_obj.SKUATTRS,t_product_mainsku_sku_obj.UnitPrice,t_product_mainsku_sku_obj.Weight,PackName,CostPrice)


        rt = '%s</table>'%rt
        return mark_safe(rt)
    show_skulist.short_description = mark_safe('<p align="center"> 子SKU信息</p>')

    def show_PackName(self,obj) :
        rt = ''
        PackNID= obj.PackNID
        if PackNID <=0 :
            return rt
        B_PackInfo_obj = B_PackInfo.objects.get(id__exact = PackNID)
        if B_PackInfo_obj is not None:
            rt =  B_PackInfo_obj.PackName
        return rt
    show_PackName.short_description = u'包装规格'

    def show_CostPrice(self,obj) :
        rt = ''
        PackNID= obj.PackNID
        if PackNID <=0 :
            return rt
        B_PackInfo_obj = B_PackInfo.objects.get(id__exact = PackNID)
        if B_PackInfo_obj is not None:
            rt =  B_PackInfo_obj.CostPrice
        return rt
    show_CostPrice.short_description = u'内包装成本'

    def show_Remark(self,obj) :
        return mark_safe(u'%s<br>%s<br>%s<br>%s'%(obj.Remark,obj.LWH,obj.SupplierPUrl1,obj.SupplierPUrl2 ))
    show_Remark.short_description = u'备注'

    def show_wjp(self,obj) :
        rt =''
        if obj.Electrification ==u'是' :
            rt = rt + u'带电;'
        if  obj.Powder ==u'是' :
            rt = rt + u'粉末;'
        if  obj.Liquid ==u'是' :
            rt = rt + u'液体;'
        if obj.Magnetism ==u'是' :
            rt = rt + u'带磁;'
        return rt
    show_wjp.short_description = u'违禁品'

    def show_name2(self,obj) :
        PrepackMark = obj.PrepackMark
        if PrepackMark is None:
            PrepackMark=''
        Name2 = obj.Name2
        if obj.Electrification ==u'是' or obj.Powder ==u'是' or obj.Liquid ==u'是' or obj.Magnetism ==u'是' :
            if obj.SmallCategory != u'手表': #手表特殊
                wjp = u'-违禁品'
                return u'%s%s%s'%(Name2,wjp,PrepackMark)
        return u'%s%s'%(Name2,PrepackMark)
    show_name2.short_description = mark_safe(u'商品<br>名称<br>(中文)')

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'6'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':6})},
        models.URLField:  {'widget': TextInput(attrs={'size':'6'})},
        }

    list_display= ('id','CreateTime','CreateStaffName','SourcePicPath2','MainSKU','Buyer','possessMan2','SpecialRemark','PrepackMark','show_skulist','LargeCategory','SmallCategory','show_name2','Material','SupplierArtNO','Unit','MinPackNum','SupplierID','Keywords2','Keywords','ReportName','ReportName2','show_oplog','show_wjp','show_Remark',)
    list_display_links= ('id','SourcePicPath2',)#,'MainSKU','LargeCategory','SmallCategory','Name2','Material','SupplierArtNO','Unit','MinPackNum','SupplierID','Keywords2','Keywords',)
    list_editable=('SpecialRemark','Buyer','possessMan2',)
    readonly_fields = ('id',)
    search_fields=('id','MainSKU','Name2','StaffID',)
    #list_filter = ('UpdateTime',)
    # 分组表单
    fieldsets = (
        (u'调研结果', {
            'fields': (
                ('id',),
                ('SourceURL','OrdersLast7Days','Keywords','Keywords2','SurveyRemark','Pricerange','ShelveDay', ),
                ('Name','Tags',),
                ('SourcePicPath',),
                       ),
                }),

        (u'开发结果', {
            'fields': (
                ('SupplierPUrl1','SupplierPDes','SupplierID',),
                ('SourcePicPath2',)
                       ),
                }),

        (u'询价结果', {
            'fields': (
                ('UnitPrice','Weight','SpecialSell',),
                       ),
                }),

       	(u'建资料', {
            'fields': (
                    ('Name2','PrepackMark','Material','Unit',),
                    ('MinOrder','SupplierArtNO','SupplierPColor','SupplierPUrl2',),
                    ('OrderDays','StockAlarmDays',),
                    ('LWH','SupplierContact','Storehouse',),
                    ('Buyer','possessMan2',),
                       ),
                }),
        (u'包装规格', {
            'fields': (
                ('MinPackNum',),
                       ),
                }),
        (u'违禁品属性', {
            'fields': (
                ('Electrification','Powder','Liquid','Magnetism',),
                       ),
                }),
        (u'备注信息', {'fields': ('Remark',)}),

        (u'SKU信息', {
            'fields': (
                ('LargeCategory','SmallCategory','Category3','MainSKU','SKU',),
                       ),
                }),
     )

    #def save_model(self, request, obj, form, change):
    def save_models(self):
        obj = self.new_obj
        request = self.request
        obj.StaffID = request.user.username
        obj.save()


class t_product_enter_ed_Admin(t_product_Admin):
    StepID = 'BMLY'
    StepName = u'部门领用'
    actions = ['to_depart_use',]
    def to_all(self, request, queryset,pname):
        cursor = connection.cursor() #
        for querysetid in queryset.all():
            sku = querysetid.SKU
            if sku != querysetid.MainSKU :
                sku = '%s%s'%(querysetid.MainSKU,querysetid.SKU)

            sql = 'insert into t_product_publish_ed(SourcePicPath2,SKU,MainSKU,Name,Name2,PlatformName,UpdateTime,StaffID,StaffName,pid) '
            sql += ' values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'%(querysetid.SourcePicPath2,sku,querysetid.MainSKU,querysetid.Name,querysetid.Name2,pname,datetime.utcnow(),request.user.username,request.user.first_name,querysetid.id)
            cursor.execute(sql)
        cursor.close()


    # ('Wish', 'Wish'),
    # ('Amazon', 'Amazon'),
    # ('Aliexpress', 'Aliexpress'),
    # ('eBay', 'eBay'),
    # ('Lazada', 'Lazada'),
    # ('1688', '1688'),
    #  ('Esty', 'Esty'),
    #  ('Others', 'Others'),
    #

#
    def to_depart_use(self, request, queryset):
        cursor = connection.cursor() #
        for querysetid in queryset.all():

            sku = querysetid.SKU
            if sku != querysetid.MainSKU :
                sku = '%s%s'%(querysetid.MainSKU,querysetid.SKU)

            t_sys_department_staff_objs = t_sys_department_staff.objects.filter(StaffID=request.user.username)
            if  t_sys_department_staff_objs.count() <=  0 :
                continue #没找到部门

            dptmtid = t_sys_department_staff_objs[0].DepartmentID
            t_product_depart_use_objs = t_product_depart_use.objects.filter(pid=querysetid.id,DepartmentID=dptmtid)
            if t_product_depart_use_objs.count() > 0 : #已领过
                continue
            sql = 'insert into t_product_depart_use(SourcePicPath2,SKU,MainSKU,Name2,DepartmentID,UpdateTime,StaffID,StaffName,pid) '
            sql += ' values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'%(querysetid.SourcePicPath2,sku,querysetid.MainSKU,querysetid.Name2,dptmtid,datetime.utcnow(),request.user.username,request.user.first_name,querysetid.id)
            cursor.execute(sql)
        cursor.close()
    to_depart_use.short_description = u'本部门领用'


    def to_exort_ed(self, request, queryset):
        from xlwt import *
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        #if not os.path.exists(path):
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s'%(MEDIA_ROOT + 'download_xls'))

        mkdir_p(path)
        os.popen('chmod 777 %s'%(path))

        w = Workbook()
        sheet = w.add_sheet('sku')

        for index,item in enumerate(XLS_FIELDS):
            sheet.write(0,index,item)

        #写数据
        row = 0

        for qs in queryset:


            #根据主SKU查找子sku
            t_product_mainsku_sku_objs = t_product_mainsku_sku.objects.filter(MainSKU =  qs.MainSKU)

            for  mainsku_sku_obj in t_product_mainsku_sku_objs :
                row = row +1
                column = 0
                sheet.write(row,column,u'add') #A 操作类型

                column = column +1
                if qs.MainSKU == mainsku_sku_obj.SKU :
                    sheet.write(row,column,'%s'%(qs.MainSKU)) #B 商品编码
                else:
                    sheet.write(row,column,'%s%s'%(qs.MainSKU,mainsku_sku_obj.SKU)) #B 商品编码

                column = column +1
                if qs.MainSKU == mainsku_sku_obj.SKU :
                    sheet.write(row,column,'%s'%(qs.MainSKU)) #C SKU
                else:
                    sheet.write(row,column,'%s%s'%(qs.MainSKU,mainsku_sku_obj.SKU)) #C SKU


                column = column +1
                sheet.write(row,column,u'否') #D 多款式

                column = column +1
                sheet.write(row,column,u'否') #E 是否有样品

                column = column +1
                #sheet.write(row,column,1) #F 样品数量

                column = column +1
                sheet.write(row,column,qs.LargeCategory) #G 大类名称

                column = column +1
                sheet.write(row,column,qs.SmallCategory) #H 小类名称



                column = column +1
                #sheet.write(row,column,qs.Name) #I 商品名称
                wjp = ''
                if qs.Electrification ==u'是' or qs.Powder ==u'是' or qs.Liquid ==u'是' or qs.Magnetism ==u'是' :
                    if qs.SmallCategory != u'手表': #手表特殊
                        wjp = u'-违禁品'
                PrepackMark = qs.PrepackMark
                if PrepackMark is None:
                    PrepackMark=''
                sheet.write(row,column,u'%s-%s%s%s'%(qs.Name2,mainsku_sku_obj.SKUATTRS,wjp,PrepackMark)) #I 商品名称


                column = column +1
                sheet.write(row,column,u'正常') #J 当前状态

                column = column +1
                sheet.write(row,column,qs.Material) #K 材质

                column = column +1
                #sheet.write(row,column,'%s'%(qs.LWH) ) #L 规格


                column = column +1
                sheet.write(row,column, '%s'%(qs.SupplierArtNO)) #M 型号

                column = column +1
                #sheet.write(row,column, u'款式' ) #N 款式

                column = column +1
                sheet.write(row,column, 'fancyqube' ) #O 品牌

                column = column +1
                sheet.write(row,column, qs.Unit) #P 单位

                column = column +1
                #zxbzs = 1
                #if qs.Unit ==u'对':
                #    zxbzs = 2
                #sheet.write(row,column, zxbzs ) #Q 最小包装数
                sheet.write(row,column, qs.MinPackNum )

                column = column +1

                weight = 0
                if  qs.Weight is not None and qs.Weight >0:
                    weight = qs.Weight
                if  mainsku_sku_obj.Weight is not None and mainsku_sku_obj.Weight >0:
                    weight = mainsku_sku_obj.Weight

                PackNID= mainsku_sku_obj.PackNID
                if PackNID <=0 :
                    PackNID = qs.PackNID
                B_PackInfo_obj = None
                try:
                    B_PackInfo_obj = B_PackInfo.objects.get(id__exact = PackNID)
                    if B_PackInfo_obj is not None:
                        weight = weight + B_PackInfo_obj.Weight

                except:
                    pass
                sheet.write(row,column,u'%s'%(weight)) #R 重量(G)
                """
                t_sys_packing_obj = None
                t_sys_packing2_obj = None
                if qs.PackingID_id is not None :
                    t_sys_packing_obj  = t_sys_packing.objects.get(id__exact = qs.PackingID_id)
                    if  t_sys_packing_obj is not None and t_sys_packing_obj.Weight is not None  :
                        weight = weight + t_sys_packing_obj.Weight

                #附加包装
                if qs.PackingID2Num is not None and qs.PackingID2Num > 0 and qs.PackingID2_id is not None:
                    t_sys_packing2_obj  = t_sys_packing2.objects.get(id__exact = qs.PackingID2_id)
                    if  t_sys_packing2_obj is not None  and t_sys_packing2_obj.Weight is not None and qs.PackingID2Num is not None :
                        weight = weight + t_sys_packing2_obj.Weight * qs.PackingID2Num
                sheet.write(row,column,u'%s'%(weight)) #R 重量(G)
                """

                column = column +1
                #sheet.write(row,column, ) #S 采购渠道

                column = column +1
                sheet.write(row,column,qs.SupplierID ) #T 供应商名称

                column = column +1
                #先找子sku有没有
                dj = qs.UnitPrice
                if  mainsku_sku_obj.UnitPrice is not None and mainsku_sku_obj.UnitPrice >0:
                    dj = mainsku_sku_obj.UnitPrice
                sheet.write(row,column,dj ) #U 成本单价(元)  就是单价 子SKU简单覆盖

                column = column +1
                #sheet.write(row,column,qs.UnitPrice ) #V 批发价格(美元)

                column = column +1
                #sheet.write(row,column,qs.UnitPrice ) #W 零售价格(美元)

                column = column +1
                #sheet.write(row,column,qs.UnitPrice ) #X 最低售价(美元)

                column = column +1
                #sheet.write(row,column,qs.UnitPrice ) #Y 最高售价(美元)

                column = column +1
                #sheet.write(row,column,qs.UnitPrice ) #Z 市场参考价(美元)

                column = column +1
                sheet.write(row,column,u'%s  \n  %s  \n   %s   \n %s'%(qs.Remark,qs.LWH,qs.SupplierPUrl1,qs.SupplierPUrl2 )) #AA 备注

                column = column +1
                sheet.write(row,column,qs.ReportName2 ) #AB 中文申报名

                column = column +1
                sheet.write(row,column,qs.ReportName ) #AC 英文申报名

                column = column +1
                if dj is None:
                    dj =0
                sheet.write(row,column,int(float(dj)/SBBL)+1  ) #AD 申报价值(美元)

                column = column +1
                sheet.write(row,column,'CN' ) #AE 原产国代码

                column = column +1
                sheet.write(row,column,'China' ) #AF 原产国

                column = column +1
                #sheet.write(row,column,100 ) #AG 库存上限

                column = column +1
                #sheet.write(row,column,5 ) #AH 库存下限

                column = column +1
                #sheet.write(row,column,qs.StaffID ) #AI 业绩归属人1
                t_product_oplog_obj1=t_product_oplog.objects.filter(StepID='DY',pid=qs.id)[0:1]
                t_product_oplog_obj2=t_product_oplog.objects.filter(MainSKU=qs.MainSKU,StepID='JZL',pid=qs.id)[0:1]
                #修改相同的业绩归属人1和2
                if t_product_oplog_obj1 is not None and len(t_product_oplog_obj1) > 0 and t_product_oplog_obj2 is not None and len(t_product_oplog_obj2) > 0 and t_product_oplog_obj1[0].OpName == t_product_oplog_obj2[0].OpName:
                    #sheet.write(row,column,t_product_oplog_obj1[0].OpName) #AI 业绩归属人1
                    pass
                else:
                    sheet.write(row,column,t_product_oplog_obj1[0].OpName) #AI 业绩归属人1

                column = column +1
                #sheet.write(row,column,qs.StaffID )
                if t_product_oplog_obj2 is not None and len(t_product_oplog_obj2) > 0:
                    sheet.write(row,column,t_product_oplog_obj2[0].OpName) #AJ 业绩归属人2


                column = column +1
                gg = ''
                if B_PackInfo_obj is not None:
                    gg =  B_PackInfo_obj.PackName
                sheet.write(row,column,gg ) #AK 包装规格
                """
                #包装1 14*14快递袋2g+3层起泡沫6g
                if t_sys_packing_obj is not None :
                    if t_sys_packing_obj.PackName == u'共济膜信封':
                        gg = gg + u'%s%s%sg'%(t_sys_packing_obj.PackStandard,t_sys_packing_obj.PackName,round(t_sys_packing_obj.Weight,1))
                    else:
                        gg = gg + u'%s%s%dg'%(t_sys_packing_obj.PackStandard,t_sys_packing_obj.PackName,round(t_sys_packing_obj.Weight))

               #附加包装
                if t_sys_packing2_obj is not None :
                    if t_sys_packing2_obj.Unit == u'层':
                        gg = gg + u'+%s%s%s%dg'%(qs.PackingID2Num,t_sys_packing2_obj.Unit,t_sys_packing2_obj.PackName,round(qs.PackingID2Num*t_sys_packing2_obj.Weight))
                    else:
                        gg = gg + u'+%s%s%s%s%dg'%(t_sys_packing2_obj.PackStandard,t_sys_packing2_obj.PackName,qs.PackingID2Num,t_sys_packing2_obj.Unit,round(qs.PackingID2Num*t_sys_packing2_obj.Weight))

                sheet.write(row,column,gg ) #AK 包装规格
                """
                column = column +1
                sheet.write(row,column,qs.UpdateTime.strftime('%Y-%m-%d') ) #AL 开发日期

                column = column +1
                #sheet.write(row,column,qs.UpdateTime ) #AM SKU款式1

                column = column +1
                #sheet.write(row,column,qs.UpdateTime ) #AN SKU款式2

                column = column +1
                #sheet.write(row,column,qs.UpdateTime ) #AO SKU款式3

                column = column +1
                #sheet.write(row,column,qs.UpdateTime ) #AP SKU描述

                column = column +1
                #sheet.write(row,column,qs.UpdateTime ) #AQ 图片URL

                column = column +1
                sheet.write(row,column,qs.Buyer ) #AR 采购员

                column = column +1
                sheet.write(row,column, qs.Storehouse) #AS 发货仓库

                column = column +1
                sheet.write(row,column,qs.OrderDays ) #AT 采购到货天数

                column = column +1
                #计算内包装成本
                cb = 0
                if B_PackInfo_obj is not None:
                    cb = cb + B_PackInfo_obj.CostPrice
                sheet.write(row,column,u'%s'%(cb) ) #AU 内包装成本
                """
                #包装1
                if t_sys_packing_obj is not None and t_sys_packing_obj.Price is not None:
                    cb = cb + t_sys_packing_obj.Price
                #附加包装
                if t_sys_packing2_obj is not None and t_sys_packing2_obj.Price is not None and  qs.PackingID2Num is not None:
                    cb = cb + t_sys_packing2_obj.Price * qs.PackingID2Num

                sheet.write(row,column,u'%s'%(cb) ) #AU 内包装成本
                """

                column = column +1
                #sheet.write(row,column, qs.SourceURL ) #AV 网页URL

                column = column +1
                #sheet.write(row,column,qs.SupplierPUrl1 ) #AW 网页URL2

                column = column +1
                #sheet.write(row,column, qs.SupplierPUrl2 ) #AX 网页URL3

                column = column +1
                #sheet.write(row,column,u'待定' ) #AY 最低采购价格

                column = column +1
                #sheet.write(row,column,u'待定' ) #AZ 海关编码

                column = column +1
                sheet.write(row,column,qs.StockAlarmDays ) #BA 库存预警销售周期

                column = column +1
                sheet.write(row,column,qs.MinOrder ) #BB 采购最小订货量

                column = column +1
                #sheet.write(row,column,qs.MinOrder ) #BC 内盒长
                column = column +1
                #sheet.write(row,column,qs.MinOrder ) #BD 内盒宽
                column = column +1
                #sheet.write(row,column,qs.MinOrder ) #BE 内盒高
                column = column +1
                #sheet.write(row,column,qs.MinOrder ) #BF 内盒毛重
                column = column +1
                #sheet.write(row,column,qs.MinOrder ) #BG 内盒净重
                column = column +1
                #sheet.write(row,column,qs.MinOrder ) #BH 外箱长
                column = column +1
                #sheet.write(row,column,qs.MinOrder ) #BI 外箱宽
                column = column +1
                #sheet.write(row,column,qs.MinOrder ) #BJ 外箱高
                column = column +1
                #sheet.write(row,column,qs.MinOrder ) #BK 外箱毛重
                column = column +1
                #sheet.write(row,column,qs.MinOrder ) #BL 外箱净重
                column = column +1
                #sheet.write(row,column,qs.MinOrder ) #BM 商品URL
                column = column +1
                #sheet.write(row,column,qs.MinOrder ) #BN 包装事项

                column = column +1
                sheet.write(row,column,qs.Electrification ) #BO 是否带电

                column = column +1
                sheet.write(row,column,u'正常' ) #BP 商品SKU状态

                column = column +1
                #sheet.write(row,column,u'正常' ) #BQ 工号权限

                column = column +1
                #sheet.write(row,column,u'正常' ) #BR 季节

                column = column +1
                sheet.write(row,column,qs.Powder ) #BS 是否粉末

                column = column +1
                sheet.write(row,column,qs.Liquid ) #BT 是否液体

                column = column +1
                #sheet.write(row,column,u'正常' ) #BU 责任归属人1

                column = column +1
                sheet.write(row,column,qs.possessMan2 ) #BV 责任归属人2

                column = column +1
                #sheet.write(row,column,u'正常' ) #BW 店铺名称
                column = column +1
                #sheet.write(row,column,u'正常' ) #BX UPC码
                column = column +1
                #sheet.write(row,column,u'正常' ) #BY ASIN码
                column = column +1
                #sheet.write(row,column,u'正常' ) #BZ 网页URL4
                column = column +1
                #sheet.write(row,column,u'正常' ) #CA 网页URL5
                column = column +1
                #sheet.write(row,column,u'正常' ) #CB 网页URL6
                column = column +1
                #sheet.write(row,column,u'正常' ) #CC 店铺运费
                column = column +1
                #sheet.write(row,column,u'正常' ) #CD 包装材料重量
                column = column +1
                #sheet.write(row,column,u'正常' ) #CE 汇率
                column = column +1
                #sheet.write(row,column,u'正常' ) #CF 物流公司价格
                column = column +1
                #sheet.write(row,column,u'正常' ) #CG 交易费
                column = column +1
                #sheet.write(row,column,u'正常' ) #CH 毛利率
                column = column +1
                #sheet.write(row,column,u'正常' ) #CI 计算售价



        filename = request.user.username + '_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.xls'
        w.save(path + '/' +  filename)
        os.popen(r'chmod 777 %s'%(path + '/' +  filename))

        #上传oss对象
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_XLS)
        bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)
        #删除现有的
        for  object_info in oss2.ObjectIterator(bucket,prefix='%s/%s_'%(request.user.username,request.user.username)):
            bucket.delete_object(object_info.key)
        bucket.put_object(u'%s/%s'%(request.user.username,filename),open(path + '/' +  filename))

        self.message_user(request,u'%s%s.%s/%s/%s'%(PREFIX,BUCKETNAME_XLS,ENDPOINT_OUT,request.user.username,filename) + u':成功导出,可点击Download下载到本地............................。' )
    to_exort_ed.short_description = u'补导出EXCEL'

    def department_use_log(self,obj):
        rt = ''
        t_product_depart_use_objs = t_product_depart_use.objects.filter(pid=obj.id).order_by('DepartmentID')
        for t_product_depart_use_obj in t_product_depart_use_objs:
            rt = u'%s{%s-%s},'%(rt,t_product_depart_use_obj.DepartmentID,t_product_depart_use_obj.StaffName)
        return rt
    department_use_log.short_description = u'部门领用记录'

    def get_queryset(self, request):

        if request.user.is_superuser:
            qs = super(t_product_enter_ed_Admin, self).get_queryset(request)
            return qs


        t_sys_department_staff_objs = t_sys_department_staff.objects.filter(StaffID=request.user.username)
        if t_sys_department_staff_objs.count() <=0 :
            self.message_user(request,u'你没有部门数据,请联系管理员正确录入部门信息！')
            return t_product_enter_ed.objects.none()

        #找本部门领用 idlist
        idlist = []
        t_product_depart_use_objs = t_product_depart_use.objects.filter(DepartmentID=t_sys_department_staff_objs[0].DepartmentID)
        for t_product_depart_use_obj in t_product_depart_use_objs:
            idlist.append(t_product_depart_use_obj.pid)

        qs = super(t_product_enter_ed_Admin, self).get_queryset(request).exclude(id__in=idlist)
        return qs

    def show_oplog(self,obj) :
        rt = ''
        t_product_oplog_objs = t_product_oplog.objects.filter(pid=obj.id).order_by('id')
        for t_product_oplog_obj in t_product_oplog_objs:
            rt = u'%s%s:%s,'%(rt,t_product_oplog_obj.StepName,t_product_oplog_obj.OpName)
        return rt
    show_oplog.short_description = u'操作历史'

    def show_skulist(self,obj) :
        rt = '<table  style="text-align:center"><tr><th style="text-align:center">子SKU</th><th style="text-align:center">属性</th><th style="text-align:center">单价</th><th style="text-align:center">克重</th><th style="text-align:center">包装规格</th><th style="text-align:center">内包装成本</th></tr>'
        t_product_mainsku_sku_objs = t_product_mainsku_sku.objects.filter(pid=obj.id).order_by('SKU')

        for t_product_mainsku_sku_obj in t_product_mainsku_sku_objs:
            PackName =''
            CostPrice =0
            PackNID= t_product_mainsku_sku_obj.PackNID
            try:
                if PackNID > 0 :
                    B_PackInfo_obj = B_PackInfo.objects.get(id__exact = PackNID)
                    if B_PackInfo_obj is not None:
                        PackName =  B_PackInfo_obj.PackName
                        CostPrice = B_PackInfo_obj.CostPrice
            except:
                pass
            rt =  '%s <tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr> '%(rt,t_product_mainsku_sku_obj.SKU,t_product_mainsku_sku_obj.SKUATTRS,t_product_mainsku_sku_obj.UnitPrice,t_product_mainsku_sku_obj.Weight,PackName,CostPrice)


        rt = '%s</table>'%rt
        return mark_safe(rt)
    show_skulist.short_description = mark_safe('<p align="center"> 子SKU信息</p>')

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':30})},
        models.URLField:  {'widget': TextInput(attrs={'size':'10'})},
        }

    list_display= ('id','CreateTime','CreateStaffName','SourcePicPath2','MainSKU','show_skulist','Keywords','Keywords2','Pricerange','SupplierPUrl1','SupplierPDes','UnitPrice','Weight','SpecialSell','show_oplog','department_use_log',)
    list_display_links=('id','SourcePicPath2','Keywords','Keywords2','Pricerange','SupplierPUrl1','SupplierPDes','UnitPrice','Weight','SpecialSell',)

    readonly_fields = ('id','SKU',)
    search_fields=('id','MainSKU','StaffID','Name2',)
    fieldsets = (
        (u'基本信息', {
            'fields': (
                ('id',),
                ('Keywords','InitialWord', ),
                       ),
                }),
       	(u'反向链接信息', {
            'fields': (
                    ('Name','Name2',),
                    ('PlatformName','PlatformPID'),
                    ('SourceURL',),
                    ('ShelveDay','SourceURLPrice',),
                    ('OrdersLast7Days','SpecialSell',),
                       ),
                }),
        (u'商品信息', {
            'fields': (
                ('SupplierID','SupplierContact','SupplierArtNO',),
                ('SupplierPUrl1','SupplierPUrl2',),
                ('UnitPrice','Unit',),
                ('MinOrder','MinPackNum',),
                ('SupplierPColor','SupplierPDes',),
                ('OrderDays','StockAlarmDays',),
                ('Material','Weight',),
                ('LWH',),
                 ('Electrification','Powder','Liquid','Magnetism',),

                      ),
                }),
        (u'备注信息', {'fields': ('Remark',)}),

        (u'SKU信息', {'fields': ('Category2','MainSKU',)}),
        (u'其他平台反向连接信息', {'fields': ('URLamazon','URLebay','URLexpress','URLwish',)}),
    )

    #def save_model(self, request, obj, form, change):
    def save_models(self):
        obj = self.new_obj
        request = self.request
        obj.StaffID = request.user.username
        obj.save()





class t_product_questions_Adimin(object):
    list_select_related = True
    list_display=('id','PTitle','Priority','ExpectedDay','Status','StaffIDSubmit','StaffIDHandle','StaffID','Description','UpdateTime',)
    list_display_links=('id','PTitle','Priority','Status','StaffIDSubmit','StaffIDHandle','ExpectedDay','StaffID','Description','UpdateTime',)
    search_fields=('id','PTitle','Description',)
    list_filter = ('UpdateTime','StaffIDSubmit','StaffIDHandle','Status','Priority',)

    readonly_fields = ('id','UpdateTime',)

    # 分组表单
    fieldsets = (
        (u'基本信息', {'fields': ('id','PTitle','Priority','ExpectedDay','Status', )}),

        (u'处理人', {'fields': ('StaffIDSubmit','StaffIDHandle',)}),

        (u'问题描述', {'fields': ('Description',)}),
    )

    #def save_model(self, request, obj, form, change):
    def save_models(self):
        obj = self.new_obj
        request = self.request
        import datetime
        now = datetime.datetime.now()
        logger = logging.getLogger('sourceDns.webdns.views')
        obj.StaffID = request.user.username
        obj.save()
        if request.method == 'POST':
            files = request.FILES.getlist('myfiles')
            for f in files :
                path = MEDIA_ROOT + 'questions_pic/' + str(obj.id)
                if not os.path.exists(path):
                    os.mkdir(path)
                destination = open(path + '/' +  f.name,'wb+')
                for chunk in f.chunks():
                  destination.write(chunk)
                destination.close()




class t_product_recycle_Admin(t_product_Admin):

    list_display=('id','CreateTime','CreateStaffName','SourcePicPath','PlatformPID','OrdersLast7Days','Name','Name2','Keywords','Keywords2','Tags','ShelveDay','Pricerange','NumBought','TotalInventory','SpecialRemark','fromT',)   #指定要显示的字段
    list_display_links=('SourcePicPath',)
    list_filter = ('UpdateTime','StaffID',)
    search_fields=('id','MainSKU','StaffID','Name2',)
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':30})},
        }

class t_product_repeats_Admin(t_product_Admin):
    def show_oplog(self,obj) :
        rt = ''
        t_product_oplog_objs = t_product_oplog.objects.filter(pid=obj.id).order_by('id')
        for t_product_oplog_obj in t_product_oplog_objs:
            rt = u'%s%s:%s,'%(rt,t_product_oplog_obj.StepName,t_product_oplog_obj.OpName)
        return rt
    show_oplog.short_description = u'操作历史'

    def show_skulist(self,obj) :
        rt = '<table  style="text-align:center"><tr><th style="text-align:center">子SKU</th><th style="text-align:center">属性</th><th style="text-align:center">单价</th><th style="text-align:center">克重</th><th style="text-align:center">包装规格</th><th style="text-align:center">内包装成本</th></tr>'
        t_product_mainsku_sku_objs = t_product_mainsku_sku.objects.filter(pid=obj.id).order_by('SKU')

        for t_product_mainsku_sku_obj in t_product_mainsku_sku_objs:
            PackName =''
            CostPrice =0
            PackNID= t_product_mainsku_sku_obj.PackNID
            try:
                if PackNID > 0 :
                    B_PackInfo_obj = B_PackInfo.objects.get(id__exact = PackNID)
                    if B_PackInfo_obj is not None:
                        PackName =  B_PackInfo_obj.PackName
                        CostPrice = B_PackInfo_obj.CostPrice
            except:
                pass
            rt =  '%s <tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr> '%(rt,t_product_mainsku_sku_obj.SKU,t_product_mainsku_sku_obj.SKUATTRS,t_product_mainsku_sku_obj.UnitPrice,t_product_mainsku_sku_obj.Weight,PackName,CostPrice)


        rt = '%s</table>'%rt
        return mark_safe(rt)
    show_skulist.short_description = mark_safe('<p align="center"> 子SKU信息</p>')

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':30})},
        }

    list_display= ('id','CreateTime','CreateStaffName','SourcePicPath','SourcePicPath2','SourceURL','SupplierPUrl1','SpecialRemark','MainSKU','show_skulist','UpdateTime','StaffID','Name2','show_oplog',)
    list_display_links= ('SourcePicPath','SourcePicPath2',) #('SourcePicPath2','id','MainSKU','Name2','Keywords','Keywords2','Pricerange','SupplierPUrl1','SupplierPDes','UnitPrice','Weight','SpecialSell',)
    search_fields=('id','MainSKU','Name2','StaffID',)
    #readonly_fields =  ALL_FIELDS_TUPLE
    list_filter = ('UpdateTime',)


class t_product_depart_use_Admin(object):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':30})},
        }


    list_display= ('id','SourcePicPath2','MainSKU','Name2','DepartmentID','UpdateTime','StaffID','StaffName','pid',)
    list_display_links= ('id','SourcePicPath2','MainSKU','Name2','DepartmentID','UpdateTime','StaffID','StaffName',)

    readonly_fields = ('id','SourcePicPath2','MainSKU','Name2','DepartmentID','UpdateTime','StaffID','StaffName',)
    search_fields=('Name2','MainSKU','pid',)
    def get_queryset(self, request):

        if request.user.is_superuser:
            qs = super(t_product_depart_use_Admin, self).get_queryset(request)
            return qs


        t_sys_department_staff_objs = t_sys_department_staff.objects.filter(StaffID=request.user.username)
        if t_sys_department_staff_objs.count() <=0 :
            self.message_user(request,u'你没有部门数据,请联系管理员正确录入部门信息！')
            return t_product_depart_use.objects.none()

        qs = super(t_product_depart_use_Admin, self).get_queryset(request).filter(DepartmentID=t_sys_department_staff_objs[0].DepartmentID)
        return qs

class t_sys_packing_Admin(object):
    list_select_related = True
    list_display=('id','PackName','PackStandard','Price','Weight','StaffID','UpdateTime')
    list_display_links=('id','PackName','PackStandard','Price','Weight','StaffID','UpdateTime')
    search_fields=('PackName','PackStandard')
    list_filter = ('PackName',)
    readonly_fields = ('id','StaffID','UpdateTime',)
    fieldsets = (
        (u'包装规格信息', {'fields': ('id','PackName','PackStandard','Price','Weight',)}),
    )

class t_sys_category_Admin(object):
    list_select_related = True
    list_display=('CategoryID','CategoryName','PCategoryID',)
    list_display_links=('CategoryID','CategoryName','PCategoryID',)
    search_fields=('CategoryID','CategoryName','PCategoryID',)
    fieldsets = (
        (u'类别信息', {'fields': ('CategoryID','CategoryName','PCategoryID',)}),
    )


class t_sys_sku_seq_Admin(object):
    list_select_related = True
    list_display=('id','CategoryName','CategoryDesc','CategoryPrefix','CurValue',)
    list_display_links=('id','CategoryName','CategoryDesc','CategoryPrefix','CurValue',)
    readonly_fields = ('id',)
    fieldsets = (
        (u'子SKU信息', {'fields': ('id','CategoryName','CategoryDesc','CategoryPrefix','CurValue',)}),
    )
'''
class t_sys_upload_zip_Admin(object):
    list_select_related = True
    list_display=('id','StaffID','UpdateTime','Name','Count',)
    list_display_links=('id','StaffID','UpdateTime','Name','Count',)
    readonly_fields = ('id','StaffID','UpdateTime','Name','Count',)

    fieldsets = (
        (u'子SKU信息', {'fields': ('id','StaffID','UpdateTime','Name','Count',)}),
    )

    #def save_model(self, request, obj, form, change):
    def save_models(self):
        obj = self.new_obj
        request = self.request
        import zipfile
        logger = logging.getLogger('sourceDns.webdns.views')    #刚才在setting.py中配置的logger
        #self.message_user(request,BASE_DIR )

        zipnames = ''
        count = 0
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_ARTED)
        bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)

        if request.method == 'POST':
            files = request.FILES.getlist('upimgzips','')
            for f in files :
                zipnames = f.name
                z = zipfile.ZipFile(f)
                for name in z.namelist() :
                    if not name.endswith (('.jpg','.png')) :
                        continue
                    #self.message_user(request,name)

                    content = z.read(name)
                    bucket.put_object(u'%s'%(name),content)
                    count += 1
                z.close()
        obj.StaffID = request.user.username
        obj.Name = zipnames
        obj.Count = count
        obj.save()
'''
#15)	调研历史表 t_product_survey_history
class t_product_survey_history_Admin(object):
    def show_oplog(self,obj) :
        rt = ''
        t_product_oplog_objs = t_product_oplog.objects.filter(pid=obj.pid).order_by('id')
        for t_product_oplog_obj in t_product_oplog_objs:
            rt = u'%s%s:%s,'%(rt,t_product_oplog_obj.StepName,t_product_oplog_obj.OpName)
        return rt
    show_oplog.short_description = u'操作历史'

    def show_mainsku(self,obj) :
        t_product_oplog_objs = t_product_oplog.objects.filter(pid=obj.pid,StepID='JZL')
        if t_product_oplog_objs.count() > 0 :
            rt = u'%s'%(t_product_oplog_objs[0].MainSKU)
            return rt
    show_mainsku.short_description = u'主SKU'

    list_display=('id','SourcePicPath','SourceURL','UpdateTime','StaffName','show_mainsku','show_oplog',)
    list_display_links=('SourcePicPath',)
    list_filter = ('UpdateTime','StaffName')
    search_fields=('SourceURL',)

#16)	全部商品SKU信息 t_product_allsku
class t_product_allsku_Admin(t_product_Admin):
    def show_oplog(self,obj) :
        rt = ''
        t_product_oplog_objs = t_product_oplog.objects.filter(pid=obj.id).order_by('id')
        for t_product_oplog_obj in t_product_oplog_objs:
            rt = u'%s%s:%s,'%(rt,t_product_oplog_obj.StepName,t_product_oplog_obj.OpName)
        return rt
    show_oplog.short_description = u'操作历史'

    def show_skulist(self,obj) :
        rt = '<table  style="text-align:center"><tr><th style="text-align:center">子SKU</th><th style="text-align:center">属性</th><th style="text-align:center">单价</th><th style="text-align:center">克重</th><th style="text-align:center">包装规格</th><th style="text-align:center">内包装成本</th></tr>'
        t_product_mainsku_sku_objs = t_product_mainsku_sku.objects.filter(pid=obj.id).order_by('SKU')

        for t_product_mainsku_sku_obj in t_product_mainsku_sku_objs:
            PackName =''
            CostPrice =0
            PackNID= t_product_mainsku_sku_obj.PackNID
            try:
                if PackNID > 0 :
                    B_PackInfo_obj = B_PackInfo.objects.get(id__exact = PackNID)
                    if B_PackInfo_obj is not None:
                        PackName =  B_PackInfo_obj.PackName
                        CostPrice = B_PackInfo_obj.CostPrice
            except:
                pass
            rt =  '%s <tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr> '%(rt,t_product_mainsku_sku_obj.SKU,t_product_mainsku_sku_obj.SKUATTRS,t_product_mainsku_sku_obj.UnitPrice,t_product_mainsku_sku_obj.Weight,PackName,CostPrice)


        rt = '%s</table>'%rt
        return mark_safe(rt)
    show_skulist.short_description = mark_safe('<p align="center"> 子SKU信息</p>')

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':30})},
        }

    list_display= ('id','T','CreateTime','CreateStaffName','SourcePicPath2','MainSKU','show_skulist','UpdateTime','StaffID','Name2','fromT','show_oplog',)
    list_display_links= ('SourcePicPath2','SourcePicPath2','MainSKU','UpdateTime','StaffID') #('SourcePicPath2','id','MainSKU','Name2','Keywords','Keywords2','Pricerange','SupplierPUrl1','SupplierPDes','UnitPrice','Weight','SpecialSell',)
    search_fields=('id','MainSKU','Name2','StaffID',)
    #readonly_fields =  ALL_FIELDS_TUPLE
    list_filter = ('UpdateTime','T',)


class t_product_oplog_Admin(object):
    list_select_related = True
    list_display=('id','MainSKU','Name2','OpID','OpName','StepID','StepName','BeginTime','EndTime','pid',)
    list_display_links=('id','MainSKU','Name2','OpID','OpName','StepID','StepName','BeginTime','EndTime','pid',)
    readonly_fields = ('id','MainSKU','Name2','OpID','OpName','StepID','StepName','BeginTime','EndTime','pid',)
    search_fields=('MainSKU','OpName','Name2','StepName','pid',)
    list_filter = ('OpName','StepName','EndTime',)
    fieldsets = (
        (u'操作记录', {'fields': ('id','MainSKU','Name','Name2','OpID','OpName','StepID','StepName','BeginTime','EndTime','pid',)}),
    )

class t_store_plan_Admin(object):
    pass

class t_store_plan_warning_Admin(object):
    pass

class t_autopic_uq_Admin(object):
    list_display=('id','MainSKU','Name','Status','BeginTime','EndTime','Category1_id','pid',)
    readonly_fields = list_display

class t_sys_department_Admin(object):
    list_display=('id','DepartmentID','DepartmentName', )
    readonly_fields = list_display
class t_sys_department_staff_Admin(object):
    list_display=('id','StaffID','DepartmentID',)
    readonly_fields = ('id',)

class t_autopic_uq_ex_Admin(object):
    list_display=('id','MainSKU','PicPath','Rate','pid',)

class t_sys_platform_role_Admin(object):
    list_display=('id','StaffID','PlatformName','StaffName',)
    readonly_fields = ('id','StaffID','StaffName',)
    fieldsets = (
            (u'设置平台角色', {'fields': ('id','StaffID','StaffName','PlatformName',)}),
        )

    #def save_model(self, request, obj, form, change):
    def save_models(self):
        obj = self.new_obj
        request = self.request
        self.message_user(request,  'obj :  %s %s %s'%(obj.StaffID,obj.PlatformName, obj.StaffName) )
        #self.message_user(request,  'form :  %s %s %s'%(form.StaffID,form.PlatformName, form.StaffName) )
        t_sys_platform_role_objs = t_sys_platform_role.objects.filter(StaffID = request.user.username,PlatformName=obj.PlatformName)
        if  t_sys_platform_role_objs.count() <=0:

            obj.StaffID = request.user.username
            obj.StaffName = request.user.first_name
            obj.save()
            self.message_user(request,  u'增加成功：%s %s %s'%(obj.StaffID,obj.PlatformName, obj.StaffName) )
        else:
            self.message_user(request,  '已存在重复了：%s %s %s'%(t_sys_platform_role_objs[0].StaffID,t_sys_platform_role_objs[0].PlatformName, t_sys_platform_role_objs[0].StaffName) )

class t_sys_shopdef_Admin(object):
    list_display=('id','ShopID','ShopDesc','StaffID','ShopkeeperName','CreateTime','UpdateTime',)
    readonly_fields = ('id',)
    list_display_links = list_display

    search_fields=('ShopID','ShopDesc','StaffID','ShopkeeperName',)
    list_filter = ('ShopkeeperName','CreateTime','UpdateTime',)
    fieldsets = (
        (u'操作记录', {'fields': ('id','ShopID','ShopDesc','CreateTime',)}),
    )

    #def save_model(self, request, obj, form, change):
    def save_models(self):
        obj = self.new_obj
        request = self.request
        obj.StaffID = request.user.username
        obj.ShopkeeperName=request.user.first_name
        obj.save()

    def get_queryset(self, request):
        if request.user.is_superuser:
            qs = super(t_sys_shopdef_Admin, self).get_queryset(request)
            return qs
        qs = super(t_sys_shopdef_Admin, self).get_queryset(request).filter(StaffID=request.user.username)
        return qs

class t_product_wait_publish_Admin(object):
    actions = ['to_finish','to_ignore']
    def to_finish(self, request, queryset):
        #queryset.all().update(PublishStatus = 1,EndTime=datetime.now())
        for querysetid in queryset.all():
            t_product_publish_ed_obj = t_product_publish_ed(SourcePicPath2=querysetid.SourcePicPath2,MainSKU=querysetid.MainSKU,SKU=querysetid.SKU,ShopID=querysetid.ShopID,Name2=querysetid.Name2,StaffID=querysetid.StaffID,StaffName=querysetid.StaffName,BeginTime=querysetid.BeginTime,EndTime=datetime.now(),PublishStatus=1,pid=querysetid.pid)
            t_product_publish_ed_obj.save()
            querysetid.delete()
    to_finish.short_description = u'刊登完成'

    def to_ignore(self, request, queryset):
        #queryset.all().update(PublishStatus = 2,EndTime=datetime.now())
        for querysetid in queryset.all():
            t_product_publish_ed_obj = t_product_publish_ed(SourcePicPath2=querysetid.SourcePicPath2,MainSKU=querysetid.MainSKU,SKU=querysetid.SKU,ShopID=querysetid.ShopID,Name2=querysetid.Name2,StaffID=querysetid.StaffID,StaffName=querysetid.StaffName,BeginTime=querysetid.BeginTime,EndTime=datetime.now(),PublishStatus=2,pid=querysetid.pid)
            t_product_publish_ed_obj.save()
            querysetid.delete()
    to_ignore.short_description = u'不用刊登直接忽略'

    list_display=('id','SourcePicPath2','MainSKU','SKU','ShopID','Name2','StaffName','BeginTime','EndTime','PublishStatus','pid',)
    readonly_fields = ('id',)
    list_display_links = ('SourcePicPath2',)

    search_fields=('ShopID','SKU',)
    list_filter = ('StaffName','PublishStatus','BeginTime','ShopID')

    def get_queryset(self, request):
        if request.user.is_superuser:
            qs = super(t_product_wait_publish_Admin, self).get_queryset(request)
            return qs
        qs = super(t_product_wait_publish_Admin, self).get_queryset(request).filter(StaffID=request.user.username)
        return qs

class t_product_publish_ed_Admin(object):
    list_display=('id','SourcePicPath2','MainSKU','SKU','ShopID','Name2','StaffName','BeginTime','EndTime','PublishStatus','pid',)
    readonly_fields = ('id',)
    list_display_links = ('SourcePicPath2',)

    search_fields=('id','ShopID','SKU',)
    list_filter = ('StaffName','PublishStatus','BeginTime','ShopID')

    def get_queryset(self, request):
        if request.user.is_superuser:
            qs = super(t_product_publish_ed_Admin, self).get_queryset(request)
            return qs
        qs = super(t_product_publish_ed_Admin, self).get_queryset(request).filter(StaffID=request.user.username)
        return qs

xadmin.site.register(t_product_survey_ing,t_product_survey_ing_Admin)
xadmin.site.register(t_product_survey_ed,t_product_survey_ed_Admin)
xadmin.site.register(t_product_unique_ed,t_product_unique_ed_Admin)
xadmin.site.register(t_product_develop_ing,t_product_develop_ing_Admin)
xadmin.site.register(t_product_wait_enquiry,t_product_wait_enquiry_Admin)
xadmin.site.register(t_product_enquiry_ing,t_product_enquiry_ing_Admin)
xadmin.site.register(t_product_build_ing,t_product_build_ing_Admin)
xadmin.site.register(t_product_photograph,t_product_photograph_Admin)
xadmin.site.register(t_product_develop_ed,t_product_develop_ed_Admin)
xadmin.site.register(t_product_art_ing,t_product_art_ing_Admin)
xadmin.site.register(t_product_art_pre_ed,t_product_art_pre_ed_Admin)
xadmin.site.register(t_product_art_ed,t_product_art_ed_Admin)
#xadmin.site.register(t_product_export_ed,t_product_export_ed_Admin)
xadmin.site.register(t_product_enter_ing,t_product_enter_ing_Admin)
xadmin.site.register(t_product_enter_ed,t_product_enter_ed_Admin)
#xadmin.site.register(t_product_pictures,t_product_pictures_Adimin)
xadmin.site.register(t_product_questions,t_product_questions_Adimin)
#xadmin.site.register(t_product_export_config,t_product_export_config_Admin)
xadmin.site.register(t_product_repeats,t_product_repeats_Admin)
#xadmin.site.register(t_sys_packing,t_sys_packing_Admin)
#xadmin.site.register(t_sys_category,t_sys_category_Admin)
xadmin.site.register(t_product_recycle,t_product_recycle_Admin)
xadmin.site.register(t_product_depart_use,t_product_depart_use_Admin)
xadmin.site.register(t_product_survey_history,t_product_survey_history_Admin)
xadmin.site.register(t_product_allsku,t_product_allsku_Admin)

xadmin.site.register(t_sys_sku_seq,t_sys_sku_seq_Admin)
#admin.site.register(t_sys_upload_zip,t_sys_upload_zip_Admin)
xadmin.site.register(t_product_oplog,t_product_oplog_Admin)
xadmin.site.register(t_store_plan,t_store_plan_Admin)
xadmin.site.register(t_store_plan_warning,t_store_plan_warning_Admin)

xadmin.site.register(t_autopic_uq,t_autopic_uq_Admin)
xadmin.site.register(t_autopic_uq_ex,t_autopic_uq_ex_Admin)
xadmin.site.register(t_sys_platform_role,t_sys_platform_role_Admin)
xadmin.site.register(t_sys_department,t_sys_department_Admin)
xadmin.site.register(t_sys_department_staff,t_sys_department_staff_Admin)
xadmin.site.register(t_sys_shopdef,t_sys_shopdef_Admin)
xadmin.site.register(t_product_wait_publish,t_product_wait_publish_Admin)
xadmin.site.register(t_product_publish_ed,t_product_publish_ed_Admin)