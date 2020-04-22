import cx_Oracle
from tuoming.tuoming_method1 import Method1

# 方案九
class Method5:
    def deal(self):
        conn = cx_Oracle.connect('dev/123456@127.0.0.1:1521/orcl')
        cursor = conn.cursor()
        sql = 'select POSITION_REF_CODE  from fault_conf_old'
        cursor.execute(sql)
        fields = cursor.fetchall()

        L = []
        sql_type = 'select * from (select distinct PICTURE_NO from train_info_old)'
        cursor.execute(sql_type)
        type1 = cursor.fetchall()
        # print(type1)
        for i in type1:
            L.append(i[0])

        # 初始化t_i的值
        sql_get = "select new_position from position_mappings where old_position = 'sequence'"
        cursor.execute(sql_get)
        position = cursor.fetchone()
        if position is not None:
            t_i = int(position[0])
            update_flag = True
        else:
            t_i = 1
            update_flag = False

        position_mapping = {}
        for tu in fields:
            # 查询是否存在这条数据
            sql_mappings = 'select old_position from position_mappings where old_position=\'%s\'' % tu[0]
            cursor.execute(sql_mappings)
            mappings = cursor.fetchone()
            if mappings is not None:
                continue
            else:
                tu_1_tmp = ''
                if tu[0] is None:
                    tu_1_tmp = 'a_null'
                    if position_mapping.__len__() == 0:
                        position_mapping.update({tu_1_tmp: tu_1_tmp})
                    else:
                        if position_mapping.get(tu[0]) is None:
                            position_mapping.update({tu_1_tmp: tu_1_tmp})
                        else:
                            pass
                else:
                    if tu[0] in L:
                        a = Method1().get_cartype(conn,tu[0])
                        position_mapping.update({tu_1_tmp: a})
                    else:
                        tu_1_tmp = tu[0]
                        if position_mapping.__len__() == 0:
                            a = '部件' + (len('000000') - len(str(t_i))) * '0' + str(t_i)
                            position_mapping.update({tu_1_tmp: a})
                            t_i += 1
                        else:
                            if position_mapping.get(tu_1_tmp) is None:
                                a = '部件' + (len('000000') - len(str(t_i))) * '0' + str(t_i)
                                position_mapping.update({tu_1_tmp: a})
                                t_i += 1
                            else:
                                pass

                sql_insert = 'insert into position_mappings(old_position,new_position) values (\'%s\',\'%s\')' % (
                tu[0], position_mapping.get(tu_1_tmp))
                try:
                    cursor.execute(sql_insert)
                    conn.commit()
                except Exception as e:
                    print(sql_insert)
                    print(e)

        if update_flag is True:
            sql_update = "update position_mappings set new_position=\'%s\' where old_position='sequence'" \
                         % (str(t_i - 1))
            try:
                cursor.execute(sql_update)
                conn.commit()
                cursor.close()
                conn.close()
            except Exception as e:
                print(sql_update)
                print(e)

        else:
            sql_ins = 'insert into position_mappings(old_position,new_position) values (\'%s\',\'%s\')' % (
            'sequence', str(t_i))
            try:
                cursor.execute(sql_ins)
                conn.commit()
                cursor.close()
                conn.close()
            except Exception as e:
                print(sql_ins)
                print(e)

    def get_position(self, x, y):
        conn = x
        cursor = conn.cursor()
        #得到新的系统部件
        sql_get = 'select new_position from position_mappings where OLD_POSITION= \'%s\'' % y
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

