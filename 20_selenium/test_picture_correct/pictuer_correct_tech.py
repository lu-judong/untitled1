from selenium import  webdriver
from new_selenium.bin.login import Login
from new_selenium.bin.main import Method
import time
from selenium.common.exceptions import NoSuchElementException
from new_selenium.tech_rams.rams_config import *
from config.config import path_dir
from config.log_config import logger
from bin.select_fault_occur import deal_fault

class Picture:
    def log_file_out(self,msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    def correct(self,url,username,password,db,value,value1,start,end,car,fault,select_fault,fault1,time_sleep,wait_time):

        driver = webdriver.Chrome()
        Login().login(url,username, password, driver)

        self.log_file_out('-----图形正确性-----')
        for i in contents:
            try:
                Method(driver).contains_xpath('click',i)
                self.log_file_out('点击'+i+'成功')
            except Exception as e:
                logger.error(e)
                self.log_file_out('点击' + i + '失败')
        time.sleep(2)
        js_s = " return $('#switchDb').prop('checked')"
        status = driver.execute_script(js_s)
        if db == '默认':
            if status is True:
                Method(driver).click('class', 'onoffswitch-label')
            else:
                time.sleep(1)
        else:
            if status is True:
                time.sleep(1)
            else:
                Method(driver).click('class', 'onoffswitch-label')

        time.sleep(time_sleep)
        try:
            Method(driver).switch_out()
            Method(driver).switch_iframe(
                driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/disposableModel/form')]"))
            time.sleep(time_sleep)
        except NoSuchElementException as e:
            self.log_file_out('切入iframe失败')


        try:
            Method(driver).select_down_list('id', 'modelObject', value)
            if value1 == '里程':
                Method(driver).input('id', 'confMileageList0_startMileage', start)
                Method(driver).input('id', 'confMileageList0_endMileage', end)
            elif value1 == '时间':
                time.sleep(time_sleep)
                Method(driver).select_down_list('id', 'confMileageSelect', 1)
                time.sleep(time_sleep)
                Method(driver).input('name', 'confDateList[0].startDate', start)
                Method(driver).input('name', 'confDateList[0].endDate', end)

        except NoSuchElementException as e:
            print('模型基本信息输入失败')
        except:
            print('请录入评估对象')
            return

        try:
            Method(driver).contains_xpath('click', '新增')
        except NoSuchElementException as e:
            print('点击新建按钮失败')

        try:
            Method(driver).switch_out()
            b = Method(driver).get_attr('css', "[class='layui-layer layui-layer-iframe my-skin']", 'times')
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

            Method(driver).two_element_click("[class='layui-layer layui-layer-iframe my-skin']", 'layui-layer-btn1')
        except NoSuchElementException as e:
            logger.error('xpath' + '不存在!')

        # 故障模式选择页面
        Method(driver).switch_out()
        c = Method(driver).get_attr('css', "[class='layui-layer layui-layer-iframe my-skin']", 'times')
        Method(driver).switch_iframe('layui-layer-iframe' + c)
        time.sleep(10)


        fault_status = deal_fault(driver, fault)
        if fault_status is True:
            self.log_file_out('故障模式选择成功')
        else:
            self.log_file_out('故障模式选择失败')

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
            driver.maximize_window()
            Method(driver).click('id', 'tab-1-btn1')
        except:
            self.log_file_out('请输入正确的模型')
            return

        Method(driver).click('id','tab-1-btn1')
        time.sleep(1)
        Method(driver).click('id','tab1chart1')

        time.sleep(2)
        js = 'var aa = echarts.getInstanceByDom($("#tab1chart1")[0]);'\
             'var option = aa.getOption();' \
             'return [[option.series[0].data[1],option.series[1].data[1],option.series[2].data[1],option.series[3].data[1],option.series[4].data[1]],[option.series[0].data[4],option.series[1].data[4],option.series[2].data[4],option.series[3].data[4],option.series[4].data[4]]]'


        try:
            value_baiwan = driver.execute_script(js)
        except:
            self.log_file_out('获取值失败')

        time.sleep(2)
        Method(driver).click('id','tab-1-btn3')
        time.sleep(1)
        Method(driver).click('id','tab1chart3')

        js1 = 'var aa = echarts.getInstanceByDom($("#tab1chart3")[0]);' \
              'var option = aa.getOption();' \
              'return [[option.series[0].data[1],option.series[1].data[1],option.series[2].data[1],option.series[3].data[1],option.series[4].data[1]],[option.series[0].data[4],option.series[1].data[4],option.series[2].data[4],option.series[3].data[4],option.series[4].data[4]]]'
        try:
            value_pinjun = driver.execute_script(js1)
        except:
            self.log_file_out('获取值失败')

        time.sleep(2)
        Method(driver).click('id', 'tab-1-btn4')
        time.sleep(1)
        Method(driver).click('id', 'tab1chart4')

        js2 = 'var aa = echarts.getInstanceByDom($("#tab1chart4")[0]);' \
              'var option = aa.getOption();' \
              'return [[option.series[0].data[1],option.series[1].data[1],option.series[2].data[1],option.series[3].data[1],option.series[4].data[1]],[option.series[0].data[4],option.series[1].data[4],option.series[2].data[4],option.series[3].data[4],option.series[4].data[4]]]'
        try:
            value_guzhang = driver.execute_script(js2)
        except:
            self.log_file_out('获取值失败')

        time.sleep(2)
        Method(driver).click('id','tab-1-btn5')
        time.sleep(1)
        Method(driver).click('id', 'tab-1-btn2')
        time.sleep(1)
        Method(driver).click('id', 'tab1chart2')

        js3 = 'var aa = echarts.getInstanceByDom($("#tab1chart2")[0]);' \
              'var option = aa.getOption();' \
              'return [[option.series[0].data[1],option.series[1].data[1],option.series[2].data[1],option.series[3].data[1],option.series[4].data[1]],[option.series[0].data[4],option.series[1].data[4],option.series[2].data[4],option.series[3].data[4],option.series[4].data[4]]]'
        try:
            value_guyou = driver.execute_script(js3)
        except:
            self.log_file_out('获取值失败')

        time.sleep(2)
        Method(driver).click('xpath','/html/body/div/ul/li[2]/a')

        time.sleep(2)
        Method(driver).click('id', 'tab-2-chart1')
        time.sleep(1)
        Method(driver).click('id', 'tab2chart1')

        js4 = 'var aa = echarts.getInstanceByDom($("#tab2chart1")[0]);' \
              'var option = aa.getOption();' \
              'return [[option.series[0].data[1],option.series[1].data[1],option.series[2].data[1],option.series[3].data[1],option.series[4].data[1]],[option.series[0].data[4],option.series[1].data[4],option.series[2].data[4],option.series[3].data[4],option.series[4].data[4]]]'
        try:
            value_danyi = driver.execute_script(js4)
        except:
            self.log_file_out('获取值失败')

        time.sleep(2)

        Method(driver).switch_out()
        driver.find_element_by_class_name('layui-layer-ico ').click()

        time.sleep(2)

        Method(driver).switch_out()
        time.sleep(1)
        Method(driver).contains_xpath('click','产品RAMS指标统计评估')

        time.sleep(2)

        Method(driver).switch_out()
        Method(driver).switch_iframe(
            driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/confModel')]"))
        time.sleep(2)


        driver.find_element_by_xpath("//a[contains(text(),\'{}\')]/../../td[8]/a[3]".format('图值正确模型')).click()
        time.sleep(2)
        Method(driver).switch_out()

        driver.find_element_by_class_name('layui-layer-btn0').click()
        time.sleep(2)
        Method(driver).switch_out()
        Method(driver).switch_iframe(
            driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/confModel')]"))
        time.sleep(60)
        driver.find_element_by_xpath("//a[contains(text(),\'{}\')]/../../td[8]/a[4]".format('图值正确模型')).click()

        time.sleep(2)
        Method(driver).switch_out()
        c = Method(driver).get_attr('css', "[class='layui-layer layui-layer-iframe']", 'times')
        Method(driver).switch_iframe('layui-layer-iframe' + c)

        time.sleep(2)
        Method(driver).click('id','chart1')

        js_rams1 = 'var aa = echarts.getInstanceByDom($("#chart1")[0]);' \
             'var option = aa.getOption();' \
              'return [[option.series[0].data[1],option.series[1].data[1],option.series[2].data[1],option.series[3].data[1],option.series[4].data[1]],[option.series[0].data[4],option.series[1].data[4],option.series[2].data[4],option.series[3].data[4],option.series[4].data[4]]]'
        try:
            value_baiwan1 = driver.execute_script(js_rams1)
        except:
            self.log_file_out('获取值失败')

        if len([item for item in value_baiwan[0] if not item in value_baiwan1[0]]) != 0 and len([item for item in value_baiwan[1] if not item in value_baiwan1[1]]) != 0:
            self.log_file_out('百万公里图的值不一致')
        else:
            self.log_file_out('百万公里的值一致')
        time.sleep(2)
        Method(driver).click('id','chart2')



        js_rams2 = 'var aa = echarts.getInstanceByDom($("#chart2")[0]);' \
                   'var option = aa.getOption();' \
                   'return [[option.series[0].data[1],option.series[1].data[1],option.series[2].data[1],option.series[3].data[1],option.series[4].data[1]],[option.series[0].data[4],option.series[1].data[4],option.series[2].data[4],option.series[3].data[4],option.series[4].data[4]]]'
        try:
            value_guzhang1 = driver.execute_script(js_rams2)
        except:
            self.log_file_out('获取值失败')

        L = [item for item in value_guzhang[0] if not item in value_guzhang1[0]]
        L1 = [item for item in value_guzhang[1] if not item in value_guzhang1[1]]
        L2 = ['0.00']
        if  len([item for item in L if not item in L2]) != 0 and len([item for item in L1 if not item in L2]) != 0:
            self.log_file_out('平均故障的值不一致')
        else:
            self.log_file_out('平均故障的值一致')

        time.sleep(2)
        Method(driver).click('id', 'chart3')
        js_rams3 = 'var aa = echarts.getInstanceByDom($("#chart3")[0]);' \
                   'var option = aa.getOption();' \
                   'return [[option.series[0].data[1],option.series[1].data[1],option.series[2].data[1],option.series[3].data[1],option.series[4].data[1]],[option.series[0].data[4],option.series[1].data[4],option.series[2].data[4],option.series[3].data[4],option.series[4].data[4]]]'

        try:
            value_pingjun1 = driver.execute_script(js_rams3)
        except:
            self.log_file_out('获取值失败')

        if len([item for item in value_pinjun[0] if not item in value_pingjun1[0]]) != 0 and len([item for item in value_pinjun[1] if not item in value_pingjun1[1]]) != 0:
            self.log_file_out('平均时间的值不一致')
        else:
            self.log_file_out('平均时间的值一致')

        time.sleep(2)
        Method(driver).click('id', 'chart4')
        js_rams4 = 'var aa = echarts.getInstanceByDom($("#chart4")[0]);' \
                   'var option = aa.getOption();' \
                   'return [[option.series[0].data[1],option.series[1].data[1],option.series[2].data[1],option.series[3].data[1],option.series[4].data[1]],[option.series[0].data[4],option.series[1].data[4],option.series[2].data[4],option.series[3].data[4],option.series[4].data[4]]]'
        try:
            value_guyou1 = driver.execute_script(js_rams4)
        except:
            self.log_file_out('获取值失败')

        if len([item for item in value_guyou[0] if not item in value_guyou1[0]]) != 0 and len([item for item in value_guyou[1] if not item in value_guyou1[1]]) != 0:
            self.log_file_out('固有可用度的值不一致')
        else:
            self.log_file_out('固有可用度的值一致')

        driver.execute_script('top.$(".layui-layer-ico")[1].click()')

        Method(driver).switch_out()
        time.sleep(1)
        Method(driver).contains_xpath('click', '单一模型指标分析')

        Method(driver).switch_out()
        Method(driver).switch_iframe(
            driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/singleModel')]"))

        time.sleep(3)
        driver.find_element_by_xpath(
            "//a[contains(text(),\'{}\')]/../../td[8]/a[3]".format('图形')).click()

        time.sleep(2)
        Method(driver).switch_out()

        driver.find_element_by_class_name('layui-layer-btn0').click()
        time.sleep(2)
        Method(driver).switch_out()
        Method(driver).switch_iframe(
            driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/singleModel')]"))
        time.sleep(wait_time)
        driver.find_element_by_xpath(
            "//a[contains(text(),\'{}\')]/../../td[8]/a[4]".format('图形')).click()

        Method(driver).switch_out()
        c = Method(driver).get_attr('css', "[class='layui-layer layui-layer-iframe']", 'times')
        Method(driver).switch_iframe('layui-layer-iframe' + c)

        time.sleep(2)
        Method(driver).click('id', 'maxMin')


        js_danyi = 'var aa = echarts.getInstanceByDom($("#maxMin")[0]);' \
              'var option = aa.getOption();' \
              'return[[option.series[6].data[1],option.series[8].data[1],option.series[4].data[1],option.series[0].data[1],option.series[3].data[1]],[option.series[6].data[4],option.series[8].data[4],option.series[4].data[4],option.series[0].data[4],option.series[3].data[4]]]'
        try:
            value_danyi1 = driver.execute_script(js_danyi)
        except:
            self.log_file_out('获取值失败')

        L3 = [item for item in value_danyi[0] if not item in value_danyi1[0]]
        L4 = [item for item in value_danyi[1] if not item in value_danyi1[1]]
        L5 = [item for item in L3 if not item in L4]
        if len(L5) != 0:
            self.log_file_out('单一模型值不一致')
        else:
            self.log_file_out('单一模型值一致')









url = 'http://192.168.1.20:8083/darams/a?login'
car = {
    'E28':'all','E27':'all'
}

fault_pattern = {'转向架':'all'}


#
fault1 = {'辅助供电系统':'all'}

time_sleep = 3
wait_time = 60


Picture().correct(url,'test','1234','默认',1,'里程','100','200',car,fault_pattern,'交集',fault1,time_sleep,wait_time)
