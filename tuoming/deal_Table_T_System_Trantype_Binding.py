import cx_Oracle
from tuoming.tuoming_method1 import Method1

class Table:
    def deal(self):
        conn = cx_Oracle.connect('dev/123456@127.0.0.1:1521/orcl')
        cursor = conn.cursor()

        sql_sys = "select * from T_SYSTEM_TRANTYPE_BINDING_OLD order by id"
        cursor.execute(sql_sys)
        fields = cursor.fetchall()
        for tu in fields:
            sql_mappings = 'select id from T_SYSTEM_TRANTYPE_BINDING where id = \'%s\'' % (tu[0])
            cursor.execute(sql_mappings)
            mappings = cursor.fetchone()
            if mappings is not None:
                continue
            else:
                t_0 = tu[0]
                t_1 = tu[1]
                t_2 = Method1().get_cartype(conn,tu[2])

                sql_insert = 'insert into T_SYSTEM_TRANTYPE_BINDING(id,traintype,systemname) values (\'%s\',\'%s\'，\'%s\')' % (
                t_0,t_1,t_2)
                try:
                    cursor.execute(sql_insert)
                    conn.commit()
                except Exception as e:
                    print(sql_insert)
                    print(e)
        cursor.close()
        conn.close()

Table().deal()
