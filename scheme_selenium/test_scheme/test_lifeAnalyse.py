from selenium import webdriver
from bin.login import Login
from selenium.common.exceptions import NoSuchElementException
from config.config import path_dir
from config.config import title9
import time
from config.log_config import logger
import os


#技术整改优化效果分析
class Tech:
    def log_file_out(self,msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    def tech_analysis(self,url):
        # option = webdriver.ChromeOptions()
        # option.add_argument("headless")
        # driver = webdriver.Chrome(chrome_options=option,                                                                executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')

        driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
        Login().login(url, 'test', '1234', driver)

        self.log_file_out('----寿命特性分析----')
        time.sleep(2)


        for i in title9:
            try:
                driver.find_element_by_xpath('//span[text()="{}"]'.format(i)).click()
                self.log_file_out('点击'+i+'成功')
                time.sleep(1)
            except Exception as e:
                logger.debug(e)
                self.log_file_out('点击' + i + '失败')

        time.sleep(2)
        a = driver.find_element_by_class_name('ivu-page-total').text[2:-2]
        try:
            driver.find_element_by_xpath('//span[text()="创建内容"]').click()
            self.log_file_out('点击创建内容成功')
        except:
            self.log_file_out('点击创建内容失败')
            return

        time.sleep(2)
        driver.find_elements_by_class_name('ivu-input-default')[1].send_keys('我是测试')

        time.sleep(1)
        driver.find_elements_by_class_name('ivu-icon-md-add')[1].click()
        time.sleep(1)
        driver.find_element_by_class_name('up-btn').click()


        time.sleep(2)
        os.system(r'C:\Users\a\Documents\temp\upload.exe')
        time.sleep(1)
        driver.find_element_by_xpath('//span[text()="确定"]').click()
        time.sleep(1)
        driver.find_element_by_xpath('//span[text()="计算"]').click()
        time.sleep(2)


        driver.find_element_by_xpath('//span[text()="保存"]').click()
        time.sleep(1)
        if int(driver.find_element_by_class_name('ivu-page-total').text[2:-2]) == int(a) + 1:
            self.log_file_out('寿命特性分析验证成功')
        else:
            self.log_file_out('寿命特性分析验证失败')

url = 'http://192.168.1.25:8081'

car = {'E27':['2651']}
fault = {'转向架':{'一系悬挂':{'一系垂向减振器':'all'},'轴箱弹簧':'all'}}

Tech().tech_analysis(url)