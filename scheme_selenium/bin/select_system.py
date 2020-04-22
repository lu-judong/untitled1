import time
from selenium.common.exceptions import NoSuchElementException
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

def deal_car(driver,car):
    # 选车
    try:
        for x in car:
            driver.find_element_by_xpath(
                "//span[@class='train zoomIn' and contains(text(),\'{}\')]".format(x)).click()
            car_num = car.get(x)
            time.sleep(2)
            if car_num == 'all':
                driver.find_elements_by_xpath("//span[text()=\'{}\']".format('全选'))[1].click()
            else:
                for i in car_num:
                    driver.find_element_by_xpath(
                        "//span[@class='ivu-tag-text' and contains(text(),\'{}\')]".format(i)).click()
                    # time.sleep(2)
            driver.find_elements_by_xpath('//span[text()="确认"]')[2].click()
            time.sleep(2)
        return True
    except NoSuchElementException as e:
        logger.debug('选车失败')
        logger.error(e)
        return False

# 选交集部件
def deal_occur(driver,fault):
    try:
        for key in fault:
            if type(fault[key]).__name__ == 'dict':
                driver.find_element_by_xpath('//*[text()=\'{}\' and @class="el-tree-node__label"]/../span'.format(key)).click()
                time.sleep(2)
                deal_occur(driver,fault[key])
            else:
                driver.find_element_by_xpath('//*[text()=\'{}\']'.format(key)).click()
                time.sleep(1)
                driver.find_elements_by_xpath('//span[text()="故障对象ID"]/../../../th[1]/div/label')[1].click()
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
                driver.find_element_by_xpath('//*[text()=\'{}\' and @class="el-tree-node__label"]/../span '.format(key)).click()
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