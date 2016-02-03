from tornado import tcpserver


class TCPServer(tcpserver.TCPServer):
    def __init__(self, callback):
        super(TCPServer, self).__init__()
        self.callback = callback

    def handle_stream(self, stream, address):
        self.callback(stream, address)


class Client():
    pass
