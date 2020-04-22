from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import requests
from bin.main import Method
from bin.login import Login

from test_EDS.select_system import *
from config.config import path_dir
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class singelmodel:
    def log_file_out(self,msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    # 单一模型
    def tech(self,url,username,password,modelName,value,select,start,end,average,supplier,car,fault,select_fault,time_sleep,wait_time):

        driver = webdriver.Chrome()
        Login().login(url,username, password, driver)

        driver.maximize_window()
        self.log_file_out('-----供应商功能-----')

        Method(driver).contains_xpath('click', '供应商')
        time.sleep(2)
        try:
            Method(driver).switch_out()
            Method(driver).switch_iframe(
                driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/eds/supplier')]"))
            time.sleep(2)
            self.log_file_out('供应商打开成功')
        except NoSuchElementException as e:
            logger.error(e)
            self.log_file_out('供应商打开失败')

        driver.find_element_by_xpath('//span[text()="新建"]').click()
        time.sleep(2)

        #对新增指标页面进行操作
        try:
            driver.find_elements_by_xpath("//input[@placeholder='请输入模型名称']")[1].send_keys(modelName)
            driver.find_elements_by_class_name('ivu-select-placeholder')[2].click()
            if value == 1:
                driver.find_element_by_xpath('//li[text()="评估系统、部件"]').click()
            else:
                driver.find_element_by_xpath('//li[text()="故障模式"]').click()
            self.log_file_out('模型录入成功')
        except Exception as e:
            logger.debug(e)
            self.log_file_out('模型录入失败')

        # 优化前里程
        if select == '里程':
            try:
                Method(driver).input('xpath','//*[@id="startMileage"]/input',start)
                Method(driver).input('xpath', '//*[@id="endMileage"]/input', end)
                Method(driver).click('id','averageSpeedSelect1')
                time.sleep(1)
                Method(driver).click('xpath','//li[text()="{}"]'.format(average))
                self.log_file_out('里程录入成功')
            except NoSuchElementException as e:
                self.log_file_out('里程录入失败')
        elif select == '时间':
            try:
                Method(driver).click('xpath','//a[text()="起始日期"]')
                time.sleep(1)
                Method(driver).input('xpath', '//*[@id="startDate"]/input', start)
                Method(driver).input('xpath', '//*[@id="endDate"]/input', end)
                Method(driver).click('id', 'averageSpeedSelect2')
                time.sleep(1)
                Method(driver).click('xpath', '//li[text()="{}"]'.format(average))
                self.log_file_out('添加时间成功')
            except NoSuchElementException as e:
                self.log_file_out('添加时间失败')

        time.sleep(2)

        driver.find_element_by_xpath('//span[text()="新增"]').click()
        time.sleep(2)

        driver.find_element_by_xpath('//span[text()="筛选供应商"]').click()
        time.sleep(2)
        try:
            driver.find_element_by_xpath('//*[text()=\'{}\']/../label'.format(supplier)).click()
            time.sleep(1)
            driver.find_element_by_xpath('//*[text()=\'{}\']'.format('选择')).click()
            self.log_file_out('供应商选择成功')
        except NoSuchElementException as e:
            logger.error(e)
            self.log_file_out('供应商选择失败')

        driver.find_element_by_xpath('//span[text()="确定"]').click()
        time.sleep(1)
        # 车型 车号新增页面
        if select_fault == '交集':
            driver.find_element_by_xpath('//*[text()=\'{}\']/./span'.format(' 是否根据车型选择')).click()
        elif select_fault == '并集':
            pass

        a = deal_car(driver, car, 0)
        if a is True:
            self.log_file_out('选车成功')
        else:
            self.log_file_out('选车失败')

        # 故障模式选择页面
        driver.find_element_by_xpath('//span[contains(text(),"下一步")]').click()
        time.sleep(5)

        if select_fault == '交集':
            fault_status = deal_occur(driver, fault, '部件')
            if fault_status is True:
                self.log_file_out('故障模式选择成功')
            else:
                self.log_file_out('故障模式选择失败')

        elif select_fault == '并集':
            fault_status = deal_union(driver, fault)
            if fault_status is True:
                self.log_file_out('故障模式选择成功')
            else:
                self.log_file_out('故障模式选择失败')

        try:
            driver.find_element_by_xpath('//span[text()="确定"]').click()
            logger.debug('bug不存在')
        except NoSuchElementException as e:
            logger.error('xpath' + '不存在!')
            logger.debug('bug存在')
        except:
            self.log_file_out('请录入正确的模型')

        driver.find_element_by_xpath('//span[text()="保存"]').click()
        try:
            driver.find_elements_by_xpath("//span[contains(text(),\'{}\')]/../../../../../td[1]/div/div/button[2]/span".format(modelName)).click()
            time.sleep(1)
            driver.find_element_by_xpath("//span[text()='是']").click()
        except WebDriverException as e:
            try:
                driver.find_element_by_xpath("//div[@class='ivu-form-item-error-tip']").is_displayed()
            except:
                print('编码重复')
            else:
                if driver.find_element_by_xpath("//div[@class='ivu-form-item-error-tip']").text == '请输入模型名称':
                    print('日期填写错误')
                elif driver.find_element_by_xpath("//div[@class='ivu-form-item-error-tip']").text == '请输入评估对象':
                    print('里程填写错误')

        try:
            a1 = WebDriverWait(driver, wait_time).until(
                EC.text_to_be_present_in_element(
                    (By.XPATH, "//span[contains(text(),\'{}\')]/../../../../../td[5]".format(modelName)), u'计算异常'))
            if a1 == True:
                self.log_file_out('计算异常,无法评估')
                driver.close()
        except Exception as e:
            text1 = driver.find_element_by_xpath(
                "//span[contains(text(),\'{}\')]/../../../td[5]".format(modelName)).text
            if text1 == '计算完成':
                logger.debug('评估成功')
                self.log_file_out('评估成功')


url = 'http://192.168.1.115:8080/darams/a?login'

car = {'E27':['2642']}

# fault_pattern = {'高压供电系统': {'高压电缆、连接器及跳线':'all'}}

# fault_pattern = {'高压供电系统': 'all'}

fault1 = {'内装系统':{'厨房设施':{"微波炉柜":{'微波炉':'all'}}}}

fault = {'E27.350公里统型':{'转向架':{'一系悬挂':'all'},'内装系统':'all','门窗系统':{'侧拉门':{'门体':'all'}}}}

# fault_object = {'E27':
#                     {'高压供电系统':{'高压电缆、连接器及跳线':{'电缆终端':"all",'跳线':"all",'电缆':'all'}}}
#                 }

time_sleep = 2
wait_time = 10


singelmodel().tech(url,'admin','admin','111',1,'里程','0','100','180','整列',car,fault,'并集',time_sleep,wait_time)