import cx_Oracle
import datetime
from tuoming.tuoming_method1 import Method1
from tuoming.tuoming_method2 import Method2
from tuoming.tuoming_method3 import Method3
from tuoming.tuoming_method4 import Method4
from tuoming.tuoming_method5 import Method5
from tuoming.tuoming_method6 import Method6
from tuoming.tuoming_method7 import Method7
import re


class Table1:
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
        sql_count = "select count(*) from fault_fick_old"
        cursor.execute(sql_count)
        count1 = cursor.fetchone()
        # 控制循环得次数 一次去1w条 直到取完为止
        t_i = 0
        M = []
        for i in range(0,int(count1[0])//10000 + 1):
            sql_get1 = "select * from FAULT_FICK_OLD order by TICKET_NUMBER"
            sqlBu = self.string_page(sql_get1, t_i, 10000)
            cursor.execute(sqlBu)
            fields = cursor.fetchall()
            for tu in fields:
                sql_mappings = 'select TICKET_NUMBER, DEPARTMENT_DESCRIPTION, TRAIN_TYPE from FAULT_FICK where TICKET_NUMBER = \'%s\' and DEPARTMENT_DESCRIPTION=\'%s\' and TRAIN_TYPE=\'%s\'' % (tu[3],tu[4],tu[6])
                cursor.execute(sql_mappings)
                mappings = cursor.fetchone()
                if mappings is not None:
                    continue
                else:
                    t_0 = tu[0]
                    t_1 = tu[1]
                    t_2 = tu[2]
                    t_3 = Method7().reserve_last_two(tu[3])
                    t_4 = Method7().reserve_lastone(tu[4])
                    t_5 = tu[5]
                    t_6 = Method1().get_cartype(conn,tu[6])
                    t_7 = Method7().reserve_lastone(tu[7])
                    t_8 = tu[8]
                    t_9 = Method7().reserve_one_lastone(tu[9])
                    if tu[10] is not None:
                         a = Method1().get_cartype(conn,tu[10][:tu[10].find('.')])
                         b = Method7().all_change(tu[10][tu[10].find('.')+1:])
                         t_10 = a +'.'+ b
                    else:
                        t_10 = tu[10]

                    # 处理直观故障对象
                    if tu[11] is None:
                        t_11 = tu[11]
                    else:
                        a = re.split('\.', tu[11])
                        t_11 = ''
                        for i in a:
                            if i != a[-1]:
                                c = Method5().get_position(conn, i)
                                t_11 += c + '.'
                            else:
                                c = Method5().get_position(conn, i)
                                t_11 += c
                    t_12 = tu[12]
                    t_13= Method7().all_change(tu[13])
                    t_14 = Method6().get_appearance(conn,tu[14])
                    t_15 = tu[15]
                    t_16 = Method7().all_change(tu[16])
                    t_17 = tu[17]
                    t_18 = tu[18]
                    t_19 = Method3().get_level(conn,tu[19])
                    t_20 = Method4().get_reason(conn,tu[20])
                    t_21 = Method7().all_change(tu[21])
                    t_22 = Method7().reserve_one(tu[22])
                    t_23 = tu[23]
                    t_24 = Method7().all_change(tu[24])
                    t_25 = Method7().all_change(tu[25])
                    t_26 = Method2().get_dutytype(conn,tu[26])
                    t_27 = Method2().get_dutytype(conn, tu[27])
                    t_28 = Method7().all_change(tu[28])
                    t_29 = tu[29]
                    t_30 = tu[30]
                    t_31 = tu[31]
                    t_32 = tu[32]
                    t_33 = Method7().all_change(tu[33])
                    t_34 = tu[34]
                    t_35 = Method7().reserve_one_lastone(tu[35])
                    t_36 = tu[36]
                    t_37 = tu[37]
                    t_38 = tu[38]
                    t_39 = tu[39]
                    t_40 = tu[40]
                    t_41 = tu[41]
                    t_42 = tu[42]
                    t_43 = Method7().all_change(tu[43])
                    t_44 = Method7().all_change(tu[44])
                    t_45 = Method7().all_change(tu[45])
                    # 处理真实故障对象
                    if tu[46] is None:
                        t_46 = tu[46]
                    else:
                        d = re.split('\.', tu[46])
                        t_46 = ''
                        for u in d:
                            if u != d[-1]:
                                f = Method5().get_position(conn, u)
                                t_46 += f + '.'
                            else:
                                f = Method5().get_position(conn, u)
                                t_46 += f

                    t_47 = tu[47]
                    t_48 = Method7().all_change(tu[48])
                    t_49 = Method6().get_appearance(conn,tu[49])
                    t_50 = tu[50]
                    t_51 = Method7().all_change(tu[51])
                    t_52 = Method7().all_change(tu[52])
                    t_53 = Method7().all_change(tu[53])
                    t_54 = Method7().all_change(tu[54])
                    t_55 = Method7().all_change(tu[55])
                    t_56 = Method7().all_change(tu[56])
                    t_57 = Method7().all_change(tu[57])
                    t_58 = tu[58]
                    t_59 = tu[59]
                    t_60 = Method7().all_change(tu[60])
                    t_61 = Method7().all_change(tu[61])
                    t_62 = tu[62]
                    t_63 = Method7().all_change(tu[63])
                    t_64 = tu[64]
                    t_65 = tu[65]
                    t_66 = tu[66]
                    t_67 = tu[67]
                    t_68 = tu[68]
                    t_69 = Method7().all_change(tu[69])
                    t_70 = Method7().all_change(tu[70])
                    t_71 = tu[71]
                    t_72 = Method7().all_change(tu[72])
                    t_73 = Method7().all_change(tu[73])
                    t_74 = Method7().all_change(tu[74])
                    t_75 = tu[75]
                    t_76 = tu[76]
                    t_77 = Method7().all_change(tu[77])
                    t_78 = tu[78]
                    t_79 = Method7().all_change(tu[79])
                    t_80 = tu[80]
                    t_81 = tu[81]
                    t_82 = tu[82]
                    t_83 = Method1().get_carnum(conn,tu[83])
                    t_84 = tu[84]
                    t_85 = tu[85]
                    t_86 = tu[86]
                    t_87 = tu[87]
                    M.append((t_0,t_1,t_2,t_3,t_4,t_5,t_6,t_7,t_8,t_9,t_10,t_11,t_12,t_13,t_14,t_15,t_16,t_17,t_18,t_19,t_20,t_21,t_22,t_23,t_24,t_25,t_26,t_27,t_28,t_29,t_30,t_31,t_32,t_33,t_34,t_35,t_36,t_37,t_38,t_39,t_40,t_41,t_42,t_43,t_44,t_45,t_46,t_47,t_48,t_49,t_50,t_51,t_52,t_53,t_54,t_55,t_56,t_57,t_58,t_59,t_60,t_61,t_62,t_63,t_64,t_65,t_66,t_67,t_68,t_69,t_70,t_71,t_72,t_73,t_74,t_75,t_76,t_77,t_78,t_79,t_80,t_81,t_82,t_83,t_84,t_85,t_86,t_87))

            sql_insert = 'insert into fault_fick(rpt_id,organization_id,ticket_id,ticket_number,department_description,ticket_status,train_type,belong_seg,vehicle_no,fault_brief,fault_location,failure_object,ft_config_relation_id,other_fail_obj,fault_phenomenon,ft_appearance_id,other_fail_pnm,relax_position,occur_date,fault_level_name,reason_class_name,occur_place,accident_level_name,duty_type_name, run_crossing,fault_environment_name,resper_name,attribute12,line_trip,cumulate_mileage,ft_consequence_name,late_time,end_late_time,attribute11,service_req,ft_description,fault_type_name,submit_date,process_date,process_result_name,ft_flag1,ft_flag3,ft_flag5,submit_person_name,submit_department,contact_phone,real_failure_obj,real_ft_config_id,real_other_fail_obj,real_fault_phenomenon,real_ft_appearance_id,real_other_fail_pnm,reason_name,real_other_ft_reason,solve_desc,real_other_ft_solve,mr_title,mr_desc,fault_nature_name,diagnosis_time,initial_analysis,final_analysis,replace_num,repair_site_name,system_debug_time,repair_person_num,fault_repair_time,total_downtime,repair_property_name,initial_treatment,finally_treatment,ft_flag7,important_number,ft_fault_type_name,notice_note,done_time ,creation_date,created_by,last_update_date, last_update_by,id,isfailure,ft_config_ids,car_riage,hisid,whetherornot,isconfirmed,synchronizetime) values (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14,:15,:16,:17,:18,:19,:20,:21,:22,:23,:24,:25,:26,:27,:28,:29,:30,:31,:32,:33,:34,:35,:36,:37,:38,:39,:40,:41,:42,:43,:44,:45,:46,:47,:48,:49,:50,:51,:52,:53,:54,:55,:56,:57,:58,:59,:60,:61,:62,:63,:64,:65,:66,:67,:68,:69,:70,:71,:72,:73,:74,:75,:76,:77,:78,:79,:80,:81,:82,:83,:84,:85,:86,:87,:88)'
            cursor.prepare(sql_insert)
            try:
                cursor.executemany(None, M[:])
                print(2,datetime.datetime.now())
                conn.commit()
                M = []
                t_i += 10000
            except Exception as e:
                print(sql_insert)
                print(e)
        cursor.close()
        conn.close()

Table1().deal()

