# -*- coding: utf-8 -*-

"""
 @desc:
 @author: 孙健
 @site:
"""

import re
import sys
import json
import base64
import hashlib
import datetime
from . import utils
from requests import request
from requests.exceptions import HTTPError

try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote
try:
    from xml.etree.ElementTree import ParseError as XMLError
except ImportError:
    from xml.parsers.expat import ExpatError as XMLError

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)


class eBayError(Exception):
    """
    Main eBay Exception class
    """
    # Allows quick access to the response object.
    # Do not rely on this attribute, always check if its not None.
    response = None


def calc_md5(string):
    """
    Calculates the MD5 encryption for the given string
    """
    md5_hash = hashlib.md5()
    md5_hash.update(string)
    return base64.b64encode(md5_hash.digest()).strip(b'\n')


def calc_request_description(params):
    request_description = ''
    for key in sorted(params):
        encoded_value = quote(params[key], safe='-_.~')
        request_description += '&{}={}'.format(key, encoded_value)
    return request_description[1:]  # don't include leading ampersand


def remove_empty(dict_):
    """
    Returns dict_ with all empty values removed.
    """
    return {k: v for k, v in dict_.items() if v}


def remove_namespace(xml):
    """
    Strips the namespace from XML document contained in a string.
    Returns the stripped string.
    """
    regex = re.compile(' xmlns(:ns2)?="[^"]+"|(ns2:)|(xml:)')
    return regex.sub('', xml)


class DictWrapper(object):
    def __init__(self, xml, rootkey=None):
        self.original = xml
        self.response = None
        self._rootkey = rootkey
        self._mydict = utils.XML2Dict().fromstring(remove_namespace(xml))
        self._response_dict = self._mydict.get(list(self._mydict.keys())[0], self._mydict)

    @property
    def parsed(self):
        if self._rootkey:
            return self._response_dict.get(self._rootkey)
        return self._response_dict


class DataWrapper(object):
    """
    Text wrapper in charge of validating the hash sent by Amazon.
    """
    def __init__(self, data, header):
        self.original = data
        self.response = None
        if 'content-md5' in header:
            hash_ = calc_md5(self.original)
            if header['content-md5'].encode() != hash_:
                raise eBayError("Wrong Contentlength, maybe amazon error...")

    @property
    def parsed(self):
        return self.original


class Exception_Error_Obj(object):

    def __init__(self, e):
        self.status_code = 500
        self.content = json.dumps({'code': 1, 'data': {}, 'message': repr(e)})


