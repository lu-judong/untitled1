from random import randint

from config.config import *

# 内控模型新增及图片保存
def incontrol_add_check(url,username,password,contents,modelName,start,end,remarks,car,wait_time):
    # option = webdriver.ChromeOptions()
    # option.add_argument("headless")
    # driver = webdriver.Chrome(chrome_options=option,                                                                executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    log_file_out('-----' + contents[1] + '保存验证' + '-----')
    status = new_built(driver, url, username, password, contents,1)
    try:
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
                error_message = driver.find_element_by_class_name("ivu-message-notice").text
            except:
                error_message = ''

            if error_message == '':
                try:
                    driver.find_element_by_xpath('//a[text()=\'{}\']'.format(modelName))
                except Exception as e:
                    log_file_out('保存失败')
                    return

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
            else:
                log_file_out(error_message)
                return
        driver.close()
    except:
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
    log_file_out('-----' + contents[1] + '保存验证' + '-----')
    status = new_built(driver, url, username, password, contents,1)
    try:
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
                WebDriverWait(driver, 2).until(EC.presence_of_element_located(
                    (By.CLASS_NAME, "ivu-message-notice")))
                error_message = driver.find_element_by_class_name("ivu-message-notice").text
            except:
                error_message = ''

            if error_message == '':
                try:
                    driver.find_element_by_xpath('//a[text()=\'{}\']'.format(modelName))
                except Exception as e:
                    log_file_out('保存失败')
                    return

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
                time.sleep(2)
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
                                # 设置图表保存目录为bin下面picture下面的repair_picture 图片中路径要为"\\"
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
                log_file_out(error_message)
                return
        else:
            log_file_out(contents[1] + '模型新增失败')
        driver.close()
    except:
        driver.close

# 技术变更新增以及图表
def technical_change_add_check(url,username,password,contents,modelName,value,remarks,select,tech_change,speed,car,fault,select_fault,wait_time):
    # option = webdriver.ChromeOptions()
    # option.add_argument("headless")
    # driver = webdriver.Chrome(chrome_options=option,                                                                executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')

    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    log_file_out('-----' + contents[1] + '保存验证' + '-----')
    status = new_built(driver, url, username, password, contents,1)
    try:
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
                error_message = driver.find_element_by_class_name("ivu-message-notice").text
            except:
                error_message = ''

            if error_message == '':
                try:
                    driver.find_element_by_xpath('//a[text()=\'{}\']'.format(modelName))
                except Exception as e:
                    log_file_out('保存失败')
                    return

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
                                # 设置图表保存目录为bin下面picture下面的tech_picture 图片中路径要为"\\"
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
                log_file_out(error_message)
                return
        else:
            log_file_out(contents[1] + '模型新增失败')
        driver.close()
    except:
        driver.close()

# 单一模型新增以及图表
def singelmodel_add_check(url,username,password,contents,modelName,value,remarks,select,start,end,speed,car,fault,select_fault,wait_time):
    # option = webdriver.ChromeOptions()
    # option.add_argument("headless")
    # driver = webdriver.Chrome(chrome_options=option,                                                                executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')

    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    log_file_out('-----' + contents[1] + '保存验证' + '-----')
    status = new_built(driver, url, username, password, contents, 1)
    try:
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

            # 优化前里程
            if select == '里程':
                try:
                    driver.find_elements_by_class_name('ivu-input-default')[4].send_keys(start)
                    time.sleep(0.5)
                    driver.find_elements_by_class_name('ivu-input-default')[5].send_keys(end)
                    time.sleep(0.5)
                    driver.find_elements_by_class_name('ivu-select-placeholder')[3].click()
                    time.sleep(0.5)
                    if speed == 1:
                        driver.find_element_by_xpath('//li[text()="180"]').click()
                    elif speed == 2:
                        driver.find_element_by_xpath('//li[text()="260"]').click()
                    log_file_out('里程录入成功')
                except NoSuchElementException as e:
                    log_file_out('里程录入失败')
            elif select == '时间':
                try:
                    Method(driver).input('xpath', "//input[@placeholder='请输入开始日期']", start)
                    time.sleep(0.5)
                    Method(driver).input('xpath', "//input[@placeholder='请输入结束日期']", end)
                    time.sleep(0.5)
                    # 平均时速选择框
                    driver.find_elements_by_class_name('ivu-select-placeholder')[5].click()
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

            # 车型 车号新增页面

            if select_fault == '交集':
                driver.find_element_by_xpath('//*[contains(text(),\'{}\')]'.format('是否根据车型选择')).click()
            elif select_fault == '并集':
                pass

            time.sleep(1)
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
                log_file_out('点击保存按钮成功')
            except NoSuchElementException as e:
                logger.error(e)
            except:
                log_file_out('模型录入错误')

            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                    (By.CLASS_NAME, "ivu-message-notice")))
                error_message = driver.find_element_by_class_name("ivu-message-notice").text
            except:
                error_message = ''

            if error_message == '':
                try:
                    driver.find_element_by_xpath('//a[text()=\'{}\']'.format(modelName))
                except Exception as e:
                    log_file_out('保存失败')
                    return

                try:
                    a = len(driver.find_elements_by_xpath('//a[text()=\'{}\']/../../../td[7]/div/a[3]'.format(modelName)))
                    for i in range(0, a):
                        try:
                            driver.find_elements_by_xpath('//a[text()=\'{}\']/../../../td[7]/div/a[3]'.format(modelName))[
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
                    '//a[text()=\'{}\']/../../../td[5]/div'.format(modelName)).text
                click_assess_time1 = datetime.datetime.strptime(click_assess_time, "%Y-%m-%d %H:%M:%S")
                if (click_assess_time1 - time_now).seconds < 60:
                    log_file_out('评估时间与实际时间相符,验证成功')
                else:
                    log_file_out('评估时间与实际时间不相符,验证失败')



                try:
                    a = WebDriverWait(driver, wait_time).until(
                        EC.text_to_be_present_in_element((By.XPATH, "//a[text()=\'{}\']/../../../td[4]".format(modelName)),
                                                         u'计算完成'))
                    if a is True:
                        logger.debug('评估成功')
                        try:
                            b = len(driver.find_elements_by_xpath('//a[text()=\'{}\']/../../../td[7]/div/a[4]'.format(modelName)))
                            for i in range(0, b):
                                try:
                                    driver.find_elements_by_xpath(
                                        '//a[text()=\'{}\']/../../../td[7]/div/a[4]'.format(modelName))[i].click()
                                    break
                                except:
                                    pass

                            log_file_out('点击图表按钮成功')

                            time.sleep(2)
                            # 设置图表保存目录为bin下面picture下面的singelmodel_picture 图片中路径要为"\\"
                            wholepath = os.path.dirname(__file__) + '\\' + 'picture' + '\\singelmodel_picture'
                            # 判断目录是否存在
                            if os.path.isdir(wholepath) is True:
                                pass
                            else:
                                os.mkdir(wholepath)

                            try:
                                time.sleep(2)

                                driver.save_screenshot(wholepath + '\\' + '最大最小百万公里故障率' + '.png')

                                time.sleep(1)
                                target = driver.find_element_by_class_name('ivu-table-wrapper')
                                driver.execute_script("arguments[0].scrollIntoView();", target)
                                driver.save_screenshot(wholepath + '\\' + '车号指标明细' + '.png')
                                log_file_out('截取单一模型图表成功')
                            except:
                                log_file_out('截取单一模型图表失败')

                        except WebDriverException:
                            log_file_out('点击图表按钮失败')
                            return
                except Exception as e:
                    logger.debug('评估失败')
            else:
                log_file_out(error_message)
                return
        else:
            log_file_out('登录失败')
        driver.close()
    except:
        driver.close()

# RAMS立即计算新增
def rams_cal_check(url, username, password, contents, value, speed,select ,start, end, car, fault, select_fault, wait_time):
    #
    # option = webdriver.ChromeOptions()
    # option.add_argument("headless")
    # driver = webdriver.Chrome(chrome_options=option,
    #                           executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    log_file_out('-----' + contents[1] + '验证' + '-----')
    status = new_built(driver, url, username, password, contents,2)
    try:
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

            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                    (By.CLASS_NAME, "ivu-message-notice")))
                error_message = driver.find_element_by_class_name("ivu-message-notice").text
            except:
                error_message = ''
            if error_message == '':

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
                    log_file_out('截取图表成功')
                except:
                    log_file_out('截取图表失败')
                    return
            else:
                log_file_out(error_message)
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
    except:
        driver.close()

