
from config.config import url,username,password,log_file_out,logger
from config.menu_config import *
from bin.test_ratio_picture import *
from bin.test_compare_picture import *

def run():

    # 通用模型
    try:
        common_model_picture(url, username, password, common_contents, '2.27测试',common_model_tabs)

    except Exception as e:
        logger.error(e)
        log_file_out(openx_contents[0]+'验证失败')
    try:
        carload_ratio_picture(url,username,password,carload_ratio_contents,'test_03')

    except Exception as e:
        logger.error(e)
        log_file_out(carload_ratio_contents[0]+'验证失败')
    try:
        cartype_ratio_picture(url, username, password, cartype_ratio_contents, '测试')
    except Exception as e:
        logger.error(e)
        log_file_out(cartype_ratio_contents[0]+'验证失败')
    # 维修维保维度
    try:
        repair_ratio_picture(url, username, password, repair_ratio_contents, '测试')
    except Exception as e:
        logger.error(e)
        log_file_out(repair_ratio_contents[0]+'验证失败')
    # 路局维度
    try:
        railway_ratio_picture(url, username, password, railway_ratio_contents, '测试')
    except Exception as e:
        logger.error(e)
        log_file_out(railway_ratio_contents[0] + '验证失败')
    # 系统部件维度
    try:
        system_unit_ratio_picture(url, username, password, system_unit_ratio_contents, '测试')
    except Exception as e:
        logger.error(e)
        log_file_out(system_unit_ratio_contents[0] + '验证失败')
    # 生产车间维度
    try:
        workshop_ratio_picture(url, username, password, workshop_ratio_contents, '测试')
    except Exception as e:
        logger.error(e)
        log_file_out(workshop_ratio_contents[0] + '验证失败')
    # 高级修维度
    try:
        high_repair_ratio_picture(url, username, password, senior_ratio_contents, '测试')
    except Exception as e:
        logger.error(e)
        log_file_out(senior_ratio_contents[0] + '验证失败')
    # 整车维度
    try:
        carload_compare_picture(url, username, password, carload_compare_contents, 'test_03')
    except Exception as e:
        logger.error(e)
        log_file_out(carload_compare_contents[0] + '验证失败')
    # 车型维度
    try:
        cartype_compare_picture(url, username, password, cartype_compare_contents, 'test_03')
    except Exception as e:
        logger.error(e)
        log_file_out(cartype_compare_contents[0] + '验证失败')
    # 维修保障维度
    try:
        repair_compare_picture(url, username, password, repair_compare_contents, 'test_03')
    except Exception as e:
        logger.error(e)
        log_file_out(repair_compare_contents[0] + '验证失败')
    # 路局维度
    try:
        railway_compare_picture(url, username, password, raliway_compare_contents, 'test_03')
    except Exception as e:
        logger.error(e)
        log_file_out(raliway_compare_contents[0] + '验证失败')
    # 系统部件对比
    try:
        system_unit_compare_picture(url, username, password, system_unit_compare_contents, 'test_03')
    except Exception as e:
        logger.error(e)
        log_file_out(system_unit_compare_contents[0]+'验证失败')
    # 供应商维度对比
    try:
        supplier_compare_picture(url, username, password, supplier_compare_contents, 'test_03')
    except Exception as e:
        logger.error(e)
        log_file_out(supplier_compare_contents[0] + '验证失败')
    # 生产车间维度对比
    try:
        workshop_compare_picture(url, username, password, workshop_compare_contents, '测试')
    except Exception as e:
        logger.error(e)
        log_file_out(workshop_compare_contents[0] + '验证失败')
    # 高级修维度对比
    try:
        high_repair_compare_picture(url, username, password, senior_compare_contents, '测试')
    except Exception as e:
        logger.error(e)
        log_file_out(senior_compare_contents[0] + '验证失败')

run()