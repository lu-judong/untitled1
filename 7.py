import paramiko
import os
from new_selenium.config.log_config import logger
import time
import datetime
import requests



def upload(localpath):
    try:
        t = paramiko.Transport((host, 22))
        t.connect(username=user, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        localpath = localpath

        local_size = os.path.getsize(localpath)

        sftp.put(localpath,'darams.war')

        t.close()
        return [True,local_size]
    except Exception as e:
        logger.error(e)
        logger.debug('上传失败')
        return [False,1]

def copy(remote_default_path,remote_purpose_path,port,url):
    # paramiko.util.log_to_file('syslogin.log') #日志记录
    a = upload(localpath)
    try:
        if a[0] is True:

            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(host, 22, username=user, password=password, timeout=10)

            stdin, stdout, stderr = client.exec_command(
                'cmd /c dir {}\\darams.war > 1.txt'.format(remote_default_path))

            time.sleep(2)
            stdin, stdout, stderr = client.exec_command(
                'cmd /c type {}\\1.txt'.format(remote_default_path))
            content = stdout.read().decode('gbk')

            remote_size = int(content.split('\r\n')[-3].split(' ')[-2].replace(',',''))
            if remote_size == a[1]:
                logger.debug('上传成功')
                print('上传成功')

                year = datetime.datetime.now().year
                month = datetime.datetime.now().month
                if month < 10:
                    new_month = '0' + str(month)
                else:
                    new_month = str(month)
                day = datetime.datetime.now().day
                if day < 10:
                    new_day = '0' + str(day)
                else:
                    new_day = str(day)


                rename_time = str(year) + new_month + new_day

                stdin_exist,stdout_exist,stderr_exist = client.exec_command('cmd /c if exist %s\\darams.war%s (echo 1) else (echo 0)'%(remote_purpose_path,rename_time))
                # stdin_exist, stdout_exist, stderr_exist = client.exec_command(
                #     'cmd /c if exist D:\\tools\\tomcat8.0-2\\webapps\\darams.war (echo 1) else (echo 0)')
                if int(stdout_exist.read().decode('gbk').split('\r\n')[0]) == 1:
                    stdin_del, stdout1_del, stderr1_del = client.exec_command(
                        'cmd /c del/f/s/q %s\\darams.war%s' % (remote_purpose_path,rename_time))
                else:
                    pass
                stdin, stdout, stderr = client.exec_command('cmd /c rename %s\\darams.war darams.war%s' % (remote_purpose_path,rename_time))

                if stdout.read().decode('gbk') == '':
                    print('重命名成功')

                    time.sleep(3)
                    stdin1, stdout1, stderr1 = client.exec_command(
                        'cmd /c copy %s\\darams.war %s\\darams.war' % (remote_default_path,remote_purpose_path))

                    if stdout1.read().decode('gbk')[:3] == '已复制':
                        print('复制成功')
                        logger.debug('复制成功')


                        stdin1, stdout1, stderr1 = client.exec_command('cmd /c netstat -ano |findstr "{}"'.format(port))
                        pid = stdout1.read().decode('gbk')[-7:].replace(' ', '')

                        if pid is not '':
                            stdin2, stdout2, stderr2 = client.exec_command('cmd /c taskkill /f /t /im %s' % pid)
                            if stdout2.read().decode('gbk')[:2] == '成功':
                                print('server kill success')
                            else:
                                print('server kill failed')

                            stdin_del_darams, stdout_del_darams, stdeer_del_darams = client.exec_command('cmd /c rd /s /q {}\\darams'.format(remote_purpose_path))

                            stdin3, stdout3, stderr3 = client.exec_command('cmd /c net start tomcat')

                            success = False
                            for i in range(10):
                                try:
                                    http_code = requests.get('{}'.format(url)).status_code
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
                                    http_code = requests.get('{}'.format(url)).status_code
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
                        print('复制失败')
                        logger.debug('复制失败')

                        stdin, stdout, stderr = client.exec_command(
                            'cmd /c rename %s\\darams.war%s darams.war'% (remote_purpose_path,rename_time))


                else:
                    print('重命名失败')
                    logger.debug('重命名失败')
                    return
            else:
                logger.debug('上传失败')
                return
            # print(stdout.read())
            # for line in stdout.readlines():
            #   print(line)
            # client.close()
        else:
            print('上传失败')
            logger.debug('上传失败')
            return

        stdin1, stdout1, stderr1 = client.exec_command('cmd /c del/f/s/q {}\\darams.war'.format(remote_default_path))
    except:
        stdin1, stdout1, stderr1 = client.exec_command('cmd /c del/f/s/q {}\\darams.war'.format(remote_default_path))

        raise Exception



host = '192.168.1.20'
user = 'Administrator'
password = 'zaq12wsx.'


# localpath = '/data/jenkins/workspace/DARAMS_CORE_T_1/target/darams.war'
localpath = r'C:\Users\a\Desktop\darams.war'

remote_default_path = 'F:\\Users\\Administrator'

remote_purpose_path = 'D:\\tools\\tomcat8.0-2\\webapps'
port = '8083'
url = 'http://192.168.1.20:8083/darams/a?login'

copy(remote_default_path,remote_purpose_path,'8083',url)








