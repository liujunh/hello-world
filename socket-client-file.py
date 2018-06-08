# -*- coding=utf-8 -*-

import socket
import sys
import os
import struct


def socket_client():
              try:
                            #创建socket
                            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                            #建立连接
                            s.connect(('192.168.17.131',6666))
              #检错
              except socket.error as msg:
                            print msg
                            sys.exit(1)
              #接收欢迎消息
              print s.recv(1024)
              #发送数据
              while 1:
							filepath = raw_input('please input file path:')
							if os.path.isfile(filepath):
								#定义文件信息及文件头信息：文件名及文件大小
								fileinfo_size = struct.calcsize('128sl')
								fheat = struct.pack('128sl' , os.path.basename(filepath) , os.stat(filepath).st_size)
								#将头文件信息传给服务端
								s.send(fheat)
								print 'client filepath:{0}'.format(filepath)
								#打开文件读数据，将文件内容赋给data
								fp = open(filepath,'rb')
								while 1:
									data = fp.read(1024)
									if not data:
										print '{0} file send over!'.format(filepath)
										break
									s.send(data)
							s.close()
							break
         

if __name__ == '__main__':
              socket_client()
