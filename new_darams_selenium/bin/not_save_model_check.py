from random import randint

from config.config import *

# 修程修制不保存计算以及图表
def repair_notsave_model_check(url,username,password,contents,value,repair_mileage,car,fault,select_fault,check_fault,wait_time):

    # option = webdriver.ChromeOptions()
    # option.add_argument("headless")
    # driver = webdriver.Chrome(chrome_options=option
    # ,executable_path=r'../apps/chromedriver.exe'
    #  )
    # driver.maximize_window()


    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    log_file_out('-----' + contents[1] + '不保存验证' + '-----')
    status = new_built(driver, url, username, password, contents,3)
    if status is True:
        log_file_out('登录成功')
        time.sleep(2)

        # 录入模型信息
        try:
            Method(driver).click('xpath', '//span[text()="请输入评估对象"]')
            time.sleep(1)
            if value == 1:
                driver.find_elements_by_xpath('//li[text()="评估系统、部件"]')[1].click()
            elif value == 2:
                driver.find_elements_by_xpath('//li[text()="故障模式"]')[1].click()
            logger.debug('录入模型基本信息成功')

        except NoSuchElementException as e:
            logger.debug('录入模型基本信息失败')
            logger.error(e)


        # 优化前里程
        try:
            driver.find_elements_by_class_name('ivu-input-default')[4].send_keys(repair_mileage[0])
            time.sleep(0.5)
            driver.find_elements_by_class_name('ivu-input-default')[5].send_keys(repair_mileage[1])
            time.sleep(0.5)

        except NoSuchElementException as e:
            logger.error('xpath' + '不存在！')
            log_file_out('优化前里程录入失败')
        except:
            log_file_out('优化前里程录入失败')

        # 优化后里程
        try:
            Method(driver).click('xpath','//a[text()="优化后里程"]')
            time.sleep(1)
            driver.find_elements_by_class_name('ivu-input-default')[7].send_keys(repair_mileage[2])

            log_file_out('优化后里程输入成功')
        except NoSuchElementException as e:
            logger.error('xpath' + '不存在！')
            log_file_out('优化后里程输入失败')
        except:
            log_file_out('优化前里程录入失败')

        # 车型 车号新增页面
        if select_fault == '交集':
            driver.find_element_by_xpath('//*[contains(text(),\'{}\')]'.format('是否根据车型选择')).click()
        elif select_fault == '并集':
            pass

        time.sleep(1)
        car_status = deal_car(driver, car, 1, 1)
        if car_status is True:
            log_file_out('选车成功')
        else:
            log_file_out('选车失败')
            return
        # 故障模式选择页面
        time.sleep(2)

        driver.find_element_by_xpath('//*[text()=\'{}\']'.format('下一步')).click()
        time.sleep(5)

        # 检查部件搜索框
        driver.find_elements_by_class_name('ivu-input-default')[-2].send_keys(check_fault)
        # 点击查询
        Method(driver).click('xpath', '//a[text()="查询"]')
        time.sleep(1)

        fault_select_status = check_fault_select(driver, check_fault)
        if fault_select_status is True:
            log_file_out('部件搜索框验证成功')
        else:
            log_file_out('部件搜索框验证失败')
        # 点击重置
        Method(driver).click('xpath', '//a[text()="重置"]')
        time.sleep(1)

        if select_fault == '交集':
            fault_status = deal_occur(driver, fault, value)
        else:
            fault_status = deal_union(driver, fault)
        if fault_status is True:
            log_file_out('选择部件成功')
        else:
            log_file_out('选择部件失败')

        try:
            driver.find_element_by_xpath('//span[text()="计算"]').click()
            log_file_out('点击计算按钮成功')
        except NoSuchElementException as e:
            logger.error(e)
            log_file_out('点击计算按钮失败')
        except:
            log_file_out('点击计算按钮失败')

        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                (By.XPATH, "ivu-message-notice")))
            a = driver.find_element_by_class_name("ivu-message-notice").text
        except:
            a = ''

        if a == '':
            pass
        else:
            if a == '结束里程必须大于开始里程':
                log_file_out('里程输入框结束里程必须大于开始里程验证成功')
                driver.find_elements_by_class_name('ivu-input-default')[6].send_keys(Keys.CONTROL, 'a')
                driver.find_elements_by_class_name('ivu-input-default')[6].send_keys(Keys.BACK_SPACE)
                time.sleep(0.5)
                driver.find_elements_by_class_name('ivu-input-default')[6].send_keys('100')
                time.sleep(1)
                driver.find_elements_by_class_name('ivu-input-default')[7].send_keys(Keys.CONTROL, 'a')
                driver.find_elements_by_class_name('ivu-input-default')[7].send_keys(Keys.BACK_SPACE)
                time.sleep(0.5)
                driver.find_elements_by_class_name('ivu-input-default')[7].send_keys('0')
                try:
                    driver.find_element_by_xpath('//span[text()="保存"]').click()
                except NoSuchElementException as e:
                    logger.error('xpath' + '不存在!')
                except:
                    log_file_out('模型录入错误')

                try:
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                        (By.CLASS_NAME, "ivu-message-notice")))
                    a1 = driver.find_element_by_class_name("ivu-message-notice").text
                except:
                    a1 = ''
                if a1 == '':
                    log_file_out('里程输入框结束里程必须大于开始里程验证失败,结束里程未小于开始里程')
                    return
                else:
                    driver.find_elements_by_class_name('ivu-input-default')[6].send_keys(Keys.CONTROL, 'a')
                    driver.find_elements_by_class_name('ivu-input-default')[6].send_keys(Keys.BACK_SPACE)
                    time.sleep(0.5)
                    driver.find_elements_by_class_name('ivu-input-default')[6].send_keys('0')
                    time.sleep(1)
                    driver.find_elements_by_class_name('ivu-input-default')[7].send_keys(Keys.CONTROL, 'a')
                    driver.find_elements_by_class_name('ivu-input-default')[7].send_keys(Keys.BACK_SPACE)
                    time.sleep(0.5)
                    driver.find_elements_by_class_name('ivu-input-default')[7].send_keys('100')

                    Method(driver).click('xpath', '//a[text()="优化后里程"]')
                    time.sleep(1)
                    driver.find_elements_by_class_name('ivu-input-default')[9].send_keys('200')
                    try:
                        driver.find_element_by_xpath('//span[text()="保存"]').click()
                    except NoSuchElementException as e:
                        logger.error('xpath' + '不存在!')
                    except:
                        log_file_out('模型录入错误')

        try:
            WebDriverWait(driver, wait_time).until(EC.presence_of_element_located(
                (By.CLASS_NAME, "ivu-message-notice")))
            error_message = driver.find_element_by_class_name("ivu-message-notice").text
        except:
            error_message = ''


        if error_message == '':
            try:
                driver.find_element_by_xpath('//span[text()=\'{}\']'.format("关联故障"))
            except Exception as e:
                log_file_out('保存失败')
                return

            log_file_out('评估成功')

            try:
                time.sleep(2)
                # 设置图表保存目录为bin下面picture下面的repair_not_save_picture 图片中路径要为"\\"
                wholepath = os.path.dirname(__file__) + '\\' + 'picture' + '\\repair_not_save_picture'
                # 判断目录是否存在
                if os.path.isdir(wholepath) is True:
                    pass
                else:
                    os.mkdir(wholepath)

                driver.save_screenshot(wholepath + '\\' + '百万公里故障率' + '.png')
                log_file_out('截取百万公里故障率图表成功')
            except:
                log_file_out('截取百万公里故障率图表失败')

            try:
                Method(driver).click('xpath','//span[text()="固有可用度"]')
                time.sleep(2)
                driver.save_screenshot(wholepath + '\\' + '固有可用度' + '.png')
                log_file_out('截取固有可用度图表成功')
            except:
                log_file_out('截取固有可用度图表失败')

            try:
                Method(driver).click('xpath','//span[text()="各部件百万公里故障率"]')
                time.sleep(2)
                if len(driver.find_elements_by_class_name('repair_selection')) == 1:
                    log_file_out('各部件百万公里故障率在图表页面增加了筛选条件输入')
                else:
                    log_file_out('各部件百万公里故障率在图表页面没有增加筛选条件输入')
                driver.save_screenshot(wholepath + '\\' + '各部件百万公里故障率' + '.png')
                log_file_out('截取各部件百万公里故障率图表成功')
            except:
                log_file_out('截取各部件百万公里故障率图表失败')

            try:
                time.sleep(1)
                Method(driver).click('xpath', '//span[text()="百万公里故障率(变化趋势)"]')
                time.sleep(2)

                driver.save_screenshot(wholepath + '\\' + '百万公里故障率(变化趋势)' + '.png')
                log_file_out('截取百万公里故障率(变化趋势)图表成功')
            except:
                log_file_out('截取百万公里故障率(变化趋势)图表失败')

            try:
                time.sleep(1)
                Method(driver).click('xpath', '//span[text()="运用概况"]')
                time.sleep(2)

                driver.save_screenshot(wholepath + '\\' + '运用概况' + '.png')
                log_file_out('截取运用概况图表成功')
            except:
                log_file_out('截取运用概况图表失败')

            try:
                time.sleep(1)
                Method(driver).click('xpath', '//span[text()="可靠性指标统计"]')
                time.sleep(2)

                driver.save_screenshot(wholepath + '\\' + '可靠性指标统计' + '.png')
                log_file_out('截取可靠性指标统计图表成功')
            except:
                log_file_out('截取可靠性指标统计图表失败')

        else:
            log_file_out(error_message)
            return
    else:
        log_file_out(contents[1] + '模型新增失败')
    driver.close()

