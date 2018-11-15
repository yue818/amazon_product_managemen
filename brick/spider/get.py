# -*- coding: utf-8 -*-
"""  
 @desc: 从五种电商平台提取详情
 @author: fangyu  
 @site: 
 @software: PyCharm
 @file: get.py
 @time: 2018-05-17 10:46
"""
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import datetime as pdttime
import errno,os,oss2,urllib2,json,string,random
from bs4 import BeautifulSoup
from brick.public.proxy import proxy
from Project.settings import *
from lxml import etree
# from brick.aliexpress.ali_compirePrice import compirePrice
from brick.public.HTTP301_302_303_307_ERROR import urlopener
from brick.requestproxy.getamazon import getAmazonConentFromURL,getTitleImageurl
WISH_URL    = 'wish.'
AMAZON_URL  = 'amazon.'
WWW1688_URL = '1688.'
EBAY_URL = 'ebay.'
ALIEXPRESS_URL = 'aliexpress.'

#获取一段指定长度随机字符串，输入：指定随机字符串长度，输出：随机字符串
def get_random_str(len):
    base_str = string.letters+string.digits
    keylist = [random.choice(base_str) for i in range(len)]
    return ("".join(keylist))

#输入一个url输出这个url的response Body
def readURL(url,type):
    from brick.requestproxy.getali1688 import getAli1688ConentFromURL
    from brick.requestproxy.getwish import getWishConentFromURL
    from brick.requestproxy.getebay import getEbayConentFromURL
    from brick.requestproxy.getaliexpress import getAliexpressConentFromURL
    err = None
    data_bytes = None
    if type == "wish"  >=0  :
        for n in range(3):
            err, data_bytes = getWishConentFromURL(url)
            if err is None:
                break

    if  type == "ebay"  >=0  :
        for n in range(3):
            err, data_bytes = getEbayConentFromURL(url)
            if err is None:
                break

    if  type == "aliexpress"  >=0  :
        for n in range(3):
            err, data_bytes = getAliexpressConentFromURL(url)
            if err is None:
                break

    if  type == "1688"  >=0  :
        for n in range(3):
            print("1688抓取")
            err, data_bytes = getAli1688ConentFromURL(url)
            if err is None:
                print("抓取成功")
                break

    if err is not None:
        print("get html err=================================")
        return None
    return data_bytes

#url格式化，输入原始url，输出格式化后的url
def format_urls(url):
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

