from config.config import path_dir
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from config.log_config import logger
import time
from bin.main import Method
from bin.login import Login
from new_selenium.tech_compare.compare_config import *




#技术整改优化效果分析
class Tech:
    def log_file_out(self,msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    def tech_analysis(self,url,username,password,value,min_model,time_sleep):
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
            Method(driver).click('id', 'calculate')
            time.sleep(time_sleep)
        except NoSuchElementException as e:
            self.log_file_out('点击不保存计算按钮失败,获取不到相应的xpath')

        Method(driver).switch_out()

        Method(driver).switch_iframe(driver.find_element_by_xpath(
            "//iframe[contains(@src,'/darams/a/mould/moreModel/form2?modelType=MORE_MODEL')]"))

        try:
            Method(driver).select_down_list('id', 'modelObject', value)
        except NoSuchElementException as e:
            print('模型录入错误 找不到对应的xpath')
        except:
            print('模型录入数据出错')

        i = 1
        try:
            for x in min_model:
                Method(driver).click('xpath', '//*[@id="inputForm"]/a[2]')

                time.sleep(2)
                Method(driver).switch_out()
                Method(driver).switch_iframe(driver.find_element_by_xpath(
                    "//iframe[contains(@src,'/darams/a/mould/moreModel/import?modelObject=3&modelType=USER_MODEL')]"))

                driver.find_element_by_xpath("//a[contains(text(),\'{}\')]/../../td[1]/input".format(x)).click()

                Method(driver).switch_out()
                js = 'top.$(".layui-layer-btn0")[1].click()'
                driver.execute_script(js)

                time.sleep(2)
                Method(driver).switch_out()
                Method(driver).switch_iframe(driver.find_element_by_xpath(
                    "//iframe[contains(@src,'/darams/a/mould/moreModel/form2?modelType=MORE_MODEL')]"))
                Method(driver).click('xpath', '//*[@id="subSet{}"]/li[1]/div/button'.format(i))
                i += 1
        except:
            self.log_file_out('模型导入出错')


        try:
            Method(driver).switch_out()

            Method(driver).click('class', 'layui-layer-btn0')
        except NoSuchElementException as e:
            logger.error('xpath' + '不存在!')
            self.log_file_out('点击计算按钮失败')
        except:
            print('请录入正确的模型')
            return

        time.sleep(20)

        try:
            Method(driver).switch_out()
            Method(driver).switch_iframe(driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/moreModel/charts?modelId=moremodelcalculate')]"))
            time.sleep(time_sleep)
            logger.debug('图表页面获取成功')
            self.log_file_out('图表页面获取成功')
        except NoSuchElementException as e:
            self.log_file_out('图表页面获取失败')
        except:
            print('图表页面获取失败')

url = 'http://192.168.1.20:8083/darams/a?login'
username = 'test'
password = '1234'
min_model = ['111','222']
time_sleep = 2


Tech().tech_analysis(url,username,password,3,min_model,time_sleep)