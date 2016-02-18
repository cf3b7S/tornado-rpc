from server import Server
from client import Client
import time
import os
from tornado.ioloop import IOLoop


def cb_sync(client, data):
    # TODO OK
    # client.close()
    print data, 'cb_sync'


def cb_async(data):
    print data, 'cb_async'


def test_sync_call():
    client = Client()
    client.connect('127.0.0.1', 8000)
    client.call('sum', [1, 2], cb=lambda data: cb_sync(client, data))


def test_sync_notify():
    client = Client()
    client.connect('127.0.0.1', 8000)
    client.notify('sum', [3, 4], cb=lambda data: cb_sync(client, data))


def test_async():
    client = Client()
    client.set_host('127.0.0.1', 8000)
    client.call_async('sum', [5, 6], cb=cb_async)
    client.notify_async('sum', [7, 8], cb=cb_async)


if __name__ == '__main__':
    class Handler(object):
        def sum(self, a, b):
            print 'sum', a, b, a + b, os.getpid()
            return a + b

    server = Server(Handler())
    server.bind()
    server.start()

    test_sync_call()
    test_sync_notify()
    test_async()

    IOLoop.current().start()
