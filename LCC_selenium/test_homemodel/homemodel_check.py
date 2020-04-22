from config.config import *


# 首页模型
def home_model(url,username,password):
    driver = webdriver.Chrome()
    status = Login().login(url, username, password, driver)
    time.sleep(2)
    driver.maximize_window()
    Method(driver).click('id', 'ballb')


    if status is True:
        log_file_out('登陆成功')
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[0])

        if len(driver.find_elements_by_xpath('ivu-dropdown-rel')) != 0:
            log_file_out('首页存在模型,验证成功')
        else:
            log_file_out('首页不存在模型,验证失败')

        # 查看修改按钮是否生效
        try:
            driver.find_elements_by_xpath('ivu-dropdown-rel')[0].click()
            log_file_out('点击首页图片上修改按钮成功')
        except:
            log_file_out('点击首页图片上修改按钮失败')

        # 修改图片
        driver.find_elements_by_xpath('ivu-dropdown-rel')[0].click()

        Method(driver).click('xpath','//span[text()="预览模型条件"]')
        time.sleep(1)
        try:
            if driver.find_elements_by_class_name('confCase-val')[0].text != '':
                log_file_out('首页模型开始日期不为空')
            else:
                log_file_out('首页模型开始日期为空,验证失败')
        except Exception as e:
            logger.error(e)
            log_file_out('首页模型验证失败')

        try:
            if driver.find_elements_by_class_name('confCase-val')[1].text != '':
                log_file_out('首页模型结束日期不为空')
            else:
                log_file_out('首页模型结束日期为空,验证失败')
        except Exception as e:
            logger.error(e)
            log_file_out('首页模型验证失败')


        try:
            if driver.find_element_by_class_name('confTrain-trainNoCol').text != '':
                log_file_out('首页模型车型车号不为空')
            else:
                log_file_out('首页模型车型车号为空,验证失败')
        except Exception as e:
            logger.error(e)
            log_file_out('首页模型车型车号验证失败')

        if driver.find_element_by_xpath('//*[@id="right_content"]/div/div/div[1]/span').text != 0:
            log_file_out('首页模型更新时间验证成功')
        else:
            log_file_out('首页模型更新时间验证失败')

        try:
            Method(driver).click('xpath','//span[text()="启用"]')
            log_file_out('首页更新车号全量数据启用成功')
            time.sleep(1)
            Method(driver).click('xpath', '//span[text()="启用"]')
        except Exception as e:
            log_file_out('首页更新车号全量数据启用失败')

        try:
            # 首页更新频率
            Method(driver).click('class','ivu-select-selected-value')
            # 点击每天
            time.sleep(1)
            Method(driver).click('xpath','//li[text()="每天"]')
            log_file_out('首页更新频率验证成功')
        except Exception as e:
            logger.error(e)
            log_file_out('首页更新频率验证失败')
        # 点击查看更多
        Method(driver).click('class','gridItems-more')
        time.sleep(1)

        text = driver.find_element_by_class_name('grid-items-txt').text
        folder_path2 = os.getcwd().replace('\\', '/')

        driver.save_screenshot('\\..\\test_picture\\picture'.format(folder_path2) + '\\' + text+'钻取图' + '.png')

        # 点击查看更多
        driver.find_elements_by_class_name('gridItems-more')[1].click()

        time.sleep(1)

        text1 = driver.find_elements_by_class_name('grid-items-txt')[1].text
        folder_path2 = os.getcwd().replace('\\', '/')

        driver.save_screenshot('\\..\\test_picture\\picture'.format(folder_path2) + '\\' + text1 + '钻取图' + '.png')


        # 退出修改
        driver.find_elements_by_class_name('power-btnOk')[2].click()