# 指标对比分析新增以及图表
def compare_add_check(url, username, password, contents, modelName, value, remarks, select, min_model, select_fault, wait_time):
    #
    # option = webdriver.ChromeOptions()
    # option.add_argument("headless")
    # driver = webdriver.Chrome(chrome_options=option,
    #                           executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    log_file_out('-----' + contents[1] + '保存验证' + '-----')
    status = new_built(driver, url, username, password, contents, 1)
    try:
        if status is True:
            log_file_out('登录成功')
            time.sleep(2)


            # 对新增指标页面进行操作
            try:
                driver.find_elements_by_class_name('ivu-input-default')[2].send_keys(modelName)
                time.sleep(1)
                driver.find_elements_by_class_name('ivu-select-placeholder')[3].click()
                if value == 1:
                    driver.find_elements_by_xpath('//li[text()="评估系统、部件"]')[1].click()
                elif value == 2:
                    driver.find_elements_by_xpath('//li[text()="故障模式"]')[1].click()

                if remarks == '':
                    time.sleep(1)
                else:
                    driver.find_elements_by_class_name('ivu-input-default')[2].send_keys(remarks)
                log_file_out('模型录入成功')
            except Exception as e:
                logger.debug(e)
                log_file_out('模型录入失败')

            sum1 = 0

            average = 0
            num = 4
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
                    time.sleep(1)

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
                driver.find_element_by_xpath('//span[text()="保存"]').click()
                logger.debug('bug不存在')
            except NoSuchElementException as e:
                logger.error('xpath' + '不存在!')
            except:
                log_file_out('模型录入错误')

            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located(
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
                    driver.find_element_by_xpath('//a[text()=\'{}\']'.format(modelName))
                except Exception as e:
                    log_file_out('保存失败')
                    return

                try:
                    a = len(driver.find_elements_by_xpath('//a[text()=\'{}\']/../../../td[7]/div/a[3]'.format(modelName)))
                    for i in range(0, a):
                        try:
                            driver.find_elements_by_xpath('//a[text()=\'{}\']/../../../td[7]/div/a[3]'.format(modelName))[
                                i].click()
                            break
                        except:
                            time.sleep(0.5)
                            pass
                    log_file_out('点击评估按钮成功')
                except WebDriverException:
                    log_file_out('点击评估按钮失败')
                    return

                try:
                    a = WebDriverWait(driver, wait_time).until(
                        EC.text_to_be_present_in_element((By.XPATH, "//a[text()=\'{}\']/../../../td[4]".format(modelName)),
                                                         u'计算完成'))
                    if a is True:
                        logger.debug('评估成功')
                        try:
                            b = len(
                                driver.find_elements_by_xpath('//a[text()=\'{}\']/../../../td[7]/div/a[4]'.format(modelName)))
                            for i in range(0, b):
                                try:
                                    driver.find_elements_by_xpath(
                                        '//a[text()=\'{}\']/../../../td[7]/div/a[4]'.format(modelName))[i].click()
                                    break
                                except:
                                    time.sleep(0.5)
                                    pass

                            log_file_out('点击图表按钮成功')
                            time.sleep(2)
                            try:
                                # 设置图表保存目录为bin下面picture下面的compare_picture 图片中路径要为"\\"
                                wholepath = os.path.dirname(__file__) + '\\' + 'picture' + '\\compare_picture'
                                # 判断目录是否存在
                                if os.path.isdir(wholepath) is True:
                                    pass
                                else:
                                    os.mkdir(wholepath)
                                driver.save_screenshot(wholepath + '\\' + '百万公里故障率' + '.png')
                                log_file_out('截取图表成功')
                            except:
                                log_file_out('截取图表失败')
                        except WebDriverException:
                            log_file_out('点击图表按钮失败')
                            return
                except Exception as e:
                    logger.error(e)
                    logger.debug('评估失败')
                    log_file_out('评估失败')
        driver.close()
    except:
        driver.close()

# femca保存及图片保存
def fmcea_add_check(url,username,password,contents,modelName,remarks,select,start,end,car,fault,select_fault,check_fault,wait_time):
    # option = webdriver.ChromeOptions()
    # option.add_argument("headless")
    # driver = webdriver.Chrome(chrome_options=option,                                                                executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    log_file_out('-----' + contents[1] + '保存验证' + '-----')
    status = new_built(driver, url, username, password, contents,1)
    try:
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
                error_message = driver.find_element_by_class_name("ivu-message-notice").text
            except:
                error_message = ''

            if error_message == '':
                try:
                    driver.find_element_by_xpath('//a[text()=\'{}\']'.format(modelName))
                except Exception as e:
                    log_file_out('保存失败')
                    return

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
                                # 设置图表保存目录为bin下面picture下面的ifemca_picture 图片中路径要为"\\"
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
            else:
                log_file_out(error_message)
                return
        driver.close()
    except:
        driver.close()

# 故障占比分析
def fault_ratio_add_check(url,username,password,contents,modelName,value,remarks,select,start,end,car,fault,select_fault,check_fault,wait_time):
    # option = webdriver.ChromeOptions()
    # option.add_argument("headless")
    # driver = webdriver.Chrome(chrome_options=option,                                                                executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')

    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    log_file_out('-----' + contents[1] + '保存验证' + '-----')
    status = new_built(driver, url, username, password, contents, 1)
    try:
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

            # 优化前里程
            if select == '里程':
                try:
                    driver.find_elements_by_class_name('ivu-input-default')[4].send_keys(start)
                    time.sleep(0.5)
                    driver.find_elements_by_class_name('ivu-input-default')[5].send_keys(end)
                    time.sleep(0.5)
                    driver.find_elements_by_class_name('ivu-select-placeholder')[3].click()
                    time.sleep(0.5)
                    if speed == 1:
                        driver.find_element_by_xpath('//li[text()="180"]').click()
                    elif speed == 2:
                        driver.find_element_by_xpath('//li[text()="260"]').click()
                    log_file_out('里程录入成功')
                except NoSuchElementException as e:
                    log_file_out('里程录入失败')
            elif select == '时间':
                try:
                    Method(driver).input('xpath', "//input[@placeholder='请输入开始日期']", start)
                    time.sleep(0.5)
                    Method(driver).input('xpath', "//input[@placeholder='请输入结束日期']", end)
                    time.sleep(0.5)
                    # 平均时速选择框
                    driver.find_elements_by_class_name('ivu-select-placeholder')[4].click()
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

            # 车型 车号新增页面

            if select_fault == '交集':
                driver.find_element_by_xpath('//*[contains(text(),\'{}\')]'.format('是否根据车型选择')).click()
            elif select_fault == '并集':
                pass

            time.sleep(1)
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
                log_file_out('点击保存按钮成功')
            except NoSuchElementException as e:
                logger.error(e)
            except:
                log_file_out('模型录入错误')

            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                    (By.CLASS_NAME, "ivu-message-notice")))
                error_message = driver.find_element_by_class_name("ivu-message-notice").text
            except:
                error_message = ''

            if error_message == '':
                try:
                    driver.find_element_by_xpath('//a[text()=\'{}\']'.format(modelName))
                except Exception as e:
                    log_file_out('保存失败')
                    return

                try:
                    a = len(driver.find_elements_by_xpath('//a[text()=\'{}\']/../../../td[6]/div/a[3]'.format(modelName)))
                    for i in range(0, a):
                        try:
                            driver.find_elements_by_xpath('//a[text()=\'{}\']/../../../td[6]/div/a[3]'.format(modelName))[
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
                click_assess_time = driver.find_element_by_xpath('//a[text()=\'{}\']/../../../td[4]/div'.format(modelName)).text
                click_assess_time1 = datetime.datetime.strptime(click_assess_time, "%Y-%m-%d %H:%M:%S")
                if (click_assess_time1 - time_now).seconds < 60:
                    log_file_out('评估时间与实际时间相符,验证成功')
                else:
                    log_file_out('评估时间与实际时间不相符,验证失败')

                try:
                    a = WebDriverWait(driver, wait_time).until(
                        EC.text_to_be_present_in_element((By.XPATH, "//a[text()=\'{}\']/../../../td[3]".format(modelName)),
                                                         u'计算完成'))
                    if a is True:
                        logger.debug('评估成功')
                        try:
                            b = len(driver.find_elements_by_xpath(
                                '//a[text()=\'{}\']/../../../td[6]/div/a[4]'.format(modelName)))
                            for i in range(0, b):
                                try:
                                    driver.find_elements_by_xpath(
                                        '//a[text()=\'{}\']/../../../td[6]/div/a[4]'.format(modelName))[i].click()
                                    break
                                except:
                                    pass

                            log_file_out('点击图表按钮成功')

                            time.sleep(2)
                            # 设置图表保存目录为bin下面picture下面的fault_ratio_picture 图片中路径要为"\\"
                            wholepath = os.path.dirname(__file__) + '\\' + 'picture' + '\\fault_ratio_picture'
                            # 判断目录是否存在
                            if os.path.isdir(wholepath) is True:
                                pass
                            else:
                                os.mkdir(wholepath)

                            try:

                                target = driver.find_elements_by_class_name('chartParatDom')[1]
                                driver.execute_script("arguments[0].scrollIntoView();", target)
                                driver.save_screenshot(wholepath + '\\' + '各路局故障占比' + '.png')
                                time.sleep(1)
                                target = driver.find_elements_by_class_name('chartParatDom')[2]
                                driver.execute_script("arguments[0].scrollIntoView();", target)
                                driver.save_screenshot(wholepath + '\\' + '各责任方故障占比' + '.png')
                                time.sleep(1)
                                target = driver.find_elements_by_class_name('chartParatDom')[3]
                                driver.execute_script("arguments[0].scrollIntoView();", target)
                                driver.save_screenshot(wholepath + '\\' + '故障原因占比' + '.png')
                                time.sleep(1)
                                target = driver.find_elements_by_class_name('chartParatDom')[4]
                                driver.execute_script("arguments[0].scrollIntoView();", target)
                                driver.save_screenshot(wholepath + '\\' + '各故障级别故障占比' + '.png')
                                log_file_out('截取'+contents[1]+'图表成功')
                            except:
                                log_file_out('截取'+contents[1]+'图表失败')

                        except WebDriverException:
                            log_file_out('点击图表按钮失败')
                            return
                except Exception as e:
                    logger.debug('评估失败')
                    log_file_out('评估失败')
            else:
                log_file_out(error_message)
                return
        driver.close()
    except:
        driver.close()

# nhpp图表
def nhpp_add_check(url,username,password,contents,modelName,modelCode,start,end,car):
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    log_file_out('-----' + contents[1] + '保存验证' + '-----')
    status = new_built(driver, url, username, password, contents, 1)
    try:
        if status is True:
            log_file_out('登录成功')
            time.sleep(2)
            # 对新增指标页面进行操作
            try:
                driver.find_elements_by_class_name('ivu-input-default')[3].send_keys(modelName)
                time.sleep(1)
                driver.find_elements_by_class_name('ivu-input-default')[4].send_keys(modelCode)

                log_file_out('模型录入成功')
            except Exception as e:
                logger.debug(e)
                log_file_out('模型录入失败')

            try:
                driver.find_elements_by_class_name('ivu-input-default')[5].send_keys(start)
                time.sleep(0.5)
                driver.find_elements_by_class_name('ivu-input-default')[6].send_keys(end)
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
                driver.find_element_by_xpath('//span[text()="保存"]').click()
            except NoSuchElementException as e:
                logger.error(e)
                log_file_out('保存失败')

            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                    (By.CLASS_NAME, "ivu-message-notice")))
                error_message = driver.find_element_by_class_name("ivu-message-notice").text
            except:
                error_message = ''

            if error_message == '':
                try:
                    driver.find_element_by_xpath('//a[text()=\'{}\']'.format(modelName))
                except Exception as e:
                    log_file_out('保存失败')
                    return

                try:
                    driver.find_element_by_xpath(
                        '//span[text()=\'{}\']/../../../td[1]/div/div/div/button[2]/span'.format(modelName)).click()

                    log_file_out('点击评估按钮成功')
                except WebDriverException:
                    log_file_out('点击评估按钮失败')
                    return

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
            else:
                log_file_out(error_message)
                return
        driver.close()
    except:
        driver.close()

