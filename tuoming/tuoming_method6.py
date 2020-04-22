import cx_Oracle
from tuoming.tuoming_method1 import Method1

# 方案十
class Method6:
    def deal(self):
        conn = cx_Oracle.connect('dev/123456@127.0.0.1:1521/orcl')
        cursor = conn.cursor()
        sql = 'select APPEARANCE_NAME from fault_appe_old order by APPEARANCE_NAME'
        cursor.execute(sql)
        fields = cursor.fetchall()

        # 初始化t_i的值
        sql_get = "select new_appearance from appearance_mappings where old_appearance = 'sequence'"
        cursor.execute(sql_get)
        appearance = cursor.fetchone()
        if appearance is not None:
            t_i = int(appearance[0])
            update_flag = True
        else:
            t_i = 1
            update_flag = False

        apperance_mapping = {}
        for tu in fields:
            # 查询是否存在这条数据
            sql_mappings = 'select old_appearance from appearance_mappings where old_appearance=\'%s\'' % tu[0]
            cursor.execute(sql_mappings)
            mappings = cursor.fetchone()
            if mappings is not None:
                continue
            else:
                tu_1_tmp = ''
                if tu[0] is None:
                    tu_1_tmp = 'a_null'
                    if apperance_mapping.__len__() == 0:
                        apperance_mapping.update({tu_1_tmp: tu_1_tmp})
                    else:
                        if apperance_mapping.get(tu[0]) is None:
                            apperance_mapping.update({tu_1_tmp: tu_1_tmp})
                        else:
                            pass
                else:
                    tu_1_tmp = tu[0]
                    if apperance_mapping.__len__() == 0:
                        a = '模式' + (len('000000') - len(str(t_i))) * '0' + str(t_i)
                        apperance_mapping.update({tu_1_tmp: a})
                        t_i += 1
                    else:
                        if apperance_mapping.get(tu_1_tmp) is None:
                            a = '模式' + (len('000000') - len(str(t_i))) * '0' + str(t_i)
                            apperance_mapping.update({tu_1_tmp: a})
                            t_i += 1
                        else:
                            pass

                sql_insert = 'insert into appearance_mappings(old_appearance,new_appearance) values (\'%s\',\'%s\')' % ( tu[0], apperance_mapping.get(tu_1_tmp))
                try:
                    cursor.execute(sql_insert)
                    conn.commit()
                except Exception as e:
                    print(sql_insert)
                    print(e)


        if update_flag is True:
            sql_update = "update appearance_mappings set new_appearance=\'%s\' where old_appearance='sequence'" % (str(t_i - 1))
            try:
                cursor.execute(sql_update)
                conn.commit()
                cursor.close()
                conn.close()
            except Exception as e:
                print(sql_update)
                print(e)

        else:
            sql_ins = 'insert into appearance_mappings(old_appearance,new_appearance) values (\'%s\',\'%s\')' % ('sequence', str(t_i))
            try:
                cursor.execute(sql_ins)
                conn.commit()
                cursor.close()
                conn.close()
            except Exception as e:
                print(sql_ins)
                print(e)

    def get_appearance(self, x, y):
        conn = x
        cursor = conn.cursor()
        #得到新的系统部件
        sql_get = 'select new_appearance from appearance_mappings where OLD_APPEARANCE= \'%s\'' % y
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
