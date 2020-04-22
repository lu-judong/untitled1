from selenium import webdriver
import time
from bin.main import Method
from bin.login import Login
from config.config import path_dir
from new_selenium.tech_reportfile.reportfile_config import *

#列车信息
class report:
    def log_file_out(self,msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    def tech(self,url,username,password):

        driver = webdriver.Chrome()
        Login().login(url,username, password, driver)

        self.log_file_out('-----月报导出-----')
        time.sleep(2)

        driver.get('http://192.168.1.115:8080/darams/a/reportForMonth/list')

        driver.maximize_window()

        time.sleep(2)

        try:
            Method(driver).input('id','year','2019')
            self.log_file_out('输入时间成功')
        except:
            self.log_file_out('输入时间失败')
        try:
            Method(driver).click('id', 'js')
            self.log_file_out('点击成功')
        except:
            self.log_file_out('点击失败')
            time.sleep(5)
        try:
            Method(driver).click('id','ceshi')
            time.sleep(5)
            self.log_file_out('点击默认数据成功')
        except:
            self.log_file_out('点击默认数据失败')
        try:
            Method(driver).click('id','export')
            self.log_file_out('点击导出按钮成功')
        except:
            self.log_file_out('点击导出按钮失败')


        time.sleep(5)
        driver.close()

        # Login().login(url, username, password, driver)
        # try:
        #     driver.get('http://{}/darams/a/reportfile/list'.format(serverURL))
        # except:
        #     self.log_file_out('月报列表获取失败')
        # time.sleep(4)
        # if driver.find_element_by_xpath('//*[@id="1"]/td[6]]').text != '正在计算':
        #     self.log_file_out('导出月报失败')
        # else:
        #     self.log_file_out('导出月报成功')


url = 'http://192.168.221.20:8083/darams/a/login'




report().tech(url,'test','1234')