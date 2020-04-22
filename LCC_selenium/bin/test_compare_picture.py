from config.config import *



# 整车对比
def carload_compare_picture(url,username,password,contents,modelName):

    driver = webdriver.Chrome()
    status = Login().login(url, username, password, driver)
    time.sleep(2)
    driver.maximize_window()
    Method(driver).click('id', 'ballb')
    # driver.execute_script("document.body.style.zoom='0.8'")
    if status is True:
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[0])
        log_file_out('---------' + '{}'.format(contents[1]) + '费用对比分析图表---------')

        time.sleep(1)
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
        # 点击图表按钮
        try:
            Method(driver).click('xpath','//a[text()=\'{}\']/../../../../td[1]/div/div/div[2]/div/span/i'.format(modelName))

            log_file_out('点击图表成功')
        except NoSuchElementException as e:
            logger.error(e)
            log_file_out('点击图表失败')

        try:
            time.sleep(2)
            # 设置图表下载路径为picture下面的car_load下
            car_load_picture_path = os.path.dirname(__file__) + '\\' + 'picture' + '\\car_load'
            if os.path.isdir(car_load_picture_path) is True:
                pass
            else:
                os.mkdir(car_load_picture_path)

            driver.save_screenshot(car_load_picture_path + '\\' + '整车总费用对比分析' + '.png')

            Method(driver).click('xpath', '//*[contains(text(),"修复性维修")]')
            time.sleep(1)
            driver.save_screenshot(car_load_picture_path + '\\'  + '整车修复性维修对比分析' + '.png')
            Method(driver).click('xpath', '//*[contains(text(),"预防性维修")]')
            time.sleep(1)

            driver.save_screenshot(car_load_picture_path + '\\' + '整车预防性维修对比分析' + '.png')
            log_file_out('截取图表成功')
        except:
            log_file_out('截取图表失败')

# 车型对比
def cartype_compare_picture(url,username,password,contents,modelName):
    # 设置excel保存目录为bin下面download_excel下面的car_type 图片中路径要为"\\"
    car_type = os.path.dirname(__file__) + '\\' + 'download_excel' + '\\car_type'
    if os.path.isdir(car_type) is True:
        pass
    else:
        os.mkdir(car_type)
    options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_settings.popups': 0,
             'download.default_directory': '{}\\bin\\download_excel\\car_type'.format(path_dir),
             "profile.default_content_setting_values.automatic_downloads": 1}
    options.add_experimental_option('prefs', prefs)

    driver = webdriver.Chrome(chrome_options=options)
    status = Login().login(url, username, password, driver)
    time.sleep(2)
    driver.maximize_window()
    Method(driver).click('id', 'ballb')
    # driver.execute_script("document.body.style.zoom='0.8'")
    if status is True:
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[0])
        log_file_out('---------' + '{}'.format(contents[0]) + '费用对比分析图表---------')

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
        # 点击图表按钮
        try:
            Method(driver).click('xpath','//a[text()=\'{}\']/../../../../td[1]/div/div/div[2]/div/span/i'.format(modelName))

            log_file_out('点击图表成功')
        except NoSuchElementException as e:
            logger.error(e)
            log_file_out('点击图表失败')
        # 判断excel是否存在
        if os.path.exists('{}\\bin\\download_excel\\car_type'.format(path_dir) + '\\' + '车型维度-对比分析.xlsx'):
            os.remove(
                '{}\\bin\\download_excel\\car_type'.format(path_dir) + '\\' + '车型维度-对比分析.xlsx')
        else:
            pass

        time.sleep(2)
        Method(driver).click('xpath', '//span[text()="一键下载"]')
        time.sleep(2)
        if os.path.exists('{}\\bin\\download_excel\\car_type'.format(path_dir) + '\\' + '车型维度-对比分析.xlsx'):
            log_file_out('一键下载成功,验证成功')
        else:
            log_file_out('一键下载失败,验证失败')
        try:
            time.sleep(2)
            # 设置图表下载路径为picture下面的car_type下
            car_type_picture_path = os.path.dirname(__file__) + '\\' + 'picture' + '\\car_type'
            if os.path.isdir(car_type_picture_path) is True:
                pass
            else:
                os.mkdir(car_type_picture_path)
            target = driver.find_elements_by_class_name('ivu-card-body')[1]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            driver.save_screenshot(car_type_picture_path + '\\' + '车型对比工时数_物料费_人工费' + '.png')

            Method(driver).click('xpath', '//*[contains(text(),"材料数")]')
            time.sleep(1)
            driver.save_screenshot(car_type_picture_path + '\\'  + '车型对比材料数' + '.png')
            target = driver.find_elements_by_class_name('ivu-card-body')[5]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            time.sleep(1)

            driver.save_screenshot(car_type_picture_path + '\\' + '车型对比维修级别_维修类别' + '.png')
            target = driver.find_elements_by_class_name('ivu-card-body')[7]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            time.sleep(1)

            driver.save_screenshot(car_type_picture_path + '\\' + '车型对比定偶检' + '.png')
            log_file_out('截取图表成功')
        except:
            log_file_out('截取图表失败')

