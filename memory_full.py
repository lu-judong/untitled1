import time
import psutil
from multiprocessing import Process



last_memory = float(int(psutil.virtual_memory()[3]) / 1024 / 1024 / 1000)

def run():
    print("100")
    while True:
        string = ''
        a = 0
        while True:
            string += "a{}=0;".format(a)
            exec(string*10000*1000)
            a += 1


def run1():
    count = 0
    while count < 50:
        b = float(int(psutil.virtual_memory()[3]) / 1024 / 1024 / 1000)
        print(last_memory,b)
        if 0 < b - last_memory < 0.1:
            count += 1
        else:
            count = 0
    print(psutil.virtual_memory()[3])
    # sys.exit()

if __name__ == '__main__':
    p2 = Process(target=run1, args=())
    p1 = Process(target=run,args=())
    p1.daemon = True
    p1.start()
    time.sleep(10)
    p2.start()
    p2.join()
    print("finish")