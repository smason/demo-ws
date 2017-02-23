import time
import uwsgi

import gevent

from django.utils import crypto

def reader(uid, ws):
    while True:
        try:
            msg = ws.recv()
        except IOError:
            break

        print(msg)

def writer(uid, ws):
    while True:
        gevent.sleep(1)
        msg = "{uid} - {time}, clients = {nclients}".format(
            uid=uid, time=time.time(),
            nclients=len(clients))

        try:
            ws.send(msg)
        except IOError:
            break

class WebSocketUWSGI(object):
    def __init__(self):
        uwsgi.websocket_handshake()
        self.request_context = uwsgi.request_context()

    def send(self, obj):
        uwsgi.websocket_send(obj, request_context=self.request_context)

    def recv(self):
        return uwsgi.websocket_recv(request_context=self.request_context)

clients = {}

@gevent.spawn
def zmqClient():
    import zmq.green as zmq

    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect('ipc://zmq.S')

    # subscribe to everything
    socket.setsockopt(zmq.SUBSCRIBE, '')

    while True:
        server_msg = socket.recv()

        print "*** sending {} to {} clients".format(server_msg, len(clients))

        for uid,ws in clients.iteritems():
            msg = "{uid} {msg}".format(
                uid=uid, msg=server_msg)
            try:
                ws.send(msg)
            except IOError:
                print "error sending to {}".format(uid)

def application(env, start_response):
    print env['PATH_INFO']

    ws = WebSocketUWSGI()

    uid = crypto.get_random_string()
    clients[uid] = ws
    try:
        gevent.joinall([
            # gevent.spawn(writer, uid, ws),
            gevent.spawn(reader, uid, ws),
        ])
    finally:
        del clients[uid]
    return []
