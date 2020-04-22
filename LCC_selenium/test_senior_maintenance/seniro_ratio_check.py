import numpy
import pymysql

class Check:
    def lcc(self, sql):
        # db = pymysql.connect("192.168.1.24", "root", "123456", port=23306,charset="utf8")
        db = pymysql.connect("192.168.221.21", "root", "123456", charset="utf8")
        cur = db.cursor()
        cur.execute("use lcc")
        cur.execute(sql)
        a = cur.fetchall()
        return a

    def main(self,car,date):
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
           if(r.repair_level is null,('空白'),r.repair_level) AS 'repair_level',
            te.duration * b.team_price AS "manhour_money",  
            te.duration AS "manhour_num"
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

        L1 = []
        if re.__len__() == 0:
            L1 = []
        else:
            num = 1
            for k in range(2):
                l_re = numpy.array(re)
                l_re1 = l_re.T
                l_re2 = list(set(l_re1[0]))
                d_1 = dict()

                for i in l_re2:
                    d_1[i] = 0
                    for j in l_re:
                        if j[0] == i:
                            d_1[i] += j[num]

                L1.append(d_1)
                num += 1

        print(L1)

        sql1 = '''
               select 
               if(r.repair_level is null,('空白'),r.repair_level) AS 'repair_level',
               IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)* IF(d.material_deal_type = '出库', d.material_quantity, 0) AS "material_money",
               IF(d.material_deal_type = '出库', d.material_quantity, -d.material_quantity) AS "material_num"
               from op_work_order_header h 
               INNER JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
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
        L2 = []
        if re.__len__() == 0:
            L2 = []
        else:
            num1 = 1
            for k in range(2):
                l_re = numpy.array(re1)
                l_re1 = l_re.T
                l_re2 = list(set(l_re1[0]))
                d_1 = dict()

                for i in l_re2:
                    d_1[i] = 0
                    for j in l_re:
                        if j[0] == i:
                            d_1[i] += j[num1]

                L2.append(d_1)
                num1 += 1

        print(L2)


    def main1(self,car,date):
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
            if(r.repair_level is null,('空白'),r.repair_level) AS 'repair_level',
            h.fault_no AS 'fault_no',
            te.duration * b.team_price AS "manHour_money"
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
        else:
            l_re = numpy.array(re)
            l_re1 = l_re.T
            l_re2 = list(set(l_re1[0]))

            for i in l_re2:
                Manhour[i] = {}
                for j in l_re:
                    if j[0] == i:
                        if j[1] is not None:
                            if '修复性费用' in Manhour[i].keys():
                                Manhour[i]['修复性费用'] += j[2]
                            else:
                                Manhour[i]['修复性费用'] = j[2]
                        else:
                            if '预防性费用' in Manhour[i].keys():
                                Manhour[i]['预防性费用'] += j[2]
                            else:
                                Manhour[i]['预防性费用'] = j[2]

            d_2 = {}

            for i in l_re2:
                d_2[i] = {}
                for j in l_re:
                    if j[0] == i:
                        if j[1] is not None:
                            if '修复性费用' in d_2[i].keys():
                                d_2[i]['修复性费用'] += 1
                            else:
                                d_2[i]['修复性费用'] = 1
                        else:
                            if '预防性费用' in d_2[i].keys():
                                d_2[i]['预防性费用'] += 1
                            else:
                                d_2[i]['预防性费用'] = 1

        print(Manhour)
        print(d_2)

        sql1 = '''
                select
                if(r.repair_level is null,('空白'),r.repair_level) AS 'repair_level',
                h.fault_no AS 'fault_no',
                IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)* IF(d.material_deal_type = '出库', d.material_quantity, 0) AS "material_money"
                from op_work_order_header h
                LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
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
        Materia = {}
        if re1.__len__() == 0:
            Materia = {}
        else:
            l_re = numpy.array(re1)
            l_re1 = l_re.T
            l_re2 = list(set(l_re1[0]))

            for i in l_re2:
                Materia[i] = {}
                for j in l_re:
                    if j[0] == i:
                        if j[1] is not None:
                            if '修复性费用' in Materia[i].keys():
                                Materia[i]['修复性费用'] += j[2]
                            else:
                                Materia[i]['修复性费用'] = j[2]
                        else:
                            if '预防性费用' in Materia[i].keys():
                                Materia[i]['预防性费用'] += j[2]
                            else:
                                Materia[i]['预防性费用'] = j[2]


        print(Materia)

    def main2(self, car, date):
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
            if(r.repair_level is null,('空白'),r.repair_level) AS 'repair_level',
            ifnull(r.repair_method,"(空白)") as "repair_method",
            te.duration * b.team_price AS "manhour_money"
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
        else:

            l_re = numpy.array(re)
            l_re1 = l_re.T
            l_re2 = list(set(l_re1[0]))
            l_re3 = list(set(l_re1[1]))

            for i in l_re2:
                Manhour[i] = {}
                for m in l_re3:
                    for j in l_re:
                        if j[1] == m and i == j[0]:
                            if '{}'.format(m) in Manhour[i].keys():
                                Manhour[i]['{}'.format(m)] += j[2]
                            else:
                                Manhour[i]['{}'.format(m)] = j[2]
            d_2 = dict()

            for i in l_re2:
                d_2[i] = {}
                for m in l_re3:
                    for j in l_re:
                        if j[1] == m and i == j[0]:
                            if '{}'.format(m) in d_2[i].keys():
                                d_2[i]['{}'.format(m)] += 1
                            else:
                                d_2[i]['{}'.format(m)] = 1
        print(Manhour)
        print(d_2)

        sql1 = '''
              select 
              if(r.repair_level is null,('空白'),r.repair_level) AS 'repair_level',
              ifnull(r.repair_method,"(空白)") as "repair_method",             
              IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)* IF(d.material_deal_type = '出库', d.material_quantity, 0) AS "material_money"
              from op_work_order_header h 
              LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
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
        if re1.__len__() == 0:
            Material = {}
        else:
            l_re = numpy.array(re1)
            l_re1 = l_re.T
            l_re2 = list(set(l_re1[0]))
            l_re3 = list(set(l_re1[1]))

            for i in l_re2:
                Material[i] = {}
                for m in l_re3:
                    for j in l_re:
                        if j[1] == m and i == j[0]:
                            if '{}'.format(m) in Material[i].keys():
                                Material[i]['{}'.format(m)] += j[2]
                            else:
                                Material[i]['{}'.format(m)] = j[2]

        print(Material)

    def main3(self, car, date):
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

        sql = '''
            SELECT
            if(r.repair_level is null,('空白'),r.repair_level) AS 'repair_level',
            r.access_name AS 'access_name',
            te.duration * b.team_price AS "manhour_money"
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
        else:
            l_re = numpy.array(re)
            l_re1 = l_re.T
            l_re2 = list(set(l_re1[0]))
            l_re3 = list(set(l_re1[1]))
            L = list(set([i.split('-')[1] for i in l_re3]))

            for i in l_re2:
                Manhour[i] = {}
                for m in L:
                    for j in l_re:
                        if j[0] == i and j[1].split('-')[1] == m:
                            if m in Manhour[i].keys():
                                Manhour[i][m] += j[2]
                            else:
                                Manhour[i][m] = j[2]
            d_2 = {}
            for i in l_re2:
                d_2[i] = {}
                for m in L:
                    for j in l_re:
                        if j[0] == i and j[1].split('-')[1] == m:
                            if m in d_2[i].keys():
                                d_2[i][m] += 1
                            else:
                                d_2[i][m] = 1

        print(Manhour)
        print(d_2)

        sql1 = \
            '''
            SELECT
            if(r.repair_level is null,('空白'),r.repair_level) AS 'repair_level',
            r.access_name AS 'access_name',
            IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)* IF(d.material_deal_type = '出库', d.material_quantity, 0) AS "material_money"
            from op_work_order_header h 
            LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
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
            l_re3 = list(set(l_re1[1]))
            L2 = list(set([i.split('-')[1] for i in l_re3]))

            for i in l_re2:
                Material[i] = {}
                for m in L2:
                    for j in l_re:
                        if j[0] == i and j[1].split('-')[1] == m:
                            if m in Material[i].keys():
                                Material[i][m] += j[2]
                            else:
                                Material[i][m] = j[2]
        print(Material)




Check().main({'E27':['2651']},['2017-05-01','2017-06-01'])



