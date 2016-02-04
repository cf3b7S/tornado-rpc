# mode
CALL_MODE = 0
NOTI_MODE = 1

SYNC_MODE = 0
ASYNC_MODE = 1


# res code
SUCCESS = [200, 'Done']
UNPACK_ERROR = [300, 'msgpack unpack error']
MSGID_MISS = [301, 'msgid not found']
METHOD_MISS = [302, 'method not found']
PARAMS_MISS = [303, 'params not found']
MODE_MISS = [304, 'mode not found']

METHOD_INVALID = [305, 'method invalid']
MODE_INVALID = [306, 'mode invalid']


keyMissMap = {
    'msgid': MSGID_MISS,
    'method': METHOD_MISS,
    'params': PARAMS_MISS,
    'mode': MODE_MISS,
}
