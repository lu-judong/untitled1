import copy

import pymysql
import numpy

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
        db = pymysql.connect("192.168.221.24", "root", "123456", port=23306, charset="utf8")
        # db = pymysql.connect("192.168.221.21", "root", "123456", charset="utf8")
        cur = db.cursor()
        cur.execute("use darams")
        cur.execute(sql_execure_mileage)
        data = cur.fetchall()
        return data

    def main(self, car, date):
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
               select 
               r.repair_location as repair_location,
               r.repair_location_no as repair_location_no,
               te.duration * b.team_price AS "manhour_money"
               from 
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
        Manhour = {}
        if re.__len__() == 0:
            Manhour = {}
        else:
            l_re = numpy.array(re)

            for i in l_re:
                if i[2] is None:
                    pass
                else:
                    if i[1] == '3':
                        if i[0].split('.')[2] in Manhour.keys():
                            Manhour[i[0].split('.')[2]] += i[2]
                        else:
                            Manhour[i[0].split('.')[2]] = i[2]
        print(Manhour)
        sql1 = '''
                select 
                r.repair_location as repair_location,
                r.repair_location_no as repair_location_no,
                IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)* IF(d.material_deal_type = '出库', d.material_quantity, 0) AS "material_money"
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

        Material = {}
        if re.__len__() == 0:
            Material = {}
        else:
            l_re = numpy.array(re1)
            for i in l_re:
                if i[2] is None:
                    pass
                else:
                    if i[1] == '3':
                        if i[0].split('.')[2] in Material.keys():
                            Material[i[0].split('.')[2]] += i[2]
                        else:
                            Material[i[0].split('.')[2]] = i[2]
        print(Material)
        d_sum = copy.deepcopy(Manhour)
        for i in Material:
            if i in d_sum.keys():
                d_sum[i] += Material[i]
            else:
                d_sum[i] = Material[i]
        print(d_sum)

    def main1(self,car,date):
        d = {}
        d1 = {}
        d2 = {}

        if len(date[0]) <= 12:
            date[0] = date[0] + ' 00:00:00'
        if len(date[1]) <= 12:
            date[1] = date[1] + ' 00:00:00'

        for i in car:
            for j in car[i]:

                sql_execure_company = \
                    '''
                   select
                    a.company AS company
                    from
                    cd_train_no n
                    INNER JOIN cd_train_real_time r on n.id = r.train_no_id
                    INNER JOIN cd_affiliated  a on r.id = a.train_real_time_id
                    where 
                    n.train_no = '{}'
                    '''.format(j)
                # print(sql_execure_mileage)
                company = self.connect_darams_mileage(sql_execure_company)
                if company.__len__() == 0:
                    pass
                else:
                    for com in company:
                        for k in com:
                            d[j] = k

                    sql = '''
                        SELECT
                        te.duration * b.team_price AS "ManHourMoney"
                        FROM
                        op_work_order_header h
                        LEFT JOIN op_work_order_team te on te.work_order_no = h.work_order_no
                        LEFT JOIN cd_team_base b on b.team_name = te.team_name
                        WHERE h.report_work_status != '已取消'          
                        AND h.train_no = {}
                        AND h.plan_begin_date >= '{}'      
                        AND h.plan_begin_date < '{}'
                        '''.format(j, date[0], date[1])
                    re = self.lcc(sql)

                    if re.__len__() == 0:
                        d1[j] = 0
                    else:
                        d1[j] = 0
                        for no in re:
                            for m in no:
                                if m is None:
                                    d1[j] += 0
                                else:
                                    d1[j] += m

                    sql1 = '''
                           select 
                           IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)* IF(d.material_deal_type = '出库', d.material_quantity, 0) AS "material_money"
                           from op_work_order_header h 
                           INNER JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
                           LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
                           LEFT JOIN cd_materials_base e ON d.material_no = e.material_no
                           LEFT JOIN cd_materials_batch t ON d.material_no = t.material_no AND d.batch_no = t.batch_no
                           LEFT JOIN cd_materials_serial s ON d.material_no = s.material_no AND d.batch_no = s.batch_no AND d.serial_no = s.serial_no
                           WHERE h.report_work_status != '已取消'          
                           AND h.train_no = {}
                           AND h.plan_begin_date >= '{}'      
                           AND h.plan_begin_date < '{}'
                          '''.format(j, date[0], date[1])
                    re1 = self.lcc(sql1)

                    if re1.__len__() == 0:
                        d2[j] = 0
                    else:
                        d2[j] = 0
                        for no in re1:
                            for m in no:
                                if m is None:
                                    d2[j] += 0
                                else:
                                    d2[j] += m

        # print(d)
        # print(d1)
        #
        # print(d2)
        d3 = copy.deepcopy(d1)
        for i in d2:
            if i in d3.keys():
                d3[i] += d2[i]
            else:
                d3[i] = d2[i]

        d4 = {}
        for i in d:
            if d[i] in d4:
                d4[d[i]] += d3[i]
            else:
                d4[d[i]] = d3[i]
        print(d4)

    def main2(self,car,date):
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

            for j in l_re:
                if j[1] is None:
                    pass
                else:
                    if j[0] in Manhour.keys():
                        Manhour[j[0]] += j[1]
                    else:
                        Manhour[j[0]] = j[1]
        print(Manhour)

        sql1 = '''
                select 
               if(r.repair_level is null,('空白'),r.repair_level) AS 'repair_level',
                IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)* IF(d.material_deal_type = '出库', d.material_quantity, 0) AS "material_money"
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
        Material = {}
        if re.__len__() == 0:
            Material = {}
        else:
            l_re = numpy.array(re1)

            for j in l_re:
                if j[1] is None:
                    pass
                else:
                    if j[0] in Material.keys():
                        Material[j[0]] += j[1]
                    else:
                        Material[j[0]] = j[1]

        print(Material)
        sum = copy.deepcopy(Manhour)
        for i in Material:
            if i in sum.keys():
                sum[i] += Material[i]
            else:
                sum[i] = Material[i]
        print(sum)

    def main3(self,car,date):
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
        sql =  '''
            SELECT
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

            for j in l_re:
                if j[1] is None:
                    pass
                else:
                    if j[0] is not None:
                        if '修复性费用' in Manhour.keys():
                            Manhour['修复性费用'] += j[1]
                        else:
                            Manhour['修复性费用'] = j[1]
                    else:
                        if '预防性费用' in Manhour.keys():
                            Manhour['预防性费用'] += j[1]
                        else:
                            Manhour['预防性费用'] = j[1]

        print(Manhour)

        sql1 = '''
              SELECT
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
        Material = {}
        if re.__len__() == 0:
            Material = {}
        else:
            l_re1 = numpy.array(re1)

            for j in l_re1:
                if j[1] is not None:
                    if j[0] is not None:
                        if '修复性费用' in Material.keys():
                            Material['修复性费用'] += j[1]
                        else:
                            Material['修复性费用'] = j[1]
                    else:
                        if '预防性费用' in Material.keys():
                            Material['预防性费用'] += j[1]
                        else:
                            Material['预防性费用'] = j[1]

        print(Material)

    def main4(self,car,date):
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
            select
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

            for j in l_re:
                if j[1] is None:
                    pass
                else:
                    if j[0] in Manhour.keys():
                        Manhour[j[0]] += j[1]
                    else:
                        Manhour[j[0]] = j[1]
        print(Manhour)

        sql1 = '''
              SELECT
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
        if re.__len__() == 0:
            Material = {}
        else:
            l_re = numpy.array(re1)

            for j in l_re:
                if j[1] is None:
                    pass
                else:
                    if j[0] in Material.keys():
                        Material[j[0]] += j[1]
                    else:
                        Material[j[0]] = j[1]

        print(Material)

    def main5(self, car, date):
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
            '''
            SELECT
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

            L = list(set([i.split('-')[1] for i in l_re2 if i is not None]))

            for m in L:
                for j in l_re:
                    if j[1] is None:
                        pass
                    else:
                        if j[0] is None:
                            if '空白' in Manhour.keys():
                                Manhour['空白'] += j[1]
                            else:
                                Manhour['空白'] = j[1]
                        else:
                            if j[0].split('-')[1] == m:
                                if m in Manhour.keys():
                                    Manhour[m] += j[1]
                                else:
                                    Manhour[m] = j[1]
        print(Manhour)

        sql1 = \
            '''
            SELECT
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

            L = list(set([i.split('-')[1] for i in l_re2 if i is not None]))

            for m in L:
                for j in l_re:
                    if j[1] is None:
                        pass
                    else:
                        if j[0] is None:
                            if '空白' in Material.keys():
                                Material['空白'] += j[1]
                            else:
                                Material['空白'] = j[1]
                        else:
                            if j[0].split('-')[1] == m:
                                if m in Material.keys():
                                    Material[m] += j[1]
                                else:
                                    Material[m] = j[1]
        print(Material)


Check().main4({'E27':['2651'],'E28':['2216','2776']},['2017-02-03','2017-08-02'])