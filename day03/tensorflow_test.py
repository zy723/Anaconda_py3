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
import time


class TensorFlowReadDataTest(object):
    def __init__(self):
        pass

    def synchronize_read_data(self):
        """
        模拟同步读取数据
        :return:
        """
        # 首先定义列队
        t0 = time.time_ns()
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
        t1 = time.time_ns()
        print("同步耗时%d ns" % (t1 - t0))

    def asynchronous_read_data(self):
        """
        模拟异步读取数据
        :return:
        """
        # 定义一个列队
        t0 = time.time_ns()
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

        t1 = time.time_ns()
        print("异步耗时%d ns" % (t1 - t0))

    def run(self):
        self.synchronize_read_data()
        self.asynchronous_read_data()


class ReadData(object):
    """
    读取各类文件 测试集合 csv,picture,bin
    """

    def __init__(self):
        self.csvFiles = [os.path.join(os.getcwd() + r"\data\csv", file) for file in
                         os.listdir(os.getcwd() + r"\data\csv")]

        self.picFiles = [os.path.join(os.getcwd() + r"\data\pic", file) for file in
                         os.listdir(os.getcwd() + r"\data\pic")]

    def csv_read_file(self):
        # 读取csv类型文件

        # 构造文件文件队列
        print(self.csvFiles)
        file_queue = tf.train.string_input_producer(self.csvFiles)
        # 构造csv阅读器一行行读取数据
        reader = tf.TextLineReader()
        key, value = reader.read(file_queue)

        # 对每行读取的数据进行解码
        records = [["None"], ["None"]]
        example, label = tf.decode_csv(value, record_defaults=records)

        # 批量处理读取多个数据
        example_batch, label_batch = tf.train.batch([example, label], batch_size=9, num_threads=1, capacity=9)

        print(example_batch, label_batch)

    def pic_read_file(self):
        # 读取图片数据并转换为张量
        print(self.picFiles)
        # 构造文件对列表
        file_queue = tf.train.string_input_producer(self.picFiles)
        # 构造阅读器, 默认每次读取一张图片
        reader = tf.WholeFileReader()
        key, values = reader.read(file_queue)
        print(values)

        # 对读取的图片进行解码
        image = tf.image.decode_gif(values)
        print(image)

        # 处理所有图片为同一大小
        image_resize = tf.image.resize_images(image, [200, 200])
        print(image_resize)

        # 固定3维图片的形状
        image_resize.set_shape([200, 200, 200, 3])
        print(image_resize)

        # 进行批量处理

        image_batch = tf.train.batch([image_resize], batch_size=20, num_threads=1, capacity=20)

        print(image_batch)

    def run(self):
        # self.csv_read_file()
        self.pic_read_file()


if __name__ == "__main__":
    # tfrd = TensorFlowReadDataTest()
    # tfrd.run()

    # tf read data
    tfrd = ReadData()
    tfrd.run()
