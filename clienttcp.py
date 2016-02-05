import netutils
import config
from tornado import tcpclient
from tornado import gen
from tornado.ioloop import IOLoop


class Client():
    def __init__(self):
        self.tcpClient = tcpclient.TCPClient()
        self.mode = config.SYNC_MODE
        self.generator = _msgid_generator()

    @gen.coroutine
    def _connect(self):
        self.stream = yield self.tcpClient.connect(self.host, self.port)

    def connect(self, host, port):
        self.host = host
        self.port = port
        IOLoop.current().run_sync(self._connect)
        # TODO
        # self.stream.set_close_callback(lambda: IOLoop.current().run_sync(self._connect))

    def call(self, method_name, params, cb):
        msg = {
            'msgid': next(self.generator),
            'method': method_name,
            'params': params,
            'mode': self.mode
        }
        netutils.send(self.stream, msg)
        netutils.recv(self.stream, cb)

    def setSync(self):
        self.mode = config.SYNC_MODE

    def setAsync(self):
        self.mode = config.ASYNC_MODE


def _msgid_generator():
    counter = 0
    while True:
        yield counter
        counter += 1
        if counter > (1 << 30):
            counter = 0


if __name__ == '__main__':
    def cb1(data):
        print 'cb1:', data

    def cb2(data):
        print 'cb2:', data
    client = Client()
    client.connect('127.0.0.1', 8000)

    for i in xrange(10000):
        client.call('sum', [i, i+1], cb1)
    # client.connect('127.0.0.1', 8000)
    # client.call('sum', [3, 4], cb2)
    IOLoop.current().start()
    # client.start()
