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


def mylinear(way=1):
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
    if way == 1:
        # estimator预测
        # 线性回归 正规方程求解方式预测结果
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
    elif way == 2:
        # 梯度下降去进行房价预测
        sgd = SGDRegressor()
        sgd.fit(x_train, y_train)
        print(sgd.coef_)
        # 预测测试集合的房子价格
        y_sgd_predict = std_y.inverse_transform(sgd.predict(x_test))
        print("梯度下降测试集里面每个房子的预测价格：", y_sgd_predict)
        print("正规方程的均方误差:", mean_squared_error(std_y.inverse_transform(y_test), y_sgd_predict))
    elif way == 3:
        # 岭回归去进行房价预测
        rd = Ridge(alpha=1.0)
        rd.fit(x_train, y_train)
        print(rd.coef_)
        # 预测测试集的房子价格
        y_rd_predict = std_y.inverse_transform(rd.predict(x_test))
        print("梯度下降测试集里面每个房子的预测价格：", y_rd_predict)
        print("正规方程的均方误差:", mean_squared_error(std_y.inverse_transform(y_test), y_rd_predict))


def logistic():
    """
    逻辑回归做二分类进行癌症预测(根据细胞的属性特征)
    :return: None
    """
    # 构造列标签名字
    column = ['Sample code number', 'Clump Thickness', 'Uniformity of Cell Size', 'Uniformity of Cell Shape',
              'Marginal Adhesion', 'Single Epithelial Cell Size', 'Bare Nuclei', 'Bland Chromatin', 'Normal Nucleoli',
              'Mitoses', 'Class']

    # data = pd.read_csv(
    #     "https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/breast-cancer-wisconsin.data",
    #     names=column)
    data = pd.read_csv(
        os.getcwd() + r"\data\breast-cancer-wisconsin.data",
        names=column)

    # 处理缺失值
    data = data.replace(to_replace='?', value=np.nan)
    data = data.dropna()

    # 对数据进行分割
    x_train, x_test, y_train, y_test = train_test_split(data[column[1:10]], data[column[10]], test_size=0.25)

    # 对数据进行标准化
    std = StandardScaler()
    x_train = std.fit_transform(x_train)
    x_test = std.transform(x_test)

    # 逻辑回归预测
    lg = LogisticRegression(C=1.0)
    lg.fit(x_train, y_train)
    print(lg.coef_)
    y_predict = lg.predict(x_test)

    print("准确率:", lg.score(x_test, y_test))
    print("召回率:", classification_report(y_test, y_predict, labels=[2, 4], target_names=["良性", "恶性"]))


if __name__ == "__main__":
    # mylinear()
    logistic()
