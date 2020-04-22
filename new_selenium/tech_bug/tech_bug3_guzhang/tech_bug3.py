from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import requests
from config.log_config import logger
import time
from bin.main import Method
from bin.login import Login
from new_selenium.tech_bug.tech_bug3_guzhang.bug_config import *

class Tech:
    def log_file_out(self,msg):
        fo = open('C:\\Users\\a\\PycharmProjects\\untitled\\new_selenium\\usecase.txt', mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    def tech_analysis(self,url,modelCode):
        # option = webdriver.ChromeOptions()
        # option.add_argument("headless")
        # driver = webdriver.Chrome(chrome_options=option,                                                                executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')
        driver = webdriver.Chrome()
        Login().login(url, 'admin', 'admin', driver)

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
            Method(driver).switch_iframe(
                driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/fault/opFaultOrder')]"))

            time.sleep(2)
        except NoSuchElementException as e:
            self.log_file_out('点击不保存计算按钮失败,获取不到相应的xpath')

        try:
            a = driver.find_element_by_xpath("/html/body/div/div/div[2]/div[2]/div[2]/div[4]/div[1]/span[1]").text
            print('bug不存在')
        except NoSuchElementException as e:
            print('bug存在')
        except:
            print('bug')



url = 'http://193.112.209.138:9092/darams/a/login;JSESSIONID=a183b49c056e4ef5991c66ad7ea7fc50000'


Tech().tech_analysis(url,'001')
