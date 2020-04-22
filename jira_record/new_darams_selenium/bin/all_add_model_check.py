from config.config import *

# 内控模型新增及图片保存
def incontrol_add_check(url,username,password,contents,modelName,start,end,remarks,car,wait_time):
    # option = webdriver.ChromeOptions()
    # option.add_argument("headless")
    # driver = webdriver.Chrome(chrome_options=option,                                                                executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    status = new_built(driver, url, username, password, contents,1)
    if status is True:
        log_file_out('登录成功')
        time.sleep(2)

        # 设置图表保存目录为bin下面picture下面的incontrol_picture 图片中路径要为"\\"
        wholepath = os.path.dirname(__file__) + '\\' + 'picture' + '\\incontrol_picture'
        # 判断目录是否存在
        if os.path.isdir(wholepath) is True:
            pass
        else:
            os.mkdir(wholepath)
        driver.save_screenshot(wholepath + '\\' + '内控模型' + '.png')

        try:
            driver.find_elements_by_class_name('ivu-input-default')[2].send_keys(modelName)
            time.sleep(0.5)
            driver.find_elements_by_class_name('ivu-input-default')[3].send_keys(start)
            time.sleep(0.5)
            driver.find_elements_by_class_name('ivu-input-default')[4].send_keys(end)

            if remarks == '':
                time.sleep(1)
            else:
                driver.find_elements_by_class_name('ivu-input-default')[5].send_keys(remarks)
            log_file_out('模型基本信息录入成功')
        except NoSuchElementException as e:
            log_file_out('模型基本信息录入失败')

        time.sleep(2)

        car_status = deal_car(driver, car, 1,1)
        if car_status is True:
            log_file_out('选车成功')
        else:
            log_file_out('选车失败')
            return

        try:
            time.sleep(2)
            driver.find_element_by_xpath('//span[text()="保存"]').click()
            log_file_out('点击保存按钮成功')
        except NoSuchElementException as e:
            logger.error(e)
            log_file_out('点击保存按钮失败')
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                (By.CLASS_NAME, "ivu-message-notice")))
            a = driver.find_element_by_class_name("ivu-message-notice").text
        except:
            a = ''

        if a == '':
            try:
                a = len(driver.find_elements_by_xpath('//a[text()=\'{}\']/../../../td[6]/div/a[1]'.format(modelName)))
                for i in range(0,a):
                    try:
                        driver.find_elements_by_xpath('//a[text()=\'{}\']/../../../td[6]/div/a[1]'.format(modelName))[i].click()
                        time_now = datetime.datetime.now().replace(microsecond=0)
                        break
                    except:
                        pass

                log_file_out('点击评估按钮成功')
            except WebDriverException:
                log_file_out('点击评估按钮失败')
                return

            time.sleep(2)
            # 获取页面中评估的时间
            try:
                click_assess_time = driver.find_element_by_xpath('//a[text()=\'{}\']/../../../td[4]/div'.format(modelName)).text
                click_assess_time1 = datetime.datetime.strptime(click_assess_time, "%Y-%m-%d %H:%M:%S")
                log_file_out('获取评估时间成功')
            except Exception as e:
                logger.error(e)
                log_file_out('获取评估时间失败')

            if (click_assess_time1 - time_now).seconds < 30:
                log_file_out('评估时间与实际时间相符,验证成功')
            else:
                log_file_out('评估时间与实际时间不相符,验证失败')

            try:
                a = WebDriverWait(driver, wait_time).until(EC.text_to_be_present_in_element((By.XPATH, "//a[text()=\'{}\']/../../../td[3]/div".format(modelName)),
                        u'计算完成'))
                if a is True:
                    logger.debug('评估成功')
                    try:
                        a = len(driver.find_elements_by_xpath('//a[text()=\'{}\']/../../../td[6]/div/a[3]'.format(modelName)))
                        for i in range(0, a):
                            try:
                                driver.find_elements_by_xpath('//a[text()=\'{}\']/../../../td[6]/div/a[3]'.format(modelName))[i].click()
                                break
                            except:
                                pass
                        log_file_out('点击图表按钮成功')
                        try:
                            driver.find_element_by_xpath('//span[text()="关闭"]')
                            driver.find_element_by_class_name('chartParatDom')
                            driver.save_screenshot(wholepath + '\\' + '责任部室故障次数' + '.png')
                            time.sleep(1)
                            target = driver.find_elements_by_class_name('chartParatDom')[1]
                            driver.execute_script("arguments[0].scrollIntoView();", target)
                            driver.save_screenshot(wholepath + '\\' + '各部室分月责任统计' + '.png')
                            time.sleep(1)
                            target = driver.find_elements_by_class_name('chartParatDom')[2]
                            driver.execute_script("arguments[0].scrollIntoView();", target)
                            driver.save_screenshot(wholepath + '\\' + '各部室月累计责任' + '.png')
                            time.sleep(1)
                            target = driver.find_elements_by_class_name('chartParatDom')[3]
                            driver.execute_script("arguments[0].scrollIntoView();", target)
                            driver.save_screenshot(wholepath + '\\' + '供应商内控指标' + '.png')
                        except:
                            log_file_out('图表保存失败')
                            return
                    except WebDriverException:
                        log_file_out('点击图表按钮失败')
                        return
            except Exception as e:
                logger.error(e)
                logger.debug('评估失败')
    driver.close()

# 修程修制新增及图片保存
def repair_add_check(url,username,password,contents,modelName,value,remarks,repair_mileage,car,fault,select_fault,check_fault,wait_time):

    # option = webdriver.ChromeOptions()
    # option.add_argument("headless")
    # driver = webdriver.Chrome(chrome_options=option
    # ,executable_path=r'../apps/chromedriver.exe'
    #  )
    # driver.maximize_window()


    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    status = new_built(driver, url, username, password, contents,1)
    if status is True:
        log_file_out('登录成功')
        time.sleep(2)

        # 录入模型信息
        try:
            Method(driver).input('xpath', "//input[@placeholder='请输入模型名称']", modelName)
            time.sleep(1)
            Method(driver).click('xpath', '//span[text()="请输入评估对象"]')
            time.sleep(1)
            if value == 1:
                driver.find_elements_by_xpath('//li[text()="评估系统、部件"]')[1].click()
            elif value == 2:
                driver.find_elements_by_xpath('//li[text()="故障模式"]')[1].click()

            if remarks == '':
                time.sleep(1)
            else:
                driver.find_elements_by_class_name('ivu-input-default')[3].send_keys(remarks)
            if remarks is '':
                pass
            else:
                Method(driver).input('xpath', "//input[@placeholder='请输入备注信息']",remarks)
            log_file_out('录入模型基本信息成功')
        except NoSuchElementException as e:
            logger.debug('录入模型基本信息失败')
            logger.error(e)


        # 优化前里程
        try:
            driver.find_elements_by_class_name('ivu-input-default')[6].send_keys(repair_mileage[0])
            time.sleep(0.5)
            driver.find_elements_by_class_name('ivu-input-default')[7].send_keys(repair_mileage[1])
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
            driver.find_elements_by_class_name('ivu-input-default')[9].send_keys(repair_mileage[2])

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
            driver.find_element_by_xpath('//span[text()="保存"]').click()
            logger.debug('bug不存在')
        except NoSuchElementException as e:
            logger.error('xpath' + '不存在!')
        except:
            log_file_out('模型录入错误')

        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                (By.CLASS_NAME, "ivu-message-notice")))
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
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                (By.CLASS_NAME, "ivu-message-notice")))
            a2 = driver.find_element_by_class_name("ivu-message-notice").text
        except:
            a2 = ''
        time.sleep(2)
        if a2 == '':

            try:
                a = len(
                    driver.find_elements_by_xpath('//a[text()=\'{}\']/../../../td[6]/div/a[3]'.format(modelName)))
                for i in range(0, a):
                    try:
                        driver.find_elements_by_xpath(
                            '//a[text()=\'{}\']/../../../td[6]/div/a[3]'.format(modelName))[
                            i].click()
                        ## 获取点击评估的时间
                        time_now = datetime.datetime.now().replace(microsecond=0)
                        break
                    except:
                        pass
                log_file_out('点击评估按钮成功')
            except WebDriverException:
                log_file_out('点击评估按钮失败')
                return
            # 获取页面中评估的时间
            click_assess_time = driver.find_element_by_xpath(
                '//a[text()=\'{}\']/../../../td[4]/div'.format(modelName)).text
            click_assess_time1 = datetime.datetime.strptime(click_assess_time, "%Y-%m-%d %H:%M:%S")
            if (click_assess_time1 - time_now).seconds < 30:
                log_file_out('评估时间与实际时间相符,验证成功')
            else:
                log_file_out('评估时间与实际时间不相符,验证失败')

            try:
                a = WebDriverWait(driver, wait_time).until(
                    EC.text_to_be_present_in_element(
                        (By.XPATH, "//a[text()=\'{}\']/../../../td[3]/div".format(modelName)),
                        u'计算完成'))
                if a is True:
                    logger.debug('评估成功')

                    try:
                        a = len(driver.find_elements_by_xpath(
                            '//a[text()=\'{}\']/../../../td[6]/div/a[4]'.format(modelName)))
                        for i in range(0, a):
                            try:
                                driver.find_elements_by_xpath(
                                    '//a[text()=\'{}\']/../../../td[6]/div/a[4]'.format(modelName))[i].click()
                                break
                            except:
                                pass
                        log_file_out('点击图表按钮成功')

                        try:
                            time.sleep(2)
                            # 设置图表保存目录为bin下面picture下面的incontrol_picture 图片中路径要为"\\"
                            wholepath = os.path.dirname(__file__) + '\\' + 'picture' + '\\repair_picture'
                            # 判断目录是否存在
                            if os.path.isdir(wholepath) is True:
                                pass
                            else:
                                os.mkdir(wholepath)
                            target = driver.find_elements_by_class_name('chartParatDom')[0]
                            driver.execute_script("arguments[0].scrollIntoView();", target)
                            driver.save_screenshot(wholepath + '\\' + '优化前后百万公里故障率' + '.png')
                        except:
                            log_file_out('截取各系统/部件故障占比失败')

                        if len(driver.find_elements_by_class_name('repair_selection')) == 1:
                            log_file_out('各部件百万公里故障率在图表页面增加了筛选条件输入')
                        else:
                            log_file_out('各部件百万公里故障率在图表页面没有增加筛选条件输入')
                        try:
                            time.sleep(1)
                            target = driver.find_elements_by_class_name('chartParatDom')[1]
                            driver.execute_script("arguments[0].scrollIntoView();", target)
                            driver.save_screenshot(wholepath + '\\' + '各部件百万公里故障率' + '.png')
                            time.sleep(1)
                            target = driver.find_elements_by_class_name('chartParatDom')[2]
                            driver.execute_script("arguments[0].scrollIntoView();", target)
                            driver.save_screenshot(wholepath + '\\' + '百万公里故障率' + '.png')
                            time.sleep(1)
                            target = driver.find_elements_by_class_name('chartParatDom')[3]
                            driver.execute_script("arguments[0].scrollIntoView();", target)
                            driver.save_screenshot(wholepath + '\\' + '固有可用度' + '.png')
                            time.sleep(1)

                        except:
                            print('点击图表按钮失败')
                            return
                    except WebDriverException:
                        log_file_out('点击图表按钮失败')
                        return

                    # 查看点击图表出来的页面是否存在

            except Exception as e:
                logger.debug('评估失败')
    else:
        log_file_out(contents[1] + '模型新增失败')
    driver.close()

