from selenium.webdriver.support.ui import Select

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
            self.driver.find_element_by_xpath('//a[contains(text(),\'{}\')]'.format(value)).click()

    def contains_new(self,value):
        a = self.driver.find_element_by_xpath('//a[text()=\'{}\']'.format(value)).get_attribute('id')
        return a

    # 点击事件3
    def contains_click(self, value):
        self.driver.find_element_by_xpath('//*[text()=\'{}\']'.format(value)).click()

    # 通过文本值定位父节点 再找到子节点的按钮进行点击
    # def find_parent_click(self,value,value1):
    #     self.driver.find_element_by_xpath("//a[contains(text(),\'{}\')]/../..".format(value)).find_element_by_xpath("//a[contains(text(),\'{}\']".format(value1)).click()







