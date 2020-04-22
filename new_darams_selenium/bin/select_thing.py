import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from config.log_config import logger



def deal_system(driver,system):
    try:
        for key in system:
            if type(system[key]).__name__ == 'dict':
                driver.find_elements_by_xpath('//span[text()=\'{}\']/../label/../span'.format(key))[0].click()
                deal_system(driver,system[key])
            else:
                driver.find_element_by_xpath('//span[text()=\'{}\']/../label/span'.format(key)).click()
        return True
    except Exception as e:
        logger.error(e)
        return False

# 选车 num 代表 车号页面全选按钮为第几个全选  num1代表车号页面的确定按钮为第几个确定
def deal_car(driver,car,num,num1):
    try:
        for x in car:
            driver.find_element_by_xpath(
                "//span[@class='train zoomIn' and contains(text(),\'{}\')]".format(x)).click()
            car_num = car.get(x)
            time.sleep(2)
            if car_num == 'all':
                driver.find_elements_by_xpath("//span[text()=\'{}\']".format('全选'))[num].click()
            else:
                for i in car_num:
                    driver.find_element_by_xpath(
                        "//span[@class='ivu-tag-text' and contains(text(),\'{}\')]".format(i)).click()
                    # time.sleep(2)
            driver.find_elements_by_xpath('//span[text()="确定"]')[num1].click()
            time.sleep(2)
        return True
    except NoSuchElementException as e:
        logger.debug('选车失败')
        logger.error(e)
        return False

# 选交集部件
def deal_occur(driver,fault,value):
    try:
        for key in fault:
            if type(fault[key]).__name__ == 'dict':
                driver.find_element_by_xpath('//*[text()=\'{}\' and @class="el-tree-node__label"]/../span'.format(key)).click()
                time.sleep(2)
                deal_occur(driver,fault[key],value)
            else:
                driver.find_element_by_xpath('//*[text()=\'{}\']'.format(key)).click()
                time.sleep(1)
                # 1代表选择部件 2代表选择故障模式
                if value == 1:
                    driver.find_elements_by_xpath('//span[text()="故障对象ID"]/../../../th[1]/div/label')[1].click()
                else:
                    driver.find_elements_by_xpath('//span[text()="故障模式"]/../../../th[1]/div/label')[1].click()
                time.sleep(2)
                driver.find_elements_by_class_name('ivu-btn-icon-only')[0].click()
        return True
    except Exception as e:
        logger.error(e)
        return False

# 选并集部件
def deal_union(driver,fault):
    try:
        for key in fault:
            if type(fault[key]).__name__ == 'dict':
                driver.find_element_by_xpath('//*[contains(text(),\'{}\') and @class="el-tree-node__label"]/../span'.format(key)).click()
                time.sleep(1)
                deal_union(driver,fault[key])
            else:
                time.sleep(0.5)
                driver.find_element_by_xpath('//*[text()=\'{}\' and @class="el-tree-node__label"]/../label/span'.format(key)).click()
                time.sleep(1)
                driver.find_element_by_xpath('//*[text()=\'{}\']'.format('增加')).click()
                time.sleep(2)
        return True
    except Exception as e:
        logger.error(e)
        return False

# 多模型选交集部件
def deal_occur1(driver,fault,value):
    try:
        for key in fault:
            if type(fault[key]).__name__ == 'dict':
                driver.find_element_by_xpath('//*[text()=\'{}\' and @class="el-tree-node__label"]/../span'.format(key)).click()
                time.sleep(2)
                deal_occur1(driver,fault[key],value)
            else:
                driver.find_element_by_xpath('//*[text()=\'{}\']'.format(key)).click()
                time.sleep(1)
                if value == 1:
                    driver.find_elements_by_xpath('//span[text()="故障对象ID"]/../../../th[1]/div/label')[1].click()
                else:
                    driver.find_elements_by_xpath('//span[text()="故障模式"]/../../../th[1]/div/label')[1].click()
                time.sleep(2)
                driver.find_elements_by_class_name('ivu-btn-icon-only')[2].click()
        return True
    except Exception as e:
        logger.error(e)
        return False

# 检查部件搜索框
def check_fault_select(driver,fault):
    L = []
    status = True
    try:
        if len(driver.find_elements_by_class_name('el-tree-node__label')) > 10:
            status = False
        else:
            for i in driver.find_elements_by_class_name('el-tree-node__label'):
                L.append(i.text)
            L.remove('全部')
            if fault in L:
                status = True
            else:
                if len(driver.find_elements_by_class_name('el-tree-node__expand-icon')) > 1:
                    driver.find_element_by_xpath( '//*[contains(text(),\'{}\') and @class="el-tree-node__label"]/../span'.format(L[-1])).click()
                    time.sleep(1)
                    check_fault_select(driver, fault)
                else:
                    status = False
        # print(status)
        return status
    except Exception as e:
        logger.error(e)
        return False

# 列车故障信息选择部件/模式
def deal_train_occur(driver,fault,value):
    try:
        for key in fault:
            if type(fault[key]).__name__ == 'dict':
                driver.find_element_by_xpath('//*[text()=\'{}\' and @class="el-tree-node__label"]/../span'.format(key)).click()
                time.sleep(2)
                deal_train_occur(driver,fault[key],value)
            else:
                driver.find_element_by_xpath('//*[text()=\'{}\']'.format(key)).click()
                time.sleep(2)
                # 1代表选择部件 2代表选择故障模式
                if value == 1:
                    driver.find_elements_by_xpath('//span[text()="系统/部件"]/../../../th[1]/div/label')[1].click()
                else:
                    driver.find_elements_by_xpath('//span[text()="故障模式"]/../../../th[1]/div/label')[1].click()
                time.sleep(2)
                driver.find_elements_by_class_name('ivu-btn-icon-only')[0].click()
        return True
    except Exception as e:
        logger.error(e)
        return False

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