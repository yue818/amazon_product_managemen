# -*- coding: utf-8 -*-
from django import template
#from skuapp import models
from django.db import models
from skuapp.table.B_PackInfo import *
#导入模块
import logging
import django.utils.log
import logging.handlers

import os
from Project.settings import *
import oss2
import re
register = template.Library()

@register.inclusion_tag('pictures.html')
def display_no_mainsku_pictures(objid):

    pictures = []
    obj  = models.t_product_survey_ing.objects.get(id__exact=objid)
    if obj is None :
        return { 'pictures': pictures }

    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_NOMAINSKU)

    for  object_info in oss2.ObjectIterator(bucket,prefix='%s/%s/'%(obj.Category1_id,obj.id)):
        pictures.append('%s%s.%s/%s'%(PREFIX,BUCKETNAME_NOMAINSKU,ENDPOINT_OUT,object_info.key))
    return { 'pictures': pictures }

@register.inclusion_tag('pictures.html')
def display_no_mainsku_pictures_survey(objid):

    pictures = []
    obj  = models.t_product_survey_ed.objects.get(id__exact=objid)
    if obj is None :
        return { 'pictures': pictures }

    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_NOMAINSKU)

    for  object_info in oss2.ObjectIterator(bucket,prefix='%s/%s/'%(obj.Category1_id,obj.id)):
        pictures.append('%s%s.%s/%s'%(PREFIX,BUCKETNAME_NOMAINSKU,ENDPOINT_OUT,object_info.key))
    return { 'pictures': pictures }

@register.inclusion_tag('pictures.html')
def display_pictures_dev(objid):
    pictures = []
    obj  = models.t_product_develop_ing.objects.get(id__exact=objid)
    if obj is None :
        return { 'pictures': pictures }
    #取调研图片
    if obj.MainSKU is None or obj.MainSKU.strip()=='':
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_NOMAINSKU)
        for  object_info in oss2.ObjectIterator(bucket,prefix='%s/%s/'%(obj.Category1_id,obj.id)):
            pictures.append('%s%s.%s/%s'%(PREFIX,BUCKETNAME_NOMAINSKU,ENDPOINT_OUT,object_info.key))
        return { 'pictures': pictures }

    #没用调研图片取开发图片
    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_DEV)
    for  object_info in oss2.ObjectIterator(bucket,prefix='%s/PUB'%(obj.MainSKU)):
        pictures.append('%s%s.%s/%s'%(PREFIX,BUCKETNAME_DEV,ENDPOINT_OUT,object_info.key))

    #开发没有上传图片默认调研图片
    if len(pictures) ==0 :
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_NOMAINSKU)
        for  object_info in oss2.ObjectIterator(bucket,prefix='%s/%s/'%(obj.Category1_id,obj.id)):
            pictures.append('%s%s.%s/%s'%(PREFIX,BUCKETNAME_NOMAINSKU,ENDPOINT_OUT,object_info.key))
        return { 'pictures': pictures }
    return { 'pictures': pictures }


@register.inclusion_tag('pictures.html')
def display_pictures(objid):
    #pictures = models.t_product_pictures.objects.filter(TradeID=objid,SourcePicPath__isnull = False)
    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_NOMAINSKU)
    #pictures = oss2.ObjectIterator(bucket)
    pictures = []
    for  object_info in oss2.ObjectIterator(bucket,prefix='%s/'%(objid)):
        pictures.append('%s%s.%s/%s'%(PREFIX,BUCKETNAME_NOMAINSKU,ENDPOINT_OUT,object_info.key))
    return { 'pictures': pictures }

@register.inclusion_tag('artedpictures.html')
def display_artedpictures(objid,platname):
    pictures = []
    obj  = models.t_product_art_ing.objects.get(id__exact=objid)
    if obj.MainSKU is None or obj.MainSKU.strip()=='':
        return { 'pictures': pictures }

    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_ARTED)

    for  object_info in oss2.ObjectIterator(bucket,prefix='%s/%s/'%(obj.MainSKU,platname)):
        pictures.append('%s%s.%s/%s'%(PREFIX,BUCKETNAME_ARTED,ENDPOINT_OUT,object_info.key))
    return { 'pictures': pictures }