# 技术变更不保存计算以及图表
def technical_nosave_model_check(url,username,password,contents,value,select,tech_change,car,fault,select_fault,wait_time):
    # option = webdriver.ChromeOptions()
    # option.add_argument("headless")
    # driver = webdriver.Chrome(chrome_options=option,                                                                executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')

    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    log_file_out('-----' + contents[1] + '保存验证' + '-----')
    status = new_built(driver, url, username, password, contents, 3)
    if status is True:
        log_file_out('登录成功')
        time.sleep(2)

        # 录入模型信息
        try:
            Method(driver).click('xpath', '//span[text()="请输入评估对象"]')
            time.sleep(1)
            if value == 1:
                driver.find_elements_by_xpath('//li[text()="评估系统、部件"]')[1].click()
            elif value == 2:
                driver.find_elements_by_xpath('//li[text()="故障模式"]')[1].click()

            log_file_out('录入模型基本信息成功')
        except NoSuchElementException as e:
            logger.debug('录入模型基本信息失败')
            logger.error(e)


        time.sleep(1)
        # 新增里程
        try:
            if select == '里程':
                driver.find_elements_by_class_name('ivu-input-default')[2].send_keys(tech_change[0])
                time.sleep(0.5)
                driver.find_elements_by_class_name('ivu-input-default')[3].send_keys(tech_change[1])
                time.sleep(1)
                driver.find_elements_by_class_name('ivu-input-default')[4].send_keys(tech_change[1])
                time.sleep(0.5)
                driver.find_elements_by_class_name('ivu-input-default')[5].send_keys(tech_change[2])
            else:
                Method(driver).click('xpath', '//a[text()="起始日期"]')
                driver.find_elements_by_class_name('ivu-input-default')[6].send_keys(tech_change[0])
                time.sleep(0.5)
                driver.find_elements_by_class_name('ivu-input-default')[7].send_keys(tech_change[1])
                time.sleep(1)
                driver.find_elements_by_class_name('ivu-input-default')[8].send_keys(tech_change[1])
                time.sleep(0.5)
                driver.find_elements_by_class_name('ivu-input-default')[9].send_keys(tech_change[2])
            log_file_out('新增'+select+'成功')
        except NoSuchElementException as e:
            logger.error('xpath' + '不存在！')
            log_file_out('新增'+select+'失败')

        time.sleep(1)
        # 车型 车号新增页面
        if select_fault == '交集':
            driver.find_element_by_xpath('//*[contains(text(),\'{}\')]'.format('是否根据车型选择')).click()
        elif select_fault == '并集':
            pass

        time.sleep(1)
        car_status = deal_car(driver, car, 1, 1)
        if car_status is True:
            log_file_out('选车成功')
        else:
            log_file_out('选车失败')
            return
        # 故障模式选择页面
        time.sleep(2)

        driver.find_element_by_xpath('//*[text()=\'{}\']'.format('下一步')).click()
        time.sleep(5)

        # 检查部件搜索框
        driver.find_elements_by_class_name('ivu-input-default')[-2].send_keys(check_fault)
        # 点击查询
        Method(driver).click('xpath', '//a[text()="查询"]')
        time.sleep(1)

        fault_select_status = check_fault_select(driver, check_fault)
        # 点击重置
        Method(driver).click('xpath', '//a[text()="重置"]')
        time.sleep(1)
        if fault_select_status is True:
            log_file_out('部件搜索框验证成功')
        else:
            log_file_out('部件搜索框验证失败')
        if select_fault == '交集':
            fault_status = deal_occur(driver, fault, value)
        else:
            fault_status = deal_union(driver, fault)
        if fault_status is True:
            log_file_out('选择部件成功')
        else:
            log_file_out('选择部件失败')

        # 点击计算按钮
        try:
            driver.find_element_by_xpath('//span[text()="计算"]').click()
            log_file_out('点击计算按钮成功')
        except NoSuchElementException as e:
            logger.error(e)
            log_file_out('点击计算按钮失败')
        except:
            log_file_out('点击计算按钮失败')


        try:
            WebDriverWait(driver, wait_time).until(EC.presence_of_element_located(
                (By.CLASS_NAME, "ivu-message-notice")))
            error_message = driver.find_element_by_class_name("ivu-message-notice").text
        except:
            error_message = ''

        if error_message == '':
            try:
                driver.find_element_by_xpath('//span[text()=\'{}\']'.format("关联故障"))
            except Exception as e:
                log_file_out('保存失败')
                return

            log_file_out('评估成功')

            try:
                time.sleep(2)
                # 设置图表保存目录为bin下面picture下面的tech_not_save_picture 图片中路径要为"\\"
                wholepath = os.path.dirname(__file__) + '\\' + 'picture' + '\\tech_not_save_picture'
                # 判断目录是否存在
                if os.path.isdir(wholepath) is True:
                    pass
                else:
                    os.mkdir(wholepath)

                driver.save_screenshot(wholepath + '\\' + '百万公里故障率' + '.png')
                log_file_out('截取百万公里故障率图表成功')
            except:
                log_file_out('截取百万公里故障率图表失败')

            try:
                Method(driver).click('xpath', '//span[text()="固有可用度"]')
                time.sleep(2)
                driver.save_screenshot(wholepath + '\\' + '固有可用度' + '.png')
                log_file_out('截取固有可用度图表成功')
            except:
                log_file_out('截取固有可用度图表失败')

            try:
                Method(driver).click('xpath', '//span[text()="各部件百万公里故障率"]')
                time.sleep(2)
                if len(driver.find_elements_by_class_name('repair_selection')) == 1:
                    log_file_out('各部件百万公里故障率在图表页面增加了筛选条件输入')
                else:
                    log_file_out('各部件百万公里故障率在图表页面没有增加筛选条件输入')
                driver.save_screenshot(wholepath + '\\' + '各部件百万公里故障率' + '.png')
                log_file_out('截取各部件百万公里故障率图表成功')
            except:
                log_file_out('截取各部件百万公里故障率图表失败')

            try:
                time.sleep(1)
                Method(driver).click('xpath', '//span[text()="百万公里故障率(变化趋势)"]')
                time.sleep(2)

                driver.save_screenshot(wholepath + '\\' + '百万公里故障率(变化趋势)' + '.png')
                log_file_out('截取百万公里故障率(变化趋势)图表成功')
            except:
                log_file_out('截取百万公里故障率(变化趋势)图表失败')

            try:
                time.sleep(1)
                Method(driver).click('xpath', '//span[text()="运用概况"]')
                time.sleep(2)

                driver.save_screenshot(wholepath + '\\' + '运用概况' + '.png')
                log_file_out('截取运用概况图表成功')
            except:
                log_file_out('截取运用概况图表失败')

            try:
                time.sleep(1)
                Method(driver).click('xpath', '//span[text()="可靠性指标统计"]')
                time.sleep(2)

                driver.save_screenshot(wholepath + '\\' + '可靠性指标统计' + '.png')
                log_file_out('截取可靠性指标统计图表成功')
            except:
                log_file_out('截取可靠性指标统计图表失败')
        else:
            log_file_out(error_message)
            return
    else:
        log_file_out(contents[1] + '模型新增失败')
    driver.close()

