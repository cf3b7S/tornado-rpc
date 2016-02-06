# -*- coding: utf-8 -*-
import netutils
import config
from tornado import tcpclient
from tornado import gen
from tornado.ioloop import IOLoop
import time


class Client():
    def __init__(self):
        self.tcpClient = tcpclient.TCPClient()
        self.mode = config.SYNC_MODE

    @gen.coroutine
    def _connect(self):
        self.stream = yield self.tcpClient.connect(self.host, self.port)

    def connect(self, host, port):
        self.host = host
        self.port = port
        IOLoop.current().run_sync(self._connect)
        # TODO when connection has been disconnected, connect server
        # self.stream.set_close_callback(lambda: IOLoop.current().run_sync(self._connect))

    def call(self, method_name, params, cb):
        msg = {
            'msgid': next(generator),
            'method': method_name,
            'params': params,
            'mode': self.mode
        }
        print 'send msgid:', msg['msgid']
        netutils.send(self.stream, msg)

        def recv_cb(data):
            self.stream.close()
            cb(data)
        netutils.recv(self.stream, recv_cb)

    def setSync(self):
        self.mode = config.SYNC_MODE

    def setAsync(self):
        self.mode = config.ASYNC_MODE

    def close(self):
        if not self.stream.closed():
            self.stream.close()


def msgid_generator():
    counter = 0
    while True:
        yield counter
        counter += 1
        if counter > (1 << 30):
            counter = 0

generator = msgid_generator()


def cb1(data):
    print 'cb1:', data

if __name__ == '__main__':

    def cb2(data):
        print 'cb2:', data
    # client.connect('127.0.0.1', 8000)

    for i in xrange(10000):
        ts = time.time()
        client = Client()
        client.connect('127.0.0.1', 8000)
        client.call('sum', [i, i+1], cb1)
        te = time.time()
        print te-ts

    IOLoop.current().start()
    # client.start()
