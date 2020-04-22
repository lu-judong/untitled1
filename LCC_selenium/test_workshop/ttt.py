# SELECT
# te.team_name as teamName,
# SUBSTRING_INDEX(
#
# IF (
# SUBSTRING_INDEX(r.repair_location, '.', 3) = SUBSTRING_INDEX(r.repair_location, '.', 2),
# NULL,
# SUBSTRING_INDEX(r.repair_location, '.', 3)
# ),
# '.' ,- 1
# ) AS repairLocation,
# SUM(IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)
# * IF(d.material_deal_type = '出库', d.material_quantity, -d.material_quantity)) AS "totalMaterialMoney",
# SUM(te.duration * b.team_price)AS "totalManHourMoney",
# SUM(d.material_quantity) AS "totalMaterialNum",
# SUM(te.duration) AS "totalManHourNum",
# h.train_no AS "trainNo",
# ifnull(r.repair_location,"(空白)") AS "repairLocationType",
# ifnull(concat(r.repair_level,""),"(空白)") AS "repairLevel",
# if(h.fault_no IS NULL and h.notice_no IS NOT NULL,"预防性维修",(
# if( h.fault_no IS NOT NULL,"修复性维修","(空白)"))) as "repairType",
# ifnull(r.repair_method,"(空白)") as "repairMethod",
# ifnull(r.access_name,"(空白)") as "accessName",
# IFNULL(tech.technology_desc,"(空白)") as "technologyDesc"
# FROM
# op_work_order_header h
# INNER JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
# LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
# LEFT JOIN cd_materials_base e ON d.material_no = e.material_no
# LEFT JOIN cd_materials_batch t ON d.material_no = t.material_no AND d.batch_no = t.batch_no
# LEFT JOIN cd_materials_serial s ON d.material_no = s.material_no AND d.batch_no = s.batch_no AND d.serial_no = s.serial_no
# INNER JOIN op_work_order_team te ON te.work_order_no = h.work_order_no
# INNER JOIN cd_team_base b ON te.team_name = b.team_name
# LEFT JOIN  op_work_order_technology tech on tech.work_order_no = h.work_order_no
#
# WHERE h.report_work_status != '已取消'
# <include refid="common_Where_if"/>
# GROUP BY te.team_name,
# repairLocation
# HAVING
# repairLocation IS NOT NULL
# #
#
#
#
# SELECT
# -- te.team_name as teamName,
# SUBSTRING_INDEX(
#
# IF (
# SUBSTRING_INDEX(r.repair_location, '.', 3) = SUBSTRING_INDEX(r.repair_location, '.', 2),
# NULL,
# SUBSTRING_INDEX(r.repair_location, '.', 3)
# ),
# '.' ,- 1
# ) AS repairLocation,
# SUM(IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)
# * IF(d.material_deal_type = '出库', d.material_quantity, -d.material_quantity)) AS "totalMaterialMoney",
# SUM(te.duration * b.team_price)AS "totalManHourMoney",
# SUM(d.material_quantity) AS "totalMaterialNum",
# SUM(te.duration) AS "totalManHourNum",
# h.train_no AS "trainNo",
# ifnull(concat(r.repair_level,""),"(空白)") AS "repairLevel"
#
# FROM
# op_work_order_header h
# INNER JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
# LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
# LEFT JOIN cd_materials_base e ON d.material_no = e.material_no
# LEFT JOIN cd_materials_batch t ON d.material_no = t.material_no AND d.batch_no = t.batch_no
# LEFT JOIN cd_materials_serial s ON d.material_no = s.material_no AND d.batch_no = s.batch_no AND d.serial_no = s.serial_no
# INNER JOIN op_work_order_team te ON te.work_order_no = h.work_order_no
# INNER JOIN cd_team_base b ON te.team_name = b.team_name
# LEFT JOIN  op_work_order_technology tech on tech.work_order_no = h.work_order_no
#
#
# WHERE h.report_work_status != '已取消'
# AND h.train_no IN ('2651')
# AND h.plan_begin_date >= '2017-02-03'
# AND h.plan_begin_date <= '2017-08-02'
#
# GROUP BY
# repairLocation,repairLevel
# HAVING
# repairLocation IS NOT NULL
# AND
# repairLocation = '转向架组成(动)[二位端]'

d1 = {'2651': [77020.70, 7702070.0000, 60019.51, 7818964.5000], '2216': [91918.30, 9191830, 31242.77, 2065950.0000],
      '2202':[1.0,1,1.0,1.0]}
d = {'2651': '武汉铁路局', '2216': '南昌铁路局', '2202':'南昌铁路局'}
d2 = {}
L3 = []
for nm in d:
    for nm1 in d1:
        if nm == nm1:
            if d[nm] in d2.keys():
                for nm2 in d2[d[nm]]:
                    a = d2[d[nm]].index(nm2)
                    nm2 += d1[nm1][a]
                    L3.append(nm2)
                d2[d[nm]] = L3
            else:
                d2[d[nm]] = d1[nm1]
print(d2)