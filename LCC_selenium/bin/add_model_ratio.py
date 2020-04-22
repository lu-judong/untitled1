from config.config import *





# 运维费用统计/占比功能/通用模型的新增
def add(url,username,password,contents,modelName,modelCode,remarks,select,type,start,end,car_start,car_end,car,repairlocation,supplier,wait_time):
    # option = webdriver.ChromeOptions()
    # option.add_argument("headless")
    # driver = webdriver.Chrome(chrome_options=option
    #                           ,
    #                           executable_path=r'.\apps\chromedriver.exe'
    #                           )

    driver = webdriver.Chrome()
    status = Login().login(url, username, password, driver)
    time.sleep(2)
    driver.maximize_window()
    Method(driver).click('id', 'ballb')
    if contents[0] == '运营费用统计' or contents[0] == '运维费用统计' or contents[0] == '通用模型':
        log_file_out('---------' + '{}'.format(contents[0]) + '新增验证---------')
    else:
        log_file_out('---------' + '{}'.format(contents[0]) + '占比分析新增验证---------')
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
            if len(contents) == 2:
                driver.find_elements_by_xpath('//span[text()=\'{}\']/../../ul/li[2]'.format(contents[0]))[1].click()


        if contents[0] == '运维费用统计' or contents[0] == '运营费用统计':
            try:
                Method(driver).click('xpath','//*[contains(text(),"新建内容")]')

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
            Method(driver).input('xpath',"//input[@placeholder='请输入模型名称']",modelName)
            Method(driver).input('xpath', "//input[@placeholder='请输入模型编码']",modelCode)
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
                    Method(driver).input('xpath',"//input[@placeholder='请输入开始里程']",start)
                    Method(driver).input('xpath',"//input[@placeholder='请输入结束里程']",end)
                except NoSuchElementException as e:
                    logger.error(e)
                    logger.debug('输入里程失败')
                    log_file_out('输入里程失败')
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
            Method(driver).click('id','trainPickRange_searchBtn')
            time.sleep(1)
            if len(driver.find_elements_by_class_name('train-no-items-off')) == 0:
                log_file_out('车号范围查询”功能异常,验证失败')
            else:
                log_file_out('车号范围查询”功能正常,验证成功')


            time.sleep(2)
            # 选车
            select_car = Method(driver).select_car(car)
            if select_car is True:
                log_file_out('选车成功')
            else:
                log_file_out('选车失败')
                return
            # 选择构型
            if repairlocation == '':
                pass
            else:
                for i in repairlocation:
                    Method(driver).click('xpath','//span[contains(@class,"node-trainType-ableItems") and text()=\'{}\']'.format(i))
                    time.sleep(1)
                    re = repairlocation[i]
                    for i in re:
                        Method(driver).select_repairlocation(i)
            # 选择供应商
            if supplier == '':
                pass
            else:
                for i in supplier:
                    Method(driver).click('xpath','//span[contains(@class,"power-item-tag") and text()=\'{}\']'.format(i))
                    for j in supplier[i]:
                        Method(driver).click('xpath','//span[contains(@class,"power-item-tag") and text()=\'{}\']'.format(j))

                    Method(driver).click('xpath', '//span[text()="选择"]')
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
                log_file_out(a)
                return
            else:
                if contents[0] == '通用模型':
                    time.sleep(2)
                    try:
                        driver.find_element_by_xpath("//a[text()=\'{}\']".format(modelName))
                        log_file_out('回到模型页面,模型新增成功,验证成功')
                    except:
                        log_file_out('回到模型页面,模型新增失败,验证失败')
                    try:
                        Method(driver).click('xpath',"//a[text()=\'{}\']/../../../../td[1]/div/div/div[2]/div[1]/span/i".format(modelName))
                        log_file_out('点击通用模型评估图标成功')
                    except:
                        log_file_out('点击通用模型评估图标失败')
                    time.sleep(1)
                    if driver.find_elements_by_class_name('ivu-checkbox-group-item')[0].text == '整车维度':
                        log_file_out('点击评估后,对话框中出现了整车维度,验证成功')
                    else:
                        log_file_out('点击评估后,对话框中没有出现整车维度,验证失败')
                    if len(driver.find_elements_by_class_name('ivu-checkbox-group-item')) == 8:
                        log_file_out('点击评估后,对话框中显示的内容完整,验证成功')
                    else:
                        log_file_out('点击评估后,对话框中显示的内容不完整,验证失败')

                    # 点击评估按钮
                    try:
                        Method(driver).click('xpath','//span[text()="评估"]')

                        log_file_out('点击通用模型评估图标之后出现的评估按钮成功')
                    except:
                        log_file_out('点击通用模型评估图标之后出现的评估按钮失败')
                    time.sleep(1)
                    Method(driver).click('xpath', '//span[text()="{}"]'.format(modelCode))
                    try:
                        a1 = WebDriverWait(driver, wait_time).until(EC.text_to_be_present_in_element(
                            (By.XPATH, "//a[text()=\'{}\']/../../../../td[4]/div/div/span/span".format(modelName)),
                            u'计算异常'))
                        if a1 == True:
                            log_file_out('计算异常,无法评估')
                            return
                    except Exception as e:
                        logger.error(e)

                        a = driver.find_element_by_xpath("//a[text()=\'{}\']/../../../../td[4]/div/div/span/span".format(modelName)).text

                        if a == '计算完成':
                            log_file_out('评估成功')

                            try:
                                # 点击设置为默认模型
                                Method(driver).click('xpath',"//a[text()=\'{}\']/../../../../td[1]/div/div/div[1]/div/span/i".format(
                                                         modelName))
                                log_file_out('设置默认模型成功')
                            except:
                                log_file_out('设置默认模型失败')
                            time.sleep(1)

                            # 点击首页模型配置
                            try:
                                Method(driver).click('xpath',
                                                     "//a[text()=\'{}\']/../../../../td[1]/div/div/div[1]/div/span/i".format(
                                                         modelName))
                                log_file_out('点击首页模型配置按钮成功')
                            except:
                                log_file_out('点击首页模型配置按钮失败')
                            time.sleep(1)
                            # 点击确定按钮
                            Method(driver).click('xpath', '//span[text()="确认"]')

                            # 点击图表按钮
                            try:
                                Method(driver).click('xpath',  "//a[text()=\'{}\']/../../../../td[1]/div/div/div[4]/div/span/i".format(
                                    modelName))

                                log_file_out('点击图表成功')
                            except NoSuchElementException as e:
                                logger.error(e)
                                log_file_out('点击图表失败')
                        else:
                            logger.debug('评估时间太长,评估失败')
                            log_file_out('评估时间太长,评估失败')
                            driver.close()
                else:
                    time.sleep(2)
                    driver.find_element_by_xpath(
                        "//a[text()=\'{}\']/../../../../td[1]/div/div/div[1]/div/span/i".format(modelName)).click()
                    # 如果计算异常 看报错信息是否为计算异常
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                        (By.CLASS_NAME, "ivu-message")))
                    assess_message = driver.find_elements_by_class_name("ivu-message-notice")[1].text

                    try:
                        a1 = WebDriverWait(driver, wait_time).until(EC.text_to_be_present_in_element(
                            (By.XPATH, "//a[text()=\'{}\']/../../../../td[4]/div/div/span/span".format(modelName)), u'计算异常'))
                        if a1 == True:
                            log_file_out('计算异常,无法评估')
                            if assess_message == '计算异常':
                                log_file_out('计算异常后,系统报错信息是计算异常,验证成功')
                            elif assess_message == '保存计算结果失败':
                                log_file_out('计算异常后,系统报错信息是保存计算结果失败,验证失败')
                            else:
                                log_file_out('计算异常后,系统报错信息不是计算异常,验证失败')
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
                                log_file_out('点击图表按钮成功')
                                # 评估完成后点击图表 查看是否报错
                                WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                                    (By.CLASS_NAME, "ivu-message")))
                                picture_message = driver.find_element_by_class_name("ivu-message-notice").text
                                if picture_message == '':
                                    log_file_out('评估完成,点击图表按钮,没有报错,验证成功')
                                else:
                                    log_file_out('评估完成,点击图表按钮,报错,验证失败')

                            except NoSuchElementException as e:
                                logger.error(e)
                                log_file_out('点击图表按钮失败,验证失败')
                        else:
                            logger.debug('评估时间太长,评估失败')
                            log_file_out('评估时间太长,评估失败,评估功能不稳定,验证失败')
                            driver.close()
        else:
            try:
                Method(driver).contains_click('模型导入')
                log_file_out('点击模型导入成功')
            except NoSuchElementException as e:
                logger.error(e)
                log_file_out('点击模型导入失败')

                time.sleep(2)
                try:
                    driver.find_element_by_xpath(
                        "//span[text()=\'{}\']/../../../td[1]/div/label/span/input".format(type)).click()
                    Method(driver).click('xpath', '/html/body/div[17]/div[2]/div/div/div[3]/div/button[2]/span')
                    log_file_out('导入模型成功')
                except NoSuchElementException as e:
                    logger.error(e)
                    log_file_out('导入模型失败')

                time.sleep(2)
                try:
                    Method(driver).click('xpath',
                                         '//*[@id="OM_edit_modal"]/div[2]/div/div/div[3]/div/button[2]/span')
                    log_file_out('保存成功')
                except NoSuchElementException as e:
                    logger.error(e)
                    log_file_out('保存失败')

                time.sleep(2)

                driver.find_element_by_xpath(
                    "//span[text()=\'{}\']/../../../td[1]/div/div/button[2]".format(type)).click()

                try:
                    a1 = WebDriverWait(driver, wait_time).until(EC.text_to_be_present_in_element(
                        (By.XPATH, "//span[text()=\'{}\']/../../../td[4]".format(modelCode)), u'计算异常'))
                    if a1 is True:
                        log_file_out('计算异常,无法评估')
                        driver.close()
                except Exception as e:
                    a = driver.find_element_by_xpath("//span[text()=\'{}\']/../../../td[4]".format(type)).text
                    if a == '计算完成':
                        log_file_out('评估成功')
                        time.sleep(2)
                        try:
                            driver.find_element_by_xpath(
                                "//span[text()=\'{}\']/../../../td[1]/div/div/button[3]".format(type)).click()
                            log_file_out('点击图表成功')
                        except NoSuchElementException as e:
                            logger.error(e)
                            log_file_out('点击图表失败')
                    else:
                        logger.debug('评估时间太长,评估失败')
                        log_file_out('评估时间太长,评估失败')
                        driver.close()
    else:
        log_file_out('登录失败')
    driver.close()

