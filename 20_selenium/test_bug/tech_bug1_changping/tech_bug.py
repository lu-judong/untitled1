from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import requests
from config.log_config import logger
import time
from bin.main import Method
from bin.login import Login
from new_selenium.tech_bug.tech_bug1_changping.bug_config import *
from config.config import path_dir

class Tech:
    def log_file_out(self, msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
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
                driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/confModel')]"))
            time.sleep(2)
        except NoSuchElementException as e:
            self.log_file_out('点击不保存计算按钮失败,获取不到相应的xpath')

        try:
            driver.find_element_by_xpath("//a[contains(text(),\'{}\')]/../../td[9]/a[3]".format(modelCode)).click()
        except NoSuchElementException as e:
            print('点击图表失败')

        time.sleep(2)

        Method(driver).switch_out()
        c = Method(driver).get_attr('css', "[class='layui-layer layui-layer-iframe']", 'times')
        try:
            next_url = Method(driver).get_attr('id', 'layui-layer-iframe' + c, 'src')
            status = requests.get(next_url).status_code
            if status == 200:
                logger.debug('bug不存在')
                self.log_file_out('图表页面获取成功')
            elif status == 404:
                logger.error('bug存在')
                self.log_file_out('图表页面获取失败')
        except Exception as e:
            logger.error(e)

url = 'http://193.112.209.138:9092/darams/a/login;JSESSIONID=a183b49c056e4ef5991c66ad7ea7fc50000'


Tech().tech_analysis(url,'001')
