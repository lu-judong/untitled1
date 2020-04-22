import pymysql
import datetime

class supplier:
    def darams(self,sql):
        conn = pymysql.connect( '192.168.221.21', 'root', '123456', charset='utf8')
        cursor = conn.cursor()
        cursor.execute('use darams')
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    # 取故障单数量
    def faultNum(self,start,end,car,fault,pattern):
        # inner JOIN  cd_fault_pattern p on p.fault_object_id = r.real_fault_object_id and p.fault_pattern_id = r.real_fault_pattern_id
        if len(car) == 1:
            sql_car = 'and n.id = \'{}\''.format(car[0])
        else:
            sql_car = 'and n.id in {}'.format(car)

        sql_faultNum = '''
                      SELECT
                          h.fault_no as faultNo,
                          h.id as faultOrderId,
                          n.train_no as trainNo ,
                          t.train_type_desc,
                          ifnull( e.debugging_time, 0 ) as debugTime,
                          ifnull( e.diagnostic_time, 0 ) as diagnosticTime,
                          ifnull( e.repair_time, 0 ) as repairTime,
                          o.fault_object_code AS faultObjectCode,
						  o.fault_object_desc AS faultObjectDesc,
						  s.main_responsibility,
						  r.real_fault_pattern,
                          t.service_fault_class as serviceFaultClass,
                          ifnull(t.start_late, 0) as startLate,
                          ifnull(t.end_late, 0) as endLate,                      
                          d.fault_property as faultProperty,
                          r.safety_supervisio_fault as safetySupervisioFault,
                          d.occurrence_time as occurrenceTime,
                          t.accumulated_mileage as  accumulatedMileage
                          FROM
                          op_fault_order_header h
                          INNER JOIN op_fault_order_detail d ON d.fault_id = h.id
                          INNER JOIN op_train t ON d.id = t.fault_detail_id AND t.del_flag = 0
                          INNER JOIN cd_train_no n ON t.train_no = n.train_no
                          INNER JOIN op_fault_real r ON d.id = r.fault_detail_id
                          inner JOIN cd_fault_object o on r.real_fault_object_id = o.fault_object_id and o.train_no_id = n.id
                          
                          INNER JOIN op_fault_associated_subject s ON d.id = s.fault_detail_id
                          INNER JOIN cd_supplier cs ON cs.supplier_name = s.main_responsibility          
                          INNER JOIN op_fault_handle e ON r.id = e.real_fault_id
                          where                    
                              h.status != '已取消'
                              {}
                              {}                    
                              {}         
                              {}
                              {}   
                          '''.format(start,end,sql_car,fault,pattern)

        va = self.darams(sql_faultNum)
        d = {}
        d1 = {}
        if pattern != 'AND 1 = 1':
            for i in va:
                if i[3] in d.keys():
                    if i[10] in d[i[3]].keys():
                        d[i[3]][i[10]] += 1
                    else:
                        d[i[3]][i[10]] = 1
                else:
                    d[i[3]] = {}
                    if i[10] in d[i[3]].keys():
                        d[i[3]][i[10]] += 1
                    else:
                        d[i[3]][i[10]] = 1

                if i[9] in d1.keys():
                    if i[10] in d1[i[9]].keys():
                        d1[i[9]][i[10]] += 1
                    else:
                        d1[i[9]][i[10]] = 1

                else:
                    d1[i[9]] = {}
                    if i[10] in d1[i[9]].keys():
                        d1[i[9]][i[10]] += 1
                    else:
                        d1[i[9]][i[10]] = 1
        else:
            for i in va:
                if i[3] in d.keys():
                    if i[7] in d[i[3]].keys():
                        d[i[3]][i[7]] += 1
                    else:
                        d[i[3]][i[7]] = 1
                else:
                    d[i[3]] = {}
                    if i[7] in d[i[3]].keys():
                        d[i[3]][i[7]] += 1
                    else:
                        d[i[3]][i[7]] = 1

                if i[9] in d1.keys():
                    if i[7] in d1[i[9]].keys():
                        d1[i[9]][i[7]] += 1
                    else:
                        d1[i[9]][i[7]] = 1

                else:
                    d1[i[9]] = {}
                    if i[7] in d1[i[9]].keys():
                        d1[i[9]][i[7]] += 1
                    else:
                        d1[i[9]][i[7]] = 1


        return [d,d1]

    # 计算百万公里故障率
    def select_value(self, modelName, supplier):

        sql_no_obj = \
            '''
             SELECT
                d.start_date,
                d.end_date,
                d.average_speed_select,
                mi.start_mileage,
                mi.end_mileage,
                mi.average_speed,
                mt.train_no_id,
                o.fault_object_id,
                p.fault_pattern_id,
                sf.fault_define,
                mi.business_flag,
                lh.late_hours_from,
                lh.late_hours_to,
                lh.late_type
            FROM
                conf_model m 
                LEFT JOIN conf_model_train mt ON mt.conf_model_id = m.id 
                LEFT JOIN conf_fault_object o ON o.conf_model_id = m.id
                LEFT JOIN conf_fault_pattern p on p.conf_model_id = m.id
                LEFT JOIN conf_date d ON d.conf_model_id = m.id 
                LEFT JOIN conf_mileage mi on mi.conf_model_id = m.id
                LEFT JOIN conf_service_fault sf ON sf.conf_model_id = m.id
                LEFT JOIN conf_late_hours lh ON lh.conf_model_id = m.id
            WHERE 
                m.model_type = 'SUPPLIER_MODEL'
                and m.model_name = '{}'
                
            '''.format(modelName)
        input_value = self.darams(sql_no_obj)
        tuple_trainno = tuple(input_value[0][6].split(','))
        # print(tuple_trainno)
        if input_value[0][7] is not None:
            tuple_objids = tuple(input_value[0][7].split(','))
            if len(tuple_objids) == 1:
                sql_fault = 'and r.real_fault_object_id = {}'.format(input_value[0][4])
            else:
                tuple_objids = tuple(input_value[0][7].split(','))
                sql_fault = 'and r.real_fault_object_id in {}'.format(tuple_objids)
        if input_value[0][8] is not None:
            if len(input_value[0][8]) != 0:
                tuple_pattern = tuple(input_value[0][8].split(','))
                if len(tuple_pattern) == 1:
                    sql_pattern = 'and r.real_fault_pattern_id = {}'.format(input_value[0][8])
                else:
                    tuple_pattern = tuple(input_value[0][8].split(','))
                    sql_pattern = 'and r.real_fault_pattern_id in {}'.format(tuple_pattern)
            else:
                sql_pattern = 'AND 1 = 1'
        else:
            sql_pattern = 'AND 1 = 1'

        if input_value[0][0] is not None:
            sql_start = 'AND d.occurrence_time >= \'{}\''.format(input_value[0][0].strftime("%Y-%m-%d"))
            sql_end = 'AND d.occurrence_time < \'{}\''.format(input_value[0][1].strftime("%Y-%m-%d"))

            # 车型的数据,供应商的数据
            L = self.faultNum(sql_start, sql_end, tuple_trainno, sql_fault, sql_pattern)
        else:
            sql_start = 'AND t.accumulated_mileage >= {}'.format(input_value[0][3])
            sql_end = 'AND t.accumulated_mileage < {}'.format(input_value[0][4])
            # 车型的数据,供应商的数据
            L = self.faultNum(sql_start, sql_end, tuple_trainno, sql_fault, sql_pattern)
        # 车型的数据
        car_d = L[0]
        # 供应商的数据
        supplier_d  = L[1]

        print(car_d)
        if supplier == 'all':
            supplier_d1 = {}
            for i in supplier_d:
                for j in supplier_d[i]:
                    if j in supplier_d1.keys():
                        supplier_d1[j] += 1
                    else:
                        supplier_d1[j] = 1
            print(supplier_d1)
        else:
            print(supplier_d)


supplier().select_value('test','all')