# 指标对比分析不保存计算及图表
def compare_nosave_model_check(url, username, password, contents, value, select, min_model, select_fault, wait_time):
    #
    # option = webdriver.ChromeOptions()
    # option.add_argument("headless")
    # driver = webdriver.Chrome(chrome_options=option,
    #                           executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    log_file_out('-----' + contents[1] + '保存验证' + '-----')
    status = new_built(driver, url, username, password, contents, 3)
    if status is True:
        log_file_out('登录成功')
        time.sleep(2)


        # 对新增指标页面进行操作
        try:
            driver.find_elements_by_class_name('ivu-select-placeholder')[3].click()
            time.sleep(1)

            if value == 1:
                driver.find_elements_by_xpath('//li[text()="评估系统、部件"]')[1].click()
            elif value == 2:
                driver.find_elements_by_xpath('//li[text()="故障模式"]')[1].click()

            log_file_out('模型录入成功')
        except Exception as e:
            logger.debug(e)
            log_file_out('模型录入失败')

        sum1 = 0

        average = 0
        num = 2
        num1 = 1
        num2 = 3
        try:
            for x in min_model:
                if len(min_model) == 2:
                    pass
                else:
                    for i in range(0, len(min_model) - 2):
                        Method(driver).click('xpath', '//span[text()="新增"]')
                driver.find_elements_by_class_name('ivu-input-default')[num].send_keys(x[0])

                time.sleep(1)
                try:
                    if select == '里程':

                        driver.find_elements_by_class_name('ivu-input-default')[num + 1].send_keys(x[1])

                        driver.find_elements_by_class_name('ivu-input-default')[num + 2].send_keys(x[2])

                        driver.find_elements_by_class_name('ivu-select-placeholder')[num2].click()
                        time.sleep(0.5)
                        if x[3] == 1:
                            driver.find_elements_by_xpath('//li[text()="180"]')[average].click()
                        elif x[3] == 2:
                            driver.find_elements_by_xpath('//li[text()="260"]')[average].click()

                    elif select == '时间':
                        time.sleep(1)
                        driver.find_elements_by_xpath('//a[text()="起始日期"]')[sum1].click()
                        time.sleep(2)

                        driver.find_elements_by_class_name('ivu-input-default')[num + 3].send_keys(x[1])

                        driver.find_elements_by_class_name('ivu-input-default')[num + 4].send_keys(x[2])

                        driver.find_elements_by_class_name('ivu-select-placeholder')[num2 + 1].click()
                        time.sleep(0.5)
                        if x[3] == 1:
                            driver.find_elements_by_xpath('//li[text()="180"]')[average + 1].click()
                        elif x[3] == 2:
                            driver.find_elements_by_xpath('//li[text()="260"]')[average + 1].click()
                except NoSuchElementException as e:
                    logger.error(e)

                driver.find_elements_by_xpath('//span[text()="新增"]')[num1].click()
                time.sleep(2)
                status = driver.execute_script(
                    'return document.querySelectorAll(".rcma .ivu-card-head .ivu-checkbox-input")[{}].checked'.format(
                        0))
                if status is True:
                    if select_fault == '交集':
                        driver.find_element_by_xpath('//*[contains(text(),\'{}\')]'.format('是否根据车型选择')).click()
                    elif select_fault == '并集':
                        pass
                else:
                    if select_fault == '交集':
                        pass
                    elif select_fault == '并集':
                        driver.find_element_by_xpath('//*[contains(text(),\'{}\')]'.format('是否根据车型选择')).click()

                time.sleep(1)
                car_status = deal_car(driver, x[4], 0,num1)
                if car_status is True:
                    log_file_out('选车成功')
                else:
                    log_file_out('选车失败')
                    return

                driver.find_element_by_xpath('//*[text()=\'{}\']'.format('下一步')).click()
                time.sleep(5)

                if select_fault == '交集':
                    fault_status = deal_occur1(driver, x[5], x[6])
                else:
                    fault_status = deal_union(driver, x[5])
                if fault_status is True:
                    log_file_out('选择部件成功')
                else:
                    log_file_out('选择部件失败')

                try:
                    driver.find_elements_by_xpath('//span[text()="确定"]')[num1].click()
                    logger.debug('bug不存在')
                except NoSuchElementException as e:
                    logger.error('xpath' + '不存在!')
                except:
                    log_file_out('模型录入错误')

                average += 2
                sum1 += 1
                num += 13
                num1 += 1
                num2 += 3
            log_file_out('录入模型成功')
        except Exception as e:
            logger.error(e)
            log_file_out('录入模型错误')
        time.sleep(2)
        try:
            driver.find_element_by_xpath('//span[text()="计算"]').click()
            logger.debug('bug不存在')
        except NoSuchElementException as e:
            logger.error('xpath' + '不存在!')
        except:
            log_file_out('模型录入错误')

        try:
            WebDriverWait(driver, wait_time).until(EC.presence_of_element_located(
                (By.CLASS_NAME, "ivu-message-notice")))
            # 获取报错信息
            error_message = driver.find_element_by_class_name("ivu-message-notice").text
        except:
            error_message = ''

        if error_message != '':
            log_file_out(error_message)
            return
        else:
            try:
                driver.find_element_by_xpath('//span[text()=\'{}\']'.format("关联故障"))
            except Exception as e:
                log_file_out('保存失败')
                return

            try:
                # 设置图表保存目录为bin下面picture下面的compare_not_save_picture 图片中路径要为"\\"
                wholepath = os.path.dirname(__file__) + '\\' + 'picture' + '\\compare_not_save_picture'
                # 判断目录是否存在
                if os.path.isdir(wholepath) is True:
                    pass
                else:
                    os.mkdir(wholepath)
                driver.save_screenshot(wholepath + '\\' + '百万公里故障率' + '.png')
                log_file_out('截取图表成功')
            except:
                log_file_out('截取图表失败')
    else:
        log_file_out(contents[1]+'不保存计算功能验证失败')

