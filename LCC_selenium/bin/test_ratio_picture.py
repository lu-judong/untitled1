from config.config import *


# 运维费用统计图表
def whole_picture(url,username,password,contents,modelname,car):
    # 设置excel保存目录为bin下面download_excel下面的whole_excel_path 图片中路径要为"\\"
    whole_excel_path = os.path.dirname(__file__) + '\\' + 'download_excel' + '\\whole_model'
    if os.path.isdir(whole_excel_path) is True:
        pass
    else:
        os.mkdir(whole_excel_path)

    options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_settings.popups': 0,
             'download.default_directory': '{}\\test_picture\\download_excel\\whole_model'.format(path_dir),
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
        log_file_out('---------' + '{}'.format(contents[1]) + '费用占比分析---------')

        driver.find_elements_by_class_name('power-collapse-item')[0].click()
        time.sleep(1)

        try:
            driver.find_elements_by_xpath('//span[text()=\'{}\']'.format(contents[0]))[1].click()
            log_file_out('点击' + contents[0] + '成功')
            time.sleep(1)
        except NoSuchElementException as e:
            log_file_out('点击' + contents[0] + '失败')
            logger.error(e)
        time.sleep(1)
        # 点击图表按钮
        try:
            Method(driver).click('xpath','//a[text()=\'{}\']/../../../../td[1]/div/div/div[2]/div/span/i'.format(modelname))

            log_file_out('点击图表成功')
        except NoSuchElementException as e:
            logger.error(e)
            log_file_out('点击图表失败')
        time.sleep(2)
        # 判断运维费用统计下excel是否存在
        if os.path.exists('{}\\bin\\download_excel\\whole_model'.format(path_dir) + '\\' + '运维费用统计-费用分析.xlsx'):
            os.remove('{}\\bin\\download_excel\\whole_model'.format(path_dir) + '\\' + '运维费用统计-费用分析.xlsx')
        else:
            pass
        Method(driver).click('xpath','//span[text()="一键下载"]')
        time.sleep(2)
        if os.path.exists('{}\\bin\\download_excel\\whole_model'.format(path_dir) + '\\' + '运维费用统计-费用分析.xlsx'):
            log_file_out('\'{}\'一键下载成功,验证成功'.format(contents[0]))
        else:
            log_file_out('\'{}\'一键下载失败,验证失败'.format(contents[0]))

        try:
            time.sleep(2)
            # 设置图表下载路径为picture下面的whole_model下
            whole_picture_path = os.path.dirname(__file__) + '\\' + 'picture' + '\\whole_model'
            if os.path.isdir(whole_picture_path) is True:
                pass
            else:
                os.mkdir(whole_picture_path)

            driver.save_screenshot('{}\\picture'.format(whole_picture_path) + '\\' + '整体费用图表' + '.png')
        except:
            log_file_out('截取整体费用图表失败')
        try:
            for i in car:
                Method(driver).click('xpath', '//span[text()="{}"]/../../../../td[1]/div'.format(i))
                time.sleep(1)
                for j in car[i]:
                    Method(driver).click('xpath', '//span[text()="{}"]'.format(j))
                    time.sleep(1)
                    target = driver.find_elements_by_class_name('ivu-card-body')[1]
                    driver.execute_script("arguments[0].scrollIntoView();", target)
                    driver.save_screenshot('{}\\picture'.format(whole_picture_path) + '\\' + j + '_整体费用图表' + '.png')

        except:
            log_file_out('截取单个车的整体费用图表失败')
            return

