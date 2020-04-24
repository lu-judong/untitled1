from selenium import webdriver
from interfaceTest.config.main import *
import requests
import json
import ddt
from interfaceTest.libext.HTMLTestRunner import *
from interfaceTest.config.config import *


@ddt.ddt
class test_trainList(unittest.TestCase):

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

    def test_2_trainList(self):
        """列车 - 根据车型/车号范围查询列车信息接口"""
        path = self.path
        if len(globals()["Authorization"]) == 0:
            write_sheet(path, '列车 - 根据车型/车号范围查询列车信息接口', '', '', '用户未登录', '')
            self.assertEqual(3, 4)
        else:
            try:
                # 获取接口的地址
                trainList_interface_url = '/darams/trainInfo/list'

                body = {
                    "trainTypeCode": "", "fmTrainNo": "", "toTrainNo": ""
                }

                # 请求保存接口
                trainList_send = requests.post(interface_url + trainList_interface_url, headers={
                    "Authorization": globals()["Authorization"]["Authorization"],
                    "Content-Type": "application/json;charset=UTF-8"},
                                          data=json.dumps(body))
                trainList_response = json.loads(trainList_send.text)
                url = interface_url + trainList_interface_url
                params = json.dumps(body, ensure_ascii=False)

                if trainList_send.status_code == 200:
                    if trainList_response['success'] is True:
                        self.assertEqual(4, 4)
                    else:
                        if 'result' in trainList_response.keys():
                            result = trainList_response['result']
                            del trainList_response['result']

                            write_sheet(path, '列车 - 根据车型/车号范围查询列车信息接口', url, params,
                                        json.dumps(trainList_response, ensure_ascii=False), json.dumps(result))
                        else:
                            write_sheet(path, '列车 - 根据车型/车号范围查询列车信息接口', url, params,
                                        json.dumps(trainList_response, ensure_ascii=False), '')

                        self.assertEqual(3, 4)
                else:
                    write_sheet(path, '列车 - 根据车型/车号范围查询列车信息接口', url, params, '列车 - 根据车型/车号范围查询列车信息接口返回'.format(trainList_response.status_code), '')

                    self.assertEqual(3, 4)
            except AssertionError:
                logger.error(AssertionError)
                self.assertEqual(3, 4)

    def test_3_trainInfo(self):
        """列车信息列表数据"""
        path = self.path
        if len(globals()["Authorization"]) == 0:
            write_sheet(path, '获取列车列表接口', '', '', '用户未登录', '')
            self.assertEqual(3, 4)
        else:
            try:
                driver = self.driver
                driver.refresh()
                time.sleep(2)
                Method(driver).click('xpath', '//span[contains(text(),"列车信息（新）")]')
                time.sleep(1)
                Method(driver).circle_click('下拉框数据')

                # 获取列表接口的地址
                trainInfo_interface_url = driver.find_element_by_xpath('//span[text()="接口地址"]/../code').text


                # 请求保存接口
                trainInfo_send = requests.post(interface_url + trainInfo_interface_url, headers={
                    "Authorization": globals()["Authorization"]["Authorization"],
                    "Content-Type": "application/json;charset=UTF-8"})
                trainInfo_response = json.loads(trainInfo_send.text)
                url = interface_url + trainInfo_interface_url

                if trainInfo_send.status_code == 200:
                    if trainInfo_response['success'] is True:
                        self.assertEqual(4, 4)
                    else:
                        if 'result' in trainInfo_response.keys():
                            result = trainInfo_response['result']
                            del trainInfo_response['result']

                            write_sheet(path, '获取列车信息接口', url, '',
                                        json.dumps(trainInfo_response, ensure_ascii=False), json.dumps(result))
                        else:
                            write_sheet(path, '获取列车信息接口', url, '',
                                        json.dumps(trainInfo_response, ensure_ascii=False), '')

                        self.assertEqual(3, 4)
                else:
                    write_sheet(path, '获取列车信息接口', url, '', '获取列车信息接口返回'.format(trainInfo_response.status_code), '')

                    self.assertEqual(3, 4)
            except AssertionError:
                logger.error(AssertionError)
                self.assertEqual(3, 4)

    @ddt.file_data('{}/testInput/test_trainList_input/test_2_trainListMove.json'.format(path_dir))
    def test_4_trainMove(self,trainNo,pageNo,pageSize):
        """列车移动信息接口"""
        path = self.path
        if len(globals()["Authorization"]) == 0:
            write_sheet(path, '列车移动信息接口', '', '', '用户未登录', '')
            self.assertEqual(3, 4)
        else:
            try:
                driver = self.driver
                driver.refresh()
                time.sleep(2)
                Method(driver).click('xpath', '//span[contains(text(),"列车信息（新）")]')
                time.sleep(1)
                Method(driver).circle_click('列车移动信息')

                # 获取列表接口的地址
                trainMove_interface_url = driver.find_element_by_xpath('//span[text()="接口地址"]/../code').text

                params = {"trainNo": trainNo,
                            "pageNo": pageNo,
                            "pageSize": pageSize}

                # 请求保存接口
                trainMove_send = requests.post(interface_url + trainMove_interface_url, headers={
                    "Authorization": globals()["Authorization"]["Authorization"],
                    "Content-Type": "application/json;charset=UTF-8"},params=params)
                trainMove_response = json.loads(trainMove_send.text)
                url = interface_url + trainMove_interface_url
                params1 = json.dumps(params, ensure_ascii=False)

                if trainMove_send.status_code == 200:
                    if trainMove_response['success'] is True:
                        self.assertEqual(4, 4)
                    else:
                        if 'result' in trainMove_response.keys():
                            result = trainMove_response['result']
                            del trainMove_response['result']

                            write_sheet(path, '列车移动信息接口', url, params1,
                                        json.dumps(trainMove_response, ensure_ascii=False), json.dumps(result))
                        else:
                            write_sheet(path, '列车移动信息接口', url, params1,
                                        json.dumps(trainMove_response, ensure_ascii=False), '')

                        self.assertEqual(3, 4)
                else:
                    write_sheet(path, '列车移动信息接口', url, params1, '列车移动信息接口返回'.format(trainMove_response.status_code), '')

                    self.assertEqual(3, 4)
            except AssertionError:
                logger.error(AssertionError)
                self.assertEqual(3, 4)

    @ddt.file_data('{}/testInput/test_trainList_input/test_2_trainListMove.json'.format(path_dir))
    def test_5_trainMileage(self,trainNo,pageNo,pageSize):
        """列车里程信息接口"""
        path = self.path
        if len(globals()["Authorization"]) == 0:
            write_sheet(path, '列车里程信息接口', '', '', '用户未登录', '')
            self.assertEqual(3, 4)
        else:
            try:
                driver = self.driver
                driver.refresh()
                time.sleep(2)
                Method(driver).click('xpath', '//span[contains(text(),"列车信息（新）")]')
                time.sleep(1)
                Method(driver).circle_click('列车里程信息')

                # 获取列表接口的地址
                trainMileage_interface_url = driver.find_element_by_xpath('//span[text()="接口地址"]/../code').text

                params = {"trainNo": trainNo,
                          "pageNo": pageNo,
                          "pageSize": pageSize}

                # 请求保存接口
                trainMileage_send = requests.post(interface_url + trainMileage_interface_url, headers={
                    "Authorization": globals()["Authorization"]["Authorization"],
                    "Content-Type": "application/json;charset=UTF-8"}, params=params)
                trainMileage_response = json.loads(trainMileage_send.text)
                url = interface_url + trainMileage_interface_url
                params1 = json.dumps(params, ensure_ascii=False)

                if trainMileage_send.status_code == 200:
                    if trainMileage_response['success'] is True:
                        self.assertEqual(4, 4)
                    else:
                        if 'result' in trainMileage_response.keys():
                            result = trainMileage_response['result']
                            del trainMileage_response['result']

                            write_sheet(path, '列车里程信息接口', url, params1,
                                        json.dumps(trainMileage_response, ensure_ascii=False), json.dumps(result))
                        else:
                            write_sheet(path, '列车里程信息接口', url, params1,
                                        json.dumps(trainMileage_response, ensure_ascii=False), '')

                        self.assertEqual(3, 4)
                else:
                    write_sheet(path, '列车里程信息接口', url, params1, '列车里程信息接口返回'.format(trainMileage_response.status_code), '')

                    self.assertEqual(3, 4)
            except AssertionError:
                logger.error(AssertionError)
                self.assertEqual(3, 4)

    @ddt.file_data('{}/testInput/test_trainList_input/test_2_trainListMove.json'.format(path_dir))
    def test_6_trainFindAccess(self,trainNo,pageNo,pageSize):
        """列车访问信息接口"""
        path = self.path
        if len(globals()["Authorization"]) == 0:
            write_sheet(path, '列车访问信息接口', '', '', '用户未登录', '')
            self.assertEqual(3, 4)
        else:
            try:
                driver = self.driver
                driver.refresh()
                time.sleep(2)
                Method(driver).click('xpath', '//span[contains(text(),"列车信息（新）")]')
                time.sleep(1)
                Method(driver).circle_click('列车访问信息')

                # 获取列表接口的地址
                trainFindAccess_interface_url = driver.find_element_by_xpath('//span[text()="接口地址"]/../code').text

                params = {"trainNo": trainNo,
                          "pageNo": pageNo,
                          "pageSize": pageSize}

                # 请求保存接口
                trainFindAccess_send = requests.post(interface_url + trainFindAccess_interface_url, headers={
                    "Authorization": globals()["Authorization"]["Authorization"],
                    "Content-Type": "application/json;charset=UTF-8"}, params=params)
                trainFindAccess_response = json.loads(trainFindAccess_send.text)
                url = interface_url + trainFindAccess_interface_url
                params1 = json.dumps(params, ensure_ascii=False)

                if trainFindAccess_send.status_code == 200:
                    if trainFindAccess_response['success'] is True:
                        self.assertEqual(4, 4)
                    else:
                        if 'result' in trainFindAccess_response.keys():
                            result = trainFindAccess_response['result']
                            del trainFindAccess_response['result']

                            write_sheet(path, '列车访问信息接口', url, params1,
                                        json.dumps(trainFindAccess_response, ensure_ascii=False), json.dumps(result))
                        else:
                            write_sheet(path, '列车访问信息接口', url, params1,
                                        json.dumps(trainFindAccess_response, ensure_ascii=False), '')

                        self.assertEqual(3, 4)
                else:
                    write_sheet(path, '列车访问信息接口', url, params1, '列车访问信息接口返回'.format(trainFindAccess_response.status_code),
                                '')

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
    st.addTest(unittest.makeSuite(test_trainList))
    # unittest.main()
    runner = HTMLTestRunner(stream=fp, verbosity=2, title='接口测试报告', description='测试结果如下: ')
    runner.run(st)  # 执行测试

    fp.close()  # 关闭文件流，将HTML内容写进测试报告文件
