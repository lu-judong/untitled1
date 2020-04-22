#!/usr/bin/env python3
# encoding: utf-8

from fabric.api import *
from fabric.context_managers import *
from fabric.contrib.console import confirm
from fabric.contrib.files import exists

import os
import time
env.roledefs = {
        'vip_d':['root@10.8.12.158'],
        'vip_t':['root@182.254.245.67'],
        'python_t':['root@115.159.49.124'],
        'python_p':['root@139.224.68.177','139.196.154.207'],
        'data_manage_t':['root@192.168.1.115'],
        'darams_core_t':['root@192.168.1.115'],
        'lcc_vue_t':['root@192.168.1.25'],
        'iframe_console_t':['root@192.168.1.115'],
        'lcc_core_t':['root@192.168.1.115'],
        }

@roles('lcc_core_t')
def lcc_core_t():
        # settings
        project_path = '/home/'
        jenkins_project_name = 'LCC_CORE_TEST'
        jar_name = 'ifarm-lcc-exec.jar'
        check_url = 'http://192.168.1.115:8283/lcc'

        # do not modify
        full_war_path = '/data/jenkins/workspace/%s/%s/lcc-startup/target/%s' % (jenkins_project_name,'ifarm-lcc',jar_name)
        if int(run('ps -ef | grep -w "%s" | grep -v grep | wc -l' % jar_name)) == 0:
                pass
        else :
                # process clean
                run('ps -ef | grep "%s" | grep -v grep | awk \'{print $2}\' | xargs kill' % jar_name)
                run('sleep 10')
        # clean old files, and move new war file to destination, and start server
        run('rm -rf %s%s' % (project_path,jar_name))
        put(full_war_path,'%s' % project_path)
        run('set -m;java -jar %s%s &' % (project_path,jar_name))
        # check server start or not
        env.warn_only = True
        try_count=10
        for i in range(try_count):
                http_code=run('curl -s -o /tmp/info -m 10 --connect-timeout 10 -w %%{http_code} %s' % check_url)
                if str(http_code) in ['200','302']:
                        print ("http_code is %s" % http_code)
                        return
                else:
                        print("waiting to recheck")
                        time.sleep(10)
                        print(i)
        abort("error, the http_code is %s, not 200" % http_code)

@roles('iframe_console_t')
def iframe_console_t():
        # settings
        project_path = '/home/'
        jenkins_project_name = 'ifarm-console'
        jar_name = 'ifarm-console-exec.jar'
        check_url = 'http://192.168.1.115:8280/console'

        # do not modify
        full_war_path = '/data/jenkins/workspace/%s/%s/console-startup/target/%s' % (jenkins_project_name,jenkins_project_name,jar_name)
        if int(run('ps -ef | grep -w "%s" | grep -v grep | wc -l' % jar_name)) == 0:
                pass
        else :
                # process clean
                run('ps -ef | grep "%s" | grep -v grep | awk \'{print $2}\' | xargs kill' % jar_name)
                run('sleep 10')
        # clean old files, and move new war file to destination, and start server
        run('rm -rf %s%s' % (project_path,jar_name))
        put(full_war_path,'%s' % project_path)
        run('set -m;java -jar %s%s &' % (project_path,jar_name))
        # check server start or not
        env.warn_only = True
        try_count=10
        for i in range(try_count):
                http_code=run('curl -s -o /tmp/info -m 10 --connect-timeout 10 -w %%{http_code} %s' % check_url)
                if str(http_code) in ['200','302']:
                        print ("http_code is %s" % http_code)
                        return
                else:
                        print("waiting to recheck")
                        time.sleep(10)
                        print(i)
        abort("error, the http_code is %s, not 200" % http_code)

@roles('lcc_vue_t')
def lcc_vue_t():
        # vue project
        project_path = '/data/jenkins/workspace/LCC_VUE_T/'
        dist_file_path = 'dist/'
        file_name = 'dist.tar.gz'
        destination_path = '/home/data/vue/'
        put(project_path+dist_file_path+file_name,destination_path)
        run('cd %s && tar -xzvf %s%s ' % (destination_path,destination_path,file_name))

