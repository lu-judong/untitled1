from selenium import webdriver
from interfaceTest.config.main import *
import requests
import json
import ddt
from interfaceTest.libext.HTMLTestRunner import *
from interfaceTest.config.config import *

@ddt.ddt
class test_customizeCar(unittest.TestCase):

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

    @ddt.file_data('{}/testInput/test_customizeCar_input/test_2_customizeSave.json'.format(path_dir))
    def test_2_customizeSave(self,save):
        """自定义选车保存接口"""
        path = self.path
        if len(globals()["Authorization"]) == 0:
                write_sheet(path, '自定义选车保存接口', '','','用户未登录','')
                self.assertEqual(3, 4)
        else:
            try:
                driver = self.driver
                driver.refresh()

                time.sleep(2)
                # 点击搜索

                Method(driver).click('xpath', '//span[contains(text(),"自定义选车")]')
                time.sleep(1)
                Method(driver).circle_click('自定义选车 - 保存（修改/更新）')
                # 获取保存接口的地址
                save_interface_url = driver.find_element_by_xpath('//span[text()="接口地址"]/../code').text

                data = save

                # 请求保存接口
                save_send = requests.post(interface_url + save_interface_url, headers={
                            "Authorization": globals()["Authorization"]["Authorization"],
                            "Content-Type": "application/json;charset=UTF-8"},
                              data=json.dumps(data))
                save_response = json.loads(save_send.text)
                url = interface_url + save_interface_url
                params =  json.dumps(save, ensure_ascii=False)
                if save_send.status_code == 200:
                    if save_response['success'] is True:

                        self.assertEqual(4, 4)
                    else:
                        if save_response['message'] == '该车组名称或编码已经存在':
                            self.assertEqual(4, 4)
                        else:

                            if 'result' in save_response.keys():
                                result = save_response['result']
                                del save_response['result']

                                write_sheet(path, '自定义选车保存接口', url, params, json.dumps(save_response, ensure_ascii=False), json.dumps(result))
                            else:
                                write_sheet(path, '自定义选车保存接口', url, params, json.dumps(save_response, ensure_ascii=False),'')

                            self.assertEqual(3, 4)
                else:
                    write_sheet(path, '自定义车组保存接口', url, params, '自定义车组保存接口返回'.format(save_response.status_code),'')

                    self.assertEqual(3, 4)
            except AssertionError:
                logger.error(AssertionError)
                self.assertEqual(3, 4)

    def test_3_customizeList(self):
        """自定义选车列表接口"""
        path = self.path
        if len(globals()["Authorization"]) == 0:
            write_sheet(path, '自定义选车 - 列表查询(模糊查询)', '', '', '用户未登录', '')
            self.assertEqual(3, 4)
        else:
            try:
                driver = self.driver
                driver.refresh()
                time.sleep(2)
                Method(driver).click('xpath', '//span[contains(text(),"自定义选车")]')
                time.sleep(1)
                Method(driver).circle_click('自定义选车 - 列表查询(模糊查询)')

                # 获取列表查询接口的地址
                list_interface_url = driver.find_element_by_xpath('//span[text()="接口地址"]/../code').text

                data = {"pageNo": 1, "pageSize": 10, "adaptation": ""}

                # 请求列表接口
                list_send = requests.post(interface_url + list_interface_url,  headers={
                            "Authorization": globals()["Authorization"]["Authorization"],
                            "Content-Type": "application/json;charset=UTF-8"},
                                          data=json.dumps(data))
                list_response = json.loads(list_send.text)
                url = interface_url + list_interface_url
                if list_send.status_code == 200:
                    # 得到登录接口的返回
                    if list_response['success'] is True:
                        self.assertEqual(4, 4)
                    else:

                        if 'result' in list_response.keys():
                            result = list_response['result']
                            del list_response['result']

                            write_sheet(path, '自定义选车-列表查询接口', url, data, json.dumps(list_response, ensure_ascii=False),
                                        json.dumps(result, ensure_ascii=False))
                        else:
                            write_sheet(path, '自定义选车-列表查询接口', url, data, json.dumps(list_response, ensure_ascii=False), '')
                        self.assertEqual(3, 4)
                else:
                    write_sheet(path, '自定义选车-列表查询接口', url, data, '自定义选车-列表查询接口返回:{}'.format(list_response.status_code), '')

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
    st.addTest(unittest.makeSuite(test_customizeCar))
    # unittest.main()
    runner = HTMLTestRunner(stream=fp, verbosity=2, title='接口测试报告', description='测试结果如下: ')
    runner.run(st)  # 执行测试

    fp.close()  # 关闭文件流，将HTML内容写进测试报告文件




