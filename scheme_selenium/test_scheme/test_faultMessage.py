from selenium import webdriver
from config.log_config import logger
import time
from selenium.common.exceptions import NoSuchElementException

from bin.login import Login
from config.config import path_dir
from config.config import title2



#技术整改优化效果分析
class Tech:
    def log_file_out(self,msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    def tech_analysis(self,url,car):
        # option = webdriver.ChromeOptions()
        # option.add_argument("headless")
        # driver = webdriver.Chrome(chrome_options=option,                                                                executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')

        driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
        Login().login(url, 'test', '1234', driver)

        self.log_file_out('故障单信息')
        time.sleep(2)

        for i in title2:
            try:
                driver.find_element_by_xpath('//span[text()="{}"]'.format(i)).click()
                self.log_file_out('点击'+i+'成功')
                time.sleep(1)
            except Exception as e:
                logger.debug(e)
                self.log_file_out('点击' + i + '失败')

        time.sleep(5)
        try:
            driver.find_element_by_class_name('ivu-page-total').text[2:-2]
            self.log_file_out('列车信息打开成功')
        except:
            self.log_file_out('列车信息测试失败')
            return
        driver.find_element_by_xpath('//span[text()="更多"]').click()
        time.sleep(1)
        driver.find_elements_by_class_name('ivu-input-search')[0].click()
        time.sleep(1)
        # 选车
        try:
            for x in car:
                driver.find_element_by_xpath(
                    "//span[@class='train zoomIn' and contains(text(),\'{}\')]".format(x)).click()
                car_num = car.get(x)
                time.sleep(2)
                for i in car_num:
                    driver.find_element_by_xpath(
                        "//span[@class='ivu-tag-text' and contains(text(),\'{}\')]".format(i)).click()
                    time.sleep(1)
                driver.find_elements_by_xpath('//span[text()="确认"]')[1].click()
                time.sleep(2)
            self.log_file_out('选车成功')
        except NoSuchElementException as e:
            logger.debug('选车失败')
            logger.error(e)
            self.log_file_out('选车失败')

        driver.find_elements_by_xpath('//span[text()="确定"]')[0].click()

        time.sleep(1)
        driver.find_element_by_xpath('//a[text()="查询"]').click()
        time.sleep(1)
        if int(driver.find_element_by_class_name('ivu-page-total').text[2:-2]) == 176:
            self.log_file_out('故障单验证成功')
        else:
            self.log_file_out('故障单验证失败')

url = 'http://192.168.1.25:8081'


car = {'E27':['2651']}

Tech().tech_analysis(url,car)