# mode
CALL_MODE = 0
NOTI_MODE = 1  # notify mode will not wait for result

# SYNC_MODE = 0
# ASYNC_MODE = 1


# res code
SUCCESS = 'Done'
UNPACK_ERROR = {
    'code': 300,
    'msg': 'msgpack unpack error'
}
ID_MISS = {
    'code': 301,
    'msg': 'id not found'
}
METHOD_MISS = {
    'code': 302,
    'msg': 'method not found'
}
PARAMS_MISS = {
    'code': 303,
    'msg': 'params not found'
}
MODE_MISS = {
    'code': 304,
    'msg': 'mode not found'
}
METHOD_INVALID = {
    'code': 305,
    'msg': 'method invalid'
}
MODE_INVALID = {
    'code': 306,
    'msg': 'mode invalid'
}

keyMissMap = {
    'id': ID_MISS,
    'method': METHOD_MISS,
    'params': PARAMS_MISS,
    'mode': MODE_MISS,
}
