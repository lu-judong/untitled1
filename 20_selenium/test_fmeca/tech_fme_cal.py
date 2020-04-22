from config.config import path_dir,url,username,password,femca_config
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import requests
from config.log_config import logger
import time
from bin.main import Method
from bin.login import Login
from test_fmeca.fmeca_config import *
from bin.select_fault_occur import deal_fault
from bin.select_car import deal_car
from bin.select_fault_union import deal_fault_union


#技术整改优化效果分析
class Tech:
    def log_file_out(self,msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    def tech_analysis(self,url,username,password,select,start,end,car,fault,select_fault,time_sleep,wait_time):
        # option = webdriver.ChromeOptions()
        # option.add_argument("headless")
        # driver = webdriver.Chrome(chrome_options=option,                                                                executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')
        driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
        Login().login(url, username, password, driver)

        self.log_file_out('-----femca立即计算-----')

        for i in femca_config:
            try:
                Method(driver).contains_xpath('click',i)
                time.sleep(1)
                self.log_file_out('点击'+i+'成功')
            except Exception as e:
                logger.debug(e)
                self.log_file_out('点击' + i + '失败')

        time.sleep(time_sleep)
        try:
            Method(driver).switch_out()
            Method(driver).switch_iframe(
                driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/dataModelReport')]"))
            Method(driver).click('id', 'calculate')
            time.sleep(time_sleep)
        except NoSuchElementException as e:
            self.log_file_out('点击不保存计算按钮失败,获取不到相应的xpath')

        Method(driver).switch_out()

        Method(driver).switch_iframe(
            driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/dataModelReport/form2?modelType=FMECA_MODEL')]"))

        if select == '里程':
            try:
                Method(driver).click('xpath','//*[@id="left-tab-1"]/a')
                Method(driver).input('id','confMileageList0_startMileage',start)
                Method(driver).input('id','confMileageList0_endMileage',end)
            except NoSuchElementException as e:
                print('添加里程失败')
        elif select == '时间':
            try:
                Method(driver).click('xpath','//*[@id="inputForm"]/div[2]/ul/li[2]/a')
                Method(driver).click('xpath','//*[@id="left-tab-2"]/a')
                Method(driver).input('id','confDateList[0].startDate',start)
                Method(driver).input('id','confDateList[0].endDate',end)
            except NoSuchElementException as e:
                print('添加时间失败')
        try:
            Method(driver).click('id','addModel')
        except NoSuchElementException as e:
            print('点击新建按钮失败')
        except:
            print('请设置里程或时间')

        try:
            Method(driver).switch_out()
            b = Method(driver).get_attr('css', "[class='layui-layer layui-layer-iframe my-skin']", 'times')
            Method(driver).switch_iframe('layui-layer-iframe' + b)
        except:
            print('请录入评估对象')
            return

        time.sleep(10)

        # 车型 车号新增页面
        # 车型 车号新增页面
        if select_fault == '交集':
            Method(driver).click('id', 'partType')
        elif select_fault == '并集':
            time.sleep(1)

        driver.find_element_by_xpath('//a[text()="车型"]').click()
        time.sleep(1)

        car_status = deal_car(driver, car)
        if car_status is True:
            self.log_file_out('选车成功')
        else:
            self.log_file_out('选车失败')

        # 故障模式选择页面
        Method(driver).switch_out()
        c = Method(driver).get_attr('css', "[class='layui-layer layui-layer-iframe my-skin']", 'times')
        Method(driver).switch_iframe('layui-layer-iframe' + c)
        time.sleep(30)
        if select_fault == '交集':
            fault_status = deal_fault(driver, fault)
            if fault_status is True:
                self.log_file_out('故障模式选择成功')
            else:
                self.log_file_out('故障模式选择失败')

        elif select_fault == '并集':
            fault_status = deal_fault_union(driver, fault)
            if fault_status is True:
                self.log_file_out('故障模式选择成功')
            else:
                self.log_file_out('故障模式选择失败')

        try:
            Method(driver).switch_out()
            Method(driver).click('class', 'layui-layer-btn2')
            time.sleep(time_sleep)
            Method(driver).click('class', 'layui-layer-btn0')
            self.log_file_out('点击计算按钮成功')
        except NoSuchElementException as e:
            logger.error('xpath' + '不存在!')
            self.log_file_out('点击确定按钮失败')
        except:
            print('请录入完整的模型')
            return

        time.sleep(wait_time)

        Method(driver).switch_out()
        try:
            c = Method(driver).get_attr('css', "[class='layui-layer layui-layer-iframe']", 'times')
        except NoSuchElementException as e:
            print('请录入正确的模型')
            return

        try:
            next_url = Method(driver).get_attr('id', 'layui-layer-iframe' + c, 'src')
            status = requests.get(next_url).status_code
            if status == 200:
                logger.debug('图表页面获取成功')
                self.log_file_out('图表页面获取成功')
            elif status == 404:
                logger.error('{}请求404'.format(next_url))
                self.log_file_out('图表页面获取失败')
        except Exception as e:
            logger.error(e)

car = {
    'E27': ['2641', '2642','2643','2644','2645','2646','2647']
}

fault_pattern = {'高压供电系统': {'高压电缆、连接器及跳线':'all'}}

fault_object = {'E27':
{'高压供电系统': {'高压电缆、连接器及跳线':{'电缆终端':'all'}}}
                }

# fault_object = {'E27':
#                     {'高压供电系统':{'高压电缆、连接器及跳线':{'电缆终端':"all",'跳线':"all",'电缆':'all'}}}
#                 }
time_sleep = 2
wait_time = 10


Tech().tech_analysis(url,username,password,'里程','0','100',car,fault_pattern,'交集',time_sleep,wait_time)