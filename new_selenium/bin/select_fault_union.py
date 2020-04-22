import time
from bin.main import Method
from selenium.common.exceptions import NoSuchElementException
from config.log_config import logger

def deal_fault_union(driver,fault):
    try:
        for key in fault:
            driver.find_element_by_xpath("//a[contains(text(),\'{}\')]/../i".format(key)).click()
            time.sleep(2)
            # if type(fault[key]).__name__ == 'dict':
            #     fault_next_1 = Method(driver).contains_xpath('get', key)
            #     Method(driver).click('xpath', '//*[@id= \'{}\']/i'.format(fault_next_1[:-7]))
            # 取出第二个子节点中的值
            for i in fault[key]:
                if type(fault[key][i]).__name__ == 'dict':
                    fault_next_2 = Method(driver).contains_xpath('get', i)
                    Method(driver).click('xpath', '//*[@id= \'{}\']/i'.format(fault_next_2[:-7]))

                    # 取出第三个子节点的值
                    for m in fault[key][i]:
                        if type(fault[key][i][m]).__name__ == 'dict':
                            fault_next_3 = Method(driver).contains_xpath('get', m)
                            Method(driver).click('xpath', '//*[@id= \'{}\']/i'.format(fault_next_3[:-7]))
                            # 取出第四个子节点的值
                            for j in fault[key][i][m]:
                                if type(fault[key][i][m][j]) == 'dict':
                                    fault_next_4 = Method(driver).contains_xpath('get', j)
                                    Method(driver).click('xpath', '//*[@id= \'{}\']/i'.format(fault_next_4[:-7]))
                                    # 取出第五个子节点的值
                                    for k in fault[key][i][m][j]:
                                        driver.find_element_by_xpath(
                                            "//a[text()=\'{}\']/i[1]".format(k)).click()
                                        Method(driver).click('id', 'right-move2')
                                else:
                                    driver.find_element_by_xpath(
                                        "//a[text()=\'{}\']/i[1]".format(j)).click()
                                    Method(driver).click('id', 'right-move2')
                                    time.sleep(2)
                        else:
                            driver.find_element_by_xpath("//a[text()=\'{}\']/i[1]".format(m)).click()
                            Method(driver).click('id', 'right-move2')
                            time.sleep(2)
                else:
                    driver.find_element_by_xpath(
                        "//a[text()=\'{}\']/i[1]".format(i)).click()
                    Method(driver).click('id', 'right-move2')
                    time.sleep(2)

            # else:
            #     Method(driver).click('xpath', '//*[text()=\'{}\']'.format(key))
            #     time.sleep(time_sleep)
            #     if fault[key] == 'all':
            #         Method(driver).click('name', 'btSelectAll')
            #         Method(driver).click('xpath', '//*[@id="right-move"]')
            #     else:
            #         for i in fault[key]:
            #             # WebDriverWait(driver, 10).until(EC.element_to_be_clickable(By.XPATH, "//td[contains(text(),\'{}\')]/../td[1]/input".format(i))).click()
            #             driver.find_element_by_xpath(
            #                 "//td[contains(text(),\'{}\')]/../td[1]/input".format(i)).click()
            #         Method(driver).click('xpath', '//*[@id="right-move"]')
        return True
    except NoSuchElementException as e:
        logger.error('xpath' + '不存在!')
        return False