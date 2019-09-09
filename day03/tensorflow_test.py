#!/usr/bin/env python
# encoding: utf-8
"""
@version: v1.0
@contact: zy723@vip.qq.com
@site: 
@software: PyCharm
@file: tensorflow_test.py
@time: 2019/9/5 16:24
"""
import tensorflow as tf
import os


def tensorflow_synchronize_read_data():
    """
    模拟同步读取数据
    :return:
    """
    # 首先定义列队
    Q = tf.FIFOQueue(3, tf.float32)
    # 存入数据
    enq_many = Q.enqueue_many([[0.1, 0.2, 0.3], ])
    # 2、定义一些处理数据的螺距，取数据的过程 取数据，+1， 入队列
    out_q = Q.dequeue()
    data = out_q + 1
    en_q = Q.enqueue(data)
    with tf.Session() as sess:
        # 初始化队列
        sess.run(enq_many)
        # 处理数据
        for i in range(100):
            sess.run(en_q)
        # 训练数据集
        for i in range(Q.size().eval()):
            print(sess.run(Q.dequeue()))


def tensorflow_asynchronous_read_data():
    """
    模拟异步读取数据
    :return:
    """
    # 定义一个列队
    Q = tf.FIFOQueue(1000, tf.float32)

    # 定义需要做的事情:循环自增
    var = tf.Variable(0.0)

    # 实现自增
    data = tf.assign_add(var, tf.constant(1.0))
    en_q = Q.enqueue(data)

    # 3、定义队列管理器op, 指定多少个子线程，子线程该干什么事情
    qr = tf.train.QueueRunner(Q, enqueue_ops=[en_q] * 2)

    # 初始化变量op
    init_op = tf.global_variables_initializer()

    with tf.Session() as sess:
        # 初始化变量
        sess.run(init_op)

        # 开启线程管理器
        coord = tf.train.Coordinator()

        # 开启真正的子线程
        threads = qr.create_threads(sess, coord=coord, start=True)

        # 主线程不断读取并训练数据
        for i in range(300):
            print(sess.run(Q.dequeue()))

        # 回收子进程
        coord.request_stop()

        coord.join(threads)


if __name__ == "__main__":
    # 同步
    # tensorflow_synchronize_read_data()
    # 异步
    tensorflow_asynchronous_read_data()
