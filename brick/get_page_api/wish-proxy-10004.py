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
import urllib2,base64,werkzeug,re
from flask import Response, Flask, send_file, request
from io import BytesIO, StringIO
app = Flask(__name__)

def get_proxy():
    """IP代理池"""
    import urllib2,requests
    from proxy_ip import get_headers,get_random_code
    # proxyAPI = r'http://dynamic.goubanjia.com/dynamic/get/0f43af0bb144af370b5c1df840c7df35.html'
    proxyAPI = r'http://dynamic.goubanjia.com/dynamic/get/995d33fcec25d7040a8e584463124997.html'
    proxy = {}

    try:
        proxyIP = urllib2.urlopen(proxyAPI).read().strip("\n")
        proxy = {'http': proxyIP}
        # proxy = {'http': "114.99.27.123:38726"}
    except:
        pass
    headers = get_headers()
    random_code = get_random_code()
    verification_url = 'http://47.100.6.69:32578/ip?randomCode=%s' % random_code
    print(verification_url)
    try:
        response = requests.get(verification_url, proxies=proxy, headers=headers)
        if response.status_code != 200:
            response.close()
            print("获取了一个不可用的代理")
            return "获取了一个不可用的代理",{}
    except Exception,e:
        return e.message,{}
    return None,proxy

def getConentFromURL(url):
    import requests
    from proxy_ip import ip_verification,get_headers
    try:
        err,http_proxy = get_proxy()
        if not http_proxy or err:
            return err,"",503,""
        headers = get_headers()
        resp = requests.get(url,proxies=http_proxy, headers=headers, timeout=30)
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

@app.route("/wish/proxy", methods=['GET','POST'])
def img():
    urlb64 = request.values.get("url", '')
    if urlb64 =="":
        return "请为本url添加url参数",404
    print(urlb64)
    url = base64.urlsafe_b64decode(urlb64.encode("utf-8"))
    if not "webimage" in url:
        re1 = re.search('/[a-z0-9]{24}', url)
        if re1:
            url = "https://www.wish.com/c/" + re1.group().replace("/", "")
    # id = url.split("?")[0].split("/")[-1]
    # if len(id) == 24:
    #     url = "https://www.wish.com/c/" + str(id)
    err, respBody, status_code, mimetype = getConentFromURL(url)
    if err:
        return str(err),status_code
    file = BytesIO(respBody)
    return send_file(filename_or_fp=file,mimetype=mimetype)

if __name__ == '__main__':
    # print(base64.urlsafe_b64encode("http://www.sohu.com/a/224999034_100122143"))
    # print(base64.urlsafe_b64decode("aHR0cHM6Ly9iZWVnby5tZS9kb2NzL212Yy9jb250cm9sbGVyL3BhcmFtcy5tZA=="))
    # app.run(host="0.0.0.0",port = 7788, debug=True)
    print(base64.urlsafe_b64encode("https://www.wish.com/c/5927f53cf4f1d061795465d1"))
    print(base64.urlsafe_b64encode("https://contestimg.wish.com/api/webimage/5927f53cf4f1d061795465d1-contest.jpg?cache_buster=44f8e082e672b9bceff24b4990f53990"))
    print(base64.urlsafe_b64encode("https://www.wish.com/feed/tabbed_feed_latest/product/58ec89e883d6311a530a0df0"))
    gevent_server = WSGIServer(('0.0.0.0', 10004), app)
    gevent_server.serve_forever()