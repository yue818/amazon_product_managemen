#-*-coding:utf-8-*-

"""  
 @desc:  
 @author: changyang  
 @site: 
 @software: PyCharm
 @file: to_translation.py
 @time: 2018-09-06 15:30
"""
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import urllib
import requests

import traceback
import re


def to_translate (FromLanguage,Translated,ToLanguage):
    result = ''
    try:
        appcode = "2cd4ea81891e4118bee6ecfae5d0f2f1"

        host = 'http://jisuzxfy.market.alicloudapi.com'
        path = '/translate/translate'
        querys = "from=" + FromLanguage + "&" + "%s"%(urllib.urlencode({"text":Translated})) + "&to=" + ToLanguage + "&type=google"
        request_url = host + path + "?" + querys

        headers = {'Content-Type':'application/json; charset=utf-8'}
        headers['Authorization'] = 'APPCODE %s' % appcode

        r = requests.get(request_url, headers=headers, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data['status'] == '0':
                results = data['result']['result']
                if '<br />' in results:
                    result = re.findall(r'^([\s\S]*?)<br />[\s\S]*?<br />', results)[0]
                else:
                    result = results
        else:
            data = r.json()
            print 'error', data['msg']

    except Exception,ex:
        print '%s_%s:%s'%(traceback.print_exc(),Exception,ex)

    return result

def concatall(Translated):
    FromLanguage = 'en'
    ToLanguage = ["es", "pt", "fr", "de", "it", "sv", "pl", "no"]

    result = [ to_translate(FromLanguage, Translated, to) for to in ToLanguage]
    return result


if __name__ == "__main__":
    Translated = 'hello china'
    result = concatall(Translated)

    print result
    print type(result)
    


'''"西班牙语": "es",
"葡萄牙语": "pt",
"法语": "fr",
"德语": "de",
"意大利语": "it",
"瑞典语": "sv"
"波兰语": "pl",
"挪威语": "no"'''