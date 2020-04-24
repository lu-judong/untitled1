from selenium import webdriver
from interfaceTest.config.main import *
import requests
import json
import ddt
from interfaceTest.libext.HTMLTestRunner import *
from interfaceTest.config.config import *


@ddt.ddt
class test_trainDataClear(unittest.TestCase):

    @classmethod
    def setUpClass(cls):  # 类中最先执行
        cls.path = '{}/testOutput/interface-sheet.xls'.format(path_dir)
        # create_sheet(cls.path)
        cls.driver = webdriver.Chrome()

        cls.driver.maximize_window()
        cls.driver.get(interface_url + '/darams/doc.html')
        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        # cls.driver = driver# 类中最后执行
        cls.driver.quit()

    @ddt.file_data('{}/testInput/test_ramsEvaluate_input/test_1_login.json'.format(path_dir))
    def test_1_login(self, username, password):
        # """登录接口"""
        try:
            # f = open('')

            driver = self.driver
            driver.refresh()

            time.sleep(2)
            # 点击搜索

            Method(driver).click('xpath', '//span[contains(text(),"登录管理")]')
            time.sleep(1)

            # 点击登录
            driver.find_element_by_xpath('//span[text()="登录"]').click()
            time.sleep(1)
            # 获取登录接口的地址
            login_interface_url = driver.find_element_by_xpath('//span[text()="接口地址"]/../code').text

            # 访问登录接口,拿到登录校验
            login_send = requests.post(interface_url + login_interface_url,
                                       data={'username': '{}'.format(username), 'password': '{}'.format(password)})
            login_response = json.loads(login_send.text)
            path = self.path
            url = interface_url + login_interface_url
            params = json.dumps({'username': '{}'.format(username), 'password': '{}'.format(password)})
            if login_send.status_code == 200:
                # 得到登录接口的返回
                if login_response['success'] is True:
                    globals()["Authorization"] = login_response['result']
                    self.assertEqual(4, 4)
                else:
                    globals()["Authorization"] = {}

                    if 'result' in login_response.keys():
                        result = login_response['result']
                        del login_response['result']

                        write_sheet(path, '登录接口', url, params, json.dumps(login_response, ensure_ascii=False),
                                    json.dumps(result, ensure_ascii=False))
                    else:
                        write_sheet(path, '登录接口', url, params, json.dumps(login_response, ensure_ascii=False), '')
                    self.assertEqual(3, 4)
            else:
                globals()["Authorization"] = {}

                write_sheet(path, '登录接口', url, params, '登录接口返回:{}'.format(login_send.status_code), '')

                self.assertEqual(3, 4)
        except AssertionError:
            logger.error(AssertionError)
            self.assertEqual(3, 4)

    @ddt.file_data('{}/testInput/test_trainDataClear_input/test_2_trainDataClearData.json'.format(path_dir))
    def test_2_trainDataClearData(self,startDate,endDate,trainNo):
        """列车数据清洗列表数据"""
        path = self.path
        if len(globals()["Authorization"]) == 0:
            write_sheet(path, '列车数据清洗列表数据接口', '', '', '用户未登录', '')
            self.assertEqual(3, 4)
        else:
            try:
                driver = self.driver
                driver.refresh()
                time.sleep(2)
                Method(driver).click('xpath', '//span[contains(text(),"列车数据清洗")]')
                time.sleep(1)
                Method(driver).circle_click('列车数据清洗列表数据')

                # 获取接口的地址
                trainDataClear_interface_url = driver.find_element_by_xpath(
                    '//span[text()="接口地址"]/../code').text

                body = {
                    "startDate": "{}".format(startDate), "endDate": "{}".format(endDate),"trainNo":"{}".format(trainNo)
                }

                # 请求保存接口
                trainDataClear_send = requests.post(interface_url + trainDataClear_interface_url,
                                                               headers={
                                                                   "Authorization": globals()["Authorization"][
                                                                       "Authorization"],
                                                                   "Content-Type": "application/json;charset=UTF-8"},
                                                               params=body)
                trainDataClear_response = json.loads(trainDataClear_send.text)
                url = interface_url + trainDataClear_interface_url
                params = json.dumps(body, ensure_ascii=False)

                if trainDataClear_send.status_code == 200:
                    if trainDataClear_response['success'] is True:
                        self.assertEqual(4, 4)
                    else:
                        if 'result' in trainDataClear_response.keys():
                            result = trainDataClear_response['result']
                            del trainDataClear_response['result']

                            write_sheet(path, '列车数据清洗列表数据接口', url, params,
                                        json.dumps(trainDataClear_response, ensure_ascii=False),
                                        json.dumps(result))
                        else:
                            write_sheet(path, '列车数据清洗列表数据接口', url, params,
                                        json.dumps(trainDataClear_response, ensure_ascii=False), '')

                        self.assertEqual(3, 4)
                else:
                    write_sheet(path, '列车数据清洗列表数据接口', url, params,
                                '列车数据清洗列表数据接口返回'.format(trainDataClear_response.status_code), '')

                    self.assertEqual(3, 4)
            except AssertionError:
                logger.error(AssertionError)
                self.assertEqual(3, 4)

    @ddt.file_data('{}/testInput/test_trainDataClear_input/test_3_trainDataClearChart.json'.format(path_dir))
    def test_2_trainDataClearChart(self, startDate, endDate, trainNo):
        """列车数据清洗列表数据图"""
        path = self.path
        if len(globals()["Authorization"]) == 0:
            write_sheet(path, '列车数据清洗列表数据图接口', '', '', '用户未登录', '')
            self.assertEqual(3, 4)
        else:
            try:
                driver = self.driver
                driver.refresh()
                time.sleep(2)
                Method(driver).click('xpath', '//span[contains(text(),"列车数据清洗")]')
                time.sleep(1)
                Method(driver).circle_click('列车数据清洗列表数据图')

                # 获取接口的地址
                trainDataClearChart_interface_url = driver.find_element_by_xpath(
                    '//span[text()="接口地址"]/../code').text

                body = {
                    "startDate": "{}".format(startDate), "endDate": "{}".format(endDate),
                    "trainNo": "{}".format(trainNo)
                }

                # 请求保存接口
                trainDataClearChart_send = requests.post(interface_url + trainDataClearChart_interface_url,
                                                    headers={
                                                        "Authorization": globals()["Authorization"][
                                                            "Authorization"],
                                                        "Content-Type": "application/json;charset=UTF-8"},
                                                    params=body)
                trainDataClearChart_response = json.loads(trainDataClearChart_send.text)
                url = interface_url + trainDataClearChart_interface_url
                params = json.dumps(body, ensure_ascii=False)

                if trainDataClearChart_send.status_code == 200:
                    if trainDataClearChart_response['success'] is True:
                        self.assertEqual(4, 4)
                    else:
                        if 'result' in trainDataClearChart_response.keys():
                            result = trainDataClearChart_response['result']
                            del trainDataClearChart_response['result']

                            write_sheet(path, '列车数据清洗列表数据图接口', url, params,
                                        json.dumps(trainDataClearChart_response, ensure_ascii=False),
                                        json.dumps(result))
                        else:
                            write_sheet(path, '列车数据清洗列表数据图接口', url, params,
                                        json.dumps(trainDataClearChart_response, ensure_ascii=False), '')

                        self.assertEqual(3, 4)
                else:
                    write_sheet(path, '列车数据清洗列表数据图接口', url, params,
                                '列车数据清洗列表数据图返回'.format(trainDataClearChart_response.status_code), '')

                    self.assertEqual(3, 4)
            except AssertionError:
                logger.error(AssertionError)
                self.assertEqual(3, 4)


if __name__ == '__main__':
    report = r"{}/Report.html".format(path_dir)  # 定义测试报告的名称（日期+report.html，引用report_name函数实现）
    fp = open(report, 'wb')
    st = unittest.TestSuite()
    # st.addTest(test_ramsInterface('test_1_login'))
    # st.addTest(test_ramsInterface('test_2_ramsEvaluate'))
    # st.addTest(test_ramsInterface('test_3_getModelStatus'))
    # st.addTest(test_ramsInterface('test_4_ramsEvaluate_charts'))
    st.addTest(unittest.makeSuite(test_trainDataClear))
    # unittest.main()
    runner = HTMLTestRunner(stream=fp, verbosity=2, title='接口测试报告', description='测试结果如下: ')
    runner.run(st)  # 执行测试

    fp.close()  # 关闭文件流，将HTML内容写进测试报告文件