#1688调研图片
def read1688(url):
    from brick.requestproxy.getali1688 import getJsonFromUrl
    SourcePicPath = ""
    try:
        err, dict = getJsonFromUrl(url)
        print("==============getJsonFromUrl=======")
        print(dict)
        if  err is None and dict["error"] == 0:
            image = dict["image"]
            title = dict["title"]
            supplier = dict["supplier"]
            price_range = dict["price_range"]
            if image is not None and image.strip() != "":
                image_bytes = readURL(image, "1688")
                if image_bytes is not None:
                    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
                    bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_SV)
                    dir = get_random_str(10)
                    name = get_random_str(10)
                    bucket.put_object(u'%s/%s.jpg'%(dir,name),image_bytes)
                    #保存图片
                    SourcePicPath =  u'%s%s.%s/%s/%s.jpg'%(PREFIX,BUCKETNAME_SV,ENDPOINT_OUT,dir,name)
            print(image)
            print("==================return==============")
            return None,supplier,title,SourcePicPath, price_range
    except:
        return "抓取1688失败", "", "", "",""
    # SupplierID = ""
    # SupplierPDes = ""
    # SourcePicPath = ""
    # if url is None or url.strip() =='':
    #     return "url err","","",""
    # urlNew = url
    # if url is not None and url.find('?') >=0 :
    #     urlNew = url.split(r'?')[0]
    #
    # www1688urls = urlNew
    #
    # data_bytes = None
    # # opener = proxy.get_proxy()
    # for n in range(3):
    #     #取网站数据
    #     try:
    #         #data_bytes = urllib2.urlopen(www1688urls, timeout = 10).read().decode('gbk')
    #         # req = urllib2.Request(www1688urls)
    #         # data_bytes = opener.open(req, timeout = 30).read().decode('gbk')
    #         data_bytes = readURL(www1688urls,"1688").decode('gbk')
    #     except urllib2.HTTPError, e:
    #         return '供货商商品链接一读取错误.%s'%e.reason, "", "", ""
    #     except urllib2.URLError, e:
    #         return '供货商商品链接一读取错误.%s'%e.reason, "", "", ""
    #     if data_bytes is not None:
    #         try:
    #             soup = BeautifulSoup(data_bytes,"lxml")
    #             SupplierID = soup.html.find("a", attrs={'href':'#','class':'company-name'})
    #             #SupplierID = soup.html.find("a", class_="chinaname hidden")
    #             if SupplierID is not None:
    #                 SupplierID = SupplierID.string
    #                 if SupplierID is not None:
    #                     SupplierID = SupplierID.strip()
    #             if soup.html.find("a", class_="box-img") is not None:
    #                 #SupplierPDes 供货商商品标题
    #                 SupplierPDes = u'%s'%(dict(soup.html.find("a", class_="box-img").find("img").attrs)['alt'])
    #                 #图片
    #                 link_jpg = dict(soup.html.find("a", class_="box-img").find("img").attrs)['src']
    #             else:
    #                 if n < 2:
    #                     print("爬取数据被反扒")
    #                     continue
    #                 return "爬取数据被反扒", "", "", ""
    #         except Exception,e:
    #             if n < 2:
    #                 print("爬取数据被反扒")
    #                 continue
    #             return "爬取数据被反扒，%s"%e.message, "", "", ""
    #         if link_jpg is not None:
    #             try:
    #                 # req = urllib2.Request(link_jpg)
    #                 # image_bytes = opener.open(req, timeout = 30).read()
    #                 image_bytes = readURL(link_jpg,"1688")
    #                 # import requests
    #                 # image_bytes = requests.get(link_jpg)
    #             except urllib2.HTTPError, e:
    #                 return '供货商商品链接一数据获取错误，请选择手动上传图片或录入数据.%s'%e.reason, "", "", ""
    #             except urllib2.URLError, e:
    #                 return '供货商商品链接一数据获取错误，请选择手动上传图片或录入数据.%s'%e.reason, "", "", ""
    #             if image_bytes is not None:
    #                 auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
    #                 bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_SV)
    #                 dir = get_random_str(10)
    #                 name = get_random_str(10)
    #                 bucket.put_object(u'%s/%s.jpg'%(dir,name),image_bytes)
    #                 #保存图片
    #                 SourcePicPath =  u'%s%s.%s/%s/%s.jpg'%(PREFIX,BUCKETNAME_SV,ENDPOINT_OUT,dir,name)
    #                 SourceURL = www1688urls
    #                 #obj.SourceURL0 = www1688urls
    #                 # obj.save()
    # print(SupplierID)
    # print(SupplierPDes)
    # print(SourcePicPath)
    # return None,SupplierID,SupplierPDes,SourcePicPath

