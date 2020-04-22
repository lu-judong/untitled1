from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from config.log_config import logger
import time
from bin.main import Method
from bin.login import Login
from test_bug.tech_home_number.test_homemodel_Final_1_way import HomeModelCal


class Tech:
    def log_file_out(self,msg):
        fo = open('C:\\Users\\a\\PycharmProjects\\untitled\\new_selenium\\usecase.txt', mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    def tech_analysis(self,url,time_sleep):
        option = webdriver.ChromeOptions()
        option.add_argument("headless")
        driver = webdriver.Chrome(chrome_options=option,executable_path=r'../../apps/chromedriver.exe')
        # driver = webdriver.Chrome()
        Login().login(url, 'admin', 'admin', driver)
        list_b1 = HomeModelCal().main()

        try:
            Method(driver).switch_out()
            Method(driver).switch_iframe(
                driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/home')]"))
            time.sleep(time_sleep)
        except NoSuchElementException as e:
            self.log_file_out('切入iframe失败')

        if list_b1[0] == int(driver.find_element_by_xpath('//div[@class="table-row-group"]//ul//li[1]//span').text):
            print('首页列车总数一致')
        else:
            print('首页列车总数不一致')

        if list_b1[1] == int(driver.find_element_by_xpath('//div[@class="table-row-group"]//ul//li[2]//span').text):
            print('首页统计部件总数一致')
        else:
            print('首页统计部件总数不一致')

        if list_b1[2] == float(driver.find_element_by_xpath('//div[@class="table-row-group"]//ul//li[3]//span').text):
            print('首页列车行驶累计里程数一致')
        else:
            print('首页列车行驶累计里程数不一致')

        if driver.find_element_by_xpath('//div[@class="table-row-group"]//ul//li[4]//span').text == '':
            if list_b1[3] == 0:
                print('首页基本故障数一致')
            else:
                print('首页基本故障数不一致')
        else:
            if list_b1[3] == int(driver.find_element_by_xpath('//div[@class="table-row-group"]//ul//li[4]//span').text):
                print('首页基本故障数一致')
            else:
                print('首页基本故障数不一致')

        if driver.find_element_by_xpath('//div[@class="table-row-group"]//ul//li[5]//span').text == '':
            if list_b1[4] == 0:
                print('首页关联故障数一致')
            else:
                print('首页关联故障数不一致')
        else:
            if list_b1[4] == int(driver.find_element_by_xpath('//div[@class="table-row-group"]//ul//li[5]//span').text):
                print('首页关联故障数一致')
            else:
                print('首页关联故障数不一致')

        if driver.find_element_by_xpath('//div[@class="table-row-group"]//ul//li[6]//span').text == '':
            if list_b1[5] == 0:
                print('首页服务故障数一致')
            else:
                print('首页服务故障数不一致')
        else:
            if list_b1[5] == int(driver.find_element_by_xpath('//div[@class="table-row-group"]//ul//li[6]//span').text):
                print('首页服务故障数一致')
            else:
                print('首页服务故障数不一致')

        if driver.find_element_by_xpath('//div[@class="table-row-group"]//ul//li[7]//span').text == '':
            if list_b1[6] == 0:
                print('首页安监故障数一致')
            else:
                print('首页安监故障数不一致')
        else:
            if list_b1[6] == int(driver.find_element_by_xpath('//div[@class="table-row-group"]//ul//li[7]//span').text):
                print('首页安监故障数一致')
            else:
                print('首页安监故障数不一致')



url = 'http://192.168.1.115:9092/darams/a?login'

Tech().tech_analysis(url,2)