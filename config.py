# mode
SYNC_MODE = 0
ASYNC_MODE = 1


# res code
SUCCESS = [0, 'Done']
MODE_INVALID = [1, 'mode invalid']
METHOD_MISS = [1, 'method not found']
UNPACK_ERROR = [1, 'msgpack unpack error']





# call('sum', [1,2], success_cb=fun1, error_cb=fun2)