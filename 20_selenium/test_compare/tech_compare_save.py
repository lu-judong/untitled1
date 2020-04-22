from config.config import path_dir,url,username,password,compare_config
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,WebDriverException
from config.log_config import logger
import time
from bin.main import Method
from bin.login import Login
from bin.select_fault_occur import deal_fault
from bin.select_car import deal_car
from bin.select_fault_union import deal_fault_union
from bin.select_fault_union2 import deal_fault_union_2
from bin.select_butongfuji import deal_different
from bin.select_fault_butongfuji_occur import deal_different_occur
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests



#技术整改优化效果分析
class Tech:
    def log_file_out(self,msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    def tech_analysis(self,url,username,password,modelName,value,select,min_model,select_fault,time_sleep):
        # option = webdriver.ChromeOptions()
        # option.add_argument("headless")
        # driver = webdriver.Chrome(chrome_options=option,                                                                executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')
        driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
        Login().login(url, username, password, driver)

        self.log_file_out('-----不同平台对比保存-----')

        for i in compare_config:
            try:
                Method(driver).contains_xpath('click',i)
                self.log_file_out('点击'+i+'成功')
            except Exception as e:
                logger.debug(e)
                self.log_file_out('点击' + i + '失败')

        time.sleep(time_sleep)
        try:
            Method(driver).switch_out()
            Method(driver).switch_iframe(
                driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/moreModel')]"))
            Method(driver).click('id', 'add')
            time.sleep(time_sleep)
        except NoSuchElementException as e:
            self.log_file_out('点击不保存计算按钮失败,获取不到相应的xpath')

        Method(driver).switch_out()

        Method(driver).switch_iframe(
            driver.find_element_by_xpath(
                "//iframe[contains(@src,'/darams/a/mould/moreModel/form?modelType=MORE_MODEL')]"))

        try:
            Method(driver).input('id','modelName',modelName)
            Method(driver).select_down_list('id', 'modelObject', value)
            self.log_file_out('模型基本信息录入成功')
        except NoSuchElementException as e:
            self.log_file_out('模型基本信息录入失败')

        sum1 = 1
        try:
            for x in min_model:
                if len(min_model) == 2:
                    pass
                else:
                    for i in range(0, len(min_model) - 2):
                        Method(driver).click('xpath', '//*[@id="inputForm"]/a[1]')
                Method(driver).input('id', 'subSetName{}_inp'.format(sum1), x[0])

                time.sleep(2)
                try:
                    if select == '里程':
                        Method(driver).click('xpath', '//*[@id="subset-{}-left-tab-1"]/a'.format(sum1))
                        time.sleep(2)
                        Method(driver).input('id', 'confMileageList{}_startMileage'.format(sum1), x[1])
                        Method(driver).input('id', 'confMileageList{}_endMileage'.format(sum1), x[2])
                        Method(driver).select_down_list('id', 'confMileageList{}_averageSpeedSelect'.format(sum1), x[3])

                    elif select == '时间':
                        Method(driver).click('xpath', '//*[@id="subSet{}"]/li[2]/div/ul/li[2]/a'.format(sum1))
                        time.sleep(2)
                        Method(driver).click('xpath', '//*[@id="subset-{}-left-tab-2"]/a'.format(sum1))
                        Method(driver).input('name', 'confDateList[{}].startDate'.format(sum1), x[1])
                        Method(driver).input('name', 'confDateList[{}].endDate'.format(sum1), x[2])
                        Method(driver).select_down_list('id', 'confDateList{}_averageSpeedSelect'.format(sum1), x[3])
                except NoSuchElementException as e:
                    print('新增里程或时间失败')

                # try:
                #     Method(driver).click('xpath','//*[@id="subSet{}"]/li[2]/div/ul/li[4]/a'.format(sum1))
                #     time.sleep(1)
                #     Method(driver).input('id','confLateHoursList{}_lateHoursFrom'.format(sum1),'0')
                #     Method(driver).input('id','confLateHoursList{}_lateHoursTo'.format(sum1),'3')
                #     time.sleep(2)
                # except:
                #     self.log_file_out('新增晚点时长失败')

                Method(driver).click('xpath', '//*[@id="subset-{}-right-tab-1"]/a'.format(sum1))

                try:
                    Method(driver).switch_out()
                    b = Method(driver).get_attr('css', "[class='layui-layer layui-layer-iframe my-skin']", 'times')
                    Method(driver).switch_iframe('layui-layer-iframe' + b)
                except:
                    print('请录入评估对象')
                    return

                Method(driver).click('xpath',
                                     '//*[@id="train-group-body"]/table/tbody/tr/td[3]/div/div[1]/div[1]/button[5]')

                time.sleep(5)
                if select_fault == '交集':
                    Method(driver).click('id', 'partType')
                elif select_fault == '并集':
                    time.sleep(1)


                driver.find_element_by_xpath('//a[text()="车型"]').click()
                time.sleep(1)

                a = deal_car(driver, x[4])
                if a is True:
                    self.log_file_out('选车成功')
                else:
                    self.log_file_out('选车失败')


                Method(driver).switch_out()
                c = Method(driver).get_attr('css', "[class='layui-layer layui-layer-iframe my-skin']", 'times')
                Method(driver).switch_iframe('layui-layer-iframe' + c)
                time.sleep(30)

                # 故障模式选择页面
                if select_fault == '交集':
                    fault_status = deal_fault(driver, x[5])
                    if fault_status is True:
                        self.log_file_out('故障模式选择成功')
                    else:
                        self.log_file_out('故障模式选择失败')

                elif select_fault == '并集':
                    if value == 1:
                        fault_status = deal_fault_union(driver, x[5])
                        if fault_status is True:
                            self.log_file_out('故障模式选择成功')
                        else:
                            self.log_file_out('故障模式选择失败')
                    elif value == 2:
                        fault_status = deal_fault_union_2(driver, x[5])
                        if fault_status is True:
                            self.log_file_out('故障模式选择成功')
                        else:
                            self.log_file_out('故障模式选择失败')

                        # Method(driver).click('id', 'differPatternSelect')

                    # time.sleep(8)
                    #
                    # Method(driver).switch_out()
                    # d = Method(driver).get_attr('css', "[class='layui-layer layui-layer-iframe my-skin']", 'times')
                    # Method(driver).switch_iframe('layui-layer-iframe' + d)
                    #
                    # fault_status1 = deal_different(driver, x[6])
                    # if fault_status1 is True:
                    #     self.log_file_out('不同父级选择成功')
                    # else:
                    #     self.log_file_out('不同父级选择失败')


                try:
                    driver.execute_script('top.$(".layui-layer-btn2")[0].click()')
                except NoSuchElementException as e:
                    logger.error('xpath' + '不存在!')
                    self.log_file_out('点击确定按钮失败')
                except:
                    print('请录入完整的模型')
                    return

                Method(driver).switch_out()
                Method(driver).switch_iframe(
                    driver.find_element_by_xpath(
                        "//iframe[contains(@src,'/darams/a/mould/moreModel/form?modelType=MORE_MODEL')]"))

                sum1 += 1
        except:
            print('录入模型错误')


        try:
            time.sleep(time_sleep)
            js1 = 'top.$(".layui-layer-btn0")[0].click()'
            driver.execute_script(js1)
        except NoSuchElementException as e:
            logger.error('xpath' + '不存在!')
            self.log_file_out('保存失败')


        time.sleep(2)
        Method(driver).switch_out()
        Method(driver).switch_iframe(
            driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/moreModel')]"))

        try:
            driver.find_element_by_xpath(
                "//a[contains(text(),\'{}\')]/../../td[8]/a[3]".format(modelName)).click()
            self.log_file_out('点击评估按钮成功')
        except WebDriverException:
            self.log_file_out('点击评估按钮失败')
            return

        time.sleep(10)

        try:
            a = WebDriverWait(driver, wait_time).until(
                EC.text_to_be_present_in_element(
                    (By.XPATH, "//a[contains(text(),\'{}\')]/../../td[5]".format(modelName)),
                    u'计算完成'))
            if a is True:
                logger.debug('评估成功')
                self.log_file_out('评估成功')

                driver.find_element_by_xpath(
                    "//a[contains(text(),\'{}\')]/../../td[8]/a[4]".format(modelName)).click()

                # 查看点击图表出来的页面是否存在
                Method(driver).switch_out()
                c = Method(driver).get_attr('css', "[class='layui-layer layui-layer-iframe']", 'times')
                try:
                    next_url = Method(driver).get_attr('id', 'layui-layer-iframe' + c, 'src')
                    status = requests.get(next_url).status_code
                    if status == 200:
                        logger.debug('图表页面获取成功')
                        self.log_file_out('图表页面获取成功')
                        driver.close()
                    elif status == 404:
                        logger.error('{}请求404'.format(next_url))
                        self.log_file_out('图表页面获取失败')
                        driver.close()
                except Exception as e:
                    logger.error(e)
                    driver.close()
        except Exception as e:
            logger.debug('评估失败')
            self.log_file_out('评估失败')

min_model = [['m1', '0', '100',2, {'E27':['2641', '2642', '2643', '2644', '2645', '2646', '2647']},{'高压供电系统': 'all'},{'内装系统':{'厨房设施':{"微波炉柜":{'微波炉':'all'}}}}], ['m2', '100', '200', 2,{'E05': ['2091', '2092']},{'高压供电系统': 'all'},{'内装系统':{'厨房设施':{"微波炉柜":{'微波炉':'all'}}}}]]


# min_model = [['m1', '2017-02-03', '2017-11-02',2,{'E27':['2641', '2642', '2643', '2644', '2645', '2646', '2647']},{'E27':{'高压供电系统': {'受电弓': 'all'}}},{'内装系统':{'厨房设施':{"微波炉柜":{'微波炉':'all'}}}}], ['m2', '2017-02-03', '2017-11-02', 2,{'E05': ['2091', '2092']},{'E05':{'高压供电系统': {'受电弓': 'all'}}},{'内装系统':{'厨房设施':{"微波炉柜":{'微波炉':'all'}}}}]]


time_sleep = 2
wait_time = 10


Tech().tech_analysis(url,username,password,'111',1,'里程',min_model,'交集',time_sleep)