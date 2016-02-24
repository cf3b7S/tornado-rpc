# -*- coding: utf-8 -*-
from tornado import tcpclient
from tornado import gen
from tornado.ioloop import IOLoop
from functools import partial

import config
import netutils


class Client():
    def __init__(self):
        self.tcpClient = tcpclient.TCPClient()
        self.gen_id = self._gen_id()
        self.call = partial(self._request, mode=config.CALL_MODE)
        self.notify = partial(self._request, mode=config.NOTI_MODE)

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

    @gen.coroutine
    def _request(self, method, params=[], mode=config.CALL_MODE):
        if self.stream.closed():
            # when connection has been disconnected, connect server
            yield self._connect()
        msg = {
            'id': next(self.gen_id),
            'method': method,
            'params': params,
            'mode': mode,
        }
        yield netutils.send(msg, self.stream)
        data = yield netutils.recv(self.stream)
        raise gen.Return(data)

    def close(self):
        if not self.stream.closed():
            self.stream.close()
        else:
            print 'client already closed.'


if __name__ == '__main__':
    def cb_async(data):
        print data, 'cb_async'

    client = Client()
    client.set_host('127.0.0.1', 8000)
    client.call_async('sum', [5, 6], cb=cb_async)
    client.call_async('sum', [5, 6], cb=cb_async)

    IOLoop.current().start()
