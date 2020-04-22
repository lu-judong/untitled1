import time
from selenium.common.exceptions import NoSuchElementException
from config.log_config import logger
from selenium.webdriver.common.action_chains import ActionChains

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

    # 点击事件3
    def contains_click(self,value):
        self.driver.find_element_by_xpath('//*[text()=\'{}\']'.format(value)).click()

    # 获取文本值
    def gain_text(self,value):
        a = self.driver.find_element_by_xpath(value).get_attribute('value')
        return a


    # 选车
    def select_car(self,car):
        try:
            for x in car:
                self.click('xpath', '//span[contains(@class,"row-trainType-items") and text()=\'{}\']'.format(
                    x))
                car_num = car.get(x)
                time.sleep(1)
                if car_num == 'all':

                   self.click('id','trainTempBtn_checkAll')
                else:
                    for i in car_num:
                        self.click('xpath', '//span[contains(@class,"train-no-items") and text()=\'{}\']'.format(
                    i))
                self.click('id', 'trainTempBtn_submit')
                time.sleep(1)
            return True
        except NoSuchElementException as e:
            logger.debug('选车失败')
            logger.error(e)
            return False

    # 选构型
    def select_repairlocation(self,repairlocation):
        try:
            if type(repairlocation).__name__ == 'dict':
                for i in repairlocation:
                    self.click('xpath', '//span[text()=\'{}\']/../span'.format(i))
                    time.sleep(1)
                    self.select_repairlocation(repairlocation[i])
            else:
                for i in repairlocation:
                    self.click('xpath', '//span[text()=\'{}\']/../label'.format(i))
                    time.sleep(1)
            return True
        except NoSuchElementException as e:
            logger.error(e)
            return False
# 写入文件
def log_file_out(msg):
    fo = open(r'usecase.txt', mode='a', encoding='utf-8')
    fo.write(msg + '\r\n')
    fo.close()

# distance为传入的总距离,拖动的范围
def get_track(distance):
    # 移动轨迹
    track=[]
    # 当前位移
    current=0
    # 减速阈值
    mid=distance*4/5
    # 计算间隔
    t=0.2
    # 初速度
    v=1

    while current<distance:
        if current<mid:
            # 加速度为2
            a=4
        else:
            # 加速度为-2
            a=-3
        v0=v
        # 当前速度
        v=v0+a*t
        # 移动距离
        move=v0*t+1/2*a*t*t
        # 当前位移
        current+=move
        # 加入轨迹
        track.append(round(move))
    return track


# slider是要移动的滑块,tracks是要传入的移动轨迹
def move_to_gap(driver,slider,tracks):
    ActionChains(driver).click_and_hold(slider).perform()
    for x in tracks:
        ActionChains(driver).move_by_offset(xoffset=x,yoffset=0).perform()
    time.sleep(0.5)
    ActionChains(driver).release().perform()



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
    def click_different_more_btn(self,driver,btn_name):
        if btn_name[0] == 1:
            try:
                Method(driver).click('xpath', '//span[text()="切换首页"]/..')
                time.sleep(1)
                Method(driver).click('xpath', '//h4[text()=\'{}\']/..'.format(btn_name[1]))
                Method(driver).click('xpath', '//span[text()="确定"]')
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
    def check_model_condition(self, driver, model_m):
        try:
            model_conditon = driver.find_elements_by_class_name('power-preWrapper-title')[0].text
            if driver.find_elements_by_class_name('power-preCase-row')[1].text == '':
                log_file_out('更换模型中打开' + model_m + '预览出现的' + model_conditon + '为空,验证失败')
            else:
                log_file_out('更换模型中打开' + model_m + '预览出现的' + model_conditon + '不为空,验证成功')
        except:
            log_file_out('更换模型验证模型条件失败')
        time.sleep(2)
        try:
            for car_i in range(0,len(driver.find_elements_by_xpath('//p[@class="power-preTrain-typeCode"]/span/i'))):
                car_name = driver.find_elements_by_xpath('//p[@class="power-preTrain-typeCode"]')[car_i].text
                driver.find_elements_by_xpath('//p[@class="power-preTrain-typeCode"]/span/i')[car_i].click()
                time.sleep(1)
                # 车型车号
                car_text = driver.find_element_by_class_name('power-preTrain-trainNo-row').text
                if car_text != '':
                    log_file_out('打开' + model_m + '预览出现的\'{}\'车号不为空,验证成功'.format(car_name))

                else:
                    log_file_out('打开' + model_m + '预览出现的\'{}\'车号为空,验证失败'.format(car_name))
                driver.find_elements_by_xpath('//p[@class="power-preTrain-typeCode"]/span/i')[car_i].click()
                time.sleep(1)

        except:
            log_file_out('更换模型中打开' + model_m + '验证车号失败')


    # 获取功能菜单中的模型
    def achieve_model(self,driver,num,status):
        model_L = []
        try:
            if int(num[0]) == 0:
                pass
            elif int(num[0]) <= 10:
                for model_n in range(0, len(driver.find_elements_by_xpath('//td[2]'))):
                    if driver.find_elements_by_xpath('//td[2]')[model_n].text != '':
                        model_L.append(driver.find_elements_by_xpath('//td[2]')[model_n].text)

            else:
                for success_n in range(0, (int(num[0]) // 10) + 1):
                    driver.find_element_by_xpath('//a[text()="{}"]'.format(success_n + 1)).click()
                    time.sleep(1)
                    for model_n in range(0, len(driver.find_elements_by_xpath('//td[2]'))):
                        if driver.find_elements_by_xpath('//td[2]')[model_n].text != '':
                            model_L.append(driver.find_elements_by_xpath('//td[2]')[model_n].text)

            log_file_out('获取\'{}\'模型列表成功'.format(status))

        except:
            log_file_out('获取\'{}\'模型列表失败'.format(status))
        return model_L

    # 点击关闭
    def click_close_but(self, driver):
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



