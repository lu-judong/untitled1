from config.config import path_dir
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from config.log_config import logger
import time
from bin.main import Method
from bin.login import Login
from new_selenium.tech_compare.compare_config import *
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC



#技术整改优化效果分析
class Tech:
    def log_file_out(self,msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    def tech_analysis(self,url,username,password,modelName,value,min_model,time_sleep,wait_time):
        # option = webdriver.ChromeOptions()
        # option.add_argument("headless")
        # driver = webdriver.Chrome(chrome_options=option,                                                                executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')
        driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
        Login().login(url, username, password, driver)

        self.log_file_out('-----不同平台对比bug 导出模型显示模型名已存在-----')

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
                driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/moreModel')]"))
            Method(driver).click('id', 'add')
            time.sleep(time_sleep)
        except NoSuchElementException as e:
            self.log_file_out('点击不保存计算按钮失败,获取不到相应的xpath')

        Method(driver).switch_out()

        Method(driver).switch_iframe(
            driver.find_element_by_xpath(
                "//iframe[contains(@src,'/darams/a/mould/moreModel/form?modelType=MORE_MODEL')]"))

        try:
            Method(driver).input('id','modelName',modelName)
            Method(driver).select_down_list('id', 'modelObject', value)
            self.log_file_out('模型基本信息录入成功')
        except NoSuchElementException as e:
            self.log_file_out('模型基本信息录入失败')

        i = 1
        for x in min_model:
            Method(driver).click('xpath','//*[@id="inputForm"]/a[2]')

            time.sleep(2)
            Method(driver).switch_out()
            Method(driver).switch_iframe(driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/moreModel/import?modelObject=3&modelType=USER_MODEL')]"))

            driver.find_element_by_xpath("//a[contains(text(),\'{}\')]/../../td[1]/input".format(x)).click()

            Method(driver).switch_out()
            js = 'top.$(".layui-layer-btn0")[1].click()'
            driver.execute_script(js)

            time.sleep(2)
            Method(driver).switch_out()
            Method(driver).switch_iframe(driver.find_element_by_xpath(
                "//iframe[contains(@src,'/darams/a/mould/moreModel/form?modelType=MORE_MODEL')]"))
            Method(driver).click('xpath', '//*[@id="subSet{}"]/li[1]/div/button'.format(i))
            i += 1

        try:
            time.sleep(time_sleep)
            js1 = 'top.$(".layui-layer-btn0")[0].click()'
            driver.execute_script(js1)
        except NoSuchElementException as e:
            logger.error('xpath' + '不存在!')
            self.log_file_out('保存失败')
        except:
            self.log_file_out('请输入正确的模型')
            return


        time.sleep(2)
        Method(driver).switch_out()
        Method(driver).switch_iframe(
            driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/moreModel')]"))

        try:
            driver.find_element_by_xpath(
                "//a[contains(text(),\'{}\')]/../../td[8]/a[3]".format(modelName)).click()
            self.log_file_out('点击评估按钮成功')
        except WebDriverException:
            self.log_file_out('点击评估按钮失败')
            return

        time.sleep(10)

        try:
            a = WebDriverWait(driver, wait_time).until(
                EC.text_to_be_present_in_element(
                    (By.XPATH, "//a[contains(text(),\'{}\')]/../../td[5]".format(modelName)),
                    u'计算完成'))
            if a is True:
                logger.debug('评估成功')
                self.log_file_out('评估成功')

                driver.find_element_by_xpath(
                    "//a[contains(text(),\'{}\')]/../../td[8]/a[4]".format(modelName)).click()

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


url = 'http://192.168.1.20:8083/darams/a?login'
username = 'test'
password = '1234'
min_model = ['111','222']
time_sleep = 2
wait_time = 20

Tech().tech_analysis(url,username,password,'不同平台测试数据2',3,min_model,time_sleep,wait_time)