@register.inclusion_tag('enteredpictures.html')
def display_enteredpictures(objid,platname):
    pictures = []
    picture_names = []
    obj  = models.t_product_enter_ed.objects.get(id__exact=objid)
    if obj.MainSKU is None or obj.MainSKU.strip()=='':
        return { 'pictures': pictures }

    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_ARTED)

    for  object_info in oss2.ObjectIterator(bucket,prefix='%s/%s/'%(obj.MainSKU,platname)):
        pictures.append('%s%s.%s/%s'%(PREFIX,BUCKETNAME_ARTED,ENDPOINT_OUT,object_info.key))
        picture_names.append('%s%s.%s/%s'%(PREFIX,BUCKETNAME_ARTED,ENDPOINT_OUT,object_info.key))
    return { 'pictures': pictures , 'picture_names':picture_names}

@register.inclusion_tag('newpictures.html')
def display_newpictures(objid):
    pictures = []
    obj  = models.t_product_develop_ing.objects.get(id__exact=objid)
    if obj.MainSKU is None or obj.MainSKU.strip()=='' or  obj.SourcePicPath2 is None or obj.SourcePicPath2.strip()=='' :
        #pictures = models.t_product_pictures.objects.filter(TradeID=objid,SourcePicPath__isnull = False)
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_NOMAINSKU)
        #pictures = oss2.ObjectIterator(bucket)

        for  object_info in oss2.ObjectIterator(bucket,prefix='%s/'%(objid)):
            pictures.append('%s%s.%s/%s'%(PREFIX,BUCKETNAME_NOMAINSKU,ENDPOINT_OUT,object_info.key))

    else:
        MainSKU = obj.MainSKU
        path_az = re.sub('[^a-zA-Z]','',MainSKU) #去掉字母
        path_09 = re.sub("\D", "", MainSKU)
        bucket_name = 'fancyqube-%s'%(path_az.lower())
        oss2auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(oss2auth, ENDPOINT,bucket_name)
        #加上子SKU
        path = path_az
        for s0 in path_09 :
            path =  u'%s/%s'%(path,s0)

        path =  u'%s/%s'%(path,obj.MainSKU)

        for  object_info in oss2.ObjectIterator(bucket,prefix='%s/'%(path)):
            pictures.append('%s%s.%s/%s'%(PREFIX,bucket_name,ENDPOINT_OUT,object_info.key))

    return { 'pictures': pictures }



@register.inclusion_tag('newpictures.html')
def display_newpictures222(objid):
    obj  = models.t_product_develop_ing.objects.get(id__exact=objid)
    if obj.MainSKU is None or obj.MainSKU.strip()=='' :
        return
    MainSKU = obj.MainSKU
    path_az = re.sub('[^a-zA-Z]','',MainSKU) #去掉字母
    path_09 = re.sub("\D", "", MainSKU)
    bucket_name = BUCKETNAME_NOMAINSKU #'fancyqube-%s'%(path_az.lower())
    oss2auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(oss2auth, ENDPOINT,bucket_name)
    #加上子SKU
    path = path_az
    for s0 in path_09 :
        path =  u'%s/%s'%(path,s0)

    path =  u'%s/%s'%(path,obj.MainSKU)
    pictures = []
    for  object_info in oss2.ObjectIterator(bucket,prefix='%s/'%(path)):
        pictures.append('%s%s.%s/%s'%(PREFIX,bucket_name,ENDPOINT_OUT,object_info.key))

    return { 'pictures': pictures }

@register.inclusion_tag('downloadxls.html')
def downloadxls(user):
    #os.popen(' cd /data/djangostack-1.9.7/apps/django/django_projects/Project')
    pwd = os.popen('pwd').read().strip()

    #downloadfiles = os.popen('ls -t media/download_xls/' + str(user) + '/*.xls').read().split()[0:3]
    #downloadfiles = os.popen('ls -t %s/%s/.xls'%(XLS_PATH,str(user))).read().split()[0:3]
    #downloadfilesxx = os.popenxxx(r' ls -t %s/%s/%s_*.xls'%(XLS_PATH,str(user),str(user))).read().split()[0:3]
    #获取之前的下载路径
    downloadfiles = []
    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_XLS)
    for  object_info in oss2.ObjectIterator(bucket,prefix='%s/%s_'%(str(user),str(user))):
        downloadfiles.append('%s%s.%s/%s'%(PREFIX,BUCKETNAME_XLS,ENDPOINT_OUT,object_info.key))
    return { 'downloadfiles': downloadfiles}

