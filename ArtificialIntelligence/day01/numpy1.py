#!/usr/bin/env python
# encoding: utf-8
"""
@version: v1.0
@contact: zy723@vip.qq.com
@site: 
@software: PyCharm
@file: numpy1.py
@time: 2019/8/22 9:44
"""
from matplotlib import pyplot as plt, font_manager
import random
import matplotlib


def test1():
    # 设置字体
    # font = {
    #     'family': 'MicroSoft YaHei',
    #     'weight': 'bold',
    #     'size': 'larger',
    # }
    # matplotlib.rc("font", **font)
    matplotlib.rc("font", family='MicroSoft YaHei', weight="bold")
    x = range(0, 120)
    y = [random.randint(20, 35) for i in range(120)]
    plt.figure(figsize=(20, 8), dpi=80)
    plt.plot(x, y)
    # 调整X轴与Y轴刻度
    _xtick_labels = ["10点{}分".format(i) for i in range(60)]
    _xtick_labels += ["11点{}分".format(i) for i in range(60)]
    # _ytick_lable = ['11点{}分'.format(i) for i in range(60)]
    plt.xticks(list(x)[::3], _xtick_labels[::3], rotation=45)
    # 添加描述信息
    plt.xlabel("时间")
    plt.ylabel("温度 单位(C)")
    plt.title("10点到12点之间每分钟温度变化")
    plt.show()


def test2():
    matplotlib.rc("font", family='MicroSoft YaHei', weight="bold")
    y = [1, 0, 1, 1, 2, 4, 3, 2, 3, 4, 4, 5, 6, 5, 4, 3, 3, 1, 1, 1]
    x = range(11, 31)

    # 设置图形大小
    plt.figure(figsize=(20, 8), dpi=80)

    plt.plot(x, y)

    # 设置x轴刻度
    _xtick_labels = ["{}岁".format(i) for i in x]
    plt.xticks(x, _xtick_labels)
    plt.yticks(range(0, 9))

    # 绘制网格
    plt.grid(alpha=0.1)

    # 展示
    plt.show()


def test3():
    matplotlib.rc("font", family='MicroSoft YaHei', weight="bold")
    y_1 = [1, 0, 1, 1, 2, 4, 3, 2, 3, 4, 4, 5, 6, 5, 4, 3, 3, 1, 1, 1]
    y_2 = [1, 0, 3, 1, 2, 2, 3, 3, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    x = range(11, 31)

    # 设置图形大小
    plt.figure(figsize=(20, 8), dpi=80)

    plt.plot(x, y_1, label="自己", color="#F08080")
    plt.plot(x, y_2, label="同桌", color="#DB7093", linestyle="--")

    # 设置x轴刻度
    _xtick_labels = ["{}岁".format(i) for i in x]
    # plt.xticks(x, _xtick_labels, fontproperties=my_font)
    plt.xticks(x, _xtick_labels)
    # plt.yticks(range(0,9))

    # 绘制网格
    plt.grid(alpha=0.4, linestyle=':')

    # 添加图例
    # plt.legend(prop=my_font, loc="upper left")
    plt.legend(loc="upper left")

    # 展示
    plt.show()


if __name__ == "__main__":
    # test1()
    # test2()
    test3()
