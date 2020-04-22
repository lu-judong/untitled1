from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from config.log_config import logger
import time
from bin.main import Method
from bin.login import Login
from test_maintenanceParameter.other6_config import *
from config.config import path_dir

#维修性参数估计
class Tech:
    def log_file_out(self, msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    def tech_all_6(self,modelCode,url,username,password,time_sleep):
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
        driver.find_elements_by_xpath('//span[text()="导入"]')[1].click()

        time.sleep(1)
        try:
            driver.find_element_by_xpath("//span[text()=\'{}\']/../../../td".format(modelCode)).click()
            time.sleep(1)
            driver.find_elements_by_xpath('//span[text()="确定"]')[0].click()
            self.log_file_out('工作时间导入成功')
        except Exception as e:
            self.log_file_out('工作时间导入失败')

        time.sleep(time_sleep)
        driver.find_elements_by_xpath('//span[text()="导入"]')[2].click()
        time.sleep(1)
        try:
            driver.find_element_by_xpath("//span[text()=\'{}\']/../../../td".format(modelCode)).click()
            time.sleep(1)
            driver.find_elements_by_xpath('//span[text()="确定"]')[1].click()
            self.log_file_out('第二个导入成功')
        except NoSuchElementException as e:
            self.log_file_out('第二个导入失败')


        try:
            driver.find_elements_by_xpath('//span[text()="计算"]')[0].click()
            logger.debug('第一次计算成功')
            self.log_file_out('第一次计算成功')
        except NoSuchElementException as e:
            logger.error(e)
            logger.debug('第一次计算失败')
            self.log_file_out('第一次计算失败')

        driver.find_elements_by_xpath('//span[text()="导入"]')[3].click()
        time.sleep(1)

        try:
            driver.find_element_by_xpath("//span[text()=\'{}\']/../../../td".format(modelCode)).click()
            time.sleep(1)
            driver.find_elements_by_xpath('//span[text()="确定"]')[2].click()
            self.log_file_out('第三个导入成功')
        except NoSuchElementException as e:
            self.log_file_out('第三个导入失败')

        try:
            driver.find_elements_by_xpath('//span[text()="计算"]')[1].click()
            logger.debug('第二次计算成功')
            self.log_file_out('第二次计算成功')
        except NoSuchElementException as e:
            logger.error(e)
            logger.debug('第二次计算失败')
            self.log_file_out('第二次计算失败')

url = 'http://192.168.221.21:8082/index.html'
username = 'test'
password = '1234'


time_sleep = 1

Tech().tech_all_6('m1',url,username,password,time_sleep)