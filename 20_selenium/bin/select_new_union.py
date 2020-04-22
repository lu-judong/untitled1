import sys
from config.log_config import logger
import random

from bin.t import *


def deal_new_union(driver):
    L = []
    try:
        # 获取所有的一级节点
        first = len(driver.find_elements_by_class_name("jstree-anchor"))


        # 点击随机的一个一级节点
        for fault_1 in  range(1,first):
            text = ''
            text2 = ''
            text3 = ''
            text4 = ''
            text5 = ''

            fault_next_1 = ''
            fault_next_2 = ''
            fault_next_3 = ''
            fault_next_4 = ''

            fault_next_1 = driver.find_elements_by_class_name("jstree-anchor")[fault_1].get_attribute('id')

            text = driver.find_elements_by_class_name("jstree-anchor")[fault_1].text.lstrip()
            time.sleep(2)

            if 'jstree-leaf' not in driver.find_element_by_xpath("//a[text()=\'{}\']/..".format(text)).get_attribute('class'):
                # Method(driver).click('xpath', '//*[@id= \'{}\']/i'.format(fault_next_1[:-7]))

                # '$("#faultObjectTree").jstree().open_node("{}")'.format(fault_next_1)
                driver.execute_script('$("#faultObjectTree").jstree().open_node("{}")'.format(fault_next_1[:-7]))

                time.sleep(2)
                # 随机1级节点下的二级节点
                second = wait_time(driver,fault_next_1)
                try:
                    fault_second = random.randint(0, second - 1)
                except:
                    fault_second = 0
                try:
                    text2 = driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_1[:-7]))[fault_second].text.lstrip()
                except:
                    text2 = driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_1[:-7]))[0].text.lstrip()
                fault_next_2 = Method(driver).contains_xpath('get', text2)
                time.sleep(2)

                # 判断二级节点是否有下级节点
                if 'jstree-leaf' not in driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_1[:-7]))[fault_second].get_attribute('class'):
                    # 随机是否要去点击下一级节点
                    # Method(driver).click('xpath', '//*[@id= \'{}\']/i'.format(fault_next_2[:-7]))
                    driver.execute_script('$("#faultObjectTree").jstree().open_node("{}")'.format(fault_next_2[:-7]))
                    # fault_next_2 = wait_time1(driver, text2)

                    third1 = wait_time(driver, fault_next_2)

                    # driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li/i'.format(fault_next_1[:-7]))[
                    #     fault_second].click()
                    time.sleep(2)
                    try:
                        third = random.randint(0, third1 - 1)
                    except:
                        third = 0

                    try:
                        text3 = driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_2[:-7]))[
                            third].text.lstrip()
                    except:
                        text3 = driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_2[:-7]))[
                            0].text.lstrip()
                    fault_next_3 = Method(driver).contains_xpath('get', text3)
                    time.sleep(2)
                    # third = 13
                    # 判断三级节点是否有下一级子节点
                    if 'jstree-leaf' not in driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_2[:-7]))[third].get_attribute('class'):

                        # Method(driver).click('xpath', '//*[@id= \'{}\']/i'.format(fault_next_3[:-7]))
                        driver.execute_script('$("#faultObjectTree").jstree().open_node("{}")'.format(fault_next_3[:-7]))
                        # fault_next_3 = wait_time1(driver, text3)
                        # driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li/ul/li/i'.format(fault_next_1[:-7]))[
                        #     third].click()
                        fourth1 = wait_time(driver, fault_next_3)
                        try:
                            fourth = random.randint(0, fourth1 - 1)
                        except:
                            fourth = 1

                        time.sleep(2)
                        try:
                            text4 = driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_3[:-7]))[fourth].text.lstrip()
                        except:
                            text4 = driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_3[:-7]))[0].text.lstrip()
                        fault_next_4 = Method(driver).contains_xpath('get', text4)
                        time.sleep(2)

                        if 'jstree-leaf' not in driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_3[:-7]))[fourth].get_attribute('class'):

                            # Method(driver).click('xpath', '//*[@id= \'{}\']/i'.format(fault_next_4[:-7]))
                            driver.execute_script('$("#faultObjectTree").jstree().open_node("{}")'.format(fault_next_4[:-7]))
                            # fault_next_4 = wait_time1(driver, text4)

                            fifth1 = wait_time(driver, fault_next_4)
                            try:
                                fifth = random.randint(0, fifth1 - 1)
                            except:
                                fifth = 0
                            time.sleep(2)
                            try:
                                text5 = driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_4[:-7]))[fifth].text.lstrip()
                            except:
                                text5 = driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_4[:-7]))[0].text.lstrip()
                            time.sleep(1)
                            fault_next_5 = Method(driver).contains_xpath('get', text5)
                            driver.execute_script('$("#faultObjectTree").jstree().select_node("{}")'.format(fault_next_5[:-7]))
                            # driver.find_element_by_xpath("//a[text()=\'{}\']/i[1]".format(text5)).click()
                            time.sleep(2)
                            Method(driver).click('id', "right-move2")
                        else:
                            time.sleep(1)
                            driver.execute_script('$("#faultObjectTree").jstree().select_node("{}")'.format(fault_next_4[:-7]))
                            time.sleep(2)
                            Method(driver).click('id', "right-move2")
                    else:
                        time.sleep(1)
                        driver.execute_script('$("#faultObjectTree").jstree().select_node("{}")'.format(fault_next_3[:-7]))
                        time.sleep(2)

                        Method(driver).click('id', "right-move2")

                else:
                    # 没有就获取三级子节点的值 在二级子节点中点击它
                    driver.execute_script('$("#faultObjectTree").jstree().select_node("{}")'.format(fault_next_2[:-7]))
                    time.sleep(2)
                    Method(driver).click('id', "right-move2")
            else:
                pass
            L.append((text,text2,text3,text4,text5))
            driver.execute_script('$("#faultObjectTree").jstree().close_node("{}")'.format(fault_next_1[:-7]))

            time.sleep(2)
        return True,L
    except Exception as e:
        logger.error(e)
        return False,L

