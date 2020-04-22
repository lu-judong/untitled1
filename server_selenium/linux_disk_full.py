from multiprocessing import Pool
import time,os


# def mycallback(i,x):
#     while True:
#         with open('\'{}\'.txt'.format(i), 'a+') as f:
#             f.writelines(str(x))
#
#
# def sayHi(num):
#     return num
#
#
# if __name__ == '__main__':
#     e1 = time.time()
#     pool = Pool()
#
#     for i in range(10000):
#         pool.apply_async(sayHi, (i,), callback=mycallback)
#
#     pool.close()
#     pool.join()
#     e2 = time.time()
#     print(float(e2 - e1))

for i in range(2):
    os.system("sudo time dd if=/dev/zero of=/mysqldata/test.dd bs=8k count=300000")
    time.sleep(0.2)
    os.system("sudo time dd if=/mysqldata/test.dd of=/dev/null bs=8k")
    print(i)
os.system("cd /mysqldata&&rm -f test.dd")
os.system('echo end')
