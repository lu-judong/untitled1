from tuoming.tuoming_method7 import Method7
from tuoming.tuoming_method1 import Method1
import cx_Oracle
import datetime

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
        print(1,datetime.datetime.now())
        conn = cx_Oracle.connect('dev/123456@127.0.0.1:1521/orcl')
        cursor = conn.cursor()
        sql_count = "select count(*) from train_dist_old"
        cursor.execute(sql_count)
        count1 = cursor.fetchone()
        # 控制循环得次数 一次去1w条 直到取完为止
        t_i = 0
        M = []
        for i in range(0,int(count1[0])//10000 + 1):
            sql_get1 = "select * from train_dist_old order by id"
            sqlBu = self.string_page(sql_get1, t_i, 10000)
            cursor.execute(sqlBu)

            fields = cursor.fetchall()
            for tu in fields:
                sql_mappings = 'select id from train_dist where id = \'%s\'' % (tu[0])
                cursor.execute(sql_mappings)
                mappings = cursor.fetchone()
                if mappings is not None:
                    continue
                else:
                    t_0 = tu[0]
                    t_1 = Method1().get_carnum(conn,tu[1])
                    t_2 = tu[2]
                    t_3 = tu[3]
                    t_4 = tu[4]
                    t_5 = Method7().all_change(tu[5])
                    t_6 = tu[6]
                    t_7 = tu[7]
                    t_8 = tu[8]
                    M.append((t_0, t_1, t_2, t_3, t_4, t_5, t_6, t_7, t_8))

            sql_insert = 'insert into train_dist(id,car_riage,mile_age,mile_date,last_updated_time,last_updated_by,trn_id,infoid,synchronizetime) values (:1,:2,:3,:4,:5,:6,:7,:8,:9)'
            cursor.prepare(sql_insert)
            try:
                cursor.executemany(None, M[:])
                print(2,datetime.datetime.now())
                conn.commit()
                M = []
                t_i += 10000
            except Exception as e:
                print(sql_insert)
                print(e)
        cursor.close()
        conn.close()


Table().deal()