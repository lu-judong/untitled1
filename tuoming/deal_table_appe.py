from tuoming.tuoming_method7 import Method7
from tuoming.tuoming_method6 import Method6
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
        conn = cx_Oracle.connect('dev/123456@127.0.0.1:1521/orcl')
        cursor = conn.cursor()
        print(1,datetime.datetime.now())
        sql_count = "select count(*) from fault_appe_old"
        cursor.execute(sql_count)
        count1 = cursor.fetchone()
        # 控制循环得次数 一次去1w条 直到取完为止
        t_i = 0
        M = []
        for i in range(0,int(count1[0])//10000 + 1):
            sql_get1 = "select * from fault_appe_old order by id"
            sqlBu = self.string_page(sql_get1, t_i, 10000)
            cursor.execute(sqlBu)

            fields = cursor.fetchall()
            for tu in fields:
                sql_mappings = 'select id from fault_appe where id = \'%s\'' % (tu[0])
                cursor.execute(sql_mappings)
                mappings = cursor.fetchone()
                if mappings is not None:
                    continue
                else:
                    t_0 = tu[0]
                    t_1 = tu[1]
                    t_2 = tu[2]
                    t_3 = tu[3]
                    t_4 = Method6().get_appearance(conn,tu[4])
                    t_5 = Method6().get_appearance(conn,tu[5])
                    t_6 = tu[6]
                    t_7 = tu[7]
                    t_8 = Method7().all_change(tu[8])
                    t_9 = tu[9]
                    t_10 = Method7().all_change(tu[10])
                    t_11 = Method7().all_change(tu[11])
                    t_12 = tu[12]
                    t_13 = tu[13]
                    t_14 = tu[14]
                    t_15 = tu[15]
                    t_16 = tu[16]
                    t_17 = tu[17]
                    t_18 = tu[18]
                    t_19 = tu[19]
                    M.append((t_0, t_1, t_2, t_3, t_4, t_5, t_6, t_7, t_8, t_9, t_10, t_11, t_12, t_13, t_14, t_15,t_16,t_17,t_18,t_19))

            sql_insert = 'insert into fault_appe(id,ft_appearance_id,appearance_number,appearance_type_desc,appearance_name,appearance_desc,enabale_flag,creation_date,created_by,last_update_date,last_updated_by,unit_type,ft_config_relation_id,attribute1,attribute2,attribute3,attribute4,attribute5,confid,synchronizetime) values (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14,:15,:16,:17,:18,:19,:20)'
            cursor.prepare(sql_insert)
            try:
                cursor.executemany(None, M[:])
                print(2, datetime.datetime.now())
                conn.commit()
                M = []
                t_i += 10000
            except Exception as e:
                print(sql_insert)
                print(e)
        cursor.close()
        conn.close()


Table().deal()