# 敏度分析的新增
def sensitivity_add(url,username,password,contents,modelCode,modelName,type,start,end,car,repairlocation):
    driver = webdriver.Chrome()
    status = Login().login(url, username, password, driver)
    time.sleep(2)
    driver.maximize_window()
    Method(driver).click('id', 'ballb')
    # driver.execute_script("document.body.style.zoom='0.8'")
    if status is True:
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[0])
        log_file_out('---------' + '{}'.format(contents[1]) + '---------')
        # try:
        #     #点击整体维修费用分析
        #     Method(driver).contains_click(contents1)
        #     self.log_file_out('点击' + contents1 + '成功')
        # except NoSuchElementException as e:
        #     self.log_file_out('点击' + contents1 + '失败')
        #     logger.error(e)

        Method(driver).click('xpath', '/html/body/div[1]/header/div[1]/div[1]/div[1]/a/i')
        time.sleep(1)
        for i in contents:
            try:
                Method(driver).contains_click(i)
                log_file_out('点击' + i + '成功')
                time.sleep(1)
            except NoSuchElementException as e:
                log_file_out('点击' + i + '失败')
                logger.error(e)
        time.sleep(1)
        driver.find_element_by_xpath('//span[text()=\'{}\']/../../ul/li'.format(contents[1])).click()
        time.sleep(2)
        try:
            Method(driver).click('xpath','//span[text()="新建内容"]')
            log_file_out('点击新建按钮成功')
        except NoSuchElementException as e:
            logger.debug('点击新建按钮失败')
            logger.error(e)
            log_file_out('点击新建按钮失败')

        time.sleep(3)

        # 录入模型信息
        try:
            Method(driver).input('xpath', "//input[@placeholder='请输入模型编码']", modelCode)
            Method(driver).input('xpath', "//input[@placeholder='请输入模型名称']", modelName)
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


        time.sleep(1)
        if type == '时间':
            # 输入时间
            try:
                Method(driver).input('xpath', "//input[@placeholder='请输入开始日期']", start)
                Method(driver).input('xpath', "//input[@placeholder='请输入结束日期']", end)
                # Method(driver).click('xpath',
                #                      '//*[@id="OM_edit_modal"]/div[2]/div/div/div[2]/div[1]/div[3]/div/div[3]/div[1]/form/div/div/div/div/div/input')
                log_file_out('输入时间成功')
                time.sleep(1)
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
        #点击车型/车号按钮
        Method(driver).click('xpath','//a[text()="车型/车号"]')
        # 选车
        time.sleep(2)
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
            driver.find_elements_by_class_name('power-btnOk')[12].click()
            log_file_out('选车成功')
        except Exception as e:
            logger.error(e)
            log_file_out('选车失败')
            return
        time.sleep(2)

        # 点击构型按钮
        Method(driver).click('xpath', '//a[text()="构型"]')
        time.sleep(1)
        try:
            # 选构型
            Method(driver).select_repairlocation(repairlocation)
            # 点击构型中的确定按钮
            time.sleep(1)
            driver.find_elements_by_class_name('power-btnOk')[-1].click()
            log_file_out('选择构型成功')
        except Exception as e:
            logger.error(e)
            log_file_out('选择构型失败')
        time.sleep(2)
        # 点击确定按钮
        try:
            Method(driver).click('class','power_cardBtn_submit')
            log_file_out('点击确定按钮成功')
        except:
            log_file_out('点击确定按钮失败')
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
            # 调动之前的百分比
            pre = driver.find_element_by_class_name('out2').find_element_by_tag_name('p').text
            # 调动百分比
            Method(driver).input('xpath','//*[@id="showArea"]/input','20')
            time.sleep(2)
            # 调动之后的百分比
            pre_new = driver.find_element_by_class_name('out2').find_element_by_tag_name('p').text
            if pre != pre_new:
                log_file_out('敏度分析调动百分比验证成功')
            else:
                log_file_out('敏度分析调动百分比验证失败')
            # 点击保存按钮
            try:
                driver.find_elements_by_class_name('power-btnOk')[-2].click()
                log_file_out('点击保存按钮成功')
            except Exception as e:
                logger.error(e)
                log_file_out('点击保存按钮失败')
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                (By.CLASS_NAME, "ivu-message-notice")))
            a1 = driver.find_element_by_class_name("ivu-message-notice").text
        except:
            a1 = ''

        if a1 != '':
            log_file_out(a1)
            return


