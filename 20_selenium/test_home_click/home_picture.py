from selenium import  webdriver
from bin.login import Login
from bin.main import Method
import time
from config.config import path_dir


class Home:
    def log_file_out(self, msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()
    def picture(self):
        driver = webdriver.Chrome()
        Login().login('http://192.168.221.20:8083/darams/a?login','test', '1234', driver)
        home_handles = driver.current_window_handle

        Method(driver).switch_out()
        Method(driver).switch_iframe(driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/home')]"))
        time.sleep(2)
        Method(driver).click('xpath','//*[@id="header_left"]')

        js = 'var aa = echarts.getInstanceByDom($("#header_left")[0]);' \
         'var option = aa.getOption();' \
         'option.series[4].data.forEach((item,index)=>{' \
         'if(item != "NaN"){' \
         'var p = {componentType:"series",name:option.xAxis[0].data[index],seriesName:"关联故障",seriesType:"line",value:option.series[4].data[index]};'\
         'skipTo(p,"百万公里故障率","CHART_MILLION_KILOMETERS_FAILURE_RATE");' \
        'throw new Error();'\
         '}'\
         '})'
        try:
            driver.execute_script(js)
        except:
            self.log_file_out('点击百万公里故障单成功')
        time.sleep(5)
        all_handle = driver.window_handles
        for i in all_handle:
         if i != home_handles:
              driver.switch_to.window(i)
              time.sleep(2)
              driver.close()


        driver.switch_to.window(home_handles)
        Method(driver).switch_out()
        Method(driver).switch_iframe(driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/home')]"))
        Method(driver).click('xpath','//*[@id="header_right"]')

        js1 = 'var aa = echarts.getInstanceByDom($("#header_right")[0]);' \
         'var option = aa.getOption();' \
         ' option.series[4].data.forEach((item,index)=>{' \
         'if( item != "NaN"){' \
         'var p = {componentType:"series",name:option.xAxis[0].data[index],seriesName:"关联故障",seriesType:"line",value:option.series[4].data[index]};'\
         'skipTo(p,"平均故障间隔里程", "CHART_AVERAGE_INTERVAL_BETWEEN_FAILURES");' \
         'throw new Error();'\
         '}' \
         '})'
        try:
            driver.execute_script(js1)
        except:
            self.log_file_out('点击平均故障图成功')
        time.sleep(5)
        all_handle1 = driver.window_handles
        for j in all_handle1:
         if j != home_handles:
              driver.switch_to.window(j)
              time.sleep(2)
              driver.close()


        driver.switch_to.window(home_handles)
        Method(driver).switch_out()
        Method(driver).switch_iframe(driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/home')]"))
        Method(driver).click('xpath','//*[@id="footer_left"]')

        js2 = 'var aa = echarts.getInstanceByDom($("#footer_left")[0]);' \
         'var option = aa.getOption();' \
         ' option.series[4].data.forEach((item,index)=>{' \
         'if( item != "NaN"){' \
         'var p = {componentType:"series",name:option.xAxis[0].data[index],seriesName:"关联故障",seriesType:"line",value:option.series[4].data[index]};'\
         'skipTo (p ,"平均修复时间", "CHART_AVERAGE_REPAIR_TIME");' \
         'throw new Error();'\
         '}' \
         '})'
        try:
            driver.execute_script(js2)
        except:
            self.log_file_out('点击平均修复时间成功')
        time.sleep(5)
        all_handle2 = driver.window_handles
        for i in all_handle2:
         if i != home_handles:
              driver.switch_to.window(i)
              time.sleep(2)
              driver.close()


        driver.switch_to.window(home_handles)
        Method(driver).switch_out()
        Method(driver).switch_iframe(driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/home')]"))
        Method(driver).click('xpath','//*[@id="footer_right"]')

        js3 = 'var aa = echarts.getInstanceByDom($("#footer_right")[0]);' \
         'var option = aa.getOption();' \
         ' option.series[4].data.forEach((item,index)=>{' \
         'if( item != "NaN"){' \
         'var p = {componentType:"series",name:option.xAxis[0].data[index],seriesName:"关联故障",seriesType:"line",value:option.series[4].data[index]};'\
         'skipTo (p ,"固有可用度", "CHART_INHERENT_AVAILABILITY");' \
        'throw new Error();'\
         '}' \
         '})'
        try:
            driver.execute_script(js3)
        except:
            self.log_file_out('点击固有可用度图表成功')
        time.sleep(5)
        all_handle3 = driver.window_handles
        for i in all_handle3:
         if i != home_handles:
              driver.switch_to.window(i)
              time.sleep(2)
              driver.close()

        driver.switch_to.window(home_handles)
        Method(driver).switch_out()
        Method(driver).switch_iframe(driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/home')]"))
        Method(driver).click('id','footer_last1')

        js4 = 'myChart5.trigger("click",{"name":"转向架开发部","componentType":"series" ,"seriesType":"bar"})'
        try:
            driver.execute_script(js4)
            self.log_file_out('点击内控指标性分析成功')
        except:
            self.log_file_out('点击内控指标分析失败')

        time.sleep(5)
        all_handle4 = driver.window_handles
        for i in all_handle4:
         if i != home_handles:
              driver.switch_to.window(i)
              time.sleep(2)
              driver.close()

        driver.switch_to.window(home_handles)
        Method(driver).switch_out()
        Method(driver).switch_iframe(driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/home')]"))
        Method(driver).click('id','footer_last2')

        js5 = 'myChart6.trigger("dblclick",{"data":{"path":"青岛亚通达铁路设备有限公司/影视信息广播系统(旅服系统)"},"componentType":"series","seriesType":"treemap"})'
        try:
            driver.execute_script(js5)
            self.log_file_out('点击供应室图表成功')
        except:
            self.log_file_out('点击供应室图表失败')
        time.sleep(5)
# var aa = echarts.getInstanceByDom($("#chart1")[0]);
# var p="";
#             var option = aa.getOption();
#             option.series[4].data.forEach((item,index)=>{
#             if(item != "NaN"){
#             p = {componentType:"series",name:option.xAxis[0].data[index],seriesName:"关联故障",seriesType:"line",value:option.series[4].data[index]};
#              }
#              })
# 			skipTo(p,"百万公里故障率","CHART_MILLION_KILOMETERS_FAILURE_RATE");

Home().picture()