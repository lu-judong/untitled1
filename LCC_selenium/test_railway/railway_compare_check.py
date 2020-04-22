import copy

import pymysql
import numpy

class Check:
    def lcc(self,sql):
        # db = pymysql.connect("192.168.1.21", "root", "123456", charset="utf8")
        db = pymysql.connect("192.168.221.24", "root", "123456", port = 23306,charset="utf8")
        cur = db.cursor()
        cur.execute("use lcc")
        cur.execute(sql)
        a = cur.fetchall()
        return a

    def connect_darams_mileage(self, sql_execure_mileage):
        db = pymysql.connect("192.168.221.24", "root", "123456", charset="utf8")
        # db = pymysql.connect("192.168.1.21", "root", "123456", charset="utf8")
        cur = db.cursor()
        cur.execute("use darams")
        cur.execute(sql_execure_mileage)
        data = cur.fetchall()
        return data

    def main(self, car, date):
        d = {}


        if len(date[0]) <= 12:
            date[0] = date[0] + ' 00:00:00'
        if len(date[1]) <= 12:
            date[1] = date[1] + ' 00:00:00'

        for i in car:
            for j in car[i]:
                L1 = []
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
                    co = company[0][0]

                    sql = '''
                        SELECT
                        te.duration * b.team_price AS "ManHourMoney",
                        te.duration AS "ManHourNum"
                        FROM
                        op_work_order_header h
                        LEFT JOIN op_work_order_team te ON te.work_order_no = h.work_order_no
                        LEFT JOIN cd_team_base b ON te.team_name = b.team_name         
                        WHERE h.report_work_status != '已取消'          
                        AND h.train_no = {}
                        AND h.plan_begin_date >= '{}'      
                        AND h.plan_begin_date < '{}'
                        '''.format(j,date[0],date[1])
                    re = self.lcc(sql)

                    L = [0,0]
                    if re.__len__() == 0:
                        L = [0,0]
                    else:
                        for i in range(0, 2):
                            l_re = numpy.array(re)
                            for j1 in l_re:
                                if j1[i] is None:
                                    pass
                                else:
                                    L[i] += j1[i]
                    L1.append(L)
                    # print(L)

                    sql1 = '''
                            select 
                            IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)* IF(d.material_deal_type = '出库', d.material_quantity, 0) AS "material_money",
                            IF(d.material_deal_type = '出库', d.material_quantity, -d.material_quantity) AS "material_num"
                            from op_work_order_header h 
                            INNER JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
                            LEFT JOIN cd_materials_base e ON d.material_no = e.material_no
                            LEFT JOIN cd_materials_batch t ON d.material_no = t.material_no AND d.batch_no = t.batch_no
                            LEFT JOIN cd_materials_serial s ON d.material_no = s.material_no AND d.batch_no = s.batch_no AND d.serial_no = s.serial_no
                            WHERE h.report_work_status != '已取消'          
                            AND h.train_no = {}
                            AND h.plan_begin_date >= '{}'      
                            AND h.plan_begin_date < '{}'
                             '''.format(j, date[0], date[1])
                    re1 = self.lcc(sql1)
                    L2 = [0, 0]
                    if re1.__len__() == 0:
                        L2 = [0, 0]
                    else:
                        for i in range(0, 2):
                            l_re = numpy.array(re1)
                            for j2 in l_re:
                                if j2[i] is None:
                                    pass
                                else:
                                    L2[i] += j2[i]
                    L1.append(L2)
                    if co in d.keys():
                        for i in L1:
                            for j3 in i:
                                d[co][L1.index(i)][i.index(j3)] += j
                    else:
                        d[co] = L1


        print(d)


    def main1(self, car, date):
        d = {}
        d1 = {}

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
                    co = company[0][0]

                    sql = '''
                        SELECT
                        ifnull(concat(r.repair_level,""),"(空白)") AS "repairLevel",
                        te.duration * b.team_price AS "ManHourMoney"
                        FROM
                        op_work_order_header h
                        LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
                        LEFT JOIN op_work_order_team te ON te.work_order_no = h.work_order_no
                        LEFT JOIN cd_team_base b ON te.team_name = b.team_name
                        WHERE h.report_work_status != '已取消'
                        AND h.train_no = '{}'
                        AND h.plan_begin_date >= '{}'      
                        AND h.plan_begin_date < '{}'
                        '''.format(j, date[0], date[1])
                    re = self.lcc(sql)
                    Manhour = {}

                    if re.__len__() == 0:
                        Manhour = {}
                    else:
                        l_re = numpy.array(re)
                        l_re1 = l_re.T
                        l_re2 = list(set(l_re1[0]))


                        for k in l_re2:
                            Manhour[k] = 0
                            for n in l_re:
                                if n[1] is None:
                                    pass
                                else:
                                    if n[0] == k:
                                        Manhour[k] += n[1]

                        d_2 = {}
                        for k in l_re2:
                            d_2[k] = 0
                            for n in l_re:
                                if n[0] == k:
                                    d_2[k] += 1

                    # print(Manhour)
                    # print(d_2)

                    sql1 = '''
                           select 
                           ifnull(concat(r.repair_level,""),"(空白)") AS "repairLevel",
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

                    Material = {}

                    if re1.__len__() == 0:
                        Material = {}
                    else:
                        l_re = numpy.array(re1)
                        l_re1 = l_re.T
                        l_re2 = list(set(l_re1[0]))

                        for k in l_re2:
                            Material[k] = 0
                            for n in l_re:
                                if n[1] is None:
                                    pass
                                else:
                                    if n[0] == k:
                                        Material[k] += n[1]
                    # print(Material)
                    L_sum = copy.deepcopy(Manhour)
                    for j in Material:
                        if j in L_sum.keys():
                            L_sum[j] += Material[j]
                        else:
                            L_sum[j] = Material[j]

                    if co in d.keys():
                        for j in L_sum:
                            if j in d[co].keys():
                                d[co][j] += L_sum[j]
                            else:
                                d[co][j] = L_sum[j]
                    else:
                        d[co] = L_sum

                    if co in d1.keys():
                        for k in d_2:
                            if k in d1[co].keys():
                                d1[co][j] += d_2[j]
                            else:
                                d1[co][j] = d_2[j]
                    else:
                        d1[co] = d_2



        print(d)
        print(d1)


    def main2(self, car ,date):
        d = {}
        d1 = {}

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
                    co = company[0][0]

                    sql = '''
                          SELECT
                          h.fault_no AS 'fault_no',
                          te.duration * b.team_price AS "ManHourMoney"
                          from 
                          op_work_order_header h
                          LEFT JOIN op_work_order_team te on te.work_order_no = h.work_order_no
                          LEFT JOIN cd_team_base b on b.team_name = te.team_name
                          WHERE h.report_work_status != '已取消'          
                          AND h.train_no = '{}'
                          AND h.plan_begin_date >= '{}'      
                          AND h.plan_begin_date < '{}'
                        '''.format(j, date[0], date[1])
                    re = self.lcc(sql)
                    Manhour = {}
                    if re.__len__() == 0:
                        Manhour = {}
                    else:
                        l_re = numpy.array(re)
                        for i in l_re:
                            if i[1] is None:
                                pass
                            else:
                                if i[0] is not None:
                                    if '修复性费用' in Manhour.keys():
                                        Manhour['修复性费用'] += i[1]
                                    else:
                                        Manhour['修复性费用'] = i[1]
                                else:
                                    if '预防性费用' in Manhour.keys():
                                        Manhour['预防性费用'] += i[1]
                                    else:
                                        Manhour['预防性费用'] = i[1]

                        d_2 = {}
                        for i in l_re:
                            if i[0] is not None:
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

                    sql1 = '''
                           select 
                           h.fault_no AS 'fault_no',
                           IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)* IF(d.material_deal_type = '出库', d.material_quantity, 0) AS "material_money"
                           from op_work_order_header h 
                           INNER JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
                           LEFT JOIN cd_materials_base e ON d.material_no = e.material_no
                           LEFT JOIN cd_materials_batch t ON d.material_no = t.material_no AND d.batch_no = t.batch_no
                           LEFT JOIN cd_materials_serial s ON d.material_no = s.material_no AND d.batch_no = s.batch_no AND d.serial_no = s.serial_no
                           WHERE h.report_work_status != '已取消'          
                           AND h.train_no = {}
                           AND h.plan_begin_date >= '{}'      
                           AND h.plan_begin_date < '{}'
                            '''.format(j, date[0], date[1])

                    re1 = self.lcc(sql1)
                    Material = {}
                    if re.__len__() == 0:
                        Material = {}
                    else:
                        l_re = numpy.array(re1)
                        for i in l_re:
                            if j[1] is None:
                                pass
                            else:
                                if i[0] is not None:
                                    if '修复性费用' in Material.keys():
                                        Material['修复性费用'] += i[1]
                                    else:
                                        Material['修复性费用'] = i[1]
                                else:
                                    if '预防性费用' in Material.keys():
                                        Material['预防性费用'] += i[1]
                                    else:
                                        Material['预防性费用'] = i[1]
                    print(Material)

                    L_sum = copy.deepcopy(Manhour)
                    for j in Material:
                        if j in L_sum.keys():
                            L_sum[j] += Material[j]
                        else:
                            L_sum[j] = Material[j]

                    if co in d.keys():
                        for j in L_sum:
                            if j in d[co].keys():
                                d[co][j] += L_sum[j]
                            else:
                                d[co][j] = L_sum[j]
                    else:
                        d[co] = L_sum

                    if co in d1.keys():
                        for k in d_2:
                            if k in d1[co].keys():
                                d1[co][j] += d_2[j]
                            else:
                                d1[co][j] = d_2[j]
                    else:
                        d1[co] = d_2
        print(d)
        print(d1)


    def main3(self, car ,date):
        d = {}
        d1 = {}

        if len(date[0]) <= 12:
            date[0] = date[0] + ' 00:00:00'
        if len(date[1]) <= 12:
            date[1] = date[1] + ' 00:00:00'

        for i in car:
            for j in car[i]:

                sql_execure_company = '''
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
                    co = company[0][0]
                    sql = '''
                        SELECT
                        ifnull(r.repair_method,"(空白)") as "repairMethod",
                        te.duration * b.team_price AS "ManHourMoney"
                        from 
                        op_work_order_header h
                        LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
                        LEFT JOIN op_work_order_team te on te.work_order_no = h.work_order_no
                        LEFT JOIN cd_team_base b on b.team_name = te.team_name
                        WHERE h.report_work_status != '已取消'
                        AND h.train_no = '{}'
                        AND h.plan_begin_date >= '{}'      
                        AND h.plan_begin_date < '{}'
                        '''.format(j, date[0], date[1])

                    re = self.lcc(sql)
                    Manhour = {}
                    if re.__len__() == 0:
                        Manhour = {}
                    else:
                        l_re = numpy.array(re)

                        d_2 = {}
                        for j1 in l_re:
                            if j1[1] is None:
                                pass
                            else:
                                if j1[0] in Manhour.keys():
                                    Manhour[j1[0]] += j1[1]

                                else:
                                    Manhour[j1[0]] = j1[1]

                        for j1 in l_re:

                            if j1[0] in d_2.keys():
                                d_2[j1[0]] += 1

                            else:
                                d_2[j1[0]] = 1

                    print(Manhour)
                    print(d_2)


                    sql1 = '''
                           select 
                           ifnull(r.repair_method,"(空白)") as "repairMethod",
                           IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)* IF(d.material_deal_type = '出库', d.material_quantity, 0) AS "material_money"
                           from op_work_order_header h 
                           INNER JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
                           LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
                           LEFT JOIN cd_materials_base e ON d.material_no = e.material_no
                           LEFT JOIN cd_materials_batch t ON d.material_no = t.material_no AND d.batch_no = t.batch_no
                           LEFT JOIN cd_materials_serial s ON d.material_no = s.material_no AND d.batch_no = s.batch_no AND d.serial_no = s.serial_no
                           WHERE h.report_work_status != '已取消'          
                           AND h.train_no = '{}'
                           AND h.plan_begin_date >= '{}'      
                           AND h.plan_begin_date < '{}'
                          '''.format(j, date[0], date[1])

                    re1 = self.lcc(sql1)
                    Material = {}
                    if re1.__len__() == 0:
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

                    L_sum = copy.deepcopy(Manhour)
                    for j in Material:
                        if j in L_sum.keys():
                            L_sum[j] += Material[j]
                        else:
                            L_sum[j] = Material[j]

                    if co in d.keys():
                        for j in L_sum:
                            if j in d[co].keys():
                                d[co][j] += L_sum[j]
                            else:
                                d[co][j] = L_sum[j]
                    else:
                        d[co] = L_sum

                    if co in d1.keys():
                        for k in d_2:
                            if k in d1[co].keys():
                                d1[co][j] += d_2[j]
                            else:
                                d1[co][j] = d_2[j]
                    else:
                        d1[co] = d_2
        print(d)
        print(d1)





# Check().main1({'E27':['2651']},['2017-02-03','2017-08-03'])

Check().main3({'E28':['2216']},['2017-01-01','2018-01-05'])



