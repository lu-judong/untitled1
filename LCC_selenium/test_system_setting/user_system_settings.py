from config.config import *
from config.menu_config import user_system_settings

def user_system_setting(url,username,password,contents):
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


        driver.find_elements_by_class_name('power-collapse-item')[-1].click()
        time.sleep(1)

        try:
            driver.find_elements_by_xpath('//span[text()=\'{}\']'.format(contents[0]))[1].click()
            log_file_out('点击' + contents[0] + '成功')
            time.sleep(1)
        except NoSuchElementException as e:
            log_file_out('点击' + contents[0] + '失败')
            logger.error(e)

        # 点击修改配置按钮
        Method(driver).click('class','power-btnOk')
        time.sleep(1)
        # 修改系统语言
        driver.find_elements_by_class_name('ivu-radio-input')[1].click()
        time.sleep(1)
        # 点击下载格式
        Method(driver).click('class', 'ivu-checkbox-input')

        time.sleep(1)
        # 日期格式
        driver.find_elements_by_class_name('ivu-radio-input')[3].click()
        time.sleep(1)

        # 进行首页配置的修改

        Method(driver).click('xpath','//span[text()="首页配置"]')
        time.sleep(1)
        try:
            # 修改菜单栏
            driver.find_elements_by_class_name('ivu-radio-input')[7].click()
            time.sleep(1)
            # 首页模块拖动修改
            driver.find_elements_by_class_name('ivu-radio-input')[9].click()
            time.sleep(1)

            log_file_out('首页配置配置成功')
        except Exception as e:
            logger.error(e)
            log_file_out('首页配置配置失败')

        # 建模配置
        Method(driver).click('xpath', '//span[text()="建模配置"]')
        time.sleep(1)
        try:
            # 修改菜单栏
            driver.find_elements_by_class_name('ivu-radio-input')[12].click()
            time.sleep(1)

            log_file_out('建模配置配置成功')
        except Exception as e:
            logger.error(e)
            log_file_out('建模配置配置失败')

        # 模型结果图配置
        Method(driver).click('xpath', '//span[text()="模型结果图配置"]')
        time.sleep(1)
        try:
            # 横轴跨度
            driver.find_elements_by_class_name('ivu-radio-input')[30].click()
            time.sleep(1)
            # 费用单位
            driver.find_elements_by_class_name('ivu-radio-input')[34].click()
            time.sleep(1)
            # 图表数据视图控件
            driver.find_elements_by_class_name('ivu-radio-input')[37].click()
            time.sleep(1)
            # 图表下载控件
            driver.find_elements_by_class_name('ivu-radio-input')[-3].click()
            time.sleep(1)

            log_file_out('模型结果图配置配置成功')
        except Exception as e:
            logger.error(e)
            log_file_out('模型结果图配置配置失败')
        # 点击修改配置按钮
        Method(driver).click('class', 'power-btnOk')
        # 退出修改
        driver.find_elements_by_class_name('power-btnOk')[2].click()


