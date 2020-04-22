from config.log_config import logger
import random
from bin.t import *

# 一个一级部件下的一个子集部件
def deal_new_fault(driver):
    try:
        text = ''
        text2 = ''
        text3 = ''
        text4 = ''
        fault_next_1 = ''
        fault_next_2 = ''
        fault_next_3 = ''
        fault_next_4 = ''

        # 获取所有的一级节点
        first = len(driver.find_elements_by_class_name("jstree-anchor"))

        # 点击随机的一个一级节点
        fault_1 = random.randint(1,first-1)
        # fault_1 = 13
        fault_next_1 = driver.find_elements_by_class_name("jstree-anchor")[fault_1].get_attribute('id')

        text = driver.find_elements_by_class_name("jstree-anchor")[fault_1].text.lstrip()

        # 判断是否有下级节点
        if 'jstree-leaf' not in driver.find_element_by_xpath("//a[text()=\'{}\']/..".format(text)).get_attribute('class'):
            # Method(driver).click('xpath', '//*[@id= \'{}\']/i'.format(fault_next_1[:-7]))
            driver.execute_script('$("#faultObjectTree").jstree().open_node("{}")'.format(fault_next_1[:-7]))
            # 随机1级节点下的二级节点
            # second = len(driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_1[:-7])))
            second = wait_time(driver, fault_next_1)
            fault_second = random.randint(0,second-1)

            text2 = driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_1[:-7]))[
                fault_second].text.lstrip()
            fault_next_2 = Method(driver).contains_xpath('get', text2)
            # fault_second = 2

            # 判断二级节点是否有下级节点
            if 'jstree-leaf' not in driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_1[:-7]))[fault_second].get_attribute('class'):
                # 随机是否要去点击下一级节点
                # select = random.randint(0,1)
                select = 1
                if select == 0:

                    driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_1[:-7]))[fault_second].click()

                    time.sleep(2)
                    driver.find_element_by_xpath('//*[@id="middleTable"]/tbody/tr[1]/td[1]/input').click()
                    Method(driver).click('id', "right-move")

                else:
                    # driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li/i'.format(fault_next_1[:-7]))[fault_second].click()
                    driver.execute_script('$("#faultObjectTree").jstree().open_node("{}")'.format(fault_next_2[:-7]))
                    time.sleep(2)
                    # third = random.randint(0,len(driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.
                    #                                                          format(fault_next_2[:-7])))-1)
                    third1 = wait_time(driver,fault_next_2)
                    third = random.randint(0,third1-1)

                    text3 = driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_2[:-7]))[
                        third].text.lstrip()

                    fault_next_3 = Method(driver).contains_xpath('get', text3)
                    time.sleep(2)
                    # third = 13
                    # 判断三级节点是否有下一级子节点
                    if 'jstree-leaf' not in driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_2[:-7]))[third].get_attribute('class'):
                        # driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li/ul/li/i'.format(fault_next_1[:-7]))[
                        #     third].click()
                        driver.execute_script(
                            '$("#faultObjectTree").jstree().open_node("{}")'.format(fault_next_3[:-7]))
                        time.sleep(2)
                        fourth1 = wait_time(driver, fault_next_3)

                        fourth = random.randint(0, fourth1 - 1)
                        # fourth = random.randint(0,len(driver.find_elements_by_xpath('//*[@id= \'{}\']'
                        #                                                             '/ul/li/ul/li/ul/li'.
                        #                                                       format(fault_next_1[:-7])))-1)

                        # text3 = driver.find_elements_by_xpath('//*[@id= \'{}\']''/ul/li/ul/li/ul/li'.format(fault_next_1[:-7]))[fourth].text.lstrip()
                        text4 = driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_3[:-7]))[
                            fourth].text.lstrip()

                        time.sleep(2)
                        # driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li/ul/li/i'.format(fault_next_1[:-7]))[third].click()
                        driver.execute_script(
                            '$("#faultObjectTree").jstree().close_node("{}")'.format(fault_next_3[:-7]))
                        time.sleep(1)
                        driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_2[:-7]))[third].click()

                        time.sleep(2)
                        try:
                            driver.find_element_by_xpath("//td[text()=\'{}\']/../td[1]/input".format(text4)).click()
                            Method(driver).click('id', "right-move")
                        except:
                            try:
                                driver.find_element_by_xpath('//*[@class="pull-right pagination"]/ul/li[4]/a').click()
                                driver.find_element_by_xpath("//td[text()=\'{}\']/../td[1]/input".format(text4)).click()
                                Method(driver).click('id', "right-move")
                            except:
                                time.sleep(1)
                                driver.find_element_by_xpath('//*[@id="middleTable"]/tbody/tr[1]/td[1]/input').click()
                                time.sleep(1)
                                Method(driver).click('id', "right-move")

                    else:
                        # 没有就获取三级子节点的值 在二级子节点中点击它
                        # text2 = driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li/ul/li'.
                        #                                      format(fault_next_1[:-7]))[third].text.lstrip()
                        time.sleep(2)

                        # driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li/i'.format(fault_next_1[:-7]))[
                        #     fault_second].click()
                        driver.execute_script(
                            '$("#faultObjectTree").jstree().close_node("{}")'.format(fault_next_2[:-7]))

                        driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_1[:-7]))[
                            fault_second].click()

                        time.sleep(2)
                        try:
                            driver.find_element_by_xpath("//td[text()=\'{}\']/../td[1]/input".format(text3)).click()
                            Method(driver).click('id', "right-move")
                        except:
                            try:
                                driver.find_element_by_xpath('//*[@class="pull-right pagination"]/ul/li[4]/a').click()
                                driver.find_element_by_xpath("//td[text()=\'{}\']/../td[1]/input".format(text3)).click()
                                Method(driver).click('id', "right-move")
                            except:
                                time.sleep(1)
                                driver.find_element_by_xpath('//*[@id="middleTable"]/tbody/tr[1]/td[1]/input').click()
                                time.sleep(1)
                                Method(driver).click('id', "right-move")

            else:
                # 获取二级节点的值
                # text1 = driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_1[:-7]))[fault_second].text.lstrip()
                # Method(driver).click('xpath', '//*[@id= \'{}\']/i'.format(fault_next_1[:-7]))
                driver.execute_script('$("#faultObjectTree").jstree().close_node("{}")'.format(fault_next_1[:-7]))
                time.sleep(2)
                # 点击1级节点 再点击相应的二级节点
                Method(driver).click('xpath', '//*[@id= \'{}\']'.format(fault_next_1[:-7]))
                time.sleep(2)
                try:
                    driver.find_element_by_xpath("//td[text()=\'{}\']/../td[1]/input".format(text2)).click()
                    Method(driver).click('id', "right-move")
                except:
                    try:
                        driver.find_element_by_xpath('//*[@class="pull-right pagination"]/ul/li[4]/a').click()
                        driver.find_element_by_xpath("//td[text()=\'{}\']/../td[1]/input".format(text2)).click()
                        Method(driver).click('id', "right-move")
                    except:
                        time.sleep(1)
                        driver.find_element_by_xpath('//*[@id="middleTable"]/tbody/tr[1]/td[1]/input').click()
                        time.sleep(1)
                        Method(driver).click('id', "right-move")

        else:
            driver.find_elements_by_class_name("jstree-anchor")[fault_1].click()
            time.sleep(2)
            driver.find_element_by_xpath('//*[@id="middleTable"]/tbody/tr[1]/td[1]/input').click()
            Method(driver).click('id', "right-move")
        return True
    except Exception as e:
        logger.error(e)
        return False