@register.inclusion_tag('downloadpic.html')
def downloadpic(user):
    #os.popen(' cd /data/djangostack-1.9.7/apps/django/django_projects/Project')
    pwd = os.popen('pwd').read().strip()

    #downloadfiles = os.popen('ls -t media/download_xls/' + str(user) + '/*.xls').read().split()[0:3]
    #downloadfiles = os.popen('ls -t %s/%s/.xls'%(XLS_PATH,str(user))).read().split()[0:3]
    #downloadfilesxx = os.popenxxx(r' ls -t %s/%s/%s_*.xls'%(XLS_PATH,str(user),str(user))).read().split()[0:3]
    #获取之前的下载路径
    downloadfiles = []
    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_ZIP)
    for  object_info in oss2.ObjectIterator(bucket,prefix='%s/media/downloadartingpic/%s_'%(str(user),str(user))):
        downloadfiles.append('%s%s.%s/%s'%(PREFIX,BUCKETNAME_ZIP,ENDPOINT_OUT,object_info.key))
    return { 'downloadfiles': downloadfiles}
    #http://fancyqube-zip.oss-cn-shanghai.aliyuncs.com/root/media/downloadartingpic/root/root_20170515151220.zip

@register.inclusion_tag('downloadpic.html')
def downloadartedpic(user):
    downloadfiles = []
    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_ZIP_ARTED)
    for  object_info in oss2.ObjectIterator(bucket,prefix='%s/media/downloadartedpic/%s_'%(str(user),str(user))):
        downloadfiles.append('%s%s.%s/%s'%(PREFIX,BUCKETNAME_ZIP_ARTED,ENDPOINT_OUT,object_info.key))
    return { 'downloadfiles': downloadfiles}

@register.inclusion_tag('questions_pic.html')
def display_questions_pic(objid):
    questions_pics = os.popen('ls -t media/questions_pic/' + str(objid) + '/*').read().split()
    return { 'questions_pics': questions_pics }

@register.inclusion_tag('category2.html')
def select_category2(objid):
    t_product_develop_ing_obj  = models.t_product_develop_ing.objects.get(id__exact=objid)
    category2s = models.t_sys_category.objects.filter(PCategoryID =  t_product_develop_ing_obj.Category1.CategoryID)
    return { 'category2s': category2s }




@register.inclusion_tag('sku_property_list.html')
def sku_property_list(objid):
    logger = logging.getLogger('sourceDns.webdns.views')    #刚才在setting.py中配置的logger

    #header name
    t_product_develop_ing_obj  = models.t_product_develop_ing.objects.get(id__exact=objid)

    mainsku_arrt_names  = models.t_product_mainsku_arrt_name.objects.filter(MainSKU =  t_product_develop_ing_obj.MainSKU).order_by('Attrid')
    mainsku_skus = models.t_product_sku_attr_value.objects.filter(MainSKU =  t_product_develop_ing_obj.MainSKU).order_by('SKU')
    sku_attr_values = {}
    tmp_sku_pics = {}
    for mainsku_sku in mainsku_skus :
        logger.error('mainsku_sku.SKU=%s'%mainsku_sku.SKU)
        sku_attr_values[mainsku_sku.SKU]  = models.t_product_sku_attr_value.objects.filter(MainSKU=t_product_develop_ing_obj.MainSKU,SKU =  mainsku_sku.SKU).order_by('Attrid')
        ##tmp_sku_pics[mainsku_sku.SKU] = '%s'%(t_product_develop_ing_obj.MainSKU)

    t_product_mainsku_sku_objs = models.t_product_mainsku_sku.objects.filter(MainSKU=t_product_develop_ing_obj.MainSKU,pid =objid)
    for t_product_mainsku_sku_obj in t_product_mainsku_sku_objs:
        tmp_sku_pics[t_product_mainsku_sku_obj.SKU] = '%s'%(t_product_develop_ing_obj.MainSKU)

    logger.error("t_product_mainsku_sku_objs = %s "%t_product_mainsku_sku_objs)
    logger.error("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    logger.error('mainsku_arrt_names=%s'%mainsku_arrt_names)
    logger.error('mainsku_skus=%s'%mainsku_skus)
    logger.error('sku_attr_values=%s'%sku_attr_values)


    i = 0
    attrijs = {}

    for (key,value) in sku_attr_values.items() :
        j=0
        xxj ={}
        for mainsku_arrt_name in mainsku_arrt_names :
            xxj['j%d'%j]=''
            for v in value :
                if v.Attrid == mainsku_arrt_name.Attrid  :
                    logger.error(u'%d %d = %s'%(i,j,v.Attrid))
                    xxj['j%d'%j]=v.AttrValue
                    break
            j=j+1
        logger.error(u'xxj====== %s'%xxj)
        attrijs[key]=xxj
        i=i+1


    logger.error(u'attrijs====== %s'%attrijs)

	#获取子SKU的图片路径
    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
    sku_pics = {}
    for (key,value) in tmp_sku_pics.items() :
        bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_DEV)
        pictures = []
        for  object_info in oss2.ObjectIterator(bucket,prefix='%s/%s/'%(value,key)):
           pictures.append(u'%s%s.%s/%s'%(PREFIX,BUCKETNAME_DEV,ENDPOINT_OUT,object_info.key))
           sku_pics[key] = pictures

    return { 'mainsku_arrt_names': mainsku_arrt_names,'attrijs': attrijs,'sku_pics':sku_pics}