# 维修及维修保障维度对比
def repair_compare_picture(url, username, password, contents, modelName):
    # 设置excel保存目录为bin下面download_excel下面的repair 图片中路径要为"\\"
    repair = os.path.dirname(__file__) + '\\' + 'download_excel' + '\\repair'
    if os.path.isdir(repair) is True:
        pass
    else:
        os.mkdir(repair)
    options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_settings.popups': 0,
             'download.default_directory': '{}\\bin\\download_excel\\repair'.format(path_dir),
             "profile.default_content_setting_values.automatic_downloads": 1}
    options.add_experimental_option('prefs', prefs)

    driver = webdriver.Chrome(chrome_options=options)
    status = Login().login(url, username, password, driver)
    time.sleep(2)
    driver.maximize_window()
    Method(driver).click('id', 'ballb')
    # driver.execute_script("document.body.style.zoom='0.8'")
    if status is True:
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[0])
        log_file_out('---------' + '{}'.format(contents[1]) + '费用对比图表---------')

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
        # 点击图表按钮
        try:
            Method(driver).click('xpath',
                                 '//a[text()=\'{}\']/../../../../td[1]/div/div/div[2]/div/span/i'.format(
                                     modelName))

            log_file_out('点击图表成功')
        except NoSuchElementException as e:
            logger.error(e)
            log_file_out('点击图表失败')
        time.sleep(2)
        # 判断excel是否存在
        if os.path.exists('{}\\bin\\download_excel\\repair'.format(path_dir) + '\\' + '维修及维修保障维度-对比分析.xlsx'):
            os.remove(
                '{}\\bin\\download_excel\\repair'.format(path_dir) + '\\' + '维修及维修保障维度-对比分析.xlsx')
        else:
            pass

        time.sleep(2)
        Method(driver).click('xpath', '//span[text()="一键下载"]')
        time.sleep(2)
        if os.path.exists('{}\\bin\\download_excel\\repair'.format(path_dir) + '\\' + '维修及维修保障维度-对比分析.xlsx'):
            log_file_out('一键下载成功,验证成功')
        else:
            log_file_out('一键下载失败,验证失败')

        try:
            time.sleep(2)
            # 设置图表下载路径为picture下面的repair下
            repair_picture_path = os.path.dirname(__file__) + '\\' + 'picture' + '\\repair'
            if os.path.isdir(repair_picture_path) is True:
                pass
            else:
                os.mkdir(repair_picture_path)

            target = driver.find_elements_by_class_name('ivu-card-body')[1]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            driver.save_screenshot(repair_picture_path + '\\' + '维修及维修保障对比工具_耗材总费用' + '.png')
            time.sleep(1)
            target = driver.find_elements_by_class_name('ivu-card-body')[5]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            driver.save_screenshot(repair_picture_path + '\\' + '维修及维修保障对比备件总费用' + '.png')
            time.sleep(1)
            Method(driver).click('xpath', '//*[contains(text(),"修复性维修")]')
            target = driver.find_elements_by_class_name('ivu-card-body')[1]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            driver.save_screenshot(repair_picture_path + '\\' + '维修及维修保障对比工具_耗材修复性费用' + '.png')
            time.sleep(1)
            target = driver.find_elements_by_class_name('ivu-card-body')[5]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            driver.save_screenshot(repair_picture_path + '\\' + '维修及维修保障对比备件修复性费用' + '.png')
            time.sleep(1)
            Method(driver).click('xpath', '//*[contains(text(),"预防性维修")]')
            target = driver.find_elements_by_class_name('ivu-card-body')[1]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            driver.save_screenshot(repair_picture_path + '\\' + '维修及维修保障对比工具_耗材预防性费用' + '.png')
            time.sleep(1)
            target = driver.find_elements_by_class_name('ivu-card-body')[5]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            driver.save_screenshot(repair_picture_path + '\\' + '维修及维修保障对比备件预防性费用' + '.png')
            log_file_out('截取图表成功')
        except Exception as e:
            logger.error(e)
            log_file_out('截取图表失败')