# Rcma计算以及图片
def rcma_add_check(url,username,password,contents,modelName,modelCode,remarks,beta,eta,target_failure_rate, percentage,timeRange):
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    log_file_out('-----' + contents[1] + '保存验证' + '-----')
    status = new_built(driver, url, username, password, contents,1)
    try:
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


                driver.find_elements_by_class_name('ivu-input-default')[8].send_keys(target_failure_rate)
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
                    # 设置图表保存目录为bin下面picture下面的rcma_picture 图片中路径要为"\\"
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
        driver.close()
    except:
        driver.close()

# RAMS指标建模新增
def rams_add_check(url,username,password,contents,modelName,value,remarks,select,start,end,speed,check_car,car,fault,select_fault,check_fault,wait_time):
    driver = webdriver.Chrome()
    log_file_out('-----' + contents[1] + '保存验证' + '-----')
    status = new_built(driver,url,username,password,contents,1)
    try:
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
                log_file_out('点击保存按钮成功')
            except NoSuchElementException as e:
                logger.error(e)
            except:
                log_file_out('模型录入错误')

            try:
                driver.find_element_by_xpath('//a[text()=\'{}\']'.format(modelName))
            except Exception as e:
                log_file_out('保存失败')
                return

            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                    (By.CLASS_NAME, "ivu-message-notice")))
                error_message = driver.find_element_by_class_name("ivu-message-notice").text
            except:
                error_message = ''

            if error_message == '':
               pass
            else:
                if select == '里程':
                    if error_message == '结束里程必须大于开始里程':
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
                error_message = driver.find_element_by_class_name("ivu-message-notice").text
            except:
                error_message = ''

            time.sleep(2)
            if error_message == '':
                try:
                    driver.find_element_by_xpath('//a[text()=\'{}\']'.format(modelName))
                except Exception as e:
                    logger.error(e)
                    log_file_out('保存失败')
                    return

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
                        try:
                            # 设置图表保存目录为bin下面picture下面的rams_save_picture 图片中路径要为"\\"
                            wholepath = os.path.dirname(__file__) + '\\' + 'picture' + '\\rams_save_picture'
                            # 判断目录是否存在
                            if os.path.isdir(wholepath) is True:
                                pass
                            else:
                                os.mkdir(wholepath)
                            driver.save_screenshot(wholepath + '\\' + '百万公里故障率' + '.png')
                            time.sleep(1)
                            driver.find_elements_by_class_name('chartParatDom')[1].click()

                            driver.save_screenshot(wholepath + '/bin/picture' + '\\' + '平均故障间隔里程' + '.png')
                            time.sleep(1)
                            driver.find_elements_by_class_name('chartParatDom')[2].click()

                            driver.save_screenshot(wholepath + '\\' + '平均修复时间' + '.png')
                            time.sleep(1)
                            driver.find_elements_by_class_name('chartParatDom')[3].click()

                            driver.save_screenshot(wholepath + '\\' + '固有可用度' + '.png')
                            log_file_out('截取\'{}\'图表成功'.format(contents[1]))
                        except:
                            log_file_out('截取\'{}\'图表失败'.format(contents[1]))
                            return

                except Exception as e:
                    logger.debug('评估失败')
            else:
                log_file_out(error_message)
                return
        else:
            log_file_out(contents[1]+'模型新增失败')
        driver.close()
    except:
        driver.close()

# RAMS指标追踪
def rams_index_tracking(url,username,password,contents,modelName):
    driver = webdriver.Chrome()
    log_file_out('-----' + contents[1] + '保存验证' + '-----')
    status = new_built(driver, url, username, password, contents, 2)
    try:
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
        driver.close()
    except:
        driver.close()

# 维修性参数评估
def main_parameter_evaluation_check(modelCode,url,username,password,contents):
    # option = webdriver.ChromeOptions()
    # option.add_argument("headless")
    # driver = webdriver.Chrome(chrome_options=option,
    #                           executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')
    driver = webdriver.Chrome()
    log_file_out('-----' + contents[1] + '保存验证' + '-----')
    status = new_built(driver, url, username, password, contents, 2)
    try:
        if status is True:
            log_file_out('登录成功')
            time.sleep(2)


            driver.find_elements_by_xpath('//span[text()="导入"]')[1].click()

            time.sleep(1)
            try:
                driver.find_element_by_xpath("//span[text()=\'{}\']/../../../td".format(modelCode)).click()
                time.sleep(1)
                driver.find_elements_by_xpath('//span[text()="确定"]')[1].click()
                log_file_out('工作时间导入成功')
            except Exception as e:
                log_file_out('工作时间导入失败')

            time.sleep(2)
            driver.find_elements_by_xpath('//span[text()="导入"]')[2].click()
            time.sleep(1)
            try:
                driver.find_elements_by_xpath("//span[text()=\'{}\']/../../../td".format(modelCode))[3].click()
                time.sleep(1)
                driver.find_elements_by_xpath('//span[text()="确定"]')[2].click()
                log_file_out('第二个导入成功')
            except NoSuchElementException as e:
                log_file_out('第二个导入失败')


            try:
                driver.find_elements_by_xpath('//span[text()="计算"]')[0].click()
                logger.debug('第一次计算成功')
                log_file_out('第一次计算成功')
            except NoSuchElementException as e:
                logger.error(e)
                logger.debug('第一次计算失败')
                log_file_out('第一次计算失败')

            driver.find_elements_by_xpath('//span[text()="导入"]')[3].click()
            time.sleep(1)

            try:
                driver.find_elements_by_xpath("//span[text()=\'{}\']/../../../td".format(modelCode))[6].click()
                time.sleep(1)
                driver.find_elements_by_xpath('//span[text()="确定"]')[3].click()
                log_file_out('第三个导入成功')
            except NoSuchElementException as e:
                log_file_out('第三个导入失败')

            try:
                driver.find_elements_by_xpath('//span[text()="计算"]')[1].click()
                logger.debug('第二次计算成功')
                log_file_out('第二次计算成功')
            except NoSuchElementException as e:
                logger.error(e)
                logger.debug('第二次计算失败')
                log_file_out('第二次计算失败')
        else:
            log_file_out(contents[1]+'新增失败')
        driver.close()
    except:
        driver.close()

# 自定义选车保存 前端页面实时刷新
def custom_car_add_check(url,username,password,contents,carname,car):
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    log_file_out('-----' + contents[1] + '保存验证' + '-----')
    status = new_built(driver, url, username, password, contents,1)
    try:
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
        else:
            log_file_out(contents[1]+'新增失败')
        driver.close()
    except:
        driver.close()

# 平均故障间隔验证
def mtbf_check(url,username,password,contents,gjb_mtbf,test_duration,iec_mtbf,iec_test_duration):
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    log_file_out('-----' + contents[1] + '保存验证' + '-----')
    status = new_built(driver, url, username, password, contents,2)
    try:
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
        else:
            log_file_out(contents[1]+'新增失败')
        driver.close()
    except:
        driver.close()

