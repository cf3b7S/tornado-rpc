import netutils
import config
from tornado import tcpclient
from tornado import gen
from tornado.ioloop import IOLoop


class Client():
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 8000
        self.tcpClient = tcpclient.TCPClient()
        self.mode = config.SYNC_MODE

    @gen.coroutine
    def _connect(self):
        self.stream = yield self.tcpClient.connect(self.host, self.port)

    def connect(self, host, port):
        IOLoop.current().run_sync(self._connect)

    def start(self):
        self.loop = IOLoop.current()
        self.loop.start()

    def send(self, method_name, params):
        msg = {
            'msgid': 123,
            'method': method_name,
            'params': params,
            'mode': self.mode
        }
        netutils.send(self.stream, msg)

    def recv(self, cb):
        netutils.recv(self.stream, cb)

    def setSync(self):
        self.mode = config.SYNC_MODE

    def setAsync(self):
        self.mode = config.ASYNC_MODE


if __name__ == '__main__':
    def cb(data):
        print data
    client = Client()
    client.connect('127.0.0.1', 8000)
    client.send('sum', [1, 2])
    client.recv(cb)
    client.start()
