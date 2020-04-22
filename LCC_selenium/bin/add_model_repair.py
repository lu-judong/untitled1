from config.config import *

# 对比功能的新增
def repair_add_model(url,username,password,contents,modelCode,modelName,remarks,select,type,min_model,wait_time):
    # option = webdriver.ChromeOptions()
    # option.add_argument("headless")
    # driver = webdriver.Chrome(chrome_options=option
    #                           ,
    #                           executable_path=r'.\apps\chromedriver.exe'
    #                           )
    # driver.maximize_window()
    driver = webdriver.Chrome()
    status = Login().login(url,username,password,driver)
    time.sleep(2)
    driver.maximize_window()

    Method(driver).click('id', 'ballb')
    # time.sleep(10)
    if status is True:
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[0])



        log_file_out('---------' + '{}'.format(contents[0]) + '对比分析新增验证---------')

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

        driver.find_elements_by_xpath('//span[text()=\'{}\']/../../ul/li[1]'.format(contents[0]))[1].click()


        time.sleep(2)
        try:
            Method(driver).contains_click('新建内容')
            log_file_out('点击新建按钮成功')
        except NoSuchElementException as e:
            logger.debug('点击新建按钮失败')
            logger.error(e)
            log_file_out('点击新建按钮失败')

        time.sleep(3)
        # 录入模型信息
        try:
            Method(driver).input('xpath',"//input[@placeholder='请输入模型名称']",modelName)
            Method(driver).input('xpath',"//input[@placeholder='请输入模型编码']",modelCode)
            # actions = ActionChains(driver)
            # actions.click(driver.find_element_by_xpath('//*[@id="OM_editForm"]/div/div[3]/div/div/div/div/div/span')).perform()

            if remarks is '':
                pass
            else:
                Method(driver).input('xpath',"//input[@placeholder='请输入备注信息']",remarks)
            log_file_out('录入模型基本信息成功')
        except NoSuchElementException as e:
            logger.debug('录入模型基本信息失败')
            logger.error(e)
            log_file_out('录入模型基本信息失败')
        time.sleep(1)
        # 验证选择其他费用阶段是否可以保存
        driver.find_elements_by_class_name('ivu-select-selected-value')[1].click()
        # 选择其他费用
        time.sleep(1)
        Method(driver).click('xpath','//li[text()="运营费用"]')


        if select == '新建':
            try:
                for x in min_model:
                    Method(driver).click('class','chiCard-addBox-ico')
                    time.sleep(1)
                    driver.find_elements_by_xpath("//input[@placeholder='请输入模型名称']")[1].send_keys(x[0])
                    if type == '时间':
                        time.sleep(1)
                        Method(driver).input('xpath', "//input[@placeholder='请输入开始日期']", x[1])
                        Method(driver).input('xpath', "//input[@placeholder='请输入结束日期']", x[2])
                    else:
                        Method(driver).click('xpath','//label[text()="里程条件"]')
                        time.sleep(1)
                        Method(driver).input('xpath',"//input[@placeholder='请输入开始里程']",x[1])
                        Method(driver).input('xpath',"//input[@placeholder='请输入结束里程']",x[2])

                    # 验证自定义车组

                    time.sleep(2)
                    select_car = Method(driver).select_car(x[3])
                    if select_car is True:
                        log_file_out('选车成功')
                    else:
                        log_file_out('选车失败')
                        return

                    # 选择构型
                    if x[4] == '':
                        pass
                    else:
                        for i in x[4]:
                            Method(driver).click('xpath', '//span[contains(@class,"node-trainType-ableItems") and text()=\'{}\']'.format(
                                                     i))
                            time.sleep(1)
                            re = x[4][i]
                            for j in re:
                                Method(driver).select_repairlocation(j)
                    # 选择供应商
                    if x[5] == '':
                        pass
                    else:
                        for i in x[5]:
                            Method(driver).click('xpath','//span[contains(@class,"power-item-tag") and text()=\'{}\']'.format(
                                                     i))
                            for j in x[5][i]:
                                Method(driver).click('xpath','//span[contains(@class,"power-item-tag") and text()=\'{}\']'.format(
                                                         j))
                            Method(driver).click('xpath', '//span[text()="选择"]')

                    driver.find_elements_by_xpath('//span[contains(text(),"确认")]')[1].click()
                    time.sleep(2)

                log_file_out('新建模型成功')

            except NoSuchElementException as e:
                logger.debug('新建失败')
                logger.error(e)
                log_file_out('新建模型失败')

            try:
                driver.find_elements_by_xpath('//span[contains(text(),"确认")]')[0].click()
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
            if a != '':
                log_file_out(a)
            else:
                log_file_out('费用阶段选择其他费用也可以正常保存,验证失败')
            try:
                # 把费用阶段改回正确的正常保存
                driver.find_element_by_xpath("//a[text()=\'{}\']".format(modelName)).click()
                time.sleep(2)
                Method(driver).click('class', 'ivu-select-placeholder')
                # 选择费用
                time.sleep(1)
                Method(driver).click('xpath', '//li[text()="维修费用"]')
                time.sleep(1)
                log_file_out('费用阶段改回维修费用成功')
            except Exception as e:
                logger.error(e)
                log_file_out('费用阶段改回维修费用失败')
            try:
                driver.find_elements_by_xpath('//span[contains(text(),"确认")]')[0].click()
                log_file_out('点击保存按钮成功')
            except NoSuchElementException as e:
                logger.error(e)
                log_file_out('点击保存按钮失败')
            try:
                WebDriverWait(driver, 3).until(EC.presence_of_element_located(
                    (By.CLASS_NAME, "ivu-message-notice")))
                a = driver.find_element_by_class_name("ivu-message-notice").text
            except:
                a = ''
            if a != '':
                log_file_out(a)
            else:
                time.sleep(2)
                driver.find_element_by_xpath(
                    "//a[text()=\'{}\']/../../../../td[1]/div/div/div[1]/div/span/i".format(modelName)).click()

                try:
                    a1 = WebDriverWait(driver, wait_time).until(EC.text_to_be_present_in_element((By.XPATH, "//a[text()=\'{}\']/../../../../td[4]/div/div/span/span".format(modelName)), u'计算异常'))
                    if a1 == True:
                        log_file_out('计算异常,无法评估')
                        return
                except Exception as e:
                    a = driver.find_element_by_xpath(
                        "//a[text()=\'{}\']/../../../../td[4]/div/div/span/span".format(modelName)).text
                    if a == '计算完成':
                        log_file_out('评估成功')
                        time.sleep(2)
                        try:
                            driver.find_element_by_xpath(
                                "//a[text()=\'{}\']/../../../../td[1]/div/div/div[2]/div/span/i".format(modelName)).click()
                            log_file_out('点击图表成功')
                        except NoSuchElementException as e:
                            logger.error(e)
                            log_file_out('点击图表失败')

    else:
        log_file_out('登陆失败')
    driver.close()


