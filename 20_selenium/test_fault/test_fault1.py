from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,WebDriverException
import requests
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bin.login import Login
from bin.select_fault_occur import deal_fault
from bin.select_car import deal_car
from bin.select_fault_union import deal_fault_union
from bin.select_fault_union2 import deal_fault_union_2
from bin.select_butongfuji import deal_different
from bin.select_fault_butongfuji_occur import deal_different_occur
from config.config import path_dir,url,username,password,fault_config
from bin.select_new_car import *
from bin.select_new_union import *
from bin.select_new_occur import *


#故障占比分析
class Tech:
    def log_file_out(self, msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    def tech_fault_analysis(self,url,username,password,modelName,value,remarks,start,end,average,car,fault,select_fault,time_sleep,wait_time):

        # option = webdriver.ChromeOptions()
        # option.add_argument("headless")
        # driver = webdriver.Chrome(chrome_options=option,
        #                           executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))

        driver = webdriver.Chrome()
        driver.maximize_window()
        Login().login(url, username, password,driver)

        driver.maximize_window()
        time.sleep(2)
        self.log_file_out('-----故障占比分析-----')
        for i in fault_config:
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
                driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/analysisProportion')]"))
            Method(driver).click('xpath','//*[@id="add"]')
            time.sleep(time_sleep)
        except NoSuchElementException as e:
            self.log_file_out('点击新建按钮失败 找不到对应的xpath')

        Method(driver).switch_out()
        a = Method(driver).get_attr('css',"[class='layui-layer layui-layer-iframe']",'times')
        Method(driver).switch_iframe('layui-layer-iframe' + a)

        try:
            Method(driver).input('id', 'modelName', modelName)
            Method(driver).select_down_list('id','modelObject',value)
            if remarks == '':
                pass
            else:
                Method(driver).input('xpath','//*[@id="remarks"]',remarks)
            self.log_file_out('模型构建成功')
        except Exception as e:
            logger.debug(e)
            self.log_file_out('模型构建失败')

        # 新增里程
        try:
            Method(driver).click('xpath','//*[@id="left-tab-1"]/a')
            Method(driver).input('xpath','//*[@id="confMileageList0_startMileage"]',start)
            Method(driver).input('xpath','//*[@id="confMileageList0_endMileage"]',end)
            Method(driver).select_down_list('xpath','//*[@id="confMileageList0_averageSpeedSelect"]',average)
            self.log_file_out('新增里程成功')
        except NoSuchElementException as e:
            logger.error('xpath' + '不存在！')
            self.log_file_out('新增里程失败')

        time.sleep(1)

        time.sleep(2)
        Method(driver).click('xpath','//*[@id="right-tab-1"]/a')
        # 从新进入新打开的iframe 先去最外层 在进入打开的iframe
        try:
            Method(driver).switch_out()
            b = Method(driver).get_attr('css',"[class='layui-layer layui-layer-iframe my-skin']", 'times')
            Method(driver).switch_iframe('layui-layer-iframe' + b)
        except:
            print('请录入评估对象')
            return
        time.sleep(3)
        # 车型 车号新增页面
        if select_fault == '交集':
            Method(driver).click('id', 'partType')
        elif select_fault == '并集':
            time.sleep(1)

        driver.find_element_by_xpath('//a[text()="车型"]').click()
        time.sleep(1)

        # car_status = deal_car(driver,car)
        if car == '1':
            car_status = deal_new_car(driver)
        elif car == '2':
            car_status = deal_new_car1(driver)
        elif car == '3':
            car_status = deal_new_car2(driver)
        elif car == '4':
            car_status = deal_new_car3(driver)
        elif car == '5':
            car_status  = deal_new_car4(driver)
        elif car == '6':
            car_status = deal_new_car5(driver)
        else:
            car_status = deal_car(driver,car)

        if car_status[0] is True:
            self.log_file_out('选车成功')
        else:
            self.log_file_out('选车失败')


        # 故障模式选择页面
        Method(driver).switch_out()
        c = Method(driver).get_attr('css',"[class='layui-layer layui-layer-iframe my-skin']", 'times')
        Method(driver).switch_iframe('layui-layer-iframe' + c)
        time.sleep(30)


        if select_fault == '交集':
            if fault == '1':
                fault_status = deal_new_fault(driver)
            elif fault == '2':
                fault_status = deal_new_fault1(driver)
            elif fault == '3':
                fault_status = deal_new_fault2(driver)
            elif fault == '4':
                fault_status = deal_new_fault3(driver)
            elif fault == '5':
                fault_status = deal_new_fault4(driver)
            elif fault == '6':
                fault_status = deal_new_fault5(driver)
            else:
                fault_status = deal_fault(driver, fault)
            if fault_status is True:
                self.log_file_out('故障模式选择成功')
            else:
                self.log_file_out('故障模式选择失败')

        elif select_fault == '并集':
            # if value == 1:
            #     fault_status = deal_fault_union(driver, fault)
            #     if fault_status is True:
            #         self.log_file_out('故障模式选择成功')
            #     else:
            #         self.log_file_out('故障模式选择失败')
            # elif value == 2:
            #     fault_status = deal_fault_union_2(driver, fault)
            #     if fault_status is True:
            #         self.log_file_out('故障模式选择成功')
            #     else:
            #         self.log_file_out('故障模式选择失败')
            if fault == '1':
                fault_status = deal_new_union(driver)
            elif fault  == '2':
                fault_status = deal_new_union1(driver)
            elif fault == '3':
                fault_status = deal_new_union2(driver)
            elif fault == '4':
                fault_status = deal_new_union3(driver)
            elif fault == '5':
                fault_status = deal_new_union4(driver)
            elif fault == '6':
                fault_status = deal_new_union5(driver)
            elif fault == '7':
                fault_status = deal_new_union6(driver)
            else:
                fault_status = deal_fault_union(driver,fault)
            if fault_status[0] is True:
                self.log_file_out('故障模式选择成功')
            else:
                self.log_file_out('故障模式选择失败')
        # elif value == 2:
        #     if select_fault == '交集':
        #         fault_status = deal_different_occur(driver, fault)
        #         if fault_status is True:
        #             self.log_file_out('故障模式选择成功')
        #         else:
        #             self.log_file_out('故障模式选择失败')
        #
        #         Method(driver).click('id', 'differPatternSelect')
            #
            # time.sleep(8)
            #
            # Method(driver).switch_out()
            # d = Method(driver).get_attr('css', "[class='layui-layer layui-layer-iframe my-skin']", 'times')
            # Method(driver).switch_iframe('layui-layer-iframe' + d)
            #
            # fault_status1 = deal_different(driver, fault1)
            # if fault_status1 is True:
            #     self.log_file_out('不同父级选择成功')
            # else:
            #     self.log_file_out('不同父级选择失败')

        try:
            Method(driver).switch_out()
            # d = "layui_layer" + c
            # e = "layui_layer" + str((int(c)-1))
            # Method(driver).click('xpath','//*[@id=\'%s\']/div[3]/a[3]' % d)
            Method(driver).click('class','layui-layer-btn2')
            #点击保存按钮
            time.sleep(time_sleep)
            # Method(driver).click('xpath','//*[@id=\'%s\']/div[3]/a[1]' % e)
            Method(driver).click('class','layui-layer-btn0')
        except NoSuchElementException as e:
            logger.error('xpath'+'不存在!')
            self.log_file_out('点击保存按钮失败')


        Method(driver).switch_out()
        Method(driver).switch_iframe(
            driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/analysisProportion')]"))
        time.sleep(1)

        try:
            driver.find_element_by_xpath("//a[contains(text(),\'{}\')]/../../td[7]/a[3]".format(modelName)).click()
        except WebDriverException:
            print('请录入正确的模型')
            return
        except NoSuchElementException as e:
            logger.error(e)
            print('点击图表按钮失败')


        try:
            a = WebDriverWait(driver, wait_time).until(EC.text_to_be_present_in_element((By.XPATH, "//a[contains(text(),\'{}\')]/../../td[4]".format(modelName)), u'计算完成'))
            if a is True:
                logger.debug('评估成功')
                driver.find_element_by_xpath("//a[contains(text(),\'{}\')]/../../td[7]/a[4]".format(modelName)).click()

                # 查看点击图表出来的页面是否存在
                Method(driver).switch_out()
                c = Method(driver).get_attr('css', "[class='layui-layer layui-layer-iframe']", 'times')
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
        except Exception as e:
            logger.debug('评估失败')
            self.log_file_out('评估失败')

car = {'E27':['2641', '2642', '2643', '2644', '2645', '2646', '2647']}

# fault_pattern = {'高压供电系统': {'高压电缆、连接器及跳线':'all'}}

fault_pattern = {'高压供电系统': 'all'}

fault_object1 = {'辅助供电系统':{'头灯':'all'}}

fault1 = {'内装系统':{'厨房设施':{"微波炉柜":{'微波炉':'all'}}}}

fault_object = {'E27':
{'高压供电系统': {'高压电缆、连接器及跳线':{'电缆终端':'all'}}}
                }

# fault_object = {'E27':
# {'高压供电系统': {'高压电缆、连接器及跳线':'all'}}}

time_sleep = 3
wait_time = 10

Tech().tech_fault_analysis(url,username,password,'1.16测试',0,'','0','100',2,'1','1','交集',time_sleep,wait_time)
