import time
from bin.main import Method
from selenium.common.exceptions import NoSuchElementException
from config.log_config import logger


# 选车

def deal_car(driver,car):
    try:
        for x in car:
            driver.find_element_by_xpath(
                "//span[@class='train zoomIn' and contains(text(),\'{}\')]".format(x)).click()
            car_num = car.get(x)
            time.sleep(2)
            for i in car_num:
                # driver.find_element_by_xpath("//span[contains(text(),\'{}\')]".format(i)).click()
                car_num = driver.find_element_by_xpath('//span[contains(text(),\'{}\')]/..'.format(i)).get_attribute('id')

                js = 'top.checked(top.$("#{}"))'.format(car_num)
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