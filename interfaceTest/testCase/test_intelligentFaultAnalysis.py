from selenium import webdriver
from interfaceTest.config.main import *
import requests
import json
import ddt
from interfaceTest.libext.HTMLTestRunner import *
from interfaceTest.config.config import *


@ddt.ddt
class test_intelligentFaultAnalysis(unittest.TestCase):

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

    @ddt.file_data('{}/testInput/test_intelligentFaultAnalysis_input/test_2_intelligent.json'.format(path_dir))
    def test_2_intelligentComponentChain(self,trainNo,component):
        """查询部件位置"""
        path = self.path
        if len(globals()["Authorization"]) == 0:
            write_sheet(path, '查询部件位置接口', '', '', '用户未登录', '')
            self.assertEqual(3, 4)
        else:
            try:
                driver = self.driver
                driver.refresh()
                time.sleep(2)
                Method(driver).click('xpath', '//span[contains(text(),"智能故障分析")]')
                time.sleep(1)
                Method(driver).circle_click('查询部件位置')

                # 获取接口的地址
                intelligentComponentChain_interface_url = driver.find_element_by_xpath('//span[text()="接口地址"]/../code').text

                body = {
                    "trainNo": "{}".format(trainNo), "component": "{}".format(component)
                }

                # 请求保存接口
                intelligentComponentChain_send = requests.post(interface_url + intelligentComponentChain_interface_url, headers={
                    "Authorization": globals()["Authorization"]["Authorization"],
                    "Content-Type": "application/json;charset=UTF-8"},
                                          params=body)
                intelligentComponentChain_response = json.loads(intelligentComponentChain_send.text)
                url = interface_url + intelligentComponentChain_interface_url
                params = json.dumps(body, ensure_ascii=False)

                if intelligentComponentChain_send.status_code == 200:
                    if intelligentComponentChain_response['success'] is True:
                        self.assertEqual(4, 4)
                    else:
                        if 'result' in intelligentComponentChain_response.keys():
                            result = intelligentComponentChain_response['result']
                            del intelligentComponentChain_response['result']

                            write_sheet(path, '列车 - 根据车型/车号范围查询列车信息接口', url, params,
                                        json.dumps(intelligentComponentChain_response, ensure_ascii=False), json.dumps(result))
                        else:
                            write_sheet(path, '列车 - 根据车型/车号范围查询列车信息接口', url, params,
                                        json.dumps(intelligentComponentChain_response, ensure_ascii=False), '')

                        self.assertEqual(3, 4)
                else:
                    write_sheet(path, '列车 - 根据车型/车号范围查询列车信息接口', url, params, '列车 - 根据车型/车号范围查询列车信息接口返回'.format(intelligentComponentChain_response.status_code), '')

                    self.assertEqual(3, 4)
            except AssertionError:
                logger.error(AssertionError)
                self.assertEqual(3, 4)


    def test_3_intelligentGetModifiedData(self):
        """获取模型数据"""
        path = self.path
        if len(globals()["Authorization"]) == 0:
            write_sheet(path, '获取模型数据接口', '', '', '用户未登录', '')
            self.assertEqual(3, 4)
        else:
            try:

                # 获取接口的地址
                intelligentGetModifiedData_interface_url = '/darams/calculator/intelligent_fault_analysis/getModifiedData'

                body = {
                    "adaptation": "",
                    "endDate": "",
                    "pageNo": 1,
                    "pageSize": 10,
                    "startDate": ""
                }
                # 请求保存接口
                intelligentGetModifiedData_send = requests.post(interface_url + intelligentGetModifiedData_interface_url,
                                                               headers={"Authorization": globals()["Authorization"][
                                                                       "Authorization"],"Content-Type": "application/json;charset=UTF-8"},
                                                               data=json.dumps(body))
                intelligentGetModifiedData_response = json.loads(intelligentGetModifiedData_send.text)
                url = interface_url + intelligentGetModifiedData_interface_url
                params = json.dumps(body, ensure_ascii=False)

                if intelligentGetModifiedData_send.status_code == 200:
                    if intelligentGetModifiedData_response['success'] is True:
                        self.assertEqual(4, 4)
                    else:
                        if 'result' in intelligentGetModifiedData_response.keys():
                            result = intelligentGetModifiedData_response['result']
                            del intelligentGetModifiedData_response['result']

                            write_sheet(path, '获取模型数据接口', url, params,
                                        json.dumps(intelligentGetModifiedData_response, ensure_ascii=False),
                                        json.dumps(result))
                        else:
                            write_sheet(path, '获取模型数据接口', url, params,
                                        json.dumps(intelligentGetModifiedData_response, ensure_ascii=False), '')

                        self.assertEqual(3, 4)
                else:
                    write_sheet(path, '获取模型数据接口', url, params,
                                '获取模型数据接口返回'.format(intelligentGetModifiedData_response.status_code), '')

                    self.assertEqual(3, 4)

            except AssertionError:
                logger.error(AssertionError)
                self.assertEqual(3, 4)

    def test_4_intelligentRecongition(self):
        """智能故障识别"""
        path = self.path
        if len(globals()["Authorization"]) == 0:
            write_sheet(path, '智能故障识别接口', '', '', '用户未登录', '')
            self.assertEqual(3, 4)
        else:
            try:
                driver = self.driver
                driver.refresh()
                time.sleep(2)
                Method(driver).click('xpath', '//span[contains(text(),"智能故障分析")]')
                time.sleep(1)
                Method(driver).circle_click('智能故障识别')

                # 获取接口的地址
                intelligentRecongition_interface_url = driver.find_element_by_xpath('//span[text()="接口地址"]/../code').text

                body = {
                    "credit": "0.2",
                    "faultBrief": "灯坏了",
                    "trainNo": "0259",
                    "trainType": "E22"
                }

                # 请求保存接口
                intelligentRecongition_send = requests.post(interface_url + intelligentRecongition_interface_url,
                                                               headers={
                                                                   "Authorization": globals()["Authorization"][
                                                                       "Authorization"],
                                                                   "Content-Type": "application/json;charset=UTF-8"},
                                                               data=json.dumps(body))
                intelligentRecongition_response = json.loads(intelligentRecongition_send.text)
                url = interface_url + intelligentRecongition_interface_url
                params = json.dumps(body, ensure_ascii=False)

                if intelligentRecongition_send.status_code == 200:
                    if intelligentRecongition_response['success'] is True:
                        self.assertEqual(4, 4)
                    else:
                        if 'result' in intelligentRecongition_response.keys():
                            result = intelligentRecongition_response['result']
                            del intelligentRecongition_response['result']

                            write_sheet(path, '智能故障识别接口', url, params,
                                        json.dumps(intelligentRecongition_response, ensure_ascii=False),
                                        json.dumps(result))
                        else:
                            write_sheet(path, '智能故障识别接口', url, params,
                                        json.dumps(intelligentRecongition_response, ensure_ascii=False), '')

                        self.assertEqual(3, 4)
                else:
                    write_sheet(path, '智能故障识别接口', url, params,
                                '智能故障识别接口返回'.format(intelligentRecongition_response.status_code), '')

                    self.assertEqual(3, 4)
            except AssertionError:
                logger.error(AssertionError)
                self.assertEqual(3, 4)

    def test_5_intelligentTrain(self):
        """列车信息列表"""
        path = self.path
        if len(globals()["Authorization"]) == 0:
            write_sheet(path, '列车信息列表', '', '', '用户未登录', '')
            self.assertEqual(3, 4)
        else:
            try:
                driver = self.driver
                driver.refresh()
                time.sleep(2)
                Method(driver).click('xpath', '//span[contains(text(),"列车信息")]')
                time.sleep(1)
                Method(driver).circle_click('列车信息列表')

                # 获取接口的地址
                intelligentTrain_interface_url = driver.find_element_by_xpath(
                    '//span[text()="接口地址"]/../code').text

                body = {
                    "pageNo": "1",
                    "pageSize": "5",
                    "trainNo": "",
                    "vehicleNo": ""
                }

                # 请求保存接口
                intelligentTrain_send = requests.post(interface_url + intelligentTrain_interface_url,
                                                            headers={
                                                                "Authorization": globals()["Authorization"][
                                                                    "Authorization"],
                                                                "Content-Type": "application/json;charset=UTF-8"},
                                                            data=json.dumps(body))
                intelligentTrain_response = json.loads(intelligentTrain_send.text)
                url = interface_url + intelligentTrain_interface_url
                params = json.dumps(body, ensure_ascii=False)

                if intelligentTrain_send.status_code == 200:
                    if intelligentTrain_response['success'] is True:
                        self.assertEqual(4, 4)
                    else:
                        if 'result' in intelligentTrain_response.keys():
                            result = intelligentTrain_response['result']
                            del intelligentTrain_response['result']

                            write_sheet(path, '列车信息列表接口', url, params,
                                        json.dumps(intelligentTrain_response, ensure_ascii=False),
                                        json.dumps(result))
                        else:
                            write_sheet(path, '列车信息列表接口', url, params,
                                        json.dumps(intelligentTrain_response, ensure_ascii=False), '')

                        self.assertEqual(3, 4)
                else:
                    write_sheet(path, '列车信息列表接口', url, params,
                                '列车信息列表接口返回'.format(intelligentTrain_response.status_code), '')

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
    st.addTest(unittest.makeSuite(test_intelligentFaultAnalysis))
    # unittest.main()
    runner = HTMLTestRunner(stream=fp, verbosity=2, title='接口测试报告', description='测试结果如下: ')
    runner.run(st)  # 执行测试

    fp.close()  # 关闭文件流，将HTML内容写进测试报告文件