from selenium import webdriver
from config.login import *
from config.config import url,username,password,compare_title
import re

def compare_test(url,username,password,modelName,value,value1):
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

    time.sleep(1)

    if driver.find_element_by_xpath('//*[@id="right_content"]/div/div[1]/div/p').text == compare_title[1]:
        print(compare_title[1]+'菜单名称与菜单页内容对应')
    else:
        print(compare_title[1] + '菜单名称与菜单页内容不对应')

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
        print('模型名称输入框高级搜索验证成功')
    else:
        print('模型名称输入框高级搜索验证失败')

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
        print('验证成功')
    elif int(nu1[0]) <= 10:
        if value == 1:
            if len(driver.find_elements_by_xpath('//div[text()="故障模式"]')) !=0:
                print('评估对象选择框验证失败')
            else:
                print('评估对象选择框验证成功')
        else:
            if len(driver.find_elements_by_xpath('//div[text()="评估系统、部件"]')) != 0:
                print('评估对象选择框验证失败')
            else:
                print('评估对象选择框验证成功')
    else:
        for i in range(0,(int(nu1[0])//10)+1):
            driver.find_element_by_xpath('//a[text()="{}"]'.format(i+1)).click()
            if value == 1:
                if len(driver.find_elements_by_xpath('//div[text()="故障模式"]')) != 0:
                    print('第'+str(i+1)+'页'+'评估对象选择框验证失败')
                else:
                    print('第'+str(i+1)+'页'+'评估对象选择框验证成功')
            else:
                if len(driver.find_elements_by_xpath('//div[text()="评估系统、部件"]')) != 0:
                    print('第'+str(i+1)+'页'+'评估对象选择框验证失败')
                else:
                    print('第'+str(i+1)+'页'+'评估对象选择框验证成功')

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
                print('计算状态选择框验证失败')
            else:
                print('计算状态选择框验证成功')
        elif value1 == 2:
            if len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0 and \
                    len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) != 0 and \
                    len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                print('计算状态选择框验证失败')
            else:
                print('计算状态选择框验证成功')
        elif value1 == 3:
            if len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0 and \
                    len(driver.find_elements_by_xpath('//div[text()="计算中"]')) != 0 and \
                    len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                print('计算状态选择框验证失败')
            else:
                print('计算状态选择框验证成功')
        else:
            if len(driver.find_elements_by_xpath('//div[text()="计算中"]')) !=0 and \
                    len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) !=0 and \
                    len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0:
                print('计算状态选择框验证失败')
            else:
                print('计算状态选择框验证成功')
    else:
        for i in range(0,(int(nu3[0])//10)+1):
            driver.find_element_by_xpath('//a[text()="{}"]'.format(i+1)).click()
            if value1 == 1:
                if len(driver.find_elements_by_xpath('//div[text()="计算中"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                    print('第' + str(i) + '页' + '计算状态选择框验证失败')
                else:
                    print('第' + str(i) + '页' + '计算状态选择框验证成功')
            elif value1 == 2:
                if len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                    print('第' + str(i) + '页' + '计算状态选择框验证失败')
                else:
                    print('第' + str(i) + '页' + '计算状态选择框验证成功')
            elif value1 == 3:
                if len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算中"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算完成"]')) != 0:
                    print('第' + str(i) + '页' + '计算状态选择框验证失败')
                else:
                    print('第' + str(i) + '页' + '计算状态选择框验证成功')
            else:
                if len(driver.find_elements_by_xpath('//div[text()="计算中"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="计算异常"]')) != 0 and \
                        len(driver.find_elements_by_xpath('//div[text()="未计算"]')) != 0:
                    print('第' + str(i) + '页' + '计算状态选择框验证失败')
                else:
                    print('第' + str(i) + '页' + '计算状态选择框验证成功')


compare_test(url,username,password,'1.16测试',1,4)