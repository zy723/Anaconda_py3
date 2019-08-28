#!/usr/bin/env python
# encoding: utf-8


import os

"""
@version: v1.0
@contact: zy723@vip.qq.com
@site: 
@software: PyCharm
@file: page32.py
@time: 2019/8/27 15:10
"""

'''
3.4.补充缺失的代码？(2018-4-16-lxy)
1．def print_directory_contents(sPath):
2． """
3． 这个函数接收文件夹的名称作为输入参数
4． 返回该文件夹中文件的路径
5． 以及其包含文件夹中文件的路径
6． """
7． # 补充代码
8． ------------代码如下------------------

===================================================================
5.8 Python 中的 os 模块常见方法？(2018-4-16-lxy)
os.remove()删除文件
os.rename()重命名文件
os.walk()生成目录树下的所有文件名
os.chdir()改变目录
os.mkdir/makedirs 创建目录/多层目录
os.rmdir/removedirs 删除目录/多层目录
os.listdir()列出指定目录的文件
os.getcwd()取得当前工作目录
os.chmod()改变目录权限
os.path.basename()去掉目录路径，返回文件名
os.path.dirname()去掉文件名，返回目录路径
os.path.join()将分离的各部分组合成一个路径名
os.path.split()返回（dirname(),basename())元组
os.path.splitext()(返回 filename,extension)元组
os.path.getatime\ctime\mtime 分别返回最近访问、创建、修改时间
os.path.getsize()返回文件大小
os.path.exists()是否存在
os.path.isabs()是否为绝对路径
os.path.isdir()是否为目录
os.path.isfile()是否为文件
'''


def print_directory_contents(sPath):
    for sChild in os.listdir(sPath):
        sChildPath = os.path.join(sPath, sChild)
        if os.path.isdir(sChildPath):
            print_directory_contents(sChildPath)
        else:
            print(sChildPath)


if __name__ == "__main__":
    # sPath = r'E:\code\python\HeiMa\conda_py3\Anaconda_py3'
    s_path = os.getcwd()

    print_directory_contents(s_path)
    # X = (i for i in range(10))
    # print(type(X))
