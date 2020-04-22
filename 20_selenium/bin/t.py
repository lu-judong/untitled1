import time
from bin.main import Method
from selenium.webdriver.common.action_chains import ActionChains


def wait_time(driver,x):
    i = 0
    while i < 20:
        try:
            time.sleep(0.2)
            if len(driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(x[:-7]))) > 0:
                return len(driver.find_elements_by_xpath('//*[@id= \'{}\']/ul/li'.format(x[:-7])))
            i += 1
        except:
            i += 1

def wait_time1(driver,text):
        i = 0

        while i < 20:
            try:
                time.sleep(0.2)
                if Method(driver).contains_new(text) is not '':
                    fault_next = Method(driver).contains_new(text)
                    xpath = driver.find_element_by_xpath('//*[@id= \'{}\']/i'.format(fault_next[:-7]))
                    ActionChains(driver).move_to_element(xpath).click(xpath).perform()

                    # Method(driver).click('xpath', '//*[@id= \'{}\']/i'.format(fault_next[:-7]))
                    return fault_next
                i += 1
            except:
                i += 1


class err_catch():
    def catch(self,object='sys.exc_info()'):
        return_val = []
        tb_curr = object[2]
        while tb_curr.tb_next:
            return_val.append('traceback:%s,function:%s,line:%s' % (
                tb_curr.tb_next.tb_frame.f_code, tb_curr.tb_next.tb_frame.f_code.co_name,
                tb_curr.tb_next.tb_frame.f_lineno))
            tb_curr = tb_curr.tb_next
        return_val.append('valueError:%s' % (str(object[1].args)))
        return return_val

