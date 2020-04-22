from bin.select_fault_union2 import deal_fault_union_2
from config.config import path_dir
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from config.log_config import logger
import time
from bin.main import Method
from bin.login import Login
from new_selenium.test_weixiu.weixiu_config import *
from selenium.webdriver.support.ui import Select
from bin.select_fault_occur import deal_fault
from bin.select_car import deal_car
from bin.select_fault_union import deal_fault_union
from bin.select_butongfuji import deal_different
from bin.select_fault_butongfuji_occur import deal_different_occur


#维修规程优化效果分析
class test_technology:
    def log_file_out(self,msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()


    # 检查RAMS运营数据分析
    def tech(self,url,username,password,value,start,end,end1,car,fault,select_fault,fault1,time_sleep,wait_time):

        # option = webdriver.ChromeOptions()
        # option.add_argument("headless")
        # driver = webdriver.Chrome(chrome_options=option
        # ,executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe'
        #  )
        # driver.maximize_window()
        driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))

        self.log_file_out('-----修程修制立即计算-----')
        Login().login(url,username,password,driver)


        for i in contents:
            try:
                Method(driver).contains_xpath('click',i)
                self.log_file_out('点击'+i+'成功')
            except Exception as e:
                logger.debug(e)
                self.log_file_out('点击' + i + '失败')
        time.sleep(time_sleep)
        # 点击新建得到弹框
        try:
            Method(driver).switch_out()
            Method(driver).switch_iframe(
                driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/repairProcedure')]"))
            Method(driver).click('id', 'calculate')
            time.sleep(time_sleep)
        except NoSuchElementException as e:
            self.log_file_out('点击新建按钮失败,未找到立即计算按钮的xpath')

        Method(driver).switch_out()
        a = Method(driver).get_attr('css', "[class='layui-layer layui-layer-iframe']", 'times')
        Method(driver).switch_iframe('layui-layer-iframe' + a)

        try:
            Method(driver).select_down_list('id', 'modelObject', value)
            Method(driver).input('id','confMileageList0_startMileage',start)
            Method(driver).input('id','confMileageList0_endMileage',end)
            Method(driver).input('id','confMileageList1_endMileage',end1)
        except NoSuchElementException as e:
            print('模型录入错误 找不到对应的xpath')
        except:
            print('模型录入数据出错')

        if Select(driver.find_element_by_id('averageSpeedSelect')).first_selected_option.text == '260':
            print('平均时速默认值正确')
        else:
            print('平均时速默认值不正确')

        if driver.find_element_by_css_selector("[class='filter-option pull-left']").text== driver.find_element_by_css_selector("[class='btn dropdown-toggle btn-default']").get_attribute('title'):
            print('服务故障定义默认值正确')
        else:
            print('服务故障定义默认值不正确')

        if driver.find_element_by_id('confLateHoursList0_lateHoursFrom').get_attribute('value') == '3':
            print('晚点时长默认正确')
        else:
            print('晚点时长默认不正确')


        try:
            Method(driver).contains_xpath('click','新增')
        except NoSuchElementException as e:
            print('点击新建按钮失败')

        try:
            Method(driver).switch_out()
            b = Method(driver).get_attr('css',"[class='layui-layer layui-layer-iframe my-skin']", 'times')
            Method(driver).switch_iframe('layui-layer-iframe' + b)
        except:
            print('请录入评估对象')
            return

        time.sleep(time_sleep)

        # 车型 车号新增页面
        if select_fault == '交集':
            js_s = "return $('#partType').prop('checked')"
            status = driver.execute_script(js_s)
            if status is True:
                Method(driver).click('id', 'partType')
            else:
                time.sleep(1)
        elif select_fault == '并集':
            js_s = "return $('#partType').prop('checked')"
            status = driver.execute_script(js_s)
            if status is True:
                time.sleep(1)
            else:
                Method(driver).click('id', 'partType')

        a = deal_car(driver, car)
        if a is True:
            self.log_file_out('选车成功')
        else:
            self.log_file_out('选车失败')

        # 故障模式选择页面
        Method(driver).switch_out()
        c = Method(driver).get_attr('css',"[class='layui-layer layui-layer-iframe my-skin']", 'times')
        Method(driver).switch_iframe('layui-layer-iframe' + c)
        time.sleep(time_sleep)
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
            Method(driver).click('class', 'layui-layer-btn2')
        except NoSuchElementException as e:
            logger.error('xpath' + '不存在!')
            self.log_file_out('点击确定按钮失败')
        except:
            self.log_file_out('请录入完整的模型')
            return


        time.sleep(time_sleep)
        try:
            Method(driver).switch_out()
            Method(driver).switch_iframe(
                driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/disposableModel/repairProcedureForm')]"))
            Method(driver).click('id', 'calculate')
            self.log_file_out('点击计算按钮成功')
        except NoSuchElementException:
            self.log_file_out('点击计算按钮失败')
        except:
            self.log_file_out('模型录入失败')

        time.sleep(wait_time)

        Method(driver).switch_out()
        try:
            c = Method(driver).get_attr('css', "[class='layui-layer layui-layer-iframe']", 'times')
        except NoSuchElementException as e:
            print('请录入正确的模型')
            return

        try:
            Method(driver).switch_out()
            Method(driver).switch_iframe(driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/disposableModel/repairProcedureView')]"))
            time.sleep(time_sleep)
            logger.debug('图表页面获取成功')
            self.log_file_out('图表页面获取成功')
        except NoSuchElementException as e:
            self.log_file_out('图表页面获取失败')
        except:
            print('图表页面获取失败')

url = 'http://192.168.1.115:8080/darams/a/login'
car = {
    'E27': ['2641','2642','2643','2644','2645','2646','2647','2648']
}

# fault_pattern = {'高压供电系统':['受电弓']}
# fault_pattern = {
#     '高压供电系统': ['无电']
# }

fault_pattern = {'E27':
{'高压供电系统': {'受电弓': 'all'}}}


fault1 = {'辅助供电系统':'all'}

time_sleep = 3
wait_time = 10


test_technology().tech(url,'test','1234',2,'0','100','200',car,fault_pattern,'并集',fault1,time_sleep,wait_time)