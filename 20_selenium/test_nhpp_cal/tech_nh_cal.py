from config.config import path_dir,url,password,username,nhpp_config
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import requests
from config.log_config import logger
import time
from bin.main import Method
from bin.login import Login
from test_nhpp.nhpp_config import *



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
        self.log_file_out('-----nhpp不保存计算-----')


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
            Method(driver).switch_out()
            Method(driver).switch_iframe(
                driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/nhppModel')]"))
            Method(driver).click('id','calculate')
            time.sleep(time_sleep)
        except NoSuchElementException as e:
            self.log_file_out('不保存计算失败')

        Method(driver).switch_out()

        Method(driver).switch_iframe(
            driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/nhppModel/form2')]"))

        try:
            Method(driver).input('id','startDate',startDate)
            Method(driver).input('id','endDate',endDate)
            self.log_file_out('模型写入成功')
        except Exception as e:
            logger.debug(e)
            self.log_file_out('模型写入失败')

        Method(driver).switch_iframe(
            driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/business/opTrainGroupCust/form')]"))
        time.sleep(time_sleep)

        driver.find_element_by_xpath('//a[text()="车型"]').click()
        time.sleep(1)

        try:
            for x in car:
                driver.find_element_by_xpath(
                    "//span[@class='train zoomIn' and contains(text(),\'{}\')]".format(x)).click()
                car_num = car.get(x)
                time.sleep(2)
                if car_num == 'all':
                    driver.execute_script('top.select_all(this,"train-no-layer-class",true,true)')
                else:
                    for i in car_num:
                        # driver.find_element_by_xpath("//span[contains(text(),\'{}\')]".format(i)).click()
                        car_num = driver.find_element_by_xpath(
                            '//span[contains(text(),\'{}\')]/..'.format(i)).get_attribute('id')

                        js = 'top.checked(top.$("#{}"))'.format(car_num)
                        driver.execute_script(js)

                    # time.sleep(2)
                driver.execute_script('top.$(".layui-layer-btn0")[1].click()')
                time.sleep(2)
            self.log_file_out('选车成功')
        except NoSuchElementException as e:
            logger.error('xpath' + '不存在!')
            self.log_file_out('选车失败')

        try:
            Method(driver).switch_out()

            Method(driver).click('class', 'layui-layer-btn0')
        except NoSuchElementException as e:
            logger.error('xpath' + '不存在!')
            self.log_file_out('点击计算按钮失败')

        time.sleep(wait_time)

        Method(driver).switch_out()

        c = Method(driver).get_attr('css', "[class='layui-layer layui-layer-iframe']", 'times')


        try:
            next_url = Method(driver).get_attr('id', 'layui-layer-iframe' + c, 'src')
            print(next_url)
            if next_url == 'http://192.168.1.115:9092/darams/a/mould/nhppModel/form2':
                print('请录入正确的模型')
            else:
                status = requests.get(next_url).status_code
                if status == 200:
                    logger.debug('图表页面获取成功')
                    self.log_file_out('图表页面获取成功')
                elif status == 404:
                    logger.error('{}请求404'.format(next_url))
                    self.log_file_out('图表页面获取失败')
        except Exception as e:
            logger.error(e)


car = {
    'E01': ['2001', '2002'],
    'E02': ['2061', '2062']
}


time_sleep = 3
wait_time = 10
Tech().tech_nhpp_model(url,username,password,'2017-02-03','2018-03-12',car,time_sleep,wait_time)