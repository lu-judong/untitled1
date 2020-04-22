import pymysql
import datetime

class Moremodel:
    def darams(self,sql):
        conn = pymysql.connect( '192.168.221.21', 'root', '123456', charset='utf8')
        cursor = conn.cursor()
        cursor.execute('use darams')
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    # 取故障单数量
    def faultNum(self, start, end, car, fault, pattern, latefrom, lateto, latetype):

        if len(car) == 1:
            sql_car = 'and n.id = \'{}\''.format(car[0])
        else:
            sql_car = 'and n.id in {}'.format(car)

        sql_faultNum = '''
                      SELECT
                          h.fault_no as faultNo,
                          h.id as faultOrderId,
                          n.id as trainId,
                          ifnull( e.debugging_time, 0 ) as debugTime,
                          ifnull( e.diagnostic_time, 0 ) as diagnosticTime,
                          ifnull( e.repair_time, 0 ) as repairTime,
                          o.fault_object_code AS faultObjectCode,
                          o.fault_object_desc AS faultObjectDesc,
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
                          '''.format(start, end, sql_car, fault, pattern)

        va = self.darams(sql_faultNum)
        d = {}

        for j in va:
            if '基本故障' in d.keys():
                d['基本故障'].append(j[2])
            else:
                d['基本故障'] = []
                d['基本故障'].append(j[2])

            if j[-4] in d.keys():
                d[j[-4]].append(j[2])
            else:
                d[j[-4]] = []
                d[j[-4]].append(j[2])

            if j[-3] == '是' and j[-4] == '关联故障':
                if '安监故障' in d.keys():
                    d['安监故障'].append(j[2])
                else:
                    d['安监故障'] = []
                    d['安监故障'].append(j[2])
            # 判断服务故障
            if j[-4] == '关联故障':
                if j[-7] == '掉线' or j[-7] == '未出库':
                    if '服务故障' in d.keys():
                        d['服务故障'].append(j[2])
                    else:
                        d['服务故障'] = []
                        d['服务故障'].append(j[2])
                elif j[-7] == '晚点':
                    if latetype is not None:
                        if latetype == 'start':
                            if latefrom is not None:
                                if j[-6] >= latefrom:
                                    if '服务故障' in d.keys():
                                        d['服务故障'].append(j[2])
                                    else:
                                        d['服务故障'] = []
                                        d['服务故障'].append(j[2])
                        elif latetype == 'end':
                            if lateto is not None:
                                if j[-5] <= lateto:
                                    if '服务故障' in d.keys():
                                        d['服务故障'].append(j[2])
                                    else:
                                        d['服务故障'] = []
                                        d['服务故障'].append(j[2])
                        elif latetype == 'either':
                            if lateto is not None and latefrom is None:
                                if j[-5] <= lateto:
                                    if '服务故障' in d.keys():
                                        d['服务故障'].append(j[2])
                                    else:
                                        d['服务故障'] = []
                                        d['服务故障'].append(j[2])
                            elif latefrom is not None and lateto is None:
                                if j[-6] >= latefrom:
                                    if '服务故障' in d.keys():
                                        d['服务故障'].append(j[2])
                                    else:
                                        d['服务故障'] = []
                                        d['服务故障'].append(j[2])
                            elif latefrom is not None and lateto is not None:
                                if j[-6] >= latefrom or j[-5] <= lateto:
                                    if '服务故障' in d.keys():
                                        d['服务故障'].append(j[2])
                                    else:
                                        d['服务故障'] = []
                                        d['服务故障'].append(j[2])
                        elif latetype == 'both':
                            if lateto is not None and latefrom is not None:
                                if j[-6] >= latefrom and j[-5] <= lateto:
                                    if '服务故障' in d.keys():
                                        d['服务故障'].append(j[2])
                                    else:
                                        d['服务故障'] = []
                                        d['服务故障'].append(j[2])
        return d

    # 根据时间查实际行驶里程:
    def mtbf_km(self, start, end, car):
        a = 0
        if len(car) == 1:
            sql_car = 'and n.id = \'{}\''.format(car[0])
        else:
            sql_car = 'and n.id in {}'.format(car)
        sql_mileage = '''
            SELECT
            n.train_no,
            m.mileage_time,          
            ifnull(max(m.current_mileage),0) AS maxMileage,
            ifnull(min(m.current_mileage),0) AS minMileage
        FROM
            cd_train_no n
            INNER JOIN cd_train_real_time tr ON n.id = tr.train_no_id
            INNER JOIN cd_mileage m ON tr.id = m.train_real_time_id 
            AND m.del_flag = '0' 
        WHERE
            1 = 1
            {}
            AND m.mileage_time >= '{}' 
             AND m.mileage_time < '{}'                           
            AND m.current_mileage IS NOT NULL 
        GROUP BY
            n.train_no
        '''.format(sql_car, start, end)
        start_mileage = self.darams(sql_mileage)
        for i in start_mileage:
            a += i[-2] - i[-1]

        return a

    # 根据里程查实际行驶里程
    def mtbf_km2(self, start, end, car, start1, end1):
        a = 0
        if len(car) == 1:
            sql_car = 'and n.id = \'{}\''.format(car[0])
        else:
            sql_car = 'and n.id in {}'.format(car)
        sql_mileage = '''
                  SELECT
                        n.train_no,
                        ifnull(max(m.current_mileage),0) AS maxMileage
                  FROM
                        cd_train_no n
                        INNER JOIN cd_train_real_time tr ON n.id = tr.train_no_id
                        INNER JOIN cd_mileage m ON tr.id = m.train_real_time_id 
                        AND m.del_flag = '0' 
                  WHERE
                      1 = 1
                      {}
                      AND m.current_mileage >= {}
                      AND m.current_mileage < {}                    
                      AND m.current_mileage IS NOT NULL 
                  group by 
                      n.train_no
              '''.format(sql_car, start, end)
        start_mileage = self.darams(sql_mileage)
        for i in start_mileage:
            if i[1] >= end1:
                a += end1
            else:
                if i[1] >= start1:
                    a += i[1] - start1
                else:
                    a += 0
        return a
    # 通过父模型找子模型
    def select_child(self,modelName):
        sql = '''
            select id from conf_model where model_name = '{}' and model_type = 'MORE_MODEL'
        
        '''.format(modelName)
        # 父模型的id
        upper_id = self.darams(sql)
        # 通过父模型的id 找子模型
        sql_childmodel = '''
                select model_name from conf_model where upper_model_id = '{}'
        '''.format(upper_id[0][0])
        child_name = self.darams(sql_childmodel)
        L = []
        for i in child_name:
            L.append(i[0])
        return [L,upper_id[0][0]]

    # 计算百万公里故障率
    def select_value(self,modelName):
        d = {}
        # 获取所有的子模型
        child = self.select_child(modelName)
        for modelname in child[0]:
            L1 = []
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
                    m.model_type = 'MORE_MODEL'
                    and m.model_name = '{}'
                    and m .upper_model_id= '{}'
                '''.format(modelname,child[1])
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
                tuple_pattern = tuple(input_value[0][8].split(','))
                if len(tuple_pattern) == 1:
                    sql_pattern = 'and r.real_fault_pattern_id = {}'.format(input_value[0][5])
                else:
                    tuple_pattern = tuple(input_value[0][8].split(','))
                    sql_pattern = 'and r.real_fault_pattern_id in {}'.format(tuple_pattern)
            else:
                sql_pattern = 'AND 1 = 1'
            # 初到晚点
            late_from = input_value[0][-3]
            # 终到晚点
            late_end = input_value[0][-2]
            # 晚点类型
            late_type = input_value[0][-1]
            # 基本故障
            L_basic = []

            # 关联故障
            L_relevance = []

            # 非关联故障
            L_not_relevance = []

            # 安监故障
            L_safety_supervision = []

            # 服务故障
            L_service = []
            L = []

            if input_value[0][0] is not None:

                mon_start = input_value[0][0]
                end = input_value[0][1]
                L.append(mon_start)
                while True:
                    if mon_start < end:
                        if mon_start.month < 12:
                            L.append(datetime.datetime(mon_start.year, mon_start.month + 1, 1))
                            mon_start = datetime.datetime(mon_start.year, mon_start.month + 1, 1)
                        else:
                            mo = mon_start.year + 1
                            L.append(datetime.datetime(mo, 1, 1))
                            mon_start = datetime.datetime(mo, 1, 1)

                    else:
                        L[-1] = end + datetime.timedelta(days=1)
                        break
                for i in range(0, len(L) - 1):
                    sql_start = 'AND d.occurrence_time >= \'{}\''.format(L[i].strftime("%Y-%m-%d"))
                    sql_end = 'AND d.occurrence_time < \'{}\''.format(L[i + 1].strftime("%Y-%m-%d"))
                    # 得到分好组的故障单
                    a = self.faultNum(sql_start, sql_end, tuple_trainno, sql_fault, sql_pattern, late_from, late_end,
                                      late_type)
                    # 累计里程
                    dist_basic_total_km = self.mtbf_km(L[i].strftime("%Y-%m-%d"), L[i + 1].strftime("%Y-%m-%d"),
                                                       tuple_trainno)
                    if '基本故障' in a.keys():
                        fcnt_total = a['基本故障']

                        # 百万公里故障率
                        if dist_basic_total_km == 0:
                            L_basic.append(0)
                        else:
                            fr_fpmk = (len(fcnt_total) / dist_basic_total_km) * 1000000
                            L_basic.append(fr_fpmk)

                    else:
                        L_basic.append(0)

                    if '关联故障' in a.keys():
                        fcnt_total = a['关联故障']

                        # 百万公里故障率
                        if dist_basic_total_km == 0:
                            L_relevance.append(0)
                        else:
                            fr_fpmk = (len(fcnt_total) / dist_basic_total_km) * 1000000
                            L_relevance.append(fr_fpmk)

                    else:
                        L_relevance.append(0)


                    if '非关联故障' in a.keys():
                        fcnt_total = a['非关联故障']

                        # 百万公里故障率
                        if dist_basic_total_km == 0:
                            L_not_relevance.append(0)
                        else:
                            fr_fpmk = (len(fcnt_total) / dist_basic_total_km) * 1000000
                            L_not_relevance.append(fr_fpmk)


                    else:
                        L_not_relevance.append(0)


                    if '安监故障' in a.keys():
                        fcnt_total = a['安监故障']

                        # 百万公里故障率
                        if dist_basic_total_km == 0:
                            L_safety_supervision.append(0)
                        else:
                            fr_fpmk = (len(fcnt_total) / dist_basic_total_km) * 1000000
                            L_safety_supervision.append(fr_fpmk)

                    else:
                        L_safety_supervision.append(0)


                    if '服务故障' in a.keys():
                        fcnt_total = a['服务故障']

                        # 百万公里故障率
                        if dist_basic_total_km == 0:
                            L_service.append(0)
                        else:
                            fr_fpmk = (len(fcnt_total) / dist_basic_total_km) * 1000000
                            L_service.append(fr_fpmk)

                    else:
                        L_service.append(0)
                L1.append(L_basic)
                L1.append(L_relevance)
                L1.append(L_not_relevance)
                L1.append(L_safety_supervision)
                L1.append(L_service)
            else:

                mileage_start = input_value[0][3]
                mileage_end = input_value[0][4]

                L.append(mileage_start)
                a = int(mileage_start // 100000)
                b = int(mileage_end // 100000)
                for i in range(a + 1, b + 1):
                    L.append(i * 100000)
                if L[-1] == int(mileage_end):
                    pass
                else:
                    L.append(mileage_end)
                for i in range(0, len(L) - 1):
                    sql_start = 'AND t.accumulated_mileage >= {}'.format(L[i])
                    sql_end = 'AND t.accumulated_mileage < {}'.format(L[i + 1])
                    # 得到分好组的故障单
                    a = self.faultNum(sql_start, sql_end, tuple_trainno, sql_fault, sql_pattern, late_from, late_end,
                                      late_type)
                    # 累计里程
                    dist_basic_total_km = self.mtbf_km2(L[0], L[-1], tuple_trainno, L[i], L[i + 1])
                    if '基本故障' in a.keys():
                        fcnt_total = a['基本故障']

                        # 百万公里故障率
                        if dist_basic_total_km == 0:
                            L_basic.append(0)
                        else:
                            fr_fpmk = (len(fcnt_total) / dist_basic_total_km) * 1000000
                            L_basic.append(fr_fpmk)

                    else:
                        L_basic.append(0)


                    if '关联故障' in a.keys():
                        fcnt_total = a['关联故障']

                        # 百万公里故障率
                        if dist_basic_total_km == 0:
                            L_relevance.append(0)
                        else:
                            fr_fpmk = (len(fcnt_total) / dist_basic_total_km) * 1000000
                            L_relevance.append(fr_fpmk)

                    else:
                        L_relevance.append(0)


                    if '非关联故障' in a.keys():
                        fcnt_total = a['非关联故障']

                        # 百万公里故障率
                        if dist_basic_total_km == 0:
                            L_not_relevance.append(0)
                        else:
                            fr_fpmk = (len(fcnt_total) / dist_basic_total_km) * 1000000
                            L_not_relevance.append(fr_fpmk)

                    else:
                        L_not_relevance.append(0)


                    if '安监故障' in a.keys():
                        fcnt_total = a['安监故障']

                        # 百万公里故障率
                        if dist_basic_total_km == 0:
                            L_safety_supervision.append(0)
                        else:
                            fr_fpmk = (len(fcnt_total) / dist_basic_total_km) * 1000000
                            L_safety_supervision.append(fr_fpmk)

                    else:
                        L_safety_supervision.append(0)


                    if '服务故障' in a.keys():
                        fcnt_total = a['服务故障']

                        # 百万公里故障率
                        if dist_basic_total_km == 0:
                            L_service.append(0)
                        else:
                            fr_fpmk = (len(fcnt_total) / dist_basic_total_km) * 1000000
                            L_service.append(fr_fpmk)

                    else:
                        L_service.append(0)
                L1.append(L_basic)
                L1.append(L_relevance)
                L1.append(L_not_relevance)
                L1.append(L_safety_supervision)
                L1.append(L_service)


            d[modelname] = L1
        print(d)

Moremodel().select_value('1.16测试1')