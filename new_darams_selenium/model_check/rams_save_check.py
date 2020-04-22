import pymysql
import datetime

class rams:
    def darams(self,sql):
        conn = pymysql.connect( '192.168.221.21', 'root', '123456', charset='utf8')
        cursor = conn.cursor()
        cursor.execute('use darams')
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    # 取故障单数量
    def faultNum(self,start,end,car,fault,latefrom,lateto,latetype):
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
                          t.service_fault_class as serviceFaultClass,
                          ifnull( t.start_late, 0) as startLate,
                          ifnull( t.end_late, 0) as endLate,                      
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
                          INNER JOIN op_fault_associated_subject s ON d.id = s.fault_detail_id
                          INNER JOIN cd_supplier cs ON cs.supplier_name = s.main_responsibility          
                          INNER JOIN op_fault_handle e ON r.id = e.real_fault_id
                          where                    
                              h.status != '已取消'
                              {}
                              {}                    
                              {}         
                              {}       
                          '''.format(start,end,sql_car,fault)

        va = self.darams(sql_faultNum)
        d = {}

        total_time = 0
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
                if j[6] == '掉线' or j[6] == '未出库':
                    if '服务故障' in d.keys():
                        d['服务故障'].append(j[2])
                    else:
                        d['服务故障'] = []
                        d['服务故障'].append(j[2])
                elif j[6] == '晚点':
                    if latetype is not None:
                        if latetype == 'start':
                            if latefrom is not None:
                                if j[7] >= latefrom:
                                    if '服务故障' in d.keys():
                                        d['服务故障'].append(j[2])
                                    else:
                                        d['服务故障'] = []
                                        d['服务故障'].append(j[2])
                        elif latetype == 'end':
                            if lateto is not None:
                                if j[8] <= lateto:
                                    if '服务故障' in d.keys():
                                        d['服务故障'].append(j[2])
                                    else:
                                        d['服务故障'] = []
                                        d['服务故障'].append(j[2])
                        elif latetype == 'either':
                            if lateto is not None and latefrom is None:
                                if j[8] <= lateto:
                                    if '服务故障' in d.keys():
                                        d['服务故障'].append(j[2])
                                    else:
                                        d['服务故障'] = []
                                        d['服务故障'].append(j[2])
                            elif latefrom is not None and lateto is None:
                                if j[7] >= latefrom:
                                    if '服务故障' in d.keys():
                                        d['服务故障'].append(j[2])
                                    else:
                                        d['服务故障'] = []
                                        d['服务故障'].append(j[2])
                            elif latefrom is not None and lateto is not None:
                                if j[7] >= latefrom or j[8] <= lateto:
                                    if '服务故障' in d.keys():
                                        d['服务故障'].append(j[2])
                                    else:
                                        d['服务故障'] = []
                                        d['服务故障'].append(j[2])
                        elif latetype == 'both':
                            if lateto is not None and latefrom is not None:
                                if j[7] >= latefrom and j[8] <= lateto:
                                    if '服务故障' in d.keys():
                                        d['服务故障'].append(j[2])
                                    else:
                                        d['服务故障'] = []
                                        d['服务故障'].append(j[2])



            total_time += j[3] + j[4] + j[5]



        # print(d)
        # print(d1)
        return [d,total_time]

    # 根据时间查实际行驶里程:
    def mtbf_km(self,start,end,car):
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
        '''.format(sql_car,start,end)
        start_mileage = self.darams(sql_mileage)
        for i in start_mileage:
            a += i[-2] - i[-1]

        return a

    # 根据里程查实际行驶里程
    def mtbf_km2(self,start,end,car,start1,end1):
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

    # 连接数据库提取数据
    def select_value(self,modelName):
        sql_no_obj = \
            '''
            SELECT
                d.start_date,
                d.end_date,
                d.average_speed_select,
                d.interval_date,
                mi.start_mileage,
                mi.end_mileage,
                mi.average_speed,
                mt.train_no_id,
                o.fault_object_id,
				p.fault_pattern_id,
                sf.fault_define,
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
                m.model_type = 'USER_MODEL'
                and m.model_name = '{}'
            '''.format(modelName)

        input_value = self.darams(sql_no_obj)

        tuple_trainno = tuple(input_value[0][7].split(','))
        # print(tuple_trainno)
        if input_value[0][8] is not None:
            tuple_objids = tuple(input_value[0][8].split(','))
            if len(tuple_objids) == 1:
                sql_fault = 'and r.real_fault_object_id = {}'.format(input_value[0][8])
            else:
                tuple_objids = tuple(input_value[0][8].split(','))
                sql_fault = 'and r.real_fault_object_id in {}'.format(tuple_objids)
        elif input_value[0][9] is not None:
            tuple_pattern = tuple(input_value[0][9].split(','))
            if len(tuple_pattern) == 1:
                sql_fault = 'and r.real_fault_pattern_id = {}'.format(input_value[0][9])
            else:
                tuple_pattern = tuple(input_value[0][9].split(','))
                sql_fault = 'and r.real_fault_pattern_id in {}'.format(tuple_pattern)

        # 初到晚点
        late_from = input_value[0][-3]
        # 终到晚点
        late_end = input_value[0][-2]
        # 晚点类型
        late_type = input_value[0][-1]


        # service_fault = tuple(input_value[0][6].split(','))
        # if input_value[0][0] is not None:
        #     start = input_value[0][0]
        #     end = input_value[0][1]
        #     average = input_value[0][2]
        # else:
        #     start = input_value[0][4]
        #     end = input_value[0][5]
        #     average = input_value[0][6]


        L = []
        if input_value[0][0] is not None:
            # 平均时速
            speed = input_value[0][2]
            mon_start = input_value[0][0]
            L.append(mon_start)
            while True:
                if mon_start < input_value[0][1]:
                    if mon_start.month < 12:
                        L.append(datetime.datetime(mon_start.year, mon_start.month + 1, 1))
                        mon_start = datetime.datetime(mon_start.year, mon_start.month + 1, 1)
                    else:
                        mo = mon_start.year + 1
                        L.append(datetime.datetime(mo, 1, 1))
                        mon_start = datetime.datetime(mo, 1, 1)

                else:
                    L[-1] = input_value[0][1] + datetime.timedelta(days=1)
                    break
            # 基本故障
            L_basic = []
            L1_basic = []
            L2_basic = []
            L3_basic = []
            for i in range(0,len(L)-1):
                sql_start = 'AND d.occurrence_time >= \'{}\''.format(L[i].strftime("%Y-%m-%d"))
                sql_end = 'AND d.occurrence_time < \'{}\''.format(L[i+1].strftime("%Y-%m-%d"))
                # 得到分好组的故障单
                a = self.faultNum(sql_start,sql_end,tuple_trainno,sql_fault,late_from,late_end,late_type)
                fcnt_total = a[0]['基本故障']
                # 累计里程
                dist_basic_total_km = self.mtbf_km(L[i].strftime("%Y-%m-%d"), L[i + 1].strftime("%Y-%m-%d"),
                                                   tuple_trainno)
                # 百万公里故障率
                if dist_basic_total_km == 0:
                    L_basic.append(0)
                else:
                    fr_fpmk = (len(fcnt_total)/dist_basic_total_km)*1000000
                    L_basic.append(fr_fpmk)
                # 平均故障间隔里程
                if len(fcnt_total) == 0:
                    mtbf_km = 0
                    mttr_min = 0
                    L1_basic.append(0)
                    L2_basic.append(0)
                else:
                    mtbf_km = dist_basic_total_km / len(fcnt_total)
                    L1_basic.append(mtbf_km)
                    # 平均修复时间
                    total_time = a[1]
                    mttr_min = (total_time / len(fcnt_total)) * 60
                    L2_basic.append(mttr_min)
                # 固有可用度
                if float(speed) == 0:
                    ai = 0
                    L3_basic.append(ai)
                else:
                    mdbf_hr = mtbf_km / float(speed)
                    ai = mdbf_hr / (mdbf_hr + mttr_min / 60)
                    L3_basic.append(ai)

            # 关联故障
            L_relevance = []
            L1_relevance = []
            L2_relevance = []
            L3_relevance = []
            for i in range(0, len(L) - 1):
                sql_start = 'AND d.occurrence_time >= \'{}\''.format(L[i].strftime("%Y-%m-%d"))
                sql_end = 'AND d.occurrence_time < \'{}\''.format(L[i + 1].strftime("%Y-%m-%d"))
                # 得到分好组的故障单
                a = self.faultNum(sql_start, sql_end, tuple_trainno, sql_fault, late_from, late_end, late_type)
                fcnt_total = a[0]['关联故障']
                # 累计里程
                dist_basic_total_km = self.mtbf_km(L[i].strftime("%Y-%m-%d"), L[i + 1].strftime("%Y-%m-%d"),
                                                   tuple_trainno)

                # 百万公里故障率
                if dist_basic_total_km == 0:
                    L_relevance.append(0)
                else:
                    fr_fpmk = (len(fcnt_total) / dist_basic_total_km) * 1000000
                    L_relevance.append(fr_fpmk)
                # 平均故障间隔里程
                if len(fcnt_total) == 0:
                    mtbf_km = 0
                    mttr_min = 0
                    L1_relevance.append(0)
                    L2_relevance.append(0)
                else:
                    mtbf_km = dist_basic_total_km / len(fcnt_total)
                    L1_relevance.append(mtbf_km)
                    # 平均修复时间
                    total_time = a[1]
                    mttr_min = (total_time / len(fcnt_total)) * 60
                    L2_relevance.append(mttr_min)
                # 固有可用度
                if float(speed) == 0:
                    ai = 0
                    L3_relevance.append(ai)
                else:
                    mdbf_hr = mtbf_km / float(speed)
                    ai = mdbf_hr / (mdbf_hr + mttr_min / 60)
                    L3_relevance.append(ai)

            # 非关联故障
            L_not_relevance = []
            L1_not_relevance = []
            L2_not_relevance = []
            L3_not_relevance = []
            for i in range(0, len(L) - 1):
                sql_start = 'AND d.occurrence_time >= \'{}\''.format(L[i].strftime("%Y-%m-%d"))
                sql_end = 'AND d.occurrence_time < \'{}\''.format(L[i + 1].strftime("%Y-%m-%d"))
                # 得到分好组的故障单
                a = self.faultNum(sql_start, sql_end, tuple_trainno, sql_fault, late_from, late_end, late_type)
                fcnt_total = a[0]['非关联故障']
                # 累计里程
                dist_basic_total_km = self.mtbf_km(L[i].strftime("%Y-%m-%d"), L[i + 1].strftime("%Y-%m-%d"),
                                                   tuple_trainno)

                # 百万公里故障率
                if dist_basic_total_km == 0:
                    L_not_relevance.append(0)
                else:
                    fr_fpmk = (len(fcnt_total) / dist_basic_total_km) * 1000000
                    L_not_relevance.append(fr_fpmk)
                # 平均故障间隔里程
                if len(fcnt_total) == 0:
                    mtbf_km = 0
                    mttr_min = 0
                    L1_not_relevance.append(0)
                    L2_not_relevance.append(0)
                else:
                    mtbf_km = dist_basic_total_km / len(fcnt_total)
                    L1_not_relevance.append(mtbf_km)
                    # 平均修复时间
                    total_time = a[1]
                    mttr_min = (total_time / len(fcnt_total)) * 60
                    L2_not_relevance.append(mttr_min)
                # 固有可用度
                if float(speed) == 0:
                    ai = 0
                    L3_not_relevance.append(ai)
                else:
                    mdbf_hr = mtbf_km / float(speed)
                    ai = mdbf_hr / (mdbf_hr + mttr_min / 60)
                    L3_not_relevance.append(ai)

            # 安监故障
            L_safety_supervision = []
            L1_safety_supervision = []
            L2_safety_supervision = []
            L3_safety_supervision = []
            for i in range(0, len(L) - 1):
                sql_start = 'AND d.occurrence_time >= \'{}\''.format(L[i].strftime("%Y-%m-%d"))
                sql_end = 'AND d.occurrence_time < \'{}\''.format(L[i + 1].strftime("%Y-%m-%d"))
                # 得到分好组的故障单
                a = self.faultNum(sql_start, sql_end, tuple_trainno, sql_fault, late_from, late_end, late_type)
                if '安监故障' in a[0].keys():
                    fcnt_total = a[0]['安监故障']
                    # 累计里程
                    dist_basic_total_km = self.mtbf_km(L[i].strftime("%Y-%m-%d"), L[i + 1].strftime("%Y-%m-%d"),
                                                       tuple_trainno)

                    # 百万公里故障率
                    if dist_basic_total_km == 0:
                        L_safety_supervision.append(0)
                    else:
                        fr_fpmk = (len(fcnt_total) / dist_basic_total_km) * 1000000
                        L_safety_supervision.append(fr_fpmk)
                    # 平均故障间隔里程
                    if len(fcnt_total) == 0:
                        mtbf_km = 0
                        mttr_min = 0
                        L1_safety_supervision.append(0)
                        L2_safety_supervision.append(0)
                    else:
                        mtbf_km = dist_basic_total_km / len(fcnt_total)
                        L1_safety_supervision.append(mtbf_km)
                        # 平均修复时间
                        total_time = a[1]
                        mttr_min = (total_time / len(fcnt_total)) * 60
                        L2_safety_supervision.append(mttr_min)
                    # 固有可用度
                    if float(speed) == 0:
                        ai = 0
                        L3_safety_supervision.append(ai)
                    else:
                        mdbf_hr = mtbf_km / float(speed)
                        ai = mdbf_hr / (mdbf_hr + mttr_min / 60)
                        L3_safety_supervision.append(ai)
                else:
                    L_safety_supervision.append(0)
                    L1_safety_supervision.append(0)
                    L2_safety_supervision.append(0)
                    L3_safety_supervision.append(0)

            # 服务故障
            L_service = []
            L1_service = []
            L2_service = []
            L3_service = []
            for i in range(0, len(L) - 1):
                sql_start = 'AND d.occurrence_time >= \'{}\''.format(L[i].strftime("%Y-%m-%d"))
                sql_end = 'AND d.occurrence_time < \'{}\''.format(L[i + 1].strftime("%Y-%m-%d"))
                # 得到分好组的故障单
                a = self.faultNum(sql_start, sql_end, tuple_trainno, sql_fault, late_from, late_end, late_type)
                if '服务故障' in a[0].keys():
                    fcnt_total = a[0]['服务故障']
                    # 累计里程
                    dist_basic_total_km = self.mtbf_km(L[i].strftime("%Y-%m-%d"), L[i + 1].strftime("%Y-%m-%d"),
                                                       tuple_trainno)

                    # 百万公里故障率
                    if dist_basic_total_km == 0:
                        L_safety_supervision.append(0)
                    else:
                        fr_fpmk = (len(fcnt_total) / dist_basic_total_km) * 1000000
                        L_service.append(fr_fpmk)
                    # 平均故障间隔里程
                    if len(fcnt_total) == 0:
                        mtbf_km = 0
                        mttr_min = 0
                        L1_service.append(0)
                        L2_service.append(0)
                    else:
                        mtbf_km = dist_basic_total_km / len(fcnt_total)
                        L1_service.append(mtbf_km)
                        # 平均修复时间
                        total_time = a[1]
                        mttr_min = (total_time / len(fcnt_total)) * 60
                        L2_service.append(mttr_min)
                    # 固有可用度
                    if float(speed) == 0:
                        ai = 0
                        L3_service.append(ai)
                    else:
                        mdbf_hr = mtbf_km / float(speed)
                        ai = mdbf_hr / (mdbf_hr + mttr_min / 60)
                        L3_service.append(ai)
                else:
                    L_service.append(0)
                    L1_service.append(0)
                    L2_service.append(0)
                    L3_service.append(0)



            # sql_start = 'AND  t.accumulated_mileage >= {}'.format(start)
            # sql_end = 'AND  t.accumulated_mileage <= {}'.format(end)

        else:
            # 平均时速
            speed = input_value[0][6]
            mon_start = input_value[0][4]
            L.append(mon_start)
            a = int(mon_start // 100000)
            b = int(input_value[0][5] // 100000)
            for i in range(a+ 1, b + 1):
                L.append(i * 100000)
            if L[-1] == int(input_value[0][5]):
                pass
            else:
                L.append(input_value[0][5])
            # 基本故障
            L_basic = []
            L1_basic = []
            L2_basic = []
            L3_basic = []
            for i in range(0, len(L) - 1):
                sql_start = 'AND t.accumulated_mileage >= {}'.format(L[i])
                sql_end = 'AND t.accumulated_mileage < {}'.format(L[i + 1])
                # 得到分好组的故障单
                a = self.faultNum(sql_start, sql_end, tuple_trainno, sql_fault, late_from, late_end, late_type)
                if '基本故障'in a[0].keys():
                    fcnt_total = a[0]['基本故障']
                    # 累计里程

                    dist_basic_total_km = self.mtbf_km2(L[0], L[-1], tuple_trainno, L[i], L[i + 1])
                    # 百万公里故障率
                    if dist_basic_total_km == 0:
                        L_basic.append(0)
                    else:
                        fr_fpmk = (len(fcnt_total) / dist_basic_total_km) * 1000000
                        L_basic.append(fr_fpmk)
                    # 平均故障间隔里程
                    if len(fcnt_total) == 0:
                        mtbf_km = 0
                        mttr_min = 0
                        L1_basic.append(0)
                        L2_basic.append(0)
                    else:
                        mtbf_km = dist_basic_total_km / len(fcnt_total)
                        L1_basic.append(mtbf_km)
                        # 平均修复时间
                        total_time = a[1]
                        mttr_min = (total_time / len(fcnt_total)) * 60
                        L2_basic.append(mttr_min)
                    # 固有可用度
                    if float(speed) == 0 or speed is None:
                        ai = 0
                        L3_basic.append(ai)
                    else:
                        mdbf_hr = mtbf_km / float(speed)
                        ai = mdbf_hr / (mdbf_hr + mttr_min / 60)
                        L3_basic.append(ai)
                else:
                    L_basic.append(0)
                    L1_basic.append(0)
                    L2_basic.append(0)
                    L3_basic.append(0)
            # 关联故障
            L_relevance = []
            L1_relevance = []
            L2_relevance = []
            L3_relevance = []
            for i in range(0, len(L) - 1):
                sql_start = 'AND t.accumulated_mileage >= {}'.format(L[i])
                sql_end = 'AND t.accumulated_mileage < {}'.format(L[i + 1])
                # 得到分好组的故障单
                a = self.faultNum(sql_start, sql_end, tuple_trainno, sql_fault, late_from, late_end, late_type)
                if '关联故障'in a[0].keys():

                    fcnt_total = a[0]['关联故障']
                    # 累计里程
                    dist_basic_total_km = self.mtbf_km2(L[0], L[-1], tuple_trainno, L[i], L[i + 1])

                    # 百万公里故障率
                    if dist_basic_total_km == 0:
                        L_relevance.append(0)
                    else:
                        fr_fpmk = (len(fcnt_total) / dist_basic_total_km) * 1000000
                        L_relevance.append(fr_fpmk)
                    # 平均故障间隔里程
                    if len(fcnt_total) == 0:
                        mtbf_km = 0
                        mttr_min = 0
                        L1_relevance.append(0)
                        L2_relevance.append(0)
                    else:
                        mtbf_km = dist_basic_total_km / len(fcnt_total)
                        L1_relevance.append(mtbf_km)
                        # 平均修复时间
                        total_time = a[1]
                        mttr_min = (total_time / len(fcnt_total)) * 60
                        L2_relevance.append(mttr_min)
                    # 固有可用度
                    if float(speed) == 0 or speed is None:
                        ai = 0
                        L3_relevance.append(ai)
                    else:
                        mdbf_hr = mtbf_km / float(speed)
                        ai = mdbf_hr / (mdbf_hr + mttr_min / 60)
                        L3_relevance.append(ai)
                else:
                    L_relevance.append(0)
                    L1_relevance.append(0)
                    L2_relevance.append(0)
                    L3_relevance.append(0)
            # 非关联故障
            L_not_relevance = []
            L1_not_relevance = []
            L2_not_relevance = []
            L3_not_relevance = []
            for i in range(0, len(L) - 1):
                sql_start = 'AND t.accumulated_mileage >= {}'.format(L[i])
                sql_end = 'AND t.accumulated_mileage < {}'.format(L[i + 1])
                # 得到分好组的故障单
                a = self.faultNum(sql_start, sql_end, tuple_trainno, sql_fault, late_from, late_end, late_type)
                if '非关联故障' in a[0].keys():
                    fcnt_total = a[0]['非关联故障']
                    # 累计里程
                    dist_basic_total_km = self.mtbf_km2(L[0], L[-1], tuple_trainno, L[i], L[i + 1])

                    # 百万公里故障率
                    if dist_basic_total_km == 0:
                        L_not_relevance.append(0)
                    else:
                        fr_fpmk = (len(fcnt_total) / dist_basic_total_km) * 1000000
                        L_not_relevance.append(fr_fpmk)
                    # 平均故障间隔里程
                    if len(fcnt_total) == 0:
                        mtbf_km = 0
                        mttr_min = 0
                        L1_not_relevance.append(0)
                        L2_not_relevance.append(0)
                    else:
                        mtbf_km = dist_basic_total_km / len(fcnt_total)
                        L1_not_relevance.append(mtbf_km)
                        # 平均修复时间
                        total_time = a[1]
                        mttr_min = (total_time / len(fcnt_total)) * 60
                        L2_not_relevance.append(mttr_min)
                    # 固有可用度
                    if float(speed) == 0:
                        ai = 0
                        L3_not_relevance.append(ai)
                    else:
                        mdbf_hr = mtbf_km / float(speed)
                        ai = mdbf_hr / (mdbf_hr + mttr_min / 60)
                        L3_not_relevance.append(ai)
                else:
                    L_not_relevance.append(0)
                    L1_not_relevance.append(0)
                    L2_not_relevance.append(0)
                    L3_not_relevance.append(0)
            # 安监故障
            L_safety_supervision = []
            L1_safety_supervision = []
            L2_safety_supervision = []
            L3_safety_supervision = []
            for i in range(0, len(L) - 1):
                sql_start = 'AND t.accumulated_mileage >= {}'.format(L[i])
                sql_end = 'AND t.accumulated_mileage < {}'.format(L[i + 1])
                # 得到分好组的故障单
                a = self.faultNum(sql_start, sql_end, tuple_trainno, sql_fault, late_from, late_end, late_type)
                if '安监故障' in a[0].keys():
                    fcnt_total = a[0]['安监故障']
                    # 累计里程
                    dist_basic_total_km = self.mtbf_km2(L[0], L[-1], tuple_trainno, L[i], L[i + 1])

                    # 百万公里故障率
                    if dist_basic_total_km == 0:
                        L_safety_supervision.append(0)
                    else:
                        fr_fpmk = (len(fcnt_total) / dist_basic_total_km) * 1000000
                        L_safety_supervision.append(fr_fpmk)
                    # 平均故障间隔里程
                    if len(fcnt_total) == 0:
                        mtbf_km = 0
                        mttr_min = 0
                        L1_safety_supervision.append(0)
                        L2_safety_supervision.append(0)
                    else:
                        mtbf_km = dist_basic_total_km / len(fcnt_total)
                        L1_safety_supervision.append(mtbf_km)
                        # 平均修复时间
                        total_time = a[1]
                        mttr_min = (total_time / len(fcnt_total)) * 60
                        L2_safety_supervision.append(mttr_min)
                    # 固有可用度
                    if float(speed) == 0:
                        ai = 0
                        L3_safety_supervision.append(ai)
                    else:
                        mdbf_hr = mtbf_km / float(speed)
                        ai = mdbf_hr / (mdbf_hr + mttr_min / 60)
                        L3_safety_supervision.append(ai)
                else:
                    L_safety_supervision.append(0)
                    L1_safety_supervision.append(0)
                    L2_safety_supervision.append(0)
                    L3_safety_supervision.append(0)
            # 服务故障
            L_service = []
            L1_service = []
            L2_service = []
            L3_service = []
            for i in range(0, len(L) - 1):
                sql_start = 'AND t.accumulated_mileage >= {}'.format(L[i])
                sql_end = 'AND t.accumulated_mileage < {}'.format(L[i + 1])
                # 得到分好组的故障单
                a = self.faultNum(sql_start, sql_end, tuple_trainno, sql_fault, late_from, late_end, late_type)
                if '服务故障' in a[0].keys():
                    fcnt_total = a[0]['服务故障']
                    # 累计里程
                    dist_basic_total_km = self.mtbf_km2(L[0], L[-1], tuple_trainno, L[i], L[i + 1])

                    # 百万公里故障率
                    if dist_basic_total_km == 0:
                        L_service.append(0)
                    else:
                        fr_fpmk = (len(fcnt_total) / dist_basic_total_km) * 1000000
                        L_service.append(fr_fpmk)
                    # 平均故障间隔里程
                    if len(fcnt_total) == 0:
                        mtbf_km = 0
                        mttr_min = 0
                        L1_service.append(0)
                        L2_service.append(0)
                    else:
                        mtbf_km = dist_basic_total_km / len(fcnt_total)
                        L1_service.append(mtbf_km)
                        # 平均修复时间
                        total_time = a[1]
                        mttr_min = (total_time / len(fcnt_total)) * 60
                        L2_service.append(mttr_min)
                    # 固有可用度
                    if float(speed) == 0:
                        ai = 0
                        L3_service.append(ai)
                    else:
                        mdbf_hr = mtbf_km / float(speed)
                        ai = mdbf_hr / (mdbf_hr + mttr_min / 60)
                        L3_service.append(ai)
                else:
                    L_service.append(0)
                    L1_service.append(0)
                    L2_service.append(0)
                    L3_service.append(0)
        print(L_basic)
        print(L1_basic)
        print(L2_basic)
        print(L3_basic)
        print(L_relevance)
        print(L1_relevance)
        print(L2_relevance)
        print(L3_relevance)
        print(L_not_relevance)
        print(L1_not_relevance)
        print(L2_not_relevance)
        print(L3_not_relevance)
        print(L_safety_supervision)
        print(L1_safety_supervision)
        print(L2_safety_supervision)
        print(L3_safety_supervision)
        print(L_service)
        print(L1_service)
        print(L2_service)
        print(L3_service)







rams().select_value('上海测试3')