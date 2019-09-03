#!/usr/bin/env python
# encoding: utf-8
"""
@version: v1.0
@contact: zy723@vip.qq.com
@site: 
@software: PyCharm
@file: page82.py
@time: 2019/9/3 9:27
"""
"""
1. 进程总结
进程：程序运行在操作系统上的一个实例，就称之为进程。进程需要相应的系统资源：内存、时间
片、pid。
创建进程：
1.首先要导入 multiprocessing 中的 Process；
2.创建一个 Process 对象；
3.创建 Process 对象时，可以传递参数；
1．p = Process(target=XXX, args=(元组,) , kwargs={key:value})
2．target = XXX 指定的任务函数,不用加()
3．args=(元组,) , kwargs={key:value} 给任务函数传递的参数
4.使用 start()启动进程；
5.结束进程。
Process 语法结构：
Process([group [, target [, name [, args [, kwargs]]]]])
target：如果传递了函数的引用，可以让这个子进程就执行函数中的代码
args：给 target 指定的函数传递的参数，以元组的形式进行传递
kwargs：给 target 指定的函数传递参数，以字典的形式进行传递
name：给进程设定一个名字，可以省略
group：指定进程组，大多数情况下用不到
Process 创建的实例对象的常用方法有：
start()：启动子进程实例(创建子进程)
is_alive()：判断进程子进程是否还在活着
join(timeout)：是否等待子进程执行结束，或者等待多少秒
terminate()：不管任务是否完成，立即终止子进程
Process 创建的实例对象的常用属性：
name：当前进程的别名，默认为 Process-N,N 为从 1 开始递增的整数
pid：当前进程的 pid(进程号)

"""

import os
import time
from multiprocessing import Process



def pro_func(name, age, **kwargs):
    for i in range(5):
        print("子程序正在运行中，name=%s, age=%d, pid=%d" % (name, age, os.getpid()))
        print(kwargs)
        time.sleep(0.02)


def start_process():
    # 创建process对象
    p = Process(target=pro_func, args=('xiaoming', 18), kwargs={'m': 20})
    # 启动进程
    p.start()
    time.sleep(1)
    # 等待1秒后结束子进程
    p.terminate()
    p.join()


if __name__ == "__main__":
    start_process()
