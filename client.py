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

    def set_host(self, host, port):
        # only used before call method 'call_async' and 'notify_async'.
        # before call method 'call' and 'notify' use method 'connect' to set host and port.
        self.host = host
        self.port = port

    def _request(self, method, params=[], mode=config.CALL_MODE, cb=None):
        msg = {
            'id': next(self.gen_id),
            'method': method,
            'params': params,
            'mode': mode,
        }
        netutils.send(self.stream, msg)
        netutils.recv(self.stream, cb)

    @gen.coroutine
    def _connect_async(self, cb=None):
        self.stream = yield self.tcpClient.connect(self.host, self.port)
        if cb:
            cb()

    def _request_async(self, method, params, mode=config.CALL_MODE, cb=None):
        def send_async():
            msg = {
                'id': next(self.gen_id),
                'method': method,
                'params': params,
                'mode': mode
            }

            def recv_cb(data):
                # self.close()
                if cb:
                    cb(data)

            netutils.send(self.stream, msg, cb=netutils.recv(self.stream, cb))
        self._connect_async(send_async)

    def call_async(self, method, params=[], cb=None):
        self._request_async(method, params, mode=config.CALL_MODE, cb=cb)

    def notify_async(self, method, params=[], cb=None):
        self._request_async(method, params, mode=config.NOTI_MODE, cb=cb)

    def call(self, method, params=[], cb=None):
        self._request(method, params, mode=config.CALL_MODE, cb=cb)

    def notify(self, method, params=[], cb=None):
        self._request(method, params, mode=config.NOTI_MODE, cb=cb)

    # def close(self):
    #     # only use this method in method 'call' and 'notify' 's callback method.
    #     # when use method 'call_async' and 'notify_async', don't need to call this method.
    #     if not self.stream.closed():
    #         self.stream.close()
    #     else:
    #         print 'client already closed.'
