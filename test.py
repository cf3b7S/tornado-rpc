from server import Server
from client import Client
import time
import os
import logging
from tornado.ioloop import IOLoop
import resource
from multiprocessing import Process

resource.setrlimit(resource.RLIMIT_NOFILE, (65536, 65536))

ts = 0
cnt = 0

process_num = 4

muti_flg = False
if muti_flg:
    loop_num = 2500
else:
    loop_num = 10000


def cb_sync(client, data):
    # print data, 'cb_sync'
    global cnt
    global ts

    cnt += 1
    # print cnt, os.getpid(), 'callback'
    if cnt == loop_num:
        te = time.time()
        print te - ts
    pass


def cb_async(data):
    # print data, 'cb_async'
    pass


def test_sync_call():
    client = Client()
    client.connect('127.0.0.1', 8000)
    client.call('sum', [0, 1], cb=lambda data: cb_sync(client, data))


def test_sync_notify():
    client = Client()
    client.connect('127.0.0.1', 8000)
    client.notify('sum', [3, 4], cb=lambda data: cb_sync(client, data))


def test_async_call():
    client = Client()
    client.set_host('127.0.0.1', 8000)
    client.call_async('sum', [5, 6], cb=cb_async)
    # client.call_async('sum', [5, 6], cb=cb_async)


def test_async_notify():
    client = Client()
    client.set_host('127.0.0.1', 8000)
    client.call_async('sum', [5, 6], cb=cb_async)


def multi_test_sync_call():
    print "start", time.time() - ts
    for i in xrange(loop_num):
        # print i, os.getpid()
        test_sync_call()
    IOLoop.current().start()


def muti_process_test():
    global ts
    ts = time.time()

    for j in xrange(process_num):
        p = Process(target=multi_test_sync_call)
        p.start()


def singal_process_test():
    global ts
    ts = time.time()

    for i in xrange(loop_num):
        # 2process 7.21562886238 10000
        test_sync_call()

        # 2process 7.70088887215 10000
        # test_sync_notify()

        # 2process 0.0398619174957 100
        # test_async_call()

        # test_async_notify()
        # te = time.time()
        # all_time += te - ts
        # print te - ts
    IOLoop.current().start()

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

    if muti_flg:
        muti_process_test()
    else:
        singal_process_test()

