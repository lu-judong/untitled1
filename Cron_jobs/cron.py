# from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from Cron_jobs.db_config import conn1
import uuid
import random
import csv
from datetime import datetime
import time
from Cron_jobs.log_config import logger

class Cron:
    def strTimeProp(self,start, end, prop, frmt):
        stime = time.mktime(time.strptime(start, frmt))
        etime = time.mktime(time.strptime(end, frmt))
        ptime = stime + prop * (etime - stime)
        return int(ptime)

    def get_uuid(self):
        uuid_now = str(uuid.uuid4())
        uuid_tmp = uuid_now.split('-')
        uuid_now = "".join(uuid_tmp)
        return uuid_now

    def randomDate(self, start, end, frmt='%Y-%m-%d %H:%M:%S'):
        return time.strftime(frmt, time.localtime(self.strTimeProp(start, end, random.random(), frmt)))

    def get_column(self, key):
        with open("data_template.csv", "r", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)
            column = [row['{}'.format(key)] for row in reader]
        column = list(set(column))
        return column

    # -----------------------------------------------------------------------------
    def get_faultobj(self):
        count = random.randint(0, 4)
        list_obj = []

        # column_all = [row for row in reader]
        if count != 0:
            for i in range(1, count + 1):
                with open("fault_object_all.csv", "r", encoding="utf-8-sig") as csvfile:
                    reader = csv.DictReader(csvfile)
                    column = [row['{}'.format(i)] for row in reader]
                    cho = random.choice(list(set(column)))
                    list_obj.append(cho)
            str_obj = ".".join(list_obj)
        else:
            str_obj = ''
        return str_obj

    def conn(self,sql):
        conn = conn1
        cur = conn.cursor()
        cur.execute("use darams")
        cur.execute(sql)
        a = cur.fetchall()
        return a

    # 获取表的所有字段
    def table_column(self,tableName):
        column_list = []
        sql = "select column_name from information_schema.COLUMNS where table_name = '{}' and table_schema = 'darams'".format(tableName)
        list1 = self.conn(sql)
        for i in list1:
            column_list.append(i[0])
        # print(column_list)
        return column_list

    # 处理数据
    def main(self, list_keys):
        #    count = 1
        #    if  count >= 1 \
        #    and count <= 10:
        list_all = []
        start = '2018-06-02 12:12:12'
        end = '2018-11-01 00:00:00'

        for key in list_keys:
            if key in ['if_fault_id']:
                cho = random.randint(1, 9999999)
            elif key in ['org_id']:
                column = self.get_column(key)
                cho1 = random.choice(column)
                while True:
                    if cho1 is not '':
                        cho = cho1
                        break
                    else:
                        cho1 = random.choice(column)
            elif key in ['report_part']:
                cho = random.randint(0,100)
                if cho < 10:
                    cho = '0' + str(cho)
            elif key in ['contact_tel']:
                cho = '18753270407'
            elif key in ['fault_desc','fault_brief']:
                cho = '故障详述模式00002'
            elif key in ['diagnostic_time', 'debugging_time', 'repair_time','total_downtime']:
                cho1 = random.uniform(0,1)
                cho = round(cho1, 1)
            elif key in ['start_late', 'end_late', 'total_repair_counts', 'replace_parts']:
                cho = random.randint(0, 10)
            elif key == 'fault_no':
                cho = 'test_' + str(list_all[0])
            elif key in ['initial_treatment_measures','final_treatment_measures']:
                cho = '解决方案模式00003'
            elif key in ['final_cause_analysis','initail_cause_analysis']:
                cho = '原因模式00003'
            elif key in ['report_time', 'processing_date']:
                cho = self.randomDate(start, end)
            elif key in ['fault_cause', 'other_fault_cause_desc']:
                cho = self.get_faultobj()
            elif key in ['fault_result', 'other_solution', 'closed_loop_time']:
                cho = 'None'
            elif key in ['create_by', 'update_by', 'report_person']:
                cho = 'LJD'
            elif key in ['create_date','update_date','occurrence_time']:
                time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cho = time_now
            elif key in ['del_flag']:
                cho = 0
            elif key in ['service_fault_class']:
                cho = '无影响'
            else:
                column = self.get_column(key)
                cho = random.choice(column)
            list_all.append(cho)
        return list_all

    # 递推生成真实故障对象
    def aa(self,real_fault_object_id,x,L):
        conn = x
        cur = conn.cursor()
        sql_real_fault_object = '''select fault_node,parent_fault_node from cd_fault_object_tree where id = '{}' '''.format(
            real_fault_object_id)
        cur.execute(sql_real_fault_object)
        r_id = cur.fetchall()
        for i in r_id:
            if i[1] is not None:
                L.append(i[0])
                self.aa(i[1],conn,L)
            else:
                L.append(i[0])
        return L

    def insert(self):
        conn = conn1

        cur = conn.cursor()
        cur.execute("use darams")
        for i in range(0,30):
            logger.debug('---start{}---'.format(i))
            # 插入数据到op_fault_header表
            id = self.get_uuid()
            while True:
                sql_select = '''select id from op_fault_order_header where id = '{}' '''.format(id)
                cur.execute(sql_select)
                h_id = cur.fetchone()
                if h_id is not None:
                    id = self.get_uuid()
                else:
                    break

            L = self.table_column('op_fault_order_header')
            L.remove('id')
            L.remove('remarks')
            L1 = self.main(L)
            # print(L)
            # print(L1)

            # sql = '''insert into op_fault_order_header values''' + '{}'.format(end_str)
            if i == 15:
                try:
                    sql = '''insert into op_fault_order_header values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',{},'{}')'''.format(id,L1[0],L1[1],'fault_{}'.format(random.randint(0,100)),L1[3],L1[4],L1[5],L1[6],L1[7],L1[8],'null',L1[9])
                    cur.execute(sql)
                except Exception as e:
                    logger.error(e)
                    logger.debug('---header---')
            else:
                try:
                    sql = '''insert into op_fault_order_header values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',{},'{}')'''.format(id,L1[0],L1[1],L1[2],L1[3],L1[4],L1[5],L1[6],L1[7],L1[8],'null',L1[9])
                    cur.execute(sql)
                except Exception as e:
                    logger.error(e)
                    logger.debug('---header---')


            # 插入数据到op_fault_detail 表
            detail_id = self.get_uuid()
            while True:
                sql_select1 = '''select id from op_fault_order_detail where id = '{}' '''.format(detail_id)
                cur.execute(sql_select1)
                d_id = cur.fetchone()
                if d_id is not None:
                    detail_id = self.get_uuid()
                else:
                    break

            detail_fault_id = id
            L_detail = self.table_column('op_fault_order_detail')
            L_detail.remove('id')
            L_detail.remove('fault_id')
            L_detail.remove('remarks')
            L1_detail = self.main(L_detail)

            try:
                sql_detail = '''insert into op_fault_order_detail values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',{},'{}','{}','{}','{}','{}','{}','{}','{}','{}')'''.format(detail_id,detail_fault_id,L1_detail[0],L1_detail[1],L1_detail[2],L1_detail[3],L1_detail[4],L1_detail[5],L1_detail[6],L1_detail[7],L1_detail[8],L1_detail[9],         L1_detail[10],L1_detail[11],L1_detail[12],L1_detail[13],'null',L1_detail[14],L1_detail[15],L1_detail[16],L1_detail[17],L1_detail[18],L1_detail[19],L1_detail[20],L1_detail[21],L1_detail[22])
                cur.execute(sql_detail)
            except Exception as e:
                logger.error(e)
                logger.debug('--detail--')
            # 插入数据到op_fault_associated_business 表
            ass_id = self.get_uuid()
            while True:
                sql_select2 = '''select id from op_fault_associated_business where id = '{}' '''.format(ass_id)
                cur.execute(sql_select2)
                a_id = cur.fetchone()
                if a_id is not None:
                    ass_id = self.get_uuid()
                else:
                    break

            ass_detail_id = detail_id
            L_ass = self.table_column('op_fault_associated_business')
            L_ass.remove('id')
            L_ass.remove('remarks')
            L_ass.remove('fault_detail_id')
            L_ass.remove('solution_process_no')
            L_ass.remove('solution_process_desc')
            L_ass.remove('other_solution')
            L1_ass = self.main(L_ass)
            # print(L1_ass)
            try:
                sql_associated = '''insert into op_fault_associated_business values('{}','{}','{}','{}','{}',{},'{}','{}','{}',{},'{}',{})'''.format(ass_id, L1_ass[0], L1_ass[1], L1_ass[2], L1_ass[3], 'null', L1_ass[4], ass_detail_id,
                    L1_ass[5], 'null', 'GZ201706190024','null')
                cur.execute(sql_associated)
            except Exception as e:
                logger.error(e)
                logger.debug('--associated--')

            # 插入数据到op_fault_associated_subject 表
            associated_subject_id = self.get_uuid()
            while True:
                sql_select3 = '''select id from op_fault_associated_subject where id = '{}' '''.format(associated_subject_id)
                cur.execute(sql_select3)
                a_s_id = cur.fetchone()
                if a_s_id is not None:
                    associated_subject_id = self.get_uuid()
                else:
                    break
            associated_subject_detail_id = detail_id
            L_ass_sub = self.table_column('op_fault_associated_subject')
            L_ass_sub.remove('id')
            L_ass_sub.remove('remarks')
            L_ass_sub.remove('fault_detail_id')
            L_ass_sub.remove('other_responsibility')

            L1_ass_sub = self.main(L_ass_sub)
            # print(L1_ass_sub)

            try:
                sql_associated_subject = '''insert into op_fault_associated_subject values('{}','{}','{}','{}','{}',{},'{}','{}','{}','{}',{})'''.format(associated_subject_id, L1_ass_sub[0], L1_ass_sub[1], L1_ass_sub[2], L1_ass_sub[3], 'null', L1_ass_sub[4], associated_subject_detail_id,L1_ass_sub[5], L1_ass_sub[6], 'null')
                cur.execute(sql_associated_subject)
            except Exception as e:
                logger.error(e)
                logger.debug('---associated_subject---')

            # 插入数据到op_fault_real表
            real_id = self.get_uuid()
            while True:
                sql_select7 = '''select id from op_fault_real where id = '{}' '''.format(real_id)
                cur.execute(sql_select7)
                r_id = cur.fetchone()
                if r_id is not None:
                    real_id = self.get_uuid()
                else:
                    break

            real_detail_id = detail_id

            # 随机生成一个部件
            sql_relationship_id = 'select DISTINCT(relationship_id) from cd_fault_object '
            cur.execute(sql_relationship_id)
            r_id = cur.fetchall()
            L = []
            for i in r_id:
                if i[0] is not None:
                    L.append(i[0])

            relationship_id = L[random.randint(0, len(L) - 1)]

            # 生成真实部件对象id
            sql_real_fault_object_id = '''select DISTINCT(fault_object_id) from cd_fault_object where relationship_id = '{}' '''.format(relationship_id)
            cur.execute(sql_real_fault_object_id)
            re_id = cur.fetchall()

            L2 = []
            for i in re_id:
                if i[0] is not None:
                    L2.append(i[0])
            real_fault_object_id = L2[random.randint(0, len(L2) - 1)]

            # 根据部件随机生成车 插入op_train表中
            sql_op_train_train_no = '''select DISTINCT(train_no_id) from cd_fault_object where fault_object_id = '{}' '''.format(real_fault_object_id)

            cur.execute(sql_op_train_train_no)
            tr_id = cur.fetchall()

            L3 = []
            for i in tr_id:
                if i[0] is not None:
                    L3.append(i[0])
            train_no_id = L3[random.randint(0, len(L3) - 1)]

            # 去cd_train_no表中取出车型的id和车号
            sql_train_no_train = '''select train_type_id,train_no from cd_train_no where id = '{}' '''.format(train_no_id)
            cur.execute(sql_train_no_train)
            train = cur.fetchall()
            train_type_id = train[0][0]
            train_no = train[0][1]

            # 去cd_train_type表中取出车型
            sql_train_no_train_type = '''select train_type_code from cd_train_type where id = '{}' '''.format(
                train_type_id)
            cur.execute(sql_train_no_train_type)
            tr_type = cur.fetchall()

            train_type = tr_type[0][0]

            # 生成位置串
            real_fault_object = train_type
            real_fault_object_L = list(reversed(self.aa(relationship_id, conn, [])))
            for i in real_fault_object_L:
                real_fault_object += '.' + i

            sql_real_fault_pattern_id = '''select fault_pattern_id from cd_fault_pattern where fault_object_id = '{}' '''.format(real_fault_object_id)

            cur.execute(sql_real_fault_pattern_id)
            p_id = cur.fetchall()
            L1 = []
            for i in p_id:
                if i[0] is not None:
                    L1.append(i[0])

            if len(L1) != 0:
                real_fault_pattern_id = L1[random.randint(0, len(L1) - 1)]
            else:
                real_fault_pattern_id = 'null'

            if real_fault_pattern_id == 'null':
                real_fault_pattern = 'null'

                try:
                    sql_real = '''insert into op_fault_real values('{}','{}','{}','{}','{}',{},'{}','{}','{}','{}',{},{},{},{},{},{},{},{},{},{},{})'''.format(real_id, L1_ass_sub[0], L1_ass_sub[1], L1_ass_sub[2], L1_ass_sub[3], 'null',L1_ass_sub[4], real_detail_id, real_fault_object, real_fault_object_id, 'null', 'null',real_fault_pattern_id, 'null', 'null', 'null', 'null', 'null', real_fault_pattern,real_fault_pattern, 'null')
                    cur.execute(sql_real)
                except Exception as e:
                    logger.error(e)
                    logger.debug('--real--')
            else:
                sql_real_fault_pattern = '''select fault_pattern_desc from cd_fault_pattern where fault_pattern_id= '{}' '''.format(real_fault_pattern_id)
                cur.execute(sql_real_fault_pattern)
                pa_id = cur.fetchone()
                real_fault_pattern = pa_id[0]

                try:
                    sql_real = '''insert into op_fault_real values('{}','{}','{}','{}','{}',{},'{}','{}','{}','{}',{},{},'{}',{},{},{},{},{},'{}','{}',{})'''.format( real_id, L1_ass_sub[0], L1_ass_sub[1], L1_ass_sub[2], L1_ass_sub[3], 'null',L1_ass_sub[4], real_detail_id, real_fault_object, real_fault_object_id, 'null', 'null',real_fault_pattern_id, 'null', 'null', 'null', 'null', 'null', real_fault_pattern,real_fault_pattern, 'null')
                    cur.execute(sql_real)
                except Exception as e:
                    logger.error(e)
                    logger.debug('--real--')

            # 插入数据到op_train 表
            train_id = self.get_uuid()

            while True:
                sql_select4 = '''select id from op_train where id = '{}' '''.format(train_id)
                cur.execute(sql_select4)
                t_id = cur.fetchone()
                if t_id is not None:
                    train_id = self.get_uuid()
                else:
                    break

            train_detail_id = detail_id
            L_train = self.table_column('op_train')
            L_train.remove('id')
            L_train.remove('fault_detail_id')
            L_train.remove('remarks')
            L_train.remove('fault_time_flag')
            L_train.remove('train_type_desc')
            L_train.remove('train_no')
            L_train.remove('accumulated_mileage')
            L_train.remove('origin_accu_mileage')

            L1_train = self.main(L_train)
            # print(L1_train)
            # 根据车号生成相应的里程
            sql_accumulated_mileage = '''
                SELECT
                distinct 
                        t.accumulated_mileage,
                        d.occurrence_time
                FROM
                        op_fault_order_detail d
                        INNER JOIN op_train t ON t.fault_detail_id = d.id
                        INNER JOIN op_fault_order_header h on d.fault_id = h.id
                WHERE
                        1 = 1
                        AND t.train_no = '{}'
                        AND h.del_flag = '0'
                        AND d.occurrence_time <= '{}'
                        AND h.status !='已取消'									
                        order by d.occurrence_time desc 
                        LIMIT 1
                '''.format(train_no,L1_train[1])
            cur.execute(sql_accumulated_mileage)

            acc_mi = cur.fetchone()
            if acc_mi is None:
                if i == 15:
                    accumulated_mileage = 0 - random.randint(1000,10000)
                else:
                    accumulated_mileage = random.randint(100, 1000)

            else:
                if i == 15:
                    accumulated_mileage = acc_mi[0] - random.randint(1000,10000)
                else:
                    accumulated_mileage = acc_mi[0] + random.randint(100, 1000)
            try:
                sql_train = '''insert into op_train values('{}','{}','{}','{}','{}',{},'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',{})'''.format(train_id,L1_train[0],L1_train[1],L1_train[2],L1_train[3],'null',L1_train[4],train_detail_id,train_type,L1_train[5],L1_train[6],L1_train[7],L1_train[8],accumulated_mileage,accumulated_mileage,L1_train[9],L1_train[10],train_no,L1_train[11],'null')
                cur.execute(sql_train)
            except Exception as e:
                logger.error(e)
                logger.debug('---train---')

            # 插入数据到po_fault_location 表
            location_id = self.get_uuid()

            while True:
                sql_select5 = '''select id from op_fault_location where id = '{}' '''.format(location_id)
                cur.execute(sql_select5)
                l_id = cur.fetchone()
                if l_id is not None:
                    location_id = self.get_uuid()
                else:
                    break

            L_location = self.table_column('op_fault_location')
            L_location.remove('id')
            L_location.remove('op_train_id')
            L_location.remove('remarks')
            L_location.remove('configuration_location')
            L_location.remove('falut_environment')

            L1_location = self.main(L_location)
            # print(L1_location)
            if L1_location[5]  == '':
                configuration_location = train_type
            else:
                configuration_location = real_fault_object

            try:
                sql_location = '''insert into op_fault_location values('{}','{}','{}','{}','{}',{},'{}','{}','{}','{}',{})'''.format(location_id, L1_location[0], L1_location[1], L1_location[2], L1_location[3], 'null', L1_location[4],train_id, configuration_location, L1_location[5], 'null')
                cur.execute(sql_location)
            except Exception as e:
                logger.error(e)
                logger.debug('---location---')

            # 插入数据到op_fault_intuitive
            intuitive_id = self.get_uuid()
            while True:
                sql_select6 = '''select id from op_fault_intuitive where id = '{}' '''.format(intuitive_id)
                cur.execute(sql_select6)
                i_id = cur.fetchone()
                if i_id is not None:
                    intuitive_id = self.get_uuid()
                else:
                    break
            intuitive_detail_id = detail_id
            intuitive_fault_object_handled = real_fault_object
            # print(L1_intuitive)
            if real_fault_pattern_id == 'null':
                try:
                    sql_intuitive = '''insert into op_fault_intuitive values('{}','{}','{}','{}','{}',{},'{}','{}','{}','{}','{}',{},'{}',{},{},{},'{}')'''.format(intuitive_id, L1_location[0], L1_location[1], L1_location[2], L1_location[3], 'null',
    L1_location[4], intuitive_detail_id, intuitive_fault_object_handled, intuitive_fault_object_handled,real_fault_object_id, 'null', real_fault_pattern, real_fault_pattern_id, 'null', 'null',real_fault_pattern)
                    cur.execute(sql_intuitive)
                except Exception as e:
                    logger.error(e)
                    logger.debug('---intuitive---')
            else:
                try:
                    sql_intuitive = '''insert into op_fault_intuitive values('{}','{}','{}','{}','{}',{},'{}','{}','{}','{}','{}',{},'{}','{}',{},{},'{}')'''.format(intuitive_id, L1_location[0], L1_location[1], L1_location[2], L1_location[3],'null',L1_location[4],intuitive_detail_id,intuitive_fault_object_handled,intuitive_fault_object_handled,real_fault_object_id,'null',real_fault_pattern,real_fault_pattern_id,'null','null',real_fault_pattern)
                    cur.execute(sql_intuitive)
                except Exception as e:
                    logger.error(e)
                    logger.debug('---intuitive---')


            # 插入数据到op_fault_handle表
            handle_id = self.get_uuid()
            while True:
                sql_select8 = '''select id from op_fault_handle where id = '{}' '''.format(handle_id)
                cur.execute(sql_select8)
                h_id = cur.fetchone()
                if h_id is not None:
                    handle_id = self.get_uuid()
                else:
                    break

            handle_real_id = real_id
            L_handle = self.table_column('op_fault_handle')
            L_handle.remove('id')
            L_handle.remove('remarks')
            L_handle.remove('real_fault_id')
            L_handle.remove('service_station')
            L_handle.remove('repair_properety')
            L_handle.remove('cause_class')
            L1_handle = self.main(L_handle)
            # print(L1_handle)

            try:
                sql_handle = '''insert into op_fault_handle values('{}','{}','{}','{}','{}',{},'{}','{}',{},'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',{})'''.format(handle_id, L1_handle[0], L1_handle[1], L1_handle[2], L1_handle[3], 'null',L1_handle[4], handle_real_id, 'null', L1_handle[5],L1_handle[6],L1_handle[7], L1_handle[8],L1_handle[9],L1_handle[10], L1_handle[11], L1_handle[12], L1_handle[13],L1_handle[14],'现车可更换','null')
                cur.execute(sql_handle)
            except Exception as e:
                logger.error(e)
                logger.debug('---handle---')

            # 插入op_special_diagnosis表
            special_id = self.get_uuid()
            while True:
                sql_select9 = '''select id from op_special_diagnosis where id = '{}' '''.format(special_id)
                cur.execute(sql_select9)
                s_id = cur.fetchone()
                if s_id is not None:
                    special_id = self.get_uuid()
                else:
                    break

            special_real_id = real_id
            try:
                sql_special = '''insert into op_special_diagnosis values('{}','{}','{}','{}','{}',{},'{}','{}',{},'{}',{},{},'{}','{}','{}','{}',{},{},{})'''.format(special_id, L1_handle[0], L1_handle[1], L1_handle[2], L1_handle[3], 'null', L1_handle[5], special_real_id,'null', '*', 'null', 'null', 'null', '空', 'CRH2A/CRH380A-WTJL-2013-002', '空,','null', 'null', random.randint(1,10000))
                cur.execute(sql_special)
            except Exception as e:
                logger.error(e)
                logger.debug('---end---')
            # print(sql)
            # print(sql_detail)
            # print(sql_train)
            # print(sql_location)
            # print(sql_associated)
            # print(sql_associated_subject)
            # print(sql_handle)
            # print(sql_real)
            # print(sql_special)
            # print(sql_intuitive)
        conn.commit()
        cur.close()
        conn.close()

    def scheduler1(self):
        scheduler = BlockingScheduler()
        scheduler.add_job(self.insert, 'cron', hour=15, minute=2)
        print('start success')
        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            pass


Cron().scheduler1()
# Cron().insert()

