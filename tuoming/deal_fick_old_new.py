import cx_Oracle
import datetime
import re
from tuoming.tuoming_method5 import Method5

class Table1:

    def deal(self):
        conn = cx_Oracle.connect('dev/123456@127.0.0.1:1521/orcl')
        cursor = conn.cursor()
        print(datetime.datetime.now())

        sql_get2 = 'select FAILURE_OBJECT,real_failure_obj,id from fault_fick_old'
        cursor.execute(sql_get2)
        fields = cursor.fetchall()
        for tu in fields:
            if tu[0] is None:
                b = tu[0]
            else:
                a = re.split('\.',tu[0])
                b = ''
                for i in a:
                    if i != a[-1]:
                        c = Method5().get_position(conn,i)
                        b += c + '.'
                    else:
                        c = Method5().get_position(conn, i)
                        b += c


            if tu[1] is None:
                e = tu[1]
            else:
                d = re.split('\.',tu[1])
                e = ''
                for u in d:
                    if u != d[-1]:
                        f = Method5().get_position(conn,u)
                        e += f + '.'
                    else:
                        f = Method5().get_position(conn, u)
                        e += f
            g = tu[2]

            sql_insert = 'insert into fault_fick_new(FAILURE_OBJECT,real_failure_obj,id) values (\'%s\',\'%s\',\'%s\')' % (b,e,g)
            try:
                cursor.execute(sql_insert)
                conn.commit()
            except Exception as e:
                print(sql_insert)
                print(e)
                conn.rollback()
                raise


Table1().deal()