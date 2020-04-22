from config.config import *



# 验证占比功能导入自定义车组之后是否可以正确保存
def check_ratio_customize_traingroup(url,username,password,contents,modelName,modelCode,remarks,select,type,start,end,select_car,customize_traingroup):
    driver = webdriver.Chrome()
    status = Login().login(url, username, password, driver)
    time.sleep(2)
    driver.maximize_window()
    Method(driver).click('id', 'ballb')
    if contents[0] == '运营费用统计' or contents[0] == '运维费用统计' or contents[0] == '通用模型':
        log_file_out('---------' + '{}'.format(contents[0]) + '导入自定义车组验证---------')
    else:
        log_file_out('---------' + '{}'.format(contents[0]) + '占比分析导入自定义车组验证---------')
    # driver.execute_script("document.body.style.zoom='0.8'")
    if status is True:
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[0])
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

        if contents[0] == '运维费用统计' or contents[0] == '运营费用统计':
            try:
                Method(driver).click('xpath', '//*[contains(text(),"新建内容")]')

                log_file_out('点击新建按钮成功')
            except NoSuchElementException as e:
                logger.debug('点击新建按钮失败')
                logger.error(e)
                log_file_out('点击新建按钮失败')
        else:
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
            Method(driver).input('xpath', "//input[@placeholder='请输入模型名称']", modelName)
            Method(driver).input('xpath', "//input[@placeholder='请输入模型编码']", modelCode)
            if remarks is '':
                pass
            else:
                Method(driver).input('xpath', "//input[@placeholder='请输入备注信息']",
                                     remarks)
            log_file_out('录入模型基本信息成功')
        except NoSuchElementException as e:
            logger.debug('录入模型基本信息失败')
            logger.error(e)
            log_file_out('录入模型基本信息失败')

        if select == '新建':
            time.sleep(1)
            if type == '时间':
                # 输入时间
                try:
                    Method(driver).input('xpath', "//input[@placeholder='请输入开始日期']", start)
                    Method(driver).input('xpath', "//input[@placeholder='请输入结束日期']", end)
                    # Method(driver).click('xpath',
                    #                      '//*[@id="OM_edit_modal"]/div[2]/div/div/div[2]/div[1]/div[3]/div/div[3]/div[1]/form/div/div/div/div/div/input')
                    log_file_out('输入时间成功')
                except NoSuchElementException as e:
                    logger.error(e)
                    logger.debug('输入时间失败')
                    log_file_out('输入时间失败')
            else:
                try:
                    Method(driver).click('xpath', '//label[text()="里程条件"]')
                    time.sleep(2)
                    Method(driver).input('xpath', "//input[@placeholder='请输入开始里程']", start)
                    Method(driver).input('xpath', "//input[@placeholder='请输入结束里程']", end)
                except NoSuchElementException as e:
                    logger.error(e)
                    logger.debug('输入里程失败')
                    log_file_out('输入里程失败')
            # 验证自定义车组
            Method(driver).click('id', 'trainPickRange_cdImportBtn')
            time.sleep(1)
            # 选择自定义车组
            driver.find_element_by_xpath(
                '//span[text()=\'{}\']/../../../td[1]/div'.format(customize_traingroup)).click()
            time.sleep(1)
            # 点击确定
            driver.find_elements_by_xpath('//span[text()="确认"]')[1].click()
            time.sleep(1)
            # 验证导入车组后 点击全选 全不选 删除是否有反应
            # 得到导入的全部车
            car_sum = len(driver.find_elements_by_class_name('train-no-items'))
            # 点击全选
            Method(driver).click('id','trainResBtn_checkAll')
            time.sleep(1)
            if len(driver.find_elements_by_class_name('train-no-items')) == len(driver.find_elements_by_class_name('train-no-items-on')):
                log_file_out('导入自定义车组后,点击全选有反应,验证成功')
            else:
                log_file_out('导入自定义车组后,点击全选没有反应,验证失败')



            # 点击全不选
            Method(driver).click('id', 'trainResBtn_checkAll')
            # 选中一辆车
            Method(driver).click('xpath',
                                 '//span[contains(@class,"train-no-items") and text()=\'{}\']'.format(select_car))
            time.sleep(1)
            if len(driver.find_elements_by_class_name('train-no-items')) -1 == len(driver.find_elements_by_class_name('train-no-items-off')):
                log_file_out('导入自定义车组后,点击全不选有反应,验证成功')
            else:
                log_file_out('导入自定义车组后,点击全不选没有反应,验证失败')

            # 点击删除
            Method(driver).click('id', 'trainResBtn_remove')
            time.sleep(1)
            if len(driver.find_elements_by_class_name('train-no-items')) == car_sum - 1:
                log_file_out('导入自定义车组后,点击删除有反应,验证成功')
            else:
                log_file_out('导入自定义车组后,点击删除没有反应,验证失败')

            time.sleep(2)
            # 点击保存验证
            try:
                Method(driver).click('xpath','//span[text()="确认"]')

                log_file_out('点击保存按钮成功')

            except NoSuchElementException as e:
                logger.error(e)
                log_file_out('点击保存按钮失败')
                return
            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                    (By.CLASS_NAME, "ivu-message-notice")))
                a = driver.find_element_by_class_name("ivu-message-notice").text
            except:
                a = ''
            if a != '':
                log_file_out('导入自定义车组后,不能正常保存,验证失败')
            else:
                log_file_out('导入自定义车组后,可以正常保存,验证成功')

