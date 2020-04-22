import re
import time
from test_rams_save.rams_config import *
from selenium import  webdriver
from new_selenium.bin.login import Login
from new_selenium.bin.main import Method
from config.config import path_dir


class Home:
    def log_file_out(self,msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    def model(self,url,username,password,modelName):
        driver = webdriver.Chrome()
        Login().login(url, username, password, driver)

        try:
            Method(driver).switch_out()
            Method(driver).switch_iframe(driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/home')]"))
            self.log_file_out('切入首页成功')
        except:
            self.log_file_out('切入首页失败')

        driver.maximize_window()
        try:
            Method(driver).click('xpath','//*[@id="model"]/div/ul[1]/li/label')
            self.log_file_out('点击首页条件成功')
        except:
            self.log_file_out('点击首页条件失败')
        Method(driver).switch_out()

        model_a = Method(driver).get_attr('css', "[class='layui-layer layui-layer-iframe']", 'times')
        Method(driver).switch_iframe('layui-layer-iframe' + model_a)

        L = []
        try:
            L.append(driver.find_element_by_id('date-table').text)
            L.append(driver.find_element_by_id('mileage-table').text)
        except:
            self.log_file_out('获取基本条件失败')
        while '' in L:
            L.remove('')
        a = L[0].split('\n')[1]

        cartype = 1

        carnum = []

        for i in range(0,len(driver.find_element_by_id('train-list').text.split('\n'))):
            Method(driver).click('xpath','//*[@id="train-list"]/tr[{}]/td'.format(cartype))
            time.sleep(2)
            carnum.append(driver.find_elements_by_class_name('container-fluid')[i].text.split('\n'))
            cartype += 2

        carnum_1 = []
        for car in carnum:
            for m in car:
                carnum_1.append(m)

        time.sleep(2)
        fault = driver.find_element_by_id('fault-list').text.split('\n')

        Method(driver).switch_out()
        driver.find_element_by_class_name('layui-layer-iframe').find_element_by_class_name('layui-layer-close1').click()

        Method(driver).switch_out()
        for i in contents:
            try:
                time.sleep(1)
                Method(driver).contains_xpath('click', i)
                self.log_file_out('点击'+i+'成功')
            except Exception as e:
                print(e)
                self.log_file_out('点击' + i + '失败')

        time.sleep(2)
        Method(driver).switch_iframe(
                    driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/confModel')]"))

        time.sleep(2)
        all_num = re.findall(r"\d+\.?\d*", driver.find_element_by_class_name('pagination-info').text)[-1]

        try:
            if int(all_num) < 10:
                pass
            else:
                yu = int(all_num) % 10
                if yu == 0:
                    for i in range(0, int(all_num) // 10):
                        driver.find_element_by_xpath("//a[text()={}]".format(i + 1)).click()
                        try:
                            driver.find_element_by_xpath(
                                "//a[text()=\'{}\']/../../td[8]/a[3]".format(modelName))
                            break
                        except:
                            pass
                else:
                    for i in range(0, int(all_num) // 10 + 1):
                        driver.find_element_by_xpath("//a[text()={}]".format(i + 1)).click()
                        time.sleep(1)
                        try:
                            driver.find_element_by_xpath(
                                "//a[text()=\'{}\']/../../td[8]/a[3]".format(modelName))
                            break
                        except:
                            pass
        except Exception as e:
           print(e)

        time.sleep(2)
        try:
            driver.find_element_by_xpath(
                "//*[text()=\'{}\']/../../td[8]/a[2]".format(modelName)).click()
            self.log_file_out('点击预览成功')
        except:
            self.log_file_out('点击预览失败')

        time.sleep(2)
        Method(driver).switch_out()
        model_a = Method(driver).get_attr('css', "[class='layui-layer-shade']", 'times')
        Method(driver).switch_iframe('layui-layer-iframe' + model_a)

        L1 = []
        L1.append(driver.find_element_by_id('date-table').text)
        L1.append(driver.find_element_by_id('mileage-table').text)
        while '' in L1:
            L1.remove('')
        if a == L1[0].split('\n')[1]:
            self.log_file_out('基础条件相同')
        else:
            self.log_file_out('基础条件不同')

        carnum1 = []

        cartype1 = 1
        for i in range(0,len(driver.find_element_by_id('train-list').text.split('\n'))):
            Method(driver).click('xpath','//*[@id="train-list"]/tr[{}]/td'.format(cartype1))
            time.sleep(2)
            carnum1.append(driver.find_elements_by_class_name('container-fluid')[i].text.split('\n'))
            cartype1 += 2

        carnum1_1 = []
        for car1 in carnum1:
            for m1 in car1:
                carnum1_1.append(m1)

        if len(carnum_1) == len(carnum1_1):
            if len(list(set(carnum_1)^set(carnum1_1))) != 0:
                self.log_file_out('车号不一致')
            else:
                self.log_file_out('车号一致')
        else:
            self.log_file_out('车号不一致')


        fault1 = driver.find_element_by_id('fault-list').text.split('\n')
        if len(fault) == len(fault1):
            if len(list(set(fault)^set(fault1))) != 0:
                self.log_file_out('故障模式不一样')
            else:
                self.log_file_out('故障模式一样')
        else:
            self.log_file_out('故障模式不一样')

url = 'http://192.168.221.20:8083/darams/a?login'
Home().model(url,'admin','admin','test11')