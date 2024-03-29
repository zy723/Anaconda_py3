#!/usr/bin/env python
# encoding: utf-8
"""
@version: v1.0
@contact: zy723@vip.qq.com
@site: sklearn study
@software: PyCharm
@file: sklearn_day02.py
@time: 2019/8/30 9:42
"""
import os
from sklearn.datasets import load_iris, fetch_20newsgroups, load_boston
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.ensemble import RandomForestClassifier
import pandas as pd


def datasets_test1():
    """
    转换器
    :return:
    """
    li = load_iris()
    # print("获取特征值")
    # print(li.data)
    # print("目标值")
    # print(li.target)
    # print(li.DESCR)

    # 注意返回值 训练集 train x_train, y_train  测试集 test x_test, y_test
    x_train, y_train, x_test, y_test = train_test_split(li.data, li.target, test_size=0.25)
    print("训练集值：", x_train, y_train)
    print("测试集值：", x_test, y_test)


def datasets_test2():
    """
    转换器
    :return:
    """
    news = fetch_20newsgroups(subset='all')
    print(news.data)
    print(news.target)


def datasets_test3():
    """
    转换器
    :return:
    """
    lb = load_boston()
    print('获取特征值')
    print(lb.data)
    print('获取目标值')
    print(lb.target)
    print(lb.DESCR)


def kanncls():
    """
    k-近邻算法
    k- 近邻用户签到预测
    data_url: https://www.kaggle.com/c/facebook-v-predicting-check-ins/data
    :return:
    """
    data_path = os.getcwd() + '/data/train.csv'
    # 读取数据
    data = pd.read_csv(data_path)
    # 处理数据
    # 1、缩小数据查询范围
    data = data.query('x > 1.0 & x < 1.25 & y > 2.5 & y < 2.75')
    # 处理时间数据
    time_value = pd.to_datetime(data['time'], unit='s')
    print(time_value)
    # 把时间格式转换为 字典格式
    time_value = pd.DatetimeIndex(time_value)
    # 构造一些特征数据
    data['day'] = time_value.day
    data['hour'] = time_value.hour
    data['weekday'] = time_value.weekday
    # 删除时间戳
    data = data.drop(['time'], axis=1)
    print(data)
    # 把签到少于3的删除
    place_count = data.groupby('place_id').count()
    tf = place_count[place_count.row_id > 3].reset_index()
    data = data[data['place_id']].isna(tf.place_id)

    # 取出数据值中的特征值与目标值
    y = data['place_id']
    x = data.drop(['place_id'], axis=1)

    # 分割数据
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)

    # 特征工程标准化
    std = StandardScaler()

    # 对特征数据标准化
    x_train = std.fit_transform(x_train)
    x_test = std.transform(x_test)

    # 进行算法流程
    knn = KNeighborsClassifier()

    knn.fit(x_train, y_train)

    # 得出预测结果
    y_predict = knn.predict(x_test)
    print("预测的目标签到位置为：", y_predict)
    # 得出准确率
    print("预测的准确率:", knn.score(x_test, y_test))

    # 构造一些参数的值进行搜索
    param = {"n_neighbors": [3, 5, 10]}

    # 进行网格搜索
    gc = GridSearchCV(knn, param_grid=param, cv=2)

    gc.fit(x_train, y_train)

    # 预测准确率
    print("在测试集上准确率：", gc.score(x_test, y_test))

    print("在交叉验证当中最好的结果：", gc.best_score_)

    print("选择最好的模型是：", gc.best_estimator_)

    print("每个超参数每次交叉验证的结果：", gc.cv_results_)

    return None


def naviebayes():
    """
    朴素贝叶斯 进行文本处理
    :return:
    """
    new = fetch_20newsgroups(subset='all')
    # 进行数据分割
    x_train, x_test, y_train, y_test = train_test_split(new.data, new.target, test_size=0.25)

    # 对数据进行特征抽取
    tf = TfidfVectorizer()

    # 以训练集当中的词列表进行每篇文章的重要性统计
    x_train = tf.fit_transform(x_train)
    print(tf.get_feature_names())
    x_test = tf.transform(x_test)
    # 进行朴素贝叶斯算法的预测
    mlt = MultinomialNB(alpha=1.0)
    print(x_train)
    mlt.fit(x_train, y_train)
    y_predict = mlt.predict(x_test)
    print("预测文章类别为：", y_predict)
    # 得出准确率
    print("准确率为：", mlt.score(x_test, y_test))

    print("每个类别的准确率与召回率：", classification_report(y_test, y_predict, target_names=new.target_names))


def decision():
    """
    决策树对泰坦尼克号进行生死预测
    url: http://biostat.mc.vanderbilt.edu/wiki/pub/Main/DataSets/titanic.txt
    :return:
    """
    titan = pd.read_csv("http://biostat.mc.vanderbilt.edu/wiki/pub/Main/DataSets/titanic.txt")
    # 处理数据，找出特征值和目标值
    x = titan[['pclass', 'age', 'sex']]

    y = titan['survived']

    print(x)
    # 缺失值处理
    x['age'].fillna(x['age'].mean(), inplace=True)

    # 分割数据集到训练集合测试集
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)

    # 进行处理（特征工程）特征-》类别-》one_hot编码
    dict = DictVectorizer(sparse=False)

    x_train = dict.fit_transform(x_train.to_dict(orient="records"))

    print(dict.get_feature_names())

    x_test = dict.transform(x_test.to_dict(orient='records'))


    # print(x_train)
    #
    # # 使用决策树进行预判
    # dec = DecisionTreeClassifier()
    # dec.fit(x_train, y_train)
    #
    # # 预测判断
    # print("预测的准确率:", dec.score(x_test, y_test))
    #
    # # 导出决策树的结构
    # export_graphviz(dec, out_file="tree.dot",
    #                 feature_names=['年龄', 'pclass=1st', 'pclass=2nd', 'pclass=3rd', '女性', '男性'])

    # 随机森林进行预测(超参数调优)
    rf = RandomForestClassifier()
    param = {"n_estimators": [120, 200, 300, 500, 800, 1200], "max_depth": [5, 8, 15, 25, 30]}

    # 网格搜索与交叉验证
    gc = GridSearchCV(rf, param_grid=param, cv=2)

    gc.fit(x_train, y_train)

    print("准确率：", gc.score(x_test, y_test))

    print("查看选择的参数模型：", gc.best_params_)



if __name__ == "__main__":
    # datasets_test1()
    # datasets_test2()
    # datasets_test3()

    # print(os.getcwd())
    # kanncls()
    # naviebayes()
    decision()
