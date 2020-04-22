from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from bin.select_fault_union2 import deal_fault_union_2
from config.log_config import logger
import time
from bin.main import Method
from bin.login import Login
from new_selenium.tech_compare.compare_config import *
from config.config import path_dir
from bin.select_fault_occur import deal_fault
from bin.select_car import deal_car
from bin.select_fault_union import deal_fault_union
from bin.select_butongfuji import deal_different
from bin.select_fault_butongfuji_occur import deal_different_occur

#技术整改优化效果分析
class Tech:
    def log_file_out(self,msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    def tech_analysis(self,url,username,password,value,select,min_model,select_fault,time_sleep):
        # option = webdriver.ChromeOptions()
        # option.add_argument("headless")
        # driver = webdriver.Chrome(chrome_options=option,                                                                executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')

        driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
        Login().login(url, username, password, driver)

        self.log_file_out('-----不同平台对比-----')

        for i in contents:
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
            Method(driver).click('id', 'calculate')
            time.sleep(time_sleep)
        except NoSuchElementException as e:
            self.log_file_out('点击不保存计算按钮失败,获取不到相应的xpath')

        Method(driver).switch_out()

        Method(driver).switch_iframe(driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/moreModel/form2?modelType=MORE_MODEL')]"))

        try:
            Method(driver).select_down_list('id', 'modelObject', value)
        except NoSuchElementException as e:
            print('模型录入错误 找不到对应的xpath')
        except:
            print('模型录入数据出错')

        sum1 = 1
        try:
            for x in min_model:
                if len(min_model) == 2:
                    pass
                else:
                    for i in range(0,len(min_model)-2):
                        Method(driver).click('xpath','//*[@id="inputForm"]/a[1]')
                Method(driver).input('id', 'subSetName{}_inp'.format(sum1), x[0])

                try:
                    if select == '里程':
                        Method(driver).click('xpath','//*[@id="subset-{}-left-tab-1"]/a'.format(sum1))
                        Method(driver).input('id','confMileageList{}_startMileage'.format(sum1),x[1])
                        Method(driver).input('id','confMileageList{}_endMileage'.format(sum1),x[2])
                        Method(driver).select_down_list('id','confMileageList{}_averageSpeedSelect'.format(sum1),x[3])

                    elif select == '时间':
                        Method(driver).click('xpath','//*[@id="subSet{}"]/li[2]/div/ul/li[2]/a'.format(sum1))
                        time.sleep(1)
                        Method(driver).click('xpath','//*[@id="subset-{}-left-tab-2"]/a'.format(sum1))
                        time.sleep(1)
                        Method(driver).input('name','confDateList[{}].startDate'.format(sum1),x[1])
                        Method(driver).input('name', 'confDateList[{}].endDate'.format(sum1), x[2])
                        Method(driver).select_down_list('id', 'confDateList{}_averageSpeedSelect'.format(sum1), x[3])
                except NoSuchElementException as e:
                    print('新增里程或时间失败')


                Method(driver).click('xpath','//*[@id="subset-{}-right-tab-1"]/a'.format(sum1))

                try:
                    Method(driver).switch_out()
                    b = Method(driver).get_attr('css', "[class='layui-layer layui-layer-iframe my-skin']", 'times')
                    Method(driver).switch_iframe('layui-layer-iframe' + b)
                except:
                    print('请录入评估对象')
                    return

                Method(driver).click('xpath','//*[@id="train-group-body"]/table/tbody/tr/td[3]/div/div[1]/div[1]/button[5]')

                time.sleep(5)

                # 车型 车号新增页面
                if select_fault == '交集':
                    Method(driver).click('id', 'partType')
                elif select_fault == '并集':
                    time.sleep(1)

                a = deal_car(driver, x[4])
                if a is True:
                    self.log_file_out('选车成功')
                else:
                    self.log_file_out('选车失败')

                Method(driver).switch_out()
                c = Method(driver).get_attr('css', "[class='layui-layer layui-layer-iframe my-skin']", 'times')
                Method(driver).switch_iframe('layui-layer-iframe' + c)
                time.sleep(8)
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
                        #
                        #     Method(driver).click('id', 'differPatternSelect')
                        #
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
                    driver.execute_script('top.$(".layui-layer-btn2")[1].click()')
                except NoSuchElementException as e:
                    logger.error('xpath' + '不存在!')
                    self.log_file_out('点击确定按钮失败')
                except:
                    print('请录入完整的模型')
                    return

                Method(driver).switch_out()
                Method(driver).switch_iframe(driver.find_element_by_xpath(
                    "//iframe[contains(@src,'/darams/a/mould/moreModel/form2?modelType=MORE_MODEL')]"))
                sum1 += 1
        except:
            print('录入模型错误')

        try:
            Method(driver).switch_out()

            Method(driver).click('class', 'layui-layer-btn0')
        except NoSuchElementException as e:
            logger.error('xpath' + '不存在!')
            self.log_file_out('点击计算按钮失败')
        except:
            print('请录入正确的模型')
            return

        time.sleep(10)

        try:
            Method(driver).switch_out()
            Method(driver).switch_iframe(driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/moreModel/charts?modelId=moremodelcalculate')]"))
            time.sleep(time_sleep)
            logger.debug('图表页面获取成功')
            self.log_file_out('图表页面获取成功')
        except NoSuchElementException as e:
            self.log_file_out('图表页面获取失败')
        except:
            print('图表页面获取失败')




# min_model = [['m1', '0', '100',2, {'E27':['2641', '2642', '2643', '2644', '2645', '2646', '2647']},{'高压供电系统': 'all'},{'内装系统':{'厨房设施':{"微波炉柜":{'微波炉':'all'}}}}], ['m2', '100', '200', 2,{'E27':['2641', '2642', '2643', '2644', '2645', '2646', '2647']},{'高压供电系统': 'all'},{'内装系统':{'厨房设施':{"微波炉柜":{'微波炉':'all'}}}}]]
#
# min_model = [['m1', '0', '100',2,{'E27':['2641', '2642', '2643', '2644', '2645', '2646', '2647']},{'E27':
# {'高压供电系统': {'受电弓': 'all'}}
#                 },{'内装系统':{'厨房设施':{"微波炉柜":{'微波炉':'all'}}}}], ['m2', '100', '200', 2,{'E05': ['2091', '2092']},{'E05':{'高压供电系统': {'受电弓': 'all'}}},{'内装系统':{'厨房设施':{"微波炉柜":{'微波炉':'all'}}}}]]

# min_model = [["m1", "0", "100","2", {"E27":["2641", "2642", "2643", "2644", "2645", "2646", "2647"]},{"高压供电系统": "all"}], ["m2", "100", "200", "2",{"E27":["2641", "2642", "2643", "2644", "2645", "2646", "2647"]},{"高压供电系统": "all"}]]
#
# min_model = [['m1', '0', '100',2, {'E27':['2641', '2642', '2643', '2644', '2645', '2646', '2647']},{'高压供电系统': 'all'},{'内装系统':{'厨房设施':{"微波炉柜":{'微波炉':'all'}}}}], ['m2', '100', '200', 2,{'E05': ['2091', '2092']},{'高压供电系统': 'all'},{'内装系统':{'厨房设施':{"微波炉柜":{'微波炉':'all'}}}}]]


min_model = [['m1', '2017-02-03', '2017-11-02',2,{'E27':['2641', '2642', '2643', '2644', '2645', '2646', '2647']},{'E27':{'高压供电系统': {'受电弓': 'all'}}},{'内装系统':{'厨房设施':{"微波炉柜":{'微波炉':'all'}}}}], ['m2', '2017-02-03', '2017-11-02', 2,{'E05': ['2091', '2092']},{'E05':{'高压供电系统': {'受电弓': 'all'}}},{'内装系统':{'厨房设施':{"微波炉柜":{'微波炉':'all'}}}}]]

url = 'http://192.168.1.115:8080/darams/a/login'


time_sleep = 2
wait_time = 10


Tech().tech_analysis(url,'admin','admin',2,'时间',min_model,'并集',time_sleep)