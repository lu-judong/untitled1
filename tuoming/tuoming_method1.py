import cx_Oracle
import random


class Method1:
    def __init__(self):
        self.t_i = 1

    # 处理车型 车号
    def deal_cartype(self,x,y):
        conn = x
        cursor = conn.cursor()
        cartype_mapping = {}
        sql_mappings = 'select old_cartype,new_cartype from train_mappings where old_cartype = \'%s\' and rownum <=1 '% y
        cursor.execute(sql_mappings)
        mappings = cursor.fetchone()
        if mappings is not None:
            return mappings[1]
        else:
            # 判断cartype_mapping是否有值 没有则把 key-车型 value-新车型存入字典
            if cartype_mapping.__len__()==0:
                cartype_mapping.update({y:'%s型车' % self.t_i})
            else:
                if cartype_mapping.get(y) is None:
                    cartype_mapping.update({y: '%s型车' % self.t_i})
                else:
                    pass
            self.t_i+=1
        c_type = cartype_mapping.get(y)

        M = []
        sql_se = 'select cartype from random_mappings where cartype = \'%s\'' % c_type
        cursor.execute(sql_se)
        ses = cursor.fetchone()
        if ses is not None:
            pass
        else:
            m = random.sample(range(0,10000),10000)
            for i in m:
                M.append((c_type,i))

            sql_insert1 = 'insert into random_mappings(cartype,random_num) values(:1,:2)'
            cursor.prepare(sql_insert1)
            try:
                cursor.executemany(None,M[:])
                conn.commit()
                M = []
            except Exception as e:
                print(sql_insert1)
                print(e)

        return cartype_mapping.get(y)


    def deal_carnum(self,x,y,z):
        conn = x
        cursor = conn.cursor()

        # 查看映射表中有没有车号-新车号这条数据
        sql_mappings = 'select old_carnum,new_carnum from train_mappings where old_carnum = \'%s\'and rownum<=1' % z
        cursor.execute(sql_mappings)
        mappings = cursor.fetchone()
        if mappings is not None:
            return mappings[1]
        else:
            m = y
            c_first2num = m[:-2]
            sql_get = 'select random_num from random_mappings where cartype=\'%s\' and rownum <= 1' % m
            cursor.execute(sql_get)
            n1 = cursor.fetchone()
            new_carnum = c_first2num + n1[0].zfill(4) if len(c_first2num) > 1 else '0' + c_first2num + n1[0].zfill(4)

            sql_delete = 'delete from random_mappings where random_num = \'%s\'and cartype=\'%s\'' % (n1[0],m)
            try:
                cursor.execute(sql_delete)
                conn.commit()
            except Exception as e:
                print(sql_delete)
                print(e)
        return new_carnum

    def insert_table(self):
        conn = cx_Oracle.connect('dev/123456@127.0.0.1:1521/orcl')
        cursor = conn.cursor()
        sql_a= 'select PICTURE_NO,CARRIAGE from train_info_old order by PICTURE_NO '
        cursor.execute(sql_a)
        # 得到一个列表 列表中的每一项是车号的元组
        fields = cursor.fetchall()
        for tu in fields:
            sql_s = 'select old_cartype,old_carnum from train_mappings where old_cartype=\'%s\' and old_carnum=\'%s\'' % (tu[0],tu[1])
            cursor.execute(sql_s)
            mappings = cursor.fetchone()
            if mappings is not None:
                continue
            else:
                tu_0 = self.deal_cartype(conn,tu[0])
                tu_1 = self.deal_carnum(conn,tu_0,tu[1])
                sql_insert = 'insert into train_mappings(old_cartype,old_carnum,new_cartype,new_carnum) values (\'%s\',\'%s\',\'%s\',\'%s\')' % (tu[0],tu[1],tu_0,tu_1)
                try:
                    cursor.execute(sql_insert)
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    print(sql_insert)
                    print(e)

        cursor.close()
        conn.close()

    # 取出表中的新车型 返回给用户
    def get_cartype(self,x,y):
        conn = x
        cursor = conn.cursor()
        # print('I',datetime.datetime.now())
        #从新表中得到新车型 和 新车号
        sql_get = 'select NEW_CARTYPE from train_mappings where  OLD_CARTYPE= \'%s\' and rownum <= 1' % y
        # print('II',datetime.datetime.now())
        cursor.execute(sql_get)
        fields = cursor.fetchone()
        # print('III',datetime.datetime.now())
        if fields is not None:
            try:
                return fields[0]
            except Exception as e:
                print(e)
        else:
            return ''
        cursor.close()

    # 取出表中的新车号 返回给用户
    def get_carnum(self,x,y):
        conn = x
        cursor = conn.cursor()
        #从新表中得到新车型 和 新车号
        sql_get = 'select NEW_CARNUM from train_mappings where OLD_CARNUM= \'%s\' and rownum <= 1' % y
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




