import pymysql
import numpy

class Method:
    def lcc(self, sql):
        db = pymysql.connect("192.168.221.24", "root", "123456", port=23306, charset="utf8")
        # db = pymysql.connect("192.168.1.21", "root", "123456", charset="utf8")
        cur = db.cursor()
        cur.execute("use lcc")
        cur.execute(sql)
        a = cur.fetchall()
        return a

    def main(self,car,date,repairlocation):
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
            '''.format(I_SQL,date[0],date[1])

        re = self.lcc(sql)
        # print(re)
        Manhour = []
        if re.__len__() == 0:
            Manhour = []
        else:
            num = 2
            if repairlocation == '全部班组':
                for k in range(2):
                    l_re = numpy.array(re)
                    l_re1 = l_re.T
                    l_re2 = list(set(l_re1[0]))
                    d_1 = dict()

                    for i in l_re2:
                        d_1[i] = 0
                        for j in l_re:
                            if j[0] == i:
                                if j[num] is None:
                                    pass
                                else:
                                    if j[1].split('.').__len__() >= 3:
                                        d_1[i] += j[num]
                                    else:
                                        pass

                    b = sorted(d_1.items(), key=lambda item:item[1], reverse=True)
                    b = b[:10]
                    dict_1 = {}
                    for i in b:
                        dict_1[i[0]] = i[1]
                    Manhour.append(dict_1)
                    num += 1
            else:
                for k in range(2):
                    l_re = numpy.array(re)

                    d_1 = dict()

                    for j in l_re:
                        if j[num] is None:
                            pass
                        else:
                            if j[1].split('.').__len__() >= 3:
                                if j[1].split('.')[2] == repairlocation:
                                    if j[0] in d_1.keys():
                                        d_1[j[0]] += j[num]
                                    else:
                                        d_1[j[0]] = j[num]
                            else:
                                pass
                    b = sorted(d_1.items(), key=lambda item: item[1], reverse=True)
                    b = b[:10]
                    dict_1 = {}
                    for i in b:
                        dict_1[i[0]] = i[1]
                    Manhour.append(dict_1)
                    num += 1

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
        Material = []
        if re.__len__() == 0:
            Material = []
        else:
            num = 2
            if repairlocation == '全部班组':
                for k in range(2):
                    l_re = numpy.array(re1)
                    l_re1 = l_re.T
                    l_re2 = list(set(l_re1[0]))
                    d_1 = dict()

                    for i in l_re2:
                        d_1[i] = 0
                        for j in l_re:
                            if j[0] == i:
                                if j[num] is None:
                                    pass
                                else:
                                    if j[1].split('.').__len__() >= 3:
                                        d_1[i] += j[num]
                                    else:
                                        pass

                    b = sorted(d_1.items(), key=lambda item: item[1], reverse=True)
                    b = b[:10]
                    dict_1 = {}
                    for i in b:
                        dict_1[i[0]] = i[1]
                    Material.append(dict_1)
                    num += 1
            else:
                for k in range(2):
                    l_re = numpy.array(re1)

                    d_1 = dict()

                    for j in l_re:
                        if j[num] is None:
                            pass
                        else:
                            if j[1].split('.').__len__() >= 3:
                                if j[1].split('.')[2] == repairlocation:
                                    if j[0] in d_1.keys():
                                        d_1[j[0]] += j[num]
                                    else:
                                        d_1[j[0]] = j[num]
                            else:
                                pass
                    b = sorted(d_1.items(), key=lambda item: item[1], reverse=True)
                    b = b[:10]
                    dict_1 = {}
                    for i in b:
                        dict_1[i[0]] = i[1]
                    Material.append(dict_1)
                    num += 1

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
        '''.format(I_SQL,date[0],date[1])

        re = self.lcc(sql)
        Manhour = {}
        if re.__len__() == 0:
            Manhour = {}
        l_re = numpy.array(re)
        l_re1 = l_re.T
        l_re2 = list(set(l_re1[2]))
        d_2 = {}

        if repairlocation == '全部班组' and teamname == '全部班组':
            for i in l_re2:
                Manhour[i] = 0
                for j in l_re:
                    if j[3] is None:
                        pass
                    else:
                        if j[1].split('.').__len__() >= 3:
                            if j[2] == i:
                                Manhour[i] += j[3]

            for i in l_re2:
                d_2[i] = 0
                for j in l_re:
                    if j[1].split('.').__len__() >= 3:
                        if j[2] == i:
                            d_2[i] += 1
                    else:
                        pass

        elif repairlocation == teamname and repairlocation !='全部班组':
            for i in l_re2:
                Manhour[i] = 0
                for j in l_re:
                    if j[3] is None:
                        pass
                    else:
                        if j[1].split('.').__len__() >= 3:
                            if j[1].split('.')[2] == repairlocation and j[2] == i:
                                Manhour[i] += j[3]
                        else:
                            pass

            for i in l_re2:
                d_2[i] = 0
                for j in l_re:
                    if j[1].split('.').__len__() >= 3:
                        if j[1].split('.')[2] == repairlocation and j[2] == i:
                            d_2[i] += 1
                    else:
                        pass

        else:
            for i in l_re2:
                Manhour[i] = 0
                for j in l_re:
                    if j[3] is None:
                        pass
                    else:
                        if j[1].split('.').__len__() >= 3:
                            if j[1].split('.')[2] == repairlocation and j[0] == teamname and j[2] == i:
                                Manhour[i] += j[3]


            for i in l_re2:
                d_2[i] = 0
                for j in l_re:
                    if j[1].split('.').__len__() >= 3:
                        if j[1].split('.')[2] == repairlocation and j[0] == teamname and j[2] == i:
                            d_2[i] += 1

        print(Manhour)
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
                        if j[1].split('.').__len__() >= 3:
                            if j[2] == i:
                                Material[i] += j[3]
                        else:
                            pass

        elif repairlocation == teamname and repairlocation != '全部班组':
            for i in l_re2:
                Material[i] = 0
                for j in l_re:
                    if j[3] is None:
                        pass
                    else:
                        if j[1].split('.').__len__() >= 3:
                            if j[1].split('.')[2] == repairlocation and j[2] == i:
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
                        if j[1].split('.').__len__() >= 3:
                            if j[1].split('.')[2] == repairlocation and j[0] == teamname and j[2] == i:
                                Material[i] += j[3]
                        else:
                            pass
        print(Material)


    def main2(self,car,date,teamname,repairlocation):
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
        l_re = numpy.array(re)

        d_2 = {}
        if re.__len__() == 0:
            Manhour = {}
        else:
            if repairlocation == '全部班组' and teamname == '全部班组':

                for j in l_re:
                    if j[3] is None:
                        pass
                    else:
                        if j[1].split('.').__len__() >= 3:
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
                    if j[1].split('.').__len__() >= 3:
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
                for j in l_re:
                    if j[3] is None:
                        pass
                    else:
                        if j[1].split('.').__len__() >= 3:
                            if j[1].split('.')[2] == repairlocation:
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
                    if j[1].split('.').__len__() >= 3:
                        if j[1].split('.')[2] == repairlocation:
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
                        if j[1].split('.').__len__() >= 3:
                            if j[1].split('.')[2] == repairlocation and j[0] == teamname:
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
                    if j[1].split('.').__len__() >= 3:
                        if j[1].split('.')[2] == repairlocation and j[0] == teamname:
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
                        if j[1].split('.').__len__() >= 3:
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
                for j in l_re1:
                    if j[3] is None:
                        pass
                    else:
                        if j[1].split('.').__len__() >= 3:
                            if j[1].split('.')[2] == repairlocation:
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
                        if j[1].split('.').__len__() >= 3:
                            if j[1].split('.')[2] == repairlocation and j[0] == teamname:
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

        print(Material)



    def main3(self,car,date,teamname,repairlocation):
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
        if re.__len__() == 0:
            Manhour = {}
        l_re = numpy.array(re)
        l_re1 = l_re.T
        l_re2 = list(set(l_re1[2]))
        d_2 = {}

        if repairlocation == '全部班组' and teamname == '全部班组':
            for i in l_re2:
                Manhour[i] = 0
                for j in l_re:
                    if j[3] is None:
                        pass
                    else:
                        if j[1].split('.').__len__() >= 3:
                            if j[2] == i:
                                Manhour[i] += j[3]

            for i in l_re2:
                d_2[i] = 0
                for j in l_re:
                    if j[1].split('.').__len__() >= 3:
                        if j[2] == i:
                            d_2[i] += 1
                    else:
                        pass

        elif repairlocation == teamname and repairlocation != '全部班组':
            for i in l_re2:
                Manhour[i] = 0
                for j in l_re:
                    if j[3] is None:
                        pass
                    else:
                        if j[1].split('.').__len__() >= 3:
                            if j[1].split('.')[2] == repairlocation and j[2] == i:
                                Manhour[i] += j[3]
                        else:
                            pass

            for i in l_re2:
                d_2[i] = 0
                for j in l_re:
                    if j[1].split('.').__len__() >= 3:
                        if j[1].split('.')[2] == repairlocation and j[2] == i:
                            d_2[i] += 1
                    else:
                        pass

        else:
            for i in l_re2:
                Manhour[i] = 0
                for j in l_re:
                    if j[3] is None:
                        pass
                    else:
                        if j[1].split('.').__len__() >= 3:
                            if j[1].split('.')[2] == repairlocation and j[0] == teamname and j[2] == i:
                                Manhour[i] += j[3]

            for i in l_re2:
                d_2[i] = 0
                for j in l_re:
                    if j[1].split('.').__len__() >= 3:
                        if j[1].split('.')[2] == repairlocation and j[0] == teamname and j[2] == i:
                            d_2[i] += 1

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
        if repairlocation == '全部班组' and teamname == '全部班组':
            for i in l_re2:
                Material[i] = 0
                for j in l_re:
                    if j[3] is None:
                        pass
                    else:
                        if j[1].split('.').__len__() >= 3:
                            if j[2] == i:
                                Material[i] += j[3]
                        else:
                            pass

        elif repairlocation == teamname and repairlocation != '全部班组':
            for i in l_re2:
                Material[i] = 0
                for j in l_re:
                    if j[3] is None:
                        pass
                    else:
                        if j[1].split('.').__len__() >= 3:
                            if j[1].split('.')[2] == repairlocation and j[2] == i:
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
                        if j[1].split('.').__len__() >= 3:
                            if j[1].split('.')[2] == repairlocation and j[0] == teamname and j[2] == i:
                                Material[i] += j[3]
                        else:
                            pass
        print(Material)


# Method().main({'E27':['2651'],'E28':['2216']},['2017-02-03','2017-08-03'],'全部班组')
# Method().main1({'E27':['2651'],'E28':['2216']},['2017-02-03','2017-08-03'],'构型000190','构型000190')
# Method().main1({'E27':['2651'],'E28':['2216']},['2017-02-03','2017-08-03'],'全部班组','全部班组')
# Method().main1({'E27':['2651'],'E28':['2216']},['2017-02-03','2017-08-03'],'检修落成2班','构型000190')


