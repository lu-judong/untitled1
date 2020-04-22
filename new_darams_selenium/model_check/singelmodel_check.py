import pymysql
import datetime

class singel:
    def darams(self,sql):
        conn = pymysql.connect( '192.168.221.21', 'root', '123456', charset='utf8')
        cursor = conn.cursor()
        cursor.execute('use darams')
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    # 取故障单数量
    def faultNum(self,start,end,car,fault,pattern,latefrom,lateto,latetype,count):

        if len(car) == 1:
            sql_car = 'and n.id = \'{}\''.format(car[0])
        else:
            sql_car = 'and n.id in {}'.format(car)

        sql_faultNum = '''
                      SELECT
                          h.fault_no as faultNo,
                          h.id as faultOrderId,
                          n.train_no as trainNo ,
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
                          '''.format(start,end,sql_car,fault,pattern)

        va = self.darams(sql_faultNum)
        d = {}

        total_time = 0
        if count == 1:
            if len(va) == 0:
                return [{},0]
            else:
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



                    total_time += j[3] + j[4] + j[5]

                # print(d)
                # print(d1)
                return [d,total_time]
        elif count == 2:
            for j in va:
                if j[2] in d.keys():
                    d[j[2]] += 1
                else:
                    d[j[2]] = 1
            return d
        elif count == 3:
            d1 = {}
            for j in va:
                if j[2] in d.keys():
                    if '基本故障' in d[j[2]].keys():
                        d[j[2]]['基本故障'] += 1
                    else:
                        d[j[2]]['基本故障'] = 1


                    if j[-4] in d[j[2]].keys():
                        d[j[2]][j[-4]] = +1
                    else:
                        d[j[2]][j[-4]] = 1

                    if j[-3] == '是' and j[-4] == '关联故障':
                        if '安监故障' in d[j[2]].keys():
                            d[j[2]]['安监故障'] += 1
                        else:
                            d[j[2]]['安监故障'] = 1
                    # 判断服务故障
                    if j[-4] == '关联故障':
                        if j[-7] == '掉线' or j[-7] == '未出库':
                            if '服务故障' in d[j[2]].keys():
                                d[j[2]]['服务故障'] += 1
                            else:
                                d[j[2]]['服务故障'] = 1
                        elif j[-7] == '晚点':
                            if latetype is not None:
                                if latetype == 'start':
                                    if latefrom is not None:
                                        if j[-6] >= latefrom:
                                            if '服务故障' in d[j[2]].keys():
                                                d[j[2]]['服务故障'] += 1
                                            else:
                                                d[j[2]]['服务故障'] = 1
                                elif latetype == 'end':
                                    if lateto is not None:
                                        if j[-5] <= lateto:
                                            if '服务故障' in d[j[2]].keys():
                                                d[j[2]]['服务故障'] += 1
                                            else:
                                                d[j[2]]['服务故障'] = 1
                                elif latetype == 'either':
                                    if lateto is not None and latefrom is None:
                                        if j[-5] <= lateto:
                                            if '服务故障' in d[j[2]].keys():
                                                d[j[2]]['服务故障'] += 1
                                            else:
                                                d[j[2]]['服务故障'] = 1
                                    elif latefrom is not None and lateto is None:
                                        if j[-6] >= latefrom:
                                            if '服务故障' in d[j[2]].keys():
                                                d[j[2]]['服务故障'] += 1
                                            else:
                                                d[j[2]]['服务故障'] = 1
                                    elif latefrom is not None and lateto is not None:
                                        if j[-6] >= latefrom or j[-5] <= lateto:
                                            if '服务故障' in d[j[2]].keys():
                                                d[j[2]]['服务故障'] += 1
                                            else:
                                                d[j[2]]['服务故障'] = 1
                                elif latetype == 'both':
                                    if lateto is not None and latefrom is not None:
                                        if j[-6] >= latefrom and j[-5] <= lateto:
                                            if '服务故障' in d[j[2]].keys():
                                                d[j[2]]['服务故障'] += 1
                                            else:
                                                d[j[2]]['服务故障'] = 1
                else:
                    d[j[2]] = {}
                    if '基本故障' in d[j[2]].keys():
                        d[j[2]]['基本故障'] += 1
                    else:
                        d[j[2]]['基本故障'] = 1

                    if j[-4] in d[j[2]].keys():
                        d[j[2]][j[-4]] = +1
                    else:
                        d[j[2]][j[-4]] = 1

                    if j[-3] == '是' and j[-4] == '关联故障':
                        if '安监故障' in d[j[2]].keys():
                            d[j[2]]['安监故障'] += 1
                        else:
                            d[j[2]]['安监故障'] = 1
                    # 判断服务故障
                    if j[-4] == '关联故障':
                        if j[-7] == '掉线' or j[-7] == '未出库':
                            if '服务故障' in d[j[2]].keys():
                                d[j[2]]['服务故障'] += 1
                            else:
                                d[j[2]]['服务故障'] = 1
                        elif j[-7] == '晚点':
                            if latetype is not None:
                                if latetype == 'start':
                                    if latefrom is not None:
                                        if j[-6] >= latefrom:
                                            if '服务故障' in d[j[2]].keys():
                                                d[j[2]]['服务故障'] += 1
                                            else:
                                                d[j[2]]['服务故障'] = 1
                                elif latetype == 'end':
                                    if lateto is not None:
                                        if j[-5] <= lateto:
                                            if '服务故障' in d[j[2]].keys():
                                                d[j[2]]['服务故障'] += 1
                                            else:
                                                d[j[2]]['服务故障'] = 1
                                elif latetype == 'either':
                                    if lateto is not None and latefrom is None:
                                        if j[-5] <= lateto:
                                            if '服务故障' in d[j[2]].keys():
                                                d[j[2]]['服务故障'] += 1
                                            else:
                                                d[j[2]]['服务故障'] = 1
                                    elif latefrom is not None and lateto is None:
                                        if j[-6] >= latefrom:
                                            if '服务故障' in d[j[2]].keys():
                                                d[j[2]]['服务故障'] += 1
                                            else:
                                                d[j[2]]['服务故障'] = 1
                                    elif latefrom is not None and lateto is not None:
                                        if j[-6] >= latefrom or j[-5] <= lateto:
                                            if '服务故障' in d[j[2]].keys():
                                                d[j[2]]['服务故障'] += 1
                                            else:
                                                d[j[2]]['服务故障'] = 1
                                elif latetype == 'both':
                                    if lateto is not None and latefrom is not None:
                                        if j[-6] >= latefrom and j[-5] <= lateto:
                                            if '服务故障' in d[j[2]].keys():
                                                d[j[2]]['服务故障'] += 1
                                            else:
                                                d[j[2]]['服务故障'] = 1

            for j in va:
                if j[2] in d1.keys():
                    d1[j[2]] += j[3] + j[4] + j[5]
                else:
                    d1[j[2]] = j[3] + j[4] + j[5]

            return [d,d1]

    # 根据时间查实际行驶里程:
    def mtbf_km(self, start, end, car, count):
        d = {}
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
        if count == 1:
            for i in start_mileage:
                a += i[-2] - i[-1]
            return a
        elif count == 2:
            for i in start_mileage:
                d[i[0]] = (i[-2] - i[-1]) / 10000
            return d
        elif count == 3:
            for i in start_mileage:
                d[i[0]] = i[-2] - i[-1]
            return d

    # 根据里程查实际行驶里程
    def mtbf_km2(self,start,end,car,start1,end1,count):
        a = 0
        d = {}
        if len(car) == 1:
            sql_car = 'and n.id = \'{}\''.format(car[0])
        else:
            sql_car = 'and n.id in {}'.format(car)
        sql_mileage = '''
                  SELECT
                        n.train_no,
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
                      AND m.current_mileage >= {}
                      AND m.current_mileage < {}                    
                      AND m.current_mileage IS NOT NULL 
                  group by 
                      n.train_no
              '''.format(sql_car, start, end)
        start_mileage = self.darams(sql_mileage)
        if count == 1:
            for i in start_mileage:
                if i[1] >= end1:
                    a += end1
                else:
                    if i[1] >= start1:
                        a += i[1] - start1
                    else:
                        a += 0
            return a
        elif count == 2:
            for i in start_mileage:
                d[i[0]] = (i[1] - i[2]) / 10000
            return d
        elif count == 3:
            for i in start_mileage:
                if i[1] >= end1:
                    d[i[0]] = end1
                else:
                    if i[1] >= start1:
                        d[i[0]] = i[1] - start1
                    else:
                        d[i[0]] = 0
            return d


    # 连接数据库提取数据
    def select_value(self,modelName):
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
                d.business_flag,
                mi.business_flag ,
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
                m.model_type = 'SINGLE_MODEL'
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
        # 取第几次的数据
        L = []
        # 基本故障
        L_basic = []

        if input_value[0][0] is not None:

            mon_start = input_value[0][0]
            end = input_value[0][1]
            speed = input_value[0][2]

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
            for i in range(0,len(L)-1):
                sql_start = 'AND d.occurrence_time >= \'{}\''.format(L[i].strftime("%Y-%m-%d"))
                sql_end = 'AND d.occurrence_time < \'{}\''.format(L[i+1].strftime("%Y-%m-%d"))

                # 得到分好组的故障单
                a = self.faultNum(sql_start, sql_end, tuple_trainno, sql_fault, sql_pattern, late_from, late_end,
                                  late_type, 1)
                # 累计里程
                dist_basic_total_km = self.mtbf_km(L[0], L[-1], tuple_trainno, 3)
                L_1 = []
                d = {}
                if len(a[0]) == 0:
                    L_basic.append((0,0))
                else:
                    for j in a[0]:
                        fcnt_total = a[0][j]
                        # 百万公里故障率
                        for i in dist_basic_total_km:
                            if dist_basic_total_km[i] == 0:
                                L_1.append(0)
                            else:
                                if i in fcnt_total:
                                    fr_fpmk = (fcnt_total.count(i) / dist_basic_total_km[i]) * 1000000
                                    L_1.append(fr_fpmk)
                                else:
                                    L_1.append(0)
                        L_1.sort(reverse=True)
                        basic_max = L_1[0]
                        basic_min = L_1[-1]
                        d[j] = [basic_max, basic_min]
                    L_basic.append(d)


            sql_start = 'AND d.occurrence_time >= \'{}\''.format(L[0].strftime("%Y-%m-%d"))
            sql_end = 'AND d.occurrence_time < \'{}\''.format(L[-1].strftime("%Y-%m-%d"))
            car_faultNum = self.faultNum(sql_start, sql_end, tuple_trainno, sql_fault, sql_pattern, late_from, late_end,
                              late_type,2)
            car_mileage = self.mtbf_km(L[0].strftime("%Y-%m-%d"), L[-1].strftime("%Y-%m-%d"), tuple_trainno,2)
            d2 = {}
            for n in car_faultNum:
                d2[n] = []
            for i in range(0, len(L) - 1):
                sql_start = 'AND d.occurrence_time >= \'{}\''.format(L[i].strftime("%Y-%m-%d"))
                sql_end = 'AND d.occurrence_time < \'{}\''.format(L[i + 1].strftime("%Y-%m-%d"))

                # 得到分好组的故障单
                a = self.faultNum(sql_start, sql_end, tuple_trainno, sql_fault, sql_pattern, late_from, late_end,
                                  late_type, 3)
                # 累计里程
                dist_basic_total_km = self.mtbf_km(L[0], L[-1], tuple_trainno, 3)
                d = {}

                for j in d2:
                    if j not in a[0].keys():
                        d2[j].append(
                            [{'基本故障': [0, 0, 0, 0]},
                             {'关联故障': [0, 0, 0, 0]},
                             {'非关联故障': [0, 0, 0, 0]},
                             {'安监故障': [0, 0, 0, 0]},
                             {'服务故障': [0, 0, 0, 0]}]
                        )
                    else:
                        fcnt_total = a[0][j]
                        # 百万公里故障率
                        # for m in dist_basic_total_km:
                        #     if m not in d.keys():
                        #         d[m] = []

                        for k in fcnt_total:
                            d[k] = []
                            if j not in dist_basic_total_km.keys():
                                d[k].append(0)
                                d[k].append(0)
                                # 平均修复时间
                                total_time = a[1][j]
                                mttr_min = (total_time / fcnt_total[k]) * 60
                                d[k].append(mttr_min)
                                d[k].append(0)
                            else:
                                if dist_basic_total_km[j] == 0:
                                    d[k].append(0)
                                else:
                                    fr_fpmk = (fcnt_total[k] / dist_basic_total_km[j]) * 1000000
                                    d[k].append(fr_fpmk)

                                # 平均故障间隔里程
                                mtbf_km = dist_basic_total_km[j] / fcnt_total[k]
                                d[k].append(mtbf_km)
                                # 平均修复时间
                                total_time = a[1][j]
                                mttr_min = (total_time / fcnt_total[k]) * 60
                                d[k].append(mttr_min)
                                # 固有可用度
                                if float(speed) == 0 or speed is None:
                                    ai = 0
                                    d[k].append(ai)
                                else:
                                    mdbf_hr = mtbf_km / float(speed)
                                    ai = mdbf_hr / (mdbf_hr + mttr_min / 60)
                                    d[k].append(ai)

                            d2[j].append([d])

        else:
            mileage_start = input_value[0][3]
            mileage_end = input_value[0][4]
            speed = input_value[0][5]
            L.append(mileage_start)
            a = int(mileage_start // 100000)
            b = int(mileage_end // 100000)
            for i in range(a + 1, b + 1):
                L.append(i * 100000)
            if L[-1] == int(mileage_end):
                pass
            else:
                L.append(mileage_end)
            # 最大最小百万公里故障率
            for i in range(0, len(L) - 1):
                sql_start = 'AND t.accumulated_mileage >= {}'.format(L[i])
                sql_end = 'AND t.accumulated_mileage < {}'.format(L[i + 1])
                # 得到分好组的故障单
                a = self.faultNum(sql_start, sql_end, tuple_trainno, sql_fault, sql_pattern, late_from, late_end,
                                  late_type,1)
                # 累计里程
                dist_basic_total_km = self.mtbf_km2(L[0], L[-1], tuple_trainno, L[i], L[i + 1],3)
                L_1 = []
                d = {}
                for j in a[0]:
                    fcnt_total = a[0][j]
                    # 百万公里故障率
                    for i in dist_basic_total_km:
                        if dist_basic_total_km[i] == 0:
                            L_1.append(0)
                        else:
                            if i in fcnt_total:
                                fr_fpmk = (fcnt_total.count(i) / dist_basic_total_km[i]) * 1000000
                                L_1.append(fr_fpmk)
                            else:
                                L_1.append(0)
                    L_1.sort(reverse=True)
                    basic_max = L_1[0]
                    basic_min = L_1[-1]
                    d[j] = [basic_max,basic_min]

                    L_1 = []
                L_basic.append(d)

            sql_start = 'AND t.accumulated_mileage >= {}'.format(L[0])
            sql_end = 'AND t.accumulated_mileage < {}'.format(L[-1])
            # 每辆车的故障总数
            car_faultNum = self.faultNum(sql_start, sql_end, tuple_trainno, sql_fault, sql_pattern, late_from, late_end,late_type,2)
            # 每辆车的行驶里程
            car_mileage = self.mtbf_km2(L[0], L[-1], tuple_trainno, L[0], L[-1], 2)
            d2 = {}
            for n in car_faultNum:
                d2[n] = []

            for i in range(0, len(L) - 1):
                sql_start = 'AND t.accumulated_mileage >= {}'.format(L[i])
                sql_end = 'AND t.accumulated_mileage < {}'.format(L[i + 1])
                # 得到分好组的故障单
                a = self.faultNum(sql_start, sql_end, tuple_trainno, sql_fault, sql_pattern, late_from, late_end,late_type,3)
                # 累计里程
                dist_basic_total_km = self.mtbf_km2(L[0], L[-1], tuple_trainno, L[i], L[i + 1],3)
                d = {}

                for j in d2:
                    if j not in a[0].keys():
                        d2[j].append(
                            [{'基本故障':[0,0,0,0]},
                            {'关联故障': [0, 0, 0, 0]},
                            {'非关联故障': [0, 0, 0, 0]},
                            {'安监故障': [0, 0, 0, 0]},
                            {'服务故障': [0, 0, 0, 0]}]
                        )
                    else:
                        fcnt_total = a[0][j]
                        # 百万公里故障率
                        # for m in dist_basic_total_km:
                        #     if m not in d.keys():
                        #         d[m] = []

                        for k in fcnt_total:
                            d[k] = []
                            if j not in dist_basic_total_km.keys():
                                d[k].append(0)
                                d[k].append(0)
                                # 平均修复时间
                                total_time = a[1][j]
                                mttr_min = (total_time / fcnt_total[k]) * 60
                                d[k].append(mttr_min)
                                d[k].append(0)
                            else:
                                if dist_basic_total_km[j] == 0:
                                    d[k].append(0)
                                else:
                                    fr_fpmk = (fcnt_total[k] / dist_basic_total_km[j]) * 1000000
                                    d[k].append(fr_fpmk)

                                # 平均故障间隔里程
                                mtbf_km = dist_basic_total_km[j] / fcnt_total[k]
                                d[k].append(mtbf_km)
                                # 平均修复时间
                                total_time = a[1][j]
                                mttr_min = (total_time / fcnt_total[k]) * 60
                                d[k].append(mttr_min)
                                # 固有可用度
                                if float(speed) == 0 or speed is None:
                                    ai = 0
                                    d[k].append(ai)
                                else:
                                    mdbf_hr = mtbf_km / float(speed)
                                    ai = mdbf_hr / (mdbf_hr + mttr_min / 60)
                                    d[k].append(ai)

                            d2[j].append([d])




        print(L_basic)

        print(d2)




singel().select_value('19测试')