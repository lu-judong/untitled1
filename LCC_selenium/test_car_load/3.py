from LCC_selenium.bin.login import Login
from LCC_selenium.bin.main import Method
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from config.log_config import logger
import time
from LCC_selenium.test_car_load.test3_fangfa1 import ProporAnalyClass
from LCC_selenium.test_car_load.test3_fangfa2 import ProporClass
from LCC_selenium.test_car_load.ratio_config import *


class t:
    def log_file_out(self, msg):
        fo = open(r'.\usecase.txt', mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    def tt(self,url,car):
        option = webdriver.ChromeOptions()
        option.add_argument("headless")
        driver = webdriver.Chrome(chrome_options=option
                                  ,
                                  executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe'
                                  )
        driver = webdriver.Chrome()
        status = Login().login(url, 'test3', '1234', driver)
        if status is True:
            time.sleep(3)
            driver.switch_to.window(driver.window_handles[0])
            self.log_file_out('---------费用占比分析---------')
            # try:
            #     #点击整体维修费用分析
            #     Method(driver).contains_click(contents1)
            #     self.log_file_out('点击' + contents1 + '成功')
            # except NoSuchElementException as e:
            #     self.log_file_out('点击' + contents1 + '失败')
            #     logger.error(e)

            for i in contents:
                try:
                    # 点击整体维修费用分析
                    Method(driver).contains_click(i)
                    self.log_file_out('点击' + i + '成功')
                    time.sleep(2)
                except NoSuchElementException as e:
                    self.log_file_out('点击' + i + '失败')
                    logger.error(e)

        time.sleep(2)
        driver.find_element_by_xpath(
            "//span[contains(text(),\'{}\')]/../../../td[1]/div/div/button[3]".format('yx')).click()

        time.sleep(2)

        a_6 = driver.find_element_by_id('chart_repairMethod_sun_P').get_attribute('textContent')
        a_7 = driver.find_element_by_id('chart_accessName_sun_P').get_attribute('textContent')
        print(a_6)
        print(a_7)


        a = ProporAnalyClass().main(car, ['2017-02-01', '2018-02-01'])
        print(a)

        c_6 = eval(a_6)
        for m_1 in c_6:
            if m_1.get('value') is None:
                if a[5].get(m_1.get('name')) == 0:
                    self.log_file_out(m_1.get('name') + '费用一致')
                else:
                    self.log_file_out(m_1.get('name') + '费用不一致')
            else:
                if a[5].get(m_1.get('name')) == m_1.get('value'):
                    self.log_file_out(m_1.get('name') + '费用一致')
                else:
                    self.log_file_out(m_1.get('name') + '费用不一致')

        d_5 = eval(a_6)[0].get('children')
        for m_2 in d_5:
            if m_2.get('value') is None:
                if a[5].get('偶检' + m_2.get('name')) == 0:
                    self.log_file_out('偶检' + m_2.get('name') + '费用一致')
                else:
                    self.log_file_out('偶检' + m_2.get('name') + '费用不一致')
            else:
                if a[5].get('偶检' + m_2.get('name')) == float(m_2.get("value")):
                    self.log_file_out('偶检' + m_2.get('name') + '费用一致')
                else:
                    self.log_file_out('偶检' + m_2.get('name') + '费用不一致')

        d_6 = eval(a_6)[1].get('children')
        for m_3 in d_6:
            if m_3.get('value') is None:
                if a[5].get('定检' + m_3.get('name')) == 0:
                    self.log_file_out('定检' + m_3.get('name') + '费用一致')
                else:
                    self.log_file_out('定检' + m_3.get('name') + '费用不一致')
            else:
                if a[5].get('定检' + m_3.get('name')) == float(m_3.get("value")):
                    self.log_file_out('定检' + m_3.get('name') + '费用一致')
                else:
                    self.log_file_out('定检' + m_3.get('name') + '费用不一致')

        c_7 = eval(a_7)
        for n_1 in c_7:
            if n_1.get('value') is None:
                if a[6].get(n_1.get('name')[:1]) == 0:
                    self.log_file_out(n_1.get('name') + '费用一致')
                else:
                    self.log_file_out(n_1.get('name') + '费用不一致')
            else:
                if a[6].get(n_1.get('name')[:1]) == n_1.get('value'):
                    self.log_file_out(n_1.get('name') + '费用一致')
                else:
                    self.log_file_out(n_1.get('name') + '费用不一致')
            for n_2 in range(0, len(eval(a_7))):
                for n_3 in eval(a_7)[n_2].get('children'):
                    if n_3.get('value') is None:
                        if a[6].get(n_1.get('name') + n_3.get('name')) == 0:
                            self.log_file_out(n_1.get('name') + n_3.get('name') + '费用一致')
                        else:
                            self.log_file_out(n_1.get('name') + n_3.get('name') + '费用不一致')
                    else:
                        if a[6].get(n_1.get('name') + n_3.get('name')) == float(n_3.get("value")):
                            self.log_file_out(n_1.get('name') + n_3.get('name') + '费用一致')
                        else:
                            self.log_file_out(n_1.get('name') + n_3.get('name') + '费用不一致')



car = {'E27':['2651']
       }

url = 'http://192.168.1.25'
t().tt(url,car)