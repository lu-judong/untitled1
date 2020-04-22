from tuoming.tuoming_method7 import Method7
from tuoming.tuoming_method5 import Method5
from tuoming.tuoming_method6 import Method6
import cx_Oracle
import datetime
import re

class Table:
    def string_page(self, sql, start, limit):
        if start == 0:
            sqlBuffer = "select * from (select row_.*, rownum rownum_ from (" + sql + ") row_ ) where rownum_ <= " + str(
                limit)
        elif start > 0:
            sqlBuffer = "select * from (select row_.*, rownum rownum_ from (" + sql + ") row_ ) where rownum_ <= " + str(
                start + limit) + " and rownum_ > " + str(start)
        else:
            sqlBuffer = sql
        return sqlBuffer

    def deal(self):
        conn = cx_Oracle.connect('dev/123456@127.0.0.1:1521/orcl')
        cursor = conn.cursor()
        print(1,datetime.datetime.now())
        sql_count = "select count(*) from fault_ocul_old"
        cursor.execute(sql_count)
        count1 = cursor.fetchone()
        # 控制循环得次数 一次去1w条 直到取完为止
        t_i = 0
        M = []
        for i in range(0, int(count1[0]) // 10000 + 1):
            sql_get1 = "select * from fault_ocul_old order by OCULAR_FAILURE_OBJ"
            sqlBu = self.string_page(sql_get1, t_i, 10000)
            cursor.execute(sqlBu)
            fields = cursor.fetchall()
            for tu in fields:
                sql_mappings = 'select id from fault_ocul where id = \'%s\'' % (tu[11])
                cursor.execute(sql_mappings)
                mappings = cursor.fetchone()
                if mappings is not None:
                    continue
                else:
                    t_0 = tu[0]

                    #直观故障对象
                    if tu[1] is None:
                        t_1 = tu[1]
                    else:
                        a = re.split('\.', tu[1])
                        t_1 = ''
                        for i in a:
                            if i != a[-1]:
                                c = Method5().get_position(conn, i)
                                t_1 += c + '.'
                            else:
                                c = Method5().get_position(conn, i)
                                t_1 += c
                    t_2 = tu[2]
                    t_3 = tu[3]
                    t_4 = Method6().get_appearance(conn,tu[4])
                    t_5 = Method7().all_change(tu[5])
                    t_6 = Method7().all_change(tu[6])
                    t_7 = tu[7]
                    t_8 = Method7().all_change(tu[8])
                    t_9 = tu[9]
                    t_10 = Method7().all_change(tu[10])
                    t_11 = tu[11]
                    t_12 = tu[12]
                    t_13 = tu[13]
                    M.append((t_0,t_1,t_2,t_3,t_4,t_5,t_6,t_7,t_8,t_9,t_10,t_11,t_12,t_13))

            sql_insert = 'insert into fault_ocul(rpt_id,ocular_failure_obj,ocular_failure_obj_id,ocular_failure_pnm_id,ocular_failure_pnm,ocular_other_fail_pnm_desc,ocular_other_fail_pnm,creation_date,created_by,last_update_date,last_update_by,id,fickid,synchronizetime) values (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14)'
            cursor.prepare(sql_insert)
            try:
                cursor.executemany(None,M[:])
                conn.commit()
                M = []
                t_i += 10000
            except Exception as e:
                print(sql_insert)
                print(e)
        cursor.close()
        conn.close()

Table().deal()