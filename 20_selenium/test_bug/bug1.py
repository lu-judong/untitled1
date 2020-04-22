from bin.login import Login
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome()
Login().login('http://192.168.1.115:9092/darams/a?login', 'admin', 'admin', driver)

time.sleep(2)
driver.find_element_by_xpath('//*[@id="1"]/li[1]/a').click()
driver.switch_to.frame(driver.find_element_by_xpath("//iframe[contains(@src,'/darams/a/home')]"))
canvas = driver.find_element_by_xpath('//*[@id="header_left"]/div[1]/canvas')
driver.execute_script(''
                      'canvas.addEventListener("click", function(event) '
                      '{getMousePos(canvas, event);});'
                      'function getMousePos(canvas, event)'
                      '{var rect = canvas.getBoundingClientRect();'
                      'var x = event.clientX - rect.left * (canvas.width / rect.width);'
                      'var y = event.clientY - rect.top * (canvas.height / rect.height);'
                      'console.log("x:"+x+",y:"+y);}')

