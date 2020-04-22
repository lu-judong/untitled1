#!/bin/env python3
#coding=utf-8
# @Time    : 2018/7/16 下午3:55
# @Author  : kelly
# @Site    : 
# @File    : compile.py
# @Software: PyCharm
import compileall
import os
import shutil

project_path='.'
out_path='/out'
expect_path=['logs','log','basic_config','.idea','build','dist']
expect_file=['compile','eurasia']

class main:
    def __init__(self):
        if project_path=='.':
            self.project_path = os.getcwd()
            # self.path=pathlib.Path(os.getcwd()+out_path)
            self.path = os.getcwd() + out_path
        else:
            self.project_path = project_path
            # self.path=pathlib.Path(project_path+out_path)
            self.path = project_path + out_path

        self.parent_path = os.path.dirname(self.project_path)
        self.project_name = self.project_path[len(self.parent_path)+1:]
        print('parent path is %s' % self.parent_path )
        print("project path is '%s'" % self.project_path)
        print("compile path is '%s'" % self.path)
        print('project name is %s' % self.project_name)

    def path_verify(self):
        try:
            a = os.listdir(self.path)
        except:
            os.mkdir(self.path)
            print("path create successfully")
        finally:
            print("path verify successfully.")

    def clean(self):
        try:
            a = os.listdir(self.path)
            shutil.rmtree(self.path)
            print("path clear successfully")
        except:
            print("path clean already")


    def compile_project(self):
        compileall.compile_dir(r'%s' % project_path)
        print('compile %s successfully' % self.project_path)

    def project_structure(self):
        for root, dirs, files in os.walk(self.project_path):
            for dir in dirs:
                if dir=='__pycache__':
                    os.mkdir(self.path+root[len(self.parent_path):])
                    print(self.path + root[len(self.parent_path):],'created.')
                    break

    def pyc_move(self):
        for root, dirs, files in os.walk(self.project_path):
            if root[-11:] == '__pycache__' and root[:-11][len(self.project_path)+1:-1] not in expect_path:
                for file in files:
                    if file.split('.')[0] not in expect_file:
                        filename=file.split('.')[0] + '.' + file.split('.')[-1]
                        shutil.copy2(root+'/'+file,self.path+'/'+root[len(self.parent_path)+1:-11-1]+'/'+filename)
                print(self.path + root[len(self.parent_path):-11], 'created.')
        # setting files move
        os.removedirs(self.path+'/'+self.project_name+'/basic_config')
        shutil.copytree(self.project_path+'/basic_config', self.path+'/'+self.project_name+'/basic_config', symlinks=False, ignore=shutil.ignore_patterns("*.pyc"),copy_function=shutil.copy2, ignore_dangling_symlinks=True)

    def pyc_clean(self):
        for root, dirs, files in os.walk(self.project_path):
            if root.__contains__('__pycache__'):
                for file in files:
                    os.remove(root+'/'+file)
                os.rmdir(root)
                print('%s deleted' % root)

    def project_archive(self):
        shutil.make_archive(self.project_name, 'zip', self.path,)
        shutil.move(self.project_path+'/'+self.project_name+'.zip', self.path , copy_function=shutil.copy2)

if __name__ == '__main__':
    a = main()
    # 清理输出目录
    a.clean()
    # 编译所有文件
    a.compile_project()
    # 创建目录结构
    a.path_verify()
    a.project_structure()
    # 移动文件并改名字
    a.pyc_move()
    # 删除所有pycache
    a.pyc_clean()
    # 压缩文件
    a.project_archive()
    # os.system('pyinstaller /Users/kelly/Desktop/现代工业信息化公司/DARAMS/系统开发/data_manage/webserver.spec')