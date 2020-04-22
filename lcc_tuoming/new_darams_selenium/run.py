from config.menu_config import *
from bin.all_add_model_check import *
from bin.chech_bug_new import *


# try:
#     rams_add_check(url,username,password,rams_title,modelName,target_of_evaluation,remarks,select,start,end,speed,check_car,car,fault_pattern,select_fault,check_fault,wait_time)
#
# except:
#     log_file_out(rams_title[1]+'验证失败')
#
# try:
#     rams_cal_check(url,username,password,rams_cal_title,target_of_evaluation,speed,'时间','2017-02-03','2017-10-20',car,fault_pattern,select_fault,wait_time)
# except:
#     log_file_out(rams_cal_title[1] + '验证失败')
# try:
#     incontrol_add_check(url,username,password,incontrol_title,modelName,incontrol_start,incontrol_end,remarks,car,wait_time)
# except:
#     log_file_out(incontrol_title[1] + '验证失败')
#
# try:
#     repair_add_check(url,username,password,repair_title,modelName,target_of_evaluation,remarks,repair_mileage,car,fault_pattern,select_fault,check_fault,wait_time)
# except:
#     log_file_out(repair_title[1] + '验证失败')
# try:
#     technical_change_add_check(url,username,password,tech_title,modelName,target_of_evaluation,remarks,tech_select,tech_change,speed,car,fault_pattern,select_fault,wait_time)
# except:
#     log_file_out(tech_title[1] + '验证失败')
# try:
#     fmcea_add_check(url,username,password,femca_title,'3.7测试',remarks,select,start,end,car,fault_pattern,select_fault,check_fault,wait_time)
# except:
#     log_file_out(femca_title[1] + '验证失败')
#
# try:
#     nhpp_add_chekc(url,username,password,nhpp_title,'1')
# except:
#     log_file_out(nhpp_title[1] + '验证失败')
# try:
#     rcma_add_check(url,username,password,rcma_title,modelName,'11',remarks,'0.2','0.3',10, 20,200)
# except:
#     log_file_out(rcma_title[1] + '验证失败')
# try:
#     custom_car_add_check(url,username,password,custom_car_selection,'1',car)
# except:
#     log_file_out(custom_car_selection[1] + '验证失败')
# try:
#     operation_maintenance_data_cleaning_chcek(url,username,password,operation_maintenance_data_cleaning)
# except:
#     log_file_out(operation_maintenance_data_cleaning[1] + '验证失败')
# try:
#     mtbf_check(url,username,password,mtbf_contents,'0.2','0.2','0.2','0.2')
# except:
#     log_file_out(mtbf_contents[1] + '验证失败')
# try:
#     mttr_add_check('X1',url,username,password,mttr_contents)
# except:
#     log_file_out(mttr_contents[1] + '验证失败')
# try:
#     taaf_add_check(url,username,password,taaf_contents)
# except:
#     log_file_out(taaf_contents[1] + '验证失败')
#
# try:
#     intelligent_fault_analysis_check(url,username,password,intelligent_fault_analysis,'2017-02-03','2018-02-03','0.2')
# except:
#     log_file_out(intelligent_fault_analysis[1] + '验证失败')
#
# try:
#     intelligent_fault_identification_check(url,username,password,intelligent_fault_identification,'18型车','186431')
# except:
#     log_file_out(intelligent_fault_identification[1] + '验证失败')
# try:
#     rams_index_tracking(url,username,password,rams_index_tracking_title,'测试55')
# except:
#     log_file_out(rams_index_tracking_title[1] + '验证失败')
#
# # 验证选择9型车是否会出现其他车型部件
# try:
#     rams_bug_nm1(url,username,password,rams_title,{'9型车':'all'},{'9型车':{'部件000250':'all'}})
# except:
#     log_file_out('验证选择9型车是否会出现其他车得部件失败')
# try:
#     more_model_bug(url,username,password,more_model_title,'故障对比',car,{'17型车':{'部件000250':'all'}})
# except:
#     log_file_out('验证指标对比分袖修改失败')
# try:
#     technical_bug(url,username,password,tech_title,'11')
# except:
#     log_file_out('验证技术变更报表失败')
# try:
#     paging_bug(url,username,password,rams_title,'a')
# except:
#     log_file_out('验证分页是否重置失败')
# try:
#     median_check(url, username, password, rams_title, '重点问题追踪')
# except:
#     log_file_out('验证中间值失败')

project_home_model(url,username,password,'')