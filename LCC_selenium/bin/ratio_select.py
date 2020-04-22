from config.config import *
import re

# 所有对占比功能的高级检索
def all_select_check(url,username,password,contents,modelCode,modelName,cal_status):
    driver = webdriver.Chrome()
    status = Login().login(url, username, password, driver)
    time.sleep(2)
    driver.maximize_window()
    Method(driver).click('id', 'ballb')
    if contents[0] == '运营费用统计' or contents[0] == '运维费用统计' or contents[0] == '通用模型':
        log_file_out('---------' + '{}'.format(contents[0]) + '高级搜索框验证---------')
    else:
        log_file_out('---------' + '{}'.format(contents[0]) + '占比分析高级搜索框验证---------')
    # driver.execute_script("document.body.style.zoom='0.8'")
    if status is True:
        log_file_out('登陆成功')
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[0])

        # try:
        #     #点击整体维修费用分析
        #     Method(driver).contains_click(contents1)
        #     self.log_file_out('点击' + contents1 + '成功')
        # except NoSuchElementException as e:
        #     self.log_file_out('点击' + contents1 + '失败')
        #     logger.error(e)
        if contents[0] == '运营费用统计' or contents[0] == '运维费用统计':
            driver.find_elements_by_class_name('power-collapse-item')[0].click()
            time.sleep(1)

            try:
                driver.find_elements_by_xpath('//span[text()=\'{}\']'.format(contents[0]))[1].click()
                log_file_out('点击' + contents[0] + '成功')
                time.sleep(1)
            except NoSuchElementException as e:
                log_file_out('点击' + contents[0] + '失败')
                logger.error(e)

            time.sleep(2)
        else:
            driver.find_elements_by_class_name('power-collapse-item')[1].click()
            time.sleep(1)

            try:
                driver.find_elements_by_xpath('//span[text()=\'{}\']'.format(contents[0]))[1].click()
                log_file_out('点击' + contents[0] + '成功')
                time.sleep(1)
            except NoSuchElementException as e:
                log_file_out('点击' + contents[0] + '失败')
                logger.error(e)
            time.sleep(1)
            if contents[1] == '占比分析':
                driver.find_elements_by_xpath('//span[text()=\'{}\']/../../ul/li[2]'.format(contents[0]))[1].click()
            else:
                driver.find_elements_by_xpath('//span[text()=\'{}\']/../../ul/li[1]'.format(contents[0]))[1].click()

        time.sleep(2)

        Method(driver).click('class','icon-btn-more')
        # 输入模型编码
        Method(driver).input('xpath', "//input[@placeholder='请输入模型编码']", modelCode)
        # 点击查询按钮
        driver.find_elements_by_class_name('power-btnOk')[0].click()

        su = driver.find_element_by_class_name('ivu-page-total').text

        su1 = re.findall(r'\d+', su)
        try:
            if int(su1[0]) == 1:
                log_file_out('模型编码输入框高级搜索支持模糊搜索,验证成功')
            else:
                log_file_out('模型编码输入框高级搜索不支持模糊搜索,验证失败')
        except Exception as e:
            logger.error(e)
            log_file_out('模型名称输入框高级搜索验证失败')
        # 点击重置按钮
        time.sleep(1)
        driver.find_elements_by_class_name('power-btnOk')[1].click()
        time.sleep(1)
        # 验证模型编码输入框
        Method(driver).input('xpath', "//input[@placeholder='请输入模型名称']", modelName)
        time.sleep(1)
        # 点击查询按钮
        driver.find_elements_by_class_name('power-btnOk')[0].click()
        try:
            if int(su1[0]) == 1:
                log_file_out('模型名称输入框高级搜索支持模糊搜索,验证成功')
            else:
                log_file_out('模型名称输入框高级搜索不支持模糊搜索,验证失败')
        except Exception as e:
            logger.error(e)
            log_file_out('模型名称输入框高级搜索验证失败')
        # 点击重置按钮
        time.sleep(1)
        driver.find_elements_by_class_name('power-btnOk')[1].click()
        time.sleep(1)
        # 计算状态选择框
        Method(driver).click('class','ivu-select-placeholder')


        time.sleep(1)
        if cal_status == 1:
            Method(driver).click('xpath', '//li[text()="未计算"]')
        elif cal_status == 2:
            Method(driver).click('xpath', '//li[text()="计算中"]')
        elif cal_status == 3:
            Method(driver).click('xpath', '//li[text()="计算异常"]')
        else:
            Method(driver).click('xpath', '//li[text()="计算完成"]')
        # 点击查询按钮
        driver.find_elements_by_class_name('power-btnOk')[0].click()
        time.sleep(1)
        # 查询的数量
        nu2 = driver.find_elements_by_class_name('ivu-page-total')[0].text
        nu3 = re.findall(r'\d+', nu2)

        if int(nu3[0]) == 0:
            log_file_out('验证成功')
        elif int(nu3[0]) <= 10:
            if cal_status == 1:
                if len(driver.find_elements_by_xpath('//span[text()="计算中"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//span[text()="计算异常"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//span[text()="计算完成"]')) != 0:
                    log_file_out('计算状态选择框验证失败')
                else:
                    log_file_out('计算状态选择框验证成功')
            elif cal_status == 2:
                if len(driver.find_elements_by_xpath('//span[text()="未计算"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//span[text()="计算异常"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//span[text()="计算完成"]')) != 0:
                    log_file_out('计算状态选择框验证失败')
                else:
                    log_file_out('计算状态选择框验证成功')
            elif cal_status == 3:
                if len(driver.find_elements_by_xpath('//span[text()="未计算"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//span[text()="计算中"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//span[text()="计算完成"]')) != 0:
                    log_file_out('计算状态选择框验证失败')
                else:
                    log_file_out('计算状态选择框验证成功')
            else:
                if len(driver.find_elements_by_xpath('//span[text()="计算中"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//span[text()="计算异常"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//span[text()="未计算"]')) != 0:
                    log_file_out('计算状态选择框验证失败')
                else:
                    log_file_out('计算状态选择框验证成功')
        else:
            for i in range(0, (int(nu3[0]) // 10) + 1):
                driver.find_element_by_xpath('//a[text()="{}"]'.format(i + 1)).click()
                if cal_status == 1:
                    if len(driver.find_elements_by_xpath('//span[text()="计算中"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//span[text()="计算异常"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//span[text()="计算完成"]')) != 0:
                        log_file_out('第' + str(i) + '页' + '计算状态选择框验证失败')
                    else:
                        log_file_out('第' + str(i) + '页' + '计算状态选择框验证成功')
                elif cal_status == 2:
                    if len(driver.find_elements_by_xpath('//span[text()="未计算"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//span[text()="计算异常"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//span[text()="计算完成"]')) != 0:
                        log_file_out('第' + str(i) + '页' + '计算状态选择框验证失败')
                    else:
                        log_file_out('第' + str(i) + '页' + '计算状态选择框验证成功')
                elif cal_status == 3:
                    if len(driver.find_elements_by_xpath('//span[text()="未计算"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//span[text()="计算中"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//span[text()="计算完成"]')) != 0:
                        log_file_out('第' + str(i + 1) + '页' + '计算状态选择框验证失败')
                    else:
                        log_file_out('第' + str(i + 1) + '页' + '计算状态选择框验证成功')
                else:
                    if len(driver.find_elements_by_xpath('//span[text()="计算中"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//span[text()="计算异常"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//span[text()="未计算"]')) != 0:
                        log_file_out('第' + str(i + 1) + '页' + '计算状态选择框验证失败')
                    else:
                        log_file_out('第' + str(i + 1) + '页' + '计算状态选择框验证成功')
        time.sleep(1)
        # 默认模型选择框
        if contents[0] == '通用模型':
            # 点击重置按钮
            time.sleep(1)
            driver.find_elements_by_class_name('power-btnOk')[1].click()
            time.sleep(1)
            try:
                # 默认模型下拉框
                driver.find_elements_by_class_name('ivu-select-placeholder')[1].click()
                time.sleep(1)
                Method(driver).click('xpath', '//li[text()="是"]')
                time.sleep(1)
                # 点击查询按钮
                driver.find_element_by_class_name('power-btnOk').click()
                time.sleep(1)
                total_sum = driver.find_element_by_class_name('ivu-page-total').text
                total_sum1 = re.findall(r'\d+', total_sum)
                if int(total_sum1[0]) == 1:
                    log_file_out('默认模型选择框验证成功')
                else:
                    log_file_out('默认模型选择框验证失败')
            except Exception as e:
                logger.error(e)
                log_file_out('默认模型选择框验证失败')
        else:
            pass
        driver.close()