from selenium import webdriver
from config.log_config import logger
import time
from bin.main import Method
from bin.login import Login
from new_selenium.tech_trainList.trainList_config import *
from config.config import path_dir

#列车信息
class test_technology:
    def log_file_out(self,msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    def tech(self,url,username,password,car,train):

        driver = webdriver.Chrome()
        Login().login(url,username, password, driver)

        self.log_file_out('-----列车信息-----')

        for i in contents:
            try:
                Method(driver).contains_xpath('click',i)
                self.log_file_out('点击'+i+'成功')
            except Exception as e:
                logger.debug(e)
                self.log_file_out('点击' + i + '失败')

        time.sleep(2)
        try:
            Method(driver).switch_out()
            Method(driver).switch_iframe(driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/train/trainlist')]"))
            self.log_file_out('切入列车信息成功')
        except:
            self.log_file_out('切入列车信息失败')

        try:
            Method(driver).input('id','carriage',car)
            Method(driver).input('id','traintype',train)
            Method(driver).click('xpath','//*[@id="collapseTwo"]/div/div[3]/div/button')
            driver.find_element_by_xpath("//span[contains(text(),\'{}\')]".format('E01')).click()
            Method(driver).click('xpath', '//*[@id="collapseTwo"]/div/div[3]/div/button')
            # 配属局
            Method(driver).click('xpath', '//*[@id="collapseTwo"]/div/div[6]/div/button')
            driver.find_element_by_xpath("//span[contains(text(),\'{}\')]".format('上海南')).click()
            Method(driver).click('xpath', '//*[@id="collapseTwo"]/div/div[6]/div/button')
            # 配属所
            Method(driver).click('xpath', '//*[@id="collapseTwo"]/div/div[7]/div/button')
            driver.find_element_by_xpath("//span[contains(text(),\'{}\')]".format('上海铁路局')).click()
            Method(driver).click('xpath', '//*[@id="collapseTwo"]/div/div[7]/div/button')
            # 使用所
            Method(driver).click('xpath', '//*[@id="collapseTwo"]/div/div[8]/div/button')
            time.sleep(2)
            driver.find_element_by_xpath('//*[@id="collapseTwo"]/div/div[8]/div/div/ul/li[1]/a/span[1]').click()
            time.sleep(2)
            Method(driver).click('xpath', '//*[@id="collapseTwo"]/div/div[8]/div/button')

            Method(driver).click('id','search')
        except:
            self.log_file_out('信息录入失败')

        time.sleep(2)
        if driver.find_element_by_xpath('//*[@id="page_right"]/div').text[-3:-1] != 0:
            self.log_file_out('列车信息测试成功')
        else:
            self.log_file_out('列车信息测试失败')

url = 'http://192.168.1.115:8080/darams/a?login'

test_technology().tech(url,'test','1234','2001','2A')