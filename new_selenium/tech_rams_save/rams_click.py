from selenium import webdriver
from new_selenium.bin.login import Login
from new_selenium.bin.main import Method
import time
from config.config import path_dir


class RAMS:
    def log_file_out(self, msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    def picture(self, url, username, password):

        driver = webdriver.Chrome()
        Login().login(url, username, password, driver)

        self.log_file_out('-----图表点击-----')

        try:
            Method(driver).contains_xpath('click', '运营数据统计分析系统')
            time.sleep(1)
            Method(driver).contains_xpath('click', '产品RAMS指标统计评估')
            self.log_file_out('点击RAMS菜单成功')
        except:
            self.log_file_out('点击RAMS菜单失败')

        Method(driver).switch_out()
        Method(driver).switch_iframe(
            driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/confModel')]"))

        driver.find_element_by_xpath("//*[text()=\'{}\']/../../td[8]/a[3]".format('yx_homemodel')).click()
        time.sleep(2)
        Method(driver).switch_out()

        driver.find_element_by_class_name('layui-layer-btn0').click()
        time.sleep(10)
        Method(driver).switch_out()
        Method(driver).switch_iframe(
            driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/confModel')]"))
        time.sleep(2)
        driver.find_element_by_xpath("//*[text()=\'{}\']/../../td[8]/a[4]".format('yx_homemodel')).click()

        Method(driver).switch_out()
        RAMS_b = Method(driver).get_attr('css', "[class='layui-layer layui-layer-iframe']", 'times')
        Method(driver).switch_iframe('layui-layer-iframe' + RAMS_b)
        time.sleep(2)

        Method(driver).click('id', 'chart1')

        js = 'var aa = echarts.getInstanceByDom($("#chart1")[0]);' \
             'var bb = "" ;' \
             'var option = aa.getOption();' \
             'for(let i in option.series[4].data){' \
             'if (option.series[4].data[i] != "NaN"){' \
             'var p = {componentType:"series",name:option.xAxis[0].data[i],seriesName:"关联故障",seriesType:"line",          value:option.series[4].data[i]};' \
             'bb = p.name;' \
             'skipTo(p,"百万公里故障率","CHART_MILLION_KILOMETERS_FAILURE_RATE");' \
             'break' \
             '}' \
             '}' \
             'return bb'
        try:
            value = driver.execute_script(js)
            self.log_file_out('点击RAMS百万公里故障率图表成功')
        except:
            self.log_file_out('点击RAMS百万公里故障率图表失败')

        Method(driver).switch_out()
        driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[-1])
        time.sleep(2)
        status_aa = driver.execute_script('return $("#opFaultOrderTable").bootstrapTable("getData").map(function(row){return $(row).attr("accumulatedMileage")}).some(function(item){return Number(item) >= %s})' % value)

        if status_aa is False:
            self.log_file_out('百万公里故障率故障单验证正确')
        else:
            self.log_file_out('百万公里故障率故障单验证错误')

        driver.execute_script('top.$(".layui-layer-btn0")[1].click()')

        time.sleep(2)
        Method(driver).switch_out()
        driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[-1])

        js1 = 'var aa = echarts.getInstanceByDom($("#chart2")[0]);' \
              'var option = aa.getOption();' \
             'var bb ="";' \
              'for(let i in option.series[4].data){' \
              'if (option.series[4].data[i] != "NaN"){' \
              'var p = {componentType:"series",name:option.xAxis[0].data[i],seriesName:"关联故障",seriesType:"line",value:option.series[4].data[i]};' \
              'bb = p.name;'\
              'skipTo(p,"平均故障间隔里程", "CHART_AVERAGE_INTERVAL_BETWEEN_FAILURES");' \
              'break' \
              '}' \
              '}' \
              'return bb'

        try:
            value1 = driver.execute_script(js1)
            self.log_file_out('点击RAMS平均故障间隔图表成功')
        except:
            self.log_file_out('点击RAMS平均故障间隔图表失败')
        Method(driver).switch_out()
        driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[-1])
        status_bb = driver.execute_script(
            'return $("#opFaultOrderTable").bootstrapTable("getData").map(function(row){return $(row).attr("accumulatedMileage")}).some(function(item){return Number(item) >= %s})' % value1)

        if status_bb is False:
            self.log_file_out('平均故障间隔故障单验证正确')
        else:
            self.log_file_out('平均故障间隔故障单验证错误')

        driver.execute_script('top.$(".layui-layer-btn0")[1].click()')

        time.sleep(3)
        Method(driver).switch_out()
        driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[-1])

        js2 = 'var aa = echarts.getInstanceByDom($("#chart3")[0]);' \
              'var option = aa.getOption();' \
              'var bb = "";' \
              'for(let i in option.series[4].data){' \
              'if (option.series[4].data[i] != "NaN"){' \
              'var p = {componentType:"series",name:option.xAxis[0].data[i],seriesName:"关联故障",seriesType:"line",value:option.series[4].data[i]};' \
              'bb = p.name;'\
              'skipTo (p ,"平均修复时间", "CHART_AVERAGE_REPAIR_TIME");' \
              'break' \
              '}' \
              '}' \
              'return bb'
        try:
            value2 = driver.execute_script(js2)
            self.log_file_out('点击RAMS平均修复时间图表成功')
        except:
            self.log_file_out('点击RAMS平均修复时间图表失败')
        Method(driver).switch_out()
        driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[-1])
        status_cc = driver.execute_script(
            'return $("#opFaultOrderTable").bootstrapTable("getData").map(function(row){return $(row).attr("accumulatedMileage")}).some(function(item){return Number(item) >= %s})' % value2)

        if status_cc is False:
            self.log_file_out('平均修复时间故障单验证正确')
        else:
            self.log_file_out('平均修复时间故障单验证错误')


        driver.execute_script('top.$(".layui-layer-btn0")[1].click()')

        time.sleep(3)
        Method(driver).switch_out()
        driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[-1])
        js3 = 'var aa = echarts.getInstanceByDom($("#chart4")[0]);' \
              'var option = aa.getOption();' \
              'var bb = "" ;' \
              'for(let i in option.series[4].data){' \
              'if (option.series[4].data[i] != "NaN"){' \
              'var p = {componentType:"series",name:option.xAxis[0].data[i],seriesName:"关联故障",seriesType:"line",value:option.series[4].data[i]};' \
              'bb = p.name;' \
              'skipTo (p ,"固有可用度", "CHART_INHERENT_AVAILABILITY");' \
              'break' \
              '}' \
              '}' \
              'return bb'
        try:
            value3 = driver.execute_script(js3)
            self.log_file_out('点击RAMS固有可用度图表成功')
        except:
            self.log_file_out('点击RAMS固有可用度图表失败')
        Method(driver).switch_out()
        driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[-1])
        status_dd = driver.execute_script(
            'return $("#opFaultOrderTable").bootstrapTable("getData").map(function(row){return $(row).attr("accumulatedMileage")}).some(function(item){return Number(item) >= %s})' % value3)

        if status_dd is False:
            self.log_file_out('固有可用度故障单验证正确')
        else:
            self.log_file_out('固有可用度故障单验证错误')


url = 'http://192.168.1.115:8080/darams/a?login'

RAMS().picture(url, 'test', '1234')