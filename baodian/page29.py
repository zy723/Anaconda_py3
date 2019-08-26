#!/usr/bin/env python
# encoding: utf-8
"""
@version: v1.0
@contact: zy723@vip.qq.com
@site: 
@software: PyCharm
@file: page29.py
@time: 2019/8/26 9:43
"""

'''
2.2 range 和 xrange 的区别？(2018-3-30-lxy)
两者用法相同，不同的是 range 返回的结果是一个列表，而 xrange 的结果是一个生成器，前者是
直接开辟一块内存空间来保存列表，后者是边循环边使用，只有使用时才会开辟内存空间，所以当列表
很长时，使用 xrange 性能要比 range 好。
2.3 考虑以下 Python 代码，如果运行结束，命令行中的运行结果是什么？
(2018-3-30-lxy)
1. l = []
2. for i in xrange(10):
3. l.append({‘num’:i})
4. print l
在考虑以下代码，运行结束后的结果是什么？
1. l = []
2. a = {‘num’:0}
3. for i in xrange(10):
4. a[‘num’] = i
5. l.append(a)
6. print l

运算结果:

[{'num': 0}, {'num': 1}, {'num': 2}, {'num': 3}, {'num': 4}, {'num': 5}, {'num': 6}, {'num': 7}, {'num': 8}, {'num': 9}]
****************************************************************************************************
[{'num': 9}, {'num': 9}, {'num': 9}, {'num': 9}, {'num': 9}, {'num': 9}, {'num': 9}, {'num': 9}, {'num': 9}, {'num': 9}]


原因是：字典是可变对象，在下方的 l.append(a)的操作中是把字典 a 的引用传到列表 l 中，当后
续操作修改 a[‘num’]的值的时候，l 中的值也会跟着改变，相当于浅拷贝


'''


def func():
    l = []
    for i in range(10):
        l.append({'num': i})
    print(l)


def func1():
    l = []
    a = {'num': 0}
    for i in range(10):
        a['num'] = i
        l.append(a)
    print(l)


if __name__ == "__main__":
    func()
    print('*' * 100)
    func1()
