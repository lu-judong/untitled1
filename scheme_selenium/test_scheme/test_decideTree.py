from selenium import webdriver
from config.log_config import logger
import time
from bin.login import Login
from config.config import path_dir
from config.config import title6


#技术整改优化效果分析
class Tech:
    def log_file_out(self,msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    def tech_analysis(self,url):
        # option = webdriver.ChromeOptions()
        # option.add_argument("headless")
        # driver = webdriver.Chrome(chrome_options=option,                                                                executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')

        driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
        Login().login(url, 'test', '1234', driver)

        self.log_file_out('----决策树----')
        time.sleep(2)
        driver.find_element_by_class_name('arrow-btn').click()
        time.sleep(1)
        driver.find_elements_by_class_name('nav-btn')[2].click()
        time.sleep(2)

        for i in title6:
            try:
                driver.find_element_by_xpath('//span[text()="{}"]'.format(i)).click()
                self.log_file_out('点击'+i+'成功')
                time.sleep(1)
            except Exception as e:
                logger.debug(e)
                self.log_file_out('点击' + i + '失败')

        time.sleep(2)
        a = driver.find_element_by_class_name('ivu-page-total').text[2:-2]
        try:
            driver.find_element_by_xpath('//span[text()="创建内容"]').click()
            self.log_file_out('点击创建内容成功')
        except:
            self.log_file_out('点击创建内容失败')
            return

        time.sleep(2)

        driver.find_elements_by_class_name('ivu-input-default')[1].send_keys('我是测试')
        time.sleep(1)
        driver.find_elements_by_class_name('ivu-input-default')[2].send_keys('A')
        time.sleep(1)

        driver.find_elements_by_class_name('ivu-collapse-header')[0].click()
        time.sleep(2)
        driver.find_elements_by_class_name('ivu-collapse-header')[1].click()

        # 拖拽
        jquery_str = ""
        try:
            f = open('../config/jquery-3.4.1.min.js','r',encoding='utf-8')
            line = f.readline()
            while line:
                jquery_str +=  line
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

        a0 = driver.find_elements_by_class_name('ogrC-labelType-blank')[0].get_attribute('id')

        driver.execute_script(jquery_str + dnd_str + "$('#que_0').simulateDragDrop({ dropTarget: '#{}'});".format(a0))
        L = []
        for i in len(driver.find_elements_by_class_name('ogrC-labelType-blank')):
            L.append(driver.find_elements_by_class_name('ogrC-labelType-blank')[i].get_attribute('id'))
        time.sleep(2)
        driver.execute_script(jquery_str + dnd_str + "$('#restore_0').simulateDragDrop({ dropTarget: '#{}});".format(L[0]))

        driver.execute_script(jquery_str + dnd_str + "$('#restore_0').simulateDragDrop({ dropTarget: '#{}'});".format(L[1]))
        driver.execute_script(jquery_str + dnd_str + "$('#restore_1').simulateDragDrop({ dropTarget: '#{}'});".format(L[2]))
        driver.execute_script(
            jquery_str + dnd_str + "$('#restore_0').simulateDragDrop({ dropTarget: '#{}'});".format(L[3]))



        driver.find_element_by_xpath('//span[text()="保存"]').click()
        time.sleep(1)
        if int(driver.find_element_by_class_name('ivu-page-total').text[2:-2]) == int(a) + 1:
            self.log_file_out('自定义编码生成器验证成功')
        else:
            self.log_file_out('自定义编码生成器验证失败')

url = 'http://192.168.1.106:8829/rcma.html#/basic/codeGenerator'

Tech().tech_analysis(url)