# 占比功能的修改/运维费用统计的修改
def revise(url, username, password, contents, type, modelName, start, end, car, wait_time):
    # option = webdriver.ChromeOptions()
    # option.add_argument("headless")
    # driver = webdriver.Chrome(chrome_options=option
    #                           ,
    #                           executable_path=r'.\apps\chromedriver.exe'
    #                           )

    driver = webdriver.Chrome()
    status = Login().login(url, username, password, driver)
    driver.maximize_window()
    Method(driver).click('id', 'ballb')
    if status is True:
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[0])
        if contents[0] == '运营费用统计' or contents[0] == '运维费用统计' or contents[0] == '通用模型':
            log_file_out('---------' + '{}'.format(contents[0]) + '修改验证---------')
        else:
            log_file_out('---------' + '{}'.format(contents[0]) + '占比分析修改验证---------')

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


        time.sleep(2)
        driver.find_element_by_xpath("//a[text()=\'{}\']".format(modelName)).click()

        time.sleep(2)

        if type == '时间':
            # 输入时间
            try:
                driver.find_element_by_xpath('//input[@placeholder="请输入开始日期"]').send_keys(Keys.CONTROL, 'a')
                driver.find_element_by_xpath("//input[@placeholder='请输入开始日期']").send_keys(Keys.BACK_SPACE)

                Method(driver).input('xpath', "//input[@placeholder='请输入开始日期']", start)

                driver.find_element_by_xpath("//input[@placeholder='请输入结束日期']").send_keys(Keys.CONTROL, 'a')
                driver.find_element_by_xpath("//input[@placeholder='请输入结束日期']").send_keys(Keys.BACK_SPACE)
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
                driver.find_element_by_xpath("//input[@placeholder='请输入开始里程']").send_keys( Keys.CONTROL, 'a')
                driver.find_element_by_xpath("//input[@placeholder='请输入开始里程']").send_keys(Keys.BACK_SPACE)
                Method(driver).input('xpath',"//input[@placeholder='请输入开始里程']",start)
                time.sleep(1)
                driver.find_element_by_xpath("//input[@placeholder='请输入结束里程']").send_keys(Keys.CONTROL, 'a')
                driver.find_element_by_xpath("//input[@placeholder='请输入结束里程']").send_keys(Keys.BACK_SPACE)
                Method(driver).input('xpath', "//input[@placeholder='请输入结束里程']", end)
            except NoSuchElementException as e:
                logger.error(e)
                logger.debug('输入里程失败')
                log_file_out('输入里程失败')

        time.sleep(2)

        # driver.find_element_by_class_name('icon-btn-remove').click()
        Method(driver).click('class','icon-btn-remove')

        # 选车
        select_car = Method(driver).select_car(car)
        if select_car is True:
            log_file_out('选车成功')
        else:
            log_file_out('选车失败')
            return

        try:
            Method(driver).click('xpath', '//span[text()="确认"]')

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
        time.sleep(2)

        if a != '':
            log_file_out(a)
            return
        else:
            if contents[0] == '通用模型':
                time.sleep(2)
                if driver.find_element_by_xpath('//a[text()=\'{}\']/../../../../td[5]/div/div/span'.format(modelName)).text == '默认模型':
                    try:
                        Method(driver).click('xpath',"//a[text()=\'{}\']/../../../../td[1]/div/div/div[3]/div[1]/span/i".format(
                                                 modelName))
                        log_file_out('点击通用模型评估图标成功')
                    except Exception as e:
                        logger.error(e)
                        log_file_out('点击通用模型评估图标失败')
                else:
                    try:
                        Method(driver).click('xpath',
                                             "//a[text()=\'{}\']/../../../../td[1]/div/div/div[2]/div[1]/span/i".format(
                                                 modelName))
                        log_file_out('点击通用模型评估图标成功')
                    except Exception as e:
                        logger.error(e)
                        log_file_out('点击通用模型评估图标失败')
                # 点击评估按钮
                try:
                    Method(driver).click('xpath', '//span[text()="评估"]')

                    log_file_out('点击通用模型评估图标之后出现的评估按钮成功')
                except:
                    log_file_out('点击通用模型评估图标之后出现的评估按钮失败')
                time.sleep(1)
                Method(driver).click('xpath', '//a[text()=\'{}\']/../../../../td[5]/div'.format(modelName))
                try:
                    a1 = WebDriverWait(driver, wait_time).until(EC.text_to_be_present_in_element(
                        (By.XPATH, "//a[text()=\'{}\']/../../../../td[4]/div/div/span/span".format(modelName)),
                        u'计算异常'))
                    if a1 == True:
                        log_file_out('计算异常,无法评估')
                        return
                except Exception as e:
                    logger.error(e)

                    a = driver.find_element_by_xpath(
                        "//a[text()=\'{}\']/../../../../td[4]/div/div/span/span".format(modelName)).text

                    if a == '计算完成':
                        log_file_out('评估成功')
                        time.sleep(1)

                        # 点击图表按钮
                        try:
                            Method(driver).click('xpath',
                                                 "//a[text()=\'{}\']/../../../../td[1]/div/div/div[4]/div/span/i".format(
                                                     modelName))

                            log_file_out('点击图表成功')
                        except NoSuchElementException as e:
                            logger.error(e)
                            log_file_out('点击图表失败')
                    else:
                        logger.debug('评估时间太长,评估失败')
                        log_file_out('评估时间太长,评估失败')
                        driver.close()
            else:
                time.sleep(2)
                driver.find_element_by_xpath(
                    "//a[text()=\'{}\']/../../../../td[1]/div/div/div[1]/div/span/i".format(modelName)).click()

                try:
                    a1 = WebDriverWait(driver, wait_time).until(EC.text_to_be_present_in_element(
                        (By.XPATH, "//a[text()=\'{}\']/../../../../td[4]/div/div/span/span".format(modelName)),
                        u'计算异常'))
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
                                "//a[text()=\'{}\']/../../../../td[1]/div/div/div[2]/div/span/i".format(
                                    modelName)).click()
                            log_file_out('点击图表成功')
                        except NoSuchElementException as e:
                            logger.error(e)
                            log_file_out('点击图表失败')
                    else:
                        logger.debug('评估时间太长,评估失败')
                        log_file_out('评估时间太长,评估失败')

        driver.close()