# 通用模型图表
def common_model_picture(url,username,password,contents,modelName,tabs):
    # 设置excel保存目录为bin下面download_excel下面的common_model 图片中路径要为"\\"
    common_excel_path = os.path.dirname(__file__) + '\\' + 'download_excel' + '\\common_model'
    if os.path.isdir(common_excel_path) is True:
        pass
    else:
        os.mkdir(common_excel_path)

    options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_settings.popups': 0,
             'download.default_directory': '{}\\bin\\download_excel\\common_model'.format(path_dir),
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
        log_file_out('---------' + '{}'.format(contents[0]) + '图表---------')

        driver.find_elements_by_class_name('power-collapse-item')[1].click()
        time.sleep(1)

        try:
            driver.find_elements_by_xpath('//span[text()=\'{}\']'.format(contents[0]))[1].click()
            log_file_out('点击' + contents[0] + '成功')
            time.sleep(1)
        except NoSuchElementException as e:
            log_file_out('点击' + contents[0] + '失败')
            logger.error(e)

        time.sleep(2)
        # 点击图表按钮
        try:
            if driver.find_element_by_xpath('//a[text()=\'{}\']/../../../../td[5]/div/div/span'.format(modelName)).text == '默认模型':
                Method(driver).click('xpath',
                                     '//a[text()=\'{}\']/../../../../td[1]/div/div/div[4]/div[1]/span/i'.format(modelName))
            else:
                Method(driver).click('xpath',
                                     '//a[text()=\'{}\']/../../../../td[1]/div/div/div[3]/div[1]/span/i'.format(modelName))
        except NoSuchElementException as e:
            logger.error(e)
            log_file_out('点击图表失败')
        time.sleep(2)
        # class定位图表 第几个图表
        picture_index = 1
        for i in tabs:
            if tabs.index(i) == 0:
                pass
            else:
                Method(driver).click('xpath', '//div[contains(text(),\'{}\')]'.format(i))
                time.sleep(1)
            # 判断交叉维度-车型维度excel是否存在
            if os.path.exists('{}\\bin\\download_excel\\common_model'.format(path_dir) + '\\' +'交叉维度-{}.xlsx'.format(i)):
                os.remove('{}\\bin\\download_excel\\common_model'.format(path_dir) + '\\' +'交叉维度-{}.xlsx'.format(i))
            else:
                pass
            driver.find_elements_by_xpath('//span[text()="一键下载"]')[tabs.index(i)].click()
            time.sleep(2)
            if os.path.exists('{}\\bin\\download_excel\\common_model'.format(path_dir) + '\\' +'交叉维度-{}.xlsx'.format(i)):
                log_file_out('交叉维度,{}一键下载成功,验证成功'.format(i))
            else:
                log_file_out('交叉维度,{}一键下载失败,验证失败'.format(i))

            try:
                time.sleep(2)
                # 设置图表下载路径为picture下面的common_model下
                common_picture_path = os.path.dirname(__file__) + '\\' + 'picture' + '\\common_model'
                if os.path.isdir(common_picture_path) is True:
                    pass
                else:
                    os.mkdir(common_picture_path)

                target = driver.find_elements_by_class_name('moreChart-items')[picture_index]
                driver.execute_script("arguments[0].scrollIntoView();", target)
                driver.save_screenshot(common_picture_path + '\\' + '交叉维度-{}'.format(i) + '.png')
                log_file_out('截取交叉维度-{}图表成功'.format(i))
            except:
                log_file_out('截取交叉维度-{}图表失败'.format(i))
            picture_index += 3