@register.inclusion_tag('autopic_uq.html')
def display_autopic_uq(objid):

    autopic_uq_results = []
    t_autopic_uq_obj = models.t_autopic_uq.objects.filter(pid =objid)[0]
    if t_autopic_uq_obj is None:
        autopic_uq_results.append(u'无结果')
        return { 'autopic_uq_results': autopic_uq_results }
    status = u'排队中'
    if t_autopic_uq_obj.Status ==1 :
        status = u'正在排重'
    if t_autopic_uq_obj.Status ==2 :
        status = u'完成'
    autopic_uq_results.append(status)
    autopic_uq_results.append(t_autopic_uq_obj.Name)
    autopic_uq_results.append(t_autopic_uq_obj.BeginTime)
    autopic_uq_results.append(t_autopic_uq_obj.EndTime)

    #autopic_uq_results = u'结果: [ %s ]   %s: 开始时间:%s  结束时间:%s  '%(status,t_autopic_uq_obj.Name,t_autopic_uq_obj.BeginTime,t_autopic_uq_obj.EndTime)
    return { 'autopic_uq_results': autopic_uq_results }

@register.inclusion_tag('autopic_uqex.html')
def display_autopic_uqex(objid):
    autopic_uqex_results = u'无明细信息'
    t_autopic_uq_obj = models.t_autopic_uq.objects.filter(pid =objid)[0]
    if t_autopic_uq_obj is None:
        return { 'autopic_uqex_results': autopic_uqex_results }

    t_autopic_uqex_objs = models.t_autopic_uq_ex.objects.filter(pid =t_autopic_uq_obj.id).order_by('-Rate')
    return { 't_autopic_uqex_objs': t_autopic_uqex_objs }

@register.inclusion_tag('t_product_mainsku_sku.html')
def display_t_product_mainsku_sku_objs(objid):
    t_product_mainsku_sku_objs = models.t_product_mainsku_sku.objects.filter(pid=objid)
    return { 't_product_mainsku_sku_objs': t_product_mainsku_sku_objs }

@register.inclusion_tag('t_product_mainsku_sku_arted.html')
def display_t_product_mainsku_sku_objs_arted (objid):
    t_product_mainsku_sku_objs = models.t_product_mainsku_sku.objects.filter(pid=objid)
    return { 't_product_mainsku_sku_objs': t_product_mainsku_sku_objs }

@register.inclusion_tag('packing2.html')
def display_packing2(packNID):

    B_PackInfos =''
    PackNID = packNID

    try:
        B_PackInfo_obj = B_PackInfo.objects.get(id__exact=int(packNID))
        B_PackInfos = u'NID=%s  规格=%s 价格(¥元)=%s 重量(g)=%s'%(B_PackInfo_obj.id,B_PackInfo_obj.PackName,B_PackInfo_obj.CostPrice,B_PackInfo_obj.Weight)
    except:
        pass
    packing2s = B_PackInfo.objects.all()
    return { 'packing2s': packing2s ,'B_PackInfos':B_PackInfos,'PackNID':PackNID}

