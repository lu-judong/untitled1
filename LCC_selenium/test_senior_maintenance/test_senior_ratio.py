from LCC_selenium.bin.add_model_ratio import *


contents = ['全寿命周期费用分析','高级修维度']
car = {'E27':'all',
       'E28':['2216']}
wait_time = 10
#
# car = {'17型车':['170770','173617']
#
#         }
repairlocation = {'E27':[{'构型62':{'构型70':['构型30']}},['构型53']]}
supplier = {'内装系统':['南京勃朗峰']}

url = 'http://192.168.221.21'
modelName = 'mmmm2'
modelCode = '12'
remarks = ''
start = '0'
end = '100'

add(url,contents,modelName,modelCode,remarks,'新建','里程',start,end,car,repairlocation,supplier,wait_time)
time.sleep(2)
# revise(url,contents,modelName, '时间', '2017-02-05', '2017-10-02', car, wait_time)
# time.sleep(2)
# delete(url,contents,modelName)