# femca不保存计算及图片保存
def fmcea_notsave_check(url,username,password,contents,select,start,end,car,fault,select_fault,check_fault,wait_time):
    # option = webdriver.ChromeOptions()
    # option.add_argument("headless")
    # driver = webdriver.Chrome(chrome_options=option,                                                                executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    log_file_out('-----' + contents[1] + '保存验证' + '-----')
    status = new_built(driver, url, username, password, contents,3)
    if status is True:
        log_file_out('登录成功')
        time.sleep(2)

        if select == '里程':
            try:
                driver.find_elements_by_class_name('ivu-input-default')[2].send_keys(start)
                driver.find_elements_by_class_name('ivu-input-default')[3].send_keys(end)
                log_file_out('添加里程成功')
            except NoSuchElementException as e:
                logger.error(e)
                log_file_out('添加里程失败')
        elif select == '时间':
            try:
                Method(driver).click('xpath', '//a[text()="起始日期"]')
                time.sleep(1)
                Method(driver).input('xpath', "//input[@placeholder='请输入开始日期']", start)
                time.sleep(0.5)
                Method(driver).input('xpath', "//input[@placeholder='请输入结束日期']", end)
                log_file_out('添加时间成功')
            except NoSuchElementException as e:
                log_file_out('添加时间失败')

            # 车型 车号新增页面
        if select_fault == '交集':
            driver.find_element_by_xpath('//*[contains(text(),\'{}\')]'.format('是否根据车型选择')).click()
        elif select_fault == '并集':
            pass

        time.sleep(1)
        car_status = deal_car(driver, car, 1, 1)
        if car_status is True:
            log_file_out('选车成功')
        else:
            log_file_out('选车失败')
            return
        # 故障模式选择页面
        time.sleep(2)

        driver.find_element_by_xpath('//*[contains(text(),\'{}\')]'.format('下一步')).click()
        time.sleep(5)

        # 检查部件搜索框
        driver.find_elements_by_class_name('ivu-input-default')[-2].send_keys(check_fault)
        # 点击查询
        Method(driver).click('xpath', '//a[text()="查询"]')
        time.sleep(1)

        fault_select_status = check_fault_select(driver, check_fault)
        # 点击重置
        Method(driver).click('xpath', '//a[text()="重置"]')
        time.sleep(1)
        if fault_select_status is True:
            log_file_out('部件搜索框验证成功')
        else:
            log_file_out('部件搜索框验证失败')
        if select_fault == '交集':
            fault_status = deal_occur(driver, fault, 1)
        else:
            fault_status = deal_union(driver, fault)
        if fault_status is True:
            log_file_out('选择部件成功')
        else:
            log_file_out('选择部件失败')

        # 点击保存按钮
        try:
            Method(driver).click('xpath','//span[text()="计算"]')
            log_file_out('点击计算按钮成功')
        except NoSuchElementException as e:
            logger.error(e)
            log_file_out('点击计算按钮失败')
        except:
            log_file_out('点击计算按钮失败')

        try:
            WebDriverWait(driver, wait_time).until(EC.presence_of_element_located(
                (By.CLASS_NAME, "ivu-message-notice")))
            error_message = driver.find_element_by_class_name("ivu-message-notice").text
        except:
            error_message = ''

        if error_message == '':
            try:
                driver.find_element_by_xpath('//span[text()=\'{}\']'.format('导出表格'))
            except Exception as e:
                log_file_out('保存失败')
                return

            try:
                time.sleep(2)
                if '.csv' not in driver.find_element_by_class_name('ivu-btn-success').find_element_by_tag_name('span').text:
                    log_file_out('导出按钮中不包含csv字样,验证成功')
                else:
                    log_file_out('导出按钮中包含csv字样,验证失败')
                # 设置图表保存目录为bin下面picture下面的femca_not_save_picture 图片中路径要为"\\"
                wholepath = os.path.dirname(__file__) + '\\' + 'picture' + '\\femca_not_save_picture'
                # 判断目录是否存在
                if os.path.isdir(wholepath) is True:
                    pass
                else:
                    os.mkdir(wholepath)

                driver.save_screenshot(wholepath + '\\' + 'FMECA分析列表' + '.png')
                return
            except:
                log_file_out('截图失败')
        else:
            log_file_out(error_message)
            return
    driver.close()

