import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from config.log_config import logger
from bin.main import Method
from bin.login import Login
from random import randint
from new_selenium.tech_other.tech_other_3.other3_config import *
from config.config import path_dir


#维修数据维护
class Tech:
    def log_file_out(self, msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    def tech_all_3(self,url,username,password,modelCode,modelName,remarks,line,avgOverallVariance,avgAcceptableValue,avgUnacceptableValue,avgProducerRisk,avgConsumerRisk,maxOverallLogVariance,maxMaintenanceDegree,maxAcceptableValue,maxUnacceptableValue,maxProducerRisk,maxConsumerRisk,logConfidence,logMaintenanceDegree,logMeanValue,logVarianceValue,unknownConfidence,unknownVarianceValue):
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
            driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/calculator/maintenanceData')]"))


        Method(driver).click('id','add')

        Method(driver).switch_out()
        Method(driver).switch_iframe(driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/calculator/maintenanceData/form')]"))


        try:
            Method(driver).input('id','modelCode',modelCode)
            Method(driver).input('id','modelName',modelName)
            if remarks is '':
                pass
            else:
                Method(driver).input('id','remarks',remarks)
            self.log_file_out('模型录入成功')
        except NoSuchElementException as e:
            logger.error(e)
            logger.debug('找不到id')
            self.log_file_out('模型录入失败')

        for i in range(1,line+1):
            if i == 1:
                Method(driver).click('id','add')
                Method(driver).input('xpath','//*[@id="wokTimeTbody"]/tr/td[3]/input',randint(10,99))
            else:
                Method(driver).click('id', 'add')
                Method(driver).input('xpath', '//*[@id="wokTimeTbody"]/tr[{}]/td[3]/input'.format(i),randint(10,99))
        try:

            Method(driver).input('id','avgOverallVariance',avgOverallVariance)
            Method(driver).input('id','avgAcceptableValue',avgAcceptableValue)
            Method(driver).input('id','avgUnacceptableValue',avgUnacceptableValue)
            Method(driver).input('id','avgProducerRisk',avgProducerRisk)
            Method(driver).input('id','avgConsumerRisk',avgConsumerRisk)
            self.log_file_out('平均维修时间输入成功')
        except NoSuchElementException as e:
            logger.error(e)
            logger.debug('找不到id')
            self.log_file_out('平均维修时间输入失败')

        try:
            Method(driver).input('id','maxOverallLogVariance',maxOverallLogVariance)
            Method(driver).input('id','maxMaintenanceDegree',maxMaintenanceDegree)
            Method(driver).input('id','maxAcceptableValue',maxAcceptableValue)
            Method(driver).input('id','maxUnacceptableValue',maxUnacceptableValue)
            Method(driver).input('id','maxProducerRisk',maxProducerRisk)
            Method(driver).input('id','maxConsumerRisk',maxConsumerRisk)
            self.log_file_out('最大维修时间输入成功')
        except NoSuchElementException as e:
            logger.debug('找不到id')
            logger.error(e)
            self.log_file_out('最大维修时间输入失败')

        try:
            Method(driver).input('id','logConfidence',logConfidence)
            Method(driver).input('id','logMaintenanceDegree',logMaintenanceDegree)
            Method(driver).input('id','logMeanValue',logMeanValue)
            Method(driver).input('id','logVarianceValue',logVarianceValue)
            Method(driver).input('id','unknownConfidence',unknownConfidence)
            Method(driver).input('id','unknownVarianceValue',unknownVarianceValue)
            self.log_file_out('维修性参数输入成功')
        except NoSuchElementException as e:
            logger.error(e)
            logger.debug('找不到id')
            self.log_file_out('维修性参数输入失败')

        Method(driver).switch_out()
        try:
            Method(driver).click('class','layui-layer-btn0')
            logger.debug('保存成功')
            self.log_file_out('点击保存按钮成功')
        except NoSuchElementException as e:
            logger.error(e)
            logger.debug('保存失败')
            self.log_file_out('点击保存按钮失败')
        time.sleep(3)
        Method(driver).switch_out()
        Method(driver).switch_iframe(
            driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/calculator/maintenanceData')]"))

        time.sleep(3)
        try:
            if driver.find_element_by_xpath("//a[contains(text(),\'{}\')]".format(modelName)).text == modelName:
                self.log_file_out('保存成功')
            else:
                self.log_file_out('保存失败')
        except:
            self.log_file_out('保存失败')


url = 'http://192.168.1.115:8080/darams/a?login'
username = 'test'
password = '1234'

Tech().tech_all_3(url,username,password,'X3','X3','',5,'0.3','0.2','1','3','4','5','1.2','0.4','1.2','1.3','6','4','5','12','14','16','17')