# js = 'var aa = echarts.getInstanceByDom($("#tab-1-chart1")[0]);' \
#               'var option = aa.getOption();' \
#               ' option.series[3].data.forEach((item,index)=>{' \
#               'if( item != "NaN"){' \
#               'var param = {componentType:"series",name:option.xAxis[0].data[index],seriesName:"关联故障",seriesType:"line",value:option.series[3].data[index]};' \
#               'var lineType = param.seriesName, x = param.name, y = param.value;' \
#               '''var faultIds = globalDataSet["tab-1-chart1"][lineType][x][y].faultIds.split(',');''' \
#               "if (faultIds != null && faultIds != '' && faultIds.length > 0) {" \
#               'skipToFautlOrder(faultIds);' \
#               'return false;' \
#               '}}})'
#
# print(js)
import json
from new_selenium.bin.login import Login
import time
from selenium import  webdriver
from new_selenium.bin.main import Method

url = 'http://192.168.1.115:8080/darams/a?login'

driver = webdriver.Chrome()
Login().login(url, 'test', '1234', driver)
# time.sleep(5)
# headers = {'Cookie': 'jeeplus.session.id=797ecc31d2344443b1b73269ca988730000; JSESSIONID=F2D1636B5EFE87CEE1C37F520522B9FB; pageNo=1; pageSize=10'}

js1 = driver.get('http://192.168.1.115:8080/darams/a/home/option5')
# print(eval(json.dumps(js1.text)).get('options'))
# print(js1)
js_=" return a=eval(({}))".format(driver.find_element_by_xpath("//pre").text)

a =  driver.execute_script(js_)
driver.close()
# print(a.get('options')[0].get('series')[0].get('data'))
# print(len(a.get('options')))
L  = ''
for i in range(0,len(a.get('options'))):
    for j in a.get('options')[i].get('series')[0].get('data'):
        if j.get('value') != 0:
            L = [j.get('name'),a.get('options')[i].get('title').get('text')]
            break
print(L)
date = L[1][0:7]
month = date[-2:]
if int(month) < 12:
    lastmonth = date[0:5] + str(int(month) + 1)
else:
    lastmonth = str(int(date[0:4])+1) + '-1'
print(type(lastmonth),month,type(date))

print(L[1][5:7])

time.sleep(2)
driver = webdriver.Chrome()
Login().login(url, 'test', '1234', driver)

Method(driver).switch_out()
Method(driver).switch_iframe(driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/home')]"))

home_handles = driver.current_window_handle

Method(driver).click('id', 'footer_last1')
js_e1 = 'myChart5.trigger("click",{{"name": "{}","componentType":"series" ,"seriesType":"bar"}})'.format(L[0])

driver.execute_script(js_e1)

all_handle4 = driver.window_handles
for i in all_handle4:
    if i != home_handles:
        driver.switch_to.window(i)


status_ee = driver.execute_script(
    'return $("#opFaultOrderTable").bootstrapTable("getData").map(function(row){return $(row).attr("mainResponsibility")}).some(function(item){return item !="技术中心"})')

if status_ee is False:
    print('责任部室验证正确')
else:
    print('责任部室验证不正确')
time.sleep(2)
status_ff = driver.execute_script(
    'return $("#opFaultOrderTable").bootstrapTable("getData").map(function(row){return $(row).attr("occurrenceTime")}).some(function(item){return new Date(item).valueOf() >= new Date(\'%s\').valueOf() && new Date(item).valueOf() <= new Date(\'%s\').valueOf()})'% (lastmonth,date))


if status_ff is False:
    print('责任部室验证正确')
else:
    print('责任部室验证不正确')