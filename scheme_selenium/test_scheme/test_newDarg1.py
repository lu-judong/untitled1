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

    # 新建
    def built(self,driver,startDate):
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
    def drag(self,driver):
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

        # 获取所有可以拖拽的元素的id
        L1 = []
        for i in range(0, len(driver.find_elements_by_class_name('tr-plan-wrap'))):
            L1.append(driver.find_elements_by_class_name('tr-plan-wrap')[i].get_attribute('id'))
        # 控制拖拽次数
        for i in range(0, 3):
            L = []

            for i in range(0, len(driver.find_elements_by_class_name('tr-plan-editUnit'))):
                L.append(driver.find_elements_by_class_name('tr-plan-editUnit')[i].get_attribute('id'))
            time.sleep(1)
            driver.execute_script("document.body.style.zoom='0.9'")
            # 随机获取一个可以拖动的元素
            a0 = L[random.randint(0, len(L) - 1)]
            self.log_file_out('--拖动前--')
            time.sleep(1)
            nu_a0 = a0.split('_')[1]
            self.log_file_out(driver.find_elements_by_class_name('timeTitle')[int(nu_a0)].text)
            self.log_file_out(driver.find_elements_by_class_name('total-para')[int(nu_a0)].text)
            time.sleep(1)
            # a0 = 'planUnit_0_2aceeffdf9814cae98b75bd88d58e4ea000'

            # a0 = 'planUnit_8_2aceeffdf9814cae98b75bd88d58e4ea000'
            # 随机获取拖拽去哪的元素的id
            if L.index(a0) == 0:
                nu = L[0].split('_')[1]
                nu1 = L[1].split('_')[1]
                L2 = []
                for i in range(0, int(nu1) + 1):
                    L2.append(i)
                L2.remove(int(nu))
                nu2 = random.randint(0, len(L2) - 1)
                a1 = 'planWrap_{}'.format(L2[nu2])

            elif L.index(a0) == len(L) - 1:
                nu = L[-1].split('_')[1]
                nu1 = L[-2].split('_')[1]
                L2 = []
                for i in range(int(nu1), 12):
                    L2.append(i)
                L2.remove(int(nu))
                nu2 = random.randint(0, len(L2) - 1)
                a1 = 'planWrap_{}'.format(L2[nu2])
            else:
                numm = L.index(a0)

                nu = L[numm - 1].split('_')[1]
                nu1 = L[numm + 1].split('_')[1]
                nu2 = L[numm].split('_')[1]
                L2 = []
                for i in range(int(nu), int(nu1) + 1):
                    L2.append(i)
                L2.remove(int(nu2))
                nu3 = random.randint(0, len(L2) - 1)
                a1 = 'planWrap_{}'.format(L2[nu3])

            nu_a1 = a1.split('_')[1]
            time.sleep(1)
            self.log_file_out(driver.find_elements_by_class_name('timeTitle')[int(nu_a1)].text)
            self.log_file_out(driver.find_elements_by_class_name('total-para')[int(nu_a1)].text)

            driver.execute_script(jquery_str + dnd_str + "$('#%s').simulateDragDrop({ dropTarget: '#%s'});" % (a0, a1))

            time.sleep(1)
            # 点击按钮 需要让文本恢复正常大小
            driver.execute_script("document.body.style.zoom='1'")
            try:
                driver.find_elements_by_xpath('//span[text()="确认"]')[1].click()
                time.sleep(1)
                if len(driver.find_elements_by_class_name('confirm-content')) > 0:
                    driver.find_element_by_xpath('//span[text()="确定"]').click()
                    time.sleep(2)
                else:
                    time.sleep(2)
            except:
                pass
            time.sleep(1)
            # 记录文本要让页面缩小 否则则记录失败
            driver.execute_script("document.body.style.zoom='0.9'")
            self.log_file_out('--拖动后--')
            time.sleep(1)

            self.log_file_out(driver.find_elements_by_class_name('timeTitle')[int(nu_a0)].text)
            self.log_file_out(driver.find_elements_by_class_name('total-para')[int(nu_a0)].text)
            time.sleep(1)

            self.log_file_out(driver.find_elements_by_class_name('timeTitle')[int(nu_a1)].text)
            self.log_file_out(driver.find_elements_by_class_name('total-para')[int(nu_a1)].text)

        # 记录完文本 需要恢复页面的大小到正常大小
        driver.execute_script("document.body.style.zoom='1.0'")

    # 删除
    def delete(self,driver):
        num = random.randint(0, len(driver.find_elements_by_class_name('tr-plan-editUnit')) - 1)

        element = driver.find_elements_by_class_name('tr-plan-editUnit')[num]
        ActionChains(driver).context_click(element).perform()
        time.sleep(1)
        driver.find_element_by_xpath('//li[text()="删除"]').click()


    def main(self, url, username, password, car, startDate):
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
        time.sleep(4)
        driver.find_element_by_xpath('//span[text()="修改"]').click()
        driver.execute_script("document.body.style.zoom='1'")
        time.sleep(2)
        # 随机定义拖，新建，删除的顺序
        select = random.randint(0,2)
        if select == 0:
            self.built(driver,startDate)
            self.drag(driver)
            self.delete(driver)
        elif select == 1:
            self.drag(driver)
            self.delete(driver)
            self.built(driver, startDate)
        else:
            self.delete(driver)
            self.built(driver, startDate)
            self.drag(driver)
        try:
            driver.find_elements_by_class_name('ivu-icon-ios-arrow-back')[5].click()
        except:
            driver.find_element_by_xpath('//span[text()="关闭"]').click()
            time.sleep(1)
            driver.find_elements_by_class_name('ivu-icon-ios-arrow-back')[5].click()
        time.sleep(2)
        driver.find_elements_by_class_name('ivu-icon-ios-arrow-back')[3].click()
        time.sleep(2)
        driver.find_element_by_xpath('//span[text()="退出修改"]').click()
        time.sleep(1)
        driver.find_element_by_xpath('//span[text()="取消"]').click()
        time.sleep(1)

        driver.close()


# url = 'http://192.168.1.25:8081/rcma.html#'
url = 'http://101.201.113.42:8284/rcma.html#/home?user=test4'

Tech().main(url,'test4','1234','17型车','2020-01-01')


