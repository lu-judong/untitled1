import cx_Oracle

# 参考方案六
class Method3:
    def deal(self):
        conn = cx_Oracle.connect('dev/123456@127.0.0.1:1521/orcl')
        cursor = conn.cursor()
        sql = 'select FAULT_LEVEL_NAME from fault_fick_old order by FAULT_LEVEL_NAME'
        cursor.execute(sql)
        fields = cursor.fetchall()

        level_mapping = {}
        for tu in fields:
            # 判断映射表中有没有这条数据
            sql_mappings = "select new_level from fault_level_mappings where old_level=\'%s\'" % (tu[0])
            cursor.execute(sql_mappings)
            mappings = cursor.fetchone()
            if mappings is not None:
                continue
            else:
                tu_1_tmp = ''
                if tu[0] is None:
                    tu_1_tmp= 'a_null'
                    if level_mapping.__len__() == 0:
                        level_mapping.update({tu_1_tmp: tu_1_tmp})
                    else:
                        if level_mapping.get(tu[0]) is None:
                            level_mapping.update({tu_1_tmp: tu_1_tmp})
                        else:
                            pass
                else:
                    if tu[0] == 'I级故障-灾难级故障':
                        tu_1_tmp = tu[0]
                        a = tu_1_tmp[:-9]
                        b = self.transform_roman_num2_alabo(a)
                        if level_mapping.__len__() == 0:
                            level_mapping.update({tu_1_tmp:b})
                        else:
                            if level_mapping.get(tu_1_tmp) is None:
                                level_mapping.update({tu_1_tmp: b})
                            else:
                                pass
                    else:
                        tu_1_tmp = tu[0]
                        a = tu_1_tmp[:-8]
                        b = self.transform_roman_num2_alabo(a)
                        if level_mapping.__len__() == 0:
                            level_mapping.update({tu_1_tmp: b})
                        else:
                            if level_mapping.get(tu_1_tmp) is None:
                                level_mapping.update({tu_1_tmp: b})
                            else:
                                pass

                    sql_insert = 'insert into fault_level_mappings(old_level,new_level) values (\'%s\',\'%s\')' % (tu[0],level_mapping.get(tu_1_tmp))
                    try:
                        cursor.execute(sql_insert)
                        conn.commit()
                    except Exception as e:
                        print(sql_insert)
                        print(e)
        cursor.close()
        conn.close()

    def transform_roman_num2_alabo(self, one_str):
        # 将罗马数字转化为阿拉伯数字
        define_dict = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        if one_str == '0':
            return 0
        else:
            res = 0
            for i in range(0, len(one_str)):
                if i == 0 or define_dict[one_str[i]] <= define_dict[one_str[i - 1]]:
                    res += define_dict[one_str[i]]
                else:
                    res += define_dict[one_str[i]] - 2 * define_dict[one_str[i - 1]]
            return res

    def get_level(self,x,y):
        conn = x
        cursor = conn.cursor()
        # 得到新的故障级别
        sql_get = 'select new_level from fault_level_mappings where OLD_LEVEL= \'%s\'' % y
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

