from config.config import *
from config.menu_config import internal_tech_settings

# 内部技术配置
def internal_technology_setting(url,username,password,contents):
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
        # 系统颜色
        try:
            driver.find_elements_by_class_name('ivu-radio-input')[1].click()
            time.sleep(1)
            log_file_out('修改系统颜色成功')
        except Exception as e:
            logger.error(e)
            log_file_out('修改系统颜色失败')

        # 菜单栏图标方案
        try:
            driver.find_elements_by_class_name('ivu-radio-input')[7].click()
            time.sleep(1)
            log_file_out('修改菜单栏图标方案成功')
        except Exception as e:
            logger.error(e)
            log_file_out('修改菜单栏图标方案失败')
        # 可修改字段名
        try:
            driver.find_element_by_class_name('ivu-input').send_keys(Keys.CONTROL, 'a')
            driver.find_element_by_class_name('ivu-input').send_keys(Keys.BACK_SPACE)

            driver.find_element_by_class_name('ivu-input').send_keys('1')
            log_file_out('修改字段名成功')
        except Exception as e:
            logger.error(e)
            log_file_out('修改字段名失败')





        # 退出修改
        driver.find_elements_by_class_name('power-btnOk')[2].click()


internal_technology_setting(url,username,password,internal_tech_settings)