# 平均维修时间验证是否出现nan
def mttr_add_check(url,username,password,contents,modelCode):
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    log_file_out('-----' + contents[1] + '保存验证' + '-----')
    status = new_built(driver, url, username, password, contents, 2)
    try:
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
        else:
            log_file_out(contents[1]+'新增失败')
        driver.close()
    except:
        driver.close()

# 最大维修时间
def max_repair_time_check(url,username,password,contents,modelCode):
    # option = webdriver.ChromeOptions()
    # option.add_argument("headless")
    # driver = webdriver.Chrome(chrome_options=option,
    #                           executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')
    driver = webdriver.Chrome()
    log_file_out('-----' + contents[1] + '保存验证' + '-----')
    status = new_built(driver, url, username, password, contents, 2)
    try:
        if status is True:
            log_file_out('登录成功')
            time.sleep(2)

            Method(driver).click('class', 'ivu-icon-md-add')

            time.sleep(1)
            try:
                driver.find_element_by_xpath("//span[text()=\'{}\']/../../../td".format(modelCode)).click()
                time.sleep(1)
                driver.find_elements_by_class_name('ivu-btn-info')[-1].click()
                log_file_out('工作时间导入成功')
            except Exception as e:
                log_file_out('工作时间导入失败')

            time.sleep(2)
            driver.find_elements_by_class_name('ivu-btn-info')[2].click()
            time.sleep(1)
            try:
                driver.find_element_by_xpath("//span[text()=\'{}\']/../../../td".format(modelCode)).click()
                time.sleep(1)
                driver.find_elements_by_class_name('ivu-btn-info')[-1].click()
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
        else:
            log_file_out(contents[1]+'新增失败')
        driver.close()
    except:
        driver.close()

# 可靠性增长验证
def taaf_add_check(url,username,password,contents):
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    log_file_out('-----' + contents[1] + '保存验证' + '-----')
    status = new_built(driver, url, username, password, contents, 2)
    try:
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
        else:
            log_file_out(contents[1]+'新增失败')
        driver.close()
    except:
        driver.close()

# 列车故障信息
def train_fault_information_check(url,username,password,contents,select,start,end,cause,car,value,fault):
    # option = webdriver.ChromeOptions()
    # option.add_argument("headless")
    # driver = webdriver.Chrome(chrome_options=option,
    #                           executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')
    driver = webdriver.Chrome()
    log_file_out('-----' + contents[1] + '验证' + '-----')
    status = new_built(driver, url, username, password, contents, 2)
    try:
        if status is True:
            log_file_out('登录成功')
            time.sleep(2)
            # 故障单的数量
            num = driver.find_elements_by_class_name('ivu-page-total')[0].text
            num1 = re.findall(r'\d+', num)

            Method(driver).click('class','beta-form-more')
            time.sleep(2)
            try:
                if select == '时间':
                    driver.find_elements_by_class_name('ivu-input-default')[0].send_keys(start)
                    time.sleep(0.5)
                    driver.find_elements_by_class_name('ivu-input-default')[1].send_keys(end)
                else:
                    driver.find_elements_by_class_name('ivu-input-default')[2].send_keys(start)
                    time.sleep(0.5)
                    driver.find_elements_by_class_name('ivu-input-default')[3].send_keys(end)
                log_file_out(select+'录入成功')
            except:
                log_file_out(select + '录入失败')

            if len(driver.find_elements_by_class_name('ivu-input-disabled')) == 2:
                log_file_out('输入'+select+'条件后,另外一个条件的两个输入框置灰,验证成功')
            else:
                log_file_out('输入' + select + '条件后,另外一个条件的两个输入框没有置灰,验证失败')
            time.sleep(1)
            # 选择原因分类
            try:
                Method(driver).click('class','ivu-select-placeholder')
                time.sleep(1)
                Method(driver).click('xpath','//li[text()=\'{}\']'.format(cause))
                time.sleep(0.5)
                Method(driver).click('class', 'ivu-select-selection')
                log_file_out('选择原因分类失败')
            except:
                log_file_out('选择原因分类成功')

            # 选车
            time.sleep(2)
            Method(driver).click('class','ivu-input-search')
            time.sleep(2)
            car_status = deal_car(driver, car, 1, 1)
            if car_status is True:
                log_file_out('选车成功')
            else:
                log_file_out('选车失败')
                return
            try:
                Method(driver).click('xpath','//*[text()=\'{}\']'.format('确认'))
                log_file_out('选车界面确认按钮点击成功')
            except:
                log_file_out('选车界面确认按钮点击失败')

            time.sleep(2)
            if value == 1:
                driver.find_elements_by_class_name('ivu-input-search')[1].click()

            else:
                driver.find_elements_by_class_name('ivu-input-search')[2].click()

            time.sleep(2)

            fault_status = deal_train_occur(driver, fault, value)

            if fault_status is True:
                log_file_out('选择部件成功')
            else:
                log_file_out('选择部件失败')

            try:
                Method(driver).click('xpath','//*[text()=\'{}\']'.format('确认'))
                log_file_out('故障对象界面确认按钮点击成功')
            except:
                log_file_out('故障对象界面确认按钮点击失败')
            time.sleep(2)
            # 点击查询按钮
            try:
                Method(driver).click('class','ct-input-group-append')
                log_file_out('点击查询按钮成功')
            except:
                log_file_out('点击查询按钮失败')
            time.sleep(2)
            # 故障单的数量
            num2 = driver.find_elements_by_class_name('ivu-page-total')[0].text
            num3 = re.findall(r'\d+', num2)

            if int(num1[0]) == int(num3[0]):
                log_file_out('查询前后故障单数量不变,验证失败')
            else:
                log_file_out('查询前后故障单数量发生变化,验证成功')
        else:
            log_file_out(contents[1]+'新增失败')
        driver.close()
    except:
        driver.close()

# 智能故障分析
def intelligent_fault_analysis_check(url,username,password,contents,start,end,trust_value):
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    log_file_out('-----' + contents[1] + '保存验证' + '-----')
    status = new_built(driver, url, username, password, contents, 2)
    try:
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
        else:
            log_file_out(contents[1]+'新增失败')
        driver.close()
    except:
        driver.close()

# 智能故障识别
def intelligent_fault_identification_check(url,username,password,contents,cartype,carnum):
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    log_file_out('-----' + contents[1] + '保存验证' + '-----')
    status = new_built(driver, url, username, password, contents, 2)
    try:
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
        else:
            log_file_out(contents[1]+'新增失败')
        driver.close()
    except:
        driver.close()

# 运维数据清洗验证
def operation_maintenance_data_cleaning_chcek(url,username,password,contents):
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    log_file_out('-----' + contents[1] + '保存验证' + '-----')
    status = new_built(driver, url, username, password, contents,2)
    try:
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
        else:
            log_file_out(contents[1]+'新增失败')
        driver.close()
    except:
        driver.close()

# 维修数据维护
def maintenance_data_maintenance(url,username,password,contents,modelCode, modelName, remarks, line, main_list):
    # option = webdriver.ChromeOptions()
    # option.add_argument("headless")
    # driver = webdriver.Chrome(chrome_options=option,
    #                           executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    log_file_out('-----' + contents[1] + '保存验证' + '-----')
    status = new_built(driver, url, username, password, contents, 1)
    try:
        if status is True:
            log_file_out('登录成功')
            time.sleep(2)

            a = driver.find_element_by_class_name('ivu-page-total').text[2:-2]

            try:
                driver.find_elements_by_class_name('ivu-input-default')[3].send_keys(modelCode)
                time.sleep(0.5)
                driver.find_elements_by_class_name('ivu-input-default')[4].send_keys(modelName)
                time.sleep(0.5)
                if remarks == '':
                    pass
                else:
                    driver.find_elements_by_class_name('ivu-input-default')[5].send_keys(remarks)
                log_file_out('基础信息输入成功')
            except Exception as e:
                logger.error(e)
                log_file_out('基础信息输入失败')

            num = 6
            for i in range(0, line):
                Method(driver).click('xpath', '//span[text()="添加行"]')
                driver.find_elements_by_class_name('ivu-input-default')[num].send_keys(randint(10, 99))
                num += 1
                time.sleep(0.2)

            try:
                for j in main_list[0:5]:
                    driver.find_elements_by_class_name('ivu-input-default')[num].send_keys(j)
                    num += 1
                    time.sleep(0.2)
                log_file_out('平均维修时间输入成功')
            except NoSuchElementException as e:
                logger.error(e)
                logger.debug('找不到id')
                log_file_out('平均维修时间输入失败')
            num = num + 1
            try:
                for j1 in main_list[5:11]:
                    driver.find_elements_by_class_name('ivu-input-default')[num].send_keys(j1)
                    num += 1
                    time.sleep(0.2)
                log_file_out('最大维修时间输入成功')
            except NoSuchElementException as e:
                logger.debug('找不到id')
                logger.error(e)
                log_file_out('最大维修时间输入失败')

            try:
                for j2 in main_list[11:18]:
                    driver.find_elements_by_class_name('ivu-input-default')[num].send_keys(j2)
                    num += 1
                    time.sleep(0.2)
                log_file_out('维修性参数输入成功')
            except NoSuchElementException as e:
                logger.error(e)
                logger.debug('找不到id')
                log_file_out('维修性参数输入失败')

            time.sleep(2)
            try:
                driver.find_element_by_xpath('//span[text()="保存"]').click()
                logger.debug('保存成功')
                log_file_out('点击保存按钮成功')
            except NoSuchElementException as e:
                logger.error(e)
                logger.debug('保存失败')
                log_file_out('点击保存按钮失败')
            time.sleep(2)

            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                    (By.CLASS_NAME, "ivu-message-notice")))
                error_message = driver.find_element_by_class_name("ivu-message-notice").text
            except:
                error_message = ''
            if error_message == '':
                if int(driver.find_element_by_class_name('ivu-page-total').text[2:-2]) == int(a) + 1:
                    log_file_out('维修数据维护验证成功')
                else:
                    log_file_out('维修数据维护验证失败')
            else:
                log_file_out(error_message)
        else:
            log_file_out(contents[1]+'新增失败')
        driver.close()
    except:
        driver.close()

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
    log_file_out('-----' + '项目首页' + '验证' + '-----')
    status = new_built(driver, url, username, password, contents,2)
    try:
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
                    # 设置图表下载路径为picture下面的project_home_model下
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
        driver.close()
    except:
        driver.close()

