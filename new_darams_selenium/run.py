from config.menu_config import *
from bin.all_add_model_check import *
from bin.chech_bug_new import *
from bin.not_save_model_check import *

def run():
    f = open('usecase.txt', "r+")

    f.truncate()

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
    # repair_notsave_model_check(url,username,password,repair_title,target_of_evaluation,repair_mileage,car,fault_pattern,select_fault,check_fault,wait_time)

    # try:
    #     technical_change_add_check(url,username,password,tech_title,modelName,target_of_evaluation,remarks,tech_select,tech_change,speed,car,fault_pattern,select_fault,wait_time)
    # except:
    #     log_file_out(tech_title[1] + '验证失败')
    # technical_nosave_model_check(url, username, password, tech_title, target_of_evaluation, select, tech_change, car,fault_pattern, select_fault, wait_time)
    # try:
    #     singelmodel_add_check(url,username,password,singelModel_title,modelName,target_of_evaluation,remarks,select,mileage_start,mileage_end,speed,car,fault_pattern,select_fault,wait_time)
    # except:
    #     log_file_out(singelModel_title[1] + '验证失败')
    # try:
    #     compare_add_check(url, username, password, more_model_title, modelName, target_of_evaluation, remarks, '时间', min_model, '并集',wait_time)
    # except:
    #     log_file_out(more_model_title[1] + '验证失败')

    # compare_nosave_model_check(url, username, password, more_model_title, target_of_evaluation, '时间', min_model, '并集',wait_time)

    # try:
    #     fmcea_add_check(url,username,password,femca_title,'3.7测试',remarks,select,mileage_start,mileage_end,car,fault_pattern,select_fault,check_fault,wait_time)
    # except:
    #     log_file_out(femca_title[1] + '验证失败')
    # fmcea_notsave_check(url,username,password,femca_title,select,mileage_start,mileage_end,car,fault_pattern,select_fault,check_fault,wait_time)
    # try:
    #     fault_ratio_add_check(url,username,password,fault_title,modelName,target_of_evaluation,remarks,select,mileage_start,mileage_end,car,fault_pattern,select_fault,check_fault,wait_time)
    # except:
    #     log_file_out(fault_title[1] + '验证失败')
    #
    # try:
    #     nhpp_add_check(url, username, password, nhpp_title, modelName, '11', time_start, time_end, car)
    # except:
    #     log_file_out(nhpp_title[1] + '验证失败')
    # nhpp_notsave_check(url,username,password,nhpp_title,time_start,time_end,car)
    # try:
    #     rcma_add_check(url,username,password,rcma_title,modelName,'11',remarks,'0.2','0.3',10, 20,200)
    # except:
    #     log_file_out(rcma_title[1] + '验证失败')
    # try:
    #     main_parameter_evaluation_check('0226', url, username, password, main_parameter_title)
    # except:
    #     log_file_out(main_parameter_title[1] + '验证失败')
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
    #     mttr_add_check(url,username,password,mttr_contents,'X1)
    # except:
    #     log_file_out(mttr_contents[1] + '验证失败')
    # try:
    #     max_repair_time_check(url,username,password,max_repair_time_title,'X1')
    # except:
    #     log_file_out(max_repair_time_title + '验证失败')
    # try:
    #     taaf_add_check(url,username,password,taaf_contents)
    # except:
    #     log_file_out(taaf_contents[1] + '验证失败')
    # try:
    #     train_fault_information_check(url, username, password, train_fault_information_title, '时间', time_start, time_end, '原因002', car, 1,fault_pattern)
    # except:
    #     log_file_out(train_fault_information_title[1] + '验证失败')

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
    # try:
    #     maintenance_data_maintenance(url, username, password, main_data_title, main_data_modelCode, main_data_modelName, remarks, line, main_data_l)
    # except:
    #     log_file_out(main_data_title[1] + '验证失败')
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

    # project_home_model(url,username,password,'')
    produce_home_page(url,username,password,'',['模型评估值总览','系统部件维度','车型维度','线路路局维度','多模型对比维度'],'一个模型',['FPMK','FPMH','FIT','FPY'],['E27','E28'],['测试26','测试42'],['对比','测试42'])
run()