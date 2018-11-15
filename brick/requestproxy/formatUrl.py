# -*- coding: utf-8 -*-
"""  
 @desc: url格式化
 @author: fangyu  
 @site: 
 @software: PyCharm
 @file: formatUrl.py
 @time: 2018-05-23 14:35
"""

WISH_URL    = 'wish.com/'
AMAZON_URL  = 'amazon.com/'
WWW1688_URL = '1688.com/'
EBAY_URL = 'ebay'
ALIEXPRESS_URL = 'aliexpress.com/'

WISH_PLATFORM    = 'wish'
AMAZON_PLATFORM  = 'amazon'
WWW1688_PLATFORM = '1688'
EBAY_PLATFORM = 'ebay'
ALIEXPRESS_PLATFORM = 'aliexpress'
CAN_NOT_FORMATE = "can not formate"
NONSUPPORT = "not support"
#外部url标准化
#输入五种url之一
#输出：如果是五种url之一则格式化之后输出，如果是None或者空则返回''，如果不是五种之一则原样返回
def format_urls(url):
    import re
    if url is None or url.strip()=='':
        return CAN_NOT_FORMATE, ''

    return_url = url
    try:
        #wish
        if url.find(WISH_URL)  >=0  :
            if  url.find('?') >=0 :
                return_url = url.split(r'?')[0]
            if  url.find('#') >=0 :
                return_url = url.split(r'#')[0]
            return_url= return_url.replace('http://','').replace('https://','').replace('www.','').replace(' ','')
            return_url = return_url.split("/")[-1]
            # return_url = "www.wish.com/c/%s"%return_url
            return WISH_PLATFORM, return_url

        if url.find(AMAZON_URL)  >=0  :
            if url.find('?') >=0 :
                return_url = url.split(r'?')[0]
            if  url.find('#') >=0 :
                return_url = url.split(r'#')[0]
            re1 = re.search('/[a-zA-Z0-9]{10}$', return_url)
            if re1:
                # print(re1.group().replace("/",""))
                return AMAZON_PLATFORM, re1.group().replace("/","")
            re2 = re.search('/[a-zA-Z0-9]{10}/', return_url)
            if re2:
                # print(re2.group().replace("/",""))
                return AMAZON_PLATFORM, re2.group().replace("/","")
            return NONSUPPORT,""

        if  url.find(EBAY_URL)  >=0  :
            if url.find('?') >=0 :
                return_url = url.split(r'?')[0]
            return_url= return_url.replace('http://','').replace('https://','').replace('www.','').replace(' ','')
            # return_url = 'https://www.%s'%(return_url)
            return_url = return_url.split("/")[-1]
            # return_url = "www.ebay.com/itm//%s"%return_url
            return EBAY_PLATFORM, return_url

        if  url.find(ALIEXPRESS_URL)  >=0  :
            if url.find('?') >=0 :
                return_url = url.split(r'?')[0]
            return_url= return_url.replace('http://','').replace('https://','').replace('www.','').replace(' ','')
            return_url = 'https://www.%s'%(return_url)
            return_url = return_url.split("/")[-1].split(".")[0]
            # return_url = "aliexpress.com/item//%s.html"%return_url
            if "_" in return_url:
                return_url = return_url.split("_")[1]
            return ALIEXPRESS_PLATFORM, return_url

        if  url.find(WWW1688_URL)  >=0  :
            if  url.find('?') >=0 :
                return_url = url.split(r'?')[0]
            if  url.find('#') >=0 :
                return_url = url.split(r'#')[0]
            return_url= return_url.replace('http://','').replace('https://','').replace('www.','').replace(' ','')
            # return_url = 'https://%s'%(return_url)
            return_url = return_url.split("/")[-1].split(".")[0]
            return WWW1688_PLATFORM,return_url
    except Exception,e:
        return NONSUPPORT,""
    return CAN_NOT_FORMATE, return_url


if __name__ == '__main__':
    print(format_urls("https://www.aliexpress.com/item/Casual-2016-New-Korean-Style-Summer-Vintage-High-Waisted-Denim-Women-Shorts-Plus-Size-Slim-Stretch/32678947505.html?spm=2114.search0103.3.169.2d1c7b68G3hXko&ws_ab_test= "))
    print(format_urls("https://detail.1688.com/offer/555099770004.html?spm=b26110380.8880418.csimg003.113.575eadccjqnitP"))
    print(format_urls(
        "https://www.ebay.com/itm/La-Vie-Est-Belle-LECLAT-Leau-De-Parfum-Spray-1-7-oz-New-in-Sealed-Box/153025838592?epid=2165476181&hash=item23a10cfe00:g:ZIMAAOSwODFab0iI"))
    print(format_urls(
        "https://www.amazon.com/Shappy-Pieces-Brooch-Safety-Plastic/dp/B075R81ZSY/ref=sr_1_25?m=A2WHNP9T84YYCA&s=merchant-items&ie=UTF8&qid=1524460518&sr=1-25"))
    print(format_urls(
        "https://www.wish.com/c/5666863ddf0a6e2094f3f6be"))
    print(format_urls(
        "https://www.amazon.com/dp/B01MRIM3B3/"))
    print(format_urls(
        "https://www.amazon.com/dp/B071KVTYBW"))
    print(format_urls(
        "https://www.amazon.com/Bulova-98D109-Diamond-Accented-Black-Stainless/dp/B0021AEDSM/ref=lp_17727431011_1_1?m=ATVPDKIKX0DER&s=apparel&ie=UTF8&qid=1527060153&sr=1-1&nodeID=17727431011&psd=1"))
    print(format_urls(""))
    print(format_urls("https://www.amazon.com/gp/product/B07C8QXGMM"))
    print(format_urls(None))
    print(format_urls("https://www.baidu.com/"))
    print(format_urls("https://www.aliexpress.com/store/product/New-Ethnic-gold-earrings-brand-handmade-vintage-jewelry-Chinese-wind-ceramics-dangle-earrings/1270540_32306755403.html"))
    print(format_urls("https://detail.1688.com/offer/549283213462.html?spm=b26110380.sw1688.mof001.159.4f8b6912trgRPd"))
    print(format_urls("https://www.aliexpress.com/store/product/New-Trendy-Long-Chain-Tassel-Double-Round-Circle-Pendant-Earrings-for-Women-Geometric-Drops-Dangle-Earrings/1472203_32831319414.html?spm=2114.12010615/itm2home-1.0.0.32154c18Mk4hJ0"))
    print(format_urls("https://www.wish.com/feed/tabbed_feed_latest/product/5aba0d5be114ef2e72fd61e8"))
    print(format_urls("https://www.aliexpress.com/item//32831319414.html"))



