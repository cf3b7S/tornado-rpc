import msgpack
import struct


class NetUtils(object):

    def send(stream, data):
        msg = msgpack.packb(data)
        msg = struct.pack('>I', len(msg)) + msg
        stream.write(msg)

    def recv(stream, callback=None):
        def read_msg(raw_msg):
            len_msg = struct.unpack('>I', raw_msg)[0]

            def handle_msg(msg):
                data = msgpack.unpackb(msg)
                callback(data)

            stream.read_bytes(len_msg, callback=handle_msg)
        stream.read_bytes(4, callback=read_msg)


    def recv_async(stream, callback):
        future = stream.read_bytes(4)

        def read_msg(raw_msg):
            len_msg = struct.unpack('>I', raw_msg)[0]
            read_future = stream.read_bytes(len_msg)

            def handle_msg(msg):
                data = msgpack.unpackb(msg)
                if callback:
                    callback(data)
                else:
                    pass
                    # raise gen.return(data)
            read_future.add_done_callback(handle_msg)
        future.add_done_callback(read_msg)
        return future
