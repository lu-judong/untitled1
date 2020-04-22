from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from bin.select_fault_union2 import deal_fault_union_2
from config.log_config import logger
import time
from bin.main import Method
from bin.login import Login
from selenium.webdriver.support.ui import Select
from config.config import path_dir,url,username,password,rams_config
from bin.select_fault_occur import deal_fault
from bin.select_car import deal_car
from bin.select_fault_union import deal_fault_union
from bin.select_butongfuji import deal_different
from bin.select_fault_butongfuji_occur import deal_different_occur



class Tech:
    def log_file_out(self, msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    def tech_fault_analysis(self,url,username,password,value,value1,start,end,car,fault,select_fault,fault1,time_sleep,wait_time):
        #
        # option = webdriver.ChromeOptions()
        # option.add_argument("headless")
        # driver = webdriver.Chrome(chrome_options=option,
        #                           executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')
        driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
        Login().login(url,username,password,driver)

        self.log_file_out('-----RAMS指标评估-----')

        for i in rams_config:
            try:
                Method(driver).contains_xpath('click',i)
                time.sleep(1)
                self.log_file_out('点击'+i+'成功')
            except Exception as e:
                logger.debug(e)
                self.log_file_out('点击' + i + '失败')

        time.sleep(time_sleep)
        try:
            Method(driver).switch_out()
            Method(driver).switch_iframe(
                driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/disposableModel/form')]"))
            time.sleep(time_sleep)
        except NoSuchElementException as e:
            self.log_file_out('切入iframe失败')


        if Select(driver.find_element_by_id('confMileageSelect')).first_selected_option.text == '里程':
            print('里程/日期框正确')
        else:
            print('里程/日期框错误')

        if Select(driver.find_element_by_id('confMileageList0_averageSpeedSelect')).first_selected_option.text == '260':
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
            Method(driver).select_down_list('id', 'modelObject', value)
            if value1 == '里程':
                Method(driver).input('id', 'confMileageList0_startMileage', start)
                Method(driver).input('id', 'confMileageList0_endMileage', end)
            elif value1 == '时间':
                time.sleep(time_sleep)
                Method(driver).select_down_list('id','confMileageSelect',1)
                time.sleep(time_sleep)
                Method(driver).input('name', 'confDateList[0].startDate', start)
                Method(driver).input('name', 'confDateList[0].endDate', end)

        except NoSuchElementException as e:
            print('模型基本信息输入失败')
        except:
            print('请录入评估对象')
            return

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

        time.sleep(5)

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

        driver.find_element_by_xpath('//a[text()="车型"]').click()
        time.sleep(1)

        try:
            for x in car:
                driver.find_element_by_xpath(
                    "//span[@class='train zoomIn' and contains(text(),\'{}\')]".format(x)).click()
                car_num = car.get(x)
                time.sleep(2)
                if car_num == 'all':
                    driver.execute_script('top.select_all(this,"train-no-layer-class",true,true)')
                else:
                    for i in car_num:
                        # driver.find_element_by_xpath("//span[contains(text(),\'{}\')]".format(i)).click()
                        car_num = driver.find_element_by_xpath(
                            '//span[contains(text(),\'{}\')]/..'.format(i)).get_attribute('id')

                        js = 'top.checked(top.$("#{}"))'.format(car_num)
                        driver.execute_script(js)

                    # time.sleep(2)
                driver.execute_script('top.$(".layui-layer-btn0")[1].click()')
                time.sleep(2)
            Method(driver).switch_out()
            # 这个可以点击得元素失去焦点
            # Message: unknown error: Element <a class="layui-layer-btn1">...</a> is not clickable at point (975, 498). Other element would receive the click: <a class="layui-layer-btn3">...</a>
            # Method(driver).two_element_click("[class='layui-layer-btn layui-layer-btn-']",'layui-layer-btn1')
            Method(driver).two_element_click("[class='layui-layer layui-layer-iframe my-skin']", 'layui-layer-btn1')
            v8 = '选车成功'
        except NoSuchElementException as e:
            logger.error('xpath' + '不存在!')
            v8 = '选车失败'



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

            #     Method(driver).click('id', 'differPatternSelect')
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
                driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/disposableModel/form')]"))
            Method(driver).click('id', 'calculate')
            self.log_file_out('点击计算按钮成功')
        except:
            self.log_file_out('点击计算按钮失败')

        time.sleep(wait_time)
        try:
            Method(driver).switch_out()
            Method(driver).switch_iframe(
                driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/disposableModel/data_view')]"))
        except:
            self.log_file_out('请输入正确的模型')
            return
        #
        # try:
        #     js = 'var aa = echarts.getInstanceByDom($("#tab1chart1")[0]);' \
        #           'var option = aa.getOption();' \
        #           ' option.series[3].data.forEach((item,index)=>{' \
        #           'if( item != "NaN"){' \
        #           'var param = {componentType:"series",name:option.xAxis[0].data[index],seriesName:"关联故障",seriesType:"line",value:option.series[3].data[index]};' \
        #          'var lineType = param.seriesName, x = param.name, y = param.value;' \
        #          '''var faultIds = globalDataSet["tab-1-chart1"][lineType][x][y].faultIds.split(',');''' \
        #           "if (faultIds != null && faultIds != '' && faultIds.length > 0) {" \
        #           'skipToFautlOrder(faultIds);' \
        #           'return false;' \
        #           '}' \
        #           '}})'
        #     driver.execute_script(js)
        # except:
        #     self.log_file_out('点击图表失败')
        #
        # time.sleep(3)
        # Method(driver).switch_out()
        # Method(driver).two_element_click("[class='layui-layer layui-layer-page']", 'layui-layer-ico')
        #
        # try:
        #     Method(driver).switch_out()
        #     Method(driver).switch_iframe(driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/disposableModel/data_view')]"))
        # except:
        #     return
        # time.sleep(3)
        #
        # try:
        #     Method(driver).click('xpath','/html/body/div/ul/li[2]/a')
        #     time.sleep(2)
        #     Method(driver).click('id', 'tab-2-chart1')
        #     self.log_file_out('点击单一模型指标分析图表成功')
        # except:
        #     self.log_file_out('点击单一模型指标分析图表失败')
        # try:
        #     js1 = 'var aa = echarts.getInstanceByDom($("#tab2chart1")[0]);' \
        #          'var option = aa.getOption();' \
        #          ' option.series[8].data.forEach((item,index)=>{' \
        #          'if( item != "NaN"){' \
        #          'var param = {componentType:"series",name:option.xAxis[0].data[index],seriesName:"MIN关联故障",seriesType:"line",value:option.series[8].data[index]};' \
        #          'var lineType = param.seriesName, x = param.name, y = param.value;' \
        #          '''var faultIds = globalDataSet["tab-2-chart1"][lineType][x][y].faultIds.split(',');''' \
        #          "if (faultIds != null && faultIds != '' && faultIds.length > 0) {" \
        #          'skipToFautlOrder(faultIds);' \
        #          'return false;' \
        #          '}' \
        #          '}})'
        #
        #     driver.execute_script(js1)
        #     self.log_file_out('点击单一模型图表上的点成功')
        # except:
        #     self.log_file_out('点击单一模型图表上的点失败')

        # time.sleep(3)
        # try:
        #     Method(driver).switch_out()
        #     Method(driver).two_element_click("[class='layui-layer layui-layer-page']", 'layui-layer-ico')
        # except:
        #     print('')
        #     pass
        #
        # try:
        #     Method(driver).switch_out()
        #     Method(driver).switch_iframe(
        #         driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/disposableModel/data_view')]"))
        # except:
        #     return
        # time.sleep(3)
        #
        # try:
        #     Method(driver).click('xpath', '/html/body/div/ul/li[3]/a')
        #     time.sleep(2)
        #     Method(driver).click('id', 'tab-3-chart11')
        #     self.log_file_out('点击故障占比分析图表成功')
        # except:
        #     self.log_file_out('点击故障占比分析图表失败')
        # try:
        #     js2 = 'var aa = echarts.getInstanceByDom($("#tab-3-chart11")[0]);' \
        #           'var option = aa.getOption();' \
        #           ' option.series[0].data.forEach((item,index)=>{' \
        #           'if( item != "NaN"){' \
        #           'var param = {componentType:"series",name:option.yAxis[0].data[index],seriesName:"关联故障",seriesType:"bar",value:option.series[0].data[index]};' \
        #           'var lineType = param.seriesName, x = param.name, y = param.value;' \
        #           '''var faultIds = globalDataSet["tab-3-chart11"][lineType][x][y].faultIds.split(',');''' \
        #           "if (faultIds != null && faultIds != '' && faultIds.length > 0) {" \
        #           'skipToFautlOrder(faultIds);' \
        #           'return false;' \
        #           '}' \
        #           '}})'
        #
        #     driver.execute_script(js2)
        #     self.log_file_out('点击故障占比图表上的点成功')
        # except:
        #     self.log_file_out('点击图表占比图表上的点失败')











car = {
    'E27': ['2641','2642','2643','2644','2645','2646','2647']
}
# fault_pattern = {'E27':{'高压供电系统': {'受电弓': 'all'}}}

fault_pattern = {'高压供电系统':'all'}
#
# fault_object = {
#     '高压供电系统':{'高压电缆、连接器及跳线':['电缆']},
#     '辅助供电系统':['刮雨器电源'],
#     '门窗系统':'all'
# }
#
fault1 = {'辅助供电系统':'all'}

time_sleep = 3
wait_time = 10


Tech().tech_fault_analysis(url,username,password,0,'时间','2017-02-03','2017-10-20',car,fault_pattern,'交集',fault1,time_sleep,wait_time)
