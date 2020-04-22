import pymysql
import numpy
class Check:
    def lcc(self,sql):
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

    def main(self,car,mileage):
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
                if date[0][0] is None:
                    pass
                else:
                    inputdata = [j, date[0][0], date[0][1]]
                    sql = \
                        '''SELECT
                        r.repair_level AS "repairLevel",
                        te.duration AS "totalManHourNum",
                        te.duration * b.team_price AS "totalManHourMoney",
                        d.material_quantity AS "totalMaterialNum",
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
                        WHERE h.report_work_status != '已取消'          
                        AND h.train_no = '{}'
                        AND h.plan_begin_date >= '{}'      
                        AND h.plan_begin_date < '{}'  
                        '''.format(inputdata[0], inputdata[1], inputdata[2])
                    re = self.lcc(sql)

                    L1 = []
                    if re.__len__() == 0:
                        pass
                    else:
                        num = 1
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

                            L1.append(d_1)
                            num += 1
                    L.append(L1)
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
        L1 = []
        for k1 in d1:
            b = sorted(k1.items(), key=lambda item: item[1], reverse=True)
            b = b[:10]
            dict_1 = {}
            for i in b:
                dict_1[i[0]] = i[1]
            L1.append(dict_1)
        print(L1)

    def main1(self,car,mileage):
        L = []
        L2 = []
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
                if date[0][0] is  None:
                    pass
                else:
                    inputdata = [j, date[0][0], date[0][1]]
                    sql = \
                        '''SELECT
                        r.repair_level AS "repairLevel",
                        if(h.fault_no IS NULL and h.notice_no IS NOT NULL,"预防性维修",(
                if( h.fault_no IS NOT NULL,"修复性维修","(空白)"))) as "repairType",
                        te.duration AS "totalManHourNum",
                        te.duration * b.team_price AS "totalManHourMoney",
                        d.material_quantity AS "totalMaterialNum",
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
                        WHERE h.report_work_status != '已取消'          
                        AND h.train_no = '{}'
                        AND h.plan_begin_date >= '{}'      
                        AND h.plan_begin_date < '{}'  
                        '''.format(inputdata[0], inputdata[1], inputdata[2])
                    re = self.lcc(sql)

                    L0 = []

                    num = 3
                    if re.__len__() == 0:
                        pass
                    else:
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

                            L0.append(d_1)

                        l_re = numpy.array(re)
                        l_re1 = l_re.T
                        l_re2 = list(set(l_re1[0]))
                        d_2 = dict()

                        for i in l_re2:
                            d_2[i] = 0
                            for j in l_re:
                                if j[0] == i:
                                    d_2[i] += 1
                        L2.append(d_2)
                        L.append(L0)

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

        d2 = {}
        for i in range(0, len(L2)):
           for k in L2[i]:
               if k in d2.keys():
                   d2[k] += L2[i][k]
               else:
                   d2[k] = L2[i][k]
        print(d1)
        print(d2)

    def main2(self,car,mileage):
        L = []
        L2 = []
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
                if date[0][0] is None:
                    pass
                else:
                    inputdata = [j, date[0][0], date[0][1]]
                    sql = \
                        '''SELECT
                        r.repair_level AS "repairLevel",
                      ifnull(r.repair_method,"(空白)") as "repairMethod",
                        te.duration AS "totalManHourNum",
                        te.duration * b.team_price AS "totalManHourMoney",
                        d.material_quantity AS "totalMaterialNum",
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
                        WHERE h.report_work_status != '已取消'          
                        AND h.train_no = '{}'
                        AND h.plan_begin_date >= '{}'      
                        AND h.plan_begin_date < '{}'  
                        '''.format(inputdata[0], inputdata[1], inputdata[2])
                    re = self.lcc(sql)

                    L0 = []

                    num = 3
                    if re.__len__() == 0:
                        pass
                    else:
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

                            L0.append(d_1)

                        l_re = numpy.array(re)
                        l_re1 = l_re.T
                        l_re2 = list(set(l_re1[0]))
                        d_2 = dict()

                        for i in l_re2:
                            d_2[i] = 0
                            for j in l_re:
                                if j[0] == i:
                                    d_2[i] += 1
                        L2.append(d_2)
                        L.append(L0)

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

        d2 = {}
        for i in range(0, len(L2)):
           for k in L2[i]:
               if k in d2.keys():
                   d2[k] += L2[i][k]
               else:
                   d2[k] = L2[i][k]
        print(d1)
        print(d2)



Check().main2({'E27':['2651','2776'],'E28':['2216']},['1700000','1900000'])