# 技术变更新增以及图表
def technical_change_add_check(url,username,password,contents,modelName,value,remarks,select,tech_change,speed,car,fault,select_fault,wait_time):
    # option = webdriver.ChromeOptions()
    # option.add_argument("headless")
    # driver = webdriver.Chrome(chrome_options=option,                                                                executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')

    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    status = new_built(driver, url, username, password, contents,1)
    if status is True:
        log_file_out('登录成功')
        time.sleep(2)

        # 录入模型信息
        try:
            Method(driver).input('xpath', "//input[@placeholder='请输入模型名称']", modelName)
            time.sleep(1)
            Method(driver).click('xpath', '//span[text()="请输入评估对象"]')
            time.sleep(1)
            if value == 1:
                driver.find_elements_by_xpath('//li[text()="评估系统、部件"]')[1].click()
            elif value == 2:
                driver.find_elements_by_xpath('//li[text()="故障模式"]')[1].click()

            if remarks is '':
                pass
            else:
                Method(driver).input('xpath', "//input[@placeholder='请输入备注信息']", remarks)
            log_file_out('录入模型基本信息成功')
        except NoSuchElementException as e:
            logger.debug('录入模型基本信息失败')
            logger.error(e)


        time.sleep(1)
        # 新增里程
        if select == '里程':
            pass
        else:
            Method(driver).click('xpath', '//a[text()="起始日期"]')
        time.sleep(1)
        try:
            driver.find_elements_by_class_name('ivu-icon-md-add')[2].click()
            driver.find_elements_by_class_name('ivu-input-default')[10].send_keys(tech_change[0])
            time.sleep(0.5)
            driver.find_elements_by_class_name('ivu-input-default')[11].send_keys(tech_change[1])
            driver.find_elements_by_class_name('ivu-icon-md-add')[2].click()
            time.sleep(1)
            driver.find_elements_by_class_name('ivu-input-default')[12].send_keys(tech_change[1])
            time.sleep(0.5)
            driver.find_elements_by_class_name('ivu-input-default')[13].send_keys(tech_change[2])

            log_file_out('新增'+select+'成功')
        except NoSuchElementException as e:
            logger.error('xpath' + '不存在！')
            log_file_out('新增'+select+'失败')

        # 选择时速
        driver.find_elements_by_class_name('ivu-select-placeholder')[-2].click()
        time.sleep(0.5)
        if speed == 1:
            driver.find_element_by_xpath('//li[text()="180"]').click()
        elif speed == 2:
            driver.find_element_by_xpath('//li[text()="260"]').click()
        time.sleep(1)
        driver.find_elements_by_class_name('ivu-select-placeholder')[-1].click()
        time.sleep(0.5)
        if speed == 1:
            driver.find_elements_by_xpath('//li[text()="180"]')[1].click()
        elif speed == 2:
            driver.find_elements_by_xpath('//li[text()="260"]')[1].click()

        time.sleep(1)
        # 点击车型-车号新增
        driver.find_elements_by_class_name('ivu-icon-md-add')[1].click()
        time.sleep(1)
        # 车型 车号新增页面
        if select_fault == '交集':
            driver.find_element_by_xpath('//*[contains(text(),\'{}\')]'.format('是否根据车型选择')).click()
        elif select_fault == '并集':
            pass

        time.sleep(1)
        car_status = deal_car(driver, car, 0, 1)
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

        # 点击确定按钮
        try:
            driver.find_elements_by_xpath('//span[text()="确定"]')[1].click()
            log_file_out('点击确定按钮成功')
        except Exception as e:
            logger.error(e)
            log_file_out('点击确定按钮失败')
        time.sleep(1)
        try:
            driver.find_element_by_xpath('//span[text()="保存"]').click()
            log_file_out('点击保存按钮成功')
        except NoSuchElementException as e:
            logger.error(e)
            log_file_out('点击保存按钮失败')
        except:
            log_file_out('点击保存按钮失败')

        # try:
        #     WebDriverWait(driver, 3).until(EC.presence_of_element_located(
        #         (By.CLASS_NAME, "ivu-message-notice")))
        #     a = driver.find_element_by_class_name("ivu-message-notice").text
        # except:
        #     a = ''
        #
        # if a == '':
        #     pass
        # else:
        #     pass

        try:
            WebDriverWait(driver, 3).until(EC.presence_of_element_located(
                (By.CLASS_NAME, "ivu-message-notice")))
            a2 = driver.find_element_by_class_name("ivu-message-notice").text
        except:
            a2 = ''

        if a2 == '':
            try:
                a = len(driver.find_elements_by_xpath('//a[text()=\'{}\']/../../../td[6]/div/a[3]'.format(modelName)))
                for i in range(0, a):
                    try:
                        driver.find_elements_by_xpath(
                            '//a[text()=\'{}\']/../../../td[6]/div/a[3]'.format(modelName))[
                            i].click()
                        ## 获取点击评估的时间
                        time_now = datetime.datetime.now().replace(microsecond=0)
                        break
                    except:
                        pass
                log_file_out('点击评估按钮成功')
            except WebDriverException:
                log_file_out('点击评估按钮失败')
                return
            time.sleep(2)
            # 获取页面中评估的时间
            click_assess_time = driver.find_element_by_xpath(
                '//a[text()=\'{}\']/../../../td[4]/div'.format(modelName)).text
            if int(click_assess_time.split(':')[0][-2:]) >= 24:
                click_assess_time = click_assess_time.split(' ')[0] + ' '+'0'+ str(int(click_assess_time.split(':')[0][-2:])-24) + ':' + \
                                    click_assess_time.split(':')[1] + ':'+click_assess_time.split(':')[2]
            else:
                pass
            click_assess_time1 = datetime.datetime.strptime(click_assess_time, "%Y-%m-%d %H:%M:%S")
            if (click_assess_time1 - time_now).seconds < 30:
                log_file_out('评估时间与实际时间相符,验证成功')
            else:
                log_file_out('评估时间与实际时间不相符,验证失败')

            try:
                a = WebDriverWait(driver, wait_time).until(
                    EC.text_to_be_present_in_element(
                        (By.XPATH, "//a[text()=\'{}\']/../../../td[3]/div".format(modelName)),
                        u'计算完成'))
                if a is True:
                    logger.debug('评估成功')
                    try:
                        a = len(driver.find_elements_by_xpath(
                            '//a[text()=\'{}\']/../../../td[6]/div/a[4]'.format(modelName)))
                        for i in range(0, a):
                            try:
                                driver.find_elements_by_xpath(
                                    '//a[text()=\'{}\']/../../../td[6]/div/a[4]'.format(modelName))[i].click()
                                break
                            except:
                                pass
                        log_file_out('点击图表按钮成功')

                        try:
                            time.sleep(2)
                            # 设置图表保存目录为bin下面picture下面的incontrol_picture 图片中路径要为"\\"
                            wholepath = os.path.dirname(__file__) + '\\' + 'picture' + '\\tech_picture'
                            # 判断目录是否存在
                            if os.path.isdir(wholepath) is True:
                                pass
                            else:
                                os.mkdir(wholepath)
                            try:
                                time.sleep(2)

                                target = driver.find_elements_by_class_name('chartParatDom')[0]
                                driver.execute_script("arguments[0].scrollIntoView();", target)
                                driver.save_screenshot(wholepath + '\\' + '变更前后百万公里故障率' + '.png')
                            except:
                                log_file_out('截取变更前后百万公里故障率失败')

                            if len(driver.find_elements_by_class_name('repair_selection')) == 1:
                                log_file_out('各部件百万公里故障率在图表页面增加了筛选条件输入,验证成功')
                            else:
                                log_file_out('各部件百万公里故障率在图表页面没有增加筛选条件输入,验证失败')
                            try:
                                time.sleep(1)
                                target = driver.find_elements_by_class_name('chartParatDom')[1]
                                driver.execute_script("arguments[0].scrollIntoView();", target)
                                driver.save_screenshot(wholepath + '\\' + '变更前后固有可用度' + '.png')
                                time.sleep(1)
                                target = driver.find_elements_by_class_name('chartParatDom')[2]
                                driver.execute_script("arguments[0].scrollIntoView();", target)
                                driver.save_screenshot(wholepath + '\\' + '各部件百万公里故障率' + '.png')
                                time.sleep(1)
                                target = driver.find_elements_by_class_name('chartParatDom')[3]
                                driver.execute_script("arguments[0].scrollIntoView();", target)
                                driver.save_screenshot(wholepath + '\\' + '白万公里故障率' + '.png')
                                time.sleep(1)
                            except:
                                log_file_out('截取图片失败')
                                return
                        except:
                            log_file_out('截图失败')
                    except WebDriverException:
                        log_file_out('点击图表按钮失败')
                        return
                    # 查看点击图表出来的页面是否存在
            except Exception as e:
                logger.debug('评估失败')
    else:
        log_file_out(contents[1] + '模型新增失败')
    driver.close()

