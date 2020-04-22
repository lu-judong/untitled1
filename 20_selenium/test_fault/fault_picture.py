from selenium import  webdriver
from new_selenium.bin.login import Login
from new_selenium.bin.main import Method
import time
from new_selenium.tech_fault.fault_config import *
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

        self.log_file_out('-----故障占比分析图表点击-----')
        for i in contents:
            try:
                Method(driver).contains_xpath('click',i)
                self.log_file_out('点击'+i+'成功')
            except Exception as e:
                logger.error(e)
                self.log_file_out('点击' + i + '失败')

        try:
            Method(driver).switch_out()
            Method(driver).switch_iframe(
                driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/analysisProportion')]"))
            self.log_file_out('切入故障占比分析成功')
        except:
            self.log_file_out('切入故障占比分析失败')

        driver.find_element_by_xpath("//a[contains(text(),\'{}\')]/../../td[7]/a[3]".format('故障占比故障单')).click()
        time.sleep(2)
        Method(driver).switch_out()

        driver.find_element_by_class_name('layui-layer-btn0').click()
        time.sleep(2)
        Method(driver).switch_out()
        Method(driver).switch_iframe(
            driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/analysisProportion')]"))
        time.sleep(10)
        driver.find_element_by_xpath("//a[contains(text(),\'{}\')]/../../td[7]/a[4]".format('故障占比故障单')).click()

        Method(driver).switch_out()
        fault = Method(driver).get_attr('css', "[class='layui-layer layui-layer-iframe']", 'times')
        Method(driver).switch_iframe('layui-layer-iframe' + fault)

        time.sleep(2)

        js = 'var aa = echarts.getInstanceByDom($("#chart1")[0]);' \
             'var option = aa.getOption();' \
            'param = {componentType:"series",name:option.yAxis[0].data[7],seriesName:"关联故障",seriesType:"bar",value:option.series[0].data[7]}; ' \
            'skipTo(param, "COMPONENT");'
        try:
            driver.execute_script(js)
            self.log_file_out('点击各系统/部件图表成功')
        except:
            self.log_file_out('点击各系统/部件图表失败')

        time.sleep(2)
        driver.execute_script('top.$(".layui-layer-btn0")[1].click()')

        time.sleep(2)

        js1 = 'var aa = echarts.getInstanceByDom($("#chart2")[0]);' \
             'var option = aa.getOption();' \
             'param = {componentType:"series",name:option.yAxis[0].data[0],seriesName:"关联故障",seriesType:"bar",value:option.series[0].data[0]}; ' \
             'skipTo(param, "RAILWAY_BUREAU");'
        try:
            driver.execute_script(js1)
            self.log_file_out('点击各路局故障占比图表成功')
        except:
            self.log_file_out('点击各路局故障占比图表失败')
        Method(driver).switch_out()
        driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[-1])
        time.sleep(2)
        status_aa = driver.execute_script(
            'return $("#opFaultOrderTable").bootstrapTable("getData").map(function(row){return $(row).attr("railway")}).some(function(item){return item !="武汉铁路局-空"})')

        if status_aa is False:
            self.log_file_out('路局验证结果正确')
        else:
            self.log_file_out('路局验证结果失败')


        time.sleep(2)
        driver.execute_script('top.$(".layui-layer-btn0")[1].click()')

        time.sleep(2)
        Method(driver).switch_out()
        driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[-1])
        Method(driver).click('id', 'chart3')
        js2 = 'var aa = echarts.getInstanceByDom($("#chart3")[0]);' \
             'var option = aa.getOption();' \
             'param = {componentType:"series",name:option.yAxis[0].data[0],seriesName:"关联故障",seriesType:"bar",value:option.series[0].data[0]}; ' \
             'skipTo(param, "RESPONSIBLE_PARTY_CLASS");'
        try:
            driver.execute_script(js2)
            self.log_file_out('点击各责任方故障占比图表成功')
        except:
            self.log_file_out('点击各责任方故障占比图表失败')
        Method(driver).switch_out()
        driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[-1])
        status_bb = driver.execute_script(
            'return $("#opFaultOrderTable").bootstrapTable("getData").map(function(row){return $(row).attr("responsibilityClass")}).some(function(item){return item !="用户单位"})')

        if status_bb is False:
            self.log_file_out('责任方验证结果正确')
        else:
            self.log_file_out('责任方验证结果失败')
        time.sleep(2)

        time.sleep(2)
        driver.execute_script('top.$(".layui-layer-btn0")[1].click()')

        time.sleep(2)
        Method(driver).switch_out()
        driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[-1])

        js3 = 'var aa = echarts.getInstanceByDom($("#chart4")[0]);' \
             'var option = aa.getOption();' \
             'param = {componentType:"series",name:option.yAxis[0].data[0],seriesName:"关联故障",seriesType:"bar",value:option.series[0].data[0]}; ' \
             'skipTo(param, "REASON_CLASS");'
        try:
            driver.execute_script(js3)
            self.log_file_out('点击故障原因占比图表成功')
        except:
            self.log_file_out('点击故障原因占比图表失败')

        driver.execute_script('top.$(".layui-layer-btn0")[1].click()')

        time.sleep(2)
        Method(driver).click('id', 'chart5')
        js4 = 'var aa = echarts.getInstanceByDom($("#chart5")[0]);' \
              'var option = aa.getOption();' \
              'param = {componentType:"series",name:option.yAxis[0].data[0],seriesName:"关联故障",seriesType:"bar",value:option.series[0].data[0]}; ' \
              'skipTo(param, "FAULTY_LEVEL");'
        try:
            driver.execute_script(js4)
            self.log_file_out('点击故障级别图表成功')
        except:
            self.log_file_out('点击故障级别图表失败')


url = 'http://192.168.1.20:8083/darams/a?login'

Fault().picture(url, 'test', '1234')