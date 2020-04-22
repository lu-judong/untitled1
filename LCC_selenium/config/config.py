import os
from bin.login import Login
from LCC_selenium.bin.main import Method,log_file_out
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from config.log_config import logger
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import re
from bin.main import *

path_dir= os.path.dirname(os.path.dirname(__file__)).replace('/', '\\')\

# 外网配置
url = 'http://192.144.173.11:8880/login.html#/'
username = 'admin'
password = '123456'

# 内网配置
# url = 'http://192.168.221.21/'
# username = 'admin'
# password = '1234'

modelName = '2.27测试'
modelCode = '11'
remarks = ''
# 日期开始时间,结束时间
time_start = '2017-02-03'
time_end = '2017-08-02'
# 里程开始里程,结束里程
mileage_start = '0'
mileage_end  = '100'
# 内网的车型
# car = {'E27':'all',
#        'E28':['2216']}
wait_time = 10
# 外网的车型
car = {'17型车':'all'}
# 外网敏度分析的车型
sen_car = {'17型车':'170770'}
# 外网敏度分析的构型
sen_repairlocation = {'构型000010':{'构型000188':{'构型000200':['构型000055']}}}

# repairlocation = {'E27':[{'构型62':{'构型70':['构型30']}},['构型53']]}
# supplier = {'内装系统':['南京勃朗峰']}
repairlocation = ''
supplier = ''

# 外网的对比模型的子模型
min_model = [['m1','2017-03-02','2017-05-04',{'17型车':'all'},'',''],['m2','2017-05-02','2017-08-04',{'17型车':'all'},'','']]

# 外网对比功能验证导入自定义车组的子模型
customize_min_model = [['m1','2017-03-02','2017-05-04'],['m2','2017-05-02','2017-08-04']]




