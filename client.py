import socket
import time
import msgpack


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 8000))


# msg = ["request", "3", {"adlist": ["h.10"], "x": {"pub_id": "xxx", "pub_type": "xxx", "uid": "xxx", "ip": "8.8.8.8", "ua": "Mozilla/5.0 (Macintosh", " Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36": "", "category": "80203", "country": "GOOGLE", "province": "GOOGLE", "day_of_week": "2", "time_period": "2", "url_domain": "stock.qq.com", "url_path": "stock.qq.com/original/zqyjy/s591.html", "browser": "Other", "browser_version": "Other", "os": "Other", "os_version": "Other"}, "query": {"pub_id": "xxx", "pub_type": "xxx", "uid": "xxx", "ip": "8.8.8.8", "ua": "Mozilla/5.0 (Macintosh", " Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36": "", "url": "http://stock.qq.com/original/zqyjy/s591.html", "category": "80203"}, "time": 1454475352.597586}]
# msg = msgpack.packb(('method', msg))
msg = [1, 4]
msg = msgpack.packb(('sum', msg))

# method

# s.sendall(msg)
s.sendall(msg)

data = s.recv(1024)
print 'Received', repr(data)

time.sleep(10)
s.close()

# print stream