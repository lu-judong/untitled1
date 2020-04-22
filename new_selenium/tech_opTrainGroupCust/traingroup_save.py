from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from config.log_config import logger
import time
from bin.main import Method
from bin.login import Login
from config.config import path_dir
from new_selenium.tech_opTrainGroupCust.traingroup_config import *


#自定义车组
class test_technology:
    def log_file_out(self,msg):
        fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()

    # 检查RAMS运营数据分析
    def tech(self,url,username,password,carname):

        driver = webdriver.Chrome()
        Login().login(url,username, password, driver)

        self.log_file_out('-----自定义车组-----')

        for i in contents:
            try:
                Method(driver).contains_xpath('click',i)
                time.sleep(1)
                self.log_file_out('点击'+i+'成功')
            except Exception as e:
                logger.debug(e)
                self.log_file_out('点击' + i + '失败')
        try:
            # 点击新建得到弹框
            Method(driver).switch_out()
            Method(driver).switch_iframe(
                driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/business/opTrainGroupCust')]"))
            Method(driver).click('id', 'add')
            time.sleep(2)
            self.log_file_out('新建成功')
        except:
            self.log_file_out('新建失败')

        # 切换到新的模型列表
        Method(driver).switch_out()
        a = Method(driver).get_attr('css', "[class='layui-layer layui-layer-iframe']", 'times')
        Method(driver).switch_iframe('layui-layer-iframe' + a)

        time.sleep(2)
        Method(driver).click('id', 'btnImport3')

        driver.execute_script('$(top.$(".layui-table-body .layui-unselect")[0]).trigger("click")')
        driver.execute_script('top.$(".layui-layer-btn0")[1].click()')
        time.sleep(2)

        Method(driver).input('id','train-group-name',carname)
        try:
            Method(driver).switch_out()
            # 点击保存按钮
            time.sleep(1)
            # Method(driver).click('xpath','//*[@id=\'%s\']/div[3]/a[1]' % e)
            Method(driver).click('class', 'layui-layer-btn0')
            self.log_file_out('点击保存按钮成功')
        except NoSuchElementException as e:
            logger.error('xpath' + '不存在!')
            self.log_file_out('点击保存按钮失败')
        except:
            self.log_file_out('请录入正确的车型')

        Method(driver).switch_out()
        Method(driver).switch_iframe(driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/business/opTrainGroupCust')]"))
        time.sleep(3)

        if driver.find_element_by_xpath("//td[contains(text(),\'{}\')]".format(carname)).text != '':
            self.log_file_out('自定义车组测试成功')
        else:
            self.log_file_out('自定义车组测试失败')

url = 'http://192.168.1.115:8080/darams/a/login'

car = {'E27':['2641', '2642', '2643', '2644', '2645', '2646', '2647']}

time_sleep = 2
wait_time = 10


test_technology().tech(url,'test','1234','0207')
