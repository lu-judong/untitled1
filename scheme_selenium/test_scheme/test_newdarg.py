import random

from selenium import webdriver
from config.log_config import logger
import time
from bin.login import Login
from config.config import path_dir
from config.config import title12
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys


class Tech:
    def log_file_out(self, msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    def tech_analysis(self, url, username, password, car, startDate):
        # option = webdriver.ChromeOptions()
        # option.add_argument("headless")
        # driver = webdriver.Chrome(chrome_options=option,                                                                executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')

        driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
        # driver.find_element_by_xpath('//span[text()="重新登录"]').click()
        driver.maximize_window()
        Login().login(url, username, password, driver)
        # time.sleep(8)
        # driver.find_element_by_id('ballc').click()

        time.sleep(2)


        for i in title12:
            try:
                driver.find_element_by_xpath('//span[text()="{}"]'.format(i)).click()
                self.log_file_out('点击' + i + '成功')
                time.sleep(1)
            except Exception as e:
                logger.debug(e)
                self.log_file_out('点击' + i + '失败')

        time.sleep(2)
        driver.find_element_by_xpath('//span[text()="{}"]'.format(car)).click()
        time.sleep(1)
        driver.find_elements_by_class_name('ivu-tag-text')[-1].click()
        driver.find_elements_by_class_name('ivu-tag-text')[-1].click()
        time.sleep(2)
        driver.find_element_by_xpath('//span[text()="修改"]').click()

        time.sleep(2)
        # driver.execute_script("document.body.style.zoom='0.9'")
        #
        # t0 = driver.find_elements_by_class_name('total-para')[0].text
        # self.log_file_out(t0)
        # t_0 = driver.find_elements_by_class_name('total-para')[11].text
        # self.log_file_out(t_0)
        driver.execute_script("document.body.style.zoom='1'")

        element = driver.find_elements_by_class_name('tr-plan-editUnit')[0]
        ActionChains(driver).context_click(element).perform()
        time.sleep(1)
        driver.find_element_by_xpath('//li[text()="新建"]').click()
        time.sleep(2)
        element = driver.find_element_by_class_name('ivu-input-with-suffix')
        ActionChains(driver).double_click(element).perform()
        time.sleep(1)
        element.send_keys(Keys.CONTROL + 'a')
        element.send_keys(Keys.BACKSPACE)
        time.sleep(1)
        driver.find_element_by_class_name('ivu-input-with-suffix').send_keys(startDate)

        driver.find_elements_by_xpath('//span[text()="确认"]')[1].click()
        driver.find_elements_by_xpath('//span[text()="确认"]')[1].click()

        time.sleep(2)
        # 拖拽
        jquery_str = ""
        try:
            f = open('../config/jquery-3.4.1.min.js', 'r', encoding='utf-8')
            line = f.readline()
            while line:
                jquery_str += line
                line = f.readline()
        except:
            self.log_file_out('打开jquery失败')

        dnd_str = ""
        try:
            f = open('../config/test.js', 'r', encoding='utf-8')
            line = f.readline()
            while line:
                dnd_str += line
                line = f.readline()
        except:
            self.log_file_out('打开js文件失败')

        L = []
        for i in range(0,len(driver.find_elements_by_class_name('tr-plan-editUnit'))):
            L.append(driver.find_elements_by_class_name('tr-plan-editUnit')[i].get_attribute('id'))

        a0 = L[random.randint(0,len(L)-1)]

        driver.execute_script(jquery_str + dnd_str + "$('#%s').simulateDragDrop({ dropTarget: '#planWrap_4'});" % a0)

        time.sleep(1)

        driver.find_elements_by_xpath('//span[text()="确认"]')[1].click()
        time.sleep(2)

        a1 = driver.find_elements_by_class_name('tr-plan-editUnit')[2].get_attribute('id')

        driver.execute_script(jquery_str + dnd_str + "$('#%s').simulateDragDrop({ dropTarget: '#%s'});" % (a1, 'planWrap_6'))
        time.sleep(1)
        driver.find_elements_by_xpath('//span[text()="确认"]')[1].click()
        time.sleep(2)
        a2 = driver.find_elements_by_class_name('tr-plan-editUnit')[1].get_attribute('id')

        driver.execute_script(jquery_str + dnd_str + "$('#%s').simulateDragDrop({ dropTarget: '#%s'});" % (a2, 'planWrap_3'))
        time.sleep(1)
        driver.find_elements_by_xpath('//span[text()="确认"]')[1].click()
        time.sleep(2)
        element = driver.find_elements_by_class_name('tr-plan-editUnit')[1]
        ActionChains(driver).context_click(element).perform()
        time.sleep(1)
        driver.find_element_by_xpath('//li[text()="删除"]').click()
        time.sleep(2)
        driver.execute_script("document.body.style.zoom='0.9'")
        t1 = driver.find_elements_by_class_name('total-para')[0].text
        time.sleep(2)
        t_1 = driver.find_elements_by_class_name('total-para')[11].text
        self.log_file_out(t1)
        self.log_file_out(t_1)
        driver.close()

    def tech_analysis1(self, url, username, password):

        driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
        Login().login(url, username, password, driver)
        driver.maximize_window()
        time.sleep(2)
        # driver.find_element_by_id('ballc').click()

        self.log_file_out('----usecase1----')
        time.sleep(2)

        for i in title12:
            try:
                driver.find_element_by_xpath('//span[text()="{}"]'.format(i)).click()
                self.log_file_out('点击' + i + '成功')
                time.sleep(1)
            except Exception as e:
                logger.debug(e)
                self.log_file_out('点击' + i + '失败')

        time.sleep(2)
        driver.find_element_by_xpath('//span[text()="17型车"]').click()
        time.sleep(1)
        driver.find_elements_by_class_name('ivu-tag-text')[-1].click()
        driver.find_elements_by_class_name('ivu-tag-text')[-1].click()
        time.sleep(2)
        driver.find_element_by_xpath('//span[text()="修改"]').click()

        driver.execute_script("document.body.style.zoom='0.9'")

        t0 = driver.find_elements_by_class_name('total-para')[0].text
        self.log_file_out(t0)
        t_0 = driver.find_elements_by_class_name('total-para')[11].text
        self.log_file_out(t_0)
        driver.execute_script("document.body.style.zoom='1'")


        time.sleep(2)
        # 拖拽
        jquery_str = ""
        try:
            f = open('../config/jquery-3.4.1.min.js', 'r', encoding='utf-8')
            line = f.readline()
            while line:
                jquery_str += line
                line = f.readline()
        except:
            self.log_file_out('打开jquery失败')

        dnd_str = ""
        try:
            f = open('../config/test.js', 'r', encoding='utf-8')
            line = f.readline()
            while line:
                dnd_str += line
                line = f.readline()
        except:
            self.log_file_out('打开js文件失败')

        a0 = driver.find_elements_by_class_name('tr-plan-editUnit')[0].get_attribute('id')

        driver.execute_script(jquery_str + dnd_str + "$('#%s').simulateDragDrop({ dropTarget: '#planWrap_1'});" % a0)

        time.sleep(1)

        driver.find_elements_by_xpath('//span[text()="确认"]')[1].click()
        time.sleep(2)

        a1 = driver.find_elements_by_class_name('tr-plan-editUnit')[0].get_attribute('id')

        driver.execute_script(
            jquery_str + dnd_str + "$('#%s').simulateDragDrop({ dropTarget: '#%s'});" % (a1, 'planWrap_2'))
        time.sleep(1)
        driver.find_elements_by_xpath('//span[text()="确认"]')[1].click()
        time.sleep(2)
        a2 = driver.find_elements_by_class_name('tr-plan-editUnit')[0].get_attribute('id')

        driver.execute_script(
            jquery_str + dnd_str + "$('#%s').simulateDragDrop({ dropTarget: '#%s'});" % (a2, 'planWrap_0'))
        time.sleep(1)
        driver.find_elements_by_xpath('//span[text()="确认"]')[1].click()
        time.sleep(2)

        element = driver.find_elements_by_class_name('tr-plan-editUnit')[-1]
        ActionChains(driver).context_click(element).perform()
        time.sleep(1)

        driver.find_element_by_xpath('//li[text()="删除"]').click()

        time.sleep(2)
        element = driver.find_elements_by_class_name('tr-plan-editUnit')[0]
        ActionChains(driver).context_click(element).perform()
        driver.find_element_by_xpath('//li[text()="新建"]').click()
        time.sleep(2)
        element = driver.find_element_by_class_name('ivu-input-with-suffix')
        ActionChains(driver).double_click(element).perform()
        time.sleep(1)
        element.send_keys(Keys.CONTROL + 'a')
        element.send_keys(Keys.BACKSPACE)
        time.sleep(1)
        driver.find_element_by_class_name('ivu-input-with-suffix').send_keys('2020-08-07')

        driver.find_elements_by_xpath('//span[text()="确认"]')[1].click()
        driver.find_elements_by_xpath('//span[text()="确认"]')[1].click()
        time.sleep(2)
        driver.execute_script("document.body.style.zoom='0.9'")
        t1 = driver.find_elements_by_class_name('total-para')[0].text
        time.sleep(2)
        t_1 = driver.find_elements_by_class_name('total-para')[11].text
        self.log_file_out(t1)
        self.log_file_out(t_1)
        driver.close()

    def tech_analysis2(self,url,username,password):
        driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
        Login().login(url, username, password, driver)
        driver.maximize_window()
        # driver.find_element_by_id('ballc').click()

        self.log_file_out('----usecase2----')
        time.sleep(2)

        for i in title12:
            try:
                driver.find_element_by_xpath('//span[text()="{}"]'.format(i)).click()
                self.log_file_out('点击' + i + '成功')
                time.sleep(1)
            except Exception as e:
                logger.debug(e)
                self.log_file_out('点击' + i + '失败')

        time.sleep(2)
        driver.find_element_by_xpath('//span[text()="17型车"]').click()
        time.sleep(1)
        driver.find_elements_by_class_name('ivu-tag-text')[-1].click()
        driver.find_elements_by_class_name('ivu-tag-text')[-1].click()
        time.sleep(2)
        driver.find_element_by_xpath('//span[text()="修改"]').click()

        time.sleep(2)
        driver.execute_script("document.body.style.zoom='0.9'")

        t0 = driver.find_elements_by_class_name('total-para')[0].text
        self.log_file_out(t0)
        t_0 = driver.find_elements_by_class_name('total-para')[11].text
        self.log_file_out(t_0)
        driver.execute_script("document.body.style.zoom='1'")

        element = driver.find_elements_by_class_name('tr-plan-editUnit')[0]
        ActionChains(driver).context_click(element).perform()
        time.sleep(1)
        driver.find_element_by_xpath('//li[text()="删除"]').click()
        time.sleep(2)

        element = driver.find_elements_by_class_name('tr-plan-editUnit')[0]
        ActionChains(driver).context_click(element).perform()
        time.sleep(1)
        driver.find_element_by_xpath('//li[text()="新建"]').click()
        time.sleep(2)
        element = driver.find_element_by_class_name('ivu-input-with-suffix')
        ActionChains(driver).double_click(element).perform()
        time.sleep(1)
        element.send_keys(Keys.CONTROL + 'a')
        element.send_keys(Keys.BACKSPACE)
        time.sleep(1)
        driver.find_element_by_class_name('ivu-input-with-suffix').send_keys('2019-09-10')

        driver.find_elements_by_xpath('//span[text()="确认"]')[1].click()
        driver.find_elements_by_xpath('//span[text()="确认"]')[1].click()

        time.sleep(2)
        # 拖拽
        jquery_str = ""
        try:
            f = open('../config/jquery-3.4.1.min.js', 'r', encoding='utf-8')
            line = f.readline()
            while line:
                jquery_str += line
                line = f.readline()
        except:
            self.log_file_out('打开jquery失败')

        dnd_str = ""
        try:
            f = open('../config/test.js', 'r', encoding='utf-8')
            line = f.readline()
            while line:
                dnd_str += line
                line = f.readline()
        except:
            self.log_file_out('打开js文件失败')

        a0 = driver.find_elements_by_class_name('tr-plan-editUnit')[0].get_attribute('id')

        driver.execute_script(jquery_str + dnd_str + "$('#%s').simulateDragDrop({ dropTarget: '#planWrap_1'});" % a0)

        time.sleep(1)

        driver.find_elements_by_xpath('//span[text()="确认"]')[1].click()
        time.sleep(2)

        a1 = driver.find_elements_by_class_name('tr-plan-editUnit')[0].get_attribute('id')

        driver.execute_script(
            jquery_str + dnd_str + "$('#%s').simulateDragDrop({ dropTarget: '#%s'});" % (a1, 'planWrap_2'))
        time.sleep(1)
        driver.find_elements_by_xpath('//span[text()="确认"]')[1].click()
        time.sleep(2)
        a1 = driver.find_elements_by_class_name('tr-plan-editUnit')[0].get_attribute('id')

        driver.execute_script(
            jquery_str + dnd_str + "$('#%s').simulateDragDrop({ dropTarget: '#%s'});" % (a1, 'planWrap_3'))

        driver.find_elements_by_xpath('//span[text()="确认"]')[1].click()
        time.sleep(2)
        a2 = driver.find_elements_by_class_name('tr-plan-editUnit')[0].get_attribute('id')

        driver.execute_script(
            jquery_str + dnd_str + "$('#%s').simulateDragDrop({ dropTarget: '#%s'});" % (a2, 'planWrap_0'))
        time.sleep(1)
        driver.find_elements_by_xpath('//span[text()="确认"]')[1].click()
        time.sleep(2)
        driver.execute_script("document.body.style.zoom='0.9'")
        t1 = driver.find_elements_by_class_name('total-para')[0].text
        time.sleep(2)
        t_1 = driver.find_elements_by_class_name('total-para')[11].text
        self.log_file_out(t1)
        self.log_file_out(t_1)
        driver.close()


# url = 'http://192.168.1.25:8081/rcma.html#'
url = 'http://101.201.113.42:8284/rcma.html#/home?user=test4'

Tech().tech_analysis(url,'test4','1234','17型车','2019-11-01')


