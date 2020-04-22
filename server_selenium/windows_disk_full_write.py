import datetime
import psutil
import multiprocessing

a = psutil.cpu_count(logical=True)


def genSizeFile(fileName):
    #file path
    filePath= "{}.txt".format(fileName)

    # 生成固定大小的文件
    # date size
    ds=0

    # with open(filePath, "w", encoding="utf8") as f:
    with open(filePath, "wb") as f:
        # if(fileName == 0):
        #     pass
        f.write(bytes(1024**3*1))
        # while ds<1024*1024*25:
        #     f.write("a")
        #     ds=os.path.getsize(filePath)

if __name__ == '__main__':
    start_time = datetime.datetime.now()
    pool = multiprocessing.Pool(processes=a)
    result = []
    for i in range(0,a):
        r = pool.apply_async(genSizeFile,args=(i,))
        # p = Process(target=run,args=[])
        print('process {} start'.format(i))
        result.append(r)


    # for res in result:
    #     print(res.get())

    pool.close()
    pool.join()

    end_time = datetime.datetime.now()
    c = a * 1024**3 / 1024 / 1024 / (end_time - start_time).seconds
    print(start_time)
    print(end_time)

    print('磁盘写入速度为:{}M/s'.format(c))


