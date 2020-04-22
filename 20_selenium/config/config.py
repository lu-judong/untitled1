import os

url = 'http://192.168.221.20:8083/darams/a?login'

username = 'admin'
password = 'admin'

path_dir= os.path.dirname(os.path.dirname(__file__)).replace('\\', '/')

path_dir1= os.path.dirname(os.path.dirname(__file__)).replace('/', '\\')

# 平均维修时间菜单
averageRepairtime_config = ['其他功能','平均维修时间']

# 不同平台对比
compare_config = ['运营数据统计分析系统','不同平台对比']

# 故障占比分析菜单
fault_config = ['运营数据统计分析系统','故障占比分析']

# 故障单菜单
faultNumber_config = ['基础数据','故障单信息']

# 自动FEMCA菜单
femca_config = ['运营数据统计分析系统', '自动FMECA']

# 内控模型配置菜单
incontrol_config = ['运营数据统计分析系统','内控模型配置']

# 维修数据维护
maintenanceDate_config = ['其他功能','维修数据维护']

# 维修性参数评估菜单
maintenanceParameter_config = ['其他功能','维修性参数评估']

# 最大维修时间菜单
maxRepairTime_config = ['其他功能','最大维修时间']

# nhpp模型管理菜单
nhpp_config = ['其他功能','NHPP模型']

# 自定义选车菜单
opTrainGroupCust_config = ['运营数据统计分析系统','自定义选车']

# RAMS指标评估菜单
rams_config = ['运营数据统计分析系统','RAMS指标评估']

# RAMS指标建模菜单
ramsSave_config = ['运营数据统计分析系统','产品RAMS指标统计评估']

# 可靠性增长计划菜单
ramsincreasePlan_config = ['其他功能','可靠性增长计划']

# 可靠性验证计划菜单
ramsTestPlan_config = ['其他功能','可靠性验证计划']

# 单一模型指标分析菜单
singelmodel_config = ['运营数据统计分析系统','单一模型指标分析']

# 技术变更效果评估菜单
tech_config = ['运营数据统计分析系统','技术变更效果评估']

# 修程修制优化分析菜单
maintain_config = ['运营数据统计分析系统','修程修制优化分析']