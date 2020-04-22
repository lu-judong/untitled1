from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from config.log_config import logger
import time
from bin.main import Method
from bin.login import Login
from new_selenium.tech_rams.rams_config import *
from config.config import path_dir



class Tech:
    def log_file_out(self, msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    def tech_fault_analysis(self,url,value,start,end,car,fault,time_sleep,wait_time):
        #
        # option = webdriver.ChromeOptions()
        # option.add_argument("headless")
        # driver = webdriver.Chrome(chrome_options=option,
        #                           executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')
        driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
        Login().login(url,'test','1234',driver)

        self.log_file_out('-----临时数据库-----')

        for i in contents:
            try:
                Method(driver).contains_xpath('click',i)
                self.log_file_out('点击'+i+'成功')
            except Exception as e:
                logger.debug(e)
                self.log_file_out('点击' + i + '失败')
        js_s = " return $('#switchDb').prop('checked')"
        status = driver.execute_script(js_s)
        if status is True:
            Method(driver).click('class', 'onoffswitch-label')
        else:
            time.sleep(1)

        time.sleep(2)
        try:
            Method(driver).switch_out()
            Method(driver).switch_iframe(
                driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/disposableModel/form')]"))
            time.sleep(time_sleep)
        except NoSuchElementException as e:
            self.log_file_out('切入iframe失败')

        try:
            Method(driver).select_down_list('id', 'modelObject', value)
            Method(driver).input('id', 'confMileageList0_startMileage', start)
            Method(driver).input('id', 'confMileageList0_endMileage', end)


        except NoSuchElementException as e:
            print('模型基本信息输入失败')
        except:
            print('请录入评估对象')
            return

        try:
            Method(driver).contains_xpath('click','新增')
        except NoSuchElementException as e:
            print('点击新建按钮失败')

        try:
            Method(driver).switch_out()
            b = Method(driver).get_attr('css',"[class='layui-layer layui-layer-iframe my-skin']", 'times')
            Method(driver).switch_iframe('layui-layer-iframe' + b)
        except:
            print('请录入评估对象')
            return

        time.sleep(time_sleep)

        # 车型 车号新增页面
        Method(driver).click('id','partType')

        try:
            for x in car:
                driver.find_element_by_xpath(
                    "//span[@class='train zoomIn' and contains(text(),\'{}\')]".format(x)).click()
                car_num = car.get(x)
                time.sleep(2)
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
            # 这个可以点击得元素失去焦点
            # Message: unknown error: Element <a class="layui-layer-btn1">...</a> is not clickable at point (975, 498). Other element would receive the click: <a class="layui-layer-btn3">...</a>
            # Method(driver).two_element_click("[class='layui-layer-btn layui-layer-btn-']",'layui-layer-btn1')
            Method(driver).two_element_click("[class='layui-layer layui-layer-iframe my-skin']", 'layui-layer-btn1')
            self.log_file_out('选车成功')
        except NoSuchElementException as e:
            logger.error('xpath' + '不存在!')
            self.log_file_out('选车失败')


        # 故障模式选择页面
        Method(driver).switch_out()
        c = Method(driver).get_attr('css',"[class='layui-layer layui-layer-iframe my-skin']", 'times')
        Method(driver).switch_iframe('layui-layer-iframe' + c)
        time.sleep(time_sleep)
        try:
            for key in fault:
                if type(fault[key]).__name__ == 'dict':
                    fault_next_1 = Method(driver).contains_xpath('get', key)
                    Method(driver).click('xpath', '//*[@id= \'{}\']/i'.format(fault_next_1[:-7]))

                    # 取出第二个子节点中的值
                    for i in fault[key]:
                        if type(fault[key][i]).__name__ == 'dict':
                            fault_next_2 = Method(driver).contains_xpath('get',i)
                            Method(driver).click('xpath', '//*[@id= \'{}\']/i'.format(fault_next_2[:-7]))

                            # 取出第三个子节点的值
                            for m in fault[key][i]:
                                if type(fault[key][i][m]).__name__ == 'dict':
                                    fault_next_3 = Method(driver).contains_xpath('get', m)
                                    Method(driver).click('xpath', '//*[@id= \'{}\']/i'.format(fault_next_3[:-7]))
                                    # 取出第四个子节点的值
                                    for j in fault[key][i][m]:
                                        if fault[key][i][m][j] == 'all':
                                            Method(driver).click('xpath', '//*[text()=\'{}\']'.format(j))
                                            Method(driver).click('name', 'btSelectAll')
                                            Method(driver).click('xpath', '//*[@id="right-move"]')
                                        else:
                                            fault_next_4 = Method(driver).contains_xpath('get', j)
                                            Method(driver).click('xpath',
                                                                 '//*[@id= \'{}\']/i'.format(fault_next_4[:-7]))
                                            time.sleep(time_sleep)
                                            for p in fault[key][i][m][j]:
                                                driver.find_element_by_xpath(
                                                    "//td[contains(text(),\'{}\')]/../td[1]/input".format(p)).click()
                                                Method(driver).click('xpath', '//*[@id="right-move"]')

                                else:
                                    Method(driver).click('xpath', '//*[text()=\'{}\']'.format(m))
                                    time.sleep(time_sleep)
                                    if fault[key][i][m] == 'all':
                                        Method(driver).click('name', 'btSelectAll')
                                        Method(driver).click('xpath', '//*[@id="right-move"]')
                                    else:
                                        for k in fault[key][i][m]:
                                            driver.find_element_by_xpath(
                                                "//td[contains(text(),\'{}\')]/../td[1]/input".format(k)).click()
                                        Method(driver).click('xpath', '//*[@id="right-move"]')
                        else:
                            Method(driver).click('xpath', '//*[text()=\'{}\']'.format(i))
                            time.sleep(time_sleep)
                            if fault[key][i] == 'all':
                                Method(driver).click('name', 'btSelectAll')
                                Method(driver).click('xpath', '//*[@id="right-move"]')
                            else:
                                for n in fault[key][i]:
                                    driver.find_element_by_xpath(
                                        "//td[contains(text(),\'{}\')]/../td[1]/input".format(n)).click()
                                    time.sleep(time_sleep)
                                Method(driver).click('xpath', '//*[@id="right-move"]')

                else:
                    Method(driver).click('xpath','//*[text()=\'{}\']'.format(key))
                    time.sleep(time_sleep)
                    if fault[key] == 'all':
                        Method(driver).click('name','btSelectAll')
                        Method(driver).click('xpath', '//*[@id="right-move"]')
                    else:
                        for i in fault[key]:
                            # WebDriverWait(driver, 10).until(EC.element_to_be_clickable(By.XPATH, "//td[contains(text(),\'{}\')]/../td[1]/input".format(i))).click()
                            driver.find_element_by_xpath("//td[contains(text(),\'{}\')]/../td[1]/input".format(i)).click()
                        Method(driver).click('xpath','//*[@id="right-move"]')
            self.log_file_out('故障模型选择成功')
        except NoSuchElementException as e:
            logger.error('xpath'+'不存在!')
            self.log_file_out('故障模型选择失败')

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
            Method(driver).click('id','tab-1-btn1')
        except:
            self.log_file_out('请输入正确的模型')
            return

        try:
            js = 'var aa = echarts.getInstanceByDom($("#tab1chart1")[0]);' \
                 'var option = aa.getOption();' \
                 'var c = option.series[4].data[1];' \
                 'return c'
            value_js = driver.execute_script(js)
        except:
            self.log_file_out('点击图表失败')

        Method(driver).switch_out()
        Method(driver).click('class', 'layui-layer-close')

        time.sleep(2)
        Method(driver).switch_out()
        try:
            Method(driver).click('xpath','//*[@id="btnImportFault"]/i')
            time.sleep(2)
            driver.find_element_by_id("fileInput").send_keys("{}/tech_login/临时数据库1.xlsx".format(path_dir))
            Method(driver).click('class','layui-layer-btn0')
            Method(driver).click('class','onoffswitch-switch')
            self.log_file_out('导入故障单成功')
        except NoSuchElementException as e:
            self.log_file_out('导入故障单失败')

        time.sleep(4)
        try:
            Method(driver).switch_out()
            Method(driver).switch_iframe(
                driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/mould/disposableModel/form')]"))
            self.log_file_out('切换数据源后,再一次切入iframe成功')

        except:
            self.log_file_out('切换数据源后,再一次切入iframe失败')

        time.sleep(2)
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
            Method(driver).click('id', 'tab-1-btn1')
        except:
            self.log_file_out('请输入正确的模型')
            return

        try:
            js1 = 'var aa = echarts.getInstanceByDom($("#tab1chart1")[0]);' \
                 'var option = aa.getOption();' \
                 'var d = option.series[4].data[1];' \
                 'return d'
            value_js1 = driver.execute_script(js1)
        except:
            self.log_file_out('点击图表失败')

        if float(value_js) == float(value_js1):
            self.log_file_out('临时数据库验证失败')
        else:
            self.log_file_out('临时数据库验证成功')




url = 'http://192.168.1.20:8083/darams/a?login'
car = {'E27':['2641', '2642', '2643', '2644', '2645', '2646', '2647']}

fault_pattern = {'高压供电系统':'all'}

time_sleep = 3
wait_time = 10


Tech().tech_fault_analysis(url,3,'0','100',car,fault_pattern,time_sleep,wait_time)
