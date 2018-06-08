# -*- coding=utf-8 -*-

import socket
import sys

def socket_client():
              try:
                            #创建socket
                            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                            #与服务器建立连接
                            s.connect(('192.168.17.131',6666))
              #检错
              except socket.error as msg:
                            print 'msg'
                            sys.exit(1)
              #接收服务端欢迎消息
              print s.recv(1024)
              #无限循环发送数据，直至发送‘exit’结束
              while 1:
                            data = raw_input('what do you want to send: ')
                            s.send(data)
                            print s.recv(1024)
                            if data == 'exit':
                                          break
              s.close()

if __name__ == '__main__':
              socket_client()