@register.inclusion_tag('SourcePicPath.html')
def display_SourcePicPath(objid):
    t_product_build_ing_obj  = models.t_product_build_ing.objects.get(id__exact=objid)
    return { 'SourcePicPath': t_product_build_ing_obj.SourcePicPath }

@register.inclusion_tag('SourcePicPath2.html')
def display_SourcePicPath2(objid):
    t_product_build_ing_obj  = models.t_product_build_ing.objects.get(id__exact=objid)
    return { 'SourcePicPath2': t_product_build_ing_obj.SourcePicPath2 }

@register.inclusion_tag('packing.html')
def display_packing(objid):
    B_PackInfos =u'请选择包装规格'
    PackNID = 0

    try:
        t_product_build_ing_obj  = models.t_product_build_ing.objects.get(id__exact=objid)
        B_PackInfo_obj = models.B_PackInfo.objects.get(id__exact=t_product_build_ing_obj.PackNID)
        PackNID   = B_PackInfo_obj.id
        B_PackInfos = u'NID=%s  规格=%s 价格(¥元)=%s 重量(g)=%s'%(B_PackInfo_obj.id,B_PackInfo_obj.PackName,B_PackInfo_obj.CostPrice,B_PackInfo_obj.Weight)

    except:
        pass
    packings = models.B_PackInfo.objects.all()
    return { 'packings': packings ,'B_PackInfos':B_PackInfos,'PackNID':PackNID}

@register.inclusion_tag('category.html')
def display_category(objid):
    LargeCategory =u'请选择大类'
    SmallCategory =u'请选择小类'
    try:
        t_product_build_ing_obj  = models.t_product_build_ing.objects.get(id__exact=objid)
        if t_product_build_ing_obj.LargeCategory is not None and t_product_build_ing_obj.LargeCategory.strip()!='':
            LargeCategory = t_product_build_ing_obj.LargeCategory
        if t_product_build_ing_obj.SmallCategory is not None and t_product_build_ing_obj.SmallCategory.strip()!='':
            SmallCategory = t_product_build_ing_obj.SmallCategory
    except:
        pass

    return { 'LargeCategory': LargeCategory ,'SmallCategory': SmallCategory }

@register.inclusion_tag('SourcePicPath.html')
def display_SourcePicPath_arted(objid):
    t_product_art_ed_obj  = models.t_product_art_ed.objects.get(id__exact=objid)
    return { 'SourcePicPath': t_product_art_ed_obj.SourcePicPath }

@register.inclusion_tag('SourcePicPath2.html')
def display_SourcePicPath2_arted(objid):
    t_product_art_ed_obj  = models.t_product_art_ed.objects.get(id__exact=objid)
    return { 'SourcePicPath2': t_product_art_ed_obj.SourcePicPath2 }

@register.inclusion_tag('packing.html')
def display_packing_arted(objid):
    B_PackInfos =u'请选择包装规格'
    PackNID = 0

    try:
        t_product_art_ed_obj  = models.t_product_art_ed.objects.get(id__exact=objid)
        B_PackInfo_obj = models.B_PackInfo.objects.get(id__exact=t_product_art_ed_obj.PackNID)
        PackNID   = B_PackInfo_obj.id
        B_PackInfos = u'NID=%s  规格=%s 价格(¥元)=%s 重量(g)=%s'%(B_PackInfo_obj.id,B_PackInfo_obj.PackName,B_PackInfo_obj.CostPrice,B_PackInfo_obj.Weight)

    except:
        pass
    packings = models.B_PackInfo.objects.all()
    return { 'packings': packings ,'B_PackInfos':B_PackInfos,'PackNID':PackNID}

@register.inclusion_tag('category.html')
def display_category_arted(objid):
    LargeCategory =u'请选择大类'
    SmallCategory =u'请选择小类'
    try:
        t_product_art_ed_obj  = models.t_product_art_ed.objects.get(id__exact=objid)
        if t_product_art_ed_obj.LargeCategory is not None and t_product_art_ed_obj.LargeCategory.strip()!='':
            LargeCategory = t_product_art_ed_obj.LargeCategory
        if t_product_art_ed_obj.SmallCategory is not None and t_product_art_ed_obj.SmallCategory.strip()!='':
            SmallCategory = t_product_art_ed_obj.SmallCategory
    except:
        pass

    return { 'LargeCategory': LargeCategory ,'SmallCategory': SmallCategory }
