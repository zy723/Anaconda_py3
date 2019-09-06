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


def tensorflow_test():
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


if __name__ == "__main__":
    tensorflow_test()
