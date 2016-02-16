from server import Server
from clienttcp import Client
import time
from tornado.ioloop import IOLoop

if __name__ == '__main__':
    class Handler(object):
        def sum(self, a, b):
            time.sleep(2)
            print 'sum', a, b, a + b
            return a + b

    server = Server(Handler())
    server.bind()
    server.start()

    def cb(data):
        print data, 11
    client = Client()
    client.connect('127.0.0.1', 8000)
    client.send('12312', cb)
    # client.start()

    IOLoop.current().start()
    # def cb2(data):
    #     print 'cb2:', data
    # # client.connect('127.0.0.1', 8000)

    # for i in xrange(10000):
    #     ts = time.time()
    #     client = Client()
    #     client.connect('127.0.0.1', 8000)
    #     client.call('sum', [i, i+1], cb1)
    #     te = time.time()
    #     print te-ts
    # client.start()