# RAMS立即计算新建
def rams_cal_check(url, username, password, contents, value, speed,select ,start, end, car, fault, select_fault, wait_time):
    #
    # option = webdriver.ChromeOptions()
    # option.add_argument("headless")
    # driver = webdriver.Chrome(chrome_options=option,
    #                           executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    status = new_built(driver, url, username, password, contents,2)
    if status is True:
        log_file_out('登录成功')
        time.sleep(2)

        try:
            Method(driver).click('class', 'ivu-select-placeholder')
            if value == 1:
                driver.find_elements_by_class_name('ivu-select-item')[0].click()
            elif value == 2:
                driver.find_elements_by_class_name('ivu-select-item')[1].click()
            # 选择时速
            Method(driver).click('class','ivu-select-placeholder')
            time.sleep(0.5)
            if speed == 1:
                driver.find_element_by_xpath('//li[text()="180"]').click()
            elif speed == 2:
                driver.find_element_by_xpath('//li[text()="260"]').click()

            if select == '里程':
                driver.find_elements_by_class_name('ivu-input')[2].send_keys(start)
                driver.find_elements_by_class_name('ivu-input')[3].send_keys(end)
            elif select == '时间':
                time.sleep(1)
                driver.find_elements_by_class_name('ivu-select-selected-value')[2].click()
                driver.find_element_by_xpath('//*[text()=\'{}\']'.format('日期')).click()
                time.sleep(1)
                driver.find_elements_by_class_name('ivu-input')[2].send_keys(start)
                driver.find_elements_by_class_name('ivu-input')[3].send_keys(end)

        except NoSuchElementException as e:
            logger.debug('模型基本信息输入失败')
            logger.error(e)
        except:
            logger.debug('请录入评估对象')
            return

        try:
            Method(driver).contains_xpath('click', '新增')
        except NoSuchElementException as e:
            logger.debug('点击新建按钮失败')
            logger.error(e)

        time.sleep(2)

        # 车型 车号新增页面

        if select_fault == '交集':
            driver.find_element_by_xpath('//*[contains(text(),\'{}\')]'.format('是否根据车型选择')).click()
        elif select_fault == '并集':
            pass

        time.sleep(1)
        car_status = deal_car(driver, car, 0,1)
        if car_status is True:
            log_file_out('选车成功')
        else:
            log_file_out('选车失败')
            return

        driver.find_element_by_xpath('//*[text()=\'{}\']'.format('下一步')).click()
        time.sleep(5)

        if select_fault == '交集':
            fault_status = deal_occur(driver, fault, value)
        else:
            fault_status = deal_union(driver, fault)
        if fault_status is True:
            log_file_out('选择部件成功')
        else:
            log_file_out('选择部件失败')

        try:
            driver.find_elements_by_xpath('//span[text()="确定"]')[1].click()
        except NoSuchElementException as e:
            logger.error('xpath' + '不存在!')
            log_file_out('点击确定按钮失败')
        except:
            log_file_out('请录入完整的模型')
            return

        time.sleep(2)
        # 点击计算按钮
        try:
            # 移动滚动条到计算按钮
            target = driver.find_element_by_class_name('ivu-btn-info')
            driver.execute_script("arguments[0].scrollIntoView();", target)
            Method(driver).click('class','ivu-btn-info')
            log_file_out('点击计算按钮成功')
        except:
            log_file_out('点击计算按钮失败')

        time.sleep(wait_time)
        try:
            # 设置图表保存目录为bin下面picture下面的rams_cal_picture 图片中路径要为"\\"
            wholepath = os.path.dirname(__file__)  + '\\' + 'picture'+'\\rams_cal_picture'
            # 判断目录是否存在
            if os.path.isdir(wholepath) is True:
                pass
            else:
                os.mkdir(wholepath)
            driver.save_screenshot(wholepath + '\\' + '运用概况' + '.png')
            time.sleep(1)
            driver.find_element_by_xpath('//span[text()="百万公里故障率"]').click()

            driver.save_screenshot(wholepath + '/bin/picture'+ '\\' + '百万公里故障率' + '.png')
            time.sleep(1)
            driver.find_element_by_xpath('//span[text()="平均修复时间"]').click()

            driver.save_screenshot(wholepath + '\\' + '平均修复时间' + '.png')
            time.sleep(1)
            driver.find_element_by_xpath('//span[text()="平均故障间隔里程"]').click()

            driver.save_screenshot(wholepath + '\\' + '平均故障间隔里程' + '.png')
            time.sleep(1)
            driver.find_element_by_xpath('//span[text()="可靠性指标值与设计值对比"]').click()

            driver.save_screenshot(wholepath + '\\' + '可靠性指标值与设计值对比' + '.png')
            time.sleep(1)
            driver.find_element_by_xpath('//span[text()="可用性指标统计值与设计值对比"]').click()

            driver.save_screenshot(wholepath + '\\' + '可用性指标统计值与设计值对比' + '.png')
            time.sleep(1)
            driver.find_element_by_xpath('//span[text()="可维修性指标统计值与设计值对比"]').click()

            driver.save_screenshot(wholepath + '\\' + '可维修性指标统计值与设计值对比' + '.png')
            time.sleep(1)
            driver.find_element_by_xpath('//span[text()="固有可用度"]').click()

            driver.save_screenshot(wholepath + '\\' + '固有可用度' + '.png')
            # 点击单一模型指标分析
            driver.find_element_by_xpath('//div[contains(text(),"单一模型指标分析")]').click()
            time.sleep(1)

            driver.save_screenshot(wholepath + '\\' + '最大最小百万公里故障率' + '.png')
            time.sleep(1)
        except:
            log_file_out('请输入正确的模型')
            return
        # 验证关闭页签 车号页面是否会保存上次车号信息
        # 点击关闭按钮
        try:
            Method(driver).click('xpath','//span[text()="关闭"]')
            time.sleep(1)
            log_file_out('点击关闭按钮成功')
        except Exception as e:
            logger.error(e)
            log_file_out('点击关闭按钮失败')
        # 关闭页签
        try:
            Method(driver).click('class','ivu-icon-ios-close')
            time.sleep(1)
            log_file_out('点击关闭页签按钮成功')
        except Exception as e:
            logger.error(e)
            log_file_out('点击关闭页签按钮失败')

        # 再打开功能页面
        for i in contents:
            try:
                Method(driver).contains_xpath('click', i)
                time.sleep(1)
                log_file_out('点击' + i + '成功')
            except Exception as e:
                logger.debug(e)
                log_file_out('点击' + i + '失败')
        # 选择评估对象
        try:
            Method(driver).click('class', 'ivu-select-placeholder')
            if value == 1:
                driver.find_elements_by_class_name('ivu-select-item')[0].click()
            elif value == 2:
                driver.find_elements_by_class_name('ivu-select-item')[1].click()
            log_file_out('选择评估对象成功')
        except Exception as e:
            logger.error(e)
            log_file_out('选择评估对象失败')
        time.sleep(1)
        try:
            Method(driver).contains_xpath('click', '新增')
        except NoSuchElementException as e:
            logger.debug('点击新建按钮失败')
            logger.error(e)
        time.sleep(2)
        if len(driver.find_elements_by_class_name('ivu-tag-color-white')) == 0:
            log_file_out('关闭可靠性快速计算,重新打开,选车界面不会显示上次计算所选列车信息,验证成功')
        else:
            log_file_out('关闭可靠性快速计算,重新打开,选车界面会显示上次计算所选列车信息,验证失败')
    driver.close()