# 对比功能的修改
def repair_revise(url,username,password,contents,modelName,type,min_model,wait_time):
    driver = webdriver.Chrome()
    status = Login().login(url, username, password, driver)
    driver.maximize_window()

    Method(driver).click('id', 'ballb')
    # time.sleep(10)
    if status is True:
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[0])

        log_file_out('---------' + '{}'.format(contents[0]) + '对比分析修改验证---------')

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

        driver.find_elements_by_xpath('//span[text()=\'{}\']/../../ul/li[1]'.format(contents[0]))[1].click()
        time.sleep(2)
        driver.find_element_by_xpath("//a[text()=\'{}\']".format(modelName)).click()
        time.sleep(2)
        Method(driver).click('class', "ivu-select-placeholder")
        time.sleep(1)

        Method(driver).contains_click('维修费用')
        time.sleep(1)
        for i in range(0,len(min_model)):
            Method(driver).click('class', "icon-btn-remove")
            time.sleep(1)

        try:
            for x in min_model:
                Method(driver).click('class', 'chiCard-addBox-ico')
                time.sleep(1)
                driver.find_elements_by_xpath("//input[@placeholder='请输入模型名称']")[1].send_keys(x[0])
                if type == '时间':
                    time.sleep(1)
                    Method(driver).input('xpath', "//input[@placeholder='请输入开始日期']", x[1])
                    Method(driver).input('xpath', "//input[@placeholder='请输入结束日期']", x[2])
                else:
                    Method(driver).click('xpath', '//label[text()="里程条件"]')
                    time.sleep(1)
                    Method(driver).input('xpath', "//input[@placeholder='请输入开始里程']", x[1])
                    Method(driver).input('xpath', "//input[@placeholder='请输入结束里程']", x[2])

                time.sleep(2)
                select_car = Method(driver).select_car(x[3])
                if select_car is True:
                    log_file_out('选车成功')
                else:
                    log_file_out('选车失败')
                    return

                # 选择构型
                if x[4] == '':
                    pass
                else:
                    for i in x[4]:
                        Method(driver).click('xpath',
                                             '//span[contains(@class,"node-trainType-ableItems") and text()=\'{}\']'.format(
                                                 i))
                        time.sleep(1)
                        re = x[4][i]
                        for j in re:
                            Method(driver).select_repairlocation(j)
                # 选择供应商
                if x[5] == '':
                    pass
                else:
                    for i in x[5]:
                        Method(driver).click('xpath',
                                             '//span[contains(@class,"power-item-tag") and text()=\'{}\']'.format(
                                                 i))
                        for j in x[5][i]:
                            Method(driver).click('xpath',
                                                 '//span[contains(@class,"power-item-tag") and text()=\'{}\']'.format(
                                                     j))
                        Method(driver).click('xpath', '//span[text()="选择"]')

                driver.find_elements_by_xpath('//span[contains(text(),"确认")]')[1].click()
                time.sleep(2)

            log_file_out('新建模型成功')

        except NoSuchElementException as e:
            logger.debug('新建失败')
            logger.error(e)
            log_file_out('新建模型失败')

        try:
            driver.find_elements_by_xpath('//span[contains(text(),"确认")]')[0].click()
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
        if a != '':
            log_file_out(a)
            return
        else:
            time.sleep(2)
            driver.find_element_by_xpath(
                "//a[text()=\'{}\']/../../../../td[1]/div/div/div[1]/div/span/i".format(modelName)).click()

            try:
                a1 = WebDriverWait(driver, wait_time).until(EC.text_to_be_present_in_element(
                    (By.XPATH, "//a[text()=\'{}\']/../../../../td[4]/div/div/span/span".format(modelName)), u'计算异常'))
                if a1 == True:
                    log_file_out('计算异常,无法评估')
                    return
            except Exception as e:
                a = driver.find_element_by_xpath(
                    "//a[text()=\'{}\']/../../../../td[4]/div/div/span/span".format(modelName)).text
                if a == '计算完成':
                    log_file_out('评估成功')
                    time.sleep(2)
                    try:
                        driver.find_element_by_xpath(
                            "//a[text()=\'{}\']/../../../../td[1]/div/div/div[2]/div/span/i".format(modelName)).click()
                        log_file_out('点击图表成功')
                    except NoSuchElementException as e:
                        logger.error(e)
                        log_file_out('点击图表失败')
    else:
        log_file_out('登陆失败')

    driver.close()

