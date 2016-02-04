import socket
import struct
import config
import time
import netutils
import msgpack
from tornado import iostream

class Client(object):

    def __init__(self, sock=None, io_loop=None, max_buffer_size=None, read_chunk_size=None, max_write_buffer_size=None):
        if not sock:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.stream = iostream.IOStream(sock, io_loop, max_buffer_size, read_chunk_size, max_write_buffer_size)
        self.mode = config.SYNC_MODE

    def connection(self, host='127.0.0.1', port=8000, callback=None, server_hostname=None):
        self.stream.connect((host, port), callback=None, server_hostname=None)

    def setSync(self):
        self.mode = config.SYNC_MODE

    def setAsync(self):
        self.mode = config.ASYNC_MODE

    def recv(self):
        netutils.recv(self.stream)
        # raw_msg = self._recv_all(4)
        # len_msg = struct.unpack('>I', raw_msg)[0]
        # msg = self._recv_all(len_msg)
        # data = msgpack.unpackb(msg)
        # return data

    def _recv_all(self, length):
        msg = ''
        while len(msg) < length:
            print length - len(msg)
            packet = self.socket.recv(length - len(msg))
            print packet
            # if not packet:
            #     return None
            msg += packet
        return msg

    def send(self, method, data):
        msg = msgpack.packb((method, data, self.mode))
        # msg = struct.pack('>I', len(msg)) + msg
        self.socket.sendall(msg)

    def close(self):
        self.socket.close()

if __name__ == '__main__':
    client = Client()
    client.connection()
    client.send('sum', [1, 2])
    print client.recv()
    client.close()
