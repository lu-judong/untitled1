from bin.main import Method
import time

class Login:
    def login(self,url,username,password,driver):
        Method(driver).jumpwebpage(url)
        time.sleep(2)
        try:
            # 用户名定位
            Method(driver).clear('id', 'username')
            Method(driver).input('id', 'username', username)
            # 密码定位
            Method(driver).clear('id', 'password')
            Method(driver).input('id', 'password', password)
            # 点击登录
            Method(driver).click('xpath', '//*[@id="submit"]')

            return True

        except Exception as e:
            print(e)

            return  False





