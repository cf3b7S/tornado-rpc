import msgpack
import struct
import config
import sys


def send(stream, data):
    msg = msgpack.packb(data)
    msg = struct.pack('>I', len(msg)) + msg
    stream.write(msg)


def recv(stream, callback):
    def read_msg(raw_msg):
        len_msg = struct.unpack('>I', raw_msg)[0]

        def handle_msg(msg):
            try:
                data = msgpack.unpackb(msg)
            except:
                print >>sys.stderr, "WARNING:", config.UNPACK_ERROR, msg
            callback(data)

        stream.read_bytes(len_msg, streaming_callback=handle_msg, partial=True)
    stream.read_bytes(4, streaming_callback=read_msg, partial=True)
