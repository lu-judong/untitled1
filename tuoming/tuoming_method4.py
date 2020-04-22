import cx_Oracle

# 参考方案七
class Method4:
    def deal(self):
        conn = cx_Oracle.connect('dev/123456@127.0.0.1:1521/orcl')
        cursor = conn.cursor()
        sql = 'select REASON_CLASS_NAME from fault_fick_old order by reason_class_name'
        cursor.execute(sql)
        fields = cursor.fetchall()

        # 初始化t_i的值
        sql_get = "select new_reason from reason_mappings where old_reason = 'sequence'"
        cursor.execute(sql_get)
        reason = cursor.fetchone()
        if reason is not None:
            t_i = int(reason[0])
            update_flag = True
        else:
            t_i = 1
            update_flag = False

        reason_mapping = {}
        for tu in fields:
            sql_mappings = 'select old_reason from reason_mappings where old_reason=\'%s\'' % tu[0]
            cursor.execute(sql_mappings)
            mappings = cursor.fetchone()
            if mappings is not None:
                continue
            else:
                tu_1_tmp = ''
                if tu[0] is None:
                    tu_1_tmp= 'a_null'
                    if reason_mapping.__len__() == 0:
                        reason_mapping.update({tu_1_tmp: tu_1_tmp})
                    else:
                        if reason_mapping.get(tu[0]) is None:
                            reason_mapping.update({tu_1_tmp: tu_1_tmp})
                        else:
                            pass
                else:
                    tu_1_tmp = tu[0]
                    if reason_mapping.__len__() == 0:
                        a = '原因' + (len('000') - len(str(t_i))) * '0' + str(t_i)
                        reason_mapping.update({tu_1_tmp:a})
                        t_i += 1
                    else:
                        if reason_mapping.get(tu_1_tmp) is None:
                            a = '原因' + (len('000') - len(str(t_i))) * '0' + str(t_i)
                            reason_mapping.update({tu_1_tmp: a})
                            t_i += 1
                        else:
                            pass

                sql_insert = 'insert into reason_mappings(old_reason,new_reason) values (\'%s\',\'%s\')' % (tu[0],reason_mapping.get(tu_1_tmp))
                try:
                    cursor.execute(sql_insert)
                    conn.commit()
                except Exception as e:
                    print(sql_insert)
                    print(e)

        if update_flag is True:
            sql_update = "update reason_mappings set new_reason=\'%s\' where old_reason='sequence'" \
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
            sql_ins =  'insert into reason_mappings(old_reason,new_reason) values (\'%s\',\'%s\')' % ('sequence',str(t_i))
            try:
                cursor.execute(sql_ins)
                conn.commit()
                cursor.close()
                conn.close()
            except Exception as e:
                print(sql_ins)
                print(e)

    def get_reason(self,x,y):
        conn = x
        cursor = conn.cursor()
        #得到新的原因
        sql_get = 'select new_reason from reason_mappings where OLD_reason= \'%s\'' % y
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

