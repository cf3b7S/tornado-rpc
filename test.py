# -*- coding: utf-8 -*-
# from server import Server
from client import Client
import time
import os
import logging
from tornado import gen
from tornado.ioloop import IOLoop
from tornado import process

muti_flg = False
all_loop_num = 1000000
process_num = 100

if muti_flg:
    loop_num = all_loop_num / process_num
else:
    loop_num = all_loop_num

ts = 0
cnt = 0
# host = '192.168.8.189'
host = '127.0.0.1'
port = 8000

def cb_sync(client, data):
    # print data, 'cb_sync', os.getpid()
    global cnt
    global ts

    cnt += 1
    if cnt == loop_num:
        te = time.time()
        print te - ts, os.getpid()
    pass


def cb_async(data):
    # print data, 'cb_async'
    pass


@gen.coroutine
def test_sync_call(client, i):
    data = yield client.call('hello')
    cb_sync(client, data)


@gen.coroutine
def test_sync_notify(client, i):
    data = yield client.notify('hello')
    cb_sync(client, data)


@gen.coroutine
def multi_test():
    # print "start", time.time() - ts
    client = Client()
    client.connect(host, port)

    for i in xrange(loop_num):
        # print i, os.getpid()
        # yield test_sync_call(client, i)
        yield test_sync_notify(client, i)


def muti_process_test():
    global ts
    ts = time.time()

    process.fork_processes(process_num)
    multi_test()


@gen.coroutine
def singal_process_test():
    global ts
    ts = time.time()
    client = Client()
    client.connect(host, port)

    for i in xrange(loop_num):
        yield test_sync_call(client, i)
        # yield test_sync_notify(client, i)


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

    IOLoop.current().start()
