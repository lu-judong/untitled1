import random

from selenium import webdriver
from bin.login import Login
from test_EDS.EDS_config import *
from config.config import path_dir
from test_EDS.select_system import *
from selenium.webdriver import ActionChains
import re

class Check_EDS:
    def log_file_out(self, msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    def calculate(self,driver,home_handles,a,b):
        L = []
        try:
            for i in range(a, b):
                driver.find_element_by_xpath('//a[text()="t1"]/../../../td[17]/div/p/span[{}]/a'.format(i)).click()
                time.sleep(5)
                all_handle = driver.window_handles
                for i in all_handle:
                    if i != home_handles:
                        driver.switch_to.window(i)
                time.sleep(2)
                a = driver.find_element_by_class_name('pagination-info').text
                L.append(re.findall(r"\d+\.?\d*", a)[-1])
                for i in all_handle:
                    if i != home_handles:
                        driver.close()
                time.sleep(2)
                driver.switch_to.window(home_handles)
                Method(driver).switch_out()
                Method(driver).switch_iframe(
                    driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/eds/main')]"))
                time.sleep(2)
            return L
        except Exception as e:
            logger.error(e)
            self.log_file_out('统计故障单数量失败')
            return L


    def check(self,url,username,password):
        driver = webdriver.Chrome()
        driver.maximize_window()
        Login().login(url, username, password, driver)

        driver.maximize_window()
        time.sleep(2)
        self.log_file_out('-----技术变更及EDS反馈系统-----')
        for i in contents:
            try:
                Method(driver).contains_xpath('click', i)
                time.sleep(1)
                self.log_file_out('点击' + i + '成功')
            except Exception as e:
                logger.debug(e)
                self.log_file_out('点击' + i + '失败')

        time.sleep(2)
        try:
            Method(driver).switch_out()
            Method(driver).switch_iframe(
                driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/eds/main')]"))
            time.sleep(2)
        except NoSuchElementException as e:
            self.log_file_out('源头问题功能打开失败')
        # L = driver.find_elements_by_xpath('//a[text()=\'{}\']/../../../td'.format('t1'))[16].text.split('、')
        #
        # driver.find_elements_by_xpath('//td[@class="el-table_1_column_2 is-left "]')[2].text

        home_handles = driver.current_window_handle
        driver.find_element_by_xpath('//a[text()=\'{}\']'.format('2')).click()
        time.sleep(1)

        xpath = driver.find_element_by_xpath('//a[text()=\'{}\']/../../../td[17]/div/p/span[1]/a'.format('t1'))
        xpath1 = driver.find_element_by_xpath('//a[text()=\'{}\']/../../../td[17]/div/p/span[9]/a'.format('t1'))
        ActionChains(driver).drag_and_drop(xpath, xpath1).perform()

        num1 = self.calculate(driver,home_handles,1,8)

        xpath2 = driver.find_element_by_xpath('//a[text()=\'{}\']/../../../td[17]/div/p/span[11]/a'.format('t1'))
        ActionChains(driver).drag_and_drop(xpath2, xpath2).perform()
        num2 = self.calculate(driver,home_handles,8,10)
        time.sleep(1)

        xpath3 = driver.find_element_by_xpath('//a[text()=\'{}\']/../../../td[17]/div/p/span[1]/a'.format('t1'))
        xpath4 = driver.find_element_by_xpath('//a[text()=\'{}\']/../../../td[18]'.format('t1'))
        ActionChains(driver).drag_and_drop(xpath3, xpath4).perform()
        num3 = self.calculate(driver, home_handles, 10, 15)
        sum = 0
        for i in range(1,len(num1)):
            sum += int(num1[i])
        sum1 = 0
        for i in range(0,len(num2)):
            sum1 += int(num2[i])
        sum2 = 0
        for i in range(0, len(num3)):
            sum2 += int(num3[i])
        if int(num1[0]) == sum + sum1 + sum2:
            self.log_file_out('故障单验证成功')
        else:
            self.log_file_out('故障单验证失败')
        driver.close()
        time.sleep(2)
        name1 = self.check_model('test','1234')
        time.sleep(2)
        Name = self.check_model('admin','123456')
        if name1 not in Name:
            self.log_file_out('不同账号之间失效情况验证成功')
        else:
            self.log_file_out('不同账号之间失效情况验证失败')

    def check_model(self,username,password):
        driver = webdriver.Chrome()
        driver.maximize_window()
        Login().login(url, username, password, driver)

        driver.maximize_window()
        time.sleep(2)
        for i in contents:
            try:
                Method(driver).contains_xpath('click', i)
                time.sleep(1)
            except Exception as e:
                logger.debug(e)

        time.sleep(2)
        try:
            Method(driver).switch_out()
            Method(driver).switch_iframe(
                driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/eds/main')]"))
            time.sleep(2)
        except NoSuchElementException as e:
            self.log_file_out('源头问题功能打开失败')
        # L = driver.find_elements_by_xpath('//a[text()=\'{}\']/../../../td'.format('t1'))[16].text.split('、')
        #

        if username == 'test':
            status = driver.find_elements_by_xpath('//td[@class="el-table_1_column_19 is-left "]')
            num = random.randint(0,len(status)-1)
            while True:
                if status[num].text == '失效':
                    model_name = driver.find_elements_by_xpath('//td[@class="el-table_1_column_2 is-left "]')[num].text
                    break
                else:
                    num = random.randint(0,len(status)-1)
            return model_name
        elif username == 'admin':
            L = []
            for i in range(0,len(driver.find_elements_by_xpath('//td[@class="el-table_1_column_2 is-left "]'))):
                L.append(driver.find_elements_by_xpath('//td[@class="el-table_1_column_2 is-left "]')[i].text)
            return L

url = 'http://192.168.1.20:8083/darams/a?login'
Check_EDS().check(url,'test','1234')


