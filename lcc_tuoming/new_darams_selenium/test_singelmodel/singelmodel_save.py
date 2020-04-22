from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from bin.main import Method
from bin.login import Login
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from config.config import path_dir,singelmodel_config,username,password,url
from bin.select_thing import *

class singelmodel:
    def log_file_out(self,msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    # 单一模型
    def tech(self,url,username,password,modelName,value,remarks,select,start,end,average,car,fault,select_fault,fault1,time_sleep,wait_time):

        driver = webdriver.Chrome()
        Login().login(url,username, password, driver)
        time.sleep(2)

        self.log_file_out('-----单一模型指标分析-----')

        for i in singelmodel_config:
            try:
                Method(driver).contains_xpath('click',i)
                time.sleep(1)
                self.log_file_out('点击'+i+'成功')
            except Exception as e:
                logger.debug(e)
                self.log_file_out('点击' + i + '失败')
        time.sleep(2)

        # 点击新建得到弹框
        try:
            Method(driver).click('xpath', '//*[text()=\'{}\']'.format('创建内容'))
            time.sleep(time_sleep)
        except NoSuchElementException as e:
            logger.error(e)
            self.log_file_out('点击创建内容按钮失败')

        # 对新增指标页面进行操作
        try:
            driver.find_elements_by_class_name('ivu-input-default')[1].send_keys(modelName)
            time.sleep(1)
            Method(driver).click('class', 'ivu-select-placeholder')
            if value == 1:
                driver.find_element_by_xpath('//li[text()="评估系统、部件"]').click()
            elif value == 2:
                driver.find_element_by_xpath('//li[text()="故障模式"]').click()

            if remarks == '':
                time.sleep(1)
            else:
                driver.find_elements_by_class_name('ivu-input-default')[2].send_keys(remarks)
            self.log_file_out('模型录入成功')
        except Exception as e:
            logger.debug(e)
            self.log_file_out('模型录入失败')

        # 优化前里程
        if select == '里程':
            try:
                driver.find_elements_by_class_name('ivu-input-default')[3].send_keys(start)
                time.sleep(0.5)
                driver.find_elements_by_class_name('ivu-input-default')[4].send_keys(end)
                time.sleep(0.5)
                driver.find_elements_by_class_name('ivu-select-placeholder')[0].click()
                time.sleep(0.5)
                if average == 1:
                    driver.find_element_by_xpath('//li[text()="180"]').click()
                elif average == 2:
                    driver.find_element_by_xpath('//li[text()="260"]').click()
                self.log_file_out('里程录入成功')
            except NoSuchElementException as e:
                self.log_file_out('里程录入失败')
        elif select == '时间':
            try:
                Method(driver).click('xpath', '//a[text()="起始日期"]')
                time.sleep(1)
                driver.find_elements_by_class_name('ivu-input-default')[5].send_keys(start)
                time.sleep(0.5)
                driver.find_elements_by_class_name('ivu-input-default')[6].send_keys(start)
                time.sleep(0.5)
                driver.find_elements_by_class_name('ivu-select-placeholder')[2].click()
                time.sleep(0.5)
                if average == 1:
                    driver.find_elements_by_xpath('//li[text()="180"]')[1].click()
                elif average == 2:
                    driver.find_elements_by_xpath('//li[text()="260"]')[1].click()
                self.log_file_out('添加时间成功')
            except NoSuchElementException as e:
                self.log_file_out('添加时间失败')

        time.sleep(2)

        # 车型 车号新增页面

        if select_fault == '交集':
            driver.find_element_by_xpath('//*[contains(text(),\'{}\')]'.format('是否根据车型选择')).click()
        elif select_fault == '并集':
            pass

        time.sleep(1)
        car_status = deal_car(driver, car, 6)
        if car_status is True:
            self.log_file_out('选车成功')
        else:
            self.log_file_out('选车失败')
            return
        # 故障模式选择页面
        time.sleep(2)

        driver.find_element_by_xpath('//*[text()=\'{}\']'.format('下一步')).click()
        time.sleep(10)

        if select_fault == '交集':
            fault_status = deal_occur(driver, fault, fault1)
        else:
            fault_status = deal_union(driver, fault)
        if fault_status is True:
            self.log_file_out('选择部件成功')
        else:
            self.log_file_out('选择部件失败')

        try:
            driver.find_element_by_xpath('//span[text()="保存"]').click()
            logger.debug('bug不存在')
        except NoSuchElementException as e:
            logger.error('xpath' + '不存在!')
        except:
            self.log_file_out('模型录入错误')

        try:
            a = len(driver.find_elements_by_xpath('//a[text()=\'{}\']/../../../td[7]/div/a[3]'.format(modelName)))
            for i in range(0, a):
                try:
                    driver.find_elements_by_xpath('//a[text()=\'{}\']/../../../td[7]/div/a[3]'.format(modelName))[
                        i].click()
                    break
                except:
                    pass
                    i += 1
            self.log_file_out('点击评估按钮成功')
        except WebDriverException:
            self.log_file_out('点击评估按钮失败')
            return

        try:
            a = WebDriverWait(driver, wait_time).until(
                EC.text_to_be_present_in_element((By.XPATH, "//a[text()=\'{}\']/../../../td[4]".format(modelName)),
                                                 u'计算完成'))
            if a is True:
                logger.debug('评估成功')
                try:
                    b = len(
                        driver.find_elements_by_xpath('//a[text()=\'{}\']/../../../td[7]/div/a[4]'.format(modelName)))
                    for i in range(0, b):
                        try:
                            driver.find_elements_by_xpath(
                                '//a[text()=\'{}\']/../../../td[7]/div/a[4]'.format(modelName))[i].click()
                            break
                        except:
                            pass
                            i += 1
                    self.log_file_out('点击图表按钮成功')
                except WebDriverException:
                    self.log_file_out('点击图表按钮失败')
                    return
        except Exception as e:
            logger.debug('评估失败')
            self.log_file_out('评估失败')


car = {'E27':['2641', '2642', '2643', '2644', '2645', '2646', '2647']}

fault_pattern = {'高压供电系统': {'高压电缆、连接器及跳线':'all'}}

# fault_pattern = {'高压供电系统': 'all'}

# fault1 = {'内装系统':{'厨房设施':{"微波炉柜":{'微波炉':'all'}}}}

fault_object = {'E27':
{'高压供电系统': {'高压电缆、连接器及跳线':{'电缆终端':'all'}}}
                }

# fault_object = {'E27':
#                     {'高压供电系统':{'高压电缆、连接器及跳线':{'电缆终端':"all",'跳线':"all",'电缆':'all'}}}
#                 }

time_sleep = 2
wait_time = 10

singelmodel().tech(url,username,password,'1205测试',1,'','里程','0','100',2,car,fault_pattern,'交集','部件',time_sleep,wait_time)