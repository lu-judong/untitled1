import pymysql
import sympy
import datetime

class Check:


    def connect_darams_mileage(self, sql_execure_mileage):
        db = pymysql.connect("192.168.221.21", "root", "123456", charset="utf8")
        cur = db.cursor()
        cur.execute("use darams")
        cur.execute(sql_execure_mileage)
        data = cur.fetchall()
        return data

    def run(self,car,date):
        L = []
        d = {}
        date1 = date.strftime("%Y-%m-%d")
        sql_execure_mileage = \
            '''
            SELECT
                current_mileage
            FROM
                cd_mileage m 
                INNER JOIN cd_train_real_time r ON r.id = m.train_real_time_id
                INNER JOIN cd_train_no n ON n.id = r.train_no_id
            WHERE
                1 = 1
                AND n.train_no = '{}'
                AND m.del_flag = '0'
                AND m.mileage_time = '{}'	
            '''.format(car,date1)

        # print(sql_execure_mileage)
        data = self.connect_darams_mileage(sql_execure_mileage)
        if len(data) == 1:
            return data[0][0]
        else:
            sql_execure_mileage1 = \
                '''
                SELECT
                distinct 
                    current_mileage,
                    mileage_time
                FROM
                    cd_mileage m 
                    INNER JOIN cd_train_real_time r ON r.id = m.train_real_time_id
                    INNER JOIN cd_train_no n ON n.id = r.train_no_id
                WHERE
                    1 = 1
                    AND n.train_no = '{}'
                    AND m.del_flag = '0'
                    AND m.mileage_time <= '{}'	
                    order by mileage_time desc 
                    LIMIT 2
                '''.format(car, date1)
            data1 = self.connect_darams_mileage(sql_execure_mileage1)

            for i in data1:
                se = (datetime.datetime.strptime(date1, '%Y-%m-%d')-i[1]).total_seconds()
                L.append(se)

            sql_execure_mileage2 = \
                '''
                SELECT
                distinct 
                    current_mileage,
                    mileage_time
                FROM
                    cd_mileage m 
                    INNER JOIN cd_train_real_time r ON r.id = m.train_real_time_id
                    INNER JOIN cd_train_no n ON n.id = r.train_no_id
                WHERE
                    1 = 1
                    AND n.train_no = '{}'
                    AND m.del_flag = '0'
                    AND m.mileage_time >= '{}'	
                    order by mileage_time 
                    LIMIT 2
                '''.format(car, date1)
            data2 = self.connect_darams_mileage(sql_execure_mileage2)
            for i1 in data2:
                se = (i1[1]-datetime.datetime.strptime(date1, '%Y-%m-%d')).total_seconds()
                L.append(se)

            sql_execure_mileage3 = '''
                SELECT
                distinct 
                        t.accumulated_mileage,
                        d.occurrence_time
                FROM
                        op_fault_order_detail d
                        INNER JOIN op_train t ON t.fault_detail_id = d.id
                        INNER JOIN op_fault_order_header h on d.fault_id = h.id
                WHERE
                        1 = 1
                        AND t.train_no = '{}'
                        AND h.del_flag = '0'
                        AND d.occurrence_time <= '{}'
                        AND h.status !='已取消'									
                        order by d.occurrence_time desc 
                        LIMIT 2
            '''.format(car,date1)

            data3 = self.connect_darams_mileage(sql_execure_mileage3)
            for i2 in data3:
                se = (datetime.datetime.strptime(date1, '%Y-%m-%d')-i2[1]).total_seconds()
                L.append(se)

            sql_execure_mileage4 = '''
                         SELECT
                         distinct 
                                 t.accumulated_mileage,
                                 d.occurrence_time
                         FROM
                                 op_fault_order_detail d
                                 INNER JOIN op_train t ON t.fault_detail_id = d.id
                                 INNER JOIN op_fault_order_header h on d.fault_id = h.id
                         WHERE
                                 1 = 1
                                 AND t.train_no = '{}'
                                 AND h.del_flag = '0'
                                 AND d.occurrence_time >= '{}'
                                 AND h.status !='已取消'									
                                 order by d.occurrence_time 
                                 LIMIT 2
                         '''.format(car, date1)

            data4 = self.connect_darams_mileage(sql_execure_mileage4)
            for i3 in data4:
                se = (i3[1] - datetime.datetime.strptime(date1, '%Y-%m-%d')).total_seconds()
                L.append(se)

            L.sort()
            L2 = L[0:2]
            # print(L2)
            for k in data1:
                for k1 in L2:
                    if (datetime.datetime.strptime(date1, '%Y-%m-%d')-k[1]).total_seconds() == k1:
                        d[k[1]] = k[0]
                    else:
                        pass
            for k2 in data2:
                for k3 in L2:
                    if (k2[1] - datetime.datetime.strptime(date1, '%Y-%m-%d')).total_seconds() == k3:
                        d[k2[1]] = k2[0]
                    else:
                        pass

            for k4 in data3:
                for k5 in L2:
                    if (datetime.datetime.strptime(date1, '%Y-%m-%d')-k4[1]).total_seconds() == k5:
                        d[k4[1]] = k4[0]
                    else:
                        pass
            for k6 in data4:
                for k7 in L2:
                    if (k6[1] - datetime.datetime.strptime(date1, '%Y-%m-%d')).total_seconds() == k7:
                        d[k6[1]] = k6[0]
                    else:
                        pass
            # print(d)
            x = sympy.symbols("x")
            if len(d) == 1:
                return tuple(d.values())[0]
            elif L2[0] == L2[1]:
                return  tuple(d.values())[0]
            else:
                if tuple(d.values())[0] - tuple(d.values())[1] == 0:
                    return  tuple(d.values())[0]
                else:
                    if abs((tuple(d.keys())[0] - datetime.datetime.strptime(date1, '%Y-%m-%d')).total_seconds()) < abs((tuple(d.keys())[1] - datetime.datetime.strptime(date1, '%Y-%m-%d')).total_seconds()):
                        # a = sympy.solve([(L2[0]-x)/(x-L2[1])-(L2[0]/L2[1])],[x])
                        a = sympy.solve([(tuple(d.values())[0] - x) / (tuple(d.values())[1] - tuple(d.values())[0]) - (L2[0] / (L2[1]-L2[0]))], [x])
                        return a[x]
                    else:
                        a = sympy.solve([(tuple(d.values())[1] - x) / (tuple(d.values())[0] - tuple(d.values())[1]) - (
                                    L2[0] / (L2[1] - L2[0]))], [x])
                        return a[x]


    def main(self, car, date):
        nu = 0
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

        for i in car:
            for j in L:
                num = self.run(i,j)
                L2.append(abs(num))
            L1.append(L2)
            L2 = []
        print(L1)
        for m in L1:
            for j in range(0,len(m)-1):
                nu += abs(m[j+1] - m[j])

        print(nu)

Check().main(['2641','2642','2643','2644','2645','2646','2647','2648'],['2017-06-14','2017-12-31'])
