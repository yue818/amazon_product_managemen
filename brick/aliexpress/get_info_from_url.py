# -*- coding: utf-8 -*-
import urllib2, json
from datetime import datetime
from lxml import etree
from brick.function.get_ip_proxy import get_ip_proxy
def get_id_from_url(url):
    if url.split('/')[3]=='item':
        id = url.split('/')[5].split('.')[0]
    else:
        id = url.split('/')[6].split('.')[0].split('_')[1]
    return id

def get_OneWeek_Sum(id):
    quantity_sum = 0
    # proxy_handler = urllib2.ProxyHandler({'http': 'http://113.87.161.12:8088','https': 'https://123.57.133.142:3128'})
    # opener = urllib2.build_opener(proxy_handler)
    opener = get_ip_proxy()
    urllib2.install_opener(opener)
    print '统计一周'
    req = urllib2.Request(
        "https://feedback.aliexpress.com/display/evaluationProductDetailAjaxService.htm?callback=&productId=%d&type=default&page=%d" % (
        id, 1))
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    jdata = json.loads(res)
    if jdata.has_key('page'):
        total = jdata['page']['total']
        current = jdata['page']['current']
        print 'total:%d 页,current:%d 页' % (int(total), int(current))
        for x in range(int(total)):
            if x>9:
                break
            req = urllib2.Request(
                "https://feedback.aliexpress.com/display/evaluationProductDetailAjaxService.htm?callback=&productId=%d&type=default&page=%d" % (
                id, x + 1))
            res_data = urllib2.urlopen(req)
            res = res_data.read()
            jdata = json.loads(res)
            records = jdata['records']
            for record in records:
                print record
                print record['quantity']
                thisdate = datetime.strptime(record['date'], "%d %b %Y %H:%M")
                if (datetime.utcnow() - thisdate).days < 7:
                    quantity_sum += int(record['quantity'])
                else:
                    print 'sum:%d' % (quantity_sum)
                    return str(quantity_sum)
    return '抓取失败！'

def get_price_sum(id):
    url = "https://www.aliexpress.com/item/abc/%d.html" % (id)
    req = urllib2.Request(url)
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    # print res
    html = etree.HTML(res)
    discountprice = html.xpath('//*[@id="j-sku-discount-price"]/span[1]')
    if len(discountprice) == 1:
        lowprice = html.xpath('//*[@id="j-sku-discount-price"]/span[1]')
        hightprice = html.xpath('//*[@id="j-sku-discount-price"]/span[2]')
        showprice = lowprice[0].text + '-' + hightprice[0].text
    elif len(html.xpath('//*[@id="j-sku-discount-price"]'))==1:
        showprice = html.xpath('//*[@id="j-sku-discount-price"]')[0].text
    else:
        price = html.xpath('//*[@id="j-sku-price"]/span[1]')
        print len(price)
        if len(price) == 1:
            lowprice = html.xpath('//*[@id="j-sku-price"]/span[1]')
            hightprice = html.xpath('//*[@id="j-sku-price"]/span[2]')
            showprice = lowprice[0].text + '-' + hightprice[0].text
            print 'price:' + showprice
        else:
            price = html.xpath('//*[@id="j-sku-price"]')
            showprice = price[0].text  # price price[0][0]  price price[0][1]
            print 'price' + price[0].text
    unithx = html.xpath('//*[@itemprop="priceCurrency"]')
    if len(unithx) == 1:
        unit = unithx[0].text
    else:
        unit = ''
    orders = html.xpath('//*[@id="j-order-num"]/text()')
    print len(orders)
    if len(orders) == 0:
        return unit+showprice, 0
    print int(orders[0].replace(' orders', ''))
    return unit+showprice, int(orders[0].replace(' orders', ''))

def get_df_saleinfo_byid(id):
    showprice,ordes = get_price_sum(id)
    oneweeksum = get_OneWeek_Sum(id)
    return showprice,ordes,oneweeksum