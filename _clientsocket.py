import netutils
import config
from tornado import tcpclient
from tornado import gen
from tornado.ioloop import IOLoop
import time
import os
import resource
resource.setrlimit(resource.RLIMIT_NOFILE, (10000, 10000))


class Client():
    def __init__(self, host, port):
        self.tcpClient = tcpclient.TCPClient()
        self.mode = config.SYNC_MODE
        self.host = host
        self.port = port

    # @gen.coroutine
    # def _connect(self):
    #     self.stream = yield self.tcpClient.connect(self.host, self.port)

    # def connect(self, host, port):
    #     self.host = host
    #     self.port = port
    #     IOLoop.current().run_sync(self._connect)

    @gen.coroutine
    def _connect(self, cb):
        stream = yield self.tcpClient.connect(self.host, self.port)
        cb(stream)

    def call(self, method_name, params, cb):
        def call_async(stream):
            # print 'connect cb'
            msg = {
                'msgid': next(generator),
                'method': method_name,
                'params': params,
                'mode': self.mode
            }
            # print 'send msgid:', msg['msgid'], os.getpid()

            def recv_cb(data):
                # print 'send cb'
                stream.close()
                cb(data)

            netutils.send(stream, msg, callback=lambda: netutils.recv(stream, recv_cb))
        self._connect(call_async)

    def set_sync(self):
        self.mode = config.SYNC_MODE

    def set_async(self):
        self.mode = config.ASYNC_MODE


def msgid_generator():
    counter = 0
    while True:
        yield counter
        counter += 1
        if counter > (1 << 30):
            counter = 0

generator = msgid_generator()

# -----------------------
start = time.time()


def cb1(data):
    # print 'cb1:', data
    end = time.time()
    print end - start
    pass
    # print 'cb1:', data


def test():
    # start = time.time()
    for i in xrange(3000):
        # ts = time.time()
        # print 'before client'
        client = Client('127.0.0.1', 8000)
        # client.set_async()
        # client.connect('127.0.0.1', 8000)
        # print 'before call'
        client.call('sum', [i, i+1], cb1)
        # data = client.call('sum', [i, i+1])
        # print data
        # te = time.time()
        # print te-ts
    end = time.time()
    print end - start

if __name__ == '__main__':

    def cb2(data):
        print 'cb2:', data
    # client.connect('127.0.0.1', 8000)
    test()

    IOLoop.current().start()
    # client.start()
