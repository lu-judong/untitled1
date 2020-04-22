from selenium import  webdriver
from new_selenium.bin.login import Login
from new_selenium.bin.main import Method
import time
from new_selenium.tech_incontrol.incontrol_config import *
from config.config import path_dir
from config.log_config import logger



class Fault:
    def log_file_out(self,msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    def picture(self,url,username,password):

        driver = webdriver.Chrome()
        Login().login(url,username, password, driver)

        self.log_file_out('-----内控指标图表点击-----')
        for i in contents:
            try:
                Method(driver).contains_xpath('click',i)
                time.sleep(2)
                self.log_file_out('点击'+i+'成功')
            except Exception as e:
                logger.error(e)
                self.log_file_out('点击' + i + '失败')

        try:
            Method(driver).switch_out()
            Method(driver).switch_iframe(
                driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/inControl')]"))
            self.log_file_out('切入内控指标成功')
        except:
            self.log_file_out('切入内控指标失败')

        driver.find_element_by_xpath("//a[contains(text(),\'{}\')]/../../td[7]/a[1]".format('111')).click()
        time.sleep(2)
        Method(driver).switch_out()

        driver.find_element_by_class_name('layui-layer-btn0').click()
        time.sleep(2)
        Method(driver).switch_out()
        Method(driver).switch_iframe(
            driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/inControl')]"))
        time.sleep(5)
        driver.find_element_by_xpath("//a[contains(text(),\'{}\')]/../../td[7]/a[2]".format('111')).click()

        Method(driver).switch_out()
        incontrol_p = Method(driver).get_attr('css', "[class='layui-layer layui-layer-iframe']", 'times')
        Method(driver).switch_iframe('layui-layer-iframe' + incontrol_p)

        home_handles = driver.current_window_handle

        time.sleep(2)

        value_com = driver.execute_script('var aa = echarts.getInstanceByDom($("#myChart2")[0]);' \
             'var option = aa.getOption();' \
             'return [option.series[0].data[0].value[0]]')

        js1 = 'myChart2.trigger("dblclick",{"data":{"path":"苏州华兴致远电子科技有限公司"},"componentType":"series","seriesType":"treemap"})'
        try:
            driver.execute_script(js1)
            self.log_file_out('点击供应商内控指标图表成功')
        except:
            self.log_file_out('点击供应商内控指标图表失败')

        time.sleep(2)
        all_handle = driver.window_handles
        for i in all_handle:
            if i != home_handles:
                driver.switch_to.window(i)

        driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div[1]/div[2]/button[1]').click()
        time.sleep(10)
        # for i in range(0,len(driver.find_elements_by_xpath('//*[@id="opFaultOrderTable"]/tbody/tr/td[12]'))):
        #     print(driver.find_elements_by_xpath('//*[@id="opFaultOrderTable"]/tbody/tr/td[12]')[i].text)
        status_aa = driver.execute_script(
            'return $("#opFaultOrderTable").bootstrapTable("getData").map(function(row){return $(row).attr("mainResponsibility")}).some(function(item){return item !="苏州华兴致远电子科技有限公司"})')

        value_com1 = driver.execute_script('return $("#opFaultOrderTable").bootstrapTable("getData").map(function(row){return $(row).attr("mainResponsibility")}).length')
        if status_aa is False and value_com[0] == value_com1:
            self.log_file_out('主要责任单位数值正确')
        else:
            self.log_file_out('主要责任单位数值不正确')

        for i in all_handle:
            if i != home_handles:
                driver.close()
        driver.switch_to.window(home_handles)
        time.sleep(2)
        # Method(driver).click('id','chart2')
        # js1 = 'var aa = echarts.getInstanceByDom($("#chart2")[0]);' \
        #      'var option = aa.getOption();' \
        #      'param = {componentType:"series",name:option.yAxis[0].data[0],seriesName:"关联故障",seriesType:"bar",value:option.series[0].data[0]}; ' \
        #      'skipTo(param, "RAILWAY_BUREAU");'
        js2 = 'var title =  "2017-07责任部室故障统计";' \
              'var dateString = title.substring(0,title.length-8);' \
              'if (dateString.length > 7){' \
              'window.open ("/darams/a/fault/opFaultOrder/qList?confModelId=ed42931a637744a0a11141ccaccfd40b000                     &chartType=INSIDE&depart=" + "转向架开发部");}else{window.open("/darams/a/fault/opFaultOrder/qList?confModelId=ed42931a637744a0a11141ccaccfd40b000&chartType=INSIDE&depart=" + "转向架开发部" + "&octMonthFrom=" + dateString + "&octMonthTo=" + dateString);}'
        try:
            driver.execute_script(js2)
            self.log_file_out('点击责任部室图表成功')
        except:
            self.log_file_out('点击责任部室图表失败')

        time.sleep(2)
        all_handle1 = driver.window_handles
        for i in all_handle1:
            if i != home_handles:
                driver.switch_to.window(i)

        status_bb = driver.execute_script(
            'return $("#opFaultOrderTable").bootstrapTable("getData").map(function(row){return $(row).attr("mainResponsibility")}).some(function(item){return item !="技术中心"})')

        if status_bb is False:
            self.log_file_out('责任部室验证正确')
        else:
            self.log_file_out('责任部室验证不正确')



url = 'http://192.168.1.115:8080/darams/a?login'

Fault().picture(url, 'test', '1234')

