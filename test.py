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