# 路局/线路对比
def railway_compare_picture(url, username, password, contents, modelName):
    # 设置excel保存目录为bin下面download_excel下面的railway 图片中路径要为"\\"
    railway = os.path.dirname(__file__) + '\\' + 'download_excel' + '\\railway'
    if os.path.isdir(railway) is True:
        pass
    else:
        os.mkdir(railway)
    options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_settings.popups': 0,
             'download.default_directory': '{}\\bin\\download_excel\\railway'.format(path_dir),
             "profile.default_content_setting_values.automatic_downloads": 1}
    options.add_experimental_option('prefs', prefs)

    driver = webdriver.Chrome(chrome_options=options)
    status = Login().login(url, username, password, driver)
    time.sleep(2)
    driver.maximize_window()
    Method(driver).click('id', 'ballb')
    # driver.execute_script("document.body.style.zoom='0.8'")
    if status is True:
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[0])
        log_file_out('---------' + '{}'.format(contents[0]) + '费用对比图表---------')
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
        # 点击图表按钮
        try:
            Method(driver).click('xpath','//a[text()=\'{}\']/../../../../td[1]/div/div/div[2]/div/span/i'.format(modelName))

            log_file_out('点击图表成功')
        except NoSuchElementException as e:
            logger.error(e)
            log_file_out('点击图表失败')
        # 判断excel是否存在
        if os.path.exists('{}\\bin\\download_excel\\railway'.format(path_dir) + '\\' + '路局_线路维度-对比分析.xlsx'):
            os.remove(
                '{}\\bin\\download_excel\\railway'.format(path_dir) + '\\' + '路局_线路维度-对比分析.xlsx')
        else:
            pass

        time.sleep(2)
        Method(driver).click('xpath', '//span[text()="一键下载"]')
        time.sleep(2)
        if os.path.exists('{}\\bin\\download_excel\\railway'.format(path_dir) + '\\' + '路局_线路维度-对比分析.xlsx'):
            log_file_out('一键下载成功,验证成功')
        else:
            log_file_out('一键下载失败,验证失败')

        try:
            time.sleep(2)
            # 设置图表下载路径为picture下面的railway下
            railway_picture_path = os.path.dirname(__file__) + '\\' + 'picture' + '\\railway'
            if os.path.isdir(railway_picture_path) is True:
                pass
            else:
                os.mkdir(railway_picture_path)

            target = driver.find_elements_by_class_name('ivu-card-body')[1]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            driver.save_screenshot(railway_picture_path + '\\' + '路局对比工时数量' + '.png')
            time.sleep(1)
            driver.find_elements_by_class_name('ivu-btn-default')[1].click()

            driver.save_screenshot(railway_picture_path + '\\' + '路局对比人工费' + '.png')
            time.sleep(1)

            target = driver.find_elements_by_class_name('ivu-card-body')[3]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            driver.save_screenshot(railway_picture_path + '\\' + '路局对比材料数量' + '.png')
            time.sleep(1)
            driver.find_elements_by_class_name('ivu-btn-default')[4].click()

            driver.save_screenshot(railway_picture_path + '\\' + '路局对比物料费' + '.png')
            time.sleep(1)
            target = driver.find_elements_by_class_name('ivu-card-body')[5]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            driver.save_screenshot(railway_picture_path + '\\' + '路局对比维修级别及类型' + '.png')
            time.sleep(1)
            target = driver.find_elements_by_class_name('ivu-card-body')[7]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            driver.save_screenshot(railway_picture_path + '\\' + '路局对比定偶检' + '.png')
            log_file_out('截取图表成功')
        except Exception as e:
            logger.error(e)
            log_file_out('截取图表失败')