#整车占比图表
def carload_ratio_picture(url,username,password,contents,modelName):
    # 设置excel保存目录为bin下面download_excel下面的car_load 图片中路径要为"\\"
    car_load = os.path.dirname(__file__) + '\\' + 'download_excel' + '\\car_load'
    if os.path.isdir(car_load) is True:
        pass
    else:
        os.mkdir(car_load)

    options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_settings.popups': 0,
             'download.default_directory': '{}\\bin\\download_excel\\car_load'.format(path_dir),
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
        log_file_out('---------' + '{}'.format(contents[0]) + '费用占比分析图表---------')

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

        driver.find_elements_by_xpath('//span[text()=\'{}\']/../../ul/li[2]'.format(contents[0]))[1].click()
        time.sleep(2)
        # 点击图表按钮
        try:
            Method(driver).click('xpath','//a[text()=\'{}\']/../../../../td[1]/div/div/div[2]/div/span/i'.format(modelName))

            log_file_out('点击图表成功')
        except NoSuchElementException as e:
            logger.error(e)
            log_file_out('点击图表失败')
        # 判断excel是否存在
        if os.path.exists('{}\\bin\\download_excel\\car_load'.format(path_dir) + '\\' + '整车维度-占比分析.xlsx'):
            os.remove(
                '{}\\bin\\download_excel\\car_load'.format(path_dir) + '\\' + '整车维度-占比分析.xlsx')
        else:
            pass


        Method(driver).click('xpath','//span[text()="一键下载"]')
        time.sleep(2)
        if os.path.exists('{}\\bin\\download_excel\\car_load'.format(path_dir) + '\\' + '整车维度-占比分析.xlsx'):
            log_file_out('一键下载成功,验证成功')
        else:
            log_file_out('一键下载失败,验证失败')

        try:
            time.sleep(2)
            # 设置图表下载路径为picture下面的car_load下
            car_load_picture_path = os.path.dirname(__file__) + '\\' + 'picture' + '\\car_load'
            if os.path.isdir(car_load_picture_path) is True:
                pass
            else:
                os.mkdir(car_load_picture_path)
            target = driver.find_elements_by_class_name('ivu-card-body')[1]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            driver.save_screenshot(car_load_picture_path + '\\' + '系统_构型费用占比' + '.png')
            time.sleep(1)
            target = driver.find_elements_by_class_name('ivu-card-body')[2]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            driver.save_screenshot(car_load_picture_path + '\\'  + '路局维修费用占比' + '.png')
            time.sleep(1)
            target = driver.find_elements_by_class_name('ivu-card-body')[3]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            driver.save_screenshot(car_load_picture_path + '\\' + '高级修维修级别费用占比' + '.png')
            time.sleep(1)
            target = driver.find_elements_by_class_name('ivu-card-body')[4]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            driver.save_screenshot(car_load_picture_path + '\\' + '维修费用占比' + '.png')
            log_file_out('截取图表成功')
        except:
            log_file_out('截取图表失败')

#车型占比图表
def cartype_ratio_picture(url,username,password,contents,modelname):
    # 设置excel保存目录为bin下面download_excel下面的car_load 图片中路径要为"\\"
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
        time.sleep(1)
        log_file_out('---------' + '{}'.format(contents[0]) + '费用占比分析图表---------')

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

        driver.find_elements_by_xpath('//span[text()=\'{}\']/../../ul/li[2]'.format(contents[0]))[1].click()
        time.sleep(2)
        # 点击图表按钮
        try:
            Method(driver).click('xpath','//a[text()=\'{}\']/../../../../td[1]/div/div/div[2]/div/span/i'.format(modelname))

            log_file_out('点击图表成功')
        except NoSuchElementException as e:
            logger.error(e)
            log_file_out('点击图表失败')
        # 判断excel是否存在
        if os.path.exists('{}\\bin\\download_excel\\car_type'.format(path_dir) + '\\' + '车型维度-占比分析.xlsx'):
            os.remove(
                '{}\\bin\\download_excel\\car_type'.format(path_dir) + '\\' + '车型维度-占比分析.xlsx')
        else:
            pass

        time.sleep(2)
        Method(driver).click('xpath','//span[text()="一键下载"]')
        time.sleep(2)
        if os.path.exists('{}\\bin\\download_excel\\car_type'.format(path_dir) + '\\' + '车型维度-占比分析.xlsx'):
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


            driver.save_screenshot(car_type_picture_path + '\\' + '车型占比工时数_材料数' + '.png')
            time.sleep(1)
            Method(driver).click('xpath', '//span[text()="人工费"]')
            time.sleep(1)
            Method(driver).click('xpath', '//span[text()="物料费"]')
            time.sleep(1)

            driver.save_screenshot(car_type_picture_path + '\\'  + '车型占比人工费_物料费' + '.png')
            time.sleep(1)
            target = driver.find_elements_by_class_name('ivu-card-body')[3]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            driver.save_screenshot(car_type_picture_path + '\\' + '车型占比维修数量' + '.png')
            time.sleep(1)
            Method(driver).click('xpath', '//span[text()="费用"]')

            driver.save_screenshot(car_type_picture_path + '\\' + '车型占比维修费用' + '.png')
            log_file_out('截取图表成功')
        except Exception as e:
            logger.error(e)
            log_file_out('截取图表失败')

