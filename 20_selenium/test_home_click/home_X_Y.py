from selenium import  webdriver
from bin.login import Login
from bin.main import Method
import time
from config.config import path_dir


class Home:
    def log_file_out(self,msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    def X_Y(self,url,username,password):

        driver = webdriver.Chrome()
        Login().login(url,username, password, driver)

        self.log_file_out('----首页X,Y轴-----')
        Method(driver).switch_out()
        Method(driver).switch_iframe(driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/home')]"))

        home_handles = driver.current_window_handle
        time.sleep(2)
        Method(driver).click('id','header_left')
        js_a = 'var aa = echarts.getInstanceByDom($("#header_left")[0]);' \
             'var option = aa.getOption(); ' \
            'a = option.series[0].data.length;' \
            'return a'
        x_a_before = driver.execute_script(js_a)

        js_b = 'var aa = echarts.getInstanceByDom($("#header_right")[0]);' \
               'var option = aa.getOption(); ' \
               'a = option.series[0].data.length;' \
               'return a'
        x_b_before = driver.execute_script(js_b)

        js_c = 'var aa = echarts.getInstanceByDom($("#footer_left")[0]);' \
               'var option = aa.getOption(); ' \
               'a = option.series[0].data.length;' \
               'return a'
        x_c_before = driver.execute_script(js_c)

        js_d = 'var aa = echarts.getInstanceByDom($("#footer_right")[0]);' \
               'var option = aa.getOption(); ' \
               'a = option.series[0].data.length;' \
               'return a'
        x_d_before = driver.execute_script(js_d)

        Method(driver).select_down_list('xpath','//*[@id="header"]/div[2]/div[2]/select[1]',1)
        js_a1 = 'var aa = echarts.getInstanceByDom($("#header_left")[0]);' \
             'var option = aa.getOption(); ' \
             'a = option.series[0].data.length;' \
             'return a'

        time.sleep(4)
        if x_a_before != driver.execute_script(js_a1) + 2 -1:
            self.log_file_out('百万公里X轴间隔不正确')
        else:
            self.log_file_out('百万公里X轴间隔正确')

        time.sleep(3)
        Method(driver).select_down_list('xpath', '//*[@id="header"]/div[2]/div[2]/select[2]', 2)
        js_a2 = 'var aa = echarts.getInstanceByDom($("#header_left")[0]);' \
             'var option = aa.getOption(); ' \
             'a = option.xAxis[0].axisLabel.interval;' \
             'return a'
        time.sleep(1)
        if driver.execute_script(js_a2) != 2:
            self.log_file_out('百万公里X轴显示跨度不正确')
        else:
            self.log_file_out('百万公里X轴显示跨度正确')

        js_a5 = 'var aa = echarts.getInstanceByDom($("#header_left")[0]);'\
             'var bb = [] ;'\
             'var option = aa.getOption();'\
             'for(let i in option.series[4].data){'\
             'if (option.series[4].data[i] != "NaN"){'\
             'var p = {componentType:"series",name:option.xAxis[0].data[i],seriesName:"关联故障",seriesType:"line",          value:option.series[4].data[i]};' \
             'bb = [p.name,option.xAxis[0].data[i-1]];'\
             'skipTo(p,"百万公里故障率","CHART_MILLION_KILOMETERS_FAILURE_RATE");'\
             'break'\
             '}' \
             '}' \
             'return bb'
        try:
            value = driver.execute_script(js_a5)
            self.log_file_out('点击百万公里故障单成功')
        except:
            self.log_file_out('点击百万公里故障单失败')

        time.sleep(3)
        all_handle = driver.window_handles
        for i in all_handle:
            if i != home_handles:
                driver.switch_to.window(i)
        status_aa = driver.execute_script(
            ' return $("#opFaultOrderTable").bootstrapTable("getData").map(function(row){return $(row).attr("occurrenceTime")}).some(function(item){return new Date(item).valueOf() >= new Date(\'%s\').valueOf() &&new Date(item).valueOf() <= new Date(\'%s\').valueOf()})' % (value[0],value[1]))

        if status_aa is False:
            self.log_file_out('百万公里故障单验证成功')
        else:
            self.log_file_out('百万公里故障单验证失败')
        for i in all_handle:
            if i != home_handles:
                driver.close()
        driver.switch_to.window(home_handles)

        Method(driver).switch_out()
        Method(driver).switch_iframe(driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/home')]"))
        time.sleep(2)
        Method(driver).input('id','y1max',8)
        time.sleep(1)
        Method(driver).click('xpath','//*[@id="header"]/div[2]/div[2]/button')
        time.sleep(1)
        js_a3 = 'var aa = echarts.getInstanceByDom($("#header_left")[0]);' \
              'var option = aa.getOption();' \
              'a = option.yAxis[0].max;' \
              'return a '
        if driver.execute_script(js_a3) != 8:
            self.log_file_out('百万公里Y轴最大值不正确')
        else:
            self.log_file_out('百万公里Y轴最大值正确')

        Method(driver).input('id','y1min',2)
        time.sleep(1)
        Method(driver).click('xpath', '//*[@id="header"]/div[2]/div[2]/button')
        time.sleep(1)
        js_a4 = 'var aa = echarts.getInstanceByDom($("#header_left")[0]);' \
              'var option = aa.getOption();' \
              'a = option.yAxis[0].min;' \
              'return a '
        if driver.execute_script(js_a4) != 2:
            self.log_file_out('百万公里Y轴最小值不正确')
        else:
            self.log_file_out('百万公里Y轴最小值正确')

        time.sleep(1)

        Method(driver).click('id','header_right')


        js_b1 = 'var aa = echarts.getInstanceByDom($("#header_right")[0]);' \
             'var option = aa.getOption(); ' \
             'a = option.series[0].data.length;' \
             'return a'

        if x_b_before != driver.execute_script(js_b1) + 2 -1:
            self.log_file_out('平均故障X轴间隔不正确')
        else:
            self.log_file_out('平均故障X轴间隔正确')

        time.sleep(3)

        js_b2 = 'var aa = echarts.getInstanceByDom($("#header_right")[0]);' \
             'var option = aa.getOption(); ' \
             'a = option.xAxis[0].axisLabel.interval;' \
             'return a'

        if driver.execute_script(js_b2) != 2:
            self.log_file_out('平均故障X轴显示跨度不正确')
        else:
            self.log_file_out('平均故障X轴显示跨度正确')

        time.sleep(3)
        js_b5 = 'var aa = echarts.getInstanceByDom($("#header_right")[0]);' \
              'var option = aa.getOption();' \
             'var bb =[];' \
              'for(let i in option.series[4].data){' \
              'if (option.series[4].data[i] != "NaN"){' \
              'var p = {componentType:"series",name:option.xAxis[0].data[i],seriesName:"关联故障",seriesType:"line",value:option.series[4].data[i]};' \
              'bb = [p.name,option.xAxis[0].data[i-1]];'\
              'skipTo(p,"平均故障间隔里程", "CHART_AVERAGE_INTERVAL_BETWEEN_FAILURES");' \
              'break' \
              '}' \
              '}' \
             'return bb'
        try:
            value1 = driver.execute_script(js_b5)
            self.log_file_out('点击平均故障故障单成功')
        except:
            self.log_file_out('点击平均故障故障单失败')

        time.sleep(3)
        all_handle1 = driver.window_handles
        for i in all_handle1:
            if i != home_handles:
                driver.switch_to.window(i)
        status_aa = driver.execute_script(
            ' return $("#opFaultOrderTable").bootstrapTable("getData").map(function(row){return $(row).attr("occurrenceTime")}).some(function(item){return new Date(item).valueOf() >= new Date(\'%s\').valueOf() &&new Date(item).valueOf() <= new Date(\'%s\').valueOf()})' % (
            value1[0], value1[1]))

        if status_aa is False:
            self.log_file_out('平均故障故障单验证成功')
        else:
            self.log_file_out('平均故障故障单验证失败')
        for i in all_handle1:
            if i != home_handles:
                driver.close()
        driver.switch_to.window(home_handles)

        Method(driver).switch_out()
        Method(driver).switch_iframe(driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/home')]"))
        time.sleep(2)
        Method(driver).input('id','y2max',800000)
        time.sleep(1)
        Method(driver).click('xpath','//*[@id="header"]/div[3]/div[2]/button')
        time.sleep(1)
        js_b3 = 'var aa = echarts.getInstanceByDom($("#header_right")[0]);' \
              'var option = aa.getOption();' \
              'a = option.yAxis[0].max;' \
              'return a '
        if driver.execute_script(js_b3) != 800000:
            self.log_file_out('平均故障Y轴最大值不正确')
        else:
            self.log_file_out('平均故障Y轴最大值正确')

        Method(driver).input('id','y2min',100000)
        time.sleep(1)
        Method(driver).click('xpath', '//*[@id="header"]/div[3]/div[2]/button')
        time.sleep(1)
        js_b4 = 'var aa = echarts.getInstanceByDom($("#header_right")[0]);' \
              'var option = aa.getOption();' \
              'a = option.yAxis[0].min;' \
              'return a '
        if driver.execute_script(js_b4) != 100000:
            self.log_file_out('平均故障Y轴最小值不正确')
        else:
            self.log_file_out('平均故障Y轴最小值正确')
        time.sleep(1)

        Method(driver).click('id', 'footer_left')

        js_c1 = 'var aa = echarts.getInstanceByDom($("#footer_left")[0]);' \
                'var option = aa.getOption(); ' \
                'a = option.series[0].data.length;' \
                'return a'

        if x_c_before != driver.execute_script(js_c1) + 2 - 1:
            self.log_file_out('平均修复时间X轴间隔不正确')
        else:
            self.log_file_out('平均修复时间X轴间隔正确')

        time.sleep(3)

        js_c2 = 'var aa = echarts.getInstanceByDom($("#footer_left")[0]);' \
                'var option = aa.getOption(); ' \
                'a = option.xAxis[0].axisLabel.interval;' \
                'return a'

        if driver.execute_script(js_c2) != 2:
            self.log_file_out('平均修复X轴显示跨度不正确')
        else:
            self.log_file_out('平均修复X轴显示跨度正确')
        js_c5 ='var aa = echarts.getInstanceByDom($("#footer_left")[0]);' \
              'var option = aa.getOption();' \
              'var bb = [];' \
              'for(let i in option.series[4].data){' \
              'if (option.series[4].data[i] != "NaN"){' \
              'var p = {componentType:"series",name:option.xAxis[0].data[i],seriesName:"关联故障",seriesType:"line",value:option.series[4].data[i]};' \
              'bb = [p.name,option.xAxis[0].data[i-1]];'\
              'skipTo (p ,"平均修复时间", "CHART_AVERAGE_REPAIR_TIME");' \
              'break' \
              '}' \
              '}' \
              'return bb'
        try:
            value2 = driver.execute_script(js_c5)
            self.log_file_out('点击平均修复时间故障单成功')
        except:
            self.log_file_out('点击平均修复时间故障单失败')

        time.sleep(3)
        all_handle2 = driver.window_handles
        for i in all_handle2:
            if i != home_handles:
                driver.switch_to.window(i)
        status_aa = driver.execute_script(
            ' return $("#opFaultOrderTable").bootstrapTable("getData").map(function(row){return $(row).attr("occurrenceTime")}).some(function(item){return new Date(item).valueOf() >= new Date(\'%s\').valueOf() &&new Date(item).valueOf() <= new Date(\'%s\').valueOf()})' % (
                value2[0], value2[1]))

        if status_aa is False:
            self.log_file_out('平均修复时间故障单验证成功')
        else:
            self.log_file_out('平均修复时间故障单验证失败')
        for i in all_handle2:
            if i != home_handles:
                driver.close()
        driver.switch_to.window(home_handles)

        Method(driver).switch_out()
        Method(driver).switch_iframe(driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/home')]"))
        time.sleep(3)

        Method(driver).input('id', 'y3max', 4)
        time.sleep(1)
        Method(driver).click('xpath', '//*[@id="footer"]/div[1]/div[2]/button')
        time.sleep(1)
        js_c3 = 'var aa = echarts.getInstanceByDom($("#footer_left")[0]);' \
                'var option = aa.getOption();' \
                'a = option.yAxis[0].max;' \
                'return a '
        if driver.execute_script(js_c3) != 4:
            self.log_file_out('平均修复Y轴最大值不正确')
        else:
            self.log_file_out('平均修复Y轴最大值正确')

        Method(driver).input('id', 'y3min', 1)
        time.sleep(1)
        Method(driver).click('xpath', '//*[@id="footer"]/div[1]/div[2]/button')
        time.sleep(1)
        js_c4 = 'var aa = echarts.getInstanceByDom($("#footer_left")[0]);' \
                'var option = aa.getOption();' \
                'a = option.yAxis[0].min;' \
                'return a '
        if driver.execute_script(js_c4) != 1:
            self.log_file_out('平均修复Y轴最小值不正确')
        else:
            self.log_file_out('平均修复Y轴最小值正确')

        Method(driver).click('id', 'footer_right')

        js_d1 = 'var aa = echarts.getInstanceByDom($("#footer_right")[0]);' \
              'var option = aa.getOption(); ' \
              'a = option.series[0].data.length;' \
              'return a'

        if x_d_before != driver.execute_script(js_d1) + 2 - 1:
            self.log_file_out('固有可用度X轴间隔不正确')
        else:
            self.log_file_out('固有可用度X轴间隔正确')

        time.sleep(3)

        js_d2 = 'var aa = echarts.getInstanceByDom($("#footer_right")[0]);' \
              'var option = aa.getOption(); ' \
              'a = option.xAxis[0].axisLabel.interval;' \
              'return a'

        if driver.execute_script(js_d2) != 2:
            self.log_file_out('固有可用度X轴显示跨度不正确')
        else:
            self.log_file_out('固有可用度X轴显示跨度正确')

        js_d5 = 'var aa = echarts.getInstanceByDom($("#footer_right")[0]);' \
              'var option = aa.getOption();' \
              'var bb = [] ;' \
              'for(let i in option.series[4].data){' \
              'if (option.series[4].data[i] != "NaN"){' \
              'var p = {componentType:"series",name:option.xAxis[0].data[i],seriesName:"关联故障",seriesType:"line",value:option.series[4].data[i]};' \
              'bb = [p.name,option.xAxis[0].data[i-1]];' \
              'skipTo (p ,"固有可用度", "CHART_INHERENT_AVAILABILITY");' \
              'break' \
              '}' \
              '}' \
              'return bb'
        try:
            value2 = driver.execute_script(js_d5)
            self.log_file_out('点击固有可用度故障单成功')
        except:
            self.log_file_out('点击固有可用度故障单失败')

        time.sleep(3)
        all_handle3 = driver.window_handles
        for i in all_handle3:
            if i != home_handles:
                driver.switch_to.window(i)
        status_aa = driver.execute_script(
            ' return $("#opFaultOrderTable").bootstrapTable("getData").map(function(row){return $(row).attr("occurrenceTime")}).some(function(item){return new Date(item).valueOf() >= new Date(\'%s\').valueOf() &&new Date(item).valueOf() <= new Date(\'%s\').valueOf()})' % (
                value2[0], value2[1]))

        if status_aa is False:
            self.log_file_out('固有可用度故障单验证成功')
        else:
            self.log_file_out('固有可用度故障单验证失败')
        for i in all_handle3:
            if i != home_handles:
                driver.close()
        driver.switch_to.window(home_handles)

        Method(driver).switch_out()
        Method(driver).switch_iframe(driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/home')]"))

        time.sleep(3)

        Method(driver).input('id', 'y4max', 4)
        time.sleep(1)
        Method(driver).click('xpath', '//*[@id="footer"]/div[2]/div[2]/button')
        time.sleep(1)
        js_d3 = 'var aa = echarts.getInstanceByDom($("#footer_right")[0]);' \
              'var option = aa.getOption();' \
              'a = option.yAxis[0].max;' \
              'return a '
        if driver.execute_script(js_d3) != 4:
            self.log_file_out('固有可用度Y轴最大值不正确')
        else:
            self.log_file_out('固有可用度Y轴最大值正确')

        Method(driver).input('id', 'y4min', 1)
        time.sleep(1)
        Method(driver).click('xpath', '//*[@id="footer"]/div[2]/div[2]/button')
        time.sleep(1)
        js_d4 = 'var aa = echarts.getInstanceByDom($("#footer_right")[0]);' \
              'var option = aa.getOption();' \
              'a = option.yAxis[0].min;' \
              'return a '
        if driver.execute_script(js_d4) != 1:
            self.log_file_out('固有可用度Y轴最小值不正确')
        else:
            self.log_file_out('固有可用度Y轴最小值正确')

        driver.get('http://192.168.221.20:8083/darams/a/home/option5')
        js_ = " return a=eval(({}))".format(driver.find_element_by_xpath("//pre").text)
        a = driver.execute_script(js_)
        driver.close()
        L = ''
        for i in range(0, len(a.get('options'))):
            for j in a.get('options')[i].get('series')[0].get('data'):
                if j.get('value') != 0:
                    L = [j.get('name'), a.get('options')[i].get('title').get('text')]
                    break

        date = L[1][0:7]
        month = date[-2:]
        if int(month) < 12:
            lastmonth = date[0:5] + str(int(month) + 1)
        else:
            lastmonth = str(int(date[0:4]) + 1) + '-1'


        time.sleep(2)
        driver = webdriver.Chrome()
        Login().login(url, 'test', '1234', driver)

        Method(driver).switch_out()
        Method(driver).switch_iframe(driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/home')]"))

        home_handles1 = driver.current_window_handle

        Method(driver).click('id', 'footer_last1')
        js_e1 = 'myChart5.trigger("click",{{"name": "{}","componentType":"series" ,"seriesType":"bar"}})'.format(L[0])

        driver.execute_script(js_e1)

        all_handle4 = driver.window_handles
        for i in all_handle4:
            if i != home_handles1:
                driver.switch_to.window(i)

        status_ee = driver.execute_script(
            'return $("#opFaultOrderTable").bootstrapTable("getData").map(function(row){return $(row).attr("mainResponsibility")}).some(function(item){return item !="技术中心"})')

        if status_ee is False:
            self.log_file_out('责任部室验证正确')
        else:
            self.log_file_out('责任部室验证不正确')
        time.sleep(2)
        status_ff = driver.execute_script(
            'return $("#opFaultOrderTable").bootstrapTable("getData").map(function(row){return $(row).attr("occurrenceTime")}).some(function(item){return new Date(item).valueOf() >= new Date(\'%s\').valueOf() && new Date(item).valueOf() <= new Date(\'%s\').valueOf()})' % (
            lastmonth, date))

        if status_ff is False:
            self.log_file_out('责任部室时间验证正确')
        else:
            self.log_file_out('责任部室时间验证不正确')


        for i in all_handle4:
            if i != home_handles1:
                driver.close()
        time.sleep(2)
        driver.switch_to.window(home_handles1)
        Method(driver).switch_out()
        Method(driver).switch_iframe(driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/home')]"))
        Method(driver).click('id', 'footer_last2')

        value_com = driver.execute_script('var aa = echarts.getInstanceByDom($("#footer_last2")[0]);' \
                                          'var option = aa.getOption();' \
                                          'return [option.series[0].data[0].value[0]]')

        js_f1 = 'myChart6.trigger("dblclick",{"data":{"path":"苏州华兴致远电子科技有限公司"},"componentType":"series","seriesType":"treemap"})'

        try:
            driver.execute_script(js_f1)
            self.log_file_out('点击供应商内控指标图表成功')
        except:
            self.log_file_out('点击供应商内控指标图表失败')
        time.sleep(2)
        all_handle7 = driver.window_handles
        for i in all_handle7:
            if i != home_handles1:
                driver.switch_to.window(i)

        driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div[1]/div[2]/button[1]').click()
        time.sleep(10)
        # for i in range(0,len(driver.find_elements_by_xpath('//*[@id="opFaultOrderTable"]/tbody/tr/td[12]'))):
        #     print(driver.find_elements_by_xpath('//*[@id="opFaultOrderTable"]/tbody/tr/td[12]')[i].text)
        status_aa = driver.execute_script(
            'return $("#opFaultOrderTable").bootstrapTable("getData").map(function(row){return $(row).attr("mainResponsibility")}).some(function(item){return item !="苏州华兴致远电子科技有限公司"})')

        value_com1 = driver.execute_script(
            'return $("#opFaultOrderTable").bootstrapTable("getData").map(function(row){return $(row).attr("mainResponsibility")}).length')
        if status_aa is False and value_com[0] == value_com1:
            self.log_file_out('主要责任单位数值正确')
        else:
            self.log_file_out('主要责任单位数值不正确')


url = 'http://192.168.221.20:8083/darams/a?login'

Home().X_Y(url, 'test', '1234')