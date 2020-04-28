from selenium import webdriver
from interfaceTest.config.main import *
import requests
import json
import ddt
from interfaceTest.libext.HTMLTestRunner import *
from interfaceTest.config.config import *

@ddt.ddt
class test_eds(unittest.TestCase):
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

    @ddt.file_data('{}/testInput/test_eds_input/test_2_edsFuzzyList.json'.format(path_dir))
    def test_2_edsFuzzyList(self,data):
        """EDS查询列表"""
        path = self.path
        if len(globals()["Authorization"]) == 0:
            write_sheet(path, 'EDS查询列表接口', '', '', '用户未登录', '')
            self.assertEqual(3, 4)
        else:
            try:
                # 获取获取模型配置接口的地址
                edsFuzzyList_interface_url = "/darams/cause/fuzzy/list"

                body = data

                # 请求计算接口
                edsFuzzyList_send = requests.post(interface_url + edsFuzzyList_interface_url,
                                                headers={
                                                    "Authorization": globals()["Authorization"][
                                                        "Authorization"],
                                                    "Content-Type": "application/json;charset=UTF-8"},
                                                  data=json.dumps(body))

                edsFuzzyList_response = json.loads(edsFuzzyList_send.text)

                url = interface_url + edsFuzzyList_interface_url
                params = json.dumps(data,ensure_ascii=False)

                if edsFuzzyList_send.status_code == 200:
                    if edsFuzzyList_response['success'] is True:
                        if edsFuzzyList_response['result'] is None:
                            self.assertEqual(3,4)
                        else:
                            self.assertEqual(4, 4)
                    else:
                        if 'result' in edsFuzzyList_response.keys():
                            result = edsFuzzyList_response['result']
                            del edsFuzzyList_response['result']

                            write_sheet(path, 'EDS查询列表接口', url, params,
                                        json.dumps(edsFuzzyList_response, ensure_ascii=False), json.dumps(result))
                        else:
                            write_sheet(path, 'EDS查询列表接口', url, params,
                                        json.dumps(edsFuzzyList_response, ensure_ascii=False), '')

                        self.assertEqual(3, 4)
                else:
                    write_sheet(path, 'EDS查询列表接口', url, params,
                                'EDS查询列表接口返回'.format(edsFuzzyList_response.status_code),
                                '')

                    self.assertEqual(3, 4)

            except AssertionError:
                logger.error(AssertionError)
                self.assertEqual(3, 4)

    @ddt.file_data('{}/testInput/test_eds_input/test_3_edsSelect.json'.format(path_dir))
    def test_3_edsSelect(self,id):
        """源头问题-根据ID查找接口"""
        path = self.path
        if len(globals()["Authorization"]) == 0:
            write_sheet(path, '源头问题-根据ID查找接口', '', '', '用户未登录', '')
            self.assertEqual(3, 4)
        else:
            try:

                # 获取根据ID查找接口的地址
                edsSelect_interface_url = "/darams/cause/select"

                body = {"id":"{}".format(id)}

                # 请求计算接口
                edsSelect_send = requests.post(interface_url + edsSelect_interface_url,
                                                  headers={
                                                      "Authorization": globals()["Authorization"][
                                                          "Authorization"],
                                                      "Content-Type": "application/json;charset=UTF-8"},
                                                  params=body)

                edsFuzzyList_response = json.loads(edsSelect_send.text)

                # 判断文件中是否存在
                file = '{}/testFile/test_eds/test_edsSelect/test_edsSelect_{}.txt'.format(
                    path_dir, id)

                url = interface_url + edsSelect_interface_url
                params = json.dumps(body, ensure_ascii=False)

                if edsSelect_send.status_code == 200:
                    if edsFuzzyList_response['success'] is True:
                        if edsFuzzyList_response['result'] is None:
                            self.assertEqual(3, 4)
                        else:
                            if os.path.exists(file) is True:
                                pass
                            else:
                                fp = open(file, 'wb')
                                fp.write(edsSelect_send.text.encode())
                                fp.close()
                                # 判断文件是否有信息
                            sz = os.path.getsize(file)
                            if not sz:
                                fp = open(file, 'wb')
                                fp.write(edsSelect_send.text.encode())
                                self.assertEqual(4, 4)
                            else:
                                fp = open(file, 'r', encoding='UTF-8')
                                # 因为每次请求的token值不一样 =所以得删除掉在对比
                                dict_fp = json.loads(fp.read())
                                dict_edsSelect = json.loads(edsSelect_send.text)
                                del dict_fp['token']
                                del dict_edsSelect['token']
                                if dict_fp == dict_edsSelect:

                                    self.assertEqual(4, 4)
                                else:
                                    if 'result' in dict_edsSelect.keys():
                                        result = dict_edsSelect['result']
                                        del dict_edsSelect['result']

                                        write_sheet(path, '源头问题-根据ID查找接口', url, params,
                                                    json.dumps(dict_edsSelect, ensure_ascii=False),
                                                    json.dumps(result, ensure_ascii=False)[:2000])
                                    else:
                                        write_sheet(path, '源头问题-根据ID查找接口', url, params,
                                                    json.dumps(dict_edsSelect, ensure_ascii=False),
                                                    '')

                                    self.assertEqual(3, 4)

                            self.assertEqual(4, 4)

                            self.assertEqual(4, 4)
                    else:
                        if 'result' in edsFuzzyList_response.keys():
                            result = edsFuzzyList_response['result']
                            del edsFuzzyList_response['result']

                            write_sheet(path, '源头问题-根据ID查找接口', url, params,
                                        json.dumps(edsFuzzyList_response, ensure_ascii=False), json.dumps(result))
                        else:
                            write_sheet(path, '源头问题-根据ID查找接口', url, params,
                                        json.dumps(edsFuzzyList_response, ensure_ascii=False), '')

                        self.assertEqual(3, 4)
                else:
                    write_sheet(path, '源头问题-根据ID查找接口', url, params,
                                '源头问题-根据ID查找接口返回'.format(edsFuzzyList_response.status_code),
                                '')

                    self.assertEqual(3, 4)

            except AssertionError:
                logger.error(AssertionError)
                self.assertEqual(3, 4)

    @ddt.file_data('{}/testInput/test_eds_input/test_4_edsSave.json'.format(path_dir))
    def test_4_edsSave(self,data):
        """EDS保存接口"""
        path = self.path
        if len(globals()["Authorization"]) == 0:
            write_sheet(path, 'EDS保存接口', '', '', '用户未登录', '')
            self.assertEqual(3, 4)
        else:
            try:

                # 获取保存接口的地址
                edsSave_interface_url = "/darams/cause/save"

                body = data

                # 请求计算接口
                edsSave_send = requests.post(interface_url + edsSave_interface_url,
                                                  headers={
                                                      "Authorization": globals()["Authorization"][
                                                          "Authorization"],
                                                      "Content-Type": "application/json;charset=UTF-8"},
                                                  data=json.dumps(body))

                edsSave_response = json.loads(edsSave_send.text)

                url = interface_url + edsSave_interface_url
                params = json.dumps(data, ensure_ascii=False)

                if edsSave_send.status_code == 200:
                    if edsSave_response['success'] is True:
                        if edsSave_response['result'] is None:
                            write_sheet(path, 'EDS保存接口', url, params,
                                        json.dumps(edsSave_response, ensure_ascii=False), '')
                            self.assertEqual(3, 4)
                        else:
                            self.assertEqual(4, 4)
                    else:
                        if edsSave_response['message'] == '项目名称已重复':
                            self.assertEqual(4, 4)
                        else:
                            if 'result' in edsSave_response.keys():
                                result = edsSave_response['result']
                                del edsSave_response['result']

                                write_sheet(path, 'EDS保存接口', url, params,
                                            json.dumps(edsSave_response, ensure_ascii=False), json.dumps(result))
                            else:
                                write_sheet(path, 'EDS保存接口', url, params,
                                            json.dumps(edsSave_response, ensure_ascii=False), '')

                            self.assertEqual(3, 4)
                else:
                    write_sheet(path, 'EDS保存接口', url, params,
                                'EDS保存接口返回'.format(edsSave_response.status_code),
                                '')

                    self.assertEqual(3, 4)

            except AssertionError:
                logger.error(AssertionError)
                self.assertEqual(3, 4)

    @ddt.file_data('{}/testInput/test_eds_input/test_5_edsExit.json'.format(path_dir))
    def test_5_edsExit(self,id):
        """EDS编辑退出接口"""
        path = self.path
        if len(globals()["Authorization"]) == 0:
            write_sheet(path, 'EDS编辑退出接口', '', '', '用户未登录', '')
            self.assertEqual(3, 4)
        else:
            try:

                # 获取保存接口的地址
                edsExit_interface_url = "/darams/cause/exit"

                body = {
                    "id":"{}".format(id)
                }

                # 请求计算接口
                edsExit_send = requests.post(interface_url + edsExit_interface_url,
                                             headers={
                                                 "Authorization": globals()["Authorization"][
                                                     "Authorization"],
                                                 "Content-Type": "application/json;charset=UTF-8"},
                                             data=json.dumps(body))

                edsExit_response = json.loads(edsExit_send.text)

                url = interface_url + edsExit_interface_url
                params = json.dumps(body, ensure_ascii=False)

                if edsExit_send.status_code == 200:
                    if edsExit_response['success'] is True:

                        self.assertEqual(4, 4)
                    else:

                        if 'result' in edsExit_response.keys():
                            result = edsExit_response['result']
                            del edsExit_response['result']

                            write_sheet(path, 'EDS编辑退出接口', url, params,
                                        json.dumps(edsExit_response, ensure_ascii=False), json.dumps(result))
                        else:
                            write_sheet(path, 'EDS编辑退出接口', url, params,
                                        json.dumps(edsExit_response, ensure_ascii=False), '')

                        self.assertEqual(3, 4)
                else:
                    write_sheet(path, 'EDS编辑退出接口', url, params,
                                'EDS编辑退出接口返回'.format(edsExit_response.status_code),
                                '')

                    self.assertEqual(3, 4)

            except AssertionError:
                logger.error(AssertionError)
                self.assertEqual(3, 4)

    @ddt.file_data('{}/testInput/test_eds_input/test_6_edsCharts.json'.format(path_dir))
    def test_6_edsCharts(self,data):
        """EDS图表接口"""
        path = self.path
        if len(globals()["Authorization"]) == 0:
            write_sheet(path, 'EDS图表接口', '', '', '用户未登录', '')
            self.assertEqual(3, 4)
        else:
            try:

                # 获取保存接口的地址
                edsCharts_interface_url = "/darams/cause/option"

                body = data

                # 请求计算接口
                edsCharts_send = requests.post(interface_url + edsCharts_interface_url,
                                             headers={
                                                 "Authorization": globals()["Authorization"][
                                                     "Authorization"],
                                                 "Content-Type": "application/json;charset=UTF-8"},
                                             params=data)

                edsCharts_response = json.loads(edsCharts_send.text)

                url = interface_url + edsCharts_interface_url
                params = json.dumps(body, ensure_ascii=False)

                if edsCharts_send.status_code == 200:
                    if edsCharts_response['success'] is True:
                        if edsCharts_response['result'] is None:
                            write_sheet(path, 'EDS编辑退出接口', url, params,
                                        json.dumps(edsCharts_response, ensure_ascii=False), '')
                            self.assertEqual(3,4)
                        else:

                            self.assertEqual(4, 4)
                    else:

                        if 'result' in edsCharts_response.keys():
                            result = edsCharts_response['result']
                            del edsCharts_response['result']

                            write_sheet(path, 'EDS编辑退出接口', url, params,
                                        json.dumps(edsCharts_response, ensure_ascii=False), json.dumps(result))
                        else:
                            write_sheet(path, 'EDS编辑退出接口', url, params,
                                        json.dumps(edsCharts_response, ensure_ascii=False), '')

                        self.assertEqual(3, 4)
                else:
                    write_sheet(path, 'EDS编辑退出接口', url, params,
                                'EDS编辑退出接口返回'.format(edsCharts_response.status_code),
                                '')

                    self.assertEqual(3, 4)

            except AssertionError:
                logger.error(AssertionError)
                self.assertEqual(3, 4)

    @ddt.file_data('{}/testInput/test_eds_input/test_7_edsPublish.json'.format(path_dir))
    def test_7_edsPublish(self,data):
        """EDS问题发布接口"""
        path = self.path
        if len(globals()["Authorization"]) == 0:
            write_sheet(path, 'EDS图表接口', '', '', '用户未登录', '')
            self.assertEqual(3, 4)
        else:
            try:

                # 获取问题发布接口的地址
                edsPublish_interface_url = "/darams/cause/publish"

                body = data

                # 请求计算接口
                edsPublish_send = requests.post(interface_url + edsPublish_interface_url,
                                               headers={
                                                   "Authorization": globals()["Authorization"][
                                                       "Authorization"],
                                                   "Content-Type": "application/json;charset=UTF-8"},
                                               data=json.dumps(body))

                edsPublish_response = json.loads(edsPublish_send.text)

                url = interface_url + edsPublish_interface_url
                params = json.dumps(body, ensure_ascii=False)

                if edsPublish_send.status_code == 200:
                    if edsPublish_response['success'] is True:

                        self.assertEqual(4, 4)
                    else:

                        if 'result' in edsPublish_response.keys():
                            result = edsPublish_response['result']
                            del edsPublish_response['result']

                            write_sheet(path, 'EDS问题发布接口', url, params,
                                        json.dumps(edsPublish_response, ensure_ascii=False), json.dumps(result))
                        else:
                            write_sheet(path, 'EDS问题发布接口', url, params,
                                        json.dumps(edsPublish_response, ensure_ascii=False), '')

                        self.assertEqual(3, 4)
                else:
                    write_sheet(path, 'EDS问题发布接口', url, params,
                                'EDS问题发布接口返回'.format(edsPublish_response.status_code),
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
    st.addTest(unittest.makeSuite(test_eds))
    # unittest.main()
    runner = HTMLTestRunner(stream=fp, verbosity=2, title='接口测试报告', description='测试结果如下: ')
    runner.run(st)  # 执行测试

    fp.close()  # 关闭文件流，将HTML内容写进测试报告文件