from selenium import webdriver
from config.login import *
from config.config import url,username,password,compare_title
import os

def compare_picture(url,username,password,modelName):
    driver = webdriver.Chrome()
    try:
        driver.get(url)
    except:
        print('地址输入错误')
    login(driver,username,password)
    time.sleep(2)
    driver.find_element_by_id('balla').click()
    time.sleep(3)

    try:
        for i in compare_title:
            driver.find_element_by_xpath('//span[text()="{}"]'.format(i)).click()
            time.sleep(1)
        print('点击'+i+'成功')
    except:
        print('点击' + i + '失败')

    driver.maximize_window()
    time.sleep(2)

    a = len(driver.find_elements_by_xpath('//a[text()="{}"]'.format(modelName)))

    for i in range(0,a):
        try:
            driver.find_elements_by_xpath('//a[text()="{}"]/../../../td[7]/div/a[4]'.format(modelName))[i].click()
        except:
            pass
    try:
        time.sleep(1)
        driver.find_element_by_xpath('//div[text()="图表"]')

        folder_path2 = os.getcwd().replace('\\', '/')
        driver.save_screenshot(folder_path2+'\\' + '百万公里故障率' +'.png')
    except Exception as e:
        print(e)
        print('点击图表按钮失败')
        return

compare_picture(url,username,password,'1.16测试')