# -*- coding: utf-8 -*-
"""  
 @desc: my description
 @author: fangyu  
 @site: 
 @software: PyCharm
 @file: flaskApi.py
 @time: 2018-05-15 10:19
"""

__author__ = 'farry'
from gevent import monkey; monkey.patch_all()
from gevent.pywsgi import WSGIServer
import urllib2,base64,werkzeug
import requests, re, json
from flask import Response, Flask, send_file, request
from io import BytesIO, StringIO
from lxml import etree
app = Flask(__name__)

def get_1688_mobile(web_url):
    image, title, supplier, price_range = None, None, None, None
    mobile_url = web_url.replace('detail', 'm')
    response = requests.get(mobile_url, timeout=30, verify=False)
    text = response.text
    pattern = r'wingxViewData\[0\]=(.*)</script></div></div>'
    s = re.findall(pattern, text)
    s_dict = json.loads(s[0])
    image_list = s_dict.get('imageList', '')
    if image_list:
        image = image_list[0].get('size310x310URL', '')
    title = s_dict.get('subject', '')
    member_id = s_dict.get('memberId', '')
    supplier = get_supplier(member_id)
    if not supplier:
        supplier = s_dict.get('companyName', '')
    price_range_list = s_dict.get('priceDisplay', '')
    price_range = [float(price) for price in price_range_list.split('-')]
    return image, title, supplier, price_range


def get_supplier(member_id):
    """获取供应商名称"""
    url = 'https://m.1688.com/winport/company/%s.html' % member_id
    response = requests.get(url, timeout=30, verify=False).text
    html = etree.HTML(response)
    supplier_list = html.xpath('//*[@id="scroller"]/div[2]/ul/li[1]/div/span/text()')

    if supplier_list:
        supplier = supplier_list[0]
    else:
        supplier = ''
    return supplier


def getConentFromURL(url):
    import requests
    from proxy_ip import ip_verification,get_headers
    try:
        # err,http_proxy = get_proxy()
        # if not http_proxy or err:
        #     return err,"",503,""
        headers = get_headers()
        resp = requests.get(url, headers=headers, timeout=30)
        respBody = resp.content
        status_code = resp.status_code
        mimetype = resp.headers.get('Content-Type')
        resp.close()
    except requests.HTTPError, e:
        print("===============================")
        print(e.message)
        return e.message,"",503,""
    except Exception,e:
        print("===============================")
        print(e.message)
        return e.message,"",503,""
    return None,respBody,status_code,mimetype

@app.route("/", methods=['GET'])
def index():
    print(base64.urlsafe_b64encode("https://cbu01.alicdn.com/img/ibank/2017/331/011/4307110133_40167139.400x400.jpg"))
    print(base64.urlsafe_b64encode("https://detail.1688.com/offer/557430880147.html"))
    return "api"

@app.route("/1688/proxy", methods=['GET','POST'])
def img():
    urlb64 = request.values.get("url", '')
    if urlb64 =="":
        return "请为本url添加url参数",404
    print(urlb64)
    url = base64.urlsafe_b64decode(urlb64.encode("utf-8"))
    err, respBody, status_code, mimetype = getConentFromURL(url)
    if err:
        return str(err),status_code
    file = BytesIO(respBody)
    return send_file(filename_or_fp=file,mimetype=mimetype)

@app.route("/1688/get", methods=['GET','POST'])
def get():
    import json
    urlb64 = request.values.get("url", '')
    dictdata = {"error": 1, 'errmsg': "NONE url"}
    if urlb64 =="":
        return json.dumps(dictdata)
    print(urlb64)
    try:
        url = base64.urlsafe_b64decode(urlb64.encode("utf-8"))
    except:
        return json.dumps({"error": 1, 'errmsg': "url cant decode"})
    try:
        image, title, supplier, price_range = get_1688_mobile(url)
        dictdata = {"image":image, "title":title, "supplier":supplier, "price_range":price_range, "error": 0, 'errmsg': ""}
    except:
        dictdata = {"error": 1, 'errmsg': "get_1688_mobile err"}
    return json.dumps(dictdata)

if __name__ == '__main__':
    print(base64.urlsafe_b64encode("https://detail.1688.com/offer/567994068883.html"))
    # print(base64.urlsafe_b64decode("aHR0cHM6Ly9iZWVnby5tZS9kb2NzL212Yy9jb250cm9sbGVyL3BhcmFtcy5tZA=="))
    # app.run(host="0.0.0.0",port = 7788, debug=True)
    gevent_server = WSGIServer(('0.0.0.0', 10003), app)
    gevent_server.serve_forever()