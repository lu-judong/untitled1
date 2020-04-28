from selenium import webdriver
from interfaceTest.config.main import *
import requests
import json
import ddt
from interfaceTest.libext.HTMLTestRunner import *
from interfaceTest.config.config import *

@ddt.ddt
class test_calculate(unittest.TestCase):
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

    # @ddt.file_data('{}/testInput/test_calculate_input/test_2_disposableModelCalculate.json'.format(path_dir))
    # def test_2_disposableModelCalculate(self,data):
    #     """三合一计算接口"""
    #     path = self.path
    #     if len(globals()["Authorization"]) == 0:
    #         write_sheet(path, '三合一计算接口', '', '', '用户未登录', '')
    #         self.assertEqual(3, 4)
    #     else:
    #         try:
    #             # 获取计算接口的地址
    #             disposableModel_interface_url = "/darams/disposableModel/calculate"
    #
    #             # 判断文件中是否存在
    #             file = '{}/testFile/test_calculate/test_disposableModel/test_disposableModel_{}.txt'.format(
    #                 path_dir, data['modelId'])
    #             body = data
    #
    #
    #             # 请求计算接口
    #             disposableModel_send = requests.post(interface_url + disposableModel_interface_url,
    #                                                 headers={
    #                                                     "Authorization": globals()["Authorization"][
    #                                                         "Authorization"],
    #                                                     "Content-Type": "application/json;charset=UTF-8"},
    #                                                 data=json.dumps(body))
    #
    #             url = interface_url + disposableModel_interface_url
    #             params = json.dumps(body, ensure_ascii=False)
    #
    #             if os.path.exists(file) is True:
    #                 pass
    #             else:
    #                 fp = open(file, 'wb')
    #                 fp.write(disposableModel_send.text.encode())
    #                 fp.close()
    #
    #                 # 判断文件是否有信息
    #                 sz = os.path.getsize(file)
    #                 if not sz:
    #                     fp = open(file, 'wb')
    #                     fp.write(disposableModel_send.text.encode())
    #                     self.assertEqual(4, 4)
    #                 else:
    #                     fp = open(file, 'r', encoding='UTF-8')
    #                     # 因为每次请求的token值不一样 =所以得删除掉在对比
    #                     dict_fp = json.loads(fp.read())
    #                     dict_ramscharts = json.loads(disposableModel_send.text)
    #                     del dict_fp['token']
    #                     del dict_ramscharts['token']
    #                     if dict_fp == dict_ramscharts:
    #
    #                         self.assertEqual(4, 4)
    #                     else:
    #                         if 'result' in dict_ramscharts.keys():
    #                             result = dict_ramscharts['result']
    #                             del dict_ramscharts['result']
    #
    #                             write_sheet(path, '三合一计算接口', url, params,
    #                                         json.dumps(dict_ramscharts, ensure_ascii=False),
    #                                         json.dumps(result, ensure_ascii=False)[:2000])
    #                         else:
    #                             write_sheet(path, '三合一计算接口', url, params,
    #                                         json.dumps(dict_ramscharts, ensure_ascii=False),
    #                                         '')
    #
    #                         self.assertEqual(3, 4)
    #
    #                 fp.close()
    #
    #         except AssertionError:
    #             logger.error(AssertionError)
    #             self.assertEqual(3, 4)
    #
    # @ddt.file_data('{}/testInput/test_calculate_input/test_3_repairDontSaveCalculate.json'.format(path_dir))
    # def test_3_repairDontSaveCalculate(self,data):
    #     """修程修制不保存计算接口"""
    #     path = self.path
    #     if len(globals()["Authorization"]) == 0:
    #         write_sheet(path, '修程修制不保存计算接口', '', '', '用户未登录', '')
    #         self.assertEqual(3, 4)
    #     else:
    #         try:
    #
    #             # 获取修程修制不保存计算接口的地址
    #             repairDontSave_interface_url = "/darams/disposableModel/dontSaveCalculate"
    #
    #             body = data
    #             # 请求计算接口
    #             repairDontSave_send = requests.post(interface_url + repairDontSave_interface_url,
    #                                                  headers={
    #                                                      "Authorization": globals()["Authorization"][
    #                                                          "Authorization"],
    #                                                      "Content-Type": "application/json;charset=UTF-8"},
    #                                                  data=json.dumps(body))
    #             repairDontSave_response = json.loads(repairDontSave_send.text)
    #
    #             url = interface_url + repairDontSave_interface_url
    #             params = json.dumps(body, ensure_ascii=False)
    #             if repairDontSave_send.status_code == 200:
    #                 # 得到登录接口的返回
    #                 if repairDontSave_response['success'] is True:
    #                     self.assertEqual(4, 4)
    #                 else:
    #                     globals()["Authorization"] = {}
    #
    #                     if 'result' in repairDontSave_response.keys():
    #                         result = repairDontSave_response['result']
    #                         del repairDontSave_response['result']
    #
    #                         write_sheet(path, '修程修制不保存计算接口', url, params, json.dumps(repairDontSave_response, ensure_ascii=False),
    #                                     json.dumps(result, ensure_ascii=False))
    #                     else:
    #                         write_sheet(path, '修程修制不保存计算接口', url, params, json.dumps(repairDontSave_response, ensure_ascii=False), '')
    #                     self.assertEqual(3, 4)
    #             else:
    #                 globals()["Authorization"] = {}
    #
    #                 write_sheet(path, '修程修制不保存计算接口', url, params, '修程修制不保存计算接口返回:{}'.format(repairDontSave_response.status_code), '')
    #
    #                 self.assertEqual(3, 4)
    #
    #         except AssertionError:
    #             logger.error(AssertionError)
    #             self.assertEqual(3, 4)
    #
    # @ddt.file_data('{}/testInput/test_calculate_input/test_4_techDontSaveCalculate.json'.format(path_dir))
    # def test_4_techDontSaveCalculate(self,data):
    #     """技术变更不保存计算接口"""
    #     path = self.path
    #     if len(globals()["Authorization"]) == 0:
    #         write_sheet(path, '技术变更不保存计算接口', '', '', '用户未登录', '')
    #         self.assertEqual(3, 4)
    #     else:
    #         try:
    #             # 获取技术变更不保存计算接口的地址
    #             techDontSave_interface_url = "/darams/disposableModel/dontSaveCalculate"
    #
    #             body = data
    #             # 请求计算接口
    #             techDontSave_send = requests.post(interface_url + techDontSave_interface_url,
    #                                                 headers={
    #                                                     "Authorization": globals()["Authorization"][
    #                                                         "Authorization"],
    #                                                     "Content-Type": "application/json;charset=UTF-8"},
    #                                                 data=json.dumps(body))
    #             techDontSave_response = json.loads(techDontSave_send.text)
    #
    #             url = interface_url + techDontSave_interface_url
    #             params = json.dumps(body, ensure_ascii=False)
    #             if techDontSave_send.status_code == 200:
    #                 # 得到登录接口的返回
    #                 if techDontSave_response['success'] is True:
    #                     self.assertEqual(4, 4)
    #                 else:
    #                     globals()["Authorization"] = {}
    #
    #                     if 'result' in techDontSave_response.keys():
    #                         result = techDontSave_response['result']
    #                         del techDontSave_response['result']
    #
    #                         write_sheet(path, '技术变更不保存计算接口', url, params,
    #                                     json.dumps(techDontSave_response, ensure_ascii=False),
    #                                     json.dumps(result, ensure_ascii=False))
    #                     else:
    #                         write_sheet(path, '技术变更不保存计算接口', url, params,
    #                                     json.dumps(techDontSave_response, ensure_ascii=False), '')
    #                     self.assertEqual(3, 4)
    #             else:
    #                 globals()["Authorization"] = {}
    #
    #                 write_sheet(path, '技术变更不保存计算接口', url, params,
    #                             '技术变更不保存计算接口返回:{}'.format(techDontSave_response.status_code), '')
    #
    #                 self.assertEqual(3, 4)
    #
    #         except AssertionError:
    #             logger.error(AssertionError)
    #             self.assertEqual(3, 4)

    @ddt.file_data('{}/testInput/test_calculate_input/test_5_moreDontSaveCalculate.json'.format(path_dir))
    def test_5_moreDontSaveCalculate(self,data):
        """多模型不保存计算接口"""
        path = self.path
        if len(globals()["Authorization"]) == 0:
            write_sheet(path, '多模型不保存计算接口', '', '', '用户未登录', '')
            self.assertEqual(3, 4)
        else:
            try:
                # 获取技术变更不保存计算接口的地址
                moreDontSave_interface_url = "/darams/disposableModel/dontSaveCalculate"

                body = data
                # 请求计算接口
                moreDontSave_send = requests.post(interface_url + moreDontSave_interface_url,
                                                  headers={
                                                      "Authorization": globals()["Authorization"][
                                                          "Authorization"],
                                                      "Content-Type": "application/json;charset=UTF-8"},
                                                  data=json.dumps(body))
                moreDontSave_response = json.loads(moreDontSave_send.text)

                url = interface_url + moreDontSave_interface_url
                params = json.dumps(body, ensure_ascii=False)
                if moreDontSave_send.status_code == 200:
                    # 得到登录接口的返回
                    if moreDontSave_response['success'] is True:
                        self.assertEqual(4, 4)
                    else:
                        globals()["Authorization"] = {}

                        if 'result' in moreDontSave_response.keys():
                            result = moreDontSave_response['result']
                            del moreDontSave_response['result']

                            write_sheet(path, '多模型不保存计算接口', url, params,
                                        json.dumps(moreDontSave_response, ensure_ascii=False),
                                        json.dumps(result, ensure_ascii=False))
                        else:
                            write_sheet(path, '多模型不保存计算接口', url, params,
                                        json.dumps(moreDontSave_response, ensure_ascii=False), '')
                        self.assertEqual(3, 4)
                else:
                    globals()["Authorization"] = {}

                    write_sheet(path, '多模型不保存计算接口', url, params,
                                '多模型不保存计算接口返回:{}'.format(moreDontSave_response.status_code), '')

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
    st.addTest(unittest.makeSuite(test_calculate))
    # unittest.main()
    runner = HTMLTestRunner(stream=fp, verbosity=2, title='接口测试报告', description='测试结果如下: ')
    runner.run(st)  # 执行测试

    fp.close()  # 关闭文件流，将HTML内容写进测试报告文件