from config.config import path_dir
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from config.log_config import logger
import time
from bin.main import Method
from bin.login import Login
from test_averageRepairTime.other4_config import *

#平均维修时间
class Tech:
    def log_file_out(self, msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    def tech_all_4(self,modelCode,url,username,password,time_sleep):
        # option = webdriver.ChromeOptions()
        # option.add_argument("headless")
        # driver = webdriver.Chrome(chrome_options=option,
        #                           executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')
        driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
        Login().login(url, username, password, driver)

        time.sleep(3)
        for i in contents:
            try:
                Method(driver).contains_xpath('click',i)
                self.log_file_out('点击'+i+'成功')
            except Exception as e:
                logger.debug(e)
                self.log_file_out('点击' + i + '失败')


        time.sleep(1)
        Method(driver).click('class','ivu-icon-md-add')

        time.sleep(1)
        try:
            driver.find_element_by_xpath("//span[text()=\'{}\']/../../../td".format(modelCode)).click()
            time.sleep(1)
            driver.find_elements_by_class_name('ivu-btn-info')[-1].click()
            self.log_file_out('工作时间导入成功')
        except Exception as e:
            self.log_file_out('工作时间导入失败')



        time.sleep(time_sleep)
        driver.find_elements_by_class_name('ivu-btn-info')[2].click()
        time.sleep(1)
        try:
            driver.find_element_by_xpath("//span[text()=\'{}\']/../../../td".format(modelCode)).click()
            time.sleep(1)
            driver.find_elements_by_class_name('ivu-btn-info')[-1].click()
            self.log_file_out('平均时间导入成功')
        except NoSuchElementException as e:
            self.log_file_out('平均时间导入失败')


        time.sleep(time_sleep)
        try:
            driver.find_element_by_xpath('//span[text()="验证"]').click()
            logger.debug('验证成功')
            self.log_file_out('验证成功')
        except NoSuchElementException as e:
            logger.error(e)
            logger.debug('验证失败')
            self.log_file_out('验证失败')


url = 'http://192.168.221.21:8082/index.html'
username = 'test'
password = '1234'
time_sleep = 1

Tech().tech_all_4('m1',url,username,password,time_sleep)
