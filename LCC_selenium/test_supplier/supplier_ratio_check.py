import pymysql
import numpy
import copy

class Check:
    def lcc(self, sql):
        db = pymysql.connect("192.168.221.24", "root", "123456", port=23306,charset="utf8")
        # db = pymysql.connect("192.168.221.21", "root", "123456", charset="utf8")
        cur = db.cursor()
        cur.execute("use lcc")
        cur.execute(sql)
        a = cur.fetchall()
        return a

    def connect_darams_mileage(self, sql_execure_mileage):
        db = pymysql.connect("192.168.221.24", "root", "123456", charset="utf8")
        cur = db.cursor()
        cur.execute("use darams")
        cur.execute(sql_execure_mileage)
        data = cur.fetchall()
        return data

    def main(self, car, date, repairlocation):
        L1 = []
        if len(date[0]) <= 12:
            date[0] = date[0] + ' 00:00:00'

        date[1] = date[1] + ' 00:00:00'

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
              h.work_order_no, 
              substring_index(substring_index(r.repair_location,'.', 3), '.', -1) as "repair_location",
              mt.produce_manufacturer,
              d.material_quantity AS "material_num",
              te.duration * b.team_price AS "manhour_money",
              te.duration
              from 
              op_work_order_header h
              LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
              LEFT JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
              LEFT JOIN op_work_order_team te on te.work_order_no = h.work_order_no
              LEFT JOIN cd_team_base b on b.team_name = te.team_name
              LEFT JOIN  cd_instance_material mt on mt.material_no = d.material_no
              AND mt.batch_no IS NULL 
              AND mt.serial_no IS NULL
              OR
              mt.material_no = d.material_no
              AND mt.batch_no = d.batch_no
              AND mt.serial_no IS NULL
              OR
              mt.material_no = d.material_no
              AND mt.batch_no = d.batch_no
              AND mt.serial_no = d.serial_no 
              WHERE h.report_work_status != '已取消'          
              {}
              AND h.plan_begin_date >= '{}'      
              AND h.plan_begin_date < '{}'
             '''.format(I_SQL,date[0],date[1])

        re = self.lcc(sql)
        Manhour = {}
        l_re = numpy.array(re)
        l_re1 = l_re.T
        l_re2 = list(set(l_re1[2]))
        # print(l_re2)
        d = {}
        for i in l_re:
            if i[0] in d.keys():
                d[i[0]] += i[3]
            else:
                d[i[0]] = i[3]

        Manhour1 = {}
        re_sum = {}

        if re.__len__() == 0:
            Manhour= {}
        else:
            if repairlocation == 'all':
                for j in l_re2:
                    Manhour[j] = 0
                    for k in l_re:
                        if k[4] is not None:
                            if j == k[2]:
                                Manhour[j] += k[4] * (k[3] / d[k[0]])

                for j in l_re2:
                    Manhour1[j] = 0
                    for k in l_re:
                        if k[5] is not None:
                            if j == k[2]:
                                Manhour1[j] += k[5] * (k[3] / d[k[0]])

                for j in l_re2:
                    re_sum[j] = 0
                    for k in l_re:
                        if j == k[2]:
                            re_sum[j] += 1

            else:
                for j in l_re2:
                    Manhour[j] = 0
                    for k in l_re:
                        if k[4] is not None:
                            if j == k[2] and k[1] == repairlocation:
                                Manhour[j] += k[4] * (k[3] / d[k[0]])

                for j in l_re2:
                    Manhour1[j] = 0
                    for k in l_re:
                        if k[5] is not None:
                            if j == k[2] and k[1] == repairlocation:
                                Manhour1[j] += k[5] * (k[3] / d[k[0]])

                for j in l_re2:
                    re_sum[j] = 0
                    for k in l_re:
                        if j == k[2] and k[1] == repairlocation:
                            re_sum[j] += 1


        b = sorted(Manhour.items(), key=lambda item: item[1], reverse=True)
        if len(b) <= 10:
            print(b)
        else:
            b = b[:10]
            print(b)

        c = sorted(Manhour1.items(), key=lambda item: item[1], reverse=True)
        if len(c) <= 10:
            print(c)
        else:
            c = c[:10]
            print(c)

        f = sorted(re_sum.items(), key=lambda item: item[1], reverse=True)
        if len(f) <= 10:
            print(f)
        else:
            f = f[:10]
            print(f)
        # print(f)

        sql1 = '''
            select 
            substring_index(substring_index(r.repair_location,'.', 3), '.', -1) as "repair_location",
            mt.produce_manufacturer,
            IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)* IF(d.material_deal_type = '出库', d.material_quantity, 0) AS "material_money",
            IF(d.material_deal_type = '出库', d.material_quantity, -d.material_quantity) AS "material_num"
            from op_work_order_header h 
            LEFT JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
            LEFT JOIN op_work_order_team te ON te.work_order_no = h.work_order_no
            LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
            LEFT JOIN cd_materials_base e ON d.material_no = e.material_no
            LEFT JOIN cd_materials_batch t ON d.material_no = t.material_no AND d.batch_no = t.batch_no
            LEFT JOIN cd_materials_serial s ON d.material_no = s.material_no AND d.batch_no = s.batch_no AND d.serial_no = s.serial_no
            LEFT JOIN  cd_instance_material mt on mt.material_no = d.material_no
            AND mt.batch_no IS NULL 
            AND mt.serial_no IS NULL
            OR
            mt.material_no = d.material_no
            AND mt.batch_no = d.batch_no
            AND mt.serial_no IS NULL
            OR
            mt.material_no = d.material_no
            AND mt.batch_no = d.batch_no
            AND mt.serial_no = d.serial_no
            WHERE h.report_work_status != '已取消'          
            {}
            AND h.plan_begin_date >= '{}'      
            AND h.plan_begin_date < '{}'
            
        '''.format(I_SQL,date[0],date[1])

        re1 = self.lcc(sql1)
        Material = {}
        Material1 = {}
        l_re = numpy.array(re1)
        l_re1 = l_re.T
        l_re2 = list(set(l_re1[1]))
        if re.__len__() == 0:
            Material = {}
        else:
            if repairlocation == 'all':
                for i in l_re2:
                    Material[i] = 0
                    for j in l_re:
                        if j[2] is not None:
                            if i == j[1]:
                                Material[i] += j[2]

                for i in l_re2:
                    Material1[i] = 0
                    for j in l_re:
                        if j[3] is not None:
                            if i == j[1]:
                                Material1[i] += j[3]
            else:
                for i in l_re2:
                    Material[i] = 0
                    for j in l_re:
                        if j[2] is not None:
                            if i == j[1] and repairlocation == j[0]:
                                Material[i] += j[2]

                for i in l_re2:
                    Material1[i] = 0
                    for j in l_re:
                        if j[3] is not None:
                            if i == j[1] and repairlocation == j[0]:
                                Material1[i] += j[3]
        d = sorted(Material.items(), key=lambda item: item[1], reverse=True)
        if len(d) <= 10:
            print(d)
        else:
            d = d[:10]
            print(d)

        e = sorted(Material1.items(), key=lambda item: item[1], reverse=True)
        if len(e) <= 10:
            print(e)
        else:
            e = e[:10]
            print(e)

        l_sum = copy.deepcopy(Manhour)
        for i in Material:
            if i in l_sum.keys():
                l_sum[i] += Material[i]
            else:
                l_sum[i] = Material[i]

        g = sorted(l_sum.items(), key=lambda item: item[1], reverse=True)
        if len(g) <= 10:
            print(g)
        else:
            g = g[:10]
            print(g)


    def main1(self, car, date, repairlocation, supplier):
        L1 = []

        date[0] = date[0] + ' 00:00:00'

        date[1] = date[1] + ' 00:00:00'

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
             h.work_order_no, 
             substring_index(substring_index(r.repair_location,'.', 3), '.', -1) as "repair_location",
             ifnull(concat(r.repair_level,""),"(空白)") AS "repair_level",
             mt.produce_manufacturer,
             d.material_quantity AS "material_num",
             te.duration * b.team_price AS "manhour_money"
             from 
             op_work_order_header h
             LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
             LEFT JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
             LEFT JOIN op_work_order_team te on te.work_order_no = h.work_order_no
             LEFT JOIN cd_team_base b on b.team_name = te.team_name
             LEFT JOIN  cd_instance_material mt on mt.material_no = d.material_no
             AND mt.batch_no IS NULL 
             AND mt.serial_no IS NULL
             OR
             mt.material_no = d.material_no
             AND mt.batch_no = d.batch_no
             AND mt.serial_no IS NULL
             OR
             mt.material_no = d.material_no
             AND mt.batch_no = d.batch_no
             AND mt.serial_no = d.serial_no 
             WHERE h.report_work_status != '已取消'          
             {}
             AND h.plan_begin_date >= '{}'      
             AND h.plan_begin_date < '{}'
            '''.format(I_SQL, date[0], date[1])

        re = self.lcc(sql)
        Manhour = {}
        count = {}

        l_re = numpy.array(re)
        l_re1 = l_re.T
        l_re2 = list(set(l_re1[2]))
        # print(l_re2)
        d = {}
        for i in l_re:
            if i[0] in d.keys():
                d[i[0]] += i[4]
            else:
                d[i[0]] = i[4]


        if re.__len__() == 0:
            Manhour = {}
        else:
            if repairlocation == 'all' and supplier == 'all':
                for j in l_re2:
                    Manhour[j] = 0
                    for k in l_re:
                        if k[5] is not None:
                            if j == k[2]:
                                Manhour[j] += k[5] * (k[4] / d[k[0]])

                for j in l_re2:
                    count[j] = 0
                    for k in l_re:
                        if j == k[2]:
                            count[j] += 1

            elif repairlocation == supplier and repairlocation != 'all':
                for j in l_re2:
                    Manhour[j] = 0
                    for k in l_re:
                        if k[5] is not None:
                            if j == k[2] and repairlocation == k[1]:
                                Manhour[j] += k[5] * (k[4] / d[k[0]])

                for j in l_re2:
                    count[j] = 0
                    for k in l_re:
                        if j == k[2] and repairlocation == k[1]:
                            count[j] += 1

            else:
                for j in l_re2:
                    Manhour[j] = 0
                    for k in l_re:
                        if k[5] is not None:
                            if j == k[2] and repairlocation == k[1] and supplier == k[3]:
                                Manhour[j] += k[5] * (k[4] / d[k[0]])

                for j in l_re2:
                    count[j] = 0
                    for k in l_re:
                        if j == k[2] and repairlocation == k[1] and supplier == k[3]:
                            count[j] += 1

        print(Manhour)
        print(count)

        sql1 = '''
                select 
                substring_index(substring_index(r.repair_location,'.', 3), '.', -1) as "repair_location",
                ifnull(concat(r.repair_level,""),"(空白)") AS "repair_level",
                mt.produce_manufacturer,
                IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)* IF(d.material_deal_type = '出库', d.material_quantity, 0) AS "material_money"
                from op_work_order_header h 
                LEFT JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
                LEFT JOIN op_work_order_team te ON te.work_order_no = h.work_order_no
                LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
                LEFT JOIN cd_materials_base e ON d.material_no = e.material_no
                LEFT JOIN cd_materials_batch t ON d.material_no = t.material_no AND d.batch_no = t.batch_no
                LEFT JOIN cd_materials_serial s ON d.material_no = s.material_no AND d.batch_no = s.batch_no AND d.serial_no = s.serial_no
                LEFT JOIN  cd_instance_material mt on mt.material_no = d.material_no
                AND mt.batch_no IS NULL 
                AND mt.serial_no IS NULL
                OR
                mt.material_no = d.material_no
                AND mt.batch_no = d.batch_no
                AND mt.serial_no IS NULL
                OR
                mt.material_no = d.material_no
                AND mt.batch_no = d.batch_no
                AND mt.serial_no = d.serial_no
                WHERE h.report_work_status != '已取消'          
                {}
                AND h.plan_begin_date >= '{}'      
                AND h.plan_begin_date < '{}'
            '''.format(I_SQL, date[0], date[1])

        re1 = self.lcc(sql1)
        Material = {}
        l_re = numpy.array(re1)
        l_re1 = l_re.T
        l_re2 = list(set(l_re1[1]))

        if re1.__len__() == 0:
            Material = {}
        else:
            if repairlocation == 'all' and supplier == 'all':
                for j in l_re2:
                    Material[j] = 0
                    for k in l_re:
                        if k[3] is not None:
                            if j == k[1]:
                                Material[j] += k[3]

            elif repairlocation == supplier and repairlocation != 'all':
                for j in l_re2:
                    Material[j] = 0
                    for k in l_re:
                        if k[3] is not None:
                            if j == k[1] and repairlocation == k[0]:
                                Material[j] += k[3]

            else:
                for j in l_re2:
                    Material[j] = 0
                    for k in l_re:
                        if k[3] is not None:
                            if j == k[1] and repairlocation == k[0] and supplier == k[2]:
                                Material[j] += k[3]

        print(Material)
        sum = copy.deepcopy(Manhour)
        for i in Material:
            if i in sum.keys():
                sum[i] += Material[i]
            else:
                sum[i] = Material[i]

        print(sum)

    def main2(self, car, date, repairlocation, supplier):
        L1 = []

        date[0] = date[0] + ' 00:00:00'

        date[1] = date[1] + ' 00:00:00'

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
             h.work_order_no, 
             substring_index(substring_index(r.repair_location,'.', 3), '.', -1) as "repair_location",
             h.fault_no,
             mt.produce_manufacturer,
             d.material_quantity AS "material_num",
             te.duration * b.team_price AS "manhour_money"
             from 
             op_work_order_header h
             LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
             LEFT JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
             LEFT JOIN op_work_order_team te on te.work_order_no = h.work_order_no
             LEFT JOIN cd_team_base b on b.team_name = te.team_name
             LEFT JOIN  cd_instance_material mt on mt.material_no = d.material_no
             AND mt.batch_no IS NULL 
             AND mt.serial_no IS NULL
             OR
             mt.material_no = d.material_no
             AND mt.batch_no = d.batch_no
             AND mt.serial_no IS NULL
             OR
             mt.material_no = d.material_no
             AND mt.batch_no = d.batch_no
             AND mt.serial_no = d.serial_no 
             WHERE h.report_work_status != '已取消'          
             {}
             AND h.plan_begin_date >= '{}'      
             AND h.plan_begin_date < '{}'
            '''.format(I_SQL, date[0], date[1])

        re = self.lcc(sql)
        l_re = numpy.array(re)
        d = {}
        for i in l_re:
            if i[0] in d.keys():
                d[i[0]] += i[4]
            else:
                d[i[0]] = i[4]

        Manhour = {}
        count = {}
        if re.__len__() == 0:
            Manhour = {}
        else:
            if repairlocation == 'all' and supplier == 'all':
                for j in l_re:
                    if j[5] is None:
                        pass
                    else:
                        if j[2] is not None:
                            if '修复性维修' in Manhour.keys():
                                Manhour['修复性维修'] += j[5] * (j[4] / d[j[0]])
                            else:
                                Manhour['修复性维修'] = j[5] * (j[4] / d[j[0]])
                        else:
                            if '预防性维修' in Manhour.keys():
                                Manhour['预防性维修'] += j[5] * (j[4] / d[j[0]])
                            else:
                                Manhour['预防性维修'] = j[5] * (j[4] / d[j[0]])

                for j in l_re:
                    if j[5] is None:
                        pass
                    else:
                        if j[2] is not None:
                            if '修复性维修' in count.keys():
                                count['修复性维修'] += 1
                            else:
                                count['修复性维修'] = 1
                        else:
                            if '预防性维修' in count.keys():
                                count['预防性维修'] += 1
                            else:
                                count['预防性维修'] = 1
            elif repairlocation == supplier and repairlocation != 'all':
                for j in l_re:
                    if j[5] is None:
                        pass
                    else:
                        if j[1] == repairlocation:
                            if j[2] is not None:
                                if '修复性维修' in Manhour.keys():
                                    Manhour['修复性维修'] += j[5] * (j[4] / d[j[0]])
                                else:
                                    Manhour['修复性维修'] = j[5] * (j[4] / d[j[0]])
                            else:
                                if '预防性维修' in Manhour.keys():
                                    Manhour['预防性维修'] += j[5] * (j[4] / d[j[0]])
                                else:
                                    Manhour['预防性维修'] = j[5] * (j[4] / d[j[0]])

                for j in l_re:
                    if j[5] is None:
                        pass
                    else:
                        if j[1] == repairlocation:
                            if j[2] is not None:
                                if '修复性维修' in count.keys():
                                    count['修复性维修'] += 1
                                else:
                                    count['修复性维修'] = 1
                            else:
                                if '预防性维修' in count.keys():
                                    count['预防性维修'] += 1
                                else:
                                    count['预防性维修'] = 1
            else:
                for j in l_re:
                    if j[5] is None:
                        pass
                    else:
                        if j[1] == repairlocation and j[3] == supplier:
                            if j[2] is not None:
                                if '修复性维修' in Manhour.keys():
                                    Manhour['修复性维修'] += j[5] * (j[4] / d[j[0]])
                                else:
                                    Manhour['修复性维修'] = j[5] * (j[4] / d[j[0]])
                            else:
                                if '预防性维修' in Manhour.keys():
                                    Manhour['预防性维修'] += j[5] * (j[4] / d[j[0]])
                                else:
                                    Manhour['预防性维修'] = j[5] * (j[4] / d[j[0]])

                for j in l_re:
                    if j[5] is None:
                        pass
                    else:
                        if j[1] == repairlocation and j[3] == supplier:
                            if j[2] is not None:
                                if '修复性维修' in count.keys():
                                    count['修复性维修'] += 1
                                else:
                                    count['修复性维修'] = 1
                            else:
                                if '预防性维修' in count.keys():
                                    count['预防性维修'] += 1
                                else:
                                    count['预防性维修'] = 1
        print(Manhour)
        print(count)

        sql1 = '''
                select 
                substring_index(substring_index(r.repair_location,'.', 3), '.', -1) as "repair_location",
                h.fault_no,
                mt.produce_manufacturer,
                IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)* IF(d.material_deal_type = '出库', d.material_quantity, 0) AS "material_money"
                from op_work_order_header h 
                LEFT JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
                LEFT JOIN op_work_order_team te ON te.work_order_no = h.work_order_no
                LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
                LEFT JOIN cd_materials_base e ON d.material_no = e.material_no
                LEFT JOIN cd_materials_batch t ON d.material_no = t.material_no AND d.batch_no = t.batch_no
                LEFT JOIN cd_materials_serial s ON d.material_no = s.material_no AND d.batch_no = s.batch_no AND d.serial_no = s.serial_no
                LEFT JOIN  cd_instance_material mt on mt.material_no = d.material_no
                AND mt.batch_no IS NULL 
                AND mt.serial_no IS NULL
                OR
                mt.material_no = d.material_no
                AND mt.batch_no = d.batch_no
                AND mt.serial_no IS NULL
                OR
                mt.material_no = d.material_no
                AND mt.batch_no = d.batch_no
                AND mt.serial_no = d.serial_no
                WHERE h.report_work_status != '已取消'          
                {}
                AND h.plan_begin_date >= '{}'      
                AND h.plan_begin_date < '{}'
            '''.format(I_SQL, date[0], date[1])

        re1 = self.lcc(sql1)
        Material = {}
        if re1.__len__() == 0:
            Material = {}
        else:
            if repairlocation == supplier and repairlocation == 'all':
                for i in re1:
                    if i[3] is None:
                        pass
                    else:
                        if i[1] is not None:
                            if '修复性维修' in Material.keys():
                                Material['修复性维修'] += i[3]
                            else:
                                Material['修复性维修'] = i[3]
                        else:
                            if '预防性维修' in Material.keys():
                                Material['预防性维修'] += i[3]
                            else:
                                Material['预防性维修'] = i[3]
            elif repairlocation == supplier and repairlocation != 'all':
                for i in re1:
                    if i[3] is None:
                        pass
                    else:
                        if i[0] == repairlocation:
                            if i[1] is not None:
                                if '修复性维修' in Material.keys():
                                    Material['修复性维修'] += i[3]
                                else:
                                    Material['修复性维修'] = i[3]
                            else:
                                if '预防性维修' in Material.keys():
                                    Material['预防性维修'] += i[3]
                                else:
                                    Material['预防性维修'] = i[3]
            else:
                for i in re1:
                    if i[3] is None:
                        pass
                    else:
                        if i[0] == repairlocation and i[2] == supplier:
                            if i[1] is not None:
                                if '修复性维修' in Material.keys():
                                    Material['修复性维修'] += i[3]
                                else:
                                    Material['修复性维修'] = i[3]
                            else:
                                if '预防性维修' in Material.keys():
                                    Material['预防性维修'] += i[3]
                                else:
                                    Material['预防性维修'] = i[3]
        print(Material)
        sum = copy.deepcopy(Manhour)
        for i in Material:
            if i in sum.keys():
                sum[i] += Material[i]
            else:
                sum[i] = Material[i]

        print(sum)

    def main3(self, car, date, repairlocation, supplier):
        L1 = []

        date[0] = date[0] + ' 00:00:00'

        date[1] = date[1] + ' 00:00:00'

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
             h.work_order_no, 
             substring_index(substring_index(r.repair_location,'.', 3), '.', -1) as "repair_location",
             ifnull(concat(r.repair_method,""),"(空白)") AS "repair_method",
             mt.produce_manufacturer,
             d.material_quantity AS "material_num",
             te.duration * b.team_price AS "manhour_money"
             from 
             op_work_order_header h
             LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
             LEFT JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
             LEFT JOIN op_work_order_team te on te.work_order_no = h.work_order_no
             LEFT JOIN cd_team_base b on b.team_name = te.team_name
             LEFT JOIN  cd_instance_material mt on mt.material_no = d.material_no
             AND mt.batch_no IS NULL 
             AND mt.serial_no IS NULL
             OR
             mt.material_no = d.material_no
             AND mt.batch_no = d.batch_no
             AND mt.serial_no IS NULL
             OR
             mt.material_no = d.material_no
             AND mt.batch_no = d.batch_no
             AND mt.serial_no = d.serial_no 
             WHERE h.report_work_status != '已取消'          
             {}
             AND h.plan_begin_date >= '{}'      
             AND h.plan_begin_date < '{}'
            '''.format(I_SQL, date[0], date[1])

        re = self.lcc(sql)
        Manhour = {}
        count = {}

        l_re = numpy.array(re)
        l_re1 = l_re.T
        l_re2 = list(set(l_re1[2]))
        # print(l_re2)
        d = {}
        for i in l_re:
            if i[0] in d.keys():
                d[i[0]] += i[4]
            else:
                d[i[0]] = i[4]


        if re.__len__() == 0:
            Manhour = {}
        else:
            if repairlocation == 'all' and supplier == 'all':
                for j in l_re2:
                    Manhour[j] = 0
                    for k in l_re:
                        if k[5] is not None:
                            if j == k[2]:
                                Manhour[j] += k[5] * (k[4] / d[k[0]])

                for j in l_re2:
                    count[j] = 0
                    for k in l_re:
                        if j == k[2]:
                            count[j] += 1

            elif repairlocation == supplier and repairlocation != 'all':
                for j in l_re2:
                    Manhour[j] = 0
                    for k in l_re:
                        if k[5] is not None:
                            if j == k[2] and repairlocation == k[1]:
                                Manhour[j] += k[5] * (k[4] / d[k[0]])

                for j in l_re2:
                    count[j] = 0
                    for k in l_re:
                        if j == k[2] and repairlocation == k[1]:
                            count[j] += 1

            else:
                for j in l_re2:
                    Manhour[j] = 0
                    for k in l_re:
                        if k[5] is not None:
                            if j == k[2] and repairlocation == k[1] and supplier == k[3]:
                                Manhour[j] += k[5] * (k[4] / d[k[0]])

                for j in l_re2:
                    count[j] = 0
                    for k in l_re:
                        if j == k[2] and repairlocation == k[1] and supplier == k[3]:
                            count[j] += 1

        print(Manhour)
        print(count)

        sql1 = '''
                select 
                substring_index(substring_index(r.repair_location,'.', 3), '.', -1) as "repair_location",
                ifnull(concat(r.repair_method,""),"(空白)") AS "repair_method",
                mt.produce_manufacturer,
                IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)* IF(d.material_deal_type = '出库', d.material_quantity, 0) AS "material_money"
                from op_work_order_header h 
                LEFT JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
                LEFT JOIN op_work_order_team te ON te.work_order_no = h.work_order_no
                LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
                LEFT JOIN cd_materials_base e ON d.material_no = e.material_no
                LEFT JOIN cd_materials_batch t ON d.material_no = t.material_no AND d.batch_no = t.batch_no
                LEFT JOIN cd_materials_serial s ON d.material_no = s.material_no AND d.batch_no = s.batch_no AND d.serial_no = s.serial_no
                LEFT JOIN  cd_instance_material mt on mt.material_no = d.material_no
                AND mt.batch_no IS NULL 
                AND mt.serial_no IS NULL
                OR
                mt.material_no = d.material_no
                AND mt.batch_no = d.batch_no
                AND mt.serial_no IS NULL
                OR
                mt.material_no = d.material_no
                AND mt.batch_no = d.batch_no
                AND mt.serial_no = d.serial_no
                WHERE h.report_work_status != '已取消'          
                {}
                AND h.plan_begin_date >= '{}'      
                AND h.plan_begin_date < '{}'
            '''.format(I_SQL, date[0], date[1])

        re1 = self.lcc(sql1)
        Material = {}
        l_re = numpy.array(re1)
        l_re1 = l_re.T
        l_re2 = list(set(l_re1[1]))

        if re1.__len__() == 0:
            Material = {}
        else:
            if repairlocation == 'all' and supplier == 'all':
                for j in l_re2:
                    Material[j] = 0
                    for k in l_re:
                        if k[3] is not None:
                            if j == k[1]:
                                Material[j] += k[3]

            elif repairlocation == supplier and repairlocation != 'all':
                for j in l_re2:
                    Material[j] = 0
                    for k in l_re:
                        if k[3] is not None:
                            if j == k[1] and repairlocation == k[0]:
                                Material[j] += k[3]

            else:
                for j in l_re2:
                    Material[j] = 0
                    for k in l_re:
                        if k[3] is not None:
                            if j == k[1] and repairlocation == k[0] and supplier == k[2]:
                                Material[j] += k[3]

        print(Material)
        sum = copy.deepcopy(Manhour)
        for i in Material:
            if i in sum.keys():
                sum[i] += Material[i]
            else:
                sum[i] = Material[i]

        print(sum)

    def main4(self, car, date, repairlocation):
        L1 = []

        date[0] = date[0] + ' 00:00:00'

        date[1] = date[1] + ' 00:00:00'

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
            mt.produce_manufacturer,
            r.repair_location
            from 
            op_work_order_header h
            LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
            LEFT JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
            LEFT JOIN  cd_instance_material mt on mt.material_no = d.material_no
            AND mt.batch_no IS NULL 
            AND mt.serial_no IS NULL
            OR
            mt.material_no = d.material_no
            AND mt.batch_no = d.batch_no
            AND mt.serial_no IS NULL
            OR
            mt.material_no = d.material_no
            AND mt.batch_no = d.batch_no
            AND mt.serial_no = d.serial_no 
            WHERE h.report_work_status != '已取消'          
            {}
            AND h.plan_begin_date >= '{}'      
            AND h.plan_begin_date < '{}'
            AND r.repair_location_no = 3
        '''.format(I_SQL,date[0],date[1])
        re1 = self.lcc(sql)
        sup1 = {}

        l_re1 = numpy.array(re1)
        l_re2 = l_re1.T
        l_re3 = tuple(l_re2[0])
        I_SQL1 = 'where mt.produce_manufacturer in {}'.format(l_re3)
        L1 = []
        if re1.__len__() == 0:
            pass
        else:
            if repairlocation == 'all':
                for i in l_re3:
                    sup1[i] = 0
                    for j in re1:
                        if j[0] == i:
                            if j[1] in L1:
                                pass
                            else:
                                sup1[i] += 1
                                L1.append(j[1])
                    L1 = []
            else:
                for i in l_re3:
                    sup1[i] = 0
                    for j in re1:
                        if j[0] == i and j[1].split('.')[2] == repairlocation:
                            if j[1] in L1:
                                pass
                            else:
                                sup1[i] += 1
                                L1.append(j[1])
                    L1 = []

        sql1 = '''
            select 
            mt.produce_manufacturer,
            trin.node_location_code as "repair_location"
            from 
            cd_trainno_instance trin
            LEFT JOIN  cd_instance_material mt on mt.material_no = trin.material_no
            AND mt.batch_no IS NULL 
            AND mt.serial_no IS NULL
            OR
            mt.material_no = trin.material_no
            AND mt.batch_no = trin.batch_no
            AND mt.serial_no IS NULL
            OR
            mt.material_no = trin.material_no
            AND mt.batch_no = trin.batch_no
            AND mt.serial_no = trin.serial_no
            {}
        '''.format(I_SQL1)

        re = self.lcc(sql1)
        sum = {}
        sup = numpy.array(re)
        l_sup = sup.T
        l_sup1 = list(set(l_sup[0]))
        L = []
        if re.__len__() == 0:
            sum = {}
        else:
            for i in l_sup1:
                sum[i] = 0
                for j in re:
                    if j[0] == i:
                        if j[1] in L:
                            pass
                        else:
                            sum[i] += 1
                            L.append(j[1])
                L = []
        print(sum)
        print(sup1)

    def main5(self, car, date, repairlocation):
        L1 = []

        date[0] = date[0] + ' 00:00:00'

        date[1] = date[1] + ' 00:00:00'

        for i in car:
            for j in car[i]:
                L1.append(j)
        if len(L1) <= 1:
            I_SQL = 'AND h.train_no = {}'.format(L1[0])
        else:
            L1 = tuple(L1)
            I_SQL = 'AND h.train_no in {}'.format(L1)

        sql1 = '''
                       SELECT
                       h.work_order_no,
                       h.fault_no
                       FROM
                       op_work_order_header h
                       LEFT JOIN op_work_order_team te on te.work_order_no = h.work_order_no
                       LEFT JOIN cd_team_base b on b.team_name = te.team_name    
                       WHERE h.report_work_status != '已取消'          
                       {}
                       AND h.plan_begin_date >= '{}'      
                       AND h.plan_begin_date < '{}'
                       '''.format(I_SQL, date[0], date[1])

        re = self.lcc(sql1)
        L = []
        d1 = {}

        if re.__len__() == 0:
            pass
        else:
            l_re = numpy.array(re)
            for i in l_re:
                L.append(i[1])
                d1[i[0]] = i[1]

        tu = tuple(set(L))
        # print(tu)
        if tu.__len__() == 0:
            I_SQL1 = 'AND h.fault_no = {}'.format(tu[0])
        else:
            I_SQL1 = 'AND h.fault_no in {}'.format(tu)

        sql2 = '''
               select h.fault_no as 'faultNo',
               t.end_late
               from op_fault_order_header h,op_train t,op_fault_order_detail d,op_fault_real r
               where d.fault_id = h.id
               and d.id = t.fault_detail_id
               and r.fault_detail_id = d.id
               {} 
               '''.format(I_SQL1)

        re1 = self.connect_darams_mileage(sql2)

        for j in re1:
            for j1 in d1:
                if j[0] == d1[j1]:
                    if j[1] is None:
                        d1[j1] = 0
                    else:
                        d1[j1] = j[1]
        # print(d1)

        sql = '''
                select
                h.work_order_no, 
                substring_index(substring_index(r.repair_location,'.', 3), '.', -1) as "repair_location",
                mt.produce_manufacturer,
                d.material_quantity AS "material_num"
                from 
                op_work_order_header h
                LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
                LEFT JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
                LEFT JOIN op_work_order_team te on te.work_order_no = h.work_order_no
                LEFT JOIN cd_team_base b on b.team_name = te.team_name
                LEFT JOIN  cd_instance_material mt on mt.material_no = d.material_no
                AND mt.batch_no IS NULL 
                AND mt.serial_no IS NULL
                OR
                mt.material_no = d.material_no
                AND mt.batch_no = d.batch_no
                AND mt.serial_no IS NULL
                OR
                mt.material_no = d.material_no
                AND mt.batch_no = d.batch_no
                AND mt.serial_no = d.serial_no 
                WHERE h.report_work_status != '已取消'          
                {}
                AND h.plan_begin_date >= '{}'      
                AND h.plan_begin_date < '{}'        
            '''.format(I_SQL,date[0],date[1])

        sup = self.lcc(sql)
        l_sup = numpy.array(sup)

        l_sup1 = l_sup.T
        if repairlocation == 'all':
            l_sup2 = list(set(l_sup1[2]))
        else:
            l_sup2 = []
            for i in l_sup:
                if i[1] == repairlocation:
                    l_sup2.append(i[2])

        d = {}
        for i in l_sup:
            if i[0] in d.keys():
                d[i[0]] += i[3]
            else:
                d[i[0]] = i[3]

        work_or = {}

        for i in l_sup2:
            work_or[i] = {}
            for j in l_sup:
                if j[3] is not None:
                    work_or[i][j[0]] = j[3] / d[j[0]]


        # print(work_or)

        d2 = {}


        for i in work_or:
            d2[i] = 0
            for j in work_or[i]:
                d2[i] = d1[j] * float(work_or[i][j])


        print(d2)











# Check().main5({'E27':['2641']},['2017-02-03','2017-08-03'],'all')

# Check().main({'E27':['2641']},['2017-02-03','2017-08-03'],'车下设备总图')
# Check().main2({'E27':['2641']},['2017-02-03','2017-08-03'],'车外设备总图','车外设备总图')
# Check().main2({'E27':['2641']},['2017-02-03','2017-08-03'],'车内设备布置','SIMU_MATERIAL_COMPANY_9')
# Check().main2({'E27':['2641']},['2017-02-03','2017-08-03'],'all','all')
# Check().main1({'E27':['2641']},['2017-02-03','2017-08-03'],'车下设备总图','车下设备总图')
# Check().main1({'E27':['2641']},['2017-02-03','2017-08-03'],'车下设备总图','SIMU_MATERIAL_COMPANY_30')
# Check().main4({'E27':['2641']},['2017-02-03','2017-08-03'],'all')