# 验证对比功能导入自定义车组之后是否可以正确保存
def check_repair_customize_traingroup(url,username,password,contents,modelName,modelCode,remarks,type,min_model,select_car,customize_traingroup,car_start,car_end):
    driver = webdriver.Chrome()
    status = Login().login(url, username, password, driver)
    time.sleep(2)
    driver.maximize_window()

    Method(driver).click('id', 'ballb')
    # time.sleep(10)
    if status is True:
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[0])

        log_file_out('---------' + '{}'.format(contents[0]) + '对比分析自定义车组验证---------')

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
            Method(driver).input('xpath', "//input[@placeholder='请输入模型名称']", modelName)
            Method(driver).input('xpath', "//input[@placeholder='请输入模型编码']", modelCode)
            # actions = ActionChains(driver)
            # actions.click(driver.find_element_by_xpath('//*[@id="OM_editForm"]/div/div[3]/div/div/div/div/div/span')).perform()

            if remarks is '':
                pass
            else:
                Method(driver).input('xpath', "//input[@placeholder='请输入备注信息']", remarks)
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
        Method(driver).click('xpath', '//li[text()="运营费用"]')

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

                    # 验证是否会缺少车型车号
                    if len(driver.find_elements_by_class_name('row-trainType-items')) == 0:
                        log_file_out('缺少可以选择的车型,验证失败')
                    else:
                        log_file_out('不缺少可以选择的车型,验证成功')
                # 验证车号范围查询
                Method(driver).input('xpath', "//input[@placeholder='请输入车号']", car_start)
                time.sleep(1)
                driver.find_elements_by_xpath("//input[@placeholder='请输入车号']")[1].send_keys(car_end)
                # 点击查询按钮
                time.sleep(1)
                Method(driver).click('id', 'trainPickRange_searchBtn')
                time.sleep(1)
                if len(driver.find_elements_by_class_name('train-no-items-off')) == 0:
                    log_file_out('车号范围查询”功能异常,验证失败')
                else:
                    log_file_out('车号范围查询”功能正常,验证成功')

                # 验证自定义车组
                Method(driver).click('id', 'trainPickRange_cdImportBtn')
                time.sleep(1)
                # 选择自定义车组
                driver.find_element_by_xpath(
                    '//span[text()=\'{}\']/../../../td[1]/div'.format(customize_traingroup)).click()
                time.sleep(1)
                # 点击确定
                driver.find_elements_by_xpath('//span[text()="确认"]')[1].click()
                time.sleep(1)
                # 验证导入车组后 点击全选 全不选 删除是否有反应
                # 得到导入的全部车
                car_sum = len(driver.find_elements_by_class_name('train-no-items'))
                # 点击全选
                Method(driver).click('id', 'trainResBtn_checkAll')
                time.sleep(1)
                if len(driver.find_elements_by_class_name('train-no-items')) == len(
                        driver.find_elements_by_class_name('train-no-items-on')):
                    log_file_out('导入自定义车组后,点击全选有反应,验证成功')
                else:
                    log_file_out('导入自定义车组后,点击全选没有反应,验证失败')

                # 点击全不选
                Method(driver).click('id', 'trainResBtn_checkAll')
                # 选中一辆车
                Method(driver).click('xpath',
                                     '//span[contains(@class,"train-no-items") and text()=\'{}\']'.format(
                                         select_car))
                time.sleep(1)
                if len(driver.find_elements_by_class_name('train-no-items')) - 1 == len(
                        driver.find_elements_by_class_name('train-no-items-off')):
                    log_file_out('导入自定义车组后,点击全不选有反应,验证成功')
                else:
                    log_file_out('导入自定义车组后,点击全不选没有反应,验证失败')

                # 点击删除
                Method(driver).click('id', 'trainResBtn_remove')
                time.sleep(1)
                if len(driver.find_elements_by_class_name('train-no-items')) == car_sum - 1:
                    log_file_out('导入自定义车组后,点击删除有反应,验证成功')
                else:
                    log_file_out('导入自定义车组后,点击删除没有反应,验证失败')


                driver.find_elements_by_xpath('//span[contains(text(),"确认")]')[1].click()
                time.sleep(2)

                try:
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                        (By.CLASS_NAME, "ivu-message-notice")))
                    a = driver.find_element_by_class_name("ivu-message-notice").text
                except:
                    a = ''
                if a != '':
                    log_file_out('导入自定义车组后,不能正常保存,验证失败')
                    return
                else:
                    log_file_out('导入自定义车组后,可以正常保存,验证成功')
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
        log_file_out('登录失败')


