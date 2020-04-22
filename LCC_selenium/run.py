from LCC_selenium.bin.add_model_ratio import *
from config.config import url,username,password,log_file_out,logger
from config.menu_config import *
from bin.check_new_bug import *
from bin.add_model_repair import *
from bin.homemodel_check import *
def run():
    f = open('usecase.txt', "r+")

    f.truncate()
    # # 运维费用统计
    # try:
    #     add(url, username, password, openx_contents, modelName, modelCode, remarks, '新建', '里程', mileage_start, mileage_end,  12, 100012, car, repairlocation, supplier, wait_time)
    #
    # except Exception as e:
    #     logger.error(e)
    #     log_file_out(openx_contents[0]+'验证失败')
    # try:
    #     check_ratio_customize_traingroup(url, username, password, openx_contents, modelName, modelCode, remarks, '新建', '时间', time_start, time_end, '179183', '测试1')
    #
    # except Exception as e:
    #     logger.error(e)
    #     log_file_out('占比功能导入自定义车组验证失败')
    #
    # # 列车对比
    # try:
    #     repair_add_model(url,username,password,carload_ratio_contents,modelCode,modelName,remarks,'新建','时间',min_model,wait_time)
    # except Exception as e:
    #         logger.error(e)
    #         log_file_out(carload_ratio_contents[1]+'新增验证失败')
    # # 通用模型
    # try:
    #     add(url, username, password, common_contents, modelName, modelCode, remarks, '新建', '时间', time_start, time_end,  12, 100012, car, repairlocation, supplier, wait_time)
    # except Exception as e:
    #     logger.error(e)
    #     log_file_out(common_contents[0]+'验证失败')
    # # 自定义选车
    # try:
    #     customize_train(url,username,password,customize_train_contents,car,'11')
    # except Exception as e:
    #     logger.error(e)
    #     log_file_out(customize_train_contents[0]+'验证失败')
    # #对比功能的导入自定义选车
    # try:
    #     check_repair_customize_traingroup(url, username, password, carload_compare_contents, modelName, modelCode, remarks, '时间',customize_min_model, '179183', '测试1', 12, 100012)
    # except Exception as e:
    #     logger.error(e)
    #     log_file_out(carload_compare_contents[0] + '对比分析导入自定义车组验证失败')
    # try:
    #     check_user_system(url, username, password, user_system_settings, openx_contents)
    # except Exception as e:
    #     logger.error(e)
    #     log_file_out(user_system_settings[0] + '修改配置验证失败')

    # home_model(url, username, password)
    produce_home_page(url, username, password, ['LCC总览数据', '系统部件维度', '车型维度', '运维检修维度', '多模型对比维度'], '测试', ['E27', 'E28'], ['测试413', '测试42'], ['测试42', '测试413'])

run()