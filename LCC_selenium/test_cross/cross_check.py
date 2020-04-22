import copy
import pymysql
import pandas
from sqlalchemy import create_engine
import numpy
import math


class Method:
    def lcc(self, sql):
        # db = pymysql.connect("192.168.221.24", "root", "123456", port=23306, charset="utf8")
        db = pymysql.connect("192.168.221.21", "root", "123456", charset="utf8")
        cur = db.cursor()
        cur.execute("use lcc")
        cur.execute(sql)
        a = cur.fetchall()
        return a

    def connect_darams_mileage(self, sql_execure_mileage,):
        # db = pymysql.connect("192.168.221.24", "root", "123456", port=23306, charset="utf8")
        db = pymysql.connect("192.168.221.21", "root", "123456", charset="utf8")
        cur = db.cursor()
        cur.execute("use darams")
        cur.execute(sql_execure_mileage)
        data = cur.fetchall()
        return data


    def main(self,car,date,value,value1):
        # 连接darams库
        darams = create_engine('mysql+pymysql://root:123456@192.168.221.21:3306/darams')
        # 连接lcc库
        lcc = create_engine('mysql+pymysql://root:123456@192.168.221.21:3306/lcc')

        L1 = []
        if len(date[0]) <= 12:
            date[0] = date[0] + ' 00:00:00'
        if len(date[1]) <= 12:
            date[1] = date[1] + ' 00:00:00'

        for i in car:
            for j in car[i]:
                L1.append(j)
        if len(L1) <= 1:
            I_SQL = 'AND h.train_no = \'{}\''.format(L1[0])
            I_SQL1 = 'n.train_no = \'{}\''.format(L1[0])
        else:
            L1 = tuple(L1)
            I_SQL = 'AND h.train_no in {}'.format(L1)
            I_SQL1 = 'n.train_no in {}'.format(L1)

        sql = '''
                select
                n.train_no,
                a.company AS company
                from
                cd_train_no n
                INNER JOIN cd_train_real_time r on n.id = r.train_no_id
                INNER JOIN cd_affiliated  a on r.id = a.train_real_time_id
                where 
                {}
            '''.format(I_SQL1)

        sql1 = '''
                SELECT
                h.work_order_no,
                h.fault_no,
                h.train_no,
                h.train_type AS 'train_type',
                ifnull(concat(r.repair_level,""),"(空白)") AS "repairLevel",
                mt.produce_manufacturer,
                substring_index(if(substring_index(r.repair_location, '.', 3) = substring_index(r.repair_location, '.', 2),null,substring_index(r.repair_location, '.', 3)
        ),'.' ,- 1) AS "repairLocation",
                date_format(h.plan_begin_date,'%%Y-%%m') AS "date",
                d.material_quantity AS "material_num",
                te.duration * b.team_price AS "ManHourMoney",
                IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)* IF(d.material_deal_type = '出库', d.material_quantity, 0) AS "material_money"
                from op_work_order_header h 
                LEFT JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
                LEFT JOIN op_work_order_team te ON te.work_order_no = h.work_order_no
                LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
                LEFT JOIN cd_materials_base e ON d.material_no = e.material_no
                LEFT JOIN cd_team_base b on b.team_name = te.team_name
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

        lcc_re = self.lcc(sql1)

        Mannum = {}
        fault_no = []
        if lcc_re.__len__() == 0:
            Mannum = {}
            fault_no = []
        else:
            l_re = numpy.array(lcc_re)
            for i in l_re:
                if i[0] is None:
                    pass
                else:
                    if i[-3] is not None:
                        if i[0] in Mannum.keys():
                            Mannum[i[0]] += i[-3]
                        else:
                            Mannum[i[0]] = i[-3]

            for j in l_re:
                if j[1] is not None:
                    fault_no.append(j[1])

        tu = tuple(list(set(fault_no)))
        # print(tu)
        if tu.__len__() == 0:
            I_SQL2 = 'AND h.fault_no = \'{}\''.format(tu[0])
        else:
            I_SQL2 = 'AND h.fault_no in {}'.format(tu)

        sql2 = '''
                select h.fault_no as 'faultNo',
                r.real_fault_object as 'realFaultObject'
                from op_fault_order_header h,op_train t,op_fault_order_detail d,op_fault_real r
                where d.fault_id = h.id
                and d.id = t.fault_detail_id
                and r.fault_detail_id = d.id
                {} 
                '''.format(I_SQL2)

        darams_re = self.connect_darams_mileage(sql2)

        darams_d = {}
        for i in darams_re:
            if len(i[1].split('.')) >= 2:
                a = i[1].split('.')[1:3]
                a1 = '.'.join(a)
                darams_d[i[0]] = a1

        # 将darams数据库查出来的数据与lcc数据库查出来的数据相拼接
        df = pandas.read_sql_query(sql, darams)

        de = pandas.read_sql_query(sql1, lcc)

        res = pandas.merge(df, de, on='train_no', how='right')

        res1 = numpy.array(res)
        res2 = res1.tolist()
        res3 = copy.deepcopy(res2)
        # print(res2[0])
        for i in res3:
            if i[2] in Mannum.keys():
                if math.isnan(i[-3]) is False and math.isnan(i[-2]) is False:
                    if i[-2] is not None and Mannum[i[2]] != 0 :
                        i[-2] = (i[-3] / float(Mannum[i[2]])) * float(i[-2])

        for i in res3:
            if i[3] is not None:
                if i[3] in darams_d.keys():
                    i[3] = darams_d[i[3]]

        # print(res2)
        # print(res3)
        # print(res3)

        senior_map = {}

        car_map = {}
        tech_map = {}
        supplier_manhour_list = []
        supplier_material_list = []
        supplier_sum_list = []
        supplier_manhour_map = {}
        supplier_material_map = {}
        component_map = {}
        repairlocation_manhour_list = []
        repairlocation_material_list = []
        repairlocation_sum_list = []
        repairlocation_manhour_map = {}
        repairlocation_material_map = {}


        railway_map = {}
        date_map = {}

        if value == '高级修':
            for i in res3:
                if math.isnan(i[-2]) is False:
                    if i[5] in senior_map.keys():
                        senior_map[i[5]][0] += i[-2]
                        senior_map[i[5]][1] += i[-1]
                        senior_map[i[5]][2] += i[-1] + i[-2]
                    else:
                        senior_map[i[5]] = [0,0,0]
                        senior_map[i[5]][0] = i[-2]
                        senior_map[i[5]][1] = i[-1]
                        senior_map[i[5]][2] = i[-1] + i[-2]
                    if value1 == '':
                        pass
                    else:
                        if i[5] == value1:
                            if i[4] in car_map.keys():
                                car_map[i[4]][0] += i[-2]
                                car_map[i[4]][1] += i[-1]
                                car_map[i[4]][2] += i[-1] + i[-2]
                            else:
                                car_map[i[4]] = [0, 0, 0]
                                car_map[i[4]][0] = i[-2]
                                car_map[i[4]][1] = i[-1]
                                car_map[i[4]][2] = i[-1] + i[-2]

                            if i[3] is not None:
                                if '修复性维修' in tech_map.keys():
                                    tech_map['修复性维修'][0] += i[-2]
                                    tech_map['修复性维修'][1] += i[-1]
                                    tech_map['修复性维修'][2] += i[-2] + i[-1]
                                else:
                                    tech_map['修复性维修'] = [0, 0, 0]
                                    tech_map['修复性维修'][0] = i[-2]
                                    tech_map['修复性维修'][1] = i[-1]
                                    tech_map['修复性维修'][2] = i[-2] + i[-1]

                                if len(i[3].split('.')) == 2:
                                    if i[3].split('.')[0] in component_map.keys():
                                        component_map[i[3].split('.')[0]][0][0] += i[-2]
                                        component_map[i[3].split('.')[0]][0][1] += i[-1]
                                        component_map[i[3].split('.')[0]][0][2] += i[-2] + i[-1]
                                    else:
                                        component_map[i[3].split('.')[0]] = [[], {}]
                                        component_map[i[3].split('.')[0]][0] = [0, 0, 0]
                                        component_map[i[3].split('.')[0]][0][0] = i[-2]
                                        component_map[i[3].split('.')[0]][0][1] = i[-1]
                                        component_map[i[3].split('.')[0]][0][2] = i[-2] + i[-1]
                                        component_map[i[3].split('.')[0]][1]['children'] = {}

                                    if i[3].split('.')[1] in component_map[i[3].split('.')[0]][1]['children'].keys():
                                        component_map[i[3].split('.')[0]][1]['children'][i[3].split('.')[1]][0] += i[-2]
                                        component_map[i[3].split('.')[0]][1]['children'][i[3].split('.')[1]][1] += i[-1]
                                        component_map[i[3].split('.')[0]][1]['children'][i[3].split('.')[1]][2] += i[-1] + i[-2]
                                    else:
                                        component_map[i[3].split('.')[0]][1]['children'][i[3].split('.')[1]] = [0, 0, 0]
                                        component_map[i[3].split('.')[0]][1]['children'][i[3].split('.')[1]][0] = i[-2]
                                        component_map[i[3].split('.')[0]][1]['children'][i[3].split('.')[1]][1] = i[-1]
                                        component_map[i[3].split('.')[0]][1]['children'][i[3].split('.')[1]][2] = i[-1] + i[-2]
                                else:
                                    if i[3].split('.')[0] in component_map.keys():
                                        component_map[i[3].split('.')[0]][0][0] += i[-2]
                                        component_map[i[3].split('.')[0]][0][1] += i[-1]
                                        component_map[i[3].split('.')[0]][0][2] += i[-2] + i[-1]
                                    else:
                                        component_map[i[3].split('.')[0]] = [[], {}]
                                        component_map[i[3].split('.')[0]][0] = [0, 0, 0]
                                        component_map[i[3].split('.')[0]][0][0] = i[-2]
                                        component_map[i[3].split('.')[0]][0][1] = i[-1]
                                        component_map[i[3].split('.')[0]][0][2] = i[-2] + i[-1]
                            else:
                                if '预防性维修' in tech_map.keys():
                                    tech_map['预防性维修'][0] += i[-2]
                                    tech_map['预防性维修'][1] += i[-1]
                                    tech_map['预防性维修'][2] += i[-2] + i[-1]
                                else:
                                    tech_map['预防性维修'] = [0, 0, 0]
                                    tech_map['预防性维修'][0] = i[-2]
                                    tech_map['预防性维修'][1] = i[-1]
                                    tech_map['预防性维修'][2] = i[-2] + i[-1]


                            if i[6] is not None:
                                if i[6] in supplier_manhour_map.keys():
                                    supplier_manhour_map[i[6]] += i[-2]
                                else:
                                    supplier_manhour_map[i[6]] = i[-2]

                                if i[6] in supplier_material_map.keys():
                                    supplier_material_map[i[6]] += i[-1]
                                else:
                                    supplier_material_map[i[6]] = i[-1]

                            if i[7] is not None:
                                if i[7] in repairlocation_manhour_map.keys():
                                    repairlocation_manhour_map[i[7]] += i[-2]
                                else:
                                    repairlocation_manhour_map[i[7]] = i[-2]

                                if i[7] in repairlocation_material_map.keys():
                                    repairlocation_material_map[i[7]] += i[-1]
                                else:
                                    repairlocation_material_map[i[7]] = i[-1]

                            if i[1] is not None:
                                if i[1] in railway_map.keys():
                                    railway_map[i[1]][0] += i[-2]
                                    railway_map[i[1]][1] += i[-1]
                                    railway_map[i[1]][2] += i[-1] + i[-2]
                                else:
                                    railway_map[i[1]] = [0, 0, 0]
                                    railway_map[i[1]][0] = i[-2]
                                    railway_map[i[1]][1] = i[-1]
                                    railway_map[i[1]][2] = i[-1] + i[-2]

                            if i[8] is not None:
                                if i[8] in date_map.keys():
                                    date_map[i[8]][0] += i[-2]
                                    date_map[i[8]][1] += i[-1]
                                    date_map[i[8]][2] += i[-1] + i[-2]
                                else:
                                    date_map[i[8]] = [0,0,0]
                                    date_map[i[8]][0] = i[-2]
                                    date_map[i[8]][1] = i[-1]
                                    date_map[i[8]][2] = i[-1] + i[-2]

        elif value == '车型':
            for i in res3:
                if math.isnan(i[-2]) is False:
                    if i[4] in car_map.keys():
                        car_map[i[4]][0] += i[-2]
                        car_map[i[4]][1] += i[-1]
                        car_map[i[4]][2] += i[-1] + i[-2]
                    else:
                        car_map[i[4]] = [0, 0, 0]
                        car_map[i[4]][0] = i[-2]
                        car_map[i[4]][1] = i[-1]
                        car_map[i[4]][2] = i[-1] + i[-2]
                    if value1 == '':
                        pass
                    else:
                        if i[4] == value1:
                            if i[5] in senior_map.keys():
                                senior_map[i[5]][0] += i[-2]
                                senior_map[i[5]][1] += i[-1]
                                senior_map[i[5]][2] += i[-1] + i[-2]
                            else:
                                senior_map[i[5]] = [0, 0, 0]
                                senior_map[i[5]][0] = i[-2]
                                senior_map[i[5]][1] = i[-1]
                                senior_map[i[5]][2] = i[-1] + i[-2]
                            if i[3] is not None:
                                if '修复性维修' in tech_map.keys():
                                    tech_map['修复性维修'][0] += i[-2]
                                    tech_map['修复性维修'][1] += i[-1]
                                    tech_map['修复性维修'][2] += i[-2] + i[-1]
                                else:
                                    tech_map['修复性维修'] = [0, 0, 0]
                                    tech_map['修复性维修'][0] = i[-2]
                                    tech_map['修复性维修'][1] = i[-1]
                                    tech_map['修复性维修'][2] = i[-2] + i[-1]

                                if len(i[3].split('.')) == 2:
                                    if i[3].split('.')[0] in component_map.keys():
                                        component_map[i[3].split('.')[0]][0][0] += i[-2]
                                        component_map[i[3].split('.')[0]][0][1] += i[-1]
                                        component_map[i[3].split('.')[0]][0][2] += i[-2] + i[-1]
                                    else:
                                        component_map[i[3].split('.')[0]] = [[], {}]
                                        component_map[i[3].split('.')[0]][0] = [0, 0, 0]
                                        component_map[i[3].split('.')[0]][0][0] = i[-2]
                                        component_map[i[3].split('.')[0]][0][1] = i[-1]
                                        component_map[i[3].split('.')[0]][0][2] = i[-2] + i[-1]
                                        component_map[i[3].split('.')[0]][1]['children'] = {}

                                    if i[3].split('.')[1] in component_map[i[3].split('.')[0]][1]['children'].keys():
                                        component_map[i[3].split('.')[0]][1]['children'][i[3].split('.')[1]][0] += i[-2]
                                        component_map[i[3].split('.')[0]][1]['children'][i[3].split('.')[1]][1] += i[-1]
                                        component_map[i[3].split('.')[0]][1]['children'][i[3].split('.')[1]][2] += i[-1] + i[-2]
                                    else:
                                        component_map[i[3].split('.')[0]][1]['children'][i[3].split('.')[1]] = [0, 0, 0]
                                        component_map[i[3].split('.')[0]][1]['children'][i[3].split('.')[1]][0] = i[-2]
                                        component_map[i[3].split('.')[0]][1]['children'][i[3].split('.')[1]][1] = i[-1]
                                        component_map[i[3].split('.')[0]][1]['children'][i[3].split('.')[1]][2] = i[-1] + i[-2]
                                else:
                                    if i[3].split('.')[0] in component_map.keys():
                                        component_map[i[3].split('.')[0]][0][0] += i[-2]
                                        component_map[i[3].split('.')[0]][0][1] += i[-1]
                                        component_map[i[3].split('.')[0]][0][2] += i[-2] + i[-1]
                                    else:
                                        component_map[i[3].split('.')[0]] = [[], {}]
                                        component_map[i[3].split('.')[0]][0] = [0, 0, 0]
                                        component_map[i[3].split('.')[0]][0][0] = i[-2]
                                        component_map[i[3].split('.')[0]][0][1] = i[-1]
                                        component_map[i[3].split('.')[0]][0][2] = i[-2] + i[-1]
                            else:
                                if '预防性维修' in tech_map.keys():
                                    tech_map['预防性维修'][0] += i[-2]
                                    tech_map['预防性维修'][1] += i[-1]
                                    tech_map['预防性维修'][2] += i[-2] + i[-1]
                                else:
                                    tech_map['预防性维修'] = [0, 0, 0]
                                    tech_map['预防性维修'][0] = i[-2]
                                    tech_map['预防性维修'][1] = i[-1]
                                    tech_map['预防性维修'][2] = i[-2] + i[-1]

                            if i[6] is not None:
                                if i[6] in supplier_manhour_map.keys():
                                    supplier_manhour_map[i[6]] += i[-2]
                                else:
                                    supplier_manhour_map[i[6]] = i[-2]

                                if i[6] in supplier_material_map.keys():
                                    supplier_material_map[i[6]] += i[-1]
                                else:
                                    supplier_material_map[i[6]] = i[-1]

                            if i[7] is not None:
                                if i[7] in repairlocation_manhour_map.keys():
                                    repairlocation_manhour_map[i[7]] += i[-2]
                                else:
                                    repairlocation_manhour_map[i[7]] = i[-2]

                                if i[7] in repairlocation_material_map.keys():
                                    repairlocation_material_map[i[7]] += i[-1]
                                else:
                                    repairlocation_material_map[i[7]] = i[-1]

                            if i[1] is not None:
                                if i[1] in railway_map.keys():
                                    railway_map[i[1]][0] += i[-2]
                                    railway_map[i[1]][1] += i[-1]
                                    railway_map[i[1]][2] += i[-1] + i[-2]
                                else:
                                    railway_map[i[1]] = [0, 0, 0]
                                    railway_map[i[1]][0] = i[-2]
                                    railway_map[i[1]][1] = i[-1]
                                    railway_map[i[1]][2] = i[-1] + i[-2]

                            if i[8] is not None:
                                if i[8] in date_map.keys():
                                    date_map[i[8]][0] += i[-2]
                                    date_map[i[8]][1] += i[-1]
                                    date_map[i[8]][2] += i[-1] + i[-2]
                                else:
                                    date_map[i[8]] = [0,0,0]
                                    date_map[i[8]][0] = i[-2]
                                    date_map[i[8]][1] = i[-1]
                                    date_map[i[8]][2] = i[-1] + i[-2]

        elif value == '维修方法':
            for i in res3:
                if math.isnan(i[-2]) is False:
                    if i[3] is not None:
                        if '修复性维修' in tech_map.keys():
                            tech_map['修复性维修'][0] += i[-2]
                            tech_map['修复性维修'][1] += i[-1]
                            tech_map['修复性维修'][2] += i[-2] + i[-1]
                        else:
                            tech_map['修复性维修'] = [0, 0, 0]
                            tech_map['修复性维修'][0] = i[-2]
                            tech_map['修复性维修'][1] = i[-1]
                            tech_map['修复性维修'][2] = i[-2] + i[-1]
                    else:
                        if '预防性维修' in tech_map.keys():
                            tech_map['预防性维修'][0] += i[-2]
                            tech_map['预防性维修'][1] += i[-1]
                            tech_map['预防性维修'][2] += i[-2] + i[-1]
                        else:
                            tech_map['预防性维修'] = [0, 0, 0]
                            tech_map['预防性维修'][0] = i[-2]
                            tech_map['预防性维修'][1] = i[-1]
                            tech_map['预防性维修'][2] = i[-2] + i[-1]
                    if value1 == '':
                        pass
                    elif value1 == '修复性维修':
                        if i[3] is not None:
                            if i[5] in senior_map.keys():
                                senior_map[i[5]][0] += i[-2]
                                senior_map[i[5]][1] += i[-1]
                                senior_map[i[5]][2] += i[-1] + i[-2]
                            else:
                                senior_map[i[5]] = [0, 0, 0]
                                senior_map[i[5]][0] = i[-2]
                                senior_map[i[5]][1] = i[-1]
                                senior_map[i[5]][2] = i[-1] + i[-2]

                            if i[4] in car_map.keys():
                                car_map[i[4]][0] += i[-2]
                                car_map[i[4]][1] += i[-1]
                                car_map[i[4]][2] += i[-1] + i[-2]
                            else:
                                car_map[i[4]] = [0, 0, 0]
                                car_map[i[4]][0] = i[-2]
                                car_map[i[4]][1] = i[-1]
                                car_map[i[4]][2] = i[-1] + i[-2]

                            if len(i[3].split('.')) == 2:
                                if i[3].split('.')[0] in component_map.keys():
                                    component_map[i[3].split('.')[0]][0][0] += i[-2]
                                    component_map[i[3].split('.')[0]][0][1] += i[-1]
                                    component_map[i[3].split('.')[0]][0][2] += i[-2] + i[-1]
                                else:
                                    component_map[i[3].split('.')[0]] = [[], {}]
                                    component_map[i[3].split('.')[0]][0] = [0, 0, 0]
                                    component_map[i[3].split('.')[0]][0][0] = i[-2]
                                    component_map[i[3].split('.')[0]][0][1] = i[-1]
                                    component_map[i[3].split('.')[0]][0][2] = i[-2] + i[-1]
                                    component_map[i[3].split('.')[0]][1]['children'] = {}

                                if i[3].split('.')[1] in component_map[i[3].split('.')[0]][1]['children'].keys():
                                    component_map[i[3].split('.')[0]][1]['children'][i[3].split('.')[1]][0] += i[-2]
                                    component_map[i[3].split('.')[0]][1]['children'][i[3].split('.')[1]][1] += i[-1]
                                    component_map[i[3].split('.')[0]][1]['children'][i[3].split('.')[1]][2] += i[-1] + i[-2]
                                else:
                                    component_map[i[3].split('.')[0]][1]['children'][i[3].split('.')[1]] = [0, 0, 0]
                                    component_map[i[3].split('.')[0]][1]['children'][i[3].split('.')[1]][0] = i[-2]
                                    component_map[i[3].split('.')[0]][1]['children'][i[3].split('.')[1]][1] = i[-1]
                                    component_map[i[3].split('.')[0]][1]['children'][i[3].split('.')[1]][2] = i[-1] + i[-2]
                            else:
                                if i[3].split('.')[0] in component_map.keys():
                                    component_map[i[3].split('.')[0]][0][0] += i[-2]
                                    component_map[i[3].split('.')[0]][0][1] += i[-1]
                                    component_map[i[3].split('.')[0]][0][2] += i[-2] + i[-1]
                                else:
                                    component_map[i[3].split('.')[0]] = [[], {}]
                                    component_map[i[3].split('.')[0]][0] = [0, 0, 0]
                                    component_map[i[3].split('.')[0]][0][0] = i[-2]
                                    component_map[i[3].split('.')[0]][0][1] = i[-1]
                                    component_map[i[3].split('.')[0]][0][2] = i[-2] + i[-1]

                            if i[6] is not None:
                                if i[6] in supplier_manhour_map.keys():
                                    supplier_manhour_map[i[6]] += i[-2]
                                else:
                                    supplier_manhour_map[i[6]] = i[-2]

                                if i[6] in supplier_material_map.keys():
                                    supplier_material_map[i[6]] += i[-1]
                                else:
                                    supplier_material_map[i[6]] = i[-1]

                            if i[7] is not None:
                                if i[7] in repairlocation_manhour_map.keys():
                                    repairlocation_manhour_map[i[7]] += i[-2]
                                else:
                                    repairlocation_manhour_map[i[7]] = i[-2]

                                if i[7] in repairlocation_material_map.keys():
                                    repairlocation_material_map[i[7]] += i[-1]
                                else:
                                    repairlocation_material_map[i[7]] = i[-1]

                            if i[1] is not None:
                                if i[1] in railway_map.keys():
                                    railway_map[i[1]][0] += i[-2]
                                    railway_map[i[1]][1] += i[-1]
                                    railway_map[i[1]][2] += i[-1] + i[-2]
                                else:
                                    railway_map[i[1]] = [0, 0, 0]
                                    railway_map[i[1]][0] = i[-2]
                                    railway_map[i[1]][1] = i[-1]
                                    railway_map[i[1]][2] = i[-1] + i[-2]

                            if i[8] is not None:
                                if i[8] in date_map.keys():
                                    date_map[i[8]][0] += i[-2]
                                    date_map[i[8]][1] += i[-1]
                                    date_map[i[8]][2] += i[-1] + i[-2]
                                else:
                                    date_map[i[8]] = [0,0,0]
                                    date_map[i[8]][0] = i[-2]
                                    date_map[i[8]][1] = i[-1]
                                    date_map[i[8]][2] = i[-1] + i[-2]
                    else:
                        if i[3] is None:
                            if i[5] in senior_map.keys():
                                senior_map[i[5]][0] += i[-2]
                                senior_map[i[5]][1] += i[-1]
                                senior_map[i[5]][2] += i[-1] + i[-2]
                            else:
                                senior_map[i[5]] = [0, 0, 0]
                                senior_map[i[5]][0] = i[-2]
                                senior_map[i[5]][1] = i[-1]
                                senior_map[i[5]][2] = i[-1] + i[-2]

                            if i[4] in car_map.keys():
                                car_map[i[4]][0] += i[-2]
                                car_map[i[4]][1] += i[-1]
                                car_map[i[4]][2] += i[-1] + i[-2]
                            else:
                                car_map[i[4]] = [0, 0, 0]
                                car_map[i[4]][0] = i[-2]
                                car_map[i[4]][1] = i[-1]
                                car_map[i[4]][2] = i[-1] + i[-2]
                            if i[7] is not None:
                                if i[7] in repairlocation_manhour_map.keys():
                                    repairlocation_manhour_map[i[7]] += i[-2]
                                else:
                                    repairlocation_manhour_map[i[7]] = i[-2]

                                if i[7] in repairlocation_material_map.keys():
                                    repairlocation_material_map[i[7]] += i[-1]
                                else:
                                    repairlocation_material_map[i[7]] = i[-1]

                            if i[1] is not None:
                                if i[1] in railway_map.keys():
                                    railway_map[i[1]][0] += i[-2]
                                    railway_map[i[1]][1] += i[-1]
                                    railway_map[i[1]][2] += i[-1] + i[-2]
                                else:
                                    railway_map[i[1]] = [0, 0, 0]
                                    railway_map[i[1]][0] = i[-2]
                                    railway_map[i[1]][1] = i[-1]
                                    railway_map[i[1]][2] = i[-1] + i[-2]
                            if i[8] is not None:
                                if i[8] in date_map.keys():
                                    date_map[i[8]][0] += i[-2]
                                    date_map[i[8]][1] += i[-1]
                                    date_map[i[8]][2] += i[-1] + i[-2]
                                else:
                                    date_map[i[8]] = [0,0,0]
                                    date_map[i[8]][0] = i[-2]
                                    date_map[i[8]][1] = i[-1]
                                    date_map[i[8]][2] = i[-1] + i[-2]
        elif value == '供应商':
            for i in res3:
                if math.isnan(i[-2]) is False:
                    if i[6] is not None:
                        if i[6] in supplier_manhour_map.keys():
                            supplier_manhour_map[i[6]] += i[-2]
                        else:
                            supplier_manhour_map[i[6]] = i[-2]

                        if i[6] in supplier_material_map.keys():
                            supplier_material_map[i[6]] += i[-1]
                        else:
                            supplier_material_map[i[6]] = i[-1]
                    if value1 == '':
                        pass
                    else:
                        if i[6] == value1:
                            if i[4] in car_map.keys():
                                car_map[i[4]][0] += i[-2]
                                car_map[i[4]][1] += i[-1]
                                car_map[i[4]][2] += i[-1] + i[-2]
                            else:
                                car_map[i[4]] = [0, 0, 0]
                                car_map[i[4]][0] = i[-2]
                                car_map[i[4]][1] = i[-1]
                                car_map[i[4]][2] = i[-1] + i[-2]

                            if i[5] in senior_map.keys():
                                senior_map[i[5]][0] += i[-2]
                                senior_map[i[5]][1] += i[-1]
                                senior_map[i[5]][2] += i[-1] + i[-2]
                            else:
                                senior_map[i[5]] = [0, 0, 0]
                                senior_map[i[5]][0] = i[-2]
                                senior_map[i[5]][1] = i[-1]
                                senior_map[i[5]][2] = i[-1] + i[-2]

                            if i[3] is not None:
                                if '修复性维修' in tech_map.keys():
                                    tech_map['修复性维修'][0] += i[-2]
                                    tech_map['修复性维修'][1] += i[-1]
                                    tech_map['修复性维修'][2] += i[-2] + i[-1]
                                else:
                                    tech_map['修复性维修'] = [0, 0, 0]
                                    tech_map['修复性维修'][0] = i[-2]
                                    tech_map['修复性维修'][1] = i[-1]
                                    tech_map['修复性维修'][2] = i[-2] + i[-1]

                                if len(i[3].split('.')) == 2:
                                    if i[3].split('.')[0] in component_map.keys():
                                        component_map[i[3].split('.')[0]][0][0] += i[-2]
                                        component_map[i[3].split('.')[0]][0][1] += i[-1]
                                        component_map[i[3].split('.')[0]][0][2] += i[-2] + i[-1]
                                    else:
                                        component_map[i[3].split('.')[0]] = [[], {}]
                                        component_map[i[3].split('.')[0]][0] = [0, 0, 0]
                                        component_map[i[3].split('.')[0]][0][0] = i[-2]
                                        component_map[i[3].split('.')[0]][0][1] = i[-1]
                                        component_map[i[3].split('.')[0]][0][2] = i[-2] + i[-1]
                                        component_map[i[3].split('.')[0]][1]['children'] = {}

                                    if i[3].split('.')[1] in component_map[i[3].split('.')[0]][1]['children'].keys():
                                        component_map[i[3].split('.')[0]][1]['children'][i[3].split('.')[1]][0] += i[-2]
                                        component_map[i[3].split('.')[0]][1]['children'][i[3].split('.')[1]][1] += i[-1]
                                        component_map[i[3].split('.')[0]][1]['children'][i[3].split('.')[1]][2] += i[-1] + \
                                                                                                                   i[-2]
                                    else:
                                        component_map[i[3].split('.')[0]][1]['children'][i[3].split('.')[1]] = [0, 0, 0]
                                        component_map[i[3].split('.')[0]][1]['children'][i[3].split('.')[1]][0] = i[-2]
                                        component_map[i[3].split('.')[0]][1]['children'][i[3].split('.')[1]][1] = i[-1]
                                        component_map[i[3].split('.')[0]][1]['children'][i[3].split('.')[1]][2] = i[-1] + i[
                                            -2]
                                else:
                                    if i[3].split('.')[0] in component_map.keys():
                                        component_map[i[3].split('.')[0]][0][0] += i[-2]
                                        component_map[i[3].split('.')[0]][0][1] += i[-1]
                                        component_map[i[3].split('.')[0]][0][2] += i[-2] + i[-1]
                                    else:
                                        component_map[i[3].split('.')[0]] = [[], {}]
                                        component_map[i[3].split('.')[0]][0] = [0, 0, 0]
                                        component_map[i[3].split('.')[0]][0][0] = i[-2]
                                        component_map[i[3].split('.')[0]][0][1] = i[-1]
                                        component_map[i[3].split('.')[0]][0][2] = i[-2] + i[-1]
                            else:
                                if '预防性维修' in tech_map.keys():
                                    tech_map['预防性维修'][0] += i[-2]
                                    tech_map['预防性维修'][1] += i[-1]
                                    tech_map['预防性维修'][2] += i[-2] + i[-1]
                                else:
                                    tech_map['预防性维修'] = [0, 0, 0]
                                    tech_map['预防性维修'][0] = i[-2]
                                    tech_map['预防性维修'][1] = i[-1]
                                    tech_map['预防性维修'][2] = i[-2] + i[-1]

                            if i[7] is not None:
                                if i[7] in repairlocation_manhour_map.keys():
                                    repairlocation_manhour_map[i[7]] += i[-2]
                                else:
                                    repairlocation_manhour_map[i[7]] = i[-2]

                                if i[7] in repairlocation_material_map.keys():
                                    repairlocation_material_map[i[7]] += i[-1]
                                else:
                                    repairlocation_material_map[i[7]] = i[-1]

                            if i[1] is not None:
                                if i[1] in railway_map.keys():
                                    railway_map[i[1]][0] += i[-2]
                                    railway_map[i[1]][1] += i[-1]
                                    railway_map[i[1]][2] += i[-1] + i[-2]
                                else:
                                    railway_map[i[1]] = [0, 0, 0]
                                    railway_map[i[1]][0] = i[-2]
                                    railway_map[i[1]][1] = i[-1]
                                    railway_map[i[1]][2] = i[-1] + i[-2]
                            if i[8] is not None:
                                if i[8] in date_map.keys():
                                    date_map[i[8]][0] += i[-2]
                                    date_map[i[8]][1] += i[-1]
                                    date_map[i[8]][2] += i[-1] + i[-2]
                                else:
                                    date_map[i[8]] = [0,0,0]
                                    date_map[i[8]][0] = i[-2]
                                    date_map[i[8]][1] = i[-1]
                                    date_map[i[8]][2] = i[-1] + i[-2]
        else:
            for i in res3:
                if math.isnan(i[-2]) is False:
                    if i[3] is not None:
                        if len(i[3].split('.')) == 2:
                            if i[3].split('.')[0] in component_map.keys():
                                component_map[i[3].split('.')[0]][0][0] += i[-2]
                                component_map[i[3].split('.')[0]][0][1] += i[-1]
                                component_map[i[3].split('.')[0]][0][2] += i[-2] + i[-1]
                            else:
                                component_map[i[3].split('.')[0]] = [[], {}]
                                component_map[i[3].split('.')[0]][0] = [0, 0, 0]
                                component_map[i[3].split('.')[0]][0][0] = i[-2]
                                component_map[i[3].split('.')[0]][0][1] = i[-1]
                                component_map[i[3].split('.')[0]][0][2] = i[-2] + i[-1]
                                component_map[i[3].split('.')[0]][1]['children'] = {}

                            if i[3].split('.')[1] in component_map[i[3].split('.')[0]][1]['children'].keys():
                                component_map[i[3].split('.')[0]][1]['children'][i[3].split('.')[1]][0] += i[-2]
                                component_map[i[3].split('.')[0]][1]['children'][i[3].split('.')[1]][1] += i[-1]
                                component_map[i[3].split('.')[0]][1]['children'][i[3].split('.')[1]][2] += i[-1] + \
                                                                                                           i[-2]
                            else:
                                component_map[i[3].split('.')[0]][1]['children'][i[3].split('.')[1]] = [0, 0, 0]
                                component_map[i[3].split('.')[0]][1]['children'][i[3].split('.')[1]][0] = i[-2]
                                component_map[i[3].split('.')[0]][1]['children'][i[3].split('.')[1]][1] = i[-1]
                                component_map[i[3].split('.')[0]][1]['children'][i[3].split('.')[1]][2] = i[-1] + i[-2]
                        else:
                            if i[3].split('.')[0] in component_map.keys():
                                component_map[i[3].split('.')[0]][0][0] += i[-2]
                                component_map[i[3].split('.')[0]][0][1] += i[-1]
                                component_map[i[3].split('.')[0]][0][2] += i[-2] + i[-1]
                            else:
                                component_map[i[3].split('.')[0]] = [[], {}]
                                component_map[i[3].split('.')[0]][0] = [0, 0, 0]
                                component_map[i[3].split('.')[0]][0][0] = i[-2]
                                component_map[i[3].split('.')[0]][0][1] = i[-1]
                                component_map[i[3].split('.')[0]][0][2] = i[-2] + i[-1]

            if value == '2':
                for i in res3:
                    if math.isnan(i[-2]) is False:
                        if i[3] is not None:
                            if i[3].split('.')[0] == value1:
                                if i[4] in car_map.keys():
                                    car_map[i[4]][0] += i[-2]
                                    car_map[i[4]][1] += i[-1]
                                    car_map[i[4]][2] += i[-1] + i[-2]
                                else:
                                    car_map[i[4]] = [0, 0, 0]
                                    car_map[i[4]][0] = i[-2]
                                    car_map[i[4]][1] = i[-1]
                                    car_map[i[4]][2] = i[-1] + i[-2]

                                if i[5] in senior_map.keys():
                                    senior_map[i[5]][0] += i[-2]
                                    senior_map[i[5]][1] += i[-1]
                                    senior_map[i[5]][2] += i[-1] + i[-2]
                                else:
                                    senior_map[i[5]] = [0, 0, 0]
                                    senior_map[i[5]][0] = i[-2]
                                    senior_map[i[5]][1] = i[-1]
                                    senior_map[i[5]][2] = i[-1] + i[-2]
                                if i[3] is not None:
                                    if '修复性维修' in tech_map.keys():
                                        tech_map['修复性维修'][0] += i[-2]
                                        tech_map['修复性维修'][1] += i[-1]
                                        tech_map['修复性维修'][2] += i[-2] + i[-1]
                                    else:
                                        tech_map['修复性维修'] = [0, 0, 0]
                                        tech_map['修复性维修'][0] = i[-2]
                                        tech_map['修复性维修'][1] = i[-1]
                                        tech_map['修复性维修'][2] = i[-2] + i[-1]
                                else:
                                    if '预防性维修' in tech_map.keys():
                                        tech_map['预防性维修'][0] += i[-2]
                                        tech_map['预防性维修'][1] += i[-1]
                                        tech_map['预防性维修'][2] += i[-2] + i[-1]
                                    else:
                                        tech_map['预防性维修'] = [0, 0, 0]
                                        tech_map['预防性维修'][0] = i[-2]
                                        tech_map['预防性维修'][1] = i[-1]
                                        tech_map['预防性维修'][2] = i[-2] + i[-1]

                                if i[6] is not None:
                                    if i[6] in supplier_manhour_map.keys():
                                        supplier_manhour_map[i[6]] += i[-2]
                                    else:
                                        supplier_manhour_map[i[6]] = i[-2]

                                    if i[6] in supplier_material_map.keys():
                                        supplier_material_map[i[6]] += i[-1]
                                    else:
                                        supplier_material_map[i[6]] = i[-1]

                                if i[7] is not None:
                                    if i[7] in repairlocation_manhour_map.keys():
                                        repairlocation_manhour_map[i[7]] += i[-2]
                                    else:
                                        repairlocation_manhour_map[i[7]] = i[-2]

                                    if i[7] in repairlocation_material_map.keys():
                                        repairlocation_material_map[i[7]] += i[-1]
                                    else:
                                        repairlocation_material_map[i[7]] = i[-1]

                                if i[1] is not None:
                                    if i[1] in railway_map.keys():
                                        railway_map[i[1]][0] += i[-2]
                                        railway_map[i[1]][1] += i[-1]
                                        railway_map[i[1]][2] += i[-1] + i[-2]
                                    else:
                                        railway_map[i[1]] = [0, 0, 0]
                                        railway_map[i[1]][0] = i[-2]
                                        railway_map[i[1]][1] = i[-1]
                                        railway_map[i[1]][2] = i[-1] + i[-2]
                                if i[8] is not None:
                                    if i[8] in date_map.keys():
                                        date_map[i[8]][0] += i[-2]
                                        date_map[i[8]][1] += i[-1]
                                        date_map[i[8]][2] += i[-1] + i[-2]
                                    else:
                                        date_map[i[8]] = [0, 0, 0]
                                        date_map[i[8]][0] = i[-2]
                                        date_map[i[8]][1] = i[-1]
                                        date_map[i[8]][2] = i[-1] + i[-2]
            elif value == '3':
                for i in res3:
                    if math.isnan(i[-2]) is False:
                        if i[3] is not None:
                            if i[3].split('.')[1] == value1:
                                if i[4] in car_map.keys():
                                    car_map[i[4]][0] += i[-2]
                                    car_map[i[4]][1] += i[-1]
                                    car_map[i[4]][2] += i[-1] + i[-2]
                                else:
                                    car_map[i[4]] = [0, 0, 0]
                                    car_map[i[4]][0] = i[-2]
                                    car_map[i[4]][1] = i[-1]
                                    car_map[i[4]][2] = i[-1] + i[-2]

                                if i[5] in senior_map.keys():
                                    senior_map[i[5]][0] += i[-2]
                                    senior_map[i[5]][1] += i[-1]
                                    senior_map[i[5]][2] += i[-1] + i[-2]
                                else:
                                    senior_map[i[5]] = [0, 0, 0]
                                    senior_map[i[5]][0] = i[-2]
                                    senior_map[i[5]][1] = i[-1]
                                    senior_map[i[5]][2] = i[-1] + i[-2]
                                if i[3] is not None:
                                    if '修复性维修' in tech_map.keys():
                                        tech_map['修复性维修'][0] += i[-2]
                                        tech_map['修复性维修'][1] += i[-1]
                                        tech_map['修复性维修'][2] += i[-2] + i[-1]
                                    else:
                                        tech_map['修复性维修'] = [0, 0, 0]
                                        tech_map['修复性维修'][0] = i[-2]
                                        tech_map['修复性维修'][1] = i[-1]
                                        tech_map['修复性维修'][2] = i[-2] + i[-1]
                                else:
                                    if '预防性维修' in tech_map.keys():
                                        tech_map['预防性维修'][0] += i[-2]
                                        tech_map['预防性维修'][1] += i[-1]
                                        tech_map['预防性维修'][2] += i[-2] + i[-1]
                                    else:
                                        tech_map['预防性维修'] = [0, 0, 0]
                                        tech_map['预防性维修'][0] = i[-2]
                                        tech_map['预防性维修'][1] = i[-1]
                                        tech_map['预防性维修'][2] = i[-2] + i[-1]

                                if i[6] is not None:
                                    if i[6] in supplier_manhour_map.keys():
                                        supplier_manhour_map[i[6]] += i[-2]
                                    else:
                                        supplier_manhour_map[i[6]] = i[-2]

                                    if i[6] in supplier_material_map.keys():
                                        supplier_material_map[i[6]] += i[-1]
                                    else:
                                        supplier_material_map[i[6]] = i[-1]

                                if i[7] is not None:
                                    if i[7] in repairlocation_manhour_map.keys():
                                        repairlocation_manhour_map[i[7]] += i[-2]
                                    else:
                                        repairlocation_manhour_map[i[7]] = i[-2]

                                    if i[7] in repairlocation_material_map.keys():
                                        repairlocation_material_map[i[7]] += i[-1]
                                    else:
                                        repairlocation_material_map[i[7]] = i[-1]

                                if i[1] is not None:
                                    if i[1] in railway_map.keys():
                                        railway_map[i[1]][0] += i[-2]
                                        railway_map[i[1]][1] += i[-1]
                                        railway_map[i[1]][2] += i[-1] + i[-2]
                                    else:
                                        railway_map[i[1]] = [0, 0, 0]
                                        railway_map[i[1]][0] = i[-2]
                                        railway_map[i[1]][1] = i[-1]
                                        railway_map[i[1]][2] = i[-1] + i[-2]
                                if i[8] is not None:
                                    if i[8] in date_map.keys():
                                        date_map[i[8]][0] += i[-2]
                                        date_map[i[8]][1] += i[-1]
                                        date_map[i[8]][2] += i[-1] + i[-2]
                                    else:
                                        date_map[i[8]] = [0, 0, 0]
                                        date_map[i[8]][0] = i[-2]
                                        date_map[i[8]][1] = i[-1]
                                        date_map[i[8]][2] = i[-1] + i[-2]


        if len(supplier_manhour_map) == 0:
            pass
        else:
            supplier_sum_map = copy.deepcopy(supplier_manhour_map)
            for m in supplier_material_map:
                if m in supplier_sum_map.keys():
                    supplier_sum_map[m] += supplier_material_map[m]
                else:
                    supplier_sum_map[m] = supplier_material_map[m]
            supplier_manhour_list = sorted(supplier_manhour_map.items(), key=lambda item: item[1],
                                           reverse=True)
            supplier_material_list = sorted(supplier_material_map.items(), key=lambda item: item[1],
                                            reverse=True)
            supplier_sum_list = sorted(supplier_sum_map.items(), key=lambda item: item[1], reverse=True)

        if len(repairlocation_manhour_map) == 0:
            pass
        else:
            repairlocation_sum_map = copy.deepcopy(repairlocation_manhour_map)
            for m in repairlocation_material_map:
                if m in repairlocation_sum_map.keys():
                    repairlocation_sum_map[m] += repairlocation_material_map[m]
                else:
                    repairlocation_sum_map[m] = repairlocation_material_map[m]

            repairlocation_manhour_list = sorted(repairlocation_manhour_map.items(), key=lambda item: item[1],
                                           reverse=True)

            repairlocation_material_list = sorted(repairlocation_material_map.items(), key=lambda item: item[1],
                                                 reverse=True)

            repairlocation_sum_list = sorted(repairlocation_sum_map.items(), key=lambda item: item[1],
                                                 reverse=True)

        print(senior_map)
        print(car_map)
        print(tech_map)
        if len(supplier_manhour_list) <= 10:
            pass
        else:
            supplier_manhour_list = supplier_manhour_list[:10]
        print(supplier_manhour_list)

        if len(supplier_material_list) <= 10:
            pass
        else:
            supplier_material_list = supplier_material_list[:10]
        print(supplier_material_list)

        if len(supplier_sum_list) <= 10:
            pass
        else:
            supplier_sum_list = supplier_sum_list[:10]
        print(supplier_sum_list)
        print(component_map)
        if len(repairlocation_manhour_list) <= 10:
            pass
        else:
            repairlocation_manhour_list = repairlocation_manhour_list[:10]
            repairlocation_manhour_list.reverse()
        print(repairlocation_manhour_list)
        if len(repairlocation_material_list) <= 10:
            pass
        else:
            repairlocation_material_list = repairlocation_material_list[:10]
            repairlocation_material_list.reverse()
        print(repairlocation_material_list)
        if len(repairlocation_sum_list) <= 10:
            pass
        else:
            repairlocation_sum_list = repairlocation_sum_list[:10]
            repairlocation_sum_list.reverse()
        print(repairlocation_sum_list)

        print(railway_map)
        print(date_map)












Method().main({'E27':['2651'],'E28':['2216']},['2018-01-01','2019-12-31'],'2','内装系统')