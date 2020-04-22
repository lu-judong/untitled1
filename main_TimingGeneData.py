# -*- coding: utf-8 -*-
"""
Created on Sun May 19 17:34:46 2019

@author: 32908
"""
import csv
import random
import time 
from datetime import datetime
import pymysql
import uuid
# -----------------------------------------------------------------------------

def strTimeProp(start, end, prop, frmt):
    stime = time.mktime(time.strptime(start, frmt))
    etime = time.mktime(time.strptime(end, frmt))
    ptime = stime + prop * (etime - stime)
    return int(ptime)
def randomDate(start, end, frmt='%Y-%m-%d %H:%M:%S'):
    return time.strftime(frmt, time.localtime(strTimeProp(start, end, random.random(), frmt)))
# -----------------------------------------------------------------------------
def get_column(key,column_all):
    column = [row[key] for row in column_all]
    column = list(set(column))
    return column 
# -----------------------------------------------------------------------------
def gen_uuid():
    uuid_now = str(uuid.uuid4())
    uuid_tmp = uuid_now.split('-')
    uuid_now = "".join(uuid_tmp)
    return uuid_now
# -----------------------------------------------------------------------------
def get_faultobj():
    count = random.randint(0,4)
    list_obj = []
    with open("fault_object_all.csv","r",encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        column_all = [row for row in reader]
        if count != 0:
            for i in range(1,count+1):
                column = get_column(str(i),column_all)
                cho = random.choice(column)
                list_obj.append(cho)
            str_obj = ".".join(list_obj)
        else:
            str_obj = ''
        return str_obj
# -----------------------------------------------------------------------------
def write2mysql(list_all):
    db = pymysql.connect("192.168.1.21","root","123456",charset="utf8")
    cur = db.cursor()
    cur.execute("use darams")
    uuid_now = gen_uuid()
    time_now = datetime.now()
    sql = \
    '''
    INSERT INTO data_fault_order_simu VALUES('{}',{},'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',{},'{}','{}','{}','{}',{},\
    '{}','{}',{},'{}','{}','{}','{}','{}','{}','{}','{}','{}',{},'{}',{},{},'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',\
    '{}','{}','{}',{},'{}','{}',{},'{}','{}','{}','{}','{}','{}',{},'{}','{}',{},'{}',{},{},{},{},'{}','{}','{}','{}','{}',\
    'YX','{}','YX','{}','0','')
    '''.format(uuid_now,list_all[0],list_all[1],list_all[2],list_all[3],list_all[4],list_all[5],list_all[6],list_all[7],list_all[8],\
    list_all[9],list_all[10],list_all[11],list_all[12],list_all[13],list_all[14],list_all[15],list_all[16],list_all[17],\
    list_all[18],list_all[19],list_all[20],list_all[23],list_all[24],list_all[25],list_all[26],\
    list_all[27],list_all[28],list_all[29],list_all[30],list_all[31],list_all[32],list_all[33],list_all[34],list_all[35],\
    list_all[36],list_all[37],list_all[38],list_all[39],list_all[40],list_all[41],list_all[42],list_all[43],list_all[44],\
    list_all[45],list_all[46],list_all[47],list_all[48],list_all[49],list_all[50],list_all[51],list_all[52],list_all[53],\
    list_all[54],list_all[55],list_all[56],list_all[57],list_all[58],list_all[59],list_all[60],list_all[61],list_all[62],\
    list_all[63],list_all[64],list_all[65],list_all[66],list_all[67],list_all[68],list_all[69],list_all[70],list_all[71],\
    time_now,time_now)
    cur.execute(sql)
    db.commit()
    db.close()
#    print(sql)
# -----------------------------------------------------------------------------
def main(list_keys):
#    count = 1
#    if  count >= 1 \
#    and count <= 10:
    list_all = []
    start = '2018-06-02 12:12:12'
    end = '2018-11-01 00:00:00'
    with open("data_template.csv","r",encoding = "utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        column_all = [row for row in reader]
        for key in list_keys:
            if key in ['if_fault_id','intuitive_fault_object_id','intuitive_fault_pattern_id','accumulated_mileage',\
                       'real_fault_object_id','real_fault_pattern_id','replace_parts']:
                cho = random.randint(1,9999999)
            elif key in ['start_late','end_late','diagnostic_time','debugging_time','total_repair_counts','repair_time',\
                         'total_downtime']:
                cho = random.uniform(0,100)
                cho = round(cho,2)
            elif key == 'fault_no':
                cho = 'simu_' + str(list_all[0])
            elif key == 'train_no':
                continue
            elif key == 'train_type':
                column = get_column(key,column_all)
                cho = random.choice(column)
                cho_split = cho.split(':')
                list_all.append(cho_split[-1])
                cho = cho_split[0]
            elif key in ['occurrence_time','occurrence_time','report_time','processing_date']:
                cho = randomDate(start,end)
            elif key in ['fault_brief','configuration_location','intuitive_fault_object','intuitive_fault_object_desc',\
                         'intuitive_fault_pattern_desc','fault_desc','report_person','report_part','contact_tel',\
                         'real_fault_object','real_other_fault_object_desc','real_other_fault_pattern_desc','fault_cause',\
                         'other_fault_cause_desc','initial_cause_analysis','final_cause_analysis','initial_treatment_measures',\
                         'final_treatment_measures']:
                cho = get_faultobj()
            elif key in ['fault_environment','fault_result','other_solution','closed_loop_time']:
                cho = 'None'
            else:
                column = get_column(key,column_all)
                cho = random.choice(column)
            list_all.append(cho)
#    print(list_all)
#    print(len(list_all))
    write2mysql(list_all)
# -----------------------------------------------------------------------------
# if __name__ == "__main__":
#     list_keys = ['if_fault_id', 'fault_no', 'status', 'occurrence_time', 'occurrence_place', 'train_no', 'train_type', 'car_no', 'railway', 'report_position', 'cause_class', 'org_id', 'fault_level', 'fault_brief', 'configuration_location', 'intuitive_fault_object', 'intuitive_fault_object_id', 'intuitive_fault_object_desc', 'intuitive_fault_pattern', 'intuitive_fault_pattern_id', 'intuitive_fault_pattern_desc', 'reconnect_location', 'occurrence_time', 'occurrence_place', 'accident_level', 'responsibility_class', 'running_way', 'fault_environment', 'main_responsibility', 'other_responsibility', 'car_trips', 'accumulated_mileage', 'fault_result', 'start_late', 'end_late', 'fault_desc', 'fault_order_type', 'report_time', 'processing_date', 'processing_result', 'special_fault', 'safety_supervisio_fault', 'in_repair', 'startup_fault_analysis', 'report_person', 'report_part', 'contact_tel', 'real_fault_object', 'real_fault_object_id', 'real_other_fault_object_desc', 'real_fault_pattern', 'real_fault_pattern_id', 'real_other_fault_pattern_desc', 'fault_cause', 'other_fault_cause_desc', 'solution', 'other_solution', 'fault_property', 'diagnostic_time', 'initial_cause_analysis', 'final_cause_analysis', 'replace_parts', 'repair_location', 'debugging_time', 'total_repair_counts', 'repair_time', 'total_downtime', 'repair_property', 'initial_treatment_measures', 'final_treatment_measures', 'important_info_no', 'closed_loop_time']
# #    list_keys = ['if_fault_id','fault_no','status','occurrence_time','train_no','train_type','intuitive_fault_object']
#     main(list_keys)


get_faultobj()