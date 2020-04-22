from config.config import *

# 选择9型车 是否会出现其他车型的数据
def rams_bug_nm1(url,username,password,contents,car,fault):
    driver = webdriver.Chrome()
    log_file_out('-----' + contents[1] + '选择9型车 是否会出现其他车型的数据验证' + '-----')
    status = new_built(driver,url,username,password,contents,1)
    if status is True:
        log_file_out('登录成功')
        time.sleep(2)
        # 录入模型信息
        try:
            Method(driver).click('xpath', '//span[text()="请输入评估对象"]')
            time.sleep(1)

            driver.find_elements_by_xpath('//li[text()="评估系统、部件"]')[1].click()

            log_file_out('录入模型基本信息成功')
        except NoSuchElementException as e:
            logger.debug('录入模型基本信息失败')
            logger.error(e)

        time.sleep(1)
        car_status = deal_car(driver, car, 1 ,1)
        if car_status is True:
            log_file_out('选车成功')
        else:
            log_file_out('选车失败')
            return
        time.sleep(2)
        driver.find_element_by_xpath('//*[text()=\'{}\']'.format('下一步')).click()
        time.sleep(5)

        for key in fault:
                driver.find_element_by_xpath(
                    '//*[contains(text(),\'{}\') and @class="el-tree-node__label"]/../span'.format(key)).click()
                time.sleep(1)
                for key1 in fault[key]:
                    driver.find_element_by_xpath(
                        '//*[text()=\'{}\' and @class="el-tree-node__label"]/../label/span'.format(key1)).click()

                driver.find_element_by_xpath('//*[text()=\'{}\']'.format('增加')).click()
                time.sleep(2)
        driver.find_elements_by_class_name('ivu-select-selected-value')[-1].click()
        time.sleep(1)

        driver.find_element_by_xpath('//li[text()="50 条/页"]').click()
        time.sleep(1)
        L = []
        for i in range(0,len(driver.find_elements_by_class_name('ivu-table-column-left'))):
            if driver.find_elements_by_class_name('ivu-table-column-left')[i].text !=  '':
                if len(driver.find_elements_by_class_name('ivu-table-column-left')[i].text.split('.')) > 1:
                    L.append(driver.find_elements_by_class_name('ivu-table-column-left')[i].text.split('.')[0])
        if len(list(set(L))) != 1:
            log_file_out('选择9型车出现其他车型的数据,验证失败')
        else:
            log_file_out('选择9型车没有出现其他车型的数据,验证成功')

    else:
        log_file_out(contents[1]+'模型新增失败')


# 对比模型的修改Bug
def more_model_bug(url,username,password,contents,modelName,car,fault):
    driver = webdriver.Chrome()
    log_file_out('-----' + contents[1] + '修改验证' + '-----')
    status = new_built(driver, url, username, password, contents, 2)
    if status is True:
        log_file_out('登录成功')
        time.sleep(2)
        target = driver.find_elements_by_xpath('//a[text()=\'{}\']'.format(modelName))[0]
        driver.execute_script("arguments[0].scrollIntoView();", target)
        a = len(driver.find_elements_by_xpath('//a[text()=\'{}\']'.format(modelName)))
        for i in range(0, a):
            try:
                driver.find_elements_by_xpath('//a[text()=\'{}\']'.format(modelName))[i].click()
                ## 获取点击评估的时间
                break
            except:
                pass
        time.sleep(2)
        try:
            driver.find_elements_by_xpath('//span[text()=\'{}\']'.format('新增'))[1].click()
            log_file_out('点击新增有反应')
        except:
            log_file_out('点击新增没有反应')
        if len(driver.find_elements_by_css_selector(
                '[class="ivu-checkbox-wrapper ivu-checkbox-wrapper-checked ivu-checkbox-large"]')) == 1:
            pass
        else:
            driver.find_element_by_xpath('//*[contains(text(),\'{}\')]'.format('是否根据车型选择')).click()
        time.sleep(2)
        driver.find_elements_by_xpath('//span[text()="删除"]')[1].click()
        deal_car(driver, car, 0, 1)

        driver.find_element_by_xpath('//*[text()=\'{}\']'.format('下一步')).click()
        time.sleep(5)
        fault_status = deal_union(driver, fault)
        if fault_status is True:
            log_file_out('选择部件成功')
        else:
            log_file_out('选择部件失败')

        driver.find_elements_by_xpath('//span[text()="确定"]')[1].click()
        time.sleep(2)
        try:
            driver.find_element_by_xpath('//span[text()="保存"]').click()
            log_file_out('点击保存按钮成功')
        except NoSuchElementException as e:
            logger.error(e)
        except:
            log_file_out('点击保存失败')
        if len(driver.find_elements_by_xpath('//a[text()=\'{}\']'.format(modelName))) > 0:
            log_file_out('保存模型成功')
        else:
            log_file_out('保存模型失败')

        time.sleep(2)
        a = len(driver.find_elements_by_xpath('//a[text()=\'{}\']'.format(modelName)))
        for i in range(0, a):
            try:
                driver.find_elements_by_xpath('//a[text()=\'{}\']'.format(modelName))[i].click()

                break
            except:
                pass
        time.sleep(2)
        try:
            driver.find_elements_by_xpath('//span[text()=\'{}\']'.format('新增'))[1].click()
            log_file_out('点击新增有反应')
        except:
            log_file_out('点击新增没有反应')

        if len(driver.find_elements_by_css_selector(
                '[class="ivu-checkbox-wrapper ivu-checkbox-wrapper-checked ivu-checkbox-large"]')) == 1:
            log_file_out('操作”是否根据车型选择“之后,该操作被记,验证成功')
        else:
            log_file_out('操作”是否根据车型选择“之后,该操作没有被记,验证失败')

        time.sleep(2)
        driver.find_element_by_xpath('//*[text()=\'{}\']'.format('下一步')).click()
        time.sleep(5)
        if len(driver.find_elements_by_class_name('el-tree-node__label')) > 1:
            log_file_out('故障对象回显成功,验证成功')
        else:
            log_file_out('故障对象回显失败,验证失败')


