import os
import paramiko
import requests
import time

host = '192.168.1.20'
user = 'Administrator'
password = 'zaq12wsx.'
localpath = '/data/jenkins/workspace/DARAMS_CORE_T_1/target/darams.war'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, 22, username=user, password=password, timeout=10)
# stdin1, stdout1, stderr1 = client.exec_command(
#                     'cmd /c copy F:\\Users\\Administrator\\bug.txt '
#                     'D:\\tools\\tomcat8.0-2\\webapps\\bug.txt')
# if stdout1.read().decode('gbk')[:3] == '已复制':
#     print('复制成功')
# else:
#     print('复制失败')
stdin1, stdout1, stderr1 = client.exec_command('cmd /c netstat -ano |findstr "8083"')
pid = stdout1.read().decode('gbk')[-7:].replace(' ','')

if pid is not '':
    stdin2, stdout2, stderr2 = client.exec_command('cmd /c taskkill /f /t /im %s' % pid)
    if stdout2.read().decode('gbk')[:2] == '成功':
        print('server kill success')
    else:
        print('server kill failed')
    stdin3, stdout3, stderr3 = client.exec_command('cmd /c net start tomcat')

    success = False
    for i in range(10):
        try:
            http_code = requests.get('http://192.168.1.20:8083/darams/a').status_code
            if str(http_code) in ['200', '302']:
                print("http_code is %s" % http_code)
                success = True
                break
            else:
                print("waiting to recheck")
                time.sleep(10)
                print(i)
        except:
            print("waiting to recheck")
            time.sleep(10)
            print(i)

    if success is False:
        raise Exception
    else:
        print('serve is start')

else:
    stdin2, stdout2, stderr2 = client.exec_command('cmd /c cd net start tomcat')
    time.sleep(3)


    success = False
    for i in range(10):
        try:
            http_code = requests.get('http://192.168.1.20:8083/darams/a').status_code
            if str(http_code) in ['200', '302']:
                print("http_code is %s" % http_code)
                success = True
                break
            else:
                print("waiting to recheck")
                time.sleep(10)
                print(i)
        except:
            print("waiting to recheck")
            time.sleep(10)
            print(i)

    if success is False:
        raise Exception
    else:
        print('serve is start')