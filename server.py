from functools import partial
from tornado.ioloop import IOLoop
from tornado import tcpserver
import msgpack
import config
import time


class TCPServer(tcpserver.TCPServer):
    def __init__(self, callback):
        super(TCPServer, self).__init__()
        self.callback = callback

    def handle_stream(self, stream, address):
        self.callback(stream, address)


class Server():
    def __init__(self, handler):
        self.handler = handler
        self.tcpServer = TCPServer(self.handle_stream)

    def bind(self, port=8000):
        self.port = port
        self.tcpServer.bind(self.port)

    def start(self, process=2):
        self.process = process
        self.tcpServer.start(process)
        self.loop = IOLoop.current()
        self.loop.start()

    def handle_stream(self, stream, address):
        stream.read_until_close(streaming_callback=lambda data: self.handle_line(data, stream))

    def handle_line(self, data, stream):
        send_msg = partial(self.send_msg, stream=stream)
        try:
            method, params, mode = msgpack.unpackb(data)
            if not hasattr(self.handler, method):
                send_msg(config.METHOD_MISS)
            else:
                if mode == config.SYNC_MODE:
                    res = getattr(self.handler, method)(*params)
                    send_msg([config.SUCCESS[0], res])
                elif mode == config.ASYNC_MODE:
                    self.loop.add_callback(getattr(self.handler, method), *params)
                    send_msg(config.SUCCESS)
                else:
                    send_msg(config.MODE_INVALID)
        except:
            send_msg(config.UNPACK_ERROR)

    def send_msg(self, msg, stream):
        stream.write(msgpack.packb(msg))


if __name__ == '__main__':
    class Handler(object):
        def sum(self, a, b):
            time.sleep(2)
            print 'sum', a, b, a + b
            return a + b

    server = Server(Handler())
    server.bind()
    server.start()