#维修及维修保障维度
def repair_ratio_picture(url,username,password,contents,modelName):
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
        log_file_out('---------' + '{}'.format(contents[0]) + '费用占比分析图表---------')

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

        driver.find_elements_by_xpath('//span[text()=\'{}\']/../../ul/li[2]'.format(contents[0]))[1].click()
        time.sleep(2)

        # 点击图表按钮
        try:
            Method(driver).click('xpath','//a[text()=\'{}\']/../../../../td[1]/div/div/div[2]/div/span/i'.format(modelName))

            log_file_out('点击图表成功')
        except NoSuchElementException as e:
            logger.error(e)
            log_file_out('点击图表失败')
        # 判断excel是否存在
        if os.path.exists('{}\\bin\\download_excel\\repair'.format(path_dir) + '\\' + '维修维保维度-占比分析.xlsx'):
            os.remove(
                '{}\\bin\\download_excel\\repair'.format(path_dir) + '\\' + '维修维保维度-占比分析.xlsx')
        else:
            pass

        time.sleep(2)
        Method(driver).click('xpath', '//span[text()="一键下载"]')
        time.sleep(2)
        if os.path.exists('{}\\bin\\download_excel\\repair'.format(path_dir) + '\\' + '维修维保维度-占比分析.xlsx'):
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
            driver.save_screenshot(repair_picture_path + '\\' + '维修及维修保障占比' + '.png')
            log_file_out('截取图表成功')
        except Exception as e:
            logger.error(e)
            log_file_out('截取图表失败')

#路局维度占比
def railway_ratio_picture(url,username,password,contents,modelName):
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
        log_file_out('---------' + '{}'.format(contents[0]) + '费用占比分析图表---------')

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

        driver.find_elements_by_xpath('//span[text()=\'{}\']/../../ul/li[2]'.format(contents[0]))[1].click()
        time.sleep(2)
        # 点击图表按钮
        try:
            Method(driver).click('xpath','//a[text()=\'{}\']/../../../../td[1]/div/div/div[2]/div/span/i'.format(modelName))

            log_file_out('点击图表成功')
        except NoSuchElementException as e:
            logger.error(e)
            log_file_out('点击图表失败')

        # 判断excel是否存在
        if os.path.exists('{}\\bin\\download_excel\\railway'.format(path_dir) + '\\' + '路局维度-占比分析.xlsx'):
            os.remove(
                '{}\\bin\\download_excel\\railway'.format(path_dir) + '\\' + '路局维度-占比分析.xlsx')
        else:
            pass

        time.sleep(2)
        Method(driver).click('xpath', '//span[text()="一键下载"]')
        time.sleep(2)
        if os.path.exists('{}\\bin\\download_excel\\railway'.format(path_dir) + '\\' + '路局维度-占比分析.xlsx'):
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
            driver.save_screenshot(railway_picture_path + '\\' + '路局占比工时数' + '.png')
            time.sleep(1)
            Method(driver).click('xpath', '//*[contains(text(),"人工费")]')

            driver.save_screenshot(railway_picture_path + '\\' + '路局占比人工费' + '.png')
            time.sleep(1)
            target = driver.find_elements_by_class_name('ivu-card-body')[2]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            driver.save_screenshot(railway_picture_path + '\\' + '路局占比材料数' + '.png')
            time.sleep(1)
            Method(driver).click('xpath', '//*[contains(text(),"物料费")]')

            driver.save_screenshot(railway_picture_path + '\\' + '路局占比物料费' + '.png')
            time.sleep(1)
            target = driver.find_elements_by_class_name('ivu-card-body')[4]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            driver.save_screenshot(railway_picture_path + '\\' + '路局占比维修数量' + '.png')
            # 移动滚动条到费用按钮
            time.sleep(1)
            target = driver.find_elements_by_class_name('ivu-card-body')[2]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            time.sleep(1)
            driver.find_elements_by_class_name('ivu-btn-default')[-1].click()
            time.sleep(1)
            target = driver.find_elements_by_class_name('ivu-card-body')[4]
            driver.execute_script("arguments[0].scrollIntoView();", target)

            driver.save_screenshot(railway_picture_path + '\\' + '路局占比维修费用' + '.png')
            log_file_out('截取图表成功')
        except Exception as e:
            logger.error(e)
            log_file_out('截取图表失败')