# 验证改变系统配置系统是否会改变
def check_user_system(url, username, password, contents, check_contents):
    driver = webdriver.Chrome()
    status = Login().login(url, username, password, driver)
    time.sleep(2)
    driver.maximize_window()
    Method(driver).click('id', 'ballb')

    log_file_out('---------' + '{}'.format(contents[0]) + '修改配置验证---------')

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
        Method(driver).click('class', 'power-btnOk')
        time.sleep(1)
        # 修改系统语言
        driver.find_elements_by_class_name('ivu-radio-input')[1].click()
        time.sleep(1)

        # 日期格式
        driver.find_elements_by_class_name('ivu-radio-input')[4].click()
        time.sleep(1)

        # 点击修改配置按钮
        Method(driver).click('class', 'power-btnOk')

        time.sleep(1)
        # 点击确定
        driver.find_elements_by_xpath('//span[text()="确定"]')[1].click()
        time.sleep(2)
        # 打开功能页面查看
        driver.find_elements_by_class_name('power-collapse-item')[0].click()
        time.sleep(1)

        try:
            driver.find_elements_by_xpath('//span[text()=\'{}\']'.format(check_contents[0]))[1].click()
            log_file_out('点击' + contents[0] + '成功')
            time.sleep(1)
        except NoSuchElementException as e:
            log_file_out('点击' + contents[0] + '失败')
            logger.error(e)

        if '/' in driver.find_elements_by_xpath('//*[@class="ivu-table-tbody"]/tr[1]/td[5]')[0].text:
            log_file_out('系统配置中改变日期格式生效,验证成功')
        else:
            log_file_out('系统配置中改变日期格式没有生效,验证失败')