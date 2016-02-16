# -*- coding: utf-8 -*-
from tornado import tcpclient
from tornado import gen
from tornado.ioloop import IOLoop

import config
import netutils


class Client():
    def __init__(self):
        self.tcpClient = tcpclient.TCPClient()
        self.gen_id = self._gen_id()

    def _gen_id(self):
        counter = 0
        COUNTER_MAX = 1 << 30
        while True:
            yield counter
            counter += 1
            if counter > COUNTER_MAX:
                counter = 0

    @gen.coroutine
    def _connect(self):
        self.stream = yield self.tcpClient.connect(self.host, self.port)

    def connect(self, host, port):
        self.host = host
        self.port = port
        IOLoop.current().run_sync(self._connect)
        return self
        # TODO when connection has been disconnected, connect server
        # self.stream.set_close_callback(lambda: IOLoop.current().run_sync(self._connect))

    def _request(self, method, params=[], mode=config.CALL_MODE, cb=None):
        msg = {
            'id': next(self.gen_id),
            'method': method,
            'params': params,
            'mode': mode,
        }
        netutils.send(self.stream, msg)
        netutils.recv(self.stream, cb)

    def call(self, method, params=[], cb=None):
        self._request(method, params, config.CALL_MODE, cb)

    def notify(self, method, params=[], cb=None):
        self._request(method, params, config.NOTI_MODE, cb)

    def close(self):
        if not self.stream.closed():
            self.stream.close()
        else:
            print 'client already closed.'


if __name__ == '__main__':
    def cb(data):
        print 'sum:', data

    client = Client()
    client.connect('127.0.0.1', 8000).call('sum', [123, 456], cb)
    client.connect('127.0.0.1', 8000).call('multi', [123, 456], cb)
    client.connect('127.0.0.1', 8000).notify('sum', [123, 456], cb)
    client.connect('127.0.0.1', 8000).notify('multi', [123, 456], cb)
    IOLoop.current().start()
