from fabric.api import *


env.shell="cmd.exe /c"
env.connect_timeout = 5

# java = 'root@192.168.1.20:22'

# java = 'root@192.168.1.115:22'
# env.hosts = ['root@192.168.1.20:22']


# env.passwords = {
#     'root@192.168.1.20:22':'123456'
# }

env.roledefs = {
  'java':['root@192.168.1.20:22']
}

env.password = '123456'

@roles('java')
def java():
    # project_path = '/home/yangtianfeng/Desktop/apache-tomcat-7.0.88'
    # jenkins_project_name = 'DARAMS_CORE_T_1'
    # war_name = 'darams.war'
    # check_url = 'http://192.168.1.115:8080/darams'

    # full_war_path = '/data/jenkins/workspace/%s/target/%s' % (jenkins_project_name, war_name)

    run('copy F:\\Users\\Administrator\\bug.txt D:\\tools\\tomcat8.0-2\\webapps\\dd.txt',timeout=10)


    print('aaa')


# p = os.popen('netstat -ano |findstr "2000"')
# print(p.read())
#
# p1 = os.popen('netstat -ano |findstr "1008"')
# print(p1.read()[-5:-1])