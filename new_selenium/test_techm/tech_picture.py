from selenium import  webdriver
from new_selenium.bin.login import Login
from new_selenium.bin.main import Method
import time
from new_selenium.test_techm.tech_config import *
from config.config import path_dir
from config.log_config import logger

class Tech:
    def log_file_out(self,msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    def picture(self,url,username,password):

        driver = webdriver.Chrome()
        Login().login(url,username, password, driver)

        self.log_file_out('-----技术整改图表点击-----')
        for i in contents:
            try:
                Method(driver).contains_xpath('click',i)
                self.log_file_out('点击'+i+'成功')
            except Exception as e:
                logger.error(e)
                self.log_file_out('点击' + i + '失败')

        try:
            Method(driver).switch_out()
            Method(driver).switch_iframe(driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/technicalOptimization')]"))
            time.sleep(2)
            self.log_file_out('切入技术更改成功')
        except:
            self.log_file_out('切入技术更改失败')

        driver.find_element_by_xpath("//a[contains(text(),\'{}\')]/../../td[7]/a[3]".format('导出故障单测试1')).click()
        time.sleep(2)
        Method(driver).switch_out()

        driver.find_element_by_class_name('layui-layer-btn0').click()
        time.sleep(5)
        Method(driver).switch_out()
        Method(driver).switch_iframe(
            driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/technicalOptimization')]"))
        time.sleep(15)
        driver.find_element_by_xpath("//a[contains(text(),\'{}\')]/../../td[7]/a[4]".format('导出故障单测试1')).click()

        time.sleep(2)

        Method(driver).switch_out()
        tech_p = Method(driver).get_attr('css', "[class='layui-layer layui-layer-iframe']", 'times')
        Method(driver).switch_iframe('layui-layer-iframe' + tech_p)

        time.sleep(2)
        Method(driver).click('id', 'chart1')

        js = 'var aa = echarts.getInstanceByDom($("#chart1")[0]);' \
             'var option = aa.getOption();' \
             'p = {componentType: "series", seriesName: "第1次变更里程", seriesType: "line",value: [option.series[1].data[3][0], option.series[1].data[3][1]]};' \
             'skipTo(p, "CHART_MILLION_KILOMETERS_FAILURE_RATE", "关联故障", "ALL");'\
             'return p.value[0]'

        try:
            value = driver.execute_script(js)
            self.log_file_out('点击百万公里故障率(关联故障)图表成功')
        except:
            self.log_file_out('点击百万公里故障率(关联故障)图表失败')
        Method(driver).switch_out()
        driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[-1])
        status_aa = driver.execute_script(
            'return $("#opFaultOrderTable").bootstrapTable("getData").map(function(row){return $(row).attr("accumulatedMileage")}).some(function(item){return Number(item) >= %s})' % value)
        if status_aa is False:
            self.log_file_out('百万公里故障率故障单验证正确')
        else:
            self.log_file_out('百万公里故障率故障单验证错误')

        driver.execute_script('top.$(".layui-layer-btn0")[1].click()')
        time.sleep(2)
        Method(driver).switch_out()
        driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[-1])
        Method(driver).click('id', 'chart3')

        js1 = 'var aa = echarts.getInstanceByDom($("#chart3")[0]);' \
              'var option = aa.getOption();' \
              'jp.openDialogView("故障单", "/darams/a/mould/repairProcedure/skip_to?XValue=" + option.xAxis[0].data[2] + "&YValue=" + option.series[0].data[2] + "&resultObjType=" + "COMPONENT_1"+"&lineType=" + "关联故障" +"&confModelId=1516e96bc13e4e6bb5b148705c836280000&chartType=index&chartCode="+"CHART_MILLION_KILOMETERS_FAILURE_RATE", "100%", "100%");'\

        try:
            driver.execute_script(js1)
            self.log_file_out('各部件百万公里故障率成功')
        except:
            self.log_file_out('各部件百万公里故障率失败')

url = 'http://192.168.1.115:8080/darams/a?login'

Tech().picture(url, 'test', '1234')