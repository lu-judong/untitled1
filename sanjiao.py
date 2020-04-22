# l = []
# for i in range(1,101):
#     for j in range(1,101-i):
#         a = (i+1)*2**(i-2)+2**(i-1)*(j-1)
#         if a % 77 == 0:
#             l.append(a)
# print(len(l))
import datetime
def a(date):
    L = []
    mon_start = datetime.datetime.strptime(date[0], '%Y-%m-%d')

    while True:
        if  mon_start < datetime.datetime.strptime(date[1],'%Y-%m-%d'):
            if mon_start.month < 12 :
                L.append([mon_start, datetime.datetime(mon_start.year, mon_start.month + 1, 1)])
                mon_start = datetime.datetime(mon_start.year,mon_start.month + 1,1)
            else:
                mo = mon_start.year + 1
                L.append([mon_start, datetime.datetime(mo, 1, 1)])
                mon_start = datetime.datetime(mo,  1, 1)

        else:
            L[-1][-1] = datetime.datetime.strptime(date[1],'%Y-%m-%d')
            break
    return L




print(a(['2017-08-02','2017-10-01']))