@roles('data_manage_t')
def py_dm_tt():
        process_key_name = 'webserver'
        jenkins_path = '/data/jenkins/workspace/DARAMS_PYTHON_CORE_T/*'
        server_path = '/home/python/data_manage/'
        server_file_name = 'webserver.py'
        python3_path = '/usr/bin/python3.6'

        if      int(run('ps -ef | grep %s | grep -v grep | wc -l' % process_key_name)) == 0:
                pass
        else:
                run('ps -ef | grep %s | grep -v grep | awk \'{print $2}\' | xargs kill -9' % process_key_name)

        put(jenkins_path,server_path)
        run('set -m;cd %s && %s %s &' %(server_path,python3_path,server_file_name))

@roles('data_manage_t')
def py_dm_t():
        env.warn_only = True
        try_count=10
        for i in range(try_count):
                http_code=run('curl -s -o /tmp/info -m 10 --connect-timeout 10 -w %{http_code} http://192.168.1.115:10009/cross')
                if str(http_code) == '200':
                        print ("http_code is %s" % http_code)
                        return
                else:
                        print("waiting to recheck")
                        time.sleep(1)
                        print(i)
        abort("error, the http_code is %s, not 200" % http_code)

@roles('darams_core_t')
def darams_core_t():
        # settings
        project_path = '/home/yangtianfeng/Desktop/apache-tomcat-7.0.88'
        jenkins_project_name = 'DARAMS_CORE_T_1'
        war_name = 'darams.war'
        check_url = 'http://192.168.1.115:8080/darams'

        # do not modify
        full_war_path = '/data/jenkins/workspace/%s/target/%s' % (jenkins_project_name,war_name)
        if int(run('ps -ef | grep -w "%s" | grep -v grep | wc -l' % project_path)) == 0:
                pass
        else :
                # process clean
                run('ps -ef | grep "%s" | grep -v grep | awk \'{print $2}\' | xargs kill' % project_path)
                run('sleep 10')
        # clean old files, and move new war file to destination, and start server
        run('rm -rf %s/webapps/*' % project_path)
        run('rm -rf %s/work/*' % project_path)
        run('rm -rf %s/temp/*' % project_path)
        put(full_war_path,'%s/webapps' % project_path)
        run('set -m;%s/bin/startup.sh' % project_path)
        # check server start or not
        env.warn_only = True
        try_count=10
        for i in range(try_count):
                http_code=run('curl -s -o /tmp/info -m 10 --connect-timeout 10 -w %%{http_code} %s' % check_url)
                if str(http_code) in ['200','302']:
                        print ("http_code is %s" % http_code)
                        return
                else:
                        print("waiting to recheck")
                        time.sleep(10)
                        print(i)
        abort("error, the http_code is %s, not 200" % http_code)

@roles('python_t')
def python_tt():
        if      int(run('ps -ef | grep httpserver | grep -v grep | wc -l')) == 0:
                put('/root/.jenkins/jobs/pythont/workspace/*','/data/test/test/')
                run('set -m;/usr/local/bin/python3 /data/test/test/httpserver.py >> /data/test/test/logs/httpserver.log &')
        else:
                run('ps -ef | grep httpserver | grep -v grep | awk \'{print $2}\' | xargs kill -9')
                put('/root/.jenkins/jobs/pythont/workspace/*','/data/test/test/')
                run('set -m;/usr/local/bin/python3 /data/test/test/httpserver.py >> /data/test/test/logs/httpserver.log &')
@roles('python_t')
def ppt():
        http_code=int(run('curl -s -o /tmp/info -m 10 --connect-timeout 10 -w %{http_code} http://127.0.0.1:10009/py/pressure'))
        if http_code == 200:
                print ("http_code is %s" % http_code)
        else:
                abort("error, the http_code is %s, not 200" % http_code)
@roles('python_p')
def python_p():
        if int(run('ps -ef | grep httpserver | grep -v grep | wc -l')) == 0:
                put('/root/.jenkins/jobs/pythonp/workspace/*','/data/script/')
                run('set -m;/usr/local/bin/python3 /data/script/httpserver.py >> /data/script/logs/httpserver.log &')
        else:
                run('ps -ef | grep httpserver | grep -v grep | awk \'{print $2}\' | xargs kill -9')
                put('/root/.jenkins/jobs/pythonp/workspace/*','/data/script/')
                run('set -m;/usr/local/bin/python3 /data/script/httpserver.py >> /data/script/logs/httpserver.log &')
