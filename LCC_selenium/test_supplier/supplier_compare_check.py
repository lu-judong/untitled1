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

    def main(self,car,date,supplier):
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
             '''.format(I_SQL, date[0], date[1])
        re = self.lcc(sql)
        Manhour = {}
        l_re = numpy.array(re)

        d = {}
        for i in l_re:
            if i[0] in d.keys():
                d[i[0]] += i[2]
            else:
                d[i[0]] = i[2]

        if re.__len__() == 0:
            Manhour = {}
        else:
            if supplier == 'all':
                for k in l_re:
                    if k[3] is not None:
                        if '工时费' in Manhour.keys():
                            Manhour['工时费'] += k[3] * (k[2] / d[k[0]])
                        else:
                            Manhour['工时费'] = k[3] * (k[2] / d[k[0]])

                for k in l_re:
                    if k[4] is not None:
                        if '工时数' in Manhour.keys():
                            Manhour['工时数'] += k[4] * (k[2] / d[k[0]])
                        else:
                            Manhour['工时数'] = k[4] * (k[2] / d[k[0]])


            else:
                for i in supplier:
                    for k in l_re:
                        if k[3] is not None:
                            if k[1] == i:
                                if '工时费' in Manhour.keys():
                                    Manhour['工时费'] += k[3] * (k[2] / d[k[0]])
                                else:
                                    Manhour['工时费'] = k[3] * (k[2] / d[k[0]])
                for i in supplier:
                    for k in l_re:
                        if k[4] is not None:
                            if k[1] == i:
                                if '工时数' in Manhour.keys():
                                    Manhour['工时数'] += k[4] * (k[2] / d[k[0]])
                                else:
                                    Manhour['工时数'] = k[4] * (k[2] / d[k[0]])

        print(Manhour)

        sql1 = '''
                select 
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
            '''.format(I_SQL, date[0], date[1])

        re1 = self.lcc(sql1)
        Material = {}
        l_re = numpy.array(re1)

        if re.__len__() == 0:
            Material = {}
        else:
            if supplier == 'all':
                for k in l_re:
                    if k[1] is not None:
                        if '材料费' in Material.keys():
                            Material['材料费'] += k[1]
                        else:
                            Material['材料费'] = k[1]

                for k in l_re:
                    if k[2] is not None:
                        if '材料数' in Material.keys():
                            Material['材料数'] += k[2]
                        else:
                            Material['材料数'] = k[2]

            else:
                for i in supplier:
                    for k in l_re:
                        if k[1] is not None:
                            if k[0] == i:
                                if '材料费' in Material.keys():
                                    Material['材料费'] += k[1]
                                else:
                                    Material['材料费'] = k[1]

                for i in supplier:
                    for k in l_re:
                        if k[2] is not None:
                            if  k[0] == i:
                                if '材料数' in Material.keys():
                                    Material['材料数'] += k[2]
                                else:
                                    Material['材料数'] = k[2]

        print(Material)

    def main1(self, car, date, supplier):
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
        l_re2 = list(set(l_re1[1]))
        # print(l_re2)
        d = {}
        for i in l_re:
            if i[0] in d.keys():
                d[i[0]] += i[3]
            else:
                d[i[0]] = i[3]

        if re.__len__() == 0:
            Manhour = {}
        else:
            if supplier == 'all':
                for j in l_re2:
                    Manhour[j] = 0
                    for k in l_re:
                        if k[4] is not None:
                            if j == k[1]:
                                Manhour[j] += k[4] * (k[3] / d[k[0]])

                for j in l_re2:
                    count[j] = 0
                    for k in l_re:
                        if j == k[1]:
                            count[j] += 1

            else:
                for j in l_re2:
                    Manhour[j] = 0

                for i in supplier:
                        for k in l_re:
                            if k[4] is not None:
                                if i == k[2]:
                                    Manhour[k[1]] += k[4] * (k[3] / d[k[0]])

                for j in l_re2:
                    count[j] = 0

                for i in supplier:
                    for k in l_re:
                        if i == k[2]:
                            count[k[1]] += 1

        print(Manhour)
        print(count)

        sql1 = '''
               select 
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
        l_re2 = list(set(l_re1[0]))

        if re1.__len__() == 0:
            Material = {}
        else:
            if supplier == 'all':
                for j in l_re2:
                    Material[j] = 0
                    for k in l_re:
                        if k[2] is not None:
                            if j == k[0]:
                                Material[j] += k[2]

            else:
                for j in l_re2:
                    Material[j] = 0

                for i in supplier:
                    for k in l_re:
                        if k[2] is not None:
                            if i == k[1]:
                                Material[k[0]] += k[2]

        print(Material)
        sum = copy.deepcopy(Manhour)
        for i in Material:
            if i in sum.keys():
                sum[i] += Material[i]
            else:
                sum[i] = Material[i]

        print(sum)

    def main2(self, car, date, supplier):
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
                d[i[0]] += i[3]
            else:
                d[i[0]] = i[3]

        Manhour = {}
        count = {}
        if re.__len__() == 0:
            Manhour = {}
        else:
            if supplier == 'all':
                for j in l_re:
                    if j[4] is None:
                        pass
                    else:
                        if j[1] is not None:
                            if '修复性维修' in Manhour.keys():
                                Manhour['修复性维修'] += j[4] * (j[3] / d[j[0]])
                            else:
                                Manhour['修复性维修'] = j[4] * (j[3] / d[j[0]])
                        else:
                            if '预防性维修' in Manhour.keys():
                                Manhour['预防性维修'] += j[4] * (j[3] / d[j[0]])
                            else:
                                Manhour['预防性维修'] = j[4] * (j[3] / d[j[0]])

                for j in l_re:
                    if j[1] is not None:
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
                for i in supplier:
                    for j in l_re:
                        if j[4] is None:
                            pass
                        else:
                            if j[2] == i:
                                if j[1] is not None:
                                    if '修复性维修' in Manhour.keys():
                                        Manhour['修复性维修'] += j[4] * (j[3] / d[j[0]])
                                    else:
                                        Manhour['修复性维修'] = j[4] * (j[3] / d[j[0]])
                                else:
                                    if '预防性维修' in Manhour.keys():
                                        Manhour['预防性维修'] += j[4] * (j[3] / d[j[0]])
                                    else:
                                        Manhour['预防性维修'] = j[4] * (j[3] / d[j[0]])
                for i in supplier:
                    for j in l_re:
                        if j[2] == i:
                            if j[1] is not None:
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
            if supplier  == 'all':
                for i in re1:
                    if i[2] is None:
                        pass
                    else:
                        if i[0] is not None:
                            if '修复性维修' in Material.keys():
                                Material['修复性维修'] += i[2]
                            else:
                                Material['修复性维修'] = i[2]
                        else:
                            if '预防性维修' in Material.keys():
                                Material['预防性维修'] += i[2]
                            else:
                                Material['预防性维修'] = i[2]
            else:
                for j in supplier:
                    for i in re1:
                        if i[2] is None:
                            pass
                        else:
                            if i[1] == j:
                                if i[0] is not None:
                                    if '修复性维修' in Material.keys():
                                        Material['修复性维修'] += i[2]
                                    else:
                                        Material['修复性维修'] = i[2]
                                else:
                                    if '预防性维修' in Material.keys():
                                        Material['预防性维修'] += i[2]
                                    else:
                                        Material['预防性维修'] = i[2]
        print(Material)
        sum = copy.deepcopy(Manhour)
        for i in Material:
            if i in sum.keys():
                sum[i] += Material[i]
            else:
                sum[i] = Material[i]

        print(sum)

    def main3(self, car, date, supplier):
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
             ifnull(concat(r.repair_method,""),"(空白)") AS "repair_method",
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
            '''.format(I_SQL, date[0], date[1])

        re = self.lcc(sql)
        Manhour = {}
        count = {}

        l_re = numpy.array(re)
        l_re1 = l_re.T
        l_re2 = list(set(l_re1[1]))
        # print(l_re2)
        d = {}
        for i in l_re:
            if i[0] in d.keys():
                d[i[0]] += i[3]
            else:
                d[i[0]] = i[3]


        if re.__len__() == 0:
            Manhour = {}
        else:
            if supplier == 'all':
                for j in l_re2:
                    Manhour[j] = 0
                    for k in l_re:
                        if k[4] is not None:
                            if j == k[1]:
                                Manhour[j] += k[4] * (k[3] / d[k[0]])

                for j in l_re2:
                    count[j] = 0
                    for k in l_re:
                        if k[5] is not None:
                            if j == k[1]:
                                count[j] += k[5] * (k[3] / d[k[0]])

            else:
                for j in l_re2:
                    Manhour[j] = 0

                for i in supplier:
                    for k in l_re:
                        if k[4] is not None:
                            if i == k[2]:
                                Manhour[k[1]] += k[4] * (k[3] / d[k[0]])

                for j in l_re2:
                    count[j] = 0

                for i in supplier:
                    for k in l_re:
                        if k[5] is not None:
                            if i == k[2]:
                                count[k[1]] += k[5] * (k[3] / d[k[0]])

        print(Manhour)
        print(count)

        sql1 = '''
                select 
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
        l_re2 = list(set(l_re1[0]))

        if re1.__len__() == 0:
            Material = {}
        else:
            if supplier == 'all':
                for j in l_re2:
                    Material[j] = 0
                    for k in l_re:
                        if k[2] is not None:
                            if j == k[0]:
                                Material[j] += k[2]

            else:
                for j in l_re2:
                    Material[j] = 0

                for i in supplier:
                    for k in l_re:
                        if k[2] is not None:
                            if i == k[1]:
                                Material[k[0]] += k[2]

        print(Material)
        sum = copy.deepcopy(Manhour)
        for i in Material:
            if i in sum.keys():
                sum[i] += Material[i]
            else:
                sum[i] = Material[i]

        print(sum)



# Check().main({'E27':['2641']},['2017-07-01','2017-08-01'],'all')
# Check().main3({'E27':['2641']},['2017-02-03','2017-08-02'],'all')
Check().main3({'E27':['2641']},['2017-02-03','2017-08-02'],['SIMU_MATERIAL_COMPANY_46','SIMU_MATERIAL_COMPANY_9','SIMU_MATERIAL_COMPANY_5'])
# Check().main2({'E27':['2641']},['2017-07-01','2017-08-01'],['SIMU_MATERIAL_COMPANY_46','SIMU_MATERIAL_COMPANY_9','SIMU_MATERIAL_COMPANY_5'])