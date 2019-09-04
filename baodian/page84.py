#!/usr/bin/env python
# encoding: utf-8
"""
@version: v1.0
@contact: zy723@vip.qq.com
@site: 
@software: PyCharm
@file: page84.py
@time: 2019/9/3 9:55
"""
from multiprocessing import Process, Queue, Pool
import os
import time
import random


class QueueCommunication(object):
    """
    进程间通信 Demo

    进程之间的通信-Queue
    在初始化 Queue()对象时，(例如 q=Queue()，若在括号中没有指定最大可接受的消息数量，或数
    量为负值时，那么就代表可接受的消息数量没有上限-直到内存的尽头)
    Queue.qsize()：返回当前队列包含的消息数量。
    Queue.empty()：如果队列为空，返回 True,反之 False。
    Queue.full()：如果队列满了，返回 True，反之 False。
    Queue.get([block[,timeout]])：获取队列中的一条消息，然后将其从队列中移除，block 默认值为
    True。
    如果 block 使用默认值，且没有设置 timeout（单位秒），消息列队如果为空，此时程序将被阻塞
    （停在读取状态），直到从消息列队读到消息为止，如果设置了 timeout，则会等待 timeout 秒，若还
    没读取到任何消息，则抛出"Queue.Empty"异常；
    如果 block 值为 False，消息列队如果为空，则会立刻抛出"Queue.Empty"异常；
    Queue.get_nowait()：相当 Queue.get(False)；
    Queue.put(item,[block[, timeout]])：将 item 消息写入队列，block 默认值为 True；
    如果 block 使用默认值，且没有设置 timeout（单位秒），消息列队如果已经没有空间可写入，此
    时程序将被阻塞（停在写入状态），直到从消息列队腾出空间为止，如果设置了 timeout，则会等待
    timeout 秒，若还没空间，则抛出"Queue.Full"异常；
    如果 block 值为 False，消息列队如果没有空间可写入，则会立刻抛出"Queue.Full"异常；
    Queue.put_nowait(item)：相当 Queue.put(item, False)；
    进程间通信 Demo：
    """

    def __init__(self):
        self.q = Queue()

    def write(self):
        for value in ['A', 'B', 'C']:
            print('Put %s to queue...' % value)
            self.q.put(value)
            time.sleep(random.random())

    def read(self):
        while True:
            if not self.q.empty():
                value = self.q.get(True)
                print('Get %s from queue' % value)
                time.sleep(random.random())
            else:
                break

    def run(self):
        pw = Process(target=self.write)
        pr = Process(target=self.read)
        # 启动子进程pw 写入数据
        pw.start()
        # 等待 pw 结束
        pw.join()
        # 启动 pr 读取数据
        pr.start()
        pr.join()
        # 等待结果全执行完毕
        print("所有数据全读写完毕")


class PoolsWorker(object):
    """
    线程池Demo

    multiprocessing.Pool 常用函数解析：
     apply_async(func[, args[, kwds]]) ：使用非阻塞方式调用 func（并行执行，堵塞方式必须等待
    上一个进程退出才能执行下一个进程），args 为传递给 func 的参数列表，kwds 为传递给 func
    的关键字参数列表；
     close()：关闭 Pool，使其不再接受新的任务；
     terminate()：不管任务是否完成，立即终止；
     join()：主进程阻塞，等待子进程的退出， 必须在 close 或 terminate 之后使用；
    进程池中使用 Queue
    如果要使用 Pool 创建进程，就需要使用 multiprocessing.Manager()中的 Queue()，而不是
    multiprocessing.Queue()，否则会得到一条如下的错误信息：
    RuntimeError: Queue objects should only be shared between processes through
    inheritance.

    """

    def __init__(self):
        pass

    def worker(self, msg):
        t_start = time.time()
        print("%s 开始执行, 进程号为：%d" % (msg, os.getpid()))
        time.sleep(random.random(1, 2))
        t_stop = time.time()
        print(msg, '执行完毕, 耗时 %0.2f' % (t_start - t_stop))

    def run(self):
        # 定义一个线程池, 最大进程数为 5
        po = Pool(3)

        for i in range(0, 10):
            # Pool().apply_async(要调用的目标,(传递给目标的参数元祖,))
            # 每次循环将会用空闲出来的子进程去调用目标
            po.apply_async(self.worker, (i,))

        print("----start----")
        # 关闭进程池
        po.close()
        # 等待线程池中的其他进程结束
        po.join()
        print("-------end------")


if __name__ == "__main__":
    # 进程池
    # qc = QueueCommunication()
    # qc.run()
    # 线程池
    pw = PoolsWorker()
    pw.run()
