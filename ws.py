import time
import uwsgi

import gevent

from django.utils import crypto

def reader(uid, ws):
    while True:
        try:
            msg = ws.recv()
            print(msg)
        except IOError:
            return

def writer(uid, ws):
    while True:
        gevent.sleep(1)
        try:
            ws.send("{uid} - {time}".format(
                uid=uid, time=time.time()))
        except IOError:
            return

class WebSocketUWSGI(object):
    def __init__(self, request_context):
        self.request_context = request_context

    def send(self, obj):
        uwsgi.websocket_send(obj, request_context=self.request_context)

    def recv(self):
        return uwsgi.websocket_recv(request_context=self.request_context)

def application(env, start_response):
    print env['CC_USER']
    uid = crypto.get_random_string()
    uwsgi.websocket_handshake()

    reqctx = uwsgi.request_context()
    print reqctx
    ws = WebSocketUWSGI(reqctx)

    gevent.joinall([
        gevent.spawn(writer, uid, ws),
        gevent.spawn(reader, uid, ws),
    ])
    return []