# 并集部件多个一级子集部件下一个部件
def deal_new_union1(driver):
    fault = []
    try:
        # 获取所有的一级节点
        first = len(driver.find_elements_by_class_name("jstree-anchor"))


        for fault_1 in range(1,first):
        # 点击随机的一个一级节点
            text = ''
            text2 = ''
            text3 = ''
            text4 = ''
            text5 = ''

            fault_next_1 = ''
            fault_next_2 = ''
            fault_next_3 = ''
            fault_next_4 = ''

            L = []
            fault_next_1 = driver.find_elements_by_class_name("jstree-anchor")[fault_1].get_attribute('id')

            text = driver.find_elements_by_class_name("jstree-anchor")[fault_1].text.lstrip()
            time.sleep(2)
            if 'jstree-leaf' not in driver.find_element_by_xpath("//a[text()=\'{}\']/..".format(text)).get_attribute(
                'class'):
                driver.execute_script('$("#faultObjectTree").jstree().open_node("{}")'.format(fault_next_1[:-7]))

                second = wait_time(driver,fault_next_1)

                num =2

                # second = len(driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_1[:-7])))

                while len(L) < num:
                    # 随机1级节点下的二级节点
                    fault_second = random.randint(0, second - 1)
                    # fault_second = 1
                    if fault_second not in L:
                        L.append(fault_second)
                        text2 = driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_1[:-7]))[
                            fault_second].text.lstrip()
                        time.sleep(1)
                        fault_next_2 = Method(driver).contains_new(text2)
                        time.sleep(1)
                        # 判断二级节点是否有下级节点
                        if 'jstree-leaf' not in driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_1[:-7]))[fault_second].get_attribute('class'):
                            # 随机是否要去点击下一级节点

                            driver.execute_script('$("#faultObjectTree").jstree().open_node("{}")'.format(fault_next_2[:-7]))

                            # fault_next_2 = wait_time1(driver,text2)

                            third1 = wait_time(driver, fault_next_2)
                            # time.sleep(2)
                            # driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li/i'.format(fault_next_1[:-7]))[
                            #     fault_second].click()

                            third = random.randint(0, third1 - 1)
                            # third = 0
                            # third = 13
                            text3 = driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_2[:-7]))[third].text.lstrip()
                            fault_next_3 = Method(driver).contains_new(text3)
                            time.sleep(1)

                            # 判断三级节点是否有下一级子节点
                            if 'jstree-leaf' not in driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_2[:-7]))[third].get_attribute('class'):
                                driver.execute_script('$("#faultObjectTree").jstree().open_node("{}")'.format(fault_next_3[:-7]))
                                # Method(driver).click('xpath', '//*[@id= \'{}\']/i'.format(fault_next_3[:-7]))
                                # fault_next_3 = wait_time1(driver,text3)

                                fourth1 = wait_time(driver, fault_next_3)
                                fourth = random.randint(0, fourth1 - 1)
                                # fourth = 4
                                time.sleep(1)
                                text4 = driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_3[:-7]))[fourth].text.lstrip()
                                time.sleep(1)
                                fault_next_4 = Method(driver).contains_new(text4)
                                time.sleep(1)
                                if 'jstree-leaf' not in  driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_3[:-7]))[fourth].get_attribute('class'):
                                    driver.execute_script('$("#faultObjectTree").jstree().open_node("{}")'.format(fault_next_4[:-7]))
                                    # Method(driver).click('xpath', '//*[@id= \'{}\']/i'.format(fault_next_4[:-7]))
                                    # fault_next_4 = wait_time1(driver,text4)

                                    fifth1 = wait_time(driver, fault_next_4)
                                    try:
                                        fifth = random.randint(0, fifth1 - 1)
                                    except:
                                        fifth = 0
                                    # fifth = 1
                                    time.sleep(1)
                                    try:
                                        text5 = driver.find_elements_by_xpath(
                                            '//*[@id= \'{}\']/ul/li'.format(fault_next_4[:-7]))[fifth].text.lstrip()
                                    except:
                                        text5 = driver.find_elements_by_xpath(
                                            '//*[@id= \'{}\']/ul/li'.format(fault_next_4[:-7]))[0].text.lstrip()
                                    fault_next_5 = Method(driver).contains_xpath('get', text5)
                                    driver.execute_script(
                                        '$("#faultObjectTree").jstree().select_node("{}")'.format(fault_next_5[:-7]))
                                    time.sleep(1)
                                    Method(driver).click('id', "right-move2")
                                else:
                                    time.sleep(1)
                                    driver.execute_script(
                                        '$("#faultObjectTree").jstree().select_node("{}")'.format(fault_next_4[:-7]))
                                    time.sleep(1)
                                    Method(driver).click('id', "right-move2")
                            else:
                                # WebDriverWait(driver, 10).until(EC.invisibility_of_element_located(
                                #     (By.XPATH, '//body[contains(@class, "bg-white")]')))
                                driver.execute_script(
                                    '$("#faultObjectTree").jstree().select_node("{}")'.format(fault_next_3[:-7]))
                                time.sleep(1)

                                Method(driver).click('id', "right-move2")
                        else:
                            # 没有就获取三级子节点的值 在二级子节点中点击它
                            driver.execute_script('$("#faultObjectTree").jstree().select_node("{}")'.format(fault_next_2[:-7]))
                            time.sleep(2)

                            Method(driver).click('id', "right-move2")
                        time.sleep(2)
                        driver.execute_script(
                            '$("#faultObjectTree").jstree().close_node("{}")'.format(fault_next_2[:-7]))
                        fault.append((text, text2, text3, text4, text5))
                        time.sleep(2)
                    else:
                        pass

                    time.sleep(1)

                driver.execute_script('$("#faultObjectTree").jstree().close_node("{}")'.format(fault_next_1[:-7]))
                time.sleep(1)
            else:
                pass
            time.sleep(1)
        return True,fault
    except Exception as e:
        logger.error(e)
        print(text,text2,text3,text4,text5)
        print(fault_next_1,fault_next_2,fault_next_3,fault_next_4)
        # f = sys.exc_info()[2].tb_frame.f_back
        # print(f.f_code.co_filename,f.f_code.co_name, str(f.f_lineno))
        # traceback.extract_stack()
        print('<<<<<-----'.join(err_catch().catch(sys.exc_info())))

        return False,fault

