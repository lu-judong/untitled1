from config.config import path_dir
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,WebDriverException
import requests
from config.log_config import logger
import time
from bin.main import Method
from bin.login import Login
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from new_selenium.tech_nhpp.nhpp_config import *



#nhpp
class Tech:
    def log_file_out(self, msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    def tech_nhpp_model(self,url,username,password,modelCode,modelName,startDate,endDate,car,time_sleep,wait_time):
        # option = webdriver.ChromeOptions()
        # option.add_argument("headless")
        # driver = webdriver.Chrome(chrome_options=option,
        #                           executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')
        driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
        Login().login(url, username, password, driver)
        self.log_file_out('-----nhpp-----')
        for i in contents:
            try:
                Method(driver).contains_xpath('click',i)
                self.log_file_out('点击'+i+'成功')
            except Exception as e:
                logger.debug(e)
                self.log_file_out('点击' + i + '失败')

        time.sleep(time_sleep)
        try:
            Method(driver).switch_out()
            Method(driver).switch_iframe(
                driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/nhppModel')]"))
            Method(driver).click('xpath','//*[@id="add"]')
            time.sleep(time_sleep)
        except NoSuchElementException as e:
            self.log_file_out('新建失败 找不到新建对应的xpath')

        Method(driver).switch_out()
        a = Method(driver).get_attr('css',"[class='layui-layer layui-layer-iframe']",'times')
        Method(driver).switch_iframe('layui-layer-iframe' + a)

        try:
            Method(driver).input('id', 'modelCode', modelCode)
            Method(driver).input('id', 'modelName', modelName)
            Method(driver).input('id','startDate',startDate)
            Method(driver).input('id','endDate',endDate)
            self.log_file_out('模型写入成功')
        except Exception as e:
            logger.debug(e)
            self.log_file_out('模型写入失败')

        Method(driver).switch_iframe('opTrainGroupForm')
        time.sleep(time_sleep)

        try:
            for x in car:
                driver.find_element_by_xpath(
                    "//span[@class='train zoomIn' and contains(text(),\'{}\')]".format(x)).click()
                car_num = car.get(x)
                time.sleep(2)
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
            self.log_file_out('点击保存按钮失败')

        Method(driver).switch_out()
        Method(driver).switch_iframe(driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/nhppModel')]"))
        time.sleep(1)

        # xpath 不合法
        # driver.find_element_by_xpath("//a[contains(text(),'\{}\')]/../../td[7]/a[2]".format(modelCode)).find_element_by_xpath(
        #     "//a[contains(text(),'评估')]").click()
        try:
            driver.find_element_by_xpath("//a[contains(text(),\'{}\')]/../../td[7]/a[2]".format(modelCode)).click()
        except WebDriverException:
            print('请录入正确的模型')
            return

        try:
            a = WebDriverWait(driver,wait_time).until(EC.text_to_be_present_in_element((By.XPATH, "//a[contains(text(),\'{}\')]/../../td[4]".format(modelCode)), u'计算完成'))
            if a is True:
                logger.debug('评估成功')
                self.log_file_out('评估成功')
                driver.find_element_by_xpath("//a[contains(text(),\'{}\')]/../../td[7]/a[3]".format(modelCode)).click()

                # 查看点击图表出来的页面是否存在
                Method(driver).switch_out()
                c = Method(driver).get_attr('css', "[class='layui-layer layui-layer-iframe']", 'times')
                try:
                    next_url = Method(driver).get_attr('id', 'layui-layer-iframe' + c, 'src')
                    status = requests.get(next_url).status_code
                    if status == 200:
                        logger.debug('图表页面获取成功')
                        self.log_file_out('图表页面获取成功')
                        driver.close()
                    elif status == 404:
                        logger.error('{}请求404'.format(next_url))
                        self.log_file_out('图表页面获取失败')
                        driver.close()
                except Exception as e:
                    logger.error(e)
        except Exception as e:
            logger.debug('评估失败')
            self.log_file_out('评估失败')

url = 'http://192.168.1.115:8080/darams/a/login'
car = {
    'E27': ['2641', '2642','2643','2644','2645','2646','2647','2648','2649']}



time_sleep = 3
wait_time = 10
Tech().tech_nhpp_model(url,'test','1234','nhpp2','nhpp2','2016-12-28','2018-03-12',car,time_sleep,wait_time)