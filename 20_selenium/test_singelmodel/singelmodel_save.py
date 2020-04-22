from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,WebDriverException
import requests

from bin.select_fault_union2 import deal_fault_union_2
from config.log_config import logger
import time
from bin.main import Method
from bin.login import Login
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bin.select_fault_occur import deal_fault
from bin.select_car import deal_car
from bin.select_fault_union import deal_fault_union
from bin.select_butongfuji import deal_different
from bin.select_fault_butongfuji_occur import deal_different_occur
from config.config import path_dir,url,username,password,singelmodel_config


class singelmodel:
    def log_file_out(self,msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    # 单一模型
    def tech(self,url,username,password,modelName,value,remarks,select,start,end,average,car,fault,select_fault,fault1,time_sleep,wait_time):

        driver = webdriver.Chrome()
        Login().login(url,username, password, driver)

        self.log_file_out('-----单一模型指标分析-----')

        for i in singelmodel_config:
            try:
                Method(driver).contains_xpath('click',i)
                time.sleep(1)
                self.log_file_out('点击'+i+'成功')
            except Exception as e:
                logger.debug(e)
                self.log_file_out('点击' + i + '失败')

        # 点击新建得到弹框
        Method(driver).switch_out()
        Method(driver).switch_iframe(
            driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/singleModel')]"))
        Method(driver).click('id', 'add')
        time.sleep(2)

        # 切换到新的模型列表
        Method(driver).switch_out()
        a = Method(driver).get_attr('css', "[class='layui-layer layui-layer-iframe']", 'times')
        Method(driver).switch_iframe('layui-layer-iframe' + a)

        #对新增指标页面进行操作
        try:
            Method(driver).input('id', 'modelName', modelName)
            Method(driver).select_down_list('id', 'modelObject', value)
            if remarks is '':
                pass
            else:
                Method(driver).input('id', 'remarks', remarks)
            self.log_file_out('模型录入成功')
        except Exception as e:
            logger.debug(e)
            self.log_file_out('模型录入失败')

        # 优化前里程
        if select == '里程':
            try:
                Method(driver).click('xpath','//*[@id="left-tab-1"]/a')
                Method(driver).input('id','confMileageList0_startMileage',start)
                Method(driver).input('id','confMileageList0_endMileage',end)
                Method(driver).select_down_list('id', 'confMileageList0_averageSpeedSelect', average)
                self.log_file_out('里程录入成功')
            except NoSuchElementException as e:
                self.log_file_out('里程录入失败')
        elif select == '时间':
            try:
                Method(driver).click('xpath','//*[@id="inputForm"]/div[2]/ul/li[2]/a')
                time.sleep(1)
                Method(driver).click('xpath','//*[@id="left-tab-2"]/a')
                time.sleep(1)
                Method(driver).input('name','confDateList[0].startDate',start)
                Method(driver).input('name','confDateList[0].endDate',end)
                Method(driver).select_down_list('id', 'confDateList0_averageSpeedSelect', average)
                self.log_file_out('添加时间成功')
            except NoSuchElementException as e:
                self.log_file_out('添加时间失败')

        time.sleep(2)
        # 晚点时长
        # try:
        #     Method(driver).click('xpath', '//*[@id="inputForm"]/div[2]/ul/li[4]/a')
        #     time.sleep(1)
        #     Method(driver).input('id', 'confLateHoursList0_lateHoursFrom','0')
        #     Method(driver).input('id', 'confLateHoursList0_lateHoursTo', '3')
        #     # 车型-车号新增
        Method(driver).click('id', 'addModel')
        #     time.sleep(1)
        #     self.log_file_out('晚点时长输入成功')
        # except NoSuchElementException as e:
        #     logger.error('xpath' + '不存在！')
        #     self.log_file_out('晚点时长输入失败')

        # 从新进入新打开的iframe 先去最外层 在进入打开的iframe
        try:
            Method(driver).switch_out()
            b = Method(driver).get_attr('css', "[class='layui-layer layui-layer-iframe my-skin']", 'times')
            Method(driver).switch_iframe('layui-layer-iframe' + b)
        except NoSuchElementException:
            self.log_file_out('请输入评估对象')
        time.sleep(time_sleep)

        # 车型 车号新增页面
        if select_fault == '交集':
            Method(driver).click('id', 'partType')
        elif select_fault == '并集':
            time.sleep(1)

        driver.find_element_by_xpath('//a[text()="车型"]').click()
        time.sleep(1)

        a = deal_car(driver, car)
        if a is True:
            self.log_file_out('选车成功')
        else:
            self.log_file_out('选车失败')

        # 故障模式选择页面
        Method(driver).switch_out()
        c = Method(driver).get_attr('css', "[class='layui-layer layui-layer-iframe my-skin']", 'times')
        Method(driver).switch_iframe('layui-layer-iframe' + c)
        time.sleep(30)

        if select_fault == '交集':
            fault_status = deal_fault(driver, fault)
            if fault_status is True:
                self.log_file_out('故障模式选择成功')
            else:
                self.log_file_out('故障模式选择失败')

        elif select_fault == '并集':
            if value == 1:
                fault_status = deal_fault_union(driver, fault)
                if fault_status is True:
                    self.log_file_out('故障模式选择成功')
                else:
                    self.log_file_out('故障模式选择失败')
            elif value == 2:
                fault_status = deal_fault_union_2(driver, fault)
                if fault_status is True:
                    self.log_file_out('故障模式选择成功')
                else:
                    self.log_file_out('故障模式选择失败')

                # Method(driver).click('id', 'differPatternSelect')
            #
            # time.sleep(8)
            #
            # Method(driver).switch_out()
            # d = Method(driver).get_attr('css', "[class='layui-layer layui-layer-iframe my-skin']", 'times')
            # Method(driver).switch_iframe('layui-layer-iframe' + d)
            #
            # fault_status1 = deal_different(driver, fault1)
            # if fault_status1 is True:
            #     self.log_file_out('不同父级选择成功')
            # else:
            #     self.log_file_out('不同父级选择失败')

        try:
            Method(driver).switch_out()
            # d = "layui_layer" + c
            # e = "layui_layer" + str((int(c)-1))
            # Method(driver).click('xpath','//*[@id=\'%s\']/div[3]/a[3]' % d)
            Method(driver).click('class', 'layui-layer-btn2')
            # 点击保存按钮
            time.sleep(1)
            # Method(driver).click('xpath','//*[@id=\'%s\']/div[3]/a[1]' % e)
            Method(driver).click('class', 'layui-layer-btn0')
            logger.debug('bug不存在')
        except NoSuchElementException as e:
            logger.error('xpath' + '不存在!')
            logger.debug('bug存在')
        except:
            self.log_file_out('请录入正确的模型')

        Method(driver).switch_out()
        Method(driver).switch_iframe(
            driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/singleModel')]"))
        time.sleep(time_sleep)
        try:
            driver.find_element_by_xpath(
                "//a[contains(text(),\'{}\')]/../../td[8]/a[3]".format(modelName)).click()
        except WebDriverException:
            print('请录入正确的模型')
            return

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
        except Exception as e:
            logger.debug('计算失败')
            self.log_file_out('计算失败')


car = {'E27':['2641', '2642', '2643', '2644', '2645', '2646', '2647']}

# fault_pattern = {'高压供电系统': {'高压电缆、连接器及跳线':'all'}}

# fault_pattern = {'高压供电系统': 'all'}

fault1 = {'内装系统':{'厨房设施':{"微波炉柜":'all'}}}

fault_object = {'E27':
{'高压供电系统': {'高压电缆、连接器及跳线':{'电缆终端':'all'}}}
                }

# fault_object = {'E27':
#                     {'高压供电系统':{'高压电缆、连接器及跳线':{'电缆终端':"all",'跳线':"all",'电缆':'all'}}}
#                 }

time_sleep = 2
wait_time = 10


singelmodel().tech(url,username,password,'1.16测试',1,'','时间','2017-02-03','2017-10-20',2,car,fault1,'交集',fault1,time_sleep,wait_time)