import pymysql
import numpy


class Method:
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
        L1 = []
        for i in car:
            for j in car[i]:
                L1.append(j)

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
             h.train_type AS 'train_type',
             te.duration * b.team_price AS "ManHourMoney",
             te.duration AS "ManHourNum"
             from 
             op_work_order_header h
             inner join op_work_order_team te on te.work_order_no = h.work_order_no
             inner join cd_team_base b on b.team_name = te.team_name
             WHERE h.report_work_status != '已取消'          
             {}
             AND h.start_repair_miles >= '{}'      
             AND h.start_repair_miles < '{}'
            '''.format(I_SQL, mileage[0], mileage[1])
        re = self.lcc(sql)
        Manhour = []
        if re.__len__() == 0:
            Manhour = []
        else:
            l_re = numpy.array(re)
            l_re1 = l_re.T
            l_re2 = list(set(l_re1[0]))
            l_re3 = list(set(l_re1[1]))

            d_1 = dict()
            d_2 = {}

            for i in l_re2:
                d_1[i] = {}
                for m in l_re3:
                    for j in l_re:
                        if j[1] == m and i == j[0]:
                            if '{}'.format(m) in d_1[i].keys():
                                d_1[i]['{}'.format(m)] += j[2]
                            else:
                                d_1[i]['{}'.format(m)] = j[2]
            Manhour.append(d_1)

            for i in l_re2:
                d_2[i] = {}
                for m in l_re3:
                    for j in l_re:
                        if j[1] == m and j[0] == i:
                            if '{}'.format(m) in d_2[i].keys():
                                d_2[i]['{}'.format(m)] += 1
                            else:
                                d_2[i]['{}'.format(m)] = 1
            Manhour.append(d_2)

        print(Manhour)

        sql1 = '''
                select 
                h.train_type AS 'train_type',
                d.material_quantity AS "MaterialNum",
                IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)* IF(d.material_deal_type = '出库', d.material_quantity, -d.material_quantity) AS "MaterialMoney"
                from op_work_order_header h 
                INNER JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
                LEFT JOIN cd_materials_base e ON d.material_no = e.material_no
                LEFT JOIN cd_materials_batch t ON d.material_no = t.material_no AND d.batch_no = t.batch_no
                LEFT JOIN cd_materials_serial s ON d.material_no = s.material_no AND d.batch_no = s.batch_no AND d.serial_no = s.serial_no
                WHERE h.report_work_status != '已取消'          
                {}
                AND h.start_repair_miles >= '{}'      
                AND h.start_repair_miles < '{}'
               '''.format(I_SQL, mileage[0], mileage[1])
        re1 = self.lcc(sql1)
        Materia = []
        if re1.__len__() == 0:
            Materia = []
        else:
            l_re = numpy.array(re1)
            l_re1 = l_re.T
            l_re2 = list(set(l_re1[0]))
            l_re3 = list(set(l_re1[1]))
            d_1 = {}
            d_2 = {}

            for i in l_re2:
                d_1[i] = {}
                for m in l_re3:
                    for j in l_re:
                        if j[1] == m and i == j[0]:
                            if '{}'.format(m) in d_1[i].keys():
                                d_1[i]['{}'.format(m)] += j[2]
                            else:
                                d_1[i]['{}'.format(m)] = j[2]
            Materia.append(d_1)

            for i in l_re2:
                d_2[i] = {}
                for m in l_re3:
                    for j in l_re:
                        if j[1] == m and j[0] == i:
                            if '{}'.format(m) in d_2[i].keys():
                                d_2[i]['{}'.format(m)] += 1
                            else:
                                d_2[i]['{}'.format(m)] = 1
            Materia.append(d_2)

        print(Materia)




Method().main({'E27':['2651'],'E28':['2216']},['1700000','1900000'])
# Method().main({'E27':['2651'],'E28':['2216']},['0','1700000'])