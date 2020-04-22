import copy
import pymysql
import numpy




class Method:
    def lcc(self, sql):
        db = pymysql.connect("192.168.221.24", "root", "123456", port=23306, charset="utf8")
        # db = pymysql.connect("192.168.1.21", "root", "123456", charset="utf8")
        cur = db.cursor()
        cur.execute("use lcc")
        cur.execute(sql)
        a = cur.fetchall()
        return a

    def connect_darams_mileage(self, sql_execure_mileage):
        db = pymysql.connect("192.168.221.24", "root", "123456", port=23306, charset="utf8")
        cur = db.cursor()
        cur.execute("use darams")
        cur.execute(sql_execure_mileage)
        data = cur.fetchall()
        return data

    # 递归把工单号换成钱
    def deal(self,num,tree):
        d = num
        for i in tree:
            if len(tree[i]['工单号']) != 0:
                l_1 = tree[i]['工单号']
                tree[i]['工单号'] = 0
                for k in l_1:
                    if d[k] is not None:
                        tree[i]['工单号'] += d[k]
                if len(tree[i]['child']) == 0:
                    pass
                else:
                    self.deal(d, tree[i]['child'])
            else:
                tree[i]['工单号'] = 0
                self.deal(d,tree[i]['child'])

        return tree

    # 递归相加
    def deal_sum(self,tree,num):
        d = tree

        for j in d:
            if d[j]['工单号'] == 0:
                num = self.deal_sum(d[j]['child'],num)
            else:
                num += d[j]['工单号']
                num = self.deal_sum(d[j]['child'], num)
        return num

    # 得到下级子节点的值
    def tree_d(self,tree,L,level):
        d= {}
        if level < len(L):
            for i in tree:
                if i == L[level]:
                    if level == len(L) - 1:
                        d = tree[i]['child']
                    else:
                        d = self.tree_d(tree[i]['child'],L,level+1)
        return d

    # 得到工单
    def work_order(self,tree,L):
        for i in tree:
            if len(tree[i]['child']) != 0:
                if len(tree[i]['工单号']) != 0:
                    for j in tree[i]['工单号']:
                        L.append(j)
                L = self.work_order(tree[i]['child'],L)
            else:
                if len(tree[i]['工单号']) != 0:
                    for j in tree[i]['工单号']:
                        L.append(j)
        return L

    def work_order2(self,I_SQL,date,component):
        sql = '''
               SELECT
               h.work_order_no,
               h.fault_no
               FROM
               op_work_order_header h
               LEFT JOIN op_work_order_team te on te.work_order_no = h.work_order_no
               LEFT JOIN cd_team_base b on b.team_name = te.team_name    
               WHERE h.report_work_status != '已取消'          
               {}
               AND h.plan_begin_date >= '{}'      
               AND h.plan_begin_date < '{}'
               '''.format(I_SQL, date[0], date[1])

        re = self.lcc(sql)
        L = []
        d = {}

        if re.__len__() == 0:
            pass
        else:
            l_re = numpy.array(re)
            for i in l_re:
                L.append(i[1])
                d[i[0]] = i[1]
        # print(L)
        # print(d)

        tu = tuple(set(L))
        # print(tu)
        if tu.__len__() == 0:
            I_SQL1 = 'AND h.fault_no = {}'.format(tu[0])
        else:
            I_SQL1 = 'AND h.fault_no in {}'.format(tu)

        sql1 = '''
               select h.fault_no as 'faultNo',
               r.real_fault_object as 'realFaultObject'
               from op_fault_order_header h,op_train t,op_fault_order_detail d,op_fault_real r
               where d.fault_id = h.id
               and d.id = t.fault_detail_id
               and r.fault_detail_id = d.id
               {} 
               '''.format(I_SQL1)

        re1 = self.connect_darams_mileage(sql1)

        for j in re1:
            for j1 in d:
                if j[0] == d[j1]:
                    d[j1] = j[1]
        # print(d)
        d1 = {}
        for i in d:
            d2 = d1
            L = d[i].split('.')[1:]
            for j in L:
                if j in d2.keys():
                    if L.index(j) == len(L) - 1:

                        d2[j]['工单号'].append(i)
                    else:
                        d2 = d2[j]['child']
                else:
                    if L.index(j) == len(L) - 1:
                        d2[j] = {}
                        d2[j]['child'] = {}
                        d2[j]['工单号'] = [i]
                    else:
                        d2[j] = {}
                        d2[j]['child'] = {}
                        d2[j]['工单号'] = []
                        d2 = d2[j]['child']
        # print(d1)
        work_order = []

        for i in component:
            L = i.split('.')
            b = self.tree_d(d1, L, 0)

            c = self.work_order(b, [])
            work_order.append(c)
        return work_order

    def main(self,car,date):
        L1 = []
        if len(date[0]) <= 12:
            date[0] = date[0] + ' 00:00:00'
        if len(date[1]) <= 12:
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
            h.work_order_no,
            h.fault_no,
            te.duration * b.team_price AS "ManHourMoney",
            te.duration AS "ManHourNum"
            FROM
            op_work_order_header h
            LEFT JOIN op_work_order_team te on te.work_order_no = h.work_order_no
            LEFT JOIN cd_team_base b on b.team_name = te.team_name    
            WHERE h.report_work_status != '已取消'          
            {}
            AND h.plan_begin_date >= '{}'      
            AND h.plan_begin_date < '{}'
            '''.format(I_SQL,date[0],date[1])

        re = self.lcc(sql)
        L = []
        d = {}
        d_manhour = {}
        d_mannum = {}
        if re.__len__() == 0:
            pass
        else:
            l_re = numpy.array(re)
            for i in l_re:
                L.append(i[1])
                d[i[0]] = i[1]
                d_manhour[i[0]] = i[2]
                d_mannum[i[0]] = i[3]
        # print(L)
        # print(d)

        tu = tuple(list(set(L)))
        # print(tu)
        if tu.__len__() == 0:
            I_SQL1 = 'AND h.fault_no = {}'.format(tu[0])
        else:
            I_SQL1 = 'AND h.fault_no in {}'.format(tu)


        sql1 = '''
                select h.fault_no as 'faultNo',
                r.real_fault_object as 'realFaultObject'
                from op_fault_order_header h,op_train t,op_fault_order_detail d,op_fault_real r
                where d.fault_id = h.id
                and d.id = t.fault_detail_id
                and r.fault_detail_id = d.id
                {} 
                '''.format(I_SQL1)

        re1 = self.connect_darams_mileage(sql1)

        for j in re1:
            for j1 in d:
                if j[0] == d[j1]:
                    d[j1] = j[1]
        # print(d)
        d1 = {}
        for i in d:
            d2 = d1
            L = d[i].split('.')[1:]
            for j in L:
                if j in d2.keys():
                    if L.index(j) == len(L) - 1:

                        d2[j]['工单号'].append(i)
                    else:
                        d2 = d2[j]['child']
                else:
                    if L.index(j) == len(L) - 1:
                        d2[j] = {}
                        d2[j]['child'] = {}
                        d2[j]['工单号'] = [i]
                    else:
                        d2[j] = {}
                        d2[j]['child'] = {}
                        d2[j]['工单号'] = []
                        d2 = d2[j]['child']
        # print(d1)
        d_1 = copy.deepcopy(d1)
        a = self.deal(d_mannum,d_1)
        # print(a)
        d3 = {}
        for i in a:
            d3[i] = {}
            d3[i]['child1'] = self.deal_sum(a[i]['child'],0)
            for j in a[i]['child']:
              d3[i][j] =  self.deal_sum(a[i]['child'][j]['child'],0)
        print(d3)

        d_2 = copy.deepcopy(d1)
        b = self.deal(d_manhour,d_2)
        d4 = {}
        for i in b:
            d4[i] = {}
            d4[i]['child1'] = self.deal_sum(b[i]['child'],0)
            for j in b[i]['child']:
              d4[i][j] =  self.deal_sum(b[i]['child'][j]['child'],0)
        print(d4)

        sql1 = '''
                select 
                h.work_order_no,
                IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)* IF(d.material_deal_type = '出库', d.material_quantity, 0) AS "material_money",
                IF(d.material_deal_type = '出库', d.material_quantity, -d.material_quantity) AS "material_num"
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

        d_material = {}
        d_materialnum = {}
        if re1.__len__() == 0:
            pass
        else:
            l_re = numpy.array(re1)
            for i in l_re:
                if i[1] is not None:
                    if i[0] in d_material.keys():
                        d_material[i[0]] += i[1]
                    else:
                        d_material[i[0]] = i[1]

            for i in l_re:
                if i[2] is not None:
                    if i[0] in d_materialnum.keys():
                        d_materialnum[i[0]] += i[2]
                    else:
                        d_materialnum[i[0]] = i[2]

            d_3 = copy.deepcopy(d1)
            c = self.deal(d_material, d_3)
            # print(a)
            d5 = {}
            for i in c:
                d5[i] = {}
                d5[i]['child1'] = self.deal_sum(c[i]['child'], 0)
                for j in c[i]['child']:
                    d5[i][j] = self.deal_sum(c[i]['child'][j]['child'], 0)
            print(d5)

            d_4 = copy.deepcopy(d1)
            e = self.deal(d_materialnum, d_4)
            # print(a)
            d6 = {}
            for i in e:
                d6[i] = {}
                d6[i]['child1'] = self.deal_sum(e[i]['child'], 0)
                for j in e[i]['child']:
                    d6[i][j] = self.deal_sum(e[i]['child'][j]['child'], 0)
            print(d6)


    def main1(self,car,date,component):
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

        if component == 'all':
            sql = '''
                  select 
                  ifnull(concat(r.repair_level,""),"(空白)") AS "repairLevel",
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

            sql1 = '''
                    select 
                    ifnull(concat(r.repair_level,""),"(空白)") AS "repairLevel",
                    IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)* IF(d.material_deal_type = '出库', d.material_quantity, 0) AS "material_money"
                    from op_work_order_header h 
                    LEFT JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
                    LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
                    LEFT JOIN cd_materials_base e ON d.material_no = e.material_no
                    LEFT JOIN cd_materials_batch t ON d.material_no = t.material_no AND d.batch_no = t.batch_no
                    LEFT JOIN cd_materials_serial s ON d.material_no = s.material_no AND d.batch_no = s.batch_no AND d.serial_no = s.serial_no
                    WHERE h.report_work_status != '已取消'          
                    {}
                    AND h.plan_begin_date >= '{}'      
                    AND h.plan_begin_date < '{}'
                   '''.format(I_SQL, date[0], date[1])

        else:
            work_order = self.work_order2(I_SQL,date,component)

            new_work = []
            for go in work_order:
                for go_new in go:
                    new_work.append(go_new)
            # print(new_work)
            if len(new_work) <= 1:
                I_SQL1 = 'AND h.work_order_no = {}'.format(new_work[0])
            else:
                new_work = tuple(new_work)
                I_SQL1 = 'AND h.work_order_no in {}'.format(new_work)

            sql = '''
                  select 
                  ifnull(concat(r.repair_level,""),"(空白)") AS "repair_level",
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
                  {}
                  '''.format(I_SQL, date[0], date[1],I_SQL1)


            sql1 = '''
                    select 
                    ifnull(concat(r.repair_level,""),"(空白)") AS "repairLevel",
                    IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)* IF(d.material_deal_type = '出库', d.material_quantity, 0) AS "material_money"
                    from op_work_order_header h 
                    LEFT JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
                    LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
                    LEFT JOIN cd_materials_base e ON d.material_no = e.material_no
                    LEFT JOIN cd_materials_batch t ON d.material_no = t.material_no AND d.batch_no = t.batch_no
                    LEFT JOIN cd_materials_serial s ON d.material_no = s.material_no AND d.batch_no = s.batch_no AND d.serial_no = s.serial_no
                    WHERE h.report_work_status != '已取消'          
                    {}
                    AND h.plan_begin_date >= '{}'      
                    AND h.plan_begin_date < '{}'
                    {}
                   '''.format(I_SQL, date[0], date[1],I_SQL1)

        re = self.lcc(sql)

        Manhour = {}
        d_2 = {}
        if re.__len__() == 0:
            Manhour = {}
        else:
            l_re = numpy.array(re)
            l_re1 = l_re.T
            l_re2 = list(set(l_re1[0]))

            for i in l_re2:
                Manhour[i] = 0
                for j in l_re:
                    if j[0] == i:
                        if j[1] is not None:
                            Manhour[i] += j[1]

            for i in l_re2:
                d_2[i] = 0
                for j in l_re:
                    if j[0] == i:
                        d_2[i] += 1
        print(Manhour)
        print(d_2)

        re1 = self.lcc(sql1)
        Material = {}

        if re1.__len__() == 0:
            Material = {}
        else:
            l_re = numpy.array(re1)
            l_re1 = l_re.T
            l_re2 = list(set(l_re1[0]))

            for i in l_re2:
                Material[i] = 0
                for j in l_re:
                    if j[0] == i:
                        if j[1] is not None:
                            Material[i] += j[1]
        print(Material)


    def main2(self,car,date,component):
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

        if component == 'all':
            sql = '''
                 select 
                 h.fault_no AS 'fault_no',
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


            sql1 = '''
                   select 
                   h.fault_no AS 'fault_no',
                   IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)* IF(d.material_deal_type = '出库', d.material_quantity, 0) AS "material_money"
                   from op_work_order_header h 
                   LEFT JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
                   LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
                   LEFT JOIN cd_materials_base e ON d.material_no = e.material_no
                   LEFT JOIN cd_materials_batch t ON d.material_no = t.material_no AND d.batch_no = t.batch_no
                   LEFT JOIN cd_materials_serial s ON d.material_no = s.material_no AND d.batch_no = s.batch_no AND d.serial_no = s.serial_no
                   WHERE h.report_work_status != '已取消'          
                   {}
                   AND h.plan_begin_date >= '{}'      
                   AND h.plan_begin_date < '{}'
                  '''.format(I_SQL, date[0], date[1])


        else:
            work_order = self.work_order2(I_SQL,date,component)

            new_work = []
            for go in work_order:
                for go_new in go:
                    new_work.append(go_new)
            # print(new_work)
            if len(new_work) <= 1:
                I_SQL1 = 'AND h.work_order_no = {}'.format(new_work[0])
            else:
                new_work = tuple(new_work)
                I_SQL1 = 'AND h.work_order_no in {}'.format(new_work)

            sql = '''
                     select 
                     h.fault_no AS 'fault_no',
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
                     {}
                         '''.format(I_SQL, date[0], date[1], I_SQL1)

            sql1 = '''
                   select 
                   h.fault_no AS 'fault_no',
                   IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)* IF(d.material_deal_type = '出库', d.material_quantity, 0) AS "material_money"
                   from op_work_order_header h 
                   LEFT JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
                   LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
                   LEFT JOIN cd_materials_base e ON d.material_no = e.material_no
                   LEFT JOIN cd_materials_batch t ON d.material_no = t.material_no AND d.batch_no = t.batch_no
                   LEFT JOIN cd_materials_serial s ON d.material_no = s.material_no AND d.batch_no = s.batch_no AND d.serial_no = s.serial_no
                   WHERE h.report_work_status != '已取消'          
                   {}
                   AND h.plan_begin_date >= '{}'      
                   AND h.plan_begin_date < '{}'
                   {}
                  '''.format(I_SQL, date[0], date[1], I_SQL1)

        re = self.lcc(sql)
        Manhour = {}
        d_2 = {}
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
        print(d_2)

        re1 = self.lcc(sql1)
        Material = {}

        if re.__len__() == 0:
            Material = {}
        else:
            l_re = numpy.array(re1)

            for i in l_re:
                if i[1] is None:
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


    def main3(self,car,date,component):
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

        if component == 'all':
            sql = '''
                 select 
                 ifnull(r.repair_method,"(空白)") as "repair_method",
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

            sql1 = '''
                   select 
                   ifnull(r.repair_method,"(空白)") as "repair_method",
                   IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)* IF(d.material_deal_type = '出库', d.material_quantity, 0) AS "material_money"
                   from op_work_order_header h 
                   LEFT JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
                   LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
                   LEFT JOIN cd_materials_base e ON d.material_no = e.material_no
                   LEFT JOIN cd_materials_batch t ON d.material_no = t.material_no AND d.batch_no = t.batch_no
                   LEFT JOIN cd_materials_serial s ON d.material_no = s.material_no AND d.batch_no = s.batch_no AND d.serial_no = s.serial_no
                   WHERE h.report_work_status != '已取消'          
                   {}
                   AND h.plan_begin_date >= '{}'      
                   AND h.plan_begin_date < '{}'
                  '''.format(I_SQL, date[0], date[1])

        else:
            work_order = self.work_order2(I_SQL, date, component)

            new_work = []
            for go in work_order:
                for go_new in go:
                    new_work.append(go_new)
            # print(new_work)
            if len(new_work) <= 1:
                I_SQL1 = 'AND h.work_order_no = {}'.format(new_work[0])
            else:
                new_work = tuple(new_work)
                I_SQL1 = 'AND h.work_order_no in {}'.format(new_work)

            sql = '''
                 select 
                 ifnull(r.repair_method,"(空白)") as "repair_method",
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
                 {}
                 '''.format(I_SQL, date[0], date[1], I_SQL1)

            sql1 = '''
                   select 
                   ifnull(r.repair_method,"(空白)") as "repair_method",
                   IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)* IF(d.material_deal_type = '出库', d.material_quantity, 0) AS "material_money"
                   from op_work_order_header h 
                   LEFT JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
                   LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
                   LEFT JOIN cd_materials_base e ON d.material_no = e.material_no
                   LEFT JOIN cd_materials_batch t ON d.material_no = t.material_no AND d.batch_no = t.batch_no
                   LEFT JOIN cd_materials_serial s ON d.material_no = s.material_no AND d.batch_no = s.batch_no AND d.serial_no = s.serial_no
                   WHERE h.report_work_status != '已取消'          
                   {}
                   AND h.plan_begin_date >= '{}'      
                   AND h.plan_begin_date < '{}'
                   {}
                  '''.format(I_SQL, date[0], date[1], I_SQL1)

        re = self.lcc(sql)

        Manhour = {}
        d_2 = {}
        if re.__len__() == 0:
            Manhour = {}
        else:
            l_re = numpy.array(re)
            l_re1 = l_re.T
            l_re2 = list(set(l_re1[0]))

            for i in l_re2:
                Manhour[i] = 0
                for j in l_re:
                    if j[0] == i:
                        if j[1] is not None:
                            Manhour[i] += j[1]

            for i in l_re2:
                d_2[i] = 0
                for j in l_re:
                    if j[0] == i:
                        d_2[i] += 1
        print(Manhour)
        print(d_2)

        re1 = self.lcc(sql1)
        Material = {}

        if re1.__len__() == 0:
            Material = {}
        else:
            l_re = numpy.array(re1)
            l_re1 = l_re.T
            l_re2 = list(set(l_re1[0]))

            for i in l_re2:
                Material[i] = 0
                for j in l_re:
                    if j[0] == i:
                        if j[1] is not None:
                            Material[i] += j[1]
        print(Material)

    def main4(self,car,date,component):
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

        if component == 'all':
            sql = '''
                SELECT
                h.work_order_no,
                mt.produce_manufacturer,
                d.material_quantity AS "material_num",
                te.duration * b.team_price AS "ManHourMoney"
                FROM
                op_work_order_header h
                LEFT JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
                LEFT JOIN op_work_order_team te ON te.work_order_no = h.work_order_no
                LEFT JOIN cd_team_base b ON te.team_name = b.team_name
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

            sql1 = '''
                  select 
                  mt.produce_manufacturer,
                  IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)* IF(d.material_deal_type = '出库', d.material_quantity, 0) AS "material_money"
                  from op_work_order_header h 
                  LEFT JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
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
        else:
            work_order = self.work_order2(I_SQL, date, component)
            # print(work_order)
            new_work = []
            for go in work_order:
                for go_new in go:
                    new_work.append(go_new)
            if len(new_work) == 0:
                return
            else:
                if len(new_work) == 1:
                    I_SQL1 = 'AND h.work_order_no = \'{}\''.format(new_work[0])
                else:
                    new_work = tuple(new_work)
                    I_SQL1 = 'AND h.work_order_no in {}'.format(new_work)
            sql = '''
                    SELECT
                    h.work_order_no,
                    mt.produce_manufacturer,
                    d.material_quantity AS "material_num",
                    te.duration * b.team_price AS "ManHourMoney"
                    FROM
                    op_work_order_header h
                    LEFT JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
                    LEFT JOIN op_work_order_team te ON te.work_order_no = h.work_order_no
                    LEFT JOIN cd_team_base b ON te.team_name = b.team_name
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
                    {}
                    '''.format(I_SQL, date[0], date[1],I_SQL1)

            sql1 = '''
                  select 
                  mt.produce_manufacturer,
                  IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)* IF(d.material_deal_type = '出库', d.material_quantity, 0) AS "material_money"
                  from op_work_order_header h 
                  LEFT JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
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
                  {}
                 '''.format(I_SQL, date[0], date[1],I_SQL1)

        re = self.lcc(sql)

        Manhour = {}

        if re.__len__() == 0:
            Manhour = {}
        else:
            l_re = numpy.array(re)
            l_re1 = l_re.T
            l_re2 = list(set(l_re1[1]))
            d = {}
            for k in l_re:
                if k[0] in d.keys():
                    d[k[0]] += k[2]
                else:
                    d[k[0]] = k[2]
            print(d)

            for i in l_re2:
                Manhour[i] = 0
                for j in l_re:
                    if j[3] is not None:
                        if j[1] == i:
                            Manhour[i] += j[3] * (j[2]/d[j[0]])

        print(Manhour)

        re1 = self.lcc(sql1)
        Material = {}

        if re1.__len__() == 0:
            Material = {}
        else:
            l_re = numpy.array(re1)
            l_re1 = l_re.T
            l_re2 = list(set(l_re1[0]))

            for i in l_re2:
                Material[i] = 0
                for j in l_re:
                    if j[0] == i:
                        if j[1] is not None:
                            Material[i] += j[1]
        print(Material)

        L_sum = copy.deepcopy(Manhour)
        for i in Material:
            if i in L_sum:
                L_sum[i] += Material[i]
            else:
                L_sum[i] = Material[i]


        b = sorted(L_sum.items(), key=lambda item: item[1], reverse=True)
        if len(b) <= 10:
            print(b)
        else:
            b = b[:10]
            print(b)



# Method().main2({'E27':['2641']},['2017-02-03','2017-08-02'],'all')
Method().main4({'E27':['2641']},['2017-02-03','2017-08-03'],['内装系统','转向架.轮对轴箱组成'])
# Method().main({'E27':['2641']},['2017-02-03','2017-08-02'])
# Method().main1({'E27':['2641']},['2017-02-03','2017-08-03'],['辅助供电系统'])