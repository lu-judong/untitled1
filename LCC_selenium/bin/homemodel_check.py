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

        if len(driver.find_elements_by_class_name('grid-btn-edit')) != 0:
            log_file_out('首页存在模型,验证成功')
        else:
            log_file_out('首页不存在模型,验证失败')

        # 查看修改按钮是否生效
        try:
            driver.find_elements_by_class_name('grid-btn-edit')[0].click()
            log_file_out('点击首页图片上修改按钮成功,验证成功')
        except:
            log_file_out('点击首页图片上修改按钮失败,验证失败')

        time.sleep(2)

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
        # 点击关闭
        driver.find_element_by_xpath('//span[text()="关闭"]').click()
        time.sleep(2)
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


        driver.save_screenshot('\\..\\picture' + '\\' + text+'钻取图' + '.png')
        # 点击关闭
        driver.find_element_by_xpath('//span[text()="关闭"]').click()
        time.sleep(2)
        # 点击查看更多
        driver.find_elements_by_class_name('gridItems-more')[1].click()

        time.sleep(1)

        text1 = driver.find_elements_by_class_name('grid-items-txt')[1].text


        driver.save_screenshot('\\..\\picture' + '\\' + text1 + '钻取图' + '.png')




# 产品首页
def produce_home_page(url,username,password,homepage_title,add_model,psi_car,ratio_model,compare_model):
    driver = webdriver.Chrome()
    status = Login().login(url, username, password, driver)
    time.sleep(2)
    driver.maximize_window()
    Method(driver).click('id', 'ballb')

    if status is True:
        log_file_out('------lcc产品首页------')
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[0])
        # 点击多功能按钮进入首页

        check_home_page().click_more_btn(driver)
        time.sleep(2)
        # 切换首页
        check_home_page().click_different_more_btn(driver,[1,homepage_title[0]])
        time.sleep(2)
        # check_home_page().click_message(driver)
        #
        # # 消息
        #
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
        #
        # time.sleep(2)
        # # 验证消息删除
        # if len(driver.find_elements_by_class_name('el-icon-close')) != 0:
        #     # 原有的条数
        #     old_num = len(driver.find_elements_by_class_name('el-icon-close'))
        #     # 点击删除
        #     driver.find_elements_by_class_name('el-icon-close')[1].click()
        #     time.sleep(1)
        #     if len(driver.find_elements_by_class_name('el-icon-close')) == old_num:
        #         log_file_out('消息列表中点击删除按钮失效,验证失败')
        #     else:
        #         log_file_out('消息列表中点击删除按钮生效,验证成功')
        #     time.sleep(1)
        # # 验证清除所有
        # pass
        # # 验证保存模型
        # if len(driver.find_elements_by_xpath('//a[text()="保存模型"]')) == 0:
        #     pass
        # else:
        #     try:
        #         Method(driver).click('xpath', '//a[text()="保存模型"]')
        #
        #         WebDriverWait(driver, 3).until(EC.presence_of_element_located(
        #             (By.CLASS_NAME, "ivu-message-notice")))
        #         error_message = driver.find_element_by_class_name("ivu-message-notice").text
        #
        #         if error_message == '保存成功':
        #             # 获取功能名
        #             function_m = driver.find_elements_by_class_name('messageContent')[0].text.split('\n')[0].split('-')[
        #                 1]
        #             message_model = ''
        #             if function_m == '多模型对比维度':
        #                 # 模型名称
        #                 message_model_L = driver.find_elements_by_class_name('messageContent')[0].text.split('\n')[
        #                     0].split('-')
        #                 compare_model = []
        #                 for mess_mo in range(3, len(message_model_L)):
        #                     if mess_mo != len(message_model_L) - 1:
        #                         message_model += message_model_L[mess_mo] + '-'
        #                     else:
        #                         message_model += message_model_L[mess_mo]
        #                     compare_model.append(message_model_L[mess_mo])
        #             else:
        #                 # 获取模型名称
        #                 message_model = driver.find_elements_by_class_name('messageContent')[0].text.split('\n')[0].split('-')[-1]
        #             # 获取菜单名
        #             menu_m = driver.find_elements_by_class_name('messageContent')[0].text.split('\n')[0].split('-')[
        #                 2]
        #
        #             time.sleep(1)
        #             try:
        #                 Method(driver).click('class', 'ivu-icon-ios-close')
        #                 time.sleep(1)
        #
        #                 Method(driver).click('class', 'el-icon-close')
        #                 time.sleep(2)
        #             except:
        #                 log_file_out('点击退出登录按钮失败')
        #             # 点击菜单
        #             try:
        #
        #                 driver.find_elements_by_class_name('power-collapse-item')[1].click()
        #
        #                 time.sleep(1)
        #                 driver.find_elements_by_xpath('//span[text()=\'{}\']'.format(menu_m))[1].click()
        #             except:
        #                 log_file_out('点击功能菜单失败')
        #             time.sleep(2)
        #             # 点击更多
        #             try:
        #                 Method(driver).click('class', 'icon-btn-more')
        #                 time.sleep(0.5)
        #                 # 计算状态选择框
        #                 Method(driver).click('class', 'ivu-select-placeholder')
        #
        #                 time.sleep(0.5)
        #                 driver.find_element_by_xpath('//li[text()="未计算"]').click()
        #                 time.sleep(0.5)
        #                 # 点击查询按钮
        #                 driver.find_elements_by_class_name('power-btnOk')[0].click()
        #                 time.sleep(1)
        #                 log_file_out('查询未计算的模型成功')
        #             except:
        #                 log_file_out('查询未计算的模型失败')
        #             target = driver.find_element_by_class_name('ivu-page-total')
        #             driver.execute_script("arguments[0].scrollIntoView();", target)
        #             time.sleep(1)
        #             no_cal_num = driver.find_elements_by_class_name('ivu-page-total')[0].text
        #             no_cal_num1 = re.findall(r'\d+', no_cal_num)
        #             model_L = check_home_page().achieve_model(driver,no_cal_num1,'未计算')
        #
        #             if function_m == '多模型对比维度':
        #                 mo = ''
        #                 for mo_na in model_L:
        #                     mo += mo_na
        #                 mo_count = 1
        #                 for com_mo in compare_model:
        #                     if com_mo not in mo:
        #                         mo_count += 1
        #                     else:
        #                         pass
        #
        #                 if mo_count != 1:
        #                     log_file_out('保存模型验证失败')
        #                 else:
        #                     log_file_out('保存模型验证成功')
        #
        #             else:
        #                 if message_model not in model_L:
        #                     log_file_out('保存模型验证失败')
        #                 else:
        #                     log_file_out('保存模型验证成功')
        #             # 获取计算完成的模型
        #             # 点击重置
        #             try:
        #                 time.sleep(1)
        #                 driver.find_elements_by_class_name('power-btnOk')[1].click()
        #
        #                 Method(driver).click('class', 'ivu-select-placeholder')
        #
        #                 time.sleep(0.5)
        #                 driver.find_element_by_xpath('//li[text()="计算完成"]').click()
        #                 time.sleep(0.5)
        #                 # 点击查询按钮
        #                 driver.find_elements_by_class_name('power-btnOk')[0].click()
        #                 target = driver.find_element_by_class_name('ivu-page-total')
        #                 driver.execute_script("arguments[0].scrollIntoView();", target)
        #                 time.sleep(1)
        #                 success_num = driver.find_elements_by_class_name('ivu-page-total')[0].text
        #                 success_num1 = re.findall(r'\d+', success_num)
        #                 success_model =check_home_page().achieve_model(driver,success_num1,'计算完成')
        #             except:
        #                 log_file_out('获取计算完成模型列表失败,验证失败')
        #
        #             time.sleep(1)
        #
        #     except:
        #         log_file_out('消息列表中保存模型验证失败')
        # try:
        #     Method(driver).click('xpath', '//span[text()="首页"]')
        # except:
        #     log_file_out('点击首页按钮失败')
        #
        # time.sleep(2)
        # # 打开页面
        # check_home_page().click_more_btn(driver)
        # time.sleep(1)
        # check_home_page().click_different_more_btn(driver,[1,homepage_title[0]])
        # time.sleep(2)
        # check_home_page().click_message(driver)
        # time.sleep(1)
        # # 验证打开模型
        # if len(driver.find_elements_by_xpath('//a[text()="打开模型"]')) != 0:
        #     driver.find_element_by_xpath('//a[text()="打开模型"]').click()
        #     time.sleep(5)
        #
        #     if function_m == '多模型对比维度':
        #
        #         try:
        #             Method(driver).click('class', 'more-modal-info-title')
        #             time.sleep(1)
        #             # 验证模型名称
        #
        #             if message_model == driver.find_element_by_class_name('more-modal-info-title').text:
        #                 log_file_out('更换模型后,模型名称与选择的模型一致,验证正确')
        #             else:
        #                 log_file_out('更换模型后,模型名称与选择的模型不一致,验证失败')
        #         except:
        #             log_file_out('多模型对比维度打开模型验证失败')
        #     else:
        #
        #
        #         try:
        #             if len(driver.find_elements_by_xpath('//span[text()="模型条件"]')) != 0:
        #                 if message_model in driver.find_elements_by_class_name('power-flex-spaceBtw')[0].text.split(':')[1].split(' ')[0]:
        #                     log_file_out('打开模型模型名称与消息列表中名称一致,验证成功')
        #                 else:
        #                     log_file_out('打开模型模型名称与消息列表中名称不一致,验证失败')
        #         except:
        #             log_file_out('占比屏打开模型验证失败')
        #     # 验证打开模型中是否可以更换模型
        #     check_home_page().click_more_btn(driver)
        #     time.sleep(2)
        #     check_home_page().click_different_more_btn(driver,[2])
        #     # 验证更换模型
        #     try:
        #         WebDriverWait(driver, 3).until(EC.presence_of_element_located(
        #             (By.CLASS_NAME, "ivu-message-notice")))
        #         screen_message = driver.find_element_by_class_name("ivu-message-notice").text
        #
        #         if screen_message == '临时屏不能更换模型':
        #             log_file_out('临时屏中不能更换模型,验证成功')
        #         else:
        #             log_file_out('临时屏中不能更换模型,验证失败')
        #     except:
        #         log_file_out('验证临时屏是否可以更换模型失败')
        # else:
        #     log_file_out('消息列表中模型数量为空')
        #     # 关闭消息页面
        #     Method(driver).click('class','ivu-icon-ios-close')
        # time.sleep(2)
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
        #     check_home_page().click_close_but(driver)
        #     log_file_out('指标预警截图成功')
        # except Exception as e:
        #     logger.error(e)
        #     log_file_out('指标预警截图失败')
        # time.sleep(2)
        # 拖拽
        jquery_str = ""
        try:
            f = open('{}\\config\\jquery-3.4.1.min.js'.format(path_dir), 'r', encoding='utf-8')
            line = f.readline()
            while line:
                jquery_str += line
                line = f.readline()
        except:
            log_file_out('打开jquery失败')

        dnd_str = ""
        try:
            f = open('{}\\config\\test.js'.format(path_dir), 'r', encoding='utf-8')
            line = f.readline()
            while line:
                dnd_str += line
                line = f.readline()
        except:
            log_file_out('打开js文件失败')
        # 切换首页
        check_home_page().click_more_btn(driver)
        time.sleep(1)
        check_home_page().click_different_more_btn(driver, [1,homepage_title[0]])
        time.sleep(2)
        # 验证更换模型
        check_home_page().click_more_btn(driver)
        time.sleep(1)
        check_home_page().click_different_more_btn(driver,[2])

        # 验证更换模型中是否都为计算完成的模型
        try:
            success_count = 1
            for success_m in range(0, len(driver.find_elements_by_xpath('//tr/td[2]'))):
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
                Method(driver).click('xpath', '//span[text()=\'{}\']/../../../td[1]/div/div/span'.format(model_m))
                log_file_out('点击更换模型中模型预览成功')
                time.sleep(2)
                check_home_page().check_model_condition(driver, model_m)

                # 点击回退按钮
                try:
                    Method(driver).click('class', 'ivu-icon-md-arrow-back')
                    log_file_out('点击更换模型中预览窗口回退按钮成功')
                except Exception as e:
                    logger.error(e)
                    log_file_out('点击更换模型中预览窗口回退按钮失败')
            except:
                log_file_out('点击更换模型中模型预览成功')
            time.sleep(1)

        # 点击取消按钮
        try:
            Method(driver).click('xpath', '//span[text()="取消"]')
            log_file_out('点击更换模型页面中取消按钮成功')
        except:
            log_file_out('点击更换模型页面中取消按钮失败')



        for home_page in homepage_title:
            # 切换首页
            check_home_page().click_more_btn(driver)
            time.sleep(2)
            check_home_page().click_different_more_btn(driver,[1,home_page])

            time.sleep(2)
            if len(driver.find_elements_by_xpath('//span[text()="添加"]')) != 0 or len(driver.find_elements_by_xpath('//span[text()="模型条件"]')) != 0:
                log_file_out(home_page + '页面打开成功,验证成功')
                # 更换模型
                check_home_page().click_more_btn(driver)
                time.sleep(2)
                check_home_page().click_different_more_btn(driver,[2])
                time.sleep(2)

                if homepage_title.index(home_page) != 4:
                    try:
                        for model_m in ratio_model:
                            Method(driver).click('xpath', '//span[text()=\'{}\']/../../../td[1]'.format(model_m))
                            time.sleep(1)
                        # 因为页面是拼接的 所以一个checked会在页面出现2次
                        if len(driver.find_elements_by_class_name('ivu-radio-checked')) != 2:
                            log_file_out(home_page + '页面更换模型中模型只能单选,验证失败')
                        else:
                            log_file_out(home_page + '页面更换模型中模型只能单选,验证成功')
                        time.sleep(1)
                        Method(driver).click('xpath', '//span[text()="确定"]')
                        log_file_out(home_page + '页面点击更换模型中确定按钮成功')
                    except Exception as e:
                        logger.error(e)
                        log_file_out(home_page + '页面点击更换模型中确定按钮失败')
                else:
                    try:
                        for model_m1 in compare_model:
                            # 判断模型是否被选中
                            if 'ivu-checkbox-checked' in driver.find_element_by_xpath('//span[text()=\'{}\']/../../../td[1]/div/div/label/span'.format(model_m1)).get_attribute('class'):
                                pass
                            else:
                                Method(driver).click('xpath', '//span[text()=\'{}\']/../../../td[1]'.format(model_m1))
                            time.sleep(1)
                        Method(driver).click('xpath', '//span[text()="确定"]')

                        log_file_out(home_page + '页面点击更换模型验证成功')
                    except Exception as e:
                        logger.error(e)
                        log_file_out(home_page + '页面点击更换模型验证失败')

                time.sleep(5)
                if len(driver.find_elements_by_xpath('//span[text()="模型条件"]')) != 0:
                    # 重置模型条件
                    check_home_page().click_more_btn(driver)
                    time.sleep(2)
                    check_home_page().click_different_more_btn(driver, [3])

                    time.sleep(7)
                    if len(driver.find_elements_by_xpath('//span[text()="模型条件"]')) != 0:
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
                        # 截图
                        try:
                            for btn_value in range(0, 3):
                                # 得到费用标题
                                title_index_text = driver.find_elements_by_xpath('//*[@class="power-proDesc-faultTypeIco"]/..')[btn_value].text
                                driver.find_elements_by_class_name('power-proDesc-faultTypeIco')[btn_value].click()
                                time.sleep(2)
                                driver.save_screenshot(
                                    produce_home_model_picture_path + '\\' + home_page + '_' + title_index_text
                                    + '.png')
                            log_file_out('截取' + home_page + '\'{}\'图表成功'.format(title_index_text))
                        except:
                            log_file_out('截取' + home_page + '图表失败')

                        if homepage_title.index(home_page) == 0:
                            # 验证总费用
                            try:
                                if float(driver.find_elements_by_class_name('power-proChart-title')[2].text.split(':')[1][:-2]) != 0:
                                    log_file_out(home_page+'总费用值不为0,验证正确')
                                else:
                                    log_file_out(home_page + '总费用值为0,验证失败')
                            except:
                                log_file_out(home_page + '总费用值验证失败')

                            try:
                                # 验证列车总数
                                car_sum = driver.find_element_by_tag_name('strong').text.split(' ')[0].split('：')[-1]
                                if float(car_sum) != 0:
                                    log_file_out('列车总数不为0,验证成功')
                                else:
                                    log_file_out('列车总数为0,验证失败')
                            except:
                                log_file_out('列车总数数量验证失败')

                            try:
                                # 验证评估对象数量
                                fault_num  = driver.find_element_by_tag_name('strong').text.split(' ')[1].split('：')[-1]
                                if fault_num != '':
                                    log_file_out('评估对象数量不为0,验证成功')
                                else:
                                    log_file_out('评估对象数量为0,验证失败')
                            except:
                                log_file_out('评估对象数量验证失败')

                            try:
                                # 验证累计费用
                                money_num = driver.find_element_by_tag_name('strong').text.split(' ')[2].split('：')[-1]
                                if float(money_num) != 0:
                                    log_file_out('累计费用不为0,验证成功')
                                else:
                                    log_file_out('累计费用为0,验证失败')
                            except:
                                log_file_out('累计费用验证失败')


                        #
                        elif homepage_title.index(home_page) != 4:
                            try:
                                if \
                                driver.find_element_by_xpath('//span[contains(text(),"模型名称")]/../span[1]').text.split(':')[
                                    1] != ratio_model[-1]:
                                    log_file_out(home_page + '页面更换模型后,模型名称未发生改变,验证失败')
                                else:
                                    log_file_out(home_page + '页面更换模型后,模型名称发生改变,验证成功')
                            except:
                                log_file_out(home_page + '页面更换模型后,模型名称未发生改变,验证失败')


                            # 验证三张图是否重复
                            picture_L = []
                            for i in range(0, len(driver.find_elements_by_class_name('power-proChart-title'))):
                                picture_L.append(driver.find_elements_by_class_name('power-proChart-title')[i].text[:3])

                            # 去重
                            picture_L = list(set(picture_L))
                            if len(picture_L) != 3:
                                log_file_out(home_page + '未出现所需的三张图表,验证失败')
                            else:
                                log_file_out(home_page + '出现所需的三张图表,验证成功')


                            # 验证模型条件
                            Method(driver).click('xpath', '//span[text()="模型条件"]')
                            time.sleep(2)
                            check_home_page().check_model_condition(driver, '')
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
                            time.sleep(5)

                            # 获取页面上的当前里程

                            try:
                                now_start = driver.find_element_by_xpath('//span[contains(text(),"模型名称")]/../span[3]').text.split(':')[1].split('~')[0]
                                now_end = driver.find_element_by_xpath('//span[contains(text(),"模型名称")]/../span[3]').text.split(':')[1].split('~')[1]

                                if now_start == first_block_place and now_end == second_block_place:
                                    log_file_out('页面上的模型条件随着自定义条件中自定义范围的改变发生正确的改变,验证成功')
                                else:
                                    log_file_out('页面上的模型条件随着自定义条件中自定义范围的改变没有发生正确的改变,验证失败')
                            except:
                                log_file_out('页面上的模型条件获取失败,无法验证改变范围页面上条件是否发生改变')
                            # 再点击模型条件看是否此范围是否对模型条件产生影响
                            try:
                                Method(driver).click('xpath', '//span[text()="模型条件"]')
                                time.sleep(2)
                                # 模型条件
                                model_conditon = driver.find_elements_by_class_name('power-preWrapper-title')[0].text
                                # 获取里程/时间信息
                                if driver.find_element_by_xpath('//span[contains(text(),"模型名称")]/../span[3]').text.split(':')[0][-2:] == '时间':
                                    # 判断是否大于10
                                    if int(driver.find_element_by_xpath('//p[@class="power-preCase-row"]/span[1]').text[:7].split('-')[1]) >= 10:

                                        start_condition = driver.find_element_by_xpath(
                                            '//p[@class="power-preCase-row"]/span[1]').text[:7]
                                        end_condition = driver.find_element_by_xpath(
                                            '//p[@class="power-preCase-row"]/span[2]').text[:7]
                                    else:
                                        start_condition = driver.find_element_by_xpath(
                                            '//p[@class="power-preCase-row"]/span[1]').text[:7].split('-')[0] + '-' + \
                                        driver.find_element_by_xpath(
                                            '//p[@class="power-preCase-row"]/span[1]').text[:7].split('-')[1][1:2]
                                        end_condition = driver.find_element_by_xpath(
                                            '//p[@class="power-preCase-row"]/span[2]').text[:7].split('-')[0] + '-' + \
                                        driver.find_element_by_xpath(
                                            '//p[@class="power-preCase-row"]/span[2]').text[:7].split('-')[1][1:2]
                                else:
                                    start_condition = re.findall(r'\d+', driver.find_element_by_xpath(
                                        '//p[@class="power-preCase-row"]/span[1]').text)
                                    end_condition = re.findall(r'\d+', driver.find_element_by_xpath(
                                        '//p[@class="power-preCase-row"]/span[2]').text)
                                if first_block_place == start_condition:
                                    log_file_out('开始条件处,改变{}范围模型条件中发生正确的改变,验证成功'.format(model_conditon))
                                else:
                                    log_file_out('开始条件处,改变{}范围模型条件中未发生正确的改变,验证失败'.format(model_conditon))

                                if second_block_place == end_condition:
                                    log_file_out('结束条件处,改变{}范围模型条件中发生正确的改变,验证成功'.format(model_conditon))
                                else:
                                    log_file_out('结束条件处,改变{}范围模型条件中未发生正确的改变,验证失败'.format(model_conditon))
                            except:
                                log_file_out('获取\'{}\'页面模型条件中里程/日期信息失败,无法验证改变范围是否会影响模型条件'.format(home_page))

                            check_home_page().click_close_but(driver)
                            time.sleep(2)

                        if homepage_title.index(home_page) == 4:
                            Method(driver).click('class', 'more-modal-info-title')
                            time.sleep(1)
                            # 验证模型名称
                            compare_count = 1
                            for compare_model_name in range(0,len(driver.find_elements_by_xpath('//span[contains(text(),"起止")]/..'))):
                                com_model_name = driver.find_elements_by_xpath('//span[contains(text(),"起止")]/..')[compare_model_name].text.split(' ')[0]
                                if com_model_name not in compare_model:
                                    compare_count += 1
                                    break
                                else:
                                    pass
                            if compare_count == 1:
                                log_file_out('更换模型后,模型名称与选择的模型一致,验证正确')
                            else:
                                log_file_out('更换模型后,模型名称与选择的模型不一致,验证失败')
                            # 收起模型名称下拉框
                            Method(driver).click('class', 'more-modal-info-title')

                            # 点开费用按钮
                            try:
                                Method(driver).click('id','div1')
                                time.sleep(1)
                            except:
                                log_file_out('点击费用按钮失败')
                            # 验证拖拽
                            try:
                                for cost_classify in range(0,len(driver.find_elements_by_id('div'))):
                                    # 拖拽块名称
                                    drop_name = driver.find_elements_by_id('div')[cost_classify].text
                                    try:
                                        driver.execute_script(jquery_str + dnd_str + "$('.%s').simulateDragDrop({ dropTarget: '#%s'});" % ('box > div:nth-child({})'.format(cost_classify+1), 'ondrop > div:nth-child(2)'))
                                        log_file_out('拖拽\'{}\'成功'.format(drop_name))
                                    except:
                                        log_file_out('拖拽\'{}\'失败'.format(drop_name))
                                    # driver.save_screenshot(produce_home_model_picture_path + '\\' + home_page + '_' + drop_name
                                    #     + '.png')
                                    time.sleep(2)
                                    try:
                                        # 点击关闭
                                        driver.find_element_by_xpath('//span[text()=\'{}\']/i'.format(drop_name)).click()
                                        log_file_out('关闭\'{}\'成功'.format(drop_name))
                                    except:
                                        log_file_out('关闭\'{}\'失败'.format(drop_name))
                                    time.sleep(1)
                            except:
                                log_file_out('拖拽费用拖拽失败,验证失败')

                            # 点开关闭费用按钮
                            check_home_page().click_close_but(driver)


                            try:
                                # 对比模型的模型条件
                                Method(driver).click('xpath', '//span[text()="模型条件"]')
                                time.sleep(2)
                            except:
                                log_file_out(home_page+'点击模型条件按钮失败')
                            # 时间/里程
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
                                log_file_out('对比功能第时间/里程条件验证失败')

                            try:
                                # 点击车型
                                driver.find_elements_by_class_name('power-multi-icoMore')[0].click()
                                time.sleep(1)

                                for compare_car in range(0, len(driver.find_elements_by_class_name('power-multi-trainTypeTag'))):
                                    driver.find_elements_by_class_name('power-multi-trainTypeTag')[compare_car].click()
                                    time.sleep(1)
                                    if driver.find_elements_by_class_name('power-multi-trainNoRow')[
                                        compare_car].text != '':
                                        log_file_out('对比功能第{}个模型车型条件不为空,验证成功'.format(compare_car+1))
                                    else:
                                        log_file_out('对比功能第{}个模型车型条件为空,验证失败'.format(compare_car+1))
                                    time.sleep(1)
                                    driver.find_elements_by_class_name('power-multi-trainTypeTag')[compare_car].click()
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
                                        log_file_out('对比功能第{}个模型构型条件不为空,验证成功'.format(compare_fault+1))
                                    else:
                                        log_file_out('对比功能第{}个模型构型条件为空,验证失败'.format(compare_fault+1))
                                    time.sleep(1)
                                    driver.find_elements_by_class_name('ivu-tree-arrow')[compare_fault].click()
                            except:
                                log_file_out('多模型构型验证失败')

                            try:
                                # 验证模型共同条件
                                Method(driver).click('xpath', '//span[contains(text(),"模型共同条件")]')
                                time.sleep(2)
                                # 共同条件
                                compare_common = driver.find_elements_by_class_name('power-pre-wrapper')[0].text
                                log_file_out('对比模型,共同模型条件为' + compare_common)
                            except:
                                log_file_out('对比模型,共同模型条件验证失败')
                            # 点击回退按钮
                            try:
                                Method(driver).click('class','ivu-icon-md-arrow-back')
                                time.sleep(1)
                            except:
                                pass
                            # 点击关闭按钮
                            check_home_page().click_close_but(driver)

                    else:
                        log_file_out('\'{}\'重新计算模型失败,页面未打开,验证失败'.format(home_page))
                        pass
                else:
                    log_file_out(home_page + '页面更换模型后,模型计算失败,验证失败')
                    pass