# 并集部件一个一级子集部件下多个子集部件
def deal_new_union2(driver):
    fault = []

    try:
        text = ''
        text2 = ''
        text3 = ''

        first = len(driver.find_elements_by_class_name("jstree-anchor"))

        for fault_1 in range(1, first):
            fault_next_1 = driver.find_elements_by_class_name("jstree-anchor")[fault_1].get_attribute('id')

            text = driver.find_elements_by_class_name("jstree-anchor")[fault_1].text.lstrip()

            if 'jstree-leaf' not in driver.find_element_by_xpath("//a[text()=\'{}\']/..".format(text)).get_attribute(
                'class'):
                driver.execute_script('$("#faultObjectTree").jstree().open_node("{}")'.format(fault_next_1[:-7]))

                time.sleep(2)

                second = len(driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_1[:-7])))

                fault_second = random.randint(0, second - 1)
                # fault_second = 3
                text2 = driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_1[:-7]))[
                    fault_second].text.lstrip()

                fault_next_2 = Method(driver).contains_new(text2)
                time.sleep(1)
                # 判断二级节点是否有下级节点
                if 'jstree-leaf' not in driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_1[:-7]))[fault_second].get_attribute('class'):
                    # 随机是否要去点击下一级节点
                    # select = random.randint(0,1)
                    time.sleep(2)

                    # driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li/i'.format(fault_next_1[:-7]))[
                    #     fault_second].click()
                    driver.execute_script('$("#faultObjectTree").jstree().open_node("{}")'.format(fault_next_2[:-7]))

                    third = random.randint(0, len(driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li/ul/li'.format(fault_next_1[:-7])))-1)
                    text3 = driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li/ul/li'.format(fault_next_1[:-7]))[third].text.lstrip()


                    fault_next_3 = Method(driver).contains_new(text3)
                    time.sleep(1)

                    # driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li/ul/li/a/i[1]'.format(fault_next_1[:-7]))[third].click()
                    driver.execute_script('$("#faultObjectTree").jstree().select_node("{}")'.format(fault_next_3[:-7]))
                    time.sleep(2)

                    Method(driver).click('id', "right-move2")

                else:
                    driver.execute_script('$("#faultObjectTree").jstree().select_node("{}")'.format(fault_next_2[:-7]))
                    time.sleep(2)

                    Method(driver).click('id', "right-move2")

                time.sleep(2)
                # driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li/i'.format(fault_next_1[:-7]))[fault_second].click()
                fault.append((text,text2,text3))
                driver.execute_script('$("#faultObjectTree").jstree().close_node("{}")'.format(fault_next_1[:-7]))
            else:
                pass
        return True,fault
    except Exception as e:
        logger.error(e)
        return False,fault

# 并集部件一个一级子集部件下全量子集部件
def deal_new_union3(driver):
    fault = []

    try:
        first = len(driver.find_elements_by_class_name("jstree-anchor"))

        for fault_1 in range(1, first):
            fault_next_1 = driver.find_elements_by_class_name("jstree-anchor")[fault_1].get_attribute('id')
            text = driver.find_elements_by_class_name("jstree-anchor")[fault_1].text.lstrip()
            if 'jstree-leaf' not in driver.find_element_by_xpath("//a[text()=\'{}\']/..".format(text)).get_attribute(
                    'class'):

                driver.execute_script('$("#faultObjectTree").jstree().open_node("{}")'.format(fault_next_1[:-7]))

                time.sleep(2)

                second = len(driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_1[:-7])))

                fault_second = random.randint(0, second - 1)

                time.sleep(2)
                text2 = driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_1[:-7]))[
                    fault_second].text.lstrip()

                fault_next_2 = Method(driver).contains_new(text2)
                time.sleep(1)

                # 没有就获取三级子节点的值 在二级子节点中点击它
                # driver.find_element_by_xpath("//a[text()=\'{}\']/i[1]".format(text2)).click()
                driver.execute_script('$("#faultObjectTree").jstree().select_node("{}")'.format(fault_next_2[:-7]))
                time.sleep(2)

                Method(driver).click('id', "right-move2")
                time.sleep(2)
                fault.append((text,text2))
                driver.execute_script('$("#faultObjectTree").jstree().close_node("{}")'.format(fault_next_1[:-7]))
                time.sleep(2)
            else:
                pass
        return True,fault
    except Exception as e:
        logger.error(e)
        return False,fault

