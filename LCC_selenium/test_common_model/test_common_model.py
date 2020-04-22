from LCC_selenium.bin.add_model_ratio import *
from config.config import *
from config.menu_config import common_contents




add(url,username,password,common_contents,modelName,modelCode,remarks,'新建','时间',start,end,car,repairlocation,supplier,wait_time)
time.sleep(2)
# revise(url,contents,modelName, '时间', '2017-02-05', '2017-10-02', car, wait_time)
# time.sleep(2)
# delete(url,contents,modelName)