#输入wish的url，输出页面相关信息
def readWish(url):
    try:
        wishurls = format_urls(url)
    except:
        wishurls = url
    NumBought = ""
    SourcePicPath = ""
    Name = ""
    wishpicurls = None
    data_bytes = None
    jo = None

    #取网站数据

    # opener = proxy.get_proxy()

    try:
        # req = urllib2.Request(wishurls)
        # data_bytes = opener.open(req, timeout = 30).read()
        data_bytes = readURL(wishurls,"wish")
        print(data_bytes)
        #logger.error("workfunc_Wishworkfunc_Wishworkfunc_Wish 1111 obj = %s wishurls =%s"%(obj,wishurls))
        #self.message_user(request,data_bytes)
    except urllib2.HTTPError, e:
        return e.reason, NumBought, '', Name, '', SourcePicPath
    except urllib2.URLError, e:
        return e.reason, NumBought, '', Name, '', SourcePicPath
    if data_bytes is not None:
        data_bytes2 = data_bytes.split('pageParams')
        print(data_bytes2)
        if data_bytes2 is not None and len(data_bytes2) > 3 and data_bytes2[3] is not None and len(data_bytes2[3]) > 25 :
            data_bytes3 =  data_bytes2[3][20:-2] 
            print(data_bytes3)
            jo = json.loads(data_bytes3)
        if jo:
            wishpicurls = jo['small_picture'].split('?')[0].replace("small","big")
            print("================wish===%s")%wishpicurls
    #logger.error("workfunc_Wishworkfunc_Wishworkfunc_Wish 3333 obj = %s wishpicurls  =%s jo =%s"%(obj,wishpicurls,jo))
    #复制图片到本地
    if  wishpicurls is not None :
        try:
            # req = urllib2.Request(wishpicurls)
            # image_bytes = opener.open(req, timeout = 30).read()
            image_bytes = readURL(wishpicurls,"wish")
            #logger.error("workfunc_Wishworkfunc_Wishworkfunc_Wish 4444 obj = %s wishpicurls =%s"%(obj,wishpicurls))
        except urllib2.HTTPError, e:
            return e.reason, NumBought, '', Name, '', SourcePicPath
        except urllib2.URLError, e:
            return e.reason, NumBought, '', Name, '', SourcePicPath
        if image_bytes is not None:
                auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
                bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_SV)
                dir = get_random_str(10)
                name = get_random_str(10)
                bucket.put_object(u'%s/%s.jpg'%(dir,name),image_bytes)
                #保存图片
                SourcePicPath =  u'%s%s.%s/%s/%s.jpg'%(PREFIX,BUCKETNAME_SV,ENDPOINT_OUT,dir,name)
                print("===============================")
                print(SourcePicPath)
                SourceURL = wishurls
    else:
        #logger.error('workfunc_Wishworkfunc_Wishworkfunc_Wish 6666 obj = %s jo = %s' %(obj,jo))
        #self.message_user(request,'url error! [%s]'%wishurls)
        return "url is None", NumBought, '', Name, '', SourcePicPath
    #logger.error('workfunc_Wishworkfunc_Wishworkfunc_Wish 7777 obj = %s jo = %s' %(obj,jo))
    if jo:
        #名称
        Name = jo['name']
        print(Name)
        #Keywords
        #obj.Keywords = jo['keywords']

        #TAGS
        Tags = jo['keywords']
        print(Tags)
        #for tag in jo['tags']:
            #obj.Tags = u'%s %s'%(obj.Tags,tag['name'])
        #logger.error('workfunc_Wishworkfunc_Wishworkfunc_Wish 8888 obj.Tags = %s jo = %s' %(obj,obj.Tags))
        #ShelveDay 上架日期
        print(type(jo['generation_time']))
        print(jo['generation_time'])
        ShelveDay = jo['generation_time']#[0:10]
        print(ShelveDay)
        #价格区间

        # minprice = 999999
        # maxprice = 0
        # for variation in jo['commerce_product_info']['variations']:
        #     #self.message_user(request,u'original_price+original_shipping [%s,%s] '%(variation['original_price'],variation['original_shipping']) )
        #     tempprice = 0.0
        #     print("==============")
        #     # print(variation['original_shipping'])
        #     # print(variation['original_price'])
        #     print(type(variation))
        #     print(variation)
        #     tempprice = variation['original_price'] + variation['original_shipping']
        #     if tempprice > maxprice:
        #         maxprice = tempprice
        #     if tempprice < minprice:
        #         minprice = tempprice
        # Pricerange = '[%s,%s]'%(minprice,maxprice)
        # print(Pricerange)

        #购买量
        NumBought = jo['num_bought']
        print(NumBought)
        #WISH库存数
        TotalInventory = jo['commerce_product_info']['total_inventory']
        print(TotalInventory)
    return None, NumBought, '', Name, '', SourcePicPath

#输入亚马逊的url，输出页面相关信息
def readAmazon(url):
    enTitle = ""
    link_jpg = ""
    SourcePicPath = ""
    try:
        err,resultDict = getTitleImageurl(url)
        if err:
            return str(err), '', '', "", '', ""
        enTitle = resultDict["title"]
        link_jpg = resultDict["imgsrc"].replace("_SL75_","_SL600_")
        print("==============amazon==========%s")%link_jpg
        err,image_bytes = getAmazonConentFromURL(link_jpg)
        if err:
            image_bytes = None
    except urllib2.HTTPError, e:
        print("3")
        return '反向链接数据获取错误.%s'%e.reason, 'fifteenOrders', 'priceRange', 'enTitle', 'cnTitle', 'imageUrl'
    except urllib2.URLError, e:
        print("4")
        return '反向链接数据获取错误.%s' % e.reason, 'fifteenOrders', 'priceRange', 'enTitle', 'cnTitle', 'imageUrl'
    if image_bytes is not None:
        print("image_bytes not None")
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_SV)
        dir = get_random_str(10)
        name = get_random_str(10)
        bucket.put_object(u'%s/%s.jpg'%(dir,name),image_bytes)
        #保存图片
        SourcePicPath =  u'%s%s.%s/%s/%s.jpg'%(PREFIX,BUCKETNAME_SV,ENDPOINT_OUT,dir,name)
    return None, '', '', enTitle, '', SourcePicPath

