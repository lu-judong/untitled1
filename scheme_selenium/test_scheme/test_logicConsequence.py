from selenium import webdriver
from config.log_config import logger
import time
from bin.login import Login

from config.config import path_dir
from config.config import title5


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

        self.log_file_out('----逻辑决断图节点信息维护----')
        time.sleep(2)

        for i in title5:
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
        driver.find_elements_by_class_name('ivu-input')[1].send_keys('我是测试')
        time.sleep(1)
        #选择节点类型
        driver.find_elements_by_class_name('ivu-input')[2].send_keys('A')
        time.sleep(1)

        driver.find_element_by_xpath('//span[text()="保存"]').click()
        time.sleep(1)
        if int(driver.find_element_by_class_name('ivu-page-total').text[2:-2]) == int(a) + 1:
            self.log_file_out('逻辑决断图后果维护验证成功')
        else:
            self.log_file_out('逻辑决断图后果维护验证失败')

url = 'http://192.168.1.25:8081'

Tech().tech_analysis(url)