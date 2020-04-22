import pandas
from sqlalchemy import create_engine
import numpy


car = {'E27':['2651'],'E28':['2216']}
date = ['2017-02-03','2017-10-02']

darams = create_engine('mysql+pymysql://root:123456@192.168.221.21:3306/darams')

lcc = create_engine('mysql+pymysql://root:123456@192.168.221.21:3306/lcc')

if len(date[0]) <= 12:
    date[0] = date[0] + ' 00:00:00'
if len(date[1]) <= 12:
    date[1] = date[1] + ' 00:00:00'

L1 = []
for i in car:
    for j in car[i]:
        L1.append(j)
if len(L1) <= 1:
    I_SQL = 'AND h.train_no = {}'.format(L1[0])
else:
    L1 = tuple(L1)
    I_SQL = 'AND h.train_no in {}'.format(L1)

sql = '''
        select
        n.train_no,
        a.company AS company
        from
        cd_train_no n
        INNER JOIN cd_train_real_time r on n.id = r.train_no_id
        INNER JOIN cd_affiliated  a on r.id = a.train_real_time_id
        where 
        n.train_no in ('2651','2216')
        '''

sql1 = '''
        SELECT
        h.work_order_no,
        h.fault_no,
        h.train_no,
        h.train_type AS 'train_type',
        ifnull(concat(r.repair_level,""),"(空白)") AS "repairLevel",
        mt.produce_manufacturer,
        substring_index(if(substring_index(r.repair_location, '.', 3) = substring_index(r.repair_location, '.', 2),null,substring_index(r.repair_location, '.', 3)
),'.' ,- 1
) AS repairLocation,
        IF(d.material_deal_type = '出库', d.material_quantity, -d.material_quantity) AS "material_num",
        te.duration * b.team_price AS "ManHourMoney",
        IF(s.purchase_price IS NULL, IF(t.purchase_price IS NULL, IF(e.purchase_price IS NULL, 0, e.purchase_price), t.purchase_price),  s.purchase_price)* IF(d.material_deal_type = '出库', d.material_quantity, 0) AS "material_money"
       from op_work_order_header h 
        LEFT JOIN op_work_order_detail d ON h.work_order_no = d.work_order_no
        LEFT JOIN op_work_order_team te ON te.work_order_no = h.work_order_no
        LEFT JOIN op_work_order_repair r ON h.work_order_no = r.work_order_no
        LEFT JOIN cd_materials_base e ON d.material_no = e.material_no
        LEFT JOIN cd_team_base b on b.team_name = te.team_name
        LEFT JOIN cd_materials_batch t ON d.material_no = t.material_no AND d.batch_no = t.batch_no
        LEFT JOIN cd_materials_serial s ON d.material_no = s.material_no AND d.batch_no = s.batch_no AND d.serial_no = s.serial_no
        LEFT JOIN  cd_instance_material mt on mt.material_no = d.material_no
        AND mt.batch_no IS NULL 
        AND mt.serial_no IS NULL
        OR
        mt.material_no = d.material_no
        AND mt.batch_no = d.batch_no
        AND mt.serial_no IS NULL
        OR
        mt.material_no = d.material_no
        AND mt.batch_no = d.batch_no
        AND mt.serial_no = d.serial_no
        WHERE h.report_work_status != '已取消' 
        {}
        AND h.plan_begin_date >= '{}'      
        AND h.plan_begin_date < '{}'
'''.format(I_SQL,date[0],date[1])



df = pandas.read_sql_query(sql, darams)

de = pandas.read_sql_query(sql1,lcc)

res = pandas.merge(df,de,on = 'train_no', how='right')

res1 = numpy.array(res)
res2 = res1.tolist()
print(res2[0])
# print(res1)