# femca保存及图片保存
def fmcea_add_check(url,username,password,contents,modelName,remarks,select,start,end,car,fault,select_fault,check_fault,wait_time):
    # option = webdriver.ChromeOptions()
    # option.add_argument("headless")
    # driver = webdriver.Chrome(chrome_options=option,                                                                executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    status = new_built(driver, url, username, password, contents,1)
    if status is True:
        log_file_out('登录成功')
        time.sleep(2)

        Method(driver).input('xpath', "//input[@placeholder='请输入模型名称']", modelName)
        time.sleep(1)

        if remarks is '':
            pass
        else:
            Method(driver).input('xpath', "//input[@placeholder='请输入备注信息']", remarks)
        time.sleep(1)
        if select == '里程':
            try:
                driver.find_elements_by_class_name('ivu-input-default')[4].send_keys(start)
                driver.find_elements_by_class_name('ivu-input-default')[5].send_keys(end)
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
            driver.find_elements_by_class_name('ivu-btn-info')[3].click()
            log_file_out('点击保存按钮成功')
        except NoSuchElementException as e:
            logger.error(e)
            log_file_out('点击保存按钮失败')
        except:
            log_file_out('点击保存按钮失败')

        try:
            WebDriverWait(driver, 3).until(EC.presence_of_element_located(
                (By.CLASS_NAME, "ivu-message-notice")))
            a2 = driver.find_element_by_class_name("ivu-message-notice").text
        except:
            a2 = ''

        try:
            driver.find_element_by_xpath('//a[text()=\'{}\']'.format(modelName))
        except Exception as e:
            log_file_out('保存失败')
            return

        if a2 == '':
            try:
                a = len(driver.find_elements_by_xpath('//a[text()=\'{}\']/../../../td[5]/div/a[2]'.format(modelName)))
                for i in range(0, a):
                    try:
                        driver.find_elements_by_xpath(
                            '//a[text()=\'{}\']/../../../td[5]/div/a[2]'.format(modelName))[i].click()
                        ## 获取点击评估的时间
                        time_now = datetime.datetime.now().replace(microsecond=0)
                        break
                    except:
                        pass
                log_file_out('点击评估按钮成功')
            except WebDriverException:
                log_file_out('点击评估按钮失败')
                return
            time.sleep(2)
            # 获取页面中评估的时间
            click_assess_time = driver.find_element_by_xpath(
                '//a[text()=\'{}\']/../../../td[3]/div'.format(modelName)).text
            if int(click_assess_time.split(':')[0][-2:]) >= 24:
                click_assess_time = click_assess_time.split(' ')[0] + ' ' + '0' + str(
                    int(click_assess_time.split(':')[0][-2:]) - 24) + ':' + \
                                    click_assess_time.split(':')[1] + ':' + click_assess_time.split(':')[2]
            else:
                pass
            click_assess_time1 = datetime.datetime.strptime(click_assess_time, "%Y-%m-%d %H:%M:%S")
            if (click_assess_time1 - time_now).seconds < 30:
                log_file_out('评估时间与实际时间相符,验证成功')
            else:
                log_file_out('评估时间与实际时间不相符,验证失败')

            try:
                a = WebDriverWait(driver, wait_time).until(
                    EC.text_to_be_present_in_element(
                        (By.XPATH, "//a[text()=\'{}\']/../../../td[2]/div".format(modelName)),
                        u'计算完成'))
                if a is True:
                    logger.debug('评估成功')
                    try:
                        a = len(driver.find_elements_by_xpath(
                            '//a[text()=\'{}\']/../../../td[5]/div/a[3]'.format(modelName)))
                        for i in range(0, a):
                            try:
                                driver.find_elements_by_xpath(
                                    '//a[text()=\'{}\']/../../../td[5]/div/a[3]'.format(modelName))[i].click()
                                break
                            except:
                                pass
                        log_file_out('点击图表按钮成功')

                        try:
                            time.sleep(2)
                            if '.csv' not in driver.find_element_by_class_name('ivu-btn-success').find_element_by_tag_name('span').text:
                                log_file_out('导出按钮中不包含csv字样,验证成功')
                            else:
                                log_file_out('导出按钮中包含csv字样,验证失败')
                            # 设置图表保存目录为bin下面picture下面的incontrol_picture 图片中路径要为"\\"
                            wholepath = os.path.dirname(__file__) + '\\' + 'picture' + '\\femca_picture'
                            # 判断目录是否存在
                            if os.path.isdir(wholepath) is True:
                                pass
                            else:
                                os.mkdir(wholepath)

                            driver.save_screenshot(wholepath + '\\' + 'FMECA分析列表' + '.png')
                            return
                        except:
                            log_file_out('截图失败')
                    except WebDriverException:
                        log_file_out('点击图表按钮失败')
                        return
                    # 查看点击图表出来的页面是否存在
            except Exception as e:
                log_file_out('评估失败')
                logger.debug('评估失败')
    driver.close()

# nhpp图表
def nhpp_add_chekc(url,username,password,contents,modelName):
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    status = new_built(driver, url, username, password, contents, 2)
    if status is True:
        log_file_out('登录成功')
        time.sleep(2)
        time.sleep(2)

        a = len(driver.find_elements_by_xpath('//a[text()="{}"]'.format(modelName)))

        for i in range(0, a):
            try:
                driver.find_elements_by_xpath('//a[text()="{}"]/../../../td[6]/div/a[3]'.format(modelName))[i].click()
                time.sleep(1)
            except:
                pass

        time.sleep(2)
        try:
            driver.find_element_by_xpath('//span[text()="关闭"]')
            # 设置图表保存目录为bin下面picture下面的nhpp_picture 图片中路径要为"\\"
            wholepath = os.path.dirname(__file__) + '\\' + 'picture' + '\\nhpp_picture'
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
    driver.close()


# Rcma计算以及图片
def rcma_add_check(url,username,password,contents,modelName,modelCode,remarks,beta,eta,target_failure_rate, percentage,timeRange):
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    status = new_built(driver, url, username, password, contents,1)
    if status is True:
        log_file_out('登录成功')
        time.sleep(2)
        try:
            driver.find_elements_by_class_name('ivu-input-default')[3].send_keys(modelName)
            time.sleep(0.5)
            driver.find_elements_by_class_name('ivu-input-default')[4].send_keys(modelCode)
            time.sleep(0.5)

            if remarks == '':
                time.sleep(1)
            else:
                driver.find_elements_by_class_name('ivu-input-default')[5].send_keys(remarks)
            log_file_out('模型基本信息录入成功')
        except NoSuchElementException as e:
            log_file_out('模型基本信息录入失败')

        # 输入目标βη 目标失效率 百分比 里程范围
        try:
            driver.find_elements_by_class_name('ivu-input-default')[6].send_keys(beta)
            time.sleep(0.5)
            driver.find_elements_by_class_name('ivu-input-default')[7].send_keys(eta)
            time.sleep(0.5)


            driver.find_elements_by_class_name('ivu-input-default')[8].send_keys(target_of_evaluation)
            time.sleep(0.5)

            driver.find_elements_by_class_name('ivu-input-default')[9].send_keys(percentage)
            time.sleep(0.5)

            driver.find_elements_by_class_name('ivu-input-default')[10].send_keys(timeRange)
            log_file_out('基本条件录入成功')
        except NoSuchElementException as e:
            log_file_out('基本条件录入失败')

        # 点击计算
        try:
            driver.find_elements_by_class_name('ivu-btn-info')[-2].click()
            log_file_out('点击计算按钮成功')
        except Exception as e:
            logger.error(e)
            log_file_out('点击计算按钮失败')

        # 点击保存按钮
        try:
            driver.find_elements_by_class_name('ivu-btn-info')[-1].click()
            log_file_out('点击保存按钮成功')
        except Exception as e:
            logger.error(e)
            log_file_out('点击保存按钮失败')

        try:
            WebDriverWait(driver, 3).until(EC.presence_of_element_located(
                (By.CLASS_NAME, "ivu-message-notice")))
            a2 = driver.find_element_by_class_name("ivu-message-notice").text
        except:
            a2 = ''
        if a2 == '':

            try:
                driver.find_element_by_xpath('//a[text()=\'{}\']'.format(modelName))
            except Exception as e:
                logger.error(e)
                log_file_out('保存失败')
                return


            a = len(driver.find_elements_by_xpath('//a[text()="{}"]/../../../td[4]/div/a[2]'.format(modelName)))
            for i in range(0, a):
                try:
                    driver.find_elements_by_xpath('//a[text()="{}"]/../../../td[4]/div/a[2]'.format(modelName))[i].click()
                except:
                    pass
            try:
                # 设置图表保存目录为bin下面picture下面的incontrol_picture 图片中路径要为"\\"
                wholepath = os.path.dirname(__file__) + '\\' + 'picture' + '\\rcma_picture'
                # 判断目录是否存在
                if os.path.isdir(wholepath) is True:
                    pass
                else:
                    os.mkdir(wholepath)

                time.sleep(1)
                target = driver.find_elements_by_class_name('chartParatDom')[0]
                driver.execute_script("arguments[0].scrollIntoView();", target)
                driver.save_screenshot(wholepath + '\\' + '失效率' + '.png')
                time.sleep(1)
                target = driver.find_elements_by_class_name('chartParatDom')[1]
                driver.execute_script("arguments[0].scrollIntoView();", target)
                driver.save_screenshot(wholepath + '\\' + '可靠度' + '.png')
                time.sleep(1)
                target = driver.find_elements_by_class_name('chartParatDom')[2]
                driver.execute_script("arguments[0].scrollIntoView();", target)
                driver.save_screenshot(wholepath + '\\' + '故障概率' + '.png')
                time.sleep(1)
                target = driver.find_elements_by_class_name('chartParatDom')[3]
                driver.execute_script("arguments[0].scrollIntoView();", target)
                driver.save_screenshot(wholepath + '\\' + '概率密度' + '.png')
            except:
                log_file_out('图表保存失败')
                return
        else:
            log_file_out(a2)

