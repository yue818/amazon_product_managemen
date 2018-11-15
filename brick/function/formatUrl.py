# -*- coding: utf-8 -*-
"""  
 @desc: my description
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
JOOM_URL = "joom.com"

WISH_PLATFORM    = 'wish'
AMAZON_PLATFORM  = 'amazon'
WWW1688_PLATFORM = '1688'
EBAY_PLATFORM = 'ebay'
ALIEXPRESS_PLATFORM = 'aliexpress'
JOOM_PLATFORM = 'joom'
CAN_NOT_PLATFORM = "can not formate"
#外部url标准化
#输入五种url之一
#输出：如果是五种url之一则格式化之后输出，如果是None或者空则返回''，如果不是五种之一则原样返回
def format_urls(url):
    try:
        if url is None or url.strip()=='':
            return CAN_NOT_PLATFORM, ''

        return_url = url
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


        if url.find(AMAZON_URL)>=0 or url.find('amazon.co.uk/')>=0 or url.find('amazon.co.jp/') >=0 :
            if url.find('?') >=0 :
                return_url = url.split(r'?')[0]
            return_url= return_url.replace('http://','').replace('https://','').replace('www.','').replace(' ','')
            for i in range(len(return_url.split("/"))):
                if return_url.split("/")[i] == "dp":
                    return_url = return_url.split("/")[i+1]
                    break
                if len(return_url.split("/")) == 2:
                    return_url = return_url.split("/")[i+1]
                    break
                if return_url.split("/")[i] == "gp":
                    return_url = return_url.split("/")[i+2]
                    break
            # return_url = "www.amazon.com//dp/%s"%return_url
            return AMAZON_PLATFORM, return_url

        if  url.find(EBAY_URL)>=0  or url.find('ebay.co.uk') >= 0:
            if url.find('?') >=0 :
                return_url = url.split(r'?')[0]
            return_url= return_url.replace('http://','').replace('https://','').replace('www.','').replace(' ','')
            for i in range(len(return_url.split("/"))):
                if return_url.split("/")[i] == "itm":
                    return_url = return_url.split("/")[i+1]
                    break
            return EBAY_PLATFORM, return_url

        if  url.find(ALIEXPRESS_URL)  >=0  :
            if url.find('?') >=0 :
                return_url = url.split(r'?')[0]
            return_url= return_url.replace('http://','').replace('https://','').replace('www.','').replace(' ','')
            return_url = 'https://www.%s'%(return_url)
            return_url = return_url.split("/")[-1].split(".")[0]
            # return_url = "aliexpress.com/item//%s.html"%return_url
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


        if url.find(JOOM_URL) >= 0:
            if url.find('?') >= 0:
                return_url = url.split(r'?')[0]
            return_url = return_url.replace('http://', '').replace('https://', '').replace('www.', '').replace(' ', '')
            for i in range(len(return_url.split("/"))):
                if return_url.split("/")[i] == "products":
                    return_url = return_url.split("/")[i+1]
                    break
            return JOOM_PLATFORM, return_url

        return CAN_NOT_PLATFORM, return_url
    except Exception:
        return CAN_NOT_PLATFORM, ''


"""
if __name__ == '__main__':
    print (format_urls("https://detail.1688.com/offer/568905240071.html?spm=b26110380.8880418.csimg003.22.6098adccuLrj7h"))
"""




