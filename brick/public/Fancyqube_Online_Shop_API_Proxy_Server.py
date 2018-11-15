# -*- coding: utf-8 -*-

import sys
import time
import json
import requests
import logging
import logging.handlers
import BaseHTTPServer
import SimpleHTTPServer
from SocketServer import ThreadingMixIn


log_formatter = logging.Formatter('%(asctime)s [%(filename)s %(funcName)s:%(lineno)d] %(thread)d %(levelname)s %(message)s')
logFile = 'Fancyqube_Online_Shop_API_Proxy_Server.log'
my_handler = logging.handlers.RotatingFileHandler(
    logFile,
    mode='a',
    maxBytes=100 * 1024 * 1024,
    backupCount=4,
    encoding=None,
    delay=0)

my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.DEBUG)

logger = logging.getLogger('root')
logger.setLevel(logging.DEBUG)

# Print out log to the console
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

logger.addHandler(my_handler)
logger.addHandler(ch)

DISABLE_HEADERS = [
    'date',
    'server',
    'connection',
    'content-type',
    'content-length',
    'content-encoding',
    'transfer-encoding',
]


class Exception_Error_Obj(object):

    def __init__(self, e):
        self.status_code = 500
        self.content = json.dumps({'code': 1, 'data': {}, 'message': str(e)})


class SETHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def req_get_url(self):
        path = self.path.replace('/fancyqube', '')
        url = 'https:/' + path
        logger.debug('[.] url: %s' % url)

        return url

    def req_get_headers(self):
        headers = self.headers.dict
        logger.debug('[.] headers: %s' % headers)
        if headers.get('host'):
            headers.pop('host')

        return headers

    def req_get_data(self):
        length = int(self.headers.getheader('content-length'))
        qs = self.rfile.read(length)
        logger.debug('[.] qs: %s' % qs)

        if 'xml' in self.headers.getheader('Content-type', ''):
            request_data = qs
        else:
            try:
                request_data = json.loads(qs)
            except Exception as e:
                logger.error("[.] req_get_data error: %s" % repr(e))
                request_data = qs

        logger.debug("[.] request_data: %s" % request_data)

        return request_data

    def req_get_data_type(self):
        if 'json' in self.headers.getheader('Content-type', ''):
            data_type = 'json'
        else:
            data_type = 'data'

        return data_type

    def request_option(self, url, method='get', **kwargs):
        try:
            response = requests.request(method, url, **kwargs)
        except Exception as e:
            response = Exception_Error_Obj(e)

        if url == 'https://':
            response.status_code = 204

        return response

    def return_response(self, response):
        code = 204
        content = {}

        code = response.status_code
        content = response.content
        logger.debug('[.] response content: %s' % content)

        self.send_response(code)
        self.send_head(response)
        self.wfile.write(content)

    def send_head(self, response):
        try:
            headers = response.headers
            logger.debug('[.] response headers: %s' % headers)
            for key, value in headers.items():
                if key.lower() in DISABLE_HEADERS or key.lower().startswith('content'):
                    continue
                self.send_header(key, value)
        except:
            self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logger.debug("[x] Method: GET")

        url = self.req_get_url()
        headers = self.req_get_headers()

        response = self.request_option(url, method='get', headers=headers)

        self.return_response(response)

    def do_OPTIONS(self):
        logger.debug("[x] Method: OPTIONS")

        url = self.req_get_url()
        headers = self.req_get_headers()

        response = self.request_option(url, method='options', headers=headers)

        self.return_response(response)

    def do_HEAD(self):
        logger.debug("[x] Method: HEAD")

        url = self.req_get_url()
        headers = self.req_get_headers()

        response = self.request_option(url, method='head', headers=headers)

        self.return_response(response)

    def do_POST(self):
        logger.debug("[x] Method: POST")

        url = self.req_get_url()
        headers = self.req_get_headers()
        request_data = self.req_get_data()
        data_type = self.req_get_data_type()

        if data_type == 'json':
            response = self.request_option(url, method='post', json=request_data, headers=headers)
        else:
            response = self.request_option(url, method='post', data=request_data, headers=headers)

        self.return_response(response)

    def do_PUT(self):
        logger.debug("[x] Method: PUT")

        url = self.req_get_url()
        headers = self.req_get_headers()
        request_data = self.req_get_data()
        data_type = self.req_get_data_type()

        if data_type == 'json':
            response = self.request_option(url, method='put', json=request_data, headers=headers)
        else:
            response = self.request_option(url, method='put', data=request_data, headers=headers)

        self.return_response(response)

    def do_PATCH(self):
        logger.debug("[x] Method: PATCH")

        url = self.req_get_url()
        headers = self.req_get_headers()
        request_data = self.req_get_data()
        data_type = self.req_get_data_type()

        if data_type == 'json':
            response = self.request_option(url, method='patch', json=request_data, headers=headers)
        else:
            response = self.request_option(url, method='patch', data=request_data, headers=headers)

        self.return_response(response)

    def do_DELETE(self):
        logger.debug("[x] Method: DELETE")

        url = self.req_get_url()
        headers = self.req_get_headers()
        request_data = self.req_get_data()
        data_type = self.req_get_data_type()

        if data_type == 'json':
            response = self.request_option(url, method='delete', json=request_data, headers=headers)
        else:
            response = self.request_option(url, method='delete', data=request_data, headers=headers)

        self.return_response(response)


class ThreadedHTTPServer(ThreadingMixIn, BaseHTTPServer.HTTPServer):
    pass


class Server():

    def __init__(self):
        self.Protocol = "HTTP/1.0"

        if sys.argv[1:]:
            port = int(sys.argv[1])
        else:
            port = 9193

        self.server_address = ('0.0.0.0', port)

    def listen_client(self):
        SETHandler.protocol_version = self.Protocol
        httpd = ThreadedHTTPServer(self.server_address, SETHandler)

        sa = httpd.socket.getsockname()
        logger.debug("[x] Serving HTTP on %s port %s ..." % (sa[0], sa[1]))

        httpd.serve_forever()


def retry():
    try:
        c = Server()
        c.listen_client()
        time.sleep(0.5)
    except Exception as e:
        logger.error(e)
        time.sleep(0.5)
        retry()


if __name__ == '__main__':
    retry()
