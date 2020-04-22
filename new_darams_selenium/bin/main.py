from selenium.webdriver.support.ui import Select
import time
from config.log_config import logger

# 封装selenium 的方法
class Method:
    # 打开浏览器
    def __init__(self,driver):
        self.driver = driver

    # 跳转页面
    def jumpwebpage(self,url):
        self.driver.get(url)

    # 验证元素是否存在
    def check_element(self, type, value):
        if type == "xpath":
            return self.driver.find_element_by_xpath(value)
        elif type == "id":
            return self.driver.find_element_by_id(value)
        elif type == "name":
            return self.driver.find_element_by_name(value)
        elif type == 'tag_name':
            return self.driver.find_element_by_tag_name(value)

    #输入内容
    def input(self,type,value,inputvalue):
        if type == "xpath":
            self.driver.find_element_by_xpath(value).send_keys(inputvalue)
        elif type == "id":
            self.driver.find_element_by_id(value).send_keys(inputvalue)
        elif type == "name":
            self.driver.find_element_by_name(value).send_keys(inputvalue)

    # 页面点击
    def click(self, type, value):
        if type == "xpath":
            self.driver.find_element_by_xpath(value).click()
        elif type == "id":
            self.driver.find_element_by_id(value).click()
        elif type == "name":
            self.driver.find_element_by_name(value).click()
        elif type == 'class':
            self.driver.find_element_by_class_name(value).click()

    # 鼠标事件方法第二
    def clear(self, type, value):
        if type == "xpath":
            self.driver.find_element_by_xpath(value).clear()
        elif type == "id":
            self.driver.find_element_by_id(value).clear()
        elif type == "name":
            self.driver.find_element_by_name(value).clear()
        elif type == "class":
            self.driver.find_element_by_class(value).clear()

    # 选择下拉框的值
    def select_down_list(self,type,value,inputvalue):
        if type== 'id':
            Select(self.driver.find_element_by_id(value)).select_by_index(inputvalue)
        elif type == 'xpath':
            Select(self.driver.find_element_by_xpath(value)).select_by_index(inputvalue)
        elif type == 'name':
            Select(self.driver.find_element_by_name(value)).select_by_index(inputvalue)

    # 获取元素的属性
    def get_attr(self,type,value,get_value):
        if type == 'css':
            value1 = self.driver.find_element_by_css_selector(value).get_attribute(get_value)
            return value1
        elif type == 'id':
            value1 = self.driver.find_element_by_id(value).get_attribute(get_value)
            return value1


    # 找到父元素 在进行点击
    def two_element_click(self,value,value1):
        self.driver.find_element_by_css_selector(
           value).find_element_by_class_name(value1).click()

    # 切到最外层iframe
    def switch_out(self):
        self.driver.switch_to.default_content()

    # 切入iframe
    def switch_iframe(self,value):
        self.driver.switch_to.frame(value)

    # 模糊匹配
    def contains_xpath(self,purpose,value):
        if purpose == "get":
            a = self.driver.find_element_by_xpath('//a[contains(text(),\'{}\')]'.format(value)).get_attribute('id')
            return a
        elif purpose == "click":
            self.driver.find_element_by_xpath('//span[contains(text(),\'{}\')]'.format(value)).click()

    def contains_new(self,value):
        a = self.driver.find_element_by_xpath('//a[text()=\'{}\']'.format(value)).get_attribute('id')
        return a

    # 点击事件3
    def contains_click(self, value):
        self.driver.find_element_by_xpath('//*[text()=\'{}\']'.format(value)).click()

    # 通过文本值定位父节点 再找到子节点的按钮进行点击
    # def find_parent_click(self,value,value1):
    #     self.driver.find_element_by_xpath("//a[contains(text(),\'{}\')]/../..".format(value)).find_element_by_xpath("//a[contains(text(),\'{}\']".format(value1)).click()



# 写入文件的方法
def log_file_out(msg):
    fo = open(r'usecase.txt', mode='a', encoding='utf-8')
    fo.write(msg + '\r\n')
    fo.close()


