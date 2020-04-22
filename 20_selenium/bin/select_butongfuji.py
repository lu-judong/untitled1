import time
from bin.main import Method
from selenium.common.exceptions import NoSuchElementException
from config.log_config import logger

def deal_different(driver,fault):
    try:
        for key in fault:
            if type(fault[key]).__name__ == 'dict':
                driver.find_element_by_xpath("//a[contains(text(),\'{}\')]/../i".format(key)).click()

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
                                    driver.find_element_by_xpath(
                                        "//a[contains(text(),\'{}\')]/i[1]".format(j)).click()
                                    Method(driver).click('id', 'faultTree-right-move')
                                    time.sleep(10)
                                    if fault[key][i][m][j] == 'all':
                                        Method(driver).click('name', 'btSelectAll')
                                        Method(driver).click('xpath', '//*[@id="right-move"]')
                                    else:
                                        for p in fault[key][i][m][j]:
                                            driver.find_element_by_xpath(
                                                "//td[contains(text(),\'{}\')]/../td[1]/input".format(p)).click()
                                        Method(driver).click('xpath', '//*[@id="right-move"]')

                            else:
                                driver.find_element_by_xpath("//a[contains(text(),\'{}\')]/i[1]".format(m)).click()
                                Method(driver).click('id', 'faultTree-right-move')
                                time.sleep(10)
                                if fault[key][i][m] == 'all':
                                    Method(driver).click('name', 'btSelectAll')
                                    Method(driver).click('xpath', '//*[@id="right-move"]')
                                else:
                                    for k in fault[key][i][m]:
                                        driver.find_element_by_xpath(
                                            "//td[contains(text(),\'{}\')]/../td[1]/input".format(k)).click()
                                    Method(driver).click('xpath', '//*[@id="right-move"]')
                    else:
                        driver.find_element_by_xpath("//a[contains(text(),\'{}\')]/i[1]".format(i)).click()
                        Method(driver).click('id', 'faultTree-right-move')
                        time.sleep(10)
                        if fault[key][i] == 'all':
                            Method(driver).click('name', 'btSelectAll')
                            Method(driver).click('xpath', '//*[@id="right-move"]')
                        else:
                            for n in fault[key][i]:
                                driver.find_element_by_xpath(
                                    "//td[contains(text(),\'{}\')]/../td[1]/input".format(n)).click()
                                time.sleep(2)
                            Method(driver).click('xpath', '//*[@id="right-move"]')

            else:
                driver.find_element_by_xpath("//a[contains(text(),\'{}\')]/i[1]".format(key)).click()
                Method(driver).click('id', 'faultTree-right-move')
                time.sleep(10)
                if fault[key] == 'all':
                    Method(driver).click('name', 'btSelectAll')
                    Method(driver).click('xpath', '//*[@id="right-move"]')
                else:
                    for i in fault[key]:
                        # WebDriverWait(driver, 10).until(EC.element_to_be_clickable(By.XPATH, "//td[contains(text(),\'{}\')]/../td[1]/input".format(i))).click()
                        driver.find_element_by_xpath("//td[contains(text(),\'{}\')]/../td[1]/input".format(i)).click()
                    Method(driver).click('xpath', '//*[@id="right-move"]')
        return True
    except NoSuchElementException as e:
        logger.error('xpath' + '不存在!')
        return False
    except:
        return False