import msgpack
import struct


def send(stream, data):
    msg = msgpack.packb(data)
    msg = struct.pack('>I', len(msg)) + msg
    stream.write(msg)

def recv(stream, callback):
    def read_msg(raw_msg):
        print 'read_msg'
        len_msg = struct.unpack('>I', raw_msg)[0]

        def handle_msg(msg):
            print 'handle_msg'
            data = msgpack.unpackb(msg)
            callback(data)

        stream.read_bytes(len_msg, streaming_callback=handle_msg, partial=True)    
    stream.read_bytes(4, streaming_callback=read_msg, partial=True)
    # stream.read_until_close(streaming_callback=read_msg)

    print 'sdfsd', read_msg

    # def recv_sync(stream):
    #     future = stream.read_bytes(4)

    #     def read_msg(raw_msg):
    #         len_msg = struct.unpack('>I', raw_msg)[0]
    #         read_future = stream.read_bytes(len_msg)

    #         def handle_msg(msg):
    #             data = msgpack.unpackb(msg)
    #         read_future.add_done_callback(handle_msg)
    #     future.add_done_callback(read_msg)
