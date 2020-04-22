# import numpy as np
# t_1 = ((1,2,3,4),(10,2,30,40),(100,2,300,400),(1000,2000,3000,4000))
# l_1 = np.array(t_1)
# print(l_1)
# l_2 = l_1.T
# print(l_2)
#
# l_3 = list(set(l_2[1]))
# print(l_3)
# d_1 = dict()
# for i in l_3:
#     d_1[i] = 0
#     for j in l_1:
#         if j[1] == i:
#             d_1[i] += j[2]
# print(d_1)
a = {1:2}
L = []
L.append(a)
b = {1:3}
L.append(b)
c = a
for i in b:
    if i in c:
        c[i] += b[i]
L.append(c)
print(L)

