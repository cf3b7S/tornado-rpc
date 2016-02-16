import msgpack
# import struct
import config
import sys
# from tornado import gen


def send(stream, data, cb=None):
    msg = msgpack.packb(data) + '\n'
    stream.write(msg, cb)


def unpack_msg(raw_data, stream, cb=None):
    try:
        data = msgpack.unpackb(raw_data[:-1])
        if cb:
            cb(data)
        stream.close()
    except:
        print >>sys.stderr, "WARNING:", config.UNPACK_ERROR


def recv(stream, cb=None):
    stream.read_until('\n', callback=lambda data: unpack_msg(data, stream, cb))
    # stream.read_until_close(streaming_callback=lambda data: unpack_msg(data, cb))


def recv_until_close(stream, cb=None):
    stream.read_until_close(streaming_callback=lambda data: unpack_msg(data, stream, cb))


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
