import os
from selenium import webdriver
from config.log_config import logger
import time
from selenium.common.exceptions import NoSuchElementException
from bin.main import Method
from bin.login import Login
from new_selenium.tech_zxx.zxx_config import *
from config.config import path_dir

#列车信息
class test_technology:
    def log_file_out(self,msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    def tech(self,url,username,password):

        options = webdriver.ChromeOptions()
        prefs = {'profile.default_content_settings.popups': 0,
                 'download.default_directory': '{}/tech_zxx'.format(path_dir),
                 "profile.default_content_setting_values.automatic_downloads": 1}
        options.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(chrome_options=options,
                                  executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
        Login().login(url,username, password, driver)

        driver.maximize_window()
        self.log_file_out('-----专项修故障导出-----')

        # for i in contents:
        #     try:
        #         Method(driver).contains_xpath('click',i)
        #         time.sleep(2)
        #         self.log_file_out('点击'+i+'成功')
        #     except Exception as e:
        #         logger.debug(e)
        #         self.log_file_out('点击' + i + '失败')
        #
        # try:
        #     Method(driver).switch_out()
        #     Method(driver).switch_iframe(driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/zxx/index/list')]"))
        #     self.log_file_out('切入专项修成功')
        # except:
        #     self.log_file_out('切入专项修失败')

        driver.get('http://192.168.1.115:8080/darams/a/zxx/index/list')
        time.sleep(2)
        try:
            Method(driver).click('id','btnImport')
            time.sleep(2)
            driver.find_element_by_id("uploadFile").send_keys("{}/tech_zxx/2017年扩大验证88列100组对比动车组信息0922.xlsx".format(path_dir))

            self.log_file_out('上传成功')
        except NoSuchElementException as e:
            self.log_file_out('上传失败')

        time.sleep(5)
        driver.execute_script('top.$(".layui-layer-btn0")[0].click()')
        try:
            Method(driver).click('xpath','//*[@id="party1table"]/tbody/tr[1]/td[1]/input')
            time.sleep(1)
            Method(driver).click('id','tag')
            self.log_file_out('标记成功')
        except NoSuchElementException as e:
            self.log_file_out('标记失败')

        time.sleep(5)

        try:
            Method(driver).click('id','btnExport')
            self.log_file_out('导出专项修成功')
        except:
            self.log_file_out('导出专项修失败')

        time.sleep(10)

        L = []
        for root, dirs, files in os.walk('{}/tech_zxx'.format(path_dir)):
            for file in files:
                if os.path.splitext(file)[1] == '.xlsx':
                    L.append(file)

        print(L)

url = 'http://192.168.1.115:8080/darams/a?login'

test_technology().tech(url,'test','1234')
