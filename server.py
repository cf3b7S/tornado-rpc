# -*- coding: utf-8 -*-
from functools import partial
from tornado import gen, tcpserver
from tornado.ioloop import IOLoop
from tornado.iostream import StreamClosedError

import config
import netutils


class TCPServer(tcpserver.TCPServer):
    def __init__(self, callback):
        super(TCPServer, self).__init__()
        self.callback = callback

    def handle_stream(self, stream, address):
        self.callback(stream, address)


class Server():
    def __init__(self):
        self.tcp_server = TCPServer(self.handle_stream)

    def bind(self, port=8000):
        self.port = port
        self.tcp_server.bind(self.port)
        return self

    def start(self, process=1):
        self.process = process
        self.tcp_server.start(process)
        return self

    @gen.coroutine
    def handle_stream(self, stream, address):
        while True:
            try:
                data = yield netutils.recv(stream)
                self.handle_line(data, stream)
            except StreamClosedError:
                break

    def handle_line(self, data, stream):
        send_msg = partial(self.send_msg, stream=stream)
        return send_msg(data)

    def send_msg(self, msg, stream):
        netutils.send(stream, msg)


if __name__ == '__main__':

    server = Server()
    server.bind()
    server.start(1)

    IOLoop.current().start()