# 并集部件多个一级子集部件下多个子集部件
def deal_new_union4(driver):
    fault = []
    try:
        text = ''
        text2 = ''
        text3 = ''

        first = len(driver.find_elements_by_class_name("jstree-anchor"))

        for fault_1 in range(1, first):
            L = []
            fault_next_1 = driver.find_elements_by_class_name("jstree-anchor")[fault_1].get_attribute('id')

            text = driver.find_elements_by_class_name("jstree-anchor")[fault_1].text.lstrip()

            if 'jstree-leaf' not in driver.find_element_by_xpath("//a[text()=\'{}\']/..".format(text)).get_attribute(
                'class'):
                driver.execute_script('$("#faultObjectTree").jstree().open_node("{}")'.format(fault_next_1[:-7]))

                time.sleep(2)

                num = 2
                second = len(driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_1[:-7])))

                while len(L) < num:
                    fault_second = random.randint(0, second - 1)
                    if fault_second not in L:
                        L.append(fault_second)

                        text2 = driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_1[:-7]))[
                            fault_second].text.lstrip()
                        time.sleep(1)
                        fault_next_2 = Method(driver).contains_new(text2)
                        time.sleep(1)

                        # 判断二级节点是否有下级节点
                        if 'jstree-leaf' not in driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_1[:-7]))[fault_second].get_attribute('class'):
                            # 随机是否要去点击下一级节点
                            # select = random.randint(0,1)
                            time.sleep(2)
                            # driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li/i'.format(fault_next_1[:-7]))[
                            #     fault_second].click()
                            driver.execute_script('$("#faultObjectTree").jstree().open_node("{}")'.format(fault_next_2[:-7]))

                            third = random.randint(0, len(driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_2[:-7])))-1)
                            text3 = driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_2[:-7]))[third].text.lstrip()
                            time.sleep(1)
                            # driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li/ul/li/a/i[1]'.format(fault_next_1[:-7]))[third].click()
                            fault_next_3 = Method(driver).contains_new(text3)
                            driver.execute_script('$("#faultObjectTree").jstree().select_node("{}")'.format(fault_next_3[:-7]))
                            time.sleep(1)

                            Method(driver).click('id', "right-move2")

                        else:
                            driver.execute_script(
                                '$("#faultObjectTree").jstree().select_node("{}")'.format(fault_next_2[:-7]))
                            time.sleep(2)

                            Method(driver).click('id', "right-move2")

                        time.sleep(2)
                        fault.append((text,text2,text3))
                        driver.execute_script('$("#faultObjectTree").jstree().close_node("{}")'.format(fault_next_2[:-7]))
                time.sleep(2)
                driver.execute_script(
                    '$("#faultObjectTree").jstree().close_node("{}")'.format(fault_next_1[:-7]))
                time.sleep(2)
            else:
                pass

        return True,fault
    except Exception as e:
        logger.error(e)
        return False,fault

