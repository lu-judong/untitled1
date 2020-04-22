import pymysql
class HomeModelCal:
	def num_1AND2(self):
		''' 功能一：列车数量-------------------------------------------------'''
		sql_no_obj = \
		'''
		SELECT
			d.start_date,
			d.end_date,
			d.average_speed_select,
			d.interval_date,
			mt.train_no_id,
			o.fault_object_id,
			sf.fault_define,
			lh.late_hours
		FROM
			conf_model m 
			INNER JOIN conf_model_train mt ON mt.conf_model_id = m.id 
			INNER JOIN conf_fault_object o ON o.conf_model_id = m.id
			INNER JOIN conf_date d ON d.conf_model_id = m.id 
			LEFT JOIN conf_service_fault sf ON sf.conf_model_id = m.id
			LEFT JOIN conf_late_hours lh ON lh.conf_model_id = m.id
		WHERE 
			m.model_type = 'USER_MODEL'
			and m.is_default = '1';
		'''
		db = pymysql.connect("192.168.1.22","root","123456",charset="utf8")
		cur = db.cursor()
		cur.execute("use darams")
		cur.execute(sql_no_obj)
		data_input = cur.fetchall()
		date_start = data_input[0][0]
		date_end = data_input[0][1]
		speed_ave = data_input[0][2]
		date_inteval = data_input[0][3]
		tuple_trainno = tuple(data_input[0][4].split(','))
		tuple_objids = tuple(data_input[0][5].split(','))
		service_fault = tuple(data_input[0][6].split(','))
		late_hours = data_input[0][7]
		result_1 = len(tuple_trainno)
		''' 功能二：部件总数-------------------------------------------------'''
		tuple_faultobj = tuple(data_input[0][5].split(','))
		if len(tuple_trainno) == 1:
			str_trainno = str(tuple_trainno[0])
			sql_objsum = \
			'''
			SELECT
				sum(train_counts) AS obj_sum
			FROM
				cd_fault_object
			WHERE
				train_no_id = '{}'
				AND fault_object_id IN {};
			'''.format(str_trainno,tuple_faultobj)
			if len(tuple_faultobj) == 1:
				str_faultobj = str(tuple_faultobj[0])
				sql_objsum = \
				'''
				SELECT
					sum(train_counts) AS obj_sum
				FROM
					cd_fault_object
				WHERE
					train_no_id = '{}'
					AND fault_object_id = '{}';
				'''.format(str_trainno,str_faultobj)
		else:
			sql_objsum = \
			'''
			SELECT
				sum(train_counts) AS obj_sum
			FROM
				cd_fault_object
			WHERE
				train_no_id IN {}
				AND fault_object_id IN {};
			'''.format(tuple_trainno,tuple_faultobj)
			if len(tuple_faultobj) == 1:
				str_faultobj = str(tuple_faultobj[0])
				sql_objsum = \
				'''
				SELECT
					sum(train_counts) AS obj_sum
				FROM
					cd_fault_object
				WHERE
					train_no_id IN {}
					AND fault_object_id = '{}';
				'''.format(tuple_trainno,str_faultobj)
		cur.execute(sql_objsum)
		data_objsum = cur.fetchall()
		result_2 = data_objsum[0][0]
		if result_2 == None:
			result_2 = 0
		return result_1,result_2,date_start,date_end,tuple_trainno,tuple_objids,service_fault,late_hours,cur

	def num_3(self,date_start,date_end,tuple_trainno,cur):
		''' 功能三：列车行驶累计里程数(万公里)-------------------------------------------------'''
		diff_mileage_sum = 0
		for train in tuple_trainno:
			sql_leftmileage = \
			'''
			SELECT 
				((if(ed.mileage is null,sd.mileage,ed.mileage) - sd.mileage) / 10000) / if(datediff(if(ed.mileage is null,sd.mileageDate,ed.mileageDate),sd.mileageDate)=0,1,datediff(if(ed.mileage is null,sd.mileageDate,ed.mileageDate),sd.mileageDate)) * datediff('{}',sd.mileageDate) + (sd.mileage / 10000) as c_mileage
			FROM
				(SELECT 
					1 id,
					m.mileage_time as mileageDate,
					m.current_mileage as mileage
				FROM cd_train_no n
				INNER JOIN cd_train_real_time tr on n.id = tr.train_no_id
				INNER JOIN cd_mileage m on tr.id = m.train_real_time_id AND m.del_flag = '0'
				where 1=1
					AND m.mileage_time < '{}'
					AND m.current_mileage IS NOT NULL
					and n.train_no IN (SELECT train_no FROM cd_train_no WHERE id = '{}')
				order by m.mileage_time desc
				limit 1) sd 
			LEFT JOIN
				(SELECT 
					1 id,
					m.mileage_time as mileageDate,
					m.current_mileage as mileage
				FROM cd_train_no n
				INNER JOIN cd_train_real_time tr on n.id = tr.train_no_id
				INNER JOIN cd_mileage m on tr.id = m.train_real_time_id AND m.del_flag = '0'
				where 1=1
					AND m.mileage_time > '{}'
					AND m.current_mileage IS NOT NULL
					and n.train_no IN (SELECT train_no FROM cd_train_no WHERE id = '{}')
				order by m.mileage_time 
				limit 1) ed ON sd.id = ed.id  
			'''.format(date_start,date_start,train,date_start,train)
			cur.execute(sql_leftmileage)
			data_leftmileage = cur.fetchall()
			try: 
				data_leftmileage = data_leftmileage[0][0]  #会报错
			except IndexError:
				print(sql_leftmileage)
				break
			sql_rightmileage = \
			'''
			SELECT 
				((if(ed.mileage is null,sd.mileage,ed.mileage) - sd.mileage) / 10000) / if(datediff(if(ed.mileage is null,sd.mileageDate,ed.mileageDate),sd.mileageDate)=0,1,datediff(if(ed.mileage is null,sd.mileageDate,ed.mileageDate),sd.mileageDate)) * datediff('{}',sd.mileageDate) + (sd.mileage / 10000) as c_mileage
			FROM
				(SELECT 
					1 id,
					m.mileage_time as mileageDate,
					m.current_mileage as mileage
				FROM cd_train_no n
				INNER JOIN cd_train_real_time tr on n.id = tr.train_no_id
				INNER JOIN cd_mileage m on tr.id = m.train_real_time_id AND m.del_flag = '0'
				where 1=1
					AND m.mileage_time < '{}'
					AND m.current_mileage IS NOT NULL
					and n.train_no IN (SELECT train_no FROM cd_train_no WHERE id = '{}')
				order by m.mileage_time desc
				limit 1) sd 
			LEFT JOIN
				(SELECT 
					1 id,
					m.mileage_time as mileageDate,
					m.current_mileage as mileage
				FROM cd_train_no n
				INNER JOIN cd_train_real_time tr on n.id = tr.train_no_id
				INNER JOIN cd_mileage m on tr.id = m.train_real_time_id AND m.del_flag = '0'
				where 1=1
					AND m.mileage_time > '{}'
					AND m.current_mileage IS NOT NULL
					and n.train_no IN (SELECT train_no FROM cd_train_no WHERE id = '{}')
				order by m.mileage_time 
				limit 1) ed ON sd.id = ed.id  
			'''.format(date_end,date_end,train,date_end,train)
			cur.execute(sql_rightmileage)
			data_rightmileage = cur.fetchall()
			data_rightmileage = data_rightmileage[0][0]     
			diff_mileage = data_rightmileage - data_leftmileage
			diff_mileage_sum += diff_mileage
		diff_mileage_sum = ("%.4f" % diff_mileage_sum)
		result_3 = float(diff_mileage_sum)
		return result_3

	def num_4567_botton2(self,date_start,date_end,tuple_trainno,tuple_objids,service_fault,late_hours,cur):
		''' 功能四：基本故障数-------------------------------------------------'''
		sum_basic = 0
		sum_associate = 0
		sum_service = 0
		sum_safe = 0
		for train in tuple_trainno:
			#  基础故障数
			sql_basic_sum = \
			'''
			SELECT
				count(1) 
			FROM
				op_fault_order_header h 
				INNER JOIN op_fault_order_detail d ON d.fault_id = h.id 
				INNER JOIN op_train n ON n.fault_detail_id = d.id
				INNER JOIN op_fault_real r ON r.fault_detail_id = d.id 
			WHERE
				h.`status` != '已取消'
				AND d.occurrence_time >= '{}'
				AND d.occurrence_time < '{}'
				AND n.train_no IN (SELECT train_no FROM cd_train_no WHERE id = '{}')  -- 基本故障
				AND r.real_fault_object_id IN {}
			'''.format(date_start,date_end,train,tuple_objids)
			cur.execute(sql_basic_sum)
			data_basic = cur.fetchall()
			sum_basic += data_basic[0][0]

			# 关联故障数
			sql_associated_sum = \
			'''
			SELECT
				count(1) 
			FROM
				op_fault_order_header h 
				INNER JOIN op_fault_order_detail d ON d.fault_id = h.id 
				INNER JOIN op_train n ON n.fault_detail_id = d.id
				INNER JOIN op_fault_real r ON r.fault_detail_id = d.id 
			WHERE
				h.`status` != '已取消'
				AND d.occurrence_time >= '{}'
				AND d.occurrence_time < '{}'
				AND n.train_no IN (SELECT train_no FROM cd_train_no WHERE id = '{}')  -- 基本故障
				AND d.fault_property = '关联故障'  -- 关联故障
				AND r.real_fault_object_id IN {}
			'''.format(date_start,date_end,train,tuple_objids)
			cur.execute(sql_associated_sum)
			data_associate = cur.fetchall()
			sum_associate += data_associate[0][0]

			# 服务故障数
			if '晚点' in service_fault:
				sql_service_sum = \
				'''
				SELECT
					count(1) 
				FROM
					op_fault_order_header h 
					INNER JOIN op_fault_order_detail d ON d.fault_id = h.id 
					INNER JOIN op_train n ON n.fault_detail_id = d.id
					INNER JOIN op_fault_real r ON r.fault_detail_id = d.id
				WHERE
					h.`status` != '已取消'
					AND d.occurrence_time >= '{}'
					AND d.occurrence_time < '{}'
					AND n.train_no IN (SELECT train_no FROM cd_train_no WHERE id = '{}')  -- 基本故障
					AND d.fault_property = '关联故障'  -- 服务故障
					AND (n.start_late >= '{}' OR n.end_late >= '{}')
					AND r.real_fault_object_id IN {}
				'''.format(date_start,date_end,train,late_hours,late_hours,tuple_objids)
				cur.execute(sql_service_sum)
				data_service_late = cur.fetchall()
				sum_service += data_service_late[0][0]
			else:
				sql_service_sum = \
				'''
				SELECT
					count(1) 
				FROM
					op_fault_order_header h 
					INNER JOIN op_fault_order_detail d ON d.fault_id = h.id 
					INNER JOIN op_train n ON n.fault_detail_id = d.id
					INNER JOIN op_fault_real r ON r.fault_detail_id = d.id 
				WHERE
					h.`status` != '已取消'
					AND d.occurrence_time >= '{}'
					AND d.occurrence_time < '{}'
					AND n.train_no IN (SELECT train_no FROM cd_train_no WHERE id = '{}')  -- 基本故障
					AND (d.fault_property = '关联故障' AND n.service_fault_class in {})  -- 服务故障
					AND d.fault_property = '关联故障'  -- 关联故障
					AND r.real_fault_object_id IN {}
				'''.format(date_start,date_end,train,service_fault,tuple_objids)
				cur.execute(sql_service_sum)
				data_service = cur.fetchall()
				sum_service += data_service[0][0]

			# 安监故障数
			sql_safe_sum = \
			'''
			SELECT 
				count(1) 
			FROM
				op_fault_order_header h 
				INNER JOIN op_fault_order_detail d ON d.fault_id = h.id 
				INNER JOIN op_train n ON n.fault_detail_id = d.id
				INNER JOIN op_fault_real r ON r.fault_detail_id = d.id 
			WHERE
				h.`status` != '已取消'
				AND d.occurrence_time >= '{}'
				AND d.occurrence_time < '{}'
				AND n.train_no IN (SELECT train_no FROM cd_train_no WHERE id = '{}')  -- 基本故障
				AND (d.fault_property = '关联故障' AND r.safety_supervisio_fault = '是')  -- 安监故障
				AND d.fault_property = '关联故障'  -- 关联故障
				AND r.real_fault_object_id IN {}
			'''.format(date_start,date_end,train,tuple_objids)
			cur.execute(sql_safe_sum)
			data_safe = cur.fetchall()
			sum_safe += data_safe[0][0]
		result_4 = sum_basic
		result_5 = sum_associate
		result_6 = sum_service
		result_7 = sum_safe
		return result_4,result_5,result_6,result_7

	def num_4567_botton1(self,date_start,date_end,tuple_trainno,tuple_objids,service_fault,late_hours,cur):
		''' 功能四：基本故障数-------------------------------------------------'''
		sum_basic = 0
		sum_associate = 0
		sum_service = 0
		sum_safe = 0

		#  求所选故障对象及其下所有子节点的对象ID
		list_allobj_ids = []
		list_trainno = list(tuple_trainno)
		list_objids = list(tuple_objids)
		for train in list_trainno:
			sql_objuuids = \
			'''
			SELECT
				o.relationship_id
			FROM
				cd_fault_object o 
				INNER JOIN cd_train_no n on n.id = o.train_no_id 
			WHERE
				o.fault_object_id IN {}
				AND n.train_no IN (SELECT train_no FROM cd_train_no WHERE id = '{}')
			'''.format(tuple_objids,train)
			cur.execute(sql_objuuids)
			data_objuuids = cur.fetchall()
			# print(data_objuuids)
			for uuid in data_objuuids:
				sql_OneObj_ids = \
				'''
				SELECT
					o.fault_object_id
				FROM
					cd_fault_object o 
					INNER JOIN cd_train_no n on n.id = o.train_no_id 
				WHERE
					n.train_no IN (SELECT train_no FROM cd_train_no WHERE id = '{}')
					AND o.fault_object_desc in 
					(SELECT fault_node FROM cd_fault_object_tree WHERE parent_fault_nodes LIKE '%{}%')
				'''.format(train,uuid[0])
				cur.execute(sql_OneObj_ids)
				data_oneobj_ids = cur.fetchall()
				for objid in data_oneobj_ids:
					list_allobj_ids.append(str(objid[0]))
				for objid in list_objids:
					list_allobj_ids.append(objid)
		list_allobj_ids = list(set(list_allobj_ids))
		list_allobj_ids.sort()
		tuple_objids = tuple(list_allobj_ids)
		# print(list_allobj_ids)     #算出来的id会比剑华的多。
		# print(len(list_allobj_ids))   
			
		for train in tuple_trainno:
			#  基础故障数
			sql_basic_sum = \
			'''
			SELECT
				count(1) 
			FROM
				op_fault_order_header h 
				INNER JOIN op_fault_order_detail d ON d.fault_id = h.id 
				INNER JOIN op_train n ON n.fault_detail_id = d.id
				INNER JOIN op_fault_real r ON r.fault_detail_id = d.id 
			WHERE
				h.`status` != '已取消'
				AND d.occurrence_time >= '{}'
				AND d.occurrence_time < '{}'
				AND n.train_no IN (SELECT train_no FROM cd_train_no WHERE id = '{}')  -- 基本故障
				AND r.real_fault_object_id IN {}
			'''.format(date_start,date_end,train,tuple_objids)
			cur.execute(sql_basic_sum)
			data_basic = cur.fetchall()
			sum_basic += data_basic[0][0]

			# 关联故障数
			sql_associated_sum = \
			'''
			SELECT
				count(1) 
			FROM
				op_fault_order_header h 
				INNER JOIN op_fault_order_detail d ON d.fault_id = h.id 
				INNER JOIN op_train n ON n.fault_detail_id = d.id
				INNER JOIN op_fault_real r ON r.fault_detail_id = d.id 
			WHERE
				h.`status` != '已取消'
				AND d.occurrence_time >= '{}'
				AND d.occurrence_time < '{}'
				AND n.train_no IN (SELECT train_no FROM cd_train_no WHERE id = '{}')  -- 基本故障
				AND d.fault_property = '关联故障'  -- 关联故障
				AND r.real_fault_object_id IN {}
			'''.format(date_start,date_end,train,tuple_objids)
			cur.execute(sql_associated_sum)
			data_associate = cur.fetchall()
			sum_associate += data_associate[0][0]

			# 服务故障数
			if '晚点' in service_fault:
				sql_service_sum = \
				'''
				SELECT
					count(1) 
				FROM
					op_fault_order_header h 
					INNER JOIN op_fault_order_detail d ON d.fault_id = h.id 
					INNER JOIN op_train n ON n.fault_detail_id = d.id
					INNER JOIN op_fault_real r ON r.fault_detail_id = d.id
				WHERE
					h.`status` != '已取消'
					AND d.occurrence_time >= '{}'
					AND d.occurrence_time < '{}'
					AND n.train_no IN (SELECT train_no FROM cd_train_no WHERE id = '{}')  -- 基本故障
					AND d.fault_property = '关联故障'  -- 服务故障
					AND (n.start_late >= '{}' OR n.end_late >= '{}')
					AND r.real_fault_object_id IN {}
				'''.format(date_start,date_end,train,late_hours,late_hours,tuple_objids)
				cur.execute(sql_service_sum)
				data_service_late = cur.fetchall()
				sum_service += data_service_late[0][0]
			else:
				sql_service_sum = \
				'''
				SELECT
					count(1) 
				FROM
					op_fault_order_header h 
					INNER JOIN op_fault_order_detail d ON d.fault_id = h.id 
					INNER JOIN op_train n ON n.fault_detail_id = d.id
					INNER JOIN op_fault_real r ON r.fault_detail_id = d.id 
				WHERE
					h.`status` != '已取消'
					AND d.occurrence_time >= '{}'
					AND d.occurrence_time < '{}'
					AND n.train_no IN (SELECT train_no FROM cd_train_no WHERE id = '{}')  -- 基本故障
					AND (d.fault_property = '关联故障' AND n.service_fault_class in {})  -- 服务故障
					AND d.fault_property = '关联故障'  -- 关联故障
					AND r.real_fault_object_id IN {}
				'''.format(date_start,date_end,train,service_fault,tuple_objids)
				cur.execute(sql_service_sum)
				data_service = cur.fetchall()
				sum_service += data_service[0][0]

			# 安监故障数
			sql_safe_sum = \
			'''
			SELECT 
				count(1) 
			FROM
				op_fault_order_header h 
				INNER JOIN op_fault_order_detail d ON d.fault_id = h.id 
				INNER JOIN op_train n ON n.fault_detail_id = d.id
				INNER JOIN op_fault_real r ON r.fault_detail_id = d.id 
			WHERE
				h.`status` != '已取消'
				AND d.occurrence_time >= '{}'
				AND d.occurrence_time < '{}'
				AND n.train_no IN (SELECT train_no FROM cd_train_no WHERE id = '{}')  -- 基本故障
				AND (d.fault_property = '关联故障' AND r.safety_supervisio_fault = '是')  -- 安监故障
				AND d.fault_property = '关联故障'  -- 关联故障
				AND r.real_fault_object_id IN {}
			'''.format(date_start,date_end,train,tuple_objids)
			cur.execute(sql_safe_sum)
			data_safe = cur.fetchall()
			sum_safe += data_safe[0][0]
		result_4 = sum_basic
		result_5 = sum_associate
		result_6 = sum_service
		result_7 = sum_safe
		return result_4,result_5,result_6,result_7



	def main(self):
		result_1,result_2,date_start,date_end,tuple_trainno,tuple_objids,service_fault,late_hours,cur = self.num_1AND2()
		result_3 = self.num_3(date_start,date_end,tuple_trainno,cur)
		result_b1_4,result_b1_5,result_b1_6,result_b1_7 = self.num_4567_botton1(date_start,date_end,tuple_trainno,tuple_objids,service_fault,late_hours,cur)
		result_2 = int(result_2)
		list_b1 = [result_1,result_2,result_3,result_b1_4,result_b1_5,result_b1_6,result_b1_7]
		return list_b1

# list_b1 = HomeModelCal().main()
# print(list_b1)






