# 系统部件占比
def system_unit_ratio_picture(url,username,password,contents,modelName):
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
        log_file_out('---------' + '{}'.format(contents[0]) + '费用占比分析图表---------')

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

        driver.find_elements_by_xpath('//span[text()=\'{}\']/../../ul/li[2]'.format(contents[0]))[1].click()
        time.sleep(2)
        # 点击图表按钮
        try:
            Method(driver).click('xpath','//a[text()=\'{}\']/../../../../td[1]/div/div/div[2]/div/span/i'.format(modelName))

            log_file_out('点击图表成功')
        except NoSuchElementException as e:
            logger.error(e)
            log_file_out('点击图表失败')
        # 判断excel是否存在
        if os.path.exists('{}\\bin\\download_excel\\system'.format(path_dir) + '\\' + '系统部件维度-占比分析.xlsx'):
            os.remove(
                '{}\\bin\\download_excel\\system'.format(path_dir) + '\\' + '系统部件维度-占比分析.xlsx')
        else:
            pass

        time.sleep(2)
        Method(driver).click('xpath', '//span[text()="一键下载"]')
        time.sleep(2)
        if os.path.exists('{}\\bin\\download_excel\\system'.format(path_dir) + '\\' + '系统部件维度-占比分析.xlsx'):
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
            driver.save_screenshot(system_picture_path + '\\' + '系统部件占比工时数_材料数' + '.png')
            time.sleep(1)
            Method(driver).click('xpath', '//*[contains(text(),"人工费")]')
            time.sleep(1)
            Method(driver).click('xpath', '//*[contains(text(),"物料费")]')
            time.sleep(1)
            driver.save_screenshot(system_picture_path + '\\' + '系统部件占比人工费_物料费' + '.png')
            time.sleep(1)

            target = driver.find_elements_by_class_name('ivu-card-body')[4]
            driver.execute_script("arguments[0].scrollIntoView();", target)

            driver.save_screenshot(system_picture_path + '\\' + '系统部件占比维修等级_维修类型数量' + '.png')
            time.sleep(1)
            target = driver.find_elements_by_class_name('ivu-card-body')[-1]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            driver.save_screenshot(system_picture_path + '\\' + '系统部件占比定偶检数量_供应商占比' + '.png')
            # 移动滚动条到维修等级费用按钮
            time.sleep(1)

            driver.find_elements_by_class_name('ivu-btn-default')[-3].click()
            time.sleep(1)
            target = driver.find_elements_by_class_name('ivu-card-body')[4]
            driver.execute_script("arguments[0].scrollIntoView();", target)

            driver.save_screenshot(system_picture_path + '\\' + '系统部件占比维修等级_维修类型费用' + '.png')
            time.sleep(1)
            # 移动滚动条到定偶检费用按钮
            driver.find_elements_by_class_name('ivu-btn-default')[-1].click()
            target = driver.find_elements_by_class_name('ivu-card-body')[-1]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            driver.save_screenshot(system_picture_path + '\\' + '系统部件占比定偶检费用_供应商占比' + '.png')
            log_file_out('截取图表成功')
        except Exception as e:
            logger.error(e)
            log_file_out('截取图表失败')

