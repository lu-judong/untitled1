from selenium import  webdriver
from new_selenium.bin.login import Login
from new_selenium.bin.main import Method
import time
from new_selenium.tech_singelmodel.singel_config import *
from config.config import path_dir
from config.log_config import logger

class Singel:
    def log_file_out(self,msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    def picture(self,url,username,password):

        driver = webdriver.Chrome()
        Login().login(url,username, password, driver)

        self.log_file_out('-----单一模型图表点击-----')
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
                driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/singleModel')]"))
            time.sleep(2)
            self.log_file_out('切入修程修制成功')
        except:
            self.log_file_out('切入修程修制失败')

        driver.find_element_by_xpath("//a[contains(text(),\'{}\')]/../../td[8]/a[3]".format('图形')).click()
        time.sleep(2)
        Method(driver).switch_out()

        driver.find_element_by_class_name('layui-layer-btn0').click()
        time.sleep(2)
        Method(driver).switch_out()
        Method(driver).switch_iframe(
            driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/singleModel')]"))
        time.sleep(10)
        driver.find_element_by_xpath("//a[contains(text(),\'{}\')]/../../td[8]/a[4]".format('图形')).click()

        Method(driver).switch_out()
        singel_p = Method(driver).get_attr('css', "[class='layui-layer layui-layer-iframe']", 'times')
        Method(driver).switch_iframe('layui-layer-iframe' + singel_p)

        time.sleep(2)
        Method(driver).click('id','maxMin')

        js = 'var aa = echarts.getInstanceByDom($("#maxMin")[0]);' \
             'var option = aa.getOption();' \
             'var bb = "";' \
             'param={name:option.xAxis[0].data[3],value:option.series[6].data[3]};' \
             'bb = param.name;'\
             'jp.openDialogView ("", "/darams/a/mould/confModel/skipTo2?XValue=" + param.name +                          "&chartCode=CHART_MIN_MILLION_KILOMETERS_FAILURE_RATE" + "&YValue=" + param.value + "&chartName=" + "最大百万公里故障率" + "&lineType=" + "关联故障" + "&confModelId=72cac1d6b9564f5193c032feab7ac697000&chartType=index", "100%", "100%");'\
            'return bb'

        try:
            value = driver.execute_script(js)
            self.log_file_out('点击最大最小百万公里故障率(关联故障)图表成功')
        except:
            self.log_file_out('点击最大最小百万公里故障率(关联故障)图表失败')

        Method(driver).switch_out()
        driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[-1])
        status_cc = driver.execute_script(
            'return $("#opFaultOrderTable").bootstrapTable("getData").map(function(row){return $(row).attr("accumulatedMileage")}).some(function(item){return Number(item) >= %s})' % value)

        if status_cc is False:
            self.log_file_out('最大最小百万公里故障率故障单验证正确')
        else:
            self.log_file_out('最大最小百万公里故障率故障单验证错误')

        time.sleep(5)

url = 'http://192.168.1.115:8080/darams/a?login'

Singel().picture(url, 'test', '1234')