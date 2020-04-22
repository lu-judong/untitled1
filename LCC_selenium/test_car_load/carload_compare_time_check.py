import datetime
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

    def main(self, car, date):
        L1 = []

        date[0] = datetime.datetime.strftime(date[0], '%Y-%m-%d %H:%M:%S')

        # if len(date[1]) <= 12:
        #     date[1] = date[1] + ' 23:59:59'
        date[1] = datetime.datetime.strftime(date[1], '%Y-%m-%d %H:%M:%S')

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
               te.duration * b.team_price AS "manhour_money"
               from 
               op_work_order_header h
               LEFT JOIN op_work_order_team te on te.work_order_no = h.work_order_no
               LEFT JOIN cd_team_base b on b.team_name = te.team_name
               WHERE h.report_work_status != '已取消'          
               {}
               AND h.plan_begin_date >= '{}'      
               AND h.plan_begin_date < '{}'
               '''.format(I_SQL, date[0], date[1])

        re = self.lcc(sql)
        Manhour = 0
        if re.__len__() == 0:
            Manhour = 0
        else:
            l_re = numpy.array(re)
            for i in l_re:
                if i[0] is None:
                    pass
                else:
                    Manhour += i[0]
        # print(Manhour)

        sql1 = '''
                select 
                IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)* IF(d.material_deal_type = '出库', d.material_quantity, 0) AS "material_money"
                from op_work_order_header h 
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

        Material = 0
        if re.__len__() == 0:
            Material = 0
        else:
            l_re = numpy.array(re1)
            for i in l_re:
                if i[0] is None:
                    pass
                else:
                    Material += i[0]
        # print(Material)
        d_sum = Manhour + Material
        L = []
        L.append(Manhour)
        L.append(Material)
        L.append(d_sum)
        return L

    def main1(self,car,date):
        L = []
        L1 = []

        date[0] = datetime.datetime.strftime(date[0], '%Y-%m-%d %H:%M:%S')

        # if len(date[1]) <= 12:
        #     date[1] = date[1] + ' 23:59:59'
        date[1] = datetime.datetime.strftime(date[1], '%Y-%m-%d %H:%M:%S')

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

        # print(Manhour)
        L.append(Manhour)

        sql1 = '''
              SELECT
              h.fault_no AS 'fault_no',
              IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)* IF(d.material_deal_type = '出库', d.material_quantity, -d.material_quantity) AS "material_money"
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

        # print(Material)
        L.append(Material)
        L_sum = copy.deepcopy(Manhour)

        for i in Material:
            if i in L_sum.keys():
                L_sum[i] += Material[i]
            else:
                L_sum[i] = Material[i]

        L.append(L_sum)

        return L

    def run(self,car,date):
        L = []
        L1 = []
        L2 = []

        mon_start = datetime.datetime.strptime(date[0], '%Y-%m-%d')
        L.append(mon_start)
        while True:
            if mon_start < datetime.datetime.strptime(date[1], '%Y-%m-%d'):
                if mon_start.month < 12:
                    L.append(datetime.datetime(mon_start.year, mon_start.month + 1, 1))
                    mon_start = datetime.datetime(mon_start.year, mon_start.month + 1, 1)
                else:
                    mo = mon_start.year + 1
                    L.append(datetime.datetime(mo, 1, 1))
                    mon_start = datetime.datetime(mo, 1, 1)

            else:
                L[-1] = datetime.datetime.strptime(date[1], '%Y-%m-%d') + datetime.timedelta(days=1)
                break
        # print(L)

        for j in L:
            if L.index(j) < len(L) - 1:
                num = self.main(car, [j,L[L.index(j)+1]])
                L1.append(num)
                num1 = self.main1(car, [j,L[L.index(j)+1]])
                L2.append(num1)
        print(L1)
        print(L2)

Check().run({'E27':['2651'],'E28':['2216']},['2017-03-02','2017-05-08'])