# 首页模型的一些公用方法
class check_home_page:
    # 点击多功能按钮
    def click_more_btn(self,driver):
        try:
            Method(driver).click('class', 'imgMore')
            log_file_out('点击多功能按钮成功')
        except:
            log_file_out('页面点击多功能按钮失败')

    # 点击多功能按钮中的按钮
    def click_different_more_btn(self,driver,btn_name,num):
        if btn_name[0] == 1:
            try:
                Method(driver).click('xpath', '//span[text()="切换首页"]/..')
                time.sleep(1)
                Method(driver).click('xpath', '//h4[text()=\'{}\']/..'.format(btn_name[1]))
                time.sleep(1)
                driver.find_elements_by_xpath('//span[text()="确定"]')[num].click()
                log_file_out('点击切换首页成功')
            except Exception as e:
                logger.error(e)
                log_file_out('点击切换首页失败')

        elif btn_name[0] == 2:
            try:
                Method(driver).click('xpath', '//span[text()="更换模型"]/..')
                log_file_out('点击更换模型按钮成功')
            except:
                log_file_out('点击更换模型按钮失败')
        elif btn_name[0] == 3:
            try:
                Method(driver).click('xpath', '//span[text()="重置模型条件"]/..')
                time.sleep(1)
                Method(driver).click('class', 'more-reset-bg')

                log_file_out('点击重置模型条件按钮成功')
            except:
                log_file_out('点击重置模型条件按钮失败')

    # 点击消息按钮
    def click_message(self,driver):
        try:
            Method(driver).click('class', 'el-icon-bell')
            log_file_out('点击消息按钮成功')
        except:
            log_file_out('点击消息按钮失败')

    # 首页模型条件中的预览
    def check_model_condition(self, driver, model_m, home_page, but_name):
        try:

            model_conditon = driver.find_elements_by_class_name('power-preWrapper-title')[0].text
            if driver.find_elements_by_class_name('power-preCase-row')[1].text != '':
                log_file_out(home_page + '打开' + model_m + '{}出现的'.format(but_name) + model_conditon + '不为空,验证成功')
            else:
                log_file_out(home_page + '打开' + model_m + '{}出现的'.format(but_name) + model_conditon + '为空,验证失败')

        except:
            log_file_out(model_m + '验证模型基础信息失败')
        time.sleep(2)

        # 车型车号
        try:
            for car_i in range(0,len(driver.find_elements_by_class_name('power-preTrain-trainNo-row'))):
                car_name = driver.find_elements_by_xpath('//p[@class="power-preTrain-typeCode"]')[car_i].text
                driver.find_elements_by_xpath('//p[@class="power-preTrain-typeCode"]/span/i')[car_i].click()
                time.sleep(1)
                car_text = driver.find_elements_by_class_name('power-preTrain-trainNo-row')[car_i].text
                if car_text != '':
                    log_file_out(home_page + '打开' + model_m + '{}出现的{}车号不为空,验证成功'.format(but_name,car_name))

                else:
                    log_file_out(home_page + '打开' + model_m + '{}出现的{}车号为空,验证失败'.format(but_name,car_name))
                driver.find_elements_by_xpath('//p[@class="power-preTrain-typeCode"]/span/i')[car_i].click()
                time.sleep(1)
        except:
            log_file_out(model_m + '验证模型车号信息失败')

        # 部件信息
        try:
            fault_text = driver.find_element_by_class_name('power-preFault-col').text
            if fault_text != '':
                log_file_out(home_page + '打开' + model_m + '预览出现的部件不为空,验证成功')
            else:
                log_file_out(home_page + '打开' + model_m + '预览出现的部件为空,验证失败')
        except:
            log_file_out('验证模型部件信息失败')




    # 获取功能菜单中的模型
    def achieve_model(self,driver,num,status):
        model_L = []
        try:
            if int(num[0]) == 0:
                log_file_out('保存模型验证失败')
            elif int(num[0]) <= 10:
                for model_n in range(0, len(driver.find_elements_by_xpath('//td[1]'))):
                    if driver.find_elements_by_xpath('//td[1]')[model_n].text != '':
                        model_L.append(driver.find_elements_by_xpath('//td[1]')[model_n].text)
            else:
                for success_n in range(0, (int(num[0]) // 10) + 1):
                    driver.find_element_by_xpath('//a[text()="{}"]'.format(success_n + 1)).click()
                    for model_n in range(0, len(driver.find_elements_by_xpath('//td[1]'))):
                        if driver.find_elements_by_xpath('//td[1]')[model_n].text != '':
                            model_L.append(driver.find_elements_by_xpath('//td[1]')[model_n].text)
            log_file_out('获取\'{}\'模型列表成功'.format(status))
        except:
            log_file_out('获取' + status + '模型列表失败')
        return model_L

    # 点击关闭
    def click_close_but(self,driver):
        try:
            for close_num in range(0, len(driver.find_elements_by_xpath('//span[text()="关闭"]'))):
                try:
                    driver.find_elements_by_xpath('//span[text()="关闭"]')[close_num].click()
                    break
                except:
                    pass
            log_file_out('点击模型条件窗口关闭按钮成功')
        except Exception as e:
            logger.error(e)
            log_file_out('点击模型条件窗口关闭按钮失败')