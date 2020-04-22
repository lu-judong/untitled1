import cx_Oracle

# 参考方案二
class Method2:
    def deal(self):
        conn = cx_Oracle.connect('dev/123456@127.0.0.1:1521/orcl')
        cursor = conn.cursor()
        # 取出DUTY_TYPE_NAME 对应的供应商的值
        sql = 'select DUTY_TYPE_NAME,RESPER_NAME from fault_fick_old order by DUTY_TYPE_NAME'
        cursor.execute(sql)
        fields = cursor.fetchall()

        # 抽取resper_mappings中 duty_type_name = 'SEQUENCE' 的数据
        sql_get = "select old_resper,type_name,new_resper from resper_mappings where duty_type_name='sequence'"
        cursor.execute(sql_get)
        name1 = cursor.fetchone()
        # 有结果
        if name1 is not None:
        #  i = old_resper， j=type_name  ，  k=new_resper
            t_i = int(name1[0])
            t_j = int(name1[1])
            t_k = int(name1[2])
            update_flag = True
        # 没有结果
        else:
            # i=1  j=1  k =1
            t_i = 1
            t_j = 1
            t_k = 1
            # update_flag = false
            update_flag = False

        resper_mapping = {}
        for tu in fields:
            # 判断映射表中有没有这条数据
            sql_mappings = "select duty_type_name, old_resper from resper_mappings where duty_type_name=\'%s\'and old_resper=\'%s\'" % (tu[0],tu[1])
            cursor.execute(sql_mappings)
            mappings = cursor.fetchone()
            if mappings is not None:
                continue
            else:
                tu_1_tmp = ''
                if tu[1] != '技术中心':
                    # 如果DUTY_TYPE_NAME 是厂内单位的话
                    if tu[0] == '厂内单位':
                        if tu[1] is None:
                            tu_1_tmp = 'internal_null'
                            if resper_mapping.__len__() == 0:
                                resper_mapping.update({tu_1_tmp: '部门%s' % t_i})
                                t_i += 1
                            else:
                                if resper_mapping.get(tu_1_tmp) is None:
                                    resper_mapping.update({tu_1_tmp: '部门%s' % t_i})
                                    t_i += 1
                                else:
                                    pass
                        else:
                            tu_1_tmp = tu[1]
                            if resper_mapping.__len__() == 0:
                                resper_mapping.update({tu_1_tmp: '部门%s' % t_i})
                                t_i += 1
                            else:
                                if resper_mapping.get(tu_1_tmp) is None:
                                    resper_mapping.update({tu_1_tmp: '部门%s' % t_i})
                                    t_i += 1
                                else:
                                    pass
                    # 如果DUTY_TYPE_NAME 是厂外单位的话
                    elif tu[0] == '厂外单位':
                        if tu[1] is None:
                            tu_1_tmp = 'external_null'
                            if resper_mapping.__len__() == 0:
                                resper_mapping.update({tu_1_tmp: '供应%s厂' % t_j})
                                t_j += 1
                            if resper_mapping.get(tu_1_tmp) is None:
                                resper_mapping.update({tu_1_tmp: '供应%s厂' % t_j})
                                t_j += 1
                            else:
                                pass
                        else:
                            tu_1_tmp = tu[1]
                            if resper_mapping.__len__() == 0:
                                resper_mapping.update({tu_1_tmp: '供应%s厂' % t_j})
                                t_j += 1
                            if resper_mapping.get(tu_1_tmp) is None:
                                resper_mapping.update({tu_1_tmp: '供应%s厂' % t_j})
                                t_j += 1
                            else:
                                pass
                    # 如果DUTY_TYPE_NAME 是用户单位
                    elif tu[0] == '用户单位':
                        if tu[1] is None:
                            tu_1_tmp = 'userternal_null'
                            if resper_mapping.__len__() == 0:
                                resper_mapping.update({tu_1_tmp: '用户%s' % t_k})
                                t_k += 1
                            if resper_mapping.get(tu_1_tmp) is None:
                                resper_mapping.update({tu_1_tmp: '用户%s' % t_k})
                                t_k += 1
                            else:
                                pass
                        else:
                            tu_1_tmp = tu[1]
                            if resper_mapping.__len__() == 0:
                                resper_mapping.update({tu_1_tmp: '用户%s' % t_k})
                                t_k += 1
                            if resper_mapping.get(tu_1_tmp) is None:
                                resper_mapping.update({tu_1_tmp: '用户%s' % t_k})
                                t_k += 1
                            else:
                                pass
                    # 当duty_type_name 为无法识别的时候
                    elif tu[0] == '无法识别':
                        if tu[1] is None:
                            tu_1_tmp = 'noternal_null'
                            if resper_mapping.__len__() == 0:
                                resper_mapping.update({tu_1_tmp: '用户%s' % t_k})
                                t_k += 1
                            if resper_mapping.get(tu_1_tmp) is None:
                                resper_mapping.update({tu_1_tmp: '用户%s' % t_k})
                                t_k += 1
                            else:
                                pass
                        else:
                            tu_1_tmp = tu[1]
                            if resper_mapping.__len__() == 0:
                                resper_mapping.update({tu_1_tmp: '用户%s' % t_k})
                                t_k += 1
                            if resper_mapping.get(tu_1_tmp) is None:
                                resper_mapping.update({tu_1_tmp: '用户%s' % t_k})
                                t_k += 1
                            else:
                                pass
                    # 当duty_type_name 为空的时候
                    else:
                        if tu[1] is None:
                            tu_1_tmp = 'nuternal_null'
                            if resper_mapping.__len__() == 0:
                                resper_mapping.update({tu_1_tmp: '用户%s' % t_k})
                                t_k += 1
                            if resper_mapping.get(tu_1_tmp) is None:
                                resper_mapping.update({tu_1_tmp: '用户%s' % t_k})
                                t_k += 1
                            else:
                                pass
                        else:
                            tu_1_tmp = tu[1]
                            if resper_mapping.__len__() == 0:
                                resper_mapping.update({tu_1_tmp: '用户%s' % t_k})
                                t_k += 1
                            if resper_mapping.get(tu_1_tmp) is None:
                                resper_mapping.update({tu_1_tmp: '用户%s' % t_k})
                                t_k += 1
                            else:
                                pass
                else:
                    tu_1_tmp = tu[1]
                    resper_mapping.update({tu_1_tmp: '技术中心'})




                sql_insert = 'insert into resper_mappings(duty_type_name,old_resper,type_name,new_resper) values (\'%s\',\'%s\',\'%s\',\'%s\')' % (tu[0],tu[1],tu[0],resper_mapping.get(tu_1_tmp))
                try:
                    cursor.execute(sql_insert)
                    conn.commit()
                except Exception as e:
                    print(sql_insert)
                    print(e)

        # 存储ijk的值
        # update_FLAG 如果true  ， update
        if update_flag is True:
            sql_update = "update resper_mappings set old_resper = \'%s\',type_name = \'%s\',new_resper = \'%s\' where duty_type_name = 'sequence'" % (str(t_i - 1),str(t_j - 1),str(t_k -1))
            try:
                cursor.execute(sql_update)
                conn.commit()
                cursor.close()
                conn.close()
            except Exception as e:
                print(sql_update)
                print(e)

        #  false，insert
        else:
            #  需要修改的内容， duty_type_name = 'SEQUENCE'  old_resper = i+1  type_name = j+1   new_resper=k+1
            sql_ins =  'insert into resper_mappings(duty_type_name,old_resper,type_name,new_resper) values (\'%s\',\'%s\',\'%s\',\'%s\')' % ('sequence',str(t_i),str(t_j),str(t_k))
            try:
                cursor.execute(sql_ins)
                conn.commit()
                cursor.close()
                conn.close()
            except Exception as e:
                print(sql_ins)
                print(e)

    def get_dutytype(self,x,y):
        conn = x
        cursor = conn.cursor()
        sql_get = 'select NEW_RESPER from resper_mappings where  OLD_RESPER= \'%s\'' % y
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





