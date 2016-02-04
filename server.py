# -*- coding: utf-8 -*-
from functools import partial
from tornado.ioloop import IOLoop
from tornado import tcpserver
import msgpack
import config
import time
import netutils


class TCPServer(tcpserver.TCPServer):
    def __init__(self, callback):
        super(TCPServer, self).__init__()
        self.callback = callback

    def handle_stream(self, stream, address):
        self.callback(stream, address)


class Server():
    def __init__(self, handler):
        self.handler = handler
        self.tcp_server = TCPServer(self.handle_stream)

    def bind(self, port=8000):
        self.port = port
        self.tcp_server.bind(self.port)

    def start(self, process=2):
        self.process = process
        self.tcp_server.start(process)
        # self.loop = IOLoop.current()
        # self.loop.start()

    def handle_stream(self, stream, address):
        # netutils.recv(stream, callback=lambda data: self.handle_line(data, stream))
        stream.read_until_close(streaming_callback=lambda data: self.handle_line(data, stream))

    def handle_line(self, data, stream):
        send_msg = partial(self.send_msg, stream=stream)
        try:
            data = msgpack.unpackb(data)
        except:
            return send_msg(config.UNPACK_ERROR)

        # handle key miss error
        key_miss_error = None
        for key in config.keyMissMap:
            if key_miss_error:
                return
            if key not in data:
                key_miss_error = config.keyMissMap[key]
        if key_miss_error:
            return send_msg(key_miss_error)

        # handle method invalid
        if not hasattr(self.handler, data['method']):
            return send_msg(config.METHOD_INVALID)

        mode = data['mode']
        method = data['method']
        params = data['params']
        if mode == config.SYNC_MODE:
            result = getattr(self.handler, method)(*params)
            return send_msg(config.SUCCESS, result=result)
        elif mode == config.ASYNC_MODE:
            # self.loop.add_callback(getattr(self.handler, method), *params)
            IOLoop.current().add_callback(getattr(self.handler, method), *params)
            return send_msg(config.SUCCESS)
        else:
            return send_msg(config.MODE_INVALID)

    def send_msg(self, msg, stream, result=None):
        if result:
            msg[1] = result
        stream.write(msgpack.packb(msg))

    # def send_msg(self, msg, stream):
    #     netutils.send(stream, msg)
    #     # stream.write(msgpack.packb(msg))

if __name__ == '__main__':
    class Handler(object):
        def sum(self, a, b):
            time.sleep(2)
            print 'sum', a, b, a + b
            return a + b

    server = Server(Handler())
    server.bind()
    server.start()
