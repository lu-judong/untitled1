from selenium import webdriver
from interfaceTest.config.main import *
import requests
import json
import ddt
from interfaceTest.libext.HTMLTestRunner import *
from interfaceTest.config.config import *



@ddt.ddt
class test_homePage(unittest.TestCase):
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


    def test_2_getMenuTree(self):
        """获取配置图表的菜单树接口"""
        path = self.path
        if len(globals()["Authorization"]) == 0:
            write_sheet(path, '获取配置图表的菜单树接口', '', '', '用户未登录', '')
            self.assertEqual(3, 4)
        else:
            try:
                driver = self.driver
                driver.refresh()

                time.sleep(2)
                # 点击搜索

                Method(driver).click('xpath', '//span[contains(text(),"首页相关接口")]')
                time.sleep(1)

                # 点击登录
                Method(driver).circle_click('获取配置图表的菜单树')
                time.sleep(1)
                # 获取获取模型配置接口的地址
                getMenuTree_interface_url =  driver.find_element_by_xpath('//span[text()="接口地址"]/../code').text

                # 请求计算接口
                getMenuTree_send = requests.get(interface_url + getMenuTree_interface_url,
                                                headers={
                                                    "Authorization": globals()["Authorization"][
                                                        "Authorization"],
                                                    "Content-Type": "application/json;charset=UTF-8"})

                getMenuTree_response = json.loads(getMenuTree_send.text)

                url = interface_url + getMenuTree_interface_url


                if getMenuTree_send.status_code == 200:
                    if getMenuTree_response['success'] is True:
                        self.assertEqual(4, 4)
                    else:
                        if 'result' in getMenuTree_response.keys():
                            result = getMenuTree_response['result']
                            del getMenuTree_response['result']

                            write_sheet(path, '获取配置图表的菜单树接口', url, '',
                                        json.dumps(getMenuTree_response, ensure_ascii=False), json.dumps(result))
                        else:
                            write_sheet(path, '获取配置图表的菜单树接口', url, '',
                                        json.dumps(getMenuTree_response, ensure_ascii=False), '')

                        self.assertEqual(3, 4)
                else:
                    write_sheet(path, '获取配置图表的菜单树接口', url, '', '获取配置图表的菜单树接口返回'.format(getMenuTree_response.status_code),
                                '')

                    self.assertEqual(3, 4)

            except AssertionError:
                logger.error(AssertionError)
                self.assertEqual(3, 4)

    def test_3_getLayout(self):
        """获取首页布局数据接口"""
        path = self.path
        if len(globals()["Authorization"]) == 0:
            write_sheet(path, '获取首页布局数据接口', '', '', '用户未登录', '')
            self.assertEqual(3, 4)
        else:
            try:
                driver = self.driver
                driver.refresh()

                time.sleep(2)
                # 点击搜索

                Method(driver).click('xpath', '//span[contains(text(),"首页相关接口")]')
                time.sleep(1)

                # 点击登录
                Method(driver).circle_click('获取首页布局数据')
                time.sleep(1)
                # 获取获取模型配置接口的地址
                getLayout_interface_url =  driver.find_element_by_xpath('//span[text()="接口地址"]/../code').text

                # 请求计算接口
                getLayout_send = requests.get(interface_url + getLayout_interface_url,
                                                headers={
                                                    "Authorization": globals()["Authorization"][
                                                        "Authorization"],
                                                    "Content-Type": "application/json;charset=UTF-8"})

                getLayout_response = json.loads(getLayout_send.text)

                url = interface_url + getLayout_interface_url

                if getLayout_send.status_code == 200:
                    if getLayout_response['success'] is True:
                        self.assertEqual(4, 4)
                    else:
                        if 'result' in getLayout_response.keys():
                            result = getLayout_response['result']
                            del getLayout_response['result']

                            write_sheet(path, '获取首页布局数据接口', url, '',
                                        json.dumps(getLayout_response, ensure_ascii=False), json.dumps(result))
                        else:
                            write_sheet(path, '获取首页布局数据接口', url, '',
                                        json.dumps(getLayout_response, ensure_ascii=False), '')

                        self.assertEqual(3, 4)
                else:
                    write_sheet(path, '获取首页布局数据接口', url, '',
                                '获取首页布局数据接口返回'.format(getLayout_response.status_code),
                                '')

                    self.assertEqual(3, 4)

            except AssertionError:
                logger.error(AssertionError)
                self.assertEqual(3, 4)

    @ddt.file_data('{}/testInput/test_homePage_input/test_4_getCharts.json'.format(path_dir))
    def test_4_getCharts(self,data):
        """获取首页图表接口"""
        path = self.path
        if len(globals()["Authorization"]) == 0:
            write_sheet(path, '获取首页图表接口', '', '', '用户未登录', '')
            self.assertEqual(3, 4)
        else:
            try:
                driver = self.driver
                driver.refresh()

                time.sleep(2)
                # 点击搜索

                Method(driver).click('xpath', '//span[contains(text(),"首页相关接口")]')
                time.sleep(1)

                # 点击登录
                Method(driver).circle_click('获取图表')
                time.sleep(1)
                # 获取首页图表接口的地址
                getCharts_interface_url = driver.find_element_by_xpath('//span[text()="接口地址"]/../code').text

                # 判断文件是否存在
                file = '{}/testFile/test_homePage/test_getCharts/test_getCharts_{}.txt'.format(
                    path_dir, data[0]["modelId"])
                body = data

                # 请求接口
                getCharts_send = requests.post(interface_url + getCharts_interface_url,
                                               headers={
                                                   "Authorization": globals()["Authorization"][
                                                       "Authorization"],
                                                   "Content-Type": "application/json;charset=UTF-8"},
                                               data=json.dumps(body))

                url = interface_url + getCharts_interface_url
                params = json.dumps(body, ensure_ascii=False)

                if os.path.exists(file) is True:
                    pass
                else:
                    fp = open(file, 'wb')
                    fp.write(getCharts_send.text.encode())
                    fp.close()
                # 判断文件是否有信息
                sz = os.path.getsize(file)
                if not sz:
                    fp = open(file, 'wb')
                    fp.write(getCharts_send.text.encode())
                    self.assertEqual(4, 4)
                else:
                    fp = open(file, 'r', encoding='UTF-8')
                    # 因为每次请求的token值不一样 =所以得删除掉在对比
                    dict_fp = json.loads(fp.read())
                    dict_getCharts = json.loads(getCharts_send.text)
                    del dict_fp['token']
                    del dict_getCharts['token']
                    if dict_fp == dict_getCharts:

                        self.assertEqual(4, 4)
                    else:
                        if 'result' in dict_getCharts.keys():
                            result = dict_getCharts['result']
                            del dict_getCharts['result']

                            write_sheet(path, '获取首页图表接口', url, params,
                                        json.dumps(dict_getCharts, ensure_ascii=False),
                                        json.dumps(result, ensure_ascii=False)[:2000])
                        else:
                            write_sheet(path, '获取首页图表接口', url, params,
                                        json.dumps(dict_getCharts, ensure_ascii=False),
                                        '')

                        self.assertEqual(3, 4)

                fp.close()

            except AssertionError:
                logger.error(AssertionError)
                self.assertEqual(3, 4)

    @ddt.file_data('{}/testInput/test_homePage_input/test_5_saveLayout.json'.format(path_dir))
    def test_5_saveLayout(self,data):
        """保存首页布局数据接口"""
        path = self.path
        if len(globals()["Authorization"]) == 0:
            write_sheet(path, '获取首页布局数据接口', '', '', '用户未登录', '')
            self.assertEqual(3, 4)
        else:
            try:
                driver = self.driver
                driver.refresh()

                time.sleep(2)
                # 点击搜索

                Method(driver).click('xpath', '//span[contains(text(),"首页相关接口")]')
                time.sleep(1)

                # 点击登录
                Method(driver).circle_click('保存首页布局数据')
                time.sleep(1)
                # 获取获取模型配置接口的地址
                saveLayout_interface_url = driver.find_element_by_xpath('//span[text()="接口地址"]/../code').text

                # 请求计算接口
                saveLayout_send = requests.post(interface_url + saveLayout_interface_url,
                                              headers={
                                                  "Authorization": globals()["Authorization"][
                                                      "Authorization"],
                                                  "Content-Type": "application/json;charset=UTF-8"},
                                               data = json.dumps(data))

                saveLayout_response = json.loads(saveLayout_send.text)

                url = interface_url + saveLayout_interface_url

                if saveLayout_send.status_code == 200:
                    if saveLayout_response['success'] is True:
                        self.assertEqual(4, 4)
                    else:
                        if 'result' in saveLayout_response.keys():
                            result = saveLayout_response['result']
                            del saveLayout_response['result']

                            write_sheet(path, '保存首页布局数据接口', url, '',
                                        json.dumps(saveLayout_response, ensure_ascii=False), json.dumps(result))
                        else:
                            write_sheet(path, '保存首页布局数据接口', url, '',
                                        json.dumps(saveLayout_response, ensure_ascii=False), '')

                        self.assertEqual(3, 4)
                else:
                    write_sheet(path, '保存首页布局数据接口', url, '',
                                '保存首页布局数据接口返回'.format(saveLayout_response.status_code),
                                '')

                    self.assertEqual(3, 4)

            except AssertionError:
                logger.error(AssertionError)
                self.assertEqual(3, 4)

    @ddt.file_data('{}/testInput/test_homePage_input/test_6_conditionPreview.json'.format(path_dir))
    def test_6_conditionPreview(self,modelId):
        """首页模型条件预览接口"""
        path = self.path
        if len(globals()["Authorization"]) == 0:
            write_sheet(path, '首页模型条件预览接口', '', '', '用户未登录', '')
            self.assertEqual(3, 4)
        else:
            try:
                # 获取获取模型配置接口的地址
                conditionPreview_interface_url = "/darams/conditionPreview/preview"
                body = {
                    "modelId":"{}".format(modelId)
                }
                # 请求计算接口
                conditionPreview_send = requests.get(interface_url + conditionPreview_interface_url,
                                                headers={
                                                    "Authorization": globals()["Authorization"][
                                                        "Authorization"],
                                                    "Content-Type": "application/json;charset=UTF-8"},
                                                params=body)

                conditionPreview_response = json.loads(conditionPreview_send.text)

                url = interface_url + conditionPreview_interface_url
                params = json.dumps(body, ensure_ascii=False)

                # 判断文件中是否存在
                file = '{}/testFile/test_homePage/test_conditionPreview/test_conditionPreview_{}.txt'.format(
                    path_dir, modelId)

                if conditionPreview_send.status_code == 200:
                    if conditionPreview_response['success'] is True:
                        if conditionPreview_response['result'] is None:
                            self.assertEqual(3, 4)
                        else:
                            if os.path.exists(file) is True:
                                pass
                            else:
                                fp = open(file, 'wb')
                                fp.write(conditionPreview_send.text.encode())
                                fp.close()
                            # 判断文件是否有信息
                            sz = os.path.getsize(file)
                            if not sz:
                                fp = open(file, 'wb')
                                fp.write(conditionPreview_send.text.encode())
                                self.assertEqual(4, 4)
                            else:
                                fp = open(file, 'r', encoding='UTF-8')
                                # 因为每次请求的token值不一样 =所以得删除掉在对比
                                dict_fp = json.loads(fp.read())
                                dict_conditionPreview = json.loads(conditionPreview_send.text)
                                del dict_fp['token']
                                del dict_conditionPreview['token']
                                if dict_fp == dict_conditionPreview:

                                    self.assertEqual(4, 4)
                                else:
                                    if 'result' in dict_conditionPreview.keys():
                                        result = dict_conditionPreview['result']
                                        del dict_conditionPreview['result']

                                        write_sheet(path, '获取模型配置信息接口', url, params,
                                                    json.dumps(dict_conditionPreview, ensure_ascii=False),
                                                    json.dumps(result, ensure_ascii=False)[:2000])
                                    else:
                                        write_sheet(path, '获取模型配置信息接口', url, params,
                                                    json.dumps(dict_conditionPreview, ensure_ascii=False),
                                                    '')

                                    self.assertEqual(3, 4)

                            self.assertEqual(4, 4)
                    else:
                        if 'result' in conditionPreview_response.keys():
                            result = conditionPreview_response['result']
                            del conditionPreview_response['result']

                            write_sheet(path, '首页模型条件预览接口', url, '',
                                        json.dumps(conditionPreview_response, ensure_ascii=False), json.dumps(result))
                        else:
                            write_sheet(path, '首页模型条件预览接口', url, '',
                                        json.dumps(conditionPreview_response, ensure_ascii=False), '')

                        self.assertEqual(3, 4)
                else:
                    write_sheet(path, '首页模型条件预览接口', url, '',
                                '首页模型条件预览接口返回'.format(conditionPreview_response.status_code),
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
    st.addTest(unittest.makeSuite(test_homePage))
    # unittest.main()
    runner = HTMLTestRunner(stream=fp, verbosity=2, title='接口测试报告', description='测试结果如下: ')
    runner.run(st)  # 执行测试

    fp.close()  # 关闭文件流，将HTML内容写进测试报告文件