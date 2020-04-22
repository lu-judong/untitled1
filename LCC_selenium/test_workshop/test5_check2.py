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

    def main(self, car, mileage, teamname,repairlocation):
        L = []

        for i in car:
            for j in car[i]:
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
                    te.team_name as teamName,
                    SUBSTRING_INDEX(          
                    IF (
                    SUBSTRING_INDEX(r.repair_location, '.', 3) = SUBSTRING_INDEX(r.repair_location, '.', 2),
                    NULL,
                    SUBSTRING_INDEX(r.repair_location, '.', 3)
                    ),
                    '.' ,- 1
                    ) AS repairLocation,
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
                    AND h.train_no = '{}'
                    AND h.plan_begin_date >= '{}'      
                    AND h.plan_begin_date <= '{}'
                    GROUP BY te.team_name,
                    repairLocation
                    HAVING
                    repairLocation IS NOT NULL    
                    '''.format(inputdata[0], inputdata[1], inputdata[2])
                re = self.lcc(sql)
                # print(re)
                num = 2
                L0 = []
                if re.__len__() == 0:
                    pass
                else:
                    if repairlocation == '全部班组' and teamname == '全部班组':
                        for k in range(4):
                            l_re = numpy.array(re)
                            l_re1 = l_re.T
                            l_re2 = list(set(l_re1[0]))
                            d_1 = dict()

                            for i in l_re2:
                                d_1[i] = 0
                                for j in l_re:
                                    if j[0] == i:
                                        d_1[i] += j[num]

                            L0.append(d_1)
                            num += 1
                    elif  repairlocation == teamname and repairlocation != '全部班组':
                        for k in range(4):
                            l_re = numpy.array(re)

                            d_1 = dict()

                            for j in l_re:
                                if j[1] == repairlocation:
                                    d_1[j[0]] = j[num]
                            L0.append(d_1)
                            num += 1
                    else:
                        for k in range(4):
                            l_re = numpy.array(re)

                            d_1 = dict()

                            for j in l_re:
                                if j[1] == repairlocation and j[0] == teamname:
                                    d_1[j[0]] = j[num]
                            L0.append(d_1)
                            num += 1
                    L.append(L0)
        print(L)
        d1 = []
        for i in range(0, len(L)):
            if i == 0:
                d1 = L[0]
            else:
                for j in L[i]:
                    for k in j.keys():
                        if k in d1[L[i].index(j)].keys():
                            d1[L[i].index(j)][k] += L[i][L[i].index(j)][k]
                        else:
                            d1[L[i].index(j)][k] = L[i][L[i].index(j)][k]
        # print(d1)
        # for k1 in d:

        print(d1)
        return d1
    def main_3(self,car, mileage, teamname, repairlocation):
        L = []
        L_d = []
        for i in car:
            for j in car[i]:
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

                sql = '''
                   SELECT
                   te.team_name as teamName,
                   SUBSTRING_INDEX(

                   IF (
                   SUBSTRING_INDEX(r.repair_location, '.', 3) = SUBSTRING_INDEX(r.repair_location, '.', 2),
                   NULL,
                   SUBSTRING_INDEX(r.repair_location, '.', 3)
                   ),
                   '.' ,- 1
                   ) AS repairLocation,
                   ifnull(r.repair_method,"(空白)") as "repairMethod",
                   te.duration AS "totalManHourNum",
                   te.duration * b.team_price AS "totalManHourMoney",

                   IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)
                      * IF(d.material_deal_type = '出库', d.material_quantity, -d.material_quantity) AS "totalMaterialMoney"
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
                   -- 
                   WHERE h.report_work_status != '已取消'
                   AND h.train_no = '{}'
                   AND h.plan_begin_date >= '{}'
                   AND h.plan_begin_date <= '{}'

                   HAVING repairLocation IS NOT NULL
                   '''.format(inputdata[0], inputdata[1], inputdata[2])
                re = self.lcc(sql)
                L0 = []
                num = 3
                if re.__len__() == 0:
                    pass
                else:
                    if repairlocation == '全部班组' and teamname == '全部班组':
                        for k in range(3):
                            l_re = numpy.array(re)
                            l_re1 = l_re.T
                            l_re2 = list(set(l_re1[2]))
                            d_1 = dict()

                            for i in l_re2:
                                d_1[i] = 0
                                for j in l_re:
                                    if j[2] == i:
                                        d_1[i] += j[num]

                            L0.append(d_1)
                            num += 1
                        L.append(L0)

                        l_re = numpy.array(re)
                        l_re1 = l_re.T
                        l_re2 = list(set(l_re1[2]))
                        d_2 = dict()

                        for i in l_re2:
                            d_2[i] = 0
                            for j in l_re:
                                if j[2] == i:
                                    d_2[i] += 1
                        L_d.append(d_2)

                    elif repairlocation == teamname and repairlocation != '全部班组':
                        for k in range(3):
                            l_re = numpy.array(re)
                            l_re1 = l_re.T
                            l_re2 = list(set(l_re1[2]))
                            d_1 = dict()

                            for i in l_re2:
                                d_1[i] = 0
                                for j in l_re:
                                    if j[1] == repairlocation and j[2] == i:
                                        d_1[i] += j[num]

                            L0.append(d_1)
                            num += 1
                        L.append(L0)

                        l_re = numpy.array(re)
                        l_re1 = l_re.T
                        l_re2 = list(set(l_re1[2]))
                        d_2 = dict()

                        for i in l_re2:
                            d_2[i] = 0
                            for j in l_re:
                                if j[2] == i and j[1] == repairlocation:
                                    d_2[i] += 1
                        L_d.append(d_2)

                    else:
                        for k in range(3):
                            l_re = numpy.array(re)
                            l_re1 = l_re.T
                            l_re2 = list(set(l_re1[2]))
                            d_1 = dict()

                            for i in l_re2:
                                d_1[i] = 0
                                for j in l_re:
                                    if j[1] == repairlocation and j[0] == teamname and j[2] == i:
                                        d_1[i] += j[num]

                            L0.append(d_1)
                            num += 1
                        L.append(L0)
                        l_re = numpy.array(re)
                        l_re1 = l_re.T
                        l_re2 = list(set(l_re1[2]))
                        d_2 = dict()

                        for i in l_re2:
                            d_2[i] = 0
                            for j in l_re:
                                if j[1] == repairlocation and j[0] == teamname and j[2] == i:
                                    d_2[i] += 1
                        L_d.append(d_2)

        d1 = []
        for i in range(0, len(L)):
            if i == 0:
                d1 = L[0]
            else:
                for j in L[i]:
                    for k in j.keys():
                        if k in d1[L[i].index(j)].keys():
                            d1[L[i].index(j)][k] += L[i][L[i].index(j)][k]
                        else:
                            d1[L[i].index(j)][k] = L[i][L[i].index(j)][k]
        # print(L_d)
        d_L = {}
        for i in L_d:
            for j in i:
                if j in d_L.keys():
                    d_L[j] += i[j]
                else:
                    d_L[j] = i[j]
        print(d_L)
        print(d1)

a = Check().main({'E27':['2651'],'E28':['2216']},['1700000','1800000'],'EMU前装检修1班','车内结构')
b = 0
for i in a[2]:
    b += a[2][i]
print(b)