# RAMS指标建模新增
def rams_add_check(url,username,password,contents,modelName,value,remarks,select,start,end,speed,check_car,car,fault,select_fault,check_fault,wait_time):
    driver = webdriver.Chrome()
    status = new_built(driver,url,username,password,contents,1)
    if status is True:
        log_file_out('登录成功')
        time.sleep(2)
        # 录入模型信息
        try:
            Method(driver).input('xpath', "//input[@placeholder='请输入模型名称']", modelName)
            time.sleep(1)
            Method(driver).click('xpath', '//span[text()="请输入评估对象"]')
            time.sleep(1)
            if value == 1:
                driver.find_elements_by_xpath('//li[text()="评估系统、部件"]')[1].click()
            elif value == 2:
                driver.find_elements_by_xpath('//li[text()="故障模式"]')[1].click()

            if remarks == '':
                time.sleep(1)
            else:
                driver.find_elements_by_class_name('ivu-input-default')[3].send_keys(remarks)
            if remarks is '':
                pass
            else:
                Method(driver).input('xpath', "//input[@placeholder='请输入备注信息']",
                                     remarks)
            log_file_out('录入模型基本信息成功')
        except NoSuchElementException as e:
            logger.debug('录入模型基本信息失败')
            logger.error(e)

        # 里程
        if select == '里程':
            try:
                driver.find_elements_by_class_name('ivu-input-default')[4].send_keys(start)
                time.sleep(0.5)
                driver.find_elements_by_class_name('ivu-input-default')[5].send_keys(end)
                time.sleep(0.5)
                # 选择平均时速
                driver.find_elements_by_class_name('ivu-select-arrow')[5].click()
                time.sleep(0.5)
                if speed == 1:
                    driver.find_element_by_xpath('//li[text()="180"]').click()
                elif speed == 2:
                    driver.find_element_by_xpath('//li[text()="260"]').click()
                log_file_out('里程录入成功')
            except NoSuchElementException as e:
                logger.error(e)
                log_file_out('里程录入失败')
        elif select == '时间':
            try:
                Method(driver).click('xpath','//a[text()="起始日期"]')
                time.sleep(1)
                Method(driver).input('xpath', "//input[@placeholder='请输入开始日期']",start)
                time.sleep(0.5)
                Method(driver).input('xpath', "//input[@placeholder='请输入结束日期']", end)
                time.sleep(0.5)
                # 平均时速选择框
                Method(driver).click('xpath','//span[text()="请选择"]')
                time.sleep(0.5)
                if speed == 1:
                    driver.find_elements_by_xpath('//li[text()="180"]')[1].click()
                elif speed == 2:
                    driver.find_elements_by_xpath('//li[text()="260"]')[1].click()
                log_file_out('添加时间成功')
            except NoSuchElementException as e:
                logger.error(e)
                log_file_out('添加时间失败')

        time.sleep(2)

        # 验证搜索框 查看没有得数据是否会查出来车号
        driver.find_elements_by_class_name('ivu-input-default')[10].send_keys('7')
        time.sleep(1)
        # 点击查询按钮
        driver.find_elements_by_xpath('//span[text()="查询"]')[1].click()
        time.sleep(1)
        if len(driver.find_elements_by_class_name('type-tag')) == 0:
            log_file_out('按照车号选择结果,无车号信息的车型不会展示在页面,验证成功')
        else:
            log_file_out('按照车号选择结果,无车号信息的车型会展示在页面,验证失败')
        # 点击取消按钮
        time.sleep(1)
        Method(driver).click('xpath','//span[text()="取消"]')

        # 验证查询之后查询结果是否正确 以及查询之后 范围内车号有没有全选
        driver.find_element_by_xpath(
            "//span[@class='train zoomIn' and contains(text(),\'{}\')]".format(check_car[0])).click()
        # 输入值查询
        time.sleep(2)
        driver.find_elements_by_class_name('ivu-input-default')[13].send_keys(check_car[1])
        time.sleep(1)
        driver.find_elements_by_class_name('ivu-input-default')[14].send_keys(check_car[2])
        # 点击查询
        driver.find_elements_by_xpath('//span[text()="查询"]')[2].click()
        time.sleep(1)
        # 获得所有选中的车列表
        try:
            chick_car_list = driver.find_elements_by_class_name('ivu-tag-color-white')
            for i in chick_car_list:
                if int(i.text) <= int(check_car[2]) and int(i.text) >= int(check_car[1]):
                    pass
                else:
                    log_file_out('点击查询按钮之后,需要默认全选筛选后的车,验证失败')
            log_file_out('点击查询按钮之后,需要默认全选筛选后的车,验证成功')
        except Exception as e:
            logger.error(e)
            log_file_out('点击查询按钮之后,需要默认全选筛选后的车,验证失败')
        # 验证重置之后 查询结果是否正确
        time.sleep(1)
        driver.find_elements_by_xpath('//span[text()="重置"]')[1].click()
        time.sleep(1)
        driver.find_elements_by_class_name('ivu-input-default')[13].send_keys(check_car[1])
        time.sleep(1)
        driver.find_elements_by_class_name('ivu-input-default')[14].send_keys(check_car[2])
        # 点击查询
        driver.find_elements_by_xpath('//span[text()="查询"]')[2].click()
        time.sleep(1)
        # 获得所有选中的车列表
        try:
            chick_car_list = driver.find_elements_by_class_name('ivu-tag-color-white')
            for i in chick_car_list:
                if int(i.text) <= int(check_car[2]) and int(i.text) >= int(check_car[1]):
                    pass
                else:
                    log_file_out('重置之后,再查询,查询之后查询结果默认全选,验证失败')
            log_file_out('重置之后,再查询,查询之后查询结果默认全选,验证成功')
        except Exception as e:
            logger.error(e)
            log_file_out('重置之后,再查询,查询之后查询结果默认全选,验证失败')

        # 点击取消按钮
        time.sleep(1)
        Method(driver).click('xpath', '//span[text()="取消"]')

        # 车型 车号新增页面
        if select_fault == '交集':
            driver.find_element_by_xpath('//*[contains(text(),\'{}\')]'.format('是否根据车型选择')).click()
        elif select_fault == '并集':
            pass

        time.sleep(1)
        car_status = deal_car(driver, car, 1 ,1)
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
        fault_select_status = check_fault_select(driver,check_fault)
        if fault_select_status is True:
            log_file_out('部件搜索框验证成功')
        else:
            log_file_out('部件搜索框验证失败')
        # 点击重置
        time.sleep(1)
        Method(driver).click('xpath', '//a[text()="重置"]')
        time.sleep(2)
        if select_fault == '交集':
            fault_status = deal_occur(driver, fault, value)
        else:
            fault_status = deal_union(driver, fault)
        if fault_status is True:
            log_file_out('选择部件成功')
        else:
            log_file_out('选择部件失败')

        try:
            driver.find_element_by_xpath('//span[text()="保存"]').click()
            logger.debug('bug不存在')
        except NoSuchElementException as e:
            logger.error('xpath' + '不存在!')
        except:
            log_file_out('模型录入错误')

        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                (By.CLASS_NAME, "ivu-message-notice")))
            a = driver.find_element_by_class_name("ivu-message-notice").text
        except:
            a = ''

        if a == '':
           pass
        else:
            if select == '里程':
                if a == '结束里程必须大于开始里程':
                    log_file_out('里程输入框结束里程必须大于开始里程验证成功')
                else:
                    log_file_out('里程输入框结束里程必须大于开始里程验证失败')
                driver.find_elements_by_class_name('ivu-input-default')[4].send_keys(Keys.CONTROL, 'a')
                driver.find_elements_by_class_name('ivu-input-default')[4].send_keys(Keys.BACK_SPACE)
                time.sleep(0.5)
                driver.find_elements_by_class_name('ivu-input-default')[4].send_keys('100')
                time.sleep(1)
                driver.find_elements_by_class_name('ivu-input-default')[5].send_keys(Keys.CONTROL, 'a')
                driver.find_elements_by_class_name('ivu-input-default')[5].send_keys(Keys.BACK_SPACE)
                time.sleep(0.5)
                driver.find_elements_by_class_name('ivu-input-default')[5].send_keys('0')
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
                    driver.find_elements_by_class_name('ivu-input-default')[4].send_keys(Keys.CONTROL, 'a')
                    driver.find_elements_by_class_name('ivu-input-default')[4].send_keys(Keys.BACK_SPACE)
                    time.sleep(0.5)
                    driver.find_elements_by_class_name('ivu-input-default')[4].send_keys('0')
                    time.sleep(1)
                    driver.find_elements_by_class_name('ivu-input-default')[5].send_keys(Keys.CONTROL, 'a')
                    driver.find_elements_by_class_name('ivu-input-default')[5].send_keys(Keys.BACK_SPACE)
                    time.sleep(0.5)
                    driver.find_elements_by_class_name('ivu-input-default')[5].send_keys('100')
                    try:
                        driver.find_element_by_xpath('//span[text()="保存"]').click()
                    except NoSuchElementException as e:
                        logger.error('xpath' + '不存在!')
                    except:
                        log_file_out('模型录入错误')

        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                (By.CLASS_NAME, "ivu-message-notice")))
            a2 = driver.find_element_by_class_name("ivu-message-notice").text
        except:
            a2 = ''
        time.sleep(2)
        if a2 == '':
            try:
                a = len(driver.find_elements_by_xpath('//a[text()=\'{}\']/../../../td[7]/div/a[4]'.format(modelName)))
                for i in range(0, a):
                    try:
                        driver.find_elements_by_xpath('//a[text()=\'{}\']/../../../td[7]/div/a[4]'.format(modelName))[
                            i].click()
                        ## 获取点击评估的时间
                        time_now = datetime.datetime.now().replace(microsecond=0)
                        break
                    except:
                        pass
                log_file_out('点击评估按钮成功')
            except WebDriverException:
                log_file_out('点击评估按钮失败')
                return
            # 获取页面中评估的时间
            click_assess_time = driver.find_element_by_xpath('//a[text()=\'{}\']/../../../td[5]/div'.format(modelName)).text
            click_assess_time1 = datetime.datetime.strptime(click_assess_time,"%Y-%m-%d %H:%M:%S")
            if (click_assess_time1 - time_now).seconds < 30:
                log_file_out('评估时间与实际时间相符,验证成功')
            else:
                log_file_out('评估时间与实际时间不相符,验证失败')

            try:
                a = WebDriverWait(driver, wait_time).until(
                    EC.text_to_be_present_in_element(
                        (By.XPATH, "//a[text()=\'{}\']/../../td[3]/div".format(modelName)),
                        u'计算完成'))
                if a is True:
                    logger.debug('评估成功')

                    try:
                        a = len(driver.find_elements_by_xpath(
                            '//a[text()=\'{}\']/../../../td[7]/div/a[5]'.format(modelName)))
                        for i in range(0, a):
                            try:
                                driver.find_elements_by_xpath( '//a[text()=\'{}\']/../../../td[7]/div/a[5]'.format(modelName))[i].click()
                                break
                            except:
                                pass
                        log_file_out('点击图表按钮成功')
                    except WebDriverException:
                        log_file_out('点击图表按钮失败')
                        return

                    # 查看点击图表出来的页面是否存在

            except Exception as e:
                logger.debug('评估失败')
    else:
        log_file_out(contents[1]+'模型新增失败')

