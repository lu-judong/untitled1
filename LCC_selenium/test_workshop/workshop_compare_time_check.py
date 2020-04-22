import copy

import numpy
import pymysql

class Method:
    def lcc(self, sql):
        db = pymysql.connect("192.168.221.24", "root", "123456", port=23306, charset="utf8")
        # db = pymysql.connect("192.168.1.21", "root", "123456", charset="utf8")
        cur = db.cursor()
        cur.execute("use lcc")
        cur.execute(sql)
        a = cur.fetchall()
        return a


    def main(self,car,date,teamname,repairlocation):
        L1 = []

        if len(date[0]) <= 12:
            date[0] = date[0] + ' 00:00:00'
        # if len(date[1]) <= 12:
        #     date[1] = date[1] + ' 23:59:59'
        date[1] = date[1] + ' 00:00:00'

        for i in car:
            for j in car[i]:
                L1.append(j)
        if len(L1) <= 1:
            I_SQL = 'AND h.train_no = {}'.format(L1[0])
        else:
            L1 = tuple(L1)
            I_SQL = 'AND h.train_no in {}'.format(L1)

        sql = \
            '''SELECT
               te.team_name as teamName,
               r.repair_location AS repairLocation,
               te.duration * b.team_price AS "ManHourMoney",
               te.duration AS "ManHourNum"
               FROM
               op_work_order_header h   
               LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
               LEFT JOIN op_work_order_team te on te.work_order_no = h.work_order_no
               LEFT JOIN cd_team_base b on b.team_name = te.team_name         
               WHERE h.report_work_status != '已取消'          
               {}
               AND h.plan_begin_date >= '{}'      
               AND h.plan_begin_date < '{}'  
               '''.format(I_SQL, date[0], date[1])

        re = self.lcc(sql)
        # print(re)
        Manhour = {}
        l_re = numpy.array(re)
        if re.__len__() == 0:
            Manhour = {}
        else:
            if repairlocation == '全部班组' and teamname == '全部班组':

                for j in l_re:
                    if j[2] is None:
                        pass
                    else:
                        if '工时费' in Manhour.keys():
                            Manhour['工时费'] += j[2]
                        else:
                            Manhour['工时费'] = j[2]

                for j1 in l_re:
                    if j1[3] is None:
                        pass
                    else:
                        if '工时数' in Manhour.keys():
                            Manhour['工时数'] += j1[3]
                        else:
                            Manhour['工时数'] = j1[3]
            elif repairlocation == teamname and repairlocation != '全部班组':
                te = []
                for i in l_re:
                    if i[1].split('.').__len__() >= 3:
                        if i[1].split('.')[2] == repairlocation:
                            te.append(i[0])
                print(tuple(set(te)))


                for j in l_re:
                    if j[2] is None:
                        pass
                    else:
                        if j[0] in te:
                            if '工时费' in Manhour.keys():
                                Manhour['工时费'] += j[2]
                            else:
                                Manhour['工时费'] = j[2]
                        else:
                            pass

                for j1 in l_re:
                    if j1[3] is None:
                        pass
                    else:
                        if j1[0] in te:
                            if '工时数' in Manhour.keys():
                                Manhour['工时数'] += j1[3]
                            else:
                                Manhour['工时数'] = j1[3]
                        else:
                            pass
            else:
                for j in l_re:
                    if j[2] is None:
                        pass
                    else:
                        if j[0] == teamname:
                            if '工时费' in Manhour.keys():
                                Manhour['工时费'] += j[2]
                            else:
                                Manhour['工时费'] = j[2]

                for j1 in l_re:
                    if j1[3] is None:
                        pass
                    else:
                        if j1[0] == teamname:
                            if '工时数' in Manhour.keys():
                                Manhour['工时数'] += j1[3]
                            else:
                                Manhour['工时数'] = j1[3]

        print(Manhour)

        sql1 = '''
              select 
              te.team_name as teamName,
              r.repair_location as repair_location,
              IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)* IF(d.material_deal_type = '出库', d.material_quantity, 0) AS "material_money",
              IF(d.material_deal_type = '出库', d.material_quantity, -d.material_quantity) AS "material_num"
              from op_work_order_header h 
              LEFT JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
              LEFT JOIN op_work_order_team te ON te.work_order_no = h.work_order_no
              LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
              LEFT JOIN cd_materials_base e ON d.material_no = e.material_no
              LEFT JOIN cd_materials_batch t ON d.material_no = t.material_no AND d.batch_no = t.batch_no
              LEFT JOIN cd_materials_serial s ON d.material_no = s.material_no AND d.batch_no = s.batch_no AND d.serial_no = s.serial_no
              WHERE h.report_work_status != '已取消'          
              {}
              AND h.plan_begin_date >= '{}'      
              AND h.plan_begin_date < '{}'
             '''.format(I_SQL, date[0], date[1])

        re1 = self.lcc(sql1)
        # print(re)
        l_re1 = numpy.array(re1)
        Material = {}
        if re.__len__() == 0:
            Material = {}
        else:
            if repairlocation == '全部班组' and teamname == '全部班组':

                for j in l_re1:
                    if j[2] is None:
                        pass
                    else:
                        if '材料费' in Material.keys():
                            Material['材料费'] += j[2]
                        else:
                            Material['材料费'] = j[2]

                for j1 in l_re1:
                    if j1[3] is None:
                        pass
                    else:
                        if '材料数' in Material.keys():
                            Material['材料数'] += j1[3]
                        else:
                            Material['材料数'] = j1[3]
            elif repairlocation == teamname and repairlocation != '全部班组':
                te = []
                for i in l_re1:
                    if i[1].split('.').__len__() >= 3:
                        if i[1].split('.')[2] == repairlocation:
                            te.append(i[0])

                for j in l_re1:
                    if j[2] is None:
                        pass
                    else:
                        if j[0] in te:
                            if '材料费' in Material.keys():
                                Material['材料费'] += j[2]
                            else:
                                Material['材料费'] = j[2]
                        else:
                            pass

                for j1 in l_re1:
                    if j1[3] is None:
                        pass
                    else:
                        if j1[0] in te:
                            if '材料数' in Material.keys():
                                Material['材料数'] += j1[3]
                            else:
                                Material['材料数'] = j1[3]
                        else:
                            pass
            else:
                for j in l_re1:
                    if j[2] is None:
                        pass
                    else:
                        if j[0] == teamname:
                            if '材料费' in Material.keys():
                                Material['材料费'] += j[2]
                            else:
                                Material['材料费'] = j[2]

                for j1 in l_re1:
                    if j1[3] is None:
                        pass
                    else:
                        if j1[0] == teamname:
                            if '材料数' in Material.keys():
                                Material['材料数'] += j1[3]
                            else:
                                Material['材料数'] = j1[3]

        print(Material)

    def main1(self, car, date, teamname, repairlocation):
        L1 = []
        if len(date[0]) <= 12:
            date[0] = date[0] + ' 00:00:00'
        if len(date[1]) <= 12:
            date[1] = date[1] + ' 00:00:00'

        for i in car:
            for j in car[i]:
                L1.append(j)
        if len(L1) <= 1:
            I_SQL = 'AND h.train_no = {}'.format(L1[0])
        else:
            L1 = tuple(L1)
            I_SQL = 'AND h.train_no in {}'.format(L1)

        sql = \
            '''SELECT
                te.team_name as teamName,
                r.repair_location AS repairLocation,
                ifnull(concat(r.repair_level,""),"(空白)") AS "repairLevel",
                te.duration * b.team_price AS "ManHourMoney"
                FROM
                op_work_order_header h
                LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
                INNER JOIN op_work_order_team te ON te.work_order_no = h.work_order_no
                INNER JOIN cd_team_base b ON te.team_name = b.team_name
                WHERE h.report_work_status != '已取消'
                 {}
                AND h.plan_begin_date >= '{}'      
                AND h.plan_begin_date < '{}'
            '''.format(I_SQL, date[0], date[1])

        re = self.lcc(sql)
        Manhour = {}
        l_re = numpy.array(re)
        l_re1 = l_re.T
        l_re2 = list(set(l_re1[2]))
        d_2 = {}
        if re.__len__() == 0:
            Manhour = {}
        else:
            if repairlocation == '全部班组' and teamname == '全部班组':
                for i in l_re2:
                    Manhour[i] = 0
                    for j in l_re:
                        if j[3] is None:
                            pass
                        else:
                            if j[2] == i:
                                Manhour[i] += j[3]
                            else:
                                pass

                for i1 in l_re2:
                    d_2[i1] = 0
                    for j1 in l_re:
                        if j1[2] == i1:
                            d_2[i1] += 1
                        else:
                            pass


            elif repairlocation == teamname and repairlocation != '全部班组':
                te = []
                for i in l_re:
                    if i[1].split('.').__len__() >= 3:
                        if i[1].split('.')[2] == repairlocation:
                            te.append(i[0])

                for i in l_re2:
                    Manhour[i] = 0
                    for j in l_re:
                        if j[3] is None:
                            pass
                        else:
                            if j[0] in te:
                                if j[2] == i:
                                    Manhour[i] += j[3]
                                else:
                                    pass
                            else:
                                pass

                for i1 in l_re2:
                    d_2[i1] = 0
                    for j1 in l_re:
                        if j1[0] in te:
                            if j1[2] == i1:
                                d_2[i1] += 1
                            else:
                                pass
                        else:
                            pass

            else:
                for i in l_re2:
                    Manhour[i] = 0
                    for j in l_re:
                        if j[3] is None:
                            pass
                        else:
                            if j[2] == i:
                                if j[0] == teamname:
                                    Manhour[i] += j[3]
                                else:
                                    pass


                for i1 in l_re2:
                    d_2[i1] = 0
                    for j1 in l_re:
                        if j1[2] == i1:
                            if j1[0] == teamname:
                                d_2[i1] += 1
                            else:
                                pass

        # print(Manhour)
        print(d_2)

        sql1 = '''
               select 
               te.team_name as teamName,
               r.repair_location as repair_location,
               ifnull(concat(r.repair_level,""),"(空白)") AS "repairLevel",
               IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)* IF(d.material_deal_type = '出库', d.material_quantity, 0) AS "material_money"
               from op_work_order_header h 
               LEFT JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
               LEFT JOIN op_work_order_team te ON te.work_order_no = h.work_order_no
               LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
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
        l_re = numpy.array(re1)
        l_re1 = l_re.T
        l_re2 = list(set(l_re1[2]))
        if repairlocation == '全部班组' and teamname == '全部班组':
            for i in l_re2:
                Material[i] = 0
                for j in l_re:
                    if j[3] is None:
                        pass
                    else:
                        if j[2] == i:
                            Material[i] += j[3]
                        else:
                            pass

        elif repairlocation == teamname and repairlocation != '全部班组':
            te = []
            for i in l_re:
                if i[1].split('.').__len__() >= 3:
                    if i[1].split('.')[2] == repairlocation:
                        te.append(i[0])

            for i in l_re2:
                Material[i] = 0
                for j in l_re:
                    if j[3] is None:
                        pass
                    else:
                        if j[0] in te:
                            if j[2] == i:
                                Material[i] += j[3]
                            else:
                                pass
                        else:
                            pass
        else:
            for i in l_re2:
                Material[i] = 0
                for j in l_re:
                    if j[3] is None:
                        pass
                    else:
                        if j[2] == i:
                            if j[0] == teamname:
                                Material [i] += j[3]
                            else:
                                pass
        # print(Material)
        L_sum = copy.deepcopy(Manhour)
        for i in Material:
            if i in L_sum.keys():
                L_sum[i] += Material[i]
            else:
                L_sum[i] = Material[i]
        print(L_sum)

    def main2(self, car, date, teamname, repairlocation):
        L1 = []
        if len(date[0]) <= 12:
            date[0] = date[0] + ' 00:00:00'
        if len(date[1]) <= 12:
            date[1] = date[1] + ' 00:00:00'

        for i in car:
            for j in car[i]:
                L1.append(j)
        if len(L1) <= 1:
            I_SQL = 'AND h.train_no = {}'.format(L1[0])
        else:
            L1 = tuple(L1)
            I_SQL = 'AND h.train_no in {}'.format(L1)

        sql = \
        '''SELECT
            te.team_name as teamName,
            r.repair_location AS repairLocation,
            h.fault_no AS 'fault_no',
            te.duration * b.team_price AS "ManHourMoney"
            FROM
            op_work_order_header h
            LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
            INNER JOIN op_work_order_team te ON te.work_order_no = h.work_order_no
            INNER JOIN cd_team_base b ON te.team_name = b.team_name
            WHERE h.report_work_status != '已取消'
             {}
            AND h.plan_begin_date >= '{}'      
            AND h.plan_begin_date < '{}'
        '''.format(I_SQL,date[0],date[1])

        re = self.lcc(sql)
        Manhour = {}
        if re.__len__() == 0:
            Manhour = {}
        l_re = numpy.array(re)

        d_2 = {}

        if repairlocation == '全部班组' and teamname == '全部班组':
            for j in l_re:
                if j[3] is None:
                    pass
                else:
                    if j[2] is not None:
                        if '修复性费用' in Manhour.keys():
                            Manhour['修复性费用'] += j[3]
                        else:
                            Manhour['修复性费用'] = j[3]
                    else:
                        if '预防性费用' in Manhour.keys():
                            Manhour['预防性费用'] += j[3]
                        else:
                            Manhour['预防性费用'] = j[3]

            for j in l_re:
                if j[2] is not None:
                    if '修复性费用' in d_2.keys():
                        d_2['修复性费用'] += 1
                    else:
                        d_2['修复性费用'] = 1
                else:
                    if '预防性费用' in d_2.keys():
                        d_2['预防性费用'] += 1
                    else:
                        d_2['预防性费用'] = 1

        elif repairlocation == teamname and repairlocation !='全部班组':
            te = []
            for i in l_re:
                if i[1].split('.').__len__() >= 3:
                    if i[1].split('.')[2] == repairlocation:
                        te.append(i[0])

            for j in l_re:
                if j[3] is None:
                    pass
                else:
                    if j[0] in te:
                        if j[2] is not None:
                            if '修复性费用' in Manhour.keys():
                                Manhour['修复性费用'] += j[3]
                            else:
                                Manhour['修复性费用'] = j[3]
                        else:
                            if '预防性费用' in Manhour.keys():
                                Manhour['预防性费用'] += j[3]
                            else:
                                Manhour['预防性费用'] = j[3]

            for j in l_re:
                if j[0] in te:
                    if j[2] is not None:
                        if '修复性费用' in d_2.keys():
                            d_2['修复性费用'] += 1
                        else:
                            d_2['修复性费用'] = 1
                    else:
                        if '预防性费用' in d_2.keys():
                            d_2['预防性费用'] += 1
                        else:
                            d_2['预防性费用'] = 1

        else:
            for j in l_re:
                if j[3] is None:
                    pass
                else:
                    if j[0] == teamname:
                        if j[2] is not None:
                            if '修复性费用' in Manhour.keys():
                                Manhour['修复性费用'] += j[3]
                            else:
                                Manhour['修复性费用'] = j[3]
                        else:
                            if '预防性费用' in Manhour.keys():
                                Manhour['预防性费用'] += j[3]
                            else:
                                Manhour['预防性费用'] = j[3]

            for j in l_re:
                if j[0] == teamname:
                    if j[2] is not None:
                        if '修复性费用' in d_2.keys():
                            d_2['修复性费用'] += 1
                        else:
                            d_2['修复性费用'] = 1
                    else:
                        if '预防性费用' in d_2.keys():
                            d_2['预防性费用'] += 1
                        else:
                            d_2['预防性费用'] = 1

        print(Manhour)
        print(d_2)

        sql1 = '''
                select 
                te.team_name as teamName,
                r.repair_location as repair_location,
                h.fault_no AS 'fault_no',
                IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)* IF(d.material_deal_type = '出库', d.material_quantity, 0) AS "material_money"
                from op_work_order_header h 
                LEFT JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
                LEFT JOIN op_work_order_team te ON te.work_order_no = h.work_order_no
                LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
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
        l_re1 = numpy.array(re1)

        if re.__len__() == 0:
            Material = {}
        else:
            if repairlocation == '全部班组' and teamname == '全部班组':
                for j in l_re1:
                    if j[3] is None:
                        pass
                    else:
                        if j[2] is not None:
                            if '修复性费用' in Material.keys():
                                Material['修复性费用'] += j[3]
                            else:
                                Material['修复性费用'] = j[3]
                        else:
                            if '预防性费用' in Material.keys():
                                Material['预防性费用'] += j[3]
                            else:
                                Material['预防性费用'] = j[3]

            elif repairlocation == teamname and repairlocation != '全部班组':
                te = []
                for i in l_re1:
                    if i[1].split('.').__len__() >= 3:
                        if i[1].split('.')[2] == repairlocation:
                            te.append(i[0])

                for j in l_re1:
                    if j[3] is None:
                        pass
                    else:
                        if j[0] in te:
                            if j[2] is not None:
                                if '修复性费用' in Material.keys():
                                    Material['修复性费用'] += j[3]
                                else:
                                    Material['修复性费用'] = j[3]
                            else:
                                if '预防性费用' in Material.keys():
                                    Material['预防性费用'] += j[3]
                                else:
                                    Material['预防性费用'] = j[3]

            else:
                for j in l_re1:
                    if j[3] is None:
                        pass
                    else:
                        if j[0] == teamname:
                            if j[2] is not None:
                                if '修复性费用' in Material.keys():
                                    Material['修复性费用'] += j[3]
                                else:
                                    Material['修复性费用'] = j[3]
                            else:
                                if '预防性费用' in Material.keys():
                                    Material['预防性费用'] += j[3]
                                else:
                                    Material['预防性费用'] = j[3]

        # print(Material)

        L_sum = copy.deepcopy(Manhour)
        for i in Material:
            if i in L_sum.keys():
                L_sum[i] += Material[i]
            else:
                L_sum[i] = Material[i]
        print(L_sum)


    def main3(self,car, date, teamname, repairlocation):
        L1 = []
        if len(date[0]) <= 12:
            date[0] = date[0] + ' 00:00:00'
        if len(date[1]) <= 12:
            date[1] = date[1] + ' 23:59:59'

        for i in car:
            for j in car[i]:
                L1.append(j)
        if len(L1) <= 1:
            I_SQL = 'AND h.train_no = {}'.format(L1[0])
        else:
            L1 = tuple(L1)
            I_SQL = 'AND h.train_no in {}'.format(L1)

        sql = \
            '''SELECT
                te.team_name as teamName,
                r.repair_location AS repairLocation,
                ifnull(r.repair_method,"(空白)") as "repair_method",
                te.duration * b.team_price AS "ManHourMoney",
                te.duration AS "ManHourNum"
                FROM
                op_work_order_header h
                LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
                INNER JOIN op_work_order_team te ON te.work_order_no = h.work_order_no
                INNER JOIN cd_team_base b ON te.team_name = b.team_name
                WHERE h.report_work_status != '已取消'
                 {}
                AND h.plan_begin_date >= '{}'      
                AND h.plan_begin_date < '{}'
            '''.format(I_SQL, date[0], date[1])

        re = self.lcc(sql)
        Manhour = {}
        l_re = numpy.array(re)
        l_re1 = l_re.T
        l_re2 = list(set(l_re1[2]))
        d_2 = {}
        if re.__len__() == 0:
            Manhour = {}
        else:
            if repairlocation == '全部班组' and teamname == '全部班组':
                for i in l_re2:
                    Manhour[i] = 0
                    for j in l_re:
                        if j[3] is None:
                            pass
                        else:
                            if j[2] == i:
                                Manhour[i] += j[3]
                            else:
                                pass

                for i in l_re2:
                    d_2[i] = 0
                    for j in l_re:
                        if j[4] is None:
                            pass
                        else:
                            if j[2] == i:
                                d_2[i] += j[4]
                            else:
                                pass

            elif repairlocation == teamname and repairlocation != '全部班组':
                te = []
                for i in l_re:
                    if i[1].split('.').__len__() >= 3:
                        if i[1].split('.')[2] == repairlocation:
                            te.append(i[0])

                for i in l_re2:
                    Manhour[i] = 0
                    for j in l_re:
                        if j[3] is None:
                            pass
                        else:
                            if j[2] == i:
                                if j[0] in te:
                                    Manhour[i] += j[3]
                                else:
                                    pass

                for i in l_re2:
                    d_2[i] = 0
                    for j in l_re:
                        if j[4] is None:
                            pass
                        else:
                            if j[2] == i:
                                if j[0] in te:
                                    d_2[i] += j[4]
                                else:
                                    pass

            else:
                for i in l_re2:
                    Manhour[i] = 0
                    for j in l_re:
                        if j[3] is None:
                            pass
                        else:
                            if j[2] == i:
                                if j[0] == teamname:
                                    Manhour[i] += j[3]
                                else:
                                    pass

                for i in l_re2:
                    d_2[i] = 0
                    for j in l_re:
                        if j[4] is None:
                            pass
                        else:
                            if j[2] == i:
                                if j[0] == teamname:
                                    d_2[i] += j[4]
                                else:
                                    pass
        print(Manhour)
        print(d_2)

        sql1 = '''
                select 
                te.team_name as teamName,
                r.repair_location as repair_location,
                ifnull(r.repair_method,"(空白)") as "repair_method",
                IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)* IF(d.material_deal_type = '出库', d.material_quantity, 0) AS "material_money"
                from op_work_order_header h 
                LEFT JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
                LEFT JOIN op_work_order_team te ON te.work_order_no = h.work_order_no
                LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
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
        l_re = numpy.array(re1)
        l_re1 = l_re.T
        l_re2 = list(set(l_re1[2]))

        if re1.__len__() == 0:
            Material = {}
        else:
            if repairlocation == '全部班组' and teamname == '全部班组':
                for i in l_re2:
                    Material[i] = 0
                    for j in l_re:
                        if j[3] is None:
                            pass
                        else:
                            if j[2] == i:
                                Material[i] += j[3]
                            else:
                                pass


            elif repairlocation == teamname and repairlocation != '全部班组':
                te = []
                for i in l_re:
                    if i[1].split('.').__len__() >= 3:
                        if i[1].split('.')[2] == repairlocation:
                            te.append(i[0])

                for i in l_re2:
                    Material[i] = 0
                    for j in l_re:
                        if j[3] is None:
                            pass
                        else:
                            if j[2] == i:
                                if j[0] in te:
                                    Material[i] += j[3]
                                else:
                                    pass


            else:
                for i in l_re2:
                    Material[i] = 0
                    for j in l_re:
                        if j[3] is None:
                            pass
                        else:
                            if j[2] == i:
                                if j[0] == teamname:
                                    Material[i] += j[3]
                                else:
                                    pass
        print(Material)


Method().main3({'E27':['2651']},['2017-06-01','2017-07-01'],'构型000190','构型000190')
# Method().main({'E27':['2651'],'E28':['2216']},['2017-03-01','2017-04-01'],'构型000172','构型000172')
# Method().main2({'E27':['2651']},['2017-02-03','2017-08-02'],'全部班组','全部班组')
# Method().main({'E27':['2651']},['2017-06-01','2017-07-01'],'全部班组','全部班组')
# for i in a[2]:
#     b += a[2][i]
# print(b)