# 供应商对比
def supplier_compare_picture(url, username, password, contents, modelname):
    # 设置excel保存目录为bin下面download_excel下面的supplier 图片中路径要为"\\"
    supplier = os.path.dirname(__file__) + '\\' + 'download_excel' + '\\supplier'
    if os.path.isdir(supplier) is True:
        pass
    else:
        os.mkdir(supplier)

    options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_settings.popups': 0,
             'download.default_directory': '{}\\bin\\download_excel\\supplier'.format(path_dir),
             "profile.default_content_setting_values.automatic_downloads": 1}
    options.add_experimental_option('prefs', prefs)

    driver = webdriver.Chrome(chrome_options=options)
    status = Login().login(url, username, password, driver)
    time.sleep(2)
    driver.maximize_window()
    Method(driver).click('id', 'ballb')
    # driver.execute_script("document.body.style.zoom='0.8'")
    if status is True:
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[0])
        log_file_out('---------' + '{}'.format(contents[0]) + '费用对比图表---------')
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
        # 点击图表按钮
        try:
            Method(driver).click('xpath','//a[text()=\'{}\']/../../../../td[1]/div/div/div[2]/div/span/i'.format(modelname))

            log_file_out('点击图表成功')
        except NoSuchElementException as e:
            logger.error(e)
            log_file_out('点击图表失败')
        # 判断excel是否存在
        if os.path.exists('{}\\bin\\download_excel\\supplier'.format(path_dir) + '\\' + '供应商维度-对比分析.xlsx'):
            os.remove(
                '{}\\bin\\download_excel\\supplier'.format(path_dir) + '\\' + '供应商维度-对比分析.xlsx')
        else:
            pass

        time.sleep(2)
        Method(driver).click('xpath', '//span[text()="一键下载"]')
        time.sleep(2)
        if os.path.exists('{}\\bin\\download_excel\\supplier'.format(path_dir) + '\\' + '供应商维度-对比分析.xlsx'):
            log_file_out('一键下载成功,验证成功')
        else:
            log_file_out('一键下载失败,验证失败')

        try:
            time.sleep(2)
            # 设置图表下载路径为picture下面的supplier下
            supplier_picture_path = os.path.dirname(__file__) + '\\' + 'picture' + '\\supplier'
            if os.path.isdir(supplier_picture_path) is True:
                pass
            else:
                os.mkdir(supplier_picture_path)

            target = driver.find_elements_by_class_name('ivu-card-body')[1]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            driver.save_screenshot(supplier_picture_path + '\\' + '供应商对比工时数_物料费人工费' + '.png')
            time.sleep(1)
            driver.find_elements_by_class_name('ivu-btn-default')[1].click()

            driver.save_screenshot(supplier_picture_path + '\\' + '供应商对比材料数' + '.png')
            time.sleep(1)

            target = driver.find_elements_by_class_name('ivu-card-body')[5]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            driver.save_screenshot(supplier_picture_path + '\\' + '供应商对比维修级别及类型' + '.png')
            time.sleep(1)
            target = driver.find_elements_by_class_name('ivu-card-body')[7]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            driver.save_screenshot(supplier_picture_path + '\\' + '供应商对比定偶检' + '.png')
            time.sleep(1)
            target = driver.find_elements_by_class_name('ivu-card-body')[-1]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            driver.save_screenshot(supplier_picture_path + '\\' + '供应商对比问题构型平均数对比' + '.png')
            log_file_out('截取图表成功')
        except Exception as e:
            logger.error(e)
            log_file_out('截取图表失败')

# 系统部件对比
def system_unit_compare_picture(url, username, password, contents, modelName):
    # 设置excel保存目录为bin下面download_excel下面的system 图片中路径要为"\\"
    system = os.path.dirname(__file__) + '\\' + 'download_excel' + '\\system'
    if os.path.isdir(system) is True:
        pass
    else:
        os.mkdir(system)
    options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_settings.popups': 0,
             'download.default_directory': '{}\\bin\\download_excel\\system'.format(path_dir),
             "profile.default_content_setting_values.automatic_downloads": 1}
    options.add_experimental_option('prefs', prefs)

    driver = webdriver.Chrome(chrome_options=options)
    status = Login().login(url, username, password, driver)
    time.sleep(2)
    driver.maximize_window()
    Method(driver).click('id', 'ballb')
    # driver.execute_script("document.body.style.zoom='0.8'")
    if status is True:
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[0])
        log_file_out('---------' + '{}'.format(contents[0]) + '费用对比图表---------')
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
        # 点击图表按钮
        try:
            Method(driver).click('xpath','//a[text()=\'{}\']/../../../../td[1]/div/div/div[2]/div/span/i'.format(modelName))

            log_file_out('点击图表成功')
        except NoSuchElementException as e:
            logger.error(e)
            log_file_out('点击图表失败')
        # 判断excel是否存在
        if os.path.exists('{}\\bin\\download_excel\\system'.format(path_dir) + '\\' + '系统部件维度-对比分析.xlsx'):
            os.remove(
                '{}\\bin\\download_excel\\system'.format(path_dir) + '\\' + '系统部件维度-对比分析.xlsx')
        else:
            pass

        time.sleep(2)
        Method(driver).click('xpath', '//span[text()="一键下载"]')
        time.sleep(2)
        if os.path.exists('{}\\bin\\download_excel\\system'.format(path_dir) + '\\' + '系统部件维度-对比分析.xlsx'):
            log_file_out('一键下载成功,验证成功')
        else:
            log_file_out('一键下载失败,验证失败')

        try:
            time.sleep(2)
            # 设置图表下载路径为picture下面的system下
            system_picture_path = os.path.dirname(__file__) + '\\' + 'picture' + '\\system'
            if os.path.isdir(system_picture_path) is True:
                pass
            else:
                os.mkdir(system_picture_path)


            target = driver.find_elements_by_class_name('ivu-card-body')[1]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            driver.save_screenshot(system_picture_path + '\\' + '系统部件对比工时数_物料费人工费' + '.png')
            time.sleep(1)
            driver.find_elements_by_class_name('ivu-btn-default')[1].click()

            driver.save_screenshot(system_picture_path + '\\' + '系统部件对比材料数' + '.png')
            time.sleep(1)

            target = driver.find_elements_by_class_name('ivu-card-body')[5]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            driver.save_screenshot(system_picture_path + '\\' + '系统部件对比维修级别及类型' + '.png')
            time.sleep(1)
            target = driver.find_elements_by_class_name('ivu-card-body')[7]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            driver.save_screenshot(system_picture_path + '\\' + '系统部件对比定偶检' + '.png')
            log_file_out('截取图表成功')
        except Exception as e:
            logger.error(e)
            log_file_out('截取图表失败')

