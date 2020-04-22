from config.config import *

# 内控模型的高级检索
def incontrol_high_select(url,username,password,contents,modelName,value):
    # option = webdriver.ChromeOptions()
    # option.add_argument("headless")
    # driver = webdriver.Chrome(chrome_options=option,                                                                executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    log_file_out('-----' + contents[1] + '高级检索验证' + '-----')
    status = new_built(driver, url, username, password, contents, 2)
    if status is True:
        log_file_out('登录成功')
        time.sleep(2)

        if driver.find_element_by_xpath('//*[@id="right_content"]/div/div[1]/div/p').text == contents[1]:
            log_file_out(contents[1]+'菜单名称与菜单页内容对应')
        else:
            log_file_out(contents[1] + '菜单名称与菜单页内容不对应')

        time.sleep(1)
        # 点击更多
        driver.find_element_by_class_name('beta-form-more').click()

        driver.find_elements_by_class_name('ivu-input')[0].send_keys(modelName)
        time.sleep(0.5)
        # 点击查询按钮
        driver.find_element_by_class_name('ct-input-group-items').click()
        time.sleep(0.5)
        su = driver.find_elements_by_class_name('ivu-page-total')[0].text


        su1 = re.findall(r'\d+',su)
        if int(su1[0]) == 1:
            log_file_out('模型名称输入框高级搜索验证成功')
        else:
            log_file_out('模型名称输入框高级搜索验证失败')


        # 重置
        driver.find_elements_by_class_name('ct-input-group-items')[1].click()
        # 计算状态选择框
        driver.find_element_by_class_name('ivu-select-placeholder').click()
        if value == 1:
            driver.find_element_by_xpath('//li[text()="未计算"]').click()
        elif value == 2:
            driver.find_element_by_xpath('//li[text()="计算中"]').click()
        elif value == 3:
            driver.find_element_by_xpath('//li[text()="计算异常"]').click()
        else:
            driver.find_element_by_xpath('//li[text()="计算完成"]').click()
        # 点击查询按钮
        driver.find_element_by_class_name('ct-input-group-items').click()
        time.sleep(2)
        # 查询的数量
        nu = driver.find_elements_by_class_name('ivu-page-total')[0].text
        nu1 = re.findall(r'\d+', nu)
        L = []
        if int(nu1[0]) == 0:
            log_file_out('验证成功')
        elif int(nu1[0]) <= 10:
            if value == 1:
                if len(driver.find_elements_by_xpath('//div[text()="计算中"]')) !=0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) !=0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                    log_file_out('计算状态选择框验证失败')
                else:
                    log_file_out('计算状态选择框验证成功')
            elif value == 2:
                if len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                    log_file_out('计算状态选择框验证失败')
                else:
                    log_file_out('计算状态选择框验证成功')
            elif value == 3:
                if len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算中"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                    log_file_out('计算状态选择框验证失败')
                else:
                    log_file_out('计算状态选择框验证成功')
            else:
                if len(driver.find_elements_by_xpath('//div[text()="计算中"]')) !=0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) !=0 and \
                        len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0:
                    log_file_out('计算状态选择框验证失败')
                else:
                    log_file_out('计算状态选择框验证成功')
        else:
            for i in range(0,(int(nu1[0])//10)+1):
                driver.find_element_by_xpath('//a[text()="{}"]'.format(i+1)).click()
                if value == 1:
                    if len(driver.find_elements_by_xpath('//div[text()="计算中"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                        log_file_out('第' + str(i+1) + '页' + '计算状态选择框验证失败')
                    else:
                        log_file_out('第' + str(i+1) + '页' + '计算状态选择框验证成功')
                elif value == 2:
                    if len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                        log_file_out('第' + str(i+1) + '页' + '计算状态选择框验证失败')
                    else:
                        log_file_out('第' + str(i+1) + '页' + '计算状态选择框验证成功')
                elif value == 3:
                    if len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算中"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                        log_file_out('第' + str(i+1) + '页' + '计算状态选择框验证失败')
                    else:
                        log_file_out('第' + str(i+1) + '页' + '计算状态选择框验证成功')
                else:
                    if len(driver.find_elements_by_xpath('//div[text()="计算中"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0:
                        log_file_out('第' + str(i+1) + '页' + '计算状态选择框验证失败')
                    else:
                        log_file_out('第' + str(i+1) + '页' + '计算状态选择框验证成功')
    else:
        log_file_out('登录失败')

# 修程修制的高级检索
def repair_high_select(url,username,password,contents,modelName,value,value1):
    # option = webdriver.ChromeOptions()
    # option.add_argument("headless")
    # driver = webdriver.Chrome(chrome_options=option,                                                                executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    log_file_out('-----' + contents[1] + '高级检索验证' + '-----')
    status = new_built(driver, url, username, password, contents, 2)
    if status is True:
        log_file_out('登录成功')
        time.sleep(2)

        if driver.find_element_by_xpath('//*[@id="right_content"]/div/div[1]/div/p').text == contents[1]:
            log_file_out(contents[1]+'菜单名称与菜单页内容对应')
        else:
            log_file_out(contents[1] + '菜单名称与菜单页内容不对应')

        time.sleep(1)
        # 点击更多
        driver.find_element_by_class_name('beta-form-more').click()

        driver.find_elements_by_class_name('ivu-input')[0].send_keys(modelName)
        time.sleep(0.5)
        # 点击查询按钮
        driver.find_element_by_class_name('ct-input-group-items').click()
        time.sleep(0.5)
        su = driver.find_elements_by_class_name('ivu-page-total')[0].text


        su1 = re.findall(r'\d+',su)
        if int(su1[0]) == 1:
            log_file_out('模型名称输入框高级搜索验证成功')
        else:
            log_file_out('模型名称输入框高级搜索验证失败')

        # 重置
        driver.find_elements_by_class_name('ct-input-group-items')[1].click()
        # 评估对象选择框
        driver.find_element_by_class_name('ivu-select-placeholder').click()
        if value == 1:
            driver.find_element_by_xpath('//li[text()="评估系统、部件"]').click()
        else:
            driver.find_element_by_xpath('//li[text()="故障模式"]').click()
        d = {1:'评估系统、部件',2:'故障模式'}
        # 点击查询按钮
        driver.find_element_by_class_name('ct-input-group-items').click()
        time.sleep(2)
        # 查询的数量
        nu = driver.find_elements_by_class_name('ivu-page-total')[0].text
        nu1 = re.findall(r'\d+', nu)

        if int(nu1[0]) == 0:
            log_file_out('验证成功')
        elif int(nu1[0]) <= 10:
            if value == 1:
                if len(driver.find_elements_by_xpath('//div[text()="故障模式"]')) !=0:
                    log_file_out('评估对象选择框验证失败')
                else:
                    log_file_out('评估对象选择框验证成功')
            else:
                if len(driver.find_elements_by_xpath('//div[text()="评估系统、部件"]')) != 0:
                    log_file_out('评估对象选择框验证失败')
                else:
                    log_file_out('评估对象选择框验证成功')
        else:
            for i in range(0,(int(nu1[0])//10)+1):
                driver.find_element_by_xpath('//a[text()="{}"]'.format(i+1)).click()
                if value == 1:
                    if len(driver.find_elements_by_xpath('//div[text()="故障模式"]')) != 0:
                        log_file_out('第'+str(i+1)+'页'+'评估对象选择框验证失败')
                    else:
                        log_file_out('第'+str(i+1)+'页'+'评估对象选择框验证成功')
                else:
                    if len(driver.find_elements_by_xpath('//div[text()="评估系统、部件"]')) != 0:
                        log_file_out('第'+str(i+1)+'页'+'评估对象选择框验证失败')
                    else:
                        log_file_out('第'+str(i+1)+'页'+'评估对象选择框验证成功')

        # 重置
        driver.find_elements_by_class_name('ct-input-group-items')[1].click()
        # 计算状态选择框
        driver.find_elements_by_class_name('ivu-select-placeholder')[1].click()
        if value1 == 1:
            driver.find_element_by_xpath('//li[text()="未计算"]').click()
        elif value1 == 2:
            driver.find_element_by_xpath('//li[text()="计算中"]').click()
        elif value1 == 3:
            driver.find_element_by_xpath('//li[text()="计算异常"]').click()
        else:
            driver.find_element_by_xpath('//li[text()="计算完成"]').click()
        # 点击查询按钮
        driver.find_element_by_class_name('ct-input-group-items').click()
        time.sleep(2)
        # 查询的数量
        nu2 = driver.find_elements_by_class_name('ivu-page-total')[0].text
        nu3 = re.findall(r'\d+', nu2)

        if int(nu3[0]) == 0:
            log_file_out('验证成功')
        elif int(nu3[0]) <= 10:
            if value1 == 1:
                if len(driver.find_elements_by_xpath('//div[text()="计算中"]')) !=0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) !=0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                    log_file_out('计算状态选择框验证失败')
                else:
                    log_file_out('计算状态选择框验证成功')
            elif value1 == 2:
                if len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                    log_file_out('计算状态选择框验证失败')
                else:
                    log_file_out('计算状态选择框验证成功')
            elif value1 == 3:
                if len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算中"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                    log_file_out('计算状态选择框验证失败')
                else:
                    log_file_out('计算状态选择框验证成功')
            else:
                if len(driver.find_elements_by_xpath('//div[text()="计算中"]')) !=0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) !=0 and \
                        len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0:
                    log_file_out('计算状态选择框验证失败')
                else:
                    log_file_out('计算状态选择框验证成功')
        else:
            for i in range(0,(int(nu3[0])//10)+1):
                driver.find_element_by_xpath('//a[text()="{}"]'.format(i+1)).click()
                if value1 == 1:
                    if len(driver.find_elements_by_xpath('//div[text()="计算中"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                        log_file_out('第' + str(i) + '页' + '计算状态选择框验证失败')
                    else:
                        log_file_out('第' + str(i) + '页' + '计算状态选择框验证成功')
                elif value1 == 2:
                    if len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                        log_file_out('第' + str(i) + '页' + '计算状态选择框验证失败')
                    else:
                        log_file_out('第' + str(i) + '页' + '计算状态选择框验证成功')
                elif value1 == 3:
                    if len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算中"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                        log_file_out('第' + str(i) + '页' + '计算状态选择框验证失败')
                    else:
                        log_file_out('第' + str(i) + '页' + '计算状态选择框验证成功')
                else:
                    if len(driver.find_elements_by_xpath('//div[text()="计算中"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0:
                        log_file_out('第' + str(i) + '页' + '计算状态选择框验证失败')
                    else:
                        log_file_out('第' + str(i) + '页' + '计算状态选择框验证成功')

# 技术变更的高级检索
def tech_test(url,username,password,contents,modelName,value,value1):
    # option = webdriver.ChromeOptions()
    # option.add_argument("headless")
    # driver = webdriver.Chrome(chrome_options=option,                                                                executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    log_file_out('-----' + contents[1] + '高级检索验证' + '-----')
    status = new_built(driver, url, username, password, contents, 2)
    if status is True:
        log_file_out('登录成功')
        time.sleep(2)

        if driver.find_element_by_xpath('//*[@id="right_content"]/div/div[1]/div/p').text == contents[1]:
            log_file_out(contents[1]+'菜单名称与菜单页内容对应')
        else:
            log_file_out(contents[1] + '菜单名称与菜单页内容不对应')

        time.sleep(1)
        # 点击更多
        driver.find_element_by_class_name('beta-form-more').click()

        driver.find_elements_by_class_name('ivu-input')[0].send_keys(modelName)
        time.sleep(0.5)
        # 点击查询按钮
        driver.find_element_by_class_name('ct-input-group-items').click()
        time.sleep(0.5)
        su = driver.find_elements_by_class_name('ivu-page-total')[0].text


        su1 = re.findall(r'\d+',su)
        if int(su1[0]) == 1:
            log_file_out('模型名称输入框高级搜索验证成功')
        else:
            log_file_out('模型名称输入框高级搜索验证失败')

        # 重置
        driver.find_elements_by_class_name('ct-input-group-items')[1].click()
        # 评估对象选择框
        driver.find_element_by_class_name('ivu-select-placeholder').click()
        if value == 1:
            driver.find_element_by_xpath('//li[text()="评估系统、部件"]').click()
        else:
            driver.find_element_by_xpath('//li[text()="故障模式"]').click()
        d = {1:'评估系统、部件',2:'故障模式'}
        # 点击查询按钮
        driver.find_element_by_class_name('ct-input-group-items').click()
        time.sleep(2)
        # 查询的数量
        nu = driver.find_elements_by_class_name('ivu-page-total')[0].text
        nu1 = re.findall(r'\d+', nu)

        if int(nu1[0]) == 0:
            log_file_out('验证成功')
        elif int(nu1[0]) <= 10:
            if value == 1:
                if len(driver.find_elements_by_xpath('//div[text()="故障模式"]')) !=0:
                    log_file_out('评估对象选择框验证失败')
                else:
                    log_file_out('评估对象选择框验证成功')
            else:
                if len(driver.find_elements_by_xpath('//div[text()="评估系统、部件"]')) != 0:
                    log_file_out('评估对象选择框验证失败')
                else:
                    log_file_out('评估对象选择框验证成功')
        else:
            for i in range(0,(int(nu1[0])//10)+1):
                driver.find_element_by_xpath('//a[text()="{}"]'.format(i+1)).click()
                if value == 1:
                    if len(driver.find_elements_by_xpath('//div[text()="故障模式"]')) != 0:
                        log_file_out('第'+str(i+1)+'页'+'评估对象选择框验证失败')
                    else:
                        log_file_out('第'+str(i+1)+'页'+'评估对象选择框验证成功')
                else:
                    if len(driver.find_elements_by_xpath('//div[text()="评估系统、部件"]')) != 0:
                        log_file_out('第'+str(i+1)+'页'+'评估对象选择框验证失败')
                    else:
                        log_file_out('第'+str(i+1)+'页'+'评估对象选择框验证成功')

        # 重置
        driver.find_elements_by_class_name('ct-input-group-items')[1].click()
        # 计算状态选择框
        driver.find_elements_by_class_name('ivu-select-placeholder')[1].click()
        if value1 == 1:
            driver.find_element_by_xpath('//li[text()="未计算"]').click()
        elif value1 == 2:
            driver.find_element_by_xpath('//li[text()="计算中"]').click()
        elif value1 == 3:
            driver.find_element_by_xpath('//li[text()="计算异常"]').click()
        else:
            driver.find_element_by_xpath('//li[text()="计算完成"]').click()
        # 点击查询按钮
        driver.find_element_by_class_name('ct-input-group-items').click()
        time.sleep(2)
        # 查询的数量
        nu2 = driver.find_elements_by_class_name('ivu-page-total')[0].text
        nu3 = re.findall(r'\d+', nu2)

        if int(nu3[0]) == 0:
            log_file_out('验证成功')
        elif int(nu3[0]) <= 10:
            if value1 == 1:
                if len(driver.find_elements_by_xpath('//div[text()="计算中"]')) !=0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) !=0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                    log_file_out('计算状态选择框验证失败')
                else:
                    log_file_out('计算状态选择框验证成功')
            elif value1 == 2:
                if len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                    log_file_out('计算状态选择框验证失败')
                else:
                    log_file_out('计算状态选择框验证成功')
            elif value1 == 3:
                if len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算中"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                    log_file_out('计算状态选择框验证失败')
                else:
                    log_file_out('计算状态选择框验证成功')
            else:
                if len(driver.find_elements_by_xpath('//div[text()="计算中"]')) !=0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) !=0 and \
                        len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0:
                    log_file_out('计算状态选择框验证失败')
                else:
                    log_file_out('计算状态选择框验证成功')
        else:
            for i in range(0,(int(nu3[0])//10)+1):
                driver.find_element_by_xpath('//a[text()="{}"]'.format(i+1)).click()
                if value1 == 1:
                    if len(driver.find_elements_by_xpath('//div[text()="计算中"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                        log_file_out('第' + str(i) + '页' + '计算状态选择框验证失败')
                    else:
                        log_file_out('第' + str(i) + '页' + '计算状态选择框验证成功')
                elif value1 == 2:
                    if len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                        log_file_out('第' + str(i) + '页' + '计算状态选择框验证失败')
                    else:
                        log_file_out('第' + str(i) + '页' + '计算状态选择框验证成功')
                elif value1 == 3:
                    if len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算中"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                        log_file_out('第' + str(i) + '页' + '计算状态选择框验证失败')
                    else:
                        log_file_out('第' + str(i) + '页' + '计算状态选择框验证成功')
                else:
                    if len(driver.find_elements_by_xpath('//div[text()="计算中"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0:
                        log_file_out('第' + str(i) + '页' + '计算状态选择框验证失败')
                    else:
                        log_file_out('第' + str(i) + '页' + '计算状态选择框验证成功')

# 单一模型的高级检索
def singelModel_high_select(url,username,password,contents,modelName,value,value1):
    # option = webdriver.ChromeOptions()
    # option.add_argument("headless")
    # driver = webdriver.Chrome(chrome_options=option,                                                                executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    log_file_out('-----' + contents[1] + '高级检索验证' + '-----')
    status = new_built(driver, url, username, password, contents, 2)
    if status is True:
        log_file_out('登录成功')
        time.sleep(2)

        if driver.find_element_by_xpath('//*[@id="right_content"]/div/div[1]/div/p').text == contents[1]:
            log_file_out(contents[1]+'菜单名称与菜单页内容对应')
        else:
            log_file_out(contents[1] + '菜单名称与菜单页内容不对应')

        time.sleep(1)
        # 点击更多
        driver.find_element_by_class_name('beta-form-more').click()

        driver.find_elements_by_class_name('ivu-input')[0].send_keys(modelName)
        time.sleep(0.5)
        # 点击查询按钮
        driver.find_element_by_class_name('ct-input-group-items').click()
        time.sleep(0.5)
        su = driver.find_elements_by_class_name('ivu-page-total')[0].text


        su1 = re.findall(r'\d+',su)
        if int(su1[0]) == 1:
            log_file_out('模型名称输入框高级搜索验证成功')
        else:
            log_file_out('模型名称输入框高级搜索验证失败')

        # 重置
        driver.find_elements_by_class_name('ct-input-group-items')[1].click()
        # 评估对象选择框
        driver.find_element_by_class_name('ivu-select-placeholder').click()
        if value == 1:
            driver.find_element_by_xpath('//li[text()="评估系统、部件"]').click()
        else:
            driver.find_element_by_xpath('//li[text()="故障模式"]').click()
        d = {1:'评估系统、部件',2:'故障模式'}
        # 点击查询按钮
        driver.find_element_by_class_name('ct-input-group-items').click()
        time.sleep(2)
        # 查询的数量
        nu = driver.find_elements_by_class_name('ivu-page-total')[0].text
        nu1 = re.findall(r'\d+', nu)

        if int(nu1[0]) == 0:
            log_file_out('验证成功')
        elif int(nu1[0]) <= 10:
            if value == 1:
                if len(driver.find_elements_by_xpath('//div[text()="故障模式"]')) !=0:
                    log_file_out('评估对象选择框验证失败')
                else:
                    log_file_out('评估对象选择框验证成功')
            else:
                if len(driver.find_elements_by_xpath('//div[text()="评估系统、部件"]')) != 0:
                    log_file_out('评估对象选择框验证失败')
                else:
                    log_file_out('评估对象选择框验证成功')
        else:
            for i in range(0,(int(nu1[0])//10)+1):
                driver.find_element_by_xpath('//a[text()="{}"]'.format(i+1)).click()
                if value == 1:
                    if len(driver.find_elements_by_xpath('//div[text()="故障模式"]')) != 0:
                        log_file_out('第'+str(i+1)+'页'+'评估对象选择框验证失败')
                    else:
                        log_file_out('第'+str(i+1)+'页'+'评估对象选择框验证成功')
                else:
                    if len(driver.find_elements_by_xpath('//div[text()="评估系统、部件"]')) != 0:
                        log_file_out('第'+str(i+1)+'页'+'评估对象选择框验证失败')
                    else:
                        log_file_out('第'+str(i+1)+'页'+'评估对象选择框验证成功')

        # 重置
        driver.find_elements_by_class_name('ct-input-group-items')[1].click()
        # 计算状态选择框
        driver.find_elements_by_class_name('ivu-select-placeholder')[1].click()
        if value1 == 1:
            driver.find_element_by_xpath('//li[text()="未计算"]').click()
        elif value1 == 2:
            driver.find_element_by_xpath('//li[text()="计算中"]').click()
        elif value1 == 3:
            driver.find_element_by_xpath('//li[text()="计算异常"]').click()
        else:
            driver.find_element_by_xpath('//li[text()="计算完成"]').click()
        # 点击查询按钮
        driver.find_element_by_class_name('ct-input-group-items').click()
        time.sleep(2)
        # 查询的数量
        nu2 = driver.find_elements_by_class_name('ivu-page-total')[0].text
        nu3 = re.findall(r'\d+', nu2)

        if int(nu3[0]) == 0:
            log_file_out('验证成功')
        elif int(nu3[0]) <= 10:
            if value1 == 1:
                if len(driver.find_elements_by_xpath('//div[text()="计算中"]')) !=0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) !=0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                    log_file_out('计算状态选择框验证失败')
                else:
                    log_file_out('计算状态选择框验证成功')
            elif value1 == 2:
                if len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                    log_file_out('计算状态选择框验证失败')
                else:
                    log_file_out('计算状态选择框验证成功')
            elif value1 == 3:
                if len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算中"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                    log_file_out('计算状态选择框验证失败')
                else:
                    log_file_out('计算状态选择框验证成功')
            else:
                if len(driver.find_elements_by_xpath('//div[text()="计算中"]')) !=0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) !=0 and \
                        len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0:
                    log_file_out('计算状态选择框验证失败')
                else:
                    log_file_out('计算状态选择框验证成功')
        else:
            for i in range(0,(int(nu3[0])//10)+1):
                driver.find_element_by_xpath('//a[text()="{}"]'.format(i+1)).click()
                if value1 == 1:
                    if len(driver.find_elements_by_xpath('//div[text()="计算中"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                        log_file_out('第' + str(i) + '页' + '计算状态选择框验证失败')
                    else:
                        log_file_out('第' + str(i) + '页' + '计算状态选择框验证成功')
                elif value1 == 2:
                    if len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                        log_file_out('第' + str(i) + '页' + '计算状态选择框验证失败')
                    else:
                        log_file_out('第' + str(i) + '页' + '计算状态选择框验证成功')
                elif value1 == 3:
                    if len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算中"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                        log_file_out('第' + str(i) + '页' + '计算状态选择框验证失败')
                    else:
                        log_file_out('第' + str(i) + '页' + '计算状态选择框验证成功')
                else:
                    if len(driver.find_elements_by_xpath('//div[text()="计算中"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0:
                        log_file_out('第' + str(i) + '页' + '计算状态选择框验证失败')
                    else:
                        log_file_out('第' + str(i) + '页' + '计算状态选择框验证成功')

# 指标对比分析的高级检索
def compare_high_select(url,username,password,contents,modelName,value,value1):
    # option = webdriver.ChromeOptions()
    # option.add_argument("headless")
    # driver = webdriver.Chrome(chrome_options=option,                                                                executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    log_file_out('-----' + contents[1] + '高级检索验证' + '-----')
    status = new_built(driver, url, username, password, contents, 2)
    if status is True:
        log_file_out('登录成功')
        time.sleep(2)

        if driver.find_element_by_xpath('//*[@id="right_content"]/div/div[1]/div/p').text == contents[1]:
            log_file_out(contents[1]+'菜单名称与菜单页内容对应')
        else:
            log_file_out(contents[1] + '菜单名称与菜单页内容不对应')

        time.sleep(1)
        # 点击更多
        driver.find_element_by_class_name('beta-form-more').click()

        driver.find_elements_by_class_name('ivu-input')[0].send_keys(modelName)
        time.sleep(0.5)
        # 点击查询按钮
        driver.find_element_by_class_name('ct-input-group-items').click()
        time.sleep(0.5)
        su = driver.find_elements_by_class_name('ivu-page-total')[0].text


        su1 = re.findall(r'\d+',su)
        if int(su1[0]) == 1:
            log_file_out('模型名称输入框高级搜索验证成功')
        else:
            log_file_out('模型名称输入框高级搜索验证失败')

        # 重置
        driver.find_elements_by_class_name('ct-input-group-items')[1].click()
        # 评估对象选择框
        driver.find_element_by_class_name('ivu-select-placeholder').click()
        if value == 1:
            driver.find_element_by_xpath('//li[text()="评估系统、部件"]').click()
        else:
            driver.find_element_by_xpath('//li[text()="故障模式"]').click()
        d = {1:'评估系统、部件',2:'故障模式'}
        # 点击查询按钮
        driver.find_element_by_class_name('ct-input-group-items').click()
        time.sleep(2)
        # 查询的数量
        nu = driver.find_elements_by_class_name('ivu-page-total')[0].text
        nu1 = re.findall(r'\d+', nu)

        if int(nu1[0]) == 0:
            log_file_out('验证成功')
        elif int(nu1[0]) <= 10:
            if value == 1:
                if len(driver.find_elements_by_xpath('//div[text()="故障模式"]')) !=0:
                    log_file_out('评估对象选择框验证失败')
                else:
                    log_file_out('评估对象选择框验证成功')
            else:
                if len(driver.find_elements_by_xpath('//div[text()="评估系统、部件"]')) != 0:
                    log_file_out('评估对象选择框验证失败')
                else:
                    log_file_out('评估对象选择框验证成功')
        else:
            for i in range(0,(int(nu1[0])//10)+1):
                driver.find_element_by_xpath('//a[text()="{}"]'.format(i+1)).click()
                if value == 1:
                    if len(driver.find_elements_by_xpath('//div[text()="故障模式"]')) != 0:
                        log_file_out('第'+str(i+1)+'页'+'评估对象选择框验证失败')
                    else:
                        log_file_out('第'+str(i+1)+'页'+'评估对象选择框验证成功')
                else:
                    if len(driver.find_elements_by_xpath('//div[text()="评估系统、部件"]')) != 0:
                        log_file_out('第'+str(i+1)+'页'+'评估对象选择框验证失败')
                    else:
                        log_file_out('第'+str(i+1)+'页'+'评估对象选择框验证成功')

        # 重置
        driver.find_elements_by_class_name('ct-input-group-items')[1].click()
        # 计算状态选择框
        driver.find_elements_by_class_name('ivu-select-placeholder')[1].click()
        if value1 == 1:
            driver.find_element_by_xpath('//li[text()="未计算"]').click()
        elif value1 == 2:
            driver.find_element_by_xpath('//li[text()="计算中"]').click()
        elif value1 == 3:
            driver.find_element_by_xpath('//li[text()="计算异常"]').click()
        else:
            driver.find_element_by_xpath('//li[text()="计算完成"]').click()
        # 点击查询按钮
        driver.find_element_by_class_name('ct-input-group-items').click()
        time.sleep(2)
        # 查询的数量
        nu2 = driver.find_elements_by_class_name('ivu-page-total')[0].text
        nu3 = re.findall(r'\d+', nu2)

        if int(nu3[0]) == 0:
            log_file_out('验证成功')
        elif int(nu3[0]) <= 10:
            if value1 == 1:
                if len(driver.find_elements_by_xpath('//div[text()="计算中"]')) !=0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) !=0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                    log_file_out('计算状态选择框验证失败')
                else:
                    log_file_out('计算状态选择框验证成功')
            elif value1 == 2:
                if len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                    log_file_out('计算状态选择框验证失败')
                else:
                    log_file_out('计算状态选择框验证成功')
            elif value1 == 3:
                if len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算中"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                    log_file_out('计算状态选择框验证失败')
                else:
                    log_file_out('计算状态选择框验证成功')
            else:
                if len(driver.find_elements_by_xpath('//div[text()="计算中"]')) !=0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) !=0 and \
                        len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0:
                    log_file_out('计算状态选择框验证失败')
                else:
                    log_file_out('计算状态选择框验证成功')
        else:
            for i in range(0,(int(nu3[0])//10)+1):
                driver.find_element_by_xpath('//a[text()="{}"]'.format(i+1)).click()
                if value1 == 1:
                    if len(driver.find_elements_by_xpath('//div[text()="计算中"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                        log_file_out('第' + str(i+1) + '页' + '计算状态选择框验证失败')
                    else:
                        log_file_out('第' + str(i+1) + '页' + '计算状态选择框验证成功')
                elif value1 == 2:
                    if len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                        log_file_out('第' + str(i+1) + '页' + '计算状态选择框验证失败')
                    else:
                        log_file_out('第' + str(i+1) + '页' + '计算状态选择框验证成功')
                elif value1 == 3:
                    if len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算中"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                        log_file_out('第' + str(i+1) + '页' + '计算状态选择框验证失败')
                    else:
                        log_file_out('第' + str(i+1) + '页' + '计算状态选择框验证成功')
                else:
                    if len(driver.find_elements_by_xpath('//div[text()="计算中"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0:
                        log_file_out('第' + str(i+1) + '页' + '计算状态选择框验证失败')
                    else:
                        log_file_out('第' + str(i+1) + '页' + '计算状态选择框验证成功')
    else:
        log_file_out('登录失败')

# 自动femca的高级检索
def femca_high_select(url,username,password,contents,modelName,value):
    # option = webdriver.ChromeOptions()
    # option.add_argument("headless")
    # driver = webdriver.Chrome(chrome_options=option,                                                                executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    log_file_out('-----' + contents[1] + '高级检索验证' + '-----')
    status = new_built(driver, url, username, password, contents, 2)
    if status is True:
        log_file_out('登录成功')
        time.sleep(2)

        time.sleep(1)

        if driver.find_element_by_xpath('//*[@id="right_content"]/div/div[1]/div/p').text == contents[1]:
            log_file_out(contents[1]+'菜单名称与菜单页内容对应')
        else:
            log_file_out(contents[1] + '菜单名称与菜单页内容不对应')

        time.sleep(1)
        # 点击更多
        driver.find_element_by_class_name('beta-form-more').click()

        driver.find_elements_by_class_name('ivu-input')[0].send_keys(modelName)
        time.sleep(0.5)
        # 点击查询按钮
        driver.find_element_by_class_name('ct-input-group-items').click()
        time.sleep(0.5)
        su = driver.find_elements_by_class_name('ivu-page-total')[0].text


        su1 = re.findall(r'\d+',su)
        if int(su1[0]) == 1:
            log_file_out('模型名称输入框高级搜索验证成功')
        else:
            log_file_out('模型名称输入框高级搜索验证失败')


        # 重置
        driver.find_elements_by_class_name('ct-input-group-items')[1].click()
        # 计算状态选择框
        driver.find_element_by_class_name('ivu-select-placeholder').click()
        if value == 1:
            driver.find_element_by_xpath('//li[text()="未计算"]').click()
        elif value == 2:
            driver.find_element_by_xpath('//li[text()="计算中"]').click()
        elif value == 3:
            driver.find_element_by_xpath('//li[text()="计算异常"]').click()
        else:
            driver.find_element_by_xpath('//li[text()="计算完成"]').click()
        # 点击查询按钮
        driver.find_element_by_class_name('ct-input-group-items').click()
        time.sleep(2)
        # 查询的数量
        nu = driver.find_elements_by_class_name('ivu-page-total')[0].text
        nu1 = re.findall(r'\d+', nu)
        L = []
        if int(nu1[0]) == 0:
            print('验证成功')
        elif int(nu1[0]) <= 10:
            if value == 1:
                if len(driver.find_elements_by_xpath('//div[text()="计算中"]')) !=0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) !=0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                    log_file_out('计算状态选择框验证失败')
                else:
                    log_file_out('计算状态选择框验证成功')
            elif value == 2:
                if len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                    log_file_out('计算状态选择框验证失败')
                else:
                    log_file_out('计算状态选择框验证成功')
            elif value == 3:
                if len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算中"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                    log_file_out('计算状态选择框验证失败')
                else:
                    log_file_out('计算状态选择框验证成功')
            else:
                if len(driver.find_elements_by_xpath('//div[text()="计算中"]')) !=0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) !=0 and \
                        len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0:
                    log_file_out('计算状态选择框验证失败')
                else:
                    log_file_out('计算状态选择框验证成功')
        else:
            for i in range(0,(int(nu1[0])//10)+1):
                driver.find_element_by_xpath('//a[text()="{}"]'.format(i+1)).click()
                if value == 1:
                    if len(driver.find_elements_by_xpath('//div[text()="计算中"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                        log_file_out('第' + str(i+1) + '页' + '计算状态选择框验证失败')
                    else:
                        log_file_out('第' + str(i+1) + '页' + '计算状态选择框验证成功')
                elif value == 2:
                    if len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                        log_file_out('第' + str(i+1) + '页' + '计算状态选择框验证失败')
                    else:
                        log_file_out('第' + str(i+1) + '页' + '计算状态选择框验证成功')
                elif value == 3:
                    if len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算中"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                        log_file_out('第' + str(i+1) + '页' + '计算状态选择框验证失败')
                    else:
                        log_file_out('第' + str(i+1) + '页' + '计算状态选择框验证成功')
                else:
                    if len(driver.find_elements_by_xpath('//div[text()="计算中"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0:
                        log_file_out('第' + str(i+1) + '页' + '计算状态选择框验证失败')
                    else:
                        log_file_out('第' + str(i+1) + '页' + '计算状态选择框验证成功')
    else:
        log_file_out('登录失败')

# 指标占比分析的高级检索
def fault_high_select(url,username,password,contents,modelName,value,value1):
    # option = webdriver.ChromeOptions()
    # option.add_argument("headless")
    # driver = webdriver.Chrome(chrome_options=option,                                                                executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    log_file_out('-----' + contents[1] + '高级检索验证' + '-----')
    status = new_built(driver, url, username, password, contents, 2)
    if status is True:
        log_file_out('登录成功')
        time.sleep(2)

        if driver.find_element_by_xpath('//*[@id="right_content"]/div/div[1]/div/p').text == contents[1]:
            log_file_out(contents[1]+'菜单名称与菜单页内容对应')
        else:
            log_file_out(contents[1] + '菜单名称与菜单页内容不对应')

        time.sleep(1)
        # 点击更多
        driver.find_element_by_class_name('beta-form-more').click()

        driver.find_elements_by_class_name('ivu-input')[0].send_keys(modelName)
        time.sleep(0.5)
        # 点击查询按钮
        driver.find_element_by_class_name('ct-input-group-items').click()
        time.sleep(0.5)
        su = driver.find_elements_by_class_name('ivu-page-total')[0].text


        su1 = re.findall(r'\d+',su)
        if int(su1[0]) == 1:
            log_file_out('模型名称输入框高级搜索验证成功')
        else:
            log_file_out('模型名称输入框高级搜索验证失败')

        # 重置
        driver.find_elements_by_class_name('ct-input-group-items')[1].click()
        # 评估对象选择框
        driver.find_element_by_class_name('ivu-select-placeholder').click()
        if value == 1:
            driver.find_element_by_xpath('//li[text()="评估系统、部件"]').click()
        else:
            driver.find_element_by_xpath('//li[text()="故障模式"]').click()
        d = {1:'评估系统、部件',2:'故障模式'}
        # 点击查询按钮
        driver.find_element_by_class_name('ct-input-group-items').click()
        time.sleep(2)
        # 查询的数量
        nu = driver.find_elements_by_class_name('ivu-page-total')[0].text
        nu1 = re.findall(r'\d+', nu)

        if int(nu1[0]) == 0:
            log_file_out('验证成功')
        elif int(nu1[0]) <= 10:
            if value == 1:
                if len(driver.find_elements_by_xpath('//div[text()="故障模式"]')) !=0:
                    log_file_out('评估对象选择框验证失败')
                else:
                    log_file_out('评估对象选择框验证成功')
            else:
                if len(driver.find_elements_by_xpath('//div[text()="评估系统、部件"]')) != 0:
                    log_file_out('评估对象选择框验证失败')
                else:
                    log_file_out('评估对象选择框验证成功')
        else:
            for i in range(0,(int(nu1[0])//10)+1):
                driver.find_element_by_xpath('//a[text()="{}"]'.format(i+1)).click()
                if value == 1:
                    if len(driver.find_elements_by_xpath('//div[text()="故障模式"]')) != 0:
                        log_file_out('第'+str(i+1)+'页'+'评估对象选择框验证失败')
                    else:
                        log_file_out('第'+str(i+1)+'页'+'评估对象选择框验证成功')
                else:
                    if len(driver.find_elements_by_xpath('//div[text()="评估系统、部件"]')) != 0:
                        log_file_out('第'+str(i+1)+'页'+'评估对象选择框验证失败')
                    else:
                        log_file_out('第'+str(i+1)+'页'+'评估对象选择框验证成功')

        # 重置
        driver.find_elements_by_class_name('ct-input-group-items')[1].click()
        # 计算状态选择框
        driver.find_elements_by_class_name('ivu-select-placeholder')[1].click()
        if value1 == 1:
            driver.find_element_by_xpath('//li[text()="未计算"]').click()
        elif value1 == 2:
            driver.find_element_by_xpath('//li[text()="计算中"]').click()
        elif value1 == 3:
            driver.find_element_by_xpath('//li[text()="计算异常"]').click()
        else:
            driver.find_element_by_xpath('//li[text()="计算完成"]').click()
        # 点击查询按钮
        driver.find_element_by_class_name('ct-input-group-items').click()
        time.sleep(2)
        # 查询的数量
        nu2 = driver.find_elements_by_class_name('ivu-page-total')[0].text
        nu3 = re.findall(r'\d+', nu2)

        if int(nu3[0]) == 0:
            print('验证成功')
        elif int(nu3[0]) <= 10:
            if value1 == 1:
                if len(driver.find_elements_by_xpath('//div[text()="计算中"]')) !=0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) !=0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                    log_file_out('计算状态选择框验证失败')
                else:
                    log_file_out('计算状态选择框验证成功')
            elif value1 == 2:
                if len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                    log_file_out('计算状态选择框验证失败')
                else:
                    log_file_out('计算状态选择框验证成功')
            elif value1 == 3:
                if len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算中"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                    log_file_out('计算状态选择框验证失败')
                else:
                    log_file_out('计算状态选择框验证成功')
            else:
                if len(driver.find_elements_by_xpath('//div[text()="计算中"]')) !=0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) !=0 and \
                        len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0:
                    log_file_out('计算状态选择框验证失败')
                else:
                    log_file_out('计算状态选择框验证成功')
        else:
            for i in range(0,(int(nu3[0])//10)+1):
                driver.find_element_by_xpath('//a[text()="{}"]'.format(i+1)).click()
                if value1 == 1:
                    if len(driver.find_elements_by_xpath('//div[text()="计算中"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                        log_file_out('第' + str(i) + '页' + '计算状态选择框验证失败')
                    else:
                        log_file_out('第' + str(i) + '页' + '计算状态选择框验证成功')
                elif value1 == 2:
                    if len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                        log_file_out('第' + str(i) + '页' + '计算状态选择框验证失败')
                    else:
                        log_file_out('第' + str(i) + '页' + '计算状态选择框验证成功')
                elif value1 == 3:
                    if len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算中"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                        log_file_out('第' + str(i+1) + '页' + '计算状态选择框验证失败')
                    else:
                        log_file_out('第' + str(i+1) + '页' + '计算状态选择框验证成功')
                else:
                    if len(driver.find_elements_by_xpath('//div[text()="计算中"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0:
                        log_file_out('第' + str(i+1) + '页' + '计算状态选择框验证失败')
                    else:
                        log_file_out('第' + str(i+1) + '页' + '计算状态选择框验证成功')
    else:
        log_file_out('登录失败')

# rcma的高级检索
def rcma_high_select(url,username,password,contents,modelCode,modelName):
    # option = webdriver.ChromeOptions()
    # option.add_argument("headless")
    # driver = webdriver.Chrome(chrome_options=option,                                                                executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    log_file_out('-----' + contents[1] + '高级检索验证' + '-----')
    status = new_built(driver, url, username, password, contents, 2)
    if status is True:
        log_file_out('登录成功')
        time.sleep(2)

        if driver.find_element_by_xpath('//*[@id="right_content"]/div/div[1]/div/p').text == contents[1]:
            log_file_out(contents[1]+'菜单名称与菜单页内容对应')
        else:
            log_file_out(contents[1] + '菜单名称与菜单页内容不对应')

        time.sleep(1)
        # 点击更多
        driver.find_element_by_class_name('beta-form-more').click()

        driver.find_elements_by_class_name('ivu-input')[0].send_keys(modelCode)
        time.sleep(0.5)
        # 点击查询按钮
        driver.find_element_by_class_name('ct-input-group-items').click()
        time.sleep(0.5)
        su = driver.find_elements_by_class_name('ivu-page-total')[0].text


        su1 = re.findall(r'\d+',su)
        if int(su1[0]) == 1:
            log_file_out('模型编码输入框高级搜索验证成功')
        else:
            log_file_out('模型编码输入框高级搜索验证失败')


        # 重置
        driver.find_elements_by_class_name('ct-input-group-items')[1].click()
        # 模型名称
        driver.find_elements_by_class_name('ivu-input')[1].send_keys(modelName)
        time.sleep(0.5)
        # 点击查询按钮
        driver.find_element_by_class_name('ct-input-group-items').click()
        time.sleep(1)
        su = driver.find_elements_by_class_name('ivu-page-total')[0].text

        su1 = re.findall(r'\d+', su)
        if int(su1[0]) == 1:
            log_file_out('模型名称输入框高级搜索验证成功')
        else:
            log_file_out('模型名称输入框高级搜索验证失败')

# rams指标建模高级检索
def Ramssave_high_select(url,username,password,contents,modelName,value,value1):
    # option = webdriver.ChromeOptions()
    # option.add_argument("headless")
    # driver = webdriver.Chrome(chrome_options=option,                                                                executable_path=r'C:\Users\a\PycharmProjects\untitled\new_selenium\apps\chromedriver.exe')
    driver = webdriver.Chrome(executable_path=r'{}/apps/chromedriver.exe'.format(path_dir))
    log_file_out('-----' + contents[1] + '高级检索验证' + '-----')
    status = new_built(driver, url, username, password, contents, 2)
    if status is True:
        log_file_out('登录成功')
        time.sleep(2)

        if driver.find_element_by_xpath('//*[@id="right_content"]/div/div[1]/div/p').text == contents[1]:
            log_file_out(contents[1]+'菜单名称与菜单页内容对应')
        else:
            log_file_out(contents[1] + '菜单名称与菜单页内容不对应')

        time.sleep(1)
        # 点击更多
        driver.find_element_by_class_name('beta-form-more').click()

        driver.find_elements_by_class_name('ivu-input')[0].send_keys(modelName)
        time.sleep(0.5)
        # 点击查询按钮
        driver.find_element_by_class_name('ct-input-group-items').click()
        time.sleep(0.5)
        su = driver.find_elements_by_class_name('ivu-page-total')[0].text


        su1 = re.findall(r'\d+',su)
        if int(su1[0]) == 1:
            log_file_out('模型名称输入框高级搜索验证成功')
        else:
            log_file_out('模型名称输入框高级搜索验证失败')

        # 重置
        driver.find_elements_by_class_name('ct-input-group-items')[1].click()
        # 评估对象选择框
        driver.find_element_by_class_name('ivu-select-placeholder').click()
        if value == 1:
            driver.find_element_by_xpath('//li[text()="评估系统、部件"]').click()
        else:
            driver.find_element_by_xpath('//li[text()="故障模式"]').click()
        d = {1:'评估系统、部件',2:'故障模式'}
        # 点击查询按钮
        driver.find_element_by_class_name('ct-input-group-items').click()
        time.sleep(2)
        # 查询的数量
        nu = driver.find_elements_by_class_name('ivu-page-total')[0].text
        nu1 = re.findall(r'\d+', nu)

        if int(nu1[0]) == 0:
            log_file_out('验证成功')
        elif int(nu1[0]) <= 10:
            if value == 1:
                if len(driver.find_elements_by_xpath('//div[text()="故障模式"]')) !=0:
                    log_file_out('评估对象选择框验证失败')
                else:
                    log_file_out('评估对象选择框验证成功')
            else:
                if len(driver.find_elements_by_xpath('//div[text()="评估系统、部件"]')) != 0:
                    log_file_out('评估对象选择框验证失败')
                else:
                    log_file_out('评估对象选择框验证成功')
        else:
            for i in range(0,(int(nu1[0])//10)+1):
                driver.find_element_by_xpath('//a[text()="{}"]'.format(i+1)).click()
                if value == 1:
                    if len(driver.find_elements_by_xpath('//div[text()="故障模式"]')) != 0:
                        log_file_out('第'+str(i+1)+'页'+'评估对象选择框验证失败')
                    else:
                        log_file_out('第'+str(i+1)+'页'+'评估对象选择框验证成功')
                else:
                    if len(driver.find_elements_by_xpath('//div[text()="评估系统、部件"]')) != 0:
                        log_file_out('第'+str(i+1)+'页'+'评估对象选择框验证失败')
                    else:
                        log_file_out('第'+str(i+1)+'页'+'评估对象选择框验证成功')

        # 重置
        driver.find_elements_by_class_name('ct-input-group-items')[1].click()
        # 计算状态选择框
        driver.find_elements_by_class_name('ivu-select-placeholder')[1].click()
        if value1 == 1:
            driver.find_element_by_xpath('//li[text()="未计算"]').click()
        elif value1 == 2:
            driver.find_element_by_xpath('//li[text()="计算中"]').click()
        elif value1 == 3:
            driver.find_element_by_xpath('//li[text()="计算异常"]').click()
        else:
            driver.find_element_by_xpath('//li[text()="计算完成"]').click()
        # 点击查询按钮
        driver.find_element_by_class_name('ct-input-group-items').click()
        time.sleep(2)
        # 查询的数量
        nu2 = driver.find_elements_by_class_name('ivu-page-total')[0].text
        nu3 = re.findall(r'\d+', nu2)

        if int(nu3[0]) == 0:
            log_file_out('验证成功')
        elif int(nu3[0]) <= 10:
            if value1 == 1:
                if len(driver.find_elements_by_xpath('//div[text()="计算中"]')) !=0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) !=0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                    log_file_out('计算状态选择框验证失败')
                else:
                    log_file_out('计算状态选择框验证成功')
            elif value1 == 2:
                if len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                    log_file_out('计算状态选择框验证失败')
                else:
                    log_file_out('计算状态选择框验证成功')
            elif value1 == 3:
                if len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算中"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                    log_file_out('计算状态选择框验证失败')
                else:
                    log_file_out('计算状态选择框验证成功')
            else:
                if len(driver.find_elements_by_xpath('//div[text()="计算中"]')) !=0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) !=0 and \
                        len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0:
                    log_file_out('计算状态选择框验证失败')
                else:
                    log_file_out('计算状态选择框验证成功')
        else:
            for i in range(0,(int(nu3[0])//10)+1):
                driver.find_element_by_xpath('//a[text()="{}"]'.format(i+1)).click()
                if value1 == 1:
                    if len(driver.find_elements_by_xpath('//div[text()="计算中"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                        log_file_out('第' + str(i+1) + '页' + '计算状态选择框验证失败')
                    else:
                        log_file_out('第' + str(i+1) + '页' + '计算状态选择框验证成功')
                elif value1 == 2:
                    if len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                        log_file_out('第' + str(i+1) + '页' + '计算状态选择框验证失败')
                    else:
                        log_file_out('第' + str(i+1) + '页' + '计算状态选择框验证成功')
                elif value1 == 3:
                    if len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算中"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                        log_file_out('第' + str(i+1) + '页' + '计算状态选择框验证失败')
                    else:
                        log_file_out('第' + str(i+1) + '页' + '计算状态选择框验证成功')
                else:
                    if len(driver.find_elements_by_xpath('//div[text()="计算中"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) != 0 and \
                            len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0:
                        log_file_out('第' + str(i+1) + '页' + '计算状态选择框验证失败')
                    else:
                        log_file_out('第' + str(i+1) + '页' + '计算状态选择框验证成功')



