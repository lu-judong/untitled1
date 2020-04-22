import logging

#日志配置
LOG_CONFIG = {
'level':logging.DEBUG,#日志文件日志级别
'format':'%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
'datefmt':'%Y-%m-%d %H:%M:%S',
'filename':'logging.log',
'filemode':'w+'
}
logging.basicConfig(**LOG_CONFIG)

#################################################################################################
# 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)#控制台日志级别
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)

logger = logging.getLogger('')
logger.addHandler(console)

