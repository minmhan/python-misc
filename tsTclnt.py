# -*- coding: utf-8 -*-
"""
Created on Sat Jul 16 14:30:04 2016

@author: minmhan
"""

from socket import *

HOST = 'localhost'
PORT = 21568
BUFSIZE = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)

while True:
    data = input('> ')
    if not data:
        break
    tcpCliSock.send(data.encode())
    data = tcpCliSock.recv(BUFSIZE)
    if not data:
        break
    print(data.decode('utf-8'))
    
tcpCliSock.close()
