from selenium import webdriver
from bin.login import Login
from bin.main import Method
from test_EDS.EDS_config import *
from config.config import path_dir
from test_EDS.select_system import *



class EDS:
    def log_file_out(self, msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    def tech(self,url,username,password,name,system,car,value1,value2,fault,list,date,list1):
        # option = webdriver.ChromeOptions()
        # option.add_argument("headless")
        # driver = webdriver.Chrome(chrome_options=option,
        #                           executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))

        driver = webdriver.Chrome()
        driver.maximize_window()
        Login().login(url, username, password, driver)

        driver.maximize_window()
        time.sleep(2)
        self.log_file_out('-----技术变更及EDS反馈系统-----')
        for i in contents:
            try:
                Method(driver).contains_xpath('click', i)
                time.sleep(1)
                self.log_file_out('点击' + i + '成功')
            except Exception as e:
                logger.debug(e)
                self.log_file_out('点击' + i + '失败')

        time.sleep(2)
        try:
            Method(driver).switch_out()
            Method(driver).switch_iframe(
                driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/eds/main')]"))
            time.sleep(2)
        except NoSuchElementException as e:
            logger.error(e)
            self.log_file_out('源头问题功能打开失败')

        try:
            Method(driver).contains_click('创建内容')
            Method(driver).input('xpath',"//input[@placeholder='请输入整治项目']",name)
            self.log_file_out('点击创建内容成功')
        except NoSuchElementException as e:
            logger.error(e)
            self.log_file_out('点击创建内容失败')

        # driver.find_elements_by_class_name('ivu-select-placeholder')[0].click()
        # Method(driver).contains_click(department)
        Method(driver).input('xpath', "//input[@placeholder='请输入申请单号']", '1')
        # driver.find_elements_by_class_name('ivu-select-placeholder')[0].click()
        # driver.find_element_by_xpath('//li[text()=\'{}\']'.format(fault_atr)).click()
        time.sleep(0.5)
        driver.find_elements_by_class_name("ivu-input-group-append")[1].click()
        time.sleep(1)
        system_status = deal_system(driver,system)
        if system_status is True:
            self.log_file_out('系统选择成功')
        else:
            self.log_file_out('系统选择失败')
            return
        time.sleep(1)
        # 点击确定按钮
        # driver.find_elements_by_xpath('//span[text()="确认"]')[2].click()
        driver.find_elements_by_class_name('ivu-btn-info')[2].click()
        time.sleep(1)
        driver.find_elements_by_class_name("ivu-input-group-append")[2].click()
        time.sleep(1)
        if value1 == '交集':
            driver.find_element_by_xpath('//*[text()=\'{}\']/./span'.format(' 是否根据车型选择')).click()
        else:
            pass
        time.sleep(1)
        if value2 == '部件':
            pass
        else:
            driver.find_elements_by_class_name('ivu-radio-input')[1].click()

        time.sleep(1)
        car_status = deal_car(driver,car,2)
        if car_status is True:
            self.log_file_out('选车成功')
        else:
            self.log_file_out('选车失败')
            return
        # driver.find_element_by_xpath('//span[text()="下一步"]').click()
        driver.find_elements_by_class_name('ivu-btn-info')[2].click()
        time.sleep(5)

        if value1 == '交集':
            fault_status = deal_occur(driver,fault,value2)
        else:
            fault_status = deal_union(driver,fault)
        if fault_status is True:
            self.log_file_out('选择部件成功')
        else:
            self.log_file_out('选择部件失败')
        # driver.find_elements_by_xpath('//*[text()=\'{}\']'.format('确认'))[2].click()
        driver.find_elements_by_class_name('ivu-btn-info')[-1].click()
        time.sleep(1)
        for i in range(0,len(list)):
            driver.find_elements_by_class_name('ivu-select-placeholder')[0].click()
            time.sleep(0.5)
            if list[i] == '无':
                driver.find_elements_by_xpath('//li[text()=\'{}\']'.format('无'))[i-1].click()
            else:
                driver.find_element_by_xpath('//li[text()=\'{}\']'.format(list[i])).click()
            time.sleep(1)
        Method(driver).input('xpath', "//input[@placeholder='请输入设计值']", '1')
        time.sleep(1)
        Method(driver).input('xpath', "//input[@placeholder='请输入预警值']", '0.5')
        time.sleep(1)
        driver.find_element_by_class_name('ivu-input-with-suffix').send_keys(date)
        for j in range(0,len(list1)):
            driver.find_elements_by_xpath('//textarea[@class="ivu-input"]')[j].send_keys(list1[j])
            time.sleep(0.5)
        # 点击保存
        # driver.find_element_by_xpath('//span[text()=\'{}\']'.format('保存')).click()
        driver.find_elements_by_class_name('ivu-btn-info')[1].click()
        time.sleep(1)
        driver.find_elements_by_xpath('//a[text()=\'{}\']/../../../td'.format(name))[-1].click()


# url = 'http://192.168.1.20:8083/darams/a?login'
url = 'http://192.168.1.115:8080/darams/a?login'
car = {'E27':'all'}

system = {'1000   车体':{'1100   车体骨架结构':{'1110   司机室框架及前端吸能装置':'all'}}}

# fault = {'E27.350公里统型':{'转向架':{'一系悬挂':'all'},'内装系统':'all','门窗系统':{'侧拉门':{'门体':'all'}}}}
fault = {'转向架':{'一系悬挂':{'一系垂向减振器':'all'},'轴箱弹簧':'all'}}
list = ['车体开发部','无','软件类变更','I类','运用修','是','无','无']

list1 = ['无','无','无']
EDS().tech(url,'admin','admin','0925',system,car,'交集','模式',fault,list,'2017-07-02',list1)