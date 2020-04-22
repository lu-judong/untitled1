'''
create at 2019/4/26
'''
import json
import requests
import time

if __name__ == '__main__':
    a = time.time()
    list_= []
    data = {
        "b":{"n":2},
        "c":{"n":3},
        "d":{"n":4},
        "e":{"n":5},
            }
    b = requests.post("http://127.0.0.1:5000/a",json.dumps(data))
    print(b)
    print(time.time()-a)