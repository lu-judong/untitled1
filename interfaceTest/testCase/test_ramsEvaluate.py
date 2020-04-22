# -*- coding: utf-8 -*-

# import os
# print(os.getcwd())
# print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))
from selenium import webdriver
from interfaceTest.config.main import *
import requests
import json
import ddt
from interfaceTest.libext.HTMLTestRunner import *
from interfaceTest.config.config import *
from interfaceTest.testInput.test_ramsEvaluate_input.test_4_ramsEvaluate_charts import *

@ddt.ddt
class test_ramsInterface(unittest.TestCase):
    # def runTest(self):
    #     pass
    # def __init__(self,methodName='runTest'):
    #     # unittest.TestCase.__init__(self, methodName)
    #     super(test_ramsInterface, self).__init__(methodName)
    # dr = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    # option = webdriver.ChromeOptions()
    # option.add_argument("headless")
    # dr = webdriver.Chrome(options=option,executable_path=r'{}\apps\chromedriver.exe'.format(path_dir))
    @classmethod
    def setUpClass(cls):  # 类中最先执行
        cls.path = '{}/testOutput/interface-sheet.xls'.format(path_dir)
        create_sheet(cls.path)
        cls.driver = webdriver.Chrome()

        cls.driver.maximize_window()
        cls.driver.get(interface_url + '/darams/doc.html')
        time.sleep(2)
    # def __init__(self,*args, **kwargs):
    #     super(test_ramsInterface, self).__init__(*args, **kwargs)
    #     self.driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))

    # def setUp(self,driver = dr):
    #
    #     self.driver = driver
    #     self.driver.maximize_window()
    #     time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        # cls.driver = driver# 类中最后执行
        cls.driver.quit()

    # @ddt.file_data("../testInput/test_ramsEvaluate_input/test_1_login.json")
    # @ddt.file_data(r'D:/PycharmProjects/untitled/interfaceTest/testInput/test_ramsEvaluate_input/test_1_login.json')
    # @runTest
    # @ddt.data([1,2],[2,3])
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

    @ddt.file_data('{}/testInput/test_ramsEvaluate_input/test_2_ramsEvaluate.json'.format(path_dir))
    def test_2_ramsEvaluate(self,modelId):
        """RAMS指标评估计算接口"""  # 说明测试用例的标题
        # option = webdriver.ChromeOptions()
        # option.add_argument("headless")
        # driver = webdriver.Chrome(executable_path=r'{}\apps\chromedriver.exe'.format(path_dir))
        path = self.path
        if len(globals()["Authorization"]) == 0:

            write_sheet(path, 'RAMS指标评估计算接口', '','','用户未登录','')
            self.assertEqual(3, 4)
        else:
            try:
                driver = self.driver
                driver.refresh()
                time.sleep(2)
                Method(driver).click('xpath', '//span[contains(text(),"Rams指标建模")]')
                time.sleep(1)

                # 计算接口
                # driver.find_element_by_xpath('//*[@id="menu"]/li[8]/ul/li[3]/div/div/span[1]/span').click()
                Method(driver).click('xpath','//*[@id="menu"]/li[8]/ul/li[3]/div/div/span[1]/span')

                # 获取计算接口的地址
                evaluate_interface_url = driver.find_element_by_xpath('//span[text()="接口地址"]/../code').text

                # 请求计算接口
                evaluate_send = requests.post(interface_url + evaluate_interface_url, headers=globals()["Authorization"],
                              params={'modelId': modelId})
                evaluate_response = json.loads(evaluate_send.text)
                url = interface_url + evaluate_interface_url
                params =  json.dumps({'modelId': modelId},ensure_ascii=False)
                if evaluate_send.status_code == 200:


                    if evaluate_response['success'] is True:

                        self.assertEqual(4, 4)
                    else:


                        if 'result'in evaluate_response.keys():
                            result = evaluate_response['result']
                            del evaluate_response['result']

                            write_sheet(path, 'RAMS指标评估计算接口', url, params, json.dumps(evaluate_response, ensure_ascii=False), json.dumps(result))
                        else:
                            write_sheet(path, 'RAMS指标评估计算接口', url, params, json.dumps(evaluate_response, ensure_ascii=False),'')

                        self.assertEqual(3, 4)
                else:
                    write_sheet(path, 'RAMS指标评估计算接口', url, params, 'RAMS指标评估计算接口返回'.format(evaluate_send.status_code),'')

                    self.assertEqual(3, 4)

            except AssertionError:
                logger.error(AssertionError)
                self.assertEqual(3, 4)

    @ddt.file_data('{}/testInput/test_ramsEvaluate_input/test_3_getModelStatus.json'.format(path_dir))
    def test_3_getModelStatus(self,modelId):
        """RAMS模型状态刷新接口"""
        path = self.path
        if len(globals()["Authorization"]) == 0:
            write_sheet(path, 'RAMS模型状态刷新接口', '', '', '用户未登录', '')

            self.assertEqual(3, 4)
        else:
            try:
                driver = self.driver
                driver.refresh()
                time.sleep(2)
                Method(driver).click('xpath', '//span[contains(text(),"用户指标模型配置")]')
                time.sleep(1)
                Method(driver).click('xpath','//span[contains(text(),"根据模型id获取模型计算状态")]')
                time.sleep(1)
                # 获取计算状态接口的地址
                getModelStatus_url = driver.find_element_by_xpath('//span[text()="接口地址"]/../code').text
                # 请求计算状态接口

                for t in range(0,10):
                    # requests.post(interface_url + getModelStatus_url,
                    #               params={"Authorization": globals()["Authorization"],
                    #                       'id': '34e0bf00d47f4b1ea6c518287ce7a86d'})
                    evaluateStatus_send = requests.get(interface_url + getModelStatus_url,
                                                  headers=globals()["Authorization"],
                                                  params={'id': modelId})
                    evaluateStatus_response = json.loads(evaluateStatus_send.text)
                    url = interface_url + getModelStatus_url
                    params = json.dumps({'id': modelId})

                    if evaluateStatus_send.status_code == 200:

                        # 计算完成的情况
                        if evaluateStatus_response['success'] is True:
                            if evaluateStatus_response['result'] == 'calculation_complete' or evaluateStatus_response['result'] == 'calculation_exception' \
                                    or evaluateStatus_response['result'] == 'new':
                                self.assertEqual(4, 4)
                                break
                            else:
                                if t == 9:
                                    self.assertEqual(4, 4)
                                else:
                                    time.sleep(2)
                        else:
                            if 'result' in evaluateStatus_response.keys():
                                result = evaluateStatus_response['result']
                                del evaluateStatus_response['result']

                                write_sheet(path, 'RAMS模型状态刷新接口', url, params, json.dumps(evaluateStatus_response, ensure_ascii=False),json.dumps(result,ensure_ascii=False))
                            else:
                                write_sheet(path, 'RAMS模型状态刷新接口', url, params, json.dumps(evaluateStatus_response, ensure_ascii=False),
                                           '')
                            self.assertEqual(3, 4)
                            break

                    else:
                        write_sheet(path, 'RAMS模型状态刷新接口', url, params, 'RAMS模型状态刷新接口返回{}'.format(evaluateStatus_send.status_code),'')
                        self.assertEqual(3, 4)
                        break


            except AssertionError:
                logger.error(AssertionError)
                self.assertEqual(3, 4)

    @ddt.file_data('{}/testInput/test_ramsEvaluate_input/test_4_ramsEvaluate_charts.json'.format(path_dir))
    def test_4_ramsEvaluate_charts(self,modelId):
        """RAMS图表接口"""
        path = self.path
        if len(globals()["Authorization"]) == 0:
            write_sheet(path, 'RAMS图表接口', '', '', '用户未登录', '')
            self.assertEqual(3, 4)
        else:
            if interface_status != 'non-existent':
                try:
                    driver = self.driver
                    driver.refresh()
                    time.sleep(2)
                    Method(driver).click('xpath', '//span[contains(text(),"Rams指标建模")]')
                    time.sleep(1)

                    # 图表接口
                    # driver.find_element_by_xpath('//*[@id="menu"]/li[8]/ul/li[3]/div/div/span[1]/span').click()
                    Method(driver).click('xpath', '//span[text()="图表(新)"]')
                    # 获取计算状态接口的地址
                    RamsEvaluate_charts_url = driver.find_element_by_xpath('//span[text()="接口地址"]/../code').text


                    # 判断接口状态
                    if interface_status == 'normal':
                        body = {
                            "chartCodes": [],
                            "modelId": "{}".format(modelId),
                            "interval": 1
                        }

                        ramscharts_send = requests.post(interface_url + RamsEvaluate_charts_url, headers={
                            "Authorization": globals()["Authorization"]["Authorization"],
                            "Content-Type": "application/json;charset=UTF-8"},
                                                        data=json.dumps(body))
                        url = interface_url + RamsEvaluate_charts_url
                        params = json.dumps(body)

                        # 判断文件中是否存在
                        file = '{}/testFile/test_ramsEvaluate/test_4_ramsEvaluate_charts/test_4_ramsEvaluate_charts_{}.txt'.format(
                            path_dir, modelId)
                        if os.path.exists(file) is True:
                            pass
                        else:
                            fp = open(file, 'wb')
                            fp.write(ramscharts_send.text.encode())
                            fp.close()

                        # 判断文件是否有信息
                        sz = os.path.getsize(file)
                        if not sz:
                            fp = open(file, 'wb')
                            fp.write(ramscharts_send.text.encode())
                            self.assertEqual(4, 4)
                        else:
                            fp = open(file, 'r', encoding='UTF-8')
                            # 因为每次请求的token值不一样 =所以得删除掉在对比
                            dict_fp = json.loads(fp.read())
                            dict_ramscharts = json.loads(ramscharts_send.text)
                            del dict_fp['token']
                            del dict_ramscharts['token']
                            if dict_fp == dict_ramscharts:

                                self.assertEqual(4, 4)
                            else:
                                if 'result' in dict_ramscharts.keys():
                                    result = dict_ramscharts['result']
                                    del dict_ramscharts['result']

                                    write_sheet(path, 'RAMS图表接口', url, params, json.dumps(dict_ramscharts, ensure_ascii=False),
                                                json.dumps(result, ensure_ascii=False)[:2000])
                                else:
                                    write_sheet(path, 'RAMS图表接口', url, params, json.dumps(dict_ramscharts, ensure_ascii=False),
                                                '')

                            # 测试用代码
                            # result = dict_ramscharts['result']
                            # del dict_ramscharts['result']
                            #
                            # write_sheet(path, 'RAMS图表接口',
                            #             json.dumps(dict_ramscharts, ensure_ascii=False),
                            #             json.dumps(result, ensure_ascii=False)[:2000])
                                self.assertEqual(3, 4)

                        fp.close()

                    else:
                        # 先放着处理逻辑
                        text = ''
                        # 清空存放接口result的文件
                        file = '{}/testFile/test_ramsEvaluate/test_4_ramsEvaluate_charts/test_4_ramsEvaluate_charts_{}.txt'.format(path_dir,modelId)
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


    # def test_4_close(self):
    #     self.driver.close()







    # def test_02(self):
    #     """测试5是否与4相等"""
    #     self.assertEqual(5, 4, '测试失败')




# unittest.main()

if __name__ == '__main__':
    report = r"{}/Report.html".format(path_dir)  # 定义测试报告的名称（日期+report.html，引用report_name函数实现）
    fp = open(report, 'wb')
    st = unittest.TestSuite()
    # st.addTest(test_ramsInterface('test_1_login'))
    # st.addTest(test_ramsInterface('test_2_ramsEvaluate'))
    # st.addTest(test_ramsInterface('test_3_getModelStatus'))
    # st.addTest(test_ramsInterface('test_4_ramsEvaluate_charts'))
    st.addTest(unittest.makeSuite(test_ramsInterface))
    # unittest.main()
    runner = HTMLTestRunner(stream=fp, verbosity=2, title='接口测试报告', description='测试结果如下: ')
    runner.run(st)  # 执行测试

    fp.close()  # 关闭文件流，将HTML内容写进测试报告文件
