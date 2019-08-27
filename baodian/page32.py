#!/usr/bin/env python
# encoding: utf-8
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

'''

import os


def print_directory_contents(sPath):
    for sChild in os.listdir(sPath):
        sChildPath = os.path.join(sPath, sChild)
        if os.path.isdir(sChildPath):
            print_directory_contents(sChildPath)
        else:
            print(sChildPath)


if __name__ == "__main__":
    sPath = r'E:\code\python\HeiMa\conda_py3\Anaconda_py3'
    print_directory_contents(sPath)
