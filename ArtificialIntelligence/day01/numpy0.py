#!/usr/bin/env python
# encoding: utf-8
"""
@version: v1.0
@contact: zy723@vip.qq.com
@site: 
@software: PyCharm
@file: numpy0.py
@time: 2019/8/21 16:49
"""

from matplotlib import pyplot as plt


def test():
    x = range(2, 26, 2)
    y = [15, 13, 14.5, 17, 20, 25, 26, 26, 27, 22, 18, 15]
    # 设置图片大小
    plt.figure(figsize=(20, 8), dpi=80)
    # 绘图
    plt.plot(x, y)
    # 设置X轴的刻度
    _xtick_labels = [i / 2 for i in range(4, 49)]
    plt.xticks(range(25, 50))
    plt.yticks(range(min(y), max(y) + 1))
    plt.savefig("./t1.png")
    plt.show()


if __name__ == "__main__":
    test()