# 多个一级部件下的一个子集部件
def deal_new_fault1(driver):
    # text = ''
    # text2 = ''
    # text3 = ''
    # text4 = ''
    # fault_next_1 = ''
    # fault_next_2 = ''
    # fault_next_3 = ''
    # fault_next_4 = ''
    try:
        L = []
        first = len(driver.find_elements_by_class_name("jstree-anchor"))
        # while len(L) < random.randint(2,len(driver.find_elements_by_class_name("jstree-anchor"))-1):
        while len(L) < 5:
        # for i in range(0,random.randint(2,len(driver.find_elements_by_class_name("jstree-anchor"))-1)):
            fault_1 = random.randint(1, first - 1)

            if fault_1 not in L:
                # fault_1 = 13
                L.append(fault_1)
                fault_next_1 = driver.find_elements_by_class_name("jstree-anchor")[fault_1].get_attribute('id')

                text = driver.find_elements_by_class_name("jstree-anchor")[fault_1].text.lstrip()

                if 'jstree-leaf' not in driver.find_element_by_xpath("//a[text()=\'{}\']/..".format(text)).get_attribute('class'):
                    # Method(driver).click('xpath', '//*[@id= \'{}\']/i'.format(fault_next_1[:-7]))
                    driver.execute_script('$("#faultObjectTree").jstree().open_node("{}")'.format(fault_next_1[:-7]))
                    # second = len(driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_1[:-7])))
                    second = wait_time(driver, fault_next_1)
                    fault_second = random.randint(0, second - 1)

                    text2 = driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_1[:-7]))[
                        fault_second].text.lstrip()
                    fault_next_2 = Method(driver).contains_xpath('get', text2)

                    # fault_second = 1
                    # while True:
                    if 'jstree-leaf' not in driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_1[:-7]))[fault_second].get_attribute('class'):
                        select = random.randint(0, 1)
                        if select == 0:
                            driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_1[:-7]))[
                                fault_second].click()

                            time.sleep(2)
                            driver.find_element_by_xpath('//*[@id="middleTable"]/tbody/tr[1]/td[1]/input').click()
                            Method(driver).click('id', "right-move")

                        else:
                            # driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li/i'.format(fault_next_1[:-7]))[
                            #     fault_second].click()
                            driver.execute_script('$("#faultObjectTree").jstree().open_node("{}")'.format(fault_next_2[:-7]))
                            time.sleep(2)
                            # third = random.randint(0, len(driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li/ul/li'.
                            #                                                             format(fault_next_1[:-7])))-1)
                            third1 = wait_time(driver, fault_next_2)
                            third = random.randint(0, third1 - 1)

                            text3 = driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_2[:-7]))[
                                third].text.lstrip()

                            fault_next_3 = Method(driver).contains_xpath('get', text3)
                            time.sleep(2)
                            if 'jstree-leaf' not in driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_2[:-7]))[third].get_attribute('class'):
                                # driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li/ul/li/i'.format(fault_next_1[:-7]))[third].click()
                                driver.execute_script('$("#faultObjectTree").jstree().open_node("{}")'.format(fault_next_3[:-7]))
                                time.sleep(2)
                                # fourth = random.randint(0, len(driver.find_elements_by_xpath('//*[@id= \'{}\']''/ul/li/ul/li/ul/li'.format(fault_next_1[:-7]))) - 1)
                                fourth1 = wait_time(driver, fault_next_3)

                                fourth = random.randint(0, fourth1 - 1)
                                text4 = driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_3[:-7]))[
                                    fourth].text.lstrip()

                                time.sleep(2)
                                # driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li/ul/li/i'.format(fault_next_1[:-7]))[third].click()
                                driver.execute_script(
                                    '$("#faultObjectTree").jstree().close_node("{}")'.format(fault_next_3[:-7]))
                                time.sleep(1)
                                driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_2[:-7]))[
                                    third].click()

                                time.sleep(2)
                                try:
                                    driver.find_element_by_xpath("//td[text()=\'{}\']/../td[1]/input".format(text4)).click()
                                    Method(driver).click('id', "right-move")
                                except:
                                    try:
                                        driver.find_element_by_xpath('//*[@class="pull-right pagination"]/ul/li[4]/a').click()
                                        driver.find_element_by_xpath("//td[text()=\'{}\']/../td[1]/input".format(text4)).click()
                                        Method(driver).click('id', "right-move")
                                    except:
                                        time.sleep(1)
                                        driver.find_element_by_xpath('//*[@id="middleTable"]/tbody/tr[1]/td[1]/input').click()
                                        time.sleep(1)
                                        Method(driver).click('id', "right-move")
                            else:
                                time.sleep(2)

                                # driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li/i'.format(fault_next_1[:-7]))[
                                #     fault_second].click()
                                driver.execute_script('$("#faultObjectTree").jstree().close_node("{}")'.format(fault_next_2[:-7]))
                                driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_1[:-7]))[fault_second].click()

                                time.sleep(2)
                                try:
                                    driver.find_element_by_xpath("//td[text()=\'{}\']/../td[1]/input".format(text3)).click()
                                    Method(driver).click('id', "right-move")
                                except:
                                    try:
                                        driver.find_element_by_xpath('//*[@class="pull-right pagination"]/ul/li[4]/a').click()
                                        driver.find_element_by_xpath("//td[text()=\'{}\']/../td[1]/input".format(text3)).click()
                                        Method(driver).click('id', "right-move")
                                    except:
                                        time.sleep(1)
                                        driver.find_element_by_xpath('//*[@id="middleTable"]/tbody/tr[1]/td[1]/input').click()
                                        time.sleep(1)
                                        Method(driver).click('id', "right-move")
                    else:
                        driver.execute_script(
                            '$("#faultObjectTree").jstree().close_node("{}")'.format(fault_next_1[:-7]))
                        time.sleep(2)
                        # 点击1级节点 再点击相应的二级节点
                        Method(driver).click('xpath', '//*[@id= \'{}\']'.format(fault_next_1[:-7]))
                        time.sleep(2)
                        try:
                            driver.find_element_by_xpath("//td[text()=\'{}\']/../td[1]/input".format(text2)).click()
                            Method(driver).click('id', "right-move")
                        except:
                            try:
                                driver.find_element_by_xpath('//*[@class="pull-right pagination"]/ul/li[4]/a').click()
                                driver.find_element_by_xpath("//td[text()=\'{}\']/../td[1]/input".format(text2)).click()
                                Method(driver).click('id', "right-move")
                            except:
                                time.sleep(1)
                                driver.find_element_by_xpath('//*[@id="middleTable"]/tbody/tr[1]/td[1]/input').click()
                                time.sleep(1)
                                Method(driver).click('id', "right-move")
                            # break

                else:
                    driver.find_elements_by_class_name("jstree-anchor")[fault_1].click()
                    time.sleep(2)
                    driver.find_element_by_xpath('//*[@id="middleTable"]/tbody/tr[1]/td[1]/input').click()
                    Method(driver).click('id', "right-move")

                driver.execute_script('$("#faultObjectTree").jstree().close_node("{}")'.format(fault_next_1[:-7]))
        return True
    except Exception as e:
        logger.error(e)
        return False

