# -*- coding: utf-8 -*-
import sys
import msgpack

import config


def send(stream, data, cb=None):
    msg = msgpack.packb(data) + '\n'
    stream.write(msg, cb)


def unpack_msg(raw_data, stream, cb=None):
    try:
        data = msgpack.unpackb(raw_data[:-1])
        if cb:
            cb(data)
        # stream.close()
    except:
        send(stream, {'error': config.UNPACK_ERROR})
        print >>sys.stderr, "WARNING:", config.UNPACK_ERROR


def recv(stream, cb=None):
    stream.read_until('\n', callback=lambda data: unpack_msg(data, stream, cb))

# def recv_until_close(stream, cb=None):
#     stream.read_until_close(streaming_callback=lambda data: unpack_msg(data, stream, cb))
