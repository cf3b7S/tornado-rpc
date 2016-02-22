# -*- coding: utf-8 -*-
import sys
import msgpack

from tornado import gen
import config

separator = '\r\n\r\r\n\n'


@gen.coroutine
def send(stream, data):
    msg = msgpack.packb(data) + separator
    yield stream.write(msg)


def unpack_msg(raw_data, stream):
    try:
        data = msgpack.unpackb(raw_data[:-6])
    except:
        send(stream, {'error': config.UNPACK_ERROR})
        print >>sys.stderr, "WARNING:", config.UNPACK_ERROR
    return data


@gen.coroutine
def recv(stream):
    data = yield stream.read_until(separator)
    raise gen.Return(unpack_msg(data, stream))
