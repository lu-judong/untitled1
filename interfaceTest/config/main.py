from selenium.webdriver.support.ui import Select
import time
from .log_config import logger
from.config import path_dir
import xlwt # 写excel
import xlrd # 读excel
from xlutils.copy import copy
import os

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

    # 循环点击页面上的文字 直到点到为止 避免每次都得去重新找元素所在的位置
    def circle_click(self,text):
        try:
            for i in range(0,len(self.driver.find_elements_by_xpath('//span[text()=\'{}\']'.format(text)))):
                try:
                    self.driver.find_elements_by_xpath('//span[text()=\'{}\']'.format(text))[i].click()
                    break
                except:
                    pass
        except Exception as e:
            logger.error(e)





# 创建excel
def create_sheet(path):
    if os.path.exists(path):
        os.remove(path)
    else:
        pass

    # 创建一个文件对象
    wb = xlwt.Workbook(encoding='utf-8')
    # 创建一个sheet对象
    sheet = wb.add_sheet('interface-sheet')
    # 设置文件头的样式,这个不是必须的可以根据自己的需求进行更改
    style_heading = xlwt.easyxf("""
                                      font:
                                          name Arial,
                                          colour_index white,
                                          bold on,
                                          height 0xA0;
                                      align:
                                          wrap off,
                                          vert center,
                                          horiz center;
                                      pattern:
                                          pattern solid,
                                          fore-colour 0x19;
                                      borders:
                                          left THIN,
                                          right THIN,
                                          top THIN,
                                          bottom THIN;  
                                        
                                      """)

    # 写入文件标题
    sheet.write(0, 0, '接口名称', style_heading)
    sheet.write(0, 1, '请求地址', style_heading)
    sheet.write(0, 2, '请求参数', style_heading)
    sheet.write(0, 3, '错误信息', style_heading)
    sheet.write(0, 4, '错误信息', style_heading)
    sheet.col(0).width = 20000
    sheet.col(1).width = 20000
    sheet.col(2).width = 20000
    sheet.col(3).width = 20000
    sheet.col(4).width = 20000
    wb.save('{}/testOutput/interface-sheet.xls'.format(path_dir))

# 写入excel
def write_sheet(path,interfaceName,url,params,message,message1):

    workbook = xlrd.open_workbook(path,formatting_info=True)
    # 获取工作簿中的所有表格
    sheets = workbook.sheet_names()
    # 获取工作簿中所有表格中的的第一个表格
    worksheet = workbook.sheet_by_name(sheets[0])
    # 获取表格中已存在的数据的行数
    # excel的下标从0开始
    rows_old = worksheet.nrows
    # 将xlrd对象拷贝转化为xlwt对象
    new_workbook = copy(workbook)

    # 获取转化后工作簿中的第一个表格
    new_worksheet = new_workbook.get_sheet(0)
    # excel的行数+1 下标为2对于excel为第三行 所以会出现换行的状态
    new_worksheet.write(1 + rows_old, 0, interfaceName)

    new_worksheet.write(1 + rows_old, 1, url)
    new_worksheet.write(1 + rows_old, 2, params)
    new_worksheet.write(1 + rows_old, 3, message)
    new_worksheet.write(1 + rows_old, 4, message1)
    # 保存工作薄
    new_workbook.save(path)