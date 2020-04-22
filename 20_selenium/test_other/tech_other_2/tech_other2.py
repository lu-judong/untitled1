from config.config import path_dir,url,username,password,ramsincreasePlan_config
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from config.log_config import logger
from bin.main import Method
from bin.login import Login
import time


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

        for i in ramsincreasePlan_config:
            try:
                Method(driver).contains_xpath('click',i)
                time.sleep(1)
                self.log_file_out('点击'+i+'成功')
            except Exception as e:
                logger.debug(e)
                self.log_file_out('点击' + i + '失败')

        Method(driver).switch_out()
        Method(driver).switch_iframe(
            driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/calculator/ramsIncreasePlan')]"))

        try:
            Method(driver).clear('id','mtbfStart')
            Method(driver).input('id', 'mtbfStart', mtbfStart)

            Method(driver).clear('id', 'mtbfEnd')
            Method(driver).input('id', 'mtbfEnd', mtbfEnd)

            Method(driver).clear('id', 'firstTestTime')
            Method(driver).input('id', 'firstTestTime', firstTestTime)

            Method(driver).clear('id', 'growthRate')
            Method(driver).input('id','growthRate',growthRate)
            self.log_file_out('数据填写成功')
        except NoSuchElementException as e:
            logger.error(e)
            logger.debug('找不到id')
            self.log_file_out('数据填写失败')
        try:
            driver.find_element_by_xpath("//button[contains(text(),'计算')]").click()
            logger.debug('计算成功')
            self.log_file_out('计算成功')
        except NoSuchElementException as e:
            logger.error(e)
            logger.debug('计算失败')
            self.log_file_out('计算失败')



Tech().tech_all_2(url,username,password,'200','50','100','0.4')