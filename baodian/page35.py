#!/usr/bin/env python
# encoding: utf-8
"""
@version: v1.0
@contact: zy723@vip.qq.com
@site: 
@software: PyCharm
@file: page35.py
@time: 2019/8/28 9:06
"""
'''
5.4 Python 里面如何生成随机数？(2018-3-30-lxy)
在 Python 中用于生成随机数的模块是 random，在使用前需要 import. 如下例子可以酌情列
举：
random.random()：生成一个 0-1 之间的随机浮点数；
random.uniform(a, b)：生成[a,b]之间的浮点数；
random.randint(a, b)：生成[a,b]之间的整数；
random.randrange(a, b, step)：在指定的集合[a,b)中，以 step 为基数随机取一个数；
random.choice(sequence)：从特定序列中随机取一个元素，这里的序列可以是字符串，列表，
元组等。

5.5 输入某年某月某日，判断这一天是这一年的第几天？(可以用 Python 标准库)(2018-3-30-lxy)

'''


import random
import datetime

def random_test():
    print(random.random())
    print(random.uniform(1, 10))
    print(random.randint(1, 10))
    print(random.randrange(10, 20, 2))
    print(random.choice('qwqeqqedssdasasdgjhg'))


def day_of_year():
    try:
        year = int(input('请输入年份：'))
        month = int(input('请输入月份：'))
        day = int(input('请输入天：'))
        date1 = datetime.date(year=year, month=month, day=day)
        date2 = datetime.date(year=year, month=1, day=1)
        return (date1 - date2).days + 1
    except TypeError:
        raise('请输入整数')


if __name__ == "__main__":
    # random_test()
    print(day_of_year())
