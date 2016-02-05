# -*- coding: utf-8 -*-
from functools import partial
from tornado.ioloop import IOLoop
from tornado import tcpserver
import config
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

    def handle_stream(self, stream, address):
        netutils.recv(stream, callback=lambda data: self.handle_line(data, stream))
        # stream.read_until_close(streaming_callback=lambda data: self.handle_line(data, stream))]

    def handle_line(self, data, stream):
        send_msg = partial(self.send_msg, stream=stream)
        msgid = data['msgid']
        mode = data['mode']
        method = data['method']
        params = data['params']

        result = {
            'msgid': msgid,
            'result': None,
            'code': None,
            'msg': None
        }
        # handle key miss error
        key_miss_error = None
        for key in config.keyMissMap:
            if key_miss_error:
                break
            if key not in data:
                key_miss_error = config.keyMissMap[key]
        if key_miss_error:
            result['code'] = key_miss_error[0]
            result['msg'] = key_miss_error[1]
            return send_msg(result)

        # handle method invalid
        if not hasattr(self.handler, data['method']):
            result['code'] = config.METHOD_INVALID[0]
            result['msg'] = config.METHOD_INVALID[1]
            return send_msg(result)

        if mode == config.SYNC_MODE:
            method_result = getattr(self.handler, method)(*params)
            result['code'] = config.SUCCESS[0]
            result['msg'] = config.SUCCESS[1]
            result['result'] = method_result
            return send_msg(result)
        elif mode == config.ASYNC_MODE:
            IOLoop.current().add_callback(getattr(self.handler, method), *params)
            result['code'] = config.SUCCESS[0]
            result['msg'] = config.SUCCESS[1]
            return send_msg(result)
        else:
            result['code'] = config.MODE_INVALID[0]
            result['msg'] = config.MODE_INVALID[1]
            return send_msg(result)

    # def send_msg(self, msg, stream, result=None):
    #     if result:
    #         msg[1] = result
    #     stream.write(msgpack.packb(msg))

    def send_msg(self, msg, stream):
        netutils.send(stream, msg)

if __name__ == '__main__':
    class Handler(object):
        def sum(self, a, b):
            print 'sum', a, b, a + b
            return a + b

    server = Server(Handler())
    server.bind()
    server.start()
    IOLoop.current().start()
