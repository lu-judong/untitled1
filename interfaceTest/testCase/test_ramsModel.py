from selenium import webdriver
from interfaceTest.config.main import *
import requests
import json
import ddt
from interfaceTest.libext.HTMLTestRunner import *
from interfaceTest.config.config import *


@ddt.ddt
class test_ramsModel(unittest.TestCase):
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

    @ddt.file_data('{}/testInput/test_ramsModel_input/test_2_getTrainTypeTree.json'.format(path_dir))
    def test_2_getTrainTypeTree(self,trainNoIds,faultObjectNames):
        """查找车型部件数接口"""
        path = self.path
        if len(globals()["Authorization"]) == 0:
            write_sheet(path, '查找车型部件数接口', '', '', '用户未登录', '')
            self.assertEqual(3, 4)
        else:
            try:
                driver = self.driver
                driver.refresh()

                time.sleep(2)
                Method(driver).click('xpath', '//span[contains(text(),"RAMS模型相关接口")]')
                time.sleep(1)

                Method(driver).circle_click("查找车型部件树")
                time.sleep(2)
                # 获取计算接口的地址
                getTrainTypeTree_interface_url = driver.find_element_by_xpath('//span[text()="接口地址"]/../code').text

                # 判断文件中是否存在
                file = '{}/testFile/test_ramsModel/test_getTrainTypeTree/test_getTrainTypeTree_{}.txt'.format(
                    path_dir, trainNoIds)
                body = {
                    "trainNoIds":"{}".format(trainNoIds),
                    "faultObjectNames":"{}".format(faultObjectNames)
                }

                # 请求计算接口
                getTrainTypeTree_send = requests.post(interface_url + getTrainTypeTree_interface_url,
                                                     headers={
                                                         "Authorization": globals()["Authorization"][
                                                             "Authorization"],
                                                         "Content-Type": "application/json;charset=UTF-8"},
                                                     params=body)

                url = interface_url + getTrainTypeTree_interface_url
                params = json.dumps(body, ensure_ascii=False)

                if os.path.exists(file) is True:
                    pass
                else:
                    fp = open(file, 'wb')
                    fp.write(getTrainTypeTree_send.text.encode())
                    fp.close()
                    # 判断文件是否有信息
                    sz = os.path.getsize(file)
                    if not sz:
                        fp = open(file, 'wb')
                        fp.write(getTrainTypeTree_send.text.encode())
                        self.assertEqual(4, 4)
                    else:
                        fp = open(file, 'r', encoding='UTF-8')
                        # 因为每次请求的token值不一样 =所以得删除掉在对比
                        dict_fp = json.loads(fp.read())
                        dict_getTrainTypeTree = json.loads(getTrainTypeTree_send.text)
                        del dict_fp['token']
                        del dict_getTrainTypeTree['token']
                        if dict_fp == dict_getTrainTypeTree:

                            self.assertEqual(4, 4)
                        else:
                            if 'result' in dict_getTrainTypeTree.keys():
                                result = dict_getTrainTypeTree['result']
                                del dict_getTrainTypeTree['result']

                                write_sheet(path, '查找车型部件数接口', url, params,
                                            json.dumps(dict_getTrainTypeTree, ensure_ascii=False),
                                            json.dumps(result, ensure_ascii=False)[:2000])
                            else:
                                write_sheet(path, '查找车型部件数接口', url, params,
                                            json.dumps(dict_getTrainTypeTree, ensure_ascii=False),
                                            '')

                            self.assertEqual(3, 4)

                    fp.close()

            except AssertionError:
                logger.error(AssertionError)
                self.assertEqual(3, 4)

    @ddt.file_data('{}/testInput/test_ramsModel_input/test_3_getPageFaultPattern.json'.format(path_dir))
    def test_3_getPageFaultPattern(self,data):
        """根据部件id查询故障对象接口"""
        path = self.path
        if len(globals()["Authorization"]) == 0:
            write_sheet(path, '根据部件id查询故障对象接口', '', '', '用户未登录', '')
            self.assertEqual(3, 4)
        else:
            try:
                driver = self.driver
                driver.refresh()

                time.sleep(2)
                Method(driver).click('xpath', '//span[contains(text(),"RAMS模型相关接口")]')
                time.sleep(1)

                Method(driver).circle_click("根据部件id查询故障对象")
                time.sleep(1)
                # 获取计算接口的地址
                getPageFaultPattern_interface_url = driver.find_element_by_xpath('//span[text()="接口地址"]/../code').text

                # 判断文件中是否存在
                file = '{}/testFile/test_ramsModel/test_getPageFaultPattern/test_getPageFaultPattern_{}.txt'.format(
                    path_dir, data['faultObjectId'])
                body = data

                # 请求计算接口
                getPageFaultPattern_send = requests.post(interface_url + getPageFaultPattern_interface_url,
                                                      headers={
                                                          "Authorization": globals()["Authorization"][
                                                              "Authorization"],
                                                          "Content-Type": "application/json;charset=UTF-8"},
                                                      params=body)

                url = interface_url + getPageFaultPattern_interface_url
                params = json.dumps(body, ensure_ascii=False)

                if os.path.exists(file) is True:
                    pass
                else:
                    fp = open(file, 'wb')
                    fp.write(getPageFaultPattern_send.text.encode())
                    fp.close()
                    # 判断文件是否有信息
                    sz = os.path.getsize(file)
                    if not sz:
                        fp = open(file, 'wb')
                        fp.write(getPageFaultPattern_send.text.encode())
                        self.assertEqual(4, 4)
                    else:
                        fp = open(file, 'r', encoding='UTF-8')
                        # 因为每次请求的token值不一样 =所以得删除掉在对比
                        dict_fp = json.loads(fp.read())
                        dict_getPageFaultPattern = json.loads(getPageFaultPattern_send.text)
                        del dict_fp['token']
                        del dict_getPageFaultPattern['token']
                        if dict_fp == dict_getPageFaultPattern:

                            self.assertEqual(4, 4)
                        else:
                            if 'result' in dict_getPageFaultPattern.keys():
                                result = dict_getPageFaultPattern['result']
                                del dict_getPageFaultPattern['result']

                                write_sheet(path, '根据部件id查询故障对象接口', url, params,
                                            json.dumps(dict_getPageFaultPattern, ensure_ascii=False),
                                            json.dumps(result, ensure_ascii=False)[:2000])
                            else:
                                write_sheet(path, '根据部件id查询故障对象接口', url, params,
                                            json.dumps(dict_getPageFaultPattern, ensure_ascii=False),
                                            '')

                            self.assertEqual(3, 4)

                    fp.close()

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
    st.addTest(unittest.makeSuite(test_ramsModel))
    # unittest.main()
    runner = HTMLTestRunner(stream=fp, verbosity=2, title='接口测试报告', description='测试结果如下: ')
    runner.run(st)  # 执行测试

    fp.close()  # 关闭文件流，将HTML内容写进测试报告文件
