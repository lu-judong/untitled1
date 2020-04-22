from LCC_selenium.bin.login import Login
from LCC_selenium.bin.main import Method
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,WebDriverException
from config.log_config import logger
import time
from LCC_selenium.test_sensitivity_analysis.test4_fangfa1 import SensiAnalyClass
from LCC_selenium.test_sensitivity_analysis.test4_fangfa2 import SensiClass
from LCC_selenium.test_sensitivity_analysis.acu_config import *
from LCC_selenium.test_sensitivity_analysis.acu_joggle import *
import requests


class Test_acu:
    def log_file_out(self, msg):
        fo = open(r'.\usecase.txt', mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    def test_acu(self,url,select,type,value1,value2,car,percent):
        # option = webdriver.ChromeOptions()
        # option.add_argument("headless")
        # driver = webdriver.Chrome(chrome_options=option
        #                           ,
        #                           executable_path=r'.\apps\chromedriver.exe'
        #                           )
        driver = webdriver.Chrome()
        status = Login().login(url,'test3','1234',driver)
        if status is True:
            time.sleep(3)
            driver.switch_to.window(driver.window_handles[0])
            self.log_file_out('---------敏度分析---------')
            for i in contents:
                try:
                    #点击整体维修费用分析
                    Method(driver).contains_click(i)
                    self.log_file_out('点击' + i + '成功')
                    time.sleep(2)
                except NoSuchElementException as e:
                    self.log_file_out('点击' + i + '失败')
                    logger.error(e)

            # try:
            #     Method(driver).contains_click(contents3)
            #     self.log_file_out('点击' + contents3 + '成功')
            # except NoSuchElementException as e:
            #     self.log_file_out('点击' + contents3 + '失败')
            #     logger.error(e)

            if requests.get(acu_cost_list.get('acu_train')).status_code == 200:
                time.sleep(1)

                if select == '新建':

                    if type == '时间':
                        try:
                            Method(driver).input('xpath','//*[@id="right_content"]/div/div[1]/div/div[2]/form/div/div[1]/div[1]/div[2]/div[1]/div/div[1]/div/div/div/div/div/input',value1)
                            Method(driver).input('xpath','//*[@id="right_content"]/div/div[1]/div/div[2]/form/div/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/div/div/div/div/input',value2)
                            self.log_file_out('输入时间成功')
                        except NoSuchElementException as e:
                            logger.debug('输入时间失败')
                            self.log_file_out('输入时间失败')
                            logger.error(e)
                    else:
                        try:
                            Method(driver).click('xpath','//*[@id="right_content"]/div/div[1]/div/div[2]/form/div/div[1]/div[1]/div[1]/div/div/div/div/div[3]')
                            time.sleep(2)
                            Method(driver).input('xpath','//*[@id="right_content"]/div/div[1]/div/div[2]/form/div/div[1]/div[1]/div[2]/div[2]/div/div[1]/div/div/div/div[2]/input',value1)
                            Method(driver).input('xpath','//*[@id="right_content"]/div/div[1]/div/div[2]/form/div/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div/div/div[2]/input',value2)
                            self.log_file_out('输入里程成功')
                        except NoSuchElementException as e:
                            self.log_file_out('输入里程失败')
                            logger.error(e)
                    try:
                        Method(driver).click('xpath','//*[@id="right_content"]/div/div[1]/div/div[2]/form/div/div[3]/div/div[1]/div/div/div/div/div[2]')
                        time.sleep(2)
                        for i in car:
                            Method(driver).contains_click(i)
                            car_num = car.get(i)
                            time.sleep(2)
                            for j in car_num:
                                Method(driver).contains_click(j)
                            Method(driver).click('xpath', '/html/body/div[12]/div[2]/div/div/div[3]/button[2]/span')
                            time.sleep(2)
                        Method(driver).click('xpath','/html/body/div[15]/div[2]/div/div/div[3]/button[2]')
                        self.log_file_out('选择车型车号成功')
                    except NoSuchElementException as e:
                        logger.debug('选择车型车号失败')
                        self.log_file_out('选择车型车号失败')
                        logger.error(e)
                    except:
                        logger.debug('选择车型车号失败')
                        self.log_file_out('选择车型车号失败')


                    time.sleep(2)
                    try:
                        # Method(driver).click('xpath','//*[@id="right_content"]/div/div[1]/div/div[2]/form/div/div[1]/div[2]/button[2]/span')
                        Method(driver).contains_click('确认')
                        self.log_file_out('点击确认按钮成功')
                    except NoSuchElementException as e:
                        self.log_file_out('点击确认按钮失败')
                        logger.error(e)
                        logger.debug('点击确认按钮失败')

                    except WebDriverException:
                        print('选车失败')

                    try:
                        if type == '时间':
                            a = SensiAnalyClass().main(car,[value1,value2],percent)
                        else:
                            a = SensiClass().main(car,[str(int(value1)*10000),str(int(value2)*10000)],percent)
                    except:
                        print('录入错误的模型')
                    # 获取文本值

                    time.sleep(1)
                    try:
                        a1 = Method(driver).gain_text('//*[@id="right_content"]/div/div[2]/div/div[2]/div/form'
                                                      '/div[1]/div[1]/div/div/div/input')
                        time.sleep(1)
                        a2 = Method(driver).gain_text('//*[@id="right_content"]/div/div[2]/div/div[2]/div'
                                                      '/form/div[1]/div[2]/div/div/div/input')
                        time.sleep(1)
                        a3 = Method(driver).gain_text('//*[@id="right_content"]/div/div[2]/div/div[2]/div'
                                                      '/form/div[1]/div[3]/div/div/div/input')
                        time.sleep(1)
                        a4 = Method(driver).gain_text('//*[@id="right_content"]/div/div[2]/div/div[2]/div'
                                                      '/form/div[1]/div[4]/div/div/div/input')
                        self.log_file_out('获取第一行数据成功')

                        if float(a1) == a.get('维修总费用'):
                            self.log_file_out('维修总费用一致')
                        else:
                            self.log_file_out('维修总费用不一致')

                        if float(a2) == a.get('总工时费'):
                            self.log_file_out('总工时费一致')
                        else:
                            self.log_file_out('总工时费不一致')

                        if float(a3) == a.get('平均工时费'):
                            self.log_file_out('平均工时费一致')
                        else:
                            self.log_file_out('平均工时费不一致')

                        if float(a4) == a.get('总工时(小时)'):
                            self.log_file_out('总工时(小时)一致')
                        else:
                            self.log_file_out('总工时(小时)不一致')
                    except NoSuchElementException as e:
                        self.log_file_out('获取第一行数据失败')
                        logger.error(e)
                        logger.debug('获取第一行数据失败')



                    try:
                        Method(driver).input('xpath','//*[@id="right_content"]/div/div[2]/div/div[2]/div/form/div[1]/div[5]/div/div/div/div[2]/input',percent)
                        self.log_file_out('输入变动工时费百分比成功')
                    except NoSuchElementException as e:
                        self.log_file_out('输入变动工时费百分比失败')
                        logger.error(e)

                    time.sleep(3)
                    try:
                        # Method(driver).click('xpath','//*[@id="right_content"]/div/div[2]/div/div[2]/div/form/div[2]/div[5]/div/button[1]')
                        Method(driver).contains_click('计算')
                        self.log_file_out('计算成功')
                        time.sleep(2)
                        a5 = Method(driver).gain_text('//*[@id="right_content"]/div/div[2]/div/div[2]/div/form/div[2]/div[1]/div/div/div/input')
                        a6 = Method(driver).gain_text('//*[@id="right_content"]/div/div[2]/div/div[2]/div'
                                                      '/form/div[2]/div[2]/div/div/div/input')
                        time.sleep(1)
                        a7 = Method(driver).gain_text('//*[@id="right_content"]/div/div[2]/div/div[2]/div'
                                                      '/form/div[2]/div[3]/div/div/div/input')
                        time.sleep(1)
                        a8 = Method(driver).gain_text('//*[@id="right_content"]/div/div[2]/div/div[2]/div'
                                                      '/form/div[2]/div[4]/div/div/div/input')
                        # print(a1,a2,a3,a4,a5,a6,a7,a8)


                        if float(a5) == a.get('变动后维修总费'):
                            self.log_file_out('变动后维修总费一致')
                        else:
                            self.log_file_out('变动后维修总费不一致')

                        if float(a6) == a.get('变动后工时费'):
                            self.log_file_out('变动后工时费一致')
                        else:
                            self.log_file_out('变动后工时费不一致')

                        if float(a7) == a.get('变动后平均工时费'):
                            self.log_file_out('变动后平均工时费一致')
                        else:
                            self.log_file_out('变动后平均工时费不一致')

                        if float(a8[:-1]) == float(a.get('变动百分比')[:-1]):
                            self.log_file_out('变动百分比一致')
                        else:
                            self.log_file_out('变动百分比不一致')
                    except NoSuchElementException as e:
                        self.log_file_out('计算失败')
                        logger.error(e)
                else:
                    try:
                        Method(driver).contains_click('模型导入')
                        self.log_file_out('点击模型导入成功')
                    except NoSuchElementException as e:
                        logger.error(e)
                        self.log_file_out('点击模型导入失败')

                    time.sleep(2)
                    try:
                        driver.find_element_by_xpath(
                            "//span[contains(text(),\'{}\')]/../../../td[1]/div/label/span/input".format(type)).click()
                        Method(driver).click('xpath', '/html/body/div[18]/div[2]/div/div/div[3]/div/button[2]')
                        self.log_file_out('导入模型成功')
                    except NoSuchElementException as e:
                        logger.error(e)
                        self.log_file_out('导入模型失败')

                    time.sleep(3)
                    try:
                        # Method(driver).click('xpath','//*[@id="right_content"]/div/div[1]/div/div[2]/form/div/div[1]/div[2]/button[2]/span')
                        Method(driver).contains_click('确认')
                        self.log_file_out('点击确认按钮成功')
                    except NoSuchElementException as e:
                        self.log_file_out('点击确认按钮失败')
                        logger.error(e)
                        logger.debug('点击确认按钮失败')

                    try:
                        Method(driver).input('xpath','//*[@id="right_content"]/div/div[2]/div/div[2]/div/form/div[1]/div[5]/div/div/div/div[2]/input',percent)
                        self.log_file_out('输入变动工时费百分比成功')
                    except NoSuchElementException as e:
                        self.log_file_out('输入变动工时费百分比失败')
                        logger.error(e)

                    try:
                        # Method(driver).click('xpath','//*[@id="right_content"]/div/div[2]/div/div[2]/div/form/div[2]/div[5]/div/button[1]')
                        Method(driver).contains_click('计算')
                        self.log_file_out('计算成功')
                    except NoSuchElementException as e:
                        logger.error(e)
                        self.log_file_out('计算失败')
            elif requests.get(acu_cost_list.get('acu_train')).status_code == 404:
                self.log_file_out('调用接口失败,测试失败')
        else:
            self.log_file_out('登录失败')

url = 'http://192.168.1.25'
car = {'E27':['2651'],
       'E28':['2216']}

Test_acu().test_acu(url,'新建','里程','170','190','1111',30)

