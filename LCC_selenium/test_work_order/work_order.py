import re

from config.config import *
from config.menu_config import work_order

def work_order_test(url,username,password,contents,car):
    driver = webdriver.Chrome()
    status = Login().login(url, username, password, driver)
    time.sleep(2)
    driver.maximize_window()
    Method(driver).click('id', 'ballb')

    log_file_out('---------' + '{}'.format(contents[0]) + '验证---------')

    if status is True:
        log_file_out('登陆成功')
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[0])


        driver.find_elements_by_class_name('power-collapse-item')[4].click()
        time.sleep(1)

        try:
            driver.find_elements_by_xpath('//span[text()=\'{}\']'.format(contents[0]))[1].click()
            log_file_out('点击' + contents[0] + '成功')
            time.sleep(1)
        except NoSuchElementException as e:
            log_file_out('点击' + contents[0] + '失败')
            logger.error(e)


        time.sleep(2)
        # 查询之前的数量
        nu = driver.find_elements_by_class_name('ivu-page-total')[0].text
        nu1 = re.findall(r'\d+', nu)

        Method(driver).click('class', 'icon-btn-more')
        # 列表选项选择框
        Method(driver).click('class', 'ivu-select-placeholder')
        time.sleep(1)
        # 选择车型车号
        Method(driver).click('xpath', '//li[text()="车型/车号"]')
        time.sleep(2)
        # 点击车型/车号搜索按钮
        Method(driver).click('class', 'ivu-icon-ios-search')

        try:
            for x in car:
                Method(driver).click('xpath', '//span[contains(@class,"train zoomIn") and text()=\'{}\']'.format(
                    x))
                car_num = car.get(x)
                time.sleep(1)

                Method(driver).click('xpath', '//span[contains(@class,"trainNo-tag") and text()=\'{}\']'.format(
                    car_num))
                driver.find_elements_by_class_name('power-btnOk')[-3].click()
                time.sleep(1)
            # 点击选车界面的确定按钮
            driver.find_elements_by_class_name('power-btnOk')[-8].click()
            log_file_out('选车成功')
        except Exception as e:
            logger.error(e)
            log_file_out('选车失败')
            return
        time.sleep(2)
        # 点击查询按钮
        try:
            Method(driver).click('class','icon-btn-search')
            log_file_out('点击查询按钮成功')
        except Exception as e:
            log_file_out('点击查询按钮失败')
        time.sleep(5)
        # 查询之后的数量
        nu2 = driver.find_elements_by_class_name('ivu-page-total')[0].text
        nu3 = re.findall(r'\d+', nu2)
        try:
            if int(nu1[0]) != int(nu3[0]):
                log_file_out('工单功能验证成功')
            else:
                log_file_out('工单功能验证失败')
        except Exception as e:
            logger.error(e)
            log_file_out('工单功能验证失败')

work_order_test(url,username,password,work_order,{'E27':['2651']})
