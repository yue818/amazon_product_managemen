# -*- coding: utf-8 -*-
import urllib2,json
import datetime as pptime
from lxml import etree

from brick.public.proxy import proxy

class compirePrice():
    @staticmethod
    def getIdFromUrl(url):
        id = url.split('/')[5].split('.')[0]
        return id

    @staticmethod
    def haveNextPage(id,num):
        url = "https://feedback.aliexpress.com/display/evaluationProductDetailAjaxService.htm" \
              "?callback=&productId=%s&type=default&page=%s" % (id, num)
        return url

    # 7天order数 count
    @staticmethod
    def getTheResultnum(id):
        req = urllib2.Request(compirePrice.haveNextPage(id,1))
        res = proxy.get_proxy().open(req, timeout=60).read()
        jdata = json.loads(res)
        total = jdata['page']['total']
        current = jdata['page']['current']
        print 'total:%s 页,current:%s 页' % (int(total), int(current))
        num = 0
        for x in range(int(total)):
            req = urllib2.Request(compirePrice.haveNextPage(id,x+1))
            res = proxy.get_proxy().open(req, timeout=60).read()
            jdata = json.loads(res)
            records = jdata['records']
            for record in records:
                thisdate = (pptime.datetime.strptime(record['date'], "%d %b %Y %H:%M")).strftime('%Y-%m-%d %H:%M')
                if thisdate >= (pptime.datetime.utcnow() + pptime.timedelta(days=-15)).strftime('%Y-%m-%d %H:%M'):
                    num += 1
        return num

    @staticmethod
    def getPriceSection(id):
        url = "https://www.aliexpress.com/item/abc/%s.html" % (id)
        req = urllib2.Request(url)
        res = proxy.get_proxy().open(req, timeout=60).read()
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
