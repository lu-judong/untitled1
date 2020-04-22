import os
import shutil
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bin.select_thing import *
from bin.main import *
from bin.login import new_built
import datetime
import re

path_dir = os.path.dirname(os.path.dirname(__file__)).replace('\\', '/')

path_dir1 = os.path.dirname(os.path.dirname(__file__)).replace('/', '\\')

# 外网地址
# url = 'http://192.144.173.11:8880/login.html#/'
#
# username = 'admin'
#
# password = '123456'
# # 内网地址
url = 'http://192.168.221.21'

username = 'admin'

password = '1234'
# 模型名称
modelName = '3.6测试'
# 选择评估对象 1代表选择评估对象 2代表选择故障模式
target_of_evaluation = 1
# 备注
remarks = ''
# 时间/里程
select = '里程'

# 里程
mileage_start = '0'
mileage_end = '100'

# 时间
time_start = '2017-02-03'
time_end = '2018-02-03'


# 时速选择 1代表180 2代表260
speed = 1

# 需要验证的车型车号
# 外网
check_car = ['17型车','170770','174970']



# 内网的车
# car = {'E27':['2641', '2642', '2643', '2644', '2645', '2646', '2647']}
# 外网的车
car = {'17型车':'all'}

# fault_pattern = {'高压供电系统': {'高压电缆、连接器及跳线':'all'}}
# 外网的部件
fault_pattern = {'部件000250':{'部件001225':'all'}}

# 交集还是并集
select_fault = '交集'

# 部件搜索框输入的值
check_fault = '部件000059'

# fault_object = {'E27':
# {'高压供电系统': {'高压电缆、连接器及跳线':{'电缆终端':'all'}}}
#                 }

min_model = [['m1', '2017-02-03', '2018-10-02',2, {'17型车':['170770', '173617', '174947']},{'17型车':{'部件000250':'all'}},1], ['m2', '2017-02-03', '2018-10-02', 2,{'18型车':'all'},{'18型车':{'部件000250':'all'}},1]]

fault_object = {'E27':
                    {'高压供电系统':{'高压电缆、连接器及跳线':{'电缆终端':"all",'跳线':"all",'电缆':'all'}}}
                }

wait_time = 20

# 内控模型的时间
incontrol_start = '2017-01-02'

incontrol_end = '2020-01-02'

# 修程修制的里程参数
# 优化前里程/优化后里程
repair_mileage = [0,100,200]

# 技术变更时间/里程
tech_select = '里程'

# 技术变更的时间/里程参数
tech_change = [0,100,200]

# 维修数据维护数据
main_data_modelName = 'X2'

main_data_modelCode = 'X2'

line = 6
main_data_l = ['0.3','0.2','1','3','4','5','1.2','0.4','1.2','1.3','6','4','5','12','14','16','17']