# 删除
def delete(url, username, password, contents, modelNama):
    # option = webdriver.ChromeOptions()
    # option.add_argument("headless")
    # driver = webdriver.Chrome(chrome_options=option
    #                           ,
    #                           executable_path=r'.\apps\chromedriver.exe'
    #                           )

    driver = webdriver.Chrome()
    status = Login().login(url, username, password, driver)
    if status is True:
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[0])
        if contents[0] == '运营费用统计' or contents[0] == '运维费用统计' or contents[0] == '通用模型':
            log_file_out('---------' + '{}'.format(contents[0]) + '修改验证---------')
        else:
            log_file_out('---------' + '{}'.format(contents[0]) + '占比分析高级搜索框验证---------')

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
        # try:
        #     #点击整体维修费用分析
        #     Method(driver).contains_click(contents1)
        #     self.log_file_out('点击' + contents1 + '成功')
        # except NoSuchElementException as e:
        #     self.log_file_out('点击' + contents1 + '失败')
        #     logger.error(e)

        driver.find_element_by_xpath(
            '//a[text()=\'{}\']/../../../../td[1]/div/label/span/input'.format(modelName)).click()

        time.sleep(2)

        # driver.find_element_by_xpath(
        #     "//a[text()=\'{}\']/../../..//td[@class='ivu-table-column-center']/div/label".format(
        #         modelCode)).click()
        time.sleep(2)
        try:
            Method(driver).click('class','icon-btn-remove-batch')
            driver.find_element_by_xpath('//span[text()="是"]').click()
            log_file_out('删除成功')
        except:
            log_file_out('删除失败')
    else:
        log_file_out('登录失败')


