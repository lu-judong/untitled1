import pymysql


class fault:
    def darams(self,sql):
        conn = pymysql.connect( '192.168.221.21', 'root', '123456', charset='utf8')
        cursor = conn.cursor()
        cursor.execute('use darams')
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    # 取故障单数量
    def faultNum(self,start,end,car,fault):
        if len(car) == 1:
            sql_car = 'and n.id = \'{}\''.format(car[0])
        else:
            sql_car = 'and n.id in {}'.format(car)
        sql_faultNum = '''
                      SELECT
                          h.fault_no as faultNo,
                          r.real_fault_object_id as faultId,
                          h.id as faultOrderId,
                          n.id as trainId,
                          ifnull( e.debugging_time, 0 ) as debugTime,
                          ifnull( e.diagnostic_time, 0 ) as diagnosticTime,
                          ifnull( e.repair_time, 0 ) as repairTime,
                          t.service_fault_class as serviceFaultClass,
                          ifnull( t.end_late, 0) as endLate,
                          ifnull( t.start_late, 0) as startLate,
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

        for j in va:
            if '基本故障' in d.keys():
                d['基本故障'].append(j[1])
            else:
                d['基本故障'] = []
                d['基本故障'].append(j[1])
            if j[-4] is not None:
                if j[-4] in d.keys():
                    d[j[-4]].append(j[1])
                else:
                    d[j[-4]] = []
                    d[j[-4]].append(j[1])

            if j[-3] == '是' and j[-4] == '关联故障':
                if '安监故障' in d.keys():
                    d['安监故障'].append(j[1])
                else:
                    d['安监故障'] = []
                    d['安监故障'].append(j[1])

            if j[7] == '掉线' or j[7] == '晚点' or j[7] == '未出库' and j[-4] == '关联故障':
                if '服务故障' in d.keys():
                    d['服务故障'].append(j[1])
                else:
                    d['服务故障'] = []
                    d['服务故障'].append(j[1])

        d1 = {}
        for i in d:
            d1[i] = {}
            if len(d[i]) != 0:
                for k in d[i]:
                    d1[i][k] = d[i].count(k) / len(d[i])


        # print(d)
        # print(d1)
        return d1

    # 根据部件id找出所有的一级部件的值
    def tree_d(self, car,fault):
        if len(car) == 1:
            sql_car = 'and o.train_no_id = \'{}\''.format(car[0])
        else:
            sql_car = 'and o.train_no_id in {}'.format(car)
        if len(fault) == 1:
            sql_fault = 'o.fault_object_id = \'{}\''.format(fault[0])
        else:
            sql_fault = 'o.fault_object_id in {}'.format(fault)

        sql = '''
                select 
                    o.relationship_id,
                    o.fault_object_id 
                from cd_fault_object o 
                where  
                {}
                {}
                group by
                 o.fault_object_id
        '''.format(sql_fault,sql_car)
        # 查出relationship_id
        d = {}
        L = []
        a = self.darams(sql)
        for i in a:
            d[i[0]] = i[1]
            L.append(i[0])
        if len(L) == 1:
            sql_id = 't.id = \'{}\''.format(L[0])
        else:
            sql_id = 't.id in {}'.format(tuple(L))
        # 查询二级部件的名称
        sql1 = '''
                select 
                    t.parent_fault_nodes,
                    t.id
                 from cd_fault_object_tree t
                 where 
                    {}
        '''.format(sql_id)
        # 二级部件的id
        two_parts = self.darams(sql1)

        L1 = []

        for i in two_parts:
            if i[0] is not None:
                if ',' in i[0]:
                    for j in d:
                        if j == i[1]:
                            d[i[1]] = d.pop(j)
            else:
                d[i[1]] = d.pop(j)
        for k in d:
            L1.append(k)
        if len(L1) == 0:
            pass
        else:
            if len(L1) ==1:
                sql_nodes =  't.id = \'{}\''.format(L1[0])
            elif len(L1) > 1:
                sql_nodes = 't.id in {}'.format(tuple(L1))
            sql2 = '''
                    select 
                        t.fault_node,
                        t.id
                     from cd_fault_object_tree t
                     where 
                        {}
            '''.format(sql_nodes)
            # 算出所有的二级部件
            tree_parts = self.darams(sql2)

            # for i in tree_parts:
            #     if i[1] in d.keys():
            #         if i[0] in d2.keys():
            #             d2[i[0]].append(d[i[1]])
            #         else:
            #             d2[i[0]] = []
            #             d2[i[0]].append(d[i[1]])
            for i in tree_parts:
                d[i[0]] = d.pop(i[1])

            print(d)
            return d
            # print(d2)

    # 查询部件
    def select_parts(self,car,fault):
        if len(car) == 1:
            sql_car = 'and a.train_no_id = \'{}\''.format(car[0])
        else:
            sql_car = 'and a.train_no_id in {}'.format(car)
        if len(fault) == 1:
            sql_fault = 'and a.fault_object_id = \'{}\''.format(fault[0])
        else:
            sql_fault = 'and a.fault_object_id in {}'.format(fault)
        sql_parts = '''
                SELECT
                a.train_no_id AS "trainNoId",
                a.fault_object_id AS "faultObjectId",
                a.relationship_id AS "relationId",
                a.fault_object_code AS "faultObjectCode",
                a.fault_object_desc AS "faultObjectDesc",
                a.id AS "faultId",
                a.train_counts as "trainNoIdFaultObjectCount"
                FROM cd_fault_object a
                where
                    a.del_flag = '0'			 
                    {}
                    {}
        '''.format(sql_car,sql_fault)
        a = self.darams(sql_parts)

    # 查询其他四个值
    def select_other_four_value(self,car,start,end,fault,lateto,latefrom,latetype):
        if len(car) == 1:
            sql_car = 'and n.id = \'{}\''.format(car[0])
        else:
            sql_car = 'and n.id in {}'.format(car)

        sql_four_value = '''
                            SELECT
                                ifnull(d.fault_level,"空白") as "faultyLevel",
                                ifnull(d.cause_class,"空白") as "reasonClassification",
                                ifnull(s.responsibility_class,"空白") as "responsiblePartiesClassification",
                                t.railway as "railwayBureau",
                                r.real_fault_object_id as "faultyObjectId",
                                r.real_fault_pattern_id as "faultyPatternId",
                                n.id as "trainId",
                                h.id as "faultId",
                                ifnull(t.start_late, 0) as startLate,
                                ifnull(t.end_late, 0) as endLate, 
                                t.service_fault_class as serviceFaultClass,                       
                                d.fault_property as faultProperty,
                                r.safety_supervisio_fault as safetySupervisioFault
                                FROM
                                op_fault_order_header h
                                INNER JOIN op_fault_order_detail d ON d.fault_id = h.id
                                INNER JOIN op_train t ON d.id = t.fault_detail_id AND t.del_flag = 0
                                INNER JOIN cd_train_no n ON t.train_no = n.train_no
                                INNER JOIN op_fault_real r ON d.id = r.fault_detail_id
                                INNER JOIN op_fault_associated_subject s ON d.id = s.fault_detail_id	
		                    where
                                h.status != '已取消'
                                {}
                                {}
                                {}
                                {}
        '''.format(sql_car,start,end,fault)
        va = self.darams(sql_four_value)
        d = {}
        d1 = {}
        d2  = {}
        d3 = {}
        d4 = {}
        if len(va) == 0:
            pass
        else:
            for i in va:
                if '基本故障' in d.keys():
                    d['基本故障'].append(i[0])
                    d1['基本故障'].append(i[1])
                    d2['基本故障'].append(i[2])
                    d3['基本故障'].append(i[3])
                else:
                    d['基本故障'] = []
                    d1['基本故障'] = []
                    d2['基本故障'] = []
                    d3['基本故障'] = []
                    d['基本故障'].append(i[0])
                    d1['基本故障'].append(i[1])
                    d2['基本故障'].append(i[2])
                    d3['基本故障'].append(i[3])
                if i[-2] is not None:
                    if i[-2] in d.keys():
                        d[i[-2]].append(i[0])
                        d1[i[-2]].append(i[1])
                        d2[i[-2]].append(i[2])
                        d3[i[-2]].append(i[3])
                    else:
                        d[i[-2]] = []
                        d1[i[-2]] = []
                        d2[i[-2]] = []
                        d3[i[-2]] = []
                        d[i[-2]].append(i[0])
                        d1[i[-2]].append(i[1])
                        d2[i[-2]].append(i[2])
                        d3[i[-2]].append(i[3])
                if i[-1] == '是' and i[-2] == '关联故障':
                    if '安监故障' in d.keys():
                        d['安监故障'].append(i[0])
                        d1['安监故障'].append(i[1])
                        d2['安监故障'].append(i[2])
                        d3['安监故障'].append(i[3])
                    else:
                        d['安监故障'] = []
                        d1['安监故障'] = []
                        d2['安监故障'] = []
                        d3['安监故障'] = []
                        d['安监故障'].append(i[0])
                        d1['安监故障'].append(i[1])
                        d2['安监故障'].append(i[2])
                        d3['安监故障'].append(i[3])
                if i[-2] == '关联故障':
                    if i[-3] == '掉线' or i[-3] == '未出库':
                        if '服务故障' in d.keys():
                            d['服务故障'].append(i[0])
                            d1['服务故障'].append(i[1])
                            d2['服务故障'].append(i[2])
                            d3['服务故障'].append(i[3])
                        else:
                            d['服务故障'] = []
                            d1['服务故障'] = []
                            d2['服务故障'] = []
                            d3['服务故障'] = []
                            d['服务故障'].append(i[0])
                            d1['服务故障'].append(i[1])
                            d2['服务故障'].append(i[2])
                            d3['服务故障'].append(i[3])
                elif i[-3] == '晚点':
                    if latetype is not None:
                        if latetype == 'start':
                            if latefrom is not None:
                                if i[8] >= latefrom:
                                    if '服务故障' in d.keys():
                                        d['服务故障'].append(i[0])
                                        d1['服务故障'].append(i[1])
                                        d2['服务故障'].append(i[2])
                                        d3['服务故障'].append(i[3])
                                    else:
                                        d['服务故障'] = []
                                        d1['服务故障'] = []
                                        d2['服务故障'] = []
                                        d3['服务故障'] = []
                                        d['服务故障'].append(i[0])
                                        d1['服务故障'].append(i[1])
                                        d2['服务故障'].append(i[2])
                                        d3['服务故障'].append(i[3])
                        elif latetype == 'end':
                            if lateto is not None:
                                if i[9] <= lateto:
                                    if '服务故障' in d.keys():
                                        d['服务故障'].append(i[0])
                                        d1['服务故障'].append(i[1])
                                        d2['服务故障'].append(i[2])
                                        d3['服务故障'].append(i[3])
                                    else:
                                        d['服务故障'] = []
                                        d1['服务故障'] = []
                                        d2['服务故障'] = []
                                        d3['服务故障'] = []
                                        d['服务故障'].append(i[0])
                                        d1['服务故障'].append(i[1])
                                        d2['服务故障'].append(i[2])
                                        d3['服务故障'].append(i[3])
                        elif latetype == 'either':
                            if lateto is not None and latefrom is None:
                                if i[9] <= lateto:
                                    if '服务故障' in d.keys():
                                        d['服务故障'].append(i[0])
                                        d1['服务故障'].append(i[1])
                                        d2['服务故障'].append(i[2])
                                        d3['服务故障'].append(i[3])
                                    else:
                                        d['服务故障'] = []
                                        d1['服务故障'] = []
                                        d2['服务故障'] = []
                                        d3['服务故障'] = []
                                        d['服务故障'].append(i[0])
                                        d1['服务故障'].append(i[1])
                                        d2['服务故障'].append(i[2])
                                        d3['服务故障'].append(i[3])
                            elif latefrom is not None and lateto is None:
                                if i[8] >= latefrom:
                                    if '服务故障' in d.keys():
                                        d['服务故障'].append(i[0])
                                        d1['服务故障'].append(i[1])
                                        d2['服务故障'].append(i[2])
                                        d3['服务故障'].append(i[3])
                                    else:
                                        d['服务故障'] = []
                                        d1['服务故障'] = []
                                        d2['服务故障'] = []
                                        d3['服务故障'] = []
                                        d['服务故障'].append(i[0])
                                        d1['服务故障'].append(i[1])
                                        d2['服务故障'].append(i[2])
                                        d3['服务故障'].append(i[3])
                            elif latefrom is not None and lateto is not None:
                                if i[8] >= latefrom or i[9] <= lateto:
                                    if '服务故障' in d.keys():
                                        d['服务故障'].append(i[0])
                                        d1['服务故障'].append(i[1])
                                        d2['服务故障'].append(i[2])
                                        d3['服务故障'].append(i[3])
                                    else:
                                        d['服务故障'] = []
                                        d1['服务故障'] = []
                                        d2['服务故障'] = []
                                        d3['服务故障'] = []
                                        d['服务故障'].append(i[0])
                                        d1['服务故障'].append(i[1])
                                        d2['服务故障'].append(i[2])
                                        d3['服务故障'].append(i[3])
                        elif latetype == 'both':
                            if lateto is not None and latefrom is not None:
                                if i[8] >= latefrom and i[9] <= lateto:
                                    if '服务故障' in d.keys():
                                        d['服务故障'].append(i[0])
                                        d1['服务故障'].append(i[1])
                                        d2['服务故障'].append(i[2])
                                        d3['服务故障'].append(i[3])
                                    else:
                                        d['服务故障'] = []
                                        d1['服务故障'] = []
                                        d2['服务故障'] = []
                                        d3['服务故障'] = []
                                        d['服务故障'].append(i[0])
                                        d1['服务故障'].append(i[1])
                                        d2['服务故障'].append(i[2])
                                        d3['服务故障'].append(i[3])



        #         if i[0] is not None:
        #             if i[0] in d1.keys():
        #                 d1[i[0]] += 1
        #             else:
        #                 d1[i[0]] = 1
        #
        #         if i[1] is not None:
        #             if i[1] in d2.keys():
        #                 d2[i[1]] += 1
        #             else:
        #                 d2[i[1]] = 1
        #         if i[2] is not None:
        #             if i[2] in d3.keys():
        #                 d3[i[2]] += 1
        #             else:
        #                 d3[i[2]] = 1
        #         if i[3] is not None:
        #             if i[3] in d4.keys():
        #                 d4[i[3]] += 1
        #             else:
        #                 d4[i[3]] = 1
        #     d['故障级别'] = {}
        #     d['故障原因'] = {}
        #     d['责任方'] = {}
        #     d['路局'] = {}
        #     # 故障级别的总值
        #     sum_fault_level= sum(d1.values())
        #     for i in d1:
        #         d['故障级别'][i] = d1[i] / sum_fault_level
        #     # 故障原因的总值
        #     sum_fault_cause = sum(d2.values())
        #     for i in d2:
        #         d['故障原因'][i] = d2[i] / sum_fault_cause
        #     # 责任方的总值
        #     sum_resp = sum(d2.values())
        #     for i in d3:
        #         d['责任方'][i] = d3[i] / sum_resp
        #     # 路局的总值
        #     sum_railway = sum(d4.values())
        #     for i in d4:
        #         d['路局'][i] = d4[i] / sum_railway
        new_d = {}
        new_d1 = {}
        new_d2 = {}
        new_d3 = {}
        for i in d:
            new_d[i] = {}
            for j in d[i]:
                new_d[i][j] = d[i].count(j) / len(d[i])
        for i in d1:
            new_d1[i] = {}
            for j in d1[i]:
                new_d1[i][j] = d1[i].count(j) / len(d1[i])
        for i in d2:
            new_d2[i] = {}
            for j in d2[i]:
                new_d2[i][j] = d2[i].count(j) / len(d2[i])
        for i in d3:
            new_d3[i] = {}
            for j in d3[i]:
                new_d3[i][j] = d3[i].count(j) / len(d3[i])
        print(new_d)
        print(new_d1)
        print(new_d2)
        print(new_d3)

    # 连接数据库提取数据
    def select_value(self, modelName):
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
                m.model_type = 'ANALYSIS_PROPORTION_MODEL'
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
        # 删选出所有的2级部件
        # two_parts = self.tree_d(tuple_trainno,tuple_objids)
        # key,value调换
        # new_two = {}
        # for i in two_parts:
        #     new_two[two_parts[i]] = i

        if input_value[0][0] is not None:
            sql_start = 'AND d.occurrence_time >= \'{}\''.format(input_value[0][0].strftime("%Y-%m-%d"))
            sql_end = 'AND d.occurrence_time < \'{}\''.format(input_value[0][1].strftime("%Y-%m-%d"))
            # 基本故障的四个值
            # a = self.faultNum(sql_start, sql_end, tuple(tuple_trainno), sql_fault)

            # for i in a:
            #     for j in a[i]:
            #         if j in new_two.keys():
            #             a[i][new_two[j]] = a[i].pop(j)

            d = self.select_other_four_value(tuple(tuple_trainno), sql_start, sql_end,sql_fault,late_from,late_end,late_type)

        else:
            sql_start = 'AND t.accumulated_mileage >= {}'.format(input_value[0][4])
            sql_end = 'AND t.accumulated_mileage < {}'.format(input_value[0][5])
            # 基本故障的四个值
            # a = self.faultNum(sql_start, sql_end, tuple(tuple_trainno), sql_fault)

            # for i in a:
            #     for j in a[i]:
            #         if j in new_two.keys():
            #             a[i][new_two[j]] = a[i].pop(j)

            d = self.select_other_four_value(tuple(tuple_trainno), sql_start, sql_end, sql_fault, late_from, late_end,late_type)

fault().select_value('测试01(1)')