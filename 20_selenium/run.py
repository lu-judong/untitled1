import time
from test_weixiu import test_methods_weixiu, tech_wei_cal
from test_techm import test_tech
from test_nhpp import tech_nhpp_s
from test_fault import test_fault1
from tech_rcma import test_rcma_a
from test_compare import compare_cal
from test_nhpp_cal import tech_nh_cal
from test_rams import tech_ram
from tech_test_cal import tech_cal_views
from test_fmeca import tech_fme_cal

url = 'http://192.168.1.115:9092/darams/a?login'

username = 'test'
password = '1234'


car = {
    'E01': ['2001', '2002']
}

min_model = [['m1', '0', '100',2, 3,{'E05': ['2091', '2092']},{'高压供电系统': 'all'}], ['m2', '100', '200', 2,3,{'E05': ['2091', '2092']},{'高压供电系统': 'all'}]]

fault_pattern = {'高压供电系统':'all'}
fault_object = {
    '高压供电系统':{'高压电缆、连接器及跳线':['电缆']},
    '辅助供电系统':['刮雨器电源'],
    '门窗系统':'all'
}

time_sleep = 2
wait_time = 10


class Run:
    def log_file_out(self,msg):
        fo = open(r'\usecase.txt', mode='a', encoding='utf-8')
        fo.write(msg + '\r\n')
        fo.close()


    def run(self):
        try:
            test_methods_weixiu.test_technology().tech(url,username,password,'111', '111', 2, '', '0', '100', 2, '200', 1, 3, car,fault_pattern,time_sleep,wait_time)
        except Exception as e:
            self.log_file_out('维修规程优化测试失败')

        time.sleep(20)
        try:
            test_tech.Tech().tech_analysis(url,username,password,'技术整改测试2','技术整改数据测试2',2,'111','180','200','300',1,'3',car,fault_pattern,time_sleep,wait_time)
        except Exception as e:
            self.log_file_out('技术整改测试失败')

        time.sleep(20)
        try:
            tech_nhpp_s.Tech().tech_nhpp_model(url,username,password,'nhpp2','nhpp2','2015-02-12','2018-03-12',car,time_sleep,wait_time)
        except Exception as e:
            self.log_file_out('整车NHPP模型测试失败')

        time.sleep(20)
        try:
            test_fault1.Tech().tech_fault_analysis(url,username,password,'数据测试2','数据测试2',1,'','0','100',1,'3',car,fault_pattern,time_sleep,wait_time)
        except Exception as e:
            self.log_file_out('故障占比分析测试失败')

        time.sleep(20)
        try:
            test_rcma_a.Tech().tech_rcma_count(url,username,password,'RCMA2','RCMA2','','1.2','200000','2','3','100000',time_sleep)
        except Exception as e:
            self.log_file_out('RCMA计算测试失败')

        time.sleep(20)
        try:
            compare_cal.Tech().tech_analysis(url,username,password,1,'里程',min_model,time_sleep,wait_time)
        except Exception as e:
            print(e)
            self.log_file_out('不同平台不保存计算测试失败')

        time.sleep(20)
        try:
            tech_nh_cal.Tech().tech_nhpp_model(url,username,password,'2017-08-01','2018-03-12',car,time_sleep,wait_time)
        except Exception as e:
            print(e)
            self.log_file_out('NHPP不保存计算测试失败')

        time.sleep(20)
        try:
            tech_ram.Tech().tech_fault_analysis(url,username,password,1,'里程','0','100',car,fault_pattern,time_sleep,wait_time)
        except Exception as e:
            print(e)
            self.log_file_out('rams三合一测试失败')

        time.sleep(20)
        try:
            tech_cal_views.Tech().tech_analysis(url,username,password,2,'0','100','100','200',car,fault_pattern,time_sleep,wait_time)
        except Exception as e:
            print(e)
            self.log_file_out('技术整改立即计算测试失败')

        time.sleep(20)
        try:
            tech_wei_cal.test_technology().tech(url, username, password, 1, '180', '200', '300', {'E03': ['2121', '2122']
                                                                                                  }, {'高压供电系统':'受电弓'}, time_sleep, wait_time)
        except Exception as e:
            print(e)
            self.log_file_out('修程修制立即计算测试失败')

        time.sleep(20)
        try:
            tech_fme_cal.Tech().tech_analysis(url,username,password,'里程','0','100',{'E05':['2091','2092']},{'高压供电系统': {'高压电缆、连接器及跳线': 'all'}
 },time_sleep,wait_time)
        except Exception as e:
            print(e)
            self.log_file_out('自动fmeca立即计算测试失败')



Run().run()