# 全量部件
def deal_new_union5(driver):
    fault = []
    try:
        first = len(driver.find_elements_by_class_name("jstree-anchor"))

        for fault_1 in range(1, first):
            fault_next_1 = driver.find_elements_by_class_name("jstree-anchor")[fault_1].get_attribute('id')

            text = driver.find_elements_by_class_name("jstree-anchor")[fault_1].text.lstrip()
            time.sleep(2)

            if 'jstree-leaf' not in driver.find_element_by_xpath("//a[text()=\'{}\']/..".format(text)).get_attribute(
                    'class'):
                driver.execute_script('$("#faultObjectTree").jstree().select_node("{}")'.format(fault_next_1[:-7]))
                fault.append(text)
                time.sleep(2)
                Method(driver).click('id', "right-move2")
                time.sleep(2)
            else:
                pass
        return True,fault
    except Exception as e:
        logger.error(e)
        return False,fault

# femca 选择
def deal_new_union6(driver):
    fault = []
    try:
        # 获取所有的一级节点
        first = len(driver.find_elements_by_class_name("jstree-anchor"))


        for fault_1 in range(1,first):
        # 点击随机的一个一级节点
            text = ''
            text2 = ''
            text3 = ''
            text4 = ''
            text5 = ''

            fault_next_1 = ''
            fault_next_2 = ''
            fault_next_3 = ''
            fault_next_4 = ''

            L = []
            fault_next_1 = driver.find_elements_by_class_name("jstree-anchor")[fault_1].get_attribute('id')

            text = driver.find_elements_by_class_name("jstree-anchor")[fault_1].text.lstrip()
            time.sleep(2)
            if 'jstree-leaf' not in driver.find_element_by_xpath("//a[text()=\'{}\']/..".format(text)).get_attribute(
                'class'):
                driver.execute_script('$("#faultObjectTree").jstree().open_node("{}")'.format(fault_next_1[:-7]))

                second = wait_time(driver,fault_next_1)

                # second = len(driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_1[:-7])))
                # 随机1级节点下的二级节点
                fault_second = random.randint(0, second - 1)
                # fault_second = 1
                if fault_second not in L:
                    L.append(fault_second)
                    text2 = driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_1[:-7]))[
                        fault_second].text.lstrip()
                    time.sleep(1)
                    fault_next_2 = Method(driver).contains_new(text2)
                    time.sleep(1)
                    # 判断二级节点是否有下级节点
                    while True:
                        if 'jstree-leaf' not in driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_1[:-7]))[fault_second].get_attribute('class'):
                            # 随机是否要去点击下一级节点

                            driver.execute_script('$("#faultObjectTree").jstree().open_node("{}")'.format(fault_next_2[:-7]))

                            # fault_next_2 = wait_time1(driver,text2)

                            third1 = wait_time(driver, fault_next_2)
                            # time.sleep(2)
                            # driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li/i'.format(fault_next_1[:-7]))[
                            #     fault_second].click()

                            third = random.randint(0, third1 - 1)
                            # third = 0
                            # third = 13
                            text3 = driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_2[:-7]))[third].text.lstrip()
                            fault_next_3 = Method(driver).contains_new(text3)
                            time.sleep(1)

                            # 判断三级节点是否有下一级子节点
                            if 'jstree-leaf' not in driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_2[:-7]))[third].get_attribute('class'):
                                driver.execute_script('$("#faultObjectTree").jstree().open_node("{}")'.format(fault_next_3[:-7]))
                                # Method(driver).click('xpath', '//*[@id= \'{}\']/i'.format(fault_next_3[:-7]))
                                # fault_next_3 = wait_time1(driver,text3)

                                fourth1 = wait_time(driver, fault_next_3)
                                fourth = random.randint(0, fourth1 - 1)
                                # fourth = 4
                                time.sleep(1)
                                text4 = driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_3[:-7]))[fourth].text.lstrip()
                                time.sleep(1)
                                fault_next_4 = Method(driver).contains_new(text4)
                                time.sleep(1)
                                if 'jstree-leaf' not in  driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(fault_next_3[:-7]))[fourth].get_attribute('class'):
                                    driver.execute_script('$("#faultObjectTree").jstree().open_node("{}")'.format(fault_next_4[:-7]))
                                    # Method(driver).click('xpath', '//*[@id= \'{}\']/i'.format(fault_next_4[:-7]))
                                    # fault_next_4 = wait_time1(driver,text4)

                                    fifth1 = wait_time(driver, fault_next_4)
                                    try:
                                        fifth = random.randint(0, fifth1 - 1)
                                    except:
                                        fifth = 0
                                    # fifth = 1
                                    time.sleep(1)
                                    try:
                                        text5 = driver.find_elements_by_xpath(
                                            '//*[@id= \'{}\']/ul/li'.format(fault_next_4[:-7]))[fifth].text.lstrip()
                                    except:
                                        text5 = driver.find_elements_by_xpath(
                                            '//*[@id= \'{}\']/ul/li'.format(fault_next_4[:-7]))[0].text.lstrip()
                                    fault_next_5 = Method(driver).contains_xpath('get', text5)
                                    driver.execute_script(
                                        '$("#faultObjectTree").jstree().select_node("{}")'.format(fault_next_5[:-7]))
                                    time.sleep(1)
                                    Method(driver).click('id', "right-move2")
                                    break
                                else:
                                    time.sleep(1)
                                    driver.execute_script(
                                        '$("#faultObjectTree").jstree().select_node("{}")'.format(fault_next_4[:-7]))
                                    time.sleep(1)
                                    Method(driver).click('id', "right-move2")
                                    break
                            else:
                                # WebDriverWait(driver, 10).until(EC.invisibility_of_element_located(
                                #     (By.XPATH, '//body[contains(@class, "bg-white")]')))
                               pass
                        else:
                            # 没有就获取三级子节点的值 在二级子节点中点击它
                            pass
                else:
                    pass

                time.sleep(1)

                driver.execute_script('$("#faultObjectTree").jstree().close_node("{}")'.format(fault_next_1[:-7]))
                time.sleep(1)
            else:
                pass
            time.sleep(1)
        return True,fault
    except Exception as e:
        logger.error(e)
        print(text,text2,text3,text4,text5)
        print(fault_next_1,fault_next_2,fault_next_3,fault_next_4)
        # f = sys.exc_info()[2].tb_frame.f_back
        # print(f.f_code.co_filename,f.f_code.co_name, str(f.f_lineno))
        # traceback.extract_stack()
        print('<<<<<-----'.join(err_catch().catch(sys.exc_info())))
        return False,fault
