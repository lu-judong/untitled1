import datetime
import xlwt
import pymysql



class Method:

    def jira(self,sql):
        db = pymysql.connect("192.168.1.22", "root", "123456", charset="utf8")
        cur = db.cursor()
        cur.execute("use jira")
        cur.execute(sql)
        a = cur.fetchall()
        return a

    def main(self,startdate,enddate):
        # mappings = {
        #     'DARAMS2':'31',
        #     'EDS':'31',
        #     'INTEGR':'31',
        #     'KTYJ':'41',
        #     'LCC':'31',
        #     'SCHEME':'31',
        #
        # }


        sql = '''
            select CONCAT(p.pkey,'-',j.issuenum) as workName,
            j.SUMMARY as summary,
            IF(j.ASSIGNEE is null,'未分配',j.ASSIGNEE) as assignee,
            j.REPORTER as reporter,
            IF(i.pname = 'Done','完成',i.pname) as status,
            j.CREATED as created,
            j.WORKFLOW_ID as workId
            -- h.FINISH_DATE as finishDate
            from 
            jiraissue j 
            INNER JOIN project  p on  j.PROJECT = p.ID
            INNER JOIN issuestatus i on j.issuestatus = i.ID
            -- INNER JOIN os_historystep h on j.WORKFLOW_ID = h.ENTRY_ID
            where i.pname in ('Done','关闭')
            -- and h.ACTION_ID = '41'
        '''
        re = self.jira(sql)

        #查询时间
        sql1 = '''
           select 
            h.ID as id,
            j.SUMMARY as summary,
            h.ENTRY_ID as entryId,
            h.action_id as action,
            h.FINISH_DATE as date
            from 
            jiraissue j 
            
            INNER JOIN os_historystep h on j.WORKFLOW_ID = h.ENTRY_ID
            where j.issuestatus in ('10001','10201')
        '''

        re1 = self.jira(sql1)
        d = {}
        for i in re1:
            if d.get(i[2]) is None:
                d[i[2]] = [[i[0],i[1],i[3],i[4]]]
            else:
                d[i[2]].append([i[0],i[1],i[3],i[4]])
        # print(d)
        # 获得完成时间
        d1 = {}
        flag = False
        for i1 in d:
            if len(d.get(i1)) == 1:
                d1[i1] = [d.get(i1)[0][0],d.get(i1)[0][2],d.get(i1)[0][3]]
            else:
                for i2 in d.get(i1):
                    if i2[2] == 41:
                        flag = True
                        if d1.get(i1) is None:
                            d1[i1] = [i2[0],i2[2],i2[3]]
                        else:
                            if i2[0] > d1[i1][0]:
                                d1[i1] = [i2[0],i2[2],i2[3]]
                            else:
                                pass
                    elif i2[2] == 31 and flag is False:
                        if d1.get(i1) is None:
                            d1[i1] = [i2[0], i2[2], i2[3]]
                        else:
                            if i2[0] > d1[i1][0]:
                                d1[i1] = [i2[0], i2[2], i2[3]]
                            else:
                                pass
                    else:
                        pass

        L = []

        for j in re:
            for j1 in d1:
                if j[-1] == j1:
                    L.append([j[0],j[1],j[2],j[3],j[4],j[5],d1.get(j1)[2]])

        # print(L)
        L_new = []
        for k in L:
            if   datetime.datetime.strptime(startdate,'%Y-%m-%d') < k[-1] and datetime.datetime.strptime(enddate,'%Y-%m-%d') > k[-1]:
                L_new.append(k)
        print(L_new)

        # 创建一个文件对象
        wb = xlwt.Workbook(encoding='utf8')
        # 创建一个sheet对象
        sheet = wb.add_sheet('jira-sheet')

        # 设置文件头的样式,这个不是必须的可以根据自己的需求进行更改
        style_heading = xlwt.easyxf("""
                                  font:
                                      name Arial,
                                      colour_index white,
                                      bold on,
                                      height 0xA0;
                                  align:
                                      wrap off,
                                      vert center,
                                      horiz center;
                                  pattern:
                                      pattern solid,
                                      fore-colour 0x19;
                                  borders:
                                      left THIN,
                                      right THIN,
                                      top THIN,
                                      bottom THIN;
                                  """)

        # 写入文件标题
        sheet.write(0, 0, '关键字', style_heading)
        sheet.write(0, 1, '概要', style_heading)
        sheet.write(0, 2, '经办人', style_heading)
        sheet.write(0, 3, '报告人', style_heading)
        sheet.write(0, 4, '状态', style_heading)
        sheet.write(0, 5, '创建时间', style_heading)
        sheet.write(0, 6, '完成时间', style_heading)

        sheet.col(0).width = 5000
        sheet.col(1).width = 20000
        sheet.col(2).width = 5000
        sheet.col(3).width = 5000
        sheet.col(4).width = 2000
        sheet.col(5).width = 5000
        sheet.col(6).width = 5000

        # 写入数据
        data_row = 1
        for m in L_new:
            sheet.write(data_row, 0, m[0])
            sheet.write(data_row, 1, m[1])
            sheet.write(data_row, 2, m[2])
            sheet.write(data_row, 3, m[3])
            sheet.write(data_row, 4, m[4])
            sheet.write(data_row, 5, m[5].strftime('%Y-%m-%d %H:%M:%S'))
            sheet.write(data_row, 6, m[6].strftime('%Y-%m-%d %H:%M:%S'))
            data_row = data_row + 1
            # 写出到IO

        wb.save('jira{}.xls'.format(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))




Method().main('2019-08-23','2019-09-23')