# 自定义车组
def customize_train(url,username,password,contents,car,car_name):
    driver = webdriver.Chrome()
    status = Login().login(url, username, password, driver)
    time.sleep(2)
    driver.maximize_window()
    Method(driver).click('id', 'ballb')

    log_file_out('---------' + '{}'.format(contents[0]) + '新增验证---------')

    # driver.execute_script("document.body.style.zoom='0.8'")
    if status is True:
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[0])

        driver.find_elements_by_class_name('power-collapse-item')[-2].click()
        time.sleep(1)

        try:
            driver.find_elements_by_xpath('//span[text()=\'{}\']'.format(contents[0]))[1].click()
            log_file_out('点击' + contents[0] + '成功')
            time.sleep(1)
        except NoSuchElementException as e:
            log_file_out('点击' + contents[0] + '失败')
            logger.error(e)
        time.sleep(1)
        # 获取所有自定义车组的车组名称
        L = []
        for i in range(0,len(driver.find_elements_by_xpath('//*[@class="ivu-table-tbody"]/tr[1]/td[2]'))):
            L.append(driver.find_elements_by_xpath('//*[@class="ivu-table-tbody"]/tr[1]/td[2]')[i].text)

        try:
            Method(driver).contains_click('新建内容')
            log_file_out('点击新建按钮成功')
        except NoSuchElementException as e:
            logger.debug('点击新建按钮失败')
            logger.error(e)
            log_file_out('点击新建按钮失败')

        # 选车
        try:
            for x in car:
                driver.find_element_by_xpath(
                    "//span[@class='train zoomIn' and contains(text(),\'{}\')]".format(x)).click()
                car_num = car.get(x)
                time.sleep(2)
                if car_num == 'all':
                    driver.find_elements_by_xpath('//span[contains(text(),"全选")]')[0].click()
                else:
                    for i in car_num:
                        driver.find_element_by_xpath(
                            "//*[@class='trainNo-tag old-trainNo-items-off' and text()=\'{}\']".format(i)).click()
                        # time.sleep(2)
                driver.find_elements_by_xpath('//span[contains(text(),"确认")]')[0].click()
                time.sleep(2)
            log_file_out('选车成功')
        except NoSuchElementException as e:
            logger.debug('选车失败')
            logger.error(e)
            log_file_out('选车失败')
        time.sleep(1)
        # 输入车组名称
        Method(driver).input('xpath', "//input[@placeholder='请输入自定义车组名称']", car_name)
        # 点击确定
        try:
            driver.find_elements_by_xpath('//span[text()="确定"]')[1].click()
            log_file_out('点击确定按钮成功')
        except Exception as e:
            logger.error(e)
            log_file_out('点击确定按钮失败')

        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                (By.CLASS_NAME, "ivu-message-notice")))
            a1 = driver.find_element_by_class_name("ivu-message-notice").text
        except:
            a1 = ''

        if a1 != '':
            if a1 == '该车组名称或编码已经存在':
                if car_name in L:
                    log_file_out('自定义车组名称重复,验证成功')
                else:
                    log_file_out('自定义车组名称不重复,验证失败')
            else:
                log_file_out(a1)
                return
        else:
            try:
                driver.find_element_by_xpath('//a[text()=\'{}\']'.format(car_name))
                log_file_out('自定义车组新增成功,验证成功')
            except:
                log_file_out('自定义车组新增失败,验证失败')