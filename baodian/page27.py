#!/usr/bin/env python
# encoding: utf-8
"""
@version: v1.0
@contact: zy723@vip.qq.com
@site: 
@software: PyCharm
@file: page27.py
@time: 2019/8/26 9:03
"""


class Parent(object):
    x = 1


class Child1(Parent):
    pass


class Child2(Parent):
    pass


if __name__ == "__main__":
    print(Parent.x, Child1.x, Child2.x)
    Child1.x = 2
    print(Parent.x, Child1.x, Child2.x)
    Parent.x = 3
    print(Parent.x, Child1.x, Child2.x)


'''
    运算结果:
    1 1 1 #继承自父类的类属性 x，所以都一样，指向同一块内存地址。
    1 2 1 #更改 Child1，Child1 的 x 指向了新的内存地址。
    3 2 3 #更改 Parent，Parent 的 x 指向了新的内存地址

'''