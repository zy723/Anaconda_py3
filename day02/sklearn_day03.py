#!/usr/bin/env python
# encoding: utf-8
"""
@version: v1.0
@contact: zy723@vip.qq.com
@site: 
@software: PyCharm
@file: sklearn_day03.py
@time: 2019/9/4 15:04
"""
from sklearn.datasets import load_boston
from sklearn.linear_model import LinearRegression, SGDRegressor, Ridge, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, classification_report
from sklearn.externals import joblib
import numpy as np
import pandas as pd
import os


def mylinear():
    """
    线性回归 直接预测房价
    :return:
    """
    # 获取数据
    lb = load_boston()
    # 分割数据到测试集与训练集
    x_train, x_test, y_train, y_test = train_test_split(lb.data, lb.target, test_size=0.25)
    print(y_train, y_test)
    # 进行标准化处理 目标处理
    # 特征值与目标值必须标准化处理，实例化两个标准化API
    std_x = StandardScaler()

    x_train = std_x.fit_transform(x_train)
    x_test = std_x.transform(x_test)

    # 目标值
    std_y = StandardScaler()
    y_train = std_y.fit_transform(y_train.reshape(1, -1))
    y_test = std_y.transform(y_test.reshape(-1, 1))

    # estimator预测
    # 正规方程求解方式预测结果
    lr = LinearRegression()
    lr.fit(x_train, y_train)
    print(lr.coef_)
    # 保存训练模型
    joblib.dump(lr, os.getcwd() + r"\data\test.pkl")

    # 预测房价测试集合
    y_lr_predict = std_y.inverse_transform(lr.predict(x_test))
    print("正规方程测试集里面每个房子的预测价格: ", y_lr_predict)
    # 正规方程的均方误差
    print("正规方程的均方误差:", mean_squared_error(std_y.inverse_transform(y_test), y_lr_predict))


if __name__ == "__main__":
    mylinear()