# 产品首页
def produce_home_page(url,username,password,contents,homepage_title,add_model,bnt_value,psi_car,ratio_model,compare_model):
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    log_file_out('-----' + '产品首页' + '验证' + '-----')
    status = new_built(driver, url, username, password, contents, 2)
    try:
        if status is True:
            log_file_out('登录成功')
            time.sleep(2)
            check_home_page().click_more_btn(driver)
            time.sleep(1)
            check_home_page().click_different_more_btn(driver, [1, homepage_title[0]], 0)

            time.sleep(2)
            check_home_page().click_message(driver)

            time.sleep(2)
            # 消息
            # try:
            #     # 设置图表下载路径为picture下面的produce_home_model的消息下
            #     produce_home_model_picture_path = os.path.dirname(
            #         __file__) + '\\' + 'picture' + '\\produce_home_model' + '\\' + '消息'
            #
            #     if os.path.isdir(produce_home_model_picture_path) is True:
            #         pass
            #     else:
            #         os.mkdir(produce_home_model_picture_path)
            #     driver.save_screenshot(produce_home_model_picture_path + '\\' + '消息' + '.png')
            #     log_file_out('消息页面截图成功')
            # except:
            #     log_file_out('消息页面截图失败')

            time.sleep(2)
            # 验证消息删除
            if len(driver.find_elements_by_class_name('el-icon-close')) != 0:
                # 原有的条数
                old_num = len(driver.find_elements_by_class_name('el-icon-close'))
                # 点击删除
                driver.find_elements_by_class_name('el-icon-close')[1].click()
                time.sleep(1)
                if len(driver.find_elements_by_class_name('el-icon-close')) == old_num:
                    log_file_out('消息列表中点击删除按钮失效,验证失败')
                else:
                    log_file_out('消息列表中点击删除按钮生效,验证成功')
            time.sleep(3)
            # 验证清除所有
            pass
            # 验证保存模型
            if len(driver.find_elements_by_xpath('//a[text()="保存模型"]')) == 0:
                pass
            else:
                try:
                    Method(driver).click('xpath', '//a[text()="保存模型"]')

                    WebDriverWait(driver, 3).until(EC.presence_of_element_located(
                        (By.CLASS_NAME, "ivu-message-notice")))
                    error_message = driver.find_element_by_class_name("ivu-message-notice").text

                    if error_message == '保存成功':
                        # 获取模型名称
                        model_m = driver.find_elements_by_class_name('messageContent')[0].text.split('\n')[0].split('-')[-1]
                        # 获取菜单名
                        menu_m = driver.find_elements_by_class_name('messageContent')[0].text.split('\n')[0].split('-')[-2]
                        time.sleep(1)
                        try:
                            Method(driver).click('class', 'ivu-icon-ios-close')
                            time.sleep(1)

                            Method(driver).click('class','el-icon-close')
                            time.sleep(2)
                        except:
                            log_file_out('点击退出登录按钮失败')
                        # 点击菜单
                        try:
                            if menu_m == '可靠性参数评估':
                                Method(driver).click('xpath', '//span[text()="RAMS指标评估"]')

                            else:
                                Method(driver).click('xpath', '//span[text()="RAMS指标分析"]')
                            time.sleep(1)
                            Method(driver).click('xpath','//span[text()=\'{}\']'.format(menu_m))
                        except:
                            log_file_out('点击功能菜单失败')
                        time.sleep(2)
                        # 点击更多
                        try:
                            driver.find_element_by_class_name('beta-form-more').click()
                            time.sleep(0.5)
                            # 计算状态选择框
                            driver.find_elements_by_class_name('ivu-select-placeholder')[1].click()
                            time.sleep(0.5)
                            driver.find_element_by_xpath('//li[text()="未计算"]').click()
                            time.sleep(0.5)
                            # 点击查询按钮
                            driver.find_element_by_class_name('ct-input-group-items').click()
                            time.sleep(2)
                            log_file_out('查询计算完成的模型成功')
                        except:
                            log_file_out('查询计算完成的模型失败')
                        target = driver.find_element_by_class_name('ivu-page-total')
                        driver.execute_script("arguments[0].scrollIntoView();", target)
                        time.sleep(1)
                        no_cal_num = driver.find_elements_by_class_name('ivu-page-total')[0].text
                        no_cal_num1 = re.findall(r'\d+', no_cal_num)
                        model_L = check_home_page().achieve_model(driver, no_cal_num1, '未计算')

                        if model_m in model_L:
                            log_file_out('保存模型验证成功')
                        else:
                            log_file_out('保存模型验证失败')

                        time.sleep(1)

                        # 重置
                        try:
                            driver.find_elements_by_class_name('ct-input-group-items')[1].click()
                            time.sleep(0.5)
                            # 计算状态选择框
                            driver.find_elements_by_class_name('ivu-select-placeholder')[1].click()
                            time.sleep(0.5)
                            driver.find_element_by_xpath('//li[text()="计算完成"]').click()
                            time.sleep(0.5)
                            # 点击查询按钮
                            driver.find_element_by_class_name('ct-input-group-items').click()
                            time.sleep(2)
                            log_file_out('查询计算完成的模型成功')
                            target = driver.find_element_by_class_name('ivu-page-total')
                            driver.execute_script("arguments[0].scrollIntoView();", target)

                            success_num = driver.find_elements_by_class_name('ivu-page-total')[0].text
                            success_num1 = re.findall(r'\d+', success_num)
                            success_model = check_home_page().achieve_model(driver, success_num1)
                        except:
                            log_file_out('查询计算完成的模型失败')

                        try:
                            Method(driver).click('xpath', '//span[text()="首页"]')
                        except:
                            log_file_out('点击首页按钮失败')
                        time.sleep(2)
                        # 打开页面
                        check_home_page().click_more_btn(driver)
                        time.sleep(1)
                        check_home_page().click_different_more_btn(driver, [1, homepage_title[0]], 3)
                        time.sleep(2)
                        check_home_page().click_message(driver)
                        time.sleep(1)

                    else:
                        log_file_out('消息列表中点击保存模型系统提示' + error_message)
                except:
                    log_file_out('消息列表中保存模型验证失败')


            # 验证打开模型
            if len(driver.find_elements_by_xpath('//a[text()="打开模型"]')) != 0:
                # 模型名称
                message_model = driver.find_elements_by_class_name('messageContent')[0].text.split('\n')[0].split('-')[-1]
                menu_m = driver.find_elements_by_class_name('messageContent')[0].text.split('\n')[0].split('-')[-2]
                driver.find_element_by_xpath('//a[text()="打开模型"]').click()
                time.sleep(5)

                if len(driver.find_elements_by_xpath('//span[text()="模型条件"]')) != 0:
                    if menu_m == '可靠性参数评估':
                        if message_model not in driver.find_elements_by_class_name('ivu-row')[1].text.split(':')[1].split(' ')[0]:
                            log_file_out('打开模型模型名称与消息列表中名称不一致,验证失败')
                        else:
                            log_file_out('打开模型模型名称与消息列表中名称一致,验证成功')
                    else:
                        if message_model not in driver.find_elements_by_xpath('//span[contains(text(),"模型名称")]/..')[0].text.split(':')[1].split(' ')[0]:

                            log_file_out('打开模型模型名称与消息列表中名称不一致,验证失败')
                        else:
                            log_file_out('打开模型模型名称与消息列表中名称一致,验证成功')


                    # 验证打开模型中是否可以更换模型
                    check_home_page().click_more_btn(driver)
                    time.sleep(2)
                    check_home_page().click_different_more_btn(driver, [2],0)
                    # 验证更换模型
                    try:
                        WebDriverWait(driver, 3).until(EC.presence_of_element_located(
                            (By.CLASS_NAME, "ivu-message-notice")))
                        screen_message = driver.find_element_by_class_name("ivu-message-notice").text

                        if screen_message == '临时屏不能更换模型':
                            log_file_out('临时屏中不能更换模型,验证成功')
                        else:
                            log_file_out('临时屏中不能更换模型,验证失败')
                    except:
                        log_file_out('验证临时屏是否可以更换模型失败')
                else:
                    log_file_out('打开模型验证失败')
            else:
                log_file_out('消息列表中模型数量为空')

                # 关闭消息页面
                Method(driver).click('class','ivu-icon-ios-close')
            time.sleep(2)


            # # 指标查看
            # try:
            #     Method(driver).click('class', 'imgMore')
            #     time.sleep(2)
            #     Method(driver).click('xpath', '//span[text()="指标查看"]/..')
            #     log_file_out('点击指标查看按钮成功')
            # except:
            #     log_file_out('点击指标查看按钮失败')
            # time.sleep(2)
            # try:
            #     for car in psi_car:
            #         driver.find_element_by_xpath(
            #             "//span[@class='train zoomIn' and contains(text(),\'{}\')]".format(car)).click()
            #         time.sleep(2)
            #         # 设置图表下载路径为picture下面的produce_home_model的指标查看下
            #         produce_home_model_picture_path = os.path.dirname(
            #             __file__) + '\\' + 'picture' + '\\produce_home_model' + '\\' + '指标查看'
            #
            #         if os.path.isdir(produce_home_model_picture_path) is True:
            #             pass
            #         else:
            #             os.mkdir(produce_home_model_picture_path)
            #         driver.save_screenshot(produce_home_model_picture_path + '\\'  + car + '_' + '指标值' + '.png')
            #         Method(driver).click('class', 'ivu-icon-md-arrow-back')
            #         time.sleep(2)
            #     # 点击关闭按钮
            #     check_home_page().click_close_but(driver)
            #     log_file_out('指标查看截图成功')
            # except Exception as e:
            #     logger.error(e)
            #     log_file_out('指标查看截图失败')
            # time.sleep(2)
            # # 指标警报按钮
            # try:
            #     Method(driver).click('class', 'imgMore')
            #     time.sleep(1)
            #     Method(driver).click('xpath', '//span[text()="指标预警"]/..')
            #     time.sleep(1)
            #     log_file_out('点击指标预警按钮成功')
            # except:
            #     log_file_out('指标预警按钮失败')
            #
            # try:
            #     # 设置图表下载路径为picture下面的produce_home_model的指标预警下
            #     produce_home_model_picture_path = os.path.dirname(
            #         __file__) + '\\' + 'picture' + '\\produce_home_model' + '\\' + '指标预警'
            #
            #     if os.path.isdir(produce_home_model_picture_path) is True:
            #         pass
            #     else:
            #         os.mkdir(produce_home_model_picture_path)
            #     driver.save_screenshot(produce_home_model_picture_path + '\\' + '指标预警' + '.png')
            #     time.sleep(2)
            #     # 点击关闭按钮
            #      check_home_page().click_close_but(driver)
            #     log_file_out('指标预警截图成功')
            # except Exception as e:
            #     logger.error(e)
            #     log_file_out('指标预警截图失败')
            # time.sleep(2)

            # 切换首页
            check_home_page().click_more_btn(driver)
            time.sleep(1)
            check_home_page().click_different_more_btn(driver, [1, homepage_title[0]], 0)
            time.sleep(2)
            # 验证更换模型
            check_home_page().click_more_btn(driver)
            time.sleep(1)
            check_home_page().click_different_more_btn(driver, [2], 0)

            # 验证更换模型中是否都为计算完成的模型
            try:
                success_count = 1
                for success_m in range(0,len(driver.find_elements_by_xpath('//tr/td[2]'))):
                    if driver.find_elements_by_xpath('//tr/td[2]')[success_m].text not in success_model:
                        success_count += 1
                        break
                    else:
                        pass
                if success_count == 1:
                    log_file_out('保存模型中模型都为计算完成模型,验证成功')
                else:
                    log_file_out('保存模型中模型不都为计算完成模型,验证失败')
            except:
                log_file_out('获取更换模型中模型列表失败')

            # 更换模型的预览
            for model_m in ratio_model:
                time.sleep(2)
                try:
                    # 移动到模型位置处
                    target = driver.find_element_by_xpath('//span[text()=\'{}\']'.format(model_m))
                    driver.execute_script("arguments[0].scrollIntoView();", target)
                    time.sleep(1)
                    Method(driver).click('xpath', '//span[text()=\'{}\']/../../../td[3]'.format(model_m))
                    time.sleep(5)
                    check_home_page().check_model_condition(driver, model_m, '', '更换模型')

                    time.sleep(1)
                    # 点击回退按钮
                    try:
                        Method(driver).click('class', 'ivu-icon-md-arrow-back')
                        log_file_out('点击更换模型中预览窗口回退按钮成功')
                    except Exception as e:
                        logger.error(e)
                        log_file_out('点击更换模型中预览窗口回退按钮失败')
                except:
                    log_file_out(model_m+'点击预览失败,验证失败')

                # 点击取消按钮
                check_home_page().click_close_but(driver)
            for home_page in homepage_title:
                # 切换首页
                check_home_page().click_more_btn(driver)
                time.sleep(2)
                check_home_page().click_different_more_btn(driver, [1, home_page], 0)
                time.sleep(7)
                if len(driver.find_elements_by_xpath('//span[text()="添加"]')) != 0 or len(driver.find_elements_by_xpath('//span[text()="模型条件"]')) != 0:
                    log_file_out(home_page + '页面打开成功,验证成功')
                    # 更换模型
                    check_home_page().click_more_btn(driver)
                    time.sleep(2)
                    check_home_page().click_different_more_btn(driver, [2], 0)
                    time.sleep(2)

                    if homepage_title.index(home_page) != 4:
                        try:
                            for model_m in ratio_model:
                                target = driver.find_element_by_xpath('//span[text()=\'{}\']'.format(model_m))
                                driver.execute_script("arguments[0].scrollIntoView();", target)
                                time.sleep(1)
                                Method(driver).click('xpath', '//span[text()=\'{}\']/../../../td[1]'.format(model_m))
                                time.sleep(1)
                            if len(driver.find_elements_by_class_name('ivu-radio-checked')) != 1:
                                log_file_out(home_page + '页面更换模型中模型只能单选,验证失败')
                            else:
                                log_file_out(home_page + '页面更换模型中模型只能单选,验证成功')

                            Method(driver).click('xpath', '//span[text()="确定"]')
                            log_file_out(home_page+'页面点击更换模型中确定按钮成功')
                        except Exception as e:
                            logger.error(e)
                            log_file_out(home_page+'页面更换模型失败')
                    else:
                        try:
                            for model_m1 in compare_model:
                                target = driver.find_element_by_xpath('//span[text()=\'{}\']'.format(model_m1))
                                driver.execute_script("arguments[0].scrollIntoView();", target)
                                time.sleep(1)
                                Method(driver).click('xpath', '//span[text()=\'{}\']/../../../td[1]'.format(model_m1))
                                time.sleep(1)
                            if len(driver.find_elements_by_class_name('ivu-radio-checked')) != 1:
                                log_file_out(home_page + '页面更换模型中模型只能单选,验证失败')
                            else:
                                log_file_out(home_page + '页面更换模型中模型只能单选,验证成功')

                            Method(driver).click('xpath', '//span[text()="确定"]')
                            log_file_out(home_page + '页面点击更换模型中确定按钮成功')
                        except Exception as e:
                            logger.error(e)
                            log_file_out(home_page + '页面更换模型失败')
                    time.sleep(10)
                    if len(driver.find_elements_by_xpath('//span[text()="添加"]')) != 0 or len(
                            driver.find_elements_by_xpath('//span[text()="模型条件"]')) != 0:
                        check_home_page().click_more_btn(driver)
                        time.sleep(2)
                        check_home_page().click_different_more_btn(driver, [3], 0)

                        time.sleep(10)
                        if len(driver.find_elements_by_xpath('//span[text()="模型条件"]')) != 0:


                            log_file_out(home_page + ':' + driver.find_elements_by_class_name('ivu-row')[1].text)
                            try:
                                if driver.find_element_by_xpath('//div[@class="ivu-dropdown-rel"]/div').text.split(':')[
                                    1].split(' ')[0] != \
                                        ratio_model[-1]:
                                    log_file_out(home_page + '页面更换模型后,模型名称未发生改变,验证失败')
                                else:
                                    log_file_out(home_page + '页面更换模型后,模型名称发生改变,验证成功')
                            except:
                                log_file_out(home_page + '页面更换模型后,模型名称未发生改变,验证失败')

                            # 模型总览页面的功能验证
                            if homepage_title.index(home_page) == 0:
                                if int(driver.find_element_by_xpath('//span[text()="列车总数"]/h3').text) == 0:
                                    log_file_out('列车总数为0,验证失败')
                                else:
                                    log_file_out('列车总数不为0,验证成功')

                                if int(driver.find_element_by_xpath('//span[text()="统计部件总数"]/h3').text) == 0:
                                    log_file_out('统计部件总数为0,验证失败')
                                else:
                                    log_file_out('统计部件总数不为0,验证成功')

                                if float(driver.find_element_by_xpath('//span[text()="列车行驶累计里程数(万公里)"]/h3').text) == 0:
                                    log_file_out('列车行驶累计里程数(万公里)为0,验证失败')
                                else:
                                    log_file_out('列车行驶累计里程数(万公里)不为0,验证成功')
                                try:
                                    # 点击图表上方4个按钮
                                    for j in bnt_value:
                                        Method(driver).click('xpath', '//span[contains(text(),\'{}\')]'.format(j))
                                        if bnt_value.index(j) == 0:
                                            if driver.find_elements_by_class_name('power-proChart-btn-empty')[0].text != j:
                                                log_file_out('点击\'{}\'后.按钮名称未发生变化,验证失败'.format(j))
                                            else:
                                                log_file_out('点击\'{}\'后.按钮名称发生变化,验证成功'.format(j))

                                            if driver.find_elements_by_class_name('power-proChart-btn-empty')[
                                                2].text != 'MDBF':
                                                log_file_out('点击\'{}\'后.平均故障里程功能的纵轴旁没有显示MDBF,验证失败'.format(j))
                                            else:
                                                log_file_out('点击\'{}\'后.平均故障里程功能的纵轴旁显示MDBF,验证成功'.format(j))

                                            if driver.find_elements_by_class_name('power-proChart-title')[2].text[
                                               :8] != '平均故障间隔里程':
                                                log_file_out('点击\'{}\'后.平均故障里程功能的图表名称不是平均故障间隔里程,验证失败'.format(j))
                                            else:
                                                log_file_out('点击\'{}\'后.平均故障里程功能的图表名称是平均故障间隔里程,验证成功'.format(j))
                                        else:
                                            if driver.find_elements_by_class_name('power-proChart-btn-empty')[0].text != j:
                                                log_file_out('点击\'{}\'后.按钮名称未发生变化,验证失败'.format(j))
                                            else:
                                                log_file_out('点击\'{}\'后.按钮名称发生变化,验证成功'.format(j))

                                            if driver.find_elements_by_class_name('power-proChart-btn-empty')[
                                                2].text != 'MTBF':
                                                log_file_out('点击\'{}\'后.平均故障里程功能的纵轴旁没有显示MTBF,验证失败'.format(j))
                                            else:
                                                log_file_out('点击\'{}\'后.平均故障里程功能的纵轴旁显示MTBF,验证成功'.format(j))

                                            if driver.find_elements_by_class_name('power-proChart-title')[2].text[
                                               :8] != '平均故障间隔时间':
                                                log_file_out('点击\'{}\'后.平均故障里程功能的图表名称不是平均故障间隔时间,验证失败'.format(j))
                                            else:
                                                log_file_out('点击\'{}\'后.平均故障里程功能的图表名称是平均故障间隔时间,验证成功'.format(j))
                                except:
                                    log_file_out(home_page + '图表名称验证失败')
                                try:
                                    # 点击平均修复时间"分钟/小时",查看值是否变化
                                    time_btn_value = driver.find_elements_by_class_name('power-chart-await')[
                                        1].find_element_by_class_name('power-proChart-btn').text
                                    driver.find_elements_by_class_name('power-chart-await')[1].find_element_by_class_name(
                                        'power-proChart-btn').click()
                                    time.sleep(1)
                                    time_btn_new_value = driver.find_elements_by_class_name('power-chart-await')[
                                        1].find_element_by_class_name(
                                        'power-proChart-btn').text
                                    if time_btn_value == time_btn_new_value:
                                        log_file_out('改变平均修复时间中时间单位按钮,未发生变化,验证失败')
                                    else:
                                        log_file_out('改变平均修复时间中时间单位按钮,发生变化,验证成功')
                                except:
                                    log_file_out(home_page + '小时/分钟按钮验证失败')
                                # 写入 评估值,合同值,设计值
                                for k in range(0, len(driver.find_elements_by_class_name('power-proChart-point'))):
                                    log_file_out(driver.find_elements_by_class_name('power-proChart-title')[k].text + ':' +
                                                 driver.find_elements_by_class_name('power-proChart-point')[k].text)

                            time.sleep(1)

                            # 验证图表名称
                            if homepage_title.index(home_page) == 0 or homepage_title.index(home_page) == 4:
                                chart_name = []
                                for chart in range(0, len(driver.find_elements_by_class_name('power-proChart-title'))):
                                    chart_name.append(driver.find_elements_by_class_name('power-proChart-title')[chart].text)
                                time.sleep(2)
                                for chart1 in range(0, len(driver.find_elements_by_class_name('power-proDesc-rightBtn')) - 3):
                                    fault_name = \
                                    driver.find_elements_by_class_name('power-proDesc-rightBtn')[chart1 + 3].text.split('\n')[0][:4]
                                    driver.find_elements_by_class_name('power-proDesc-rightBtn')[chart1 + 3].click()
                                    break

                                time.sleep(2)
                                # 记录变换之后的图表名称
                                chart_new_name = []
                                for new_chart in range(0, len(driver.find_elements_by_class_name('power-proChart-title'))):
                                    chart_new_name.append(driver.find_elements_by_class_name('power-proChart-title')[new_chart].text)

                                count = 1
                                for i in chart_new_name:
                                    if fault_name in i:
                                        pass
                                    else:
                                        count += 1
                                        break
                                if count != 1:
                                    log_file_out('点击失效类型,图表名称未发生变化,验证失败')
                                else:
                                    log_file_out('点击失效类型,图表名称发生变化,验证成功')
                                # 再点击失效类型 图表名称恢复成原来样子
                                Method(driver).click('xpath', '//p[contains(text(),\'{}\')]'.format(fault_name))
                                time.sleep(2)
                                count1 = 1
                                for old_chart in range(0, len(driver.find_elements_by_class_name('power-proChart-title'))):
                                    if driver.find_elements_by_class_name('power-proChart-title')[old_chart].text not in chart_name:
                                        count1 += 1
                                        break
                                    else:
                                        pass
                                if count1 != 1:
                                    log_file_out('再次点击失效类型,图表名称未发生变化,验证失败')
                                else:
                                    log_file_out('再次点击失效类型,图表名称发生变化,验证成功')
                            # 占比功能中的全图
                            if homepage_title.index(home_page) != 0 and homepage_title.index(home_page) != 4:

                                # 验证三张图是否重复
                                picture_L = []
                                for i in range(0, len(driver.find_elements_by_class_name('power-proChart-title'))):
                                    picture_L.append(driver.find_elements_by_class_name('power-proChart-title')[i].text)

                                # 去重
                                picture_L = list(set(picture_L))
                                if len(picture_L) != 3:
                                    log_file_out(home_page + '未出现所需的三张图表,验证失败')
                                else:
                                    log_file_out(home_page + '出现所需的三张图表,验证成功')

                                # 图表初始化,图表位置第一次落于百万公里故障率处
                                driver.find_element_by_xpath('//span[text()="百万公里故障率"]').click()

                                # 设置图表下载路径为picture下面的produce_home_model下
                                produce_home_model_picture_path = os.path.dirname(
                                    __file__) + '\\' + 'picture' + '\\produce_home_model' + '\\' + home_page
                                # 删除文件夹下的所有png文件 确保每一次截的图是最新的图

                                if os.path.isdir(produce_home_model_picture_path) is True:
                                    picture_list = os.listdir(produce_home_model_picture_path)
                                    for l in picture_list:
                                        if l.endswith('.png'):
                                            os.remove(produce_home_model_picture_path + "\\" + l)
                                else:
                                    os.mkdir(produce_home_model_picture_path)
                                time.sleep(1)
                                driver.save_screenshot(produce_home_model_picture_path + '\\' + home_page + '_' +
                                                       driver.find_elements_by_class_name('power-proChart-btn-active')[
                                                           -1].text + '.png')
                                time.sleep(2)
                                title_index = -3
                                try:
                                    for n in range(0, 3):
                                        title_index_text = driver.find_elements_by_class_name('power-proDesc-rightBtn')[
                                            title_index].text
                                        driver.find_elements_by_class_name('power-proDesc-rightBtn')[title_index].click()
                                        time.sleep(2)
                                        driver.save_screenshot(
                                            produce_home_model_picture_path + '\\' + home_page + '_' + title_index_text
                                            + '.png')
                                        title_index += 1
                                    log_file_out('截取' + home_page + '趋势图图表成功')
                                except:
                                    log_file_out('截取' + home_page + '趋势图图表失败')
                                time.sleep(2)
                                # 指标值个数
                                try:
                                    psi_num = driver.find_element_by_tag_name('strong').text
                                    # 点击指标值按钮
                                    driver.find_element_by_tag_name('strong').click()
                                    log_file_out(
                                        home_page + '页面指标值个数: ' + psi_num + ' 指标值内容: ' + driver.find_element_by_class_name(
                                            'ivu-dropdown-menu').text)
                                except:
                                    log_file_out('指标值获取失败')



                            # 多模型对比维度的功能验证
                            if homepage_title.index(home_page) == 4:

                                # 点击图表上方4个按钮
                                for j in bnt_value:
                                    Method(driver).click('xpath', '//span[contains(text(),\'{}\')]'.format(j))
                                    btn_vaule = 0
                                    for btn in range(0, len(driver.find_elements_by_class_name('power-proChart-btn'))):
                                        if driver.find_elements_by_class_name('power-proChart-btn')[0].text != j:
                                            btn_vaule += 1
                                            break
                                        else:
                                            pass
                                    if btn_vaule != 0:
                                        log_file_out('点击\'{}\'后.按钮名称未发生变化,验证失败'.format(j))
                                    else:
                                        log_file_out('点击\'{}\'后.按钮名称发生变化,验证成功'.format(j))

                                # 设置图表下载路径为picture下面的produce_home_model下
                                produce_more_model_picture_path = os.path.dirname(
                                    __file__) + '\\' + 'picture' + '\\produce_home_model' + '\\' + home_page

                                if os.path.isdir(produce_more_model_picture_path) is True:
                                    pass
                                else:
                                    os.mkdir(produce_more_model_picture_path)
                                driver.save_screenshot(produce_more_model_picture_path + '\\' + home_page + '.png')

                            # 查看模型条件 以及自定义范围
                            if homepage_title.index(home_page) != 4:


                                Method(driver).click('xpath', '//span[text()="模型条件"]')
                                time.sleep(5)
                                check_home_page().check_model_condition(driver, '', home_page, '模型条件')
                                time.sleep(2)

                                # 点击关闭按钮
                                check_home_page().click_close_but(driver)

                                time.sleep(2)
                                try:
                                    Method(driver).click('xpath', '//span[text()="自定义计算条件"]')
                                except Exception as e:
                                    log_file_out('点击自定义计算条件按钮失败')
                                    logger.error(e)
                                time.sleep(2)
                                # 点击复位按钮
                                if len(driver.find_elements_by_xpath('//span[text()="复位"]')) != 0:
                                    Method(driver).click('xpath', '//span[text()="复位"]')
                                else:
                                    pass
                                time.sleep(1)
                                try:
                                    # 定位第一个拖动的方块
                                    block = driver.find_elements_by_class_name('el-slider__button')[0]
                                    # 拖动方块
                                    move_to_gap(driver, block, get_track(50))
                                    time.sleep(2)
                                    # 拖动完第一个方块的位置
                                    first_block_place = driver.find_elements_by_class_name('showCurMes')[0].text
                                except:
                                    log_file_out('拖动开始位置方块失败')
                                try:
                                    # 定位第二个拖动的方块
                                    second_block = driver.find_elements_by_class_name('el-slider__button')[1]
                                    # 拖动第二个方块
                                    move_to_gap(driver, second_block, get_track(50))
                                    time.sleep(2)
                                    # 拖动完第二个方块的位置
                                    second_block_place = driver.find_elements_by_class_name('showCurMes')[1].text
                                    # 点击运用此范围
                                    Method(driver).click('xpath', '//span[text()="运用此范围"]')
                                except:
                                    log_file_out('拖动结束位置方块失败')
                                time.sleep(2)
                                # 获取页面上的当前里程

                                try:
                                    now_start = driver.find_element_by_xpath(
                                        '//span[contains(text(),"模型名称")]/../span[3]').text.split(':')[1].split('~')[
                                        0]
                                    now_end = driver.find_element_by_xpath(
                                        '//span[contains(text(),"模型名称")]/../span[3]').text.split(':')[1].split('~')[
                                        1]

                                    if now_start == first_block_place and now_end == second_block_place:
                                        log_file_out('页面上的当前里程随着里程范围发生正确的改变,验证成功')
                                    else:
                                        log_file_out('页面上的当前里程随着里程范围没有发生正确的改变,验证失败')
                                except:
                                    log_file_out('页面上的当前里程随着里程范围没有发生正确的改变,验证失败')

                                # 再点击模型条件看是否此范围是否对模型条件产生影响
                                try:
                                    Method(driver).click('xpath', '//span[text()="模型条件"]')
                                    time.sleep(2)
                                    # 模型条件
                                    model_conditon = driver.find_elements_by_class_name('power-preWrapper-title')[0].text
                                    # 获取里程/时间信息
                                    if driver.find_element_by_xpath('//span[contains(text(),"模型名称")]/../span[3]').text.split(':')[0][
                                       -2:] == '时间':
                                        start_condition = driver.find_element_by_xpath(
                                            '//p[@class="power-preCase-row"]/span[2]').text[:7]
                                        end_condition = driver.find_element_by_xpath(
                                            '//p[@class="power-preCase-row"]/span[3]').text[:7]
                                    else:
                                        start_condition = re.findall(r'\d+', driver.find_element_by_xpath(
                                            '//p[@class="power-preCase-row"]/span[2]').text)
                                        end_condition = re.findall(r'\d+', driver.find_element_by_xpath(
                                            '//p[@class="power-preCase-row"]/span[3]').text)
                                    if first_block_place == start_condition[0]:
                                        log_file_out('开始条件处,改变{}范围模型条件中发生正确的改变,验证成功'.format(model_conditon))
                                    else:
                                        log_file_out('开始条件处,改变{}范围模型条件中未发生正确的改变,验证失败'.format(model_conditon))

                                    if second_block_place == end_condition[0]:
                                        log_file_out('结束条件处,改变{}范围模型条件中发生正确的改变,验证成功'.format(model_conditon))
                                    else:
                                        log_file_out('结束条件处,改变{}范围模型条件中未发生正确的改变,验证失败'.format(model_conditon))
                                except:
                                    log_file_out('获取\'{}\'页面模型条件中里程/日期信息失败,无法验证改变范围是否会影响模型条件'.format(home_page))

                                # 点击关闭按钮
                                check_home_page().click_close_but(driver)

                            else:
                                # 暂时留着对比模型的模型条件
                                Method(driver).click('xpath', '//span[text()="模型条件"]')
                                time.sleep(5)
                                # 时间/理财
                                try:
                                    for compare_con in range(0, len(driver.find_elements_by_class_name('power-multi-tr')[
                                                                        1].find_elements_by_class_name(
                                            'power-multi-child'))):
                                        if \
                                        driver.find_elements_by_class_name('power-multi-tr')[1].find_elements_by_class_name(
                                                'power-multi-child')[compare_con].text != '':
                                            log_file_out('对比功能第{}个模型时间/里程条件不为空,验证成功'.format(compare_con))
                                        else:
                                            log_file_out('对比功能第{}个模型时间/里程条件为空,验证失败'.format(compare_con))
                                except:
                                    log_file_out('对比功能时间/里程条件验证失败')

                                try:
                                    # 点击车型
                                    driver.find_elements_by_class_name('power-multi-icoMore')[0].click()
                                    time.sleep(1)

                                    for compare_car in range(0, len(
                                            driver.find_elements_by_class_name('power-multi-trainTypeRow'))):
                                        driver.find_elements_by_class_name('power-multi-trainTypeTag')[compare_car].click()
                                        time.sleep(1)
                                        if driver.find_elements_by_class_name('power-multi-trainNoRow')[
                                            compare_car].text != '':
                                            log_file_out('对比功能第{}个模型车型条件不为空,验证成功'.format(compare_car))
                                        else:
                                            log_file_out('对比功能第{}个模型车型条件为空,验证失败'.format(compare_car))
                                except:
                                    log_file_out('对比模型车型车号验证失败')

                                try:
                                    # 点击部件
                                    driver.find_elements_by_class_name('power-multi-icoMore')[2].click()
                                    time.sleep(1)
                                    for compare_fault in range(0,
                                                               len(driver.find_elements_by_class_name('ivu-tree-arrow'))):
                                        driver.find_elements_by_class_name('ivu-tree-arrow')[compare_fault].click()
                                        time.sleep(1)
                                        if driver.find_elements_by_class_name('power-preFault-col')[compare_fault] != '':
                                            log_file_out('对比功能第{}个模型部件/故障模式条件不为空,验证成功'.format(compare_fault))
                                        else:
                                            log_file_out('对比功能第{}个模型部件/故障模式条件为空,验证失败'.format(compare_fault))
                                except:
                                    log_file_out('多模型部件验证失败')

                                try:
                                    # 验证模型共同条件
                                    Method(driver).click('xpath', '//span[contains(text(),"模型共同条件")]')
                                    time.sleep(2)
                                    # 模型名称
                                    compare_name = \
                                    driver.find_elements_by_class_name('ivu-row')[1].text.split(':')[1].split(' ')[0]
                                    # 共同条件
                                    compare_common = driver.find_elements_by_class_name('power-pre-wrapper')[1].text
                                    log_file_out('对比模型,\'{}\'模型,共同模型条件为'.format(compare_name) + compare_common)
                                except:
                                    log_file_out('对比模型,\'{}\'模型,共同模型条件为空'.format(compare_name))

                                # 点击模型共同条件的关闭按钮
                                check_home_page().click_close_but(driver)
                                time.sleep(1)
                                # 点击模型条件的关闭按钮
                                check_home_page().click_close_but(driver)



                        else:
                            log_file_out('\'{}\'重新计算模型失败,页面未打开,验证失败'.format(home_page))
                            pass
                    else:
                        log_file_out(home_page + '页面更换模型后,模型计算失败,验证失败')

                else:
                    log_file_out(home_page+'页面打开失败,验证失败')
                    pass
        driver.close()
    except:
        driver.close()

#
#
#             time.sleep(1)
#
#
#
#
#
#





















