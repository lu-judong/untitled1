from selenium import webdriver

from bin.login import Login

from config.config import path_dir
from bin.select_system import  *



#技术整改优化效果分析
class Tech:
    def log_file_out(self,msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    def tech_analysis(self,url,type,start,end,select,car,fault):
        # option = webdriver.ChromeOptions()
        # option.add_argument("headless")
        # driver = webdriver.Chrome(chrome_options=option,                                                                executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')

        driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
        Login().login(url, 'test', '1234', driver)

        self.log_file_out('----自动FMECA----')
        time.sleep(2)


        try:
            driver.find_element_by_xpath('//span[text()="{}"]'.format('自动FMECA')).click()
            self.log_file_out('点击成功')
            time.sleep(1)
        except Exception as e:
            logger.debug(e)
            self.log_file_out('点击失败')

        driver.find_elements_by_xpath('//span[text()="{}"]'.format('自动FMECA'))[1].click()

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
        driver.find_elements_by_class_name('ivu-input-default')[2].send_keys('1')
        time.sleep(1)
        try:
            if type == '时间':
                driver.find_elements_by_class_name('ivu-input-with-suffix')[0].send_keys(start)
                time.sleep(0.5)
                driver.find_elements_by_class_name('ivu-input-with-suffix')[1].send_keys(end)
            else:
                driver.find_element_by_xpath('//a[text()="里程"]').click()
                time.sleep(0.5)
                driver.find_element_by_xpath('//span[text()="是"]').click()

        except NoSuchElementException as e:
            logger.error(e)
            self.log_file_out('填入里程/时间失败')
        if select == '交集':
            driver.find_element_by_class_name('ivu-checkbox-input').click()
        else:
            pass

        # 选车
        try:
            for x in car:
                driver.find_element_by_xpath(
                    "//span[@class='train zoomIn' and contains(text(),\'{}\')]".format(x)).click()
                car_num = car.get(x)
                time.sleep(2)
                for i in car_num:
                    driver.find_element_by_xpath(
                        "//span[@class='ivu-tag-text' and contains(text(),\'{}\')]".format(i)).click()
                    time.sleep(1)
                driver.find_elements_by_xpath('//span[text()="确认"]')[0].click()
                time.sleep(2)
            self.log_file_out('选车成功')
        except NoSuchElementException as e:
            logger.debug('选车失败')
            logger.error(e)
            self.log_file_out('选车失败')

        driver.find_elements_by_xpath('//span[text()="下一步"]')[0].click()
        time.sleep(2)
        if select == '交集':
            fault_status = deal_occur(driver,fault)
        else:
            fault_status = deal_union(driver,fault)
        if fault_status is True:
            self.log_file_out('选择部件成功')
        else:
            self.log_file_out('选择部件失败')

        time.sleep(2)

        driver.find_element_by_xpath('//span[text()="保存"]').click()
        time.sleep(1)
        if int(driver.find_element_by_class_name('ivu-page-total').text[2:-2]) == int(a) + 1:
            self.log_file_out('自动FMECA验证成功')
        else:
            self.log_file_out('自动FMECA验证失败')

url = 'http://192.168.1.25:8081'

car = {'E27':['2651']}
fault = {'转向架':{'一系悬挂':{'一系垂向减振器':'all'},'轴箱弹簧':'all'}}

Tech().tech_analysis(url,'时间','2017-02-03','2017-08-02','交集',car,fault)