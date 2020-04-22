#!/bin/env python3
#coding=utf-8
# @Time    : 16/12/5 18:15
# @Author  : kelly
# @Site    : 
# @File    : multithread.py
# @Software: PyCharm

import sys
sys.path.append("./")
sys.path.append("../")

import threading
import business_logic.insurance_logic as ins_logic
import dbconfig

# print(dbconfig.position(),'imported')

if dbconfig.env == 'prd':
    threading_num = 20
else:
    threading_num = 2

class myThread:
    def set_parameter(self,parameter):
        self.p = [[] for a in range(threading_num)]
        i = 0
        parameter = list(parameter)
        while len(parameter) > 0:
            i = 0
            while i < threading_num:
                if len(parameter) == 0:
                    break
                self.p[i].append(parameter.pop())
                i += 1

    def set(self,program):
        self.program = program
        if self.program == 'auto_quote_daily':
            request_program = ins_logic.refresh_quote()
            request_program.get_quotable_objects()
            self.set_parameter(request_program.quotable_result)

    def main(self):
        threads = []
        while len(threads) < threading_num:
            # threads.append(threading.Thread(target=self.program.refresh_objects(),name=self.main_program))
            if self.program == 'auto_quote_daily':
                threads.append(threading.Thread(target=ins_logic.refresh_quote().refresh_objects(self.p[len(threads)])))
            else:
                break

        print(dbconfig.position(),'%s threads ready...go' % len(threads))
        for t in threads:
            # t.setDaemon(True)
            t.start()

        for t in threads:
            t.join()

        print(dbconfig.position(), "all over")
