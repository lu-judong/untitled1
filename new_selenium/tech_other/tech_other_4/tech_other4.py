from config.config import path_dir
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from config.log_config import logger
import time
from bin.main import Method
from bin.login import Login
from new_selenium.tech_other.tech_other_4.other4_config import *

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

        for i in contents:
            try:
                Method(driver).contains_xpath('click',i)
                self.log_file_out('点击'+i+'成功')
            except Exception as e:
                logger.debug(e)
                self.log_file_out('点击' + i + '失败')

        Method(driver).switch_out()
        Method(driver).switch_iframe(
            driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/calculator/averageRepairTime')]"))
        time.sleep(time_sleep)

        Method(driver).click('id','importWorkTime')

        try:
            Method(driver).switch_out()

            Method(driver).switch_iframe(driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/tag/gridselect?url=%2Fdarams%2Fa%2Fcalculator%2FmaintenanceData%2FpopData%3FdataType%3DmaintenanceData&fieldLabels=%E6%A8%A1%E5%9E%8B%E7%BC%96%E7%A0%81%7C%E6%A8%A1%E5%9E%8B%E5%90%8D%E7%A7%B0&fieldKeys=modelCode%7CmodelName&searchLabels=%E6%A8%A1%E5%9E%8B%E7%BC%96%E7%A0%81%7C%E6%A8%A1%E5%9E%8B%E5%90%8D%E7%A7%B0&searchKeys=modelCode%7CmodelName&isMultiSelected=false')]"))
            time.sleep(time_sleep)
        except NoSuchElementException as e:
            self.log_file_out('找不到第一个导入按键进入的iframe')

        try:
            driver.find_element_by_xpath("//td[contains(text(),\'{}\')]/../td[1]/input".format(modelCode)).click()

            Method(driver).switch_out()
            Method(driver).click('class','layui-layer-btn0')
            self.log_file_out('工作时间导入成功')
        except Exception as e:
            self.log_file_out('工作时间导入失败')

        Method(driver).switch_out()
        Method(driver).switch_iframe(
            driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/calculator/averageRepairTime')]"))

        time.sleep(time_sleep)
        Method(driver).click('id', 'importaAvgRepairTime')
        try:
            Method(driver).switch_out()
            Method(driver).switch_iframe(driver.find_element_by_xpath(
                "//iframe[contains(@src,'/darams/a/tag/gridselect?url=%2Fdarams%2Fa%2Fcalculator%2FmaintenanceData%2FpopData%3FdataType%3DaverageRepairTime&fieldLabels=%E6%A8%A1%E5%9E%8B%E7%BC%96%E7%A0%81%7C%E6%A8%A1%E5%9E%8B%E5%90%8D%E7%A7%B0&fieldKeys=modelCode%7CmodelName&searchLabels=%E6%A8%A1%E5%9E%8B%E7%BC%96%E7%A0%81%7C%E6%A8%A1%E5%9E%8B%E5%90%8D%E7%A7%B0&searchKeys=modelCode%7CmodelName&isMultiSelected=false')]"))
            time.sleep(time_sleep)
        except Exception as e:
            self.log_file_out('找不到第二个导入按键进入的iframe')
        try:
            driver.find_element_by_xpath("//td[contains(text(),\'{}\')]/../td[1]/input".format(modelCode)).click()
            Method(driver).switch_out()
            Method(driver).click('class', 'layui-layer-btn0')
            self.log_file_out('平均时间导入成功')
        except NoSuchElementException as e:
            self.log_file_out('平均时间导入失败')

        Method(driver).switch_out()
        Method(driver).switch_iframe(
            driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/calculator/averageRepairTime')]"))
        time.sleep(time_sleep)
        try:
            Method(driver).contains_xpath('click','验证')
            logger.debug('验证成功')
            self.log_file_out('验证成功')
        except NoSuchElementException as e:
            logger.error(e)
            logger.debug('验证失败')
            self.log_file_out('验证失败')


url = 'http://192.168.1.115:8080/darams/a?login'
username = 'test'
password = '1234'
time_sleep = 1

Tech().tech_all_4('X1',url,username,password,time_sleep)
