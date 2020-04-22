from selenium import webdriver
from config.login import *
from config.config import url,username,password,tech_title
import os

def tech_picture(url,username,password,modelName):
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
        for i in tech_title:
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
            driver.find_elements_by_xpath('//a[text()="{}"]/../../../td[6]/div/a[4]'.format(modelName))[i].click()
        except:
            pass
    try:
        time.sleep(2)
        folder_path2 = os.getcwd().replace('\\', '/')
        target = driver.find_elements_by_class_name('chartParatDom')[0]
        driver.execute_script("arguments[0].scrollIntoView();", target)
        driver.save_screenshot(folder_path2 +'\\' + '变更前后百万公里故障率' + '.png')
    except:
        print('截取各系统/部件故障占比失败')
    try:
        time.sleep(1)
        target = driver.find_elements_by_class_name('chartParatDom')[1]
        driver.execute_script("arguments[0].scrollIntoView();", target)
        driver.save_screenshot(folder_path2 + '\\' + '各部件变更前后百万公里故障率' + '.png')
        time.sleep(1)
        target = driver.find_elements_by_class_name('chartParatDom')[2]
        driver.execute_script("arguments[0].scrollIntoView();", target)
        driver.save_screenshot(folder_path2 + '\\' + '百万公里故障率' + '.png')
        time.sleep(1)
        target = driver.find_elements_by_class_name('chartParatDom')[3]
        driver.execute_script("arguments[0].scrollIntoView();", target)
        driver.save_screenshot(folder_path2 + '\\' + '变更前后固有可用度' + '.png')
        time.sleep(1)

    except:
        print('点击图表按钮失败')
        return

tech_picture(url,username,password,'西安测试dateold')