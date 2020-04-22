from config.config import path_dir,nhpp_config,url,username,password
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from bin.main import Method
from bin.login import Login
from bin.select_thing import *



#nhpp
class Tech:
    def log_file_out(self, msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    def tech_nhpp_model(self,url,username,password,startDate,endDate,car,time_sleep,wait_time):
        # option = webdriver.ChromeOptions()
        # option.add_argument("headless")
        # driver = webdriver.Chrome(chrome_options=option,
        #                           executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')
        driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
        Login().login(url, username, password, driver)
        time.sleep(2)
        self.log_file_out('-----nhpp-----')
        for i in nhpp_config:
            try:
                Method(driver).contains_xpath('click',i)
                time.sleep(1)
                self.log_file_out('点击'+i+'成功')
            except Exception as e:
                logger.debug(e)
                self.log_file_out('点击' + i + '失败')

        time.sleep(time_sleep)
        try:
            Method(driver).click('xpath','//span[text()="不保存计算"]')
            time.sleep(time_sleep)
        except NoSuchElementException as e:
            self.log_file_out('新建失败 找不到新建对应的xpath')

        # 不保存计算
        try:
            driver.find_elements_by_class_name('ivu-input-default')[0].send_keys(startDate)
            time.sleep(0.5)
            driver.find_elements_by_class_name('ivu-input-default')[1].send_keys(endDate)
            time.sleep(0.5)

            self.log_file_out('里程录入成功')
        except NoSuchElementException as e:
            self.log_file_out('里程录入失败')

        car_status = deal_car(driver, car, 1)
        if car_status is True:
            self.log_file_out('选车成功')
        else:
            self.log_file_out('选车失败')
            return
        try:
            time.sleep(time_sleep)
            driver.find_element_by_xpath('//span[text()="计算"]').click()
        except NoSuchElementException as e:
            logger.error(e)
            self.log_file_out('保存失败')

        time.sleep(10)


car = {
    'E27': ['2641', '2642','2643','2644','2645','2646','2647','2648','2649']}

time_sleep = 3
wait_time = 10
Tech().tech_nhpp_model(url,username,password,'2016-12-28','2018-03-12',car,time_sleep,wait_time)