from server import Server
from client import Client
import time
import os
import logging
from tornado.ioloop import IOLoop


def cb_sync(client, data):
    # TODO OK
    # client.close()
    # print data, 'cb_sync'
    pass


def cb_async(data):
    # print data, 'cb_async'
    pass


def test_sync_call():
    client = Client()
    client.connect('127.0.0.1', 8000)
    client.call('sum', [1, 2], cb=lambda data: cb_sync(client, data))


def test_sync_notify():
    client = Client()
    client.connect('127.0.0.1', 8000)
    client.notify('sum', [3, 4], cb=lambda data: cb_sync(client, data))


def test_async_call():
    client = Client()
    client.set_host('127.0.0.1', 8000)
    client.call_async('sum', [5, 6], cb=cb_async)


def test_async_notify():
    client = Client()
    client.set_host('127.0.0.1', 8000)
    client.call_async('sum', [5, 6], cb=cb_async)


if __name__ == '__main__':
    if not logging.getLogger().handlers:
        logging.basicConfig()

    # class Handler(object):
    #     def sum(self, a, b):
    #         print 'sum', a, b, a + b, os.getpid()
    #         return a + b

    # server = Server(Handler())
    # server.bind()
    # server.start()

    ts = time.time()
    for i in xrange(10000):
        # 2process 7.21562886238 10000
        # test_sync_call()

        # 2process 7.70088887215 10000
        # test_sync_notify()

        # 2process 0.0398619174957 100
        test_async_call()

        # test_async_notify()

    print time.time() - ts

    IOLoop.current().start()
