'''
create at 2019/4/26
'''

import json
import time
from flask import Flask, request
from m_ import *
from thread_utils import pool
from m1_ import *

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/a',methods=['GET', 'POST'])
def a():
    body = eval(request.get_data())
    rs = [pool.submit(eval(x),body.get(x)) for x in body.keys()]
    return json.dumps([x.result() for x in rs])

@app.route('/b')
def b(arg):
    time.sleep(2)
    return bb(arg)

@app.route('/c')
def c(arg):
    time.sleep(2)
    return cc(arg)
@app.route('/d')
def d(arg):
    time.sleep(2)
    return dd(arg)
@app.route('/e')
def e(arg):
    time.sleep(2)
    return ee(arg)

def print_():
    print("start")
    time.sleep(5)
    print("end")
    return "1"

if __name__ == '__main__':
    app.run(threaded = True)
