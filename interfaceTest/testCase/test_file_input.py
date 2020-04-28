from selenium import webdriver
from interfaceTest.config.main import *
import requests
import json
import ddt
from interfaceTest.libext.HTMLTestRunner import *
from interfaceTest.config.config import *

# 信息发布
@ddt.ddt
class test_file(unittest.TestCase):

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

    def test_2_fileFuzzyQuery(self):
        """信息发布 模糊查询（分页）接口"""
        path = self.path
        if len(globals()["Authorization"]) == 0:
            write_sheet(path, '信息发布 模糊查询（分页）接口', '', '', '用户未登录', '')
            self.assertEqual(3, 4)
        else:
            try:
                driver = self.driver
                driver.refresh()
                time.sleep(2)
                Method(driver).click('xpath', '//span[contains(text(),"信息发布")]')
                time.sleep(1)

                # 计算接口

                Method(driver).circle_click('信息发布 模糊查询（分页）')
                time.sleep(1)
                body = {
                    "filename": "",
                    "pageNo": "1",
                    "pageSize": "10"
                }

                # 获取计算接口的地址
                fileFuzzyQuery_interface_url = driver.find_element_by_xpath('//span[text()="接口地址"]/../code').text

                # 请求计算接口
                fileFuzzyQuery_send = requests.post(interface_url + fileFuzzyQuery_interface_url,
                                                     headers={
                                                         "Authorization": globals()["Authorization"][
                                                             "Authorization"],
                                                         "Content-Type": "application/json;charset=UTF-8"},
                                                     data=json.dumps(body))
                fileFuzzyQuery_response = json.loads(fileFuzzyQuery_send.text)
                url = interface_url + fileFuzzyQuery_interface_url
                params = json.dumps(body, ensure_ascii=False)

                if fileFuzzyQuery_send.status_code == 200:

                    if fileFuzzyQuery_response['success'] is True:

                        self.assertEqual(4, 4)
                    else:
                        if 'result' in fileFuzzyQuery_response.keys():
                            result = fileFuzzyQuery_response['result']
                            del fileFuzzyQuery_response['result']

                            write_sheet(path, '信息发布 模糊查询（分页）接口', url, params,
                                        json.dumps(fileFuzzyQuery_response, ensure_ascii=False), json.dumps(result))
                        else:
                            write_sheet(path, '信息发布 模糊查询（分页）接口', url, params,
                                        json.dumps(fileFuzzyQuery_response, ensure_ascii=False), '')

                        self.assertEqual(3, 4)
                else:
                    write_sheet(path, '信息发布 模糊查询（分页）接口', url, params,
                                '信息发布 模糊查询（分页）接口返回'.format(fileFuzzyQuery_response.status_code), '')
                    self.assertEqual(3, 4)

            except AssertionError:
                logger.error(AssertionError)
                self.assertEqual(3, 4)

    @ddt.file_data('{}/testInput/test_file_input/test_3_fileDownload.json'.format(path_dir))
    def test_3_fileDownload(self,filepath):
        """信息发布下载接口"""
        path = self.path
        if len(globals()["Authorization"]) == 0:
            write_sheet(path, '信息发布下载接口', '', '', '用户未登录', '')
            self.assertEqual(3, 4)
        else:
            try:
                driver = self.driver
                driver.refresh()
                time.sleep(2)
                Method(driver).click('xpath', '//span[contains(text(),"信息发布")]')
                time.sleep(1)

                # 计算接口

                Method(driver).circle_click('下载')
                time.sleep(1)
                body = {
                    "filepath": "{}".format(filepath)
                }

                # 获取计算接口的地址
                filedownload_interface_url = driver.find_element_by_xpath('//span[text()="接口地址"]/../code').text

                # 请求计算接口
                filedownload_send = requests.post(interface_url + filedownload_interface_url,
                                                    headers={
                                                        "Authorization": globals()["Authorization"][
                                                            "Authorization"],
                                                        "Content-Type": "application/json;charset=UTF-8"},
                                                    params=body)

                url = interface_url + filedownload_interface_url
                params = json.dumps(body, ensure_ascii=False)

                if filedownload_send.status_code == 200:

                    if filedownload_send.text != '':

                        self.assertEqual(4, 4)
                    else:

                        write_sheet(path, '信息发布下载接口', url, params,
                                    '', '')

                        self.assertEqual(3, 4)
                else:
                    write_sheet(path, '信息发布下载接口', url, params,
                                '信息发布下载接口返回'.format(filedownload_send.status_code), '')
                    self.assertEqual(3, 4)

            except AssertionError:
                logger.error(AssertionError)
                self.assertEqual(3, 4)

    @ddt.file_data('{}/testInput/test_file_input/test_4_fileSave.json'.format(path_dir))
    def test_4_fileSave(self,file):
        """信息发布保存文件接口"""
        path = self.path
        if len(globals()["Authorization"]) == 0:
            write_sheet(path, '信息发布 模糊查询（分页）接口', '', '', '用户未登录', '')
            self.assertEqual(3, 4)
        else:
            try:
                driver = self.driver
                driver.refresh()
                time.sleep(2)
                Method(driver).click('xpath', '//span[contains(text(),"信息发布")]')
                time.sleep(1)

                # 计算接口

                Method(driver).circle_click('保存文件')
                time.sleep(1)
                body = file

                # 获取计算接口的地址
                fileSave_interface_url = driver.find_element_by_xpath('//span[text()="接口地址"]/../code').text

                # 请求计算接口
                fileSave_send = requests.post(interface_url + fileSave_interface_url,
                                                    headers={
                                                        "Authorization": globals()["Authorization"][
                                                            "Authorization"],
                                                        "Content-Type": "application/json;charset=UTF-8"},
                                                    data=json.dumps(body))
                fileSave_response = json.loads(fileSave_send.text)
                url = interface_url + fileSave_interface_url
                params = json.dumps(body, ensure_ascii=False)

                if fileSave_send.status_code == 200:

                    if fileSave_response['success'] is True:

                        self.assertEqual(4, 4)
                    else:
                        if 'result' in fileSave_response.keys():
                            result = fileSave_response['result']
                            del fileSave_response['result']

                            write_sheet(path, '信息发布保存文件接口', url, params,
                                        json.dumps(fileSave_response, ensure_ascii=False), json.dumps(result))
                        else:
                            write_sheet(path, '信息发布保存文件接口', url, params,
                                        json.dumps(fileSave_response, ensure_ascii=False), '')

                        self.assertEqual(3, 4)
                else:
                    write_sheet(path, '信息发布保存文件接口', url, params,
                                '信息发布保存文件接口返回'.format(fileSave_response.status_code), '')
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
    st.addTest(unittest.makeSuite(test_file))
    # unittest.main()
    runner = HTMLTestRunner(stream=fp, verbosity=2, title='接口测试报告', description='测试结果如下: ')
    runner.run(st)  # 执行测试

    fp.close()  # 关闭文件流，将HTML内容写进测试报告文件
