import pymysql
import numpy
import copy

class Method:
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
             h.fault_no,
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

        Manhour = {}
        if re.__len__() == 0:
            Manhour = {}
        else:
            for i in re:
                if i[1] is not None:
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

        print(Manhour)


        sql1 = '''
                select 
                h.fault_no,
                IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)* IF(d.material_deal_type = '出库', d.material_quantity, 0) AS "material_money"
                from op_work_order_header h 
                LEFT JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
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
            for i in re1:
                if i[1] is not None:
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
        sum = copy.deepcopy(Manhour)
        for i in Material:
            if i in sum.keys():
                sum[i] += Material[i]
            else:
                sum[i] = Material[i]

        print(sum)


Method().main({'E28':['2216'],'E27':['2651']},['2017-03-01','2017-08-03'])