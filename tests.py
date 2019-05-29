import requests
import time
import os

os.environ['NO_PROXY'] = '0.0.0.0'
URL = "http://0.0.0.0:5000/crud"
requests.get("http://0.0.0.0:5000/end")
requests.get("http://0.0.0.0:5000")
f = open("./test.txt", "w+")
# testing post
for _ in range(100):
    start = time.time()
    for i in range(1000):
        PARAMS = {'date': '2019-04-24', 'time': '12:00:00', 'location': str(_) + '_' + str(i)}
        requests.post(URL, params=PARAMS)
    f.write('POST no ' + str(_) + ': ' + str(time.time() - start) + '\n')
# testing get
for _ in range(100):
    start = time.time()
    for i in range(1000):
        PARAMS = {'date': '2019-04-24', 'time': '12:00:00', 'location': str(_) + '_' + str(i)}
        requests.get(URL, params=PARAMS)
    f.write('GET no ' + str(_) + ': ' + str(time.time() - start) + '\n')
# TESTING PUTS
for _ in range(100):
    start = time.time()
    for i in range(1000):
        PARAMS = {'date': '2019-04-24', 'time': '12:00:00', 'location': str(_) + '_' + str(i), 'nmhc': '22.56'}
        requests.put(URL, params=PARAMS)
    f.write('PUT no ' + str(_) + ': ' + str(time.time() - start) + '\n')
# TESTING DELETES
for _ in range(100):
    start = time.time()
    for i in range(1000):
        PARAMS = {'date': '2019-04-24', 'time': '12:00:00', 'location': str(_) + '_' + str(i)}
        requests.delete(URL, params=PARAMS)
    f.write('DELETE no ' + str(_) + ': ' + str(time.time() - start) + '\n')
requests.get("http://0.0.0.0:5000/end")
f.close()
