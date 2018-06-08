#!/user/bin/env python
# -*- coding=utf-8 -*-

import socket
import threading
import time
import sys

def socket_service():
	try:
		#创建socket
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		#防止socket server重启后端口被使用
		s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		#绑定到特定的地址及端口上
		s.bind(('192.168.17.131',6666))
		#等待连接的最大数量为100
		s.listen(100)
	except socket.error as msg:
		print msg
		sys.exit(1)
	print 'Waiting connecting...'

	while 1:
		#接受一个新连接，将客户端传输的内容及客户端地址赋值给conn,addr
		conn,addr = s.accept()
		#创建新线程处理TCP连接
		t = threading.Thread(target=deal_data,args=(conn,addr))
		t.start()
def deal_data(conn,addr):
	print 'Accept new connection from {0}'.format(addr)
	conn.send('Welcome to the server!')
	while 1:
    #接收客户端传来的数据
		data = conn.recv(1024)
		print '{0} client send data is {1}'.format(addr,data)
		if data == 'exit' or not data:
			print '{0} connection close'.format(addr)
			conn.send('Connection close!')
			break
		conn.send('accept:{0}'.format(data))
	conn.close()

if __name__ == '__main__':
	socket_service()
