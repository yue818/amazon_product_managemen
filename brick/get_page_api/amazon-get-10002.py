# -*- coding: utf-8 -*-
"""  
 @desc: my description
 @author: fangyu  
 @site: 
 @software: PyCharm
 @file: amazonApi.py
 @time: 2018-05-26 8:40
"""

__author__ = 'farry'
from gevent import monkey; monkey.patch_all()
from gevent.pywsgi import WSGIServer
import json,urllib2,base64,werkzeug
from flask import Response, Flask, send_file, request, jsonify
from mws import *
from io import BytesIO

app = Flask(__name__)

def getConentFromURL(url):
    import requests
    from proxy_ip import get_headers
    try:
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
    return "api"

@app.route("/amazon/get", methods=['GET'])
def html():
    ASIN = request.values.get("ASIN", '')
    dictdata = {}
    Products_rsp_dict = {}
    add_time = ""
    if ASIN != "":
        ProductsIMP = Products('AKIAI3VXKSMW236VTP2Q', 'Nnlcb4O2SWTnoJnHxA3mAiGxOEnIWAXXIJXJNTpm', 'A3C5W7VJSG67TC')
        Products_rsp = ProductsIMP.get_matching_product_for_id('ATVPDKIKX0DER', 'ASIN', [ASIN])  # ATVPDKIKX0DER
        # print 'Products_rsp=%s'%Products_rsp.original
        Products_rsp_dict = Products_rsp.parsed
        # print 'Products_rsp_dict=%s' % Products_rsp_dict
        dictdata = {"title":Products_rsp_dict["Products"]["Product"]["AttributeSets"]["ItemAttributes"]["Title"]["value"],
                    "imgsrc":Products_rsp_dict["Products"]["Product"]["AttributeSets"]["ItemAttributes"]["SmallImage"]["URL"]["value"]}
    return json.dumps(dictdata)
    # return jsonify(dictdata)

@app.route("/amazon/proxy", methods=['GET','POST'])
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

if __name__ == '__main__':
    # app.run(host="0.0.0.0",port = 7790, debug=True)
    print(base64.urlsafe_b64encode("http://fancyqube-sv.oss-cn-shanghai.aliyuncs.com/LDxQqrupGf/P8xNSlWol9.jpg"))
    print(base64.urlsafe_b64encode("http://fancyqube-sv.oss-cn-shanghai.aliyuncs.com/LDxQqrupGf/P8xNSlWol9.jpg"))
    gevent_server = WSGIServer(('0.0.0.0', 10002), app)
    gevent_server.serve_forever()