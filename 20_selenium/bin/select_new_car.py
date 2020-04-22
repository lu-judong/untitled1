import time
from bin.main import Method
from config.log_config import logger
import random



# 一个车型一个车号
def deal_new_car(driver):
    carList = []

    try:
        first = len(driver.find_elements_by_xpath("//span[@class='train zoomIn']"))

        car_1 = random.randint(0, first - 1)
        # car_1 = 0
        driver.find_elements_by_xpath("//span[@class='train zoomIn']")[car_1].click()

        carList.append(driver.find_elements_by_xpath("//span[@class='train zoomIn']")[car_1].text)

        car_num = random.randint(0,len(driver.find_elements_by_xpath("//div[@class='train-no-layer-class ivu-modal-wrap ivu-tag ']"))-1)

        js = ' return $($(".train-no-layer-class>span")[{}]).text()'.format(car_num)
        carnum = driver.execute_script(js)
        carList.append(carnum)
        id1 = driver.find_element_by_xpath('//span[text()=\'{}\']/..'.format(carnum)).get_attribute('id')
        js1 = 'top.checked(top.$("#{}"))'.format(id1)
        driver.execute_script(js1)
        time.sleep(2)
        driver.execute_script('top.$(".layui-layer-btn0")[2].click()')
        time.sleep(2)

        Method(driver).switch_out()

        Method(driver).two_element_click("[class='layui-layer layui-layer-iframe my-skin']", 'layui-layer-btn1')
        return True,carList
    except:
        logger.error('xpath' + '不存在!')
        return False,carList

# 一个车型多个车号
def deal_new_car1(driver):
    carList = []
    try:
        L = []
        first = len(driver.find_elements_by_xpath("//span[@class='train zoomIn']"))

        car_1 = random.randint(0, first - 1)
        # car_1 = 0
        driver.find_elements_by_xpath("//span[@class='train zoomIn']")[car_1].click()

        carList.append(driver.find_elements_by_xpath("//span[@class='train zoomIn']")[car_1].text)

        if len( driver.find_elements_by_xpath("//div[@class='train-no-layer-class ivu-modal-wrap ivu-tag ']")) == 1:
            car_num = 0
        else:
            car_num = random.randint(1, len(driver.find_elements_by_xpath("//div[@class='train-no-layer-class ivu-modal-wrap ivu-tag ']")) - 1)
        while len(L) <= car_num:
            car_num1 = random.randint(0, len(
                driver.find_elements_by_xpath("//div[@class='train-no-layer-class ivu-modal-wrap ivu-tag ']")) - 1)
            if car_num1 not in L:
                L.append(car_num1)
                js = ' return $($(".train-no-layer-class>span")[{}]).text()'.format(car_num1)
                carnum = driver.execute_script(js)
                carList.append(carnum)
                id1 = driver.find_element_by_xpath('//span[text()=\'{}\']/..'.format(carnum)).get_attribute('id')
                js1 = 'top.checked(top.$("#{}"))'.format(id1)
                driver.execute_script(js1)
                time.sleep(2)
            else:
                pass
        driver.execute_script('top.$(".layui-layer-btn0")[2].click()')
        time.sleep(2)

        Method(driver).switch_out()

        Method(driver).two_element_click("[class='layui-layer layui-layer-iframe my-skin']", 'layui-layer-btn1')
        return True,carList
    except:
        logger.error('xpath'+'不存在')
        return False,carList

# 一个车型全量车号
def deal_new_car2(driver):
    carList = []
    try:
        first = len(driver.find_elements_by_xpath("//span[@class='train zoomIn']"))

        car_1 = random.randint(0, first - 1)
        # car_1 = 0
        driver.find_elements_by_xpath("//span[@class='train zoomIn']")[car_1].click()

        carList.append(driver.find_elements_by_xpath("//span[@class='train zoomIn']")[car_1].text)
        carList.append('all')
        driver.execute_script('top.select_all(this,"train-no-layer-class",true,true)')
        time.sleep(2)
        driver.execute_script('top.$(".layui-layer-btn0")[2].click()')
        time.sleep(2)

        Method(driver).switch_out()

        Method(driver).two_element_click("[class='layui-layer layui-layer-iframe my-skin']", 'layui-layer-btn1')
        return True,carList
    except:
        logger.error('xpath' + '不存在!')
        return False,carList