# 一个一级部件下多个子集部件
def deal_new_fault2(driver):
    try:
        # 获取所有的一级节点
        first = len(driver.find_elements_by_class_name("jstree-anchor"))

        # 点击随机的一个一级节点
        fault_1 = random.randint(1,first-1)
        # fault_1 = 13
        fault_next_1 = driver.find_elements_by_class_name("jstree-anchor")[fault_1].get_attribute('id')

        text = driver.find_elements_by_class_name("jstree-anchor")[fault_1].text.lstrip()
        time.sleep(1)

        # 判断是否有下级节点
        if 'jstree-leaf' not in driver.find_element_by_xpath("//a[text()=\'{}\']/..".format(text)).get_attribute('class'):
            Method(driver).click('xpath', '//*[@id= \'{}\']/i'.format(fault_next_1[:-7]))
            time.sleep(1)
            # 随机1级节点下的二级节点
            second = len(driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_1[:-7])))
            if second == 1:
                driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_1[:-7]))[0].click()
                time.sleep(2)
                Method(driver).click('name', 'btSelectAll')
                Method(driver).click('xpath', '//*[@id="right-move"]')
            for i in range(0,random.randint(1,second-1)):
                if 'jstree-leaf' not in driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_1[:-7]))[i].get_attribute('class'):
                    driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_1[:-7]))[i].click()
                    time.sleep(2)
                    Method(driver).click('name', 'btSelectAll')
                    time.sleep(1)
                    Method(driver).click('xpath', '//*[@id="right-move"]')
                else:
                    text1 = driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_1[:-7]))[
                        i].text.lstrip()
                    Method(driver).click('xpath', '//*[@id= \'{}\']/i'.format(fault_next_1[:-7]))
                    time.sleep(2)
                    Method(driver).click('xpath', '//*[@id= \'{}\']'.format(fault_next_1[:-7]))
                    time.sleep(2)
                    try:
                        driver.find_element_by_xpath("//td[text()=\'{}\']/../td[1]/input".format(text1)).click()
                        Method(driver).click('id', "right-move")
                    except:
                        driver.find_element_by_xpath('//*[@class="pull-right pagination"]/ul/li[4]/a').click()
                        time.sleep(1)
                        driver.find_element_by_xpath("//td[text()=\'{}\']/../td[1]/input".format(text1)).click()
                        time.sleep(1)
                        Method(driver).click('id', "right-move")
                        time.sleep(1)
                        driver.find_element_by_xpath('//*[@class="pull-right pagination"]/ul/li[3]/a').click()

                    time.sleep(2)
                    Method(driver).click('xpath', '//*[@id= \'{}\']/i'.format(fault_next_1[:-7]))

        else:
            driver.find_elements_by_class_name("jstree-anchor")[fault_1].click()
            time.sleep(2)
            driver.find_element_by_xpath('//*[@id="middleTable"]/tbody/tr[1]/td[1]/input').click()
            Method(driver).click('id', "right-move")
        return True
    except Exception as e:
        logger.error(e)
        return False