#输入ebay的url，输出页面相关信息
def readeBay(url):
    #判断新老url是否相等
    new_SourceURL = url
    old_SourceURL = url
    eBayurls = new_SourceURL
    OrdersLast7Days, Pricerange, Keywords, SourcePicPath = "","","",""
    data_bytes = None
    try:
        data_bytes = readURL(eBayurls,"ebay")
    except urllib2.HTTPError, e:
        return e.reason, OrdersLast7Days, Pricerange, Keywords, '', SourcePicPath
    except urllib2.URLError, e:
        return e.reason, OrdersLast7Days, Pricerange, Keywords, '', SourcePicPath
    if data_bytes is not None:
        html = etree.HTML(data_bytes)
        keywords = '%s'%html.xpath('//*[@id="itemTitle"]/text()')
        Keywords = keywords[2:-2]
        print(Keywords)
        soup = BeautifulSoup(data_bytes,"lxml")
        #图片
        image_bytes =None
        try:
            link_jpg_list = html.xpath('//*[@id="icImg"]/@src')
            if link_jpg_list:
                link_jpg = link_jpg_list[0]
            else:
                link_jpg = dict(soup.find("div", id="vi_main_img_fs").find("td",class_="tdThumb").find("img").attrs)['src'].replace("s-l64.jpg","s-l500.jpg")
            image_bytes = readURL(link_jpg,"ebay")
        except urllib2.HTTPError, e:
            return e.reason, OrdersLast7Days, Pricerange, Keywords, '', SourcePicPath
        except urllib2.URLError, e:
            return e.reason, OrdersLast7Days, Pricerange, Keywords, '', SourcePicPath
        if image_bytes is not None:
            auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
            bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_SV)
            dir = get_random_str(10)
            name = get_random_str(10)
            bucket.put_object(u'%s/%s.jpg'%(dir,name),image_bytes)
            #保存图片
            SourcePicPath =  u'%s%s.%s/%s/%s.jpg'%(PREFIX,BUCKETNAME_SV,ENDPOINT_OUT,dir,name)
            print(SourcePicPath)

    return None, OrdersLast7Days, Pricerange, Keywords, '', SourcePicPath

#输入wish的url，输出页面相关详情信息
def read_ebay_detail(soup):
    details_bytes = None
    detailsurl = ''
    Pricerange = ""
    OrdersLast7Days = ""
    for atemp in soup.find_all('a'):
        detailsurl = atemp.get('href','')
        urlstring = ('%s'%atemp.string).split(' ')
        if urlstring[-1] == 'sold' and detailsurl.find('http://') == 0:
            break
    if detailsurl:
        try:
            # detreq = urllib2.Request(detailsurl)
            # details_bytes = proxy.get_proxy().open(detreq, timeout=60).read()
            details_bytes = readURL(detailsurl,"ebay")
        except urllib2.HTTPError, e:
            print ('反向链接数据获取错误，请选择手动上传图片或录入数据.%s' % e.reason)
            return
        except urllib2.URLError, e:
            print ('反向链接数据获取错误，请选择手动上传图片或录入数据.%s' % e.reason)
            return
    pirce_list = []
    time_list = []
    if details_bytes:
        # print(details_bytes)
        soup_details = BeautifulSoup(details_bytes, "lxml")
        rows_table = soup_details.find('table').find_all('tr') #无法定位
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
    # 价格区间
    if pirce_list:
        minprice = min(pirce_list)
        maxprice = max(pirce_list)
        if minprice == maxprice:
            Pricerange = '[%s]'%minprice
        else:
            Pricerange = ('[%s,%s]' % (minprice, maxprice)).replace(' ','')
            print("============================")
        print(Pricerange)
    # 7天order数量
    sorder = 0
    for mtime in time_list:
        if mtime >= (pdttime.datetime.now() + pdttime.timedelta(days=-15)).strftime('%Y-%m-%d %H:%M:%S'):
            sorder += 1
    OrdersLast7Days = sorder
    print(OrdersLast7Days)
    # obj.save()
    return Pricerange, OrdersLast7Days