# 多个车型一个车号
def deal_new_car3(driver):
    carList = []
    try:


        L  = []
        first = len(driver.find_elements_by_xpath("//span[@class='train zoomIn']"))
        # num = random.randint(1, 7)
        num = 7
        while len(L) <= num:
            car_1 = random.randint(0, first-1)

            if car_1 not in L:
                L.append(car_1)
                driver.find_elements_by_xpath("//span[@class='train zoomIn']")[car_1].click()

                car_num = random.randint(0, len(
                    driver.find_elements_by_xpath("//div[@class='train-no-layer-class ivu-modal-wrap ivu-tag ']")) - 1)

                js = ' return $($(".train-no-layer-class>span")[{}]).text()'.format(car_num)
                carnum = driver.execute_script(js)

                carList.append((driver.find_elements_by_xpath("//span[@class='train zoomIn']")[car_1].text,carnum))

                id1 = driver.find_element_by_xpath('//span[text()=\'{}\']/..'.format(carnum)).get_attribute('id')
                js1 = 'top.checked(top.$("#{}"))'.format(id1)
                driver.execute_script(js1)
                time.sleep(2)
                driver.execute_script('top.$(".layui-layer-btn0")[2].click()')
                time.sleep(2)
            else:
                pass

        Method(driver).switch_out()

        Method(driver).two_element_click("[class='layui-layer layui-layer-iframe my-skin']", 'layui-layer-btn1')
        return True,carList
    except:
        logger.error('xpath' + '不存在')
        return False,carList

# 多个车型多个车号
def deal_new_car4(driver):
    carList = []
    try:
        L = []

        first = len(driver.find_elements_by_xpath("//span[@class='train zoomIn']"))

        num = random.randint(1, 8)
        while len(L) <= num:
            car_1 = random.randint(0, first - 1)
            if car_1 not in L:
                L.append(car_1)
                driver.find_elements_by_xpath("//span[@class='train zoomIn']")[car_1].click()

                carNum = []
                L1 = []
                if len(driver.find_elements_by_xpath("//div[@class='train-no-layer-class ivu-modal-wrap ivu-tag ']")) == 1:
                    car_num = 0
                else:
                    # car_num = random.randint(1, len(driver.find_elements_by_xpath("//div[@class='train-no-layer-class ivu-modal-wrap ivu-tag ']")) - 1)
                    car_num = 1
                while len(L1) <= car_num:
                    car_num1 = random.randint(0, len(driver.find_elements_by_xpath("//div[@class='train-no-layer-class ivu-modal-wrap ivu-tag ']")) - 1)
                    if car_num1 not in L1:
                        L1.append(car_num1)
                        js = ' return $($(".train-no-layer-class>span")[{}]).text()'.format(car_num1)
                        carnum = driver.execute_script(js)
                        carNum.append(carnum)
                        id1 = driver.find_element_by_xpath('//span[text()=\'{}\']/..'.format(carnum)).get_attribute(
                            'id')
                        js1 = 'top.checked(top.$("#{}"))'.format(id1)
                        driver.execute_script(js1)
                        time.sleep(2)
                    else:
                        pass
                carList.append((driver.find_elements_by_xpath("//span[@class='train zoomIn']")[car_1].text,carNum))
                driver.execute_script('top.$(".layui-layer-btn0")[2].click()')
                time.sleep(2)
            else:
                pass
        # car_1 = 0

        time.sleep(2)

        Method(driver).switch_out()

        Method(driver).two_element_click("[class='layui-layer layui-layer-iframe my-skin']", 'layui-layer-btn1')
        return True,carList
    except Exception as e:
        logger.error(e)
        return False,carList

# 多车型全量车号
def deal_new_car5(driver):
    carList = []
    try:
        L = []

        first = len(driver.find_elements_by_xpath("//span[@class='train zoomIn']"))

        # num = random.randint(1, 4)
        num = 4
        while len(L) <= num:
            car_1 = random.randint(0, first - 1)
            if car_1 not in L:
                L.append(car_1)
                driver.find_elements_by_xpath("//span[@class='train zoomIn']")[car_1].click()

                carList.append((driver.find_elements_by_xpath("//span[@class='train zoomIn']")[car_1].text,'all'))

                time.sleep(1)
                driver.execute_script('top.select_all(this,"train-no-layer-class",true,true)')
                time.sleep(2)

                driver.execute_script('top.$(".layui-layer-btn0")[2].click()')
                time.sleep(2)
            else:
                pass
        # car_1 = 0

        time.sleep(2)

        Method(driver).switch_out()

        Method(driver).two_element_click("[class='layui-layer layui-layer-iframe my-skin']", 'layui-layer-btn1')
        return True,carList
    except:
        logger.error('xpath' + '不存在!')
        return False,carList