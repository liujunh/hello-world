#!/user/bin/env python
# -*- coding=utf-8 -*-

import socket
import threading
import time
import sys
import struct
import os

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
		#接受一个新连接
		sock,addr = s.accept()
		#创建新线程处理TCP连接
		t = threading.Thread(target=deal_data,args=(sock,addr))
		t.start()

def deal_data(sock,addr):
	print 'Accept new connection from {0}'.format(addr)
	sock.send('Welcome to the server!')
	while 1:
		#将文件信息放在buf中
		fileinfo_size = struct.calcsize('128sl')
		buf = sock.recv(fileinfo_size)
		if buf:
			#将字节流转换成python数据结构
			filename,filesize = struct.unpack('128sl',buf)
			#将解出的文件名去除字符\00
			fn = filename.strip('\00')
			#新文件的存储地址，文件名及其大小
			new_filename = os.path.join('./','new_' + fn)
			print 'accept file new name is: {0}, filesize is: {1}KB'.format(new_filename,filesize)

			recved_size = 0
			#创建空文件
			fp = open(new_filename,'wb')
			print 'Start receiving...'
			#判断接收文件与原有文件是否一样大，不是则继续接收，是则停止
			while not recved_size == filesize:
				if filesize - recved_size > 1024:
					data = sock.recv(1024)
					recved_size += len(data)
				else:
					data = sock.recv(filesize - recved_size)
					recved_size = filesize
				#将接收到的文件内容写入新空白文件中
				fp.write(data)
			fp.close()
			print 'receive end!'
		sock.close()
		break


if __name__  == '__main__':
	socket_service()
