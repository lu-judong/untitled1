from selenium import  webdriver
from new_selenium.bin.login import Login
from new_selenium.bin.main import Method
import time
from new_selenium.tech_compare.compare_config import *
from config.config import path_dir
from config.log_config import logger



class Compare:
    def log_file_out(self,msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    def picture(self,url,username,password):

        driver = webdriver.Chrome()
        Login().login(url,username, password, driver)

        self.log_file_out('-----不同平台图表点击-----')
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
                driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/moreModel')]"))
            self.log_file_out('切入不同平台成功')
        except:
            self.log_file_out('切入不同平台失败')

        time.sleep(2)
        driver.find_element_by_xpath(
            "//a[contains(text(),\'{}\')]/../../td[8]/a[4]".format('data')).click()

        Method(driver).switch_out()
        compare_p = Method(driver).get_attr('css', "[class='layui-layer layui-layer-iframe']", 'times')
        Method(driver).switch_iframe('layui-layer-iframe' + compare_p)
        time.sleep(2)

        Method(driver).click('id','moreModel')
        js = 'var aa = echarts.getInstanceByDom($("#moreModel")[0]);' \
             'var option = aa.getOption();' \
             'jp.openDialogView ("", "/darams/a/mould/moreModel/skipTo?XValue=" + option.series[0].data[1][0]+ "&YValue=" + option.series[0].data[1][1] + "&confModelName=" + option.series[0].name + "&lineType=" + "关联故障" + "&confModelId=70342a5b20a14381a7458f348aa82c83000&chartType=index","100%", "100%");'
        try:
            driver.execute_script(js)
            self.log_file_out('点击不同平台百万公里故障率图表成功')
        except:
            self.log_file_out('点击不同平台百万公里故障率图表失败')

        time.sleep(2)
        driver.execute_script('top.$(".layui-layer-btn0")[1].click()')

        time.sleep(3)

        Method(driver).click('id','basicFault')
        Method(driver).click('id', 'moreModel')

        js1 = 'var aa = echarts.getInstanceByDom($("#moreModel")[0]);' \
             'var option = aa.getOption();' \
             'jp.openDialogView (\'\', "/darams/a/mould/moreModel/skipTo?XValue=" + option.series[0].data[1][0]+ "&YValue=" + option.series[0].data[1][1] + "&confModelName=" + option.series[0].name + "&lineType=" + "基本故障" + "&confModelId=70342a5b20a14381a7458f348aa82c83000&chartType=index","100%", "100%");'
        try:
            driver.execute_script(js1)
            self.log_file_out('点击不同平台基本故障图表成功')
        except:
            self.log_file_out('点击不同平台基本故障图表失败')

        time.sleep(2)

        driver.execute_script('top.$(".layui-layer-btn0")[1].click()')

        time.sleep(3)

        Method(driver).click('id', 'safeFault')
        Method(driver).click('id', 'moreModel')

        js2 = 'var aa = echarts.getInstanceByDom($("#moreModel")[0]);' \
              'var option = aa.getOption();' \
              'jp.openDialogView (\'\', "/darams/a/mould/moreModel/skipTo?XValue=" + option.series[0].data[1][0]+ "&YValue=" + option.series[0].data[1][1] + "&confModelName=" + option.series[0].name + "&lineType=" + "安监故障" + "&confModelId=70342a5b20a14381a7458f348aa82c83000&chartType=index","100%", "100%");'
        try:
            driver.execute_script(js2)
            self.log_file_out('点击不同平台安监故障图表成功')
        except:
            self.log_file_out('点击不同平台安监故障图表失败')

        time.sleep(2)

        driver.execute_script('top.$(".layui-layer-btn0")[1].click()')

        time.sleep(2)

        Method(driver).click('id', 'serviceFault')
        Method(driver).click('id', 'moreModel')

        js3 = 'var aa = echarts.getInstanceByDom($("#moreModel")[0]);' \
              'var option = aa.getOption();' \
              'jp.openDialogView (\'\', "/darams/a/mould/moreModel/skipTo?XValue=" + option.series[0].data[1][0]+ "&YValue=" + option.series[0].data[1][1] + "&confModelName=" + option.series[0].name + "&lineType=" + "服务故障" + "&confModelId=70342a5b20a14381a7458f348aa82c83000&chartType=index","100%", "100%");'
        try:
            driver.execute_script(js3)
            self.log_file_out('点击不同平台服务故障图表成功')
        except:
            self.log_file_out('点击不同平台服务故障图表失败')

        time.sleep(2)

        driver.execute_script('top.$(".layui-layer-btn0")[1].click()')

        time.sleep(2)

        Method(driver).click('id', 'notAssociatedFault')
        Method(driver).click('id', 'moreModel')

        js4 = 'var aa = echarts.getInstanceByDom($("#moreModel")[0]);' \
              'var option = aa.getOption();' \
              'jp.openDialogView (\'\', "/darams/a/mould/moreModel/skipTo?XValue=" + option.series[0].data[1][0]+ "&YValue=" + option.series[0].data[1][1] + "&confModelName=" + option.series[0].name + "&lineType=" + "非关联故障" + "&confModelId=70342a5b20a14381a7458f348aa82c83000&chartType=index","100%", "100%");'
        try:
            driver.execute_script(js4)
            self.log_file_out('点击不同平台非关联故障图表成功')
        except:
            self.log_file_out('点击不同平台非关联故障图表失败')

url = 'http://192.168.1.115:8080/darams/a?login'

Compare().picture(url, 'test', '1234')
