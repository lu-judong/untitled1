from selenium import webdriver
from bin.login import Login
from selenium.common.exceptions import NoSuchElementException
from config.config import path_dir
from bin.select_system import  *
from config.config import title10


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

        self.log_file_out('----自动FMECA----')
        time.sleep(2)


        for i in title10:
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
            driver.find_element_by_xpath('//a[text()="创建内容"]').click()
            self.log_file_out('点击创建内容成功')
        except:
            self.log_file_out('点击创建内容失败')
            return

        driver.find_elements_by_class_name('ivu-input-default')[2].send_keys('我是测试')
        time.sleep(0.5)
        driver.find_elements_by_class_name('ivu-input-default')[3].send_keys('A')
        time.sleep(0.5)

        driver.find_elements_by_class_name('ivu-input-default')[5].send_keys('1')
        time.sleep(0.5)
        driver.find_elements_by_class_name('ivu-input-default')[6].send_keys('20')
        time.sleep(0.5)
        driver.find_elements_by_class_name('ivu-input-default')[7].send_keys('0.8')
        time.sleep(0.5)
        driver.find_elements_by_class_name('ivu-input-default')[8].send_keys('30')
        time.sleep(0.5)
        driver.find_elements_by_class_name('ivu-input-default')[9].send_keys('200')
        time.sleep(0.5)

        try:
            driver.find_element_by_xpath('//span[text()="计算"]').click()
            self.log_file_out('点击计算成功')
        except NoSuchElementException as e:
            logger.error(e)
            self.log_file_out('点击计算失败')
        time.sleep(2)
        driver.find_element_by_xpath('//span[text()="保存"]').click()
        time.sleep(3)
        if int(driver.find_element_by_class_name('ivu-page-total').text[2:-2]) == int(a) + 1:
            self.log_file_out('RCM计算验证成功')
        else:
            self.log_file_out('RCM计算验证失败')

url = 'http://192.168.1.25:8081'

Tech().tech_analysis(url)