@roles('python_p')
def ppp():
        http_code=int(run('curl -s -o /tmp/info -m 10 --connect-timeout 10 -w %{http_code} http://www.vipchexian.com/py/pressure'))
        if http_code == 200:
                print ("http_code is %s" % http_code)
        else:
                abort("error,the http_code is %s, not 200" % http_code)
@roles('vip_d')
def vip_d():
        if int(run('ps -ef | grep -w "tomcat-vip" | grep -v grep | wc -l')) == 0:
                run('rm -rf /data/tomcat-vip/webapps/*')
                run('rm -rf /data/tomcat-vip/work/*')
                run('rm -rf /data/tomcat-vip/temp/*')
                put('/root/.jenkins/jobs/vipD-dev/workspace/target/vipinsurance.war','/data/tomcat-vip/webapps')
                run('set -m;/data/tomcat-vip/bin/startup.sh')
                http_codes=int(run('curl -s -o /tmp/info -m 10 --connect-timeout 10 http://m.vipchexian.com/vipinsurance/running -w %{http_code}'))
                if http_codes == 200:
                        print("http_code is 200, ok")
                else:
                        print ("http_code is %s" % http_codes)
                        abort ("error")
        else :
                run('ps -ef | grep "tomcat-vip" | grep -v grep | awk \'{print $2}\' | xargs kill')
                run('sleep 10')
                run('rm -rf /data/tomcat-vip/webapps/*')
                run('rm -rf /data/tomcat-vip/work/*')
                run('rm -rf /data/tomcat-vip/temp/*')
                put('/root/.jenkins/jobs/vipD-dev/workspace/target/vipinsurance.war','/data/tomcat-vip/webapps')
                run('set -m;/data/tomcat-vip/bin/startup.sh')
                http_codes=int(run('curl -s -o /tmp/info -m 10 --connect-timeout 10 http://m.vipchexian.com/vipinsurance/running -w %{http_code}'))
                if http_codes == 200:
                        print("http_code is 200, ok")
                else:
                        print ("http_code is %s" % http_codes)
                        abort ("error")

@roles('vip_t')
def vip_t():
        if int(run('ps -ef | grep -w "tomcat-vip" | grep -v grep | wc -l')) == 0:
                run('rm -rf /data/usr/local/tomcat-vip/webapps/*')
                run('rm -rf /data/usr/local/tomcat-vip/work/*')
                run('rm -rf /data/usr/local/tomcat-vip/temp/*')
                put('/root/.jenkins/jobs/vipT-test_20161101/workspace/target/vipinsurance.war','/data/usr/local/tomcat-vip/webapps')
                run('set -m;/data/usr/local/tomcat-vip/bin/startup.sh')
                run('sleep 20')
                http_code=int(run('curl -s -o /tmp/info -m 10 --connect-timeout 10 http://182.254.245.67:9087/vipinsurance/running -w %{http_code}'))
                if http_code == 200:
                        print("http_code is 200, ok")
                else:
                        print("http_code is not 200 ,error")
                        abort ("error")
        else :
                run('ps -ef | grep "tomcat-vip" | grep -v grep | awk \'{print $2}\' | xargs kill')
                run('sleep 10')
                run('rm -rf /data/usr/local/tomcat-vip/webapps/*')
                run('rm -rf /data/usr/local/tomcat-vip/work/*')
                run('rm -rf /data/usr/local/tomcat-vip/temp/*')
                put('/root/.jenkins/jobs/vipT-test_20161101/workspace/target/vipinsurance.war','/data/usr/local/tomcat-vip/webapps')
                run('set -m;/data/usr/local/tomcat-vip/bin/startup.sh')
                run('sleep 20')
                http_code=int(run('curl -s -o /tmp/info -m 10 --connect-timeout 10 http://182.254.245.67:9087/vipinsurance/running -w %{http_code}'))
                if http_code == 200:
                        print ("http_code is 200, ok")
                else:
                        print ("http_code is not 200 ,error")
                        abort ("error")

