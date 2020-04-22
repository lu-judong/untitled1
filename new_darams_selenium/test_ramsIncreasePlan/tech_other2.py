from config.config import path_dir
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from config.log_config import logger
from bin.main import Method
from bin.login import Login
from test_ramsIncreasePlan.other2_config import *
import time
from selenium.webdriver import ActionChains

#可靠性增长计划
class Tech:
    def log_file_out(self, msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    def tech_all_2(self,url,username,password,mtbfStart,mtbfEnd,firstTestTime,growthRate):
        # option = webdriver.ChromeOptions()
        # option.add_argument("headless")
        # driver = webdriver.Chrome(chrome_options=option,
        #                           executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')
        driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
        Login().login(url, username, password, driver)
        time.sleep(2)

        for i in contents:
            try:
                Method(driver).contains_xpath('click',i)
                time.sleep(1)
                self.log_file_out('点击'+i+'成功')
            except Exception as e:
                logger.debug(e)
                self.log_file_out('点击' + i + '失败')

        time.sleep(1)

        try:
            element = driver.find_element_by_class_name('ivu-input-number-input')
            ActionChains(driver).double_click(element).perform()
            time.sleep(1)
            driver.find_elements_by_class_name('ivu-input-number-input')[0].send_keys(mtbfStart)

            element1 = driver.find_elements_by_class_name('ivu-input-number-input')[1]
            ActionChains(driver).double_click(element1).perform()
            time.sleep(1)
            driver.find_elements_by_class_name('ivu-input-number-input')[1].send_keys(mtbfEnd)

            element2 = driver.find_elements_by_class_name('ivu-input-number-input')[3]
            ActionChains(driver).double_click(element2).perform()
            time.sleep(1)
            driver.find_elements_by_class_name('ivu-input-number-input')[3].send_keys(firstTestTime)

            element3 = driver.find_elements_by_class_name('ivu-input-number-input')[4]
            ActionChains(driver).double_click(element3).perform()
            time.sleep(1)
            driver.find_elements_by_class_name('ivu-input-number-input')[4].send_keys(growthRate)
            self.log_file_out('数据填写成功')
        except NoSuchElementException as e:
            logger.error(e)
            logger.debug('找不到id')
            self.log_file_out('数据填写失败')
        time.sleep(1)
        try:
            driver.find_element_by_xpath("//span[text()='计算']").click()
            logger.debug('计算成功')
            self.log_file_out('计算成功')
        except NoSuchElementException as e:
            logger.error(e)
            logger.debug('计算失败')
            self.log_file_out('计算失败')

url = 'http://192.168.221.21:8082/index.html'
username = 'test'
password = '1234'

Tech().tech_all_2(url,username,password,'200','50','100','0.4')