import socket
import time
import msgpack
from tornado import tcpclient
from tornado import gen
from tornado.ioloop import IOLoop


class Client():
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 8000
        self.tcpClient = tcpclient.TCPClient()

    @gen.coroutine
    def _connect(self):
        self.stream = yield self.tcpClient.connect(self.host, self.port)

    def connect(self, host, port):
        IOLoop.current().run_sync(self._connect)
        self.loop = IOLoop.current()

    def start(self):
        self.loop.start()

    def send(self, msg, cb):
        print msg
        self.stream.write(msg)
        self.stream.read_until_close(streaming_callback=cb)

if __name__ == '__main__':
    def cb(data):
        print msgpack.unpackb(data)

    client = Client()
    client.connect('127.0.0.1', 8000)
    client.send('12312', cb)
    client.start()

# msg = msgpack.packb({
#     'msgid': 123,
#     'method': 'sum',
#     'params': msg,
#     'mode': 1,
# })
