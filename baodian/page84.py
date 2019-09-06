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

"""
    2. 谈谈你对多进程，多线程，以及协程的理解，项目是否用？(2018-3-30-lxy)
        这个问题被问的概率相当之大，其实多线程，多进程，在实际开发中用到的很少，除非是那些对项
    目性能要求特别高的，有的开发工作几年了，也确实没用过，你可以这么回答，给他扯扯什么是进程，
    线程（cpython 中是伪多线程）的概念就行，实在不行你就说你之前写过下载文件时，用过多线程技术，
    或者业余时间用过多线程写爬虫，提升效率。
        进程：一个运行的程序（代码）就是一个进程，没有运行的代码叫程序，进程是系统资源分配的最
    小单位，进程拥有自己独立的内存空间，所以进程间数据不共享，开销大。
    线程： 调度执行的最小单位，也叫执行路径，不能独立存在，依赖进程存在一个进程至少有一个
        线程，叫主线程，而多个线程共享内存(数据共享，共享全局变量)，从而极大地提高了程序的运行效率。
        协程：是一种用户态的轻量级线程，协程的调度完全由用户控制。协程拥有自己的寄存器上下文和
    栈。 协程调度切换时，将寄存器上下文和栈保存到其他地方，在切回来的时候，恢复先前保存的寄存
    器上下文和栈，直接操作栈则基本没有内核切换的开销，可以不加锁的访问全局变量，所以上下文的切
    换非常快

    3. 什么是多线程竞争？(2018-3-30-lxy)
        线程是非独立的， 同一个进程里线程是数据共享的， 当各个线程访问数据资源时会出现竞争状态即：
    数据几乎同步会被多个线程占用，造成数据混乱 ，即所谓的线程不安全
    那么怎么解决多线程竞争问题？-- 锁。
    锁的好处：
        确保了某段关键代码(共享数据资源)只能由一个线程从头到尾完整地执行能解决多线程资源竞争下
    的原子操作问题。
    锁的坏处：
        阻止了多线程并发执行，包含锁的某段代码实际上只能以单线程模式执行，效率就大大地下降了
    锁的致命问题：死锁。

    4. 解释一下什么是锁，有哪几种锁? (2018-3-30-lxy)
        锁(Lock)是 Python 提供的对线程控制的对象。有互斥锁、可重入锁、死锁。

    5. 什么是死锁呢？(2018-3-30-lxy)
        若干子线程在系统资源竞争时，都在等待对方对某部分资源解除占用状态，结果是谁也不愿先解锁，
    互相干等着，程序无法执行下去，这就是死锁。
    GIL 锁（有时候，面试官不问，你自己要主动说，增加 b 格，尽量别一问一答的尬聊，不然最后等
    到的一句话就是：你还有什么想问的么？）
    GIL 锁 全局解释器锁（只在 cpython 里才有）
    作用：限制多线程同时执行，保证同一时间只有一个线程执行，所以 cpython 里的多线程其实是伪
    多线程!
        所以 Python 里常常使用协程技术来代替多线程，协程是一种更轻量级的线程，
    进程和线程的切换时由系统决定，而协程由我们程序员自己决定，而模块 gevent 下切换是遇到了
    耗时操作才会切换。
        三者的关系：进程里有线程，线程里有协程。

    6. 什么是线程安全，什么是互斥锁？(2018-3-30-lxy)
        每个对象都对应于一个可称为" 互斥锁" 的标记，这个标记用来保证在任一时刻，只能有一个线程
    访问该对象。
        同一个进程中的多线程之间是共享系统资源的，多个线程同时对一个对象进行操作，一个线程操作
    尚未结束，另一个线程已经对其进行操作，导致最终结果出现错误，此时需要对被操作对象添加互斥锁，
    保证每个线程对该对象的操作都得到正确的结果。

    7. 说说下面几个概念：同步，异步，阻塞，非阻塞?(2018-3-30-lxy)
        同步：多个任务之间有先后顺序执行，一个执行完下个才能执行。
        异步：多个任务之间没有先后顺序，可以同时执行有时候一个任务可能要在必要的时候获取另一个
    同时执行的任务的结果，这个就叫回调！
        阻塞：如果卡住了调用者，调用者不能继续往下执行，就是说调用者阻塞了。
        非阻塞：如果不会卡住，可以继续执行，就是说非阻塞的。
        同步异步相对于多任务而言，阻塞非阻塞相对于代码执行而言。

    8. 什么是僵尸进程和孤儿进程？怎么避免僵尸进程? (2018-3-30-lxy)
        孤儿进程：父进程退出，子进程还在运行的这些子进程都是孤儿进程，孤儿进程将被 init 进程(进
    程号为 1)所收养，并由 init 进程对它们完成状态收集工作。
        僵尸进程： 进程使用 fork 创建子进程， 如果子进程退出， 而父进程并没有调用 wait 或 waitpid 获
    取子进程的状态信息，那么子进程的进程描述符仍然保存在系统中的这些进程是僵尸进程。
    避免僵尸进程的方法：
    1.fork 两次用孙子进程去完成子进程的任务；
    2.用 wait()函数使父进程阻塞；
    3.使用信号量，在 signal handler 中调用 waitpid，这样父进程不用阻塞。

    9. Python 中的进程与线程的使用场景? (2018-3-30-lxy)
    多进程适合在 CPU 密集型操作(cpu 操作指令比较多，如位数多的浮点运算)。
    多线程适合在 IO 密集型操作(读写数据操作较多的，比如爬虫)。

    10.线程是并发还是并行，进程是并发还是并行？(2018-3-30-lxy)
    线程是并发，进程是并行；
    进程之间相互独立，是系统分配资源的最小单位，同一个线程中的所有线程共享资源。

    11.并行（parallel）和并发（concurrency）？(2018-3-30-lxy)
    并行：同一时刻多个任务同时在运行。
    并发：在同一时间间隔内多个任务都在运行，但是并不会在同一时刻同时运行，存在交替执行的情况
    实现并行的库有：multiprocessing
    实现并发的库有：threading
    程序需要执行较多的读写、请求和回复任务的需要大量的 IO 操作，IO 密集型操作使用并发更好。
    CPU 运算量大的程序程序，使用并行会更好。

    12.IO 密集型和 CPU 密集型区别？(2018-4-16-lxy)
    IO 密集型：系统运作，大部分的状况是 CPU 在等 I/O (硬盘/内存)的读/写。
    CPU 密集型：大部份时间用来做计算、逻辑判断等 CPU 动作的程序称之 CPU 密集型。


"""

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