# 供应商占比
def supplier_ratio_picture(url,username,password,contents,modelName):
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

        log_file_out('---------' + '{}'.format(contents[0]) + '费用占比分析图表---------')

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

        driver.find_elements_by_xpath('//span[text()=\'{}\']/../../ul/li[2]'.format(contents[0]))[1].click()
        time.sleep(2)
        # 点击图表按钮
        try:
            Method(driver).click('xpath','//a[text()=\'{}\']/../../../../td[1]/div/div/div[2]/div/span/i'.format(modelName))

            log_file_out('点击图表成功')
        except NoSuchElementException as e:
            logger.error(e)
            log_file_out('点击图表失败')
        # 判断excel是否存在
        if os.path.exists('{}\\bin\\download_excel\\supplier'.format(path_dir) + '\\' + '供应商维度-占比分析.xlsx'):
            os.remove(
                '{}\\bin\\download_excel\\supplier'.format(path_dir) + '\\' + '供应商维度-占比分析.xlsx')
        else:
            pass

        time.sleep(2)
        Method(driver).click('xpath', '//span[text()="一键下载"]')
        time.sleep(2)
        if os.path.exists('{}\\bin\\download_excel\\supplier'.format(path_dir) + '\\' + '供应商维度-占比分析.xlsx'):
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
            driver.save_screenshot(supplier_picture_path + '\\' + '供应商占比工时数_材料数' + '.png')
            time.sleep(1)
            Method(driver).click('xpath', '//*[contains(text(),"人工费")]')
            time.sleep(1)
            Method(driver).click('xpath', '//*[contains(text(),"物料费")]')
            time.sleep(1)
            driver.save_screenshot(supplier_picture_path + '\\' + '供应商占比人工费_物料费' + '.png')
            time.sleep(1)

            target = driver.find_elements_by_class_name('ivu-card-body')[4]
            driver.execute_script("arguments[0].scrollIntoView();", target)

            driver.save_screenshot(supplier_picture_path + '\\' + '供应商占比总费用_问题构型数量' + '.png')
            time.sleep(1)
            target = driver.find_elements_by_class_name('ivu-card-body')[6]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            driver.save_screenshot(supplier_picture_path + '\\' + '供应商占比维修数量' + '.png')
            # 移动滚动条到费用按钮
            time.sleep(1)

            driver.find_elements_by_class_name('ivu-btn-default')[-1].click()
            time.sleep(1)
            target = driver.find_elements_by_class_name('ivu-card-body')[6]
            driver.execute_script("arguments[0].scrollIntoView();", target)

            driver.save_screenshot(supplier_picture_path + '\\' + '供应商占比维修费用' + '.png')
            log_file_out('截取图表成功')
        except Exception as e:
            logger.error(e)
            log_file_out('截取图表失败')