# 生产车间/生产线对比
def workshop_compare_picture(url, username, password, contents, modelName):
    # 设置excel保存目录为bin下面download_excel下面的workshop 图片中路径要为"\\"
    workshop = os.path.dirname(__file__) + '\\' + 'download_excel' + '\\workshop'
    if os.path.isdir(workshop) is True:
        pass
    else:
        os.mkdir(workshop)
    options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_settings.popups': 0,
             'download.default_directory': '{}\\bin\\download_excel\\workshop'.format(path_dir),
             "profile.default_content_setting_values.automatic_downloads": 1}
    options.add_experimental_option('prefs', prefs)

    driver = webdriver.Chrome(chrome_options=options)
    status = Login().login(url, username, password, driver)
    time.sleep(2)
    driver.maximize_window()
    Method(driver).click('id', 'ballb')
    # driver.execute_script("document.body.style.zoom='0.8'")
    if status is True:
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[0])
        log_file_out('---------' + '{}'.format(contents[0]) + '费用对比图表---------')
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
        # 点击图表按钮
        try:
            Method(driver).click('xpath','//a[text()=\'{}\']/../../../../td[1]/div/div/div[2]/div/span/i'.format(modelName))

            log_file_out('点击图表成功')
        except NoSuchElementException as e:
            logger.error(e)
            log_file_out('点击图表失败')
        time.sleep(2)
        # 判断excel是否存在
        if os.path.exists('{}\\bin\\download_excel\\workshop'.format(path_dir) + '\\' + '生产车间_生产线维度-对比分析.xlsx'):
            os.remove(
                '{}\\bin\\download_excel\\workshop'.format(path_dir) + '\\' + '生产车间_生产线维度-对比分析.xlsx')
        else:
            pass

        time.sleep(2)
        Method(driver).click('xpath', '//span[text()="一键下载"]')
        time.sleep(2)
        if os.path.exists('{}\\bin\\download_excel\\workshop'.format(path_dir) + '\\' + '生产车间_生产线维度-对比分析.xlsx'):
            log_file_out('一键下载成功,验证成功')
        else:
            log_file_out('一键下载失败,验证失败')

        try:
            time.sleep(2)
            # 设置图表下载路径为picture下面的workshop下
            workshop_picture_path = os.path.dirname(__file__) + '\\' + 'picture' + '\\workshop'
            if os.path.isdir(workshop_picture_path) is True:
                pass
            else:
                os.mkdir(workshop_picture_path)

            target = driver.find_elements_by_class_name('ivu-card-body')[1]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            driver.save_screenshot(workshop_picture_path + '\\' +'生产车间对比工时数' + '.png')
            time.sleep(1)
            driver.find_elements_by_class_name('ivu-btn-default')[1].click()

            driver.save_screenshot(workshop_picture_path + '\\' +'生产车间对比人工费' + '.png')
            time.sleep(1)

            target = driver.find_elements_by_class_name('ivu-card-body')[3]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            driver.save_screenshot(workshop_picture_path + '\\' +'生产车间对比材料数' + '.png')
            time.sleep(1)
            driver.find_elements_by_class_name('ivu-btn-default')[4].click()
            target = driver.find_elements_by_class_name('ivu-card-body')[3]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            driver.save_screenshot(workshop_picture_path + '\\' + '生产车间对比物料费' + '.png')
            time.sleep(1)
            target = driver.find_elements_by_class_name('ivu-card-body')[5]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            driver.save_screenshot(workshop_picture_path + '\\' + '生产车间对比维修级别及维修类型' + '.png')
            time.sleep(1)
            target = driver.find_elements_by_class_name('ivu-card-body')[-1]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            driver.save_screenshot(workshop_picture_path + '\\' +'生产车间对比定偶检' + '.png')
            log_file_out('截取图表成功')
        except Exception as e:
            logger.error(e)
            log_file_out('截取图表失败')