# 技术变更报表出错
def technical_bug(url,username,password,contents,modelName):
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    log_file_out('-----' + contents[1] + '报表验证' + '-----')
    status = new_built(driver, url, username, password, contents, 2)
    if status is True:
        log_file_out('登录成功')
        time.sleep(2)

        target = driver.find_elements_by_xpath('//a[text()=\'{}\']'.format(modelName))[0]
        driver.execute_script("arguments[0].scrollIntoView();", target)
        try:
            a = len(driver.find_elements_by_xpath('//a[text()=\'{}\']/../../../td[6]/div/a[5]'.format(modelName)))
            for i in range(0, a):
                try:
                    driver.find_elements_by_xpath(
                        '//a[text()=\'{}\']/../../../td[6]/div/a[5]'.format(modelName))[
                        i].click()
                    break
                except:
                    pass
            log_file_out('点击报表按钮成功')
        except WebDriverException:
            log_file_out('点击报表按钮失败')
            return

        time.sleep(2)
        if len(driver.find_elements_by_xpath('//div[text()="运用概况"]')) == 0:
            log_file_out('技术变更报表未出现结果,验证失败')
        else:
            log_file_out('技术变更报表出现结果,验证成功')

# 分页 50/页 删除模型 页面被重置
def paging_bug(url,username,password,contents,modelName):
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    log_file_out('-----' + contents[1] + '分页验证' + '-----')
    status = new_built(driver, url, username, password, contents, 2)
    if status is True:
        log_file_out('登录成功')
        time.sleep(2)

        Method(driver).click('class','ivu-select-selected-value')
        time.sleep(1)
        driver.find_element_by_xpath('//li[text()="40 条/页"]').click()
        time.sleep(2)
        try:
            a = len(driver.find_elements_by_xpath('//a[text()=\'{}\']/../../../td[6]/div/a[7]'.format(modelName)))
            for i in range(0, a):
                try:
                    driver.find_elements_by_xpath(
                        '//a[text()=\'{}\']/../../../td[6]/div/a[7]'.format(modelName))[
                        i].click()
                    break
                except:
                    pass
            log_file_out('点击删除按钮成功')
        except WebDriverException:
            log_file_out('点击删除按钮失败')
            return

        time.sleep(2)
        if driver.find_element_by_class_name('ivu-select-selected-value').text == '40 条/页':
            log_file_out('选择40/页,删除当前页面的数据以后,页面没有重置,验证成功')
        else:
            log_file_out('选择40/页,删除当前页面的数据以后,页面没有重置,y验证失败')


# 验证中间值
def median_check(url,username,password,contents,modelName):
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    log_file_out('-----' + contents[1] + '中间值验证' + '-----')
    status = new_built(driver, url, username, password, contents, 2)
    if status is True:
        log_file_out('登录成功')
        time.sleep(2)

        target = driver.find_elements_by_xpath('//a[text()=\'{}\']'.format(modelName))[0]
        driver.execute_script("arguments[0].scrollIntoView();", target)
        time.sleep(2)
        try:
            a = len(driver.find_elements_by_xpath('//a[text()=\'{}\']/../../../td[7]/div/a[6]'.format(modelName)))
            for i in range(0, a):
                try:
                    driver.find_elements_by_xpath('//a[text()=\'{}\']/../../../td[7]/div/a[6]'.format(modelName))[i].click()
                    break
                except:
                    pass
            log_file_out('点击中间值按钮成功')
        except WebDriverException:
            log_file_out('点击中间值按钮失败')
            return
        time.sleep(2)
        # 设置图表保存目录为bin下面picture下面的incontrol_picture 图片中路径要为"\\"
        wholepath = os.path.dirname(__file__) + '\\' + 'picture' + '\\median_picture'
        # 判断目录是否存在
        if os.path.isdir(wholepath) is True:
            pass
        else:
            os.mkdir(wholepath)

        time.sleep(2)

        driver.save_screenshot(wholepath + '\\' + '中间值' + '.png')


