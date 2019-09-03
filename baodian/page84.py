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

"""
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

def func():
    pass


if __name__ == "__main__":
    func()

 