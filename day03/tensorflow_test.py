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
    读取各类文件 测试集合 csv,picture
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


class CifarRead(object):
    """
    对二进制的读写操作

    """

    def __init__(self):
        self.fileList = [os.path.join(os.getcwd() + r'\data\bin', file) for file in
                         os.listdir(os.getcwd() + r'\data\bin') if file[-3:] == 'bin']

        self.savePath = os.getcwd() + r'\data\bin\path'
        # 每张图片的属性
        self.height = 32
        self.width = 32
        self.channel = 3
        # 二进制文件每张图片的字节
        self.label_bytes = 1
        self.image_bytes = self.height * self.width * self.channel
        self.bytes = self.label_bytes + self.image_bytes

    def read_and_decode(self):
        """
        读取本地文件并解码
        :return: None
        """
        # 构造文件队列
        file_queue = tf.train.string_input_producer(self.fileList)
        # 构造二进制读取器
        reader = tf.FixedLengthRecordReader(self.bytes)
        key, value = reader.read(file_queue)

        # 解码内容，二进制文件内容解码
        lable_image = tf.decode_raw(value, tf.uint8)
        print(lable_image)

        # 分割导出图片和标签数据，切除特征值和目标值
        lable = tf.cast(tf.slice(lable_image, [0], [self.label_bytes]), tf.int32)
        image = tf.slice(lable_image, [self.label_bytes], [self.image_bytes])

        # 对图片特征值进行改变
        image_reshape = tf.reshape(image, [self.height, self.width, self.channel])
        print(image_reshape, lable)

        # 批量处理数据
        image_batch, lable_batch = tf.train.batch([image_reshape, lable], batch_size=10, num_threads=1, capacity=10)
        print(image_batch, lable_batch)

        return image_batch, lable_batch

    def write_ro_tfrecords(self, image_batch, label_batch):
        """
        将图片的特征值进行存储
        :param image_batch: 图片的特征值
        :param label_batch: 图片的目标值
        :return: None
        """
        # 建立 TFRcord 储存器
        writer = tf.python_io.TFRecordWriter(self.savePath)

        # 将每张图循环写出到文件 按example协议存储
        for i in range(10):
            # 分别取出第i个图片数据的特征值与目标值
            image = image_batch[i].eval().tostring()
            lable = int(label_batch[i].eval()[0])

            # 构造example 数据
            example = tf.train.Example(
                features=tf.train.Features(
                    feature={
                        "image": tf.train.Feature(bytes_list=tf.train.BytesList(value=[image])),
                        "lable": tf.train.Feature(int64_list=tf.train.Int64List(value=[lable]))
                    }
                )
            )

            # 写出单独的样本
            writer.write(example.SerializeToString())

    def read_from_tfrecords(self):
        """
        读取数据 example 格式数据读取
        :return:None
        """
        file_queue = tf.train.string_input_producer(self.savePath)

        # 构造阅读器
        reader = tf.TFRecordReader()
        key, value = reader.read(file_queue)

        # 解析example 数据
        features = tf.parse_single_example(
            value,
            features={
                "image": tf.FixedLenFeature([], tf.string),
                "lable": tf.FixedLenFeature([], tf.int64)
            }
        )

        # 解码读取的内容
        image = tf.decode_raw(features["image"], tf.int8)

        # 固定图片形状，方便下面处理
        image_reshpe = tf.reshape(image, [self.height, self.width, self.channel])
        lable = tf.cast(features["lable"], tf.int32)
        print(image_reshpe, lable)

        # 进行批量处理
        image_batch, lable_batch = tf.train.batch([image_reshpe, lable], batch_size=10, num_threads=1, capacity=10)

        return image_batch, lable_batch

    def run(self):
        """
        测试方法
        :return: None
        """
        if os.listdir(self.savePath):
            image_batch, lable_batch = self.read_from_tfrecords()
        else:
            image_batch, lable_batch = self.read_and_decode()

        with tf.Session() as sess:
            # 定义一个线程协助器
            coord = tf.train.Coordinator()

            # 开启读取文件线程
            threads = tf.train.start_queue_runners(sess, coord=coord)

            # 开启存储
            self.write_ro_tfrecords(image_batch, lable_batch)

            # 打印读取的内容
            print(sess.run([image_batch, lable_batch]))
            # 回收子线程
            coord.request_stop()
            coord.join(threads)


if __name__ == "__main__":
    # tfrd = TensorFlowReadDataTest()
    # tfrd.run()

    # tf read data
    tfrd = ReadData()
    tfrd.run()
