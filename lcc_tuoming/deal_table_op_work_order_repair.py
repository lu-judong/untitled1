from lcc_tuoming.lcc_tuoming_method1 import Method
import pymysql
import datetime
import re

class Table1:

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
        print(datetime.datetime.now())

        sql_count = "select count(*) from op_work_order_repair_old"
        cursor.execute(sql_count)
        count1 = cursor.fetchone()

        t_i = 0
        M = []
        for i in range(0, int(count1[0]) // 1000 + 1):
            sql_get2 = 'select * from op_work_order_repair_old order by id limit {},1000'.format(t_i)
            cursor.execute(sql_get2)
            fields = cursor.fetchall()
            for tu in fields:
                sql_mappings = 'select id from op_work_order_repair where id = \'%s\''% (tu[0])
                cursor.execute(sql_mappings)
                mappings = cursor.fetchone()
                if mappings is not None:
                    continue
                else:
                    t_0 = tu[0]
                    t_1 = tu[1]
                    t_2 = tu[2]
                    if tu[3] is None:
                        t_3 = tu[3]
                    else:
                        a = re.split('\.', tu[3])
                        t_3 = ''
                        for i in a:
                            if i != a[-1]:
                                c = Method().get_repair(conn,i)
                                t_3 += c + '.'
                            else:
                                c = Method().get_repair(conn, i)
                                t_3 += c

                    t_4 = tu[4]
                    t_5 = tu[5]
                    t_6= tu[6]
                    t_7 = tu[7]
                    t_8 = tu[8]
                    t_9 = tu[9]
                    t_10 = tu[10]
                    t_11 = tu[11]
                    t_12 = tu[12]
                    t_13 = tu[13]
                    t_14 = tu[14]

                    M.append((t_0, t_1, t_2, t_3, t_4, t_5, t_6, t_7, t_8, t_9, t_10, t_11, t_12, t_13, t_14))
            sql_insert = 'insert into op_work_order_repair(id,work_order_no,repair_object,repair_location,repair_location_no,repair_method,repair_level,access_name,cell_configuration,operation_contents,create_date,modify_date,create_by,update_by,del_flag) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

            try:
                cursor.executemany(sql_insert, M[:])
                print(2, datetime.datetime.now())
                conn.commit()
                M = []
                t_i += 1000
            except Exception as e:
                print(sql_insert)
                print(e)
        cursor.close()
        conn.close()


Table1().deal()
