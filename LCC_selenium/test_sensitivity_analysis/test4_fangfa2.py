import pymysql
		
class SensiClass:
	def adjust_per_teamprice(self,cost_average_team,percentage,data_overall_duration,cost_overall,cost_overall_team):
		percentage = percentage / 100
		cost_average_team_new = cost_average_team * percentage + cost_average_team
		cost_overall_team_new = cost_average_team_new * data_overall_duration
		cost_overall_new = cost_overall + cost_overall_team_new - cost_overall_team
		percentage_new = (cost_overall_new - cost_overall) / cost_overall
		cost_average_team_new = float(("%.2f" % cost_average_team_new))
		cost_overall_team_new = float(("%.2f" % cost_overall_team_new))
		cost_overall_new = float(("%.2f" % cost_overall_new))	
		percentage_new = format(percentage_new, '.2%')
		return cost_overall_new,cost_overall_team_new,percentage_new,cost_average_team_new

	def connect_mysql_lcc(self,sql_exe_mate,sql_exe_team):
		db = pymysql.connect("192.168.1.21","root","123456",charset="utf8")
		cur = db.cursor()
		cur.execute("use lcc")
		cur.execute(sql_exe_mate)
		data_mate = cur.fetchall()
		try:
			data_mate = float(data_mate[0][0])
		except TypeError:
			data_mate = 0
		cur.execute(sql_exe_team)
		data_team_all = cur.fetchall()
		try:
			data_team,data_duration = float(data_team_all[0][0]),float(data_team_all[0][1])
		except TypeError:
			data_team = 0
			data_duration = 0
		db.commit()
		cur.close()
		db.close()
		return data_mate,data_team,data_duration

	def connect_darams_mileage(self,sql_execure_mileage):
		db = pymysql.connect("192.168.1.21","root","123456",charset="utf8")
		cur = db.cursor()
		cur.execute("use darams")
		cur.execute(sql_execure_mileage)
		data = cur.fetchall()
		return data 

	def main(self,car,mileage,percentage):
		cost_overall = 0
		cost_overall_team = 0
		data_overall_duration = 0
		sql_execure_mileage = \
		'''
		SELECT
			MIN( mileage_time ),MAX( mileage_time ) 
		FROM
			cd_mileage m INNER JOIN cd_train_real_time r ON r.id = m.train_real_time_id
		WHERE
			1 = 1 AND m.del_flag = '0' 
			AND m.current_mileage >= '{}' 
			AND m.current_mileage < '{}';'''.format(mileage[0],mileage[1])
		date = self.connect_darams_mileage(sql_execure_mileage)
		# print(date[0][0],date[0][1])
		for i in car:
			for j in car[i]:
				inputdata = [i,j,date[0][0],date[0][1]]
				sql_exe_mate = \
				'''
				SELECT sum(IF(s.purchase_price IS NULL,IF( t.purchase_price IS NULL,IF ( e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),s.purchase_price) * IF(d.material_deal_type = '出库', d.material_quantity, -d.material_quantity)) AS 'money'
				FROM op_work_order_header h INNER JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no LEFT JOIN cd_materials_base e ON d.material_no = e.material_no LEFT JOIN cd_materials_batch t ON d.material_no = t.material_no AND d.batch_no = t.batch_no
					LEFT JOIN cd_materials_serial s ON d.material_no = s.material_no AND d.batch_no = s.batch_no AND d.serial_no = s.serial_no
				WHERE
					1 = 1 AND h.train_type = '{}' AND h.train_no ='{}' AND h.report_work_status != '已取消' AND h.plan_begin_date >= '{}' AND h.plan_begin_date <= '{}';
				'''.format(inputdata[0],inputdata[1],inputdata[2],inputdata[3])	
				sql_exe_team = \
				'''
				SELECT sum(IF(b.team_price IS NULL, 0, b.team_price) * t.duration),sum(t.duration)
				FROM op_work_order_header h INNER JOIN op_work_order_team t ON h.work_order_no = t.work_order_no LEFT JOIN cd_team_base b ON t.team_name = b.team_name
				WHERE 1 = 1 AND h.train_type = '{}' AND h.train_no ='{}' AND h.report_work_status != '已取消' AND h.plan_begin_date >= '{}' AND h.plan_begin_date <= '{}';
				'''.format(inputdata[0],inputdata[1],inputdata[2],inputdata[3])

				cost_mate,cost_team,data_duration = self.connect_mysql_lcc(sql_exe_mate,sql_exe_team)
				data_overall_duration += data_duration
				cost_overall_team += cost_team
				cost_overall += cost_mate
				cost_overall += cost_team
		cost_average_team = cost_overall_team / data_overall_duration
		cost_overall_new,cost_overall_team_new,percentage_new,cost_average_team_new = self.adjust_per_teamprice(cost_average_team,percentage,data_overall_duration,cost_overall,cost_overall_team)
		data_overall_duration = float(("%.2f" % data_overall_duration))
		cost_average_team = float(("%.2f" % cost_average_team))
		return {'维修总费用':cost_overall,'总工时费':cost_overall_team,'平均工时费':cost_average_team,'总工时(小时)':data_overall_duration,'变动后维修总费':cost_overall_new,'变动后工时费':cost_overall_team_new,'变动后平均工时费':cost_average_team_new,'变动百分比':percentage_new}

# a = SensiAnalyClass().main({'E27':['2776','2886'],'E28':['2216']},['2017-05-01','2018-03-31'],23)
# print(a)
# a = SensiClass().main({'E27':['2651'],'E28':['2216']},['1500000','2300000'],23)
# print(a)
