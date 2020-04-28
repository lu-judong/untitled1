from selenium import webdriver
from interfaceTest.config.main import *
import requests
import json
import ddt
from interfaceTest.libext.HTMLTestRunner import *
from interfaceTest.config.config import *


@ddt.ddt
class test_userModelDeploy(unittest.TestCase):
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

    @ddt.file_data('{}/testInput/test_userModelDeploy_input/test_2_getExtend.json'.format(path_dir))
    def test_2_getExtend(self,id):
        """获取模型配置信息接口"""
        path = self.path
        if len(globals()["Authorization"]) == 0:
            write_sheet(path, '获取模型配置信息接口', '', '', '用户未登录', '')
            self.assertEqual(3, 4)
        else:
            try:
                # 获取获取模型配置接口的地址
                getExtend_interface_url = "/darams/model/confModel/getExtend"

                # 判断文件中是否存在
                file = '{}/testFile/test_userModelDeploy/test_getExtend/test_getExtend_{}.txt'.format(
                    path_dir, id)
                body = {"id":"{}".format(id)}

                # 请求接口
                getExtend__send = requests.get(interface_url + getExtend_interface_url,
                                                      headers={
                                                          "Authorization": globals()["Authorization"][
                                                              "Authorization"],
                                                          "Content-Type": "application/json;charset=UTF-8"},
                                                      params=body)

                url = interface_url + getExtend_interface_url
                params = json.dumps(body, ensure_ascii=False)

                if os.path.exists(file) is True:
                    pass
                else:
                    fp = open(file, 'wb')
                    fp.write(getExtend__send.text.encode())
                    fp.close()
                # 判断文件是否有信息
                sz = os.path.getsize(file)
                if not sz:
                    fp = open(file, 'wb')
                    fp.write(getExtend__send.text.encode())
                    self.assertEqual(4, 4)
                else:
                    fp = open(file, 'r', encoding='UTF-8')
                    # 因为每次请求的token值不一样 =所以得删除掉在对比
                    dict_fp = json.loads(fp.read())
                    dict_getExtend = json.loads(getExtend__send.text)
                    del dict_fp['token']
                    del dict_getExtend['token']
                    if dict_fp == dict_getExtend:

                        self.assertEqual(4, 4)
                    else:
                        if 'result' in dict_getExtend.keys():
                            result = dict_getExtend['result']
                            del dict_getExtend['result']

                            write_sheet(path, '获取模型配置信息接口', url, params,
                                        json.dumps(dict_getExtend, ensure_ascii=False),
                                        json.dumps(result, ensure_ascii=False)[:2000])
                        else:
                            write_sheet(path, '获取模型配置信息接口', url, params,
                                        json.dumps(dict_getExtend, ensure_ascii=False),
                                        '')

                        self.assertEqual(3, 4)

                fp.close()

            except AssertionError:
                logger.error(AssertionError)
                self.assertEqual(3, 4)

    @ddt.file_data('{}/testInput/test_userModelDeploy_input/test_3_fuzzyQuery.json'.format(path_dir))
    def test_3_fuzzyQuery(self,model):
        """获取模型列表模型 - 模糊查询（分页）接口"""
        path = self.path
        if len(globals()["Authorization"]) == 0:
            write_sheet(path, '获取模型列表模型接口', '', '', '用户未登录', '')
            self.assertEqual(3, 4)
        else:
            try:
                # 获取获取模型配置接口的地址
                fuzzyQuery_interface_url = "/darams/model/confModel/fuzzyQuery"


                body = model

                # 请求计算接口
                fuzzyQuery_send = requests.post(interface_url + fuzzyQuery_interface_url,
                                                headers={
                                                    "Authorization": globals()["Authorization"][
                                                        "Authorization"],
                                                    "Content-Type": "application/json;charset=UTF-8"},
                                                data=json.dumps(body))

                fuzzyQuery_response = json.loads(fuzzyQuery_send.text)

                url = interface_url + fuzzyQuery_interface_url
                params = json.dumps(body, ensure_ascii=False)

                if fuzzyQuery_send.status_code == 200:
                    if fuzzyQuery_response['success'] is True:
                        self.assertEqual(4, 4)
                    else:
                        if 'result' in fuzzyQuery_response.keys():
                            result = fuzzyQuery_response['result']
                            del fuzzyQuery_response['result']

                            write_sheet(path, '获取模型列表模型接口', url, params,
                                        json.dumps(fuzzyQuery_response, ensure_ascii=False), json.dumps(result))
                        else:
                            write_sheet(path, '获取模型列表模型接口', url, params,
                                        json.dumps(fuzzyQuery_response, ensure_ascii=False), '')

                        self.assertEqual(3, 4)
                else:
                    write_sheet(path, '获取模型列表模型接口', url, params, '获取模型列表模型接口返回'.format(fuzzyQuery_response.status_code), '')

                    self.assertEqual(3, 4)

            except AssertionError:
                logger.error(AssertionError)
                self.assertEqual(3, 4)


    @ddt.file_data('{}/testInput/test_userModelDeploy_input/test_4_modelSave.json'.format(path_dir))
    def test_4_modelSave(self,save):
        """保存模型配置信息接口"""
        path = self.path
        if len(globals()["Authorization"]) == 0:
            write_sheet(path, '保存模型配置信息接口', '', '', '用户未登录', '')
            self.assertEqual(3, 4)
        else:
            try:
                # 获取获取模型配置接口的地址
                fuzzyQuery_interface_url = "/darams/model/confModel/save"

                body = save

                # 请求计算接口
                modelSave_send = requests.post(interface_url + fuzzyQuery_interface_url,
                                                headers={
                                                    "Authorization": globals()["Authorization"][
                                                        "Authorization"],
                                                    "Content-Type": "application/json;charset=UTF-8"},
                                                data=json.dumps(body))

                modelSave_response = json.loads(modelSave_send.text)

                url = interface_url + fuzzyQuery_interface_url
                params = json.dumps(body, ensure_ascii=False)

                if modelSave_send.status_code == 200:
                    if modelSave_response['success'] is True:
                        self.assertEqual(4, 4)
                    else:
                        if 'result' in modelSave_response.keys():
                            result = modelSave_response['result']
                            del modelSave_response['result']

                            write_sheet(path, '保存模型配置信息接口', url, params,
                                        json.dumps(modelSave_response, ensure_ascii=False), json.dumps(result))
                        else:
                            write_sheet(path, '保存模型配置信息接口', url, params,
                                        json.dumps(modelSave_response, ensure_ascii=False), '')

                        self.assertEqual(3, 4)
                else:
                    write_sheet(path, '保存模型配置信息接口', url, params, '保存模型配置信息接口返回'.format(modelSave_response.status_code),
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
    st.addTest(unittest.makeSuite(test_userModelDeploy))
    # unittest.main()
    runner = HTMLTestRunner(stream=fp, verbosity=2, title='接口测试报告', description='测试结果如下: ')
    runner.run(st)  # 执行测试

    fp.close()  # 关闭文件流，将HTML内容写进测试报告文件