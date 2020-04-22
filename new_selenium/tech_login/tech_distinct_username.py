import re
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from config.log_config import logger
import time
from bin.main import Method
from bin.login import Login
from new_selenium.test_weixiu.weixiu_config import *
from config.config import path_dir

#维修规程优化效果分析
class test_technology:
    def log_file_out(self,msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()


    # 检查RAMS运营数据分析
    def tech(self,url,account):

        # option = webdriver.ChromeOptions()
        # option.add_argument("headless")
        # driver = webdriver.Chrome(chrome_options=option
        # ,executable_path=r'../apps/chromedriver.exe'
        #  )
        # driver.maximize_window()

        L = []
        for use_pass in account:
            driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
            Login().login(url,use_pass,account.get(use_pass),driver)

            self.log_file_out('-----账号隔离-----')

            try:
                for i in contents:
                    try:
                        Method(driver).contains_xpath('click',i)
                        self.log_file_out('点击'+i+'成功')
                    except Exception as e:
                        logger.debug(e)
                        self.log_file_out('点击' + i + '失败')
                time.sleep(2)
                # 点击新建得到弹框
                try:
                    Method(driver).switch_out()
                    Method(driver).switch_iframe(driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/repairProcedure')]"))
                    a = driver.find_element_by_class_name('pagination-info').text[13:]
                    b = re.sub("\D", "", a)
                    time.sleep(2)
                    L.append(b)
                    driver.close()
                except NoSuchElementException as e:
                    self.log_file_out('点击新建按钮失败,未找到新建按钮的xpath')

            except:
                print(e)


        if int(L[0]) != int(L[-1]):
            self.log_file_out('账号隔离验证成功')
        else:
            self.log_file_out('账号隔离验证失败')



url = 'http://192.168.1.115:8080/darams/a/login'
account = {'admin':'admin','test':'1234'}

test_technology().tech(url,account)