import os

from selenium import webdriver
from bin.login import Login
import time
from config.config import path_dir
from new_selenium.tech_reportfile.reportfile_config import *
from bin.main import Method

class Reportfile:
    def log_file_out(self,msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()


    def tech(self,url,username,password):
        # option = webdriver.ChromeOptions()
        # option.add_argument("headless")
        # driver = webdriver.Chrome(chrome_options=option,                                                                executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')
        options = webdriver.ChromeOptions()
        prefs = {'profile.default_content_settings.popups': 0,
                 'download.default_directory': '{}/tech_reportfile'.format(path_dir),
                 "profile.default_content_setting_values.automatic_downloads": 1}
        options.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(chrome_options=options,
                                  executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
        Login().login(url, username, password, driver)

        self.log_file_out('----月报文件列表----')
        Method(driver).contains_xpath('click', '其他功能')
        time.sleep(1)
        Method(driver).contains_xpath('click','月报文件列表')

        time.sleep(2)
        Method(driver).switch_out()
        Method(driver).switch_iframe(
            driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/reportfile/list')]"))

        a = driver.find_element_by_xpath('//*[@id="1"]/td[2]').text

        time.sleep(4)
        try:
            # driver.get('http://{}/darams/a/reportfile/download?id=575'.format(serverURL))
            driver.get('http://%s/darams/a/reportfile/download?id=%s'%(serverURL,str(int(a+1))))
        except:
            self.log_file_out('月报列表404')

        time.sleep(5)
        L = []
        for root, dirs, files in os.walk('{}/tech_reportfile'.format(path_dir)):
            for file in files:
                if os.path.splitext(file)[1] == '.doc':
                    L.append(file)

        for i in L:
            if i.split('.')[0][-4:] != '2019':
                self.log_file_out('导出月报时间不对')
            else:
                self.log_file_out('导出月报正确')

url = 'http://192.168.1.115:8080/darams/a?login'

Reportfile().tech(url,'test','1234')
