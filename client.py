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

    @gen.coroutine
    def _request(self, msg, mode=config.CALL_MODE):
        yield netutils.send(self.stream, msg)
        data = yield netutils.recv(self.stream)
        raise gen.Return(data)

    @gen.coroutine
    def call(self, msg):
        data = yield self._request(msg, mode=config.CALL_MODE)
        raise gen.Return(data)

    @gen.coroutine
    def notify(self, msg):
        data = yield self._request(msg, mode=config.NOTI_MODE)
        raise gen.Return(data)


if __name__ == '__main__':
    def cb_async(data):
        print data, 'cb_async'

    client = Client()
    client.set_host('127.0.0.1', 8000)
    client.call_async('sum', [5, 6], cb=cb_async)
    client.call_async('sum', [5, 6], cb=cb_async)

    IOLoop.current().start()
