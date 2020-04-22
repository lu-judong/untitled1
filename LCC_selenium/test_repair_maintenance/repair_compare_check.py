import copy
import datetime
from decimal import Decimal

import numpy
import pymysql

class Check:
    def lcc(self, sql):
        # db = pymysql.connect("192.168.221.24", "root", "123456", port=23306,charset="utf8")
        db = pymysql.connect("192.168.221.21", "root", "123456", charset="utf8")
        cur = db.cursor()
        cur.execute("use lcc")
        cur.execute(sql)
        a = cur.fetchall()
        return a

    def main(self, car, date):
        L1 = []

        date[0] = datetime.datetime.strftime(date[0],'%Y-%m-%d %H:%M:%S')

        # if len(date[1]) <= 12:
        #     date[1] = date[1] + ' 23:59:59'
        date[1] = datetime.datetime.strftime(date[1],'%Y-%m-%d %H:%M:%S')


        for i in car:
            for j in car[i]:
                L1.append(j)
        if len(L1) <= 1:
            I_SQL = 'AND h.train_no = {}'.format(L1[0])
        else:
            L1 = tuple(L1)
            I_SQL = 'AND h.train_no in {}'.format(L1)

        sql = '''
              select 
              d.material_category AS 'category',
              h.work_order_no as 'work_order',
              te.duration * b.team_price AS "manhour_money"
              from 
              op_work_order_header h
              LEFT JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
              LEFT JOIN op_work_order_team te on te.work_order_no = h.work_order_no
              LEFT JOIN cd_team_base b on b.team_name = te.team_name
              WHERE h.report_work_status != '已取消'          
              {}
              AND h.plan_begin_date >= '{}'      
              AND h.plan_begin_date < '{}'
              '''.format(I_SQL, date[0], date[1])

        re = self.lcc(sql)
        Manhour = {}
        if re.__len__() == 0:
            Manhour = {}
        else:
            l_re = numpy.array(re)
            l_re1 = l_re.T
            l_re2 = list(set(l_re1[1]))
            d = {}
            l_re3 = list(set(l_re1[0]))

            for i in l_re3:
                if i == '0':
                    Manhour['工具'] = {}
                elif i == '1':
                    Manhour['耗材'] = {}
                elif i == '2':
                    Manhour['备件'] = {}
                else:
                    Manhour['空白'] = {}

            for i in l_re2:
                if i is None:
                    pass
                else:
                    d[i] = {}
                    for j in l_re:
                        if j[1] == i:
                            if j[0] not in ['1','2','0']:
                                if '空白' in d[i].keys():
                                    d[i]['空白'] += 1
                                else:
                                    d[i]['空白'] = 1
                            else:
                                if j[0] in d[i].keys():
                                    d[i][j[0]] += 1
                                else:
                                    d[i][j[0]] = 1
            # print(d)
            d1 = {}
            for i in d:
                d1[i] = 0
                for j in d[i]:
                    d1[i] += d[i][j]
            # print(d1)

            for j in l_re:
                if j[1] is None or j[2] is None:
                    pass
                else:
                    if j[0] == '0':
                        if j[1] in Manhour['工具'].keys():
                            pass
                        else:
                            Manhour['工具'][j[1]] = float(j[2]) * (d[j[1]][j[0]] / d1[j[1]])
                    elif j[0] == '1':
                        if j[1] in Manhour['耗材'].keys():
                            pass
                        else:
                            Manhour['耗材'][j[1]] = float(j[2]) * (d[j[1]][j[0]] / d1[j[1]])
                    elif j[0] == '2':
                        if j[1] in Manhour['备件'].keys():
                            pass
                        else:
                            Manhour['备件'][j[1]] = float(j[2]) * (d[j[1]][j[0]] / d1[j[1]])
                    else:
                        if j[1] in Manhour['空白'].keys():
                            pass
                        else:
                            Manhour['空白'][j[1]] = float(j[2]) * (d[j[1]]['空白'] / d1[j[1]])

            # print(Manhour)
        Manhour_new = {}
        for i in Manhour:
            Manhour_new[i] = 0
            for j in Manhour[i]:
                Manhour_new[i] += Manhour[i][j]
        # print(Manhour_new)

        # print(Manhour)

        sql1 = '''
                   select 
                   d.material_category AS 'category',
                   IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)* IF(d.material_deal_type = '出库', d.material_quantity, 0) AS "material_money"
                   from op_work_order_header h 
                   INNER JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
                   LEFT JOIN cd_materials_base e ON d.material_no = e.material_no
                   LEFT JOIN cd_materials_batch t ON d.material_no = t.material_no AND d.batch_no = t.batch_no
                   LEFT JOIN cd_materials_serial s ON d.material_no = s.material_no AND d.batch_no = s.batch_no AND d.serial_no = s.serial_no
                   WHERE h.report_work_status != '已取消'          
                   {}
                   AND h.plan_begin_date >= '{}'      
                   AND h.plan_begin_date < '{}'
                  '''.format(I_SQL, date[0], date[1])

        re1 = self.lcc(sql1)
        Material = {}
        if re.__len__() == 0:
            Material = {}
        else:
            l_re = numpy.array(re1)

            for j in l_re:
                if j[1] is None:
                    pass
                else:
                    if j[0] == '0':
                        if '工具' in Material.keys():
                            Material['工具'] += j[1]
                        else:
                            Material['工具'] = j[1]
                    elif j[0] == '1':
                        if '耗材' in Material.keys():
                            Material['耗材'] += j[1]
                        else:
                            Material['耗材'] = j[1]
                    elif j[0] == '2':
                        if '备件' in Material.keys():
                            Material['备件'] += j[1]
                        else:
                            Material['备件'] = j[1]
                    else:
                        if '空白' in Material.keys():
                            Material['空白'] += j[1]
                        else:
                            Material['空白'] = j[1]

        # print(Material)
        d_sum = copy.deepcopy(Manhour_new)
        for i in Material:
            if i in d_sum.keys():
                d_sum[i] += float(Material[i])
            else:
                d_sum[i] = float(Material[i])

        L1  = []
        # L1.append(Manhour_new)
        # L1.append(Material)
        L1.append(d_sum)
        return L1

    def main1(self, car, date):
        L1 = []
        # if len(date[0]) <= 12:
        #     date[0] = date[0] + ' 00:00:00'
        # # if len(date[1]) <= 12:
        # #     date[1] = date[1] + ' 23:59:59'
        # date[1] = date[1] + ' 00:00:00'
        date[0] = datetime.datetime.strftime(date[0], '%Y-%m-%d %H:%M:%S')

        # if len(date[1]) <= 12:
        #     date[1] = date[1] + ' 23:59:59'
        date[1] = datetime.datetime.strftime(date[1], '%Y-%m-%d %H:%M:%S')

        for i in car:
            for j in car[i]:
                L1.append(j)
        if len(L1) <= 1:
            I_SQL = 'AND h.train_no = {}'.format(L1[0])
        else:
            L1 = tuple(L1)
            I_SQL = 'AND h.train_no in {}'.format(L1)

        sql = '''
                  select 
                  d.material_category AS 'category',
                  h.work_order_no as 'work_order',
                  h.fault_no AS 'fault_no',
                  te.duration * b.team_price AS "manhour_money"
                  from 
                  op_work_order_header h
                  LEFT JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
                  LEFT JOIN op_work_order_team te on te.work_order_no = h.work_order_no
                  LEFT JOIN cd_team_base b on b.team_name = te.team_name
                  WHERE h.report_work_status != '已取消'          
                  {}
                  AND h.plan_begin_date >= '{}'      
                  AND h.plan_begin_date < '{}'
                  '''.format(I_SQL, date[0], date[1])

        re = self.lcc(sql)
        Manhour = {}
        if re.__len__() == 0:
            Manhour = {}
        else:
            l_re = numpy.array(re)
            l_re1 = l_re.T
            l_re2 = list(set(l_re1[0]))
            l_re3 = list(set(l_re1[1]))

            for i in l_re2:
                if i == '0':
                    Manhour['工具'] = {}
                elif i == '1':
                    Manhour['耗材'] = {}
                elif i == '2':
                    Manhour['备件'] = {}
                else:
                    Manhour['空白'] = {}
            d = {}
            for i in l_re3:
                if i is None:
                    pass
                else:
                    d[i] = {}
                    for j in l_re:
                        if j[1] == i:
                            if j[0] not in ['1', '2', '0']:
                                if '空白' in d[i].keys():
                                    d[i]['空白'] += 1
                                else:
                                    d[i]['空白'] = 1
                            else:
                                if j[0] in d[i].keys():
                                    d[i][j[0]] += 1
                                else:
                                    d[i][j[0]] = 1
            # print(d)

            d1 = {}
            for i in d:
                d1[i] = 0
                for j in d[i]:
                    d1[i] += d[i][j]

            L2 = []
            L3 = []
            L4 = []
            L5 = []
            L6 = []
            L7 = []
            L8 = []
            for j in l_re:
                if j[1] is None or j[3] is None:
                    pass
                else:
                    if j[0] == '0':
                        if j[2] is not None:
                            if '修复性费用' in Manhour['工具'].keys():
                                if j[1] in L2:
                                    pass
                                else:
                                    Manhour['工具']['修复性费用'] += j[3] * Decimal(d[j[1]][j[0]] / d1[j[1]])
                                    L2.append(j[1])
                            else:
                                Manhour['工具']['修复性费用'] = j[3] * Decimal(d[j[1]][j[0]] / d1[j[1]])
                                L2.append(j[1])
                        else:
                            if '预防性费用' in Manhour['工具'].keys():
                                if j[1] in L3:
                                    pass
                                else:
                                    Manhour['工具']['预防性费用'] += j[3] * Decimal(d[j[1]][j[0]] / d1[j[1]])
                                    L3.append(j[1])
                            else:
                                Manhour['工具']['预防性费用'] = j[3] * Decimal(d[j[1]][j[0]] / d1[j[1]])
                                L3.append(j[1])
                    elif j[0] == '1':
                        if j[2] is not None:
                            if '修复性费用' in Manhour['耗材'].keys():
                                if j[1] in L4:
                                    pass
                                else:
                                    Manhour['耗材']['修复性费用'] += j[3] * Decimal(d[j[1]][j[0]] / d1[j[1]])
                                    L4.append(j[1])
                            else:
                                Manhour['耗材']['修复性费用'] = j[3] * Decimal(d[j[1]][j[0]] / d1[j[1]])
                                L4.append(j[1])
                        else:
                            if '预防性费用' in Manhour['耗材'].keys():
                                if j[1] in L5:
                                    pass
                                else:
                                    Manhour['耗材']['预防性费用'] += j[3] * Decimal(d[j[1]][j[0]] / d1[j[1]])
                                    L5.append(j[1])
                            else:
                                Manhour['耗材']['预防性费用'] = j[3] * Decimal(d[j[1]][j[0]] / d1[j[1]])
                                L5.append(j[1])
                    elif j[0] == '2':
                        if j[2] is not None:
                            if '修复性费用' in Manhour['备件'].keys():
                                if j[1] in L6:
                                    pass
                                else:
                                    Manhour['备件']['修复性费用'] += j[3] * Decimal(d[j[1]][j[0]] / d1[j[1]])
                                    L6.append(j[1])
                            else:
                                Manhour['备件']['修复性费用'] = j[3] * Decimal(d[j[1]][j[0]] / d1[j[1]])
                                L6.append(j[1])
                        else:
                            if '预防性费用' in Manhour['备件'].keys():
                                if j[1] in L7:
                                    pass
                                else:
                                    Manhour['备件']['预防性费用'] += j[3] * Decimal(d[j[1]][j[0]] / d1[j[1]])
                                    L7.append(j[1])
                            else:
                                Manhour['备件']['预防性费用'] = j[3] * Decimal(d[j[1]][j[0]] / d1[j[1]])
                                L7.append(j[1])
                    else:
                        if j[2] is not None:
                            if '修复性费用' in Manhour['空白'].keys():
                                if j[1] in L8:
                                    pass
                                else:
                                    Manhour['空白']['修复性费用'] += j[3] * Decimal(d[j[1]]['空白'] / d1[j[1]])
                                    L8.append(j[1])
                            else:
                                Manhour['备件']['修复性费用'] = j[3] * Decimal(d[j[1]]['空白'] / d1[j[1]])
                                L8.append(j[1])
                        else:
                            if '预防性费用' in Manhour['空白'].keys():
                                if j[1] in L8:
                                    pass
                                else:
                                    Manhour['空白']['预防性费用'] += j[3] * Decimal(d[j[1]]['空白'] / d1[j[1]])
                                    L8.append(j[1])
                            else:
                                Manhour['空白']['预防性费用'] = j[3] * Decimal(d[j[1]]['空白'] / d1[j[1]])
                                L8.append(j[1])


        # print(Manhour)

        sql1 = '''
                   select 
                   d.material_category AS 'category',
                   h.fault_no AS 'fault_no',
                   IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)* IF(d.material_deal_type = '出库', d.material_quantity, 0) AS "material_money"
                   from op_work_order_header h 
                   INNER JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
                   LEFT JOIN cd_materials_base e ON d.material_no = e.material_no
                   LEFT JOIN cd_materials_batch t ON d.material_no = t.material_no AND d.batch_no = t.batch_no
                   LEFT JOIN cd_materials_serial s ON d.material_no = s.material_no AND d.batch_no = s.batch_no AND d.serial_no = s.serial_no
                   WHERE h.report_work_status != '已取消'          
                   {}
                   AND h.plan_begin_date >= '{}'      
                   AND h.plan_begin_date < '{}'
                  '''.format(I_SQL, date[0], date[1])

        re1 = self.lcc(sql1)
        Material = {}
        if re.__len__() == 0:
            Material = {}
        else:
            l_re = numpy.array(re1)
            l_re1 = l_re.T
            l_re2 = list(set(l_re1[0]))

            for i in l_re2:
                if i == '0':
                    Material['工具'] = {}
                elif i == '1':
                    Material['耗材'] = {}
                elif i == '2':
                    Material['备件'] = {}
                else:
                    Material['空白'] = {}
            for j in l_re:
                if j[2] is None:
                    pass
                else:
                    if j[0] == '0':
                        if j[1] is not None:
                            if '修复性费用' in Material['工具'].keys():
                                Material['工具']['修复性费用'] += j[2]
                            else:
                                Material['工具']['修复性费用'] = j[2]
                        else:
                            if '预防性费用' in Material['工具'].keys():
                                Material['工具']['预防性费用'] += j[2]
                            else:
                                Material['工具']['预防性费用'] = j[2]
                    elif j[0] == '1':
                        if j[1] is not None:
                            if '修复性费用' in Material['耗材'].keys():
                                Material['耗材']['修复性费用'] += j[2]
                            else:
                                Material['耗材']['修复性费用'] = j[2]
                        else:
                            if '预防性费用' in Material['耗材'].keys():
                                Material['耗材']['预防性费用'] += j[2]
                            else:
                                Material['耗材']['预防性费用'] = j[2]
                    elif j[0] == '2':
                        if j[1] is not None:
                            if '修复性费用' in Material['备件'].keys():
                                Material['备件']['修复性费用'] += j[2]
                            else:
                                Material['备件']['修复性费用'] = j[2]
                        else:
                            if '预防性费用' in Material['备件'].keys():
                                Material['备件']['预防性费用'] += j[2]
                            else:
                                Material['备件']['预防性费用'] = j[2]
                    else:
                        if j[1] is not None:
                            if '修复性费用' in Material['空白'].keys():
                                Material['空白']['修复性费用'] += j[2]
                            else:
                                Material['空白']['修复性费用'] = j[2]
                        else:
                            if '预防性费用' in Material['空白'].keys():
                                Material['空白']['预防性费用'] += j[2]
                            else:
                                Material['空白']['预防性费用'] = j[2]

        # print(Material)
        L_sum = copy.deepcopy(Manhour)

        for i in Material:
            if i in L_sum.keys():
                for l in Material[i]:
                    if l in L_sum[i].keys():
                        L_sum[i][l] += Material[i][l]
                    else:
                        L_sum[i][l] = Material[i][l]
            else:
                L_sum[i] = Material[i]
        # print(L_sum)

        L1 = []
        # L1.append(Manhour)
        # L1.append(Material)
        L1.append(L_sum)
        return L1

    def run(self,car,date):
        L = []
        L1 = []
        L2 = []

        mon_start = datetime.datetime.strptime(date[0], '%Y-%m-%d')
        L.append(mon_start)
        while True:
            if mon_start < datetime.datetime.strptime(date[1], '%Y-%m-%d'):
                if mon_start.month < 12:
                    L.append(datetime.datetime(mon_start.year, mon_start.month + 1, 1))
                    mon_start = datetime.datetime(mon_start.year, mon_start.month + 1, 1)
                else:
                    mo = mon_start.year + 1
                    L.append(datetime.datetime(mo, 1, 1))
                    mon_start = datetime.datetime(mo, 1, 1)

            else:
                L[-1] = datetime.datetime.strptime(date[1], '%Y-%m-%d') + datetime.timedelta(days=1)
                break
        # print(L)

        for j in L:
            if L.index(j) < len(L) - 1:
                num = self.main(car, [j,L[L.index(j)+1]])
                L1.append(num)
                num1 = self.main1(car, [j, L[L.index(j) + 1]])
                L2.append(num1)
        print(L1)
        print(L2)





Check().run({'E27':['2651'],'E28':['2216']},['2017-02-03','2017-10-02'])
