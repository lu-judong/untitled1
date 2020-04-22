# import paramiko
#
#
# host = '192.168.1.20'
# user = 'Administrator'
# password = 'zaq12wsx.'
#
# client = paramiko.SSHClient()
# client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# client.connect(host, 22, username=user, password=password, timeout=10)
#
#
# stdin3, stdout3, stderr3 = client.exec_command('cmd /c D:\\tools\\tomcat8.0-2\\bin\startup.bat')
# print(stdout3.read().decode())
import numpy
import pymysql

db = pymysql.connect("192.168.1.21", "root", "123456", charset="utf8")
cur = db.cursor()
cur.execute("use lcc")
sql = '''
SELECT
te.team_name as teamName,
SUBSTRING_INDEX(

IF (
SUBSTRING_INDEX(r.repair_location, '.', 3) = SUBSTRING_INDEX(r.repair_location, '.', 2),
NULL,
SUBSTRING_INDEX(r.repair_location, '.', 3)
),
'.' ,- 1
) AS repairLocation,

ifnull(concat(r.repair_level,""),"(空白)") AS "repairLevel",
te.duration * b.team_price AS "totalManHourMoney",
IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)
    * IF(d.material_deal_type = '出库', d.material_quantity, -d.material_quantity) AS "totalMaterialMoney"

-- COUNT(*) AS "repairLevelCount"
FROM
op_work_order_header h
INNER JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
LEFT JOIN cd_materials_base e ON d.material_no = e.material_no
LEFT JOIN cd_materials_batch t ON d.material_no = t.material_no AND d.batch_no = t.batch_no
LEFT JOIN cd_materials_serial s ON d.material_no = s.material_no AND d.batch_no = s.batch_no AND d.serial_no = s.serial_no
INNER JOIN op_work_order_team te ON te.work_order_no = h.work_order_no
INNER JOIN cd_team_base b ON te.team_name = b.team_name
LEFT JOIN  op_work_order_technology tech on tech.work_order_no = h.work_order_no
-- 
WHERE h.report_work_status != '已取消'
AND h.train_no IN ('2651','2216')
AND h.plan_begin_date >= '2017-02-03'
AND h.plan_begin_date <= '2017-08-02'
HAVING
    repairLocation IS NOT NULL
'''
cur.execute(sql)
re = cur.fetchall()

L0 = []
num = 3


for k in range(2):
    l_re = numpy.array(re)
    l_re1 = l_re.T
    l_re2 = list(set(l_re1[2]))
    d_1 = dict()

    for i in l_re2:
        d_1[i] = 0
        for j in l_re:
            if j[1] == '车内结构' and j[2] == i:
                d_1[i] += j[num]

    L0.append(d_1)
    num += 1


l_re = numpy.array(re)
l_re1 = l_re.T
l_re2 = list(set(l_re1[2]))
d_2 = dict()

for i in l_re2:
    d_2[i] = 0
    for j in l_re:
        if j[2] == i and j[1] == '车内结构':
            d_2[i] += 1

print(L0)
print(d_2)