# RAMS指标追踪
def rams_index_tracking(url,username,password,contents,modelName):
    driver = webdriver.Chrome()
    status = new_built(driver, url, username, password, contents, 2)
    if status is True:
        log_file_out('登录成功')
        time.sleep(2)
        driver.find_element_by_xpath(
            '//*[@id="right_content"]/div/div/div/div/section/div[1]/div/div[4]/div[2]/table/tbody/tr[1]/td[1]/div/a').click()
        try:
            WebDriverWait(driver, 3).until(EC.presence_of_element_located(
                (By.CLASS_NAME, "ivu-message-notice")))
            a2 = driver.find_element_by_class_name("ivu-message-notice").text
        except:
            a2 = ''
        if a2 != '':
            log_file_out(a2)
        else:
            log_file_out('点击模型 不会出现查询结果为null')
        # 点击取消
        driver.find_elements_by_class_name("ivu-btn-default")[3].click()
        time.sleep(2)
        # 点击确定
        driver.find_element_by_class_name("ivu-btn-primary").click()
        # 点击发布
        driver.find_element_by_xpath('//*[@id="right_content"]/div/div/div/div/section/div[1]/div/div[5]/div[2]/table/tbody/tr[1]/td[31]/div/span/a').click()

        try:
            WebDriverWait(driver, 3).until(EC.presence_of_element_located(
                (By.CLASS_NAME, "ivu-message-notice")))
            a2 = driver.find_element_by_class_name("ivu-message-notice").text
        except:
            a2 = ''
        if a2 == '成功':
            log_file_out('点击发布成功')
        else:
            if a2 == '关联模型评估失败，请重新创建追踪记录':
                log_file_out('发布报错，页面提示关联模型评估失败，请重新创建追踪记录')
            else:
                log_file_out('发布报错，页面未提示关联模型评估失败，请重新创建追踪记录')



# 自定义选车保存 前端页面实时刷新
def custom_car_add_check(url,username,password,contents,carname,car):
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    status = new_built(driver, url, username, password, contents,1)
    if status is True:
        log_file_out('登录成功')
        time.sleep(2)

        car_status = deal_car(driver, car, 0,1)
        if car_status is True:
            log_file_out('选车成功')
        else:
            log_file_out('选车失败')
        time.sleep(1)
        driver.find_elements_by_class_name('ivu-input-default')[-1].send_keys(carname)
        try:
            Method(driver).click('xpath', '//*[text()=\'{}\']'.format('保存'))
        except NoSuchElementException as e:
            logger.error('xpath' + '不存在!')
            log_file_out('点击保存按钮失败')
        except:
            log_file_out('请录入正确的车型')

        time.sleep(2)
        try:
            if driver.find_element_by_xpath("//div[text()=\'{}\']".format(carname)).text != '':
                log_file_out('自定义车组实时保存验证成功')
            else:
                log_file_out('自定义车组实时保存验证失败')
        except Exception as e:
            logger.error(e)
            log_file_out('自定义车组实时保存验证失败')

# 平均故障间隔验证
def mtbf_check(url,username,password,contents,gjb_mtbf,test_duration,iec_mtbf,iec_test_duration):
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    status = new_built(driver, url, username, password, contents,2)
    if status is True:
        log_file_out('登录成功')
        time.sleep(2)

        # 输入mtbf
        driver.find_elements_by_class_name('ivu-input-number-input')[0].send_keys(gjb_mtbf)
        time.sleep(0.5)
        driver.find_elements_by_class_name('ivu-input-number-input')[1].send_keys(test_duration)
        # 检查标题
        if driver.find_elements_by_class_name('ivu-table-title')[0].text == '标准型定时试验统计方案':
            log_file_out('GJB899A下面的标题是标准型定时试验统计方案,验证成功')
        else:
            log_file_out('GJB899A下面的标题不是标准型定时试验统计方案,验证失败')

        # 检查mtbf输入值 前端是否会提示报错信息
        driver.find_elements_by_class_name('ivu-btn-default')[0].click()
        time.sleep(1)
        if len(driver.find_elements_by_class_name('ivu-form-item-error-tip')) != 0:
            L = ''
            for i in range(0,len(driver.find_elements_by_class_name('ivu-form-item-error-tip'))):
                L.append(i)
            if 'MTBF不能为空' in L:
                log_file_out('mtbf输入值 前端会提示报错信息,验证失败')
        else:
            log_file_out('mtbf输入值 前端不会提示报错信息,验证成功')

        # 切换页签到IEC-61124
        driver.find_elements_by_class_name('ivu-tabs-tab')[1].click()
        time.sleep(2)
        # 输入mtbf
        driver.find_elements_by_class_name('ivu-input-number-input')[2].send_keys(iec_mtbf)
        time.sleep(0.5)
        driver.find_elements_by_class_name('ivu-input-number-input')[3].send_keys(iec_test_duration)
        # 检查标题
        if '门限值' not in driver.find_elements_by_class_name('ivu-table-header')[2].text.split(' ')[4]:
            log_file_out('标题:试验时间是MTBF目标值的倍数,验证成功')
        else:
            log_file_out('标题:试验时间不是MTBF目标值的倍数,验证失败')

        # 检查mtbf输入值 前端是否会提示报错信息
        driver.find_elements_by_class_name('ivu-btn-default')[2].click()
        time.sleep(1)
        if len(driver.find_elements_by_class_name('ivu-form-item-error-tip')) != 0:
            L = ''
            for i in range(0, len(driver.find_elements_by_class_name('ivu-form-item-error-tip'))):
                L.append(i)
            if 'MTBF不能为空' in L:
                log_file_out('mtbf输入值 前端会提示报错信息,验证失败')
        else:
            log_file_out('mtbf输入值 前端不会提示报错信息,验证成功')

