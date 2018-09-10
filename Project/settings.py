# -*- coding: utf-8 -*-
"""
Django settings for Project project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

import logging
import django.utils.log
import logging.handlers


import djcelery
from kombu import Queue, Exchange
djcelery.setup_loader()

BROKER_URL = 'redis://:K120Esc1@r-uf63c26510a32804.redis.rds.aliyuncs.com:6379/0'    #配置broker,使用redis的0数据库
BROKER_POOL_LIMIT = 0
CELERYD_CONCURRENCY = 4  # 并发worker数
CELERYD_PREFETCH_MULTIPLIER = 1 # woker预取任务数量1，不能设置为0,0为尽可能的取
TASK_ACKS_LATE = True
CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'  #配置backend,任务结果
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler' #定时任务
CELERYD_LOG_FILE = "/tmp/celery_log/celery.log"  # log路径
CELERYBEAT_LOG_FILE = "/tmp/celery_log/celerybeat.log"  # beat log路径
CELERY_ENABLE_UTC = False
CELERY_RESULT_SERIALIZER = 'json'
CELERYD_MAX_TASKS_PER_CHILD = 2 # 每个worker最大执行任务数

# 任务队列
CELERY_QUEUE = (
    # Queue(name='default', exchange=Exchange('default'), routing_key='default'),
    Queue(name='real_time', exchange=Exchange('real_time'), routing_key='real_time'), #实时任务
    Queue(name='timing', exchange=Exchange('timing'), routing_key='timing'), #定时任务
    Queue(name='off_shelf', exchange=Exchange('off_shelf'), routing_key='off_shelf'), #下架任务
    Queue(name='wish_shopinfo', exchange=Exchange('wish_shopinfo'), routing_key='wish_shopinfo'), # Wish店铺任务
    Queue(name='wish_shop_manage', exchange=Exchange('wish_shop_manage'), routing_key='wish_shop_manage'), # Wish店铺任务
    Queue(name='on_shelf', exchange=Exchange('on_shelf'), routing_key='on_shelf'), #上架任务
    Queue(name='off_shelf_urgent', exchange=Exchange('off_shelf_urgent'), routing_key='off_shelf_urgent'), #紧急下架任务
    Queue(name='goodsbatchstate_redis', exchange=Exchange('goodsbatchstate_redis'), routing_key='goodsbatchstate_redis'), #批量同步商品库存、状态到redis
    Queue(name='kc_purchaser', exchange=Exchange('kc_purchaser'), routing_key='kc_purchaser'), #更新采购员数据
    Queue(name='web_crawler', exchange=Exchange('web_crawler'), routing_key='web_crawler'), #爬虫获取商品信息
    Queue(name='wish_refresh', exchange=Exchange('wish_refresh'), routing_key='wish_refresh'), #Wish定时任务队列
    Queue(name='ali_shop_manage', exchange=Exchange('ali_shop_manage'), routing_key='ali_shop_manage'), #AliExpress店铺管理任务队列
    Queue(name='amazon_upload', exchange=Exchange('amazon_upload'), routing_key='amazon_upload'), #亚马逊刊登任务队列
)

# 任务路由
from app_djcelery.tasks_routes import TASKS_LIST
CELERY_ROUTES = {}
for i in range(len(TASKS_LIST)):
    CELERY_ROUTES = dict(CELERY_ROUTES, **TASKS_LIST[i])

# CELERY_IGNORE_RESULT = True   # 丢弃任务结果
# CELERYD_TASK_TIME_LIMIT = 60    # 单个任务的运行时间不超过此值，否则会被SIGKILL 信号杀死,设置的值过小，任务会不执行完
# BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 90}
            #  任务发出后，经过一段时间还未收到acknowledge , 就将任务重新交给其他worker执行，设置的值过小，任务会被重复执行


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

MEDIA_URL = '/media/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pt=dq(=j(ty)hf$h-m-ldzs^rf8lx5#%5$rs=$##i_(v(v2+_y'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'storeapp',
    'xadmin',
    #'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'aliapp',
    'ebayapp',
    'skuapp',
    'gather_app',
    'pyapp',
    'djcelery',
    'app_djcelery',
    'chart_app',
    'picapp',
    'joom_app',
    'aliexpress_app',
    'mymall_app',
    'wishpubapp',
    'reportapp',
]

MIDDLEWARE_CLASSES = [
    #'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
]

ROOT_URLCONF = 'Project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'skuapp/templates'),)
WSGI_APPLICATION = 'Project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
#rm-uf6kd5a4wee2n2ze6rw.mysql.rds.aliyuncs.com
#'HOST': 'hequskuapp.mysql.rds.aliyuncs.com',
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hq_db',
        'HOST': 'hequskuapp.mysql.rds.aliyuncs.com',
        'PORT': '3306',
        'USER': 'by15161458383',
        'PASSWORD': 'K120Esc1'
    },
    'syn': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'py_db',
        'HOST': 'hequskuapp.mysql.rds.aliyuncs.com',
        'PORT': '3306',
        'USER': 'by15161458383',
        'PASSWORD': 'K120Esc1'
    },
    'pic': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pic_db',
        'HOST': 'hequskuapp.mysql.rds.aliyuncs.com',
        'PORT': '3306',
        'USER': 'by15161458383',
        'PASSWORD': 'K120Esc1'
    },
    'ali': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hq',
        'HOST': 'rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com',
        'PORT': '3306',
        'USER': 'by15161458383',
        'PASSWORD': 'K120Esc1'

    },
    'report': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'report_db',
        'HOST': 'rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com',
        'PORT': '3306',
        'USER': 'by15161458383',
        'PASSWORD': 'K120Esc1'

    },
}
DATABASE_APPS_MAPPING = {
    'pyapp': 'syn',
    'picapp': 'pic',
    'aliapp': 'ali',
    'reportapp':'report',
}
DATABASE_ROUTERS = ['Project.db_router.pyappRouter']
SQLSERVERDB = 'DRIVER={SQLServer};SERVER=122.226.216.10;port=18793;DATABASE=ShopElf;UID=sa;PWD=$%^AcB2@9!@#'

#db = MySQLdb.connect('hequskuapp.mysql.rds.aliyuncs.com','user_by','user_by','hq_db' )

EXAMPLE_DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

#LANGUAGES =(
    #见http://www.i18nguy.com/unicode/language-identifiers.html，但全部小写
    #('en-gb',_fake_gettext('UK English')),
    #('en-us',_fake_gettext('US English')),
#)
#LANGUAGES =(
    #('en-us',ugettext('English')),
    #('uk',ugettext('Ukrainian')),
#)
#LANGUAGE_CODE ='en-gb'
# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

#LANGUAGE_CODE = 'en-us'
#LANGUAGE_CODE = 'zh-Hans'

LANGUAGE_CODE = 'en'
lang_code = 'en'
#TIME_ZONE = 'UTC'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False




# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR,'static/')
#认证信息
ACCESS_KEY_ID= 'LTAIH6IHuMj6Fq2h'
ACCESS_KEY_SECRET = 'N5eWsbw8qBkMfPREkgF2JnTsDASelM'

PREFIX = 'http://'

ENDPOINT = 'vpc100-oss-cn-shanghai.aliyuncs.com'
ENDPOINT_OUT = 'oss-cn-shanghai.aliyuncs.com'

#在没有主SKU的情况下原始图片存放路径，后续产生了主SKU这些要挪走

BUCKETNAME_HAVEMAINSKU = 'fancyqube-havemainsku'
BUCKETNAME_XLS = 'fancyqube-xls'
BUCKETNAME_ZIP = 'fancyqube-zip'
BUCKETNAME_ZIP_ARTED  = 'fancyqube-zip-arted'
BUCKETNAME_DOWNLOAD='fancyqube-download'
BUCKETNAME_AMAZON  = 'fancyqube-amazon'
BUCKETNAME_PIC = 'fancyqube-mainskupic'
BUCKETNAME_overseas_warehouse_cargo_infor_xls = 'fancyqube-overseas-warehouse-cargo-infor-xls'
BUCKETNAME_ALL_MAINSKU_PIC = 'fancyqube-all-mainsku-pic'
BUCKETNAME_PDF = 'fancyqube-pdf'
BUCKETNAME_CSV = 'fancyqube-kc-csv'
#存放调研阶段没建主SKU的图片
BUCKETNAME_NOMAINSKU = 'fancyqube-nomainsku'

#存放开放阶段所有的图片
BUCKETNAME_DEV = 'fancyqube-dev'

#美工后的图片
BUCKETNAME_ARTED = 'fancyqube-arted'

#原始调研图片和供应商图片
BUCKETNAME_SV = 'fancyqube-sv'
BUCKETNAME_1688  = 'fancyqube-1688'
#测试
#BUCKETNAME_SV = 'fancyqube-sv-test'
#BUCKETNAME_1688  = 'fancyqube-1688-test'
#普源的图片存放地址
BUCKETNAME_PY  = 'fancyqube-py'
#侵权图片
BUCKETNAME_TORT = 'fancyqube-tort'


LIST_PLATFORM= ['amazon','ebay','express','lazada','wish']

LIST_DISPLAY_FIELD = ('id','SourcePicPath','Name','Category1','Category2','MainSKU','Keywords','SourceURL','PlatformName','Remark','StaffID','UpdateTime','show_oplog',)

#Amazon印度站算价配置
#汇率
EXCHANGE_RATE = 9.9
#利润率
PROFIT_RATE = 0.3
#gati运费(带电/不带电)
TRACK_PRICE_ELEC = 0.038
TRACK_PRICE_UNELEC = 0.048
#gati处理费规格(首重/单价)
TRACK_DEAL_WEIGHT = 500
TRACK_DEAL_PRICE = 7
#价格单配置
MARKETED = 'Fanku Eretail Pvt. Ltd.'
MANUFACTURED = 'Fanku Eretail Pvt. Ltd.'
MRP_START = 'RS.'
MRP_END = '/-(inclusive of all taxes)'
CUSTOMER_PHONE = '8512020156'
END_MESSAGE = 'Made by Fanku'



#申报比例
SBBL =6.5
#普源表单字段定义
XLS_FIELDS = (u'操作类型',u'商品编码',u'SKU',u'多款式',u'是否有样品',u'样品数量',u'大类名称', u'小类名称',u'商品名称',u'当前状态',
              u'材质',u'规格',u'型号',u'款式',u'品牌',u'单位',u'最小包装数',u'重量(G)',u'采购渠道',u'供应商名称',
              u'成本单价(元)',u'批发价格(美元)',u'零售价格(美元)',u'最低售价(美元)',u'最高售价(美元)',u'市场参考价(美元)',u'备注',u'中文申报名',u'英文申报名',u'申报价值(美元)',
              u'原产国代码',u'原产国',u'库存上限',u'库存下限',u'业绩归属人1',u'业绩归属人2',u'包装规格',u'开发日期',u'SKU款式1',u'SKU款式2',
              u'SKU款式3', u'SKU描述',u'图片URL',u'采购员',u'发货仓库',u'采购到货天数',u'内包装成本',u'网页URL',u'网页URL2',u'网页URL3',
              u'最低采购价格',u'海关编码',u'库存预警销售周期',u'采购最小订货量',u'内盒长',u'内盒宽',u'内盒高',u'内盒毛重',u'内盒净重',u'外箱长',
              u'外箱宽',u'外箱高',u'外箱毛重',u'外箱净重',u'商品URL',u'包装事项',u'是否带电',u'商品SKU状态',u'工号权限',u'季节',
              u'是否粉末',u'是否液体',u'责任归属人1',u'责任归属人2',u'商品属性',u'包装难度系数',u'店铺名称',u'UPC码',u'ASN码',u'网页URL4',u'网页URL5',u'网页URL6',
              u'店铺运费',u'包装材料重量',u'汇率',u'物流公司价格',u'交易费',u'毛利率',u'计算售价',
              )
# 普源B_Goods表中英文对应
ITEM_DICT = {
    'GoodsName': u'商品名称', 'GoodsStatus': u'当前状态', 'Material': u'材质', 'Class': u'规格', 'Model': u'型号',
    'Style': u'款式', 'Brand': u'品牌', 'Unit': u'单位', 'PackageCount': u'最小包装数', 'Weight': u'重量(G)',
    'BarCode': u'采购渠道', 'SupplierName': u'供应商名称', 'CostPrice': u'成本单价(元)','BatchPrice': u'批发价格(美元)',
    'RetailPrice': u'零售价格(美元)', 'SalePrice': u'最低售价(美元)','MaxSalePrice': u'最高售价(美元)',
    'MarketPrice': u'市场参考价(美元)', 'Notes': u'备注', 'AliasCnName': u'中文申报名', 'AliasEnName': u'英文申报名',
    'DeclaredValue': u'申报价值(美元)', 'OriginCountryCode': u'原产国代码', 'OriginCountry': u'原产国',
    'MaxNum': u'库存上限', 'MinNum': u'库存下限', 'SalerName': u'业绩归属人1', 'SalerName2': u'业绩归属人2',
    'PackName': u'包装规格', 'DevDate': u'开发日期', 'BmpUrl': u'换图要求', 'Purchaser': u'采购员', 'StoreID': u'发货仓库',
    'StockDays': u'采购到货天数', 'LinkUrl': u'供应商链接', 'LinkUrl2': u'网页URL2', 'LinkUrl3': u'网页URL3',
    'MinPrice': u'最低采购价格', 'HSCODE': u'海关编码', 'SellDays': u'库存预警销售周期', 'StockMinAmount': u'采购最小订货量',
    'InLong': u'内盒长','InWide': u'内盒宽', 'InHigh': u'内盒高', 'InGrossweight': u'内盒毛重', 'InNetweight': u'内盒净重',
    'OutLong': u'外箱长', 'OutWide': u'外箱宽', 'OutHigh': u'内盒高', 'OutGrossweight': u'外箱毛重',
    'OutNetweight': u'外箱净重', 'ItemUrl': u'商品URL', 'PackMsg': u'包装事项' , 'IsCharged': u'是否带电(1-是,0-否)',
    'IsPowder': u'是否粉末(1-是,0-否)', 'IsLiquid': u'是否液体(1-是,0-否)', 'possessMan1': u'责任归属人1', 'possessMan2': u'责任归属人2',
    'ShopTitle': u'店铺名称', 'LinkUrl4': u'备用供应商链接', 'LinkUrl5': u'网页URL5', 'LinkUrl6': u'网页URL6',
    'ShopCarryCost': u'店铺运费', 'PackWeight': u'包装材料重量', 'ExchangeRate': u'汇率', 'LogisticsCost': u'物流公司价格',
    'GrossRate': u'毛利率', 'CalSalePrice': u'计算售价', 'TQBH': u'提前备货', 'BMLGYLSP': u'备面料供应链商品',
    'WMLGYLSP': u'无面料供应链商品', 'GHBWSP': u'供货不稳商品', 'WarningCats': u'库存预警', 'Season': u'季节',
    'PackFee': u'内包装成本', 'AttributeName': u'商品属性'
}

# 信息修改下拉框排序
ITEM_ORDER_LIST = [
    'GoodsName', 'GoodsStatus', 'Purchaser', 'SupplierName', 'LinkUrl', 'Notes', 'WarningCats', 'CostPrice', 'BmpUrl',
    'SalerName', 'SalerName2', 'possessMan1', 'possessMan2', 'Unit', 'Material', 'AttributeName', 'PackName', 'PackFee',
    'Class', 'Model', 'Style', 'Brand', 'PackageCount', 'Weight', 'BatchPrice', 'RetailPrice', 'SalePrice',
    'MaxSalePrice', 'MarketPrice', 'AliasCnName', 'AliasEnName', 'DeclaredValue', 'OriginCountryCode', 'OriginCountry',
    'MaxNum', 'MinNum', 'StoreID', 'StockDays', 'LinkUrl2', 'LinkUrl3', 'LinkUrl4', 'LinkUrl5', 'LinkUrl6', 'MinPrice',
    'HSCODE', 'SellDays', 'StockMinAmount', 'InLong', 'InWide', 'InHigh', 'InGrossweight', 'InNetweight', 'OutLong',
    'OutWide', 'OutHigh', 'OutGrossweight', 'OutNetweight', 'ItemUrl', 'ShopCarryCost', 'PackWeight', 'ExchangeRate',
    'LogisticsCost', 'GrossRate', 'CalSalePrice', 'BarCode', 'PackMsg', 'Season', 'IsCharged', 'IsPowder', 'IsLiquid',
    'ShopTitle', 'DevDate'
]

# PackName', 'PackFee',

# 库存预警对应关系
WARNING_DICT = {
    'wrNone': u'未指派', 'wrPurOnRode': u'采购途中', 'wrStopPur': u'永不采购', 'wrSleepPur': u'暂不采购',
    'wradvanceStock': u'提前备货', 'wrhaveFabricsupply': u'备面料供应链商品', 'wrnoneFabricsupply': u'无面料供应链商品',
    'wrInstabilitySupply': u'供货不稳商品', 'wrwaitsupplychain': u'待转供应链', 'empty': u'置回普通商品',
    'factorythree': u'供应链服装生产工期3天', 'factoryfive': u'供应链服装生产工期5天',
    'factoryseven': u'供应链服装生产工期7天', 'factoryfifteen': u'供应链服装生产工期15天',
    'factoryfive01': u'亚马逊供应链服装工期5天'
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
       'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'},
            'direct': {
                'format': '%(asctime)s - %(message)s'
            },
            'json': {
                'format': '%(message)s'
            },
    },
    'filters': {
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'default': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': 'sourceDns/log/all.log',     #日志输出文件
            'maxBytes': 1024*1024*5,                  #文件大小
            'backupCount': 5,                         #备份份数
            'formatter':'standard',                   #使用哪种formatters日志格式
        },
        'error': {
            'level':'ERROR',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': 'sourceDns/log/error.log',
            'maxBytes':1024*1024*5,
            'backupCount': 5,
            'formatter':'standard',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'request_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': 'sourceDns/log/script.log',
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter':'standard',
        },
        'scprits_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename':'sourceDns/log/script.log',
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter':'standard',
        },
        'celery.worker': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/log/celery.worker.log',
            'formatter': 'direct'
        },
        'celery.task': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/log/celery.task.log',
            'formatter': 'direct'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'scripts': {
            'handlers': ['scprits_handler'],
            'level': 'INFO',
            'propagate': False
        },
        'sourceDns.webdns.views': {
            'handlers': ['default', 'error'],
            'level': 'DEBUG',
            'propagate': False
        },
        'sourceDns.webdns.util':{
            'handlers': ['error'],
            'level': 'ERROR',
            'propagate': False
        },
        'celery.worker': {
            'handlers': ['celery.worker'],
            'level': 'DEBUG'
        },
        'celery.task': {
            'handlers': ['celery.task'],
            'level': 'DEBUG'
        },
    }
}


# redis配置
CACHES = {
    # 页面缓存redis数据库2
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:K120Esc1@r-uf6206e9df36e854.redis.rds.aliyuncs.com:6379/2",
        'TIMEOUT': 1800,
    },

    # 商品信息缓存数据库0
    "product": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:K120Esc1@r-uf6206e9df36e854.redis.rds.aliyuncs.com:6379/0",
    },

    # 普源增量缓存数据库0
    "py_add": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:K120Esc1@r-uf6206e9df36e854.redis.rds.aliyuncs.com:6379/5",
    },
    
        # 普源增量缓存数据库0
    "py_add1": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:K120Esc1@r-uf688e4200cb5104.redis.rds.aliyuncs.com:6379",
        'TIMEOUT': 1800,
    }, 
    "aliexpress_online_info": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://:K120Esc1@r-uf6206e9df36e854.redis.rds.aliyuncs.com:6379/10",    #速卖通api redis
            'TIMEOUT': 1800,
            "OPTIONS": {
                "IGNORE_EXCEPTIONS": True,
            }
    }, 
    
    # 存放异步调用进度
    "schedule": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:K120Esc1@r-uf6206e9df36e854.redis.rds.aliyuncs.com:6379/6",
    },
}

# redis数据库用途
# redis 0  商品信息正式环境
# redis 1  任务队列正式环境
# redis 2  页面缓存正式环境
# redis 5  普源增量正式环境

# redis 3  商品信息.8测试环境
# redis 4  任务队列.8测试环境


# redis连接方式
# from django_redis import get_redis_connection
# redis_client = get_redis_connection(alias='py_add')   