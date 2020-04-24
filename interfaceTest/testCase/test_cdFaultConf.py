from selenium import webdriver
from interfaceTest.config.main import *
import requests
import json
import ddt
from interfaceTest.libext.HTMLTestRunner import *
from interfaceTest.config.config import *


@ddt.ddt
class test_cdFaultConf(unittest.TestCase):

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
    def test_1_login(self,username,password):
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
            params = json.dumps({'username': '{}'.format(username),'password': '{}'.format(password)})
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

                        write_sheet(path, '登录接口', url,params ,json.dumps(login_response,ensure_ascii=False),json.dumps(result, ensure_ascii=False))
                    else:
                        write_sheet(path, '登录接口', url,params,json.dumps(login_response, ensure_ascii=False),'')
                    self.assertEqual(3, 4)
            else:
                globals()["Authorization"] = {}

                write_sheet(path, '登录接口',url,params ,'登录接口返回:{}'.format(login_send.status_code),'')

                self.assertEqual(3, 4)
        except AssertionError:
            logger.error(AssertionError)
            self.assertEqual(3, 4)


    def test_2_getAllTrainType(self):
        """获取所有车型接口"""  # 说明测试用例的标题
        # option = webdriver.ChromeOptions()
        # option.add_argument("headless")
        # driver = webdriver.Chrome(executable_path=r'{}\apps\chromedriver.exe'.format(path_dir))
        path = self.path
        if len(globals()["Authorization"]) == 0:

            write_sheet(path, '获取所有车型接口', '', '', '用户未登录', '')
            self.assertEqual(3, 4)
        else:
            try:
                driver = self.driver
                driver.refresh()
                time.sleep(2)
                Method(driver).click('xpath', '//span[contains(text(),"故障字典")]')
                time.sleep(1)

                # 计算接口

                Method(driver).circle_click('获取所有车型')

                # 获取计算接口的地址
                getAllTrainType_interface_url = driver.find_element_by_xpath('//span[text()="接口地址"]/../code').text

                # 请求计算接口
                getAllTrainType_send = requests.get(interface_url + getAllTrainType_interface_url,
                                              headers=globals()["Authorization"])
                getAllTrainType_response = json.loads(getAllTrainType_send.text)
                url = interface_url + getAllTrainType_interface_url

                if getAllTrainType_send.status_code == 200:

                    if getAllTrainType_response['success'] is True:

                        self.assertEqual(4, 4)
                    else:
                        if 'result' in getAllTrainType_response.keys():
                            result = getAllTrainType_response['result']
                            del getAllTrainType_response['result']

                            write_sheet(path, '获取所有车型接口', url, '',
                                        json.dumps(getAllTrainType_response, ensure_ascii=False), json.dumps(result))
                        else:
                            write_sheet(path, '获取所有车型接口', url, '',
                                        json.dumps(getAllTrainType_response, ensure_ascii=False), '')

                        self.assertEqual(3, 4)
                else:
                    write_sheet(path, '获取所有车型接口', url, '', '获取所有车型接口返回'.format(getAllTrainType_response.status_code), '')

                    self.assertEqual(3, 4)

            except AssertionError:
                logger.error(AssertionError)
                self.assertEqual(3, 4)

    @ddt.file_data('{}/testInput/test_cdFaultConf_input/test_3_getFaultObjectInfo.json'.format(path_dir))
    def test_3_getFaultObjectInfo(self,faultObjectInfoQueryId):
        """获取故障对象信息"""  # 说明测试用例的标题
        # option = webdriver.ChromeOptions()
        # option.add_argument("headless")
        # driver = webdriver.Chrome(executable_path=r'{}\apps\chromedriver.exe'.format(path_dir))
        path = self.path
        if len(globals()["Authorization"]) == 0:

            write_sheet(path, '获取故障对象信息', '', '', '用户未登录', '')
            self.assertEqual(3, 4)
        else:
            try:
                driver = self.driver
                driver.refresh()
                time.sleep(2)
                Method(driver).click('xpath', '//span[contains(text(),"故障字典")]')
                time.sleep(1)

                # 计算接口

                Method(driver).circle_click('获取故障对象信息')
                body = {
                    "faultObjectInfoQueryId": "{}".format(faultObjectInfoQueryId)
                }


                # 获取计算接口的地址
                getFaultObjectInfo_interface_url = driver.find_element_by_xpath('//span[text()="接口地址"]/../code').text

                # 请求计算接口
                getFaultObjectInfo_send = requests.get(interface_url + getFaultObjectInfo_interface_url,
                                              headers=globals()["Authorization"],params=body)
                getFaultObjectInfo_response = json.loads(getFaultObjectInfo_send.text)
                url = interface_url + getFaultObjectInfo_interface_url
                params=json.dumps(body, ensure_ascii=False)

                if getFaultObjectInfo_send.status_code == 200:

                    if getFaultObjectInfo_response['success'] is True:

                        self.assertEqual(4, 4)
                    else:
                        if 'result' in getFaultObjectInfo_response.keys():
                            result = getFaultObjectInfo_response['result']
                            del getFaultObjectInfo_response['result']

                            write_sheet(path, '获取故障对象信息接口', url, params,
                                        json.dumps(getFaultObjectInfo_response, ensure_ascii=False), json.dumps(result))
                        else:
                            write_sheet(path, '获取故障对象信息接口', url, params,
                                        json.dumps(getFaultObjectInfo_response, ensure_ascii=False), '')

                        self.assertEqual(3, 4)
                else:
                    write_sheet(path, '获取故障对象信息接口', url, params, '获取故障对象信息接口返回'.format(getFaultObjectInfo_response.status_code), '')

                    self.assertEqual(3, 4)

            except AssertionError:
                logger.error(AssertionError)
                self.assertEqual(3, 4)

    @ddt.file_data('{}/testInput/test_cdFaultConf_input/test_4_getFaultPatter.json'.format(path_dir))
    def test_4_getFaultPatter(self, body):
        """根据故障对象id+查询条件获取故障模式接口"""  # 说明测试用例的标题
        # option = webdriver.ChromeOptions()
        # option.add_argument("headless")
        # driver = webdriver.Chrome(executable_path=r'{}\apps\chromedriver.exe'.format(path_dir))
        path = self.path
        if len(globals()["Authorization"]) == 0:

            write_sheet(path, '根据故障对象id+查询条件获取故障模式接口', '', '', '用户未登录', '')
            self.assertEqual(3, 4)
        else:
            try:
                driver = self.driver
                driver.refresh()
                time.sleep(2)
                Method(driver).click('xpath', '//span[contains(text(),"故障字典")]')
                time.sleep(1)

                # 计算接口

                Method(driver).circle_click('根据故障对象id+查询条件获取故障模式')
                body = body

                # 获取计算接口的地址
                getFaultPattern_interface_url = driver.find_element_by_xpath('//span[text()="接口地址"]/../code').text

                # 请求计算接口
                getFaultPattern_send = requests.post(interface_url + getFaultPattern_interface_url,
                                                     headers={
                                                         "Authorization": globals()["Authorization"]["Authorization"],
                                                         "Content-Type": "application/json;charset=UTF-8"}, data=json.dumps(body))
                getFaultPattern_response = json.loads(getFaultPattern_send.text)
                url = interface_url + getFaultPattern_interface_url
                params = json.dumps(body, ensure_ascii=False)

                if getFaultPattern_send.status_code == 200:

                    if getFaultPattern_response['success'] is True:

                        self.assertEqual(4, 4)
                    else:
                        if 'result' in getFaultPattern_response.keys():
                            result = getFaultPattern_response['result']
                            del getFaultPattern_response['result']

                            write_sheet(path, '根据故障对象id+查询条件获取故障模式接口', url, params,
                                        json.dumps(getFaultPattern_response, ensure_ascii=False), json.dumps(result))
                        else:
                            write_sheet(path, '根据故障对象id+查询条件获取故障模式接口', url, params,
                                        json.dumps(getFaultPattern_response, ensure_ascii=False), '')

                        self.assertEqual(3, 4)
                else:
                    write_sheet(path, '根据故障对象id+查询条件获取故障模式接口', url, params,
                                '根据故障对象id+查询条件获取故障模式接口返回'.format(getFaultPattern_send.status_code), '')

                    self.assertEqual(3, 4)

            except AssertionError:
                logger.error(AssertionError)
                self.assertEqual(3, 4)

    @ddt.file_data('{}/testInput/test_cdFaultConf_input/test_5_getSingleFaultObjectTree.json'.format(path_dir))
    def test_5_getSingleFaultObjectTree(self,trainTypeId):
        """获取单个车型故障对象树"""  # 说明测试用例的标题
        # option = webdriver.ChromeOptions()
        # option.add_argument("headless")
        # driver = webdriver.Chrome(executable_path=r'{}\apps\chromedriver.exe'.format(path_dir))
        path = self.path
        if len(globals()["Authorization"]) == 0:

            write_sheet(path, '获取单个车型故障对象树', '', '', '用户未登录', '')
            self.assertEqual(3, 4)
        else:
            try:
                driver = self.driver
                driver.refresh()
                time.sleep(2)
                Method(driver).click('xpath', '//span[contains(text(),"故障字典")]')
                time.sleep(1)

                # 计算接口

                Method(driver).circle_click('获取单个车型故障对象树')
                body = {"trainTypeId":"{}".format(trainTypeId)}

                # 获取计算接口的地址
                getSingleFaultObjectTree_interface_url = driver.find_element_by_xpath('//span[text()="接口地址"]/../code').text

                # 请求计算接口
                getSingleFaultObjectTree_send = requests.get(interface_url + getSingleFaultObjectTree_interface_url,
                                                             headers={
                                                                 "Authorization": globals()["Authorization"][
                                                                     "Authorization"],
                                                                 "Content-Type": "application/json;charset=UTF-8"}, params=body)
                getSingleFaultObjectTree_response = json.loads(getSingleFaultObjectTree_send.text)
                url = interface_url + getSingleFaultObjectTree_interface_url
                params = json.dumps(body, ensure_ascii=False)

                if getSingleFaultObjectTree_send.status_code == 200:

                    if getSingleFaultObjectTree_response['success'] is True:
                        if getSingleFaultObjectTree_response['result'] is None:
                            write_sheet(path, '根据故障对象id+查询条件获取故障模式接口', url, params,
                                        json.dumps(getSingleFaultObjectTree_response, ensure_ascii=False), '')
                            self.assertEqual(3, 4)
                        else:

                            self.assertEqual(4, 4)
                    else:
                        if 'result' in getSingleFaultObjectTree_response.keys():
                            result = getSingleFaultObjectTree_response['result']
                            del getSingleFaultObjectTree_response['result']

                            write_sheet(path, '根据故障对象id+查询条件获取故障模式接口', url, params,
                                        json.dumps(getSingleFaultObjectTree_response, ensure_ascii=False), json.dumps(result))
                        else:
                            write_sheet(path, '根据故障对象id+查询条件获取故障模式接口', url, params,
                                        json.dumps(getSingleFaultObjectTree_response, ensure_ascii=False), '')

                        self.assertEqual(3, 4)
                else:
                    write_sheet(path, '根据故障对象id+查询条件获取故障模式接口', url, params,
                                '根据故障对象id+查询条件获取故障模式接口返回'.format(getSingleFaultObjectTree_send.status_code), '')

                    self.assertEqual(3, 4)

            except AssertionError:
                logger.error(AssertionError)
                self.assertEqual(3, 4)

    def test_6_getunitType(self):
        """获取单元类型接口"""  # 说明测试用例的标题
        # option = webdriver.ChromeOptions()
        # option.add_argument("headless")
        # driver = webdriver.Chrome(executable_path=r'{}\apps\chromedriver.exe'.format(path_dir))
        path = self.path
        if len(globals()["Authorization"]) == 0:

            write_sheet(path, '获取单元类型接口', '', '', '用户未登录', '')
            self.assertEqual(3, 4)
        else:
            try:
                driver = self.driver
                driver.refresh()
                time.sleep(2)
                Method(driver).click('xpath', '//span[contains(text(),"故障字典")]')
                time.sleep(1)

                # 计算接口

                Method(driver).circle_click('获取单元类型-用于故障字典的查询条件')

                # 获取计算接口的地址
                getunitType_interface_url = driver.find_element_by_xpath('//span[text()="接口地址"]/../code').text

                # 请求计算接口
                getunitType_send = requests.get(interface_url + getunitType_interface_url,
                                              headers=globals()["Authorization"])
                getunitType_response = json.loads(getunitType_send.text)
                url = interface_url + getunitType_interface_url

                if getunitType_send.status_code == 200:

                    if getunitType_response['success'] is True:

                        self.assertEqual(4, 4)
                    else:
                        if 'result' in getunitType_response.keys():
                            result = getunitType_response['result']
                            del getunitType_response['result']

                            write_sheet(path, '获取单元类型接口', url, '',
                                        json.dumps(getunitType_response, ensure_ascii=False), json.dumps(result))
                        else:
                            write_sheet(path, '获取单元类型接口', url, '',
                                        json.dumps(getunitType_response, ensure_ascii=False), '')

                        self.assertEqual(3, 4)
                else:
                    write_sheet(path, '获取单元类型接口', url, '', '获取单元类型接口返回'.format(getunitType_response.status_code), '')

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
    st.addTest(unittest.makeSuite(test_cdFaultConf))
    # unittest.main()
    runner = HTMLTestRunner(stream=fp, verbosity=2, title='接口测试报告', description='测试结果如下: ')
    runner.run(st)  # 执行测试

    fp.close()  # 关闭文件流，将HTML内容写进测试报告文件
