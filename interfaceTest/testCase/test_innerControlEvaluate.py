from selenium import webdriver
from interfaceTest.config.main import *
import requests
import json
import ddt
from interfaceTest.libext.HTMLTestRunner import *
from interfaceTest.config.config import *
from interfaceTest.testInput.test_innerControlEvaluate_input.test_4_innerControlEvaluate_charts import *


@ddt.ddt
class test_innerControl(unittest.TestCase):

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


    # @ddt.file_data('{}/testInput/test_innerControlEvaluate_input/test_2_innerControlEvaluate.json'.format(path_dir))
    # def test_2_innerControlEvaluate(self,modelId):
    #     """内控模型计算接口"""  # 说明测试用例的标题
    #     # option = webdriver.ChromeOptions()
    #     # option.add_argument("headless")
    #     # driver = webdriver.Chrome(executable_path=r'{}\apps\chromedriver.exe'.format(path_dir))
    #     path = self.path
    #     if len(globals()["Authorization"]) == 0:
    #
    #         write_sheet(path, '内控模型', '','','用户未登录','')
    #         self.assertEqual(3, 4)
    #     else:
    #         try:
    #             driver = self.driver
    #             driver.refresh()
    #             time.sleep(2)
    #             Method(driver).click('xpath', '//span[contains(text(),"内控指标建模接口")]')
    #             time.sleep(1)
    #
    #             # 计算接口
    #
    #             Method(driver).circle_click('内控指标模型评估')
    #
    #             # 获取计算接口的地址
    #             evaluate_interface_url = driver.find_element_by_xpath('//span[text()="接口地址"]/../code').text
    #
    #             # 请求计算接口
    #             evaluate_send = requests.post(interface_url + evaluate_interface_url, headers=globals()["Authorization"],
    #                           params={'modelId': modelId})
    #             evaluate_response = json.loads(evaluate_send.text)
    #             url = interface_url + evaluate_interface_url
    #             params =  json.dumps({'modelId': modelId},ensure_ascii=False)
    #             if evaluate_send.status_code == 200:
    #
    #
    #                 if evaluate_response['success'] is True:
    #
    #                     self.assertEqual(4, 4)
    #                 else:
    #                     if 'result'in evaluate_response.keys():
    #                         result = evaluate_response['result']
    #                         del evaluate_response['result']
    #
    #                         write_sheet(path, '内控模型计算接口', url, params, json.dumps(evaluate_response, ensure_ascii=False), json.dumps(result))
    #                     else:
    #                         write_sheet(path, '内控模型计算接口', url, params, json.dumps(evaluate_response, ensure_ascii=False),'')
    #
    #                     self.assertEqual(3, 4)
    #             else:
    #                 write_sheet(path, '内控模型计算接口', url, params, '内控模型计算接口返回'.format(evaluate_send.status_code),'')
    #
    #                 self.assertEqual(3, 4)
    #
    #         except AssertionError:
    #             logger.error(AssertionError)
    #             self.assertEqual(3, 4)
    # #
    # def test_3_getDepartRoom(self):
    #     """部室接口"""
    #     path = self.path
    #     if len(globals()["Authorization"]) == 0:
    #         write_sheet(path, '部室接口', '', '', '用户未登录', '')
    #
    #         self.assertEqual(3, 4)
    #     else:
    #         try:
    #             driver = self.driver
    #             driver.refresh()
    #             time.sleep(2)
    #             Method(driver).click('xpath', '//span[contains(text(),"内控指标建模接口")]')
    #             time.sleep(1)
    #             Method(driver).circle_click('部室')
    #             time.sleep(1)
    #             # 获取计算状态接口的地址
    #             getModelStatus_url = driver.find_element_by_xpath('//span[text()="接口地址"]/../code').text
    #             # 请求计算状态接口
    #
    #             getdepart_send = requests.get(interface_url + getModelStatus_url,
    #                                                headers=globals()["Authorization"])
    #             getdepart_response = json.loads(getdepart_send.text)
    #             url = interface_url + getModelStatus_url
    #
    #
    #             if getdepart_response.status_code == 200:
    #
    #                 # 计算完成的情况
    #                 if getdepart_response['success'] is True:
    #                    self.assertEqual(4,4)
    #                 else:
    #                     if 'result'in getdepart_response.keys():
    #                         result = getdepart_response['result']
    #                         del getdepart_response['result']
    #
    #                         write_sheet(path, '内控模型部室接口', url, '', json.dumps(getdepart_response, ensure_ascii=False), json.dumps(result))
    #                     else:
    #                         write_sheet(path, '内控模型部室接口', url, '', json.dumps(getdepart_response, ensure_ascii=False),'')
    #
    #                     self.assertEqual(3, 4)
    #
    #             else:
    #                 write_sheet(path, '内控模型部室接口', url, '',
    #                             '内控模型部室接口返回{}'.format(getdepart_response.status_code), '')
    #                 self.assertEqual(3, 4)
    #         except AssertionError:
    #             logger.error(AssertionError)
    #             self.assertEqual(3, 4)

    @ddt.file_data(
        '{}/testInput/test_innerControlEvaluate_input/test_4_innerControlEvaluate_charts.json'.format(path_dir))
    def test_4_innerControlEvaluate_charts1(self, modelId):
        """内控模型图表1接口"""
        path = self.path
        if len(globals()["Authorization"]) == 0:
            write_sheet(path, '内控模型图表1接口', '', '', '用户未登录', '')

            self.assertEqual(3, 4)
        else:
            if charts1_interface_status != 'non-existent':
                try:
                    driver = self.driver
                    driver.refresh()
                    time.sleep(2)
                    Method(driver).click('xpath', '//span[contains(text(),"内控指标建模接口")]')
                    time.sleep(1)
                    Method(driver).circle_click('图表1')
                    time.sleep(1)
                    # 获取计算状态接口的地址
                    charts_url = driver.find_element_by_xpath('//span[text()="接口地址"]/../code').text

                    # 判断文件中是否存在
                    file = '{}/testFile/test_innerControlEvaluate/test_innerControlEvaluate_charts1/test_innerControlEvaluate_charts1_{}.txt'.format(
                        path_dir, modelId)

                    # 判断接口状态
                    if charts1_interface_status == 'normal':
                        body = {"modelId": "{}".format(modelId)
                                }

                        charts5_send = requests.post(interface_url + charts_url, headers={
                            "Authorization": globals()["Authorization"]["Authorization"],
                            "Content-Type": "application/json;charset=UTF-8"},
                                                     params=body)
                        url = interface_url + charts_url
                        params = json.dumps(body)

                        if os.path.exists(file) is True:
                            pass
                        else:
                            fp = open(file, 'wb')
                            fp.write(charts5_send.text.encode())
                            fp.close()

                        # 判断文件是否有信息
                        sz = os.path.getsize(file)
                        if not sz:
                            fp = open(file, 'wb')
                            fp.write(charts5_send.text.encode())
                            self.assertEqual(4, 4)
                        else:
                            fp = open(file, 'r', encoding='UTF-8')
                            # 因为每次请求的token值不一样 =所以得删除掉在对比
                            dict_fp = json.loads(fp.read())
                            dict_ramscharts = json.loads(charts5_send.text)
                            del dict_fp['token']
                            del dict_ramscharts['token']
                            if dict_fp == dict_ramscharts:

                                self.assertEqual(4, 4)
                            else:
                                if 'result' in dict_ramscharts.keys():
                                    result = dict_ramscharts['result']
                                    del dict_ramscharts['result']

                                    write_sheet(path, '内控模型图表1接口', url, params,
                                                json.dumps(dict_ramscharts, ensure_ascii=False),
                                                json.dumps(result, ensure_ascii=False)[:2000])
                                else:
                                    write_sheet(path, '内控模型图表1接口', url, params,
                                                json.dumps(dict_ramscharts, ensure_ascii=False),
                                                '')

                                self.assertEqual(3, 4)

                        fp.close()

                    else:
                        # 先放着处理逻辑
                        text = ''
                        # 清空存放接口result的文件
                        if os.path.exists(file) is True:
                            fp = open(file, 'wb')
                            fp.truncate()
                            fp.close()
                        else:
                            fp = open(file, 'wb')
                            fp.write(text)
                            fp.close()


                except AssertionError:
                    logger.error(AssertionError)
                    self.assertEqual(3, 4)
            else:
                pass

    @ddt.file_data('{}/testInput/test_innerControlEvaluate_input/test_4_innerControlEvaluate_charts.json'.format(path_dir))
    def test_5_innerControlEvaluate_charts2(self, modelId):
        """内控模型图表2接口"""
        path = self.path
        if len(globals()["Authorization"]) == 0:
            write_sheet(path, '内控模型图表2接口', '', '', '用户未登录', '')

            self.assertEqual(3, 4)
        else:
            if charts2_interface_status != 'non-existent':
                try:
                    driver = self.driver
                    driver.refresh()
                    time.sleep(2)
                    Method(driver).click('xpath', '//span[contains(text(),"内控指标建模接口")]')
                    time.sleep(1)
                    Method(driver).circle_click('图表2')
                    time.sleep(1)
                    # 获取计算状态接口的地址
                    charts2_url = driver.find_element_by_xpath('//span[text()="接口地址"]/../code').text

                    # 判断文件中是否存在
                    file = '{}/testFile/test_innerControlEvaluate/test_innerControlEvaluate_charts2/test_innerControlEvaluate_charts2_{}.txt'.format(
                        path_dir, modelId)

                    # 判断接口状态
                    if charts2_interface_status == 'normal':
                        body = {"modelId": "{}".format(modelId)
                                }

                        charts2_send = requests.post(interface_url + charts2_url, headers={
                            "Authorization": globals()["Authorization"]["Authorization"],
                            "Content-Type": "application/json;charset=UTF-8"},
                                                        params=body)
                        url = interface_url + charts2_url
                        params = json.dumps(body)

                        if os.path.exists(file) is True:
                            pass
                        else:
                            fp = open(file, 'wb')
                            fp.write(charts2_send.text.encode())
                            fp.close()

                        # 判断文件是否有信息
                        sz = os.path.getsize(file)
                        if not sz:
                            fp = open(file, 'wb')
                            fp.write(charts2_send.text.encode())
                            self.assertEqual(4, 4)
                        else:
                            fp = open(file, 'r', encoding='UTF-8')
                            # 因为每次请求的token值不一样 =所以得删除掉在对比
                            dict_fp = json.loads(fp.read())
                            dict_ramscharts = json.loads(charts2_send.text)
                            del dict_fp['token']
                            del dict_ramscharts['token']
                            if dict_fp == dict_ramscharts:

                                self.assertEqual(4, 4)
                            else:
                                if 'result' in dict_ramscharts.keys():
                                    result = dict_ramscharts['result']
                                    del dict_ramscharts['result']

                                    write_sheet(path, '内控模型图表2接口', url, params,
                                                json.dumps(dict_ramscharts, ensure_ascii=False),
                                                json.dumps(result, ensure_ascii=False)[:2000])
                                else:
                                    write_sheet(path, '内控模型图表2接口', url, params,
                                                json.dumps(dict_ramscharts, ensure_ascii=False),
                                                '')

                                self.assertEqual(3, 4)

                        fp.close()

                    else:
                        # 先放着处理逻辑
                        text = ''
                        # 清空存放接口result的文件
                        if os.path.exists(file) is True:
                            fp = open(file, 'wb')
                            fp.truncate()
                            fp.close()
                        else:
                            fp = open(file, 'wb')
                            fp.write(text)
                            fp.close()


                except AssertionError:
                    logger.error(AssertionError)
                    self.assertEqual(3, 4)
            else:
                pass

    @ddt.file_data(
        '{}/testInput/test_innerControlEvaluate_input/test_4_innerControlEvaluate_charts.json'.format(path_dir))
    def test_6_innerControlEvaluate_charts3(self, modelId):
        """内控模型图表3接口"""
        path = self.path
        if len(globals()["Authorization"]) == 0:
            write_sheet(path, '内控模型图表3接口', '', '', '用户未登录', '')

            self.assertEqual(3, 4)
        else:
            if charts3_interface_status != 'non-existent':
                try:
                    driver = self.driver
                    driver.refresh()
                    time.sleep(2)
                    Method(driver).click('xpath', '//span[contains(text(),"内控指标建模接口")]')
                    time.sleep(1)
                    Method(driver).circle_click('图表3')
                    time.sleep(1)
                    # 获取计算状态接口的地址
                    charts3_url = driver.find_element_by_xpath('//span[text()="接口地址"]/../code').text

                    # 判断文件中是否存在
                    file = '{}/testFile/test_innerControlEvaluate/test_innerControlEvaluate_charts3/test_innerControlEvaluate_charts3_{}.txt'.format(
                        path_dir, modelId)

                    # 判断接口状态
                    if charts3_interface_status == 'normal':
                        body = {"modelId": "{}".format(modelId),
                                "lineType": "机械开发部"
                                }

                        charts3_send = requests.post(interface_url + charts3_url, headers={
                            "Authorization": globals()["Authorization"]["Authorization"],
                            "Content-Type": "application/json;charset=UTF-8"},
                                                        params=body)
                        url = interface_url + charts3_url
                        params = json.dumps(body)

                        if os.path.exists(file) is True:
                            pass
                        else:
                            fp = open(file, 'wb')
                            fp.write(charts3_send.text.encode())
                            fp.close()

                        # 判断文件是否有信息
                        sz = os.path.getsize(file)
                        if not sz:
                            fp = open(file, 'wb')
                            fp.write(charts3_send.text.encode())
                            self.assertEqual(4, 4)
                        else:
                            fp = open(file, 'r', encoding='UTF-8')
                            # 因为每次请求的token值不一样 =所以得删除掉在对比
                            dict_fp = json.loads(fp.read())
                            dict_ramscharts = json.loads(charts3_send.text)
                            del dict_fp['token']
                            del dict_ramscharts['token']
                            if dict_fp == dict_ramscharts:

                                self.assertEqual(4, 4)
                            else:
                                if 'result' in dict_ramscharts.keys():
                                    result = dict_ramscharts['result']
                                    del dict_ramscharts['result']

                                    write_sheet(path, '内控模型图表3接口', url, params,
                                                json.dumps(dict_ramscharts, ensure_ascii=False),
                                                json.dumps(result, ensure_ascii=False)[:2000])
                                else:
                                    write_sheet(path, '内控模型图表3接口', url, params,
                                                json.dumps(dict_ramscharts, ensure_ascii=False),
                                                '')

                                self.assertEqual(3, 4)

                        fp.close()

                    else:
                        # 先放着处理逻辑
                        text = ''
                        # 清空存放接口result的文件
                        if os.path.exists(file) is True:
                            fp = open(file, 'wb')
                            fp.truncate()
                            fp.close()
                        else:
                            fp = open(file, 'wb')
                            fp.write(text)
                            fp.close()


                except AssertionError:
                    logger.error(AssertionError)
                    self.assertEqual(3, 4)
            else:
                pass

    @ddt.file_data(
        '{}/testInput/test_innerControlEvaluate_input/test_4_innerControlEvaluate_charts.json'.format(path_dir))
    def test_7_innerControlEvaluate_charts4(self, modelId):
        """内控模型图表4接口"""
        path = self.path
        if len(globals()["Authorization"]) == 0:
            write_sheet(path, '内控模型图表4接口', '', '', '用户未登录', '')

            self.assertEqual(3, 4)
        else:
            if charts4_interface_status != 'non-existent':
                try:
                    driver = self.driver
                    driver.refresh()
                    time.sleep(2)
                    Method(driver).click('xpath', '//span[contains(text(),"内控指标建模接口")]')
                    time.sleep(1)
                    Method(driver).circle_click('图表4')
                    time.sleep(1)
                    # 获取计算状态接口的地址
                    charts4_url = driver.find_element_by_xpath('//span[text()="接口地址"]/../code').text

                    # 判断文件中是否存在
                    file = '{}/testFile/test_innerControlEvaluate/test_innerControlEvaluate_charts4/test_innerControlEvaluate_charts4_{}.txt'.format(
                        path_dir, modelId)

                    # 判断接口状态
                    if charts4_interface_status == 'normal':
                        body = {"modelId": "{}".format(modelId),
                                "lineType": "机械开发部"
                                }

                        charts4_send = requests.post(interface_url + charts4_url, headers={
                            "Authorization": globals()["Authorization"]["Authorization"],
                            "Content-Type": "application/json;charset=UTF-8"},
                                                        params=body)
                        url = interface_url + charts4_url
                        params = json.dumps(body)

                        if os.path.exists(file) is True:
                            pass
                        else:
                            fp = open(file, 'wb')
                            fp.write(charts4_send.text.encode())
                            fp.close()

                        # 判断文件是否有信息
                        sz = os.path.getsize(file)
                        if not sz:
                            fp = open(file, 'wb')
                            fp.write(charts4_send.text.encode())
                            self.assertEqual(4, 4)
                        else:
                            fp = open(file, 'r', encoding='UTF-8')
                            # 因为每次请求的token值不一样 =所以得删除掉在对比
                            dict_fp = json.loads(fp.read())
                            dict_ramscharts = json.loads(charts4_send.text)
                            del dict_fp['token']
                            del dict_ramscharts['token']
                            if dict_fp == dict_ramscharts:

                                self.assertEqual(4, 4)
                            else:
                                if 'result' in dict_ramscharts.keys():
                                    result = dict_ramscharts['result']
                                    del dict_ramscharts['result']

                                    write_sheet(path, '内控模型图表4接口', url, params,
                                                json.dumps(dict_ramscharts, ensure_ascii=False),
                                                json.dumps(result, ensure_ascii=False)[:2000])
                                else:
                                    write_sheet(path, '内控模型图表4接口', url, params,
                                                json.dumps(dict_ramscharts, ensure_ascii=False),
                                                '')

                                self.assertEqual(3, 4)

                        fp.close()

                    else:
                        # 先放着处理逻辑
                        text = ''
                        # 清空存放接口result的文件
                        if os.path.exists(file) is True:
                            fp = open(file, 'wb')
                            fp.truncate()
                            fp.close()
                        else:
                            fp = open(file, 'wb')
                            fp.write(text)
                            fp.close()


                except AssertionError:
                    logger.error(AssertionError)
                    self.assertEqual(3, 4)
            else:
                pass



if __name__ == '__main__':
    report = r"{}/Report.html".format(path_dir)  # 定义测试报告的名称（日期+report.html，引用report_name函数实现）
    fp = open(report, 'wb')
    st = unittest.TestSuite()
    # st.addTest(test_ramsInterface('test_1_login'))
    # st.addTest(test_ramsInterface('test_2_ramsEvaluate'))
    # st.addTest(test_ramsInterface('test_3_getModelStatus'))
    # st.addTest(test_ramsInterface('test_4_ramsEvaluate_charts'))
    st.addTest(unittest.makeSuite(test_innerControl))
    # unittest.main()
    runner = HTMLTestRunner(stream=fp, verbosity=2, title='接口测试报告', description='测试结果如下: ')
    runner.run(st)  # 执行测试

    fp.close()  # 关闭文件流，将HTML内容写进测试报告文件