# 生产车间/生产线占比
def workshop_ratio_picture(url,username,password,contents,modelName):
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
        log_file_out('---------' + '{}'.format(contents[0]) + '费用占比分析图表---------')

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

        driver.find_elements_by_xpath('//span[text()=\'{}\']/../../ul/li[2]'.format(contents[0]))[1].click()
        time.sleep(2)
        # 点击图表按钮
        try:
            Method(driver).click('xpath','//a[text()=\'{}\']/../../../../td[1]/div/div/div[2]/div/span/i'.format(modelName))

            log_file_out('点击图表成功')
        except NoSuchElementException as e:
            logger.error(e)
            log_file_out('点击图表失败')

        # 判断excel是否存在
        if os.path.exists('{}\\bin\\download_excel\\workshop'.format(path_dir) + '\\' + '生产车间维度-占比分析.xlsx'):
            os.remove(
                '{}\\bin\\download_excel\\workshop'.format(path_dir) + '\\' + '生产车间维度-占比分析.xlsx')
        else:
            pass

        time.sleep(2)
        Method(driver).click('xpath', '//span[text()="一键下载"]')
        time.sleep(2)
        if os.path.exists('{}\\bin\\download_excel\\workshop'.format(path_dir) + '\\' + '生产车间维度-占比分析.xlsx'):
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
            driver.save_screenshot(workshop_picture_path + '\\' + '生产车间占比工时数_材料数' + '.png')
            time.sleep(1)
            Method(driver).click('xpath', '//*[contains(text(),"人工费")]')
            time.sleep(1)
            Method(driver).click('xpath', '//*[contains(text(),"物料费")]')
            time.sleep(1)
            driver.save_screenshot(workshop_picture_path + '\\' + '生产车间占比人工费_物料费' + '.png')
            time.sleep(1)

            target = driver.find_elements_by_class_name('ivu-card-body')[4]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            driver.save_screenshot(workshop_picture_path + '\\' + '生产车间占比维修数量' + '.png')
            # 移动滚动条到费用按钮
            time.sleep(1)

            driver.find_elements_by_class_name('ivu-btn-default')[-1].click()
            time.sleep(1)
            target = driver.find_elements_by_class_name('ivu-card-body')[4]
            driver.execute_script("arguments[0].scrollIntoView();", target)

            driver.save_screenshot(workshop_picture_path + '\\' + '生产车间占比维修费用' + '.png')
            log_file_out('截取图表成功')
        except Exception as e:
            logger.error(e)
            log_file_out('截取图表失败')

# 高级修占比
def high_repair_ratio_picture(url,username,password,contents,modelname):
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
        log_file_out('---------' + '{}'.format(contents[0]) + '费用占比分析图表---------')

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

        driver.find_elements_by_xpath('//span[text()=\'{}\']/../../ul/li[2]'.format(contents[0]))[1].click()
        time.sleep(2)


        # 点击图表按钮
        try:
            Method(driver).click('xpath','//a[text()=\'{}\']/../../../../td[1]/div/div/div[2]/div/span/i'.format(modelname))

            log_file_out('点击图表成功')
        except NoSuchElementException as e:
            logger.error(e)
            log_file_out('点击图表失败')
        # 判断excel是否存在
        if os.path.exists('{}\\bin\\download_excel\\high_repair'.format(path_dir) + '\\' + '高级修维度-占比分析.xlsx'):
            os.remove(
                '{}\\bin\\download_excel\\high_repair'.format(path_dir) + '\\' + '高级修维度-占比分析.xlsx')
        else:
            pass

        time.sleep(2)
        Method(driver).click('xpath', '//span[text()="一键下载"]')
        time.sleep(2)
        if os.path.exists('{}\\bin\\download_excel\\high_repair'.format(path_dir) + '\\' + '高级修维度-占比分析.xlsx'):
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
            driver.save_screenshot(high_repair_picture_path + '\\' + '高级修占比工时数_总费用' + '.png')
            time.sleep(1)

            driver.find_elements_by_class_name('ivu-btn-default')[1].click()
            time.sleep(1)
            driver.save_screenshot(high_repair_picture_path + '\\' + '高级修占比材料数' + '.png')
            time.sleep(1)

            target = driver.find_elements_by_class_name('ivu-card-body')[4]
            driver.execute_script("arguments[0].scrollIntoView();", target)
            driver.save_screenshot(high_repair_picture_path + '\\' + '高级修占比维修数量' + '.png')
            # 移动滚动条到费用按钮
            time.sleep(1)

            driver.find_elements_by_class_name('ivu-btn-default')[-1].click()
            time.sleep(1)
            target = driver.find_elements_by_class_name('ivu-card-body')[4]
            driver.execute_script("arguments[0].scrollIntoView();", target)

            driver.save_screenshot(high_repair_picture_path + '\\' + '高级修占比维修费用' + '.png')
            log_file_out('截取图表成功')
        except Exception as e:
            logger.error(e)
            log_file_out('截取图表失败')
