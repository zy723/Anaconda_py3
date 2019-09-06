#!/usr/bin/env python
# encoding: utf-8
"""
@version: v1.0
@contact: zy723@vip.qq.com
@site: 
@software: PyCharm
@file: page87.py
@time: 2019/9/6 8:53
"""
import socket
from multiprocessing import Process


class UdpSocket(object):
    """
    udp test

    """

    def __init__(self):
        pass

    def udp_user_client(self):
        # 创建UDP套接字
        # socket.AF_INET 表示IPV4 地址, AF_INET6 表示IPV6地址
        # socket.SOCK_DGRAM 数据报套接字，用于UDP传输

        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 声明socket类型，同时生成链接对象
        client.connect(('localhost', 6999))  # 建立一个链接，连接到本地的6969端口
        while True:
            # addr = client.accept()
            # print '连接地址：', addr
            msg = '我是客服端！'  # strip默认取出字符串的头尾空格
            client.send(msg.encode('utf-8'))  # 发送一条信息 python3 只接收btye流
            data = client.recv(1024)  # 接收一个信息，并指定接收的大小 为1024字节
            print('recv:', data.decode())  # 输出我接收的信息

        # client.close()

    def udp_user_server(self):
        # 创建套接字
        # socket.INET 表示IPV4 socket.INET6 表示ipv6
        # socket.SOCK_DGRAM 数据套接字 只用于UDP
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.bind(('localhost', 6999))  # 绑定要监听的端口
        server.listen(5)  # 开始监听 表示可以使用五个链接排队
        while True:  # conn就是客户端链接过来而在服务端为期生成的一个链接实例
            conn, addr = server.accept()  # 等待链接,多个链接的时候就会出现问题,其实返回了两个值
            print(conn, addr)
            while True:
                try:
                    data = conn.recv(1024)  # 接收数据
                    print('recive:', data.decode())  # 打印接收到的数据
                    conn.send(data.upper())  # 然后再发送数据
                except ConnectionResetError as e:
                    print('关闭了正在占线的链接！')
                    break
            conn.close()

    def run(self):
        pserver = Process(target=self.udp_user_server)
        pclient = Process(target=self.udp_user_client)
        pserver.start()
        pclient.start()
        pclient.join()
        pserver.join()
        pserver.close()
        pclient.close()


class TcpSocket(object):
    """
    TCP test
    """
    def __init__(self):
        pass

    def tcp_server_socket(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('localhost', 9090))  # 绑定要监听的端口
        server.listen(5)  # 开始监听 表示可以使用五个链接排队
        while True:  # conn就是客户端链接过来而在服务端为期生成的一个链接实例
            conn, addr = server.accept()  # 等待链接,多个链接的时候就会出现问题,其实返回了两个值
            print(conn, addr)
            while True:
                data = conn.recv(1024)  # 接收数据
                print('recive:', data.decode())  # 打印接收到的数据
                conn.send(data.upper())  # 然后再发送数据
            conn.close()

    def tcp_client_socket(self):

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 声明socket类型，同时生成链接对象
        client.connect(('localhost', 9090))  # 建立一个链接，连接到本地的6969端口
        while True:
            # addr = client.accept()
            # print '连接地址：', addr
            msg = 'TCP client test！'  # strip默认取出字符串的头尾空格
            client.send(msg.encode('utf-8'))  # 发送一条信息 python3 只接收btye流
            data = client.recv(1024)  # 接收一个信息，并指定接收的大小 为1024字节
            print('recv:', data.decode())  # 输出我接收的信息
        client.close()  # 关闭这个链接

    def run(self):
        pserver = Process(target=self.tcp_server_socket)
        pclient = Process(target=self.tcp_client_socket)
        pserver.start()
        pclient.start()
        pclient.join()
        pserver.join()
        pserver.close()
        pclient.close()


if __name__ == "__main__":
    udpTest = UdpSocket()
    udpTest.run()
    # tcpTest = TcpSocket()
    # tcpTest.run()