# 平均维修时间验证是否出现nan
def mttr_add_check(modelCode,url,username,password,contents):
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    status = new_built(driver, url, username, password, contents, 2)
    if status is True:
        log_file_out('登录成功')
        time.sleep(2)

        time.sleep(1)
        Method(driver).click('class','ivu-icon-md-add')

        time.sleep(1)
        try:
            driver.find_element_by_xpath("//span[text()=\'{}\']/../../../td".format(modelCode)).click()
            time.sleep(1)
            driver.find_elements_by_class_name('ivu-btn-info')[-2].click()
            log_file_out('工作时间导入成功')
        except Exception as e:
            log_file_out('工作时间导入失败')

        time.sleep(2)
        driver.find_elements_by_class_name('ivu-btn-info')[2].click()
        time.sleep(1)
        try:
            driver.find_element_by_xpath("//span[text()=\'{}\']/../../../td".format(modelCode)).click()
            time.sleep(1)
            driver.find_elements_by_class_name('ivu-btn-info')[-2].click()
            log_file_out('平均时间导入成功')
        except NoSuchElementException as e:
            log_file_out('平均时间导入失败')


        time.sleep(2)
        try:
            driver.find_element_by_xpath('//span[text()="验证"]').click()
            logger.debug('验证成功')
            log_file_out('验证成功')
        except NoSuchElementException as e:
            logger.error(e)
            logger.debug('验证失败')
            log_file_out('验证失败')

        time.sleep(2)
        L = []
        for i in range(0,len(driver.find_elements_by_class_name('ivu-input-default'))):
            L.append(driver.find_elements_by_class_name('ivu-input-default')[i].text)

        if 'nan' in L:
            log_file_out(contents[1] + 'nan与NaN没统一为NaN,验证失败')
        else:
            log_file_out(contents[1] + 'nan与NaN统一为NaN,验证成功')

# 可靠性增长验证
def taaf_add_check(url,username,password,contents):
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    status = new_built(driver, url, username, password, contents, 2)
    if status is True:
        log_file_out('登录成功')
        time.sleep(2)
        # 设置图表保存目录为bin下面picture下面的taaf_picture 图片中路径要为"\\"
        wholepath = os.path.dirname(__file__) + '\\' + 'picture' + '\\taaf_picture'
        # 判断目录是否存在
        if os.path.isdir(wholepath) is True:
            pass
        else:
            os.mkdir(wholepath)
        driver.save_screenshot(wholepath + '\\' + '可靠性增长' + '.png')

        # 验证增长率是否为0.1-0.7 且步长为0.1
        driver.find_elements_by_class_name('ivu-input-number-input')[4].send_keys(Keys.CONTROL, 'a')
        driver.find_elements_by_class_name('ivu-input-number-input')[4].send_keys(Keys.BACK_SPACE)
        time.sleep(0.5)
        driver.find_elements_by_class_name('ivu-input-number-input')[4].send_keys('0.1')
        try:
            for i in range(0,7):
                driver.find_elements_by_class_name('ivu-icon-ios-arrow-up')[-1].click()
            log_file_out('增长率是为0.1-0.6,验证成功')
        except Exception as e:
            log_file_out('增长率不是为0.1-0.7,验证失败')

        # 验证MTBF初始值是否小于MTBF目标值
        driver.find_elements_by_class_name('ivu-input-number-input')[0].send_keys(Keys.CONTROL, 'a')
        driver.find_elements_by_class_name('ivu-input-number-input')[0].send_keys(Keys.BACK_SPACE)
        time.sleep(0.5)
        driver.find_elements_by_class_name('ivu-input-number-input')[0].send_keys('700')
        # 点击计算
        driver.find_elements_by_class_name('ivu-btn-info')[-2].click()
        try:
            WebDriverWait(driver, 3).until(EC.presence_of_element_located(
                (By.CLASS_NAME, "ivu-message-notice")))
            a2 = driver.find_element_by_class_name("ivu-message-notice").text
        except:
            a2 = ''

        if a2 == '可靠性增长初始水平不能高于目标水平':
            log_file_out('可靠性增长初始水平不能高于目标水平验证成功')
        else:
            log_file_out('可靠性增长初始水平不能高于目标水平验证失败')

        # 验证所有t值是否都不等于0
        # 点击重置
        driver.find_elements_by_class_name('ivu-btn-info')[-1].click()
        time.sleep(1)
        driver.find_elements_by_class_name('ivu-input-number-input')[0].send_keys('400')
        # 点击计算
        driver.find_elements_by_class_name('ivu-btn-info')[-2].click()
        time.sleep(2)
        L = []
        for i in range(0,len(driver.find_elements_by_class_name('ivu-table-row'))):
            L.append(driver.find_elements_by_class_name('ivu-table-row')[i].text.split('\n')[0])

        if '0' in L:
            log_file_out('t中包含0的值,验证失败')
        else:
            log_file_out('t中不包含0的值,验证成功')


# 智能故障分析
def intelligent_fault_analysis_check(url,username,password,contents,start,end,trust_value):
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    status = new_built(driver, url, username, password, contents, 2)
    if status is True:
        log_file_out('登录成功')
        time.sleep(2)
        # 点击更多
        Method(driver).click('class','beta-form-more')
        time.sleep(1)
        driver.find_elements_by_class_name('ivu-input-default')[0].send_keys(start)
        time.sleep(0.5)
        driver.find_elements_by_class_name('ivu-input-default')[1].send_keys(end)
        time.sleep(0.5)
        driver.find_elements_by_class_name('ivu-input-default')[2].send_keys(trust_value)
        # 点击查询
        Method(driver).click('class','ct-input-group-append')
        time.sleep(3)
        su = driver.find_elements_by_class_name('ivu-page-total')[0].text

        su1 = re.findall(r'\d+', su)
        if int(su1[0]) != 0:
            if int(su1[0]) % 10 == 0:
                if int(su1[0])//10 == len(driver.find_elements_by_class_name('ivu-page-item-active')):
                    log_file_out('故障单数量与分页匹配,验证成功')
                else:
                    log_file_out('故障单数量与分页不匹配,验证失败')
            else:
                if int(su1[0])//10 +1 == len(driver.find_elements_by_class_name('ivu-page-item-active')):
                    log_file_out('故障单数量与分页匹配,验证成功')
                else:
                    log_file_out('故障单数量与分页不匹配,验证失败')

        # 点击重置按钮
        Method(driver).click('xpath','//span[text()="重置"]')
        time.sleep(1)
        # 设置图表保存目录为bin下面picture下面的intelligent_fault_picture 图片中路径要为"\\"
        wholepath = os.path.dirname(__file__) + '\\' + 'picture' + '\\intelligent_fault_picture'
        # 判断目录是否存在
        if os.path.isdir(wholepath) is True:
            pass
        else:
            os.mkdir(wholepath)
        driver.save_screenshot(wholepath + '\\' + '智能故障分析重置' + '.png')