# 一个一级部件下全量子集部件
def deal_new_fault3(driver):
    try:
        # 获取所有的一级节点
        first = len(driver.find_elements_by_class_name("jstree-anchor"))

        # 点击随机的一个一级节点
        fault_1 = random.randint(1,first-1)
        # fault_1 = 13

        text = driver.find_elements_by_class_name("jstree-anchor")[fault_1].text.lstrip()
        time.sleep(1)
        driver.find_element_by_xpath("//a[text()=\'{}\']/..".format(text)).click()
        time.sleep(2)
        Method(driver).click('name', 'btSelectAll')
        time.sleep(1)
        Method(driver).click('xpath', '//*[@id="right-move"]')
        try:
            driver.find_element_by_xpath('//*[@class="pull-right pagination"]/ul/li[4]/a').click()
            time.sleep(2)
            Method(driver).click('name', 'btSelectAll')
            time.sleep(1)
            Method(driver).click('xpath', '//*[@id="right-move"]')
        except:
            pass
        return True

    except:
        logger.error('xpath' + '不存在!')
        return False

# 多个一个部件下多个子集部件
def deal_new_fault4(driver):
    try:
        L = []
        first = len(driver.find_elements_by_class_name("jstree-anchor"))
        # while len(L) < random.randint(2,len(driver.find_elements_by_class_name("jstree-anchor"))-1):
        while len(L) < 5:
            fault_1 = random.randint(1, first - 1)

            if fault_1 not in L:
                L.append(fault_1)
                # 点击随机的一个一级节点
                time.sleep(1)
                fault_1 = random.randint(1, first - 1)
                # fault_1 = 13
                fault_next_1 = driver.find_elements_by_class_name("jstree-anchor")[fault_1].get_attribute('id')

                text = driver.find_elements_by_class_name("jstree-anchor")[fault_1].text.lstrip()
                time.sleep(1)

                # 判断是否有下级节点
                if 'jstree-leaf' not in driver.find_element_by_xpath("//a[text()=\'{}\']/..".format(text)).get_attribute(
                        'class'):
                    Method(driver).click('xpath', '//*[@id= \'{}\']/i'.format(fault_next_1[:-7]))
                    time.sleep(1)
                    # 随机1级节点下的二级节点
                    second = len(driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_1[:-7])))
                    if second == 1:
                        driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_1[:-7]))[0].click()
                        time.sleep(2)
                        Method(driver).click('name', 'btSelectAll')
                        Method(driver).click('xpath', '//*[@id="right-move"]')
                        Method(driver).click('xpath', '//*[@id= \'{}\']/i'.format(fault_next_1[:-7]))
                    b = random.randint(1, second - 1)
                    for i in range(0, b):
                        if 'jstree-leaf' not in driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_1[:-7]))[i].get_attribute('class'):
                            driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_1[:-7]))[i].click()
                            time.sleep(2)
                            Method(driver).click('name', 'btSelectAll')
                            time.sleep(1)
                            Method(driver).click('xpath', '//*[@id="right-move"]')
                        else:
                            text1 = driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_1[:-7]))[
                                i].text.lstrip()
                            Method(driver).click('xpath', '//*[@id= \'{}\']/i'.format(fault_next_1[:-7]))
                            time.sleep(2)
                            Method(driver).click('xpath', '//*[@id= \'{}\']'.format(fault_next_1[:-7]))
                            time.sleep(2)
                            try:
                                driver.find_element_by_xpath("//td[text()=\'{}\']/../td[1]/input".format(text1)).click()
                                Method(driver).click('id', "right-move")
                            except:
                                driver.find_element_by_xpath('//*[@class="pull-right pagination"]/ul/li[4]/a').click()
                                time.sleep(1)
                                driver.find_element_by_xpath("//td[text()=\'{}\']/../td[1]/input".format(text1)).click()
                                time.sleep(1)
                                Method(driver).click('id', "right-move")
                                time.sleep(1)
                                driver.find_element_by_xpath('//*[@class="pull-right pagination"]/ul/li[3]/a').click()

                            time.sleep(2)
                            Method(driver).click('xpath', '//*[@id= \'{}\']/i'.format(fault_next_1[:-7]))

                    Method(driver).click('xpath', '//*[@id= \'{}\']/i'.format(fault_next_1[:-7]))

                else:
                    driver.find_elements_by_class_name("jstree-anchor")[fault_1].click()
                    time.sleep(2)
                    driver.find_element_by_xpath('//*[@id="middleTable"]/tbody/tr[1]/td[1]/input').click()
                    Method(driver).click('id', "right-move")
        return True
    except Exception as e:
        logger.error(e)
        return False

# 全量部件
def deal_new_fault5(driver):
    try:
        driver.find_elements_by_class_name("jstree-anchor")[0].click()
        time.sleep(5)
        Method(driver).click('name', 'btSelectAll')
        Method(driver).click('id', "right-move")
        time.sleep(2)
        driver.find_element_by_xpath('//*[@class="pull-right pagination"]/ul/li[4]/a').click()
        time.sleep(2)
        Method(driver).click('name', 'btSelectAll')
        Method(driver).click('id', "right-move")
        return True
    except:
        logger.error('xpath' + '不存在!')
        return False