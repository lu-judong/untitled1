from config.config import path_dir,url,username,password,compare_config,path_dir1
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from bin.main import Method
from bin.login import Login
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bin.select_thing import *
import os,datetime
from openpyxl import load_workbook



#技术整改优化效果分析
class Tech:
    def log_file_out(self,msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    def tech_analysis(self,url,username,password,modelName,value,remarks,select,min_model,select_fault,time_sleep):
        # option = webdriver.ChromeOptions()
        # option.add_argument("headless")
        # driver = webdriver.Chrome(chrome_options=option,
        #                                                             executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')
        all_file = os.listdir(os.curdir)

        for j in all_file:
            if os.path.isdir(j):
                pass
            else:
                ext = os.path.splitext(j)[1]
                if ext == '.xlsx':
                    os.remove(j)
                else:
                    pass

        options = webdriver.ChromeOptions()
        prefs = {'profile.default_content_settings.popups': 0,
                 'download.default_directory': '{}\\test_compare'.format(path_dir1),
                 "profile.default_content_setting_values.automatic_downloads": 1}
        options.add_experimental_option('prefs', prefs)


        driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
        Login().login(url, username, password, driver)

        self.log_file_out('-----不同平台对比保存-----')
        time.sleep(2)

        for i in compare_config:
            try:
                Method(driver).contains_xpath('click',i)
                time.sleep(1)
                self.log_file_out('点击'+i+'成功')
            except Exception as e:
                logger.debug(e)
                self.log_file_out('点击' + i + '失败')

        time.sleep(time_sleep)
        try:
            driver.find_element_by_xpath('//a[text()="创建内容"]').click()
            self.log_file_out('点击创建内容按钮成功')
        except:
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

        sum1 = 0

        average = 0
        num = 3
        num1 = 1
        num2 = 0
        try:
            for x in min_model:
                if len(min_model) == 2:
                    pass
                else:
                    for i in range(0, len(min_model) - 2):
                        Method(driver).click('xpath', '//span[text()="新增"]')
                driver.find_elements_by_class_name('ivu-input-default')[num].send_keys(x[0])

                time.sleep(1)
                try:
                    if select == '里程':

                        driver.find_elements_by_class_name('ivu-input-default')[num+1].send_keys(x[1])

                        driver.find_elements_by_class_name('ivu-input-default')[num+2].send_keys(x[2])

                        driver.find_elements_by_class_name('ivu-select-placeholder')[num2].click()
                        time.sleep(0.5)
                        if x[3] == 1:
                            driver.find_elements_by_xpath('//li[text()="180"]')[average].click()
                        elif x[3] == 2:
                            driver.find_elements_by_xpath('//li[text()="260"]')[average].click()

                    elif select == '时间':
                        time.sleep(1)
                        driver.find_elements_by_xpath('//a[text()="起始日期"]')[sum1].click()
                        time.sleep(2)

                        driver.find_elements_by_class_name('ivu-input-default')[num+3].send_keys(x[1])

                        driver.find_elements_by_class_name('ivu-input-default')[num+4].send_keys(x[2])

                        driver.find_elements_by_class_name('ivu-select-placeholder')[num2+1].click()
                        time.sleep(0.5)
                        if x[3] == 1:
                            driver.find_elements_by_xpath('//li[text()="180"]')[average+1].click()
                        elif x[3] == 2:
                            driver.find_elements_by_xpath('//li[text()="260"]')[average+1].click()

                    num += 2
                except NoSuchElementException as e:
                    print(e)

                driver.find_elements_by_xpath('//span[text()="新增"]')[num1].click()
                time.sleep(2)
                status = driver.execute_script('return document.querySelectorAll(".rcma .ivu-card-head .ivu-checkbox-input")[{}].checked'.format(0))
                if status is True:
                    if select_fault == '交集':
                        driver.find_element_by_xpath('//*[contains(text(),\'{}\')]'.format('是否根据车型选择')).click()
                    elif select_fault == '并集':
                        pass
                else:
                    if select_fault == '交集':
                        pass
                    elif select_fault == '并集':
                        driver.find_element_by_xpath('//*[contains(text(),\'{}\')]'.format('是否根据车型选择')).click()

                time.sleep(1)
                car_status = deal_car(driver, x[4], 2)
                if car_status is True:
                    self.log_file_out('选车成功')
                else:
                    self.log_file_out('选车失败')
                    return

                driver.find_element_by_xpath('//*[text()=\'{}\']'.format('下一步')).click()
                time.sleep(5)

                if select_fault == '交集':
                    fault_status = deal_occur1(driver, x[5], x[6])
                else:
                    fault_status = deal_union(driver, x[5])
                if fault_status is True:
                    self.log_file_out('选择部件成功')
                else:
                    self.log_file_out('选择部件失败')

                try:
                    driver.find_element_by_xpath('//span[text()="确定"]').click()
                    logger.debug('bug不存在')
                except NoSuchElementException as e:
                    logger.error('xpath' + '不存在!')
                except:
                    self.log_file_out('模型录入错误')


                average += 2
                sum1 += 1
                num += 11
                num1 += 1
                num2 += 1
        except Exception as e:
            logger.error(e)
            print('录入模型错误')

        try:
            driver.find_element_by_xpath('//span[text()="保存"]').click()
            logger.debug('bug不存在')
        except NoSuchElementException as e:
            logger.error('xpath' + '不存在!')
        except:
            self.log_file_out('模型录入错误')
        time.sleep(2)
        try:
            a = len(driver.find_elements_by_xpath('//a[text()=\'{}\']/../../../td[7]/div/a[3]'.format(modelName)))
            for i in range(0, a):
                try:
                    driver.find_elements_by_xpath('//a[text()=\'{}\']/../../../td[7]/div/a[3]'.format(modelName))[
                        i].click()
                    break
                except:
                    time.sleep(0.5)
                    pass
            self.log_file_out('点击评估按钮成功')
        except WebDriverException:
            self.log_file_out('点击评估按钮失败')
            return

        try:
            a = WebDriverWait(driver, wait_time).until(EC.text_to_be_present_in_element((By.XPATH, "//a[text()=\'{}\']/../../../td[4]".format(modelName)),
                                                 u'计算完成'))
            if a is True:
                logger.debug('评估成功')
                try:
                    b = len(driver.find_elements_by_xpath('//a[text()=\'{}\']/../../../td[7]/div/a[4]'.format(modelName)))
                    for i in range(0, b):
                        try:
                            driver.find_elements_by_xpath(
                                '//a[text()=\'{}\']/../../../td[7]/div/a[4]'.format(modelName))[i].click()
                            break
                        except:
                            time.sleep(0.5)
                            pass
                    self.log_file_out('点击图表按钮成功')
                except WebDriverException:
                    self.log_file_out('点击图表按钮失败')
                    return
        except Exception as e:
            logger.error(e)
            logger.debug('评估失败')
            self.log_file_out('评估失败')



min_model = [['m1', '0', '100',2, {'E27':['2641', '2642', '2643', '2644', '2645', '2646', '2647']},{'高压供电系统': 'all'},'部件'], ['m2', '0', '100', 2,{'E05': ['2091', '2092']},{'高压供电系统': 'all'},'部件']]


# min_model = [['m1', '2017-02-03', '2017-11-02',2,{'E27':['2641', '2642', '2643', '2644', '2645', '2646', '2647']},{'E27':{'高压供电系统': {'受电弓': 'all'}}},{'内装系统':{'厨房设施':{"微波炉柜":{'微波炉':'all'}}}}], ['m2', '2017-02-03', '2017-11-02', 2,{'E05': ['2091', '2092']},{'E05':{'高压供电系统': {'受电弓': 'all'}}},{'内装系统':{'厨房设施':{"微波炉柜":{'微波炉':'all'}}}}]]


time_sleep = 2
wait_time = 10


Tech().tech_analysis(url,username,password,'111',1,'','里程',min_model,'交集',time_sleep)