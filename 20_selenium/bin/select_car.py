import time
from bin.main import Method
from selenium.common.exceptions import NoSuchElementException
from config.log_config import logger


# 选车

def deal_car(driver,car):
    try:
        for x in car:
            driver.find_element_by_xpath(
                "//span[@class='train zoomIn' and text()=\'{}\']".format(x)).click()
            car_num = car.get(x)
            time.sleep(2)
            if car_num == 'all':
                driver.execute_script('top.select_all(this,"train-no-layer-class",true,true)')
            elif type(car_num).__name__ == 'list':
                for i in car_num:
                    # driver.find_element_by_xpath("//span[contains(text(),\'{}\')]".format(i)).click()
                    car_num = driver.find_element_by_xpath('//span[text()=\'{}\']/..'.format(i)).get_attribute('id')

                    js = 'top.checked(top.$("#{}"))'.format(car_num)
                    driver.execute_script(js)
            else:
                if round(len(driver.find_elements_by_class_name("train-no-layer-class"))*float(car_num)) == 0:
                    a = 1
                else:
                    a = round(len(driver.find_elements_by_class_name("train-no-layer-class"))*float(car_num))
                for i in range(0,a):
                    carnum = driver.execute_script('return $($(".train-no-layer-class>span")[{}]).text()'.format(i))
                    id1 = driver.find_element_by_xpath('//span[text()=\'{}\']/..'.format(carnum)).get_attribute('id')
                    js = 'top.checked(top.$("#{}"))'.format(id1)
                    driver.execute_script(js)

                # time.sleep(2)
            driver.execute_script('top.$(".layui-layer-btn0")[2].click()')
            time.sleep(2)
        Method(driver).switch_out()
        # 这个可以点击得元素失去焦点
        # Message: unknown error: Element <a class="layui-layer-btn1">...</a> is not clickable at point (975, 498). Other element would receive the click: <a class="layui-layer-btn3">...</a>
        # Method(driver).two_element_click("[class='layui-layer-btn layui-layer-btn-']",'layui-layer-btn1')
        Method(driver).two_element_click("[class='layui-layer layui-layer-iframe my-skin']", 'layui-layer-btn1')
        return True
    except NoSuchElementException as e:
        logger.error('xpath' + '不存在!')
        return False