# 高级修对比
def high_repair_compare_picture(url, username, password, contents, modelName):
    # 设置excel保存目录为bin下面download_excel下面的high_repair 图片中路径要为"\\"
    high_repair = os.path.dirname(__file__) + '\\' + 'download_excel' + '\\high_repair'
    if os.path.isdir(high_repair) is True:
        pass
    else:
        os.mkdir(high_repair)
    options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_settings.popups': 0,
             'download.default_directory': '{}\\bin\\download_excel\\high_repair'.format(path_dir),
             "profile.default_content_setting_values.automatic_downloads": 1}
    options.add_experimental_option('prefs', prefs)

    driver = webdriver.Chrome(chrome_options=options)
    status = Login().login(url, username, password, driver)
    time.sleep(2)
    driver.maximize_window()
    Method(driver).click('id', 'ballb')
    # driver.execute_script("document.body.style.zoom='0.8'")
    if status is True:
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[0])
        log_file_out('---------' + '{}'.format(contents[0]) + '费用对比图表---------')
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
        # 点击图表按钮
        try:
            Method(driver).click('xpath','//a[text()=\'{}\']/../../../../td[1]/div/div/div[2]/div/span/i'.format(modelName))

            log_file_out('点击图表成功')
        except NoSuchElementException as e:
            logger.error(e)
            log_file_out('点击图表失败')
        # 判断excel是否存在
        if os.path.exists('{}\\bin\\download_excel\\high_repair'.format(path_dir) + '\\' + '高级修维度-对比分析.xlsx'):
            os.remove(
                '{}\\bin\\download_excel\\high_repair'.format(path_dir) + '\\' + '高级修维度-对比分析.xlsx')
        else:
            pass

        time.sleep(2)
        Method(driver).click('xpath', '//span[text()="一键下载"]')
        time.sleep(2)
        if os.path.exists('{}\\bin\\download_excel\\high_repair'.format(path_dir) + '\\' + '高级修维度-对比分析.xlsx'):
            log_file_out('一键下载成功,验证成功')
        else:
            log_file_out('一键下载失败,验证失败')

        try:
            time.sleep(2)
            # 设置图表下载路径为picture下面的high_repair下
            high_repair_picture_path = os.path.dirname(__file__) + '\\' + 'picture' + '\\high_repair'
            if os.path.isdir(high_repair_picture_path) is True:
                pass
            else:
                os.mkdir(high_repair_picture_path)

            target = driver.find_elements_by_class_name('ivu-card-body')[1]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            driver.save_screenshot(high_repair_picture_path + '\\' +'高级修对比工时数_物料费_人工费' + '.png')
            time.sleep(1)
            # 点击材料数
            driver.find_elements_by_class_name('ivu-btn-default')[1].click()
            target = driver.find_elements_by_class_name('ivu-card-body')[1]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            driver.save_screenshot(high_repair_picture_path + '\\' +'高级修对比材料数' + '.png')
            time.sleep(1)

            target = driver.find_elements_by_class_name('ivu-card-body')[5]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            driver.save_screenshot(high_repair_picture_path + '\\' + '高级修对比维修级别及维修类型' + '.png')
            time.sleep(1)
            target = driver.find_elements_by_class_name('ivu-card-body')[8]
            driver.execute_script("arguments[0].scrollIntoView();", target)

            driver.save_screenshot(high_repair_picture_path + '\\' +'高级修对比定偶检' + '.png')
            log_file_out('截取图表成功')
        except Exception as e:
            logger.error(e)
            log_file_out('截取图表失败')

