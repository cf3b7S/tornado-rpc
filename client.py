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



    # client.send('asdfsadf')




# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect(('127.0.0.1', 8000))


# # msg = ["request", "3", {"adlist": ["h.10"], "x": {"pub_id": "xxx", "pub_type": "xxx", "uid": "xxx", "ip": "8.8.8.8", "ua": "Mozilla/5.0 (Macintosh", " Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36": "", "category": "80203", "country": "GOOGLE", "province": "GOOGLE", "day_of_week": "2", "time_period": "2", "url_domain": "stock.qq.com", "url_path": "stock.qq.com/original/zqyjy/s591.html", "browser": "Other", "browser_version": "Other", "os": "Other", "os_version": "Other"}, "query": {"pub_id": "xxx", "pub_type": "xxx", "uid": "xxx", "ip": "8.8.8.8", "ua": "Mozilla/5.0 (Macintosh", " Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36": "", "url": "http://stock.qq.com/original/zqyjy/s591.html", "category": "80203"}, "time": 1454475352.597586}]
# # msg = msgpack.packb(('method', msg))
# msg = [1, 4]
# msg = msgpack.packb(('sum', msg, 2))
# msg = msgpack.packb({
#     'msgid': 123,
#     'method': 'sum',
#     'params': msg,
#     'mode': 1,
# })

# # method

# # s.sendall(msg)
# s.sendall(msg + 'a')

# data = s.recv(1024)
# data = msgpack.unpackb(data)
# print 'Received', repr(data)

# time.sleep(10)
# s.close()