# 智能故障识别
def intelligent_fault_identification_check(url,username,password,contents,cartype,carnum):
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    status = new_built(driver, url, username, password, contents, 2)
    if status is True:
        log_file_out('登录成功')
        time.sleep(2)

        # 点击添加按钮之后出现的窗口可以模糊查询
        Method(driver).click('class','ivu-icon-md-add')
        time.sleep(1)
        driver.find_elements_by_class_name('ivu-input-default')[1].send_keys(cartype)
        # 点击查询
        Method(driver).click('class','ivu-icon-md-search')
        L = []
        for i in range(0,len(driver.find_elements_by_class_name('ivu-table-row'))):
            L.append(driver.find_elements_by_class_name('ivu-table-row')[i].text.split('\n')[0])
        if len(list(set(L))) != 1:
            log_file_out('车型的模糊查询验证失败')
        else:
            log_file_out('车型的模糊查询验证成功')
        # 点击重置
        driver.find_elements_by_class_name('ivu-icon-md-refresh')[0].click()
        time.sleep(1)
        # 验证车号
        driver.find_elements_by_class_name('ivu-input-default')[2].send_keys(carnum)
        # 点击查询
        Method(driver).click('class', 'ivu-icon-md-search')
        time.sleep(1)
        L = []
        for i in range(0, len(driver.find_elements_by_class_name('ivu-table-row'))):
            L.append(driver.find_elements_by_class_name('ivu-table-row')[i].text.split('\n')[1])
        if len(list(set(L))) != 1:
            log_file_out('车号的模糊查询验证失败')
        else:
            log_file_out('车号的模糊查询验证成功')
        # 点击重置
        driver.find_elements_by_class_name('ivu-icon-md-refresh')[0].click()
        time.sleep(1)
        driver.find_elements_by_class_name('ivu-radio-input')[0].click()
        time.sleep(1)
        # 点击确定
        try:
            driver.find_elements_by_class_name('ivu-btn-info')[-2].click()
            log_file_out('点击添加页面确定按钮成功')
        except Exception as e:
            logger.error(e)
            log_file_out('点击添加页面确定按钮失败')

        time.sleep(1)
        # 输入信任值
        try:
            driver.find_elements_by_class_name('ivu-input-default')[0].send_keys('0.2')
            # 输入故障描述
            driver.find_elements_by_class_name('ivu-input')[1].send_keys('灯坏了')
            # 点击识别
            driver.find_elements_by_class_name('allButton_style')[1].click()
            log_file_out('录入信任值和故障描述成功')
        except Exception as e:
            logger.error(e)
            log_file_out('录入信任值和故障描述失败')
        time.sleep(2)
        try:
            # 选择
            driver.find_element_by_xpath('//tr[@class="ivu-table-row"]/td[1]/div').click()
            time.sleep(1)
            # 选中
            driver.find_elements_by_class_name('ivu-icon-ios-arrow-forward')[1].click()
            time.sleep(1)
            driver.find_element_by_xpath('//tr[@class="ivu-table-row"]/td[1]/div').click()
            # 选中
            time.sleep(1)

            driver.find_elements_by_class_name('ivu-icon-ios-arrow-forward')[2].click()
            time.sleep(1)
            driver.find_elements_by_xpath('//tr[@class="ivu-table-row"]/td[1]/div')[1].click()
            time.sleep(1)
            # 点击确定
            driver.find_elements_by_class_name('allButton_style')[-1].click()
            log_file_out('识别结果选择成功')
        except Exception as e:
            logger.error(e)
            log_file_out('识别结果选择成功')
        time.sleep(2)
        # 检验 再点击是否会出现错误结果
        driver.find_element_by_xpath('//tr[@class="ivu-table-row"]/td[1]/div').click()
        time.sleep(1)
        driver.find_elements_by_class_name('allButton_style')[-1].click()
        time.sleep(1)
        try:
            WebDriverWait(driver, 3).until(EC.presence_of_element_located(
                (By.CLASS_NAME, "ivu-message-notice")))
            a2 = driver.find_element_by_class_name("ivu-message-notice").text
        except:
            a2 = ''
        if a2 != '':
            log_file_out('在点击第一栏或第二栏,直接选择确认,不会出现错误结果,验证成功')
        else:
            log_file_out('在点击第一栏或第二栏,直接选择确认.会出现错误结果,验证失败')

        # 点击重置

        driver.find_elements_by_class_name('allButton_style')[2].click()
        time.sleep(1)
        # 设置图表保存目录为bin下面picture下面的intelligent_fault_identification_picture 图片中路径要为"\\"
        wholepath = os.path.dirname(__file__) + '\\' + 'picture' + '\\intelligent_fault_identification_picture'
        # 判断目录是否存在
        if os.path.isdir(wholepath) is True:
            pass
        else:
            os.mkdir(wholepath)
        driver.save_screenshot(wholepath + '\\' + '智能故障识别重置' + '.png')


# 运维数据清洗验证
def operation_maintenance_data_cleaning_chcek(url,username,password,contents):
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    status = new_built(driver, url, username, password, contents,2)
    if status is True:
        log_file_out('登录成功')
        time.sleep(2)


        # 设置图表保存目录为bin下面picture下面的operation_maintenance_data_cleaning_picture 图片中路径要为"\\"
        wholepath = os.path.dirname(__file__) + '\\' + 'picture' + '\\operation_maintenance_data_cleaning_picture'
        # 判断目录是否存在
        if os.path.isdir(wholepath) is True:
            pass
        else:
            os.mkdir(wholepath)
        driver.save_screenshot(wholepath + '\\' + '运维数据清洗' + '.png')

        L = []
        if len(driver.find_elements_by_class_name('el-tree-node__expand-icon')) == 0:
            pass
        else:
            try:
                for i in range(0,len(driver.find_elements_by_xpath('//span[contains(text(),"车型")]'))):
                    driver.find_elements_by_xpath('//span[contains(text(),"车型")]')[i].click()
                    time.sleep(1)

                    for j in range(0, len(driver.find_elements_by_class_name('el-tree-node__label'))):
                        L.append(driver.find_elements_by_class_name('el-tree-node__label')[j].text.split(':')[-1][:-1])

                    time.sleep(1)
                log_file_out('点击车型下拉按钮成功')
            except Exception as e:
                logger.error(e)
                log_file_out('点击车型下拉按钮失败')

            # 得到大于100的数组
            L1 =  [i if i == '' else float(i) >= 100 for i in L]
            if True in L1:
                log_file_out('数据清洗中出现大于100的数据,验证失败')
            else:
                log_file_out('数据清洗中没有出现大于100的数据,验证成功')



# 项目首页
def project_home_model(url,username,password,contents):
    # 设置excel的下载路径为bin目录下的download_excel下的project_home_model
    project_home_model = os.path.dirname(__file__) + '\\' + 'download_excel' + '\\project_home_model'
    if os.path.isdir(project_home_model) is True:
        pass
    else:
        os.mkdir(project_home_model)
    options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_settings.popups': 0,
             'download.default_directory': '{}\\bin\\download_excel\\project_home_model'.format(path_dir1),
             "profile.default_content_setting_values.automatic_downloads": 1}
    options.add_experimental_option('prefs', prefs)

    driver = webdriver.Chrome(chrome_options=options)
    status = new_built(driver, url, username, password, contents,2)
    if status is True:
        log_file_out('--项目首页--')
        log_file_out('登录成功')
        time.sleep(2)
        #

        # 依次查看每个模型的预览
        for i in range(0,len(driver.find_elements_by_xpath('//div[@class="grid-items-title"]'))):
            # 下载的excel的名称
            text_name = driver.find_elements_by_xpath('//div[@class="grid-items-title"]/div')[i].text
            try:
                # 点击预览查看信息是否存在
                driver.find_elements_by_xpath('//div[@class="grid-items-title"]/div[1]/div[1]')[i].click()
                # 查看模型是否需要选择车型车号
                if len(driver.find_elements_by_class_name('power-preTrain-typeCode')) == 0:
                    pass
                else:
                    # 点击车号下拉按钮
                    time.sleep(2)
                    driver.find_element_by_xpath('//p[@class="power-preTrain-typeCode"]/span/i').click()
                    time.sleep(1)
                    # 车型车号
                    car_text = driver.find_element_by_class_name('power-preTrain-trainNo-row').text
                    if car_text != '':
                        log_file_out(text_name+'车号不为空,验证成功')
                    else:
                        log_file_out(text_name + '车号为空,验证失败')
                # 判断是否有部件
                if len(driver.find_elements_by_class_name('power-preFault-col')) == 0:
                    pass
                else:
                    # 部件信息
                    fault_text = driver.find_element_by_class_name('power-preFault-col').text
                    if fault_text != '':
                        log_file_out(text_name + '部件不为空,验证成功')
                    else:
                        log_file_out(text_name + '部件为空,验证失败')
                # 点击关闭
                Method(driver).click('class','power-btn-sub')
            except Exception as e:
                logger.error(e)
                log_file_out('模型预览条件失败')
            try:
                # 判断excel是否存在
                if os.path.exists('{}\\bin\\download_excel\\project_home_model'.format(path_dir1) + '\\' + '{}.xlsx'.format(text_name)):
                    os.remove(
                        '{}\\bin\\download_excel\\project_home_model'.format(path_dir1) + '\\' + '{}.xlsx'.format(text_name))
                else:
                    pass
                # 点击下载
                driver.find_elements_by_xpath('//div[@class="grid-items-title"]/div[1]/div[2]')[i].click()
                time.sleep(2)

                if os.path.exists('{}\\bin\\download_excel\\project_home_model'.format(path_dir1) + '\\' + '{}.xlsx'.format(text_name)):
                    log_file_out('下载成功,验证成功')
                else:
                    log_file_out('下载失败,验证失败')
            except Exception as e:
                logger.error(e)
                log_file_out(text_name+'excel下载失败')

            try:
                # 点击更多查看图表
                driver.find_elements_by_class_name('gridItems-more')[i].click()

                # 截图,图表的class从第几个开始
                time.sleep(2)
                # 设置图表下载路径为picture下面的workshop下
                project_home_model_picture_path = os.path.dirname(__file__) + '\\' + 'picture' + '\\project_home_model' + '\\' + text_name
                if os.path.isdir(project_home_model_picture_path) is True:
                    pass
                else:
                    os.mkdir(project_home_model_picture_path)

                class_index = len(driver.find_elements_by_xpath('//div[@class="grid-items-title"]'))
                for i in range(class_index ,len(driver.find_elements_by_class_name('chartParatDom'))):
                    driver.find_elements_by_class_name('chartParatDom')[i].click()
                    time.sleep(1)
                    driver.save_screenshot(project_home_model_picture_path + '\\' + text_name + '_' + str(i-class_index) + '.png')

                # 点击关闭
                Method(driver).click('xpath', '//span[text()="关闭"]')
                time.sleep(1)
            except Exception as e:
                logger.error(e)
                log_file_out(text_name+'查看更多失败')




















