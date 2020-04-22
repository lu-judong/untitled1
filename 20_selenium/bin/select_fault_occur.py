import time
from bin.main import Method
from selenium.common.exceptions import NoSuchElementException
from config.log_config import logger

def deal_fault(driver,fault):
    try:
        for key in fault:
            if type(fault[key]).__name__ == 'dict':
                fault_next_1 = Method(driver).contains_xpath('get', key)
                Method(driver).click('xpath', '//*[@id= \'{}\']/i'.format(fault_next_1[:-7]))

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
                                    if fault[key][i][m][j] == 'all':
                                        Method(driver).click('xpath', '//*[text()=\'{}\']'.format(j))
                                        Method(driver).click('name', 'btSelectAll')
                                        time.sleep(1)
                                        Method(driver).click('xpath', '//*[@id="right-move"]')
                                    else:
                                        fault_next_4 = Method(driver).contains_xpath('get', j)
                                        Method(driver).click('xpath',
                                                             '//*[@id= \'{}\']/i'.format(fault_next_4[:-7]))
                                        time.sleep(2)
                                        for p in fault[key][i][m][j]:
                                            driver.find_element_by_xpath(
                                                "//td[contains(text(),\'{}\')]/../td[1]/input".format(p)).click()
                                            Method(driver).click('xpath', '//*[@id="right-move"]')

                            else:
                                Method(driver).click('xpath', '//*[text()=\'{}\']'.format(m))
                                time.sleep(2)
                                if fault[key][i][m] == 'all':
                                    Method(driver).click('name', 'btSelectAll')
                                    time.sleep(1)
                                    Method(driver).click('xpath', '//*[@id="right-move"]')
                                else:
                                    for k in fault[key][i][m]:
                                        driver.find_element_by_xpath(
                                            "//td[contains(text(),\'{}\')]/../td[1]/input".format(k)).click()
                                    Method(driver).click('xpath', '//*[@id="right-move"]')
                    else:
                        Method(driver).click('xpath', '//*[text()=\'{}\']'.format(i))
                        time.sleep(2)
                        if fault[key][i] == 'all':
                            Method(driver).click('name', 'btSelectAll')
                            time.sleep(1)
                            Method(driver).click('xpath', '//*[@id="right-move"]')
                        else:
                            for n in fault[key][i]:
                                driver.find_element_by_xpath(
                                    "//td[contains(text(),\'{}\')]/../td[1]/input".format(n)).click()
                                time.sleep(2)
                            Method(driver).click('xpath', '//*[@id="right-move"]')

            else:
                Method(driver).click('xpath', '//*[text()=\'{}\']'.format(key))
                time.sleep(2)
                if fault[key] == 'all':
                    Method(driver).click('name', 'btSelectAll')
                    time.sleep(1)
                    Method(driver).click('xpath', '//*[@id="right-move"]')
                else:
                    for i in fault[key]:
                        # WebDriverWait(driver, 10).until(EC.element_to_be_clickable(By.XPATH, "//td[contains(text(),\'{}\')]/../td[1]/input".format(i))).click()
                        driver.find_element_by_xpath(
                            "//td[contains(text(),\'{}\')]/../td[1]/input".format(i)).click()
                    Method(driver).click('xpath', '//*[@id="right-move"]')
        return True
    except NoSuchElementException as e:
        logger.error('xpath' + '不存在!')
        return False