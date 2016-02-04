import socket
import struct
import config
import time
import netutils
import msgpack
from tornado import iostream, ioloop

class Client(object):

    def __init__(self, sock=None, io_loop=None, max_buffer_size=None, read_chunk_size=None, max_write_buffer_size=None):
        if not sock:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.stream = iostream.IOStream(sock, io_loop, max_buffer_size, read_chunk_size, max_write_buffer_size)
        self.mode = config.SYNC_MODE

    def connection(self, host='127.0.0.1', port=8000, callback=None, server_hostname=None):
        self.stream.connect((host, port))

    def setSync(self):
        self.mode = config.SYNC_MODE

    def setAsync(self):
        self.mode = config.ASYNC_MODE

    def recv(self, callback):
        netutils.recv(self.stream, callback)
        # raw_msg = self._recv_all(4)
        # len_msg = struct.unpack('>I', raw_msg)[0]
        # msg = self._recv_all(len_msg)
        # data = msgpack.unpackb(msg)
        # return data

    # def _recv_all(self, length):
    #     msg = ''
    #     while len(msg) < length:
    #         print length - len(msg)
    #         packet = self.socket.recv(length - len(msg))
    #         print packet
    #         # if not packet:
    #         #     return None
    #         msg += packet
    #     return msg

    def send(self, method, param):
        data = {'msgid': 123, 'method': method, 'params': param, 'mode': self.mode}
        netutils.send(self.stream, data)
        # msg = msgpack.packb(data)
        # msg = struct.pack('>I', len(msg)) + msg
        # self.socket.sendall(msg)

    def close(self):
        self.stream.close()

if __name__ == '__main__':
    def callback(data):
        print data
    client = Client()
    client.connection()
    client.send('sum', [1, 2])
    client.recv(callback)
    ioloop.IOLoop.current().start()
    client.close()

    while True:
        pass