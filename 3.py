# import json
#
# from config.config import *
# def log_file_out(msg):
#     fo = open(r'{}/usecase.txt'.format(path_dir), mode='a', encoding='utf-8')
#     fo.write(msg)
#     fo.close()
#
# def a():
#     p = ''
#     data = {
#         'errorMsg': [],
#         'errorCode': [],
#         'result': 'success'
#     }
#     p += json.dumps(data) + '\n'
#     p += '2' + '\n'
#     p += '1' + '\n'
#     p += '2' + '\n'
#     log_file_out(p)
#
# def b():
#     try:
#         fo = open(r'{}/usecase.txt'.format(path_dir), mode='w', encoding='utf-8', )
#         fo.truncate()
#         fo.close()
#         print('1')
#         return True
#
#     except:
#         return False
#
# def c():
#     L = []
#     for line in open(r'{}/usecase.txt'.format(path_dir),encoding='utf-8'):
#         L.append(line)
#     for i in L:
#         print(i)
#
# if __name__ == '__main__':
#     b()

# import sympy
# import datetime
# a = (datetime.datetime(2018,2,1)-datetime.datetime(2018, 1, 31, 23, 8, 25)).total_seconds()
# print(a)
# b = (datetime.datetime(2018,2,1)-datetime.datetime(2018, 2, 1, 23, 14, 26)).total_seconds()
# print(b)
# x = sympy.symbols("x")
# # c = sympy.solve([(2117670-x)/(2119408-2117670)-(3095)/(83666-3095)],[x])
# c = sympy.solve([(2128674-x)/(2127272-2128674)-(1730788/1817252-1730788)],[x])
# print(c)
# L = [{'工时': [{'E27': 4254966}, {'E27': 42549.66}]}, {'物料': [{'E27': 107439.45}, {'E27': 12378135}]},{'工时': [{'E27': 4254966}, {'E27': 42549.66}]}, {'物料': [{'E27': 107439.45}, {'E27': 12378135}]},{'工时': [{'E28': 18635}, {'E28': 1863}]}, {'物料': [{'E28': 312}, {'E28': 206}]},{'工时': [{'E28': 18635}, {'E28': 1863}]}, {'物料': [{'E28': 312}, {'E28': 206}]}]
#
# d = {'工时':[],'物料':[]}
#
# for i in L:
#     a = '工时'
#     if '物料' in i.keys():
#         a = '物料'
#     if i[a].__len__() == 0:
#         pass
#     else:
#         if d[a].__len__() == 0:
#             d.update({a: i[a]})
#         else:
#             for j in i[a]:
#                 for k in j:
#                     num = i[a].index(j)
#                     for k1 in d[a]:
#                         if k in k1.keys():
#                             index = [key for key, value in enumerate(d[a]) if k in value.keys()]
#                             if num == 0:
#                                 d[a][index[0]][k] += i[a][0][k]
#                             else:
#
#                                 d[a][index[1]][k] += i[a][1][k]
#                         else:
#                             d[a].append(j)
# print(d)
            # d[a][i[a].index(k)][k1] += i[a][i[a].index(k)][k1]
            # else:
            #     # d[a][k1] = i[a][i[a].index(k)][k1]
            #     d.update({a: {k1:i[a]}})

# Manhour = {'E28': {'3': 1365700.0000, '4': 4800.0000, 'None': 493070.0000}, 'E27': {'3': 2185330.0000, '4': 828000.0000, 'None': 69710.0000}}
# Materia = {'E28': {'3': 302200.0, '4': 3600.0000, 'None': 3826100.0000}, 'E27': {'3': 8563580.0000, '4': 4029649.0000, 'None': 3044700.0000}}
# L_sum = Manhour
#
# for i in Materia:
#     if i in L_sum.keys():
#         for l in Materia[i]:
#             if l in L_sum[i].keys():
#                 L_sum[i][l] += Materia[i][l]
#             else:
#                 L_sum[i][l] = Materia[i][l]
#     else:
#         L_sum[i] = Materia[i]
# print(L_sum)
def deal_obj(obj,num):
    for key,value in obj.items():
        if type(value).__name__ == 'dict':

            num = deal_obj(value,num+1)
        else:
            num = num + 1
    return num
#
# a = [{1:{2:{5:{3:4}}}},{1:2}]
# for i in a:
#     num = deal_obj(i,0)
#     print(num)
# lines = [(1, 1, '父1节点'), (2, 1, '1-2'), (3, 1, '1-3'), (4, 3, '1-3-4'), (5, 3, '1-3-5'), (6, 3, '1-3-6'),
#      (7, 7, '父7节点'), (8, 7, '7-8'), (9, 7, '7-9')]
#
# nodes = {}
# data_temp =[]
# for line in lines:
#     id, parentId, name = line
#     nodes[id] = {'children': [], 'id': id, "parentId": parentId, "name": name, 'orLeafnode': '1'} # orLeafnode 是叶子节点
#     data_temp.append({'children': [], 'id': id, "parentId": parentId, "name": name, 'orLeafnode': '1'})
# data = []
# for i in data_temp:
#     id = i['id']
#     parent_id = i['parentId']
#     node = nodes[id]
#     if id == parent_id:
#         node['orLeafnode'] = '0'
#         data.append(node)
#     else:
#         parent = nodes[parent_id]
#         parent['orLeafnode'] = '0'
#         parent['children'].append(node)
# print(data)

