import psutil
import multiprocessing

a = psutil.cpu_count(logical=True)


def run():
    while True:
        pass


if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=a)
    result = []
    for i in range(0,a):
        r = pool.apply_async(run,args=())
        # p = Process(target=run,args=[])
        print('process {} start'.format(i))
        result.append(r)
    print("cpu最大占用:",psutil.cpu_percent(1))
        # p.start()

    # for res in result:
    #     print(res.get())

    pool.close()
    # pool.join()

