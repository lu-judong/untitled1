from config.config import path_dir
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from config.log_config import logger
import time
from bin.main import Method
from bin.login import Login
from new_selenium.tech_other.tech_other_1.other1_config import *
from config.config import path_dir

#可靠性验证计划
class Tech:
    def log_file_out(self, msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    def tech_all_1(self,url,username,password,test,select,mtbfOne,testPlanDateOne,time_sleep):
        # option = webdriver.ChromeOptions()
        # option.add_argument("headless")
        # driver = webdriver.Chrome(chrome_options=option,
        #                           executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')
        driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
        Login().login(url, username, password, driver)

        self.log_file_out('-----可靠性验证计划-----')
        for i in contents:
            try:
                Method(driver).contains_xpath('click',i)
                self.log_file_out('点击'+i+'成功')
            except Exception as e:
                logger.debug(e)
                self.log_file_out('点击' + i + '失败')

        time.sleep(time_sleep)
        Method(driver).switch_out()
        Method(driver).switch_iframe(
            driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/calculator/ramsTestPlan')]"))


        try:
            if test == 'GJB-899A':
                Method(driver).input('id','mtbfOne',mtbfOne)
                Method(driver).select_down_list('id', 'selectOne', select)
                Method(driver).input('id','testPlanDateOne',testPlanDateOne)
                driver.find_element_by_xpath("//button[contains(text(),'计算')]").click()
                logger.debug('计算成功')
                self.log_file_out('计算成功')
            elif test == 'IEC-61124':
                Method(driver).contains_xpath('click','IEC-61124')
                time.sleep(time_sleep)
                Method(driver).input('id','mtbfTwo',mtbfOne)
                Method(driver).select_down_list('id', 'selectTwo', select)
                Method(driver).input('id','testPlanDateTwo',testPlanDateOne)
                Method(driver).click('xpath','//*[@id="IEC"]/div[1]/table/tbody/tr/td[6]/button[1]')
                logger.debug('计算成功')
                self.log_file_out('计算成功')
        except NoSuchElementException as e:
            logger.debug('计算失败')
            self.log_file_out('计算失败')


url = 'http://192.168.1.115:8080/darams/a/login'
username = 'test'
password = '1234'
time_sleep = 1
Tech().tech_all_1(url,username,password,'IEC-61124',1,'3','4',time_sleep)
