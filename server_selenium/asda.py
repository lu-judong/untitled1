import os
import random

def genSizeFile(fileName):
    #file path
    filePath= "{}.txt".format(fileName)

    # 生成固定大小的文件
    # date size
    ds=0
    with open(filePath, "w", encoding="utf8") as f:
        while ds<1024*1024*50:
            f.write(str(round(random.uniform(-1000, 1000),2)))
            f.write("\n")
            ds=os.path.getsize(filePath)
genSizeFile(50)