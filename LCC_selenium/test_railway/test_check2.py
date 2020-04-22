import pymysql
import numpy


class Check:
    def lcc(self, sql):
        db = pymysql.connect("192.168.1.21", "root", "123456", charset="utf8")
        cur = db.cursor()
        cur.execute("use lcc")
        cur.execute(sql)
        a = cur.fetchall()
        return a

    def connect_darams_mileage(self, sql_execure_mileage):
        db = pymysql.connect("192.168.1.21", "root", "123456", charset="utf8")
        cur = db.cursor()
        cur.execute("use darams")
        cur.execute(sql_execure_mileage)
        data = cur.fetchall()
        return data

    def main(self, car, mileage):
        d = {}
        d1 = {}


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
                for com in company:
                    for k in com:
                        d[j] = k
                inputdata = [i, j, mileage[0], mileage[1]]
                sql_execure_mileage = \
                    '''
                    SELECT
                        MIN(mileage_time),MAX(mileage_time)
                    FROM
                        cd_mileage m 
                        INNER JOIN cd_train_real_time r ON r.id = m.train_real_time_id
                        INNER JOIN cd_train_no n ON n.id = r.train_no_id
                        INNER JOIN cd_train_type t ON t.id = n.train_type_id
                    WHERE
                          1 = 1
                        AND t.train_type_code = '{}'
                        AND n.train_no = '{}'
                        AND m.del_flag = '0'
                        AND m.current_mileage >= '{}'
                        AND m.current_mileage < '{}';	
                    '''.format(inputdata[0], inputdata[1], inputdata[2], inputdata[3])
                # print(sql_execure_mileage)
                date = self.connect_darams_mileage(sql_execure_mileage)
                inputdata = [j, date[0][0], date[0][1]]


                sql = \
                    '''SELECT
                    SUM(te.duration) AS "totalManHourNum",
                    SUM(te.duration * b.team_price)AS "totalManHourMoney",
                    SUM(d.material_quantity) AS "totalMaterialNum",
                    SUM(IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)
                    * IF(d.material_deal_type = '出库', d.material_quantity, -d.material_quantity)) AS "totalMaterialMoney"  
                    FROM
                    op_work_order_header h
                    INNER JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
                    LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
                    LEFT JOIN cd_materials_base e ON d.material_no = e.material_no
                    LEFT JOIN cd_materials_batch t ON d.material_no = t.material_no AND d.batch_no = t.batch_no
                    LEFT JOIN cd_materials_serial s ON d.material_no = s.material_no AND d.batch_no = s.batch_no AND d.serial_no = s.serial_no
                    INNER JOIN op_work_order_team te ON te.work_order_no = h.work_order_no
                    INNER JOIN cd_team_base b ON te.team_name = b.team_name         
                    WHERE h.report_work_status != '已取消'          
                    AND h.train_no = {}
                    AND h.plan_begin_date >= '{}'      
                    AND h.plan_begin_date <= '{}'
                    GROUP BY h.train_no
                    '''.format(inputdata[0], inputdata[1], inputdata[2])
                re = self.lcc(sql)

                if re.__len__() == 0:
                    pass
                else:
                    d1[j] = re

                L1 = []
                if re.__len__() == 0:
                    L1 = [0, 0, 0, 0]
                    d1[j] = L1
                else:
                    for no in re:
                        for m in no:
                            L1.append(m)
                    d1[j] = L1
        print(d1)
        print(d)
        d2 = {}
        L3 = []
        for nm in d:
            for nm1 in d1:
                if nm == nm1:
                    if d[nm] in d2.keys():
                        for nm2 in d2[d[nm]]:
                            a = d2[d[nm]].index(nm2)
                            nm2 += d1[nm1][a]
                            L3.append(nm2)
                        d2[d[nm]] = L3
                    else:
                        d2[d[nm]] = d1[nm1]

        print(d2)

    def main_1(self, car, mileage):
        d = {}
        d1 = {}

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
                for com in company:
                    for k in com:
                        d[j] = k
                inputdata = [i, j, mileage[0], mileage[1]]
                sql_execure_mileage = \
                    '''
                    SELECT
                        MIN(mileage_time),MAX(mileage_time)
                    FROM
                        cd_mileage m 
                        INNER JOIN cd_train_real_time r ON r.id = m.train_real_time_id
                        INNER JOIN cd_train_no n ON n.id = r.train_no_id
                        INNER JOIN cd_train_type t ON t.id = n.train_type_id
                    WHERE
                          1 = 1
                        AND t.train_type_code = '{}'
                        AND n.train_no = '{}'
                        AND m.del_flag = '0'
                        AND m.current_mileage >= '{}'
                        AND m.current_mileage < '{}';	
                    '''.format(inputdata[0], inputdata[1], inputdata[2], inputdata[3])
                # print(sql_execure_mileage)
                date = self.connect_darams_mileage(sql_execure_mileage)
                inputdata = [j, date[0][0], date[0][1]]

                sql = \
                    '''SELECT
                    ifnull(concat(r.repair_level,""),"(空白)") AS "repairLevel",
                    SUM(te.duration * b.team_price)AS "totalManHourMoney",

                    SUM(IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)
                    * IF(d.material_deal_type = '出库', d.material_quantity, -d.material_quantity)) AS "totalMaterialMoney",

                    COUNT(*) AS "repairLevelCount"
                    FROM
                    op_work_order_header h
                    INNER JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
                    LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
                    LEFT JOIN cd_materials_base e ON d.material_no = e.material_no
                    LEFT JOIN cd_materials_batch t ON d.material_no = t.material_no AND d.batch_no = t.batch_no
                    LEFT JOIN cd_materials_serial s ON d.material_no = s.material_no AND d.batch_no = s.batch_no AND d.serial_no = s.serial_no
                    INNER JOIN op_work_order_team te ON te.work_order_no = h.work_order_no
                    INNER JOIN cd_team_base b ON te.team_name = b.team_name
                    LEFT JOIN  op_work_order_technology tech on tech.work_order_no = h.work_order_no   
                    WHERE h.report_work_status != '已取消'
                    AND h.train_no = '{}'
                    AND h.plan_begin_date >= '{}'      
                    AND h.plan_begin_date <= '{}'
                    GROUP BY 
                    repairLevel

                    '''.format(inputdata[0], inputdata[1], inputdata[2])
                re = self.lcc(sql)

                if re.__len__() == 0:
                    pass
                else:
                    d1[j] = re
        print(d)
        print(d1)
        d2 = {}
        for nm in d:
            for nm1 in d1:
                if nm == nm1:
                    if d[nm] in d2.keys():
                        a = d1[nm1]
                        b = d2[d[nm]] + a
                        d2[d[nm]] = b
                    else:
                        d2[d[nm]] = d1[nm1]
        print(d2)
        d3 = {}

        for k in d2:
            L0 = []
            num = 1
            for k1 in range(3):
                l_re = numpy.array(d2[k])
                # print(l_re)
                l_re1 = l_re.T
                l_re2 = list(set(l_re1[0]))
                d_1 = dict()
                for i in l_re2:
                    d_1[i] = 0
                    for j in l_re:
                        if j[0] == i:
                            d_1[i] += float(j[num])

                L0.append(d_1)
                num += 1
            d3[k] = L0
        print(d3)

    def main_2(self, car , mileage):
        d = {}
        d1 = {}


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
                for com in company:
                    for k in com:
                        d[j] = k
                inputdata = [i, j, mileage[0], mileage[1]]
                sql_execure_mileage = \
                    '''
                    SELECT
                        MIN(mileage_time),MAX(mileage_time)
                    FROM
                        cd_mileage m 
                        INNER JOIN cd_train_real_time r ON r.id = m.train_real_time_id
                        INNER JOIN cd_train_no n ON n.id = r.train_no_id
                        INNER JOIN cd_train_type t ON t.id = n.train_type_id
                    WHERE
                          1 = 1
                        AND t.train_type_code = '{}'
                        AND n.train_no = '{}'
                        AND m.del_flag = '0'
                        AND m.current_mileage >= '{}'
                        AND m.current_mileage < '{}';	
                    '''.format(inputdata[0], inputdata[1], inputdata[2], inputdata[3])
                # print(sql_execure_mileage)
                date = self.connect_darams_mileage(sql_execure_mileage)
                inputdata = [j, date[0][0], date[0][1]]

                sql = \
                    '''SELECT
                     if(h.fault_no IS NULL and h.notice_no IS NOT NULL,"预防性维修",(
                    if( h.fault_no IS NOT NULL,"修复性维修","(空白)"))) as "repairType",
                    SUM(te.duration * b.team_price)AS "totalManHourMoney",
                    SUM(IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)
                    * IF(d.material_deal_type = '出库', d.material_quantity, -d.material_quantity)) AS "totalMaterialMoney",
                    COUNT(*) AS "repairLevelCount"
                    FROM
                    op_work_order_header h
                    INNER JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
                    LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
                    LEFT JOIN cd_materials_base e ON d.material_no = e.material_no
                    LEFT JOIN cd_materials_batch t ON d.material_no = t.material_no AND d.batch_no = t.batch_no
                    LEFT JOIN cd_materials_serial s ON d.material_no = s.material_no AND d.batch_no = s.batch_no AND d.serial_no = s.serial_no
                    INNER JOIN op_work_order_team te ON te.work_order_no = h.work_order_no
                    INNER JOIN cd_team_base b ON te.team_name = b.team_name
                    LEFT JOIN  op_work_order_technology tech on tech.work_order_no = h.work_order_no   
                    WHERE h.report_work_status != '已取消'
                    AND h.train_no = '{}'
                    AND h.plan_begin_date >= '{}'      
                    AND h.plan_begin_date <= '{}'
                    GROUP BY 
                    repairType

                    '''.format(inputdata[0], inputdata[1], inputdata[2])
                re = self.lcc(sql)
                if re.__len__() == 0:
                    pass
                else:
                    d1[j] = re

        print(d)
        print(d1)
        d2 = {}
        for nm in d:
            for nm1 in d1:
                if nm == nm1:
                    if d[nm] in d2.keys():
                        a = d1[nm1]
                        b = d2[d[nm]] + a
                        d2[d[nm]] = b
                    else:
                        d2[d[nm]] = d1[nm1]
        print(d2)
        d3 = {}

        for k in d2:
            L0 = []
            num = 1
            for k1 in range(3):
                l_re = numpy.array(d2[k])
                # print(l_re)
                l_re1 = l_re.T
                l_re2 = list(set(l_re1[0]))
                d_1 = dict()
                for i in l_re2:
                    d_1[i] = 0
                    for j in l_re:
                        if j[0] == i:
                            d_1[i] += float(j[num])

                L0.append(d_1)
                num += 1
            d3[k] = L0
        print(d3)

    def main_3(self, car, mileage):
        d = {}
        d1 = {}

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
                for com in company:
                    for k in com:
                        d[j] = k
                inputdata = [i, j, mileage[0], mileage[1]]
                sql_execure_mileage = \
                    '''
                    SELECT
                        MIN(mileage_time),MAX(mileage_time)
                    FROM
                        cd_mileage m 
                        INNER JOIN cd_train_real_time r ON r.id = m.train_real_time_id
                        INNER JOIN cd_train_no n ON n.id = r.train_no_id
                        INNER JOIN cd_train_type t ON t.id = n.train_type_id
                    WHERE
                          1 = 1
                        AND t.train_type_code = '{}'
                        AND n.train_no = '{}'
                        AND m.del_flag = '0'
                        AND m.current_mileage >= '{}'
                        AND m.current_mileage < '{}';	
                    '''.format(inputdata[0], inputdata[1], inputdata[2], inputdata[3])
                # print(sql_execure_mileage)
                date = self.connect_darams_mileage(sql_execure_mileage)
                inputdata = [j, date[0][0], date[0][1]]

                sql = \
                    '''SELECT
                    ifnull(r.repair_method,"(空白)") as "repairMethod",
                    SUM(te.duration * b.team_price)AS "totalManHourMoney",
                    SUM(IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)
                    * IF(d.material_deal_type = '出库', d.material_quantity, -d.material_quantity)) AS "totalMaterialMoney",
                    COUNT(*) AS "repairLevelCount"
                    FROM
                    op_work_order_header h
                    INNER JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
                    LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
                    LEFT JOIN cd_materials_base e ON d.material_no = e.material_no
                    LEFT JOIN cd_materials_batch t ON d.material_no = t.material_no AND d.batch_no = t.batch_no
                    LEFT JOIN cd_materials_serial s ON d.material_no = s.material_no AND d.batch_no = s.batch_no AND d.serial_no = s.serial_no
                    INNER JOIN op_work_order_team te ON te.work_order_no = h.work_order_no
                    INNER JOIN cd_team_base b ON te.team_name = b.team_name
                    LEFT JOIN  op_work_order_technology tech on tech.work_order_no = h.work_order_no   
                    WHERE h.report_work_status != '已取消'
                    AND h.train_no = '{}'
                    AND h.plan_begin_date >= '{}'      
                    AND h.plan_begin_date <= '{}'
                    GROUP BY 
                    repairMethod

                    '''.format(inputdata[0], inputdata[1], inputdata[2])

                re = self.lcc(sql)
                if re.__len__() == 0:
                    pass
                else:
                    d1[j] = re

        print(d)
        print(d1)
        d2 = {}
        for nm in d:
            for nm1 in d1:
                if nm == nm1:
                    if d[nm] in d2.keys():
                        a = d1[nm1]
                        b = d2[d[nm]] + a
                        d2[d[nm]] = b
                    else:
                        d2[d[nm]] = d1[nm1]
        print(d2)
        d3 = {}

        for k in d2:
            L0 = []
            num = 1
            for k1 in range(3):
                l_re = numpy.array(d2[k])
                # print(l_re)
                l_re1 = l_re.T
                l_re2 = list(set(l_re1[0]))
                d_1 = dict()
                for i in l_re2:
                    d_1[i] = 0
                    for j in l_re:
                        if j[0] == i:
                            d_1[i] += float(j[num])

                L0.append(d_1)
                num += 1
            d3[k] = L0
        print(d3)

Check().main_3({'E27':['2651'],'E28':['2216']},['1700000','1900000'])

