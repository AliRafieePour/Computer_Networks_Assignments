# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 14:38:14 2019

@author: Mah
"""
#CLIENT
import socket

s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

port = 1234
server = socket.gethostname()

s.connect((server, port))
while True:
    s.send(bytes(input(), "utf-8"))
    msg = s.recv(2048)
    print(msg.decode("utf-8"))