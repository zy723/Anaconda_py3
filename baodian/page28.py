#!/usr/bin/env python
# encoding: utf-8
"""
@version: v1.0
@contact: zy723@vip.qq.com
@site: 
@software: PyCharm
@file: page28.py
@time: 2019/8/26 9:13
"""

'''
2.1 阅读下面的代码，写出 A0，A1 至 An 的最终值。(2018-3-30-lxy)
1. A0 = dict(zip(('a'，'b'，'c'，'d'，'e')，(1，2，3，4，5)))
2. A1 = range(10)
3. A2 = [i for i in A1 if i in A0]
4. A3 = [A0[s] for s in A0]
5. A4 = [i for i in A1 if i in A3]
6. A5 = {i:i*i for i in A1}
7. A6 = [[i，i*i] for i in A1]

计算结果:
A0 = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
A1 = range(0, 10) = [0,1,2,3,4,5,6,7,8,9]
A2 = []
A3 = [1, 2, 3, 4, 5]
A4 = [1, 2, 3, 4, 5]
A5 = {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25, 6: 36, 7: 49, 8: 64, 9: 81}
A6 = [[0, 0], [1, 1], [2, 4], [3, 9], [4, 16], [5, 25], [6, 36], [7, 49], [8, 64], [9, 81]]

'''


def func():
    A0 = dict(zip(('a', 'b', 'c', 'd', 'e'), (1, 2, 3, 4, 5)))
    print(A0)
    A1 = range(10)
    print(A1)
    A2 = [i for i in A1 if i in A0]
    print(A2)
    A3 = [A0[s] for s in A0]
    print(A3)
    A4 = [i for i in A1 if i in A3]
    print(A4)
    A5 = {i: i * i for i in A1}
    print(A5)
    A6 = [[i, i * i] for i in A1]
    print(A6)
    print('*'*100)


if __name__ == "__main__":
    func()
