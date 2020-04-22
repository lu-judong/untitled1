import pymysql
import re

class Method:
    def deal(self):
        conn = pymysql.connect(
            host='192.168.1.21',
            port=3306,
            user='root',
            passwd='123456',
            db='lcc_tuoming',
            charset='utf8'
        )
        cursor = conn.cursor()
        sql = 'select repair_location from op_work_order_repair'
        cursor.execute(sql)
        fields = cursor.fetchall()
        L = []
        for tu in fields:
            # print(tu[0])
            if tu[0] is None:
                L.append('')
            else:
                j = re.split('\.', tu[0])
                for k in j:
                    L.append(k)
        # print(L)
        # print(list(set(L)))
        L1 = list(set(L))
        # print(L1)
        L1.sort()
        # 初始化t_i的值
        sql_get = "select new_repair_location from repair_mappings where old_repair_location = 'sequence'"
        cursor.execute(sql_get)
        repair = cursor.fetchone()
        if repair is not None:
            t_i = int(repair[0])
            update_flag = True
        else:
            t_i = 1
            update_flag = False

        for repair_i in L1:
            if repair_i in ['', 'E27', 'E28', 'T1', 'T2', 'T3', 'T4', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6']:
                new_repair = repair_i
            else:
                new_repair = '构型000{}'.format(t_i)
                t_i += 1

            sql_insert = 'insert into repair_mappings(old_repair_location,new_repair_location) values (\'%s\',\'%s\')' % (repair_i, new_repair)
            try:
                cursor.execute(sql_insert)
                conn.commit()

            except Exception as e:
                print(sql_insert)
                print(e)

        if update_flag is True:
            sql_update = "update repair_mappings set new_repair_location=\'%s\' where old_repair_location='sequence'" % (str(t_i - 1))
            try:
                cursor.execute(sql_update)
                conn.commit()
                cursor.close()
                conn.close()
            except Exception as e:
                print(sql_update)
                print(e)
        else:
            sql_ins = 'insert into repair_mappings(old_repair_location,new_repair_location) values (\'%s\',\'%s\')' % (
                'sequence', str(t_i))
            try:
                cursor.execute(sql_ins)
                conn.commit()
                cursor.close()
                conn.close()
            except Exception as e:
                print(sql_ins)
                print(e)

    def get_repair(self, x, y):
        conn = x
        cursor = conn.cursor()
        #得到新的系统部件
        sql_get = 'select new_repair_location from repair_mappings where old_repair_location = \'%s\'' % y
        cursor.execute(sql_get)
        fields = cursor.fetchone()
        if fields is not None:
            try:
                return fields[0]
            except Exception as e:
                print(e)
        else:
            return ''
        cursor.close()

Method().deal()