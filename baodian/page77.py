#!/usr/bin/env python
# encoding: utf-8
"""
@version: v1.0
@contact: zy723@vip.qq.com
@site: 
@software: PyCharm
@file: page77.py
@time: 2019/9/2 9:06
"""
"""
4.3 请尝试用 “一行代码” 实现将 1-N 的整数列表以 3 为单位分组， 比如 1-100分组后为? (2018-4-20-lxy)

4.4 Python 中 yield 的用法？(2018-4-16-lxy)
yield 就是保存当前程序执行状态。你用 for 循环的时候，每次取一个元素的时候就会计算一次。用 yield 的函数
叫 generator， 和 iterator 一样， 它的好处是不用一次计算所有元素， 而是用一次算一次， 可以节省很多空间。 generator
每次计算需要上一次计算结果，所以用 yield，否则一 return，上次计算结果就没了。

"""


def demo4_3():
    # print([[x for x in range(1, 100)][i:i+3] for i in range(0, len(list_a), 3)])
    print([[x for x in range(1, 100)]])


if __name__ == "__main__":
    demo4_3()
