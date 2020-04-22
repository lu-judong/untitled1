import datetime
import psutil
import multiprocessing

a = psutil.cpu_count(logical=True)

def readSizeFile(fileName):
    #file path
    filePath= "{}.txt".format(fileName)

    # with open(filePath, "w", encoding="utf8") as f:
    with open(filePath, "r") as f:
        while True:
            block = f.read(1024**2*100)
            if not block:
                break
        # while ds<1024*1024*25:
        #     f.write("a")
        #     ds=os.path.getsize(filePath)

if __name__ == '__main__':
    start_time = datetime.datetime.now()
    pool = multiprocessing.Pool(processes=a)
    result = []
    for i in range(0,a):
        r = pool.apply_async(readSizeFile,args=(i,))
        # p = Process(target=run,args=[])
        print('process {} start'.format(i))
        result.append(r)

    pool.close()
    pool.join()

    end_time = datetime.datetime.now()
    c = a * 1024**3 / 1024 / 1024 / (end_time - start_time).seconds
    print(start_time)
    print(end_time)

    print('磁盘读取速度为:{}M/s'.format(c))