class eBayAPI(object):

    request_url = 'https://api.ebay.com/ws/api.dll'
    header = {'X-EBAY-API-SITEID': '0', 'X-EBAY-API-COMPATIBILITY-LEVEL': '989', 'Content-Type': 'application/xml'}

    def __init__(self, appinfo, storeinfo):
        self.storeinfo = storeinfo
        self.header['X-EBAY-API-APP-NAME'] = appinfo['appID']
        self.header['X-EBAY-API-DEV-NAME'] = appinfo['deviceID']
        self.header['X-EBAY-API-CERT-NAME'] = appinfo['certID']
        self.header['X-EBAY-API-SITEID'] = str(self.storeinfo.get('siteID', '0'))
        self.runame = appinfo['runame']
        if appinfo.get('runIP'):
            self.request_url = 'http://%s:9193/fancyqube/api.ebay.com/ws/api.dll' % appinfo['runIP']
        else:
            self.request_url = 'https://api.ebay.com/ws/api.dll'

    def make_request(self, extra_data, method="GET", **kwargs):
        """
        Make request to eBay API with these parameters
        Like MWS API.
        """

        # Remove all keys with an empty value because
        # Amazon's MWS does not allow such a thing.
        extra_data = remove_empty(extra_data)

        # convert all Python date/time objects to isoformat
        for key, value in extra_data.items():
            if isinstance(value, (datetime.datetime, datetime.date)):
                extra_data[key] = value.isoformat()

        headers = self.header
        headers.update(kwargs.get('extra_headers', {}))

        try:
            # Some might wonder as to why i don't pass the params dict as the params argument to request.
            # My answer is, here i have to get the url parsed string of params in order to sign it, so
            # if i pass the params dict as params to request, request will repeat that step because it will need
            # to convert the dict to a url parsed string, so why do it twice if i can just pass the full url :).
            response = request(method, self.request_url, data=kwargs.get('body', ''), headers=headers, timeout=kwargs.get('timeout', None))
            response.raise_for_status()
            # When retrieving data from the response object,
            # be aware that response.content returns the content in bytes while response.text calls
            # response.content and converts it to unicode.

            data = response.content
            # I do not check the headers to decide which content structure to server simply because sometimes
            # Amazon's MWS API returns XML error responses with "text/plain" as the Content-Type.
            rootkey = kwargs.get('rootkey', extra_data.get("Action") + "Result")
            try:
                try:
                    parsed_response = DictWrapper(data, rootkey)
                except TypeError:  # raised when using Python 3 and trying to remove_namespace()
                    # When we got CSV as result, we will got error on this
                    parsed_response = DictWrapper(response.text, rootkey)

            except XMLError:
                parsed_response = DataWrapper(data, response.headers)

        except HTTPError as e:
            error = eBayError(str(e.response.text))
            error.response = e.response
            raise error

        # Store the response object in the parsed_response for quick access
        parsed_response.response = response
        return parsed_response

    def GetItem(self, ItemID):
        extra_headers = {'X-EBAY-API-CALL-NAME': 'GetItem'}

        request_Item = """
            <?xml version="1.0" encoding="utf-8"?>
                <GetItemRequest xmlns="urn:ebay:apis:eBLBaseComponents">
                    <RequesterCredentials>
                        <eBayAuthToken>""" + self.storeinfo['token'] + """</eBayAuthToken>
                    </RequesterCredentials>
                    <ItemID>""" + ItemID + """</ItemID>
                    <DetailLevel>ReturnAll</DetailLevel>
                    <ErrorLanguage>en_US</ErrorLanguage>
                    <WarningLevel>High</WarningLevel>
                </GetItemRequest>
        """

        try:
            response = self.make_request(
                extra_data=dict(Action='GetItem'),
                method='POST',
                body=request_Item,
                extra_headers=extra_headers,
                timeout=60)
        except Exception as e:
            response = Exception_Error_Obj(e)

        return response

    def GetCategory(self, category_id=None, level_limit=None):
        extra_headers = {
            'X-EBAY-API-CALL-NAME': 'GetCategories',
            # 'X-EBAY-API-COMPATIBILITY-LEVEL': '967',
        }

        request_Category = """
            <?xml version="1.0" encoding="utf-8"?>
            <GetCategoriesRequest xmlns="urn:ebay:apis:eBLBaseComponents">
              <RequesterCredentials>
                <eBayAuthToken>""" + self.storeinfo['token'] + """</eBayAuthToken>
              </RequesterCredentials>"""
        if category_id:
            request_Category += "<CategoryParent>" + category_id + "</CategoryParent>"
        request_Category += "<CategorySiteID>" + self.storeinfo.get('siteID', '0') + "</CategorySiteID>"
        request_Category += "<DetailLevel>ReturnAll</DetailLevel>"
        if level_limit:
            request_Category += "<LevelLimit>%s</LevelLimit>" % level_limit
        request_Category += """</GetCategoriesRequest>"""

        try:
            response = self.make_request(
                extra_data=dict(Action='GetCategories'),
                method='POST',
                body=request_Category,
                extra_headers=extra_headers,
                timeout=60
            )
        except Exception as e:
            response = Exception_Error_Obj(e)

        return response


def get_data():
    from skuapp.table.t_config_store_ebay import t_config_store_ebay
    from ebayapp.table.t_developer_info_ebay import t_developer_info_ebay
    store_info = t_config_store_ebay.objects.get(storeName='97k')
    # store_info = t_config_store_ebay.objects.get(storeName='abcmanfashion')
    developer_info = t_developer_info_ebay.objects.get(appID=store_info.appID)
    appinfo = dict()
    appinfo['appID'] = developer_info.appID
    appinfo['deviceID'] = developer_info.deviceID
    appinfo['certID'] = developer_info.certID
    appinfo['runame'] = developer_info.runame
    appinfo['runIP'] = developer_info.runIP
    storeinfo = dict()
    storeinfo['siteID'] = str(store_info.siteID)
    storeinfo['token'] = store_info.token
    ebay_obj = eBayAPI(appinfo, storeinfo)
    ItemID = '362282195180'
    # ItemID = "401513405955"
    # ItemID = "142733669329"
    # ItemID = "262691736386"
    # ItemID = "401551685487"
    response = ebay_obj.GetItem(ItemID=ItemID)
    return response


def handle_description(description):
    html_des = str()
    descriptions = description.split('<!--[Datacaciques code start')
    for i in descriptions:
        if i and not i.endswith('<!--[Datacaciques code end]-->'):
            if i.find('<!--[Datacaciques code end]-->'):
                html_des += i.split('<!--[Datacaciques code end]-->')[-1]
            else:
                html_des += i
        else:
            continue
    html_des = html_des.replace('\n', '').replace('\t', '')
    return html_des


def test():
    response = get_data()
    des = response._response_dict.get('Item').get('Description').get('value')
    tmp_des = handle_description(des)
    return tmp_des
