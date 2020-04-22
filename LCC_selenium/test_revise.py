from bin.add_model_ratio import revise
from bin.add_model_repair import repair_revise
from config.config import url,username,password,log_file_out,logger,car,min_model
from config.menu_config import *

def run():
    # 运维费用统计
    # try:
    #     revise(url,username,password,openx_contents,'时间','测试02','2017-03-02','2017-10-03',car,10)
    #
    # except Exception as e:
    #     logger.error(e)
    #     log_file_out(openx_contents[0]+'修改验证失败')
    # # 通用模型
    # try:
    #     revise(url, username, password, common_contents, '时间', '2.27测试', '2017-03-02', '2017-10-03', car, 10)
    #
    # except Exception as e:
    #
    #     logger.error(e)
    #     log_file_out(common_contents[0]+'通用模型修改验证失败')

    # # 列车维度
    # try:
    #     revise(url, username, password, carload_ratio_contents, '时间', 'test_03', '2017-03-02', '2017-10-03', car, 10)
    # except Exception as e:
    #     logger.error(e)
    #     log_file_out(carload_ratio_contents[0]+carload_ratio_contents[1]+'修改验证失败')
    #
    # try:
    #     repair_revise(url, username, password, carload_compare_contents, 'test_03', '时间',min_model, 10)
    # except Exception as e:
    #     logger.error(e)
    #     log_file_out(carload_compare_contents[0]+carload_compare_contents[1]+'修改验证失败')

    # 路局维度
    # try:
    #     revise(url, username, password, railway_ratio_contents, '时间', 'test_03', '2017-03-02', '2017-10-03', car, 10)
    # except Exception as e:
    #     logger.error(e)
    #     log_file_out(railway_ratio_contents[0]+railway_ratio_contents[1]+'修改验证失败')

    # try:
    #     repair_revise(url, username, password, raliway_compare_contents, 'test_03', '时间', min_model, 10)
    # except Exception as e:
    #     logger.error(e)
    #     log_file_out(raliway_compare_contents[0]+raliway_compare_contents[1]+'修改验证失败')

    # # 维修级别维度
    # try:
    #     revise(url, username, password, senior_ratio_contents, '时间', '测试', '2017-03-02', '2017-10-03', car, 10)
    # except Exception as e:
    #     logger.error(e)
    #     log_file_out(senior_ratio_contents[0] + senior_ratio_contents[1] + '修改验证失败')

    # try:
    #     repair_revise(url, username, password, senior_ratio_contents, '测试', '时间', min_model, 10)
    # except Exception as e:
    #     logger.error(e)
    #     log_file_out(senior_compare_contents[0] + senior_compare_contents[1] + '修改验证失败')
    #
    # 供应商维度
    try:
        revise(url, username, password, supplier_ratio_contents, '时间', '测试', '2017-03-02', '2017-10-03', car, 10)
    except Exception as e:
        logger.error(e)
        log_file_out(supplier_ratio_contents[0] + supplier_ratio_contents[1] + '验证失败')

    try:
        repair_revise(url, username, password, supplier_ratio_contents, 'test_03', '时间', min_model, 10)
    except Exception as e:
        logger.error(e)
        log_file_out(supplier_compare_contents[0] + supplier_compare_contents[1] + '验证失败')
    # # 系统部件/系统维度
    # try:
    #     ratio_select_check(url, username, password, system_unit_ratio_contents, '测试', '测试', 4)
    # except Exception as e:
    #     logger.error(e)
    #     log_file_out(system_unit_ratio_contents[0] + system_unit_ratio_contents[1] + '修改验证失败')
    #
    # try:
    #     ratio_select_check(url, username, password, system_unit_compare_contents, 'test_03', 'test_03', 4)
    # except Exception as e:
    #     logger.error(e)
    #     log_file_out(system_unit_compare_contents[0] + system_unit_compare_contents[1] + '修改验证失败')
    # # 维修及维修保障维度/维修保障维度
    # try:
    #     ratio_select_check(url, username, password, repair_ratio_contents, '测试', '测试', 4)
    # except Exception as e:
    #     logger.error(e)
    #     log_file_out(repair_ratio_contents[0] + repair_ratio_contents[1] + '修改验证失败')
    #
    # try:
    #     ratio_select_check(url, username, password, raliway_compare_contents, 'test_03', 'test_03', 4)
    # except Exception as e:
    #     logger.error(e)
    #     log_file_out(raliway_compare_contents[0] + raliway_compare_contents[1] + '修改验证失败')

    # # 生产车间/生产线维度/产线维度
    # try:
    #     all_select_check(url, username, password, workshop_ratio_contents, '测试', '测试', 4)
    # except Exception as e:
    #     logger.error(e)
    #     log_file_out(workshop_ratio_contents[0] + workshop_ratio_contents[1] + '修改验证失败')
    #
    # try:
    #     all_select_check(url, username, password, workshop_compare_contents, '测试', '测试', 4)\
    #
    # except Exception as e:
    #     logger.error(e)
    #     log_file_out(workshop_compare_contents[0] + workshop_compare_contents[1] + '修改验证失败')
    # # 车型维度/车组维度
    # try:
    #     all_select_check(url, username, password, cartype_ratio_contents, '测试', '测试', 4)
    # except Exception as e:
    #     logger.error(e)
    #     log_file_out(cartype_ratio_contents[0] + cartype_ratio_contents[1] + '修改验证失败')
    #
    # try:
    #     all_select_check(url, username, password, cartype_compare_contents, 'test_03', 'test_03', 4)
    # except Exception as e:
    #     logger.error(e)
    #     log_file_out(cartype_compare_contents[0] + cartype_compare_contents[1] + '修改验证失败')





run()