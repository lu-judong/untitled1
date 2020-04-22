from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import requests

from bin.select_fault_union2 import deal_fault_union_2
from config.log_config import logger
import time
from bin.main import Method
from bin.login import Login
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from new_selenium.test_techm.tech_config import *
from bin.select_fault_occur import deal_fault
from bin.select_car import deal_car
from bin.select_fault_union import deal_fault_union
from bin.select_butongfuji import deal_different
from bin.select_fault_butongfuji_occur import deal_different_occur
from config.config import path_dir


#技术整改优化效果分析
class Tech:
    def log_file_out(self,msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    def tech_analysis(self,url,username,password,modelName,value,remarks,select,start,end,end1,average,car,fault,select_fault,fault1,time_sleep,wait_time):
        # option = webdriver.ChromeOptions()
        # option.add_argument("headless")
        # driver = webdriver.Chrome(chrome_options=option,                                                                executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')

        driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
        Login().login(url, username, password, driver)

        self.log_file_out('-----技术整改-----')

        for i in contents:
            try:
                Method(driver).contains_xpath('click',i)
                self.log_file_out('点击'+i+'成功')
            except Exception as e:
                logger.debug(e)
                self.log_file_out('点击' + i + '失败')

        time.sleep(time_sleep)
        try:
            Method(driver).switch_out()
            Method(driver).switch_iframe(
                driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/technicalOptimization')]"))
            Method(driver).click('xpath','//*[@id="add"]')
            time.sleep(time_sleep)
        except NoSuchElementException as e:
            self.log_file_out('点击新建按钮失败,获取不到相应的xpath')

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
            self.log_file_out('模型新建成功')
        except Exception as e:
            logger.debug(e)
            self.log_file_out('模型新建失败')

        # 新增里程
        if select == '里程':
            try:
                Method(driver).click('xpath','//*[@id="left-tab-1"]/a')
                Method(driver).input('xpath','//*[@id="confMileageList1_startMileage"]',start)
                Method(driver).input('xpath','//*[@id="confMileageList1_endMileage"]',end)
                Method(driver).select_down_list('xpath','//*[@id="confMileageList1_averageSpeedSelect"]',average)
                Method(driver).click('xpath', '//*[@id="left-tab-1"]/a')
                Method(driver).input('xpath', '//*[@id="confMileageList2_startMileage"]', end)
                Method(driver).input('xpath', '//*[@id="confMileageList2_endMileage"]', end1)
                Method(driver).select_down_list('xpath', '//*[@id="confMileageList2_averageSpeedSelect"]', average)
                self.log_file_out('新增里程成功')
            except NoSuchElementException as e:
                logger.error('xpath' + '不存在！')
                self.log_file_out('新增里程失败')
        else:
            try:
                Method(driver).click('xpath', '//*[@id="inputForm"]/div[1]/ul/li[2]/a')
                time.sleep(1)
                Method(driver).click('xpath', '//*[@id="left-tab-2"]/a')
                Method(driver).input('name', 'confDateList[1].startDate', start)
                Method(driver).input('name', 'confDateList[1].endDate', end)
                Method(driver).select_down_list('name', 'confDateList[1].averageSpeedSelect',average)
                time.sleep(1)
                Method(driver).click('xpath', '//*[@id="left-tab-2"]/a')
                Method(driver).input('name', 'confDateList[2].startDate', end)
                Method(driver).input('name', 'confDateList[2].endDate', end1)
                Method(driver).select_down_list('name', 'confDateList[2].averageSpeedSelect', average)
                v3 = '新增时间成功'
            except NoSuchElementException as e:
                logger.error('xpath' + '不存在！')
                v3 = '新增时间失败'

        time.sleep(1)


        # 晚点时长
        # try:
        #     Method(driver).click('xpath','//*[@id="inputForm"]/div[1]/ul/li[4]/a')
        #     time.sleep(1)
        #     Method(driver).input('id','confLateHoursList0_lateHoursFrom','0')
        #     Method(driver).input('id','confLateHoursList0_lateHoursTo','3')
        #     self.log_file_out('晚点时长添加成功')
        # except NoSuchElementException as e:
        #     logger.debug('xpath找不到')
        #     self.log_file_out('晚点时长添加失败')
        Method(driver).click('xpath', '//*[@id="right-tab-1"]/a')
        time.sleep(1)

        # 从新进入新打开的iframe 先去最外层 在进入打开的iframe
        Method(driver).switch_out()
        b = Method(driver).get_attr('css',"[class='layui-layer layui-layer-iframe my-skin']", 'times')
        Method(driver).switch_iframe('layui-layer-iframe' + b)
        time.sleep(5)

        # 车型 车号新增页面
        if select_fault == '交集':
            js_s = "return $('#partType').prop('checked')"
            status = driver.execute_script(js_s)
            if status is True:
                Method(driver).click('id', 'partType')
            else:
                time.sleep(1)
        elif select_fault == '并集':
            js_s = "return $('#partType').prop('checked')"
            status = driver.execute_script(js_s)
            if status is True:
                time.sleep(1)
            else:
                Method(driver).click('id', 'partType')

        a = deal_car(driver, car)
        if a is True:
            self.log_file_out('选车成功')
        else:
            self.log_file_out('选车失败')

        # 故障模式选择页面
        Method(driver).switch_out()
        c = Method(driver).get_attr('css',"[class='layui-layer layui-layer-iframe my-skin']", 'times')
        Method(driver).switch_iframe('layui-layer-iframe' + c)
        time.sleep(8)
        if select_fault == '交集':
            fault_status = deal_fault(driver, fault)
            if fault_status is True:
                self.log_file_out('故障模式选择成功')
            else:
                self.log_file_out('故障模式选择失败')

        elif select_fault == '并集':
            if value == 1:
                fault_status = deal_fault_union(driver, fault)
                if fault_status is True:
                    self.log_file_out('故障模式选择成功')
                else:
                    self.log_file_out('故障模式选择失败')
            elif value == 2:
                fault_status = deal_fault_union_2(driver, fault)
                if fault_status is True:
                    self.log_file_out('故障模式选择成功')
                else:
                    self.log_file_out('故障模式选择失败')
                #
                # Method(driver).click('id', 'differPatternSelect')
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
            self.log_file_out('保存失败')
        except:
            self.log_file_out('请录入正确的模型条件')
            return

        Method(driver).switch_out()
        Method(driver).switch_iframe(
            driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/technicalOptimization')]"))
        time.sleep(time_sleep)

        driver.find_element_by_xpath(
            "//a[contains(text(),\'{}\')]/../../td[7]/a[3]".format(modelName)).click()


        try:
            a = WebDriverWait(driver, wait_time).until(
                EC.text_to_be_present_in_element(
                    (By.XPATH, "//a[contains(text(),\'{}\')]/../../td[4]".format(modelName)),
                    u'计算完成'))
            if a is True:
                logger.debug('评估成功')
                self.log_file_out('评估成功')

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
                        driver.close()
                    elif status == 404:
                        logger.error('{}请求404'.format(next_url))
                        self.log_file_out('图表页面获取失败')
                        driver.close()
                except Exception as e:
                    logger.error(e)
        except Exception as e:
            logger.debug('评估失败')
            self.log_file_out('评估失败')

url = 'http://192.168.1.115:8080/darams/a/login'

car = {
    'E27': ['2641','2642','2643','2644','2645','2646','2647']
}

# fault_pattern = {
#     '高压供电系统': 'all'
# }



fault_pattern = {'E27':
{'高压供电系统': {'受电弓': 'all'}}}

fault_object = {
    '高压供电系统':{'高压电缆、连接器及跳线':['电缆']},
    '辅助供电系统':['刮雨器电源'],
    '门窗系统':'all'
}
fault1 = {'辅助供电系统':'all'}

time_sleep = 1
wait_time = 10
#
Tech().tech_analysis(url,'admin','admin','技术整改数据测试2',2,'','时间','2017-02-01','2017-12-01','2018-03-01',1,car,fault_pattern,'并集',fault1,time_sleep,wait_time)