# import time
#
# import paramiko
#
#
# # 服务器地址
# host = '192.168.1.20'
# # 服务器账号
# user = 'Administrator'
# # 服务器密码
# password = 'zaq12wsx.'
#
#
# client = paramiko.SSHClient()
# client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# client.connect(host, 22, username=user, password=password, timeout=10)
#
# # 服务器上传默认地址
# remote_default_path = 'F:\\Users\\Administrator'
#
# time.sleep(2)
# stdin, stdout, stderr = client.exec_command(
#     'cmd /c type {}\\1.txt'.format(remote_default_path))
# content = stdout.read().decode('gbk')
# print(content)
# remote_size = int(content.split('\r\n')[-3].split(' ')[-2].replace(',',''))
# print(remote_size)

# L = [[{'1':1,'2':2},{'3':3,'4':4,'5':5}],[{'1':1,'2':2},{'3':3,'4':4}]]
# d1 = []
# for i in range(0,len(L)):
#     if i == 0:
#         d1 = L[0]
#     else:
#         for j in L[i]:
#             for k in j.keys():
#                 if k in d1[L[i].index(j)].keys():
#                     d1[L[i].index(j)][k] += L[i][L[i].index(j)][k]
#                 else:
#                     d1[L[i].index(j)][k] =  L[i][L[i].index(j)][k]
# 
# 
# print(d1)
# import numpy
#
# d = {'2651': '武汉铁路局', '2216': '南昌铁路局', '2202': '南昌铁路局'}
# d1 = {'2651': (('(空白)', 206250, 1522350.0000, 250), ('3',5013420, 4281790, 2608), ('4', 2482400.0000, 2014, 3103)), '2216': (('(空白)', 1099630, 1913, 899), ('3', 8087400, 151100, 1072), ('4', 4800, 1800, 12)),'2202':
#     (('(空白)', 1, 1, 1),('4', 1, 1, 1))}
# d2 = {}
# for nm in d:
#     for nm1 in d1:
#         if nm == nm1:
#             if d[nm] in d2.keys():
#                 a = d1[nm1]
#                 b = d2[d[nm]] +a
#                 d2[d[nm]] = b
#             else:
#                 d2[d[nm]] = d1[nm1]
# print(d2)
# d3 = {}
#
#
# for k in d2:
#     L0 = []
#     num = 1
#     for k1 in range(3):
#         l_re = numpy.array(d2[k])
#         # print(l_re)
#         l_re1 = l_re.T
#         l_re2 = list(set(l_re1[0]))
#         d_1 = dict()
#         for i in l_re2:
#             d_1[i] = 0
#             for j in l_re:
#                 if j[0] == i:
#                     d_1[i] += float(j[num])
#
#         L0.append(d_1)
#         num += 1
#     d3[k] = L0
# print(d3)

a = 'a' + '\n' +  'b'

print(a)