from .main import Method,log_file_out
import time
from config.log_config import logger

def login(url,username,password,driver):
    Method(driver).jumpwebpage(url)
    time.sleep(2)
    try:
        # 用户名定位
        Method(driver).clear('id','username')
        Method(driver).input('id','username',username)
        # 密码定位
        Method(driver).clear('id', 'password')
        Method(driver).input('id', 'password', password)

        # 点击登录
        Method(driver).click('xpath','//*[@id="submit"]')
        return True
    except Exception as e:
        logger.error(e)
        return False



# 模型新增 从登录到点击创建内容按钮之间的动作
def new_built(driver,url,username,password,contents,type):
    try:
        status = login(url, username, password, driver)
        if status is True:
            time.sleep(2)
            driver.maximize_window()
            Method(driver).click('id', 'balla')
            driver.maximize_window()


            time.sleep(2)
            if contents == '':
                pass
            else:
                if contents[1] == '运维数据清洗':
                    Method(driver).contains_xpath('click', contents[0])
                    time.sleep(1)
                    target = driver.find_element_by_xpath('//span[text()=\'{}\']'.format(contents[1]))
                    driver.execute_script("arguments[0].scrollIntoView();", target)
                    time.sleep(1)
                    Method(driver).contains_xpath('click', contents[1])
                else:
                    for i in contents:
                        try:
                            Method(driver).contains_xpath('click', i)
                            time.sleep(1)
                            log_file_out('点击' + i + '成功')
                        except Exception as e:
                            logger.debug(e)
                            log_file_out('点击' + i + '失败')
            time.sleep(2)
            # 1代表新建 2代表其他
            if type == 1:
                # 点击新建得到弹框
                try:
                    Method(driver).click('xpath', '//*[text()=\'{}\']'.format('创建内容'))
                    log_file_out('点击创建内容按钮成功')
                except Exception as e:
                    logger.error(e)
                    log_file_out('点击创建内容按钮失败')
            elif type == 2:
                pass
            elif type == 3:
                # 点击不保存计算
                try:
                    Method(driver).click('xpath','//span[text()=\'{}\']'.format('不保存计算'))
                    log_file_out('点击不保存计算按钮成功')
                except Exception as e:
                    logger.error(e)
                    log_file_out('点击不保存计算按钮失败')
            return True
        else:
            log_file_out('登录失败')
            return
    except Exception as e:
        logger.error(e)
        return False

