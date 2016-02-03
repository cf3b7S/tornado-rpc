# import tornado
from tornado.ioloop import IOLoop
from tcp import TCPServer
import msgpack
import time


class Handler(object):
    def sum(self, a, b):
        time.sleep(2)
        print 'sum', a, b, a + b
        return a + b


class Server():
    def __init__(self, handler):
        self.handler = handler
        self.tcpServer = TCPServer(self.handle_stream)

    def bind(self, port=8000):
        self.port = port
        self.tcpServer.bind(self.port)

    def start(self, process=2):
        self.process = process
        self.tcpServer.start(process)
        self.loop = IOLoop.current()
        self.loop.start()

    def handle_stream(self, stream, address):
        stream.read_until_close(streaming_callback=lambda data: self.handle_line(data, stream))

    def handle_line(self, data, stream):
        try:
            method, params = msgpack.unpackb(data)
            if not hasattr(self.handler, method):
                stream.write('method not found')
            else:
                res = getattr(self.handler, method)(*params)
                stream.write(str(res))
        except:
            stream.write('msgpack unpack error')


if __name__ == '__main__':
    server = Server(Handler())
    server.bind()
    server.start()





# class TCP(TCPServer):
#     def __init__(self):

#     def handle_stream(self, stream, address):
#         print stream, address
#         stream.read_until('\n', log)
#         stream.write('Done')
#         stream.read_until('\n', log)
#         stream.write('Done')

# def connection_ready(sock, fd, events):
#     while True:
#         try:
#             connection, address = sock.accept()
#         except socket.error as e:
#             if e.args[0] not in (errno.EWOULDBLOCK, errno.EAGAIN):
#                 raise
#             return
#         connection.setblocking(0)
#         handle_connection(connection, address)

# server = Server()
# server.bind(8888)
# server.start(2)  # Forks multiple sub-processes

# io_loop = IOLoop.current()
# callback = functools.partial(connection_ready, sock)
# io_loop.add_handler(sock.fileno(), callback, io_loop.READ)
# io_loop.start()

# # IOLoop.current().start()
