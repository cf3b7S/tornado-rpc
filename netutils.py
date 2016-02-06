import msgpack
import struct
import config
import sys
# from tornado import gen


def send(stream, data, callback=None):
    msg = msgpack.packb(data)
    msg = struct.pack('>I', len(msg)) + msg
    if callback:
        stream.write(msg, callback)
    else:
        stream.write(msg)


def recv(stream, callback=None):
    def read_msg(raw_msg):
        len_msg = struct.unpack('>I', raw_msg)[0]

        def handle_msg(msg):
            try:
                data = msgpack.unpackb(msg)
            except:
                print >>sys.stderr, "WARNING:", config.UNPACK_ERROR, msg
            callback(data)

        stream.read_bytes(len_msg, streaming_callback=handle_msg)
    stream.read_bytes(4, streaming_callback=read_msg)

# @gen.coroutine
# def recv(stream, callback=None):
#     raw_msg = yield stream.read_bytes(4)
#     len_msg = struct.unpack('>I', raw_msg)[0]
#     msg = yield stream.read_bytes(len_msg)
#     try:
#         data = msgpack.unpackb(msg)
#     except:
#         print >>sys.stderr, "WARNING:", config.UNPACK_ERROR, msg
#     if callback:
#         callback(data)
#     else:
#         raise gen.Return(data)