#输入速卖通的url，输出页面相关信息
def readAliexpress(url):
    #判断新老url是否相等
    new_SourceURL = url
    old_SourceURL = ''
    aliexpressurls = new_SourceURL
    data_bytes = None
    Keywords, SourcePicPath, Pricerange, OrdersLast7Days = "", "", "", ""
    # opener = proxy.get_proxy()
    try:
        # req = urllib2.Request(aliexpressurls)
        # data_bytes = opener.open(req, timeout = 30).read()#.decode('gbk')
        data_bytes = readURL(aliexpressurls,"aliexpress")
    except urllib2.HTTPError, e:
        return '%s' % e.reason, Keywords, SourcePicPath, Pricerange, OrdersLast7Days
    except urllib2.URLError, e:
        return '%s' % e.reason, Keywords, SourcePicPath, Pricerange, OrdersLast7Days
    if data_bytes is not None:
        html = etree.HTML(data_bytes)
        keywords = '%s'%html.xpath('//*[@id="j-product-detail-bd"]/div[1]/div/h1/text()')
        Keywords = keywords[2:-2]
        print(Keywords)
        soup = BeautifulSoup(data_bytes,"lxml")
        #图片
        if soup is None:
            return
        try:
            link_jpg = dict(soup.find("ul", id="j-image-thumb-list").find("img").attrs)['src'].replace("50x50.jpg","640x640.jpg")
            # req = urllib2.Request(link_jpg)
            # image_bytes = opener.open(req, timeout = 30).read()
            image_bytes = readURL(link_jpg,"aliexpress")
        except urllib2.HTTPError, e:
            return '%s' % e.reason, Keywords, SourcePicPath, Pricerange, OrdersLast7Days
        except urllib2.URLError, e:
            return '%s'%e.reason, Keywords, SourcePicPath, Pricerange, OrdersLast7Days
        if image_bytes is not None:
            auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
            bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_SV)
            dir = get_random_str(10)
            name = get_random_str(10)
            bucket.put_object(u'%s/%s.jpg'%(dir,name),image_bytes)
            #保存图片
            SourcePicPath =  u'%s%s.%s/%s/%s.jpg'%(PREFIX,BUCKETNAME_SV,ENDPOINT_OUT,dir,name)
            print(SourcePicPath)
            SourceURL = aliexpressurls
            #obj.SourceURL0 = aliexpressurls
            # obj.save()
            try:
                Pricerange, OrdersLast7Days = read_Aliexpress_detail(aliexpressurls)
            except:
                Pricerange, OrdersLast7Days = "", ""
    return None, Keywords, SourcePicPath, Pricerange, OrdersLast7Days

#输入速卖通的url，输出页面相关详细信息
def read_Aliexpress_detail(aliurl):
    # product_id = compirePrice.getIdFromUrl(aliurl)
    from brick.requestproxy.formatUrl import format_urls
    platform, product_id = format_urls(aliurl)
    print(product_id)
    # Pricerange = compirePrice.getPriceSection(product_id)
    if platform == "aliexpress":
        Pricerange = getPriceSection(product_id)
    else:
        return "", ""
    print(Pricerange)
    # OrdersLast7Days = compirePrice.getTheResultnum(product_id)
    # print(OrdersLast7Days)
    # obj.save()
    return Pricerange, "" #OrdersLast7Days

def getPriceSection(id):
    url = "https://www.aliexpress.com/item//%s.html" % (id)
    print(url)
    # req = urllib2.Request(url)
    # res = proxy.get_proxy().open(req, timeout=60).read()
    res = readURL(url,"aliexpress")
    if res is None:
        return ""
    html = etree.HTML(res)
    discountprice = html.xpath('//*[@id="j-sku-discount-price"]/span[1]')
    pricecode = html.xpath('//*[@id="j-product-detail-bd"]/div[1]/div/div[2]/div[2]/div/div[2]/div/div[1]/span[1]')
    if len(discountprice) == 1:
        lowprice = html.xpath('//*[@id="j-sku-discount-price"]/span[1]')
        hightprice = html.xpath('//*[@id="j-sku-discount-price"]/span[2]')
        showprice = ('[%s,%s]' % (lowprice[0].text, hightprice[0].text)).replace(' ', '')
    else:
        price = html.xpath('//*[@id="j-sku-price"]/span[1]')
        if len(price) == 1:
            lowprice = html.xpath('//*[@id="j-sku-price"]/span[1]')
            hightprice = html.xpath('//*[@id="j-sku-price"]/span[2]')
            showprice = ('[%s,%s]' % (lowprice[0].text, hightprice[0].text)).replace(' ', '')
        else:
            price = html.xpath('//*[@id="j-sku-price"]')
            showprice = '[%s]' % (price[0].text)

    return showprice


if __name__ == '__main__':
    # read1688("https://detail.1688.com/offer/557430880147.html")
    # readWish("https://www.wish.com/c/5a814cb2f3bcca52052a366c")  #wish API 变化https://www.wish.com/c/55b5ec637327a04083684f30
    # readWish("https://www.wish.com/c/5a814cb2f3bcca52052a366c")
    print readAmazon("https://www.amazon.com/dp/B01MRIM3B3")  #无法访问网站
    # readeBay("https://www.ebay.co.uk/itm/183142919925")
    # readAliexpress("https://www.aliexpress.com/item/Mara-s-Dream-PU-Leather-Women-Handbag-Vintage-Women-Messenger-Bag-Fashion-Lock-Female-Shoulder-Bag/32833673814.html")