# nhpp不保存计算及图片保存
def nhpp_notsave_check(url,username,password,contents,start,end,car):
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    log_file_out('-----' + contents[1] + '保存验证' + '-----')
    status = new_built(driver, url, username, password, contents, 3)

    if status is True:
        log_file_out('登录成功')
        time.sleep(2)
        # 对不保存页面进行操作
        try:
            driver.find_elements_by_class_name('ivu-input-default')[3].send_keys(start)
            time.sleep(0.5)
            driver.find_elements_by_class_name('ivu-input-default')[4].send_keys(end)
            time.sleep(0.5)

            log_file_out('时间录入成功')
        except NoSuchElementException as e:
            logger.error(e)
            log_file_out('时间录入失败')

        car_status = deal_car(driver, car, 1,1)
        if car_status is True:
            log_file_out('选车成功')
        else:
            log_file_out('选车失败')
            return

        try:
            time.sleep(1)
            driver.find_element_by_xpath('//span[text()="计算"]').click()
            log_file_out('点击计算按钮成功')
        except NoSuchElementException as e:
            logger.error(e)
            log_file_out('点击计算按钮失败')

        try:
            WebDriverWait(driver, wait_time).until(EC.presence_of_element_located(
                (By.CLASS_NAME, "ivu-message-notice")))
            error_message = driver.find_element_by_class_name("ivu-message-notice").text
        except:
            error_message = ''

        if error_message == '':
            if len(driver.find_elements_by_class_name('chartParatDom')) == 0:
                log_file_out('计算失败')
                return
            else:
                log_file_out('计算成功')

                time.sleep(2)
                try:
                    driver.find_element_by_xpath('//span[text()="关闭"]')
                    # 设置图表保存目录为bin下面picture下面的nhpp_not_save_picture 图片中路径要为"\\"
                    wholepath = os.path.dirname(__file__) + '\\' + 'picture' + '\\nhpp_not_save_picture'
                    # 判断目录是否存在
                    if os.path.isdir(wholepath) is True:
                        pass
                    else:
                        os.mkdir(wholepath)

                    time.sleep(1)
                    target = driver.find_elements_by_class_name('chartParatDom')[0]
                    driver.execute_script("arguments[0].scrollIntoView();", target)
                    driver.save_screenshot(wholepath + '\\' + '平均累计里程数' + '.png')
                    time.sleep(1)
                    target = driver.find_elements_by_class_name('chartParatDom')[1]
                    driver.execute_script("arguments[0].scrollIntoView();", target)
                    driver.save_screenshot(wholepath + '\\' + 'CMDFB&IMDFB' + '.png')
                    time.sleep(1)
                    target = driver.find_elements_by_class_name('chartParatDom')[2]
                    driver.execute_script("arguments[0].scrollIntoView();", target)
                    driver.save_screenshot(wholepath + '\\' + '车辆真实累计故障数与计算累计故障数对比' + '.png')
                    time.sleep(1)
                    target = driver.find_elements_by_class_name('chartParatDom')[3]
                    driver.execute_script("arguments[0].scrollIntoView();", target)
                    driver.save_screenshot(wholepath + '\\' + '累计里程故障预测与预测差值对比' + '.png')
                    log_file_out('图表截取成功')
                except:
                    log_file_out('图表截取失败')
                    return
        else:
            log_file_out(error_message)
            return
    driver.close()