jquery_str = ""
try:
    f = open('../config/jquery-3.4.1.min.js','r',encoding='utf-8')
    line = f.readline()
    while line:
        jquery_str +=  line
        line = f.readline()
except:
    print('打开jquery失败')

print(jquery_str)
