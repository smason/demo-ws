import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind('ipc://zmq.S')

while True:
    msg = str(time.time())
    print "** sending {}".format(msg)
    socket.send_string(msg)
    time.sleep(1)
